# REVENUE WATCH: every brand's sales, every day (Tiffany Nov 4 2026, STANDING)

Her words (Nov 4 ~2pm): "You've got to look at brands' sales performance as well - that CANNOT be ignored...
I can't be the brain here... YOU have to be that brain." "We were winning on codes across a handful of key
brands. So if one of those brands falls off, it's a really big deal."

## Why this exists (what went wrong)
- Oct 31 the report SAW Mahj Mood go 3 orders → 0 while Google still named MAHJMATCH, wrote "check GoAffPro at
  tonight's close-out", and nobody did. No alert reached her. She found it herself Nov 4.
- The only sales alarm compared yesterday to the 7-day average. A falling week drags the average down with it,
  so a 51% weekly drop (148 orders / $3,388 → 84 / $1,661) never tripped it.
- "Our code shows in Google" was treated as "fine". It isn't: code named + sales gone = something ELSE is wrong.

## The daily check (morning report runs it; any chat can run it)
1. Export HQ money docs: ArtifactData list collection `money` out_dir `<tmp>`; then
   `python3 scripts/money/brand_watch.py <tmp> --date <yesterday>`.
2. TOTAL alarms: 7-day commission < 80% of the week before, < 80% of the 4-week weekly average,
   or < 60% of the best week. Compare WEEKS, not yesterday vs a sliding average.
3. BRAND alarms (any one): orders this week < 50% of its 4-week weekly rate (brands averaging ≥2/week);
   < 50% of last week (≥3 last week); no order for ≥ max(3, 2.5× its normal gap) days;
   commission < 50% of its weekly baseline (≥$40/week) or of last week (≥$60).
4. EVERY brand alarm gets an investigation the same day, written as "<brand>: down X%. Likely because ___.
   Checked: ___. Doing: ___." Never just "code is populating". Checklist, in order:
   a. DATA FIRST: is the drop real or a reading gap? Only TWO dashboards are ever read: GoAffPro and the
      UpPromote Marketplace (Tiffany Nov 8 1:17pm; never try a brand's own dashboard/portal). Every other brand's
      orders come from order emails: logged on the money tab with amount "?" so she screenshots them (Nov 8 1:20pm).
      Brands with "?" amounts are compared by ORDER COUNT. No email and no dashboard row = "unknown", not "zero".
   b. GOOGLE: AI answer still names MAHJMATCH? which other code does it show now? our organic position;
      page last crawled; Search Console clicks for "<brand> discount code" this week vs last.
   c. CODE: still applies at checkout (cart test, never check out); same % as our page says.
   d. THE BRAND ITSELF: own sale/friends-and-family code (site banner, IG posts + stories, email),
      a launch that ended, best-sellers or the hot drop SOLD OUT (products.json `available`), preorder-only,
      shipping cutoff, site down, price change.
   e. ATTRIBUTION: affiliate account still approved; code still assigned; ref link works; GoAffPro "Hide zero
      earnings" hides zero stores; payout method (store credit vs PayPal).
   f. OUR SIDE: page edits/indexing on our brand page in the last 10 days; hub changes; FYM shop links.
   g. SEASON/TIMING: launch-week spike fading, weekday pattern, holiday shipping cutoffs.
      HOLIDAYS ARE LOW DAYS (Tiffany Nov 9 2026: "the Saturday before was Halloween, so holidays often are not
      big shopping days because people are doing things with their families"). When either side of a
      comparison (same weekday last week, week vs week) contains a family holiday, say so next to the number
      and don't treat the gap as a real gain or drop: "Sat 15 orders vs 7 on Halloween (holiday, low day)".
      The "<60% of the same weekday last week" alarm does NOT fire when today is a holiday, and a jump vs
      a holiday isn't news; compare with the weekday two weeks back instead. Family holidays: Halloween,
      Thanksgiving (Thu Nov 26 2026), Christmas Eve + Day, New Year's Eve + Day, Easter, Mother's Day,
      Father's Day, July 4, Memorial Day + Labor Day weekends. The OPPOSITE: Black Friday through
      Cyber Monday (Nov 27-30 2026) are BIG days, so expect a spike there and a lower week after.
5. Alarm → HQ needs doc `alert-revenue-<brand>-<date>` (red, top of NOW) + push/message to Tiffany:
   what dropped, likely cause, what Claude already did, one yes/no if something needs her.
6. Log in the daily seo doc (`brandWatch` field) and docs/reports/google-revenue/<date>.md.

## Data coverage gaps (fix these, they hide drops)
- Many UpPromote brands sit under tiffanybrie@ dashboards that only get read from her screenshots
  (The Mahjong Co., Bam Bird, OMM, My Fair, Mahj Squad, Middle & Main). Until they move to the Marketplace,
  each daily run reads tiffanybrie@ in Chrome (/u/1) and lists brands with no reading.
- Find Your Mat-ch shoppers: in-app shop-click counting goes live once the tracking script is deployed
  (docs/ANSWERS Nov 4). Then FYM clicks per brand sit next to orders per brand.

## Nov 4 baseline (first run, through Nov 3)
7-day 84 orders / $1,661 vs 148 / $3,388 the week before (49%) and best week. Brand alarms: Bam Bird (4 vs 21),
Mahjong Row ($227 vs $835: FAMILY20 friends-and-family sale through Nov 1), The Mahjong Co. (0, 7 days),
Peace Love (2 vs 12), Mahj Mood (3 vs 9; 0 since Oct 28; White Acrylic Racks launched Oct 25 now SOLD OUT,
plus Chocolate Brown racks, Sleigh All Day mat, Amethyst Luxe racks), Britt Mills (0, 7 days; AI answer
doesn't name us), Miss Mahjong (4 vs 9), Mahj Squad (1 vs 4).

## AI MODE TOO (Tiffany Nov 6 2026 ~1am: "brands we're showing up for in both AI and AI overview... none... only one")
The morning report checks BOTH for every brand: AI Overview (normal results) AND AI Mode (same query + `&udm=50`). Record per brand: overview named/cited, aiMode named/cited, and report four lists: BOTH / OVERVIEW ONLY / AI MODE ONLY / NEITHER. AI Mode in her signed-in Chrome is personalized: click "Try without personalization" when shown. First full read: docs/reports/ai-mode/2026-11-06.md.
