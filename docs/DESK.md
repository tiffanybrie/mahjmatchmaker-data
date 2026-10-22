# The Desk

Rewritten nightly by the end-of-day desk cleanup (9:23pm ET). The morning HQ cleanup (6:47am ET) reads it. Rules: CLAUDE.md ("THE DESK"). During the day, when an agent stops, Chrome drops or a QA stalls, add the item here right away with its next step.

**Last rewrite:** Wed Oct 21, 2026, ~9:45pm ET (desk cleanup run). Covers everything committed Oct 21 ET (271 commits), Planoly (both workspaces), HQ needs/log/albums, Ready to Ship, and site/livepatch READMEs.

**Thu Oct 22: Tiffany is mostly unavailable (her 5:11pm call).** Give her nothing to post by hand. Only auto-posts (feed, carousels, plain stories with no stickers, pins). Any reminder post dated Oct 22 becomes an undated draft and moves to a later day. Brand credit goes in Tag people and caption @mentions, not stickers.

- [x] Brand boxes publish: DONE Oct 21 ~11:20pm ET (32 brand pages + B&B rack colors, OMM JSON-LD image swapped; verified by curl and Playwright at 390). Left for Tiffany's call: B&B page SEO title ("All 94 Paint Colors & Stains") and the "94 colors and stains" hero/intro lines. No 301 added for /bird-and-bamboo-discount-code-2 (told not to touch redirects); it still serves the fixed copy.

- [ ] **B&B 'standard or scalloped in every color' (Tiffany 10:32pm)**: add the line to (1) FYM rack cards/tray next build, (2) B&B brand page + /bird-and-bamboo-rack-colors (with the brand-box publish), (3) album 'Racks shown' lines on every album that shows a B&B rack (Chrome sweep, batch with the card refresh), (4) future match-card captions + social captions. Links stay 20-inch; never mention 19/21.

- [ ] **Find Your Mat-ch as a home-screen app (Tiffany, Oct 22 3:50am: "I definitely want that… I want it to feel like an app").** Clean full-screen page (e.g. mahjmatchmaker.com/app: just the tool, no site header), web app manifest + flame-heart icons (iOS apple-touch-icon + Android), name "Find Your Mat-ch", standalone display, branded splash, picks remembered; in-tool "Add to your home screen" tip (iPhone 2-step; Android install prompt). Build after the Sun Oct 25 usage reset; aim to have it ready by or soon after launch. Independent QA on real iOS/Android emulation.

## USAGE PAUSE until Sun Oct 25 11am ET weekly reset (Tiffany, Oct 22 3:41am; 90% of weekly limit used)
- KEPT: ONE sales check/day, trig_019FjiaFBVX512N67EYxrGUw now 10:04pm ET daily (was 4x). Launch-day one-shots (Oct 27) untouched. Weekly Monday tasks (fire Oct 26, after reset) untouched.
- PAUSED by Claude (enabled:false): HQ Talk inbox (trig_015cSez…), New affiliate onboarding (trig_01C7xPr…), Pinterest autopin (trig_01UsWfw…; queue full through Nov 30), Mahji Mentor 3x (trig_01LC2kw…), Today's sales check 3x (trig_01ErLFa…), Match Builder refresh (trig_01UwvubnW…), Missed computer task watchdog (trig_011puGf…), Daily Google AI answer check (trig_016VJmC…), Daily affiliate income report (trig_01SwPc3…), Weekday morning brief (trig_019JjET…).
- COULD NOT PAUSE (blocked by the permission check; Tiffany to pause in Scheduled): Hourly brand launch watch (trig_01S2Vsj…), Brand email watch 3x (trig_01Ljz8p…), Google code report daily (trig_01GQHwe…), End-of-day desk cleanup (trig_01WeCbw…), Daily HQ cleanup (trig_01RgaYK…).
- SUNDAY after reset: re-enable at a lighter pace (daily instead of hourly; routine checks lighter), with her OK.
- **NEW STANDING CADENCE after Sunday's reset (Tiffany, Oct 22 3:45am: "these were amped up too high… some could go to dailies or twice dailies"):**
  - Sales: 3x daily (she likes watching sales during the day), ONE task (merge the two sales tasks + morning income report).
  - Brand watch (websites + brand emails merged): twice daily, morning + evening. Not hourly.
  - HQ inbox sweep: once daily.
  - End-of-day desk cleanup: keep nightly (important). Morning HQ cleanup: daily.
  - Mahji Mentor group: once daily. New-affiliate onboarding: once daily.
  - Pinterest autopin: low priority, every 3 days (queue is full through Nov 30).
  - Google code report: a few times a week, not daily (merge the AI answer check into it).
  - Match Builder refresh: weekly. Watchdog + morning brief: stay off unless she asks.
  - Rule going forward: when she flags something we missed, fix the CHECK (what it looks at), don't just raise the frequency.

## Tomorrow's top priorities (Thu Oct 22), in order
Standing order: (1) Find Your Mat-ch™ launch Tue Oct 27, (2) fall content before it expires (Brownstone Bloom), then holiday.

1. **Launch countdown is not scheduled.** All 14 Instagram items in Planoly are drafts waiting on her yes; nothing is scheduled for Oct 22-28. The "6 days" countdown (Wed 6:30pm CT) never went out. The "5 days" story is set for Thu 7:30am CT but won't post as a draft. Ask (HQ Today #1): one yes for the auto-post countdown stories, then Claude schedules them. Owner: Tiffany (yes), then Claude (schedule).
2. **Brownstone Bloom album: her one tap** on Ready to Ship `l-brownstone-v2` (31 cards + 13 missing mats). Fall content, Anders Ruff ships it soon. On her yes: publish per site/livepatch/brownstone-bloom-oct20/README.md (code block pinned @0f8738b, 31/31 URLs warmed).
3. **DONE Oct 22: Pinterest pace fixed (see docs/PINTEREST.md).** Original problem: 163 pins are scheduled in workspace 019fc27b; 121 are hourly `utm_campaign=evergreen` pins, about 25 a day Oct 22-26. The rule in config/pinterest/queue.json is 4 a day at most. These pins are not in queue.json, and git doesn't show who scheduled them. The ShopMy product-pin test (check Oct 24) can't be read cleanly at this volume. Next: re-space them to 4 a day or fewer with set_post_group_schedule (move, never delete), record them in queue.json, and tell the 9:41am autopin run.
4. **QA and paste the v72 tutorial (Claude, coordinator).** The 6-step tutorial was re-captured from live v72 (b02e87a). The page block and launch email were rebuilt with it at 9:29pm (0fc5008c): built, not pasted. The live preview still runs block @8dd3d49 with the old 5-step tutorial. Next: independent QA of the tutorial page and the email, then re-paste the new block on /find-your-mat-ch-preview and re-pin launch-oct27 README step 0a to it. Then swap the Squarespace email draft 6ad90449db1bc22351dc7e9d images (step-sq1..6, now 6 steps). Last, rewrite RTS `d-email-templates` in place and delete its `archived` ship doc so it shows again. **Oct 21 ~11:40pm ET: Squarespace email draft 6ad90449db1bc22351dc7e9d now has all 6 steps** (step-sq1..6 images from jsDelivr @fcf9fd1, alt text and captions 2-6 from tutorial.json; step 5 image + caption duplicated and swapped for step 6; reload confirmed it saved; not scheduled, not sent, sender + legal address still empty). RTS `d-email-templates` is visible again (archived ship doc deleted). Still to do: independent QA of the page tutorial + the email, re-paste the page block, README 0a re-pin.
5. **Pre-launch homepage block live (Claude, Squarespace).** She said yes on Ready to Ship at 3:22pm (l-navplan-fym). /home-preview has it, but the live homepage doesn't (curl at 9:30pm: no prelaunch block). Next: a Chrome session pastes block v2 (site/livepatch/home-prelaunch-fym/README.md go-live steps), then verifies by curl and Playwright at 390/1280.

## In progress

| Item | Owner | Next step | Target |
|---|---|---|---|
| Brand-page boxes | Claude | LIVE (see top). Nothing left except the two calls above. | Done |
| Planoly launch-week posts (14 IG drafts) | Tiffany yes → Claude | Countdown 5/4/3/2/1/LIVE, Papaya "still available", Miss Classic tease are auto-post plain frames: schedule on her yes. Mahj Mood "back tomorrow" (Thu) and restock (Fri) stories are reminders. Oct 22 rule: move the Thu one to an undated draft. Papaya x Vivienne carousel slot (Wed 5:30pm) passed; re-slot on her yes. "6 days" countdown is dead: leave it unscheduled. | Thu Oct 22 7am CT |
| Petalée IG story (draft, auto Sat 10/24) | Claude | Petalée is BANKED and its album isn't live, so the story must not run Sat. Leave it unscheduled and move it to the Petalée go-live day. | Before Sat Oct 24 |
| Pinterest pace (DONE Oct 22) | Claude | 104 burst pins re-spaced to max 4/day, queue ends Nov 30; cap check added to autopin.py (`cap`, `snapshot`, `mark` refuses over cap); see docs/PINTEREST.md. Remaining: tell the 9:41am autopin run to use `autopin.py cap` first. | Done |
| ShopMy product-pin test (10 pins, 1/day 18:00Z) | Claude | Oct 24 check per docs/PINTEREST.md (published, not flagged, go.shopmy.us resolves), then scale or pause | Sat Oct 24 |
| FYM v72 tutorial → page + email (see priority 4) | Claude (coordinator) | Built @0fc5008c. Remaining: independent QA, re-paste, README 0a re-pin, Squarespace email images, RTS d-email-templates | Fri Oct 23 |
| Site search: INSTALL (Oct 22) | Claude (Chrome) | QA passed (Chromium+WebKit, 390/1280); snippet pinned @c6e395f, warmed 783/783. NOT installed: Chrome tab group held another agent's Squarespace Campaigns composer tab (mid-edit), so I did not drive. Next: when Chrome is free, Settings > Developer Tools > Code Injection > Header, APPEND site/livepatch/search/header-injection.html, save the previous injection text to site/livepatch/search/rollback-header-injection-prev.txt first, then curl-verify + Playwright live. Also add HQ need "Optional: turn on search logging (5 min)" (README Tracking). | Thu Oct 22 |
| Pre-launch homepage live (see priority 5) | Claude (Chrome) | Paste + verify | Thu Oct 22 |
| Launch-week copy: FB group description (d-fbdesc2), partner thank-you email (l-partner-email), Work With page (l-workwith6) | Claude | All three drafts still say "Find Your Match". Brand rule (Oct 21 11:26) says "Find *Your* Mat-ch™" in body text and plain in headlines. Hidden tonight (RTS ship `archived`, HQ launch-copy parked). Next: re-word, update the RTS items in place, remove `archived`, re-add to NOW, and reopen HQ `launch-copy-oct21`. | Fri Oct 23 (she answers by Sat) |
| Launch-day triggers | Claude | Homepage switch trig_011jdGG… reads README step 0a's pin (now @8dd3d49), so the old @4b7f8c9 pin note is resolved. Re-pin again after priority 4. Email trigger trig_01ErZy… still names the old subject in its already-sent check (it still works; editing it was blocked). | Mon Oct 26 |
| Soirée All Day 6 holiday mats (FYM + gallery Holiday) | Claude | **Gallery DONE Oct 22:** 6 rows live in Mat Gallery Holiday (block pasted from matgallery-v5 @9efc54b, images @3f8a310 warmed; live diff = only the 6 rows + IB map; gate [13] clean; QA 390/1280 clean). FYM already live (v71/v72). Still open: IG follow + favorite @soireeallday.co (Chrome). | Fri Oct 23 |
| FYM missing swipe-book products (OMM Miracle / Twilight Waltz / Merry Mahjong / Santa Baby mats; PLM Spirit of Christmas + Nutcracker; OMM Vault tiles) | Claude (Chrome) | Brand sites 403 to curl. Save photos in Chrome, add via the pending queue; yeses are in config/swipe-yeses/holiday-oct21.json | After launch (holiday) |
| FYM tile photo audit | Claude (builder) | Apply builder/fym_flags/tile_photo_upgrades.json (73 upgrade / 102 keep / 50 coming_soon) + locks; send tile_photo_requests.json to brands | Next FYM build |
| Discount links not converted (Britt Mills, Mahjong Register, YMI, RMS, Hip Hip, Wren/Soirée/Amanda Toppe) | Claude | Proof in builder/fym_fix_oct21/discount_check_oct21.json; per-brand fix or leave as plain links | After launch |
| Verified-date refresh (blocked Oct 21 3:27/3:28pm by the unattended-publish safety check) | Tiffany OK → attended Claude session | HQ need `codes-2026-10-21` (This week). Google report also wants fresh dates on Anders Ruff, Britt Mills, Amanda Toppe. | This week |
| Indexing | Claude (Chrome) | Oct 21 used 2 of ~10 slots (/mahjong-mats + OMM re-crawl). Use the slots on brand pages the AI Overview skips, in the hq/indexing order. | Daily |
| Thin-album swipe (78 mats) | Tiffany | 0 votes so far. On her ♥s Claude builds cards and brings them back on RTS. | This week |
| Malachite 8 new cards, December 1994 (31), Spirit of Christmas (10) | Claude | All staged since Oct 20 (READMEs), not live. Malachite is year-round; Dec 1994 + Spirit are holiday (Nov 1+). Check each RTS ship answer, then go-live steps in each README. | Malachite this week; holiday from Nov 1 |
| Sunset Vivienne card text | Claude | "Racks shown" lists 7 mat racks + 2 tile racks; image shows 5. Fix on next Sunset edit. Older Sunset cards still say "MAHJONG SOCIAL CLUB" (global card refresh). | Next Sunset edit |
| Site search (staged @7bd75af) | Claude | Independent QA, then install snippet | After launch |
| Email-my-match proposal | Claude → Tiffany | Proposal only (prototype never sent email). Bring to her after launch. | After launch |

## Waiting on Tiffany (only things she can answer now)
On HQ in this order. Today = items 1-4.
1. **Planoly: yes to the auto-post countdown stories** (HQ Today). Phone is fine: reply in the HQ box or chat.
2. **Brownstone Bloom: one tap** (Ready to Ship `l-brownstone-v2`).
3. **Reconnect Instagram via Facebook in Planoly** (computer, 2 min). Then Claude re-checks list_channels, re-adds @ohmymahjong Tag people on the Papaya x Vivienne carousel, and re-points drafts. Remind her in the morning cleanup.
4. **Vivienne mat album: approve the card order** (RTS `l-viv-order2`).
5. This week: email footer mailing address (P.O. box works; Squarespace needs it before the Oct 27 send); OK to refresh verified dates on live brand pages; Fait à Main affiliate link + code; thin-album swipe; 3 FYM questionable photos; Q4 content plan look in Planoly.
6. Also open (not on HQ Today/This week): sender hello@mahjmatchmaker.com + DKIM/DMARC yes; standing yes for auto-posting feed pieces; keep or swap the no-commission bow lamp (ShopMy); Submit the filled-in OMM TEACHMAHJ Google feedback (her Chrome); site menu pick for the desktop nav overflow (site/livepatch/nav-overflow-oct21 screenshots; fix option 1 = fold to ~6 items).
7. **Parked until after launch (Oct 28):** Holiday-or-not calls on 11 mats, ShopMy 5 quick calls, Amazon storefront old-board delete (needs her login). Etsy re-apply reopens Oct 26; Planoly add-on keep/cancel by Oct 25.

## Banked (finished, held on purpose)
- **Petalée (Virora)**: 61 cards + contact sheet, RTS `l-final-petalee`, HQ `petalee-swipe` parked. Her call: sits behind Brownstone. Goes live when we need fresh content. Before publishing: 10% band sweep on the Amanda Toppe/Girly cards, cleaner Petalwing/Coralia photos.
- **Green Light Gatsby (Anders Ruff)**: swipe book built, saved for after launch (config/release-calendar.json `upcomingAlbums`).
- **Season 2 episode reels (13) + trailer**: hidden on RTS. Episodes 6/8/13 were the pre-launch plan; the rest become the ongoing "Dating life of tile sets" series after launch. 9 reel drafts still sit in the old Planoly workspace (bytes not downloadable).
- **Miss Classic Malachite + Jade content**: held for the restock window (release calendar, week of Nov 3).
- **Holiday mood boards / Color Me Merry mood board (Nov 5) / Soirée roundup (Nov 4)**: in the Q4 plan (docs/q4-content-plan.md).

## Later / ideas
- **REMIND TIFFANY: start matching Aurora's racks (her ask, Oct 22 4:48am).** Cute scalloped wood racks, 19" only, $69 (great price for wood). RULE: Claude never uses them in mat-level rack picks (a mat can go with any tiles; 19" won't fit every set). She picks them herself per tile set when she knows the set fits a 19" rack. Bring it up at her next album/match session. Check partner status + IG handle when adding.
- **FYM Sunday build: Tiffany's desktop test notes (Oct 22 4:44am), one build + gate + QA with the share prompt above:**
  1. **Rack screen layout:** match the mat screen. Picker ("♥ a rack") goes up top under the chosen mat; rack suitors go on the BOTTOM. Today they're swapped and it feels disjointed.
  2. **One "Tiffany's picks" toggle on the rack screen.** Today there are 3 (top, bottom, over the rack photo); keep one.
  3. **Back button on racks** (today a missed rack is gone for good).
  4. **Tutorial runs all the way through:** mats, then Next, then the rack swipe, then Make it official, then the card. The last step is too condensed now.
  5. **Share card:** our logo + slogan much bigger and readable, partner brand logos bigger ("a brand moment for us and the partner brands").
  6. **Rename the card formats:** "Love triangle" becomes "Mood board"; "Mood board" becomes "Close up".
  7. **RACK PICKS DATA BUG (root cause found 4:50am):** every pairing in a set gets the SET's 3 racks (locks sets.<slug>.m), not the racks on that album card. E.g. Amara + Chinoiserie Songbird shows PLM Pink / B&B Kelly Green / MRC tortoise; her Songbird picks (config/mat-racks-picks.json) are PLM Pink, PLM Chartreuse, Mahj Mood Clear, so PLM Chartreuse is missing. Only 26 mats have mat-level picks (D.lm). Fix: rebuild racks per (set, mat) from each album card's real racks, plus mat-racks-picks. Add a gate check that diffs every album card's racks against FYM, so she never has to test pairings. Opal on Songbird: NO (Tiffany 4:49am: the clear scallop is the better call for such a busy mat). Songbird racks stay PLM Pink, PLM Chartreuse, Mahj Mood Clear.
  8. Phone pass still to come from her: hold layout changes 1-2 until her phone notes arrive, if they come before Sunday.
- **Color suggestions → album candidates (Tiffany, Oct 22 4:22am, "we'll talk about that"):** after launch, pull the strongest measured color matches from Find Your Mat-ch (sets she has NOT matched yet) into a short swipe list so she can add the good ones to albums. Not before launch (usage).
- **FYM share prompt + #mahjmatch (Tiffany, Oct 22 4:27am, build SUNDAY with her tutorial feedback, one gate + QA + publish):** (1) one Share button (phone share sheet, already wired); drop the separate FB/Pinterest buttons; (2) tapping Share auto-copies the caption text with #mahjmatch, toast "Caption copied: paste it into your post"; (3) #mahjmatch + mahjmatchmaker.com printed small on the card image itself; (4) prompt line, HER FINAL WORDING (4:29am): "Share your match on social or with your group! Tag #mahjmatch, we love to see your matches!"; (5) after launch: reshare "Great match by @..." posts from the hashtag, asking permission first; watch the hashtag in the Monday brand watch.
- Pinterest single-product ShopMy pins at scale + gift-guide pins ("mahjong gifts under $50"). Tiffany, Oct 21 5:34pm ("flood the zones"). Scale only after the Oct 24 test.
- Weekly IG brand watch (Mondays, first run Mon Oct 26): follow + favorite new partner/ShopMy brands; handles still needed for Splash of Color, Hip Hip Mahjong, Yellow Mountain Imports, Mahjong Register. CLAUDE.md, Oct 21 5:25pm.
- Brand alert sign-ups (Bam Bird, Mahjong Row & Co, Charleston Mahjong Club, Middle & Main, Britt Mills, Virora, TdT): need her yes. Q4 plan, Oct 21.
- Keep-Planoly-paid decision by Oct 26; comment-for-link reversal is her call; UPS 2026 holiday cutoffs re-check Dec 1. Q4 plan, Oct 21.
- Talk: Shop page on the site vs straight to ShopMy. HQ `shop-experience-pages-review`, parked to Oct 28.
- Site colors: one rainbow + separate Yellow/Orange pages. RTS Oct 19, parked to after launch.
- "Press for" → "Press for Mahjong" name change in FYM (locked name, needs her OK). Oct 21 v71 notes.
- Holiday set count check: she counted 12, FYM has 10 hol + 4 candidates. Tile audit, Oct 21.
- Upcoming albums from the brand launch watch (not started, Claude's queue): see HQ Albums → Not started (Amahj Garden Stamped + On the Water, Cabana Club, Miss Darling Lilac, TdT/MFM/Soirée holiday mats, PLM vegan leather mats, etc.).

## Daily operations (Wed Oct 21)
| Operation | Done today? | Notes |
|---|---|---|
| Affiliate tracking (Money tab) | ✅ Done | 9 checks; 15 sales, $405.90; October to date $5,089.97. Mahjong Row + Mini Mahjer amounts came in (HQ need closed tonight). Flagged `partial` (pending orders). |
| Google code report | ✅ Done | Ran 10:55-11:55am ET: AI Overview names MAHJMATCH for 25/35 brands (was 27); OMM #8, not in either AI answer. |
| Verified dates (1st/15th) | ⏸ Not due | Next run Sun Nov 1. A manual run today was blocked by the unattended-publish safety check, so nothing changed. HQ asks for her OK. |
| Pinterest queue health | ❌ Not OK | Over the pace cap: about 25 pins/day Oct 22-26 vs the 4/day rule (see priority 3). The channel is connected and auto-publishing. |
| Indexing | ⚠️ Partly | 2 of ~10 slots used (/mahjong-mats + OMM re-crawl). |
| Planoly next-7-days coverage (IG) | ❌ Not covered | 0 IG posts scheduled Oct 22-28; 14 drafts waiting on her yes (see priority 1). |
| FYM feedback inbox (Gmail label Site/FYM feedback) | ✅ Done | Form tested end to end; only the TEST thread. |
| HQ + Ready to Ship cleanup | ✅ Done | Morning run plus this desk run. |

## Never-ending projects
- **Find Your Mat-ch™ app** (artifact 6epA9HuEdT32zUp79Qv3kd): gate + independent QA before every publish; locks; catalog pending queue; photo flags; her feedback the same day.
- **Google / MAHJMATCH in AI answers**: daily code report, indexing (~10/day), verified dates on the 1st and 15th, brand-guide pages.
- **Albums**: new releases → swipe books → cards → her yes → live; thin albums; holiday sections.
- **Social**: every approved post in Planoly at its time; auto-post wherever possible; feed + every slide to stories; brand tags; collabs.
- **Pinterest**: daily autopin within the pace rule; evergreen pins only of our own images.
- **Affiliates + money**: daily commission checks; onboarding new partners (page, hub, logos, FYM, indexing, IG follow/favorite).
- **Mat Gallery + colour system**: sort rule, holiday rule, partner-only gate.
- **ShopMy + Amazon storefronts**: shelves, covers, collages.
- **HQ hygiene**: Today ≤5, nothing she can't answer, no outdated drafts.

## Log of this rewrite (Oct 21 night)
- HQ open needs: 16 → 12 (Today 4, This week 6, plus the inbox box and one red LIVE YES moved to Claude). Closed: Mahjong Row/Mini Mahjer amounts (both logged). Parked: launch-week copy (outdated naming), holiday-or-not, ShopMy 5 calls, Amazon old boards. Rewritten: Planoly yes, verified-date OK, email footer address.
- RTS NOW: hid d-email-templates (5-step tutorial, superseded by the v72 6-step capture), d-fbdesc2, l-partner-email, l-workwith6 (old "Find Your Match" naming) via ship `archived`.
- RTS NOW (Oct 22): re-worded d-fbdesc2, l-partner-email, l-workwith6 to Find Your Mat-ch™ (™ once; italic Your only in Work With body text) in place, source files in site/livepatch/workwith updated, Work With preview artifact republished, `archived` removed (none had an answer from her). Still open: reopen HQ `launch-copy-oct21`.
- HQ Albums tab: six groups (Needs your yes / Started, stalled / Claude building / Not started / Banked / Live collapsed) from a new `group` field on each hq/albums item.

See CLAUDE.md.
