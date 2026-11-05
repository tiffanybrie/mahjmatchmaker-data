# The Desk
Rewritten nightly by the end-of-day desk cleanup (9:23pm ET). The morning HQ cleanup (6:47am ET) reads it. Rules: CLAUDE.md ("THE DESK"), docs/CHATS.md (which chat owns what). During the day, when an agent stops, Chrome drops or a QA stalls, add the item here right away with its next step.

**Last rewrite:** Wed Nov 4, 2026, ~9:55pm ET (desk cleanup run, cloud, no computer linked). Covers the 40 commits of Nov 4 ET (fe0c4a7 … 0953453; Main stopped committing at 3:57pm, two launch/partner watches after), docs/ANSWERS.md (Nov 4 lines 951-970), docs/MATCH-INBOX.md, Planoly (IG workspace 019fc27c…: 20 groups, export docs/social/planoly-exports/ig-2026-11-04-desk.json; Pinterest 019fc27b…: 3-4 pins/day scheduled through Nov 30), HQ needs (18 open → 15) / hq/albums / hq/now / hq/priorities / hq/social / log (22 entries today), Ready to Ship (NOW list: all 6 answered, nothing waiting), config/release-calendar.json, content_lint (repo + Planoly IG export), curl checks (Amanda Toppe, hub, Wren, Mahj Pit, /mahjong-tile-matches, /links, /find-your-match).

**Owners (three chats, Oct 22):** Main (Opus) = social/Planoly, site pages, email, HQ/DESK, decisions, Google + SEO. Matches & Catalog (Opus) = Find Your Mat-ch, albums, gallery, catalog, search index. Ops (Sonnet) = the ONLY Chrome driver: Squarespace pastes, uploads, IG follows/checks.

**Repo note:** checkout on `partner-catalogs-sqsp` (~4.7 GB with assets). A plain fetch hangs (tonight it died with "early EOF" after 2 min). Working recipe: `git fetch -q --depth=60 origin partner-catalogs-sqsp:refs/remotes/origin/partner-catalogs-sqsp` then `git checkout -B partner-catalogs-sqsp origin/partner-catalogs-sqsp` (~1 min). Never `git ls-tree -l` on a blobless clone.

**PARTNER SEND GATE (Oct 27 3:08am, standing):** before scheduling ANY partner email or graphics drop, run `python3 scripts/partner_send_check.py`; it must exit 0.

**Standing from today (Nov 4, in CLAUDE.md / ANSWERS):** A YES IS A YES (never re-confirm a swipe/picks/HQ/chat yes) · BLOCKED IS NOT DROPPED (approved-but-blocked work sits in "Blocked, approved" below and every attended chat raises it at the top of its reply) · REVENUE WATCH (brand week-over-week daily, docs/REVENUE-WATCH.md; a falling brand gets an investigation the same day) · NO 'ASK ONCE' (ask, move on, COME BACK until she answers) · SOCIAL 13: nothing disappears from Planoly, past-dated drafts roll forward nightly · a partner launch found by the launch watch gets its FB group post drafted the same day (posted once the brand announces) · payouts are CASH via PayPal (a few Venmo), only Maison Mahj is store credit · ShopMy pickup DAILY 9:02am · Chrome: no saved tabs; Claude opens/closes its own (docs/CHROME-SETUP.md) · IG evergreen codes post = the ONE IG post with every code typed (overrides the Oct 30 rule for that post only).

## Tomorrow's top priorities (Thu Nov 5), in order
Standing order: RESTOCK FIRST (rule c), then Google #1 (Tiffany Oct 29 11:03pm), then the newest ANSWERS (FYM tracking, holiday follow-through, Planoly week, FYM 1.15 + Mahj Pit), then DESK 'Never-ending'. **Restock check (c): no album-set restock is dated Thu Nov 5** (Thu: Mahj Mood Playing for Keeps subscriber preorder; not an album set). Next dated: Fri Nov 6 Mahjong Row 2 tile sets 10am CT + Bam Bird MCM Olive restock 10am CT + Mahjong Moxie tiles 12pm CT + Mahj Mood public preorder (none is an album set); Virora Lilacée Nov 10; OMM Juniper + Lotus Cove Wed Nov 11 10am CT (Juniper album = Claude's picks waiting on her). The order is clear, so no "Set tomorrow's order" card.

1. **Google (Ops with Chrome, Main checks). OVERDUE 3 DAYS, first thing.** (a) Live site STILL says **Amanda Toppe 20%** (curl 9:50pm tonight): /amanda-toppe-discount-code SEO title + meta/og/twitter description ("Amanda Toppe Discount Code: 20% Off…", "Save 20% at Amanda Toppe Living…") + body "for 20% off at Amanda Toppe checkout"; hub /mahjong-discount-codes "Amanda Toppe: 20% off with MAHJMATCH" (ItemList), "Amanda Toppe (20% off with MAHJMATCH)", "20% at Amanda Toppe" (FAQ). It is 10% (Tiffany Nov 2 ~9am). The hub was edited today for Mahj Pit and this was missed again. Fix every spot (page settings SEO title/description too) + repo config/hub-at-a-glance.html + assets/search/search-index.json + FYM brand note; curl-verify 0 "20%" for Amanda Toppe; request indexing for both. (b) **Wren Mats page still "Verified: October 9, 2026"** (curl tonight; indexing run skipped it): set to the current verified date (standing authority), then request indexing. (c) Morning report Thu (OMM still not named; 3 brands lost Wed: Soirée first in the indexing queue, Bam! Let's re-crawl requested, Tigre de Tartán = image-only code by their policy). (d) Indexing: Soirée, Middle & Main, Noli June, Virora, Mahjong Co, Royal, Register, YOLO (waiting since Nov 2) + Mahj Pit page + hub. Code report next due Fri.
2. **DONE Nov 5 10:25am: FYM 1.15 LIVE in all 3 places** (artifact Version 113; /find-your-match + /find-your-mat-ch-preview pasted, curl = fym-v115, page-block @cc0de626; live phone test: Version 1.15, TRK_URL set, 2 Juniper swipes sent a beacon POST -> 302 -> 200 = 2 test rows 'left' set juniper in the tracking sheet, from Claude's test). Remaining from 1.15: Mahj Pit RACKS (6b review), Mahj Pit in Mat Gallery, Spring Love + Shangri-La. ~~[Nov 5 ~4am] FYM 1.15: QA PASSED (2 rounds); live artifact PUBLISHED (Version 113); README pin bumped to app @57f0b4e6. BLOCKED, APPROVED: Squarespace paste of site/livepatch/fym-preview-oct21/page-block.html on /find-your-match + /find-your-mat-ch-preview (Chrome offline; she said do it tomorrow), then fym_snapshot.py refresh + confirm a phone swipe lands a row in the tracking sheet. Earlier: FYM 1.15 (v115) BUILT, gate PASS ([104] pin warning only): TRK_URL ON + the 2b catalog adds. QA r1 fixes in (Isla twin, Turkey Dinner/Flower Shop/Poppylicious photos, gate [158]). Website copy site-app/fym-v115 @57f0b4e on fym-site-preview (assets @a3cba38, all 16 jsDelivr 200). Preview artifact 5QjNXjw15MuZTqzDT1ptbp v29 (artifact at the 256 MiB cap: only the 21 Mahj Pit mats + 8 tile sets fit; the other 49 v115 mat adds are website-only, as v113). NEXT (Main): independent QA on the WEBSITE copy (390 + desktop), then publish live artifact 6epA9HuEdT32zUp79Qv3kd from pub115 (builder/fym_fix_nov05/artifact115.py, command in its docstring) + README 0a pin + Squarespace, fym_snapshot refresh, confirm a phone swipe lands a row in the Find Your Mat-ch Tracking sheet. Still open: Mahj Pit RACKS (rule 6b white+navy review), Mahj Pit tiles/mats in the Mat Gallery, Spring Love + Shangri-La Santa Baby yeses (vault sets, not FYM sets).** 2. **Find Your Mat-ch: tracking into the live app, then 1.15 (Matches & Catalog). Blocked, approved since Oct 17; endpoint live since Nov 4 2:25pm, NOT applied** (live /find-your-match still pins fym-v114, built Nov 3 before the endpoint). (a) Apply TRK_URL (config/fym-tracking.json; builder/fym_track_oct17.py) and release to BOTH places + README 0a pin; gate [157]; confirm a real phone swipe lands a row in the "Find Your Mat-ch Tracking" sheet. (b) Then the 1.15 catalog build: **Mahj Pit catalog (gate [114] 24h mark = Thu 3:40pm ET)**, OMM Juniper tiles + Lotus Cove mat, Noli June FA LA LADIES ×4, LBB Electric ZigZag + Christmas Lights + Camellia Kaleidoscope + the 8 Nov 3 LBB mats, Bespoke Sunshine Glow (LIVE Nov 4) + It's a Vibe Glitter Glow Green, 33 ShopMy Etsy mats, Britt Mills Isla, TdT House Tigers Oyster, Splash Santa Baby's Cocktail Hour mat + the late-holiday m-lists (config/late-holiday-picks-nov03.json + swipe-yeses 'santababy'), OMM Esme → retired (gone from OMM Nov 4). Gate + independent QA, snapshot refresh. Mahjong Row Moody Tortoise + Brunette Burl the moment product pages exist (Fri 10am CT latest).
3. **Planoly (Main). 0 IG posts SCHEDULED in the next 7 days (rule d), and Wed's posts did not go out.** (a) **Roll forward Wed Nov 4 (SOCIAL 13):** Polo Club reel reminder 01a16476-febc + its FB reel 01a1a2b7-3d0e + Polo 7-frame story reminder 01a16477-0078 → Thu Nov 5 (set_post_group_schedule; tonight's unattended run was refused that permission, so Main does it), and the New this week story 01a1a2b6-7c1e + the undated New this week carousel 01a19e04-1f13 get "📅 Planned: Thu 11/5" as the first caption line. (b) **Story-caption lint, 3rd day:** content_lint --planoly FAILs on all 8 story drafts (no MAHJMATCH typed + no #MahjMatch: 01a1a2b6-7c1e/-73c0/-7707/-7a67, IG + FB each): add the code line + #MahjMatch, or exempt story captions in the lint. (c) The IG evergreen codes post 01a1a859-bcb8 FAILs Planoly length (1,993 chars): it is her approved one-off exception (ANSWERS Nov 4 3:55pm), so add its id to the lint allow-list; it has no FB target on purpose (Oct 30 rule) and no Tag people (39 brands > 20 tag limit: fine). She taps Post. (d) Polo + Rudolph 7-frame sticker-story reminders (01a16477-0078, -03c8) still have no FB Page target (their reels' FB versions are separate groups). Default kit if she gives no yes by Fri: album-of-the-week kit from the Friday social prep task.
4. **Holiday + site follow-through (Main → Ops).** (a) New-albums email for the holiday albums (NEW-ALBUM-CHECKLIST §4; template OK'd; build the draft in Squarespace, she does the final read: drafts only, Oct 24 rule). (b) **Work With page v3 + Brands form goes live TODAY** (her stated default since Nov 1; HQ Today; site/livepatch/workwith/README.md) unless she says wait. (c) **7 quick-call defaults went ahead Wed** (needs/site-maint-2026-11-b, no reply = defaults): Ops applies them (OMM Emerald + Pearlescent Retired labels, Bama Mahj as non-partner, Brownstone keeps 3 retired OMM mats, etc.) and Main rebuilds the **Nov 2 monthly site check** into git from the HQ log (36 dead links, 73 newly Retired cards). (d) Ops: FB Page intro still says "Find Your Match (coming 10.27)" → live line.
5. **Match inbox + catalog backlog (Matches & Catalog), rule e.** 81 dated lines older than Nov 2 have no DONE (14 say FIXED/LIVE inline: mark DONE with proof first), plus every Nov 3 line is now 2 days old (8 LBB Nov 3 mats, Bespoke Glitter Glow, Lotus Cove, Juniper, LBB renamed handle, Mahjong Row, FYM racks-step gap, Rackin' Rudolph empty tile circle on v113 cards, Camellia Kaleidoscope, OMM all-in, Noli ×4): most close with 1.15 (priority 2). Also: 8 TNT recs from the Nov 3 scan not in config/tnt-recs.json; Ops TNT searches for Juniper, Bespoke Sunshine Glow, Glitter Glow Green.

## Handoffs (do first)
- **OPS + Matches & Catalog (morning report Nov 5): The Mahjong Co. shop is empty** (1 product, sold out; our mat links 404; 0 orders in 8 days). Wait for Tiffany's answer on HQ alert-revenue-mahjong-co-2026-11-05, then retire/hide their mats and fix the /mahjong-co-discount-code links. Also: Amanda Toppe 20% is now quoted by Google's AI answer ("MAHJMATCH: Save 20%"); priority 1a is urgent.
- **Matches & Catalog: SUNDAY ALBUMS OVERDUE (Tiffany Nov 5 12:21am HQ box: "Why aren't these albums made if I swiped over a week ago. Albums keep falling off"; she re-opened the Sunday Sets book WJT7jTYfXX45917UkEqKyq and got all 121 mats with her old Sunday Blues answers again: confusing).** Build Sunday Blues, Nature Walk, Plum Panda, Hummingbird album cards from her EXISTING yeses (book db votes), then give her ONE short page with ONLY mats added since her swipe (never the full book again). Owner Matches & Catalog, date **Fri Nov 6**. HQ: needs/sunday-moody-mats = 'Overdue, Claude's job' (no ask); hq/albums Sunday x4 owner claude, group building. Re-point the HQ card to the new-mats page when it exists.
- **Main: OMM Juniper mentor presale is 'tomorrow'** (Tiffany Nov 5 12:22am HQ box, from the mentor-group comments: Thu Nov 5 or Fri Nov 6). Confirm time in the mentor group; make sure FYM 1.15 (Juniper + Lotus Cove) is on the website by then (Squarespace paste, blocked on Chrome) and decide on a presale group post per the Papaya precedent. HQ card launch-juniper-mahjong-tiles updated.
- **Matches & Catalog: Lotus Cove swipe book (L8teRCj5w9ncskZYkwNEoZ) + every open book: show FULL mat names and brands** (Tiffany Nov 5 12:42am, standing; book_gate [n]). Fix the CSS before she swipes; re-run book_gate.
- **DONE Nov 5 10:15am (Matches & Catalog): search Code Injection now @98e58057 (curl verified both lines).** ~~OPS (or any attended chat with Chrome): site search fix into Code Injection. Blocked, approved (Nov 5 12:35am, Chrome offline).~~ Squarespace > Settings > Developer Tools > Code Injection > Header: in the existing search lines replace commit `6a8c34900885f4f127abd58f60817da46ba84ac7` with `98e580577e285311fc3ad237ef6dc5f98c5eaf02` (both the .css and .js line; leave MM_SEARCH_LOG_URL and everything else). Pinned + warmed (site/livepatch/search/header-injection.html). Fixes: '+N more' albums now open in place; See in gallery keeps the mat centred while the phone gallery loads. Check: ?mmq=dapper%202 on a phone, tap +6 more, tap See in gallery.
- **Main: blog posts name tile sets that have albums but don't link them** (Tiffany Nov 5 12:29am: 'when you said something was in an album it just sent you to the albums page'). Live audit Nov 5: christmas-mahjong-sets (Heritage, Emerald), mahjong-buying-guide (Amara, Pearlescent, Heritage, Smith; its 3 'tile match albums' links go to the index), mahjong-tile-set-details-to-know (Pearlescent, Heritage), most-versatile-mahjong-tiles (Amara, Glow Wild, Sierra, Smith, Talulah, Cypress Forest), my-favorite-yellow-orange (Pippa), my-favorite-mahjong-racks (Heritage), my-favorite-blue (Osler), my-favorite-green (Lagoon), most-versatile-mahjong-mats (Seabreeze, Papaya Spritz), pearlescent-tiles-heron (Sorbet). Rule: every set named in a post links its own album (/<set>-mahjong-tile-matches); the index link is only for 'browse every album'. (Palm Royale hits are the mat, check by eye.)
- **OPS: Amanda Toppe 10% everywhere + Wren verified line** (priority 1a/1b). Overdue since Nov 2 9am.
- **Matches & Catalog: TRK_URL into the live app** (priority 2a). Blocked, approved.
- **Matches & Catalog: Mahj Pit catalog into FYM + Mat Gallery within 24h** (MATCH-INBOX Nov 4 3:40pm; gate [114]; due Thu 3:40pm ET).
- **Main: Planoly roll-forward + story lint fixes + codes-post lint allow-list** (priority 3).
- **OPS: follow + favorite @mahjpit.co**, log in docs/IG-FAVORITES.md (new partner Nov 4).
- **Main: launch reel redo** (assets/social/fym-launch/redo-nov03/launch-reel-redo.mp4, 58s) stays at the TOP of HQ "for you" (her Nov 4 2:31pm); on "send me the launch reel": file + swap/pin steps in chat; Claude does the FB Page.
- **Main (launch watch): Mahjong Row Moody Tortoise + Brunette Burl**: group post LIVE Nov 4 2:40pm with no links; watch mahjongrowandco.com/products.json → edit the first comment with the links + hand to Matches & Catalog for FYM before Fri Nov 6 10am CT.
- **OPS (Nov 3 launch watch): copy flat renders to Dropbox /Mahj Matchmaker Albums/New releases/** (OMM Lotus Cove + Juniper, 8 LBB Nov 3 mats, Bespoke Glitter Glow Green, Nov 2 leftovers: Bespoke Sunshine Glow, Britt Mills Isla, LBB Electric ZigZag + Christmas Lights). Chrome method: ANSWERS Nov 1 12:50am.
- **OPS: Tiles & Tablescapes searches** for OMM Juniper, Bespoke Sunshine Glow, Bespoke It's a Vibe Glitter Glow Green.
- **OPS: minimahjer.com store-wide / Black Friday code check** (from Nov 3; curl 429).
- **Main: Mahj Mood code check** (unused codes expire after 4 months) before the Playing for Keeps public preorder Fri Nov 6 10am CT (subscribers Thu).
- **Main: GoAffPro order drop** (Nov 1-4: 3 orders vs 24 Oct 25-28; clicks -27%, orders -88% = code-typed Google orders fell, not tracking; ANSWERS Nov 4 1:47pm): REVENUE-WATCH investigation per brand (Mahj Mood, Miss, Peace Love, Virora) in tomorrow's morning report.
- **Matches & Catalog: brand-lock FYM sample for Bird & Bamboo (Emily)**, hosted embed only (docs/brand-lock/STATUS.md).
- **Matches & Catalog: FYM 1.12 follow-ups still open:** nightly stock check publish path; rack cut-out review for the 12 hidden racks; Mat Gallery rows (gallery_rows112.py); two-colour coordination ranking bonus.
- **Main: launch + partner watch prompts** must check the storefront page for "wholesale customers only" (Nov 3) and draft the FB group post the same day for a partner launch (Nov 4 rule gap). Add at next prompt edit.
- **Main: sales-check prompt fix** (ALL secomapp + goaffpro + backinstock emails, refunds on the refund date, tiffanybrie@ at /mail/u/1; repo clone step). Not applied.
- **Main: "close leftover finished Claude tab groups at start"** in every Chrome task TAB RULE (Oct 30). Not done.
- **Main: mat-edit-alert build step** in launch watch trig_01S2VsjwznnHev1uUbYmEwJq (Oct 30; docs/MAT-EDIT-ALERT.md). Not done.
- **Main: duplicate catch-up tasks** trig_019StaM8LkmrxGKtK7xhXang + trig_013ZpyRxFivSKPoYTgSvVBU6: pausing one is her call (HQ rules-audit-2026-10-30).
- **Main: config/pinterest/queue.json shows only 15 scheduled (Nov 5-14) while Planoly has 3-4/day through Nov 30**: resync queue.json from Planoly at the next autopin run.
- **OPS (standing): HQ ShopMy tab inbox** (db `shopmy`, status new) at the start of every Ops reply.
- **Partner feedback watch** trig_01RKw9eUwTYPo39gbYHb65gh runs daily through Nov 10 (0 new Nov 4).

## In progress
| Item | Owner | Next step | Target |
|---|---|---|---|
| Google: Amanda Toppe 10%, Wren verified line, indexing queue (8 + Mahj Pit), 3 lost AI answers (TdT, Bam! Let's, Soirée) + OMM | Ops + Main + tasks | Priority 1. | Thu Nov 5 |
| FYM tracking TRK_URL into the live app | Matches & Catalog | Priority 2a: release both places, confirm a sheet row. | Thu Nov 5 |
| FYM 1.15 (Mahj Pit, Juniper, Lotus Cove, Noli ×4, LBB ×11, Bespoke ×2, 33 Etsy, Isla, Oyster, Santa Baby + holiday m-lists, Esme retired) | Matches & Catalog | Priority 2b: one build, gate + independent QA, both places + pin + snapshot. | Fri Nov 6 (Mahj Pit by Thu 3:40pm) |
| This week's IG posts (Planoly drafts Thu-Sun + rolled Wed) | Main | Roll forward, story lint fixes; she reviews in Planoly; "send me X" → file + steps in chat. | Thu Nov 5 |
| IG evergreen codes post (Planoly 01a1a859-bcb8) | Tiffany taps Post / Main | After it posts: drag to the bottom of the grid (her Meta One), Claude keeps the caption current in Chrome; morning report checks "<brand> discount code" for an @mahjmatchmaker result. | When she posts |
| Holiday new-albums email | Main | Squarespace draft; her final read. | Thu Nov 5 |
| Juniper album (Claude's own 12 picks, her ask Nov 4 3:27pm) | Tiffany → Matches & Catalog | She says which to keep (HQ This week; https://claude.ai/artifact/3ezNyhHbUzDz5J6d24iV1p); then cards + album page live with the Nov 11 launch. | Mon Nov 9 (launch Nov 11) |
| Lotus Cove swipe book (L8teRCj5w9ncskZYkwNEoZ) | Tiffany | She swipes (HQ This week, OMM card). | Before Nov 11 |
| Work With v3 + Brands form | Ops | Goes live Thu (her default) unless she says wait; curl-verify. | Thu Nov 5 |
| 7 quick-call defaults + Nov 2 site check rebuild | Ops + Main | Apply defaults; rebuild site check from HQ log into git. | Thu Nov 5 |
| Mahjong Row Nov 6 drop (2 tile sets) | Main + Matches & Catalog | Group post live; add links + FYM when pages exist. | Fri Nov 6 |
| Payout reconcile pass 2 | Main (Chrome) | Real payout terms per program → config/payout-terms.json; re-split Oct $4,093 "approved, not yet due"; HQ Money "Payouts" section; PayPal signed in. Design Mill = Britt Mills (resolved). | Fri Nov 6 |
| UpPromote accounts → mahjmatchmaker@ | Tiffany (started, Mahj Squad no reply yet) / Main | Screenshots before each switch; Bird & Bamboo next. | This week |
| Holiday colour cards (Tinselle ×2, Dec 1994, PLM Spirit + Nutcracker) | Matches & Catalog | Not started (was due Oct 31). | Mon Nov 9 |
| My Fair Mahjong Style of Your Life (#1 album) | Matches & Catalog | Colour card + TNT, then swipe book (Wed target slipped). | Mon Nov 9 |
| Holiday album covers page update | Matches & Catalog | Late picks are live; covers next. | Fri Nov 6 |
| Hummingbird holiday section (hidden) | Matches & Catalog | Stays display:none until the Hummingbird / Sunday Sets album goes live; then un-hide + album holiday section. | With Sunday Sets launch |
| Sunday Sets TNT rec leftovers | Matches & Catalog | docs/research/sunday-sets-colorcards-tnt-oct29.md. | Fri Nov 6 |
| Larkspur hearts into 27 tile albums | Matches & Catalog → Ops | Paste album by album (0 of 27). | Fri Nov 6 |
| December 1994 redo (her RTS notes) | Matches & Catalog | After holiday colour cards. | Mon Nov 9 |
| Holiday reels redo (Nutcracker/FYM reel with Table view) | Main | v5 standard; storyboard first. | Fri Nov 6 |
| Bam Bird Deco trio (Indigo first) | Matches & Catalog | Colour cards ×3, then books. | Week of Nov 9 |
| Brand-lock sample for Bird & Bamboo | Matches & Catalog | Hosted embed only. | Week of Nov 9 |
| Affiliate applications (apply kit) | Tiffany submits / Main | Kit doc 00h; HQ apply-kit-oct31. | This week |
| FB group weekly Claude Doc | Main | https://claude.ai/artifact/54ovPaB6BQU78ztjUgQSbe; add the Nov 4 posts (Mahjong Row, OMM Juniper, holiday albums, FYM holiday). | Thu Nov 5 |
| Tortoise rack piece (her Oct 28) | Main | Scope + storyboard; gift-guide tie-in. | Fri Nov 6 |
| Discount links not converted (Britt Mills, Mahjong Register, YMI, RMS, Hip Hip, Wren/Soirée/Amanda Toppe) | Main | builder/fym_fix_oct21/discount_check_oct21.json. | Fri Nov 6 |
| Amazon mats into gallery + FYM | Ops → Matches & Catalog | Her pick (1, HQ This week). | Fri Nov 6 |
| ShopMy holiday leftovers | Main → Ops | ShopMy (not MAHJMATCH) for Charleston Mahjong Club + Bamlet's in holiday posts. | Fri Nov 6 |
| Fait à Main code | Main | MAHJMATCH still not applicable at cart. | Watch |

## Blocked, approved (raise at the top of every attended reply until done)
- **FYM tracking TRK_URL into the live app** (Matches & Catalog): approved Oct 17, endpoint live Nov 4 2:25pm, v114 release with it did NOT happen Nov 4. Priority 2a.
- **IG EVERGREEN CODES POST** (Main, her plan Nov 4 3:55pm): ONE grid post, Partner Brands graphic + every code typed in the caption, moved to the very bottom of the grid (her Meta One drag), caption kept current by Claude in Chrome on instagram.com. Draft in Planoly 01a1a859-bcb8 (auto-publish scheduling blocked for Claude; she taps Post). NOT on the FB Page; no Tigre de Tartán / YMI typed.
- **PAYOUT RECONCILE PASS 2** (Main): needs PayPal + each dashboard signed in; then HQ Money "Payouts" section from collection payouts. Kathrine Zell $3.15 Oct 15: Tiffany checking her email. Peace Love $402.88 store-gift-card payout: she fixes the GoAffPro setting herself.
- **Planoly roll-forward** (Main): tonight's unattended run was refused `set_post_group_schedule` (external write), so the Wed Nov 4 drafts are still dated Wed. Priority 3a.
- **UpPromote Marketplace + Bird & Bamboo dashboards signed out** (blocks amounts + Google alert follow-up): her sign-in (HQ Today, Google alert card); Ops reads them right after.
- **Mahjong Row product links** (Main, launch watch): edit the group-post comment + FYM the moment pages exist.

## Waiting on Tiffany (only things she can answer now)
**On HQ Today, in this order (5):**
1. **Google alert: sign back in to UpPromote Marketplace + Bird & Bamboo in Chrome** (1 min).
2. **Launch reel redo: watch it** (stays on top until she gets to it; "send me the launch reel").
3. **This week's posts in Planoly** (Wed's Polo Club reel + New this week roll to Thu; Dear Santa Thu; the evergreen codes post is hers to tap Post).
4. **Work With page v3 + Brands form: goes live today unless she says wait.**
5. **Amounts: My Fair ×3 + Bam Bird ×1 from Nov 4** (type them, or sign in to those dashboards).

**On HQ This week:** Sweet Jojo W-9 (moved from Today); Juniper: Claude's 12 picks (which to keep); My Fair Black Friday "shop through our link" yes/no; 2 quick FYM checks + Holy Mahj; Sunday Sets round 2 (4 sets); OMM Juniper + Lotus Cove (swipe Lotus Cove before Nov 11); affiliate apply kit; 1 hidden FYM photo (Grace Peacock); 1 Amazon mat to pick; ShopMy 5 quick calls + 2 stray links.

**Asked in chat, not yet answered: the owning chat RE-ASKS at the top of every reply until answered, with its default:**
- Main: **separate Google/revenue chat?** (Nov 4 ~2:20pm; Claude recommends yes; default: keep it in Main until she says); Malachite how-to reel v2 OK + day; FB group B&B racks wording.
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
- **Per-brand IG code posts / reels**: not now (her Nov 4 3:55pm pick = one evergreen post); revisit if the evergreen post doesn't show in Google (Nov 4).
- **Tiffany's Takes editor** (DkRn8W5qaMBxHfqqeJVE8V) data is from Oct 10 (37 albums): refresh with Brownstone + holiday albums when she wants to write takes (offered Nov 4 1:45pm).
- **Maison Mahj House Line No. 1** public preorder ($595, Nov 4), **Bougie Mahjong neoprene versions** of 5 mats ($80/$90, non-partner), **My Fair Mega Swirl Dice** ($40, accessory), **Splash of Color tile set** ($285), **Anders Ruff 'new product' reel tease**: record only (watches Nov 4).
- **Mahjong Moxie Moxie Tiles** (first tile set) LIVE Fri Nov 6 12pm CT: non-partner except Duck Camp/Heron Landing mats; record only unless she says.
- **Clean up 52 legacy caption lint warnings** (still 52 Nov 4) (config/social/content_lint_baseline.json; mostly missing #MahjMatch, '(affiliate)', 2 TdT captions) (rules audit E9, Oct 30). Also 78 legacy FAILs (length 42, naming 36) in banked Season 2 captions: same kinds as yesterday, nothing new.
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

## Daily operations (Wed Nov 4)
| Operation | Done today? | Notes |
|---|---|---|
| Affiliate tracking (Money tab) | ✅ Done | 1:37am close-out (5 late Nov 3 sales, 33 emails reconciled); 2:04pm run: 6 sales (My Fair ×3 + Bam Bird ×1 amounts unknown → HQ amounts card), Tigre refund -$15.75, 9 emails reconciled; My Fair spike (its early Black Friday). GoAffPro drop checked (orders -88%, not tracking). Payout reconcile first pass (docs/reports/payouts/2026-11-04.md). Midnight close-out still to run. |
| Google code report | ✅ Done | Wed run 12:00-1:05pm (Project doc 99i): AI Overview 20/38, AI Mode 34/38; feedback sent. Next due Fri. |
| Morning Google report | ✅ Late | Ran 12:05-1:25pm (7:13am missed, catch-up). 27/38 AI answers (-1: lost TdT, Bam! Let's, Soirée; gained My Fair, Amahj; OMM still not named); SC 7-day 625 clicks (+242%). HQ alert card. |
| Verified dates (weekly, Mondays) | ❌ Miss | Not due Wed, but Wren still "Verified: October 9" (priority 1b). |
| Codes post (Mondays) | ⏭ Not due | FB group codes post went up Tue. IG evergreen codes post drafted in Planoly for her (Blocked, approved). |
| Pinterest queue health | ✅ OK | Autopin 7 published, 0 failed. Planoly Pinterest: 3-4 pins/day scheduled Nov 5 → Nov 30. queue.json out of sync (handoff). |
| Indexing | ✅ Done | 10 changed brand pages requested 12:08pm (built-in browser); Wren skipped; 8 waiting since Nov 2 (Soirée first). Mahj Pit page + hub to request. Amanda Toppe was re-requested while still saying 20%: request again after the fix. |
| Planoly next-7-days (IG + FB Page) | ❌ Not covered | 0 IG posts SCHEDULED Nov 5-11 (all drafts for her review); Wed's Polo Club reel + New this week not posted and not yet rolled (permission refused tonight). Planoly lint 19 FAIL: 16 story-draft captions (no MAHJMATCH / #MahjMatch), 2 banked Retro Rattan reel, 1 codes post length (approved exception). FB targets: all feed groups have one; codes post none by rule; Polo + Rudolph sticker-story reminders none. Priority 3. |
| New albums (last 7 days) (f) | ✅ All checks | Brownstone Bloom (live Nov 1): /mahjong-tile-matches ✅, /links ✅, Pinterest queue ✅, colour + brand pages ✅ (Nov 3), indexing ✅ (Nov 2). Nov 4 late holiday picks went onto existing albums (not new albums). |
| Repo caption lint (g) | ⚠️ Legacy only | 78 FAIL (length 42, naming 36), all banked Season 2 captions; 52 legacy WARN. Same kinds as yesterday, nothing new. |
| Restock first (c) | ✅ Checked | No album-set restock dated Thu. |
| Match inbox (e) | ⚠️ 81 old open + Nov 3 lines aging | Priority 5. |
| Launch + partner watch | ✅ Done | Launch watch 8:57am (3 new) + 5:57pm (1 new, Splash record-only); partner watch 9:45am, 1:35pm, 6:40pm (Bespoke Sunshine Glow LIVE 9:58am; Bougie neoprene, MFM dice); mentor group confirms Juniper + Lotus Cove 11/11 10am CT. |
| FYM + partner feedback | ✅ Done | 0 new (2:25pm). |
| FYM releases | ❌ None | TRK_URL not applied; 1.15 not built (priority 2). |
| Social posted today | ✅ FB group | Mahjong Row drop post (2:40pm), OMM Juniper + Lotus Cove post (2:55pm), holiday albums post + FYM holiday post (~4:10pm), each with first-comment links. Nothing on IG. |
| HQ + Ready to Ship cleanup | ✅ Done | Morning 6:59am, sweeps 9:48am / 1:47pm / 7:47pm; this desk run 18 → 15 open, Today 5. RTS NOW: all 6 answered. |

## Never-ending projects
- **Find Your Mat-ch™ app** (artifact 6epA9HuEdT32zUp79Qv3kd; public **Version 1.14** = v114 (tracking NOT in it yet): website pin fym-v114 @be2ab101, page-block c1a73bd2 on /find-your-match + /find-your-mat-ch-preview, verified by curl Nov 3): gate + independent QA before every publish (QA loads the WEBSITE copy as live: 0 broken images, gate [115]); artifact AND website copy AND README 0a pin in the same step; +0.1 version label (docs/FYM-VERSIONS.md); her feedback the same day with a gate check; when a publish/paste fails, MESSAGE HER right away. Artifact file budget: run builder/fym_artifact_fit.py and publish ONCE. Every nav/header change: screenshot live at 1280, 1440 and 390 with the phone menu OPEN. New partner catalog in FYM within 24h of its inbox line (gate [114]). Refresh config/fym-mats-snapshot.json after every publish.
- **Match inbox** (docs/MATCH-INBOX.md): any chat writes match/catalog misses there the same turn; Matches & Catalog marks DONE when shipped.
- **Google / MAHJMATCH in AI answers (her #1)**: AI Overview + AI Mode per partner, code report (Mon/Wed/Fri), daily morning report, indexing (brand pages first), sitemap health, weekly verified dates + hub date, weekly codes post (FB GROUP only typed out; IG/FB Page = logos graphic + short caption), alarm on any lost citation.
- **Albums**: order (her Oct 28 3:31pm): MFM Style of Your Life → Bam Bird Deco trio (Indigo first) → Sunday Blues → Sunday Nature Walk → Middle & Main Peach and Pine, Mac + Miller; Mahjong Row fall + OMM green set (Juniper) jump the line; a known restock goes FIRST. Doc 86b (colour card FIRST), book_gate.py, PICKING-RULES.md, NEW-ALBUM-CHECKLIST.md (incl. the new-albums email).
- **Holiday (Merry Mahjong)**: intro reel posted Nov 3; next = late picks into holiday albums, holiday albums + FYM holiday group posts, new-albums email; docs/MERRY-MAHJONG-BRIEF.md + docs/plans/holiday-calendar-nov-dec.md; promote FIND YOUR MAT-CH, not albums (her Oct 30); any FYM social shows the tool working; storyboard before render; song shortlist on every reel; FYM-REEL-RULES 23-41.
- **New products**: hq/newproducts → gallery + FYM colour-tagged → weekly roundup. Never albums. New-mat social = "Match up <mat> in Find Your Mat-ch", never ahead of the brand; wholesale-only/unannounced = confidential.
- **Social** (docs/SOCIAL-SYSTEM.md, ~2 hrs/week of her time): every planned post as a Planoly DRAFT on its day (final media, lint PASS, Tag people, FB Page target, story version); she reviews in Planoly; FB Page target on every IG group; every slide to stories; brand tags + collabs; restocks/launches SAME DAY or never; ≥4 IG posts in every next-7-days window.
- **Facebook group**: community, never ads; weekly codes post (doc 94); weekly Claude Doc of planned posts; @everyone at most ~once a week.
- **Partner share graphics**: one per brand + our MAHJMATCH version (39 logos as of Mahj Pit, Nov 4: assets/hub/partner-brands-2026-11-04.jpg).
- **Pinterest**: queue within the pace rule; evergreen pins of our own images.
- **Affiliates + money**: sales checks 2:04pm + 12:04am, reconcile every referral email (both inboxes), refunds on the refund date, spike AND drop checks; onboarding new partners (page, hub, logos, FYM within 24h, indexing, IG follow/favorite); affiliate applications (kit doc 00h).
- **Mat Gallery + colour system**: sort rule, holiday rule, partner-only gate (plus her Oct 31 non-partner picks), shop-by-colour partners first (Oct 31); gallery row for every visible FYM mat (gate [90]).
- **ShopMy + Amazon storefronts**: square-safe covers, aerial mat photos, HQ ShopMy tab intake, weekly ShopMy mats check (Tue).
- **HQ hygiene**: Today ≤5, answered = gone, event passed = gone, timestamps on every card, inline previews; ANSWERS.md before asking anything; no answer is not a no.

## Log of this rewrite (Wed Nov 4 night)
- **Done today:** 45 late holiday cards LIVE on 20 albums + the holiday page (33 late picks + her 12 Santa Baby's Cocktail Hour yeses; independent QA, 2 numbering fixes, new scripts/checks/holiday_numbering.py); 4 FB group posts (Mahjong Row drop, OMM Juniper + Lotus Cove, holiday albums, FYM holiday); new partner Mahj Pit onboarded (page + hub 39 brands + 39-logo graphic + payout terms); FYM tracking endpoint deployed (gate [157]); revenue watch + payout reconcile first pass; Juniper colour card + Claude's 12 picks page; IG evergreen codes post drafted; rules: A YES IS A YES, BLOCKED IS NOT DROPPED, REVENUE WATCH, no 'ask once', SOCIAL 13; morning report (27/38) + Wed code report; 10 pages indexed; 2 launch watches + 3 partner watches + mentor check; Pinterest autopin 7.
- **Found mid-way and given a home:** Amanda Toppe 20% still live, 3 days (hub edited today and missed it) → priority 1a; Wren Oct 9 → 1b; TRK_URL never applied to the live app → priority 2a + Blocked; FYM 1.15 + Mahj Pit catalog (24h gate Thu 3:40pm) not started → 2b; Wed's Planoly drafts not posted / not rolled (permission refused tonight) → 3a + Blocked; story-caption lint 3rd day → 3b; codes post lint length → 3c allow-list; 7 quick-call defaults + Nov 2 site check not applied → 4c; new-albums email not built → 4a; Esme gone from OMM → 1.15; queue.json out of sync → handoff; GoAffPro drop → handoff.
- **HQ:** archived launch-bespoke-sunshine-glow (event passed) and site-maint-2026-11-b (defaults applied, Claude's job), Sweet Jojo W-9 → This week top; Albums: Santa Baby → Live, Juniper → Needs your yes (picks page), targets refreshed. "Yours" 4 → 5 (Sunday ×4 swipe page + Juniper picks page; RTS NOW has 0 open).
- HQ smoke test at 390px not run tonight (data-only change, no page HTML changed).

See CLAUDE.md.
