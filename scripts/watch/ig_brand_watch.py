#!/usr/bin/env python3
"""Instagram brand watch (Pillar 2, Nov 6 2026).

The posts are fetched by Claude with the Planoly MCP tool
`get_instagram_account_posts` (workspace 019fc27c-0bef-7533-bc3f-030acc19a135,
which reads any PUBLIC business/creator account). There is no API key for this
in the repo, so the fetch step is done by the agent; this script does the rest.

Usage
  # 1) save each account's posts (full MCP JSON, or compact records) to a file in
  #    config/ig-watch-raw/ (compact record: {h,id,ts,url,cap,kids?})
  # 2) run:
  python3 scripts/watch/ig_brand_watch.py [--days 10] [--raw config/ig-watch-raw]

  Outputs
  - config/ig-watch-snapshot.json : every post id seen (so later runs only flag NEW posts)
  - docs/status/mahj-watch.json   : one merged feed (IG + store watcher docs/status/partner-launches.json)
  - docs/status/mahj-watch.md     : this week's launches / restocks / preorders / sales / coming soon
  Prints the NEW IG items (not in the previous snapshot) as JSON lines for the caller.

Classification is keyword-based on the FULL caption (carousel captions are one caption;
the agent must still read carousel slides when drafting content, see CLAUDE.md READ THE WHOLE POST).
"""
import argparse, csv, glob, json, os, re, sys
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = lambda *a: os.path.join(ROOT, *a)

EXCLUDE = {"mahjongrowandco"}          # Mahjong Row & Co. out (Nov 6)
NEVER_NAME = {"tigre_de_tartan"}       # TdT: never typed in group posts (image only)
NEVER_SOCIAL = {"ymimports"}           # YMI never featured on social

KINDS = [  # order = priority when several match
    ("sale",      r"\b(\d+% ?off|flash sale|sale\b|code [A-Z0-9]{3,}|\$\d+ tiles|now just \$)"),
    ("restock",   r"(restock|back in stock|is back|are back|they.re back|returns? this|making its return|second chance|has returned|back\b.*\bstock)"),
    ("preorder",  r"(pre-?order|preorder)"),
    ("drop date", r"(drop(s|ping)? (tomorrow|today|\d|on|this)|launch(es|ing)? (on|november|\d|tomorrow|this)|available (tomorrow|\d{1,2}/\d|november|nov\.? \d)|goes live|opens? (for )?(public )?pre|releases? (this|on|monday|tuesday|wednesday|thursday|friday)|arrives? (sunday|monday|\d)|coming (soon|this november|any day)|sneak peek|stay tuned|on the way|in production)"),
    ("launch",    r"(new drop|introducing|meet (our|the|juniper)|just dropped|is live|are live|officially (here|available|live|open)|now available|available now|new (racks|mat|mats|tiles|collection|designs)|ready (for shopping|to ship))"),
    ("collab",    r"(collab|collaboration| x [A-Z]|teamed up)"),
]
PRODUCT_WORDS = [("tiles", r"\btiles?\b|tile set"), ("mat", r"\bmats?\b"), ("rack", r"\bracks?\b"),
                 ("travel", r"travel"), ("bag", r"\bbags?\b|tote"), ("card", r"card\b")]


def classify(cap):
    c = cap or ""
    kinds = [k for k, rx in KINDS if re.search(rx, c, re.I)]
    prods = [p for p, rx in PRODUCT_WORDS if re.search(rx, c, re.I)]
    dates = re.findall(r"\b(?:\d{1,2}/\d{1,2}|(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.? \d{1,2}(?:st|nd|rd|th)?|tomorrow|today|this (?:friday|saturday|sunday|monday|tuesday|wednesday|thursday)|(?:january|february) 20\d\d)\b", c, re.I)
    return (kinds[0] if kinds else "other"), kinds, prods, sorted(set(d.strip() for d in dates))


def load_brand_maps():
    handles = json.load(open(P("config/social/ig-handles.json")))
    h2b = {v.lower(): k for k, v in handles.items() if not k.startswith("_") and isinstance(v, str)}
    partners = set()
    try:
        for r in csv.DictReader(open(P("config/partner-brand-contacts.csv"))):
            partners.add(r["brand"].split("(")[0].strip().lower())
    except FileNotFoundError:
        pass
    np = {}
    try:
        for b in json.load(open(P("config/watch-major-nonpartners.json")))["brands"]:
            if b.get("handle"):
                np[b["handle"].lower()] = b["brand"]
    except FileNotFoundError:
        pass
    return h2b, partners, np


def is_partner(brand, partners):
    b = brand.lower()
    return any(b.startswith(p[:8]) or p.startswith(b[:8]) for p in partners)


def read_raw(rawdir):
    posts = []
    for f in sorted(glob.glob(os.path.join(rawdir, "*.json"))):
        d = json.load(open(f))
        if isinstance(d, dict) and "posts" in d:  # full MCP response
            for p in d["posts"]:
                posts.append({"h": d["username"], "id": p["id"], "ts": p["timestamp"], "url": p.get("permalink"),
                              "cap": p.get("caption") or "", "kids": len(p.get("children") or [])})
        elif isinstance(d, list):
            posts.extend(d)
    return posts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw", default=P("config/ig-watch-raw"))
    ap.add_argument("--days", type=int, default=10)
    ap.add_argument("--now", default=None)
    a = ap.parse_args()
    now = datetime.fromisoformat(a.now) if a.now else datetime.now(timezone.utc)
    cutoff = now - timedelta(days=a.days)

    h2b, partners, np = load_brand_maps()
    snap_path = P("config/ig-watch-snapshot.json")
    snap = json.load(open(snap_path)) if os.path.exists(snap_path) else {"seen": {}, "first_run": now.isoformat()}

    items, new = [], []
    for p in read_raw(a.raw):
        h = p["h"].lower()
        if h in EXCLUDE:
            continue
        ts = datetime.fromisoformat(p["ts"].replace("Z", "+00:00").replace("+0000", "+00:00"))
        brand = h2b.get(h) or np.get(h) or h
        # every handle in ig-handles.json is a partner unless listed in watch-major-nonpartners.json
        partner = h not in np
        kind, kinds, prods, dates = classify(p.get("cap", ""))
        it = {"src": "instagram", "brand": brand, "handle": h, "partner": partner, "kind": kind, "kinds": kinds,
              "products": prods, "dates": dates, "posted": ts.date().isoformat(), "url": p.get("url"),
              "caption": (p.get("cap") or "")[:400], "slides": p.get("kids", 0),
              "never_name": h in NEVER_NAME, "never_social": h in NEVER_SOCIAL}
        is_new = p["id"] not in snap["seen"]
        snap["seen"].setdefault(p["id"], {"h": h, "ts": p["ts"], "kind": kind})
        if ts >= cutoff and kind != "other":
            items.append(it)
            if is_new:
                new.append(it)

    # merge store watcher
    store = []
    try:
        pl = json.load(open(P("docs/status/partner-launches.json")))
        for r in pl.get("recent", []) + pl.get("events", []):
            if (r.get("when") or "") >= cutoff.date().isoformat():
                store.append({"src": "store", "brand": r.get("brand"), "partner": True, "kind": {"recent": "launch", "restock": "restock", "preorder": "preorder", "price": "sale"}.get(r.get("ev"), r.get("ev")),
                              "products": [r.get("kind")], "posted": r.get("when"), "url": r.get("url"), "caption": r.get("title"),
                              "preorder": r.get("pre"), "available": r.get("avail")})
    except FileNotFoundError:
        pass

    snap["last_run"] = now.isoformat()
    json.dump(snap, open(snap_path, "w"), indent=1)
    feed = {"run_at": now.isoformat(), "days": a.days, "instagram": sorted(items, key=lambda x: x["posted"], reverse=True),
            "store": sorted(store, key=lambda x: x["posted"] or "", reverse=True)}
    json.dump(feed, open(P("docs/status/mahj-watch.json"), "w"), indent=1, ensure_ascii=False)

    order = ["drop date", "launch", "restock", "preorder", "sale", "collab"]
    L = [f"# Mahj Watch: what's new across brands (last {a.days} days, run {now:%b %d %H:%M} UTC)", "",
         "Instagram (partner first). Store-watcher lines: docs/status/partner-launches.md.", ""]
    for k in order:
        rows = [i for i in items if i["kind"] == k]
        if not rows:
            continue
        L.append(f"## {k.title()}")
        for i in sorted(rows, key=lambda x: (not x["partner"], x["posted"]), reverse=False):
            tag = "partner" if i["partner"] else "non-partner"
            flag = " (image-only brand: never type its name)" if i["never_name"] else ""
            d = f" · dates: {', '.join(i['dates'])}" if i["dates"] else ""
            L.append(f"- **{i['brand']}** [{tag}]{flag} · {i['posted']}{d} · {i['caption'][:160].replace(chr(10), ' ')} · {i['url']}")
        L.append("")
    L.append(f"Store watcher items in window: {len(store)}")
    open(P("docs/status/mahj-watch.md"), "w").write("\n".join(L) + "\n")
    for n in new:
        print(json.dumps({k: n[k] for k in ("brand", "partner", "kind", "posted", "dates", "url")}, ensure_ascii=False))
    print(f"# {len(items)} classified IG items in window, {len(new)} new vs snapshot, {len(store)} store items", file=sys.stderr)


if __name__ == "__main__":
    main()
