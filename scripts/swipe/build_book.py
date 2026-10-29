#!/usr/bin/env python3
"""Build a tile-set (or mat) swipe book the one approved way.

Rules (Tiffany, Oct 14-15; project doc 51):
  1. Mat pool = the vetted Find Your Match catalog ONLY (isolated flat mat photos).
     Color pull (Oct 19): rank candidates with scripts/colors/matcolors.pull_score(key, set_colors, set_tone):
     Tiffany's Mat Color Tagger tags (config/mat-color-overrides.json) win, primary weighted over accents,
     set_tone = the TILE tone from config/tile-tones.json (matcolors.tile_tone(name)): clean tile -> clean/pastel/blend
     mats, earthy tile -> earthy/blend, transitional -> all with blend first; clean-on-earthy is a hard 0 (doc 76).
     Skipped mats are never pulled.
     TIGHT (Oct 19 3:03am): use matcolors.pull(set_name, match_pool_keys): the mat's PRIMARY must be one of the set's own
     colors (matcolors.tile_colors: dominant + analogous neighbor only for true in-betweens); accents only rank; capped at 60.
     Never raw store feeds, never album-card crops (alb:*), never graphics.
  2. Auto-excluded: holiday mats, travel/mini mats, starter kits, bundles, caddies,
     desk mats, table covers, foldable tables, solo-play mats, pool mats, logo mats.
  3. Every mat image is the brand's FULL-RES flat photo (the same shot the catalog
     vetted, matched by similarity), trimmed to the mat edge (no white margin),
     saved as its own file m/<n>.jpg at up to 1600px. No data URIs, no 288/520px.
  4. Tile pile = the album tile shot from assets/tiles/album/ (never a product photo).
  6. GATE (Oct 29): scripts/swipe/book_gate.py must pass (colour card, TNT recs first, FYM photos, no holiday/hidden/
     skip/Mahjong Studios/Splash, widest pool: spec "pool_src":"fym-full-measured","pool_n":<ranked>). Failing books
     are renamed index.BLOCKED.html.
  5. Card = the holiday-studio card: mat fills the card, pile inset lower right,
     zoom scales mat + pile together. Done button via finish_patch.py.

Usage:
  python3 -I build_book.py <spec.json> <outdir>
spec: {"title","col","mode":"tile","listTitle",
       "group":{"id","label","sub","pile":"<repo path>"},
       "items":[{"id","key":"<fym key domain/handle>","label"?}],   # order = deck order
       "fym_mats":"<path to FYM mats json>", "fym_ref":"<dir of mc/*.json>",
       "template":"<template html with __DATA__>"}
"""
import json, os, re, sys, io, base64, glob, urllib.request
from PIL import Image, ImageChops, ImageStat

EXCL = re.compile(r"travel|\bmini\b|mini-|starter|\bkit\b|bundle|caddy|desk mat|desk\b|table cover|"
                  r"foldable|solo play|\bpool\b|logo mat|art print|\btube only|\bbag\b|pet mat|bath mat", re.I)
HOLIDAY = re.compile(r"christmas|xmas|holly|yuletide|merriment|winterberry|nutcracker|sugarplum|\bclara\b|santa|noel|jingle|"
                     r"candy cane|\bcane mat|winter wonderland|mistletoe|reindeer|snowflake|halloween|o-ween|\bween\b|spooky|pumpkin|witch|valentine|easter|hanukkah", re.I)
UA = {"User-Agent": "Mozilla/5.0"}


def excluded(m, key):
    txt = " ".join([m.get("n", ""), key])
    t = txt.replace("-", " ")
    return bool(m.get("hol")) or bool(EXCL.search(t)) or bool(HOLIDAY.search(t))


def get(url, timeout=25):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()


def product_images(url):
    base = url.split("?")[0].rstrip("/")
    try:
        j = json.loads(get(base + ".json"))
        return [i["src"] for i in j["product"]["images"]]
    except Exception:
        return []


def sized(src, w=1600):
    # Shopify CDN: ask for a 1600px rendition
    s = src.split("?")[0]
    return s + ("?" if "?" not in s else "&") + f"width={w}"


def sig(im):
    im = im.convert("RGB").copy()
    im = trim(im, pad=0)
    return im.resize((24, 24))


def dist(a, b):
    d = ImageChops.difference(a, b)
    return sum(ImageStat.Stat(d).mean)


def trim(im, pad=0.006, tol=28):
    """Crop away uniform background margins (white or any flat border color)."""
    rgb = im.convert("RGB")
    w, h = rgb.size
    corners = [rgb.getpixel(p) for p in [(1, 1), (w - 2, 1), (1, h - 2), (w - 2, h - 2)]]
    bg = tuple(sorted(c[i] for c in corners)[1] for i in range(3))
    diff = ImageChops.difference(rgb, Image.new("RGB", rgb.size, bg)).convert("L")
    mask = diff.point(lambda v: 255 if v > tol else 0)
    box = mask.getbbox()
    if not box:
        return rgb
    x0, y0, x1, y1 = box
    # ignore crops that would remove almost nothing or almost everything
    if (x1 - x0) * (y1 - y0) < 0.25 * w * h:
        return rgb
    px, py = int(w * pad), int(h * pad)
    return rgb.crop((max(0, x0 - px), max(0, y0 - py), min(w, x1 + px), min(h, y1 + py)))


def load_refs(ref_dir):
    R = {}
    for f in glob.glob(os.path.join(ref_dir, "*.json")):
        R.update(json.load(open(f)))
    return R


def b64img(u):
    return Image.open(io.BytesIO(base64.b64decode(u.split(",", 1)[1])))


def best_photo(m, ref):
    """Full-res version of the vetted catalog photo, or None."""
    srcs = product_images(m.get("u", ""))
    if not srcs:
        return None, "no product feed"
    rs = sig(ref) if ref is not None else None
    best = None
    for s in srcs[:10]:
        try:
            im = Image.open(io.BytesIO(get(sized(s, 400))))
        except Exception:
            continue
        d = dist(sig(im), rs) if rs is not None else 0
        if best is None or d < best[0]:
            best = (d, s)
        if rs is None:
            break
    if not best:
        return None, "images unreachable"
    if rs is not None and best[0] > 60:
        return None, f"no close match in feed ({best[0]:.0f})"
    return Image.open(io.BytesIO(get(sized(best[1], 1600)))), f"feed match {best[0]:.0f}"


def main(spec_path, out):
    S = json.load(open(spec_path))
    M = json.load(open(S["fym_mats"]))
    R = load_refs(S["fym_ref"])
    # photo fixes + pool additions shared by every book (photo_overrides.json, Oct 18)
    OV = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "photo_overrides.json")))
    REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
    OVF = {k: os.path.join(REPO, v["file"]) for k, v in {**OV.get("fix", {}), **OV.get("add", {})}.items()}
    for k, v in OV.get("add", {}).items():
        M.setdefault(k, dict(v["entry"]))
    os.makedirs(out + "/m", exist_ok=True)
    os.makedirs(out + "/t", exist_ok=True)
    rep, items = [], []
    for n, it in enumerate(S["items"]):
        if it.get("file"):  # hand-kept clean photo (retired OMM mats, Squarespace brands, her cutouts)
            im = trim(Image.open(it["file"]).convert("RGB")); im.thumbnail((1600, 1600))
            fn = f"m/{n}.jpg"; im.save(os.path.join(out, fn), "JPEG", quality=86)
            items.append({"id": it["id"], "label": it["label"], "img": fn, "url": it.get("url", ""), "w": im.width, "h": im.height, "key": it.get("key"), "ph": "canon-override"})
            rep.append((it["id"], f"OK file {im.width}x{im.height}")); continue
        key = it["key"]
        m = M.get(key)
        if key in OVF and m and not excluded(m, key):
            im = trim(Image.open(OVF[key]).convert("RGB")); im.thumbnail((1600, 1600))
            fn = f"m/{n}.jpg"; im.save(os.path.join(out, fn), "JPEG", quality=86)
            items.append({"id": it["id"], "label": it.get("label") or f"{m['n']} · {m['bn']}", "img": fn,
                          "url": m.get("u", ""), "w": im.width, "h": im.height, "key": key, "ph": "canon-override"})
            rep.append((it["id"], f"OK override file {im.width}x{im.height}")); continue
        if not m or key.startswith("alb:"):
            rep.append((it["id"], "SKIP not in vetted catalog"));
            continue
        if it["id"] in set(S.get("drop", [])):
            rep.append((it["id"], "SKIP failed visual check (not a flat isolated mat photo)")); continue
        if excluded(m, key):
            rep.append((it["id"], "SKIP rule (holiday/travel/mini/kit/etc)"));
            continue
        ref = b64img(R[m["f"]]) if m.get("f") in R else None
        if ref is not None and ref.mode in ("RGBA", "LA", "P"):
            r = ref.convert("RGBA"); bg = Image.new("RGB", r.size, "white"); bg.paste(r, mask=r.split()[3]); ref = bg
        im, how = best_photo(m, ref)
        if im is None and ref is not None:
            # last resort: the catalog's own (smaller) image; flagged in the report
            im, how = ref, "LOWRES catalog image (" + how + ")"
        if im is None:
            rep.append((it["id"], "SKIP no photo")); continue
        im = trim(im)
        im.thumbnail((1600, 1600))
        fn = f"m/{n}.jpg"
        im.convert("RGB").save(os.path.join(out, fn), "JPEG", quality=86)
        items.append({"id": it["id"], "label": it.get("label") or f"{m['n']} · {m['bn']}", "img": fn,
                      "url": m.get("u", ""), "w": im.width, "h": im.height, "key": key,
                      "ph": "fym" if how.startswith("LOWRES") else "fym-hires"})
        rep.append((it["id"], f"OK {how} {im.width}x{im.height}"))
    # pool for "+ Try another mat": the rest of the vetted catalog (catalog-size images, lazy-loaded)
    os.makedirs(out + "/p", exist_ok=True)
    have = {x["id"] for x in items}
    pool = []
    for n, it in enumerate(S.get("pool", [])):
        m = M.get(it["key"])
        if not m or it["id"] in have or excluded(m, it["key"]): continue
        if it["key"] in OVF:
            im = Image.open(OVF[it["key"]]).convert("RGB"); im.thumbnail((520, 520))
        elif m.get("f") in R:
            im = b64img(R[m["f"]])
        else:
            continue
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA"); bg = Image.new("RGB", im.size, "white"); bg.paste(im, mask=im.split()[3]); im = bg
        im = trim(im.convert("RGB")); fn = f"p/{n}.jpg"; im.save(os.path.join(out, fn), "JPEG", quality=82)
        pool.append({"id": it["id"], "label": f"{m['n']} · {m['bn']}", "img": fn, "url": m.get("u", "")})
    g = S["group"]
    pile = Image.open(g["pile"]).convert("RGB")
    pile.thumbnail((1400, 1400))
    pile.save(out + "/t/pile.jpg", "JPEG", quality=90)
    D = {"col": S["col"], "mode": S.get("mode", "tile"), "listTitle": S["listTitle"],
         "groups": [{"id": g["id"], "label": g["label"], "sub": g["sub"], "img": "t/pile.jpg", "thumb": "t/pile.jpg"}],
         "items": items + pool, "order": {g["id"]: [x["id"] for x in items]}, "pileShadow": True,
         "pool": {"src": S.get("pool_src", ""), "n": S.get("pool_n", 0)}}  # book_gate [e]: widest pool only
    tpl = open(S["template"]).read()
    html = tpl.replace("__DATA__", json.dumps(D, ensure_ascii=False))
    html = re.sub(r"<title>.*?</title>", f"<title>{S['title']}</title>", html, count=1)
    # "+ Try another mat" sheet: lazy images + a search box (Tiffany, Oct 15: she must be able to pull in mats she thinks of)
    html = html.replace("const im=document.createElement('img');im.src=x.img;", "const im=document.createElement('img');im.loading='lazy';im.src=x.img;")
    html = html.replace("$('shT').textContent='Add another mat (all moody, classic and neutral mats)';",
        "$('shT').textContent='Add another mat';{const q=document.createElement('input');q.placeholder='Search mats or brands…';q.style.cssText='grid-column:1/-1;font:inherit;font-size:16px;padding:10px 12px;border-radius:10px;border:0';q.oninput=()=>{const t=q.value.toLowerCase();[...B.querySelectorAll('button.it')].forEach(b=>b.style.display=b.textContent.toLowerCase().includes(t)?'':'none')};B.append(q);setTimeout(()=>q.focus(),50)}")
    open(out + "/index.html", "w").write(html)
    # Tiffany Oct 28: Bam Bird + Virora (and Heritage/Sunday/etc.) always use the canonical FYM photos
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from canon_tiles import fix_book
    fix_book(out + "/index.html")
    json.dump(rep, open(out + "/report.json", "w"), indent=0)
    # Oct 29 (Tiffany 12:35pm): the rules are enforced here. A failing book is not written as index.html.
    import subprocess
    g_ = subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "book_gate.py"), out + "/index.html"])
    if g_.returncode != 0:
        os.replace(out + "/index.html", out + "/index.BLOCKED.html")
        sys.exit("book_gate.py FAILED: book left as index.BLOCKED.html, do not publish")
    ok = sum(1 for _, r in rep if r.startswith("OK"))
    print(f"{ok} mats in book, {len(rep) - ok} skipped")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
