# Brand watch rules (binding; read FIRST every partner-watch run; overrides the task prompt)

## 000. ONE FIND = FOUR WRITES, SAME RUN, NO CHECK-IN NEEDED (Tiffany Nov 10 10:32pm: "you can know a rule, but that doesn't mean that it's going to be followed or acted upon"; the hidden Brand Watch page is her test of whether we can keep up)
The partner watch runs on its own schedule. A find must NEVER wait for another chat's scheduled check-in. Every partner find, in the run that finds it:
1. **Sheet**: append a row to "Brand news (live)" (section 00). This is her scoreboard: found time, posted where.
2. **List**: add it to config/brand-watch-curated.json (this_week / coming_soon / just_dropped / sales) WITH `found` = when we found it, ET, `YYYY-MM-DDTHH:MM`, and bump top-level `updated` (Tiffany Nov 11 10:04am: every update timestamped, page shows 'Last updated', like a ticker). Page order (site_brand_watch.py): Launching now -> Just dropped (last 10 days) -> On sale now -> Coming soon; newest first; an item never shows twice.
3. **Page**: run `python3 scripts/site_brand_watch.py && python3 scripts/site_brand_watch_preview.py`, publish site/livepatch/brand-watch/brand-watch-preview.html to the Brand Watch artifact https://claude.ai/artifact/18JAJeZRLcZtcqVejgKHMs, then write the new curated sha256 into site/livepatch/brand-watch/published.json. If the run can't publish, the front door (every chat, every message) prints "BRAND WATCH PAGE IS BEHIND" until a chat does it.
4. **Push** (NOW items only): phone push to Tiffany with the draft group post (section 00/2).
Before ANY group / IG / FB post, the chat posting reads the sheet and puts every NOT POSTED item in (one group post a day; later finds are EDITS to it), then fills "Posted where".
The 9:55am "brand watch check-in" is only a safety net now, never the path.
**Tiles first (Tiffany Nov 11 10:14am):** a new tile set is bigger news than a mat or rack. When tiles and a mat launch together, the item's photo and Shop link are the TILE SET (the mat is the lesser player), and tile news leads its section (site_brand_watch.py sorts tile news first; `buy` must point at the tiles).
**Launches get the photo (Tiffany Nov 11 10:19am):** an upcoming tile launch (e.g. Mahj Pit Christmas tiles) is worth a photo even before the product page exists: save the brand's teaser to assets/launches/<brand>-<item>/ and set the item's `img`; it beats a rack/mat photo from the same brand.
**No brand dominates (Tiffany Nov 11 10:17am):** max 2 items per brand per section on the main page (tiles first), then '+N more · see everything from <brand>' to that brand's own page (#<brand> in the preview; /brand-watch/<brand> on the site). Every brand has its own page = the full list; the main page is fed from them. Big-inventory brands (Let's Be Besties, Splash of Color, Mahjong by SI): pick the best 1-2 to show, not the whole drop.
**Her test tab**: "Tiffany found it first" in the same sheet. When she sees partner news before we do, she logs it there (or tells any chat, which logs it). Claude fills "when we had it" + "why we missed it + fix" the same day and adds the fix (new source, new store in the snapshot, rule) so that miss can't repeat. Brand Watch goes public only when that tab stays empty for her test period.
**Every partner is watched**: scripts/checks/partner_checklist.py lists any partner whose store is not in the store snapshot (config/partner-products-snapshot.json): add it the same day (Nov 10: Mahj Pit, YOLO, Noli June, Maison Mahj, Mah Jongg Maven, Soirée, Wren, Amanda Toppe, Middle & Main were missing).

## 00. LIVE SHEET + PUSH THE MOMENT IT'S FOUND (Tiffany Nov 10 12:28pm; REPLACES section 0's "never messages Tiffany" for NOW items)
Why: Nov 10 the watch found Cabana Club, Mahj Mood flash sale and Tinselle Ruby at ~9:50am; Main's check-in had fired at 9:55 (before the 9:58 DESK write), the next was 1:55pm, and the 12:03pm group post went out without them. Brand news must NOT wait for a chat check-in.
- ONE live sheet: "Brand news (live) - read before every post" https://docs.google.com/spreadsheets/d/1Lm3mydRx3cXXYz9HTAkL2LLleQx8x5OrThr2IEXJRUM/edit (tab "Untitled", columns A-G: Found (ET) | Brand | News | When it happens | Posted where (group / IG / stories) | Draft | Notes).
- Every watch task (partner watch, brand launch watch, Mahji Mentor check) APPENDS each new partner finding the moment it is found (Google Sheets append_values, range "Untitled!A:G", one row per item; read A:G first and skip a brand+news already there; Posted where = "NOT POSTED"). Mahjong Row & Co., Yellow Mountain Imports and Paige Spearin x TdT never go in.
- When anything is posted (any chat or task), fill that row's "Posted where" (update_values) with where + time.
- NOW items (live today or within 48h): send Tiffany a push RIGHT AWAY in the same run (PushNotification + SendUserMessage): one line per item ("<Brand> <what> <when>") + the sheet link. Don't wait for any chat check-in.
- config/launch-actions.json stays as the machine copy (front door / launch_48h_check.py); keep writing it too.
- Every chat reads the sheet right before ANY post (group, IG, FB Page) and includes everything not yet posted.
- IF GOOGLE SHEETS TOOLS DON'T LOAD in a scheduled run (as of Nov 10 the cloud watch tasks' connector list has no Google Sheets): still send the NOW push (with the sheet link), append the rows to docs/status/brand-news-pending.jsonl (one JSON object per line, same 7 fields) and commit/push, and put a line at the TOP of docs/DESK.md "Main: append N rows from docs/status/brand-news-pending.jsonl to the Brand news (live) sheet NOW". Any attended chat that sees that file non-empty appends the rows to the sheet, empties the file and deletes the DESK line.

## 0. WHO TALKS TO TIFFANY (Tiffany Nov 10 8:02am: "I don't go to partner watch... They've got to report back to someone like you who then reports to me.")
(Superseded for NOW items by section 00 above: the watch now pushes NOW items to her itself, the same run.) The partner watch is a background worker. Apart from the section 00 NOW push, it does not message Tiffany. It writes:
- the list (config/brand-watch-curated.json + HQ Brand Watch tab),
- NOW items + their draft group posts into config/launch-actions.json ("drafted") and docs/social/,
- one line at the TOP of docs/DESK.md "Main: brand watch <time>: N NOW items ready (launch-actions.json)".
The MAIN chat reports to her: its front door shows every NOW item (scripts/checks/launch_48h_check.py), and Main checks in after each watch run (9:23am, 1:23pm, 6:23pm) and brings her the drafts for a yes.
Tiffany Nov 10 7:59am, after TdT Domino Blonde (caught Mon 1:30pm, drops Tue 4pm CT) was filed and never acted on:
"something that is launching today at 4 p.m. that gets caught the day before can't go on next week's partner launch document. So the partner watch has to understand dates and urgency... people are expecting us to do it for them... this is a test right now to see if you guys can actually keep up with how fast this world moves."

## 1. Every item gets a date and an urgency, every run
For each partner item found (store, email, Instagram): compute hours until it happens (drop / restock / preorder open / sale end) in America/New_York.
- **NOW: live already, or happening within 48h.** ACT THIS RUN (section 2). Never only file it.
- **SOON: 2 to 7 days.** Goes in this week's watch + the next Monday codes post if Monday is before it; if Monday's post already went out, it gets its own group post the day before.
- **LATER: more than 7 days or undated.** Watch tab + calendar only.
A Monday codes post that already went out does NOT cover anything caught after it. "We already posted codes" is never a reason to skip.

## 2. What ACT means (NOW items)
a. Draft a same-day FACEBOOK GROUP post: docs/social/<brand-slug>-<product-slug>-<date>.post.txt with the brand's own photos (assets/social/<brand-slug>-<product-slug>/), the drop time, buy links to the BRAND's product page with our code/affiliate link (never our own page), and the code typed: "use code MAHJMATCH to save X%". The Tigre de Tartán image-only rule is for the WEBSITE/Google only; in our own group the code and name are typed (Tiffany Nov 10 7:49am).
b. Add it to config/launch-actions.json as "drafted" (key = scripts/checks/launch_48h_check.py's key) so every chat's front door shows it until it is posted or she says skip.
c. Message Tiffany the same run: first line "<Brand> <product> drops <day time>. Group post ready for your yes:" + the text + photos. Day before AND morning of.
d. NO STORY FRAMES, REELS OR GRAPHICS unless Tiffany asks for them for that item (Tiffany Nov 10 8:01am: "you guys are then just immediately building a story frame, which I don't believe I ever told you to do... burning up usage... It's not, let's go build a story frame, but not tell Tiffany. That is absolutely out of order."). The list and the group post come first; she reshares brand content herself from the list.
No hype: never "goes fast"/"sells out"; "Set your alarms!" is fine.

## 3. Checks
- scripts/checks/launch_48h_check.py (front door, every chat, every message) lists partner items within 48h that are not posted/skipped.

## 4. Where everything goes (the flow)
Sources (3x daily): partner stores (products.json diff), email (mahjmatchmaker@ + tiffanybrie@), partner Instagram (Planoly), Sunday release page.
1. LIST FIRST: config/brand-watch-curated.json (this_week / coming_soon / just_dropped / sales), each with date, time, brand, what, buy link (brand page + our code), source link (their post, for her reshares), urgency NOW / SOON / LATER.
2. HQ Brand Watch tab (hq/brandWatch) mirrors the list. This is her social cheat sheet: brand post links she can reshare.
3. WEBSITE "Brand Watch" page (planned, Tiffany Nov 10): the same list, live, public; group + email list + page = where people get it.
4. GROUP: Monday codes post carries the week; NOW items caught after Monday get their own group post (section 2), on her yes.
5. Tiffany is told the same run for NOW items (one message: what, when, draft post). SOON/LATER: list only, no message.
Nothing else gets built automatically.
