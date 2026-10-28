# The Desk
Rewritten nightly by the end-of-day desk cleanup (9:23pm ET). The morning HQ cleanup (6:47am ET) reads it. Rules: CLAUDE.md ("THE DESK"), docs/CHATS.md (which chat owns what). During the day, when an agent stops, Chrome drops or a QA stalls, add the item here right away with its next step.

**Last rewrite:** Tue Oct 27, 2026, ~9:45pm ET (desk cleanup run). Covers the ~95 commits of launch day (fbcff22 … dd68a3a), docs/ANSWERS.md (Oct 27 lines through 8:21pm), docs/MATCH-INBOX.md, Planoly (IG workspace 019fc27c… + Pinterest 019fc27b…), HQ needs / log / hq/albums, Ready to Ship `ship` docs (no new answers today), the Brownstone order page (db `review` still EMPTY), site/livepatch READMEs and curl checks of the live site tonight.

**Owners (three chats, Oct 22):** Main (Opus) = social/Planoly, site pages, email, HQ/DESK, decisions, Google + SEO. Matches & Catalog (Opus) = Find Your Mat-ch, albums, gallery, catalog, search index. Ops (Sonnet) = the ONLY Chrome driver: Squarespace pastes, uploads, IG follows/checks.

**Repo note:** checkout on `partner-catalogs-sqsp`. A full fetch of this repo times out: use `git clone --depth=60 --single-branch -b partner-catalogs-sqsp --filter=blob:limit=2m` (tonight's run worked from /home/claude/mmd-pcs) or `git fetch --depth=60`.

**PARTNER SEND GATE (Oct 27 3:08am, standing):** before scheduling ANY partner email or graphics drop, run `python3 scripts/partner_send_check.py`; it must exit 0.

## Tomorrow's top priorities (Wed Oct 28), in order
Find Your Mat-ch™ launched (live ~1:25am Oct 27, Version 1.5 on the site since 9:05am). The launch item of the standing order is done, and Tiffany said at 6:31pm "GOOGLE IS #1". So the post-launch order is a real call: HQ need `set-order-2026-10-28` asks her to order it. Until she answers, run this default (fall content has the only hard deadline):

1. **Brownstone Bloom album live by Thu Oct 29 (fall, before Halloween).** Waits on her: 40 cards in order + Save on the order page (https://claude.ai/artifact/WNjXTGjxfdqoa1tzUiYgQ4; db `review` empty tonight; RTS `l-brownstone-order` top of NOW; HQ Today). On Save: Matches & Catalog runs brownstone_block.py, warms jsDelivr, Ops pastes, /links latest-album card, docs/NEW-ALBUM-CHECKLIST.md top to bottom. If no Save by Wed 6pm ET, Main messages her once (Thu is the last day).
2. **Wed social goes into Planoly on her yes (Main).** HQ need `social-plan-2026-10-28`: Malachite how-to reel v2 ~12pm (everyday + holiday, B&B Red + Dark Teal racks, tall card, tall cover takes the Malachite grid slot, collab @missmahjongofficial, her song), FB group: Bird & Bamboo stained wood racks back (+ MAHJMATCH), FB group FYM post 'launches tomorrow' → 'live now', FB Page copy of the reel. 0 IG posts are scheduled for the next 7 days, so this is the only coverage. Storyboard-before-render applies to anything new.
3. **Google / MAHJMATCH daily (Main).** Her 6:31pm brief: MAHJMATCH in AI Overview AND AI Mode for every partner ("[brand] discount code" / "promo code" + "mahjong discount code"); OMM first (20% ends Nov 25), then Mahjong Row, Miss Mahjong, Bam Bird; competitor Charlotte Mahjong. Daily: did the code show, rank, why sales were what they were vs the calendar. Indexing: refreshed brand pages first, ~10/day (quota hit at 4 today). Code report not run today (last: Oct 26). The single daily "Google & Revenue" task waits on her usage-plan yes (HQ).
4. **Find Your Mat-ch Version 1.6 (Matches & Catalog).** Must slim first: artifact ~265.9 of 268.4 MB (256 MiB cap). Then add: Bird & Bamboo White Wood Stain rack, Bam Bird Plaid Neoprene x3 (Pink on Pink, Green and Azure, Green with Pink), Britt Mills Bella Leatherette (2nd link), TdT Beechwood tiles (not findable), card-title clean-up check (no outlines anywhere), two-colour ranking rule (ANSWERS Oct 27 10:57am), MATCH-INBOX rack items. Gate + independent QA, artifact AND website (rule 0), +0.1 version label.
5. **Overdue site pastes, Claude's job (Ops with Chrome, standing authority).** (a) Her 41 thin-album hearts: STILL 0 of 9 albums live (curl tonight; README site/livepatch/thin-albums-oct26) — 4th day overdue. (b) Holiday anchors: Sierra etc. still `id="holiday"` (approved Oct 25) → `holiday-matches` on 34 albums + /holiday-mahjong-matches links. (c) Site search header (QA passed Oct 22) not live. (d) Stray `fym-v72` string still on /find-your-match. Flagged on HQ as "overdue, Claude's job" (needs an Ops chat with Chrome on her computer).

## Handoffs to do first (Wed morning)
- **OPS: check @sunday_mahjong on Instagram in Chrome** on every partner-watch day (Planoly can't read it: not a Business/Creator account). Add finds to docs/brand-social/sunday-mahjong.md + HQ launches.
- **Main: put the Jade how-to reel on the Facebook Page.** She posted how-jade-v2 to IG herself (1:06pm) and it became the Jade row cover; Planoly shows no FB Page copy (only the launch reel went to FB today). FB Page rule (Oct 26): Claude's job, same day; it's a day late, so post it with the Malachite reel or skip it only if it's a restock-style post (it's evergreen, so post it).
- **Main: Miss Classic restock Planoly group 01a17a6c-12c1 (IG+FB) and IG grid draft 01a17a6c-12c5 stay UNSCHEDULED** (restock = stories + FB only; same-day rule). The Wed Malachite reel replaces them. Leave the drafts; clear only on her "clear old drafts".
- **Main: stale Planoly items.** One leftover SCHEDULED reminder story from Oct 21 (group 01a16052-2828, Papaya × Vivienne 3 frames, reminder already sent) still shows as scheduled; countdown/launch-day drafts (01a16052-33a6 … -40c3, 01a17911-ab58) and old launch drafts (01a17a6a-943b, -95d3, -9777, 01a17a6c-10e4, 01a176a0-8458, 01a1791a-d167) are past their day. Clear their dates on her "clear old drafts"; never delete. Halloween Raven carousel 01a16477-092f: confirm it's dated Thu 10/29 noon, not Wed.

## In progress
| Item | Owner | Next step | Target |
|---|---|---|---|
| Brownstone Bloom album | Matches & Catalog → Ops | Her Save on the order page, then block + paste + checklist (priority 1). | Thu Oct 29 |
| Wed social plan into Planoly | Main | Her yes on HQ `social-plan-2026-10-28` → schedule each, reminders for hand posts (priority 2). | Wed ~12pm |
| Google & Revenue daily | Main | Priority 3. Usage plan yes decides whether it's one task. | Daily |
| FYM Version 1.6 (slim + new partner items) | Matches & Catalog | Priority 4. | Thu |
| Overdue Ops pastes (thin albums, holiday anchors, search, fym-v72) | Ops | Priority 5; then Matches & Catalog runs builder/fym_fix_oct26/v94_thinpicks.py. | Wed |
| Malachite how-to reel v2 (Tinder cut, everyday + Holiday button) | Main | Built (assets/social/restock-oct27/how/malachite/); in the Wed plan. Malachite still in stock 8:25pm. | Wed |
| Deco carousel: inside one brand / across brands (Bam Bird Deco x Britt Mills) | Main | Her favourite = Deco Lagoon on Reba (two-colour). Make the final 7-slide STORYBOARD (stills, all 3 colourways, crossed colourways, two-colour picks) for her veto before any render. | This week |
| Table view / "Build your set" walls mock | Matches & Catalog | Walls mock v5 sent ~6:15pm (real OMM back photo, walls against 4 racks, Fruit Stand mat). Waiting on her reaction; she'll send 2 tile sets to mimic. Phase 2, post-launch. | Her reply |
| FB group: weekly Claude Doc of planned group posts | Main | Her 6:31pm ask: one doc per week with the group posts + copy she edits in place; first one this week (B&B stained racks, launches/restocks). | Thu |
| Verified line missing | Main | I Love Mahj + /mahjong-discount-codes (Sunday/Wren have no code). Verified dates now refresh every Monday 8:17am ET (trig_01PGtT8). | Mon Nov 2 |
| UpPromote accounts → mahjmatchmaker@ | Main | Her 6:20pm ask: move every UpPromote account (+ Marketplace) from tiffanybrie@ so one inbox/dashboard is checked. Needs her logins where a move needs the owner. | This week |
| YOLO Mahjong onboarding | Main | Approved Oct 23 (missed); HQ brands/yolo-mahjong set approved: page, hub, logo, FYM, indexing, IG follow/favorite. | This week |
| The Royal Mahjong Society first sale (Oct 26) | Main | Add to affiliate logins + sales checks. | This week |
| Partner feedback watch | Main | Daily 2:13pm; DISABLE after the Nov 10 run (trig_01RKw9eUwTYPo39gbYHb65gh) unless feedback arrives. 0 real partner feedback so far. | Nov 10 |
| MATCH-INBOX open items | Matches & Catalog | OMM leveled rack cut-outs in the app, TdT racks level, Bam! White Wooden single cut-out, PLM true chartreuse rack, MRC Scalloped Tortoise for every set (20"), tortoise rack order, rack length by TILE SIZE (length in data), 69 FYM mats with no gallery row (gate [90]), 38 angled mats (gate [89]), Spirit of Christmas composite photo. | This week |
| Late partner holiday mats → holiday albums | Matches & Catalog | Waits on her picks (HQ This week). | After her picks |
| Mat swipe-book hearts into tile albums | Matches & Catalog → Ops | Larkspur cards built, on 0 of 27 albums; then Revelry, Isla, Peony & Parasol, Art Deco Dayz, Spring Fling, Santa Baby's, Vivienne, Brownstone. | After priority 5 |
| Mahj & Moon ShopMy links into FYM | Matches & Catalog | Collection done (shopmy.us/collections/8525607, 13 listings); config/mahj-moon-shopmy-links.json → v95_mahjmoon.py in 1.6. | Thu |
| IG pinned row, 3rd pin cover | Main | "We've been busy matching" cover still says LAUNCHING TOMORROW · 10.27: prep a NOW LIVE cover she swaps in one step; bring with the file when she has a minute. | This week |
| /links dead card cleanup | Main → Ops | Remove the dead "Coming 10.27" mmlFymSoon card + date-switch script (page "Mahj Squad Discount Code (Copy)"). Not urgent. | This week |
| Subscriber "It's here!" email | Main | Never approved (her Oct 23 NO + revisions not applied). Apply the revisions; ask "send or skip" once, in chat, next time she's in Main. | This week |
| ShopMy holiday leftovers + 2:3 covers + Canva template samples | Main → Ops | As on the Oct 26 desk (Kate & Laurel, pink lamp, Sweet JoJo shelf, Retro Rattan list rename; ~35 covers on her yes; Canva samples shown once). | Thu |
| Discount links not converted (Britt Mills, Mahjong Register, YMI, RMS, Hip Hip, Wren/Soirée/Amanda Toppe) | Main | Proof in builder/fym_fix_oct21/discount_check_oct21.json. | This week |
| Bam Bird page ~#17 on Google; Bird & Bamboo sales drop | Main | Re-crawl request; Search Console check. Part of priority 3. | This week |
| Outreach page + Work With rebuild + launch/restock form | Main → Ops | Her l-workwith6 notes; first use Backyard Yacht Club. | Next week |
| Amazon mats into gallery + FYM; missing swipe-book products | Ops → Matches & Catalog | Her picks only (parked need returns Wed); OMM Miracle / Twilight Waltz / Merry Mahjong / Santa Baby, PLM Spirit + Nutcracker photos → pending queue. | Next week |
| Papaya Beechwood README | Matches & Catalog | Live since Oct 22; README still says NOT LIVE. | Next touch |

## Waiting on Tiffany (only things she can answer now)
**On HQ Today, in this order:**
1. **Set tomorrow's order** (quick): Google/MAHJMATCH vs Brownstone vs FYM 1.6 vs Deco carousel vs table view. Default runs if she skips.
2. **Wed social: yes or change a line** (HQ `social-plan-2026-10-28`).
3. **Brownstone Bloom: put the 40 cards in order and Save** (Ready to Ship → order page). Fall, publish by Thu.
4. **Usage plan: yes or change** (one daily Google & Revenue task, trim the background schedule, storyboard before renders). Usage hit ~50% of the week by Tuesday.
5. **Tue sale amounts:** Anders Ruff 1, Bird & Bamboo 1, Tigre de Tartán 1 (quick).

**On HQ This week:** Planoly Content Marketplace add-on keep/cancel ($13/mo, trial ended Oct 27; quick); overdue site pastes need an Ops chat with Chrome (Claude's job, flagged); late partner holiday mats → which holiday albums; Sunday sets round 2 (4 sets); FYM hidden photos (8); Fait à Main link + code (quick). Parked, back Wed Oct 28 (morning cleanup reopens): Gatsby round 2, Amazon holiday picks, Amazon old boards, Etsy re-apply (Rakuten), holiday-or-not on 11 mats, ShopMy 5 calls, Shop page talk.

**Asked in chat, not on HQ (the owning chat asks once, next time she's there):**
- Main: walls mock v5 reaction + her 2 tile sets (Matches & Catalog builds); subscriber "It's here!" email send or skip; ShopMy 2:3 cover samples; Canva template samples; her lost Pippa teardown.
- Matches & Catalog: TdT Estate Sale also works-for-holiday?; more Let's Be Besties mats? (defaults applied, nothing blocked); which "Photo coming soon" tile sets to show; Lagoon + Mulberry splits; Bam Bird Classic Tortoise match pick; album idea MFM Jubilee × Parquet Petal.

## Banked (finished, held on purpose)
- **Petalée (Virora)**: 61 cards, RTS `l-final-petalee`, vault. Before publishing: 10% band sweep on the Amanda Toppe/Girly cards, cleaner Petalwing/Coralia photos.
- **Vivienne mat album (OMM)**: 16 cards, parked (no mat albums, Oct 23); its hearts go into the tile albums.
- **Sunday Blues + Nature Walk**: vault once her round-2 swipe is in (never two Sunday sets back to back).
- **Season 2 episode reels + trailer**: undated Planoly drafts (Ep 1-13). Dating-life series OFF this week. Each gets redone with an intro first. Jade "Smith-style" reel parked (needs her song).
- **Halloween**: Night of the Raven carousel (Thu 10/29 noon) + Happy Halloween story (10/31).
- **Holiday tables** (Polo Club 11/4, Rackin' Rudolph 11/6, Retro Rattan held): Planoly drafts.
- **Malachite 8 new cards, December 1994 (31), Spirit of Christmas (10)**: staged since Oct 20; holiday ones from Nov 1 (December 1994 still needs her RTS notes applied).
- **Partner kit explainer video v2 + launch explainer reel + tutorial reel (real speed / 1.5x)**: built, not used.
- **Restock companion frames** (Malachite/Jade/Catrina, assets/social/restock-oct27/): Catrina dropped (sold out 8:25pm; same-day rule). Reuse the format at the next restock.

## Later / ideas
- **Build your set / table view (Oct 27 5:36pm, Tiffany):** live tablescape (big real mat photo, tile circle bottom-right, racks; tap strips to swap); WALLS (4×19 double stacks against each rack, tile-back colour, on/off, photoreal only); later tablecloths, dice dish, lamps, bags.
- **Accounts + "I own this" stars + "match what I own"; save-to-home-screen web app** (Oct 27 6:01pm). Competitor Mahj Closet ($9.99); her angle "Mahj Garage" (whole catalog + your items; name TBD).
- **Mahj registry** (shareable wishlist), **AI "dream mat"** (prompt → mat, maybe print/sell), **dream set builder** → demand data for brands ("Mahj dreams") (Oct 27 5:49pm, ideating).
- **Content like @mahjandmotif** (Oct 27 10:35am): images, music that fits, templates, not match cards all the time (research docs/research/mahjandmotif-grid-oct27.jpg).
- **A better FYM reel later this week with different products** (Oct 27 10:23am; docs/FYM-REEL-RULES.md).
- **Partner portal** (Oct 26): bookmarkable per-brand place for uploads/photo swaps. Not this week.
- **Separate desktop vs mobile FYM** (Oct 25); **mat-only brand "eye candy" story** (Oct 26); **OMM reshares only 100%-OMM content** (Oct 26); **FB group growth plan** (Oct 26; @everyone for the biggest moment); **keep IG lean** (Oct 26 data).
- **Canva template library + #MahjMatch follower reshares** (Oct 25); **IDEAS 3.0** private studio, per-product links (Oct 23); **internal FYM sets view** (Oct 24); **new products roundup** + **every-tile-set gallery** (Oct 24); **Bam Bird Deco album** (Oct 24, after Gatsby); **Match Monday / Reader Request / "Matchmakers"** (Oct 23); **colour model** (Oct 23); **holiday gift series from ShopMy videos** (Oct 22); **Rebecca Illustrated 15% ShopMy** (Oct 22); **Aurora's racks** (Oct 22); **Pinterest ShopMy single-product pins** (Oct 24); **brand alert sign-ups, comment-for-link, UPS cutoffs Dec 1** (Oct 21); **site colours, "Press for Mahjong" rename, nav overflow** (after launch); **$200/mo API credits plan** (after launch).
- **New brand releases** are NEW PRODUCTS, never albums (Anders Ruff Bellamy Bloom / All American / Boston Mahj Party / Heritage Tartan; Bespoke x Brooks Brothers; Bespoke x Gray Malin; Britt Mills Emerald Mirage; Mahjong Row & Co. fall collection ~mid-Nov).

## Daily operations (Tue Oct 27)
| Operation | Done today? | Notes |
|---|---|---|
| Affiliate tracking (Money tab) | ✅ Partial | 5:50pm ET: 11 sales, $206.28 known; 3 amounts unknown (Anders Ruff, Bird & Bamboo, TdT) → HQ Today 5. Oct 26 card closed. 12:04am close-out still to run (slots now 2:04pm + 12:04am, trig_019Fjia). |
| Google code report | ❌ Not done | Last run Oct 26 (project doc 99e). Her new daily brief (priority 3) starts Wed. |
| Verified dates | ✅ Done | All 32 brand pages + OMM refreshed to Oct 27 (curl-checked 6:44pm). Now weekly, Mondays 8:17am ET. Missing line: I Love Mahj, /mahjong-discount-codes. |
| Pinterest queue health | ✅ OK | Pins scheduled daily from Wed Oct 28 (4/day pattern), no failures. |
| Indexing | ✅ Done | 4 requested (find-your-match, versatile mats blog, /blog, holiday page); quota hit on the 5th. Brand pages go first from Wed. |
| Planoly next-7-days (IG) | ❌ Not covered | 0 IG posts scheduled Oct 28-Nov 3 (only a stale Oct 21 reminder). Wed plan waits on her yes (priority 2). Raven Thu, Halloween story Sat, holiday tables Nov 4/6 are drafts. |
| FYM + partner feedback | ✅ Done | Daily watch; 0 real partner feedback (2 tests). |
| Launch watch (new products) | ✅ Done | 9:27am, 1:45pm, 6:08pm, 6:40pm runs: Catrina/Jade/Malachite restock, TdT Beechwood + Estate Sale, Bam Bird Plaid x3, B&B racks back → MATCH-INBOX / HQ. |
| HQ + Ready to Ship cleanup | ✅ Done | Morning 6:47am + Main 7:10pm (3 archived, timestamps + Quick answers live) + this desk run. No new RTS answers. |

## Never-ending projects
- **Find Your Mat-ch™ app** (artifact 6epA9HuEdT32zUp79Qv3kd; public Version 1.5 = v101 in the artifact AND on /find-your-match + preview): gate + independent QA before every publish; artifact AND website copy AND README 0a pin in the same step; locks; pending queue; photo flags; +0.1 version label per publish (docs/FYM-VERSIONS.md); her feedback the same day with a gate check; when a publish/paste fails, MESSAGE HER right away. Watch the 256 MiB artifact cap.
- **Match inbox** (docs/MATCH-INBOX.md): any chat writes match/catalog misses there the same turn; launch watch hands new partner products there twice a day.
- **Google / MAHJMATCH in AI answers (her #1, Oct 27)**: AI Overview + AI Mode per partner daily, code report, indexing (brand pages first), weekly verified dates, brand-guide pages, captions that type out "[Brand] discount code MAHJMATCH".
- **Albums**: process doc 86b (colour card FIRST), her yes, live (docs/NEW-ALBUM-CHECKLIST.md); thin albums; mat swipe-book hearts into tile albums; late partner holiday mats.
- **New products**: hq/newproducts → gallery + FYM colour-tagged → weekly roundup. Never albums.
- **Social**: every approved post in Planoly at its time; storyboard (stills) before any render; restocks/launches SAME DAY or never, stories + FB only, never the IG grid (Rule D); every slide to stories; brand tags + collabs; FB Page copy of every IG post (brand names); #mahjmatch; reminder posts lead with the one key action; tall 9:16 match cards in reels; center_check.py on every render.
- **Facebook group**: community, never ads; launches/restocks/news with pretty pictures + MAHJMATCH; weekly Claude Doc of planned posts for her to edit.
- **Partner share graphics**: one per brand + our MAHJMATCH version (one brand a day).
- **Pinterest**: queue within the pace rule; evergreen pins of our own images.
- **Affiliates + money**: sales checks 2:04pm + 12:04am with spike AND drop checks; onboarding new partners (page, hub, logos, FYM, indexing, IG follow/favorite).
- **Mat Gallery + colour system**: sort rule, holiday rule, partner-only gate; gallery row for every visible FYM mat (gate [90]); two-colour coordination over tonal.
- **ShopMy + Amazon storefronts**: shelves, 2:3 covers, aerial mat photos only, weekly ShopMy mats check Mondays.
- **HQ hygiene**: Today ≤5, answered = gone, event passed = gone, timestamps on every card, inline previews, Ready to Ship holds anything one step from done; ANSWERS.md before asking anything.

## Log of this rewrite (Tue Oct 27 night)
- **Done today (launch day):** Find Your Mat-ch live (~1:25am) and Version 1.4 (3:15am) → 1.5 (4:05am artifact, 9:05am website: ~20 missing partner mats + Spirit of Christmas); Mat Gallery live with 18 new mats + intro links to FYM; homepage hero → FYM app trio phones; /links FYM card live with the white trio; partner email sent 7:00am to 31 brands + Virora DM (all 31 have graphics); launch reel v5 (Sunday × Brownstone Bloom, 4 brands) posted by Tiffany + FB Page copy auto-posted; Anders Ruff reshared it; IG pinned row fixed; Jade how-to reel posted as the Jade row cover; Malachite how-to v2 built; Deco storyboards; walls mock v4 → v5; verified dates refreshed on 33 pages; partner send check + center check scripts; HQ timestamps + Quick answers.
- **Found mid-way and given a home:** thin-album hearts (4th day not pasted) + holiday anchors + search + stray fym-v72 → priority 5 + HQ overdue flag; Jade reel missing from FB Page → handoff; FYM artifact size cap → priority 4; Bam Bird Plaid x3, Britt Mills Bella Leatherette, B&B White Wood Stain, TdT Beechwood → 1.6; Deco carousel stopped at storyboards → In progress (storyboard first); subscriber email never approved → In progress (Main asks once); Catrina restock frames never posted → banked (too late, sold out); Miss Classic restock drafts → stay unscheduled; stale scheduled Oct 21 reminder + past-day drafts → handoff; Google code report not run → priority 3; usage plan → HQ Today; post-launch order unclear → HQ "Set tomorrow's order".

See CLAUDE.md.

- **Main, Oct 27 10pm (open tonight):** (1) Fix the FB group Find Your Mat-ch post to "live now" (her yes, tonight; needs a browser). (2) Planoly cleanup (stale Oct 21 reminder + old drafts; she can't tell where to look). (3) Draft the FB group Bird & Bamboo stained wood racks post for her look (approved). (4) Malachite reel v2 sent in chat; on her yes → Planoly IG reel ~12pm Oct 28 (collab @missmahjongofficial, tall cover) + FB Page copy.
