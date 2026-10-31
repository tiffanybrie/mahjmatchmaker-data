# The Desk
Rewritten nightly by the end-of-day desk cleanup (9:23pm ET). The morning HQ cleanup (6:47am ET) reads it. Rules: CLAUDE.md ("THE DESK"), docs/CHATS.md (which chat owns what). During the day, when an agent stops, Chrome drops or a QA stalls, add the item here right away with its next step.

**Last rewrite:** Fri Oct 30, 2026, ~9:45pm ET (desk cleanup run). Covers the 84 commits of Oct 30 ET (eac71e46 … 72dfd817), docs/ANSWERS.md (Oct 30 lines 718-762), docs/MATCH-INBOX.md, Planoly (IG workspace 019fc27c… all 55 groups + Pinterest 019fc27b… queue), HQ needs / answers / log / hq/albums / hq/now / hq/priorities, Ready to Ship (`ship` docs + NOW list: 0 open), site/livepatch READMEs, config/release-calendar.json, content_lint (repo + Planoly next 7 days), and curl checks of the live site tonight.

**Owners (three chats, Oct 22):** Main (Opus) = social/Planoly, site pages, email, HQ/DESK, decisions, Google + SEO. Matches & Catalog (Opus) = Find Your Mat-ch, albums, gallery, catalog, search index. Ops (Sonnet) = the ONLY Chrome driver: Squarespace pastes, uploads, IG follows/checks.

**Repo note:** checkout on `partner-catalogs-sqsp`. The repo is ~3.5 GB; if a plain fetch dies use `git fetch --depth=60 origin partner-catalogs-sqsp:refs/remotes/origin/partner-catalogs-sqsp`.

**PARTNER SEND GATE (Oct 27 3:08am, standing):** before scheduling ANY partner email or graphics drop, run `python3 scripts/partner_send_check.py`; it must exit 0.

## Tomorrow's top priorities (Sat Oct 31, Halloween), in order
Standing order: Google is #1 (Tiffany Oct 29 11:03pm: Google work before reels/graphics), then fall content before it expires (Halloween is tomorrow, Brownstone is the last fall album), then holiday from Mon Nov 2. RESTOCK FIRST check (c): no dated restock for an album set tomorrow (Hunt Club restock is not an album set; next album restocks are Sunday Blues ~Nov 23, Jade & Brass racks ~Nov 24). The order is clear, so no "Set tomorrow's order" card tonight.

1. **Google: the open Claude jobs (Main + Ops).** (a) **Sitemap resubmit** in Search Console (sitemap.xml → Sitemaps; confirm brand pages listed) — on the plan since Oct 29 (docs/research/ai-overview-drop-oct29.md step 4), still NOT done. (b) **Bam Bird page check** in Search Console + AI Overview (3-day sales stop Oct 26-28; Bam Bird dropped out of AI Overview again in report v12). (c) Today's morning Google & Revenue report stayed PARTIAL (computer offline; catch-up couldn't re-fire it): fill the Search Console clicks/position fields by hand in seo/2026-10-30 on the next browser run. (d) Codes post: the FB-group redo card (needs/codes-post-2026-10-29) was closed from HQ at 2:33pm with no yes and no change note; the Monday codes-post draft task (trig_01QNpTLC6egFF4u4oethFWVP, Mon 7:37am) makes Monday's card. Main: ask her once in chat whether she posted it herself or wants Monday's version (don't re-ask on HQ). Overview count is 22/36 (report v12, was 24).
2. **Halloween (Main, time-boxed to Sat).** (a) Night of the Raven mood board reel: still no export (HQ Today). On her export or "post without": Planoly reminder reel (first line = the one key action, song shortlist, brand tags + collab) + FB Page copy (brand names), Sat morning. If nothing by Sat 2pm ET, the reel is done for this year (keep it banked, never delete). (b) **Halloween story draft 01a16477-0b08** is dated Sat 10/31 10am CT but is a DRAFT with a REVIEW line and no OK found in ANSWERS: it will NOT post. Plain frame (shop-the-look), no tags = auto-post eligible. Ask her once in chat at the start of Main ("Post the Halloween story at 10am CT?"); on yes, add a Facebook Page story target and schedule. (c) Clear the date on the OLD Raven carousel 01a16477-092f (never delete).
3. **Planoly next 7 days = 0 IG posts scheduled (Main).** Audit (d): only the stale Oct 21 Papaya reminder shows "scheduled"; Oct 31-Nov 6 has 5 undated-for-her drafts (Halloween story; Polo Club reel + story Wed 11/4; Rackin' Rudolph reel + story Fri 11/6), none with a Facebook target, and the Polo + Rudolph reel captions FAIL lint (length 544/431 > 350, no #MahjMatch). Default kit: next week's storyboards (HQ needs/social-week-2026-11-02, 7 days from existing albums) are the album-of-the-week kit; push for her yes Sat. ON HER YES: render finals, Planoly IG + Facebook Page targets, stories with every slide, Tag people from config/social/ig-handles.json, `content_lint.py --planoly <export> --only-ig` must pass. Rework the Polo/Rudolph captions before they're offered (lint). Planoly API can't add a target to an existing group: recreate the group with IG + FB when scheduling. Merry Mahjong kickoff + Anders Ruff Christmas #1 stills (brief docs/MERRY-MAHJONG-BRIEF.md) still not storyboarded: fold into this kit for Mon Nov 2.
4. **Brownstone Bloom album LIVE + MATCH-INBOX sweep (Matches & Catalog → Ops).** Brownstone MISSED Fri: the 40 cards were never rebuilt with her 8:04am Oct 29 rack swap (no commit), live page still 404 tonight. Steps: rebuild cards (M&M Hawksbill on the Brownstone mat side, no B&B Wine) → brownstone_block.py (site/livepatch/brownstone-bloom-oct20/README.md) → warm jsDelivr → Ops paste (new page + /mahjong-tile-matches cover + home + colour page) → /links latest-album card → docs/NEW-ALBUM-CHECKLIST.md top to bottom → curl 200. Tell her the new time once in chat. **MATCH-INBOX (e): ~30 lines older than 2 days have no DONE.** Several shipped in v104-v106 and only need marking DONE (Bam Bird Plaid ×3, AR Paws in the Garden, LBB Tidal Glass / Retro Riviera / Retro Riviera Simple Middle, LBB Ornamental Charm). Still open: OMM Dapper 2 → retired + replacement, Sunday Rattan + Festive Plaid back in stock, LBB Jingle Jungle Leatherette, MFM Solid Poppy Red racks, Britt Mills Bella Leatherette, late holiday mats into albums (waits on her Send), 69 FYM mats with no gallery row (gate [90]), 38 angled mat photos (gate [89]), rack length by tile size + Scalloped Tortoise for all sets, Spirit of Christmas composite, TdT Estate Sale question. Plus tonight's: Launch watch Oct 30 6pm (8 LBB/Britt Mills mats). FYM artifact is at 512/512 files: the next version must delete before adding (builder/fym_artifact_fit.py).
5. **Overdue Ops trip with Chrome (9th day, Claude's job; HQ `overdue-site-pastes-oct27`).** Curl tonight: stray `fym-v72` still on /find-your-match + /find-your-mat-ch-preview (next to fym-v106); /links still has the dead `mmlFymSoon` "Coming 10.27" card; 41 thin-album hearts (site/livepatch/thin-albums-oct26, pin e718949b) 0 of 9 pasted; holiday anchor fix; site search header (site/livepatch/search); Brownstone paste (#4); **Brands footer link + /brands form + /work-with-us** (decided Oct 19/24, due Fri Oct 30, MISSED: both 404; Main writes the copy per her Oct 29 rules, form + footer link can go up first with the approved Oct 19 copy; site/livepatch/workwith/README.md); Planoly $13/mo Content Marketplace add-on cancel (her "cancel" Oct 27); Amazon: post the new 'A Reindeer Holiday Table' board (same 6 tags) then note on HQ needs/amazon-remove-old-boards-oct21 for her to delete the old one; Dropbox copies of the Oct 30 new-release renders (Britt Mills ×5, Let's Be Besties ×3 → /Mahj Matchmaker Albums/New releases/…); Mahj & Moon ShopMy links (config/mahj-moon-shopmy-links.json, 14 mats); Etsy Palm Beach Chic flat photo check. Run it FIRST in the next Ops chat; close finished Claude tab groups at start.

## Handoffs (do first)
- **Main: Virora Tinselle Emerald Green RESTOCK (Oct 31 ~9:35am ET, live, $299; holiday album set, 23 FYM matches).** Tiffany messaged + push 9:45am ET. 3 story frames for her review (never posted): assets/social/restock-tinselle-oct31/out/ (tin-A-cream-trio, tin-B-green-trio, tin-C-white-duo). HQ needs/launch-virora-tinselle-emerald-oct31. Virora had no IG post yet; reshare theirs if one appears. Next desk: if not shared and it sells out again, archive "too late".
- **Main: CMC Hunt Club restock (Oct 30, same day only).** HQ needs/launch-cmc-hunt-club-oct30 (reshare https://www.instagram.com/p/DfIegGSBKS2/ + 3 frames assets/social/restock-huntclub-oct30/out/). Morning cleanup: if she didn't reshare, check stock; sold out or not done = archive "too late" (rule 9).
- **Main: add "close leftover finished Claude tab groups at start" to every Chrome task TAB RULE** (Tiffany Oct 30 10:10am). Not done yet.
- **Main: add the mat-edit-alert build step to launch watch trig_01S2VsjwznnHev1uUbYmEwJq** (Tiffany Oct 30 9:05am; rework mat_alert.py into an FYM phone-mockup "Match up <mat> in Find Your Mat-ch" builder per her 10:14am direction; show the TOOL working). Runbook docs/MAT-EDIT-ALERT.md.
- **Main: POPPINS on hold** until OMM announces it + its paired tile set; then the FYM match-up piece for her tile pick (ANSWERS Oct 30 10:14am).
- **Matches & Catalog: FYM next-build notes** (MATCH-INBOX Oct 30 eve): searched mat ignores later filters; Noli June "$100 min" on the card; Noli 4-mat holiday drop when released; Maison Mahj catalog.
- **Main: sales-check prompt fix** (list ALL secomapp + goaffpro + backinstock emails, reconcile each referral number, drop check vs same time of day). Still not applied.
- **OPS (standing): HQ ShopMy tab inbox** (db `shopmy`, status new) at the start of every Ops reply (docs/SHOPMY-INTAKE.md).
- **Main: partner feedback watch** trig_01RKw9eUwTYPo39gbYHb65gh: DISABLE after the Nov 10 run.

## In progress
| Item | Owner | Next step | Target |
|---|---|---|---|
| Google: sitemap resubmit, Bam Bird check, partial morning report | Main + Ops | Priority 1. | Sat Oct 31 |
| Night of the Raven reel + Halloween story | Main | Priority 2; her export / OK. | Sat Oct 31 |
| Next week's social (Nov 2-8) + Merry Mahjong kickoff | Main | Priority 3; her yes, then render + Planoly IG + FB Page. | Sun Nov 1 (for Mon Nov 2) |
| Brownstone Bloom album | Matches & Catalog → Ops | Priority 4: rebuild 40 cards, block, paste, checklist. | Mon Nov 2 |
| MATCH-INBOX stale lines | Matches & Catalog | Priority 4: mark shipped DONE, work the rest. | Mon Nov 2 |
| Overdue Ops trip (incl. Brands form + /work-with-us) | Ops (+ Main copy) | Priority 5. | Next Ops chat |
| Launch reel redo | Main | Storyboard on HQ This week; on OK render → archive old → pin. | After her OK |
| FYM next version (1.9.2) | Matches & Catalog | Next-build notes + launch-watch adds; delete files first (512/512). | Tue Nov 3 |
| Holiday colour cards (Tinselle ×2, Dec 1994, PLM Spirit + Nutcracker) | Matches & Catalog | Cards + TNT search (was due Sat Oct 31, not started). | Mon Nov 2 |
| My Fair Style of Your Life album (#1 in her order) | Matches & Catalog | Colour card + TNT first (was due to start Fri, not started). | Swipe book by Tue Nov 3 |
| Sunday Sets TNT rec hunt leftovers | Matches & Catalog (+ Ops reads) | Holy Mahj whole flat, Haus of Tiles, Silk Mahjong, Piper Chase… (docs/research/sunday-sets-colorcards-tnt-oct29.md). | Tue Nov 3 |
| Bam Bird Deco trio (Indigo first) | Matches & Catalog | Colour cards ×3, then books. | Week of Nov 9 |
| Planoly cleanup (her Oct 27 ask) | Main | Clear dates (never delete) on past-day drafts (01a16052-33a6…-40c3, 01a16052-36fd, -3da0, 01a16793-3e02, 01a16477-0ce9, 01a17a6a-943b/-95d3/-9777, 01a17c71-b34b, 01a17c72-0c6d/-0e9a/-11d0/-152c, 01a17a6c-10e4, 01a17a6c-12c1, 01a16477-092f); the Oct 21 reminder 01a16052-2828 still shows "scheduled". | Sun Nov 1 |
| FB group weekly Claude Doc | Main | Doc exists (https://claude.ai/artifact/54ovPaB6BQU78ztjUgQSbe); keep it current with the week. | Mon Nov 2 |
| Santa Baby's Cocktail Hour | Main | Ask once in chat whether her 12 yes go anywhere (was due Fri). | Sun Nov 1 |
| Tortoise rack piece (her Oct 28) | Main | Scope + storyboard; gift-guide tie-in. | Wed Nov 4 |
| Table view / walls | Matches & Catalog | Waits on her size-check photos (HQ This week). | Wed Nov 4 |
| Mahj Mood code check (unused codes expire after 4 months) | Main | Check ours before the next Mahj Mood post. | Mon Nov 2 |
| Hosting + sign-in cost estimate; usage recap | Main | In chat, no HQ card. | Mon Nov 2 |
| UpPromote accounts → mahjmatchmaker@ | Main | Her logins where the owner must move it. | Wed Nov 4 |
| Discount links not converted (Britt Mills, Mahjong Register, YMI, RMS, Hip Hip, Wren/Soirée/Amanda Toppe) | Main | builder/fym_fix_oct21/discount_check_oct21.json. | Wed Nov 4 |
| Amazon mats into gallery + FYM | Ops → Matches & Catalog | Her picks only. | Wed Nov 4 |
| ShopMy holiday leftovers | Main → Ops | ShopMy (not MAHJMATCH) for Charleston Mahjong Club + Bamlet's in holiday posts. | Wed Nov 4 |
| Mat swipe-book hearts into tile albums | Matches & Catalog → Ops | Larkspur cards built, on 0 of 27 albums; after the Ops trip. | After the Ops trip |
| Fait à Main code | Main | MAHJMATCH still not applicable at cart (waiting on their link/coupon). | Watch |

## Waiting on Tiffany (only things she can answer now)
**On HQ Today, in this order:**
1. **Raven reel: wiggle + export, or "post without"** (Halloween is Sat).
2. **Next week's social (Nov 2-8): yes all, or yes/no per day** (one yes covers the week; brand-mix default b).
3. **Bird & Bamboo amount** for Fri's sale (screenshot of the commission page).
4. **Late holiday mats: tap Send final answers** on the picks page.
5. **CMC Hunt Club: reshare + 3 story frames** (tonight only; the morning cleanup archives it if not done).

**On HQ This week:** launch reel redo storyboard OK; Sunday Sets round 2 (4 sets); open the gate to non-partner brands?; table view size-check photos; rules check: pause 2 old tasks?; LBB Artist Collective sneak peek (info); overdue Ops trip (Claude's job).

**Asked in chat, not on HQ (the owning chat asks once, next time she's there):**
- Main: Halloween story 10am CT yes?; did she post the FB group codes post herself (card closed with no yes)?; Malachite how-to reel v2 OK + day; FB group B&B racks wording; subscriber "It's here!" email send or skip; ShopMy 2-hourly pickup yes; Santa Baby's 12 yes; table view as a partner perk vs open to all (undecided, don't push).
- Matches & Catalog: TdT Estate Sale works-for-holiday?; Lagoon + Mulberry splits; Bam Bird Classic Tortoise match pick; Dapper 2 replacement mat.

## Banked (finished, held on purpose)
- **Petalée (Virora)**: 61 cards, RTS `l-final-petalee`, vault (her Oct 28). Before publishing: colour card, 10% band sweep on the Amanda Toppe/Girly cards, cleaner Petalwing/Coralia photos.
- **Vivienne mat album (OMM)**: 16 cards, parked (no mat albums, Oct 23); its hearts go into the tile albums.
- **Season 2 episode reels + trailer**: undated Planoly drafts (Ep 1-13). Each gets redone with an intro first, and the captions fail lint today (length + "Find Your Match" naming): rewrite before reuse. Jade "Smith-style" reel parked (needs her song).
- **Night of the Raven carousel** (Planoly 01a16477-092f) + the mood board reel if not posted Sat: keep for next Halloween.
- **Holiday tables** (Polo Club, Rackin' Rudolph, Retro Rattan): Planoly drafts, need her OK + caption lint fixes + FB targets before scheduling.
- **Poppins mat-alert set** (assets/social/mat-edit/poppins/): not approved as is; held until OMM announces Poppins.
- **Partner kit explainer video v2 + launch explainer reel + tutorial reel**: built, not used.
- **Restock companion frames** (assets/social/restock-oct27/, restock-huntclub-oct30/): reuse at the next restock.
- **Brand-locked FYM sample (Mahjong Row & Co.)**: "keep exploring" (her Oct 30); status docs/brand-lock/STATUS.md; rebuild on the current FYM when Matches & Catalog has room.

## Later / ideas
- **Clean up 52 legacy caption lint warnings** (config/social/content_lint_baseline.json; mostly missing #MahjMatch, '(affiliate)', 2 TdT captions) (rules audit E9, Oct 30). Also 78 legacy FAILs (length + naming) in banked Season 2 captions (assets/reels/ep*-caption.txt, assets/reels/s2/captions.json): no new kind today.
- **LBB Artist Collective mats** (early Nov; LBB new site Oct 30): new products, never albums (partner watch Oct 30).
- **Bam Bird restock/brand announcement** teaser (IG Oct 30): watch; same day or never.
- **Maison Mahj House Line No. 1** windows Nov 1-4 (non-partner, record only) (Oct 30).
- **Mary Benson Hydrangea tiles** Mon Nov 2 12pm/1pm ET (non-partner) (email Oct 29).
- **Amanda Toppe Lila**: travel Lila Mon Nov 2 10am ET (no album); full-size later = swipe book the day it lists (Oct 29).
- **FYM default tile-set order by brand logos + commission ranking** beyond the opening screen (Oct 29 3:29pm).
- **Opening the gate to non-partner brands** (Oct 29; on HQ This week).
- **Brand-locked FYM as a partner perk** (Oct 29 12:41pm); **brand demand data for partners** once user numbers are real; **accounts / stars** (Oct 29 1:00pm).
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

## Daily operations (Fri Oct 30)
| Operation | Done today? | Notes |
|---|---|---|
| Affiliate tracking (Money tab) | ⚠️ Done with gaps | 12:04am close-out (Oct 29 = 12 sales, Mini Mahjer filled from her screenshot → $257.92); 2:04pm run: 3 sales $32.62 (Peace Love, TdT, B&B amount pending: Chrome's UpPromote login is on Mini Mahjer); SITE DROP alarm (half of normal by 2pm; Mahjong Row's own FAMILY20 sale explains MRC). MTD $8,770.45. 12:04am close-out still to run. |
| Google code report | ✅ Done | Fri report day: v12 (https://claude.ai/artifact/PRpayBhn7vP4dJ8qR7i68X) Overview 22/36 (was 24), AI Mode 33/36; OMM MJTI feedback sent. Morning Google & Revenue report PARTIAL (computer offline; re-fire blocked). |
| Verified dates (weekly, Mondays) | ➖ Not due | Next Mon Nov 2 8:17am ET. Noli June page went live today with "verified October 30, 2026". |
| Codes post (Mondays) | ➖ Not due | Draft task Mon 7:37am. This week's FB-group redo card was closed with no yes (priority 1d). |
| Pinterest queue health | ✅ OK | 100+ pins scheduled Oct 31 → Nov 25 (3-4/day), 0 failed. |
| Indexing | ✅ Done | 11 tier-0 brand pages requested 12:35pm (quota hit on the 12th). Sitemap resubmit NOT done (priority 1a). Noli June page queued. |
| Planoly next-7-days (IG + FB Page) | ❌ Not covered | 0 IG posts scheduled Oct 31-Nov 6; 5 dated drafts, none with an FB target; 2 reel captions fail lint (priority 3). |
| New albums (last 7 days) | ➖ None | No album went live Oct 24-30 (Brownstone still 404), so the new-album checks (f) had nothing to check. |
| Repo caption lint (g) | ⚠️ Legacy only | 78 FAIL (length 42, naming 36) all in banked Season 2 captions untouched today; 52 legacy WARN. No new kind. |
| Launch + partner watch | ✅ Done | Runs 9:52am, 10:20am, 1:30pm, 6:05pm, 6:30pm: MR&Co FAMILY20 sale, LBB new site + Artist Collective, Jade Luxe racks live, CMC Hunt Club back in stock, 8 new LBB/Britt Mills mats → MATCH-INBOX, Maison Mahj dates, Bam Bird teaser. |
| FYM + partner feedback | ✅ Done | 0 partner feedback. |
| HQ + Ready to Ship cleanup | ✅ Done | Morning 6:50am + sweeps 9:47am / 1:47pm / 7:47pm + this desk run. RTS NOW = 0 open. |

## Never-ending projects
- **Find Your Mat-ch™ app** (artifact 6epA9HuEdT32zUp79Qv3kd; public Version 1.9.1 = v106 in the artifact AND /find-your-match + preview, pin 3fc677cc → fym-v106 @95a97a30): gate + independent QA before every publish (QA loads the WEBSITE copy as live: 0 broken images, gate [115]); artifact AND website copy AND README 0a pin in the same step; +0.1 version label (docs/FYM-VERSIONS.md); her feedback the same day with a gate check; when a publish/paste fails, MESSAGE HER right away. Artifact is at 512/512 files: run builder/fym_artifact_fit.py and publish ONCE. Every nav/header change: screenshot live at 1280, 1440 and 390 with the phone menu OPEN. New partner catalog in FYM within 24h of its inbox line (gate [114]).
- **Match inbox** (docs/MATCH-INBOX.md): any chat writes match/catalog misses there the same turn; Matches & Catalog marks DONE when shipped.
- **Google / MAHJMATCH in AI answers (her #1)**: AI Overview + AI Mode per partner, code report (Mon/Wed/Fri), indexing (brand pages first), sitemap health, weekly verified dates + hub date, weekly codes post (FB GROUP only typed out; IG/FB Page = logos graphic + short caption), alarm on any lost citation.
- **Albums**: order (her Oct 28 3:31pm): MFM Style of Your Life → Bam Bird Deco trio (Indigo first) → Sunday Blues → Sunday Nature Walk → Middle & Main Peach and Pine, Mac + Miller; Mahjong Row fall + OMM green set jump the line; a known restock goes FIRST. Doc 86b (colour card FIRST), book_gate.py (no second swipe book: config/swipe-books.json), PICKING-RULES.md, NEW-ALBUM-CHECKLIST.md.
- **Holiday (Merry Mahjong, from Nov 2)**: docs/MERRY-MAHJONG-BRIEF.md + docs/plans/holiday-calendar-nov-dec.md; promote FIND YOUR MAT-CH, not albums (her Oct 30); any FYM social shows the tool working; storyboard before render; song shortlist on every reel.
- **New products**: hq/newproducts → gallery + FYM colour-tagged → weekly roundup. Never albums. New-mat social = "Match up <mat> in Find Your Mat-ch", never ahead of the brand.
- **Social** (docs/SOCIAL-SYSTEM.md, ~2 hrs/week of her time): every approved post in Planoly at its time; FB Page target on every IG group; every slide to stories; brand tags + collabs; restocks/launches SAME DAY or never; ≥4 IG posts in every next-7-days window.
- **Facebook group**: community, never ads; weekly codes post (doc 94); weekly Claude Doc of planned posts.
- **Partner share graphics**: one per brand + our MAHJMATCH version (38 logos as of Noli June).
- **Pinterest**: queue within the pace rule; evergreen pins of our own images.
- **Affiliates + money**: sales checks 2:04pm + 12:04am, reconcile every referral email, spike AND drop checks; onboarding new partners (page, hub, logos, FYM within 24h, indexing, IG follow/favorite).
- **Mat Gallery + colour system**: sort rule, holiday rule, partner-only gate; gallery row for every visible FYM mat (gate [90]).
- **ShopMy + Amazon storefronts**: square-safe covers, aerial mat photos, HQ ShopMy tab intake, weekly ShopMy mats check Mondays.
- **HQ hygiene**: Today ≤5, answered = gone, event passed = gone, timestamps on every card, inline previews; ANSWERS.md before asking anything; no answer is not a no.

## Log of this rewrite (Fri Oct 30 night)
- **Done today:** Find Your Mat-ch went 1.7 → 1.8 (partner logos open the tiles door, real photos for 26+ "coming soon" sets) → 1.9 (photo + card touching, search at every step, Gray Malin Side A/B) → rolled back when the website copy broke 182 tile photos → 1.9.1 live in the artifact and both pages (B&B racks brand filter, Noli June + YOLO catalogs, gates [113]-[115]); phone menu fix live (FYM first, one line); Noli June onboarded and LIVE (page + hub 38 codes + logo graphic); Maison Mahj code partner live; TdT visible-code compliance on 97 album cards; Gmail signature v2 installed; rules audit applied (21 task edits, gates GA1-GA4, no second swipe book); Mat Edit / new-mat alert builder + Poppins set (held); next week's social storyboards built; 11 brand pages sent for indexing; code report v12; 5 launch/partner watch runs.
- **Found mid-way and given a home:** Brownstone missed its Fri date (cards never rebuilt) → priority 4; sitemap resubmit still undone → priority 1a; morning report partial → 1c; codes-post redo card closed with no yes → 1d (ask once in chat); Halloween story is a draft that won't post → 2b; Planoly empty for the next 7 days → priority 3; ~30 stale MATCH-INBOX lines → priority 4; Brands form/work-with-us missed Fri → Ops trip #5; Amazon reindeer board + Dropbox render copies (4:47pm Chrome run never logged) → Ops trip #5; Noli June README still said STAGED though live → marked LIVE; holiday colour cards + MFM Style of Your Life not started → In progress with new dates.

See CLAUDE.md.
- **OPS (Oct 31): paste FYM 1.9.2 on /find-your-match AND /find-your-mat-ch-preview.** Block: https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@e6688bd33f144b1d96219e3efe0097cc3b8054a2/site/livepatch/fym-preview-oct21/page-block.html (warmed). Steps: page → Edit → double-click the code block → CM6 dispatch the fetched html, then TYPE a space + Backspace while the editor is open, confirm Save is black, Escape, Save, Exit. Verify: curl both pages show fym-v107, then open a set with a new photo (Round Top Stamped) on the live page and confirm the photo loads. Artifact already on 1.9.2. Chrome was disconnected from Matches & Catalog ~1pm.
