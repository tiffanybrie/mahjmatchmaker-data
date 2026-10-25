# The Desk

Rewritten nightly by the end-of-day desk cleanup (9:23pm ET). The morning HQ cleanup (6:47am ET) reads it. Rules: CLAUDE.md ("THE DESK"), docs/CHATS.md (which chat owns what). During the day, when an agent stops, Chrome drops or a QA stalls, add the item here right away with its next step.

**Last rewrite:** Sat Oct 24, 2026, ~9:40pm ET (desk cleanup run). Covers the 25 commits since the Fri desk (8874c1d3 → 4940aeeb), docs/ANSWERS.md, Planoly (IG workspace 019fc27c… + Pinterest 019fc27b…), HQ needs / log / albums / money / launchPlan, Ready to Ship `ship` docs, the Brownstone order page db, site/livepatch READMEs and curl checks of the live site.

**Owners (three chats, Oct 22):** Main (Opus) = social/Planoly, site pages, email, HQ/DESK, decisions. Matches & Catalog (Opus) = Find Your Mat-ch, albums, gallery, catalog, search index. Ops (Sonnet) = the ONLY Chrome driver: Squarespace pastes, uploads, IG follows, verified-date refreshes.

**Usage:** weekly limit resets Sun Oct 25 11am ET; trig_01MrL5j re-enables the paused tasks at the lighter cadence (see bottom). Tiffany: go full speed on launch work; tell her the moment a chat hits the limit.

**Repo note (desk run):** the old checkout at /home/claude/mahjmatchmaker-data was found mid-rebase on `main` (12 picks pending, 11 deleted Papaya launch photos unstaged, untracked CLAUDE.md + assets/amazon-store/). The rebase was aborted (nothing lost; main is back where it was); the leftover untracked files are untouched. This run worked in a clean worktree at /home/claude/mmd-sqsp on partner-catalogs-sqsp. Next session that uses the old checkout: `git checkout partner-catalogs-sqsp` there after checking those untracked files.

## Tomorrow's top priorities (Sun Oct 25), in order
Standing order: (1) Find Your Mat-ch™ launch Tue Oct 27, (2) fall content before it expires (Brownstone Bloom = the week of Oct 26), then holiday (November, through Find Your Mat-ch). No ordering question needed.

1. **FYM: independent QA for v81 + v82, then the rest of the VIP list (Matches & Catalog).** Website preview caught up today (live /find-your-mat-ch-preview serves `site-app/fym-v82`; launch-oct27 README 0a pins the same block @9d98705). But no independent QA PASS is recorded for v79, v80, v81 or v82 (last recorded PASS = v75; the v80 commit only says "(QA)"). CLAUDE.md FYM rule 2. Next: (a) separate agent runs phone 390 + desktop on the website preview AND the artifact: both doors, colour filter, zoom, card + share, mat-door tile swipe + See all grid, contact sheets; record PASS/FAIL in site/livepatch/fym-preview-oct21/README.md; (b) the preview page HTML still contains a `site-app/fym-v72` string next to v82 (curl tonight): find whether an old block or the tutorial still loads v72, fix in the same Ops paste; (c) after 11am, the open VIP items (HQ `vip-sunday-fym-oct25`): coordinated collections first, tour from the mat door, missing tile sets from the audit, hidden/removed review list, tray flags + rack cutouts, Bam Bird Classic Tortoise cover, share caption/PWA/sticky box/WebKit. Each publish = gate + QA + artifact AND website copy AND README 0a pin together. Target: Sun night.
2. **Pre-launch social into Planoly (Main).** Planoly IG has 0 posts scheduled Oct 25-31 (only one old Oct 21 reminder story). Drafts with passed dates: Smith swipe reel (dated Sat 10/24 11am CT; her fixes still not rendered: navy ✕, Find Your Mat-ch™, current racks, new end card, Season 2 intro), rejected Papaya "Still available" story (dated Fri 10/23: undate, never delete). Drafts dated ahead: Papaya × Heiress carousel Sun 10/25 11am CT (auto, still draft = won't post), Miss Classic tease Mon 10/26 (re-check vs launch push), launch-day link story Tue 10/27. Countdown "2 days"/"1 day"/"LIVE today" drafts are undated with stale copy in the title. Next, in order: render Smith with her fixes and re-date; Reel 1 with her 2:22pm notes (slower, "43 tile sets and counting" bigger + held, end on Bam Bird Classic Tortoise, tag every brand); launch stories (Sun/Mon/Tue) as ONE contact sheet → her one yes in Planoly; partner launch email (Squarespace "Partner Brands" list + Dropbox link + graphics kit). Target: Sun.
3. **The overdue Ops Chrome session, now 4 days late (Ops; standing authority, no OK needed).** Today only the FYM preview paste happened. Still not done: (a) pre-launch homepage block (curl tonight: 0 `mmfym` on /; her yes Oct 21; site/livepatch/home-prelaunch-fym); (b) site search header injection (site/livepatch/search @c6e395f, QA passed); (c) welcome + album-request + launch emails built as Squarespace automation DRAFTS only (her Oct 24 12:49am: nothing sends until her final read; footer address in ANSWERS); (d) verified dates (curl tonight: Anders Ruff still "verified October 9"): dates only, no code re-testing; (e) Soirée All Day IG follow + favorite; (f) sign back into the Mahjong Row & Co. affiliate dashboard (signed out tonight) and retry GoAffPro (errored) so the 8 unknown Oct 24 amounts fill in; (g) Tiles & Tablescapes "Gatsby" scan for TNT recs; (h) Amazon "Mahjong Mats I Love" 34 ASINs → config/amazon-mats.json (title, main image, ShopMy/tagged link). Save rollback text first, close every tab. Target: Sun.
4. **Emails + launch-day tasks before Mon (Main + Matches & Catalog for screens).** Launch email revised (Montserrat-style "Here's how it works", step screens from the live v82 app mirroring the tour, fewer arrows/text) and back on RTS `d-email-templates`. Then re-check both launch tasks: homepage switch trig_011jdGG (README 0a pin = v82 or newer after Sunday's publishes) and email trig_01ErZy (must NOT send; at most flips automation wording after her read). FB group description v3 rebuilt in place on RTS `d-fbdesc2` with her line "Use our group code MAHJMATCH to save 10% or more at our partner brands". Target: Mon Oct 26 morning.
5. **Brownstone Bloom live the week of Oct 26 (Matches & Catalog).** Cards rebuilt today (40 + manifest, assets/cards/brownstone-bloom-oct24, her racks AR Tortoise + Bam Bird Olive + B&B Wine, Scarlett #2, Autumn Saffron #4, 9 hearts appended). Her Save on the order page (artifact WNjXTGjxfdqoa1tzUiYgQ4, db review/order) has NOT come in yet: HQ Today. On Save: rename in her order, brownstone_block.py, warm jsDelivr, publish, then redo the Ep 11 Brownstone reel with an intro before dating it. Target: live by Thu Oct 29 (before Halloween).

## In progress
- OPS (Oct 25, Matches chat; Tiffany approved the fix 15:21): HOLIDAY LINKS land at the top of albums. Cause: the header Holiday menu's hidden dropdown has id="holiday" (Squarespace derives it from the NAVIGATION title, so renaming the folder slug /holiday-menu + page title 'Holiday Menu' did NOT change it), so /<album>#holiday jumps to the hidden menu. Fix = new anchor name: on each of the 34 album pages listed in pushes/holiday_sections.json, in the album code block replace <section class="mm3-hol" id="holiday"> with id="holiday-matches"; on /holiday-mahjong-matches replace every '#holiday"' link with '#holiday-matches"' (34 links). Also update pushes/holiday_sections.json + pushes/holiday_page.html the same way. Verify: /sierra-mahjong-tile-matches#holiday-matches scrolls to the holiday section on a phone. Close tabs.
- [x] DONE Oct 25 1:30pm (Matches chat): preview page re-pasted, serves fym-v83, no How it works, tour link live, phone check Version 83. WAS: OPS, today (Oct 25, Matches chat; Tiffany OK'd the change 11:07am). Next step: re-paste the FYM page block on the HIDDEN /find-your-mat-ch-preview page. The 30-second tour replaces the step-by-step walkthrough and the desktop tip boxes; independent QA passed. Block: https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@0facb6aefe06273de13a44e66202f3b126f3a93e/site/livepatch/fym-preview-oct21/page-block.html (same CodeMirror paste). Verify that curl contains data-fx-tour and site-app/fym-v83/index.html and does NOT contain fymx-how; the app footer must read Version 83 (adds the House of Hearts mats). The launch 0a pin is already updated to this block. Close your tab.
| Item | Owner | Next step | Target |
|---|---|---|---|
| FYM QA v81/v82 + VIP list | Matches & Catalog | Priority 1. | Sun Oct 25 |
| Preview page stray v72 reference | Matches & Catalog → Ops | Priority 1b. | Sun Oct 25 |
| Smith swipe reel fixes | Main | Priority 2; Planoly draft 01a16793 (reminder, her song). | Sun Oct 25 |
| Reel 1 hype revision + pinned-row Reel 2 (app teaser) | Main | Priority 2. Covers = the two existing pinned halves. | Sun-Mon |
| Launch stories → contact sheet → Planoly | Main | Priority 2; rules in docs/FYM-LAUNCH-CAMPAIGN.md (rotate mat brands, partner brands only). | Sun Oct 25 |
| Undate rejected Papaya "Still available" story | Main | Planoly draft 01a16052… dated Oct 23; clear the date, keep the draft. | Sun Oct 25 |
| Partner launch email + "Partner Brands" list | Main + Ops | Priority 2. Watch Dropbox /Mahj Matchmaker/Partner Photo Swaps daily after it goes. | Before Tue |
| Overdue Ops Chrome session | Ops | Priority 3. | Sun Oct 25 |
| Squarespace automation drafts (welcome, album request, launch) | Ops + Main | Priority 3c; drafts only, then HQ need "Final read in Squarespace" on Mon. | Mon Oct 26 |
| Launch email revision + launch-task re-check | Main | Priority 4. | Mon Oct 26 |
| FB group description v3 | Main | Priority 4; one yes on RTS; goes in Oct 27 with the cover. | Mon Oct 26 |
| Work With page rebuild + new "brands" page with launch/restock form | Main | Her l-workwith6 notes (ANSWERS Oct 24 3:32am); Work With stays hidden; form answers → social calendar + daily email scrape; fix empty partner-ticker boxes. Rebuilt item replaces l-workwith6 in place, then one yes. | Tue-Wed (after launch essentials) |
| Brownstone Bloom publish | Matches & Catalog | Priority 5, waits on her Save. | Thu Oct 29 |
| Green Light Gatsby round 2 | Tiffany → Matches & Catalog | Round 2 (26 complement mats) is open in the book; her hearts + round 1's 32 yes → card build. TNT recs from the Ops scan get added. | After launch |
| Thin albums: next quick-spot pages | Matches & Catalog | Her GO Oct 23: same quick-spot style for the rest of the thin albums, bigger tile photo; build cards from her 78-mat hearts. | After launch |
| Malachite + Kingfisher | Matches & Catalog | Add Kingfisher (Needlepoint Clubhouse) to Malachite via nonpartner_allow.json; racks Miss Mahjong Jade, PLM Oak, Bam Bird Indigo; Scream Queens = no. | This week |
| Tile images (Hummingbird, Bam Bird) | Matches & Catalog | Hummingbird tile image under the logo bar, smaller, off the racks (Vivienne + Hummingbird album); Bam Bird tile image per Bam Bird's mock-up (her screenshot). | This week |
| Amazon mats into gallery + FYM | Ops → Matches & Catalog | Priority 3h, then measure colour and add (her Oct 24: always pull Amazon + Etsy). | After launch |
| Standing tile set audit | Matches & Catalog | `python3 builder/fym_tile_audit.py`; batches in the VIP list. | Sun-Mon |
| Bam Bird spike check fix | Main | Flag on ORDER COUNT (5+ or 2x 14-day avg) + release calendar; fold into the merged 3x sales task after the reset. | Sun Oct 25 |
| YOLO Mahjong affiliate approval | Main | Seen in tonight's sales check emails (not counted as a sale). Confirm the approval, then onboarding (page, hub, logo, FYM, indexing, IG follow/favorite). New brand = check ANSWERS before asking anything. | This week |
| Rack data (lengths, colour index, "goes with everything" shortlist) | Matches & Catalog | Her Oct 23 8:35pm list (ANSWERS). Never a non-partner rack first. | After launch |
| Google feedback drafts (OMM TEACHMAHJ teacher-only, MJTI dead, Yellow Mountain, thumbs up x6) | Ops | Standing authority. Confirm MJTI dead, submit, log. | This week |
| Discount links not converted (Britt Mills, Mahjong Register, YMI, RMS, Hip Hip, Wren/Soirée/Amanda Toppe) | Main | Proof in builder/fym_fix_oct21/discount_check_oct21.json. | After launch |
| Missing swipe-book products (OMM Miracle / Twilight Waltz / Merry Mahjong / Santa Baby; PLM Spirit + Nutcracker; OMM Vault) | Ops → Matches & Catalog | Photos in Chrome → pending queue. | After launch |
| Papaya Beechwood README | Matches & Catalog | Live since Oct 22; README still says STAGED: mark LIVE next touch. | Next touch |

## Waiting on Tiffany (only things she can answer now)
On HQ in this order.
- **Today:** (0) VIP list (read-only mirror of priority 1); (1) Brownstone Bloom: put the 40 cards in order and Save (order page); (2) reconnect Instagram via Facebook in Planoly (computer, 2 min; Tag people + collabs stay off until then); (3) Planoly Content Marketplace add-on: keep or cancel ($13/mo, trial ends ~Oct 27; reopened tonight from parked).
- **This week:** Sunday sets round 2 (4 sets); Green Light Gatsby round 2 (26 mats); 3 FYM questionable photos; Fait à Main link + code.
- **Asked in chat, not on HQ (ask once, in the next chat with her):** match card header A or B (images shown Oct 23 ~9pm; A is the default); Brownstone: Bam Bird Walnut racks too, or only AR Tortoise (the order page asks this in its note box); her lost Pippa teardown (2-3 lines); Bam Bird Classic Tortoise match pick; whether the other swiped MAT albums (Larkspur, Revelry, Isla, Peony & Parasol, Art Deco Dayz, Spring Fling, Santa Baby's, Mat of the Moment Brownstone) park with Vivienne under "no mat albums".
- **Parked until after launch (Oct 28):** holiday-or-not on 11 mats, ShopMy 5 quick calls, Amazon old-board delete, Shop page vs ShopMy talk, sender hello@ + DKIM/DMARC, bow lamp keep/swap, nav overflow pick. Etsy re-apply reopens Mon Oct 26 (HQ parked, showFrom Oct 26).

## Banked (finished, held on purpose)
- **Petalée (Virora)**: 61 cards, RTS `l-final-petalee`, vault (her Oct 23 plan). Before publishing: 10% band sweep on the Amanda Toppe/Girly cards, cleaner Petalwing/Coralia photos.
- **Vivienne mat album (OMM)**: 16 cards, PARKED (no mat albums, Oct 23 6:50pm). Drop Hummingbird if it ever returns.
- **Sunday Blues + Nature Walk**: vault once her round-2 swipe is in (never two Sunday sets back to back).
- **Season 2 episode reels + trailer**: undated Planoly drafts. DO NOT re-date assets/reels/s2/*.mp4 or assets/social/countdown/*: she rejected those versions; each gets redone with an intro first.
- **Miss Classic Malachite + Jade**: held for the restock window (week of Nov 3). Tease draft dated Mon 10/26: re-check it fits the launch push.
- **Halloween**: Night of the Raven carousel (draft 10/28) + Happy Halloween story (10/31); small throw-ins only.
- **Holiday tables** (Polo Club 11/4, Rackin' Rudolph 11/6, Retro Rattan held): Planoly drafts.
- **Malachite 8 new cards, December 1994 (31), Spirit of Christmas (10)**: staged since Oct 20; holiday ones from Nov 1 (December 1994 still needs her last RTS notes applied before it ships).

## Later / ideas
- **IDEAS / 3.0 (Tiffany Oct 23 7:25pm):** private studio view of FYM for her (pre-filtered by colour, measured colours on each mat, rank favorites, picks feed album builds); table view (tablecloth, lamp, dice dish via ShopMy); per-product links after testing which partner links auto-apply the code (never OMM).
- **Internal FYM for reviewing new matches (Tiffany Oct 24, Brownstone note):** review new album matches inside an internal Find Your Mat-ch "sets" view instead of separate swipe pages. Source: ANSWERS Oct 24.
- **New products roundup (Tiffany Oct 24 9:03am):** weekly "new this week" (better: "coming next week") gallery for social from hq/newproducts; launches on the social calendar aligned with buying days; reposts are fine.
- **Every-tile-set-from-every-brand gallery (Oct 24):** separate from Albums.
- **Bam Bird Deco moment (Oct 24):** album + bigger brand moment (9 orders Oct 22 with little promotion). Album queue after Gatsby.
- **Match Monday (Oct 23):** weekly Monday album from December, announced only after a few ship clean. Monthly Reader Request album later. Community = "Matchmakers".
- **Colour model (Oct 23 8:01pm):** contrast + secondary tile colours by shade; style/theme menu (Holiday, Earthy, Pastel, Floral).
- **Holiday gift series from ShopMy share videos (Oct 22 5:14am).** IG bio "Find Your Match" → update at launch.
- **Rebecca Illustrated, 15% ShopMy (Oct 22 5:01am):** whole mat line into gallery + FYM, ShopMy links, IG onboarding, shelf cover.
- **Aurora's racks (Oct 22 4:48am):** remind her to match them herself (19" only).
- **FYM share + #mahjmatch (Oct 22 4:27am):** reshare "Great match by @…" posts after launch (ask permission).
- **Pinterest ShopMy single-product pins at scale** after the Oct 24 test (10 pins, 1/day 18:00Z): check published, not flagged, go.shopmy.us resolves.
- **Weekly IG brand watch** from Mon Oct 26; handles still needed: Splash of Color, Hip Hip, Yellow Mountain, Mahjong Register.
- **Brand alert sign-ups**, keep-Planoly-paid by Oct 26, comment-for-link, UPS cutoffs Dec 1 (Q4 plan, Oct 21).
- **Site colours** (one rainbow + Yellow/Orange pages), "Press for Mahjong" rename, holiday set count: after launch.
- **New brand releases** (launch watch Oct 22-23): Anders Ruff Bellamy Bloom / All American / Boston Mahj Party / Heritage Tartan; Bespoke x Brooks Brothers; Britt Mills Emerald Mirage + House Print; Bespoke x Gray Malin; Tigre Domino Blonde. These are NEW PRODUCTS (hq/newproducts → gallery + FYM + roundup), never albums (her Oct 24 rule).
- **Weekly /links refresh** from Sunday; **$200/mo API credits** plan after launch.

## Daily operations (Sat Oct 24)
| Operation | Done today? | Notes |
|---|---|---|
| Affiliate tracking (Money tab) | ✅ Partial | 8:40pm ET check: 15 sales, $88.38 known; 8 amounts unknown (Mahjong Row dashboard signed out, GoAffPro errored: Ops 3f). Oct 22 now $463.17 (Mahjong Co. screenshot); only Amahj Line outstanding there. October to date $6,242.52. Scheduled 10:04pm check still to run. |
| Google code report | ❌ Not done | Paused since Oct 23 4:20pm (usage). Comes back after the Sun 11am reset (a few times a week). |
| Verified dates | ❌ Not done | Pages still say Oct 9/10. Ops priority 3d. Scheduled run Sun Nov 1 (trig_01PGtT8). |
| Pinterest queue health | ✅ OK | 4 pins/day scheduled Oct 25-31 (and on), 0 failed. |
| Indexing | ❌ Not done | Paused (usage). Next when it resumes: /mahj-matchmaker-community; albums only once live. |
| Planoly next-7-days (IG) | ❌ Not covered | 0 scheduled Oct 25-31. Priority 2. |
| FYM feedback inbox | ⏳ Unknown | No log line today; the morning cleanup checks Gmail label Site/FYM feedback. |
| HQ + Ready to Ship cleanup | ✅ Done | Morning run (7:05am) + this desk run. No new RTS answers today (latest ship doc = Oct 24 2:48am, logged). |

## Never-ending projects
- **Find Your Mat-ch™ app** (artifact 6epA9HuEdT32zUp79Qv3kd): gate + independent QA before every publish; artifact AND website copy AND README 0a pin in the same step; locks; pending queue; photo flags; her feedback the same day with a gate check.
- **Google / MAHJMATCH in AI answers**: code report, indexing, verified dates on the 1st and 15th, brand-guide pages.
- **Albums**: process doc 86b (colour card FIRST, colour-wheel pull incl. Amazon + Etsy, by-sight cut, reuse similar sets, outside research), her yes, live; thin albums; holiday features in FYM.
- **New products**: hq/newproducts → gallery + FYM colour-tagged → weekly roundup. Never albums.
- **Social**: every approved post in Planoly at its time; auto-post wherever possible; every slide to stories; brand tags; collabs; partner brands only in launch promo.
- **Pinterest**: queue within the pace rule; evergreen pins of our own images.
- **Affiliates + money**: daily commission checks with spike AND drop checks; onboarding new partners (page, hub, logos, FYM, indexing, IG follow/favorite).
- **Mat Gallery + colour system**: sort rule, holiday rule, partner-only gate.
- **ShopMy + Amazon storefronts**: shelves, covers, collages.
- **HQ hygiene**: Today ≤5, nothing she can't answer, no outdated drafts; ANSWERS.md before asking anything.

## USAGE PAUSE + NEW CADENCE (until Sun Oct 25 11am ET)
- Paused Oct 23 4:20pm: Google code report, daily indexing, release radar. Still running: sales check 10:04pm ET, HQ cleanup 6:47am, desk cleanup 9:23pm.
- Sunday: trig_01MrL5j re-enables at her lighter cadence (Oct 22 3:45am): sales 3x daily in ONE task; brand watch (sites + emails) twice daily; HQ inbox daily; desk nightly + HQ daily; Mahji Mentor + onboarding daily; Pinterest every 3 days; Google code report a few times a week (merge the AI answer check); Match Builder weekly; watchdog + morning brief off. Fix the CHECK, not the frequency.

## Log of this rewrite (Oct 24 night)
- Done today: FYM v81 (mat door swipes tile sets, See all grid, filters beat picks, same intro on both doors) and v82 (picks OFF = measured colour ranking) on the artifact; v82 copied to the website (fym-site-preview @65b2344, files pinned @3cac1c6 + warmed) and pasted on the hidden preview page (live serves fym-v82; her husband's test link works); launch README 0a pinned to the same block. Brownstone Bloom rebuilt (40 cards, her racks + order calls). Green Light Gatsby rebuilt with the new process (colour card, 45-mat colour pull), round 1 swiped by her (32 yes), round 2 (26 complements) published. Album process doc 86b + HQ rule "new products are not albums" (hq/newproducts). Overnight answers logged (footer address, emails stay drafts, Work With notes, thin albums GO, Kingfisher yes, tile images). Money: Mahjong Co. Oct 22 amount filled.
- Found orphaned and given a home: no independent QA PASS for v79-v82 → priority 1a; preview page still carries a v72 string → 1b; Smith reel's Sat draft date passed with fixes unrendered → priority 2; Papaya "Still available" still dated → In progress; Ops Chrome work slipped a third day (only the preview paste happened) → priority 3 with the dashboard sign-in + Amazon list + TNT scan folded in; YOLO Mahjong approval email (seen by the sales check, no owner) → In progress; Brownstone order Save not in → HQ Today stays; Planoly add-on trial reaches its date → HQ Today; Gatsby album item still said "swipe the 113 mats" → fixed on HQ.
- Local repo: aborted a stale mid-rebase in the old checkout (see Repo note at top).
- HQ Albums regrouped: Oct 15-swiped holiday books, holiday covers, December 1994 and Spirit/Nutcracker → Started, stalled (honest: nothing moved since Oct 15-20; November holiday plan picks them up); Bam Bird Deco → Not started (no colour card yet); Mahjong Row & Co #2 + Bam Bird MCM added as Not started (her album queue).
- Priority order follows the standing order; no "Set tomorrow's order" need added.

See CLAUDE.md.

- **CANVA TEMPLATE LIBRARY (Main, Oct 25 4:42pm ask):** first samples REJECTED as unjudgeable (built on an old card). Redo all four from the CURRENT live FYM card (artifact 6epA9HuEdT32zUp79Qv3kd, local copy /home/claude/fymlive), then resend. Original samples (assets/social/canva-templates/samples/: rate-this-match story, match-of-the-week Reel cover + grid guide, iPhone screenshot story, "Great match! #mahjmatch" reshare sticker PNG). NEXT: on her yes, build the approved ones as editable Canva templates (no browser), then a short how-to. Don't build more until she picks.

- **OUTREACH PAGE (Main build, Ops paste; Tiffany Oct 25 5:56pm):** she needs a page to send when SHE contacts a brand. Use the Work With page (site/livepatch/workwith) with her Oct 24 l-workwith6 notes applied, no "tell me about your brand" ask, live HIDDEN at /work-with-us (noindex). HQ snippets (hq/snippets) now hold her outreach emails pointing at that URL; when it's live, drop the 'delete that line' note from both snippets. Fix the partner ticker's empty boxes.

## IN PROGRESS (Oct 25 6:50pm ET): holiday mats -> ShopMy "Etsy & Amazon Holiday Mats" (8507446), owner Ops chat
Source: Amazon idea list 2DG7AI4T6U8KJ "Holiday & Christmas Mahjong Mats" (51 items). Chrome extension dropped mid-run.
- DONE (shelf count 40 incl. the 14 original): the first 25 of the list (through B0FMPWC2S7). B0HCV4TZZK may or may not have saved: check the shelf before re-adding.
- REMAINING ASIN:imgid (add via +Product, Edit, image https://m.media-amazon.com/images/I/<imgid>._AC_SL1500_.jpg):
B0HCV4TZZK:51xe-R5NgjL, B0H82R6CKQ:61CZRnajfyL, B0HDB5B6J8:51gdHUh2tKL, B0HCJ6FVP4:517VI7p0aQL, B0HFZGHMR7:51R0QUlKQ6L, B0H7MGTJS6:51vfNUapzDL, B0H9LDCNHP:51HkLKB9-HL, B0HG837PPZ:51biGlF+qSL, B0H395WLYR:51FSo1PD9CL, B0H2HVMT2W:51R0EkjuqXL, B0H5KLYX28:511IdiRuTBL, B0HB8JHS3N:51f7YQwb63L, B0H9QK7532:51ZeaJfmucL, B0GYN72SSX:51QhKwYsheL, B0FPWMGCSY:51KnGe+pZML, B0HDZ9G4RN:51+txe37PfL, B0H7BKCJV4:51L3OM18pTL, B0HB3FH1SF:51lpKbeWevL, B0H8T5L81P:61AqozOsp8L, B0HC6748QK:51+duafyCUL, B0FQJBYPDZ:51gjTUZ9CxL, B0H98XCQH7:51dnCuIQZyL, B0HB314FBP:51qDiSZV++L, B0G1LV2VZ9:41o0SRpTllL, B0H8DLFXGV:61vL8nCl+fL
- Then: cross-list the two tablecloths (B0HJ2LCBNZ, B0H9KZY2L4) into Mahjong Tablecloths 8400954; add Kate & Laurel Celia table + Santa/Reindeer mat to Tables; holiday-post tag audit; shelf reorder (Trinkets last).

- **VERSATILE MATS ARTICLE v2 (Main; Tiffany Oct 25 7:38pm):** draft preview https://claude.ai/artifact/QmhrQMo5M9Eofn6raA5Atf (site/livepatch/blog-versatile-mats-v2/build.py). Leather (CMC Brown Vegan Leather, Bam Bird Vegan Leather, OMM Cognac match card since the mat is gone from OMM's shop) → lots of color (M&V Chinoiserie Songbird, OMM Larkspur, TdT Jardín, OMM Lorelei, OMM Darjeeling) → earthy + greens (Sunday Rattan, MRC Autumn Saffron/Ivy Reverie/Osmanthus Grove, CMC Hunt Club, TdT Nantucket Basket, OMM Jade). NEXT: her edits → affiliate product links → Ops swaps the live post body + images; re-crawl request.
- **/LINKS + BROWNSTONE BLOOM RELEASE (Main; Tiffany Oct 25 7:39pm):** /links leads with Find Your Mat-ch this week; Papaya Spritz moves down; add the Brownstone Bloom album card; release Brownstone Bloom this week with social mock-ups of the Brownstone Bloom mat in unexpected pairings. Check Planoly's week plan first.
