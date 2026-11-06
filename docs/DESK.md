# The Desk
Rewritten nightly by the end-of-day desk cleanup (9:23pm ET). The morning HQ cleanup (6:47am ET) reads it. Rules: CLAUDE.md ("THE DESK"), docs/CHATS.md (which chat owns what). During the day, when an agent stops, Chrome drops or a QA stalls, add the item here right away with its next step.

**Last rewrite:** Thu Nov 5, 2026, ~9:50pm ET (desk cleanup run, cloud, no computer linked). Covers the 38 commits of Nov 5 ET (0bf730b … bf1e1b7), docs/ANSWERS.md (Nov 5 lines), docs/MATCH-INBOX.md, Planoly (IG workspace 019fc27c…: 20 groups, export docs/social/planoly-exports/ig-2026-11-05-desk.json; Pinterest 019fc27b…: 3-4 pins/day scheduled Nov 6 → Nov 30, 0 errors), HQ needs (29 open → 27; Today 5) / hq/albums / hq/now / hq/priorities / log, Ready to Ship (no new answers since Oct 30, per the 7:47pm sweep), config/release-calendar.json, content_lint (repo + Planoly IG export), curl checks (Mahjong Row page + hub, Amanda Toppe, Wren, OMM, /mahjong-tile-matches, /links, Brownstone Bloom).

**Owners (three chats, Oct 22):** Main (Opus) = social/Planoly, site pages, email, HQ/DESK, decisions, Google + SEO. Matches & Catalog (Opus) = Find Your Mat-ch, albums, gallery, catalog, search index. Ops (Sonnet) = the ONLY Chrome driver: Squarespace pastes, uploads, IG follows/checks.

**Repo note:** checkout on `partner-catalogs-sqsp` (~4.7 GB with assets). A plain fetch hangs. Working recipe: `git fetch -q --depth=60 origin partner-catalogs-sqsp:refs/remotes/origin/partner-catalogs-sqsp` then `git checkout -B partner-catalogs-sqsp origin/partner-catalogs-sqsp` (~1 min). Never `git ls-tree -l` on a blobless clone.

**PARTNER SEND GATE (Oct 27 3:08am, standing):** before scheduling ANY partner email or graphics drop, run `python3 scripts/partner_send_check.py`; it must exit 0.

**NEW RULE TODAY (Tiffany Nov 5 9:20pm, ANSWERS):** a partner pausing or ending its program is a NEW decision: ask her first. The "broken code" standing authority does NOT cover removing a partner's code from public pages. Mahjong Row & Co. is ON HOLD: MAHJMATCH fails at their cart, but nothing comes off our pages until Brad replies and she decides. (Tonight's removal was reversed live; Main restored config/fym-code-pct.json and marked MATCH-INBOX's line CANCELLED, 34820da.)

**Standing (Nov 4):** A YES IS A YES · BLOCKED IS NOT DROPPED · REVENUE WATCH · NO 'ASK ONCE' · SOCIAL 13 (nothing disappears from Planoly; past-dated drafts roll forward nightly) · partner launch → FB group post drafted the same day · payouts are CASH via PayPal (a few Venmo), only Maison Mahj is store credit · ShopMy pickup DAILY 9:02am · Chrome: no saved tabs · IG evergreen codes post = the ONE IG post with every code typed.

## Tomorrow's top priorities (Fri Nov 6), in order
Standing order: RESTOCK FIRST (rule c), then Google #1 (Tiffany Oct 29 11:03pm), then the newest ANSWERS (Mahjong Row hold, Sunday albums overdue, Juniper, FYM 1.15 follow-ups), then DESK 'Never-ending'. **Restock check (c): no album-set restock is dated Fri Nov 6** (Fri 10am CT: Mahjong Row 2 new tile sets, Bam Bird MCM Olive restock, Mahj Mood Playing for Keeps public preorder, Mahjong Moxie tiles 12pm CT: none has a live album). Next dated: Miss Mahjong acrylic racks Tue Nov 10; Virora Lilacée Nov 10; OMM Juniper + Lotus Cove Wed Nov 11 10am CT (Juniper album waits on her picks); Mahj Pit Christmas tiles + Confetti restock Wed Nov 11. The order is clear, so no "Set tomorrow's order" card.

1. **Google (Ops with Chrome, Main checks). OVERDUE 4 DAYS, first thing.** (a) Live site STILL says **Amanda Toppe 20%** (curl 9:45pm tonight: SEO title "Amanda Toppe Discount Code: 20% Off…", og description "Save 20% at Amanda Toppe Living…", hub ItemList "Amanda Toppe: 20% off with MAHJMATCH" + "Amanda Toppe (20% off with MAHJMATCH)"); Google's AI answer now QUOTES the 20%. It is 10% (Tiffany Nov 2). Fix every spot (page settings SEO title/description too) + config/hub-at-a-glance.html + assets/search/search-index.json + FYM brand note + config/fym-code-pct.json (still 20); curl-verify 0 "20%"; request indexing for both. (b) **Wren Mats page still "October 9, 2026"** and **OMM page box still "October 21, 2026"** (curl tonight): current verified date (standing authority), then indexing (OMM first: AI answer still doesn't name us). (c) Fri code report due (Mon/Wed/Fri) + morning report 7:13am; Google feedback on the wrong code form "MAHJMATCH10" shown for Middle & Main + Mahj Pit, and My Fair lost from the AI answer (My Fair page to tier 0 of indexing). (d) Mahjong Row: do NOT change the page/hub (hold); if Brad replies, Main brings it to her.
2. **Fri 11am ET partner drops (Main, then Matches & Catalog).** Store checks right after 10am CT: Mahjong Row Brunette Burl + Moody Tortoise (watch mahjongrowandco.com/products.json; add the product links to the Nov 4 group-post first comment WITHOUT pushing the code; FYM + gallery adds as products, code pill question on hold), Bam Bird MCM Olive restock, Mahj Mood Playing for Keeps public preorder (Mahj Mood code check first: unused codes expire after 4 months). HQ Today card launch-fri-nov6-drops tells her to reshare (Mahjong Row without the code). Watch Gmail (mahjmatchmaker@) for Brad's reply + any Mahjong Row payout (owed $2,589.65, docs/reports/payouts/mahjong-row-final-2026-11-05.md; check-in Nov 15).
3. **Sunday albums, OVERDUE, due TODAY Fri Nov 6 (Matches & Catalog).** Build Sunday Blues, Nature Walk, Plum Panda, Hummingbird album cards from her EXISTING yeses (Sunday Sets book WJT7jTYfXX45917UkEqKyq db votes), then ONE short page with ONLY mats added since her swipe (never the full 121-mat book again). **BUILT Fri Nov 6 ~7pm ET (agent): 180 DRAFT cards from her yeses (Nature Walk 42, Sunday Blues 56, Plum Panda 41, Hummingbird 41; assets/cards/<set>/ + manifest.json) + new-mats-only page (31 mats: NW 8, SB 7, PP 7, HB 9) at site/livepatch/sunday-albums-nov06/ (README + files.json), NOT published.** Next (Main/Matches): publish the page (Artifact, root = repo, files.json) and re-point HQ needs/sunday-moody-mats to it; her OK on PLM racks + card order; then album pages + holiday sections (#hummingbird un-hide; holiday yeses in manifests) + FYM m-lists per NEW-ALBUM-CHECKLIST. Mahjong Row mats on these cards: check the hold before live.
4. **Planoly (Main), rule d: 0 IG posts SCHEDULED Nov 6-12 (everything is a draft), and Wed + Thu drafts are past-dated.** (a) **Roll forward (SOCIAL 13), refused for the unattended run 2 nights running, so an attended chat does it:** Polo Club reel reminder 01a16476-febc + its FB reel 01a1a2b7-3d0e + Polo 7-frame story reminder 01a16477-0078 (dated Wed 11/4) → suggest Sat 11/7 17:00Z (set_post_group_schedule); New this week carousel 01a19e04-1f13 (undated) + its story 01a1a2b6-7c1e (Wed 11/4) and Dear Santa carousel 01a1a2b5-d469 + story 01a1a2b6-73c0 (Thu 11/5) get "📅 Planned: <day>" as the first caption line (auto-publish groups stay drafts). (b) **Story-caption lint, 4th day:** content_lint --planoly FAILs on all 8 story-draft captions (01a1a2b6-7c1e/-73c0/-7707/-7a67, IG + FB): add "Code MAHJMATCH · #MahjMatch" or exempt story captions in the lint. (c) Codes post 01a1a859-bcb8 length FAIL = her approved exception: add to the lint allow-list. Banked Retro Rattan reel 01a16477-0588 fails length + hashtag (fix before reuse). (d) FB Page targets missing on the Polo + Rudolph sticker-story reminders 01a16477-0078 and -03c8 (rule d: add them; their reels' FB versions are separate groups). Default kit: album-of-the-week kit from the Friday social prep task (storyboards for her yes).
5. **Match inbox (Matches & Catalog), rule e: ~91 dated lines older than Nov 4 have no DONE** (Oct 26: 23, Oct 27: 6, Oct 28-31: 28, Nov 1: 10, Nov 2: 5, Nov 3: 19). Most Nov 3 lines shipped in FYM 1.15 (Juniper, Lotus Cove, LBB ×10, Noli ×4, Bespoke ×2, Mahj Pit, Isla, Esme retired): mark DONE with proof (v115 build). Then the 1.15 leftovers + today's launch-watch adds: Mahj Pit RACKS (rule 6b white + navy review), Mahj Pit in the Mat Gallery, Mahj Mood Playing for Keeps mat + tiles, Mac + Miller 2 seconds, Fait à Main handle change, 32 older LBB listings, Spring Love + Shangri-La Santa Baby yeses. Ops TNT searches: Juniper, Bespoke Sunshine Glow, Glitter Glow Green, Middle & Main Clearwater Dockside.

## Handoffs (do first)
- **Matches & Catalog OWNS (BLOCKED, APPROVED: Tiffany YES Nov 6 5:30pm; she opens Chrome when home tonight): paste BOTH in one session: (1) Code Injection search lines @0b5e4270895b3fe6b92ef83aeea54979a2d2ac34 (site/livepatch/search/header-injection.html) and (2) Mat Gallery v6 block @ae6af119bc4dbcc4c75cec6b8e21ee06bad3fb94 on /mahjong-mats (README v6 steps). Search is built on the v6 rows, so never one without the other.** BOTH READY: gallery independent QA r3 PASSED (Nov 6 ~6am); search tests passed vs ae6af119 (the old v5 index issues QA saw are fixed by @0b5e4270).
- **Matches & Catalog OWNS (next time Chrome is open): paste Mat Gallery v6 on /mahjong-mats AFTER independent QA passes (QA r1 FAILED Nov 6 ~3am: duplicate photos, close-up photos, pastel-vs-brights colour mapping, 1 Christmas mat outside Holiday, Fait a Main links; fixes in progress, then re-QA)** (Nov 6 ~2am; Tiffany 1:22am gap: Dapper 2 not Retired, gallery 793 vs FYM 1,734). Block = site/livepatch/matgallery/matgallery-v6.html @ae6af119bc4dbcc4c75cec6b8e21ee06bad3fb94 (rows from data @ada16762), paste steps + verify string (`data-fym="v115"`, "1461 mats") in site/livepatch/matgallery/README.md "v6". 1,461 mats (28 duplicate photos merged, QA round 2), Dapper 2 + Esme Retired, 65 Sold out pills, partner links auto-apply the code (TdT / Mahjong Row hold / Squarespace stores untouched). From now on every FYM release rebuilds the gallery (site/livepatch/fym-preview-oct21/README.md 'EVERY FYM RELEASE'; gate [159b] FAILS --release until /mahjong-mats is stamped).
- **ALL CHATS: Mahjong Row & Co. is ON HOLD (Tiffany Nov 5 9:20pm).** The Main fork's 9:45pm "STILL TO DO" list (strip sca_ref + code pills from 9 album pages, 4 blog posts, homepage ticker, FYM cards, Mat Gallery rows) is CANCELLED until she decides. Main verified the reversal live ~10:30pm (34820da): brand page + hub identical to the originals (hub 39 brands, 'Updated November 4, 2026', 39-logo graphic), IG codes draft + FB group edits restored. Leave the Nov 4 group-post edits as Main left them. HQ needs/alert-revenue-mahjong-row-2026-11-06 archived as answered (hold). Main: when Brad replies, bring her the reply + options (pause line on our pages / swap to a referral link / remove) as ONE question.
- **Main: delete the stale 12 GB duplicate clone** /home/claude/tiffanybrie/mahjmatchmaker-data (Oct 22, clean, nothing unpushed) is HER call (safety check): ask at the top of the next Main reply (default: delete).
- **OPS + Matches & Catalog: The Mahjong Co. shop is empty** (1 product, sold out; our mat links 404; 0 orders in 9 days). Her yes/no is on HQ Today; then retire/hide their mats and fix /mahjong-co-discount-code links.
- ~~OPS: Amanda Toppe 10% everywhere + Wren + OMM dates~~ DONE by Main Nov 6 12:40am (live check PASS); indexing requests are in docs/OVERDUE.md.
- **Matches & Catalog: Sunday albums** (priority 3, due Fri).
- **Matches & Catalog: Lotus Cove swipe book (L8teRCj5w9ncskZYkwNEoZ) + every open book: show FULL mat names and brands** (Tiffany Nov 5, standing; book_gate [n]). Fix before she swipes; then HQ OMM card points to it.
- **Matches & Catalog: "mat matches" view proposal** (her Nov 5 12:47am ask: all match cards for one mat in one place): Claude proposed one data-driven view opened from search + gallery; RE-ASK her at the top of the next reply (default: build it after the Sunday albums).
- **Main: blog posts name tile sets that have albums but don't link them** (Tiffany Nov 5 12:29am). Live audit list: christmas-mahjong-sets (Heritage, Emerald), mahjong-buying-guide (Amara, Pearlescent, Heritage, Smith; 3 'tile match albums' links go to the index), mahjong-tile-set-details-to-know (Pearlescent, Heritage), most-versatile-mahjong-tiles (Amara, Glow Wild, Sierra, Smith, Talulah, Cypress Forest), my-favorite-yellow-orange (Pippa), my-favorite-mahjong-racks (Heritage), my-favorite-blue (Osler), my-favorite-green (Lagoon), most-versatile-mahjong-mats (Seabreeze, Papaya Spritz), pearlescent-tiles-heron (Sorbet). Every set named links its own album. Target Mon Nov 9.
- **Main: revenue-alert cards.** 11 per-brand alert cards were on HQ Today; tonight 9 info-only ones (no question for her) moved to This week. Main decides whether the morning report should fold info-only brand alerts into one HQ Money summary (HQ-CLEANUP Oct 27 rule 3: info-only = not a card) so they stop crowding HQ.
- **Main: OMM Juniper mentor presale** ends Fri 8am CT (live since Thu); FYM 1.15 has Juniper + Lotus Cove on the website. Public launch Wed Nov 11 10am CT: group post per the Papaya precedent.
- **Main: launch reel redo** (assets/social/fym-launch/redo-nov03/launch-reel-redo.mp4, 58s) stays near the TOP of HQ Today (her Nov 4 2:31pm); on "send me the launch reel": file + swap/pin steps in chat; Claude does the FB Page.
- **OPS: follow + favorite @mahjpit.co**, log in docs/IG-FAVORITES.md (new partner Nov 4).
- **OPS: copy flat renders to Dropbox /Mahj Matchmaker Albums/New releases/<brand>/**: Nov 3 + Nov 2 leftovers (OMM Lotus Cove + Juniper, 8 LBB Nov 3 mats, Bespoke Glitter Glow Green + Sunshine Glow, Britt Mills Isla, LBB Electric ZigZag + Christmas Lights) and Nov 5 (assets/launches/mahjmood-playing-for-keeps-mat/ + -tiles/, middleandmain-clearwater-dockside-…/, macandmiller-laissez-…-perfectly-imperfect/ + macandmiller-sweet-dreams-…-copy/) and Nov 6 (assets/launches/faitamain-le-bandana-pink-green/, Fait à Main; assets/launches/letsbebesties-pink-christmas-mahjong-mat/, Let's Be Besties; Splash Valentine mats assets/launches/splash-love-at-first-mahj-sweet-valentine-…/, splash-sweetness-youre-my-weakness-…/, splash-valentine-mahjong-mat-love-at-first-mahj-…/). Flat render first (01).
- **OPS: minimahjer.com store-wide / Black Friday code check** (from Nov 3; curl 429).
- **Main: GoAffPro order drop** follow-through in the REVENUE-WATCH (Mahj Mood recovering Thu night; Miss code doesn't apply to accessories: check our page says "tile sets" if that's their rule).
- **Matches & Catalog: brand-lock FYM sample for Bird & Bamboo (Emily)**, hosted embed only (docs/brand-lock/STATUS.md).
- **Matches & Catalog: FYM 1.12 follow-ups still open:** nightly stock check publish path; rack cut-out review for the 12 hidden racks; Mat Gallery rows (gallery_rows112.py); two-colour coordination ranking bonus. FYM 1.15 photo watch list (QA pass, could be better): Mahj Pit Sage Green Botanical (336px), Acid in the Library + Poppylicious, Turkey Dinner, Butterfly Dolly, Luna EK Studio 28 Etsy renders.
- **Main: launch + partner watch prompts**: check "wholesale customers only" (Nov 3) and draft the FB group post the same day for a partner launch. Add at next prompt edit.
- **Main: sales-check prompt fix** (ALL secomapp + goaffpro + backinstock emails, refunds on the refund date, tiffanybrie@ at /mail/u/1; repo clone step). Not applied.
- **Main: "close leftover finished Claude tab groups at start"** in every Chrome task TAB RULE (Oct 30). Not done.
- **Main: mat-edit-alert build step** in launch watch trig_01S2VsjwznnHev1uUbYmEwJq (Oct 30; docs/MAT-EDIT-ALERT.md). Not done.
- **Main: duplicate catch-up tasks** trig_019StaM8LkmrxGKtK7xhXang + trig_013ZpyRxFivSKPoYTgSvVBU6: pausing one is her call (HQ rules-audit-2026-10-30).
- **Main: config/pinterest/queue.json** last updated Nov 4 (16 scheduled) while Planoly has 3-4/day through Nov 30: resync at the next autopin run.
- **OPS (standing): HQ ShopMy tab inbox** (db `shopmy`, status new) at the start of every Ops reply.
- **Partner feedback watch** trig_01RKw9eUwTYPo39gbYHb65gh runs daily through Nov 10 (0 new Nov 5).

## In progress
- [Main] PEACE LOVE -> LEVEL 2 PUSH (Tiffany Nov 5): need $5K referred sales in one month (Oct ~ $3.6K). Next step: plan (PLM page refresh + indexing, oak rack shelf/collage, PLM racks into more albums/FYM rack picks, holiday hats/rack pets in gift posts); track PLM referred sales MTD daily in the morning report.

| Item | Owner | Next step | Target |
|---|---|---|---|
| Google: Amanda Toppe 10%, Wren + OMM dates, indexing (My Fair tier 0, OMM, Wren, Amanda Toppe, hub), Fri code report, wrong-form MAHJMATCH10 feedback | Ops + Main + tasks | Priority 1. | Fri Nov 6 |
| Fri partner drops (Mahjong Row ×2, Bam Bird MCM Olive, Mahj Mood PFK) | Main → Matches & Catalog | Priority 2: store checks after 10am CT, group-post links, FYM adds. | Fri Nov 6 |
| Mahjong Row hold (Brad's reply, payout $2,589.65) | Main | Watch Gmail; bring her the reply as one question. No page changes. | Check-in Nov 15 |
| Sunday albums ×4 from existing yeses + new-mats-only page | Matches & Catalog | Priority 3. | Fri Nov 6 (overdue) |
| This week's IG posts (Planoly drafts; roll-forward) | Main | Priority 4. | Fri Nov 6 |
| Match inbox close-out after 1.15 + launch-watch adds | Matches & Catalog | Priority 5. | Fri Nov 6 |
| FYM 1.15 leftovers: Mahj Pit racks (6b) + Mat Gallery, Mahj Mood PFK, Mac + Miller seconds | Matches & Catalog | Next build (1.16): gate + independent QA + both places + pin + snapshot. | Mon Nov 9 |
| Juniper album (round 2, 33 mats) | Tiffany → Matches & Catalog | Full set BUILT Nov 6 (agent): cover, wheel + colour theory, 47 face cutouts + faces pick page, Her best features DRAFT, dating profile, 7-slide intro, 33 DRAFT match cards: site/livepatch/juniper-album-nov06/README.md. Waiting on her: 4 faces (pick page), card order/cuts, racks OK, pronoun ('her' in drafts). Then album page live with the launch. | Mon Nov 9 (launch Nov 11) |
| Lotus Cove swipe book | Matches & Catalog → Tiffany | Fix full names (book_gate [n]), then HQ points her to it. | Sat Nov 7 |
| Playing for Keeps mat swipe book (JTgtEfAAdS6qrDJUhvPB3n) | Tiffany | Optional, before Valentine's content (HQ Albums "Needs your yes"). | When she likes |
| Work With v3 + Brands form | Tiffany yes → Ops | Her yes on HQ Today; README says nothing goes live until she has seen it. | On her yes |
| IG evergreen codes post (Planoly 01a1a859-bcb8) | Tiffany taps Post / Main | After it posts: drag to the bottom of the grid; Claude keeps the caption current. | When she posts |
| Holiday new-albums email | Main | Squarespace draft; her final read. (Slipped from Thu.) | Mon Nov 9 |
| 7 quick-call defaults + Nov 2 site check rebuild | Ops + Main | Apply defaults; rebuild site check from HQ log into git. (Slipped from Thu.) | Mon Nov 9 |
| Blog album links | Main | See Handoffs. | Mon Nov 9 |
| Payout reconcile pass 2 | Main (Chrome) | Real payout terms per program → config/payout-terms.json; re-split Oct; HQ Money "Payouts". | Mon Nov 9 |
| UpPromote accounts → mahjmatchmaker@ | Tiffany (Mahj Squad no reply yet) / Main | Screenshots before each switch; Bird & Bamboo next. | This week |
| Holiday colour cards (Tinselle ×2, Dec 1994, PLM Spirit + Nutcracker) | Matches & Catalog | Not started (was due Oct 31). | Mon Nov 9 |
| My Fair Mahjong Style of Your Life (#1 album) | Matches & Catalog | Colour card + TNT, then swipe book. | Mon Nov 9 |
| Holiday album covers page update | Matches & Catalog | Late picks are live; covers next. | Fri Nov 6 |
| Larkspur hearts into 27 tile albums | Matches & Catalog → Ops | Paste album by album (0 of 27). | Tue Nov 10 |
| December 1994 redo (her RTS notes) | Matches & Catalog | After holiday colour cards. | Tue Nov 10 |
| Hummingbird holiday section (hidden) | Matches & Catalog | Un-hide with the Hummingbird album. | With Sunday albums |
| Sunday Sets TNT rec leftovers | Matches & Catalog | docs/research/sunday-sets-colorcards-tnt-oct29.md. | Fri Nov 6 |
| Holiday reels redo (Nutcracker/FYM reel with Table view) | Main | v5 standard; storyboard first. | Mon Nov 9 |
| Bam Bird Deco trio (Indigo first) | Matches & Catalog | Colour cards ×3, then books. | Week of Nov 9 |
| Brand-lock sample for Bird & Bamboo | Matches & Catalog | Hosted embed only. | Week of Nov 9 |
| Affiliate applications (apply kit) | Tiffany submits / Main | Kit doc 00h; HQ apply-kit-oct31. | This week |
| FB group weekly Claude Doc | Main | https://claude.ai/artifact/54ovPaB6BQU78ztjUgQSbe; add the Nov 4 posts. (Slipped from Thu.) | Fri Nov 6 |
| Tortoise rack piece (her Oct 28) | Main | Scope + storyboard; gift-guide tie-in. | Mon Nov 9 |
| Discount links not converted (Britt Mills, Mahjong Register, YMI, RMS, Hip Hip, Wren/Soirée/Amanda Toppe) | Main | builder/fym_fix_oct21/discount_check_oct21.json. | Mon Nov 9 |
| Amazon mats into gallery + FYM | Ops → Matches & Catalog | Her pick (1, HQ This week). | On her pick |
| ShopMy holiday leftovers | Main → Ops | ShopMy (not MAHJMATCH) for Charleston Mahjong Club + Bamlet's in holiday posts. | Mon Nov 9 |
| Fait à Main code | Main | MAHJMATCH still not applicable at cart. | Watch |

## Blocked, approved (raise at the top of every attended reply until done)
- (Nov 6, Main) Mahjong Row & Co. OUT (Tiffany 1:19 + 1:33pm, approved, no more asks): Squarespace pages + FB group list per site/livepatch/mahjong-row-out-nov06/README.md (BLOCKED: Chrome not connected at 1:40pm; again offline ~5:40pm, nothing started or half-saved; exact steps in the OVERDUE line). Matches & Catalog: FYM v116 = run builder/fym_fix_nov06/mr_out.py + gate [160] + QA + publish both copies. Parked copy: archive/mahjong-row-parked-2026-11-06. Done = live_codes_check PASS.
- **Planoly roll-forward** (Main): the unattended desk run was refused `set_post_group_schedule` again tonight (2nd night). Priority 4a.
- **IG EVERGREEN CODES POST** (Main, her plan Nov 4 3:55pm): draft in Planoly 01a1a859-bcb8 (caption has the Mahjong Row line restored, bf1e1b7); she taps Post. NOT on the FB Page.
- **PAYOUT RECONCILE PASS 2** (Main): needs PayPal + each dashboard signed in. Kathrine Zell $3.15 Oct 15: Tiffany checking her email. Peace Love $402.88 gift-card payout = their Level 1 tier (store credit only; cash starts at Level 2 = $5K referred sales/month), NOT a GoAffPro setting (Main found Nov 5).
- **Dashboards signed out: Bird & Bamboo UpPromote, My Fair, OMM, Mini Mahjer** (blocks amounts + revenue watch): her sign-in (HQ Today card #1). Marketplace + GoAffPro are signed in again.
- **Mahjong Row product links** (Main): edit the group-post comment the moment pages exist (Fri 10am CT), no code.
- DONE today: FYM tracking TRK_URL live in all 3 places (1.15, 10:25am; beacon rows land in the sheet; website QA PASS ~9:40pm). Site search Code Injection on 98e58057.

## Waiting on Tiffany (only things she can answer now)
**On HQ Today, in this order (5):**
1. **Google: sign back in to Bird & Bamboo, My Fair, OMM and Mini Mahjer dashboards** (1 min each).
2. **Launch reel redo: watch it** ("send me the launch reel").
3. **Fri 11am ET drops: reshare Mahjong Row (without the code), Bam Bird MCM Olive, Mahj Mood.**
4. **Work With page v3 + Brands form: yes / wait / changes.**
5. **The Mahjong Co.: do you know if they closed or moved?** (yes/no)

**On HQ This week:** Sweet Jojo W-9; Juniper album picks (by Mon Nov 9); Mahj Squad: is the code still assigned after the account switch?; unknown amounts Nov 4-5; My Fair Black Friday "shop through our link" yes/no; 2 quick FYM checks + Holy Mahj; affiliate apply kit; 1 hidden FYM photo (Grace Peacock); ShopMy quick calls + 2 stray links; This week's posts in Planoly; CMC Cabana Club sneak peek; 9 info-only brand revenue alerts; Sunday albums (Claude's job, no ask).

**Asked in chat, not yet answered: the owning chat RE-ASKS at the top of every reply until answered, with its default:**
- Main: **delete the stale 12 GB clone?** (Nov 5 9:40pm; default delete); **separate Google/revenue chat?** (Nov 4; default: keep it in Main); Malachite how-to reel v2 OK + day; FB group B&B racks wording.
- Matches & Catalog: **"mat matches" view** (Nov 5 12:47am; default build after Sunday albums); Lagoon + Mulberry splits; Bam Bird Classic Tortoise match pick; Sunday Rattan: is the 'new' one the Blue Rattan; Fruit Stand rack-edge (default a); brand-lock pricing (undecided, don't push).
- Mahjong Row: nothing to ask her until Brad replies.

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
- **Mahjong Row & Co. future** (Nov 5): Brad may offer one-time referral links instead of codes; her call once he replies (Main brings it). Their fall album and new Foxhill Plaid / Hawthorne Floral mats + Oxblood / Cognac Burl racks wait on that.
- **Charleston Mahjong Club Cabana Club full-size tiles** 'arriving any day now' (partner watch Nov 5); giveaway ends Mon Nov 9 8pm ET; HQ sneak card. Small album idea already in Later (Oct 28).
- **My Fair Mahjong 4 new Confetti acrylic rack colours** (launch watch Nov 5): accessory, record only; FYM rack lists when there's room.
- **Mahj Mood Playing for Keeps tiles** ($390, Valentine set, ships January): not an album now; the PFK mat swipe book is optional before Valentine's content (Nov 5).
- **Per-brand IG code posts / reels**: not now (her Nov 4 3:55pm pick = one evergreen post); revisit if the evergreen post doesn't show in Google (Nov 4).
- **Tiffany's Takes editor** (DkRn8W5qaMBxHfqqeJVE8V) data is from Oct 10 (37 albums): refresh with Brownstone + holiday albums when she wants to write takes (offered Nov 4 1:45pm).
- **Maison Mahj House Line No. 1** public preorder ($595, Nov 4), **Bougie Mahjong neoprene versions** of 5 mats ($80/$90, non-partner), **My Fair Mega Swirl Dice** ($40, accessory), **Splash of Color tile set** ($285), **Anders Ruff 'new product' reel tease**: record only (watches Nov 4).
- **Mahjong Moxie Moxie Tiles** (first tile set) LIVE Fri Nov 6 12pm CT: non-partner except Duck Camp/Heron Landing mats; record only unless she says.
- **Clean up 52 legacy caption lint warnings** (still 52 Nov 5) (config/social/content_lint_baseline.json; mostly missing #MahjMatch, '(affiliate)', 2 TdT captions) (rules audit E9, Oct 30). Also 78 legacy FAILs (length 42, naming 36) in banked Season 2 captions: same kinds as yesterday, nothing new.
- **FYM Shuffle** idea for 1.15 (Matches & Catalog, Nov 3).
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
- **Mahjong Register** Crystal Palace acrylic racks + Solid Wood racks (launch watch Oct 31): FYM rack lists when Matches & Catalog has room.
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

## Daily operations (Thu Nov 5)
| Operation | Done today? | Notes |
|---|---|---|
| Affiliate tracking (Money tab) | ✅ Done | Sales check 2:11pm; morning report reconciled Thu to 9pm: 11 orders / $168.16 known (3 no amount: My Fair ×2, OMM), 92% of last Thursday's orders, no alarm. Mahjong Row record: owed $2,589.65 (dashboard Inactive). Midnight close-out still to run. |
| Google code report | ⏭ Not due | Mon/Wed/Fri: next Fri Nov 6. |
| Morning Google report | ✅ Twice | Thu report ran late (10:07am catch-up; 24/39). Fri's ran early Thu 8:40pm: 36/39 AI answers (desktop at night, partly method); lost My Fair; OMM + Soirée not named; Amanda Toppe 20% quoted. 7:13am run refreshes it. |
| Verified dates (weekly, Mondays) | ❌ Stale pages | Not due Thu, but Wren "October 9" + OMM "October 21" still live (priority 1b). |
| Codes post (Mondays) | ⏭ Not due | Next Mon Nov 9 (FB group, typed out; use the current hub list: Mahjong Row on hold). IG evergreen codes draft waits on her tap. |
| Pinterest queue health | ✅ OK | Planoly Pinterest: 3-4 pins/day scheduled Nov 6 → Nov 30, 0 errors. queue.json last updated Nov 4 (handoff). |
| Indexing | ✅ Done | 11 requested 12:35pm (Mahj Pit page + hub + changed brand pages). Waiting: Wren + OMM (after the date fixes), Amanda Toppe (after 10% fix), My Fair (tier 0). /juniper-mahjong-tile-matches 404 (album not built yet: expected). |
| Planoly next-7-days (IG + FB Page) | ❌ Not covered | 0 IG posts SCHEDULED Nov 6-12 (7 drafts with dates + the codes post, none scheduled); Wed + Thu drafts past-dated and not rolled (permission refused again). Planoly lint 19 FAIL, same as yesterday (16 story captions, 2 banked Retro Rattan, 1 codes-post length). FB targets: all feed groups have one; codes post none by rule; Polo + Rudolph sticker-story reminders none. Priority 4. |
| New albums (last 7 days) (f) | ✅ All checks | Brownstone Bloom (live Nov 1): /mahjong-tile-matches ✅, /links latest ✅, Pinterest queue ✅ (54 refs), indexing ✅, colour + brand pages ✅ (Nov 3). No new album went live Nov 5. |
| Repo caption lint (g) | ⚠️ Legacy only | 78 FAIL (banked Season 2), 52 legacy WARN. Same kinds as yesterday, nothing new. |
| Restock first (c) | ✅ Checked | No album-set restock dated Fri. |
| Match inbox (e) | ⚠️ ~91 old open | Priority 5. |
| Launch + partner watch | ✅ Done | Launch watch 9:10am (1 new) + 6:05pm (5 new: PFK mat + tiles, Clearwater Dockside, 2 Mac + Miller seconds); partner watch 9:45am, 1:41pm, 6:35pm (Miss racks 11/10, Bam! bag restock, Mahj Pit Christmas tiles + Confetti restock 11/11, CMC Cabana Club). ShopMy mat check: nothing new. |
| FYM + partner feedback | ✅ Done | 0 new (2:21pm). |
| FYM releases | ✅ 1.15 LIVE | All 3 places 10:25am (tracking ON, Mahj Pit, Juniper, Lotus Cove, Noli, LBB, Bespoke, 33 Etsy, Isla, Santa Baby m-lists, Esme retired); website QA PASS ~9:40pm. Snapshot refreshed (1248d48). |
| Social posted today | ❌ None recorded | No IG post went out (all Planoly drafts); no FB group post recorded in git/HQ today (only the Main fork's Mahjong Row edits, reversed). |
| HQ + Ready to Ship cleanup | ✅ Done | Morning 7:04am (15 → 14), sweeps 9:47am / 1:47pm / 7:47pm; this desk run 29 open → 27, Today 12 → 5. RTS: no new answers since Oct 30. |

## Never-ending projects
- **Find Your Mat-ch™ app** (artifact 6epA9HuEdT32zUp79Qv3kd; public **Version 1.15** = v115 with usage tracking ON (live artifact Version 113; website pin fym-v115 @57f0b4e6, page-block @cc0de626 on /find-your-match + /find-your-mat-ch-preview; live Nov 5 10:25am, website QA PASS Nov 5 ~9:40pm): gate + independent QA before every publish (QA loads the WEBSITE copy as live: 0 broken images, gate [115]); artifact AND website copy AND README 0a pin in the same step; +0.1 version label (docs/FYM-VERSIONS.md); her feedback the same day with a gate check; when a publish/paste fails, MESSAGE HER right away. Artifact file budget: run builder/fym_artifact_fit.py and publish ONCE. Every nav/header change: screenshot live at 1280, 1440 and 390 with the phone menu OPEN. New partner catalog in FYM within 24h of its inbox line (gate [114]). Refresh config/fym-mats-snapshot.json after every publish.
- **Match inbox** (docs/MATCH-INBOX.md): any chat writes match/catalog misses there the same turn; Matches & Catalog marks DONE when shipped.
- **Google / MAHJMATCH in AI answers (her #1)**: AI Overview + AI Mode per partner, code report (Mon/Wed/Fri), daily morning report, indexing (brand pages first), sitemap health, weekly verified dates + hub date, weekly codes post (FB GROUP only typed out; IG/FB Page = logos graphic + short caption), alarm on any lost citation.
- **Albums**: order (her Oct 28 3:31pm): MFM Style of Your Life → Bam Bird Deco trio (Indigo first) → Sunday Blues → Sunday Nature Walk → Middle & Main Peach and Pine, Mac + Miller; Mahjong Row fall + OMM green set (Juniper) jump the line; a known restock goes FIRST. Doc 86b (colour card FIRST), book_gate.py, PICKING-RULES.md, NEW-ALBUM-CHECKLIST.md (incl. the new-albums email).
- **Holiday (Merry Mahjong)**: intro reel posted Nov 3; next = late picks into holiday albums, holiday albums + FYM holiday group posts, new-albums email; docs/MERRY-MAHJONG-BRIEF.md + docs/plans/holiday-calendar-nov-dec.md; promote FIND YOUR MAT-CH, not albums (her Oct 30); any FYM social shows the tool working; storyboard before render; song shortlist on every reel; FYM-REEL-RULES 23-41.
- **New products**: hq/newproducts → gallery + FYM colour-tagged → weekly roundup. Never albums. New-mat social = "Match up <mat> in Find Your Mat-ch", never ahead of the brand; wholesale-only/unannounced = confidential.
- **Social** (docs/SOCIAL-SYSTEM.md, ~2 hrs/week of her time): every planned post as a Planoly DRAFT on its day (final media, lint PASS, Tag people, FB Page target, story version); she reviews in Planoly; FB Page target on every IG group; every slide to stories; brand tags + collabs; restocks/launches SAME DAY or never; ≥4 IG posts in every next-7-days window.
- **Facebook group**: community, never ads; weekly codes post (doc 94); weekly Claude Doc of planned posts; @everyone at most ~once a week.
- **Partner share graphics**: one per brand + our MAHJMATCH version (39 logos as of Mahj Pit, Nov 4: assets/hub/partner-brands-2026-11-04.jpg; a 38-logo version without Mahjong Row exists, assets/hub/partner-brands-2026-11-05.jpg, NOT in use: Mahjong Row on hold).
- **Pinterest**: queue within the pace rule; evergreen pins of our own images.
- **Affiliates + money**: sales checks 2:04pm + 12:04am, reconcile every referral email (both inboxes), refunds on the refund date, spike AND drop checks; onboarding new partners (page, hub, logos, FYM within 24h, indexing, IG follow/favorite); affiliate applications (kit doc 00h).
- **Mat Gallery + colour system**: sort rule, holiday rule, partner-only gate (plus her Oct 31 non-partner picks), shop-by-colour partners first (Oct 31); gallery row for every visible FYM mat (gate [90]).
- **ShopMy + Amazon storefronts**: square-safe covers, aerial mat photos, HQ ShopMy tab intake, weekly ShopMy mats check (Tue).
- **HQ hygiene**: Today ≤5, answered = gone, event passed = gone, timestamps on every card, inline previews; ANSWERS.md before asking anything; no answer is not a no.

## Log of this rewrite (Thu Nov 5 night)
- **Done today:** FYM 1.15 LIVE in all 3 places with usage tracking (approved Oct 17, finally live) + independent website QA PASS; site search fix live (Code Injection 98e58057); Juniper round 2 (33 mats, her notes) + book_gate [n] full names; gate [158] extreme aspect ratios; 2 morning reports (Thu catch-up 24/39; Fri early 36/39); revenue watch per brand (11 alerts); 11 pages indexed; 2 launch watches + 3 partner watches + ShopMy check; Mahjong Row deactivation handled: record of owed $2,589.65, Tiffany's reply sent by her; the removal of the code was REVERSED on her word (live pages restored; new rule: a partner pausing = ask her first).
- **Found mid-way and given a home:** Mahjong Row leftovers list from the Main fork → CANCELLED (hold; Main's 34820da reversal verified live); Amanda Toppe 20% (4th day, Google quotes it) + Wren/OMM dates → priority 1; Sunday albums (due Fri, nothing committed) → priority 3; Planoly roll-forward refused 2nd night + story lint 4th day → priority 4 + Blocked; Thu's holiday email, Work With live, 7 quick-call defaults, FB group Claude Doc all slipped → In progress with new dates; 1.15 photo watch list + Mahj Pit racks → handoffs; stale 12 GB clone → Main re-asks; HQ Today was 12 cards → 5.
- **HQ:** archived alert-revenue-mahjong-row-2026-11-06 (answered: hold) and amounts-2026-11-05 (merged into amounts-2026-11-04); 9 info-only revenue alerts + Mahj Squad + Juniper + social-week + amounts → This week; Google card rewritten (4 dashboards); Fri drops card → Today. Albums: Juniper detail = round 2 (33 mats), Larkspur + December 1994 targets → Tue Nov 10, Mahjong Row fall album ON HOLD. "Yours" = 2 (Juniper picks page, PFK mat swipe book; RTS NOW has 0 open).
- HQ smoke test at 390px not run tonight (data-only change, no page HTML changed).

See CLAUDE.md.

- MAIN (Nov 6, ~2:30am): Rudolph mood-board reel, Canva DAHaHg27cPw, has her 2:10am notes applied on all 8 pages: no writing, no arrows, the white rack bigger and overlapping the mat, and the lamp, dice dish and tablecloth scaled up as the stars. UNSAVED (transaction 8602396589085057806, NOT committed). Next step: she glances at it when she has time, nothing for her to direct. On her OK: commit, export MP4, replace the Rudolph Planoly drafts, then do Polo and Rattan the same way. If it's still not right, stop mood-board reels for this season (her call, Nov 6 2:10am).

- OPS: paste FYM v116 pin on Squarespace + gallery rebuild (rule 0). [Nov 6 ~7pm, independent QA agent] FYM v116 r1 (Version 1.16: Mahjong Row parked + Mahjong Co. mats hidden) independent QA PASSED (390 + 1440, both doors, colour switch/clear, zoom persists, card + share, MAHJMATCH on all 3,347 partner combos, contact sheets of 283 tiles / 1,219 mats / 292 racks; website copy also tested inside the page-block on the live preview page). Live artifact 6epA9HuEdT32zUp79Qv3kd PUBLISHED (Version 114 = 1.16). README 0a pin + page-block IDX -> site-app/fym-v116 @80d4f0b8. NEXT (needs Chrome): paste site/livepatch/fym-preview-oct21/page-block.html (pin = the commit carrying the Nov 6 README line) on /find-your-match + /find-your-mat-ch-preview, curl-verify fym-v116; then paste the staged Mat Gallery block (matgallery-v6.html @ba6479d0, rows @8ed532e9; check no /discount/MAHJMATCH on the 9 Mahjong Row gallery mats); fym_snapshot.py refresh. NOTE: a superset r2 (@fdcc1868 on fym-site-preview: dead shop links, auto-apply links, colour fixes, thin-album hearts) exists and has NOT had independent QA; r1 still shows 15 dead OMM/TdT/MFM shop links (gate [162], pre-existing in 1.15). r2 needs its own QA + publish (Matches & Catalog).
- Matches & Catalog / Main (Nov 6 ~7:15pm): FYM 1.16 r2 = the FULL 1.16 Main asked for (r1 live + auto-apply links, 17 dead links no shop button + gate [162], colour fixes, Juniper pair mat top 3, Mahj Pit White Beech rack, 41 thin-album hearts, inbox fixes) is BUILT, gate PASS, NOT published. Needs a new label (r1 took 'Version 1.16'), then independent QA. Website copy fym-site-preview @fdcc1868; Mat Gallery matgallery-v6.html stamped v116 from r2 (staged, not pasted). Details: builder/fym_fix_nov06/RELEASE-v116.md top.
