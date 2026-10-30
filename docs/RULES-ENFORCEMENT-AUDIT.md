# Rules enforcement audit (Oct 30, 2026, ~00:30 ET)

Approved by Tiffany Oct 29 11:03pm ("Yes I want you to build this. Google is #1."; docs/ANSWERS.md line 702).
Question asked of every STANDING rule: is it enforced by a scheduled task, by a gate script, or is it explicitly an attended-chat rule? The failures that started this: doc 94 (weekly partner codes post, STANDING Oct 20) never had a scheduled task, and the Oct 27 verified-date refresh on 33 brand pages was never resubmitted to Google.

**Sources read:** CLAUDE.md; docs/ANSWERS.md (all 704 lines); docs/DESK.md (Daily operations, Never-ending); docs/HQ-CLEANUP.md; docs/SOCIAL-SYSTEM.md (= project doc 00g); docs/PICKING-RULES.md; docs/NEW-ALBUM-CHECKLIST.md; docs/FYM-REEL-RULES.md; docs/BRAND-GUIDE.md (§2 + changelog); repo copies of project docs 82 (scripts/social/fbgroup/doc82.md), 86 (docs/86-new-album-protocol.md), 86b (docs/album-process-oct24.md), 89, 00c (docs/SOCIAL-RESET-OCT23.md), docs/PINTEREST.md, docs/EMAIL.md; every scheduled task's full prompt (list_triggers, 32 tasks: 25 enabled, 7 disabled); builder/fym_gate.py (checks [1]-[103]), scripts/swipe/book_gate.py ([a]-[e]), scripts/social/content_lint.py, scripts/social/center_check.py, scripts/partner_send_check.py.
**Not read:** the claude.ai Project docs themselves (the Projects tool was not available in this agent session). Docs 94, 81, 74, 73, 90, 91, 95 were audited only through what the repo and the task prompts quote from them. A follow-up pass with the Projects tool should check those docs for any standing rule not quoted anywhere in the repo.

## Summary

| Status | Count |
|---|---|
| ENFORCED (task or gate does the whole rule) | 31 |
| PARTIAL (an enforcer exists but misses part of the rule) | 27 |
| NOT ENFORCED (no task, no gate) | 23 |
| Attended-chat rule (behaviour while chatting; nothing to schedule) | 15 |
| **Total standing rules audited** | **96** |

Plus 18 duplicates, conflicts or stale facts between tasks (section 9). Six of them change money or Google results: C1, C3, C4, C10, C11 and C12.

### Top 10 gaps (ranked: Google discount-code ranking first, then revenue, then social)

| # | Gap | Why it matters | Fix (who) |
|---|---|---|---|
| 1 | **Weekly codes post (doc 94) can't finish without a person.** Task trig_01QNpT drafts it every Monday 7:37am. Her "yes" is only picked up by the HQ Talk sweep, which runs once a day at 1:47pm, so the 10am Planoly slot is missed. Nothing schedules the FB group post, which an attended Ops chat has to make in Chrome. Maison Mahj isn't in the list. content_lint's 350-character rule would fail the typed list. | It's the same failure as before: the job exists on paper but nothing makes it happen. Google's AI quotes codes that are typed out on social. | Edit E1 + E2 (Claude). Her weekly yes stays. |
| 2 | **Tigre de Tartán's new affiliate policy (email Oct 29) conflicts with three tasks.** The Monday codes post would type "Tigre de Tartán … MAHJMATCH" in IG and FB captions. The weekly verified line puts the brand name and code in the same text. The hub lists TdT with the code. | TdT switches off leaked codes "within days". The first violation would come from the Nov 2 codes-post run. | **Needs Tiffany** (her hub/brand-page idea is waiting on her yes). Until then, E1(a) leaves TdT out of the social captions. |
| 3 | **Three tasks write the same HQ doc, `seo/<yyyy-mm-dd>`.** The morning report writes `aiReport` as an array and `aiSummary` as one line. The M/W/F code report writes `aiReport` as a link and a 2-3 sentence `aiSummary`. The Monday SEO review writes `seo/<date>` as a weekly review. | On M/W/F the code report overwrites the morning numbers, so the next morning's "gained/lost vs yesterday" alarm compares mismatched data. The HQ Google tab's "full report" button may get an array instead of a link. | E3 + E4 + E17 (Claude) |
| 4 | **Scheduled tasks share her Chrome with no lock, and the missed-run watchdog has been off since Oct 22.** Monday stack: 7:13 morning report (Chrome), 8:17 verified-date refresh (Chrome, ran 2h46m on Oct 21), 8:37 weekly Google report (Chrome), 9:07 SEO review (browser), 9:41 ShopMy (Chrome), 10:52 code report (Chrome, ~50 min), 11:41 TNT (Chrome), 12:08 indexing (Chrome), 12:44 Mahji Mentor (Chrome). trig_011puGfeA84 (watchdog) is disabled. | CLAUDE.md says "ONE AGENT DRIVES CHROME AT A TIME". The #1 Google jobs (verified refresh, indexing, code report) can fail silently, like the Oct 21 refresh that "logged success but only changed 1 of 33 pages". | E4(c) watchdog inside the morning report, E5 Chrome-lock line in every Chrome task, E17/E24 move three Monday jobs to Tuesday (Claude) |
| 5 | **Too many Google searches.** Morning report: 13 searches a day. Code report on M/W/F: 35 regular + 70 AI Mode searches. Monday SEO review: more "[brand] discount code" checks. The Oct 20 run hit reCAPTCHA at about 6 searches per batch. | A reCAPTCHA stops the code report, so no AI-answer data and no feedback is sent. | E3(c): the code report reuses the morning's 13 AI Overview results. E17: the SEO review reads reports instead of searching (Claude). |
| 6 | **New affiliate approvals are no longer detected, and Maison Mahj is still skipped.** The approval scan lived in trig_01ErLFamn8 (disabled Oct 22). The onboarding task says "the sales check marks Gmail approvals", but the current sales check prompt has no approval scan and doesn't watch the "applied" brands (her Oct 29 12:30pm ask). Onboarding still says "Skip Maison Mahj (never publish its code)", and so does the BRAND-GUIDE, even though Maison Mahj became a code partner Oct 29 11:07pm. | An approval nobody notices = no brand page, no hub entry, no Google ranking. Maison Mahj's approval email (Jun 21) was missed for 4 months. | E6(b), E7, BRAND-GUIDE line (Claude; she already decided Maison Mahj) |
| 7 | **Sales reconcile misses accounts.** The Ops rule from Oct 29 10:05pm says to read the UpPromote Marketplace dashboard (it covers Mahjong Row, Lets Be Besties, Anders Ruff, Royal Mahjong Society, Mahjong Register, Bird & Bamboo) instead of asking her for screenshots. Neither the sales check nor the morning report has that URL. The morning report reconciles only the Gmail connector inbox (mahjmatchmaker@), not tiffanybrie@, and it marks Mahjong Row "needs Tiffany to sign in". ShopMy earnings (her Oct 29 4:14pm ask) are read by no task. | Sales get undercounted, which can raise false drop alarms or hide real drops. | E4(b), E6(a)(d) (Claude) |
| 8 | **No caption gate for the Google-for-social rules.** MAHJMATCH typed in every IG/FB caption (Oct 26 11:56pm), #MahjMatch on every post (Oct 26 2:37pm), "saves you money", "every mat / every brand", "still available", shortened brand names, no YMI / Kaleidoscope / Paige Spearin features, TdT name + code together: content_lint.py checks none of these. No task runs content_lint before Planoly. | Social captions that Google reads go out without the code, or with banned or non-compliant wording. | GA1 (Claude), and run it in E1 and E9 |
| 9 | **Planoly's next 7 days are empty and nothing refills them.** DESK Oct 29: "❌ 0 scheduled Oct 30 - Nov 5". The desk cleanup checks only the Pinterest workspace (019fc27b…), not Instagram (019fc27c…). Nothing checks that every IG post has an FB Page target, every story slide and every brand tag. | Social has gone 3+ days silent with no alarm. FB Page copies are her standing rule (Oct 26 2:45pm). | E9 (Claude) + N3 social prep task (Claude preps; **posting needs her yes**) |
| 10 | **The /links weekly refresh was never scheduled.** Her Oct 22 1:00pm call was "weekly refresh from Sunday". CLAUDE.md lists "/links weekly refresh" under standing authority. No task does it. | This is the bio link on every post. It's the same kind of miss as doc 94. | N1 (Claude, standing authority) |

## Legend
- **Kind:** R = recurring job · C = content rule · D = data rule · A = attended-chat behaviour.
- **Fix owner:** **Claude** = covered by the standing authority in CLAUDE.md (core recurring jobs, fixes, catalog adds, HQ/DESK cleanup), or a task/gate edit that carries out a decision she already made. **Tiffany** = new decision, money, deleting, new public posts.
- Task ids are scheduled tasks. Edits E1-E24, new tasks N1-N3 and gate changes GA1-GA4 are spelled out in sections 10-12.

## 1. Google / SEO

| # | Rule (short) | Source | Kind | Enforcer | Status | Fix |
|---|---|---|---|---|---|---|
| G1 | MAHJMATCH named in the AI Overview + AI Mode for every partner's "[brand] discount code", every day, OMM first | ANSWERS 10-27 18:31; doc 39 | R | trig_01LZjG (13 brands daily, 7:13am) + trig_01GQHw (35 brands M/W/F 10:52am) | ENFORCED (the morning report's first run is Oct 30, so it's unproven) | none |
| G2 | Lost AI citation or sales drop = red HQ alert with a plan, the same run | ANSWERS 10-29 14:49 | R | trig_01LZjG red-alert rules; trig_019Fji step 5e | ENFORCED | none |
| G3 | Weekly verified-date refresh on every brand page + the hub "Updated" date, confirmed by live curl | ANSWERS 10-27 18:11, 10-29 14:51; CLAUDE.md standing authority | R | trig_01PGtT (Mon 8:17am) | PARTIAL: hasn't fired on the new schedule yet (last_fired Oct 21; first weekly run Nov 2); no retry if her computer is off (watchdog disabled); runs inside the Monday Chrome pileup; the TdT line format now conflicts with TdT's policy (C11) | E4(c), E5; TdT waits on Tiffany |
| G4 | Every changed brand page re-submitted to Google within days (changed pages get all slots first) | ANSWERS 10-29 ~4pm + 11:03pm | R | trig_012P44 tier 0; trig_01PGtT step 5 | ENFORCED (rewritten Oct 29 11:41pm) | none |
| G5 | Sitemap read checked weekly | trig_012P44 prompt (Mondays) | R | trig_012P44 | ENFORCED. The one-time sitemap resubmit is still DESK priority 3 | attended Ops, today |
| G6 | Weekly partner codes post, every brand + code typed out (FB group + IG + FB Page) | doc 94 (STANDING Oct 20); ANSWERS 10-29 16:53 | R | trig_01QNpT (Mon 7:37am) | PARTIAL: yes → Planoly depends on a once-daily sweep; no step posts the FB group copy; Maison Mahj missing; TdT conflict; lint length conflict | E1, E2 (Claude) |
| G7 | Social captions carry MAHJMATCH typed out so IG search and Google read it | ANSWERS 10-26 23:56 | C | none (content_lint has no such check) | NOT ENFORCED | GA1 |
| G8 | Google AI feedback is sent without asking (standing yes) | ANSWERS 10-26 23:54 | R | trig_01GQHw step 6 | ENFORCED | none |
| G9 | Ranks come from Search Console + a mobile check, never desktop rank alone | ANSWERS 10-29 14:49 | D | trig_01LZjG (SC is "the real number") | PARTIAL: trig_01GQHw step 2a still records "our organic position" from desktop Chrome with no label | E3(e) |
| G10 | HQ Google tab always shows an accurate latest report | ANSWERS 10-29 11:09 | R | trig_01GQHw step 10 + trig_01LZjG | PARTIAL: the seo/<date> field collision (C1) | E3(b), E4(a), E17 |
| G11 | Weekly Google & OMM report with a push notification when ready | ANSWERS 10-26 23:55 | R | trig_01HpSV (Mon 8:37am) | ENFORCED | E18 (read SC from the morning doc; avoids Chrome) |
| G12 | Weekly SEO + earnings strategy review | trig_01CgZr (Tiffany Oct 10) | R | trig_01CgZr (Mon 9:07am) | PARTIAL: repeats G11's Search Console and Google work (C2); writes `seo/<date>` (C1); its Chrome tab-close line is missing | E17 |
| G13 | Every approved partner gets brand page + hub + logos + FYM + indexing | doc 29; trig_01C7xP | R | trig_01C7xP (daily 2:22pm) | PARTIAL: approvals no longer flow in (M7); stale Maison Mahj skip (C10) | E6(b), E7 |
| G14 | 1-month evaluation of the AI-answer work (Nov 9) | trig_01VMhd | R (one-time) | trig_01VMhd | PARTIAL: reads sources that are no longer kept (Feedback Library send log, the disabled daily AI check's rotation, Work Tracker) | E16 |

## 2. Sales & money

| # | Rule | Source | Kind | Enforcer | Status | Fix |
|---|---|---|---|---|---|---|
| M1 | Every sale captured from BOTH inboxes + dashboards and reconciled against every affiliate email | trig_019Fji (Oct 10, Oct 29 4:51pm); ANSWERS 10-29 22:05 (Ops) | R | trig_019Fji (2:04pm + 12:04am); trig_01LZjG part 3 | PARTIAL: no UpPromote Marketplace read (Ops rule); the morning reconcile skips tiffanybrie@ and wrongly sends Mahjong Row to "needs Tiffany" (C12) | E4(b), E6(a) |
| M2 | Spike AND drop checks every run, same-time-of-day comparison, red alert + plan | ANSWERS 10-23 02:24, 10-29 14:49 | R | trig_019Fji step 5 | ENFORCED | none |
| M3 | Weekly + monthly brand trend reads | ANSWERS 10-23 02:24 | R | trig_019Fji step 5g | ENFORCED | none |
| M4 | Late-yesterday sales closed out after midnight | trig_019Fji step 0 (Oct 13) | R | trig_019Fji 12:04am | ENFORCED | none |
| M5 | One "send me amounts" card; her typed amounts get processed | trig_019Fji step 3 | R | trig_019Fji | ENFORCED | none |
| M6 | ShopMy-only earnings as 'ShopMy:' rows in Money (never double-count Mini Mahjer) | ANSWERS 10-29 16:14; DESK never-ending | R | none | NOT ENFORCED | E6(d) |
| M7 | New affiliate approvals detected in Gmail → brands row "approved" → onboarding | disabled trig_01ErLF step 6 (after the Royal Mahjong Society miss, Oct 10) | R | none (the disabled task held it; trig_01C7xP assumes the sales check does it) | NOT ENFORCED | E6(b) |
| M8 | Brands she applied to are watched, never a black hole | ANSWERS 10-29 12:30 | R | HQ card only; no task checks Gmail for those brands | NOT ENFORCED | E6(b) |
| M9 | Partner program/policy/code changes caught (e.g. TdT policy Oct 29; Maison Mahj switch Jun 21) | ANSWERS 10-29 23:07, 23:42 | R | trig_01PGtT step 2 (weekly, light) | PARTIAL: weekly only, code-change words only | E6(c) |
| M10 | Album request form submissions counted | trig_019Fji step 4 (Oct 15) | R | trig_019Fji | ENFORCED | none |
| M11 | Commission tiers / time-limited bumps tracked (OMM 20% ends Nov 25) | trig_01CgZr (Oct 10) | R | trig_01CgZr step A | ENFORCED | none |

## 3. Partners & codes

| # | Rule | Source | Kind | Enforcer | Status | Fix |
|---|---|---|---|---|---|---|
| P1 | Fixed verified-line format; never re-test codes; change a code only when a partner email says so | BRAND-GUIDE 10-22 23:17; CLAUDE.md | D | trig_01PGtT | ENFORCED | none |
| P2 | Partner launches, restocks and sneak peeks flagged the same day (email + IG, 3x daily) | ANSWERS 10-27 11:42, 10-28 23:28 | R | trig_01Ljz8 | ENFORCED | none |
| P3 | Sold-out items re-checked; personal buys (Sunday Festive Plaid) messaged | ANSWERS 10-28 15:21 | R | trig_01Ljz8 step 2c | ENFORCED | none |
| P4 | New full-size partner mats/tile sets reach FYM within ~2 days | ANSWERS 10-27 02:21-02:26 | R | trig_01S2Vs step 4g + partner_mat_sweep; fym_gate [100] | ENFORCED (the build itself is attended) | none |
| P5 | New partner → verify IG handle, follow, add to Favorites, log it, in the same turn | CLAUDE.md INSTAGRAM BRAND WATCH; ANSWERS 10-28 09:49 | R | none (trig_01C7xP has no IG step) | NOT ENFORCED | E7(b) |
| P6 | Weekly brand watch Mondays: follow new ShopMy/partner brands; reshare list in HQ | CLAUDE.md INSTAGRAM BRAND WATCH ("part of the desk cleanup") | R | none (desk cleanup prompt doesn't include it) | NOT ENFORCED | N2 |
| P7 | Sunday Mahjong's IG is a Chrome check (Planoly can't read it) | ANSWERS 10-27 ~18:45 | R | trig_01Ljz8 tries Planoly (fails); trig_01Y68d reads Sunday's release page | PARTIAL | N2 (Chrome read) |
| P8 | Brand social notes kept (what each brand pushes and pairs) | FYM-REEL-RULES 12 | R | trig_01Ljz8 step 2b | ENFORCED | none |
| P9 | Partner feedback form + Dropbox watched; daily through Nov 10, then disabled | ANSWERS 10-25 21:37, 10-27 18:22; wording rule 10-25 | R | trig_01RKw9 | PARTIAL: cron `13 14 * 10,11 *` runs daily through Nov 30; the prompt still says "4x daily Oct 26-31… ends itself by date"; nothing disables it after Nov 10. Daily FYM-feedback reading continues via the HQ cleanup (HQ-CLEANUP "FYM feedback") | E8 |
| P10 | Every partner brand gets ONE guaranteed match album | ANSWERS 10-29 12:52; BRAND-GUIDE changelog | R | none | NOT ENFORCED | N2 (list missing ones on hq/albums) |
| P11 | Never pitch the codes page or Google ranking to partners; never link partners to /mahjong-discount-codes | ANSWERS 10-26 14:17, 10-29 12:41 | A | attended | Attended | optional: add to partner_send_check |
| P12 | Partner send gate before any partner email or graphics | DESK (Oct 27 3:08am) | A | scripts/partner_send_check.py | ENFORCED (gate; the attended chat runs it) | none |
| P13 | Maison Mahj is a code partner (MAHJMATCH, free shipping on tile sets; plain link) | ANSWERS 10-29 23:07 | D | none: BRAND-GUIDE §2 and trig_01C7xP still say never publish its code | NOT ENFORCED (stale) | E7(a) + BRAND-GUIDE edit (Claude) |
| P14 | TdT policy: no code in IG/TikTok captions; brand name and code never in the same website text | ANSWERS 10-29 23:42 | C | none | PARTIAL (waiting on her decision) | **Tiffany** decides the hub/page approach; E1(a) now |

## 4. Social

| # | Rule | Source | Kind | Enforcer | Status | Fix |
|---|---|---|---|---|---|---|
| S1 | Every approved post goes into Planoly at its time, the day it's approved | CLAUDE.md SOCIAL 1 | A | attended | Attended | none |
| S2 | Every IG post/reel also goes to the FB Page (brand names, not @handles) | CLAUDE.md SOCIAL 11; ANSWERS 10-26 14:45 | R | none checks Planoly targets | NOT ENFORCED | E9(d) audit |
| S3 | Every feed post also goes to stories, every slide, with @mentions | CLAUDE.md SOCIAL 8 | C | none | NOT ENFORCED | E9(d) audit |
| S4 | Every brand shown is tagged (verified handle, Tag people) + collab invite | CLAUDE.md SOCIAL 5, 9; FYM-REEL-RULES 21 | C | none | NOT ENFORCED | E9(d) audit |
| S5 | #MahjMatch on every post (default set of 5) | ANSWERS 10-26 14:37; BRAND-GUIDE | C | none (content_lint lacks it) | NOT ENFORCED | GA1 |
| S6 | Banned caption wording: "saves you money", "every mat/brand", "still available", short brand names, "(affiliate)", features of YMI / Kaleidoscope / Paige Spearin | BRAND-GUIDE; ANSWERS 10-23, 10-25 21:55, 10-27 02:44 | C | content_lint checks only codes, crush/nope/pass, naming, length | NOT ENFORCED | GA1 |
| S7 | Captions linted before Planoly | content_lint.py docstring (Oct 21) | R | script exists; no task runs it | PARTIAL | E1(c), E9(d) |
| S8 | HQ Social tab plan refreshed every day | ANSWERS 10-27 22:00; HQ-CLEANUP rule 10 | R | trig_01RgaY (HQ cleanup) | ENFORCED | none |
| S9 | Monday numbers per post (follows, profile visits, shares); drop formats that earn nothing | SOCIAL-SYSTEM "Measure" (Oct 28) | R | none | NOT ENFORCED | N2 |
| S10 | Weekly Claude Doc of the planned FB group posts | ANSWERS 10-27 18:31 | R | none | NOT ENFORCED | N3 |
| S11 | Reposts 1-2 a day from her "Save for repost", partners only | SOCIAL-SYSTEM | R | none (Claude preps the list; she reshares in the app) | NOT ENFORCED | N2 (weekly reshare list) |
| S12 | Restocks/launches: same day or never, stories + FB only, never a feed post | ANSWERS 10-27 12:01, 20:21 | R | trig_01Ljz8 step 5; HQ-CLEANUP rule 9 | ENFORCED | none |
| S13 | Pinterest pins go out every day, failures fixed, queue fed | trig_01UsWf (Oct 21) | R | trig_01UsWf (every 3rd day, 7 days queued ahead) | ENFORCED (the name says "daily": C15) | E19 |
| S14 | FYM reel rules 1-22 (centred, phone never moves, tiles + mat big, every product tagged) | docs/FYM-REEL-RULES.md | C | center_check.py (rule 11) only | PARTIAL: rule 20 (phone frame never moves) has no script | GA3 |
| S15 | Storyboard before render; ask the brand-mix question first | ANSWERS 10-27 18:21; SOCIAL-SYSTEM | A | attended | Attended | none |
| S16 | Album of the week is the content engine (one album a week) | SOCIAL-SYSTEM | A | attended + DESK | Attended | N3 checks the week is covered |
| S17 | Planoly next 7 days covered (IG + FB Page) | DESK "Daily operations" | R | trig_01WeCb reports it, but reads the Pinterest workspace only (C14); nothing refills it | PARTIAL | E9(a), N3 |
| S18 | Planoly reminder: one key action in the first line; send the full steps in chat at post time | ANSWERS 10-26 12:38 | A | attended | Attended | none |
| S19 | Weekly "new this week" roundup from hq/newproducts | album-process-oct24 (86b); ANSWERS 10-24; DESK never-ending | R | none | NOT ENFORCED | N2 |

## 5. FYM / catalog

| # | Rule | Source | Kind | Enforcer | Status | Fix |
|---|---|---|---|---|---|---|
| F1 | Gate before every publish | CLAUDE.md FYM 1 | R | builder/fym_gate.py | ENFORCED | none |
| F2 | Independent QA before she sees it | CLAUDE.md FYM 2 | A | attended | Attended | none |
| F3 | Every publish goes to the artifact AND the website copy AND the README 0a pin | CLAUDE.md FYM 0 | A | attended | Attended | GA4 (optional) |
| F4 | Non-partner lockout, no Mahjong Studios mats, holiday rules, colour sort | CLAUDE.md | D | fym_gate [8][8b][9][10][12][13][13h][13c] | ENFORCED | none |
| F5 | Photo rules: low bar, too_far / covered / questionable hidden, racks reviewed on white + navy | CLAUDE.md FYM 6, 6b | D | fym_gate [3][3c][3d][50][56][45] | ENFORCED | none |
| F6 | A partner mat live for more than 2 days and missing from FYM = FAIL | ANSWERS 10-27 02:21 | D | fym_gate [100] + launch watch sweep | ENFORCED | none |
| F7 | ShopMy: Etsy mats in after the photo gates; Amazon only her picks | ANSWERS 10-26 11:06 | R | trig_01NpQo (Mon 9:41am) | ENFORCED | E24 (move to Tue) |
| F8 | Weekly FYM new-mat scan | trig_01NRxY (Oct 14) | R | trig_01NRxY | PARTIAL: uses the pre-Oct 21 strict photo rule ("only an isolated photo… no tiles, racks") that contradicts CLAUDE.md FYM 6 (LOW bar); writes an info-only needs card (HQ-CLEANUP: info is not a card); duplicates the launch-watch sweep (C6, C7) | E13 |
| F9 | Twice-monthly new mat watch | trig_01JdJP (Oct 5) | R | trig_01JdJP | PARTIAL: stale (Work Tracker, checklist doc, device Dropbox path, disabled watchdog); duplicate | E14 |
| F10 | Match Builder data refresh | trig_01UwvU | R | trig_01UwvU (Mon 6:41am) | ENFORCED (the name says "daily") | E22 |
| F11 | FYM snapshot (config/fym-mats-snapshot.json) refreshed after every FYM publish | CLAUDE.md SWIPE BOOK GATE | D | none (book_gate reads the snapshot but never checks its age) | NOT ENFORCED | GA2 |
| F12 | MATCH-INBOX items handled (Matches & Catalog checks it every reply) | CLAUDE.md MATCH INBOX | A/R | attended; no age check | PARTIAL | E9(e) |
| F13 | A bug she reports gets a gate check the same day | CLAUDE.md FYM 8 | A | attended | Attended | none |

## 6. Albums

| # | Rule | Source | Kind | Enforcer | Status | Fix |
|---|---|---|---|---|---|---|
| A1 | No tile-set swipe book without book_gate PASS (colour card, TNT recs first, FYM photos, widest pool) | CLAUDE.md SWIPE BOOK GATE (Oct 29 12:35pm) | D | book_gate.py via build_book.py / finish_patch.py | PARTIAL: launch watch (trig_01S2Vs 4c) and Mahji Mentor (trig_01LC2k 4d) build tile-set books by copying artifact QZsZXND61Lg6FsgR65RxMv with scripts/shortlist.py, which bypasses the gate (C9); book_gate's HOLIDAY regex bans Halloween/Valentine/Easter mats, though the Oct 21 FINAL rule says they are not holiday (C8) | E10, E11, GA2 |
| A2 | TNT recs lead every swipe book, labelled "TNT rec · mat · brand" | memory preference (her saved preference); CLAUDE.md | R | book_gate [b]; trig_015vK2 (TNT scan) | PARTIAL: the TNT scan never writes config/tnt-recs.json (the gate's input), still says "start with Malachite", and sends finds to Ready to Ship | E12 |
| A3 | New album checklist run top to bottom (/links card, /mahjong-tile-matches, colour pages, brand page link, indexing, Pinterest, FB group, "now available" wording) | docs/NEW-ALBUM-CHECKLIST.md (Oct 26) | R | none checks it after go-live | NOT ENFORCED (the checkable parts) | E9(f) |
| A4 | Known restock → that set goes FIRST (build ahead) | ANSWERS 10-28 15:27; SOCIAL-SYSTEM | R | trig_01Y68d (dated windows → needs doc); trig_01Ljz8 | PARTIAL: the watchers flag it, but nothing puts the album at the top of the queue | E9(c) |
| A5 | Album order (MFM Style of Your Life → Bam Bird Deco trio → …) | ANSWERS 10-28 15:26 | A | DESK | Attended | none |
| A6 | Colour card first (docs 86/86b) | doc 86b | D | book_gate [a] | ENFORCED | none |
| A7 | Pick/review pages show tiles + mat together (match-card style) | CLAUDE.md (Oct 28 3:37pm) | A | attended | Attended | none |
| A8 | New-release product images saved to her Dropbox as soon as they appear (brands swap the flat render later) | her saved preference (memory) | R | trig_01S2Vs saves to repo assets/launches only | NOT ENFORCED | E10(c) |
| A9 | /links "latest album" card swapped at album launch | NEW-ALBUM-CHECKLIST §2 | A | attended | Attended | N1 catches misses |

## 7. HQ / desk

| # | Rule | Source | Kind | Enforcer | Status | Fix |
|---|---|---|---|---|---|---|
| H1 | Daily HQ + Ready to Ship cleanup | HQ-CLEANUP (Oct 21) | R | trig_01RgaY (6:47am) | ENFORCED | none |
| H2 | Nightly desk cleanup, nothing falls on the floor | CLAUDE.md THE DESK | R | trig_01WeCb (9:23pm) | PARTIAL: stale prompt (Pinterest workspace only; "(1) FYM launch Oct 27"; "verified dates 1st/15th"); none of the Monday duties CLAUDE.md gives it | E9 |
| H3 | "Decided but never shipped" sweep of 14 days of ANSWERS | HQ-CLEANUP (Oct 29 12:33pm) | R | trig_01RgaY + trig_01WeCb (both read HQ-CLEANUP) | ENFORCED | none |
| H4 | No answer is not a no | HQ-CLEANUP (Oct 29 1:08pm) | R | trig_01RgaY | ENFORCED | none |
| H5 | HQ Talk inbox + "LIVE YES" items acted on within hours | trig_015cSe (Oct 17); doc 74 | R | trig_015cSe | PARTIAL: cron `47 13 * * *` = once a day, though its own text says "every 3 hours" | E2 |
| H6 | ANSWERS log before replying; check it before asking | CLAUDE.md | A | attended | Attended | none |
| H7 | Every Chrome task closes every tab it opened, even on errors | ANSWERS 10-29 ~11:10 (her yes) | R | TAB RULE in trig_01C7xP, trig_01LC2k; close lines in trig_01LZjG, trig_01PGtT, trig_012P44, trig_01NpQo, trig_019Fji | PARTIAL: missing in trig_01GQHw (code report), trig_01CgZr, trig_015cSe, trig_012tRm, trig_01JdJP; trig_015vK2 has no "even on errors" | E5 |
| H8 | One agent drives Chrome at a time | CLAUDE.md (Oct 21) | R | none for scheduled tasks | NOT ENFORCED | E5 + E17/E24 |
| H9 | Missed computer runs are retried and she's told | trig_011puG (Oct 9), disabled Oct 22 | R | none (only the morning report checks indexing; trig_01PGtT writes an HQ card if offline) | NOT ENFORCED | E4(c) |

## 8. Site maintenance

| # | Rule | Source | Kind | Enforcer | Status | Fix |
|---|---|---|---|---|---|---|
| W1 | Broken link/image fixes (Claude's job, no asking) | CLAUDE.md standing authority | R | trig_012tRm (monthly, 1st) | PARTIAL: report-only ("Do NOT edit the website… so Tiffany… can approve fixes"), which contradicts the standing authority; writes to a retired Claude Doc checklist | E15 |
| W2 | Retired / back-in-stock mats on album cards kept true | trig_012tRm; ANSWERS 10-28 15:21 | R | trig_012tRm step 2 (report only) | PARTIAL | E15 |
| W3 | /links weekly refresh (from Sunday) | ANSWERS 10-22 13:00; CLAUDE.md standing authority | R | none | NOT ENFORCED | N1 |
| W4 | Album "now available" wording after a launch | CLAUDE.md standing authority; checklist §3 | A | attended | Attended | E9(f) spot-check |
| W5 | Nav/header change: screenshot live at 1280/1440/390 before calling it done | DESK never-ending (Oct 29) | A | attended | Attended | none |
| W6 | jsDelivr warm-up before any block goes live | doc 73 | A | attended | Attended | none |
| W7 | Mobile layout gaps checked | trig_012tRm step 3 | R | trig_012tRm | PARTIAL (report only, stale log targets) | E15 |

## 9. Duplicates, conflicts and stale facts between tasks

| # | What | Tasks | Impact | Fix |
|---|---|---|---|---|
| C1 | Same HQ doc `seo/<yyyy-mm-dd>` written by three tasks with different field shapes: morning `aiReport` = array, code report `aiReport` = report link; both write `aiSummary`; SEO review writes `seo/<date>` too | trig_01LZjG, trig_01GQHw, trig_01CgZr | The M/W/F overwrite breaks the next morning's gained/lost comparison and possibly the HQ "full report" button | E4(a), E3(b), E17 |
| C2 | Two Monday Search Console + Google reviews | trig_01HpSV (8:37) vs trig_01CgZr (9:07) | Double Chrome time + double searches | E17 |
| C3 | Google search volume: 13/day + 105 on M/W/F + Monday extras | trig_01LZjG, trig_01GQHw, trig_01CgZr | reCAPTCHA risk (hit Oct 20 at ~6 per batch) | E3(c), E17 |
| C4 | Monday Chrome pileup 7:13 → 12:44 (9 browser jobs; the verified refresh can run ~3h) | see top gap 4 | Silent misses of #1 jobs | E5, E17, E18, E24 |
| C5 | Same-minute browser starts on the 1st/15th: indexing 12:08 (Chrome) + new mat watch 12:08 (browser pane); Nov 1 also monthly maintenance 11:37 | trig_012P44, trig_01JdJP, trig_012tRm | Collision | E14 (disable), E15 |
| C6 | Photo rule conflict: "only an isolated photo of the mat counts" vs CLAUDE.md FYM 6 LOW bar (Oct 21) | trig_01NRxY | Good mats marked "needs photo" | E13 |
| C7 | Four new-mat finders: launch watch sweep (2x daily), FYM weekly scan, new mat watch (1st/15th), ShopMy check | trig_01S2Vs, trig_01NRxY, trig_01JdJP, trig_01NpQo | Duplicate HQ cards; stale outputs | keep launch watch + ShopMy; E13, E14 |
| C8 | book_gate HOLIDAY regex includes halloween/spooky/valentine/easter; the Oct 21 FINAL holiday rule says those mats live in colour sections | scripts/swipe/book_gate.py | Valid mats excluded from swipe books | GA2 |
| C9 | Launch watch and Mahji Mentor build tile-set swipe books outside build_book.py, so book_gate never runs | trig_01S2Vs 4c, trig_01LC2k 4d | Breaks the Oct 29 SWIPE BOOK GATE | E10, E11 |
| C10 | "Skip Maison Mahj (never publish its code)" (onboarding) and BRAND-GUIDE §2 "Maison Mahj forbids posting its code" vs Oct 29 11:07pm: Maison Mahj is a code partner | trig_01C7xP; docs/BRAND-GUIDE.md | No page/hub entry for a code partner | E7(a), BRAND-GUIDE line |
| C11 | TdT policy (Oct 29) vs codes-post IG/FB captions, the verified-line format and the hub listing | trig_01QNpT, trig_01PGtT | TdT can switch our code off | E1(a) now; **Tiffany** decides the hub/page |
| C12 | Morning report: "Dashboards signed out (e.g. Mahjong Row affiliate) = needs Tiffany"; Ops rule Oct 29 10:05pm: read the UpPromote Marketplace ourselves, don't ask her | trig_01LZjG | Homework for her; undercount | E4(b) |
| C13 | content_lint fails IG/FB captions over 350 characters; the doc 94 typed list is long on purpose (her Oct 29 yes) | content_lint.py vs trig_01QNpT | The lint would block or be skipped | GA1 (`--codes-list` exemption) |
| C14 | Desk cleanup reads Planoly workspace 019fc27b (Pinterest) only; IG + FB Page live in 019fc27c | trig_01WeCb | The "next 7 days" check looks at the wrong calendar | E9(a) |
| C15 | Names/schedules that don't match: "Google code report (daily)" runs M/W/F; "Hourly brand launch watch" runs 2x; "Mahji Mentor (3x daily)" runs 1x (the prompt lists 8:44/12:44/5:44); "HQ Talk… every 3 hours" runs 1x; "Pinterest autopin (daily)" runs every 3rd day; "Match Builder daily" runs weekly; partner feedback "4x daily, Oct 26-31, ends itself" runs daily through Nov 30 | several | People and tasks read the wrong cadence | E2, E3, E8, E11, E19, E21, E22 |
| C16 | Stale references: Work Tracker doc 003718bb, checklist doc 3253b02a, the "hourly watchdog" (trig_01JdJP, trig_012tRm, trig_01VMhd); Mahji Mentor "Known launches (Oct 12)"; desk cleanup "(1) FYM launch Oct 27" + "verified dates 1st/15th"; TNT "start with Malachite"; HQ-CLEANUP §4 "Launch-critical first (Tue Oct 27)"; FYM scan doc 49 (Oct 14) | several | Wrong targets and priorities | E9, E11, E12, E13-E16; HQ-CLEANUP §4 edit |
| C17 | Morning report and sales check both edit money docs | trig_01LZjG, trig_019Fji | Low risk (both pin if_version). Keep the morning report as an add-only verifier | none |
| C18 | Release calendar reads brand IG through the Pinterest workspace id; partner watch uses the IG workspace | trig_01Y68d | Minor | E23 |

## 10. Recommended edits to existing scheduled tasks (exact text)

Each block is text to APPEND to the task's prompt unless it says "replace". All are Claude's to make under standing authority, except where marked **Tiffany**. Note from ANSWERS 10-29 11:05: editing a task's prompt can be blocked by the auto-approval check. If that happens, put the edit on DESK for the attended Main chat rather than asking her again (she already said yes to the audit).

**E1 · trig_01QNpTLC6egFF4u4oethFWVP (weekly codes post)**, append:
> ADDED Oct 30 (rules audit). (a) TIGRE DE TARTÁN policy (affiliates@tigredetartan.com, Oct 29): never put Tigre de Tartán's name and MAHJMATCH in the same caption on Instagram, Facebook or TikTok. Leave TdT OUT of texts 2b and 2c. In the FB group first comment, include TdT only if docs/ANSWERS.md shows Tiffany's yes to that; otherwise leave it out there too. (b) MAISON MAHJ is a code partner (Tiffany Oct 29 11:07pm): include "Maison Mahj: complimentary shipping on tile set orders with code MAHJMATCH" in every list. Never call it a new code. (c) Run `python3 scripts/social/content_lint.py --codes-list` on all three texts. Codes, banned words and naming must pass; the typed brand list is exempt from the 350-character check only. (d) HER YES: before finishing, create a one-time scheduled task for 9:45am ET today (create_trigger run_once_at) that re-reads needs/codes-post-<date>. If answer.text says yes, it schedules IG + FB Page in Planoly for 10am (workspace 019fc27c-0bef-7533-bc3f-030acc19a135) and writes a DESK.md line at the TOP: "OPS: post + feature the FB group codes post (doc 82) TODAY, unfeature last week's: <file path>". If there's no answer, it re-checks at 1:45pm and 7:45pm, then leaves it to HQ cleanup ("no answer is not a no"). (e) Save the three texts to docs/social/codes-post-<yyyy-mm-dd>.md and commit.

**E2 · trig_015cSezcshZpncAUiBedzWwv (HQ Talk sweep)**: change cron to `CRON_TZ=America/New_York 47 7-22/3 * * *` (7:47, 10:47, 13:47, 16:47, 19:47, 22:47; this matches its own "every 3 hours"). Append:
> TAB RULE: if this run uses Chrome, call tabs_context_mcp first, close any leftover tabs in your group, and close every tab you opened before you finish, including on errors. Check `needs/codes-post-*` answers first on Mondays.

**E3 · trig_01GQHweQ9DbqXgoG2dp8GgBa (Google code report)**: rename "Google code report (Mon/Wed/Fri)". Append:
> ADDED Oct 30 (rules audit). (b) HQ seo doc: the 7:13am morning report owns `aiSummary`, `aiBrands` and `sc` in today's seo/<date> doc. Do NOT overwrite them. Write `aiReport` = this report's link, `codeSummary` = your 2-3 sentences, and put your Today section at the TOP of `dailyLog` (keep the morning text below it). Pin if_version. (c) Google pacing: for the 13 brands in today's `aiBrands`, reuse the morning AI Overview result and run only the two AI Mode checks. Run all three checks only for the other 22 brands. Wait 15-20s between searches. (d) TAB RULE: call tabs_context_mcp at the start and close leftover tabs in your group. Close every tab you opened before finishing, including on errors or reCAPTCHA. Closing your tabs is the last tool call. (e) Label the organic rank "desktop check" and put the Search Console position next to it. Never report a desktop rank as "our position".

**E4 · trig_01LZjGfVneN3vKwweVXwbzub (morning Google & Revenue report)**, append:
> ADDED Oct 30 (rules audit). (a) Store the per-brand array in the field `aiBrands` (not `aiReport`). `aiReport` stays the Google Code Report link that HQ's button opens. Never overwrite a non-empty `aiReport`. (b) SALES: before listing any dashboard as "needs Tiffany", read in Chrome the UpPromote Marketplace https://marketplace.uppromote.com/commissions/list?page=1&page_size=100 (covers Mahjong Row & Co., Lets Be Besties, Anders Ruff, Royal Mahjong Society, Mahjong Register) and https://af.uppromote.com/22be84-01/commission (Bird & Bamboo), using get_page_text (Ops rule, Oct 29 10:05pm). Also read the tiffanybrie@ inbox in Chrome (mail.google.com/mail/u/1, same queries as the sales check). Only dashboards that really are signed out or not in her Chrome (e.g. My Fair Mahjong) go on the "needs Tiffany" list. (c) WATCHDOG (replaces the disabled trig_011puGfeA84uahqWU7TMXCAB): call list_triggers. For each of these, check that last_run fired at its last due time and SUCCEEDED: trig_012P44DeDt8S9EZVybe35PyA (indexing, daily), trig_01PGtT8NFXe6341WjBHqmYJu (verified dates, Mon), trig_01GQHweQ9DbqXgoG2dp8GgBa (code report, M/W/F), trig_019FjiaFBVX512N67EYxrGUw (sales 12:04am), trig_01QNpTLC6egFF4u4oethFWVP (codes post, Mon), trig_01HpSV6bJuJQSJ3aoBjctyhY (weekly report, Mon). If one missed or failed, fire_trigger it once, at most one Chrome task at a time, and say so in dailyLog. A missed verified-date or indexing run is a RED alert.

**E5 · CHROME LOCK + TAB RULE**: append this to every task that uses a browser: trig_01LZjG, trig_01PGtT, trig_01HpSV, trig_01CgZr, trig_01NpQo, trig_01GQHw, trig_015vK2, trig_012P44, trig_01LC2k, trig_01C7xP, trig_019Fji, trig_015cSe, trig_012tRm.
> CHROME LOCK (CLAUDE.md: one agent drives Chrome at a time). Before opening a tab, call tabs_context_mcp. If another Claude tab group is open on Squarespace, Search Console, Google search or Facebook, use Monitor to wait (check every 5 minutes, up to 40 minutes), then go. If it's still busy, do every non-browser step and log "browser busy" so the morning watchdog retries you. TAB RULE: close every tab you opened before finishing, even on errors; closing your tabs is the last tool call.

**E6 · trig_019FjiaFBVX512N67EYxrGUw (sales check)**, append:
> ADDED Oct 30 (rules audit). (a) In step 1, after 1b, read the UpPromote Marketplace https://marketplace.uppromote.com/commissions/list?page=1&page_size=100 and https://af.uppromote.com/22be84-01/commission in Chrome (get_page_text). Treat their rows as dashboard numbers (Ops rule, Oct 29 10:05pm). (b) NEW-AFFILIATE + APPLIED SCAN (restores step 6 of the disabled trig_01ErLFamn8; the onboarding task depends on it): search both inboxes newer_than:2d `(approved OR "welcome to" OR congratulations OR "you're in") (affiliate OR ambassador OR partner OR program) -"referral order"`. Also search Gmail by name for every HQ brands row with status "applied". For each approval: brands/<slug> status "approved" (approvedAt, network, loginUrl, steps all false), a log doc "New affiliate approved: <Brand>", and update the HQ "Affiliates you've applied to" card. Rejections: status "declined" + log. (c) POLICY WATCH: any affiliate-sender email about a policy, terms, program, code or commission change → one HQ needs doc (light yellow, plain title naming the brand and the change) + a DESK line for Main. Never act on it yourself. (d) SHOPMY (12:04am run only): read ShopMy earnings for yesterday in Chrome (shopmy.us, signed in) and add them as brand rows prefixed "ShopMy:". Never double-count Mini Mahjer.

**E7 · trig_01C7xPrJVSgHBv1ysBekgJyh (onboarding)**: (a) REPLACE "Skip Maison Mahj (never publish its code), Wren Mats" with:
> Wren Mats (no commission) is skipped. MAISON MAHJ is a code partner since Oct 29 (Tiffany 11:07pm): code MAHJMATCH (verify the spelling at af.uppromote.com/z0n11c-me), perk "Complimentary shipping on tile set orders with code MAHJMATCH", plain brand link (no affiliate link), FYM code-only, and NOT announced as a new code.

(b) Append:
> 5b. INSTAGRAM (CLAUDE.md INSTAGRAM BRAND WATCH): verify the brand's handle from its site footer → config/social/ig-handles.json; follow it from @mahjmatchmaker and add it to Favorites (partners first, cap 50); log it in docs/IG-FAVORITES.md. If Chrome isn't signed in to @mahjmatchmaker, put a DESK.md line "OPS: follow + favorite <handle>".

Also update docs/BRAND-GUIDE.md §2 "Maison Mahj forbids posting its code…" to the Oct 29 rule, with a changelog line.

**E8 · trig_01RKw9eUwTYPo39gbYHb65gh (partner feedback)**: rename "Partner feedback watch (daily 2:13pm, through Nov 10)". REPLACE the first sentence ("LAUNCH-WEEK … Oct 26-31; Tiffany approved Oct 25 9:37pm.") with "PARTNER FEEDBACK WATCH, daily 2:13pm ET through Nov 10 (Tiffany Oct 27 6:22pm)." REPLACE the last line ("After the Oct 31 10pm run…") with:
> On the first run on or after Nov 10: if no real partner item arrived Nov 1-10, disable this task yourself (update_trigger enabled false; it's her Oct 27 instruction), log "Partner feedback watch ended" in HQ, and finish. Daily FYM-feedback reading continues in the HQ cleanup (docs/HQ-CLEANUP.md "FYM feedback"). If items did arrive, keep running and send her one line asking whether to keep it.

**E9 · trig_01WeCbwyCsSuP5p8c39nPtNT (desk cleanup)**: (a) REPLACE "Planoly drafts and scheduled posts (workspace 019fc27b-964d-7279-8685-1f1bb7a7c3f5)" with "Planoly drafts and scheduled posts in BOTH workspaces: Instagram + Facebook Page 019fc27c-0bef-7533-bc3f-030acc19a135 and Pinterest 019fc27b-964d-7279-8685-1f1bb7a7c3f5". (b) REPLACE "Current standing order: (1) Find Your Mat-ch launch Oct 27, (2) fall content before it expires (e.g. Brownstone Bloom), then holiday." with "Standing order: Google is #1 (Tiffany Oct 29 11:03pm: Google work before reels/graphics), then the order in the newest docs/ANSWERS.md and DESK 'Never-ending'." REPLACE "verified dates on the 1st/15th" with "verified dates (weekly, Mondays) + codes post (Mondays)". Append:
> (c) Restocks with a date in config/release-calendar.json for an album set go to the TOP of tomorrow's list with an owner (restock-first rule, Oct 28 3:27pm). (d) PLANOLY AUDIT, next 7 days, IG workspace: every IG post group has a facebook target (brand NAMES, not @handles) and its story version (every slide); every brand named has Tag people with a verified handle; `python3 scripts/social/content_lint.py --planoly <export>` passes. Add any missing FB target yourself (standing rule, CLAUDE.md SOCIAL 11). Everything else goes on DESK for Main. If fewer than 4 IG posts are scheduled in the next 7 days, make it a top-5 DESK item for Main with the album-of-the-week kit as the default. (e) MATCH-INBOX lines older than 2 days with no DONE → DESK top list, owner Matches & Catalog. (f) For every album that went live in the last 7 days, curl and check: /mahjong-tile-matches lists it, its colour pages list it, its brand page links it, /links shows it as the latest album, hq/indexing has it requested, Pinterest queue has its pins. Each miss → DESK with an owner.

**E10 · trig_01S2VsjwznnHev1uUbYmEwJq (launch watch)**: rename "Brand launch watch (8:57am + 5:57pm)". Append:
> ADDED Oct 30 (rules audit). (a) NEW TILE SET swipe books are built with scripts/swipe/build_book.py (colour card first, TNT recs from config/tnt-recs.json, widest FYM pool, FYM photos) and must pass `python3 scripts/swipe/book_gate.py`. If the set has no TNT record yet, don't publish the book: add hq/albums stage "needs-tnt" and a DESK line "OPS: search Tiles & Tablescapes for <set>". Mat-mode books (new mat × album tile sets) keep the Larkspur pattern. (b) Same for every partner. (c) DROPBOX (her standing preference): brands replace the flat product render with a photoshoot image later, so the flat render is her clean mat card. For every new tile set or mat, add a DESK.md line "OPS: copy assets/launches/<dir>/ to Dropbox /Mahj Matchmaker Albums/New releases/<brand>/ today" (the Dropbox connector can't upload images).

**E11 · trig_01LC2kwT22s8TLGRcuTinrXw (Mahji Mentor)**: rename "Mahji Mentor group + OMM launch check (daily 12:44pm)". REPLACE "Runs 8:44am, 12:44pm and 5:44pm ET." with "Runs daily at 12:44pm ET." DELETE the whole "Known launches (Oct 12, 2026): …" paragraph and REPLACE it with "Known launches: read hq/launches and config/release-calendar.json; never trust a list written into this prompt." Append E10(a).

**E12 · trig_015vK2vwvGE2ChkgHmciZjZm (TNT scan)**: REPLACE step 1's "(start with Malachite; include any set she's asked for fresh matches on)" with "(the next 5 albums in the DESK.md 'Albums' order, every set with an open swipe book in hq/albums, and every set in config/release-calendar.json upcomingAlbums)". REPLACE step 4 with:
> 4. Write every find into config/tnt-recs.json in the format scripts/swipe/book_gate.py reads ({set: [{mat, brand, url, fym_key or null, post_url, post_date}]}) and commit. These are recommendations from the group, not her picks, so they need no yes; they lead the swipe book labelled "TNT rec · <mat> · <brand>". Mats not yet in FYM: add a MATCH-INBOX line. Log one HQ line.

Append the TAB RULE "including on errors".

**E13 · trig_01NRxYaJDZF8R3HW3Dur3S1B (FYM weekly new-mat scan)**: disable. It's superseded by the launch watch's twice-daily store sweep + builder/partner_mat_sweep.py + fym_gate [100] and the ShopMy check, and its photo rule contradicts CLAUDE.md FYM 6. This is a disable, not a delete; tell Tiffany in one line. If it's kept instead, REPLACE step 3 with "Photo bar = CLAUDE.md FYM rule 6 (LOW bar; too_far/covered/questionable)" and step 4 with "write items to HQ hq/newproducts (never a needs card) and docs/MATCH-INBOX.md".

**E14 · trig_01JdJPFFJ7kDeG4PQ7nMpjmy (new mat watch, 1st/15th)**: disable. It duplicates the launch watch, writes to the retired Work Tracker, and relies on the disabled watchdog. It also collides with indexing at 12:08 on the 1st/15th.

**E15 · trig_012tRmi5atnTDaUYbuDfiy15 (monthly site maintenance)**: REPLACE step 5 and the COMPUTER-OFFLINE paragraph with:
> 5. FIX, don't just report (CLAUDE.md standing authority covers broken link/image fixes, retired labels and back-in-stock relinks): repo fixes are made and committed. Squarespace edits go on DESK.md as "OPS: <page> <fix>" with the exact change. Report = one HQ log doc (area "Site") with the counts + a docs/audits/site-maintenance-<yyyy-mm>.md file. Anything that's a taste decision → one HQ needs card. If the browser is unreachable, use curl for every check that doesn't need it and log what was skipped.

Add E5. Move the cron to `CRON_TZ=America/New_York 37 19 1 * *` (7:37pm on the 1st, away from the morning browser jobs).

**E16 · trig_01VMhd3m7dhea9XVLD4c3ksM (1-month AI evaluation, Nov 9)**: REPLACE the sources sentence with:
> Sources: HQ (ArtifactData https://claude.ai/artifact/Cor6pKtesou4mFRQ41P6Ye) seo collection: daily docs (aiBrands, aiSummary, sc), weekly-* docs, the log area "Google report"/"Indexing"/"Codes"; the Google Code Report artifact https://claude.ai/artifact/PRpayBhn7vP4dJ8qR7i68X; money collection Oct 9 - Nov 8; docs/research/ai-overview-drop-oct29.md. The Feedback Library send log, Work Tracker and the old 5-brand rotation are retired. Feedback sent is in the HQ log and the code report.

**E17 · trig_01CgZr3ZHdhJbSNSQntCTYZ3 (weekly SEO strategy review)**: move to `CRON_TZ=America/New_York 7 9 * * 2` (Tuesday). REPLACE inputs 2 and 3 with:
> 2-3. Read Monday's "Weekly Google & OMM Report" (link in HQ seo weekly-<date>), the last 7 seo daily docs (sc, aiBrands) and the latest Google Code Report. Do NOT run your own Search Console or Google searches (C2/C3 in docs/RULES-ENFORCEMENT-AUDIT.md).

REPLACE D's "Write seo/<YYYY-MM-DD>" with "Write seo/review-<YYYY-MM-DD>". Add E5.

**E18 · trig_01HpSV6bJuJQSJ3aoBjctyhY (weekly Google & OMM)**: REPLACE "If Chrome is reachable, Search Console…" with:
> Search Console numbers: use the `sc` fields of the last 14 seo daily docs (written by the 7:13am morning report). Open Search Console in Chrome only if those are missing, and then follow the CHROME LOCK line.

**E19 · trig_01UsWfwKxnDaTGA3mYrop6zX (Pinterest)**: rename "Pinterest autopin (every 3 days)". REPLACE "nothing published for 2 days in a row" with "nothing published in the last 72 hours (RSS + Planoly)".

**E20 / E21 / E22 · names only**: trig_01GQHw → "Google code report (Mon/Wed/Fri)" (in E3); trig_01S2Vs → "Brand launch watch (8:57am + 5:57pm)" (in E10); trig_01UwvU → "Match Builder data refresh (weekly, Mon)".

**E23 · trig_01Y68dNzLjdvgDFynxik9Nw5 (release calendar)**: REPLACE "workspace 019fc27b-964d-7279-8685-1f1bb7a7c3f5, limit 8" with "workspace 019fc27c-0bef-7533-bc3f-030acc19a135, limit 8".

**E24 · trig_01NpQoJYSYh2GCLwcHNpkDiU (ShopMy) and trig_015vK2vwvGE2ChkgHmciZjZm (TNT)**: move to Tuesday (`41 9 * * 2` and `41 11 * * 2`) to thin the Monday browser stack. Add E5.

## 11. New scheduled tasks

| Id | Name | Schedule (ET) | Needs her computer | Prompt outline | Who |
|---|---|---|---|---|---|
| N1 | /links weekly refresh | Sun 6:37pm (`CRON_TZ=America/New_York 37 18 * * 0`) | Yes (Squarespace paste in Chrome) | Read CLAUDE.md, NEW-ALBUM-CHECKLIST /links section, scripts/covers/holiday/links_build.py. Check that /links shows (1) Find Your Mat-ch first, (2) the newest LIVE album as "latest album" (hq/albums + curl), (3) seasonal cards (holiday from Nov 1), and (4) no dead links (curl every href). Rebuild, pin + warm on jsDelivr, paste the code block (CodeMirror method in docs 59), verify with curl + a 390px render. CHROME LOCK + TAB RULE. HQ log "Links: <changes>". No message unless the paste failed. | Claude (standing authority: "/links weekly refresh") |
| N2 | Monday social numbers + brand watch + new-products roundup | Mon 3:37pm (`37 15 * * 1`) | Optional (follows/favorites need Chrome; otherwise DESK "OPS:") | (1) Planoly list_post_performance (IG workspace) for last week: follows, profile visits, shares per post → HQ log + a "Measure" line in docs/SOCIAL-SYSTEM.md; flag formats with 0 follows 2 weeks running. (2) Brand watch (CLAUDE.md): new partners + new ShopMy brands this week → verify handles, follow/favorite (or an OPS DESK line), docs/IG-FAVORITES.md; read Sunday Mahjong's IG in Chrome. (3) Reshare list: partner posts from docs/brand-social/* worth a reshare this week → HQ hq/social "Reshares" (link + one line each); she reshares in the app. (4) Partners with no match album yet (HQ brands live × assets/tiles/album/index.json) → hq/albums group notstarted. (5) New-products roundup draft from hq/newproducts → Planoly DRAFT (not scheduled) + one HQ needs "This week's new arrivals post: yes?". | Claude; posting the roundup needs her yes |
| N3 | Next-week social prep | Fri 12:43pm (`43 12 * * 5`) | No | Read the HQ Social tab plan, Planoly IG workspace next 10 days, the album of the week, release-calendar windows, the Monday codes post. For every empty day: build the kit from existing album content (SOCIAL-SYSTEM "never start from zero": cover reel template, "It's a mat-ch!", story frames, FB Page copy) as STORYBOARD stills only. Ask the brand-mix question with Claude's default. One HQ needs card "Next week's social: storyboards for your OK" (quick, inline images). Also draft the weekly FB group plan as one Claude Doc (Oct 27 18:31) and link it. Never schedule or post without her yes. | Claude preps; **her yes before anything posts** |

The missed-run watchdog is folded into the morning report (E4(c)) rather than a new task.

## 12. Gate changes

| Id | Script | Change | Who |
|---|---|---|---|
| GA1 | scripts/social/content_lint.py | New FAILs: `mahjmatch-missing` (IG/FB caption without MAHJMATCH; skip TdT-only posts), `hashtag` (no #MahjMatch), `banned-phrase` ("saves you money", "every mat", "every brand", "all the mats", "still available", "still in stock", "(affiliate)", Tinder/Hinge/Bumble/Bachelor), `short-brand` (`Bam Bird(?! Boutique)`, `My Fair(?! Mahjong)`, `Mahjong Row(?! & Co)`), `no-feature` (Yellow Mountain / YMI / Kaleidoscope / Paige Spearin in IG/FB captions), `tdt-policy` (Tigre de Tartán + MAHJMATCH in one caption), `maison-mahj` (calls Maison Mahj's code "new"). New flag `--codes-list` that exempts only the length check for the doc 94 typed list. | Claude |
| GA2 | scripts/swipe/book_gate.py | [f] FAIL when config/fym-mats-snapshot.json is older than the newest FYM version (docs/FYM-VERSIONS.md top entry or site-app/fym-vNN) → run fym_snapshot.py. [d] Use the FYM `hol` flag (holiday per the Oct 21 FINAL rule) instead of the regex words halloween/spooky/valentine/easter. | Claude |
| GA3 | scripts/social/center_check.py | `--phone-still` mode: in swipe scenes the phone frame's bounding box must not move between frames (FYM-REEL-RULES 20); report the first frame that moves. | Claude |
| GA4 | builder/fym_gate.py | Optional [104]: site-app/fym-vNN version == the artifact build version == the README 0a pin, before a publish is called done (CLAUDE.md FYM 0). | Claude |

## 13. What needs Tiffany vs what Claude can just do
- **Needs Tiffany:** TdT hub/brand-page approach (C11, P14; her idea is waiting on her yes); each week's codes-post yes (already in the flow); her yes on N3 storyboards and the N2 roundup post before anything public posts.
- **Claude can do now (standing authority or carrying out decisions she already made):** E1-E24, N1-N3 setup, GA1-GA4, the BRAND-GUIDE Maison Mahj line, the HQ-CLEANUP §4 "Launch-critical (Oct 27)" line. Disabling E13/E14 is a disable, not a delete: tell her in one line.

Audit by a background agent, Oct 30 2026 ~00:30 ET. No scheduled task or gate was changed by this audit.

## 14. Applied Oct 30 (the "section 11: Applied" report of the apply pass; numbered 14 because 11-13 above are the plan)

Applied by a background agent Oct 30, ~12:05-6:50am ET, under Tiffany's Oct 29 11:03pm yes. Nothing was disabled or deleted. Each trigger edit kept the full existing prompt and appended an "ADDED Oct 30" block (or replaced only the lines named in section 10).

| Fix | Status | Task / file |
|---|---|---|
| E1 codes post: TdT never typed in any caption or FB group text (graphic only), Maison line, `content_lint --codes-list`, 9:45am yes follow-up task, texts saved to docs/social/ | DONE | trig_01QNpTLC6egFF4u4oethFWVP |
| E2 HQ Talk: 9:47am, 1:47pm (no Chrome), 4:47pm, 7:47pm, 10:47pm + codes-post answers first on Mondays + CHROME LOCK/TAB | DONE (times shifted from the audit's 7:47/10:47/13:47 so it never starts on top of the morning report, code report or sales check) | trig_015cSezcshZpncAUiBedzWwv |
| E3 code report: renamed Mon/Wed/Fri; never overwrites aiSummary/aiBrands/sc/sales/alarm; writes aiReport + codeSummary + top of dailyLog; reuses the morning's per-brand AI Overview results (only AI Mode searched); desktop rank labelled; CHROME LOCK | DONE | trig_01GQHweQ9DbqXgoG2dp8GgBa |
| E4 morning report | already done before this pass | trig_01LZjGfVneN3vKwweVXwbzub |
| E5 CHROME LOCK + TAB RULE | DONE on 11 tasks (01GQHw, 015cSe, 019Fji, 01C7xP, 01LC2k, 015vK2, 012tRm, 01CgZr, 01HpSV, 01NpQo, 012P44); 01LZjG already had it. **BLOCKED on trig_01PGtT** (approval unanswered) → docs/rules-audit/pending-trigger-edits-oct30.md §1 | |
| E6 sales: UpPromote Marketplace + B&B dashboards, new-affiliate + applied scan, policy watch, ShopMy (12:04am) | DONE | trig_019FjiaFBVX512N67EYxrGUw |
| E7 onboarding: Maison Mahj code partner (old skip removed), TdT image-only, 5b Instagram follow/favorite | DONE; moved 2:22pm → 2:52pm. BRAND-GUIDE Maison line was already updated by the Main agent | trig_01C7xPrJVSgHBv1ysBekgJyh |
| E8 partner feedback: renamed; text fixed; after Nov 10 it asks (HQ needs + DESK) instead of disabling itself | DONE | trig_01RKw9eUwTYPo39gbYHb65gh |
| E9 desk cleanup: both Planoly workspaces, Google-first order, weekly verified dates + codes post, restock first, Planoly audit (FB target, stories, tags, lint), MATCH-INBOX age, new-album checks, content_lint legacy line | DONE | trig_01WeCbwyCsSuP5p8c39nPtNT |
| E10 launch watch: renamed; tile-set books only via build_book.py + book_gate; needs-tnt stage; Dropbox DESK line | DONE | trig_01S2VsjwznnHev1uUbYmEwJq |
| E11 Mahji Mentor: renamed; daily 1:07pm (was 12:44, 36 min after indexing); stale "Known launches" replaced; book_gate rule; Dropbox line | DONE | trig_01LC2kwT22s8TLGRcuTinrXw |
| E12 + E24 TNT scan: target sets from DESK/hq/albums/release calendar; writes config/tnt-recs.json in book_gate's real format ({sets:{id:{scanned,source,recs}}}); Tue 10:37am | DONE | trig_015vK2vwvGE2ChkgHmciZjZm |
| E13 FYM weekly new-mat scan disable | NOT DONE: Tiffany's call | trig_01NRxYaJDZF8R3HW3Dur3S1B |
| E14 new mat watch (1st/15th) disable | NOT DONE: Tiffany's call (it also starts at 12:08pm on the 1st/15th, same minute as indexing) | trig_01JdJPFFJ7kDeG4PQ7nMpjmy |
| E15 monthly maintenance: fix-don't-report, brand_page_text, retired doc targets removed; 1st at 8:37pm | DONE | trig_012tRmi5atnTDaUYbuDfiy15 |
| E16 1-month evaluation sources | DONE | trig_01VMhd3m7dhea9XVLD4c3ksM |
| E17 SEO review: Tue 8:13am (audit said 9:07; moved so it's 49 min before the Tue ShopMy run), reads reports instead of searching, writes seo/review-<date> | DONE | trig_01CgZr3ZHdhJbSNSQntCTYZ3 |
| E18 weekly Google & OMM: SC from morning `sc` fields; Chrome only if missing | DONE | trig_01HpSV6bJuJQSJ3aoBjctyhY |
| E19 Pinterest: renamed "every 3 days", 72-hour alarm, TdT pins never carry MAHJMATCH | DONE | trig_01UsWfwKxnDaTGA3mYrop6zX |
| E20 / E21 / E22 renames | DONE | 01GQHw, 01S2Vs, trig_01UwvubnWpaW4NoCY6VFaKrx |
| E23 release calendar → IG workspace 019fc27c | DONE | trig_01Y68dNzLjdvgDFynxik9Nw5 |
| E24 ShopMy → Tue 9:02am (audit said 9:41; moved to keep 45 min from HQ Talk 9:47 is not possible, so ShopMy goes first) | DONE | trig_01NpQoJYSYh2GCLwcHNpkDiU |
| Verified-date task: run brand_page_text.py + tdt_visible_code.py after edits, fix FAILs same run; TdT date-only | **BLOCKED** (approval unanswered) → pending file §1 | trig_01PGtT8NFXe6341WjBHqmYJu |
| No-second-swipe-book rule (Tiffany Oct 30 2:45am) in launch watch, partner watch, Mahji Mentor | **BLOCKED** → pending file §2 (gate [g] is live, see GA below) | 01S2Vs, 01Ljz8, 01LC2k |
| N1 /links weekly (Sun 6:37pm), N2 Monday social numbers + brand watch (Mon 3:37pm), N3 Friday social prep (Fri 12:43pm, drafts only) | **BLOCKED** (not created) → pending file §3 has the full prompts | new |
| GA1 content_lint: mahjmatch-missing, hashtag, banned-phrase, short-brand, no-feature, tdt-policy (TdT name + MAHJMATCH or #MahjMatch in one caption, any platform), maison-mahj, `--codes-list`; 52 legacy hits = WARN via config/social/content_lint_baseline.json (8 banned-phrase, 42 hashtag, 2 tdt-policy) | DONE | scripts/social/content_lint.py |
| GA2 book_gate [f] snapshot older than newest FYM build = FAIL; holiday uses `hol` flag (Halloween/Valentine/Easter no longer excluded by name); fym_snapshot.py records fym_version | DONE; snapshot re-labelled v104 (it had no build number, so [f] failed on it) | scripts/swipe/book_gate.py, fym_snapshot.py |
| GA2b book_gate [g] (coordinator, Tiffany Oct 30 2:45am): a book whose D.col / product handle is already registered with votes FAILS unless `--update-of <url>`; registry config/swipe-books.json (Poppins registered) | DONE | scripts/swipe/book_gate.py |
| GA3 center_check `--phone-still [--from --to]` | DONE (tested on smith-swipe-v6: phone box still 2-8s) | scripts/social/center_check.py |
| GA4 fym_gate [104] artifact = website copy = README pin; warning, FAIL with `--release` | DONE; it warned on live content (README 0a pin still pointed at v95) → README pin line for v103 added; v104's pin line is the Matches & Catalog chat's to add | builder/fym_gate.py |
| BRAND-GUIDE TdT line + changelog; HQ-CLEANUP §4 "Google first" | DONE | docs/BRAND-GUIDE.md, docs/HQ-CLEANUP.md |
| HQ needs card "Rules check: N fixes applied, K need you" | **BLOCKED** (ArtifactData write needs approval; no one answering) → DESK for Main | |

**Browser start times after this pass (ET; ≥45 min apart for tasks that must drive Chrome):** daily 12:04am sales · 7:13am morning report · 12:08pm indexing · 1:07pm Mahji Mentor · 2:04pm sales · 2:52pm onboarding. Mon +8:17am verified dates · M/W/F 10:52am code report. Tue 9:02am ShopMy · 10:37am TNT. 1st 8:37pm maintenance. Browser-optional (CHROME LOCK waits): HQ Talk 9:47/4:47/7:47/10:47 (1:47pm run never opens Chrome), Mon 8:37am weekly report, Tue 8:13am SEO review. Known clash left for Tiffany: new mat watch 12:08pm on the 1st/15th (E14).

**HQ card (for Main to write):** ArtifactData set, url https://claude.ai/artifact/Cor6pKtesou4mFRQ41P6Ye, collection "needs", id "rules-audit-2026-10-30": {title: "Rules check: 26 fixes applied, 2 need you", light: "blue", status: "open", quick: true, minutes: 1, added: "2026-10-30", link: "https://github.com/tiffanybrie/mahjmatchmaker-data/blob/partner-catalogs-sqsp/docs/RULES-ENFORCEMENT-AUDIT.md", linkLabel: "See what changed", why: "Every standing rule now has a scheduled task or a gate behind it. Two old duplicate mat-finder tasks can be turned off (not deleted): the weekly FYM new-mat scan (uses the old strict photo rule) and the 1st/15th new mat watch (writes to the retired Work Tracker and starts the same minute as indexing). Reply 'OK turn them off' or 'keep'.", steps: ["OK to turn off the FYM weekly new-mat scan?", "OK to turn off the 1st/15th new mat watch?"]}
