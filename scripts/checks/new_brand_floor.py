#!/usr/bin/env python3
"""NEW BRAND FLOOR CHECK (Tiffany Nov 23 2026: Spools + Brewtifully were approved Nov 18-19 and had no page on Nov 23:
"that's dropping money on the floor... we need a safety check against this stuff").
For every brand in config/partners-pipeline.json with approved: true, checks the LIVE site:
  page  = https://www.mahjmatchmaker.com/<slug>-discount-code answers 200
  hub   = the brand is named on /mahjong-discount-codes
Prints one line per brand that is approved and NOT finished, with the days it has sat. Exit 1 if any brand has sat 2+ days.
This is the only alarm for this: it prints nothing when all is done, so it is never 'always red' (partner_checklist shows
45 of 45 gaps for newsletters, which is why nobody saw the real one)."""
import json, re, sys, datetime, urllib.request
UA = {"User-Agent": "Mozilla/5.0"}
def get(u):
    try:
        with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=25) as r:
            return r.status, r.read().decode("utf-8", "ignore")
    except Exception as e:
        return getattr(e, "code", 0), ""
SLUG = {"Averill": "averill-mahjong", "Spools": "spools", "Brewtifully": "brewtifully"}
def slug(b):
    return SLUG.get(b) or re.sub(r"[^a-z0-9]+", "-", b.lower().replace("&", "and").replace("+", "and")).strip("-")
d = json.load(open("config/partners-pipeline.json"))
_, hub = get("https://www.mahjmatchmaker.com/mahjong-discount-codes")
today = datetime.date.today(); bad = 0
for r in d.get("brands", []):
    if not r.get("approved"): continue
    b = r["brand"]; code = None; s = r.get("slug") or slug(b)
    for cand in (s + "-discount-code", s + "-mahjong-discount-code", s + "-code"):
        code, _t = get("https://www.mahjmatchmaker.com/" + cand)
        if code == 200: break
    on_hub = b.lower() in hub.lower()
    if code == 200 and on_hub: continue
    try: days = (today - datetime.date.fromisoformat(str(r.get("approvedAt"))[:10])).days
    except Exception: days = "?"
    print(f"NEW BRAND NOT FINISHED: {b} | approved {r.get('approvedAt')} ({days} days) | page {'LIVE' if code==200 else 'MISSING'} | codes page {'yes' if on_hub else 'NO'}")
    if days == "?" or days >= 2: bad = 1
sys.exit(bad)
