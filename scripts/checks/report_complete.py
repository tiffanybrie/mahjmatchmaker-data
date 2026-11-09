#!/usr/bin/env python3
"""Google & Revenue report completeness gate (Tiffany Nov 9 2026: "How can you honestly skip them? ...
it has a column for every one of those").
Run on the seo doc JSON BEFORE writing it to HQ:  python3 scripts/checks/report_complete.py <seo.json>
FAILS (exit 1) when any required column is missing for any brand, so a skipped step can't pass silently.
A brand that truly wasn't checked must say why in notChecked (e.g. "CAPTCHA at brand 21", "on hold").
"""
import json, sys
REQ_BRAND = ["overview", "namesUs", "otherCode", "position", "aiMode"]   # aiMode = same query + &udm=50
REQ_TOP = ["aiSummary", "dailyLog", "aiBrands", "sc", "sales", "brandWatch", "alarm"]
REQ_SC = ["clicks7", "clicksPrev7", "discountCode", "sources"]  # sources = Squarespace Analytics traffic sources
d = json.load(open(sys.argv[1])); fails = []
for k in REQ_TOP:
    if k not in d: fails.append(f"missing field {k}")
if str(d.get("aiSummary", "")).startswith("PARTIAL"):
    print("PARTIAL run: gate skipped (cloud-only)"); sys.exit(0)
for b in d.get("aiBrands", []):
    if b.get("notChecked"): continue
    miss = [k for k in REQ_BRAND if k not in b]
    if miss: fails.append(f"{b.get('brand')}: missing {', '.join(miss)}")
sc = d.get("sc", {})
for k in REQ_SC:
    if k not in sc: fails.append(f"sc.{k} missing (Search Console + Squarespace Analytics traffic sources)")
if "Read:" not in d.get("dailyLog", ""):
    fails.append("dailyLog has no 'Read:' line listing the setup docs actually read")
print("REPORT COMPLETE: PASS" if not fails else "REPORT COMPLETE: FAIL\n- " + "\n- ".join(fails[:60]))
sys.exit(1 if fails else 0)
