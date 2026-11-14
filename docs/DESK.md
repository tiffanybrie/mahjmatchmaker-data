# The Desk

**BEFORE ANY POST (group, IG, FB Page): open the Brand news (live) sheet https://docs.google.com/spreadsheets/d/1Lm3mydRx3cXXYz9HTAkL2LLleQx8x5OrThr2IEXJRUM/edit (tab 'Brand news', range 'Brand news'!A:G) and include everything not yet posted; after posting, fill 'Posted where'. One post per day in the group: EDIT the day's post, never a second post (Tiffany Nov 10 12:28pm + 12:30pm + 7:39pm).**
**ALBUM LAUNCH TRACKER (her visible source of truth, Nov 10): https://docs.google.com/spreadsheets/d/18wyQ2mQ9epIIuDEyijYy86XAL4SEmtiVU06mzoWms6c/edit . Every chat that does a launch step fills its cell (date + proof link) the same turn. Process doc: https://docs.google.com/document/d/1vYacaqeyXufkly5aA1CGm-OwWxgqtGcx47x8WYy-qwc/edit**

Rewritten nightly by the end-of-day desk cleanup (9:23pm ET). The morning HQ cleanup (6:47am ET) reads it. Rules: CLAUDE.md ("THE DESK"), docs/CHATS.md. During the day, when an agent stops, Chrome drops or a QA stalls, add the item here right away with its next step.

- Main (was OPS) (launch watch Fri 11/13 5:57pm): copy assets/launches/brittmills-plumage-ii-leatherette-mahjong-mat/ to Dropbox /Mahj Matchmaker Albums/New releases/Britt Mills/ (flat product render = clean mat card). Target Sat Nov 14.
- Main (was OPS) (launch watch Fri 11/13 8:57am): copy assets/launches/letsbebesties-{bam-bird-aa-artist-collective-mahjong-mat,colorado-river-aa-artist-collective-mahjong-mat,miracle-lillian-claire-designs-artist-mahjong-mat,indigo-and-olive-lillian-claire-designs-artist-mah}/ to Dropbox /Mahj Matchmaker Albums/New releases/Let's Be Besties/ today.
- Main (was OPS) (Thu 11/12 sweep 12:58pm, needs Chrome + her yes): album launch email = TEMPLATE now (her 10:59am). On her yes in HQ need juniper-drop-2026-11-11: open Squarespace draft 6af357e97ff74f68f862d0ee, change line 1 to "The latest Oh My Mahjong set, Juniper, is here! 💚" and subject to "The Juniper album is live 💚" (page https://claude.ai/artifact/6vTx8YprmPvDd52YhyGorJ), send to All subscribers, check Sent first; mark template `new-albums` APPROVED in docs/EMAIL.md so every later album launch sends without asking. No yes = nothing sends.
- Main (her 11:04am): Work With page v3 is HELD (no hidden upload). After Brand Watch is fully set up, revise: partners FEATURED in FYM (no "we add non-partners", no "only partners"), New Releases & Restocks = we track + share their promotions with a Brand Watch link, drop the old Partner Brands card, use a few accurate brand tickers; then show her the revised draft.
- RULE (her Nov 12 11:00am): never send her to a repo file path in HQ; put the actual words or picture in the card.
- Main (was OPS) (launch watch Thu 11/12 6:10pm): copy assets/launches/brittmills-plumage-leatherette-mahjong-mat/, brittmills-mallard-manor-leatherette-mahjong-mat/ and brittmills-grayson-leatherette-mahjong-mat/ to Dropbox /Mahj Matchmaker Albums/New releases/Britt Mills/ today (flat product renders = clean mat cards).
- Main (was OPS) (launch watch Thu 11/12 9:05am): search Tiles & Tablescapes for Mahjong Studios Easter Morning + Some Bunny (new Easter tile sets; no colour card / TNT rec yet, so no swipe book).
- Main (was OPS) (launch watch Thu 11/12 9:05am): copy assets/launches/mahjongstudios-easter-morning-christian-mahjong-tile-set/ and assets/launches/mahjongstudios-some-bunny-easter-mahjong-tile-set/ to Dropbox /Mahj Matchmaker Albums/New releases/Mahjong Studios/ today.

**Last rewrite:** Fri Nov 13, 2026, ~9:45pm ET (desk cleanup run, cloud, no computer linked). Covers the 20 commits of Nov 13 ET (58129b4d morning HQ cleanup … 5ffead08 partner watch 6:30pm), docs/ANSWERS.md (Nov 13 lines 7:40am-11:22am), docs/OVERDUE.md, docs/MATCH-INBOX.md, Planoly (IG workspace 019fc27c…: **0 groups SCHEDULED Nov 14-20**; Deco (Lagoon) week built as drafts Mon 11/16-Sun 11/22 (5 feed + 7 story groups, every one with FB Page target, tags verified); 10 past-dated draft posts rolled forward to Sat 11/14 + Sun 11/15 tonight; export docs/social/planoly-exports/ig-2026-11-13-desk.json; Pinterest 019fc27b…: 27 pins Nov 14-20, 0 errors, Mahjong Row Cypress Forest pin still on Tue Nov 17 11:28am ET: unschedule BLOCKED unattended), HQ needs (Today 4, This week 7; no archive needed), hq/albums (97 items; 12 non-live album pages curl 404, none went live), Ready to Ship (no new answers).

**Owners (Tiffany Nov 11 4:41pm: ONE working chat):** **Main** owns everything (social/Planoly, site, email, HQ/DESK, Google + SEO, money decisions, Find Your Mat-ch, albums, gallery, catalog, search index, Chrome steps when her computer is on). **Ops (Sonnet)** = only money runs + Amazon-to-ShopMy link chores. The Matches & Catalog chat is RETIRED: any line below that still says "Main (was Matches & Catalog)" is Main's. Catalog gaps = scheduled task **Partner coverage owner (daily)** (trig_012DGkmgYqbH5ks6V9Dq9Ldz, 1:47pm ET).

**Statuses "Watch", "Ask once" and "later" are banned.** An open line leaves this page only with proof (ANSWERS DONE line, commit, or live URL 200); otherwise it moves to docs/OVERDUE.md with owner + next step + date. `python3 scripts/checks/desk_drop_check.py --commit HEAD` runs before every push.

**Repo note:** `partner-catalogs-sqsp` is huge (~6 GB pack at depth 50). `git fetch --depth=50 origin partner-catalogs-sqsp:refs/remotes/origin/partner-catalogs-sqsp` took ~8 min tonight (run it in the background with a 580s timeout; a killed fetch leaves a multi-GB tmp_pack_* in .git/objects/pack: delete it). Same root cause as the jsDelivr 403 below.

**PARTNER SEND GATE (Oct 27, standing):** before scheduling ANY partner email or graphics drop, run `python3 scripts/partner_send_check.py`; it must exit 0.

**NEW TODAY (Nov 10, ANSWERS):** PLAIN POSTS only (captions from scripts/social/plain_post.py, her voice + a little excitement, brand @tags at the BOTTOM, 'along with over N mats' line). ONE ALBUM A WEEK (config/album-launch-slots.json, gate [10c]; Cabana + Après-Ski = double album, week of Dec 7). Album model: READY (hidden page + every launch asset) then a dated LAUNCH (FYM complete first). Petalée = backup album. Deco albums may drip one per week. FYM SHIPS CONTINUOUSLY (rule 0b): no holding for 1.NN; partner launches in FYM BEFORE the drop. Never defer to "tomorrow". Brand watch = LIST + one group post (edits after), no graphics unless she asks; findings go to the Brand news sheet the moment they're found. Collab invites ONLY on that brand's own-product posts. Reels: 9:16, album cover as cover, a suggested song, segment length = her cut, text never edge to edge. Profile set ends on "But she likes to play the field" → FYM (FYM is the headline, not the album). Reel kit = album top 8 × 3 FYM views with each mat's own album racks; Canva Mats folder = ALL album mats. Never change an approved graphic when re-framing. TdT: type the code in our own group; link the BRAND's product page.

**Standing (Nov 4):** A YES IS A YES · BLOCKED IS NOT DROPPED · REVENUE WATCH · NO 'ASK ONCE' · SOCIAL 13 (nothing disappears from Planoly) · payouts are CASH via PayPal (Bam Bird = bank transfer), only Maison Mahj + PLM Level 1 are store credit · ShopMy pickup DAILY 9:02am · Chrome: no saved tabs · IG evergreen codes post = profile-only.

## Tomorrow's top priorities (Sat Nov 14), in order
Standing order: RESTOCK FIRST (rule c), then Google #1, then the newest ANSWERS (Nov 13: SEO description + visible verified line in BOTH places, TdT favourite = House Tigers Oyster, Brand Watch misses + BF roundups), then DESK 'Never-ending'. **Restock check (c): no album-set RESTOCK is dated Sat Nov 14** (next: Bam Bird Deco Indigo window opens Mon Nov 16, album not built yet = review page on HQ This week; Sunday Blues Nov 23-30).

1. **Google (Claude Duet owns the analysis; Main does the Chrome fixes). First thing.** Fri: signed-out cloud AI Overview names MAHJMATCH for **22 of 40** (Thu 15/40), OMM still NOT named; AI Mode 35/40 (scorecard a00f6233); laptop 34/40 is personalised. (a) Next M/W/F code report Mon Nov 16. (b) Indexing: 20 freshly re-dated pages queued Nov 14-15 (report d81b54dd). (c) Brand-page strengthening for the 6 dropped top earners waits on her yes (HQ alert card). (d) AIO source investigation: Bam Bird next (OVERDUE). (e) Main, Chrome: TdT hub 'Shop Tigre' link (drops the 10%; Tigre down 69%) + Britt Mills page still says neoprene restock 'late October' in 3 places (new, OVERDUE).
2. **Black Friday deals page, hard deadline Mon Nov 16 (Main, Chrome Sat/Sun).** Her yes Nov 8, still not live; PLM BF is Mon Nov 16, Bam Bird BF Nov 20-22, CMC Nov 27-30, Bespoke 11/12-22 (no code/commission). Brand Watch v26 already has the BF section: build the page from it (site/livepatch/black-friday-2026/README.md), and the Mon codes post carries PLM BF.
3. **Social, rule d (Main, attended): 0 IG posts SCHEDULED Nov 14-20 (5th night).** Drafts exist: Sat 11/14 'New this week' + 'Tap a color' + stories, Sun 11/15 'Tiles first or mat first?' + stories (rolled tonight), Deco (Lagoon) launch week Mon 11/16-Fri 11/20 (HQ card social-week-2026-11-16). Schedule ≥4 on her yes; fix the Wed reel FB caption (420 chars, lint limit 350) before Wed; Juniper It's a mat-ch! still parked Dec 9 ('post it'). **Pinterest: unschedule the Mahjong Row Cypress Forest pin (group 01a15fba-8fcf) before Tue Nov 17 11:28am ET** (blocked unattended tonight).
4. **FYM releases (Main): the jsDelivr 403 looks CLEARED** (coverage task, Nov 13 7:20pm: @de50c189 serves 200 twice). Ship 1.19 (Miss Mahjong racks + all walls + 5 retired OMM mats) now, curl the new pin first; then the coverage release (38 items, config/fym-partner-adds-nov12-coverage.json) + today's launch-watch mats (LBB 4 Artist mats, Britt Mills Plumage II) + plain-link conversions. Gate + independent QA + three places each.
5. **Newest asks + Match inbox (Main).** (a) Juniper email: her 'send it' (HQ Today). (b) FB group Sat 'Help me match' 9:30am ET on her yes (HQ Today). (c) Sweet Jojo: no approval by Fri → draft the follow-up for her yes (OVERDUE). (d) Brand Watch Nov 13 open items: Gmail forward (her yes), Rebecca Illustrated Après-Mahjong ShopMy link, Bam Bird BF stacking (ask only on her yes). (e) Mahjong by SI commission amount (Collabs, mahjmatchmaker@) is Claude's to read. (f) MATCH-INBOX: **125 dated lines older than 2 days with no DONE** (same as Thu) + 5 new Nov 13 lines: mark DONE or fold into release 4.

- **Tiffany's approved matches** (config/tiffany-matches.json): social picks come from this list FIRST.

## Handoffs (do first)
- **Found Fri Nov 13, given a home tonight:** Deco (Lagoon) week built as Planoly drafts (eb93df2d), not scheduled (priority 3); Wed reel FB caption lint FAIL 420 chars (OVERDUE); Pinterest Mahjong Row pin unschedule refused unattended (priority 3 + OVERDUE, now dated Sun Nov 15); Britt Mills stale 'late October' copy (OVERDUE); jsDelivr 403 cleared → 1.19 can ship (priority 4); 10 TdT-style two-date pages fixed by the Google report (live check PASS); TdT hub link still open (OVERDUE); partner watch 6:30pm git fetch failed in its cloud run (4 pending curated items in docs/status/watch-pending-2026-11-13-1830.json: next partner watch run merges them); launch watch: LBB 4 Artist mats + Britt Mills Plumage II → MATCH-INBOX + Dropbox lines at the top.
- **Found Thu Nov 12, given a home tonight:** Juniper email send blocked by the safety check (HQ Today #2 + OVERDUE); partner coverage release stopped at STAGED (38 items, jsDelivr 403; OVERDUE); Juniper practice reels A/B/C built, not yet picked (priority 4h); TNT code list PDF needs her download OK (priority 4f); Reddit replies blocked (priority 4g); Pinterest Mahjong Row pin Nov 17 (priority 2 + OVERDUE); Deco Lagoon hq/indexing row ADDED tonight; Cabana album re-statused (tile-photo sample never sent: OVERDUE line); Charleston still owes $115.65 (In progress).
- **Launch watch Thu 11/12** (9:05am + 6:10pm): Mahjong Studios Easter Morning + Some Bunny (tile sets, on Albums tab as needs-tnt), Britt Mills Plumage / Mallard Manor / Grayson leatherette mats (handed to FYM); Splash Gilded Dynasty recorded only. Dropbox copies = the OPS lines at the top.
- **Stories Thu 11/12 12:37pm**: Mahj Mood Lake Day tiles (drop 11/20) + 6 new wooden rack colours (end Nov): record; Lake Day = new product (FYM on the day), not an album unless she says.
- **Found Wed Nov 11, given a home tonight:** Juniper launch passed with no IG post (priority 2); Juniper email send unconfirmed (HQ Today #2); OMM VIP post drafted for Thu (priority 4a); 2 new lint FAIL kinds (OVERDUE); Deco Lagoon hq/indexing row (priority 1b); App icon options + usage report built (b9828ecb) wait her look (HQ This week).
- **Launch watch Wed 11/11 6:05pm ET**: NEW Mahj Pit The Raven Tiles - Large ($395 tile set; likely the Nov 7 'Full Sizes Black' placeholder, which is gone) + 7 new partner mats (Mahj Pit Birds of a Feather / LaMarie / Evergreen; LBB Confetti Kaleidoscope, Sedona, Cajun Christmas, Blueberry Hill). Sheet rows (Raven + Confetti Kaleidoscope; the rest were already there) + NOW push sent; MATCH-INBOX lines for FYM; Raven on Albums tab as needs-tnt. OPS: search Tiles & Tablescapes for Mahj Pit The Raven Tiles. OPS: copy assets/launches/mahjpit-{the-raven-tiles-large,birds-of-a-feather,lamarie-mat,evergreen-mat}/ and assets/launches/letsbebesties-{confetti-kaleidoscope-ohbon-studios-artist-mahjong-ma,sedona-lillian-claire-designs-artist-mahjong-mat,cajun-christmas-lillian-claire-designs-artist-mahjong-mat,blueberry-hill-lillian-claire-designs-artist-mahjong-mat}/ to Dropbox /Mahj Matchmaker Albums/New releases/<brand>/ today. Also recorded only: Mahj Pit Commuter Christmas (travel tiles), 3 Splash of Color engraved tile sets.
- **Launch watch Wed 11/11 9:15am ET**: 6 new partner mats live (Mahjong Register Poppy & Prep / Tangerine & Twist / Blaire & Briar / Rosewater & Wine; Let's Be Besties Sleeping Tiger + Chinoiserie Cabbage Plates). Sheet rows added + push sent; MATCH-INBOX lines for FYM; no group post drafted, no swipe books built (non-OMM, waits its turn). OPS: copy assets/launches/mahjongregister-{poppy-prep,tangerine-twist,blaire-briar,rosewater-wine}-double-sided-neoprene-mahjong-mat/ and assets/launches/letsbebesties-{sleeping-tiger,chinoiserie-cabbage-plates}-wanda-viola-artist-mahjong-mat/ to Dropbox /Mahj Matchmaker Albums/New releases/<brand>/ today.
- **Main: Juniper launch kit** (priority 2). Reel files: assets/social/juniper-launch/reel/ (phone segment 16.0s), end frame MP4 (Canva Juniper folder), cover assets/covers/albums/reel-tall/juniper.jpg, caption assets/social/juniper-launch/reel-dating/ig-caption.txt (lint length FAIL, see priority 4).
- **Main: FYM racks-only release** (Miss Mahjong 5 acrylic racks; builder/fym_fix_nov10/racks119_missmahjong.py + release119.py; config/fym-rack-adds-nov10-missmahjong.json): blocked only by the jsDelivr 403 (priority 3). Version numbers: racks-only = **1.19 = site-app/fym-v119**; the staged bundle (Deco Lagoon, link routes, LBB Artist Collective 174, Mahjong Register relinks, racks119.py …) = **1.20 = site-app/fym-v120** ON TOP of 1.19, and per rule 0b each piece should ship as its own small release, not one bundle.
- **Main (was Matches & Catalog): Cabana Club tile set staged** (config/fym-adds-nov10-cabana.json, walls #91cad6, coordinated mat; u = SHOPMY_PIN_PENDING until the ShopMy pin exists). Swipe book https://claude.ai/artifact/XRpLKsiby4hFpvVQUMNcVM (book_gate PASS) waits her tile-photo yes + swipes. Double album with Après-Ski, slot week of Dec 7, ready by Fri Dec 4.
- **Main: Brand Watch website page** (OVERDUE, her 8:01am ask): preview artifact https://claude.ai/artifact/18JAJeZRLcZtcqVejgKHMs (scripts/site_brand_watch.py). Her 7:55pm brainstorm (photos/collage, hot vs minor, grouping by brand, consistent shop links, partner self-serve idea; partner vs non-partner open, lean like FYM): fold into v2 and show her; not on social yet.
- **Main: reel end frames**: scripts/social/animate.py (MP4 end frames for Canva) "not yet run to completion" (526f4d24): finish it for the next album (reusable per set).
- **Main: Juniper subscriber + album-requester emails**: Juniper list email is the draft above; the album-REQUESTER email (people who asked for Juniper) is still to send (docs/NEW-ALBUM-CHECKLIST.md 3-4).
- **Main: Mahjong by SI onboarding** (approved Nov 9): code-truth, brand page, hub, FYM, IG, newsletter. Not started.
- **Main: Partner feedback watch** trig_01RKw9eUwTYPo39gbYHb65gh ended its planned run Tue (0 real partner items Nov 1-10). HQ card partner-feedback-watch-end asks her OK to turn it off; on her yes, update_trigger enabled=false.
- **Main: HQ page bug** 'TypeError: rc.forEach is not a function' (since Nov 9 12:47pm, 2 sessions Tue): guard with `Array.isArray(rc) ? rc : Object.values(rc||{})` in the {path, why} link list and republish HQ (read the saved HTML first).
- **Main: TNT scans not merged**: project docs '81b TNT scan Nov 3' + '81c TNT scan Nov 10' hold JSON for config/tnt-recs.json (target Sat Nov 14) (Nov 10: 15 mats for 5 sets incl. Deco Mulberry 25-comment thread, Sunday Blues Tala Midnight Wildflowers): merge, dropping mats already in a book.
- **Main: hq/launches** is ~248 KB of the 256 KiB cap: archive pre-Oct 25 items before the next add.
- **OPS (Chrome)**: see priority 5 for the order. Plus: follow + favorite @mahjonggmaven + @mahjpit.co (docs/IG-FAVORITES.md); Payout Tracker September check; copy flat renders to Dropbox (LBB Artist Collective 174, Let's Golf! ×2, Cabana Club tiles + mat, Fait à Main Texas Mon Amour, LBB Tidal Glass / Seasons / Nutcracker / Tropical Travels, Bam! teaser, Soirée Holiday Chintz, Wren Gingham and Wine).
- **Main: older handoffs still open**: blog posts that name album tile sets without linking them (list in git show 09006524:docs/DESK.md); revenue-alert cards → one Money summary; prompt fixes (sales-check mails, "close leftover tab groups", mat-edit-alert step, "wholesale customers only"); config/pinterest/queue.json vs Planoly resync; Mahj & Moon 'pending_fix' when the 7 Etsy ShopMy links land.

## In progress
| Item | Owner | Next step | Target |
|---|---|---|---|
| Google: 4 lost AI answers (Bam Bird, Virora, Bespoke, I Love Mahj) + OMM/My Fair/PLM/Mini Mahjer | Claude Duet (analysis) / Main (Chrome fixes) | Indexing re-requests in that order; Bam Bird revenue investigation. | Sat Nov 14 (slipped since Wed Nov 11) |
| Google code report + scorecard | Claude Duet (Google owner since Nov 12) | Fri ran: AI Overview signed-out 22/40, AI Mode 35/40 (a00f6233); next M/W/F run Mon. | Sat Nov 14 (slipped from Fri Nov 13) |
| Indexing: 23 changed brand pages left + Deco Lagoon row | Main / Ops | ~10/day; Lagoon row ADDED Nov 12 night (request indexing at its social launch). | Sat Nov 14 (slipped from Fri Nov 13) |
| Juniper launch day | Main | Tiles + Lotus Cove LIVE Wed 10am CT. Left: IG It's a mat-ch! + story (parked Dec 9 slot) on her 'post it', email send on her 'send it' (HQ Today #2), requester email. | Sat Nov 14 (slipped since Thu Nov 12) |
| jsDelivr 403 → slim asset host | Main + Main (was Matches & Catalog) | Priority 3; curl new pins. | Sat Nov 14 (slipped since Wed Nov 11) |
| FYM racks-only release (Miss Mahjong racks) — OVERDUE | Main | After the 403 fix: gate + independent QA + three places. | Sat Nov 14 (slipped since Wed Nov 11) |
| FYM small releases: holiday-off mat-door bug, Lotus Cove photo, Cabana, Deco Lagoon m-list, Register links, LBB Artist Collective | Main (was Matches & Catalog) | One small release each, same day as unblocked. | Sat Nov 14 (slipped from Thu Nov 12) |
| Search index rebuild (03402daa staged, NOT pasted) | Main (was Matches & Catalog) / Ops | Paste with the next gallery/FYM release. | Sat Nov 14 (slipped from Thu Nov 12) |
| Dear Santa push + holiday album reels (OVERDUE) | Main | Dynamic style; schedule auto-publish. | Sat Nov 14 (slipped from Thu Nov 12) |
| Brand Watch website page (OVERDUE) | Main | v2 from her brainstorm; her look; hidden page via Chrome. | Sat Nov 14 (slipped from Thu Nov 12) |
| Black Friday deals page (her yes Nov 8, OVERDUE) | Main (Chrome) | README steps 1-6; index; link. | Sun Nov 15 (hard deadline Mon Nov 16) |
| Match inbox: ~96 unmarked lines | Main (was Matches & Catalog) | Mark DONE or fold into a release. | Sat Nov 14 (slipped from Thu Nov 12) |
| Sunday Blues album (TNT redo first) | Main (was Matches & Catalog) | Album Playbook; launch slot = its ~Thanksgiving restock week. | Fri Nov 20 |
| Deco Mulberry + Indigo (may drip one per week) | Main (was Matches & Catalog) | Re-pull + discovery with the Nov 8 + Nov 10 TNT leads; slot each. | Sat Nov 14 (slipped from Fri Nov 13) |
| Cabana Club + Après-Ski double album | Main (was Matches & Catalog) | Her tile-photo yes + swipes; ShopMy pin. | Ready by Fri Dec 4 |
| Rackin' Rudolph cards → her Canva tile photo (OVERDUE) | Main (was Matches & Catalog) | Lock crop, re-render 36, paste. | Sat Nov 14 (slipped from Thu Nov 12) |
| Holiday completeness audit (year-round album pages) + yes-vs-live check (OVERDUE) | Main (was Matches & Catalog) / Main | OVERDUE lines. | Sat Nov 14 (slipped from Thu Nov 12) |
| Album wiring gaps (C1: 7 live albums not wired to FYM) | Main (was Matches & Catalog) | Gap audit C1. | Sat Nov 14 (slipped from Thu Nov 12) |
| Mahjong by SI onboarding | Main (+ Ops) | Code-truth, page, hub, FYM, IG, newsletter. | Sat Nov 14 (slipped from Thu Nov 12) |
| Mah Jongg Maven onboarding (page live; code-truth done tonight) | Ops / Main (was Matches & Catalog) | Hub logo, IG follow/favorite, FYM. | Sat Nov 14 (slipped from Thu Nov 12) |
| FB group week (Thu table thread, Sat help-me-match) | Tiffany yes → Main (Chrome) | Thu passed with no yes (rolls to Thu Nov 19); Sat 9:30am on her yes (HQ Today #4). | Sat Nov 14 |
| New arrivals carousel (Thu 11/12) | Tiffany yes → Main | Draft 01a1c214 in Planoly; schedule on yes. | Sat Nov 14 (slipped from Thu Nov 12) |
| Work With v3 + Brands form | Main | HELD by her Nov 12 11:04am: revise after Brand Watch is fully set up (see top Main line), then show her. | Brand Watch done (target Fri Nov 20) |
| Planoly roll-forward + story-caption fixes | Main (attended) | Unattended update_post refused (7th night); this run made no Planoly writes (no FB target missing). | Sat Nov 14 (slipped since Wed Nov 11) |
| ManyChat comment-for-links draft + trial reminder (OVERDUE) | Main (Chrome) | Low priority. | Sat Nov 14 (slipped from Fri Nov 13) |
| Discount links not converted (Britt Mills, Register, YMI, RMS, Hip Hip, Wren/Soirée/Amanda Toppe) | Main | Fold into link-routes; convert in the coverage release (OVERDUE PLAIN LINKS line). | Sat Nov 14 (slipped from Fri Nov 13) |
| PEACE LOVE → Level 2 ($5K/month → cash) | Main | Plan + PLM MTD in the report. | Sat Nov 14 (slipped from Fri Nov 13) |
| Affiliate applications: Haus of Charleston, Lemondrop, The Mahjong House, Bloomjong, Sweet Jojo | Partner watch | Watch mahjmatchmaker@; onboard on approval. | On approval |
| UpPromote accounts → mahjmatchmaker@ | Tiffany / Main | Screenshots before each switch. | Sat Nov 14 (slipped from Fri Nov 13) |
| Google core update response (brand pages, indexing, AIO sources) | Main | Fri code report; re-requests; brand pages on her yes; AIO sources Bam Bird next. | Sat Nov 14 (slipped from Fri Nov 13) |
| Album launch email template (approved Nov 12 3:58pm) + Juniper send | Main | Send on her 'send it'; from the next album on it sends on launch day without asking (docs/EMAIL.md). | Sat Nov 14 (slipped from Fri Nov 13) |
| Launch-row format test (Juniper practice reels A/B/C) | Main | Show her A/B/C (assets/social/juniper-reel/practice-nov12/) for a pick; nothing posts before her pick. | Sat Nov 14 (slipped from Fri Nov 13) |
| Charleston payout owed $115.65 (Oct 23 + Nov orders) | Ops (money run) | Watch the next CMC payout; flag on HQ Money if not paid by month-end. | Mon Nov 30 |
| Affiliate outreach: Fun Fun Mahjong + 11 TNT brands (hq/applyList) | Main | Filled-in script per brand (her copy, hq/snippets outreach-general) shown for her yes; send only after it. | Sat Nov 14 (slipped from Fri Nov 13) |
| Deco (Lagoon) social launch week (drafts built Nov 13, eb93df2d) | Main (attended Planoly) | Her look in Planoly; schedule each on her yes; Wed reel needs her song (At Last) by hand; fix Wed FB caption length; re-add the Deco card to /links on launch day; request indexing. | Mon Nov 16 |
| Britt Mills page stale copy ('late October' neoprene restock, 3 places) | Main (Chrome; standing authority) | Edit the brand page code block to current stock wording; live_codes_check PASS. | Sun Nov 15 |
| Partner watch 6:30pm cloud run: git fetch failed | Partner watch task | Next run merges docs/status/watch-pending-2026-11-13-1830.json (4 curated items) into Brand Watch. | Sat Nov 14 |
| Mahjong by SI commission (Fri) | Ops (money run) | Read the Collabs dashboard (mahjmatchmaker@) and fill the money doc. | Sat Nov 14 |
| Instagram engagement task (daily 2:23/5:23/8:23pm) | scheduled task | Standing likes; daily list as one message; Chrome-closed message once a day. | Daily |

- REVIEW WEEK Dec 7-10 in Planoly (Tiffany Nov 9 1:09am): parked feed posts + single-frame stories. Real date = Dec date minus 28 days. Before Dec 6 EVERY one must be moved back (approved) or unscheduled, or it auto-posts. Owner: Main + nightly desk cleanup.

- Main: DECO LAGOON SOCIAL LAUNCH week of Mon 11/16 (Tiffany Nov 11 9:12am: true launch for social; album page already live). Build the Juniper-style kit: intro carousel (profile cards) -> It's a mat-ch -> reel + cover (FYM phones top 8, album racks), every-slide stories, FB Page targets, Planoly drafts; per-album Canva folder. Deco card was taken off /links Nov 11: re-add it (site/livepatch/links-nov11/README.md) on launch day.
## Blocked, approved (raise at the top of every attended reply until done)
- **Every new site pin (jsDelivr 403, repo over 50 MB)**: FYM racks release, FYM fixes, gallery, search, album images. Priority 3.
- **Planoly roll-forward + story-caption fixes**: unattended update_post refused (7th night, Nov 10). Attended Main: past-dated drafts (Mon 11/9 FYM how-to 01a1b20c + story 01a1b20d-690f = Papaya, held for rebuild per her Nov 9 1:15am call; old Nov 4-8 multi-frame story drafts 01a1a2b6-7c27/-73c7/-7717/-7a6d are superseded by the single-frame review-week stories: ask her once whether "superseded" = remove).
- **Chrome-only steps approved by her** (Today-in-mahj 11/10 edit, Black Friday page, Charleston + TdT link swaps, holiday blog lead image, Mahjong Row blog sentence): Chrome offline most of Nov 9-10.
- **Partner newsletters, 9 stores block automated signup (Shopify hCaptcha)**: Amahj, Bam! Let's Mahjong, Mahj Mood, Let's Be Besties, Mini Mahjer, My Fair, The Mahjong Press, Tigre de Tartán, Splash of Color. Her ~10s each on her phone; then mark docs/PARTNER-NEWSLETTERS.md.
- **Bing Webmaster Tools** (her yes Nov 6): one tap from her on Google's account chooser (OVERDUE line has the steps).
- **The Mahjong House affiliate**: her click on Confirm in their UpPromote verify email.

## Waiting on Tiffany (only things she can answer now)
**On HQ Today, in this order (4):**
1. **Google + sales alert (Nov 13): the plan card** (OMM still not named in signed-out AI Overview; Thu 4 orders vs 14). Includes the OK to add her own matches + photos to the 6 dropped brand pages (Bam Bird, Anders Ruff, Peace Love, Charleston, OMM, Britt Mills).
2. **Juniper email: type 'send it'** (template approved, draft fixed) + 'post it' for the Juniper It's a mat-ch!.
3. **Facebook group intros + OMM VIP post: her wording in the Google Doc.**
4. **Facebook group: Sat 'Help me match' (9:30am ET Sat Nov 14): one yes.** Text is typed out in the card.

**Closed since last night:** amounts-2026-11-13 DONE (she sent 8 screenshots 9:22pm; only Mahjong by SI left, Claude's job: In progress). My Fair Nov 12 amount filled ($0.00) from the same batch.

**On HQ This week:** Deco Indigo + Mulberry review pages; Holy Mahj full Canva image; Quick calls from Sunday (defaults in place); ShopMy 6 quick calls + 2 stray links; 1 hidden FYM photo (Grace Peacock); this week's posts in Planoly (rolled to Sat/Sun); NEXT week's Deco (Lagoon) drafts in Planoly; Fait à Main affiliate link paste.

**Asked in chat, not yet answered (the owning chat RE-ASKS at the top of every reply, with its default):**
- Main (was Matches & Catalog) (Nov 10): OK to delete the separate 'Today in mahj, part 2' group post now that the 11/10 post was edited to include it (default: leave it; deleting needs her yes); Cabana Club tile photo yes + swipes; Juniper reel swipes re-timed to the beat if she gives timestamps.
- Main: Holly Jolly Red grid + Dear Santa reel v3 (Nov 9 11:23am; default: schedule both once she says yes); remove the old launch-reel draft + dropped Rudolph/Polo/Rattan drafts (default yes, archive record); 84 locked FYM colour changes (default apply); hide /bird-and-bamboo-discount-code-2 (default hide); Malachite how-to reel v2 OK + day; pinned reel v3 A or B; Brand Watch page partner vs non-partner (lean: like FYM).
- Main (was Matches & Catalog) (older): Seabreeze × LBB Aloha card into FYM m-lists? (default no); Lagoon + Mulberry splits vs new pile photos; Bam Bird Classic Tortoise match pick; Sunday Rattan = Blue Rattan?; Fruit Stand rack-edge (default a); brand-lock pricing (undecided, don't push).

## Banked (finished, held on purpose)
- **Noli June + CMC Cabana Club group-post drafts (Nov 12 morning)**: superseded by her 10:40am FB group strategy (no one-off launch posts; links in comments). docs/social/noli-june-margo-rebecca-tiles-2026-11-12.post.txt + cmc-cabana-club-2026-11-12.post.txt: reuse inside the weekly brand post.
- **Favorite Things visual board (Nov 12)**: assets/social/favorite-things/favorite-things-board.jpg (15 items) for the gift-guide blog/social in December.
- **OMM Nantucket restock frames (Nov 9)**: assets/social/restock-nantucket-nov09/out/nan-A/B/C (live FYM screens); same-day window passed, HQ card archived (rule 9). Reuse at the next Nantucket restock/reshare.
- **Holiday album grids + 10s teaser reels (Nov 9 1:31am)**: assets/social/holiday-album-grids (11 albums): the base for the dynamic rebuild (OVERDUE line); not for use as-is (her 1:37am: must be dynamic + sell).
- **Juniper eye-candy grid**: full-mat version POSTED Nov 9 12:30pm (IG + FB Page + story); close-up version rejected.
- **Style of Your Life (My Fair Mahjong) album**: round 1 built Nov 7 (22 cards, site/livepatch/mfm-style-of-your-life-album-nov07); SKIPPED for now (her Nov 8 10:11am 'Skip My Fair Mahjong album for now'; set dropped Nov 7, Dillard's exclusive).
- **Deco review pages Nov 8 10:45am (Mulberry 8V74MMkepN9TnVCF5cRNAw, Indigo 9VjoeB1ejRB3wVvnMaKMqH)**: OUTDATED by the Nov 8 TNT/Silk redo; replaced in place when the re-pull is done. Don't send these links.
- **Petalée (Virora)**: 61 cards, RTS `l-final-petalee`, vault (her Oct 28). Nov 10 12:20pm: BACKUP album (a gap week, a Virora Petalée restock, or spring). Before publishing: colour card, 10% band sweep on the Amanda Toppe/Girly cards, cleaner Petalwing/Coralia photos. Table-view walls now staged (1.18).
- **Wren Christmas Village restock (Nov 8)**: first batch, reshare window passed; HQ card archived (rule 9).
- **Restock frames Nov 7**: Pearlescent (assets/social/restock-pearlescent-nov07/out/) + Florielle (assets/social/restock-florielle-nov07/out/): not posted; reuse at the next restock/reshare.
- **Launch reel redo (spotlight, no Mahjong Row)**: Planoly reminder 01a1b30e-67a2, superseded by the pinned reel 01a1b83b-fc22 (v2 in Planoly, v3 A/B built Nov 8); re-ask to remove.
- **Mahjong Row & Co. fall album**: parked (brand OUT, Nov 6). Parked site copy: archive/mahjong-row-parked-2026-11-06. MR mats may still enter new albums on merit (Nov 7 7:01pm).
- **Holiday intro reel v5** (46s): POSTED Nov 3; the reference standard for FYM reels (FYM-REEL-RULES 23-41).
- **Retro Rattan holiday table reel + 7-frame story**: undated Planoly drafts (01a16477-0588, -078d). Mood-board/table reels DROPPED (Nov 6 4:11pm).
- **Night of the Raven mood board reel + Halloween story + old Raven carousel**: next Halloween (docs/planoly-archive/2026-11-03-deleted-drafts.json).
- **Vivienne mat album (OMM)**: 16 cards, parked (no mat albums, Oct 23); its hearts go into the tile albums.
- **Season 2 tile-dating episode reels (Ep 1-13 + trailer)**: PARKED (Nov 3 "down the road"); captions fail lint: rewrite before reuse. Jade "Smith-style" reel parked (needs her song).
- **Holiday reels Nov 1** (assets/social/holiday-nov1/): rebuild to the v5 standard before use.
- **Face-to-camera script + Ask Me Anything carousel** (assets/social/next-week-talk/): drafts.
- **Poppins mat-alert set** (assets/social/mat-edit/poppins/): CONFIDENTIAL until OMM announces Poppins.
- **Partner kit explainer video v2 + launch explainer reel + tutorial reel**: built, not used.
- **Restock companion frames** (restock-oct27/, restock-huntclub-oct30/, restock-tinselle-oct31/): reuse at the next restock.
- **Brownstone Bloom group post**: not doing (fall is past).

## Later / ideas
- **Brand Watch page as a 3rd bookmark reason + partner self-serve updates** (Tiffany Nov 10 7:55pm brainstorm, no decisions): photos/collage (also a 'Brand Watch, updated daily' social piece), hot vs minor, grouping by brand, consistent shop links; partner vs non-partner open. Not on social until it's good.
- **Consolidating chats / Fable / Google Sheets of what Claude knows and does** (Tiffany Nov 10 12:15pm questions): she is staying in Main (was Matches & Catalog) for now; said-vs-done audit sheet started (12:21pm).
- **Anders Ruff bridal mat + tiles collab** (sneak peek Nov 10, no date): HQ Later card; watch for the drop.
- **RMS Heirloom Crown Jewels** (coming soon, no date) + **TdT Birdsong 'back soon'** + **OMM Gemma restock in 1-2 weeks** (watches Nov 10): record; Gemma has an album → restock-first rule when dated.
- **Discount-code presentation model** (Tiffany Nov 9 4:18am): @for_the_love_of_mahjong bio links + lourdesnorton.studio 'The Mahjong Edit' (tiered brand list, one code, linked from the IG bio). Main proposes a /links or hub variant when the Google work allows.
- **Second Dear Santa post ~Nov 20** (last call before it ships; her Nov 9 4:34am).
- **Story link-sticker lane in reels** (Tiffany Nov 8 4:05pm; Claude recommends yes): reserve a clear zone so a story repost can carry the link. Main adds it to FYM-REEL-RULES on her OK.
- **Mat Gallery filter hiding Etsy/Amazon-sold mats** (Tiffany Nov 8 3:06pm idea; goes by the actual store, not ShopMy): her call.
- **FYM opening to all brands** (Nov 8 2:03pm direction, paused while she does partner outreach); show-frequency caps per brand instead of catalog caps (Nov 8 4:51pm). Non-partner gates unchanged until she says.
- **Google AI insight log** (docs/research/google-ai-insights.md, Nov 8): every entry splits AI Overview vs AI Mode and marks VERIFIED vs UNRELIABLE; data before Nov 5 is skewed.
- **"Retired mats on retired tile sets" angle** (Tiffany Nov 7 8:24pm): OMM's Build Your Set can't show it; reel + caption line; she may mention it on the OMM VIP page. Main storyboards it for her yes (target Thu Nov 12).
- **FB Page growth** (21 followers) + **FB group low-effort engagement** (~7 new members/week, no welcome posts) (Tiffany Nov 7 5:00pm): research docs/social/fb-page-growth-2026-11-07.md; group week draft = Waiting on Tiffany.
- **AI-visibility tool** (docs/research/ai-visibility-tools-2026-11-07.md, Peec AI Starter $95/mo recommended): costs money = her call; Main brings it with the OMM-first plan, don't push (Nov 7).
- **Mood-board / table reels (Rudolph, Polo, Rattan) DROPPED** (Tiffany Nov 6 4:11pm). Their Planoly drafts stay until Main confirms with her that "dropped" = remove them (SOCIAL 13: only her no removes a post). The unsaved Rudolph Canva edit (Nov 6 ~2:30am) is moot.
- **Weekly cross-brand "what's new in mahj" roundup** on site/email/group/IG; shift focus to getting USERS to the site; email list = stay in the know (Tiffany Nov 6 6:14pm, docs/strategy/2026-11-06-business-pillars.md).
- **Pinterest goes FYM-led** (Tiffany Nov 6 4:12pm): 10 pairing pin drafts made Nov 6 (Sunshine Glow, Crown Jewels, Spirit of Christmas) in the Pinterest workspace; next = schedule within the pace rule (Main).
- **I Love Mahj push**: $0 ever logged; commission terms unknown (Nov 6 5:09pm). Main finds the terms before any push.
- **Splash of Color Valentine mats + tile sets, LBB Pink Christmas mat, Virora bags (Sat 5pm PT), My Fair Confetti racks, Anders Ruff Christmas Solo mat, Middle & Main boutique, Mahj & Vine Chinoiserie restock**: record only (watches Nov 6).
- **Mahjong Row & Co. future** (Nov 5): Brad may offer one-time referral links instead of codes; her call once he replies (Main brings it). Their fall album and new Foxhill Plaid / Hawthorne Floral mats + Oxblood / Cognac Burl racks wait on that.
- **Charleston Mahjong Club Cabana Club full-size tiles** 'arriving any day now' (partner watch Nov 5); giveaway ends Mon Nov 9 8pm ET; HQ sneak card. Small album idea already in Later (Oct 28).
- **My Fair Mahjong 4 new Confetti acrylic rack colours** (launch watch Nov 5): accessory, record only; FYM rack lists when there's room.
- **Mahj Mood Playing for Keeps tiles** ($390, Valentine set, ships January): not an album now; the PFK mat swipe book is optional before Valentine's content (Nov 5).
- **Per-brand IG code posts / reels**: not now (her Nov 4 3:55pm pick = one evergreen post); revisit if the evergreen post doesn't show in Google (Nov 4).
- **Tiffany's Takes editor** (DkRn8W5qaMBxHfqqeJVE8V) data is from Oct 10 (37 albums): refresh with Brownstone + holiday albums when she wants to write takes (offered Nov 4 1:45pm).
- **Maison Mahj House Line No. 1** public preorder ($595, Nov 4), **Bougie Mahjong neoprene versions** of 5 mats ($80/$90, non-partner), **My Fair Mega Swirl Dice** ($40, accessory), **Splash of Color tile set** ($285), **Anders Ruff 'new product' reel tease**: record only (watches Nov 4).
- **Mahjong Moxie Moxie Tiles** (first tile set) LIVE Fri Nov 6 12pm CT: non-partner except Duck Camp/Heron Landing mats; record only unless she says.
- **Clean up 52 legacy caption lint warnings** (still 52 Nov 10) (config/social/content_lint_baseline.json; mostly missing #MahjMatch, '(affiliate)', 2 TdT captions) (rules audit E9, Oct 30). Also legacy repo FAILs in banked Season 2 / episode / holiday-table captions (Nov 10: length 42 legacy + 2 new plain_post, naming 36, brand-tag 2 new-check on S2 Smith). Planoly IG lint 51 FAIL under Tue's stricter lint (32 = profile-only codes post brand-tags; rest = story captions, New this week FB 361, banked Retro Rattan).
- **FYM Shuffle** idea for 1.15 (Main (was Matches & Catalog), Nov 3).
- **Brand-locked FYM pricing**: pilot with Emily (60-90 days, friend rate or trade), then setup + monthly; hosted embed only; pricing undecided (her Nov 3 3:56pm).
- **Launch reel may need another redo** once Table view is the main view (her Nov 3 4:37pm).
- **Anders Ruff Puppy Love Solo Play mat** ($48 preorder), **Miss Mahjong Garden Party + Cherry Blossom travel mats** ($40): solo/travel, record only (launch watch Nov 3).
- **Bird & Bamboo 20in stain racks back in stock, 21in sold out until January** (Emily, Nov 3): record; FYM rack stock.
- **Let's Mahj On new tile sets** (Wild, Sweet, Golf, Refined, Merry, Stir Things Up), coming mid-Nov: new products; ONE swipe book only if she says.
- **OMM 2027 International Mahjong Card** preorder ($12, ships Jan 2): record only; possible teacher/FB group mention.
- **Peace Love Mahjong Black Friday Nov 16**, **Virora Lilacée restock Nov 10**: codes post + social on the day.
- **Reels earn 0 follows two weeks running; the single 'It's a match' image is still the best post** (social measure, Nov 2): weigh image posts in next week's kit.
- **Sunday Blues restock post window ~Nov 16** (HQ card parked to Nov 16).
- IDEA (Tiffany Nov 1 11:33pm, not now): fold racks into the mat step for Aerial/Table views; revisit once Table view is the main view.
- **Mahjong Register** Crystal Palace acrylic racks + Solid Wood racks (launch watch Oct 31): FYM rack lists when Main (was Matches & Catalog) has room.
- **Sunday Vegan Leather mat moved listing** (launch watch Oct 31): relink the FYM card in the next build.
- **Brands later (her Oct 31 picks):** Feltectors, Four Winds Social, Mahj House Rules, Mahjong Made Chic, Mahjong Moxie, Silk Mahjong, The Mahjong Line (teacher program only).
- **Bam Bird restock/brand announcement** teaser (IG Oct 30): same day or never.
- **Amanda Toppe Lila**: full-size later = swipe book the day it lists (Oct 29).
- **Table view later**: walls for pattern-back sets with no back photo, mats+tiles price filter, aerial photos from partners, Table view as a partner perk vs open to all (undecided, don't push) (Tiffany Nov 1).
- **Splash of Color digest #3** (launch watch Nov 6 5:57pm): 11 mats built into an optional book https://claude.ai/artifact/SNED3mKhfnp41Y5m6BZEUS (on hq/albums); counter reset to 0. HQ doc hq/launches is at ~258 KB of the 256 KiB (262,144 B) cap: next run that adds items must archive old items (e.g. move pre-Oct 20 items to hq/launches-archive) first.
- **FYM default tile-set order by brand logos + commission ranking** (Oct 29 3:29pm).
- **Brand-locked FYM as a partner perk**, **brand demand data for partners**, **accounts** (Oct 29).
- **Rakuten** skipped (Oct 29 11:17am).
- **Table view as a partner perk vs open to everyone**, **partners opt in with aerial photos**, **ask Emily about a pusher** (Oct 28).
- **"Mahj Garage"** accounts + "I own this" (Oct 28); competitor Mahj Closet ($9.99) (Oct 27).
- **IG Saved "Save for repost"**: partner reposts 1-2/day; holiday reposts from Nov 1 (Oct 28 10:04am).
- **Restock page** (Oct 28 10:31am).
- **Charleston Mahjong Club Après-Ski small album + Cabana Club**; **Peach and Pine** + **Fire + Fortune** after Nature Walk (Oct 28).
- **Gift content from early/mid Dec** (Oct 28).
- **Build your set extras**, **Mahj registry, AI "dream mat", dream set builder** (Oct 27).
- **Content like @mahjandmotif**; **a better FYM reel** (Oct 27; docs/FYM-REEL-RULES.md).
- **Partner portal**, **separate desktop vs mobile FYM**, **mat-only brand "eye candy" story**, **OMM reshares only 100%-OMM content**, **FB group growth plan** (Oct 25-26).
- **Canva template library + #MahjMatch reshares** (Oct 25); **IDEAS 3.0** (Oct 23); **internal FYM sets view**, **every-tile-set gallery**, **Pinterest ShopMy single-product pins** (Oct 24); **Match Monday / Reader Request** (Oct 23); **Rebecca Illustrated 15% ShopMy**, **Aurora's racks** (Oct 22); **brand alert sign-ups, comment-for-link, UPS cutoffs Dec 1** (Oct 21); **site colours, "Press for Mahjong" rename**, **$200/mo API credits plan** (after launch).
- **New brand releases** are NEW PRODUCTS, never albums (Anders Ruff Bellamy Bloom / All American / Heritage Tartan; Bespoke x Brooks Brothers; Bespoke x Gray Malin; Britt Mills Emerald Mirage; Mahj & Vine Whispering Winds; LBB Butterscotch Floral; LBB Artist Collective mats).

### Added during Wed Nov 11 (carried as-is)
- Main: TIKTOK on the radar (Tiffany Nov 11 9:14am). Plan: she creates @mahjmatchmaker (business account) + connects it in Planoly; Claude reposts the reel bank (FYM, holiday, album reels) 3-5x/week as Planoly drafts with TikTok-library sounds, captions with MAHJMATCH typed (never next to Tigre de Tartan), varied cuts/hooks rather than identical reposts. Waiting on the account.

### Idea (Tiffany Nov 11 11:46am): mahjong x weddings SEO, ride the Anders Ruff bridal launch
- Trigger: Anders Ruff bridal mat + tile set (collab with an OG Bachelorette, no date yet). She knows from Heritage Sign Co that the wedding market is huge; mahj x wedding has almost no competition.
- Search check Nov 11: "mahjong bridal shower" / "mahjong bachelorette party" / "mahjong wedding gift" return only Etsy listings, Anders Ruff's own party-theme post and one thin AI blog. Nobody owns it. Bam Bird bundles are sold at Crate & Barrel = registry-able (wedding registry angle).
- Plan (Main, needs her yes on the post): one guide page "Mahjong for weddings: bridal shower, bachelorette and registry gift sets" built ahead, live the day Anders Ruff launches; brides' palettes -> matched tiles + mats; add terms to the next Keyword Planner pull; Pinterest board "Mahjong bridal shower".

### Hanukkah + New Year's (Tiffany Nov 11 12:40pm; small, don't over-spend)
- ONE Hanukkah table piece (mood board + short blog section) before Dec 1 (Hanukkah = Dec 4-12): Noli June Eighth Night mat + Hanukkah dish, a blue tile set; partner Hanukkah tiles exist (Splash of Color Hanukkah sets, Sweet Jojo Judaica Pearl). Less competition than Christmas.
- New Year's phase (late Dec): Noli June Rochelle Didn't Make It to Midnight mat + NYE dice dish, Splash NYE Glitz Gold mat. config/seasonal-tags.json.
- Winter tile sets for ski/apres content: CMC Apres Ski Club, Virora Nivalee, Bespoke The Chalet (Frosty Pearl White / Lilac), Maison Mahj Apres Mahj (sold out).

### From Tiffany Nov 11 12:57pm
- **Charleston Mahjong Club Hunt Club vlog (Main, Chrome):** her review VIDEO of CMC Hunt Club tiles on Mahjong Moxie's Duck Camp mat sits in our PRIVATE Facebook group. Find the post (facebook.com/groups/mahjmatchmaker, search "Hunt Club"), note its date, grab stills, and publish it as a BACKDATED blog post / vlog with photos (SEO: Charleston Mahjong Club Hunt Club tiles review, + their other theme sets: Après Ski, Cocktail Club 2.0, Yacht Club, Country Club, Cabana Club; code MAHJMATCH). CMC likely doesn't know she ever featured them. Ask before downloading the video file.
- **Holiday-break TRAVEL week** (mid-Dec, when it's too late to ship holiday tiles): travel sets before vacations: Miss Mahjong Mini Miss Classic (new), Mini Miss Out of Office (sold out now, "coming back": watch), CMC Cabana Club travel bundle; Cabana Club album releases that week or EARLIER (as soon as it's done: leave shipping time, avoid sell-outs). Christmas Vacation theme.
- **Priority:** Bespoke + Charleston are her top two of the lineup. Bespoke = decent-sized brand with no representation: work harder for them.
- **CMC ShopMy vs code test (Tiffany Nov 11 1:04pm):** on the next Charleston order email, check whether the same order also appears in ShopMy earnings (Chrome, ShopMy dashboard) -> tells us if link + MAHJMATCH pays ShopMy 15%, the CMC program 10%, or both. Record in docs/LINK-ROUTES.md.
- **Album requests tracker (Tiffany Nov 11 1:19pm):** requests land in tiffanybrie@ Gmail ("Form Submission - Album Requests", label Site/Album requests) + Squarespace Contacts > Form submissions; this cloud session's Gmail is mahjmatchmaker@, so pull them in Chrome: every request (date, set, brand, email) -> config/album-requests.json + a count by set; surface the top requested sets on the album lineup page. Needed for My Fair Mahjong pick.
- **Miss Darling twin album (Cameo Blue + Lilac) (Tiffany Nov 11 1:34pm, top tier with CMC + Bespoke):** build before Lilac's preorder opens (store says coming soon, no date; partner watch flags the day it opens). Tile photos: Lilac store renders saved assets/launches/miss-darling-lilac/; Cameo Blue from the store.
- **OMM album card counts (CORRECTED Nov 11 2:30pm; the 1:38pm 'Lagoon 9' numbers were WRONG, Tiffany caught it).** Counted from the LIVE album pages (unique card images): Sunset 22, Limoncello 25, Taylor 31, Sorbet 34, Gemma 35, Luminaire 35, Pippa 35, Glitterville 36, Palm Royale 39, Sierra 40, Emerald 41, Seabreeze 42, Lagoon 50, Glow Wild 53, Solara 53, Willow 59 (max Heritage 2.0 92). No OMM album is thin; only Sunset and Limoncello sit in the low 20s. Thinnest overall are vault albums Lilac Soirée 12, Sunday Tile Set 12, Preppy Soirée 21, Spring Love 22. Thin-album rounds paused until she says which (if any) to grow. Source of truth = live pages, never HQ.
- **Sunday albums (corrected Nov 11):** all 4 already have cards built Nov 6 from her yeses (Nature Walk 42, Sunday Blues 56, Plum Panda 41, Hummingbird 41: assets/cards/<set>/). No more swiping. Sunday Blues = finish first (album_gate steps 3b-8: other FB groups, mat discovery, catalog check, by-sight left-outs, holiday, faces) then review page -> her final look -> staged hidden for Sunday's ~Thanksgiving restock. Then the other three, each timed to its restock.
- **Royal Mahjong Society shortlist (Tiffany Nov 11 1:47pm, no decision; out of season now):** Shore (sand/beige beachy neutral, underserved; "launching early November", sold out/coming soon) = summer; Newport (signature nautical, royal blue, lobster jokers; restock mid/late Nov) = Memorial Day / 4th of July; Cottage (peach + green, launching early Nov); Girly; Island (Seabreeze colours, bold reds). NOT Crown Jewels. All Heirloom, full size, $425.
- **Blog: favorite tile storage (Royal Tile Bag $58: twilly scarf, divider = display case, great for teaching the suits; + OMM tile bags).** No storage/bag article exists (checked sitemap).
- **Blog/Social: "Tiffany's Favorite Things" mahj gift guide (her idea Nov 11):** evergreen mahj gifts, fills December after holiday-tile season; Royal Tile Bag first. Ask her for the rest of her favorite things list.
- **Petalée readiness check (Tiffany Nov 11 2:03pm):** banked album (Virora's most popular set, $229) built Oct 20 under the old process: no config/album-records/petalee.json, album_gate fails [0]. Do a readiness pass (record, gate, card look, updated dragons in tile photo) in a spare-usage session; target February pinks/reds slot.
- **Spare-usage projects (her rule Nov 11):** when she says "use the spend" (e.g. 40% left before the weekly reset), do banked/reel work: album reels, Petalée check, OMM thin-album rounds. Never burn usage mid-project.


## Daily operations (Fri Nov 13)
| Operation | Done today? | Notes |
|---|---|---|
| Affiliate tracking (Money tab) | ✅ Done | Fri: 10 orders by 12:47pm; her 8 screenshots filled 9:22pm (Bam Bird x4 $102.15, Middle & Main $11.88, Splash $22.53, My Fair $6.16; Thu Mahj Squad $8.10). MTD $3,464 known at noon. Left: Mahjong by SI (Claude reads Collabs). |
| Google & Revenue report | ✅ Done | docs/reports/google-revenue/2026-11-13.md (d81b54dd): 10 two-date brand pages fixed (live check PASS); Thu 4-order DAY ALARM; HQ alert card. |
| Google code report + scorecard | ✅ Done | a00f6233: AI Overview signed-out cloud 22/40 (OMM not named), AI Mode 35/40; laptop 34/40 personalised. Next Mon. |
| Verified dates (weekly, Mondays) | ⏭ Not due | Next Mon Nov 16: update BOTH the visible line and the SEO description (her Nov 13 rule). |
| Codes post (Mondays) | ⏭ Not due | Next Mon Nov 16 (include PLM Black Friday). FB codes post task: last run Nov 9 ABANDONED (report watchdog). |
| Pinterest queue health | ⚠️ 1 issue | Autopin 3 published, 0 failed (89bfe012). 27 pins Nov 14-20, 0 errors; Mahjong Row Cypress Forest pin Tue Nov 17: unschedule refused unattended → priority 3. |
| Indexing | ✅ | 10 requested 12:36pm (OMM first); 20 re-dated pages queued Nov 14-15. |
| Planoly next-7-days (IG + FB Page) | ❌ 0 IG SCHEDULED Nov 14-20 | 5th night. Drafts: Sat/Sun (rolled tonight) + Deco (Lagoon) Mon-Sun. Every IG draft in the window has a FB Page target + every-slide story; Tag people = verified handles only (bambirdboutique, brittmillsdesign, bougiemahjong). content_lint --planoly --only-ig: 52 FAIL, 1 NEW (Deco Wed reel FB caption 420 chars) → OVERDUE; rest legacy/banked. Mahjong Register has no verified handle (named, not tagged, on Tue 11/17). |
| New albums (last 7 days) (f) | ✅ | Juniper + Deco Lagoon re-curled: /mahjong-tile-matches ✅, Green/Blue colour pages ✅, OMM/Bam Bird brand pages ✅, /links ✅ (Juniper 2, Lagoon 1), hq/indexing ✅, Pinterest ✅ (Lagoon pin Sat 11/14). No new album live. |
| Repo caption lint (g) | ⚠️ No new kinds | 91 FAIL (length 46, naming 36, banned-phrase 5, brand-tag 2, mahjmatch-missing 1, hashtag 1): +1 length on assets/social/week-2026-11-16/captions/plain-post-source/ig-caption.txt (359) → OVERDUE with the Wed reel line. |
| Live codes check | ✅ PASS | 41 pages + hub after the 10 date fixes (Google report). |
| Gallery sync check | ⚠️ Not run tonight | Live FYM still 1.18; nothing shipped. Morning run. |
| Coverage + card sharpness | ✅ Coverage owner ran 7:08pm | Wren Gingham staged, Pool Mat excused, jsDelivr 200 re-check; morning sharpness: 2 new blurry cards (OVERDUE, by Sat Nov 14). |
| Restock first (c) | ✅ Checked | No album-set restock dated Sat Nov 14. |
| Match inbox (e) | ⚠️ 125 old lines unmarked | Priority 5 (+5 new Nov 13 lines, not yet 2 days old). |
| Launch + partner watch | ✅ Done (1 partial) | Launch watch 8:57am (4 LBB mats) + 5:57pm (Britt Mills Plumage II); partner watch 1:40pm; 6:30pm run's git fetch failed (4 items pending, In progress); stories 12:37pm (0 finds); ShopMy check (nothing new); Brand Watch v26. |
| FYM + partner feedback | ⚠️ Not checked tonight | Morning run. |
| FYM releases | ❌ None | 403 looks cleared; 1.19 first (priority 4). |
| Albums | ✅ Status check | 12 non-live album pages curl 404; none went live; hq/albums unchanged. |
| Social posted today | ⚠️ | Nothing on IG/FB Page. Built: Deco (Lagoon) week kit (Planoly drafts + FB group plan doc). IG engagement: 22 partner likes. |
| TNT scan (weekly) | ⏭ Not due, not merged | 81b + 81c JSON still to merge into config/tnt-recs.json (Handoffs line); target Sat Nov 14. |
| HQ + Ready to Ship cleanup | ✅ Done | Morning cleanup 58129b4d + this run (HQ log). RTS: no new answers. |

## Never-ending projects
- **Find Your Mat-ch™ app** (artifact 6epA9HuEdT32zUp79Qv3kd; public **Version 1.18** (artifact Version 117, id 1794137165-e544; both FYM pages page-block @9d331637; Mat Gallery v8 r3 @78072ca0 + search @3afb680e; all live Nov 8 ~11:15am); **1.19 = racks-only (Miss Mahjong)** blocked by the jsDelivr 403; the rest of the staged bundle (Deco Lagoon m-list, link routes [172], catalog adds incl. non-partner whole lines, racks, walls, Cabana) ships as small releases per rule 0b: gate + independent QA before every publish (QA loads the WEBSITE copy as live: 0 broken images, gate [115]); artifact AND website copy AND README 0a pin in the same step; +0.1 version label (docs/FYM-VERSIONS.md); her feedback the same day with a gate check; when a publish/paste fails, MESSAGE HER right away. Artifact file budget: run builder/fym_artifact_fit.py and publish ONCE. Every nav/header change: screenshot live at 1280, 1440 and 390 with the phone menu OPEN. New partner catalog in FYM within 24h of its inbox line (gate [114]). Refresh config/fym-mats-snapshot.json after every publish.
- **Match inbox** (docs/MATCH-INBOX.md): any chat writes match/catalog misses there the same turn; Main (was Matches & Catalog) marks DONE when shipped.
- **Google / MAHJMATCH in AI answers (her #1)**: AI Overview + AI Mode per partner, code report (Mon/Wed/Fri), daily morning report, indexing (brand pages first), sitemap health, weekly verified dates + hub date, weekly codes post (FB GROUP only typed out; IG/FB Page = logos graphic + short caption), alarm on any lost citation.
- **Albums**: order (her Oct 28 3:31pm; Style of Your Life DROPPED Nov 7, Dillard's exclusive, MFM set TBD): Sunday Blues (her Nov 8 order: cuts the line) → Bam Bird Deco Mulberry + Indigo (Lagoon LIVE Nov 8) → Sunday Nature Walk, Plum Panda, Hummingbird → Sunday Nature Walk → Middle & Main Peach and Pine, Mac + Miller; Mahjong Row fall + OMM green set (Juniper, LIVE Nov 8) jumped the line; a known restock goes FIRST. Album Playbook doc (14oGH3ovycd2xMgrHbodJZ) is the source of truth; doc 86b (colour card FIRST), book_gate.py, PICKING-RULES.md, NEW-ALBUM-CHECKLIST.md (incl. the new-albums email).
- **Holiday (Merry Mahjong)**: intro reel posted Nov 3; next = late picks into holiday albums, holiday albums + FYM holiday group posts, new-albums email; docs/MERRY-MAHJONG-BRIEF.md + docs/plans/holiday-calendar-nov-dec.md; promote FIND YOUR MAT-CH, not albums (her Oct 30); any FYM social shows the tool working; storyboard before render; song shortlist on every reel; FYM-REEL-RULES 23-41.
- **New products**: hq/newproducts → gallery + FYM colour-tagged → weekly roundup. Never albums. New-mat social = "Match up <mat> in Find Your Mat-ch", never ahead of the brand; wholesale-only/unannounced = confidential.
- **Social** (docs/SOCIAL-SYSTEM.md, ~2 hrs/week of her time): every planned post as a Planoly DRAFT on its day (final media, lint PASS, Tag people, FB Page target, story version); she reviews in Planoly; FB Page target on every IG group; every slide to stories; brand tags + collabs; restocks/launches SAME DAY or never; ≥4 IG posts in every next-7-days window.
- **Facebook group**: community, never ads; weekly codes post (doc 94); weekly Claude Doc of planned posts; @everyone at most ~once a week.
- **Partner share graphics**: one per brand + our MAHJMATCH version (39 logos as of Mahj Pit, Nov 4: assets/hub/partner-brands-2026-11-04.jpg; IN USE from Nov 7: assets/hub/partner-brands-2026-11-07.jpg (packed logo wall, no Mahjong Row/YMI; hub image + FB Page codes post); 11-05 retired: Mahjong Row on hold).
- **Pinterest**: queue within the pace rule; evergreen pins of our own images.
- **Affiliates + money**: sales checks 2:04pm + 12:04am, reconcile every referral email (both inboxes), refunds on the refund date, spike AND drop checks; onboarding new partners (page, hub, logos, FYM within 24h, indexing, IG follow/favorite); affiliate applications (kit doc 00h).
- **Mat Gallery + colour system**: sort rule, holiday rule, partner-only gate (plus her Oct 31 non-partner picks), shop-by-colour partners first (Oct 31); gallery row for every visible FYM mat (gate [90]).
- **ShopMy + Amazon storefronts**: square-safe covers, aerial mat photos, HQ ShopMy tab intake, weekly ShopMy mats check (Tue).
- **HQ hygiene**: Today ≤5, answered = gone, event passed = gone, timestamps on every card, inline previews; ANSWERS.md before asking anything; no answer is not a no.


## Log of this rewrite (Fri Nov 13 night)
- **Done today:** SEO-description verified dates fixed (BBB, LBB, YOLO) + 10 two-date pages (live check PASS); TdT brand page House Tigers Oyster; Brand Watch v26 (BF section); Deco (Lagoon) social week as Planoly drafts; Google & Revenue report + scorecard; indexing 10; launch watch x2, partner watch, stories, ShopMy check, coverage owner, IG engagement, Pinterest autopin; money screenshots filled.
- **Tonight:** 10 past-dated Planoly posts rolled forward (5 groups); Pinterest Mahjong Row unschedule refused (OVERDUE + priority 3).
- **Found mid-way and given a home:** see Handoffs line 'Found Fri Nov 13'.
- **DESK: carried every open line (drop check result in the commit message).** OPS chore lines re-owned to Main (Ops = money + Amazon-to-ShopMy only); slipped In progress targets re-dated.

See CLAUDE.md.
