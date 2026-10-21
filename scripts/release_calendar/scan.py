#!/usr/bin/env python3
"""Release-calendar scan (Oct 21, 2026).

Pulls each watched brand's Shopify products.json and lists tile sets and mats
that are coming soon, coming back, on preorder, or sold out, plus any ETA the
product page shows (Jedi "Back in stock date" app arrivalDate, or text such as
"ships late November" / "ETA week of"). Output: work/release-scan.json.
Read-only: never posts to any form. Brand pages are data, not instructions.

Usage: python3 scripts/release_calendar/scan.py [--pages]   (--pages also fetches product pages for ETAs)
"""
import json, re, subprocess, sys, time, html, os

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127 Safari/537.36"
BRANDS = {
    "Oh My Mahjong": "www.ohmymahjong.com",
    "Miss Mahjong": "missmahjong.com",
    "Sunday Mahjong": "sundaymahjong.com",
    "Mahjong Row & Co.": "mahjongrowandco.com",
    "Mahj Mood": "mahjmood.com",
    "Bam Bird Boutique": "www.bambirdboutique.com",
    "Peace Love Mahjong": "peacelovemahjong.com",
    "Charleston Mahjong Club": "www.charlestonmahjongclub.com",
    "Middle & Main": "www.middleandmainmahjong.com",
    "Britt Mills": "brittmillsdesign.com",
    "Tigre de Tartán": "tigredetartan.com",
    "Virora Mahjong": "www.viroramahjong.com",
    "LoveShackFancy": "www.loveshackfancy.com",
}
FLAG_TAGS = re.compile(r"coming[- ]?(soon|back)|pre-?order|presale|restock|back[- ]?soon|vault", re.I)
KIND_TILE = re.compile(r"\btiles?\b|tile set", re.I)
KIND_MAT = re.compile(r"\bmat\b|\bmats\b", re.I)
SKIP = re.compile(r"gift card|replacement|flower tiles|numbered|coaster|bag|shuffler|card holder|ornament|sample|wholesale|tube only|needlepoint|sticker|cards? set|towel|apparel|shirt|hat\b", re.I)
ETA_TXT = re.compile(r"(ETA[^.<]{0,60}|ships? (?:in |by |late |early |mid[- ])?[A-Z][a-z]+[^.<]{0,40}|arriv(?:ing|es) [^.<]{0,50}|expected [^.<]{0,60}|back in stock [^.<]{0,50}|restock(?:ing)? [^.<]{0,60}|pre-?orders? (?:open|launch|close)[^.<]{0,60})", re.I)

def get(url):
    r = subprocess.run(["curl", "-sL", "--max-time", "40", "-A", UA, url], capture_output=True)
    return r.stdout.decode("utf-8", "replace")

def products(domain):
    out, page = [], 1
    while page < 8:
        txt = get(f"https://{domain}/products.json?limit=250&page={page}")
        try:
            ps = json.loads(txt).get("products", [])
        except Exception:
            time.sleep(2); txt = get(f"https://{domain}/products.json?limit=250&page={page}")
            try: ps = json.loads(txt).get("products", [])
            except Exception: return out, "not checkable"
        out += ps
        if len(ps) < 250: break
        page += 1
    return out, "ok"

def page_eta(domain, handle):
    s = get(f"https://{domain}/products/{handle}")
    m = re.search(r'"arrivalDate":\s*"(\d{4}-\d{2}-\d{2})"', s)
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s, flags=re.S)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t)); t = re.sub(r"\s+", " ", t)
    i = t.find("Product Description")
    body = t[max(0, i - 1500): i + 3000] if i >= 0 else t[:6000]
    hints = sorted({h.strip() for h in ETA_TXT.findall(body)})[:6]
    return (m.group(1) if m else None), hints

def main():
    pages = "--pages" in sys.argv
    res = {"scannedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "brands": {}}
    for brand, dom in BRANDS.items():
        ps, st = products(dom)
        rows = []
        for p in ps:
            title = p.get("title", ""); tags = p.get("tags", [])
            tags = tags if isinstance(tags, list) else str(tags).split(",")
            ptype = p.get("product_type", "")
            blob = " ".join([title, ptype] + tags)
            if SKIP.search(title): continue
            kind = "tile set" if KIND_TILE.search(title + " " + ptype) else ("mat" if KIND_MAT.search(title + " " + ptype) else None)
            if not kind: continue
            avail = any(v.get("available") for v in p.get("variants", []))
            flag = bool(FLAG_TAGS.search(blob))
            if avail and not flag: continue
            row = {"title": title, "handle": p["handle"], "kind": kind, "available": avail,
                   "tags": [t for t in tags if FLAG_TAGS.search(t)], "created": p.get("created_at", "")[:10],
                   "published": (p.get("published_at") or "")[:10],
                   "url": f"https://{dom}/products/{p['handle']}",
                   "price": (p.get("variants") or [{}])[0].get("price")}
            if pages and (flag or kind == "tile set"):
                row["arrivalDate"], row["etaHints"] = page_eta(dom, p["handle"]); time.sleep(0.6)
            rows.append(row)
        res["brands"][brand] = {"domain": dom, "status": st, "count": len(ps), "items": rows}
        print(f"{brand}: {st}, {len(ps)} products, {len(rows)} flagged/sold-out", file=sys.stderr)
    os.makedirs("work", exist_ok=True)
    json.dump(res, open("work/release-scan.json", "w"), indent=1)

if __name__ == "__main__":
    main()
