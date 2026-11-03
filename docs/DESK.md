# The Desk
Rewritten nightly by the end-of-day desk cleanup (9:23pm ET). The morning HQ cleanup (6:47am ET) reads it. Rules: CLAUDE.md ("THE DESK"), docs/CHATS.md (which chat owns what). During the day, when an agent stops, Chrome drops or a QA stalls, add the item here right away with its next step.

**Last rewrite:** Mon Nov 2, 2026, ~9:45pm ET (desk cleanup run, cloud, no computer linked). Covers the 43 commits of Nov 2 ET (308a264 … 7fbf5c7), docs/ANSWERS.md (Nov 2 lines), docs/MATCH-INBOX.md, Planoly (IG workspace 019fc27c… scheduled + drafts; IG account posts), HQ needs (23 open → 17) / hq/albums / hq/now / hq/priorities / hq/social / hq/indexing / log (22 entries today), config/release-calendar.json, content_lint (repo + Planoly IG export), curl checks (Amanda Toppe page + hub).

**Owners (three chats, Oct 22):** Main (Opus) = social/Planoly, site pages, email, HQ/DESK, decisions, Google + SEO. Matches & Catalog (Opus) = Find Your Mat-ch, albums, gallery, catalog, search index. Ops (Sonnet) = the ONLY Chrome driver: Squarespace pastes, uploads, IG follows/checks.

**Repo note:** checkout on `partner-catalogs-sqsp` (~4.7 GB with assets). A plain fetch hangs. Working recipe: `git fetch --depth=50 origin +refs/heads/partner-catalogs-sqsp:refs/remotes/origin/partner-catalogs-sqsp` (took ~1 min tonight), or blobless + sparse without `/assets/` (keep `/assets/**/*caption*.txt`, `/assets/**/captions/*`, `/assets/reels/s2/captions.json` so content_lint runs). Never `git ls-tree -l` on a blobless clone.

**PARTNER SEND GATE (Oct 27 3:08am, standing):** before scheduling ANY partner email or graphics drop, run `python3 scripts/partner_send_check.py`; it must exit 0.

- **Main: (partner watch Nov 3 9:45am ET) Noli June FA LA LADIES is LIVE** (6am CT; 4 mats $215 all in stock, nolijune.com/collections/falaladies; partner, MAHJMATCH 10% off $100+). No restock frames built: the 4 mats are not in FYM yet and have no swipe-book matches (no book in config/swipe-books.json), so a "Mock up with her matches" frame can't be real. Order: Matches & Catalog adds the 4 mats to FYM + gallery today (item 4a) → swipe book (check config/swipe-books.json, book_gate) → then story frames for her review. Noli has no IG post of the drop yet (latest Nov 1): reshare their launch post/story when it appears. HQ needs/launch-noli-june-falaladies.
- **Main/Ops/Matches (Nov 3): launch + partner watch scheduled tasks must check the storefront page text for "wholesale customers only" before calling a product live (OMM Poppins: JSON says available, page says wholesale only). Add to their prompts at next edit.**
- **HQ PIN (Nov 1): needs/supabase-settings-nov01 stays at the very top of HQ (order -100) until she finishes it. Nothing above it.** Now down to email templates + Resend (Site URL + redirects done Nov 2 10:10am).

## Tomorrow's top priorities (Tue Nov 3), in order
Standing order: RESTOCK FIRST (rule c), then Google #1 (Tiffany Oct 29 11:03pm), then the newest ANSWERS (Table view ASAP; holiday intro reel was to post Nov 2; codes post format), then DESK 'Never-ending'. **Restock check (c): no album-set restock is dated for Tue Nov 3.** Tue has TdT House Tigers 4pm CT and Miss Classic travel 10am CT (neither is an album set: record + FYM stock only). Tinselle Emerald (album set) still in stock since Oct 31; its card expired (rule 9). Next dated album-set restock: Virora Lilacée Nov 10 (not an album set; codes post), Bam Bird Deco Indigo mid/late Nov (album #2), Sunday Blues ~Nov 23-30 (album #3). The order is clear, so no "Set tomorrow's order" card.
- **Fri Nov 6 11am ET: Mahjong Row & Co. 2 new tile sets drop (Moody Tortoise + 1).** Matches & Catalog: FYM + gallery same day; Main: reshare + code, Dropbox renders, next codes post. (IG Nov 3 ~10am; release-calendar mrc-drop-nov6)

1. **Google (Main + Ops + tasks).** (a) **OVERDUE, Ops/Main with Chrome, first thing:** the live site still says **Amanda Toppe 20%** (it is 10%, Tiffany Nov 2 ~9am). Curl tonight: /amanda-toppe-discount-code 13× "20%" (title line, verified line, FAQ JSON-LD); hub /mahjong-discount-codes at-a-glance "20% at Amanda Toppe", ItemList "Amanda Toppe: 20% off", FAQ. Fix all spots + repo config/hub-at-a-glance.html + assets/search/search-index.json + any FYM brand note, curl-verify, then request indexing for both pages. (Britt Mills = 15% everywhere on the hub tonight; check its brand page.) (b) **Indexing after ~9:05am ET** (rolling quota; Mon used 11): 27 changed pages waiting, order in hq/indexing tier0Queue: My Fair, Bam Bird, Bespoke, Yellow Mountain, Britt Mills, Amahj, then Amanda Toppe (after a), then Wren (after c). Needs her computer on (HQ Today alert-indexing-2026-11-01). (c) Code report finds: **Wren Mats page still "Verified: October 9"** and **OMM page has a second "verified October 21" line**: fix both (verified-line refresh is standing authority). (d) **AI-answer gaps** (Nov 2 8pm): Bam Bird, My Fair, Peace Love, Oh My Mahjong, Miss Mahjong do not name MAHJMATCH: tier-0 indexing + Google AI feedback on the next runs. (e) Morning report daily; code report due Wed.
2. **Table view → FYM 1.14 live (Matches & Catalog).** Preview artifact 5QjNXjw15MuZTqzDT1ptbp **v22** (round 8, real wood grain on 10 wood racks, commit e2b8c5d; site copy fym-site-preview @e7a6d0a, jsDelivr warm, NOT pinned). No independent QA PASS is recorded for round 8: run the QA re-check first, then on her OK publish to BOTH places (live artifact 6epA9HuEdT32zUp79Qv3kd + /find-your-match + /find-your-mat-ch-preview + README 0a pin) → fym_snapshot.py. Held commit 43b9ca7 (tablet sheet) folds in. HQ Today needs/tableview-storyboard-nov01.
3. **Instagram is silent since Oct 27; Planoly next 7 days = 0 IG posts (Main).** Audit (d): Nov 3-9 has nothing scheduled (01a16052-2828, the Oct 21 Papaya reminder, is still "scheduled": clear its date, never delete). Ready and waiting on her: holiday intro reel v2 (she posts via Edits with the song; HQ This week top), codes post v3 (FB group; HQ Today), **New this week carousel** Planoly 01a19e04 (IG + FB Page targets ✅, brand names on FB ✅, Tag people ✅ 4 verified handles, lint PASS) **but no 7-frame story version: build it with the schedule on her yes**; this week's posts (HQ Today needs/social-week-2026-11-02). Default kit if no yes by Wed: album-of-the-week kit from the Friday social prep task. Every post on her yes: IG + FB Page target, every slide as story, Tag people from config/social/ig-handles.json, `content_lint.py --planoly <export> --only-ig` must pass.
4. **Catalog (Matches & Catalog).** (a) **Same day Tue:** Noli June FA LA LADIES 4 mats → FYM + gallery the day they list (6am CT). (b) **Broken FYM links:** Let's Be Besties renamed listings (MATCH-INBOX Nov 1 6:10pm, Nov 2 9:35am + 5:57pm lines: old URLs 404). (c) New: Britt Mills Isla Leatherette (2nd shop link), Bespoke Garden Glow Sunshine Glow (tile set, drops Wed Nov 4 9am CT; needs TNT rec + colour card before any book), LBB Electric ZigZag + Christmas Lights, TdT Domino Blonde w/ rules; the 39 photo-OK mats from the Nov 2 weekly scan (HQ card archived as Claude's job). (d) MATCH-INBOX older than 2 days (rule e): still ~37 real open (66 dated lines without DONE; many say FIXED inline but were never marked): mark DONE with proof, then Sunday Gingham/Rattan, Britt Mills leatherettes, late holiday mats (waits on her Send), gate [90] 69 mats with no gallery row, gate [89] 38 angled photos, rack length by tile size + tortoise order, TNT recs not in FYM, FYM default tile-set order.
5. **Overdue + mid-way Claude jobs.** (a) Main: **Nov 2 monthly site check never reached the repo** (proxy 403 Nov 1-2; HQ log 2026-11-02-site-maintenance re-logged 8:45pm, still no site-maint folder or audit file in git). Re-run attended or rebuild from the HQ log detail; Emerald + Pearlescent Retired labels go ahead Wed Nov 4 on the default (needs/site-maint-2026-11). (b) OPS: Dropbox copies of flat renders → /Mahj Matchmaker Albums/New releases/: Bespoke Sunshine Glow, Britt Mills Isla Leatherette, LBB Electric ZigZag + Christmas Lights (Chrome method: ANSWERS Nov 1 12:50am). (c) OPS: Tiles & Tablescapes search for Bespoke Garden Glow Sunshine Glow. (d) Amazon 'A Reindeer Holiday Table' board (approved Oct 30) when Amazon is signed in.

## Handoffs (do first)
- **OPS (Nov 3 launch watch): copy assets/launches/omm-lotus-cove-mat-in-tube/ and assets/launches/omm-juniper-mahjong-tiles/ to Dropbox /Mahj Matchmaker Albums/New releases/Oh My Mahjong/ today** (flat renders get replaced by photoshoot images later).
- **OPS: search Tiles & Tablescapes for Oh My Mahjong Juniper** (new OMM tile set Nov 3; its swipe book waits on a TNT rec + colour card per the book gate; HQ Albums: needs-colourcard).
- **Matches & Catalog: Juniper colour card** (scripts/colorcards) so the Juniper swipe book can be built (OMM = top priority).
- **OPS / Main: Amanda Toppe 10% live fix** (priority 1a). Overdue since Nov 2 9am.
- **OPS: Dropbox new-release copies** (priority 5b) + **TNT search for Sunshine Glow** (5c).
- **Main: re-run / rebuild the unpushed Nov 2 site check** (priority 5a).
- **Main: Wren Mats + OMM verified lines** (priority 1c).
- **Main: new-arrivals story version** in Planoly on her yes (priority 3).
- **Matches & Catalog: round 8 QA re-check of 1.14** (priority 2); FYM 1.12 follow-ups still open: nightly stock check publish path; rack cut-out review for the 12 hidden racks (builder/fym_fix_nov01 README step 3b); Mat Gallery rows (gallery_rows112.py); two-color coordination ranking bonus.
- **Main: Planoly cleanup** (clear dates, never delete): Raven 01a16477-0b08 + -092f, the past-day drafts in "In progress", and the stale scheduled 01a16052-2828.
- **Main: CONTENT BANK on her yes** (HQ week of Nov 9-15; assets/social/week-2026-11-09/README.md; 8 FYM pins queued pending in config/pinterest/queue.json).
- **Main: duplicate catch-up tasks** trig_019StaM8LkmrxGKtK7xhXang + trig_013ZpyRxFivSKPoYTgSvVBU6: pausing one is her call (HQ rules-audit-2026-10-30).
- **Main: sales-check prompt fix** (ALL secomapp + goaffpro + backinstock emails, refunds on the refund date, tiffanybrie@ at mail.google.com/mail/u/1 per her Oct 31 3pm rule). Still not applied. Also: the 2:04pm sales check said "DESK.md not found in this workspace": its prompt needs the repo clone step.
- **Main: "close leftover finished Claude tab groups at start"** in every Chrome task TAB RULE (Oct 30 10:10am). Not done.
- **Main: mat-edit-alert build step** in launch watch trig_01S2VsjwznnHev1uUbYmEwJq (Oct 30 9:05am; docs/MAT-EDIT-ALERT.md). Not done.
- **Pinterest autopin** next run Wed Nov 4 (blocked by usage limit Sun); Main re-checks Wed.
- **OPS (standing): HQ ShopMy tab inbox** (db `shopmy`, status new) at the start of every Ops reply. The 2 stray ShopMy links are HER click (HQ needs/shopmy-delete-2-links).
- **Partner feedback watch** trig_01RKw9eUwTYPo39gbYHb65gh runs daily through Nov 10 (0 new Nov 2).
- **Matches & Catalog: ShopMy Etsy mats staged (Nov 3 weekly check)**: include `builder/fym_fix_nov03/etsy_shopmy_nov03.py` (spec config/fym-etsy-shopmy-nov03.json: Luna EK Studio 28, BJ&J Grace x3, Strawberry Thief, Pink Hummingbird; 1 Questionable hidden) in the next FYM build after 1.14, then full gate + QA. Check 4 Luna colours by eye (docs/SHOPMY-MAT-AUDIT-nov03.md). Not published.

## In progress
| Item | Owner | Next step | Target |
|---|---|---|---|
| Google: Amanda Toppe 10% fix, 27 pages to re-send, Wren/OMM verified lines, 5 AI-answer gaps | Main + Ops + tasks | Priority 1. | Tue Nov 3 |
| Table view → FYM 1.14 | Matches & Catalog | Round 8 QA re-check → her OK → publish both places + README pin → snapshot. | Tue Nov 3 (else Wed) |
| Instagram restart (reel, codes post, new arrivals, week's posts) | Main | Her yes/post → Planoly IG + FB Page + stories. | Tue Nov 3 |
| Holiday reels redo (Nutcracker/FYM reel with Table view) | Main | After 1.14 is live; intro reel v2 goes first. | Thu Nov 5 |
| Catalog: Noli June, LBB broken links, Isla, Sunshine Glow, 39 new mats, MATCH-INBOX | Matches & Catalog | Priority 4. | Tue Nov 3 |
| Nov 2 monthly site check (unpushed) | Main → Ops | Re-run attended, then OPS pastes. | Tue Nov 3 |
| My Fair drop watch (14 → 4 orders/week) + Black Friday policy | Main | Watch; her answer on "use our link" (HQ This week). | Wed Nov 4 |
| Bam Bird + Peace Love week drops | Main | Watch; Bam Bird dashboard signed out (email-only amounts). | Wed Nov 4 |
| 1 amount (My Fair 35473474) | Tiffany / Ops | Screenshot of My Fair commission page. | This week |
| Holiday colour cards (Tinselle ×2, Dec 1994, PLM Spirit + Nutcracker) | Matches & Catalog | Not started (was due Oct 31). | Wed Nov 4 |
| My Fair Mahjong Style of Your Life (#1 album) | Matches & Catalog | Colour card + TNT, then swipe book. | Wed Nov 4 |
| Sunday Sets TNT rec leftovers | Matches & Catalog | docs/research/sunday-sets-colorcards-tnt-oct29.md. | Wed Nov 4 |
| Larkspur hearts into 27 tile albums | Matches & Catalog → Ops | Paste album by album. | Wed Nov 4 |
| Holiday album covers page update | Matches & Catalog | After 1.14 live. | Thu Nov 5 |
| December 1994 redo (her RTS notes) | Matches & Catalog | After holiday colour cards. | Fri Nov 6 |
| Bam Bird Deco trio (Indigo first) | Matches & Catalog | Colour cards ×3, then books. | Week of Nov 9 |
| Affiliate applications (6 apply-first brands) | Tiffany submits / Main | Kit doc 00h; HQ apply-kit-oct31. | This week |
| Planoly cleanup (her Oct 27 ask) | Main | DONE Nov 3: 46 old drafts archived (docs/planoly-archive/) then deleted on her 1:31pm yes; 01a16052-2828 (still 'scheduled', Oct 21) left as is. | done |
| FB group weekly Claude Doc | Main | https://claude.ai/artifact/54ovPaB6BQU78ztjUgQSbe; keep current. | Tue Nov 3 |
| Mahj Mood code check (unused codes expire after 4 months) | Main | Before the next Mahj Mood post (Playing for Keeps Fri Nov 6). | Thu Nov 5 |
| Tortoise rack piece (her Oct 28) | Main | Scope + storyboard; gift-guide tie-in. | Wed Nov 4 |
| UpPromote accounts → mahjmatchmaker@ | Main | Her logins where the owner must move it. | Wed Nov 4 |
| Discount links not converted (Britt Mills, Mahjong Register, YMI, RMS, Hip Hip, Wren/Soirée/Amanda Toppe) | Main | builder/fym_fix_oct21/discount_check_oct21.json. | Wed Nov 4 |
| Amazon mats into gallery + FYM | Ops → Matches & Catalog | Her picks only. | Wed Nov 4 |
| ShopMy holiday leftovers | Main → Ops | ShopMy (not MAHJMATCH) for Charleston Mahjong Club + Bamlet's in holiday posts. | Wed Nov 4 |
| Search logging | Main | Needs her Apps Script URL (site/livepatch/search README "Tracking"). | Ask once |
| Fait à Main code | Main | MAHJMATCH still not applicable at cart. | Watch |

## Waiting on Tiffany (only things she can answer now)
**On HQ Today, in this order (5):**
1. **Supabase: finish the email templates + Resend** (pinned -100; Site URL + redirects done).
2. **Google: leave the computer on with the Claude app open Tuesday morning** (27 pages to re-send from ~9am).
3. **Facebook group codes post v3: yes to post** (text + first comment on the card).
4. **Try Find Your Mat-ch 1.14 (Table view) on the preview, reply OK to go live.**
5. **This week's posts: yes all, or yes/no per day** (Planoly is empty).

**On HQ This week:** holiday intro reel v2: post it with the song in Edits (top); My Fair Black Friday: say "use our link" or not; 1 amount (My Fair screenshot); late holiday picks: tap Send final answers; 2 quick FYM checks + Holy Mahj from her Canva; Work With v3 live yes; 5 quick calls (defaults go ahead Wed Nov 4); new-arrivals carousel yes; Sunday Sets round 2 (4 sets); affiliate apply kit; 2 stray ShopMy links.

**Asked in chat, not on HQ (the owning chat asks once, next time she's there):**
- Main: Malachite how-to reel v2 OK + day; FB group B&B racks wording; subscriber "It's here!" email send or skip; ShopMy 2-hourly pickup yes; Santa Baby's 12 yes; Apps Script URL for search logging; her Nov 1 5:47pm message cut off at "that has nothing to do with the number of" (ask her to finish the thought).
- Matches & Catalog: Lagoon + Mulberry splits; Bam Bird Classic Tortoise match pick; Sunday Rattan: is the 'new' one the Blue Rattan (her Nov 1 4:50am question: answer it; Blue Rattan is now listed); Fruit Stand rack-edge (default a).

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
- **Season 2 tile-dating episode reels (Ep 1-13 + trailer): PARKED, not abandoned** (Tiffany Nov 3: "down the road"; focus now = people using Find Your Mat-ch). Renders assets/reels/s2/; captions + Planoly records docs/planoly-archive/2026-11-03-deleted-drafts.json (README there).
- **Let's Mahj On new tile sets** (Wild, Sweet, Golf, Refined, Merry, Stir Things Up), sneak peek Nov 2, coming mid-Nov: new products; ONE swipe book only if she says (partner watch Nov 2; HQ card archived as info-only).
- **OMM 2027 International Mahjong Card** preorder live Nov 2 ($12, ships Jan 2; TEACHMAHJ + code work): record only; possible teacher/FB group mention (mentor check, Nov 2).
- **Peace Love Mahjong Black Friday Nov 16**, **Mahj Mood Playing for Keeps preorder Fri Nov 6 10am CT**, **Virora Lilacée restock Nov 10** (release calendar Nov 2): codes post + social on the day.
- **Reels earn 0 follows two weeks running; the single 'It's a match' image is still the best post** (social measure, Nov 2): weigh image posts in next week's kit.
- **Sunday Blues restock post window ~Nov 16** (HQ card parked to Nov 16).
- IDEA (Tiffany Nov 1 11:33pm, not now): fold racks into the mat step (no step-3 jump) for Aerial/Table views — racks come in/out on the same view like the match card; only Up close needs a jump. Revisit once Table view is live and if Table/Aerial become the main view.
- **Clean up 52 legacy caption lint warnings** (still 52 Nov 2) (config/social/content_lint_baseline.json; mostly missing #MahjMatch, '(affiliate)', 2 TdT captions) (rules audit E9, Oct 30). Also 78 legacy FAILs (length 42, naming 36) in banked Season 2 captions: same kinds as yesterday, nothing new.
- **Tigre de Tartán House Tigers** return Tue Nov 3 4pm CT (record + FYM stock; no album); **Mary Benson Hydrangea** went live Nov 2, tiles sold out (non-partner, record only); **CMC x OTG247** bags live Nov 2 (record only); **Mahjong Moxie Moxie Tiles** Fri Nov 6 (non-partner, record only) (watches, Nov 2).
- **Mahjong Register** Crystal Palace acrylic racks + Solid Wood racks (launch watch Oct 31): racks, FYM rack lists when Matches & Catalog has room.
- **Sunday Vegan Leather mat moved listing** (launch watch Oct 31): relink the FYM card in the next build.
- **Brands later (her Oct 31 picks):** Feltectors, Four Winds Social, Mahj House Rules, Mahjong Made Chic, Mahjong Moxie, Silk Mahjong, The Mahjong Line (teacher program only).
- **LBB Artist Collective mats** (early Nov): new products, never albums (Oct 30).
- **Bam Bird restock/brand announcement** teaser (IG Oct 30): same day or never.
- **Amanda Toppe Lila**: travel Lila listed Nov 2 (no album); full-size later = swipe book the day it lists (Oct 29).
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

## Daily operations (Mon Nov 2)
| Operation | Done today? | Notes |
|---|---|---|
| Affiliate tracking (Money tab) | ✅ Done | Sales checks 12:04am (Nov 1 final $238.79, 13 sales) + 2:04pm ($90.45, 6 sales); amounts filled from her screenshots (Ops 7:25pm), 1 left. Weekly brand trends: 103 orders vs 139 (-26%). Midnight close-out still to run. |
| Google code report | ✅ Done | 12:50pm: Overview 24/38, AI Mode 34/38, 14 feedback sent, indexing queue reordered. Next due Wed. |
| Morning Google report | ✅ Done | 8:15am: 24/38 AI answers (lost Mini Mahjer + I Love Mahj; gained TdT, Charleston, Soirée). Weekly Google & OMM report artifact EnPpqMnAc3PCgYnkRmy2aE. |
| Verified dates (weekly, Mondays) | ✅ Done | 9am: 36/36 pages + hub "verified November 2, 2026", live-checked. Misses found later: Wren Oct 9 line, OMM second Oct 21 line (priority 1c). |
| Codes post (Mondays) | ⚠️ Drafted, not posted | v3 (Partner Codes + Updates, 10 photos, Amanda Toppe 10%) waits on her yes (HQ Today). |
| Pinterest queue health | ✅ OK | Planoly Pinterest 3-4 pins/day through Nov 9 (per Sun check); autopin next Wed. |
| Indexing | ✅ Done (quota) | 11 requested (10 by verified-date run + Brownstone Bloom); My Fair hit quota. Sitemap OK (130 pages). 27 waiting. |
| Planoly next-7-days (IG + FB Page) | ❌ Not covered | 0 IG posts Nov 3-9; IG last post Oct 27. New-arrivals draft has IG + FB targets + Tag people, lint PASS (2 captions, 0 FAIL); no story version yet (priority 3). No FB target was missing on any IG group in the window. |
| New albums (last 7 days) (f) | ✅ All checks | Brownstone Bloom (live Nov 1): /mahjong-tile-matches ✅, /ivory ✅, /anders-ruff-discount-code ✅, /links ✅, Pinterest queue ✅, **indexing ✅ requested Nov 2 12:40pm**. No other album went live. |
| Repo caption lint (g) | ⚠️ Legacy only | 78 FAIL (length 42, naming 36), all banked Season 2 captions; 52 legacy WARN. Same kinds as yesterday, nothing new. |
| Restock first (c) | ✅ Checked | No album-set restock dated Tue. |
| Match inbox (e) | ⚠️ ~37 old open | Priority 4d. |
| Launch + partner watch | ✅ Done | Release calendar (7 changes); launch watch 9:35am + 5:57pm (Sunshine Glow, Isla Leatherette, LBB renames); partner watch 10:05am, 1:35pm, 6:30pm (LMO sneak peek, Moxie Nov 6, Hydrangea sold out); mentor check (OMM 2027 card). |
| FYM + partner feedback | ✅ Done | 0 new (2:19pm). |
| FYM releases | ⚠️ Preview only | 1.14 rounds 3-8 on the preview (v22); nothing published live. |
| Social measure + brand watch (Mon) | ✅ Done | +61 follows; reels 0 follows 2 weeks running; Maison Mahj favorited. |
| HQ + Ready to Ship cleanup | ✅ Done | Morning 6:47am (25 → 12), 3 sweeps, this desk run 23 → 17 open, Today 11 → 5. RTS: no new answers since Oct 30. |

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

## Log of this rewrite (Mon Nov 2 night)
- **Done today:** verified dates (36 pages + hub), 11 indexing requests, code report + morning report + weekly Google report; FYM 1.14 rounds 3-8 (rack re-cuts, corner view fills the square, peel fills, gray list, wood grain); holiday intro reel v2; codes post v1-v3; new-arrivals carousel draft (Planoly IG + FB); amounts filled; Supabase step A1 (her); release calendar + 2 launch watches + 3 partner watches + mentor check; social measure + brand watch; AI-answer gap list.
- **Found mid-way and given a home:** Amanda Toppe 20% still live → priority 1a; Wren/OMM verified-line misses → 1c; 1.14 round 8 has no QA PASS recorded → priority 2; holiday intro reel not posted + IG silent since Oct 27 → priority 3 + HQ This week top; new-arrivals has no story version → priority 3; LBB renamed listings break FYM links → 4b; Nov 2 site check still not in git → 5a; sales-check task can't find DESK.md → Handoffs; 5 info-only HQ cards archived, Sunday Blues card parked to Nov 16.
- HQ smoke test at 390px not run tonight (data-only change, no page HTML changed).

See CLAUDE.md.
