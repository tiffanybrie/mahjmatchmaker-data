# The Desk
Rewritten nightly by the end-of-day desk cleanup (9:23pm ET). The morning HQ cleanup (6:47am ET) reads it. Rules: CLAUDE.md ("THE DESK"), docs/CHATS.md (which chat owns what). During the day, when an agent stops, Chrome drops or a QA stalls, add the item here right away with its next step.

**Last rewrite:** Tue Nov 3, 2026, ~9:50pm ET (desk cleanup run, cloud, no computer linked). Covers the 92 commits of Nov 3 ET (c4ff727 … b85a962), docs/ANSWERS.md (Nov 3 lines 894-950), docs/MATCH-INBOX.md, Planoly (IG workspace 019fc27c…: 19 groups, export docs/social/planoly-exports/ig-2026-11-03-desk.json; Pinterest 019fc27b… scheduled), HQ needs (17 open → 15) / hq/albums / hq/now / hq/priorities / hq/social / hq/indexing / log (35 entries today), config/release-calendar.json, content_lint (repo + Planoly IG export), curl checks (Amanda Toppe, hub, Wren, OMM, Brownstone Bloom pages).

**Owners (three chats, Oct 22):** Main (Opus) = social/Planoly, site pages, email, HQ/DESK, decisions, Google + SEO. Matches & Catalog (Opus) = Find Your Mat-ch, albums, gallery, catalog, search index. Ops (Sonnet) = the ONLY Chrome driver: Squarespace pastes, uploads, IG follows/checks.

**Repo note:** checkout on `partner-catalogs-sqsp` (~4.7 GB with assets). A plain fetch hangs (tonight a plain `git fetch` timed out at 2 min). Working recipe: `git fetch --depth=200 origin partner-catalogs-sqsp:refs/remotes/origin/partner-catalogs-sqsp` then `git checkout -B partner-catalogs-sqsp origin/partner-catalogs-sqsp` (~1 min), or blobless + sparse without `/assets/` (keep `/assets/**/*caption*.txt`, `/assets/**/captions/*`, `/assets/reels/s2/captions.json` so content_lint runs). Never `git ls-tree -l` on a blobless clone.

**PARTNER SEND GATE (Oct 27 3:08am, standing):** before scheduling ANY partner email or graphics drop, run `python3 scripts/partner_send_check.py`; it must exit 0.

**Standing from today (Nov 3, in CLAUDE.md / ANSWERS):** social review happens IN PLANOLY (drafts on their day; HQ = one short line per post; "send me X" → file + full steps in chat) · launch/partner checks read the rendered page for "wholesale customers only" (OMM Poppins) and anything wholesale-only/unannounced is confidential · once a partner publicly announces a product, pull it into FYM as soon as a product page exists · read EVERY carousel slide before drafting from a brand post · reels: FYM-REEL-RULES 23-41 (v5 holiday intro is the standard), IG safe zones (top 250 / bottom 420 / right buttons) on every frame · racks in mock-ups: at most one painted colour + wood/pearl/acrylic, never orange for Christmas · logo rows next to "use code MAHJMATCH" = code partners only · every launch/announcement gets its full marketing set by default (main post + FYM tie-in post + covers) · every new album sends the new-albums email (NEW-ALBUM-CHECKLIST §4).

## Tomorrow's top priorities (Wed Nov 4), in order
Standing order: RESTOCK FIRST (rule c), then Google #1 (Tiffany Oct 29 11:03pm), then the newest ANSWERS (holiday albums + late picks, Planoly week, FYM 1.15 catalog adds), then DESK 'Never-ending'. **Restock check (c): no album-set restock is dated for Wed Nov 4** (Wed: Bespoke Sunshine Glow launch 9am CT, PLM mini holiday 8am CT, Miss Mahjong Mini Miss Classic ETA; none is an album set). Next dated: Mahjong Row 2 tile sets + Bam Bird MCM Olive restock + Mahj Mood Playing for Keeps preorder Fri Nov 6 (none an album set yet); Virora Lilacée Nov 10; OMM Juniper + Lotus Cove Wed Nov 11 10am CT. The order is clear, so no "Set tomorrow's order" card.

1. **Google (Main + Ops, Chrome).** (a) **OVERDUE 2 days, first thing, Ops with Chrome:** live site STILL says **Amanda Toppe 20%** (curl 9:45pm tonight: /amanda-toppe-discount-code 15× "20%"; hub /mahjong-discount-codes "Amanda Toppe (20% off with MAHJMATCH)" + ItemList "Amanda Toppe: 20% off" + "20% at … Amanda Toppe"). It is 10% (Tiffany Nov 2 ~9am). Fix every spot + repo config/hub-at-a-glance.html + assets/search/search-index.json + FYM brand note, curl-verify, request indexing for both pages. (b) **Wren Mats page still "Verified: October 9, 2026"** (curl tonight): set to the current verified date (standing authority). OMM page reads "verified Nov 2" everywhere now (its 20% lines are the OMM 20%-through-Dec-31 offer: leave). (c) **Code report is due Wed** (Mon/Wed/Fri) + morning report (28/38 AI answers Tue; OMM still not named). (d) Indexing: 9 sent Tue; continue hq/indexing tier0Queue after ~9am (Amanda Toppe + Wren after a/b).
2. **Holiday albums: late picks in (DONE) → announce (Main).** DONE Nov 4 ~4pm (Main fork): 45 cards LIVE (33 late picks + her 12 Santa Baby's Cocktail Hour yeses) on 20 album pages + /holiday-mahjong-matches (Dear Santa, Nutcracker Ballet, Holly Jolly Pink/Red, Tinselle Emerald, Rackin' Rudolph, Hummingbird); new holiday sections on Heritage, Pippa, Sunday Tile Set; curl-verified 21/21 pages; cards assets/cards/holiday-late-nov04 @14968bdd. NEXT Main: holiday albums group post + FYM holiday group post + new-albums email on her OK.
3. **Planoly: 0 IG posts scheduled in the next 7 days (rule d) (Main).** 8 IG drafts sit on Wed-Sun waiting for her look (social-week card on HQ Today): Wed Polo Club reel (reminder) + New this week carousel (undated: she drags to Wed) + its 7-frame story; Thu Dear Santa x Anders Ruff carousel (9) + story; Fri Rackin' Rudolph reel (reminder); Sat It's a mat-ch! Holly Jolly x Holiday Love; Sun It's a mat-ch! Rackin' Rudolph x Candy Cane Lane. **Fix before she schedules:** content_lint --planoly FAILs on all 8 story drafts (no MAHJMATCH typed + no #MahjMatch in the story captions: 01a1a2b6-7c1e/-73c0/-7707/-7a67, IG + FB each) — add the code line + #MahjMatch or confirm story captions are exempt in the lint; the Polo + Rudolph 7-frame story reminder groups (01a16477-0078, 01a16477-03c8) have no FB Page target (their reels' FB versions are separate groups 01a1a2b7-3d0e / -3eb3, fine). Default kit if she gives no yes by Thu: album-of-the-week kit from the Friday social prep task.
4. **FYM 1.15 catalog build (Matches & Catalog).** In one build after 1.14 (gate + independent QA, both places + README pin + snapshot): OMM Juniper tiles + Lotus Cove mat (her GO Nov 3 2:05/2:08pm), Noli June FA LA LADIES ×4 (her "Yes put in FYM"), LBB Electric ZigZag + Christmas Lights + Camellia Kaleidoscope (remove the TEMP ignores in config/partner-mat-sweep-ignore.json), 8 new LBB Nov 3 mats (log 23:15-23:22), Bespoke Sunshine Glow tiles (drop Wed 10am ET) + It's a Vibe Glitter Glow Green, 33 ShopMy Etsy mats (builder/fym_fix_nov03/etsy_shopmy_nov03.py; check 4 Luna colours by eye), Britt Mills Isla, TdT House Tigers Oyster stock. Mahjong Row Moody Tortoise + Brunette Burl the day product pages exist (Fri Nov 6 11am ET at the latest).
5. **Match inbox + overdue Claude jobs.** (a) **MATCH-INBOX (rule e), owner Matches & Catalog:** ~76 dated lines older than Nov 2 have no DONE (many say FIXED inline): mark DONE with proof, then the real open ones (LBB renamed-listing 404s, Sunday Gingham/Rattan, Britt Mills leatherettes, gate [90] 69 mats with no gallery row, gate [89] angled photos, rack length by tile size, TNT recs not in FYM, FYM default tile-set order). (b) **TNT scan Nov 3: 8 new mat recs not in config/tnt-recs.json** (Hummingbird 5, Nature Walk 1, Plum Panda 2; Project doc 81b) → M&C adds them. (c) Main: **Nov 2 monthly site check still not in git** (no site-maint folder; HQ log 2026-11-02-site-maintenance has the findings: 36 dead links, 73 cards newly Retired) → rebuild from the log detail; the 7 quick calls' defaults (needs/site-maint-2026-11-b) go ahead Wed Nov 4 unless she answers. (d) Ops: FB Page intro still says "Find Your Match (coming 10.27)" (seen Nov 3 4:33pm) → update to the live line.

## Handoffs (do first)
- **OPS / Main: Amanda Toppe 10% live fix + Wren verified line** (priority 1a/1b). Overdue since Nov 2 9am.
- ~~Matches & Catalog: late holiday picks → holiday albums~~ DONE Nov 4 ~4pm (Main fork): 45 cards LIVE (33 late picks + her 12 Santa Baby's Cocktail Hour yeses) on 20 album pages + /holiday-mahjong-matches (Dear Santa, Nutcracker Ballet, Holly Jolly Pink/Red, Tinselle Emerald, Rackin' Rudolph, Hummingbird); new holiday sections on Heritage, Pippa, Sunday Tile Set; curl-verified 21/21 pages; cards assets/cards/holiday-late-nov04 @14968bdd. NEXT Main: holiday albums group post + FYM holiday group post + new-albums email on her OK.
- **Main: launch reel redo** (assets/social/fym-launch/redo-nov03/launch-reel-redo.mp4, 58.0s, Dancing On My Own) was sent in chat ~5:35pm Nov 3 for her OK: no answer yet. On her OK it replaces the pinned launch reel (she swaps it in IG; Claude does the FB Page).
- **Main: Mahjong Row Nov 6 FB group post** (docs/social/mahjong-row-drop-nov6.post.txt + .comment.txt, both sets, brown hearts, no ⏰, no @everyone): waits on her better photo + OK. On Fri: reshare + code, FYM same day, next codes post.
- **Main: Planoly story-caption lint fixes** (priority 3) before any of this week's drafts is scheduled.
- **OPS (Nov 3 launch watch): copy flat renders to Dropbox /Mahj Matchmaker Albums/New releases/**: Oh My Mahjong/ ← assets/launches/omm-lotus-cove-mat-in-tube/, assets/launches/omm-juniper-mahjong-tiles/ · Let's Be Besties/ ← the 8 assets/launches/letsbebesties-*-mahjong-mat/ folders of Nov 3 (tiger stripes, spinning dreidel, champange bubbles, mid century floral, pink pizzazz, gatsby glow, mad for plaid, disco dot simple middle) · Bespoke Mahjong/ ← assets/launches/bespoke-coming-this-november-mahjong-its-a-vibe-glitter-glow-green/ · plus the Nov 2 leftovers: Bespoke Sunshine Glow, Britt Mills Isla Leatherette, LBB Electric ZigZag + Christmas Lights (Chrome method: ANSWERS Nov 1 12:50am).
- **OPS: Tiles & Tablescapes searches** for OMM Juniper, Bespoke Sunshine Glow, Bespoke It's a Vibe Glitter Glow Green (book gate needs a TNT rec + colour card).
- **Matches & Catalog: Juniper colour card** (scripts/colorcards) so the Juniper swipe book can be built before Nov 11 (OMM = top priority). Lotus Cove swipe book (L8teRCj5w9ncskZYkwNEoZ) is built and waits on her swipe.
- **OPS (HQ sweep 7:47pm): check minimahjer.com for a store-wide/Black Friday code bigger than MAHJMATCH** (curl 429). B&B + Miss Mahjong homepages show no sale code.
- **Matches & Catalog: brand-lock FYM sample for Bird & Bamboo (Emily)**, hosted embed only (her 3:56-3:59pm); docs/brand-lock/STATUS.md. Shuffle idea for 1.15.
- **Matches & Catalog: FYM 1.12 follow-ups still open:** nightly stock check publish path; rack cut-out review for the 12 hidden racks (builder/fym_fix_nov01 README step 3b); Mat Gallery rows (gallery_rows112.py); two-colour coordination ranking bonus.
- **Main/Ops/Matches: launch + partner watch prompts must check the storefront page text for "wholesale customers only"** before calling a product live (her Nov 3 8:47am rule). Add at next prompt edit.
- **Main: CONTENT BANK on her yes** (HQ week of Nov 9-15; assets/social/week-2026-11-09/README.md; 8 FYM pins queued pending in config/pinterest/queue.json).
- **Main: duplicate catch-up tasks** trig_019StaM8LkmrxGKtK7xhXang + trig_013ZpyRxFivSKPoYTgSvVBU6: pausing one is her call (HQ rules-audit-2026-10-30).
- **Main: sales-check prompt fix** (ALL secomapp + goaffpro + backinstock emails, refunds on the refund date, tiffanybrie@ at mail.google.com/mail/u/1 per her Oct 31 3pm rule; repo clone step so it finds DESK.md). Not applied.
- **Main: "close leftover finished Claude tab groups at start"** in every Chrome task TAB RULE (Oct 30 10:10am). Not done.
- **Main: mat-edit-alert build step** in launch watch trig_01S2VsjwznnHev1uUbYmEwJq (Oct 30 9:05am; docs/MAT-EDIT-ALERT.md). Not done.
- **Main: Mahj Mood code check** (unused codes expire after 4 months) before the Playing for Keeps preorder Fri Nov 6 10am CT.
- **Pinterest autopin** runs Wed Nov 4; queue is healthy (3-4 pins/day through Nov 29).
- **OPS (standing): HQ ShopMy tab inbox** (db `shopmy`, status new) at the start of every Ops reply. The 2 stray ShopMy links are HER click (HQ needs/shopmy-delete-2-links).
- **Partner feedback watch** trig_01RKw9eUwTYPo39gbYHb65gh runs daily through Nov 10 (0 new Nov 3).

## In progress
| Item | Owner | Next step | Target |
|---|---|---|---|
| Google: Amanda Toppe 10% fix, Wren verified line, code report, indexing queue, AI-answer gaps (OMM, Bam Bird, My Fair, Peace Love) | Main + Ops + tasks | Priority 1. | Wed Nov 4 |
| Hummingbird holiday section (hidden) | Matches & Catalog | /holiday-mahjong-matches #hummingbird stays display:none until the Hummingbird / Sunday Sets album goes live; it now holds 3 cards incl. Hummingbird + Home for the Holidays (Nov 4). When that album launches: un-hide the section and add a holiday section on the album page (NEW-ALBUM-CHECKLIST). | With Sunday Sets launch |
| FYM m-lists: late holiday picks + Santa Baby yeses | Matches & Catalog | Add Tiffany's real picks to FYM m-lists in the next build: config/late-holiday-picks-nov03.json (33) + config/swipe-yeses/holiday-oct21.json 'santababy' (12). Santa Baby's Cocktail Hour (Splash of Color) is NOT in FYM at all: add it (flat crop assets/mats/holiday-late-nov04/splash-santa-baby-s-cocktail-hour-flat.png, holiday). Manifest assets/cards/holiday-late-nov04/manifest.json. | Thu Nov 5 |
| Late holiday picks (33) + Santa Baby yeses (12) → holiday albums | Main (fork) | DONE Nov 4: 45 cards live on 21 pages (curl-verified). | DONE |
| Holiday albums group post + FYM holiday group post + new-albums email | Main | After the albums update; her OK on each. | Thu Nov 5 |
| This week's IG posts (8 Planoly drafts Wed-Sun) | Main | Story-caption lint fixes; she reviews in Planoly; schedule on her yes. | Wed Nov 4 |
| Launch reel redo (58s, Dancing On My Own) | Main | Her OK in chat → she swaps the pinned reel; Claude does the FB Page. | Wed Nov 4 |
| FYM 1.15 catalog build (Juniper, Lotus Cove, Noli ×4, LBB ×11, Bespoke ×2, 33 Etsy, Isla) | Matches & Catalog | One build, gate + independent QA, both places + pin + snapshot. | Thu Nov 5 |
| Mahjong Row Nov 6 drop (2 tile sets) | Main + Matches & Catalog | Group post on her photo + OK; FYM the day pages exist. | Fri Nov 6 |
| Juniper colour card + swipe book; Lotus Cove swipe | Matches & Catalog / Tiffany | Colour card, TNT, book gate; she swipes Lotus Cove. | Mon Nov 9 (launch Nov 11) |
| Bespoke Sunshine Glow launch | Tiffany (reshare) / Matches & Catalog | Drops Wed 10am ET: she reshares Bespoke's post; FYM add in 1.15. | Wed Nov 4 |
| Nov 2 monthly site check (unpushed) + 7 quick-call defaults | Main → Ops | Rebuild from HQ log; defaults go ahead Wed. | Wed Nov 4 |
| MATCH-INBOX old lines (~76) + 8 TNT recs | Matches & Catalog | Priority 5a/5b. | Thu Nov 5 |
| Mini Mahjer code check; B&B / Miss / Mini 0-order watch | Ops / Main | Chrome check of minimahjer.com; watch orders. | Wed Nov 4 |
| My Fair drop watch + Black Friday policy | Main | Her yes/no on the "shop through our link" line (HQ This week). | Fri Nov 6 |
| 7 amounts (My Fair ×4, OMM ×2, Middle & Main) | Tiffany / Ops | Screenshots or sign-ins (HQ This week). | This week |
| Holiday colour cards (Tinselle ×2, Dec 1994, PLM Spirit + Nutcracker) | Matches & Catalog | Not started (was due Oct 31). | Thu Nov 5 |
| My Fair Mahjong Style of Your Life (#1 album) | Matches & Catalog | Colour card + TNT, then swipe book. | Thu Nov 5 |
| Sunday Sets TNT rec leftovers | Matches & Catalog | docs/research/sunday-sets-colorcards-tnt-oct29.md. | Thu Nov 5 |
| Larkspur hearts into 27 tile albums | Matches & Catalog → Ops | Paste album by album. | Fri Nov 6 |
| Holiday album covers page update | Matches & Catalog | With the late-picks update (1.14 is live). | Thu Nov 5 |
| December 1994 redo (her RTS notes) | Matches & Catalog | After holiday colour cards. | Fri Nov 6 |
| Holiday reels redo (Nutcracker/FYM reel with Table view) | Main | 1.14 live + v5 standard; storyboard first. | Fri Nov 6 |
| Bam Bird Deco trio (Indigo first) | Matches & Catalog | Colour cards ×3, then books. | Week of Nov 9 |
| Brand-lock sample for Bird & Bamboo | Matches & Catalog | Hosted embed only. | Week of Nov 9 |
| Affiliate applications (apply kit) | Tiffany submits / Main | Kit doc 00h; HQ apply-kit-oct31. | This week |
| FB group weekly Claude Doc | Main | https://claude.ai/artifact/54ovPaB6BQU78ztjUgQSbe; add holiday albums + Mahjong Row posts. | Wed Nov 4 |
| Tortoise rack piece (her Oct 28) | Main | Scope + storyboard; gift-guide tie-in. | Fri Nov 6 |
| UpPromote accounts → mahjmatchmaker@ | Main | Her logins where the owner must move it. | Fri Nov 6 |
| Discount links not converted (Britt Mills, Mahjong Register, YMI, RMS, Hip Hip, Wren/Soirée/Amanda Toppe) | Main | builder/fym_fix_oct21/discount_check_oct21.json. | Fri Nov 6 |
| Amazon mats into gallery + FYM | Ops → Matches & Catalog | Her picks only (1 to pick, HQ This week). | Fri Nov 6 |
| ShopMy holiday leftovers | Main → Ops | ShopMy (not MAHJMATCH) for Charleston Mahjong Club + Bamlet's in holiday posts. | Fri Nov 6 |
| FYM usage tracking LIVE ENDPOINT | Matches & Catalog | DEPLOYED Nov 4 2:25pm (config/fym-tracking.json, tested OK). Matches & Catalog: apply TRK_URL with builder/fym_track_oct17.py in the v114 release TODAY (both places); gate [157] blocks --release without it. Then confirm rows land in the sheet from a real phone swipe. | TODAY |
| Fait à Main code | Main | MAHJMATCH still not applicable at cart. | Watch |

- **OPS: follow + favorite @mahjpit.co** (new partner Mahj Pit, Nov 4; handle verified: their return-policy page names @mahjpit.co + public IG business account); log in docs/IG-FAVORITES.md.
- **Matches & Catalog: Mahj Pit catalog into FYM** (mats, racks, tile sets; partner, code MAHJMATCH) via the partner catalog pipeline + photo flags, in the next build (MATCH-INBOX Nov 4 NEW PARTNER line; gate [114] blocks release until done).

## Blocked, approved (raise at the top of every attended reply until done)
- IG EVERGREEN CODES POST (Main, her plan Nov 4 3:55pm): ONE grid post, Partner Brands graphic + every code typed in the caption ("<Brand> discount code: MAHJMATCH (x% off)"), moved to the very bottom of the grid (her Meta One drag), caption EDITED to stay current (new brand, % change) by Claude in Chrome on instagram.com; replace the image when the graphic changes. Draft in Planoly 01a1a859-bcb8 (auto-publish blocked for Claude; she taps Post). After it posts: Google check "<brand> discount code" for an @mahjmatchmaker result in the morning report. NOT on the FB Page (Oct 30 rule) and no Tigre de Tartan / YMI typed.
- PAYOUT RECONCILE PASS 2 (Main): read every program's actual payout terms (schedule, minimum, hold days) from its dashboard Program details / Payment page + GoAffPro store terms -> config/payout-terms.json; re-split Oct "approved, not yet due" $4,093 into due-by-<date> vs overdue; needs PayPal signed in. Britt Mills = "Design Mill" PayPal (resolved). Kathrine Zell $3.15 Oct 15: Tiffany checking.
- Mahjong Row Moody Tortoise + Brunette Burl: group post LIVE Nov 4 2:40pm (no links yet). WATCH mahjongrowandco.com/products.json: the moment either product page exists -> edit the group post comment with the links + pull both into FYM (Matches & Catalog) before Fri Nov 6 10am CT. Owner: Main (launch watch).
- Main: render HQ Money "Payouts" section from collection payouts (summary + per brand). First pass data in HQ Nov 4 (docs/reports/payouts/2026-11-04.md). Next pass: read Bam Bird, My Fair, Mini Mahjer, Hip Hip, Charleston, Bam!, Splash, Amahj UpPromote dashboards (one shop session at a time) + PayPal once signed in; identify "Design Mill" $135.48 (Nov 1) and "Kathrine Zell" $3.15 (Oct 15) payers.
- PAYOUT RECONCILE (Main, started Nov 4): ledger of earned vs paid vs pending vs overdue per brand, PayPal matched, HQ Money "Payouts" section; spec docs/PAYOUT-RECONCILE.md. First pass today in Chrome (GoAffPro payouts, Marketplace payments, PayPal read-only, both inboxes); then weekly + 1st/16th.
- FYM tracking TRK_URL into the live app: Matches & Catalog, v114 release, today (endpoint live Nov 4).

## Waiting on Tiffany (only things she can answer now)
**On HQ Today, in this order (4):**
1. **This week's posts: look at the drafts in Planoly** (Wed Polo Club reel + New this week first; drag the carousel onto Wed).
2. **Bespoke Sunshine Glow drops 10am ET: reshare their post to stories.**
3. **7 quick calls: defaults go ahead today** (reply only with the numbers you want different).
4. **Work With page v3 + Brands form: yes to go live** (open since Nov 1; default: Claude puts it live Thu Nov 5 unless she says wait).

**On HQ This week:** OMM Juniper + Lotus Cove (swipe Lotus Cove before Nov 11); My Fair Black Friday "shop through our link" yes/no; 7 amounts; Sweet Jojo W-9; 2 quick FYM checks + Holy Mahj; Sunday Sets round 2 (4 sets); affiliate apply kit; 1 hidden FYM photo (Grace Peacock); 1 Amazon mat to pick; 2 stray ShopMy links.

**Asked in chat, not yet answered: the owning chat RE-ASKS at the top of every reply until answered, with its default (Tiffany Nov 4: nobody said 'ask once'; her rule is 'ask, move on, COME BACK'):**
- Main: **launch reel redo OK** (sent ~5:35pm Nov 3); Malachite how-to reel v2 OK + day; FB group B&B racks wording; (search logging: same Apps Script endpoint as FYM tracking, done Nov 4, wire into search with the site-search install);
- Matches & Catalog: Lagoon + Mulberry splits; Bam Bird Classic Tortoise match pick; Sunday Rattan: is the 'new' one the Blue Rattan; Fruit Stand rack-edge (default a); brand-lock pricing (undecided, don't push).

## Banked (finished, held on purpose)
- **Petalée (Virora)**: 61 cards, RTS `l-final-petalee`, vault (her Oct 28). Before publishing: colour card, 10% band sweep on the Amanda Toppe/Girly cards, cleaner Petalwing/Coralia photos.
- **Holiday intro reel v5** (46s): POSTED Nov 3 ~4:30pm on IG + story + FB Page (Reels tab). It is the reference standard for future FYM reels (FYM-REEL-RULES 23-41).
- **Retro Rattan holiday table reel + 7-frame story**: undated Planoly drafts (01a16477-0588, -078d); reel caption fails lint (510 chars, no #MahjMatch): fix before reuse.
- **Night of the Raven mood board reel (Canva) + Halloween story + old Raven carousel**: keep for next Halloween (Planoly records in docs/planoly-archive/2026-11-03-deleted-drafts.json).
- **Vivienne mat album (OMM)**: 16 cards, parked (no mat albums, Oct 23); its hearts go into the tile albums.
- **Season 2 tile-dating episode reels (Ep 1-13 + trailer): PARKED, not abandoned** (Tiffany Nov 3: "down the road"). Renders assets/reels/s2/; captions fail lint (length + naming): rewrite before reuse. Jade "Smith-style" reel parked (needs her song).
- **Holiday reels Nov 1** (FYM Nutcracker, Holiday Vault + albums carousel, 3 brand reshare reels; assets/social/holiday-nov1/): rebuild to the v5 standard before use.
- **Face-to-camera script + Ask Me Anything carousel** (assets/social/next-week-talk/): drafts, HQ needs/talk-and-ama-2026-11-01.
- **Poppins mat-alert set** (assets/social/mat-edit/poppins/): CONFIDENTIAL until OMM announces Poppins (wholesale-only, her Nov 3 rule).
- **Partner kit explainer video v2 + launch explainer reel + tutorial reel**: built, not used.
- **Restock companion frames** (assets/social/restock-oct27/, restock-huntclub-oct30/, restock-tinselle-oct31/): reuse at the next restock.
- **Brownstone Bloom group post**: not doing (her Nov 3 2:00pm: fall is past); holiday albums get the first new-albums email.

## Later / ideas
- **Clean up 52 legacy caption lint warnings** (still 52 Nov 3) (config/social/content_lint_baseline.json; mostly missing #MahjMatch, '(affiliate)', 2 TdT captions) (rules audit E9, Oct 30). Also 78 legacy FAILs (length 42, naming 36) in banked Season 2 captions: same kinds as yesterday, nothing new.
- **FYM Shuffle** idea for 1.15 (Matches & Catalog, Nov 3).
- **Brand-locked FYM pricing**: pilot with Emily (60-90 days, friend rate or trade), then setup + monthly; hosted embed only; pricing undecided (her Nov 3 3:56pm).
- **Launch reel may need another redo** once Table view is the main view (her Nov 3 4:37pm).
- **Anders Ruff Puppy Love Solo Play mat** ($48 preorder), **Miss Mahjong Garden Party + Cherry Blossom travel mats** ($40): solo/travel, record only (launch watch Nov 3).
- **Peace Love Mahjong mini holiday launch** Wed Nov 4 8am CT (Merry Mahjong hats, Rack Pets, tile bag): accessories, codes post mention only (partner watch Nov 3).
- **Bird & Bamboo 20in stain racks back in stock, 21in sold out until January** (Emily, Nov 3): record; FYM rack stock.
- **Maison Mahj first sale** ($595, Nov 3): onboarding worked; watch.
- **Let's Mahj On new tile sets** (Wild, Sweet, Golf, Refined, Merry, Stir Things Up), coming mid-Nov: new products; ONE swipe book only if she says.
- **OMM 2027 International Mahjong Card** preorder ($12, ships Jan 2): record only; possible teacher/FB group mention.
- **Peace Love Mahjong Black Friday Nov 16**, **Virora Lilacée restock Nov 10**: codes post + social on the day.
- **Reels earn 0 follows two weeks running; the single 'It's a match' image is still the best post** (social measure, Nov 2): weigh image posts in next week's kit.
- **Sunday Blues restock post window ~Nov 16** (HQ card parked to Nov 16).
- IDEA (Tiffany Nov 1 11:33pm, not now): fold racks into the mat step for Aerial/Table views; revisit once Table view is the main view.
- **Mahjong Register** Crystal Palace acrylic racks + Solid Wood racks (launch watch Oct 31): FYM rack lists when Matches & Catalog has room.
- **Sunday Vegan Leather mat moved listing** (launch watch Oct 31): relink the FYM card in the next build.
- **Brands later (her Oct 31 picks):** Feltectors, Four Winds Social, Mahj House Rules, Mahjong Made Chic, Mahjong Moxie, Silk Mahjong, The Mahjong Line (teacher program only).
- **Bam Bird restock/brand announcement** teaser (IG Oct 30): same day or never.
- **Amanda Toppe Lila**: full-size later = swipe book the day it lists (Oct 29).
- **Table view later**: walls for pattern-back sets with no back photo, mats+tiles price filter, aerial photos from partners, Table view as a partner perk vs open to all (undecided, don't push) (Tiffany Nov 1).
- **Splash of Color digest**: 4 undigested Splash mats; digest at 10+ (launch watch Nov 1).
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

## Daily operations (Tue Nov 3)
| Operation | Done today? | Notes |
|---|---|---|
| Affiliate tracking (Money tab) | ✅ Done | Mon close-out 9:38am (final $114.39, 12 sales); 2:04pm check $73.60 / 6 sales (Maison Mahj first sale $59.50); 27 affiliate emails reconciled. Spikes: Anders Ruff, Amanda Toppe, Maison. 0-order alert B&B / Miss / Mini Mahjer (answered in HQ; Mini Mahjer code check to Ops). 7 amounts open. Midnight close-out still to run. |
| Google code report | ⏭ Not due | Mon done (24/38 Overview, 34/38 AI Mode). Next due Wed Nov 4. |
| Morning Google report | ✅ Done | 10:26am: 28/38 AI answers name MAHJMATCH (+4: Miss Mahjong, Anders Ruff, Mini Mahjer, Maison Mahj); OMM still not named; SC 7-day clicks 602 (+242%). Weekly strategy review logged. |
| Verified dates (weekly, Mondays) | ✅ Mon | Not due Tue. Miss still live: Wren "Verified: October 9" (priority 1b). |
| Codes post (Mondays) | ✅ Done | Published Tue ~9:25am in the FB group from her account (Poppins removed, Amanda Toppe 10%), list as first comment, featured. |
| Pinterest queue health | ✅ OK | Planoly Pinterest: 3-4 pins/day scheduled Nov 4 → Nov 29+, 0 errors. Autopin Wed. |
| Indexing | ✅ Done | 9 changed brand pages requested (built-in browser, 1:20pm). Amanda Toppe + Wren wait on their fixes. |
| Planoly next-7-days (IG + FB Page) | ❌ Not covered | 0 IG posts SCHEDULED Nov 4-10 (all 8 are drafts for her review, per her Nov 3 rule). Holiday intro reel posted by her (IG + story + FB Page). Planoly lint: 18 FAIL (16 on story-draft captions: no MAHJMATCH / #MahjMatch; 2 on banked Retro Rattan reel). FB targets: all feed/story groups have one except the Polo + Rudolph sticker-story reminders (reel FB versions are separate groups). Priority 3. |
| New albums (last 7 days) (f) | ✅ All checks | Brownstone Bloom (live Nov 1): /mahjong-tile-matches ✅, /ivory-mahjong-tile-matches ✅, /anders-ruff-discount-code ✅, /links ✅, Pinterest queue ✅, indexing ✅ (Nov 2). No other album went live (Emerald/Pearlescent entries are Retired-label updates). |
| Repo caption lint (g) | ⚠️ Legacy only | 78 FAIL (length 42, naming 36), all banked Season 2 captions; 52 legacy WARN. Same kinds as yesterday, nothing new. |
| Restock first (c) | ✅ Checked | No album-set restock dated Wed. |
| Match inbox (e) | ⚠️ ~76 old open | Priority 5a. |
| Launch + partner watch | ✅ Done | Launch watch 9:15am (3 new) + 6:15pm (11 new, 9 to FYM); partner watch 9:45am, 2:50pm, 6:40pm (Noli live, Sunshine Glow Wed, Bam Bird MCM Olive Fri, PLM mini holiday, MRC teasers, TdT Oyster live, B&B 20in racks back); mentor check (Juniper/Lotus Cove Nov 11). Missed: Mahjong Row's ~10am IG announcement (caught by her 12:57pm). |
| FYM + partner feedback | ✅ Done | 0 new (2:17pm). |
| FYM releases | ✅ LIVE | **Version 1.14 live ~7:20pm** (Table view, tour rebuild, hearts, one match card per set, rack menu, Wood tone/Painted, picks off) in all 3 places after 3 QA rounds; snapshot v114 (1664 mats). |
| Weekly ShopMy mats check (Tue) | ✅ Done | 33 Etsy staged for 1.15, 1 Amazon to pick. |
| TNT scan (Tue) | ✅ Done | 8 new recs, not yet in tnt-recs.json (priority 5b). |
| HQ + Ready to Ship cleanup | ✅ Done | Morning 6:47am (17 → 16), sweeps 9:47am / 1:47pm / 7:47pm, this desk run 17 → 15 open, Today 4. Supabase pin closed (accounts work, her 2:40pm). |

## Never-ending projects
- **Find Your Mat-ch™ app** (artifact 6epA9HuEdT32zUp79Qv3kd; public **Version 1.14** = v114: website pin fym-v114 @be2ab101, page-block c1a73bd2 on /find-your-match + /find-your-mat-ch-preview, verified by curl Nov 3): gate + independent QA before every publish (QA loads the WEBSITE copy as live: 0 broken images, gate [115]); artifact AND website copy AND README 0a pin in the same step; +0.1 version label (docs/FYM-VERSIONS.md); her feedback the same day with a gate check; when a publish/paste fails, MESSAGE HER right away. Artifact file budget: run builder/fym_artifact_fit.py and publish ONCE. Every nav/header change: screenshot live at 1280, 1440 and 390 with the phone menu OPEN. New partner catalog in FYM within 24h of its inbox line (gate [114]). Refresh config/fym-mats-snapshot.json after every publish.
- **Match inbox** (docs/MATCH-INBOX.md): any chat writes match/catalog misses there the same turn; Matches & Catalog marks DONE when shipped.
- **Google / MAHJMATCH in AI answers (her #1)**: AI Overview + AI Mode per partner, code report (Mon/Wed/Fri), daily morning report, indexing (brand pages first), sitemap health, weekly verified dates + hub date, weekly codes post (FB GROUP only typed out; IG/FB Page = logos graphic + short caption), alarm on any lost citation.
- **Albums**: order (her Oct 28 3:31pm): MFM Style of Your Life → Bam Bird Deco trio (Indigo first) → Sunday Blues → Sunday Nature Walk → Middle & Main Peach and Pine, Mac + Miller; Mahjong Row fall + OMM green set (Juniper) jump the line; a known restock goes FIRST. Doc 86b (colour card FIRST), book_gate.py, PICKING-RULES.md, NEW-ALBUM-CHECKLIST.md (incl. the new-albums email).
- **Holiday (Merry Mahjong)**: intro reel posted Nov 3; next = late picks into holiday albums, holiday albums + FYM holiday group posts, new-albums email; docs/MERRY-MAHJONG-BRIEF.md + docs/plans/holiday-calendar-nov-dec.md; promote FIND YOUR MAT-CH, not albums (her Oct 30); any FYM social shows the tool working; storyboard before render; song shortlist on every reel; FYM-REEL-RULES 23-41.
- **New products**: hq/newproducts → gallery + FYM colour-tagged → weekly roundup. Never albums. New-mat social = "Match up <mat> in Find Your Mat-ch", never ahead of the brand; wholesale-only/unannounced = confidential.
- **Social** (docs/SOCIAL-SYSTEM.md, ~2 hrs/week of her time): every planned post as a Planoly DRAFT on its day (final media, lint PASS, Tag people, FB Page target, story version); she reviews in Planoly; FB Page target on every IG group; every slide to stories; brand tags + collabs; restocks/launches SAME DAY or never; ≥4 IG posts in every next-7-days window.
- **Facebook group**: community, never ads; weekly codes post (doc 94); weekly Claude Doc of planned posts; @everyone at most ~once a week.
- **Partner share graphics**: one per brand + our MAHJMATCH version (38 logos as of Noli June).
- **Pinterest**: queue within the pace rule; evergreen pins of our own images.
- **Affiliates + money**: sales checks 2:04pm + 12:04am, reconcile every referral email (both inboxes), refunds on the refund date, spike AND drop checks; onboarding new partners (page, hub, logos, FYM within 24h, indexing, IG follow/favorite); affiliate applications (kit doc 00h).
- **Mat Gallery + colour system**: sort rule, holiday rule, partner-only gate (plus her Oct 31 non-partner picks), shop-by-colour partners first (Oct 31); gallery row for every visible FYM mat (gate [90]).
- **ShopMy + Amazon storefronts**: square-safe covers, aerial mat photos, HQ ShopMy tab intake, weekly ShopMy mats check (Tue).
- **HQ hygiene**: Today ≤5, answered = gone, event passed = gone, timestamps on every card, inline previews; ANSWERS.md before asking anything; no answer is not a no.

## Log of this rewrite (Tue Nov 3 night)
- **Done today:** FYM 1.14 live (Table view + tour rebuild + hearts, 3 QA rounds); holiday intro reel v1→v5, approved, posted by her on IG + story + FB Page; codes post published in the FB group; accounts sign-in working (Supabase + Resend DNS); 46 stale Planoly drafts archived + deleted; this week's 8 drafts in Planoly; launch reel redo built; Mahjong Row group post drafted; holiday albums + FYM holiday group posts drafted; new-albums email template; late holiday picks recorded; 9 pages indexed; morning report (28/38); ShopMy + TNT weekly scans; 2 launch watches + 3 partner watches + mentor check; reel rules 23-41 + brand guide tagline/wordmark rules.
- **Found mid-way and given a home:** Amanda Toppe 20% still live (2 days) → priority 1a; Wren Oct 9 verified line → 1b; late picks not in holiday albums → 2; story-draft captions fail Planoly lint + 0 IG scheduled → 3; launch reel redo unanswered → Waiting (chat); FB Page intro "coming 10.27" → 5d; Nov 2 site check still not in git → 5c; TNT 8 recs not in tnt-recs.json → 5b; holiday-intro HQ card (posted) archived; Lotus Cove card merged into the OMM Juniper card.
- HQ smoke test at 390px not run tonight (data-only change, no page HTML changed).

See CLAUDE.md.
