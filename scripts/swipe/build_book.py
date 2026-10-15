#!/usr/bin/env python3
"""Build a tile-set (or mat) swipe book the one approved way.

Rules (Tiffany, Oct 14-15; project doc 51):
  1. Mat pool = the vetted Find Your Match catalog ONLY (isolated flat mat photos).
     Never raw store feeds, never album-card crops (alb:*), never graphics.
  2. Auto-excluded: holiday mats, travel/mini mats, starter kits, bundles, caddies,
     desk mats, table covers, foldable tables, solo-play mats, pool mats, logo mats.
  3. Every mat image is the brand's FULL-RES flat photo (the same shot the catalog
     vetted, matched by similarity), trimmed to the mat edge (no white margin),
     saved as its own file m/<n>.jpg at up to 1600px. No data URIs, no 288/520px.
  4. Tile pile = the album tile shot from assets/tiles/album/ (never a product photo).
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
HOLIDAY = re.compile(r"christmas|xmas|holly|yuletide|merriment|nutcracker|sugarplum|\bclara\b|santa|noel|jingle|"
                     r"candy cane|\bcane mat|winter wonderland|mistletoe|reindeer|snowflake|halloween|spooky|valentine|easter|hanukkah", re.I)
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
    os.makedirs(out + "/m", exist_ok=True)
    os.makedirs(out + "/t", exist_ok=True)
    rep, items = [], []
    for n, it in enumerate(S["items"]):
        key = it["key"]
        m = M.get(key)
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
                      "url": m.get("u", ""), "w": im.width, "h": im.height})
        rep.append((it["id"], f"OK {how} {im.width}x{im.height}"))
    g = S["group"]
    pile = Image.open(g["pile"]).convert("RGB")
    pile.thumbnail((1400, 1400))
    pile.save(out + "/t/pile.jpg", "JPEG", quality=90)
    D = {"col": S["col"], "mode": S.get("mode", "tile"), "listTitle": S["listTitle"],
         "groups": [{"id": g["id"], "label": g["label"], "sub": g["sub"], "img": "t/pile.jpg", "thumb": "t/pile.jpg"}],
         "items": items, "order": {g["id"]: [x["id"] for x in items]}, "pileShadow": True}
    tpl = open(S["template"]).read()
    html = tpl.replace("__DATA__", json.dumps(D, ensure_ascii=False))
    html = re.sub(r"<title>.*?</title>", f"<title>{S['title']}</title>", html, count=1)
    open(out + "/index.html", "w").write(html)
    json.dump(rep, open(out + "/report.json", "w"), indent=0)
    ok = sum(1 for _, r in rep if r.startswith("OK"))
    print(f"{ok} mats in book, {len(rep) - ok} skipped")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
