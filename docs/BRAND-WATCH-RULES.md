# 00000-A. FOUR MISSES FOUND BY TIFFANY, NOV 13 11:22am (BINDING; "If things are being missed, then we need to figure out why")
1. **Affiliate emails land in tiffanybrie@, which no unattended run can read** (the Gmail connector is mahjmatchmaker@ only). Missed there: Bespoke (Sheri Wood) BF terms Nov 13, CMC "Affiliate Sneak Peek" BF Nov 12, Bam Bird BF Nov 12, My Fair BF early access Nov 2. Until her Gmail forwards partner mail to mahjmatchmaker@ (her yes needed: OVERDUE), EVERY attended run with Chrome reads tiffanybrie@ (mail.google.com/mail/?authuser=tiffanybrie@gmail.com, search `(affiliate OR "black friday" OR "sneak peek" OR sale) (mahjong OR mahj) newer_than:3d`). A run without Chrome writes "tiffanybrie@ NOT READ" in its log.
2. **Partner affiliate emails ARE the sale source** (source_kind email) and decide the code line: write `affiliate_terms` (does our code stack? is commission paid?) on every BF/sale item. A sale our code can't be used with gets `nocode: true` (plain Shop button, no code line). Bespoke Nov 12-22: codes don't combine and sale items earn NO commission (resumes Nov 23).
3. **Copied product pages carry the old product's photos** (CMC Cabana = the-hunt-club-edition-copy showed Hunt Club). Every launch item gets its own `img`; site_brand_watch.py refuses a `-copy` page without one. Better photo beats a story screenshot (Glitter Glow red set from bespoke's CDN).
4. **ShopMy brands that make mahjong goods are watched like partners** (Rebecca Illustrated, Tala Mahj, The Mahjong House added to partner_launch_watch.py STORES Nov 13; Rebecca's Apres-Mahjong mat, new Nov 9, was missed).
Domino Blonde (TdT) was NOT missed: found Nov 9 1:30pm, on the page since; it lacked its own photo (fixed). TdT's newsletter is NOT read: signup blocked by hCaptcha Nov 8 (her 10s, OVERDUE).

# 00000. CATALOG ONLY, NO GROUP POSTS, NO YES-ASKS (Tiffany Nov 12 10:26am, BINDING; overrides 000.4, 00(b), 2(a-c), 4.4 and the task prompt's step 5 + "LIVE SHEET FIRST (b)")
"I'm not planning on posting all of these things in the group live as they go... You're basically bombarding me with yeses. Please don't do that."
- The watch CATALOGS: Brand Watch tab + Brand news sheet + release calendar + MATCH-INBOX/FYM queue. That's it.
- NO per-item Facebook group post drafts, NO "group post ready for your yes" messages, NO pushes for NOW items, NO "Do:" / "I did it" lines (brand_watch_hq.py strips every `action`; never add one back).
- The group gets the week through the Monday codes post only (links in comments; docs/FB-GROUP-STRATEGY.md). No one-off launch posts.
- Past dated drops leave "this week" automatically.
# 0000. BURY MAHJONG STUDIOS + SPLASH OF COLOR (Tiffany Nov 12 10:27am, BINDING)
"Bury them at the very bottom. They rank always last. Don't ever put them up front and center." brand_watch_hq.py moves every Mahjong Studios / Splash of Color line out of this week / just dropped / coming soon / sales to the very END of the last list. Same in any brand news list, sheet order or summary: they go last.

# 0-USAGE. HOW THE WATCH RUNS (Tiffany Nov 11 12:26pm, BINDING; overrides the task prompt's step 2 "EVERY partner handle")
- Model: the partner watch runs on Sonnet. Scripts do the routine work; Claude only reads what changed and writes the shopper-facing line.
- INSTAGRAM BY TIER: read config/ig-watch-tiers.json. Each run fetches only the tiers its time slot lists (A every run: biggest earners + social-first brands; B morning + evening; C midday). A brand with a dated launch/restock in the next 7 days is read every run until it drops. Keep the 26-hour window, so nothing between runs is missed for A/B.
- Planoly reads FEED posts and reels only, never Stories (Instagram doesn't share stories through that API). Brands that announce in stories also email/post; don't claim story coverage.
- ONE OWNER: this partner watch is the only job that updates Brand Watch. After editing config/brand-watch-curated.json run `python3 scripts/site_brand_watch.py && python3 scripts/site_brand_watch_preview.py`, publish site/livepatch/brand-watch/brand-watch-preview.html to https://claude.ai/artifact/18JAJeZRLcZtcqVejgKHMs (Artifact tool, same url), then write the sha stamp to site/livepatch/brand-watch/published.json. If a script FAILS (error / refuses on internal wording, missing date), fix the item it names and re-run; never publish around it; if it can't be fixed, say so in the HQ log line and the DESK.
- NON-SHOPIFY STORES (Tiffany Nov 11 3:04pm): every run also runs `python3 scripts/watch/nonshopify_watch.py` (Maven WooCommerce, Squarespace stores); each store it prints as NOT READ is opened in Chrome that run (one tab) and its products listed, or the run logs why it couldn't and the next attended chat does it the same day.
- PARTNER COVERAGE (Tiffany Nov 11 3:01pm): every run ends with `python3 scripts/checks/partner_coverage.py --hq <scratch>/catalog.json`, then ArtifactData set HQ hq/catalog from that file (read it first, pin if_version). New products a run finds must show up there as missing until they are in the app. Mondays: also check by hand the stores the snapshot can't read (Amanda Toppe, Soirée All Day, Wren Mats, Mah Jongg Maven, Mahjong by SI) and log new items in MATCH-INBOX.
- No separate brand-watch check-in task: NOW items are pushed to Tiffany by this run (section 00).

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
**Photos + fairness (Tiffany Nov 11 10:21-10:23am):** every partner card gets a photo (be fair: if Mahj Pit and OMM show pictures, Peace Love's clutches do too). Main page: ONE photo per brand card (its first item). Brand page: a photo on EVERY item we have one for ("a picture is worth 1,000 words"). Photo order: item `img` > snapshot > the live product page's own image > a teaser saved in assets/launches/. When a watch logs a find with no product page, save the teaser image and set `img` the same run.
**OMM leads (Tiffany Nov 11 10:22am):** an Oh My Mahjong tile launch day is ALWAYS the first card under Launching now (our biggest brand, the one we most want to rank for).
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

## News rank: what leads (Tiffany Nov 11 10:29am)
- A TILE SET always leads, travel sets included (big ticket; travel is only kept out of Find Your Mat-ch, not out of the news).
- Brand-new beats a restock of something everyone has seen. Every item shows a **New** or **Restock** badge so "Just dropped" is never ambiguous.
- Default order inside a brand: tile sets > new items > restocks, and racks > mats within each.
- Brands known for something get their own order in config/brand-known-for.json. Miss Mahjong: tile sets > new racks > rack restocks > mat restocks (her opal / brass / tortoise acrylic racks are in more demand than her mats).
- The item's `tag` decides its kind ("mats back, pair with Catrina tiles" is a mat). Mark `new: true` / `restock: true` in curated when the words don't say it.
- Coming-soon tile sets from the store (Shopify tag `coming-soon`) go on the watch the day they appear (missed: Miss Darling Lilac, on the store since Oct 20, added Nov 11).

## Customer-facing words only (Tiffany Nov 11 11:33am)
- `what` is what shoppers read: plain facts ("The Holly Berry holiday mat is in stock for holiday mahj. Jade Luxe racks are sold out."). Never brand-email or internal language: "pushing", affiliate, commission, draft, waiting on her yes, codes post, album day, teaser, sneak peek, FYM, we/our.
- Our notes (what to post, who approved) go in `action`, which is never shown.
- site_brand_watch.py refuses to build if `what` carries internal words (_INTERNAL).

## Sales, Black Friday, savings lines, timing, what counts (Tiffany Nov 11 11:37-11:42am)
- Section is "Sale", never "On sale now" (reads like "for sale").
- A sale usually replaces our code, so a sale shows ONLY on her yes (`approved: true`; `null` = asked, hidden). Never surface comment-for-link / DM-for-code discounts (Noli June FALALADIES: hidden, `hidden: true`).
- Black Friday is a standing yes (too big to hide): `bf: true` items get their own "Black Friday deals" section at the very top. A huge sale she approves (OMM warehouse-sale size) gets `big: true` and leads too.
- Under every code button: "Use code MAHJMATCH at <Brand> to save N%" from config/code-truth.json; Maison Mahj = free shipping on tile set orders; Tigre de Tartán gets no typed line (image-only code).
- Coming soon must say WHEN, or "No date yet" / "No name or date yet". Build refuses otherwise.
- Not drops: store openings, gift cards, in-store-only previews, brick-and-mortar news. Keep only the product news (e.g. Middle & Main's Summit to Sea under Coming soon).
- Know the product before writing it: open the product page (Noli June "Sue Adores a Scallop" is a $1,699 folding table, not a tablecloth).

## Ticker style is GOOD (Tiffany Nov 11 12:04pm, clarifying 11:33)
- The ban is only on brand-insider talk ("pushing", "here's what we want"). Timestamps and live status ("LIVE now since 4pm CT") are wanted: they show the page is current.
- Keep the history: when a heads-up turns into a drop, don't erase the heads-up. Put it in the item's `history` [{found, what}] (shows as "Earlier · <time>: ...") and make `what` the new status. It proves we warned people first.
- Tigre de Tartán: button says just "Shop" (code is image-only on the website).

## Where sales come from (Tiffany Nov 11 12:08pm)
- Never scrape a partner's SALE off their social (it bypasses our code: "working a little too hard for them"). A sale is a candidate only if the brand sent it to us (affiliate update / partner email), or it is huge public news (OMM warehouse sale, Black Friday). Record `source_kind`: email | social | store. Social-sourced sales stay hidden; the watch doesn't even ask.
- Buy links: an explicit `buy` always wins; the page never word-guesses a product unless the kind matches (tiles/mat/rack/table/tablecloth, travel vs full size). Two bad guesses found Nov 11: Noli June table -> tablecloth; Cabana Club full-size tiles -> a scratch-and-dent mat.
