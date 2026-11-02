# The Desk
Rewritten nightly by the end-of-day desk cleanup (9:23pm ET). The morning HQ cleanup (6:47am ET) reads it. Rules: CLAUDE.md ("THE DESK"), docs/CHATS.md (which chat owns what). During the day, when an agent stops, Chrome drops or a QA stalls, add the item here right away with its next step.

**Last rewrite:** Sun Nov 1, 2026, ~9:55pm ET (desk cleanup run, cloud, no computer linked). Covers the 81 commits of Nov 1 ET (e850b65 … 5964498), docs/ANSWERS.md (Nov 1 lines), docs/MATCH-INBOX.md, Planoly (IG workspace 019fc27c… all 55 groups + Pinterest 019fc27b… scheduled queue), HQ needs (34 open → 25) / hq/albums / hq/now / hq/priorities / hq/social / log, Ready to Ship NOW (0 open), site/livepatch READMEs, config/release-calendar.json, content_lint (repo + Planoly IG export), curl checks (Brownstone checklist, Tinselle stock).

**Owners (three chats, Oct 22):** Main (Opus) = social/Planoly, site pages, email, HQ/DESK, decisions, Google + SEO. Matches & Catalog (Opus) = Find Your Mat-ch, albums, gallery, catalog, search index. Ops (Sonnet) = the ONLY Chrome driver: Squarespace pastes, uploads, IG follows/checks.

**Repo note:** checkout on `partner-catalogs-sqsp` (~4.7 GB with assets). A plain fetch hangs. Tonight's working recipe: `git fetch --filter=blob:none --depth=80 origin partner-catalogs-sqsp:refs/remotes/origin/partner-catalogs-sqsp`, then sparse checkout without `/assets/` (add back `/assets/**/*caption*.txt`, `/assets/**/captions/*`, `/assets/reels/s2/captions.json` so content_lint runs). Never `git ls-tree -l` on a blobless clone (fetches every blob).

**PARTNER SEND GATE (Oct 27 3:08am, standing):** before scheduling ANY partner email or graphics drop, run `python3 scripts/partner_send_check.py`; it must exit 0.

- **HQ PIN (Nov 1): needs/supabase-settings-nov01 stays at the very top of HQ (order -100) until she does it. Nothing above it. Morning cleanup must not move it.**

## Tomorrow's top priorities (Mon Nov 2), in order
Standing order: RESTOCK FIRST (rule c), then Google #1 (Tiffany Oct 29 11:03pm), then the newest ANSWERS (Table view ASAP, target live Mon night; holiday launch Tue/Wed to show it), then DESK 'Never-ending'. **Restock check (c): no album-set restock is dated for Mon Nov 2.** Tinselle Emerald (Oct 31) is still in stock but its card expired (rule 9, archived tonight). Next dated: TdT House Tigers Tue Nov 3 4pm CT (not an album set; record + FYM stock), Sunday Blues ~Nov 23-30 (album #3), Bam Bird Deco Indigo mid/late Nov (album #2 trio). The order is clear, so no "Set tomorrow's order" card.

1. **Google (Main + scheduled tasks).** (a) Indexing: 9 pages waiting: Mahj & Vine, Splash of Color, The Mahjong Press, Mahjong Studios, Let's Mahj On (since Oct 27, over the 3-day rule), Anders Ruff, I Love Mahj, Wren Mats + the new **Brownstone Bloom album** (new-album check f: not yet requested; hq/indexing has the 1:30am quota hit). Sunday's 1:15pm run hit quota; later runs had no browser. Needs her computer on (HQ Today card alert-indexing-2026-11-01, order -99). (b) Morning report: AI answers + Search Console carried over from Sunday (Oh My Mahjong first); Tigre de Tartán + Charleston still to re-check (lost Oct 31). (c) **Verified dates task Mon 8:17am ET** (trig_01PGtT8NFXe6341WjBHqmYJu; last recorded run Oct 21): if no "Verified dates refreshed" HQ log by 10am, Main runs it by hand. (d) Codes post: Monday draft task 7:37am (FB GROUP only). (e) Google code report is due Mon (Mon/Wed/Fri).
2. **Table view → live Mon night (Matches & Catalog).** Preview v14 passed independent QA Sun ~9:30pm and is with her (HQ Today needs/tableview-storyboard-nov01, artifact 5QjNXjw15MuZTqzDT1ptbp). Commit 43b9ca7 (tablet/small-desktop sheet keeps the whole card visible) is BUILT + HELD, not published: fold it into her next round. On her + husband's notes: fix → gate → independent QA → publish as FYM 1.14 to BOTH places (artifact + /find-your-match + /find-your-mat-ch-preview + README 0a pin) → scripts/swipe/fym_snapshot.py. Else Tue. Then Main/social: holiday reels redrafted to show Table view.
3. **Planoly next 7 days = 0 IG posts scheduled (Main).** Audit (d) tonight: nothing scheduled Nov 2-8 (01a16052-2828 is the stale Oct 21 Papaya reminder still "scheduled"). Dated drafts in the window: Polo Club reel + story Wed 11/4, Rackin' Rudolph reel + story Fri 11/6, both with no Facebook target, no her-OK, reel captions FAIL lint (length 544/431, no #MahjMatch). Default kit = next week's storyboards (HQ Today needs/social-week-2026-11-02, order -96; album-of-the-week kit, brand-mix default b). The Mon 10am Merry Mahjong kickoff moves to the Tue/Wed holiday launch. ON HER YES: render finals, Planoly IG + Facebook Page targets (brand NAMES on FB), every slide as a story, Tag people from config/social/ig-handles.json, `content_lint.py --planoly <export> --only-ig` must pass. I could not add FB targets tonight: the API can't add a target to an existing group and recreating means deleting the old one (never delete) — do it on her yes.
4. **MATCH-INBOX older than 2 days: 37 open (Matches & Catalog).** Tonight 7 lines marked DONE with proof (Dapper 2 ×3, brand menu copy, shop-by-colour partners first, In stock only, My stars → shipped in 1.11/1.12). Real work left: Sunday Green Gingham / Blue Gingham / Blue Rattan Premium (Oct 29); Britt Mills leatherette versions (Oct 27); late partner holiday mats into albums (waits on her Send); 69 FYM mats with no gallery row (gate [90]); 38 angled photos (gate [89]); rack length by tile size + tortoise rack order; Spirit of Christmas composite; TNT recs not in FYM (Sloan Story …); Hummingbird black background; FYM default tile-set order. **Same day Tue Nov 3:** Noli June FA LA LADIES 4 mats → FYM + gallery the day they list (6am CT); LBB Electric ZigZag + Christmas Lights (Nov 1 6:10pm line). FYM thin-picks patch (thin hearts are live).
5. **Overdue + mid-way Claude jobs (Ops with Chrome, Main).** (a) ~~FYM 1.13 onto /find-your-mat-ch-preview~~ DONE Nov 1 ~9:40pm (commit 5964498; curl tonight: fym-v113). (b) Main: the **Nov 2 monthly site check (HQ log 2026-11-02-site-maintenance) could not push** (proxy 403): commit 07358309 (DESK OPS line, MATCH-INBOX line, tile-retired.json, docs/audits/site-maintenance-2026-11.md, site/livepatch/site-maint-nov02/) exists only in that cloud session. It is NOT in the repo. Re-run the site check attended (or rebuild from the HQ log detail): 36 dead links, 73 cards newly Retired, Astor/Vivara/Year of the Horse relinks, 2 layout issues; Emerald + Pearlescent Retired labels wait on her default-yes card (needs/site-maint-2026-11, defaults go ahead Wed Nov 4). (c) OPS: Dropbox copies of LBB Electric ZigZag + Christmas Lights flat renders → /Mahj Matchmaker Albums/New releases/Let's Be Besties/ (Chrome method in ANSWERS Nov 1 12:50am). (d) Amazon 'A Reindeer Holiday Table' board (approved Oct 30) when a chat she's in has Amazon signed in.

## Handoffs (do first)
- **Main:** re-run / rebuild the unpushed Nov 2 site check (priority 5b).
- **Matches & Catalog:** commit 43b9ca7 Table view tablet fix is held, not published (priority 2). FYM 1.12 follow-ups still open: nightly stock check needs a publish path before it can be a scheduled task; rack cut-out review for the 12 hidden racks (builder/fym_fix_nov01 README step 3b); Mat Gallery rows (gallery_rows112.py); two-color coordination ranking bonus.
- **Main: Raven reel + Halloween story are BANKED.** Clear the dates (never delete) on Planoly 01a16477-0b08 (story, 10/31) and 01a16477-092f; plus the past-day drafts list in "In progress" (Planoly cleanup).
- **Main: CONTENT BANK on her yes (HQ needs/content-bank-2026-10-31, week of Nov 9-15).** Planoly IG + FB Page + every slide as stories, brand @mentions, Tag people, collabs; dates per assets/social/week-2026-11-09/README.md; captions lint 12 / 0 FAIL. 8 FYM pins queued pending in config/pinterest/queue.json.
- **Main: duplicate catch-up tasks** trig_019StaM8LkmrxGKtK7xhXang (old) + trig_013ZpyRxFivSKPoYTgSvVBU6 (new): pausing one is her call, on HQ rules-audit-2026-10-30.
- **Main: sales-check prompt fix** (list ALL secomapp + goaffpro + backinstock emails, refunds on the refund date, read tiffanybrie@ at mail.google.com/mail/u/1 per her Oct 31 3pm rule). Still not applied.
- **Main: "close leftover finished Claude tab groups at start" in every Chrome task TAB RULE** (Oct 30 10:10am). Not done.
- **Main: mat-edit-alert build step in launch watch trig_01S2VsjwznnHev1uUbYmEwJq** (Oct 30 9:05am; docs/MAT-EDIT-ALERT.md). Not done. Poppins piece waits on its paired tile set announcement.
- **Pinterest autopin** was blocked by the usage limit Sun 9:41am; its next run is Wed Nov 4. Planoly Pinterest has 3-4 pins a day scheduled through Nov 9, 0 errors, so no gap; Main re-checks Wed.
- **OPS (standing): HQ ShopMy tab inbox** (db `shopmy`, status new) at the start of every Ops reply. The 2 stray ShopMy links are HER click (HQ needs/shopmy-delete-2-links: a ShopMy delete can't be undone).
- **Partner feedback watch** trig_01RKw9eUwTYPo39gbYHb65gh runs daily through Nov 10 (0 new Nov 1).

## In progress
| Item | Owner | Next step | Target |
|---|---|---|---|
| Google: 9 pages to re-index, carried-over AI check, verified dates, codes post, code report | Main + tasks | Priority 1; needs her computer on. | Mon Nov 2 |
| Table view (full preview v14) → FYM 1.14 | Matches & Catalog | v114 round 3 (after independent QA Nov 2): 120 Table racks re-cut (incl. Bam Bird pusher sticks removed, see-through clear acrylic, black + white acrylic from brand top-down photos), none grayed for white edges; rack filter singles; Table tour step; price chips on all 3 decks with 'Under $X with code MAHJMATCH' note. Gate + --site PASS. Website copy fym-site-preview @5cf22b3 (site-app/fym-v114, jsDelivr warm, NOT pinned); Preview artifact 5QjNXjw15MuZTqzDT1ptbp v17 (~253.7 of 256 MiB, 512 files). Next: QA re-check of racks → her morning test → her OK → publish live artifact + README 0a pin → fym_snapshot.py. | Mon Nov 2 night (else Tue) |
| Next week's social (Nov 2-8) | Main | Her yes → render → Planoly IG + FB Page + stories. | Mon Nov 2 |
| Holiday launch + holiday reels redo (with Table view) | Main | Her detailed notes (HQ This week) → redraft; no re-render before. | Tue/Wed Nov 3-4 |
| MATCH-INBOX (37 old) + Noli June FA LA LADIES + LBB new mats | Matches & Catalog | Priority 4. | Tue Nov 3 |
| Nov 2 monthly site check (unpushed) | Main → Ops | Re-run attended, then OPS pastes from its README. | Tue Nov 3 |
| Sales dip watch (FAMILY20 ended Sun) | Main | Mon vs last Mon; Tue: Mahjong Row Google answer + page if still <3/day. | Tue Nov 3 |
| 9 amounts | Tiffany / Main | Her screenshots (HQ Today). | Mon Nov 2 |
| Holiday colour cards (Tinselle ×2, Dec 1994, PLM Spirit + Nutcracker) | Matches & Catalog | Not started (was due Oct 31). | Wed Nov 4 |
| My Fair Mahjong Style of Your Life (#1 album) | Matches & Catalog | Colour card + TNT, then swipe book. | Tue Nov 3 |
| Sunday Sets TNT rec leftovers | Matches & Catalog | docs/research/sunday-sets-colorcards-tnt-oct29.md. | Tue Nov 3 |
| Larkspur hearts into 27 tile albums | Matches & Catalog → Ops | Ops trip done; paste album by album. | Wed Nov 4 |
| Bam Bird Deco trio (Indigo first) | Matches & Catalog | Colour cards ×3, then books. | Week of Nov 9 |
| Affiliate applications (6 apply-first brands) | Tiffany submits / Main | Kit doc 00h; HQ apply-kit-oct31. | This week |
| Planoly cleanup (her Oct 27 ask) | Main | Clear dates (never delete) on past-day drafts: 01a16052-33a6…-40c3, -36fd, -3da0, 01a16793-3e02, 01a16477-0ce9, 01a17a6a-943b/-95d3/-9777, 01a17c71-b34b, 01a17c72-0c6d/-0e9a/-11d0/-152c, 01a17a6c-10e4, -12c1, 01a16477-092f, -0b08; 01a16052-2828 still "scheduled". | Mon Nov 2 |
| FB group weekly Claude Doc | Main | https://claude.ai/artifact/54ovPaB6BQU78ztjUgQSbe; keep current. | Mon Nov 2 |
| Mahj Mood code check (unused codes expire after 4 months) | Main | Before the next Mahj Mood post. | Mon Nov 2 |
| Tortoise rack piece (her Oct 28) | Main | Scope + storyboard; gift-guide tie-in. | Wed Nov 4 |
| UpPromote accounts → mahjmatchmaker@ | Main | Her logins where the owner must move it. | Wed Nov 4 |
| Discount links not converted (Britt Mills, Mahjong Register, YMI, RMS, Hip Hip, Wren/Soirée/Amanda Toppe) | Main | builder/fym_fix_oct21/discount_check_oct21.json. | Wed Nov 4 |
| Amazon mats into gallery + FYM | Ops → Matches & Catalog | Her picks only. | Wed Nov 4 |
| ShopMy holiday leftovers | Main → Ops | ShopMy (not MAHJMATCH) for Charleston Mahjong Club + Bamlet's in holiday posts. | Wed Nov 4 |
| Search logging | Main | Needs her Apps Script URL (site/livepatch/search README "Tracking"). | Ask once |
| Fait à Main code | Main | MAHJMATCH still not applicable at cart. | Watch |

## Waiting on Tiffany (only things she can answer now)
**On HQ Today, in this order (5):**
1. **Supabase + Resend settings** so Find Your Mat-ch sign-in emails send (pinned -100).
2. **Google: leave the computer on with the Claude app open Monday morning** (9 pages + carried-over Google checks).
3. **Test the full Find Your Mat-ch Preview with Table view** with her husband, notes in chat.
4. **9 amounts** (screenshots).
5. **Next week's posts (Nov 2-8): yes all, or yes/no per day** (Planoly is empty).

**On HQ This week:** sales dip plan (watch only); late holiday picks: tap Send final answers; Holy Mahj from her Canva; quick 1.13 check (TdT link-only + PLM chartreuse); content bank week of Nov 9; holiday reels detailed notes; Work With v3 live yes; face-to-camera + AMA drafts; Sunday Sets round 2 (4 sets); launch reel redo OK; affiliate apply kit; FYM accounts which way; Bama Mahj skip / non-partner / exception; Brownstone keep/drop 3 retired OMM mats; yellow & gold borderline mats; Emerald + Pearlescent Retired labels (default yes Wed); rules check: pause 2 old tasks?; Noli June sneak peek; 2 stray ShopMy links.

**Asked in chat, not on HQ (the owning chat asks once, next time she's there):**
- Main: did she post the FB group codes post herself (Oct 29)?; Malachite how-to reel v2 OK + day; FB group B&B racks wording; subscriber "It's here!" email send or skip; ShopMy 2-hourly pickup yes; Santa Baby's 12 yes; Apps Script URL for search logging; her Nov 1 5:47pm message cut off at "that has nothing to do with the number of" (ask her to finish the thought).
- Matches & Catalog: Lagoon + Mulberry splits; Bam Bird Classic Tortoise match pick; Sunday Rattan: is the 'new' one the Blue Rattan (her Nov 1 4:50am question back to us: answer it); Fruit Stand rack-edge (default a).

## Banked (finished, held on purpose)
- **Petalée (Virora)**: 61 cards, RTS `l-final-petalee`, vault (her Oct 28). Before publishing: colour card, 10% band sweep on the Amanda Toppe/Girly cards, cleaner Petalwing/Coralia photos.
- **Night of the Raven mood board reel (Canva) + Halloween story (Planoly 01a16477-0b08) + old Raven carousel (01a16477-092f)**: not posted for Halloween 2026; keep for next Halloween.
- **Vivienne mat album (OMM)**: 16 cards, parked (no mat albums, Oct 23); its hearts go into the tile albums.
- **Season 2 episode reels + trailer**: undated Planoly drafts (Ep 1-13). Each gets an intro first; captions fail lint (length + "Find Your Match" naming): rewrite before reuse. Jade "Smith-style" reel parked (needs her song).
- **Holiday tables** (Polo Club Wed 11/4, Rackin' Rudolph Fri 11/6, Retro Rattan undated): Planoly drafts, need her OK + caption lint fixes (length 544/431, no #MahjMatch) + FB targets (recreate the group; never delete) before scheduling.
- **Holiday reels Nov 1** (intro 'We made a holiday list', FYM Nutcracker, Holiday Vault + albums carousel, 3 brand reshare reels; assets/social/holiday-nov1/): built, held for her detailed notes (Nov 1 6:11pm: don't re-render yet). HQ needs/holiday-intro-2026-11-01.
- **Face-to-camera script + Ask Me Anything carousel** (assets/social/next-week-talk/): drafts, HQ needs/talk-and-ama-2026-11-01.
- **Poppins mat-alert set** (assets/social/mat-edit/poppins/): held until OMM announces Poppins' paired tile set.
- **Partner kit explainer video v2 + launch explainer reel + tutorial reel**: built, not used.
- **Restock companion frames** (assets/social/restock-oct27/, restock-huntclub-oct30/, restock-tinselle-oct31/): reuse at the next restock. Hunt Club + Tinselle Emerald cards expired (rule 9; Tinselle still in stock Nov 1 night).
- **Brand-locked FYM sample (Mahjong Row & Co.)**: "keep exploring" (her Oct 30); docs/brand-lock/STATUS.md.

## Later / ideas
- IDEA (Tiffany Nov 1 11:33pm, not now): fold racks into the mat step (no step-3 jump) for Aerial/Table views — racks come in/out on the same view like the match card; only Up close needs a jump. Revisit once Table view is live and if Table/Aerial become the main view.
- **Clean up 52 legacy caption lint warnings** (still 52 Nov 1) (config/social/content_lint_baseline.json; mostly missing #MahjMatch, '(affiliate)', 2 TdT captions) (rules audit E9, Oct 30). Also 78 legacy FAILs (length 42, naming 36) in banked Season 2 captions: same kinds as yesterday, nothing new.
- **Noli June FA LA LADIES** winter collection (4 mats incl. Hanukkah + ski) Tue Nov 3: new products → FYM + gallery the day they list (HQ sneak card, Oct 31).
- **Tigre de Tartán House Tigers** return Nov 3; **Mary Benson Hydrangea tiles** Mon Nov 2 12pm/1pm ET (non-partner); **Maison Mahj** bags Nov 1 / House Line windows Nov 1-4 (record only); **CMC OTG247** announced Nov 1 (release calendar, Oct 31).
- **Mahjong Register** Crystal Palace acrylic racks + Solid Wood racks (launch watch Oct 31): racks, FYM rack lists when Matches & Catalog has room.
- **Sunday Vegan Leather mat moved listing** (launch watch Oct 31): relink the FYM card in the next build.
- **Brands later (her Oct 31 picks):** Feltectors, Four Winds Social, Mahj House Rules, Mahjong Made Chic, Mahjong Moxie, Silk Mahjong, The Mahjong Line (teacher program only).
- **LBB Artist Collective mats** (early Nov): new products, never albums (Oct 30).
- **Bam Bird restock/brand announcement** teaser (IG Oct 30): same day or never.
- **Amanda Toppe Lila**: travel Lila Mon Nov 2 10am ET (no album); full-size later = swipe book the day it lists (Oct 29).
- **Table view later**: walls for pattern-back sets with no back photo (grayed), mats+tiles price filter (racks have it), aerial photos from partners, Table view as a partner perk vs open to all (undecided, don't push) (Tiffany Nov 1).
- **Splash of Color digest**: 4 undigested Splash mats (Kitschmas Mahj Club, Jolly Nostalgic Santa…); digest at 10+ (launch watch Nov 1 6:10pm).
- **Mahjong Row Rosy / Ellington** not on their store yet (partner watch Nov 1).
- **FYM default tile-set order by brand logos + commission ranking** (Oct 29 3:29pm).
- **Brand-locked FYM as a partner perk** (Oct 29 12:41pm); **brand demand data for partners**; **accounts / stars** (Oct 29 1:00pm).
- **Rakuten** skipped (Oct 29 11:17am).
- **Let's Mahj On 7 new tile sets** mid-Nov: new products, never albums unless she says (Oct 29).
- **Table view as a partner perk vs open to everyone**, **partners opt in with aerial photos**, **ask Emily about a pusher** (Oct 28).
- **"Mahj Garage"** accounts + "I own this" (Oct 28); competitor Mahj Closet ($9.99) (Oct 27).
- **IG Saved "Save for repost"**: partner reposts 1-2/day; holiday reposts from Nov 1 (Oct 28 10:04am).
- **Restock page** (Oct 28 10:31am).
- **Mahjong Row & Co. fall collection** + **OMM green set** jump the album line the day they drop (Oct 28).
- **Charleston Mahjong Club Après-Ski small album + Cabana Club**; **Peach and Pine** + **Fire + Fortune** after Nature Walk (Oct 28).
- **Gift content from early/mid Dec** (Oct 28).
- **Build your set extras**, **Mahj registry, AI "dream mat", dream set builder** (Oct 27).
- **Content like @mahjandmotif**; **a better FYM reel** (Oct 27; docs/FYM-REEL-RULES.md).
- **Partner portal**, **separate desktop vs mobile FYM**, **mat-only brand "eye candy" story**, **OMM reshares only 100%-OMM content**, **FB group growth plan** (Oct 25-26).
- **Canva template library + #MahjMatch reshares** (Oct 25); **IDEAS 3.0** (Oct 23); **internal FYM sets view**, **every-tile-set gallery**, **Pinterest ShopMy single-product pins** (Oct 24); **Match Monday / Reader Request** (Oct 23); **Rebecca Illustrated 15% ShopMy**, **Aurora's racks** (Oct 22); **brand alert sign-ups, comment-for-link, UPS cutoffs Dec 1** (Oct 21); **site colours, "Press for Mahjong" rename**, **$200/mo API credits plan** (after launch).
- **New brand releases** are NEW PRODUCTS, never albums (Anders Ruff Bellamy Bloom / All American / Heritage Tartan; Bespoke x Brooks Brothers; Bespoke x Gray Malin; Britt Mills Emerald Mirage; Mahj & Vine Whispering Winds; LBB Butterscotch Floral).

## Daily operations (Sun Nov 1)
| Operation | Done today? | Notes |
|---|---|---|
| Affiliate tracking (Money tab) | ⚠️ Done with gaps | Sales checks ran; Nov 1 sales logged (Anders Ruff $28.89 filled), 9 amounts open (HQ Today). Sales alarm: Sat 7 sales vs 17.6 avg, cause Mahjong Row FAMILY20 (ended Sun night); plan on HQ This week. 12:04am close-out still to run. |
| Google code report | ➖ Not due | Mon/Wed/Fri: due Mon. Morning Google & Revenue report ran PARTIAL (10:54am + 2:50pm + 6:48pm re-runs; no computer: AI answers + Search Console carried over). |
| Verified dates (weekly, Mondays) | ➖ Not due | Mon Nov 2 8:17am ET. Watch it (priority 1c). |
| Codes post (Mondays) | ➖ Not due | Draft task Mon 7:37am (FB GROUP only). |
| Pinterest queue health | ✅ OK | Planoly Pinterest: 30+ pins scheduled Nov 2 → Nov 9 (3-4/day), 0 errors. Autopin 9:41am blocked by usage limit (next run Wed Nov 4); queue.json has Brownstone pins. |
| Indexing | ❌ Not done | 1:15pm run: quota exceeded on the first request; later runs: no browser (computer not linked). 9 pages waiting (priority 1a). Sitemap now lists Brownstone. |
| Planoly next-7-days (IG + FB Page) | ❌ Not covered | 0 IG posts scheduled Nov 2-8 (priority 3). Planoly IG lint: 63 captions, 81 FAIL, all on past-dated or unapproved drafts (the 11/4 + 11/6 reels among them). |
| New albums (last 7 days) (f) | ⚠️ 1 miss | Brownstone Bloom (live Nov 1): /mahjong-tile-matches ✅, /ivory-mahjong-tile-matches ✅, /anders-ruff-discount-code ✅, /links latest album ✅, Pinterest queue ✅ (54 lines), sitemap ✅; **indexing ❌ not requested yet** (quota) → priority 1a. FYM album link → MATCH-INBOX (Nov 1 ~1am line). |
| Repo caption lint (g) | ⚠️ Legacy only | 78 FAIL (length 42, naming 36), all banked Season 2 captions; 52 legacy WARN. Same kinds as yesterday, nothing new. Holiday Nov 1 captions pass. |
| Restock first (c) | ✅ Checked | No album-set restock dated for Mon. Tinselle Emerald still in stock (store check 9:50pm ET) but card expired (rule 9). |
| Match inbox (e) | ⚠️ 37 old open | 7 marked DONE tonight with proof; priority 4. |
| Launch + partner watch | ✅ Done | Launch watch 6:10pm (LBB Electric ZigZag + Christmas Lights, Vibrant Vortex relist; Splash Kitschmas recorded); partner watch 1:45pm (House of Hearts Juliette mat, CMC Cabana travel preorder) + 6:40pm (nothing new); restock watchlist all still sold out. |
| FYM + partner feedback | ✅ Done | 0 partner feedback (2:20pm run). |
| FYM releases | ✅ Done | 1.12 live ~5:10am (both pages); 1.13 live ~8:15pm on the artifact + /find-your-match, preview page ~9:40pm. Swipe-book snapshot refreshed. |
| HQ + Ready to Ship cleanup | ⚠️ Partly | Morning 6:47am run blocked by the usage limit; 7:47pm sweep ran; this desk run: Today 19 → 5, open 34 → 25. RTS NOW 0 open. |

## Never-ending projects
- **Find Your Mat-ch™ app** (artifact 6epA9HuEdT32zUp79Qv3kd; public Version 1.13 = v113: artifact v111 + /find-your-match + /find-your-mat-ch-preview (page-block @62196501 → app @3c0b8ceb, both verified live Nov 1 ~9:40pm)): gate + independent QA before every publish (QA loads the WEBSITE copy as live: 0 broken images, gate [115]); artifact AND website copy AND README 0a pin in the same step; +0.1 version label (docs/FYM-VERSIONS.md); her feedback the same day with a gate check; when a publish/paste fails, MESSAGE HER right away. Artifact file budget: run builder/fym_artifact_fit.py and publish ONCE. Every nav/header change: screenshot live at 1280, 1440 and 390 with the phone menu OPEN. New partner catalog in FYM within 24h of its inbox line (gate [114]). Refresh config/fym-mats-snapshot.json after every publish.
- **Match inbox** (docs/MATCH-INBOX.md): any chat writes match/catalog misses there the same turn; Matches & Catalog marks DONE when shipped.
- **Google / MAHJMATCH in AI answers (her #1)**: AI Overview + AI Mode per partner, code report (Mon/Wed/Fri), daily morning report, indexing (brand pages first), sitemap health, weekly verified dates + hub date, weekly codes post (FB GROUP only typed out; IG/FB Page = logos graphic + short caption), alarm on any lost citation.
- **Albums**: order (her Oct 28 3:31pm): MFM Style of Your Life → Bam Bird Deco trio (Indigo first) → Sunday Blues → Sunday Nature Walk → Middle & Main Peach and Pine, Mac + Miller; Mahjong Row fall + OMM green set jump the line; a known restock goes FIRST. Doc 86b (colour card FIRST), book_gate.py, PICKING-RULES.md, NEW-ALBUM-CHECKLIST.md.
- **Holiday (Merry Mahjong; launch leaning Tue/Wed Nov 3-4 with Table view, her Nov 1 6:15pm)**: docs/MERRY-MAHJONG-BRIEF.md + docs/plans/holiday-calendar-nov-dec.md; promote FIND YOUR MAT-CH, not albums (her Oct 30); any FYM social shows the tool working; storyboard before render; song shortlist on every reel.
- **New products**: hq/newproducts → gallery + FYM colour-tagged → weekly roundup. Never albums. New-mat social = "Match up <mat> in Find Your Mat-ch", never ahead of the brand.
- **Social** (docs/SOCIAL-SYSTEM.md, ~2 hrs/week of her time): every approved post in Planoly at its time; FB Page target on every IG group; every slide to stories; brand tags + collabs; restocks/launches SAME DAY or never; ≥4 IG posts in every next-7-days window.
- **Facebook group**: community, never ads; weekly codes post (doc 94); weekly Claude Doc of planned posts.
- **Partner share graphics**: one per brand + our MAHJMATCH version (38 logos as of Noli June).
- **Pinterest**: queue within the pace rule; evergreen pins of our own images.
- **Affiliates + money**: sales checks 2:04pm + 12:04am, reconcile every referral email (both inboxes), refunds on the refund date, spike AND drop checks; onboarding new partners (page, hub, logos, FYM within 24h, indexing, IG follow/favorite); affiliate applications (kit doc 00h).
- **Mat Gallery + colour system**: sort rule, holiday rule, partner-only gate (plus her Oct 31 non-partner picks), shop-by-colour partners first (Oct 31); gallery row for every visible FYM mat (gate [90]).
- **ShopMy + Amazon storefronts**: square-safe covers, aerial mat photos, HQ ShopMy tab intake, weekly ShopMy mats check (Tue).
- **HQ hygiene**: Today ≤5, answered = gone, event passed = gone, timestamps on every card, inline previews; ANSWERS.md before asking anything; no answer is not a no.

## Log of this rewrite (Sun Nov 1 night)
- **Done today:** FYM 1.11 accounts (1am), 1.12 In stock only + Sold out badges + inbox sweep (5:10am), 1.13 Let's Be Besties catalog + per-brand cap + Pearl racks + Dapper explainer link (8:15pm); Brownstone Bloom album LIVE; privacy policy + FAQ page live, footer links; thin-album hearts (41), holiday anchors (37 albums), site search header, holiday stat strip, /christmas-mahjong-mats sold-out/retired labels; Planoly Content Marketplace add-on removed; Table view storyboard → working sample (v2-v4) → full-flow preview v14 (QA passed); size-check photo calibration; 4 holiday reel pieces + slow review copies; face-to-camera + AMA drafts; HQ video links → jsDelivr; LBB Tropicana render to Dropbox; 3 watch runs; partial Google report.
- **Found mid-way and given a home:** preview page still 1.12 → pasted by another session ~9:40pm (verified); Table view tablet fix held → priority 2; 9 pages not re-indexed (quota, then no browser) → priority 1 + HQ Today; Planoly 0 IG posts → priority 3; Nov 2 site check never pushed (proxy 403) → priority 5b; Tinselle card expired (rule 9) → archived, frames banked; HQ cleanup + Pinterest autopin blocked by usage limit → logged, autopin Wed; her cut-off 5:47pm message → ask once; 4 holiday reel cards + 2 amounts cards + 2 Google cards + duplicate late-picks card merged on HQ.
- HQ smoke test at 390px not run tonight (data-only change, no page HTML changed).

See CLAUDE.md.
