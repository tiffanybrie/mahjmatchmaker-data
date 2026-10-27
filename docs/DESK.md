# The Desk

- **OPS / Matches & Catalog (Oct 27 3:15am): paste FYM Version 1.4 on BOTH /find-your-match (live tool page) and /find-your-mat-ch-preview.** Artifact already on 1.4. Block: `https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@10f3498743be6ccbd73cd4d47bae2151be6ba296/site/livepatch/fym-preview-oct21/page-block.html` (CodeMirror dispatch, Escape, Save, Exit; search iframes for .cm-editor). Verify `curl -s https://www.mahjmatchmaker.com/find-your-match?v=$RANDOM | grep -o fym-v100`. Built-in browser lost the computer mid-paste (nothing was changed on the site).
- **MAIN (Tiffany Oct 27 12:01am): the "It's here!" launch email is Main/Social's job, not Matches & Catalog's. Partners are LEFT OFF it (they get their own partner email). Keep all launch-day email in Main so it stays cohesive.** STATUS 12:05am: the launch email (site/email/templates/launch.html) is NOT approved: she said NO on Oct 23 with revisions (ANSWERS line 15: one Montserrat-style subhead for 'Here's how it works'; tutorial must mirror the current in-app tutorial) and they were never applied (file unchanged since Oct 21). The 7:40am check skips it (v=no). Main: revise + get her yes before it can send.
- **Matches & Catalog, NEXT BUILD after 1.4 (Tiffany Oct 27 2:21am: "This is going to get very old, me chasing down mats"):** add the partner mats the store sweep found missing (config/partner-mat-sweep-oct27.json): Britt Mills House Print (Oct 22); TdT Domino Blonde, Fair Isle Cashmere, Estate Sale, Domino Faded Carolina, Domino Oxblood; Bespoke x Brooks Brothers Oxford Classic; OMM Holly Jolly mat; PLM vegan leather mats; PLUS PLM Spirit of Christmas tile set (sold out label). Build a gate check: a partner store's full-size mat live > 2 days but not in FYM + gallery = FAIL unless listed with a reason. Process the launch-watch new-product list DAILY.
Rewritten nightly by the end-of-day desk cleanup (9:23pm ET). The morning HQ cleanup (6:47am ET) reads it. Rules: CLAUDE.md ("THE DESK"), docs/CHATS.md (which chat owns what). During the day, when an agent stops, Chrome drops or a QA stalls, add the item here right away with its next step.
- **Matches & Catalog (Oct 26 11:50pm): FYM Version 1.3 (rack pass) is LIVE in the app + website preview; launch README 0a pin = page-block @b103418 / fym-v99.** Left for the next build: Bam! White Wooden single cut-out (assets/racks/bam-white-wooden-single.png, made for Main tonight), OMM uniform rack format, Hip Hip Hostess + Mahj Mood Scalloped Tortoise still stacks (horizontal now), Bam Bird Lucite Emerald shows its pusher strip, AR Clear sets in white boxes; 71 racks still on lifestyle/stack photos (gate [97] warning list).

**Last rewrite:** Mon Oct 26, 2026, ~9:30pm ET (desk cleanup run). Covers the ~405 commits of Mon Oct 26 (93012f2 … c3cf448: FYM v94 → v98b = public Version 1.0 / 1.1 / 1.2), docs/ANSWERS.md (Oct 26 lines through 8:53pm), docs/MATCH-INBOX.md, Planoly (IG workspace 019fc27c… + Pinterest 019fc27b…), HQ needs / log / money / albums, Ready to Ship `ship` docs (nothing new answered today), the Launch week plan page (artifact TodweWYVb8f9iLUGtsd1KQ), scheduled tasks, site/livepatch READMEs and curl checks of the live site tonight.

**Owners (three chats, Oct 22):** Main (Opus) = social/Planoly, site pages, email, HQ/DESK, decisions. Matches & Catalog (Opus) = Find Your Mat-ch, albums, gallery, catalog, search index. Ops (Sonnet) = the ONLY Chrome driver: Squarespace pastes, uploads, IG follows, verified-date refreshes.

**Repo note:** checkout /home/claude/mahjmatchmaker-data on `partner-catalogs-sqsp` (use `git fetch --depth=60`; a full fetch of this 3 GB repo times out).

## Handoffs to do first (Tue morning, before 9am CT)
- **OPS: paste FYM Version 1.2 on the website preview page (handed off 8:45pm Mon; NOT done at 9:30pm, curl still shows fym-v97).** Squarespace Pages > Not Linked > Find Your Mat-ch Preview (/find-your-mat-ch-preview) > Edit > double-click the code block > `const html=await (await fetch('https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@80a2aad8318b1688c27c77ebd00dc48f80bbad40/site/livepatch/fym-preview-oct21/page-block.html')).text(); const v=document.querySelector('.cm-editor .cm-content').cmTile.view; v.dispatch({changes:{from:0,to:v.state.doc.length,insert:html}})` (search iframes for .cm-editor) > Escape > Save > Exit. Verify `curl -s https://www.mahjmatchmaker.com/find-your-mat-ch-preview?v=$RANDOM | grep fym-v98`. While there: the stray `site-app/fym-v72` string is still on that page (4th night): find and drop it. Artifact is already on Version 1.2; launch README 0a pin is already 80a2aad / fym-v98, so the launch swap ships 1.2 even if this paste slips.
- **OPS / Main: the 9am CT launch switch runs as a cloud scheduled task (trig_011jdGG, 14:00 UTC) that does NOT require her computer, so it has no Claude in Chrome.** Its Squarespace steps (0a tool onto /find-your-match, hero swap, CSS, announcement bar off) will likely fail. Fix: Tiffany turns on "Require this computer" for that task in the Claude desktop app (HQ Today 1), or an attended Ops chat with Chrome runs site/livepatch/launch-oct27/README.md by hand at 9am CT. Note: the README step 1 says italic "Your" in the H1; the brand guide (Oct 21 18:30) and the task prompt say the website H1 is PLAIN, no <em>. Follow the brand guide. Same Chrome gap applies to the 8:15am CT launch-email task (trig_01ErZy), but that one stops at step 1 anyway (RTS d-email-templates is `no`) and will set HQ need email-templates-approve to red/today: the morning cleanup should merge that into the launch-plan need, since the subscriber email ask is on the Launch week plan page.

## Tomorrow's top priorities (Tue Oct 27, launch day), in order
Standing order: (1) Find Your Mat-ch™ launch TODAY 9am CT, (2) fall content before it expires (Brownstone Bloom by Thu, before Halloween), then holiday (November, through Find Your Mat-ch). The order is clear; no "Set tomorrow's order" question.

1. **Launch the site at 9am CT (Ops, Main checks).** Make sure the switch can actually run (handoff above), then: /find-your-match shows the tool (README 0a pin 80a2aad = Version 1.2), homepage hero "Find Your Mat-ch™ is here" (plain H1), "Start swiping" → /find-your-match, countdown bar off. /links already auto-flips its FYM card to live at 9am CT (no repaste). Verify by curl + 390/1280 screenshots; rollback text is in the README. Target 9:30am CT.
2. **Launch social goes from draft to scheduled on her "posts yes" (Main).** All dated in Planoly IG workspace as DRAFTS (nothing auto-posts without her yes): launch carousel 01a17a6a-943b (IG + FB Page, Tue 9:00am CT), 5-frame story 01a17a6a-95d3 (9:01am CT), link-sticker reminder 01a17a6a-9777 (9:05am CT, hers), Brownstone Bloom post + stories 01a17a6c-10e4 (Tue 1pm CT), Miss Classic Malachite + Jade 01a17a6c-12c1 (Wed 10am CT). Same yes covers: FB group launch post Tue 9am CT ("group yes"), partner follow-up email + hidden /partner-kit page Tue 9:30am CT ("partner yes"; page block staged @c3cf448), subscriber email to site signups only ("subscriber email yes" or "skip"). Also fix in Planoly: Halloween Raven carousel 01a16477-092f is still dated Wed 10/28 11am CT but the plan moved it to Thu 10/29 noon; clear the dates on drafts whose day passed without posting (Papaya "Still available" 10/23, Smith swipe reel 10/24, Papaya × Heiress 10/25, Miss Classic tease 10/26 with the old "week of Nov 3" wording) — clear dates, never delete. Target: switch to scheduled within minutes of her yes; if no yes by 8:30am CT, message her once.
3. **Partner graphics finished and on /partner-kit (Main).** 24 brands approved on the review page (QEn8r2kcY3d8avT5FB3Fun). Still open from her 8:53pm notes: Tigre de Tartán (House Clovers on Domino Oxblood, TdT racks rotated level), Mahj Squad (Seafoam or Ballet Pink + Gold Metallic; default A), Royal Mahjong Society (Girly × Girly, peachy-pink title), Amanda Toppe (Miss Classic JADE on Serenity; default Serenity), Virora Petalée (pink title, Virora pearl scallop + a pink; default own racks), YMI Sakura placeholder OK, Boots & Bubbles racks lower, Papaya OMM racks same proportion. Defaults apply if she doesn't pick. Then the OUR-VERSION set (MAHJMATCH bar) into assets/social/partner-kit/ours/ and the one-brand-a-day calendar from Thu. I Love Mahj + The Mahjong Press have no FYM product: email text only. Target: before the 9:30am CT email.
4. **Launch-day watch (all chats).** Partner feedback 9am/1pm/5pm/9pm CT (trig_01RKw9e) → HQ Partner tab; FYM feedback + tester form (/find-your-mat-ch-tester); any bug she or a player reports → fixed the same day with a gate check (rule 8). Also today: OMM moving sale mentor early access 10am CT (Elizabeth posts the link; codes don't work on sale items; heads-up post idea for Wed public opening); Mahj Tile Haus Imperial Lotus restock 11am CT (non-partner, ShopMy only: no promo); Miss Classic drop watch (ETA week of Oct 28). Sales checks per her schedule.
5. **Fall content + overdue site catch-up (Matches & Catalog → Ops).** Brownstone Bloom live by Thu Oct 29: her Save on the order page (https://claude.ai/artifact/WNjXTGjxfdqoa1tzUiYgQ4, db `review/order` still EMPTY tonight; HQ Today) → brownstone_block.py, warm jsDelivr, publish, /links card, NEW-ALBUM-CHECKLIST. Ops catch-up, standing authority, no OK needed: (a) her 41 thin-album hearts are STILL not on the 9 album pages (curl tonight: 0 of 9; README site/livepatch/thin-albums-oct26 @2cd234fe, cards @e718949b) — her picks, overdue since Oct 24, do right after the launch switch; (b) holiday anchor fix (Sierra still `id="holiday"`, approved Oct 25 3:21pm): rename to `holiday-matches` on the 34 albums + 34 links on /holiday-mahjong-matches; (c) site search header injection (site/livepatch/search, QA passed Oct 22) still not live.

## Later / ideas (added Main Oct 26 11:31pm)
- Partner portal: a bookmarkable place where each partner brand manages its content (uploads, photo swaps) and gets personalized graphics. Tiffany: "eventually it would make sense". Not this week.

## In progress
| Item | Owner | Next step | Target |
|---|---|---|---|
| FYM Version 1.2 on the website preview page | Ops | Handoff above. | Tue before 9am CT |
| Launch switch (/find-your-match + homepage hero + bar off) | Ops (scheduled task trig_011jdGG) | Priority 1; Chrome gap above. | Tue 9am CT |
| Launch social + emails + FB group post | Main | Priority 2 (waits on her yes on the Launch week plan page). | Tue 9am CT |
| Partner share graphics + /partner-kit + our-version set | Main | Priority 3. | Tue 9:30am CT |
| MATCH-INBOX open items (docs/MATCH-INBOX.md) | Matches & Catalog | After launch-day bugs: OMM racks in the app → the 4 leveled cut-outs in assets/racks/omm-level/ (one format); Tigre de Tartán racks rotated level; Bam! White Wooden rack single cut-out (still in a white box); MRC Scalloped Tortoise is 20" → offer with every set + preferred tortoise, then M&M Hawksbill (use the clean mm:Hawksbill cut); rack length by TILE SIZE research (length in every rack's data; B&B 20" only); Virora pearl scallop rack if sold; late partner holiday mats into holiday albums (after her picks). | Wed Oct 28 |
| Angled mat photos with white corners (38 mats, gate [89]) | Matches & Catalog | Her 7:49pm call: post-launch. Perspective-flatten like amahj-blue-citron-lilac-flat.jpg (config/fym-mat-flat-oct26.json + v98_matflat.py WIP). | Wed-Thu |
| 69 visible FYM mats without a Mat Gallery row (gate [90]) | Matches & Catalog | Gallery synced to 775 tonight (live); re-run gate [90] on b98 and add what's still missing. Skipped on purpose: Bespoke Gray Malin (photo flagged), YOTD Periwinkle duplicate. | Wed |
| Mat Gallery intro + 414 jsDelivr request | Matches & Catalog | After launch: /mahjong-mats intro "coming 10.27" → link to /find-your-match; trace the one 414 request on /find-your-mat-ch-preview (Bam Art Deco mat JSON appended to a URL). | Tue after launch |
| Rack ranking: accent colour, not the dominant one | Matches & Catalog | Her Oct 26 4:45pm rule (blue racks on a blue mat = overmatch); never lead Bird & Bamboo with White / White Metallic; gate check. | This week |
| Bird & Bamboo tile zoom in the match-card circle | Matches & Catalog | Same treatment as PLM/MFM (config/fym-tile-focus-oct25.json + gate [45]). Done for the B&B partner card only. | This week |
| Classic Tortoise tile crop (Bam Bird) | Matches & Catalog | Crop in so tiles read bigger; try the split frame (her Oct 25 9:56pm). | This week |
| Malachite: Jade & Brass racks early + her YOTD Amped-Up Grey pick | Matches & Catalog | Her Oct 26 1:47pm: verify on Version 1.2 that Miss Mahjong Jade & Brass show early for Malachite and Malachite × YOTD Amped-Up Grey is in her picks (m); add the same-brand-rack-buried gate check if not. | Wed |
| Bespoke racks on app cards | Matches & Catalog | v96 re-cut 8 clean cut-outs + gate [81]; v98 draws Bespoke racks bigger, off the mat's left. Re-check Peacock Blue / Highlighter Pink / Holiday Red on 1.2 (her 4:40pm report, 2nd time). | Tue |
| Mahj & Moon ShopMy collection + 14 FYM relinks (approved Oct 26 11:04am) | Ops → Matches & Catalog | Collection created (shopmy.us/collections/8525607, empty). Ops pins the 14 Etsy listings (config/mahj-moon-shopmy-links.json), then v95_mahjmoon.py in the next FYM build. ShopMy cover in the portrait style. | After launch |
| Thin albums → FYM picks | Matches & Catalog | After Ops pastes the cards (priority 5a): run builder/fym_fix_oct26/v94_thinpicks.py in the next build. | After 5a |
| Mat swipe-book hearts into tile albums | Matches & Catalog → Ops | Larkspur cards built (assets/cards/larkspur-v6), on 0 of 27 albums; then Revelry, Isla, Peony & Parasol, Art Deco Dayz, Spring Fling, Santa Baby's, Vivienne, Brownstone. | Wed+ |
| Ops Chrome catch-up | Ops | Priority 5 (thin albums, holiday anchors, search). Then: welcome/album-request automations stay drafts; Mahjong Row + Anders Ruff + Royal Mahjong Society dashboard sign-ins so sales checks read amounts. Close every tab. | Tue after launch |
| ShopMy holiday leftovers | Ops | Kate & Laurel Celia + Santa/Reindeer mat (JUDFNCDE) → Tables; pink lamp B0GD1585QW → Lamps; shelf reorder; Sweet JoJo shelf; holiday tag audit; Retro Rattan list = "A Natural Green Holiday Table" (her Oct 26 12:55am title; rename not done); rack on the Reindeer list. | This week |
| ShopMy covers break on phone (2:3) | Main → Ops | Samples + generator built Oct 25 (14b504b); show her once after launch; on her yes Ops re-uploads ~35 covers. | Thu |
| Canva template library samples | Main | Built Oct 25 (0dd3acd); show once after launch. | Thu |
| Bird & Bamboo sales drop check | Main | Search Console clicks/impressions + "bird and bamboo discount code" query + AI Overview; verified date is Oct 21 (current). | This week |
| Bam Bird Boutique page fell to ~#17 on Google | Main | Weekly SEO review (Oct 26 1:40pm): request re-crawl. | This week |
| YOLO Mahjong affiliate approval | Main | Confirm the email, then onboarding (page, hub, logo, FYM, indexing, IG follow/favorite). | This week |
| The Royal Mahjong Society: first sale Oct 26 (UpPromote) | Main | Add to the affiliate logins list + sales checks. | This week |
| Outreach page (hidden /work-with-us) + Work With rebuild + launch/restock form | Main → Ops | Her l-workwith6 notes; fix the ticker's empty boxes. First use: Backyard Yacht Club. | After launch |
| Discount links not converted (Britt Mills, Mahjong Register, YMI, RMS, Hip Hip, Wren/Soirée/Amanda Toppe) | Main | Proof in builder/fym_fix_oct21/discount_check_oct21.json. | After launch |
| Google feedback drafts (TEACHMAHJ teacher-only, MJTI dead, YM, thumbs up x6) | Ops | Standing authority. | This week |
| Amazon mats into gallery + FYM | Ops → Matches & Catalog | Only her picks (HQ need, parked to Wed). | After launch |
| Missing swipe-book products (OMM Miracle / Twilight Waltz / Merry Mahjong / Santa Baby; PLM Spirit + Nutcracker; OMM Vault) | Ops → Matches & Catalog | Photos in Chrome → pending queue. | After launch |
| New releases (Splash of Color x5, YM Sea Mist, Mahjong Register Cane Cabana + Celestial Chromatic racks, Britt Mills Crimson Harvest leatherette) | Matches & Catalog | hq/newproducts → gallery + FYM when photos pass; never albums; never Splash tile mock-ups. | This week |
| FB group album end graphics (made, never added) | Main → Ops | Low priority (her Oct 26 4:12pm): find them in Dropbox, add to the FB albums. | After launch |
| Malachite + Kingfisher | Matches & Catalog | Kingfisher via nonpartner_allow.json; racks Miss Mahjong Jade, PLM Oak, Bam Bird Indigo. With the Miss Classic restock (now week of Oct 28). | This week |
| Papaya Beechwood README | Matches & Catalog | Live since Oct 22; README still says STAGED. | Next touch |

## Waiting on Tiffany (only things she can answer now)
**On HQ Today, in this order:**
1. **Launch switch: turn on "Require this computer"** for the "Launch day: switch homepage hero" task in the Claude desktop app, and leave the laptop on with Chrome open 8:45-10am CT (or tell us to run it by hand).
2. **Launch week plan: answer the asks** (https://claude.ai/artifact/TodweWYVb8f9iLUGtsd1KQ): "posts yes", "partner yes", "group yes", "subscriber email yes" or "skip", and the last partner graphic picks on the review page (defaults go if she skips).
3. **Planoly Content Marketplace add-on: keep or cancel** ($13/mo; trial ends ~today).
4. **Monday's missing sale amounts:** Mahjong Row & Co. (6), Anders Ruff (1), The Royal Mahjong Society (1).
5. **Brownstone Bloom: put the 40 cards in order and Save** (order page). Fall content, publish by Thu.

**On HQ This week:** late partner holiday mats → which holiday albums (https://claude.ai/artifact/YXt3CzLisaRSEeqKHaoTez; shortlist docs/holiday-late-mats-shortlist-oct26.md); Sunday sets round 2 (4 sets); FYM hidden photos (8) + questionable mats (3); Fait à Main link + code. Parked to Wed Oct 28: Gatsby round 2, Amazon holiday picks, Etsy re-apply (Rakuten), holiday-or-not on 11 mats, ShopMy 5 calls, Shop page talk, Amazon old boards.

**Asked in chat, not on HQ (the owning chat asks once, next time she's there):**
- Main: Peace Love Mahjong partner graphic — she picks it herself now that Desert Dreams' tile view is fixed (Version 1.1+): tell her it's ready to match. ShopMy 2:3 cover samples; Canva template samples; her lost Pippa teardown (2-3 lines).
- Matches & Catalog: which of the "Photo coming soon" tile sets to show; Lagoon + Mulberry splits once rebuilt from their own colourway photos; Bam Bird Classic Tortoise match pick; album idea MFM Jubilee × Parquet Petal + MFM wood racks (her swipe book, not FYM m).

## Banked (finished, held on purpose)
- **Petalée (Virora)**: 61 cards, RTS `l-final-petalee`, vault. Before publishing: 10% band sweep on the Amanda Toppe/Girly cards, cleaner Petalwing/Coralia photos.
- **Vivienne mat album (OMM)**: 16 cards, parked (no mat albums, Oct 23); its hearts go into the tile albums.
- **Sunday Blues + Nature Walk**: vault once her round-2 swipe is in (never two Sunday sets back to back).
- **Season 2 episode reels + trailer**: undated Planoly drafts (Ep 1-13). The dating-life series is OFF this week (her Oct 26 12:26pm). Don't re-date assets/reels/s2/*.mp4 or assets/social/countdown/*; each gets redone with an intro first. Jade "Smith-style" reel: parked after launch week (needs her song).
- **Halloween**: Night of the Raven carousel (move to Thu 10/29 noon) + Happy Halloween story (10/31).
- **Holiday tables** (Polo Club 11/4, Rackin' Rudolph 11/6, Retro Rattan held): Planoly drafts.
- **Malachite 8 new cards, December 1994 (31), Spirit of Christmas (10)**: staged since Oct 20; holiday ones from Nov 1 (December 1994 still needs her RTS notes applied).
- **Partner kit explainer video v2 + launch explainer reel**: built Oct 26 1am; not used tomorrow (launch plan uses the carousel).

## Later / ideas
- **Separate desktop vs mobile FYM experience** (her open question, ANSWERS Oct 25 11:07).
- **Mat-only brand "eye candy" story** (Oct 26 4:16pm): frame 1 = a grid of the brand's mats, frame 2 = the trio (Britt Mills, Amanda Toppe).
- **OMM reshares only 100%-OMM content** (Oct 26 4:14pm): watch what OMM reshares.
- **FB group growth plan** (Oct 26 4:12pm history: ~2,400 members, reach 100-200; @everyone capped weekly by Facebook, save it for the biggest moment).
- **IG engagement is low for the effort** (Oct 26 4:01pm data): keep IG lean; partners + group first.
- **Canva template library + FYM-to-content brainstorm** (Oct 25): reshare followers' matches with #MahjMatch.
- **IDEAS / 3.0 (Oct 23):** private studio view; table view (tablecloth, lamp, dice dish via ShopMy); per-product links after testing which partner links auto-apply the code (never OMM).
- **Internal FYM "sets" view for reviewing album matches** (Oct 24).
- **New products roundup** (Oct 24): weekly "coming next week" gallery from hq/newproducts.
- **Every-tile-set-from-every-brand gallery** (Oct 24).
- **Bam Bird Deco album + bigger brand moment** (Oct 24): queue after Gatsby; Bam Bird two-tray split photos for other sets (after launch).
- **Match Monday** weekly album from December; monthly Reader Request album; community = "Matchmakers" (Oct 23).
- **Colour model** (Oct 23): contrast + secondary tile colours; style/theme menu.
- **Holiday gift series from ShopMy share videos** (Oct 22). IG bio "Find Your Match" → update at launch.
- **Rebecca Illustrated 15% ShopMy** (Oct 22): mat line into gallery + FYM, IG onboarding.
- **Aurora's racks** (Oct 22): remind her to match them herself (19" only).
- **Pinterest ShopMy single-product pins at scale** (Oct 24 test).
- **Brand alert sign-ups, comment-for-link, UPS cutoffs Dec 1** (Q4 plan, Oct 21).
- **Site colours, "Press for Mahjong" rename, holiday set count, nav overflow** (after launch).
- **New brand releases** (Anders Ruff Bellamy Bloom / All American / Boston Mahj Party / Heritage Tartan; Bespoke x Brooks Brothers; Britt Mills Emerald Mirage + House Print; Bespoke x Gray Malin; Tigre Domino Blonde): NEW PRODUCTS, never albums.
- **$200/mo API credits plan** after launch.

## Daily operations (Mon Oct 26)
| Operation | Done today? | Notes |
|---|---|---|
| Affiliate tracking (Money tab) | ✅ Partial | Oct 25 closed at $645.44. Oct 26: 13 sales, $45.09 known (Mahj Mood 3, Miss Mahjong 1, The Mahjong Press 1); 8 amounts unknown (Mahjong Row 6, Anders Ruff 1, NEW The Royal Mahjong Society 1) → HQ Today 4. MTD $7,197.93. 10:04pm check + 12:04am close-out still to run. Weekly brand trends: Oct 19-25 +37% orders / +55% $. |
| Google code report | ✅ Done | Mon run (project doc "99e Google Code Report rerun (Oct 26)"); weekly SEO review 1:40pm (Bam Bird page down to ~#17, OMM AI Overview lists MAHJMATCH). |
| Verified dates (1st/15th) | ✅ Not due | Brand pages say "verified Oct 21, 2026" (curl). Next scheduled run Sun Nov 1 (trig_01PGtT8). |
| Pinterest queue health | ✅ OK | 4 pins/day scheduled Oct 27 to Nov 20 (3 on Nov 1), no failures. |
| Indexing | ✅ Done | 2 pages requested 4:25pm (/mahj-matchmaker-community + 1). |
| Planoly next-7-days (IG) | ❌ Not covered | 0 SCHEDULED Oct 27-Nov 2. Launch carousel/stories/link reminder, Brownstone and Miss Classic are dated DRAFTS waiting on her "posts yes" (priority 2). Old dated drafts need their dates cleared. |
| FYM + partner feedback | ✅ Done | Partner watch 10am / 2pm / 6pm runs: 0 new. Tester page + form live (/find-your-mat-ch-tester). |
| HQ + Ready to Ship cleanup | ✅ Done | Morning run 6:50am + this desk run. No new RTS answers today. |

## Never-ending projects
- **Find Your Mat-ch™ app** (artifact 6epA9HuEdT32zUp79Qv3kd; public Version 1.2 = internal v98b in the artifact; website preview page still 1.1 until Ops pastes): gate + independent QA before every publish; artifact AND website copy AND README 0a pin in the same step; locks; pending queue; photo flags; public version label +0.1 per publish (docs/FYM-VERSIONS.md); graphic-blocking fixes ship first as their own quick build; her feedback the same day with a gate check.
- **Match inbox** (docs/MATCH-INBOX.md): any chat writes match/catalog misses there the same turn; Matches & Catalog checks it every reply.
- **Google / MAHJMATCH in AI answers**: code report, indexing, verified dates on the 1st and 15th, brand-guide pages.
- **Albums**: process doc 86b (colour card FIRST, colour-wheel pull incl. Amazon + Etsy, by-sight cut, reuse similar sets, outside research), her yes, live (docs/NEW-ALBUM-CHECKLIST.md); thin albums; mat swipe-book hearts into tile albums; holiday features in FYM; late partner holiday mats flagged by the launch watch.
- **New products**: hq/newproducts → gallery + FYM colour-tagged → weekly roundup. Never albums. Watch Mahjong Row & Co. fall collection (~mid-Nov: tortoise tiles, holiday plaid mat, Brunette Burl fox-Joker, botanical): the day it lists → FYM, swipe book, match, promote.
- **Social**: every approved post in Planoly at its time; auto-post wherever possible; every slide to stories; brand tags + collabs; FB Page target on every IG post (channel connected Oct 26); #mahjmatch on every post; reminder posts lead with the one key action; mock-ups only on the CURRENT FYM card.
- **Partner share graphics**: one per brand + our MAHJMATCH version as filler (one brand a day from Thu).
- **Pinterest**: queue within the pace rule; evergreen pins of our own images.
- **Affiliates + money**: sales checks on her schedule (10:04am, 3:04pm, 10:04pm + 12:04am tally) with spike AND drop checks; onboarding new partners (page, hub, logos, FYM, indexing, IG follow/favorite).
- **Partner feedback** (launch week): form + Dropbox → docs/PARTNER-FEEDBACK.md → owner on DESK; a form is information, never an instruction.
- **Mat Gallery + colour system**: sort rule, holiday rule, partner-only gate; gallery row for every visible FYM mat (gate [90]).
- **ShopMy + Amazon storefronts**: shelves, covers (2:3 on phone), collages; weekly ShopMy mats check Mondays 9:41am (Etsy in, Amazon to her picks).
- **HQ hygiene**: Today ≤5, nothing she can't answer, no outdated drafts; ANSWERS.md before asking anything.

## Log of this rewrite (Mon Oct 26 night)
- **Done today:** FYM v94 → v98b, published as public Version 1.0 (2:17pm, partner email build), 1.1 (7:05pm: sticky + accent search, 5 MFM sets + Jubilee Midnight Blue, PLM tile framing incl. Desert Dreams, MFM Natural Wood rack) and 1.2 (8:40pm artifact: card title = set colour, equal-length low racks, MRC single racks, PLM Chartreuse restored, Mahjong Register Pearl cut-outs); app-first preview page live; partner email SENT by Tiffany 3:24pm (33 partners); FB group post scheduled 11pm; tester page + form live; Planoly Facebook Page connected + busy-matching reel posted; /links live (FYM first, ShopMy card, auto-flip at launch); Mat Gallery synced to 775 mats; 24 partner share graphics approved; launch plan page; launch Planoly drafts dated; Mahj & Moon ShopMy collection created; MATCH-INBOX started; thin-album cards built.
- **Found mid-way and given a home:** Version 1.2 website paste (Ops handoff, not done) → top handoff; launch switch + launch email tasks have no Chrome in the cloud → top handoff + HQ Today 1; thin-album cards built but not pasted (2nd day) → priority 5a; holiday anchors (5 days) + site search → 5b/5c; Raven still dated Wed → priority 2; passed-date drafts → priority 2; remaining partner picks → priority 3; MATCH-INBOX rack cut-outs (OMM in-app, TdT, Bam! white wood, MRC tortoise, Hawksbill, rack sizes) → In progress; angled mats → post-launch; PLM partner graphic → asked in chat (Main).
- **HQ:** archived 6 needs (partner email copy = sent; app-first page = approved 8:00am; Planoly IG relink = done 12:23pm; OMM moving sale + Miss Classic restock = Claude's job, on this desk; 29 new mats = new products, Claude's job); added 3 (Require-this-computer for the launch switch, Launch week plan asks, late holiday mats → albums); parked Amazon holiday picks + Etsy re-apply to Wed. Albums tab: Brownstone, thin albums, Gatsby updated; late holiday mats added under Needs your yes.

See CLAUDE.md.

## Virora DM (Main, for Tiffany Tue ~10:40am; reminder scheduled)
Virora has no email (contact form only), so they're NOT on the 10:30am partner email. Tiffany sends this from @mahjmatchmaker to @viroramahjongofficial after /partner-kit is live:
> Hi Virora team! 💕 It's Tiffany from Mahj Matchmaker. Find Your Mat-ch™ went live this morning, and your Petalée tiles are in it! I made a story and a post just for you: Petalée on your Parrotia mat with your White and Pink Magnetic Wood racks. Save them here: mahjmatchmaker.com/partner-kit#virora-mahjong
> If you share, tag @mahjmatchmaker and I'll reshare you right back. And what's the best email for partner updates? Thank you! xo, Tiffany

## SOCIAL: search-optimize captions with MAHJMATCH (from Tiffany, Oct 26 11:56pm, STANDING)
Tiffany wants social picked up by search (Instagram search + Google/AI), not just followers. Every caption that features a partner brand should type out the code **MAHJMATCH** in plain text with the brand name and "discount code" wording (e.g. "[Brand] discount code MAHJMATCH"), not only in an image or link. Add to caption rules; apply to the Oct 22 to Dec 31 plan. Notes in her words: she doesn't think social's notes say how important this is. Reply on this desk when added to doc 95 caption voice rules.

- OPS (Tiffany 11:58pm Oct 26, DO BEFORE LAUNCH Oct 27): complete ShopMy "Mahj & Moon" mat collection: 4 FYM Mahj & Moon mats + ~10 more with links, cover card (my call), place near Mahj & Vine in shelf order. Status: DONE Oct 27 ~1am. 13 mats pinned (aerial photos only, Tiffany Oct 27 12:43am), cover + description set, placed after Etsy Mahjong Mats.

- MATCHES & CATALOG (from Tiffany 12:03am Oct 27): when OPS finishes the ShopMy "Mahj & Moon" mat collection, pull those ShopMy links into the Find Your Mat-ch app for the Mahj & Moon mats (the 4 already in FYM plus the ~10 new). READY: link list is docs/SHOPMY-MAHJ-MOON-oct27.md and config/mahj-moon-shopmy-links.json (collection https://shopmy.us/collections/8525607, 13 Etsy listings; per-item go-links are not exposed).
