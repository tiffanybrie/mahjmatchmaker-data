# The Desk
Rewritten nightly by the end-of-day desk cleanup (9:23pm ET). The morning HQ cleanup (6:47am ET) reads it. Rules: CLAUDE.md ("THE DESK"), docs/CHATS.md (which chat owns what). During the day, when an agent stops, Chrome drops or a QA stalls, add the item here right away with its next step.

**Last rewrite:** Thu Oct 29, 2026, ~9:45pm ET (desk cleanup run). Covers the 90 commits of Oct 29 ET (5a97a19 … 29c4d92), docs/ANSWERS.md (Oct 29 lines 633-700), docs/MATCH-INBOX.md (Oct 29), Planoly (IG workspace 019fc27c… + Pinterest 019fc27b…), HQ needs / hq/albums / hq/now / hq/priorities, Ready to Ship (`ship` docs + NOW list), the scheduled task list, and curl checks of the live site tonight.

**Owners (three chats, Oct 22):** Main (Opus) = social/Planoly, site pages, email, HQ/DESK, decisions, Google + SEO. Matches & Catalog (Opus) = Find Your Mat-ch, albums, gallery, catalog, search index. Ops (Sonnet) = the ONLY Chrome driver: Squarespace pastes, uploads, IG follows/checks.

**Repo note:** checkout on `partner-catalogs-sqsp`. The repo is ~3.5 GB locally; a plain fetch dies. Tonight worked: `git fetch --depth=60 origin partner-catalogs-sqsp:refs/remotes/origin/partner-catalogs-sqsp`, then `git fetch --shallow-since=<date> …`.

**PARTNER SEND GATE (Oct 27 3:08am, standing):** before scheduling ANY partner email or graphics drop, run `python3 scripts/partner_send_check.py`; it must exit 0.

## Tomorrow's top priorities (Fri Oct 30), in order
Standing order: (1) Find Your Mat-ch launch: DONE Oct 27 (now Version 1.7 = v103, live in the artifact, /find-your-match and /find-your-mat-ch-preview). (2) Fall content before it expires: Brownstone Bloom live Fri, Night of the Raven before Halloween Sat. Then holiday: Merry Mahjong from Mon Nov 2. Her Oct 29 Google alarm ("major drop") rides as priority 3 because it is money. The order is clear from her answers, so no "set the order" card tonight.

1. **Brownstone Bloom album LIVE Fri Oct 30 (Matches & Catalog → Ops).** She answered in HQ 8:04am: order is good (no Save needed), drop the B&B Wine rack, swap the messy AR tortoise for the best tortoise. Config done (M&M Hawksbill Heritage Tortoise + Bam Bird Olive on the tile side; M&M Hawksbill + PLM Burl on the Brownstone Bloom mat side). NOT DONE: rebuild the 40 cards with the new racks (MATCH-INBOX Oct 29 ~2pm). Steps: rebuild cards → brownstone_block.py (site/livepatch/brownstone-bloom-oct20/README.md "Live step") → warm jsDelivr → Ops pastes (new page + /mahjong-tile-matches cover + home + colour page) → /links latest-album card → docs/NEW-ALBUM-CHECKLIST.md top to bottom → curl 200. Live check tonight: /brownstone-bloom-mahjong-tile-matches = 404. Not a Christmas piece. If it can't go live Fri, message her once with the new time.
2. **Night of the Raven mood board reel before Halloween (Main).** Missed Thu noon: no export from her. Waits on her: tile wiggle + export, or "post without" (HQ Today #3; Canva https://www.canva.com/d/zMN-9inujTcWD-C, design DAHZU2dFIQY). On export: Planoly reminder reel (first line = the one key action, song shortlist, brand tags + collab) + FB Page copy (brand names), Fri evening or Sat morning. If nothing by Fri 2pm ET, message her once in chat. Clear the date on the OLD Raven carousel 01a16477-092f (never delete).
3. **Google AI Overview drop: the plan (Main + Ops).** Diagnosis docs/research/ai-overview-drop-oct29.md: Google holds Oct 2-10 copies of 5 pages; overviews favour codes typed out on social. (a) Partner codes post: 3 texts ready (HQ Today #1, `needs/codes-post-2026-10-29`); on her yes, IG + FB Page into Planoly 10am ET, FB group post from her account in Chrome (doc 82) and featured. Weekly Monday draft task now exists (trig_01QNpTLC6egFF4u4oethFWVP, Mon 7:37am). (b) Sitemap resubmit + recrawl of My Fair, Peace Love, Bespoke, Mini Mahjer, Hip Hip in Search Console = Claude's job, Ops/Main in Chrome tomorrow (was on the alert card, now archived as merged). (c) Mahjong Row & Co. affiliate dashboard is SIGNED OUT in Chrome: only she can sign in (HQ Today #2); until then MRC sales (our #1 brand) are undercounted.
4. **Overdue Ops trip with Chrome (6th day, Claude's job; HQ `overdue-site-pastes-oct27`).** Curl tonight: stray `fym-v72` still on /find-your-match + preview; /links still carries the dead `mmlFymSoon` "Coming 10.27" card; holiday anchor fix not live (`holiday-matches` 0 hits on Sierra); thin-album 41 hearts (site/livepatch/thin-albums-oct26, pin e718949b) + site search header (site/livepatch/search) still not done. DONE today: YOLO page re-paste (all 21 links carry ?sca_ref=12572562.5IBLjBHZ1vuX4J, live). Same trip: Brownstone paste (priority 1), Planoly $13/mo Content Marketplace add-on cancel (her "cancel" Oct 27), Etsy Palm Beach Chic (listing 4444245533) flat photo check, Mahj & Moon ShopMy links (handoff below), IG partner follows/favorites ONE profile at a time 20-30s apart (YOLO included). Ops had Chrome today (1.7 preview paste, ShopMy covers) but this list wasn't run: run it FIRST in the next Ops chat.
5. **Merry Mahjong week (Nov 2-8) storyboards (Main), due Fri Oct 30.** Not started today. Stills first for her OK: Mon Merry Mahjong kickoff (every Christmas album, holiday mats + tile sets, FYM holiday flow) and Anders Ruff Christmas #1 (every AR Christmas mat on Dear Santa; preorder, ships Nov 17; B&B wood racks tie-in). Into the HQ Social tab with a 3-5 song shortlist each; variety rule. Brief: docs/MERRY-MAHJONG-BRIEF.md, calendar docs/plans/holiday-calendar-nov-dec.md.

**Watch tomorrow:** Mahjong Row & Co. "something good is coming your way tomorrow… friends and family first dibs" (IG teaser Oct 29) = Fri Oct 30, product unnamed. If it is the fall collection (Rosy / Ellington), it JUMPS the album line the same day (colour card first, doc 86b). Mahj Mood Jade Luxe racks drop Fri 10am CST (story + FB group line, same day or never).

## Handoffs to do first (Fri morning)
- **Matches & Catalog: Brownstone card rebuild** (priority 1 above).
- **Matches & Catalog: FYM Version 1.8 (v104)**, all approved Oct 29, gate + independent QA, artifact AND website (rule 0), +0.1 label:
  - Brand menu copy APPROVED 3:32pm: title "Shop by brand", subline "Code MAHJMATCH works at brands marked ♥", heart badge per partner, non-partners at the bottom (replaces "Partner brands come first…"). Keep the pink box at the top (3:33pm).
  - Opening screen (her 3:31pm clarification): keep "Shop by colour" where it is; NO colour selected on arrival; the default view below = partner brand LOGOS (OMM first, then by last-30-day commission; tap a logo = that brand's sets). Tapping a colour shows that colour's sets, partners first, non-partners last. Mock-up stills to her FIRST (MATCH-INBOX 15:27-15:33).
  - Holiday calls on 11 mats (config/tiffany-color-notes/2026-10-29-holiday-calls.json: all holiday except OMM Liberty + Britt Mills Crimson Harvest).
  - Chinoiserie Cheer flat photo (assets/mats/v95-etsy/chinoiserie-cheer-flat.jpg); YOLO links with ?sca_ref; Holy Mahj (Bluest Blooms) + Queen Bee real photos from her Canva uploads.
  - Launch watch adds (MATCH-INBOX Oct 29 6:30pm): OMM Poppins, Sunday Green Gingham + Blue Gingham + Blue Rattan, Let's Be Besties Sapphire Leaves; plus the Oct 28 list still owed (Bam Bird Plaid x3, B&B White Wood Stain rack, Britt Mills Bella Leatherette, AR Paws in the Garden + full-size preorder, LBB Ornamental Charm + Tidal Glass + Jingle Jungle, Retro Riviera x2, OMM Dapper 2 → retired).
  - v103 QA photo notes: Gray Malin (Bespoke) corner close-up → hide + Questionable unless a whole-mat image exists; Peaches 'n Cream (M&M) washed out → better brand photo.
  - Mahj & Moon ShopMy links once Ops makes them.
  - After publish: refresh config/fym-mats-snapshot.json (fym_snapshot.py).
- **OPS: ShopMy links for the 14 VISIBLE Mahj & Moon mats in FYM** (her Oct 26 decision, caught again Oct 29 1:31pm; still not done). config/mahj-moon-shopmy-links.json: find each Etsy listing (MahjandMoonCo), add to her ShopMy "Mahj & Moon Mats" collection (aerial photo), copy the go.shopmy.us link into the JSON, commit; mark not_on_etsy where missing.
- **DONE Oct 30 12:30am: Gmail signature v2 installed in mahjmatchmaker@gmail.com** (signature "Mahj Matchmaker", default for new + replies; verified after reload, 8 images incl. FYM banner). site/livepatch/gmail-signature-oct29.html
- **OPS (standing): HQ ShopMy tab inbox** (db `shopmy`, status new) at the start of every Ops reply, per docs/SHOPMY-INTAKE.md. 2-hourly pickup proposed, waiting on her yes (ask once in chat).
- **Main: footer "Brands" link → /brands form → auto-reply → hidden /work-with-us, DUE Fri Oct 30** (decided Oct 19 + Oct 24; she caught it Oct 29 12:33pm). Live tonight: /brands 404, /work-with-us 404. Copy must follow her Oct 29 rules: only TWO groups (partners give a code, non-partners = no discount); never pitch the Discount Codes page or Google ranking; one guaranteed match album per partner brand; data stays internal; drop "Partners get featured…"; add the "Why affiliate programs make sense" section (her 12:55pm points); answer what happens if a shop is NOT on Shopify (her RTS l-workwith6 note). site/livepatch/workwith/README.md. Form + footer link can go up first with the approved Oct 19 copy (Ops paste).
- **Main: sales-check fix (Oct 29 miss).** The 2pm run missed a Mahjong Row "approved" email at 7:57am. Update the sales-check task prompt: list ALL secomapp + goaffpro + backinstock emails of the day (no keyword filter), reconcile each referral number to a money entry, report unmatched; drop check every run vs same time of day (her 2:49pm alarm).
- **Main: Bam Bird 3-day sales stop** (0 orders Oct 26-28 after a record week): check the Bam Bird page in Search Console + AI Overview. Claude's job (HQ card archived tonight).
- **Main: launch reel redo.** Storyboard sent 12:08pm (assets/social/fym-launch/redo-oct29/storyboard.jpg, 31 stills ~38s, more dynamic per her 11:41am). Waiting on her OK → render → archive (not delete) the Oct 27 reel → post the redo → pin it in the old spot. On HQ This week (`launch-reel-redo-oct29`).
- **Main: Planoly cleanup (her Oct 27 ask, still not done).** Clear dates (never delete) on past-day drafts (list on the Oct 28 desk: 01a16052-33a6 … -40c3, 01a17911-ab58, 01a17a6a-943b / -95d3 / -9777, 01a17a6c-10e4, 01a176a0-8458, 01a1791a-d167, 01a17c71-b34b, 01a17c72-0c6d / -0e9a / -11d0 / -152c, 01a16477-0ce9, 01a16052-36fd / -3da0, 01a16793-3e02, 01a17a6c-12c1, Raven carousel 01a16477-092f). Oct 21 reminder 01a16052-2828 still shows "scheduled". Halloween story 01a16477-0b08 (Sat 10/31 9am CT): confirm it's still a draft and that she OK'd it, then schedule (plain frames auto-post); not found in tonight's first two Planoly pages, check by id.
- **Main: Santa Baby's Cocktail Hour** (Splash mat, banned from books/albums, doc 55): ask her once in chat whether her 12 yes go anywhere; else archive. **Due Fri Oct 30.**
- **Main: FB group weekly Claude Doc of planned group posts** (her Oct 27 ask), first one due Fri Oct 30: codes post (doc 94), B&B racks, Mahj Mood Jade Luxe racks, Lucky Bam sale.
- **Matches & Catalog: Sunday Sets TNT rec hunt, due Fri Oct 30** (book v26 has the rest). Still missing: Holy Mahj / Bluest Blooms WHOLE flat photo (Canva uploads), Mahjong by SI Brewtifully, Haus of Tiles (Dapplefield, Fieldmark; Ops/Chrome), Mahjong Made Chic Leopard Luxe (password-locked), Silk Mahjong, Piper Chase Studios, Cheetah in Bloom, unnamed Lemondrop / Rack It / Let's Be Besties / 2 TdT. docs/research/sunday-sets-colorcards-tnt-oct29.md.
- **Matches & Catalog: My Fair Style of Your Life colour card + TNT search START Fri Oct 30** (album #1 in her Oct 28 order).
- **Matches & Catalog: TAB RULE** on the remaining Chrome scheduled tasks (left: sales check, Google code report, ShopMy check, TNT scan, verified dates, weekly Google & OMM, weekly SEO review). Her YES Oct 29 ~11:10am.
- **Main: Mahj Mood code** (unused codes deactivated after 4 months, email Oct 28): check ours works before the next Mahj Mood post (Jade Luxe Fri).
- **Main: partner feedback watch** (trig_01RKw9eUwTYPo39gbYHb65gh): its cron runs every day of Oct + Nov; DISABLE after the Nov 10 run.

## Swipe-book rules audit (Oct 29, book_gate.py; owner Matches & Catalog unless noted)
- **Sunday Sets ×4**: rebuilt today to every rule (colour cards, TNT recs incl. her non-partner recs, widest pool, fill-frame Hummingbird; book v26, gate PASS). Waits on her round-2 swipe (HQ This week).
- **Tinselle Emerald + Ruby**, **December 1994**, **Peace Love Spirit of Christmas + Merry Nutcracker**: colour cards + TNT search before cards. **Due Sat Oct 31.**
- **Petalée** (banked): colour card before it goes live.
- **OMM / Peace Love holiday mats**: "Mat Edit" colour cards with the Nov 2 holiday push.
- **Green Light Gatsby** round 2: widest pool + TNT; **Nov 9**.
- **Not started** (MFM Style of Your Life, Bam Bird Deco trio, Peach and Pine, Fire + Fortune, Bam Bird MCM, Mahjong Row fall): book_gate blocks any book without colour card + TNT record + widest pool.

## In progress
| Item | Owner | Next step | Target |
|---|---|---|---|
| Brownstone Bloom album | Matches & Catalog → Ops | Priority 1: rebuild 40 cards (new racks), block, paste, checklist. | Fri Oct 30 |
| Night of the Raven mood board reel | Main | Priority 2: her export, then Planoly reminder + FB Page. | Fri Oct 30 / Sat Oct 31 |
| Google AI Overview drop plan | Main + Ops | Priority 3: codes post on her yes; sitemap + recrawl in Chrome; MRC sign-in. | Fri Oct 30 |
| Overdue Ops trip | Ops | Priority 4 (6th day). | Fri Oct 30 |
| Merry Mahjong kickoff + AR Christmas #1 storyboards | Main | Priority 5. | Fri Oct 30 (for Mon Nov 2) |
| FYM Version 1.8 (v104) | Matches & Catalog | Handoff list above; opening-screen mock-up stills to her first. | Mon Nov 2 |
| Brands footer link + /brands form + /work-with-us | Main copy → Ops paste | Handoff above. | Fri Oct 30 |
| Launch reel redo | Main | Her storyboard OK → render → swap on grid. | After her OK |
| My Fair Style of Your Life album (#1 in her order) | Matches & Catalog | Colour card + TNT first, then mat swipe book (PICKING-RULES). | Swipe book by Mon Nov 2 |
| Bam Bird Deco trio (Indigo first) | Matches & Catalog | Colour cards ×3, then mat books, then racks. | Week of Nov 9 |
| Holiday colour cards (Tinselle ×2, Dec 1994, PLM Spirit + Nutcracker) | Matches & Catalog | Cards + TNT search. | Sat Oct 31 |
| Sunday Sets TNT rec hunt | Matches & Catalog (+ Ops reads) | Handoff above. | Fri Oct 30 |
| Mahj & Moon ShopMy links in FYM | Ops → Matches & Catalog | Handoff above. | Fri Oct 30 |
| Sales-check prompt fix + Bam Bird lull | Main | Handoffs above. | Fri Oct 30 |
| Planoly cleanup + Halloween story | Main | Handoff above. | Fri Oct 30 |
| FB group weekly Claude Doc | Main | First one. | Fri Oct 30 |
| Tortoise rack piece (overdue, her Oct 28) | Main | Find any started draft (doc 55), scope, storyboard; gift-guide tie-in. | Storyboard by Wed Nov 4 |
| Table view / walls (Build your set) | Matches & Catalog | Sample phase; storyboard of the table view in FYM; waits on her size-check photos (HQ This week). | Storyboard by Wed Nov 4 |
| Wed social leftovers (Malachite reel v2, B&B racks FB group post, Jade FB Page copy) | Main | Offer Malachite for Sun Nov 1; show B&B wording; Jade FB copy with the next reel. | Sun Nov 1 |
| Hosting + sign-in cost estimate | Main | In chat next time she's in Main. | Mon Nov 2 |
| Usage plan recap | Main | Chat recap, no HQ card. | Mon Nov 2 |
| YOLO Mahjong onboarding | Matches & Catalog → Ops | Page live with ref (done). Left: FYM links (v104), IG follow/favorite. | Mon Nov 2 |
| UpPromote accounts → mahjmatchmaker@ | Main | Her Oct 27 ask; needs her logins where the owner must move it. | Wed Nov 4 |
| Verified line missing | Main | I Love Mahj. Weekly refresh Mondays 8:17am ET (hub date fixed Oct 29). | Mon Nov 2 |
| MATCH-INBOX open items | Matches & Catalog | Rack cut-outs, MRC Scalloped Tortoise for every set, rack length by tile size, 69 FYM mats with no gallery row (gate [90]), 38 angled mats (gate [89]), Spirit of Christmas composite, MFM Poppy Red racks, TdT/OMM/Fait à Main TNT recs not in FYM. | Wed Nov 4 |
| Late partner holiday mats → holiday albums | Matches & Catalog | Her 30 picks: picks page now autosaves + has Send final answers; db `picks` still EMPTY tonight. Once in, build into the holiday albums. | On her Send |
| Holiday albums content from Nov 1 | Matches & Catalog | Spirit of Christmas (10 cards) + Malachite 8 new cards ready; Dec 1994 RTS notes; Tinselle, OMM + PLM holiday mats, Santa Baby's. | Nov 1 onward |
| Mat swipe-book hearts into tile albums | Matches & Catalog → Ops | Larkspur cards built, on 0 of 27 albums; then the rest. | After the Ops trip |
| IG pinned row, 3rd pin cover | Main | NOW LIVE cover to replace "LAUNCHING TOMORROW". Pairs with the launch reel redo pin. | With the redo |
| Subscriber "It's here!" email | Main | Never approved; ask "send or skip" once in chat. | Mon Nov 2 |
| Discount links not converted (Britt Mills, Mahjong Register, YMI, RMS, Hip Hip, Wren/Soirée/Amanda Toppe) | Main | builder/fym_fix_oct21/discount_check_oct21.json. | Wed Nov 4 |
| Amazon mats into gallery + FYM; missing swipe-book products | Ops → Matches & Catalog | Her picks only. | Wed Nov 4 |
| ShopMy holiday leftovers + square-safe covers | Main → Ops | Covers v3 done Oct 29 (25 shelves). ShopMy (not MAHJMATCH) for Charleston Mahjong Club + Bamlet's in holiday posts. | Wed Nov 4 |
| Partner feedback watch | Main | Daily; 0 real partner feedback so far. Disable after Nov 10. | Nov 10 |
| Papaya Beechwood README | Matches & Catalog | Live since Oct 22; README already says LIVE (closed). | Done |

## Waiting on Tiffany (only things she can answer now)
**On HQ Today, in this order:**
1. **Partner codes post: say yes** (three texts ready; Google reads these).
2. **Sign back in to the Mahjong Row & Co. affiliate dashboard** in Chrome (signed out; our #1 brand's sales aren't counting).
3. **Raven reel: wiggle + export, or "post without"** (Halloween is Sat).
4. **Today's amounts: Bird & Bamboo + My Fair Mahjong** (2 orders).
5. **Late holiday mats: tap Send final answers** on the picks page (her 30 picks are saved on her phone).

**On HQ This week:** OMM Poppins swipe (all 49 album sets); launch reel redo storyboard OK; Gmail signature v2 yes/change; "no answer is not a no" into CLAUDE.md OK; open the gate to non-partner brands?; brand-locked FYM for partners, keep exploring?; Sunday Sets round 2 (4 sets); table view size-check photos; Amazon storefront old holiday posts (her login); overdue Ops trip (Claude's job, open the Ops chat when the computer is on).

**Asked in chat, not on HQ (the owning chat asks once, next time she's there):**
- Main: Malachite how-to reel v2 OK + day; FB group B&B racks wording; subscriber "It's here!" email send or skip; ShopMy 2-hourly pickup yes; Santa Baby's 12 yes (by Fri); table view as a partner perk vs open to all (undecided, don't push).
- Matches & Catalog: TdT Estate Sale works-for-holiday?; which "Photo coming soon" sets to show; Lagoon + Mulberry splits; Bam Bird Classic Tortoise match pick; Dapper 2 replacement mat; FYM default tile-set order proposal (brand logo headers, OMM first, then by 30-day commission) beyond the approved opening screen.

## Banked (finished, held on purpose)
- **Petalée (Virora)**: 61 cards, RTS `l-final-petalee`, vault (her Oct 28). Before publishing: colour card, 10% band sweep on the Amanda Toppe/Girly cards, cleaner Petalwing/Coralia photos.
- **Vivienne mat album (OMM)**: 16 cards, parked (no mat albums, Oct 23); its hearts go into the tile albums.
- **Season 2 episode reels + trailer**: undated Planoly drafts (Ep 1-13). Each gets redone with an intro first. Jade "Smith-style" reel parked (needs her song).
- **Night of the Raven carousel** (Planoly 01a16477-092f): superseded by the mood board reel; keep for next Halloween.
- **Holiday tables** (Polo Club, Rackin' Rudolph, Retro Rattan): Planoly drafts, need her OK before scheduling.
- **Partner kit explainer video v2 + launch explainer reel + tutorial reel**: built, not used.
- **Restock companion frames** (assets/social/restock-oct27/): reuse at the next restock.
- **Brand-locked FYM sample (Mahjong Row & Co.)**: built Oct 29 (2113012), not public; waits on her "keep exploring?" (HQ This week).

## Later / ideas
- **FYM default tile-set order by brand logos + commission ranking** (Oct 29 3:29pm, proposal pending beyond the opening screen).
- **Opening the gate to non-partner brands** (Mahjong by SI, Haus of Tiles, Lemondrop…; Oct 29 12:01pm + 1:18pm; she is deciding).
- **Brand-locked FYM as a partner perk** (Oct 29 12:41pm).
- **Brand demand data for partners** later, once user numbers are real (Oct 29 1:00pm; stays internal for now). **Accounts / stars** to know real user counts (Oct 29 1:00pm).
- **Rakuten** skipped (Oct 29 11:17am); revisit only if ShopMy's Etsy rate drops or a wanted brand is Rakuten-only.
- **Let's Mahj On 7 new tile sets** delayed to mid-Nov (IG Oct 29 6:14pm): new products, never albums unless she says.
- **Amanda Toppe Lila**: travel Lila drops Mon Nov 2 10am ET (100 made; travel = no album); full-size 33in Lila later: swipe book the day the listing appears (partner watch Oct 29).
- **Table view as a partner perk vs open to everyone** (Oct 28 2:43pm); **partners opt in with aerial photos** (Oct 28 2:39pm); **ask Emily about a pusher** (Oct 28 2:52pm).
- **"Mahj Garage"** accounts + "I own this" (Oct 28 2:35pm); competitor Mahj Closet ($9.99) (Oct 27 6:01pm).
- **IG Saved "Save for repost"**: partner reposts 1-2/day; holiday reposts from Nov 1 (Oct 28 10:04am).
- **Restock page** (Oct 28 10:31am).
- **Mahjong Row & Co. fall collection** + **OMM green set** jump the album line the day they drop (Oct 28 3:26/3:34pm).
- **Charleston Mahjong Club Après-Ski small album + Cabana Club** (Oct 28 3:13pm). **Middle & Main Peach and Pine** and **Mac + Miller Fire + Fortune** after Nature Walk (Oct 28 3:31pm).
- **Gift content from early/mid Dec** (Oct 28 3:13pm).
- **Build your set extras**, **Mahj registry, AI "dream mat", dream set builder** (Oct 27).
- **Content like @mahjandmotif**; **a better FYM reel** (Oct 27; docs/FYM-REEL-RULES.md, rules 20-22 added Oct 29).
- **Partner portal**, **separate desktop vs mobile FYM**, **mat-only brand "eye candy" story**, **OMM reshares only 100%-OMM content**, **FB group growth plan** (Oct 25-26).
- **Canva template library + #MahjMatch reshares** (Oct 25); **IDEAS 3.0** (Oct 23); **internal FYM sets view**, **every-tile-set gallery**, **Pinterest ShopMy single-product pins** (Oct 24); **Match Monday / Reader Request** (Oct 23); **Rebecca Illustrated 15% ShopMy**, **Aurora's racks** (Oct 22); **brand alert sign-ups, comment-for-link, UPS cutoffs Dec 1** (Oct 21); **site colours, "Press for Mahjong" rename**, **$200/mo API credits plan** (after launch).
- **New brand releases** are NEW PRODUCTS, never albums (Anders Ruff Bellamy Bloom / All American / Heritage Tartan; Bespoke x Brooks Brothers; Bespoke x Gray Malin; Britt Mills Emerald Mirage; Mahj & Vine Whispering Winds).

## Daily operations (Thu Oct 29)
| Operation | Done today? | Notes |
|---|---|---|
| Affiliate tracking (Money tab) | ⚠️ Done with gaps | 5 missed sales found 4:51pm and added (MRC ×3, LBB, Miss Mahjong $38.25); ShopMy-only rows added (MTD $8,504.73); 2 amounts still owed (HQ Today); MRC dashboard signed out = undercount. Launch week Oct 22-28: 147 sales / $3,228 (+32% vs prior week). 12:04am close-out still to run. |
| Google code report | ✅ Done | Not a report day (Mon/Wed/Fri), but the AI Overview drop check ran (docs/research/ai-overview-drop-oct29.md): 5 brands lost, The Mahjong Co. recovered; feedback sent. Next report Fri 10:52am. |
| Verified dates (1st/15th) | ➖ Not due | Weekly Mondays 8:17am ET; next Nov 2. Hub /mahjong-discount-codes fixed to "Updated October 29, 2026" (live). |
| Pinterest queue health | ✅ OK | 100+ pins scheduled Oct 30 → Nov 24, 0 errors. |
| Indexing | ✅ Done | Re-index requested for the 5 dropped brand pages (7648b15). Sitemap resubmit still to do (priority 3). |
| Planoly next-7-days (IG + FB Page) | ❌ Not covered | 0 scheduled Oct 30 - Nov 5; last post Oct 27. Raven reel waits on her export; codes post waits on her yes; Halloween story Sat unconfirmed; Merry Mahjong Mon Nov 2 not storyboarded. |
| Launch + partner watch | ✅ Done | 5 runs: Holly Jolly DS leatherette back (Mahjong Register), MR&Co teaser for Fri, Poppins, Sunday ginghams + Blue Rattan, LBB Sapphire Leaves, Amanda Toppe Lila, Let's Mahj On delay. |
| FYM + partner feedback | ✅ Done | 0 real partner feedback. |
| HQ + Ready to Ship cleanup | ✅ Done | Morning 6:48am + Main sweeps + this desk run. RTS NOW = 0 open (Brownstone order answered in HQ). |

## Never-ending projects
- **Find Your Mat-ch™ app** (artifact 6epA9HuEdT32zUp79Qv3kd; public Version 1.7 = v103 in the artifact AND /find-your-match + preview): gate + independent QA before every publish; artifact AND website copy AND README 0a pin in the same step; locks; pending queue; photo flags; +0.1 version label (docs/FYM-VERSIONS.md); her feedback the same day with a gate check; when a publish/paste fails, MESSAGE HER right away. Watch the 256 MiB artifact cap. Every nav/header change: screenshot live at 1280, 1440 and 390 before calling it done (Oct 29 rule).
- **Match inbox** (docs/MATCH-INBOX.md): any chat writes match/catalog misses there the same turn.
- **Google / MAHJMATCH in AI answers (her #1)**: AI Overview + AI Mode per partner, code report, indexing (brand pages first), weekly verified dates + hub date, weekly codes post typed out on social (doc 94, Mondays), alarm on any lost citation.
- **Albums**: order (her Oct 28 3:31pm): MFM Style of Your Life → Bam Bird Deco trio (Indigo first) → Sunday Blues → Sunday Nature Walk → Middle & Main Peach and Pine, Mac + Miller; Mahjong Row fall + OMM green set jump the line; a known restock goes FIRST. Doc 86b (colour card FIRST), book_gate.py, PICKING-RULES.md, NEW-ALBUM-CHECKLIST.md; pick pages show mat + tiles together.
- **Holiday (Merry Mahjong, from Nov 2)**: docs/MERRY-MAHJONG-BRIEF.md + docs/plans/holiday-calendar-nov-dec.md; Anders Ruff first; storyboard before render; variety; song shortlist on every reel.
- **New products**: hq/newproducts → gallery + FYM colour-tagged → weekly roundup. Never albums.
- **Social** (docs/SOCIAL-SYSTEM.md, ~2 hrs/week of her time): every approved post in Planoly at its time; storyboard before any render; restocks/launches SAME DAY or never, stories + FB only; every slide to stories; brand tags + collabs; FB Page copy of every IG post; social plan in the HQ Social tab; reel rules 20-22 (phone never moves, every product tagged, tiles + mat together).
- **Facebook group**: community, never ads; weekly codes post (doc 94); weekly Claude Doc of planned posts.
- **Partner share graphics**: one per brand + our MAHJMATCH version.
- **Pinterest**: queue within the pace rule; evergreen pins of our own images.
- **Affiliates + money**: sales checks 2:04pm + 12:04am, reconcile every referral email, spike AND drop checks every run; "Affiliates you've applied to" card on top of HQ's Affiliates tab; ShopMy-only earnings as 'ShopMy:' rows (never double count Mini Mahjer); onboarding new partners (page, hub, logos, FYM, indexing, IG follow/favorite).
- **Mat Gallery + colour system**: sort rule, holiday rule, partner-only gate; gallery row for every visible FYM mat (gate [90]); two-colour coordination over tonal.
- **ShopMy + Amazon storefronts**: square-safe covers (preview both tile shapes), aerial mat photos, Etsy collections end ' (Etsy)', HQ ShopMy tab intake, weekly ShopMy mats check Mondays.
- **HQ hygiene**: Today ≤5, answered = gone, event passed = gone, timestamps on every card, inline previews, Ready to Ship holds anything one step from done; ANSWERS.md before asking anything; no answer is not a no.

## Log of this rewrite (Thu Oct 29 night)
- **Done today:** FYM Version 1.6 (v102: aerial switch by the deck, bottom-right tile inset, mat-door aerial, Shop by brand in both doors with discount labels) and Version 1.7 (v103: pink Shop by brand feature box, card titles = tile back colour, fill-frame Hummingbird) live in the artifact + both website pages, gates [102]/[103] added; FYM leads the site menu as a pink pill (CSS v39; header button reverted after it covered the nav); Sunday Sets swipe book rebuilt three times to the new rules (FYM photos, widest pool, colour cards with 7-8 faces, TNT + non-partner recs, book v26) and scripts/swipe/book_gate.py now enforces them; YOLO page re-pasted with her affiliate link; hub "Updated" date fixed; AI Overview drop diagnosed + re-index requested + weekly codes-post task created + this week's codes post drafted; 5 missed sales found and logged, ShopMy added to Money; ShopMy square-safe covers (25) + HQ ShopMy intake tab; Rakuten skipped (her call); traffic numbers saved; partner pitch + brand tier rules into the brand guide; Gmail signature v1 → v2; launch reel redo storyboard; HQ "Affiliates you've applied to" card; 5 launch/partner watch runs.
- **Found mid-way and given a home:** Brownstone cards never rebuilt after her 8:04am rack answer (and RTS still showed "put in order" though she'd said the order is good) → priority 1, RTS item answered; Raven reel missed Thu noon → priority 2; MRC dashboard signed out (sales undercounted) → new HQ Today card; sitemap resubmit was sitting on her alert card though it's our job → priority 3, card merged into the codes post; Ops trip still not run though Ops had Chrome → priority 4 (6th day); Merry Mahjong storyboards not started → priority 5; Mahj & Moon ShopMy links still not made → Ops handoff; approved FYM menu copy + opening screen + holiday calls + launch-watch adds not yet built → v104 handoff; launch reel redo storyboard waiting only in chat → HQ This week card; Bam Bird sales-lull card was our job → archived to Main; Holly Jolly restock card (same-day only) and Amanda Toppe sneak peek (info only) → archived; Brands page/form still 404 on its due date eve → Main handoff Fri.

See CLAUDE.md.
