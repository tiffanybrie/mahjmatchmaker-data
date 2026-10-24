# The Desk

Rewritten nightly by the end-of-day desk cleanup (9:23pm ET). The morning HQ cleanup (6:47am ET) reads it. Rules: CLAUDE.md ("THE DESK"), docs/CHATS.md (which chat owns what). During the day, when an agent stops, Chrome drops or a QA stalls, add the item here right away with its next step.

**Last rewrite:** Fri Oct 23, 2026, ~9:45pm ET (desk cleanup run). Covers all 64 commits on Oct 23 ET, Planoly (IG workspace 019fc27c… and Pinterest 019fc27b…), HQ needs / log / albums / money, Ready to Ship NOW + ship answers, docs/ANSWERS.md, site/livepatch READMEs, the fym-site-preview branch and curl checks of the live site.

**Owners (three chats, Oct 22):** Main (Opus) = social/Planoly, site pages, email, HQ/DESK, decisions. Matches & Catalog (Opus) = Find Your Mat-ch, albums, gallery, catalog, search index. Ops (Sonnet) = the ONLY Chrome driver: Squarespace pastes, uploads, IG follows, verified-date refreshes.

**Usage:** weekly limit resets Sun Oct 25 11am ET (trig_01MrL5j re-enables the paused tasks at the lighter cadence). Tiffany Oct 23 9:19am + 8:35pm: go full speed on launch work; she buys extra usage when the limit actually hits; tell her the moment a chat hits it.

## Tomorrow's top priorities (Sat Oct 24), in order
Standing order: (1) Find Your Mat-ch™ launch Tue Oct 27, (2) fall content before it expires (Brownstone Bloom = next week's release, her Oct 23 7:12pm call), then holiday (November, through Find Your Mat-ch). Everything below follows it; no ordering question needed.

1. **FYM website copy is 8 versions behind (Matches & Catalog → Ops).** curl tonight: /find-your-mat-ch-preview still loads `site-app/fym-v72`. The artifact is at v80 (v79 racks mirror mats + v80 match card, published ~9:05pm). fym-site-preview has folders only up to fym-v77; the page block pin is v77 (@fb133512) and was never pasted. Tiffany tests from the website link on her phone, and the Oct 27 launch task reads README 0a, so a stale pin launches an old app. Next: (a) record an independent QA PASS for v79 + v80 in the repo (none recorded; only "(QA)" in the v80 commit title); (b) copy v80 to `site-app/fym-v80` on fym-site-preview (t78/, b23v1.js, b24v1 reachable + jsDelivr-warmed, rule doc 73); (c) rebuild + re-pin page-block.html and launch-oct27 README 0a; (d) Ops pastes the block, curl for `site-app/fym-v80/index.html`, Playwright 390/1280. Target: Sat midday.
2. **Weekend pre-launch social has nothing scheduled (Main).** Her plan: post all weekend, big push Mon, launch Tue. Planoly IG: 0 posts scheduled Oct 24-30, only drafts. In order:
   - **Smith swipe reel (her YES 8:44am on v6 with clicks)** is a draft dated Sat 10/24 11am CT, but her fixes were never rendered (navy ✕, Find Your Mat-ch™, current racks, new end card, Season 2 intro). Render from assets/reels/smith-swipe + scripts/social/smith-swipe-src, swap the file into Planoly draft 01a16793 (reminder, her song), or move its date if it can't be ready.
   - **Reel 1 (FYM hype)** needs her 2:22pm notes: a little slower, album flash fast-ish, "43 tile sets and counting" BIGGER and held, end the flash on Bam Bird Classic Tortoise, tag every brand significantly shown. assets/social/fym-launch/reels/render.py.
   - **Launch stories** (countdown-story-*.jpg: Papaya × Heiress OK for now; Cypress × Knox/El Tigre/Hunt Club/Palomino options, Tortoise draft; doc FYM-LAUNCH-CAMPAIGN rules: rotate mat brands, partner brands only, small phone = two doors) → ONE contact sheet in chat, one yes, then Planoly as reminder stories (countdown + link stickers) Sat/Sun/Mon. Pinned-row Reel 2 (app teaser) not started.
   - **Undate the rejected Papaya "Still available" story** (draft still dated Fri Oct 23 12pm CT; she rejected that framing 2:24am). Never delete.
   - **Partner launch email** (Squarespace "Partner Brands" list, Dropbox upload link, graphics kit): not built yet; she wanted it ASAP. Main writes, Ops builds the list.
3. **One Ops Chrome session for everything overdue (Ops; standing authority, no OK needed).** None of these happened Oct 22 or 23: (a) pre-launch homepage block, her yes Oct 21 3:22pm, curl tonight still 0 `mmfym` on / → now "overdue, Claude's job" (site/livepatch/home-prelaunch-fym/README.md); (b) site search header injection (site/livepatch/search, @c6e395f, QA passed); (c) welcome + album-request automations with pre-launch wording (approved Oct 23 2:27am; wording in the Oct 22 desk, docs/EMAIL.md §5 still shows nothing built); (d) verified dates (curl tonight: Soirée All Day Oct 10, Anders Ruff + Britt Mills Oct 9): refresh dates only, no code re-testing; (e) FYM page block from priority 1; (f) Soirée All Day IG follow + favorite. Save rollback text first, close every tab.
4. **Sunday after the 11am reset: the VIP FYM list + launch email revision (Matches & Catalog + Main).** VIP list below (also HQ `vip-sunday-fym-oct25`). Launch email must be revised and back on RTS `d-email-templates` before Mon Oct 26 (Montserrat-style "Here's how it works"; step screens rebuilt from the live app, mirroring the in-app tour; fewer arrows/text). Then update launch task trig_01ErZy so it only sends + flips automation wording (it still builds automations).
5. **Brownstone Bloom (fall, next week's release).** Her one tap on RTS `l-brownstone-v2` (31 cards + ♥/✕ on 13 missing mats) is HQ Today. On her yes: publish per site/livepatch/brownstone-bloom-oct20/README.md (code block pinned @0f8738b, 31/31 URLs warmed) in the week of Oct 26 so it lands before Halloween; re-date the Ep 11 Brownstone reel only after it's redone with an intro (social reset rules).

## Morning HQ cleanup adds (Sat Oct 24, 7:05am ET): overnight answers that are now Claude's jobs
- **EMAILS: DO NOT SEND (Tiffany, Oct 24 12:49am).** Build welcome, album-request and launch emails as Squarespace automation drafts for her final read; footer address is in ANSWERS. Main must re-check launch task trig_01ErZy so it does NOT send without her read (owner Main, today).
- **Work With page + new "brands" page with form (Main).** Her l-workwith6 notes (ANSWERS Oct 24); form answers land in the social calendar and get monitored in the daily email scrape. Fix the empty partner-ticker boxes.
- **Thin albums (Matches & Catalog).** Build cards for her 78-mat hearts; make the next quick-spot pages for the rest of the thin albums (bigger tile photo).
- **Malachite + Kingfisher (Matches & Catalog).** Add the match (non-partner, her pick → nonpartner_allow.json) with racks Miss Mahjong Jade, PLM Oak, Bam Bird Indigo; Scream Queens = no.
- **Tile images (Matches & Catalog).** Hummingbird tile image under the logo bar, smaller, off the racks (Hummingbird album too); Bam Bird tile image per Bam Bird's mock-up (her screenshot in chat). Vivienne: drop Hummingbird; stays parked.

## ⭐ VIP SUNDAY (Oct 25, 11am) FYM LIST, mirrored on HQ item vip-sunday-fym-oct25 (order 0). Same list both places; tick both.
Built in v79/v80 tonight (artifact only; website copy = priority 1):
- [x] Rack suitors: none preselected, tap shows on the mat image, 2nd splits the frame, max 2 (v79)
- [x] Rack heading back to "Make it a love triangle", "Pick your racks" under it (v79)
- [x] Picks OFF colour-ranks racks, partner racks first (v79)
- [x] Mat suitor back/remove (v79); 9-step tour (v79)
- [x] Match card: bigger logos everywhere, logos on mood board, left-aligned labels, nothing touching the code bar, transparent stacked racks, bottom band (v80). Header A is the default; A vs B is her pick (shown to her in chat as images)
Still open:
- [ ] BUG (7:53pm): swipe gesture stops after ~16 mat suitors (OMM Sierra); buttons still work. Fix + gate check (20+ hearts, phone + desktop)
- [ ] Filters beat picks: with Holiday (or a colour) on, first cards fit the filter; picks OFF re-ranks mats by colour, visibly different from ON (Heritage + Holiday, 8:27pm). Gate check
- [ ] Mat door = same intro as tiles door (tour link stays; "1 Swipe on tiles, 2 Pick your favorites, 3 Add racks"); tour works mat-first (8:24pm)
- [ ] Mat door swipes TILE SETS right after picking the mat (no frozen "Your mat" step); "See all" grid toggle on both doors (8:54pm)
- [ ] Coordinated collections first (brand's own matching racks/mats for a set, e.g. Bam Bird Deco); collection check per brand (8:01pm)
- [ ] Mat screen: "Uncheck your suitor to keep swiping"; tour step 1 text; tour racks step points at rack search
- [ ] Missing tile sets from docs/audits/tile-audit-2026-10-23.md, one row per colorway: My Fair Mahjong, Bespoke (standard only), Mahjong Studios, Let's Be Besties, Amahj On the Water, Green Light Gatsby, TdT House Clovers Warm White; verify the holiday name-matches
- [ ] Hidden/removed-from-FYM review list for her (photos + reason), one place
- [ ] Recheck the wrong "acrylic trays = no tiles" flags; rack cutout audit (Bespoke Highlighter Pink fringe)
- [ ] Bam Bird Classic Tortoise: her Canva photo 1400×1400
- [ ] Share caption auto-copied; PWA (live version every open, no offline cache); sticky box bug on the preview page; WebKit tour check
- [ ] (explore, not now) style/theme menu (Holiday, Earthy, Pastel, Floral); shade-level colour; contrast-aware ranking
- Kept out (her call): Splash of Color, Bespoke mega, OMM Debutantes

## In progress
| Item | Owner | Next step | Target |
|---|---|---|---|
| FYM v80 → website + launch pin | Matches & Catalog → Ops | Priority 1. | Sat Oct 24 |
| Smith swipe reel fixes | Main | Priority 2; Planoly draft 01a16793. | Sat 11am CT |
| Reel 1 hype revision + pinned-row Reel 2 (app teaser) | Main | Priority 2. Covers = the two existing pinned halves. | Sun Oct 25 |
| Launch stories → contact sheet → Planoly | Main | Priority 2. | Sat Oct 24 |
| Partner launch email + "Partner Brands" list | Main + Ops | Priority 2. Watch Dropbox /Mahj Matchmaker/Partner Photo Swaps daily after it goes. | ASAP, before Tue |
| FB group description v3 | Main | Her RTS change (8:47am, now in ANSWERS): drop "saves you money", use "Use our group code MAHJMATCH to save 10% or more at our partner brands". Rebuild d-fbdesc2 in place on RTS, then one yes. Goes in Oct 27 with the cover. | Mon Oct 26 |
| Overdue Ops Chrome session | Ops | Priority 3. | Sat Oct 24 |
| Launch email revision | Main + Matches & Catalog (screens) | Priority 4. | Mon Oct 26 |
| Launch-day tasks (homepage switch trig_011jdGG, email trig_01ErZy) | Main | Re-check both Mon Oct 26: README 0a pin = latest app; email task only sends + flips wording. | Mon Oct 26 |
| VIP FYM list | Matches & Catalog | Priority 4; gate + independent QA each publish; artifact AND website together. | Sun Oct 25 |
| Standing tile set audit | Matches & Catalog | `python3 builder/fym_tile_audit.py`; batches in the VIP list; Bam Bird done (v78). Add to the Monday cleanup. | Sun-Mon |
| Album pipeline (her Oct 23 7:05-7:12pm plan, docs/plans/album-content-plan-oct23.md) | Matches & Catalog | Brownstone (next week) → holiday features in FYM (Nov) → new holiday-set albums → Gatsby → Bam Bird MCM + Deco → Mahjong Row #2 → partner brands with no album (coverage table first). Inputs first: mat library audit incl. non-Shopify brands, ShopMy, Etsy, Amazon. Pick + lock the app tile photo at the START of each swipe book. | After launch |
| Bam Bird Classic Tortoise feature | Main | She picks the match from its album (pending); then a launch/post-launch piece, tag Bam Bird. | When she picks |
| Sunday Hummingbird album | Matches & Catalog | She asked how easy an album would be: answer with a size estimate next album session. | After launch |
| Papaya Beechwood README | Matches & Catalog | Live since Oct 22; README still says STAGED: mark LIVE next touch. | Next touch |
| Rack data (lengths, colour index, shop-by-colour, "goes with everything" shortlist for her approval) | Matches & Catalog | Her 8:35pm list (ANSWERS). Lengths: OMM + Mahjong Row 18.5"; MFM, B&B, M&M, TdT, Mahj Mood 20"; verify Virora, Anders Ruff, Mahjong Studios, Bespoke. Never a non-partner rack first. | After launch |
| Google feedback drafts (OMM TEACHMAHJ teacher-only, MJTI dead, Yellow Mountain, thumbs up x6) | Ops | Standing authority. Confirm MJTI dead, submit, log. | This week |
| Discount links not converted (Britt Mills, Mahjong Register, YMI, RMS, Hip Hip, Wren/Soirée/Amanda Toppe) | Main | Proof in builder/fym_fix_oct21/discount_check_oct21.json. | After launch |
| Missing swipe-book products (OMM Miracle / Twilight Waltz / Merry Mahjong / Santa Baby; PLM Spirit + Nutcracker; OMM Vault) | Ops → Matches & Catalog | Photos in Chrome → pending queue. | After launch |
| Bam Bird spike check fix | Main | Flag on ORDER COUNT (5+ or 2x 14-day avg) + release calendar cross-check; fold into the merged 3x sales task Sunday. | Sun Oct 25 |

## Waiting on Tiffany (only things she can answer now)
On HQ in this order.
- **Today:** (0) VIP list (read-only mirror); (1) footer mailing address for marketing email, in the HQ box (P.O. box works; before Mon); (2) reconnect Instagram via Facebook in Planoly (computer, 2 min; Tag people + collabs stay off until then); (3) Brownstone Bloom one tap on RTS.
- **This week:** Work With page yes/change (RTS l-workwith6, hidden page); Green Light Gatsby swipe (113 mats); Sunday sets round 2 (4 sets); thin-album swipe (78 mats); 3 FYM questionable photos; 3 missing sale amounts (Mahjong Co., Amahj Line, Middle & Main); Fait à Main link + code.
- **Asked in chat, not on HQ:** match card header A or B (images shown in chat Oct 23 ~9pm); her lost Pippa teardown (2-3 lines); Bam Bird Classic Tortoise match pick; do the other swiped mat albums (Larkspur, Revelry, Isla, Peony & Parasol, Art Deco Dayz, Spring Fling, Santa Baby's, Mat of the Moment Brownstone) park with Vivienne under her "no mat albums" call (Oct 23 6:50pm)? Ask once at the next album talk; until then they stay in Claude's queue untouched.
- **Parked until after launch (Oct 28):** holiday-or-not on 11 mats, ShopMy 5 quick calls, Amazon old-board delete, Shop page vs ShopMy talk, sender hello@ + DKIM/DMARC, bow lamp keep/swap, nav overflow pick. Etsy re-apply reopens Oct 26; Planoly Content Marketplace add-on keep/cancel by Oct 25 (HQ parked, shows Oct 25).

## Banked (finished, held on purpose)
- **Petalée (Virora)**: 61 cards, RTS `l-final-petalee`, vault (her Oct 23 plan). Before publishing: 10% band sweep on the Amanda Toppe/Girly cards, cleaner Petalwing/Coralia photos.
- **Vivienne mat album (OMM)**: 16 cards built, PARKED (her Oct 23 6:50pm: no mat albums; "The Mat Edit" likely dropped). RTS `l-viv-order2` hidden tonight.
- **Sunday Blues + Nature Walk**: vault once her round-2 swipe is in (never two Sunday sets back to back).
- **Green Light Gatsby**: swipe book built (113 mats), on HQ This week for her swipe (GO given Oct 23 7:05pm).
- **Season 2 episode reels + trailer**: undated drafts in Planoly (cleaned Oct 23 3am). DO NOT re-date assets/reels/s2/*.mp4 or assets/social/countdown/*: she rejected those versions. Each gets redone with an intro before it returns.
- **Miss Classic Malachite + Jade**: held for the restock window (week of Nov 3). Miss Classic tease draft dated Mon 10/26: re-check it fits the launch push before asking her.
- **Halloween**: Night of the Raven carousel (draft 10/28) + Happy Halloween story (10/31); only small throw-ins beyond that (her 7:12pm plan).
- **Holiday tables** (Polo Club 11/4, Rackin' Rudolph 11/6, Retro Rattan held): Planoly drafts.
- **Malachite 8 new cards, December 1994 (31), Spirit of Christmas (10)**: staged since Oct 20; holiday ones from Nov 1.

## Later / ideas
- **IDEAS / 3.0 (Tiffany Oct 23 7:25pm):** private studio view of FYM for her (pre-filtered by colour, measured colours on each mat, rank favorites/top 3, picks feed album builds); 3.0 table view (tablecloth, lamp, dice dish via ShopMy); 3.0 per-product links, but first TEST which partner links auto-apply the code (never OMM: code only).
- **Match Monday (Tiffany Oct 23 6:52pm, leaning; 7:12pm plan):** weekly Monday album from December, announced only after a few ship clean. Monthly Reader Request album later (list private; "you voted it in"; outreach lever). Community name = "Matchmakers" (brand guide).
- **Colour model (Oct 23 8:01pm):** contrast + secondary tile colours by shade; "orange isn't just orange"; gallery and app mirror each other.
- **Holiday gift series from ShopMy share videos (Oct 22 5:14am):** one reel/story per shelf; she taps Save, Claude loads Planoly. IG bio says "Find Your Match" → update at launch.
- **Rebecca Illustrated, 15% ShopMy (Oct 22 5:01am):** whole mat line into gallery + FYM pending queue, ShopMy links, IG onboarding, shelf cover. After the Sunday reset.
- **Aurora's racks (Oct 22 4:48am):** remind her to match them herself (19" only; never in Claude's mat-level picks).
- **Colour suggestions → album candidates (Oct 22 4:22am):** after launch.
- **FYM share + #mahjmatch (Oct 22 4:27am):** reshare "Great match by @…" posts after launch (ask permission); watch the hashtag Mondays.
- **Pinterest ShopMy single-product pins at scale** after the Oct 24 test (10 pins, 1/day 18:00Z; check published, not flagged, go.shopmy.us resolves).
- **Weekly IG brand watch** from Mon Oct 26; handles still needed: Splash of Color, Hip Hip, Yellow Mountain, Mahjong Register.
- **Brand alert sign-ups**, keep-Planoly-paid by Oct 26, comment-for-link, UPS cutoffs Dec 1 (Q4 plan, Oct 21).
- **Site colours** (one rainbow + Yellow/Orange pages), "Press for Mahjong" rename, holiday set count (she counted 12): after launch.
- **New brand releases** (Oct 22-23 launch watch): Anders Ruff Bellamy Bloom / All American / Boston Mahj Party / Heritage Tartan; Bespoke x Brooks Brothers; Britt Mills Emerald Mirage + House Print; Bespoke x Gray Malin Very Merry Getaway; Tigre Domino Blonde; Sunday Emerald racks + Cola restock (record only); Splash holiday mats (digest at 10; she keeps Splash tile sets out). HQ Albums → Not started.
- **Weekly /links refresh** from Sunday; **$200/mo API credits** plan after launch (Oct 22 1:32pm).

## USAGE PAUSE + NEW CADENCE (until Sun Oct 25 11am ET)
- Paused Oct 23 4:20pm: Google code report, daily indexing, release radar. Still running: sales check 10:04pm ET, HQ cleanup 6:47am, desk cleanup 9:23pm. Brand launch watch + email watch were paused earlier.
- Sunday: trig_01MrL5j re-enables at her lighter cadence (Oct 22 3:45am): sales 3x daily in ONE task; brand watch (sites + emails) twice daily; HQ inbox daily; desk nightly + HQ daily; Mahji Mentor + onboarding daily; Pinterest every 3 days; Google code report a few times a week (merge the AI answer check); Match Builder weekly; watchdog + morning brief off. Fix the CHECK, not the frequency.

## Daily operations (Fri Oct 23)
| Operation | Done today? | Notes |
|---|---|---|
| Affiliate tracking (Money tab) | ⏳ Not yet | The one daily sales check fires 10:04pm ET. Oct 23 doc shows $0 as of 12:43am. Oct 22 closed partial at $445.17 (26 sales; Bam Bird record 9 orders $231.20); Mahjong Co. + Amahj Line amounts missing (HQ This week). October to date $5,653.04. |
| Google code report | ✅ Ran | Project doc 99d (Oct 23), then paused at 4:20pm until Sunday. |
| Verified dates | ❌ Not done | Pages still say Oct 9/10. Ops priority 3 (standing authority). Scheduled run Sun Nov 1 (trig_01PGtT8). |
| Pinterest queue health | ✅ OK | 4 pins/day scheduled Oct 24 → Nov 17, 0 failed. Autopin paused; queue covers it. |
| Indexing | ⚠️ Partly | 1 requested (/blog/mahjong-buying-guide); nothing else eligible (13 planned albums still 404). Next: /mahj-matchmaker-community (Oct 24+). |
| Planoly next-7-days (IG) | ❌ Not covered | 0 scheduled Oct 24-30; all drafts. Priority 2. |
| FYM feedback inbox | ✅ Morning | Only a test message (HQ cleanup 6:59am). |
| Brand launch watch | ✅ Ran (before pause) | Splash holiday mat, Sunday Emerald racks, Sunday Cola restock (record only). |
| HQ + Ready to Ship cleanup | ✅ Done | Morning run (11 → 10 open) + this desk run. |

## Never-ending projects
- **Find Your Mat-ch™ app** (artifact 6epA9HuEdT32zUp79Qv3kd): gate + independent QA before every publish; artifact AND website copy AND README 0a pin in the same step; locks; pending queue; photo flags; her feedback the same day with a gate check.
- **Google / MAHJMATCH in AI answers**: code report, indexing, verified dates on the 1st and 15th, brand-guide pages.
- **Albums**: built through the app (lock the tile photo first, Coquette-size colour shortlist, racks carry over), her yes, live; thin albums; holiday features in FYM.
- **Social**: every approved post in Planoly at its time; auto-post wherever possible; every slide to stories; brand tags; collabs; partner brands only in launch promo; cross-brand features.
- **Pinterest**: queue within the pace rule; evergreen pins of our own images.
- **Affiliates + money**: daily commission checks with spike AND drop checks; onboarding new partners (page, hub, logos, FYM, indexing, IG follow/favorite).
- **Mat Gallery + colour system**: sort rule, holiday rule, partner-only gate.
- **ShopMy + Amazon storefronts**: shelves, covers, collages.
- **HQ hygiene**: Today ≤5, nothing she can't answer, no outdated drafts; ANSWERS.md before asking anything.

## Log of this rewrite (Oct 23 night)
- Found done since the Oct 22 desk: FYM v75 → v80 on the artifact (rack mirror, 30-second tour, Bam Bird 16 colorways, mat search fix, racks mirror mats, match card); Smith swipe v6 recovered and confirmed (her yes 8:44am); Planoly cleaned of the rejected S2 reels + countdown; launch campaign brief, launch stories and Reel 1 built; partner Dropbox upload link made; album + content plan written; tile audit made standing.
- Found orphaned and given a home: FYM website copy stuck at v72 (pins never pasted, v78-v80 never copied) → priority 1; no independent QA PASS recorded for v79/v80 → priority 1a; her RTS change on the FB description (8:47am) was never logged → ANSWERS + brand guide + Main v3; Smith fixes never rendered for the Sat draft → priority 2; Reel 1 notes not applied → priority 2; rejected Papaya "Still available" still dated → undate; all Ops Chrome work slipped a second day (homepage block now overdue) → priority 3; VIP list on HQ was missing the 7:53-8:54pm items and didn't show what v79/v80 finished → HQ updated.
- HQ: launch-week copy need narrowed to the Work With page (FB description answered with a change; partner email being rewritten) and moved to This week; Vivienne → Banked (parked); Sunday sets + Gatsby → Needs your yes (swipe pages open now); RTS l-viv-order2 hidden.
- Priority order follows the standing order; no "Set tomorrow's order" need added.

See CLAUDE.md.

## Oct 24 (Matches & Catalog)
- Green Light Gatsby swipe book REBUILT (artifact PNi1a7ckEZKQwxDs88sVJ7 v2): color card first (assets/colorcards/green-light-gatsby/), 45 mats = colour pull (weighted palette emerald 55 / mint 15 / copper 15 / sage 10 / ivory 5) from FYM-visible mats + her Drake/Emerald picks, cut by eye from 154. The old 113-mat book had Four Winds Social + Mahjong Studios mats (banned) and wasn't a colour pull.
- [ ] Ops (Chrome): scan Tiles & Tablescapes FB group for "Gatsby" mat suggestions -> add as "TNT rec" to the book; note brands we don't carry for outreach.
- [ ] Bam Bird Deco album: colour card first (Mulberry/Lagoon/Indigo) + 3 Deco Dragon mats + Deco racks, same process.
- Brownstone order page: cards now bundled in the artifact (external jsDelivr images are blocked inside artifacts).
- Gatsby round 1: 32 yes of 45 (her: "good start; mostly Gatsby's own green"). Round 2 published (same book, first group): 26 complement/coordinate mats (wine/berry/plum, copper/cognac/rust/gold, each with a green or cream tie-in), cut by eye from 120. Matching photo = compilation (row of faces + back close-up + tiles on mat).
- [ ] AMAZON MATS ARE NOT IN OUR LIBRARY (Tiffany Oct 24: always pull Amazon + Etsy). Etsy is in FYM (Betty June & Jeannette, Sophie Clima, etc). Amazon: her list "Mahjong Mats I Love" (34 ASINs, doc 97b) needs ingesting into the mat gallery + FYM with photos + colour. The cloud shell can't read Amazon pages: Ops (Chrome) grabs title + main image + ShopMy/tagged link per ASIN into config/amazon-mats.json; Matches & Catalog then measures colour and adds them.
- [ ] OPS (Tiffany asked Oct 24 10:02am): paste FYM v82 page block on the HIDDEN /find-your-mat-ch-preview page so her husband can test on his phone (artifact email-sharing fails). Block: https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@9d98705d8cb21aa52684bb0d37249486bf418332/site/livepatch/fym-preview-oct21/page-block.html . Verify curl contains site-app/fym-v82/index.html. /find-your-match stays the teaser until the Oct 27 launch task (its 0a pin is now this same block).
