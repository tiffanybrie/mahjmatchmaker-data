# The Desk
Rewritten nightly by the end-of-day desk cleanup (9:23pm ET). The morning HQ cleanup (6:47am ET) reads it. Rules: CLAUDE.md ("THE DESK"), docs/CHATS.md (which chat owns what). During the day, when an agent stops, Chrome drops or a QA stalls, add the item here right away with its next step.

**Last rewrite:** Fri Nov 6, 2026, ~9:55pm ET (desk cleanup run, cloud, no computer linked). Covers the 169 commits of Nov 6 ET (57ca12f … 66953b1), docs/ANSWERS.md (Nov 6 lines), docs/OVERDUE.md, docs/MATCH-INBOX.md, Planoly (IG workspace 019fc27c…: 37 drafts + 1 stale Oct 21 reminder, export docs/social/planoly-exports/ig-2026-11-06-desk.json; Pinterest 019fc27b…: pins scheduled Nov 7-8 on the first page, 10 new FYM pairing pin drafts), HQ needs (15 open → 14; Today 3 → 5) / hq/albums / hq/now / hq/priorities / log, Ready to Ship (no new answers since Oct 30, per the 7:47pm sweep), config/release-calendar.json, content_lint (repo + Planoly IG export), live_codes_check, gallery_sync_check, curl checks (/mahjong-tile-matches, /links).

**Owners (three chats, Oct 22):** Main (Opus) = social/Planoly, site pages, email, HQ/DESK, decisions, Google + SEO, money. Matches & Catalog (Opus) = Find Your Mat-ch, albums, gallery, catalog, search index. Ops (Sonnet) = the ONLY Chrome driver: Squarespace pastes, uploads, IG follows/checks.

**Repo note:** `partner-catalogs-sqsp` is ~9 GB. A plain fetch into the old /home/claude/mahjmatchmaker-data checkout hangs (it sat on detached main). Working recipe tonight: fresh `git clone --depth 50 --filter=blob:limit=2m --single-branch -b partner-catalogs-sqsp` (~8 min, in the background), then `git fetch --shallow-since=<date>` for more history.

**PARTNER SEND GATE (Oct 27, standing):** before scheduling ANY partner email or graphics drop, run `python3 scripts/partner_send_check.py`; it must exit 0.

**NEW TODAY (Nov 6, ANSWERS):** Mahjong Row & Co. is OUT (her 1:19 + 1:33pm; album match cards, Halloween blog and 9 gallery mats stay, no code). Sales come from the CODES, never explain a day by FYM/launch buzz (5:48pm). Name AI OVERVIEW vs AI MODE every time, never "Google's AI answer" (5:11pm). Chrome on = do the Chrome work now (5:11pm). Mood-board/table reels DROPPED; social just runs: standing yes to likes/reshares/comments and to auto-posting already-approved FINAL formats, never album cards before the album + promo plan are final (4:11-4:12pm). Spotlight is THE FYM reel style (FYM-REEL-RULES #39). Reel music = cheeky love songs from the Instagram catalog, never repeat a song (docs/social/songs-used.md). Subscribe mahjmatchmaker@ to every partner newsletter (standing). Bing: yes. Payout dates for every brand (Payout Tracker Q3r6wMhYLqoyJSYnfKmtH2).

**Standing (Nov 4):** A YES IS A YES · BLOCKED IS NOT DROPPED · REVENUE WATCH · NO 'ASK ONCE' · SOCIAL 13 (nothing disappears from Planoly; past-dated drafts roll forward nightly) · partner launch → FB group post drafted the same day · payouts are CASH via PayPal (Bam Bird = bank transfer), only Maison Mahj is store credit (PLM Level 1 = gift card) · ShopMy pickup DAILY 9:02am · Chrome: no saved tabs · IG evergreen codes post = the ONE IG post with every code typed.

## Tomorrow's top priorities (Sat Nov 7), in order
Standing order: RESTOCK FIRST (rule c), then Google #1 (Tiffany Oct 29 11:03pm), then the newest ANSWERS (money + Juniper first, social system reset, Sunday albums overdue), then DESK 'Never-ending'. **Restock check (c): no restock or launch dated Sat Nov 7 is for an album set** (Sat: Virora bags 5pm PT, accessory, record only). Next dated: Virora Lilacée restock + Miss Mahjong acrylic racks Tue Nov 10 (no albums); **OMM Juniper + Lotus Cove Wed Nov 11 10am CT = album set (Juniper), owner Matches & Catalog, album live with the launch**; Mahj Pit Christmas tiles + Confetti restock Wed Nov 11 (no albums); Mahjong Row Sloane/Foxhill Nov 13 (brand OUT). The order is clear, so no "Set tomorrow's order" card.

1. **Google + money (Main; Ops for Chrome steps). First thing.** (a) **Friday code report did NOT run** (Mon/Wed/Fri; last report in the project = 99i Nov 4) and Fri's 7:13am morning report was never refreshed (only the early Thu 8:40pm run exists, docs/reports/google-revenue/2026-11-06.md). The Sat morning report re-runs both, MOBILE, and reports AI OVERVIEW and AI MODE separately per brand; her 5:16pm check found MAHJMATCH missing in AI Overview for Miss Mahjong, Bam Bird, Bespoke, PLM: no single-snapshot claims. OMM still not named anywhere (Squarespace AI Visibility too). (b) **Nov 6 sales close-out** (OVERDUE): fill My Fair ×3, Mini Mahjer, Bam Bird amounts; re-sweep both inboxes; find why the 10am/2pm sweeps didn't run and fix the schedule. Rule: Money tab never sits at 0 sales by afternoon without telling her. (c) Bing Webmaster Tools import (her yes 5:29pm) + AI-assistant code check (OVERDUE) next time Chrome is on. (d) Dashboards signed out (B&B UpPromote, My Fair, OMM, Mini Mahjer): her HQ Today card #1.
2. **Chrome pastes, all APPROVED, all staged + QA'd (Ops / Matches & Catalog the moment Chrome is on).** `live_codes_check` = **FAIL (61), every line is Mahjong Row still on live pages** (brand pages + hub + album links): run site/livepatch/mahjong-row-out-nov06/README.md + homepage order (FYM > Holiday > albums > blog) + FB group comment; done = PASS. `gallery_sync_check` = **FAIL (live gallery has no data-fym stamp)**: paste Mat Gallery block @ba6479d0 (v116) + Code Injection search @2bd4c475 TOGETHER (paired QA PASSED), or the v117 pair once 1.17 passes QA (see #5; never one without the other). **/find-your-mat-ch-preview still fym-v115**: re-paste page-block @1062af2a (Chrome dropped mid-save ~8:45pm). Partner newsletter signups (docs/PARTNER-NEWSLETTERS.md, CMC first).
3. **Planoly (Main), rule d: 0 IG posts SCHEDULED in the next 7 days** (the only "scheduled" IG item is the stale Oct 21 Papaya story reminder 01a16052-2828). Nov 7-8 and Mon-Sun Nov 9-15 are all DRAFTS (13 groups from the Friday prep + Holly Jolly / Rudolph It's a mat-ch + 3 easy-content samples). Default kit = these drafts + the album-of-the-week kit. (a) **Roll-forward half done tonight** (update_post allowed 3 of 8, permission check refused 5): DONE = New this week FB post 01a19e04-1f24 + FB story 01a1a2b6-7c33 ("📅 Planned: Sat 11/7"), Dear Santa IG post 01a1a2b5-d473 ("📅 Planned: Sun 11/8"). STILL TO DO, same text: IG 01a19e04-1f1c (New this week, Sat 11/7), FB 01a1a2b5-d47e (Dear Santa, Sun 11/8), stories 01a1a2b6-7c27 (Sat 11/7), 01a1a2b6-73c7 + -73cc (Sun 11/8), each story caption ending "Code MAHJMATCH · #MahjMatch" (clears the story lint). (b) Polo/Rudolph reel + story reminders dated Nov 4 + Nov 6 (01a16476-febc, 01a1a2b7-3d0e, 01a16477-0078, 01a16477-0208, 01a1a2b7-3eb3, 01a16477-03c8): mood-board reels are DROPPED (her 4:11pm): ask her in one line "remove the dropped Rudolph/Polo/Rattan drafts from Planoly? (default: yes, archive record in docs/planoly-archive)"; do NOT roll them. (c) Remove or reschedule the stale Oct 21 Papaya story reminder (her call: it's a reminder that already fired). (d) Juniper x Palm Royale "It's a mat-ch!" Wed 11/11 stays a draft until the album is final (her 4:12pm limit). (e) After her yes on the 3 easy-content samples: switch the Fri social-prep task to 1 auto FYM post/day (OVERDUE line).
4. **Sunday albums + Juniper (Matches & Catalog; Tiffany picks).** Sunday: 180 draft cards + the 31-new-mats page are PUBLISHED for her (https://claude.ai/artifact/7tUcQUKDhS9yUntFLNUd1i, HQ Today); on her picks: 4 album pages + holiday sections (#hummingbird un-hide) + FYM m-lists per NEW-ALBUM-CHECKLIST, no Mahjong Row mats with a code. Juniper: round-3 notes applied offline (@95ec1edf, CHANGES-round3.md); she picks 4 faces + cuts (said "tonight"); album live with the Wed Nov 11 10am CT launch + group post (Papaya precedent).
5. **Match inbox + FYM 1.17 (Matches & Catalog), rule e: 11 lines older than 2 days with no DONE** (Oct 1 ×1, Oct 27 ×2, Oct 29 ×5, Oct 30 ×2, Oct 31 ×1: non-partner "No code available" line, two-colour ranking, partners-first + brand-logo default order (Oct 29 ×5, check her OK), Gray Malin Getaway Dogs close-up, YMI Ivory Stripes merge, v109 re-QA hides) + the Nov 5 32 LBB listings. Mark DONE with proof or build them into 1.18. **FYM 1.17 r2: gate PASS (66953b1) but NO independent QA recorded**: run it (390 + 1440, both doors, contact sheets), then publish all three places; the 84 locked colour changes wait on her (Main asks, one line, default: apply).

## Handoffs (do first)
- **Main: OMM Pearlescent is back on ohmymahjong.com (Sat Nov 7, republished 9:14am CT, $475, tagged 'retiring soon'; ALBUM set, 40 of her matches in FYM).** Frames for her review (NOT posted): assets/social/restock-pearlescent-nov07/out/pea-A-cream-trio.jpg, pea-B-pink-trio.jpg, pea-C-white-duo.jpg (sent in chat + push). HQ needs/launch-omm-pearlescent-nov07. No OMM IG post about it yet (as of 1:30pm ET); if one appears, that's the post to reshare. If she picks a frame: Planoly story draft (reminder: @ohmymahjong + link sticker).
- **Main: Virora Florielle restock (Sat Nov 7 9:35am ET, partner watch).** Rose Red 4 layers back in stock ($229). Frames for her review (NOT posted): assets/social/restock-florielle-nov07/out/flo-A-cream-trio.jpg, flo-B-pink-trio.jpg, flo-C-white-duo.jpg (sent to her in chat + push). She has 0 Florielle matches, so copy says 'every mat'. HQ needs/launch-virora-florielle-nov07. If she picks one: Planoly reminder story with @viroramahjongofficial + link sticker + code MAHJMATCH.
- **Matches & Catalog: FYM 1.17 r2 independent QA** (above #5). Orphaned tonight: build + gate finished 8:12pm, no QA agent started.
- **Ops/Matches & Catalog: the paired Mat Gallery + search paste** (above #2). If 1.17 passes QA first, paste the v117 pair (matgallery-v7.html @46c47075, rows @c90f4aaf) and rebuild search against it instead of v116.
- **Main: launch reel** is a Planoly reminder Sat 11/7 (01a1b30e-67a2): on "send me the launch reel" send file + post-new/pin/archive-old steps; add the Oct 27 song to docs/social/songs-used.md once she names it.
- **Main: Bam Bird bank deposits** (her screenshot of date + amount since Sep 1) into the Payout Tracker; OMM account email switch (record kept, docs/reports/payouts/snapshots/omm-dashboard-2026-11-06.png).
- **Main: Charleston Mahjong Club Cabana Club Travel Bundle** (live preorder since Oct 29, we missed it): codes post + calendar fixed? Check the CMC newsletter signup and the Mon codes post line.
- **Main: delete the stale 12 GB duplicate clone** /home/claude/tiffanybrie/mahjmatchmaker-data is HER call: re-ask (default: delete). Note: /home/claude/mahjmatchmaker-data in the cloud box is also stale (detached main); tonight's run used a fresh clone.
- **OPS + Matches & Catalog: The Mahjong Co.** mats are hidden in FYM 1.16 (her Nov 6 3:56pm call, ANSWERS); her HQ "did they close?" card is gone. Next: decide with the hide whether /mahjong-co-discount-code stays as is (Main, check ANSWERS first, never re-ask).
- **Main: blog posts name tile sets with albums but don't link them** (list in the Nov 5 desk, git show 09006524:docs/DESK.md). Target Mon Nov 9.
- **Main: revenue-alert cards**: 11 per-brand alert docs still in HQ needs (archived/info-only); fold into one Money summary in the morning report.
- **OPS: copy flat renders to Dropbox /Mahj Matchmaker Albums/New releases/<brand>/** (Nov 2-6 list in the Nov 5 desk) + Bam! Let's Mahjong teaser (assets/launches/bamlets-new-mat-teaser/).
- **OPS: copy assets/launches/faitamain-texas-mon-amour-mat-cream/ to Dropbox /Mahj Matchmaker Albums/New releases/Fait à Main/ today** and **assets/launches/letsbebesties-tidal-glass-with-simple-middle-mahjong-mat/ to /New releases/Let's Be Besties/** (launch watch Nov 7 6pm).
- **OPS: search Tiles & Tablescapes for Mahj Pit Full Sizes Black Tiles** (listed Nov 7, $385, no photos yet; copy its photos to Dropbox /New releases/Mahj Pit/ once posted).
- **OPS: follow + favorite @mahjpit.co** (docs/IG-FAVORITES.md); minimahjer.com Black Friday code check.
- **Main: prompt fixes still not applied**: sales-check prompt (all secomapp/goaffpro/backinstock mails, refunds on the refund date); "close leftover Claude tab groups" in every Chrome task; mat-edit-alert step in launch watch trig_01S2VsjwznnHev1uUbYmEwJq; launch/partner watch "wholesale customers only" + same-day FB group draft.
- **Main: duplicate catch-up tasks** trig_019StaM8LkmrxGKtK7xhXang + trig_013ZpyRxFivSKPoYTgSvVBU6: pausing one is her call.
- **Main: config/pinterest/queue.json** last updated Nov 4: resync with Planoly at the next autopin run, then FYM-led pins.
- **Main: hq/launches is at ~258 KB of the 256 KiB cap**: archive pre-Oct 20 items to hq/launches-archive before the next add.
- **OPS (standing): HQ ShopMy tab inbox** at the start of every Ops reply.
- **Partner feedback watch** trig_01RKw9eUwTYPo39gbYHb65gh runs daily through Nov 10 (0 new Nov 6).

## In progress
| Item | Owner | Next step | Target |
|---|---|---|---|
| Google: Fri code report + morning report (AI Overview vs AI Mode), OMM not named, Bing, AI-assistant check | Main + tasks (Ops for Chrome) | Priority 1. | Sat Nov 7 |
| Nov 6 sales close-out + why the daytime sweeps didn't run | Main | Priority 1b. | Sat Nov 7 |
| Mahjong Row OUT of the site (pages, hub, homepage order, FB comment) | Ops (Chrome) | Priority 2; done = live_codes_check PASS. | Sat Nov 7 |
| Mat Gallery + search pair; FYM preview page re-paste | Matches & Catalog / Ops (Chrome) | Priority 2. | Sat Nov 7 |
| Planoly next 7 days (roll-forward leftovers, dropped reels, stale reminder) | Main | Priority 3. | Sat Nov 7 |
| Easy content button (3 samples → daily auto post) | Tiffany yes → Main | Her yes in chat (HQ Today), then switch the Fri prep task. | Mon Nov 9 |
| Sunday albums ×4 | Tiffany picks → Matches & Catalog | Priority 4. | Mon Nov 9 |
| Juniper album | Tiffany picks → Matches & Catalog | Priority 4; live with the launch. | Mon Nov 9 (launch Wed Nov 11) |
| FYM 1.17 independent QA + publish (3 places) | Matches & Catalog | Priority 5. | Sun Nov 8 |
| Match inbox: 11 old lines + 32 LBB | Matches & Catalog | Priority 5. | Mon Nov 9 |
| Payout Tracker weekly refresh + Bam Bird deposits | Main | Her screenshot; docs/PAYOUT-RECONCILE.md. | Fri Nov 13 |
| PEACE LOVE → Level 2 ($5K referred/month) | Main | Plan + PLM MTD in the morning report. | Mon Nov 9 |
| Partner newsletter signups (26 brands) | any Chrome chat | docs/PARTNER-NEWSLETTERS.md, CMC first. | Mon Nov 9 |
| ManyChat comment-for-links draft (low priority, her 4:11pm) | Main (Chrome) | OVERDUE line; trial day-12 reminder task. | Tue Nov 10 |
| Work With v3 + Brands form | Tiffany yes → Ops | Her yes on HQ Today (waiting since Nov 1). | On her yes |
| IG evergreen codes post (01a1a859-bcb8) | Tiffany taps Post | Auto-schedule refused; she taps Post, drags it bottom-left. | When she posts |
| Holiday new-albums email | Main | Squarespace draft; her final read. | Mon Nov 9 |
| Blog album links | Main | Handoffs. | Mon Nov 9 |
| Holiday colour cards (Tinselle ×2, Dec 1994, PLM Spirit + Nutcracker) | Matches & Catalog | Not started (was Oct 31). | Tue Nov 10 |
| My Fair Style of Your Life (#1 album) | Matches & Catalog | Colour card + TNT, then swipe book. | Tue Nov 10 |
| Larkspur hearts into 27 tile albums | Matches & Catalog → Ops | 0 of 27. | Tue Nov 10 |
| December 1994 redo (her RTS notes) | Matches & Catalog | After holiday colour cards. | Wed Nov 11 |
| Lotus Cove swipe book full names (book_gate [n]) | Matches & Catalog | Before Juniper launch. | Mon Nov 9 |
| Bam Bird Deco trio (Indigo first), Bird & Bamboo brand-lock sample | Matches & Catalog | Colour cards / hosted embed. | Week of Nov 9 |
| Discount links not converted (Britt Mills, Mahjong Register, YMI, RMS, Hip Hip, Wren/Soirée/Amanda Toppe) | Main | builder/fym_fix_oct21/discount_check_oct21.json (auto-apply links now in the gallery build). | Mon Nov 9 |
| UpPromote accounts → mahjmatchmaker@ (Mahj Squad code still assigned?) | Tiffany / Main | Screenshots before each switch. | This week |
| Affiliate applications (apply kit, now top of the Affiliates tab) | Tiffany submits | Kit doc 00h. | This week |

## Blocked, approved (raise at the top of every attended reply until done)
- **Mahjong Row & Co. OUT of the site** (Tiffany Nov 6, approved): Chrome. live_codes_check FAIL 61 until done.
- **Mat Gallery + site search pair** (her yes Nov 6 5:30pm): Chrome.
- **/find-your-mat-ch-preview re-paste** (FYM 1.16): Chrome dropped mid-save.
- **Bing Webmaster Tools** (her yes 5:29pm) + **partner newsletter signups** (standing yes): Chrome.
- **Planoly roll-forward**: the unattended desk run is refused for most update_post / set_post_group_schedule calls (3rd night; 3 of 8 caption edits went through tonight). Priority 3a lists the 5 left.
- **IG EVERGREEN CODES POST**: auto-schedule refused; she taps Post.
- **Dashboards signed out** (B&B UpPromote, My Fair, OMM, Mini Mahjer): her sign-in (HQ Today #1).

## Waiting on Tiffany (only things she can answer now)
**On HQ Today, in this order (5):**
1. **Google: sign back in to Bird & Bamboo, My Fair, OMM and Mini Mahjer dashboards** (1 min each).
2. **Work With page v3 + Brands form: yes / wait / changes** (since Nov 1).
3. **Juniper: 4 favorite faces + any cuts** (by Mon Nov 9).
4. **Sunday albums: ♥/✕ the 31 new mats** (short page, no 121-mat book).
5. **Easy content button: yes or changes on the 3 samples in Planoly.**

**On HQ This week:** Sweet Jojo W-9; FYM 2 quick checks + Holy Mahj image; next week's posts in Planoly (one-line card); 1 hidden FYM photo (Grace Peacock); ShopMy 6 quick calls + 2 stray links; Bam! Let's Mahjong sneak peek; partner launches + IG reshare lists.

**Asked in chat, not yet answered: the owning chat RE-ASKS at the top of every reply until answered, with its default:**
- Main: **remove the dropped Rudolph/Polo/Rattan drafts from Planoly?** (default yes, with archive record); **84 locked FYM colour changes** (default apply); **delete the stale 12 GB clone?** (default delete); Bam Bird deposit screenshot; which song is on the Oct 27 launch reel; Malachite how-to reel v2 OK + day.
- Matches & Catalog: Lagoon + Mulberry splits; Bam Bird Classic Tortoise match pick; Sunday Rattan = Blue Rattan?; Fruit Stand rack-edge (default a); brand-lock pricing (undecided, don't push).

## Banked (finished, held on purpose)
- **Mahjong Row & Co. fall album**: parked (Mahjong Row OUT, Tiffany Nov 6). Parked site copy: archive/mahjong-row-parked-2026-11-06.
- **Launch reel redo (spotlight, no Mahjong Row)**: done Nov 6 ~6:10pm; Planoly reminder draft 01a1b30e-67a2 Sat 11/7 (IG + FB Page reel); she posts it new, pins it, archives the Oct 27 reel.
- **Petalée (Virora)**: 61 cards, RTS `l-final-petalee`, vault (her Oct 28). Before publishing: colour card, 10% band sweep on the Amanda Toppe/Girly cards, cleaner Petalwing/Coralia photos.
- **Holiday intro reel v5** (46s): POSTED Nov 3 ~4:30pm on IG + story + FB Page (Reels tab). It is the reference standard for future FYM reels (FYM-REEL-RULES 23-41).
- **Retro Rattan holiday table reel + 7-frame story**: undated Planoly drafts (01a16477-0588, -078d). Mood-board/table reels DROPPED (her Nov 6 4:11pm); see Later.
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
- **Clean up 52 legacy caption lint warnings** (still 52 Nov 6) (config/social/content_lint_baseline.json; mostly missing #MahjMatch, '(affiliate)', 2 TdT captions) (rules audit E9, Oct 30). Also 78 legacy FAILs (length 42, naming 36) in banked Season 2 captions: same kinds as yesterday, nothing new.
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

## Daily operations (Fri Nov 6)
| Operation | Done today? | Notes |
|---|---|---|
| Affiliate tracking (Money tab) | ⚠️ Partial | No 10am/2pm sweep ran (she caught it 5:31pm); 5:45pm catch-up: Anders Ruff 2 = $54.63, My Fair 3 / Mini Mahjer 1 / Bam Bird 1 amounts unknown. Close-out = priority 1b. Payout Tracker built (Q3r6wMhYLqoyJSYnfKmtH2); PayPal Oct 6-Nov 6 logged; Miss Mahjong $339.39 paid. |
| Google code report | ❌ Not done | Fri was due (Mon/Wed/Fri); no Nov 6 report. Priority 1a. |
| Morning Google report | ⚠️ Early only | Only the Thu 8:40pm early run (36/39, desktop, at night); Fri 7:13am refresh missing. Her own check 5:16pm disagreed (Miss, Bam Bird, Bespoke, PLM not in AI Overview). AI Mode sweep (39 brands) ran 1:12am. Squarespace AI Visibility first run: ChatGPT 5/10, Gemini 6/10, OMM missing. |
| Verified dates (weekly, Mondays) | ✅ Fixed live | OMM, Wren, Mahjong Co. dates + Amanda Toppe 10% fixed 12:42am (check PASS for those); next weekly pass Mon Nov 9. |
| Codes post (Mondays) | ⏭ Not due | Next Mon Nov 9 (FB group, typed out; hub list WITHOUT Mahjong Row). Nov 3 post edited: Bam Bird MCM Olive line. |
| Pinterest queue health | ✅ OK | Planoly Pinterest has scheduled pins Nov 7-8 (first page; last night 3-4/day through Nov 30), 0 errors; 10 FYM pairing pin drafts unscheduled. queue.json stale (Nov 4). |
| Indexing | ✅ Done | 6 requested ~5:30pm (OMM, Amanda Toppe, hub, Wren, Mahjong Co., My Fair), no quota error. |
| Planoly next-7-days (IG + FB Page) | ❌ Not covered | 0 IG scheduled Nov 7-13; every day has drafts. Roll-forward 3 of 8 done. Planoly lint 21 FAIL (same kinds: story captions, codes-post length = her exception, banked Retro Rattan; +2 = the stale Oct 21 Papaya reminder). FB targets: all feed groups have one; IG-only = the codes post (by rule), the dropped Polo/Rudolph reminders and the 6 🛑 easy-content story/reel samples (their FB versions are in the same groups) and the stale Oct 21 reminder. |
| New albums (last 7 days) (f) | ✅ All checks | Brownstone Bloom (live Nov 1): /mahjong-tile-matches ✅, /links ✅, Pinterest queue ✅ (54 refs), indexing ✅ (hq/indexing), colour + brand pages ✅ (Nov 3). No new album went live Nov 6. |
| Repo caption lint (g) | ⚠️ Legacy only | 78 FAIL (length 42, naming 36: Season 1/2 episode captions, holiday-table captions, Papaya long intro), 52 legacy WARN. Same kinds as yesterday, nothing new. |
| Live codes check | ❌ FAIL 61 | All Mahjong Row (approved removal, Chrome). |
| Gallery sync check | ❌ FAIL | Live /mahjong-mats has no data-fym stamp (old v5 block); app is v116. Pair paste = priority 2. |
| Restock first (c) | ✅ Checked | No album-set restock dated Sat Nov 7. |
| Match inbox (e) | ⚠️ 11 old open | Down from ~91 (35 marked DONE 6:39pm). Priority 5. |
| Launch + partner watch | ✅ Done | Launch watch 9:05am + 5:57pm (Splash Valentine ×5, LBB Pink Christmas, Fait à Main Le Bandana); partner watch 9:45am, 1:40pm (MRC/Bam Bird/Mahj Mood drops LIVE), 6:30pm; new store watcher + IG brand watch built. |
| FYM + partner feedback | ✅ Done | 0 new (2:19pm). |
| FYM releases | ✅ 1.16 LIVE (app) | 1.16 r2 artifact + /find-your-match (~8:45pm); preview page still v115; 1.17 built, QA pending. |
| Social posted today | ❌ None recorded | No IG/FB Page post went out; evergreen codes post waits on her tap. |
| HQ + Ready to Ship cleanup | ✅ Done | Morning 7:05am, sweeps 9:47am / 1:47pm / 7:47pm; this run 15 open → 14, Today 3 → 5. RTS: no new answers since Oct 30. |

## Never-ending projects
- **Find Your Mat-ch™ app** (artifact 6epA9HuEdT32zUp79Qv3kd; public **Version 1.16** (r2, artifact Version 115; website /find-your-match = fym-v116 @fdcc1868 pasted Nov 6 ~8:45pm; /find-your-mat-ch-preview still v115 until the re-paste); **1.17** built, gate PASS, independent QA pending: gate + independent QA before every publish (QA loads the WEBSITE copy as live: 0 broken images, gate [115]); artifact AND website copy AND README 0a pin in the same step; +0.1 version label (docs/FYM-VERSIONS.md); her feedback the same day with a gate check; when a publish/paste fails, MESSAGE HER right away. Artifact file budget: run builder/fym_artifact_fit.py and publish ONCE. Every nav/header change: screenshot live at 1280, 1440 and 390 with the phone menu OPEN. New partner catalog in FYM within 24h of its inbox line (gate [114]). Refresh config/fym-mats-snapshot.json after every publish.
- **Match inbox** (docs/MATCH-INBOX.md): any chat writes match/catalog misses there the same turn; Matches & Catalog marks DONE when shipped.
- **Google / MAHJMATCH in AI answers (her #1)**: AI Overview + AI Mode per partner, code report (Mon/Wed/Fri), daily morning report, indexing (brand pages first), sitemap health, weekly verified dates + hub date, weekly codes post (FB GROUP only typed out; IG/FB Page = logos graphic + short caption), alarm on any lost citation.
- **Albums**: order (her Oct 28 3:31pm): MFM Style of Your Life → Bam Bird Deco trio (Indigo first) → Sunday Blues → Sunday Nature Walk → Middle & Main Peach and Pine, Mac + Miller; Mahjong Row fall + OMM green set (Juniper) jump the line; a known restock goes FIRST. Doc 86b (colour card FIRST), book_gate.py, PICKING-RULES.md, NEW-ALBUM-CHECKLIST.md (incl. the new-albums email).
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

## Log of this rewrite (Fri Nov 6 night)
- **Done today:** Find Your Mat-ch 1.16 (Mahjong Row parked, Mahjong Co. mats hidden, 17 dead links, auto-apply code links) independent QA PASS, artifact + /find-your-match live; 1.17 built (gate PASS); Mat Gallery v6/v116/v117 blocks + search rebuilt and paired-QA'd (staged); Amanda Toppe 10% + OMM/Wren/Mahjong Co. dates fixed live; NOTHING SLIPS system (live codes checker, front-door hook, OVERDUE); dead brand-page links fixed; Sunday albums 180 cards + 31-mat page; Juniper round 3 applied offline; launch reel re-cut (no Mahjong Row, spotlight); next week's 13 social drafts; easy-content samples; Payout Tracker + PayPal read; keyword volumes refreshed; AI Mode sweep + Squarespace AI Visibility; partner store watcher + IG brand watch; 6 pages indexed; business pillars strategy doc.
- **Found mid-way and given a home:** FYM 1.17 independent QA never started → priority 5 + Handoffs; preview page paste dropped mid-save → priority 2 + Blocked; Fri code report + 7:13am morning report missing → priority 1a; daytime sales sweeps missing → priority 1b; Planoly roll-forward refused (3rd night, 3 of 8 done) → priority 3a with the exact 5 posts; dropped mood-board reel drafts → one re-ask (Main); Rudolph Canva unsaved edit → moot (reels dropped); launch-reel HQ card → archived (done, in Planoly); stale /home/claude/mahjmatchmaker-data checkout → repo note.
- **HQ:** archived launch-reel-redo-nov03 (done + in Planoly). Today = Google dashboards, Work With v3, Juniper picks, Sunday 31 mats, easy-content samples. hq/now + hq/priorities rewritten for Sat. Albums: Sunday Blues / Nature Walk / Plum Panda / Hummingbird → Needs your yes (31-mat page); Juniper detail = round 3 applied; Mahjong Row fall → Banked (parked). "Yours" = 8 (Juniper, 4 Sunday on one page, PFK mat book, Le Bandana mat book, Splash optional book).
- HQ smoke test at 390px not run (data-only change, no page HTML changed).

See CLAUDE.md.

- OPS (Chrome): SEPTEMBER CHECK for the Payout Tracker 'Close October': on each own-dashboard brand (My Fair, Mahjong Co., Mini Mahjer, Hip Hip, Bam!, CMC, Amahj, Splash, Mac + Miller, OMM) read Commission filtered Sep 1-30: any Approved/Pending (unpaid) September rows -> amount per brand into docs/payouts/brands.csv sep_check, re-upload + update dataset 'brands' on https://claude.ai/artifact/Q3r6wMhYLqoyJSYnfKmtH2. Also confirm the Middle & Main Oct 13 $43.88 payout is September and the Bird & Bamboo Oct 26 $106.65 is September (payments.csv for_month). Bam Bird bank transfer: exact amount + date from Tiffany's screenshot.
