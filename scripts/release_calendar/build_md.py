#!/usr/bin/env python3
"""Render docs/release-calendar.md from config/release-calendar.json.
Usage: python3 scripts/release_calendar/build_md.py [YYYY-MM-DD]  (default: today)"""
import json, sys, datetime as dt
c = json.load(open("config/release-calendar.json"))
today = dt.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else dt.date.today()
end = today + dt.timedelta(weeks=8)
def d(s):
    try: return dt.date.fromisoformat(str(s)[:10])
    except Exception: return None
def when(i):
    if i.get("date"): return str(i["date"])[:16].replace("T", " ")
    return i.get("window", "")
def key(i):
    return d(i.get("contentWindowStart")) or d(i.get("date")) or d(i.get("windowStart")) or dt.date(2099, 1, 1)
def yn(v): return "yes" if v else "no"
def alb(v): return v if isinstance(v, str) else yn(v)
L = [f"# Mahj Matchmaker release calendar", "",
     f"Updated {c['updated']} from brand sites, the Sunday release schedule, brand Instagram feeds (Planoly) and Gmail. Source of truth: `config/release-calendar.json`; regenerate with `python3 scripts/release_calendar/build_md.py`.", "",
     "**Rule (Tiffany, Oct 21):** save restock content for the buying window. Don't spend a set's content before you can buy it; post 1-2 weeks before a dated restock so people pick their mat and have the code ready when it drops.", ""]
L += [f"## Next 8 weeks ({today:%b %d} - {end:%b %d})", "", "| Post window | Brand | Product | Drop date / window | Album | Affiliate | What to post |", "|---|---|---|---|---|---|---|"]
for i in sorted(c["items"], key=key):
    k = key(i); de = d(i.get("contentWindowEnd")) or d(i.get("windowEnd")) or k
    if k > end or (de and de < today): continue
    pw = i.get("contentWindowStart") or (str(i.get("date"))[:10] if i.get("date") else i.get("windowStart", ""))
    if i.get("contentWindowEnd"): pw += f" to {i['contentWindowEnd']}"
    L.append(f"| {pw} | {i['brand']} | {i['product']} | {when(i)} | {alb(i.get('album'))} | {yn(i.get('affiliate'))} | {i.get('contentTiming','')} |")
L += ["", "## Held content: restocks with no date yet (do not post until dated)", ""]
for i in c["items"]:
    if not (i.get("date") or i.get("windowStart")) and i.get("album") and i.get("type") in ("restock", "re-release"):
        L.append(f"- **{i['brand']} {i['product']}** ({alb(i['album'])}): {i.get('window','')}. [source]({i.get('sourceUrl','')})")
L += ["", "## Everything we're tracking", "", "| Brand | Product | Type | Date / window | Album | Affiliate | Content timing | Source |", "|---|---|---|---|---|---|---|---|"]
for i in sorted(c["items"], key=lambda x: (x["brand"], key(x))):
    src = f"[{i.get('source','link')[:60]}]({i['sourceUrl']})" if i.get("sourceUrl") else i.get("source", "")
    L.append(f"| {i['brand']} | {i['product']} | {i['type']} | {when(i)} | {alb(i.get('album'))} | {yn(i.get('affiliate'))} | {i.get('contentTiming','')} | {src} |")
L += ["", "## Content timing rules", ""] + [f"- **{k.replace('_',' ')}**: {v}" for k, v in c["rules"]["timing"].items()]
n = c.get("newsletters", {})
if n:
    L += ["", f"## Brand newsletters ({n.get('checked','')})", "", "Receiving:"] + [f"- {r['brand']}: {r['from']} ({r['kind']})" for r in n["receiving"]]
    L += ["", "Not receiving (sign-up needs Tiffany's OK; nothing was signed up):"] + [f"- {g['brand']}: {g['signup']}" for g in n["gaps"]]
    L += ["", n.get("note", "")]
open("docs/release-calendar.md", "w").write("\n".join(L) + "\n")
print("wrote docs/release-calendar.md")
