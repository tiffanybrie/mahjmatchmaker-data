# The Desk
**BEFORE ANY POST (group, IG, FB Page): open the Brand news (live) sheet https://docs.google.com/spreadsheets/d/1Lm3mydRx3cXXYz9HTAkL2LLleQx8x5OrThr2IEXJRUM/edit (tab 'Brand news', range 'Brand news'!A:G) and include everything not yet posted; after posting, fill 'Posted where'. One post per day in the group: EDIT the day's post, never a second post (Tiffany Nov 10 12:28pm + 12:30pm + 7:39pm).**
**ALBUM LAUNCH TRACKER (her visible source of truth, Nov 10): https://docs.google.com/spreadsheets/d/18wyQ2mQ9epIIuDEyijYy86XAL4SEmtiVU06mzoWms6c/edit . Every chat that does a launch step fills its cell (date + proof link) the same turn. Process doc: https://docs.google.com/document/d/1vYacaqeyXufkly5aA1CGm-OwWxgqtGcx47x8WYy-qwc/edit**

Rewritten nightly by the end-of-day desk cleanup (9:23pm ET). The morning HQ cleanup (6:47am ET) reads it. Rules: CLAUDE.md ("THE DESK"), docs/CHATS.md. During the day, when an agent stops, Chrome drops or a QA stalls, add the item here right away with its next step.

- OPS (Thu 11/12 sweep 12:58pm, needs Chrome + her yes): album launch email = TEMPLATE now (her 10:59am). On her yes in HQ need juniper-drop-2026-11-11: open Squarespace draft 6af357e97ff74f68f862d0ee, change line 1 to "The latest Oh My Mahjong set, Juniper, is here! 💚" and subject to "The Juniper album is live 💚" (page https://claude.ai/artifact/6vTx8YprmPvDd52YhyGorJ), send to All subscribers, check Sent first; mark template `new-albums` APPROVED in docs/EMAIL.md so every later album launch sends without asking. No yes = nothing sends.
- Main (her 11:04am): Work With page v3 is HELD (no hidden upload). After Brand Watch is fully set up, revise: partners FEATURED in FYM (no "we add non-partners", no "only partners"), New Releases & Restocks = we track + share their promotions with a Brand Watch link, drop the old Partner Brands card, use a few accurate brand tickers; then show her the revised draft.
- RULE (her Nov 12 11:00am): never send her to a repo file path in HQ; put the actual words or picture in the card.
- OPS (launch watch Thu 11/12 9:05am): search Tiles & Tablescapes for Mahjong Studios Easter Morning + Some Bunny (new Easter tile sets; no colour card / TNT rec yet, so no swipe book).
- OPS (launch watch Thu 11/12 9:05am): copy assets/launches/mahjongstudios-easter-morning-christian-mahjong-tile-set/ and assets/launches/mahjongstudios-some-bunny-easter-mahjong-tile-set/ to Dropbox /Mahj Matchmaker Albums/New releases/Mahjong Studios/ today.

**Last rewrite:** Wed Nov 11, 2026, ~9:55pm ET (desk cleanup run, cloud, no computer linked). Covers the 60 commits of Nov 11 ET (13:30 Maison Mahj … b9828ecb usage report), docs/ANSWERS.md (Nov 11 lines, 12:26pm-9:17pm), docs/OVERDUE.md, docs/MATCH-INBOX.md, Planoly (IG workspace 019fc27c…: 36 scheduled groups, all in the Dec 7-10 review week or past reminders, + 32 drafts; exports docs/social/planoly-exports/ig-2026-11-11-desk.json + ig-2026-11-11-desk-drafts.json; Pinterest 019fc27b…: 4/day scheduled Nov 12-26+, 0 errors, pin-2026-11-11-desk-scheduled.json), HQ needs (17 open before → 13 after), hq/albums (94 items, live pages curl-checked), Ready to Ship (no new answers).

**Owners (Tiffany Nov 11 4:41pm: ONE working chat):** **Main** owns everything (social/Planoly, site, email, HQ/DESK, Google + SEO, money decisions, Find Your Mat-ch, albums, gallery, catalog, search index, Chrome steps when her computer is on). **Ops (Sonnet)** = only money runs + Amazon-to-ShopMy link chores. The Matches & Catalog chat is RETIRED: any line below that still says "Main (was Matches & Catalog)" is Main's. Catalog gaps = scheduled task **Partner coverage owner (daily)** (trig_012DGkmgYqbH5ks6V9Dq9Ldz, 1:47pm ET).

**Statuses "Watch", "Ask once" and "later" are banned.** An open line leaves this page only with proof (ANSWERS DONE line, commit, or live URL 200); otherwise it moves to docs/OVERDUE.md with owner + next step + date. `python3 scripts/checks/desk_drop_check.py --commit HEAD` runs before every push.

**Repo note:** `partner-catalogs-sqsp` is huge (~6 GB pack at depth 50). `git fetch --depth=50 origin partner-catalogs-sqsp:refs/remotes/origin/partner-catalogs-sqsp` took ~8 min tonight (run it in the background with a 580s timeout; a killed fetch leaves a multi-GB tmp_pack_* in .git/objects/pack: delete it). Same root cause as the jsDelivr 403 below.

**PARTNER SEND GATE (Oct 27, standing):** before scheduling ANY partner email or graphics drop, run `python3 scripts/partner_send_check.py`; it must exit 0.

**NEW TODAY (Nov 10, ANSWERS):** PLAIN POSTS only (captions from scripts/social/plain_post.py, her voice + a little excitement, brand @tags at the BOTTOM, 'along with over N mats' line). ONE ALBUM A WEEK (config/album-launch-slots.json, gate [10c]; Cabana + Après-Ski = double album, week of Dec 7). Album model: READY (hidden page + every launch asset) then a dated LAUNCH (FYM complete first). Petalée = backup album. Deco albums may drip one per week. FYM SHIPS CONTINUOUSLY (rule 0b): no holding for 1.NN; partner launches in FYM BEFORE the drop. Never defer to "tomorrow". Brand watch = LIST + one group post (edits after), no graphics unless she asks; findings go to the Brand news sheet the moment they're found. Collab invites ONLY on that brand's own-product posts. Reels: 9:16, album cover as cover, a suggested song, segment length = her cut, text never edge to edge. Profile set ends on "But she likes to play the field" → FYM (FYM is the headline, not the album). Reel kit = album top 8 × 3 FYM views with each mat's own album racks; Canva Mats folder = ALL album mats. Never change an approved graphic when re-framing. TdT: type the code in our own group; link the BRAND's product page.

**Standing (Nov 4):** A YES IS A YES · BLOCKED IS NOT DROPPED · REVENUE WATCH · NO 'ASK ONCE' · SOCIAL 13 (nothing disappears from Planoly) · payouts are CASH via PayPal (Bam Bird = bank transfer), only Maison Mahj + PLM Level 1 are store credit · ShopMy pickup DAILY 9:02am · Chrome: no saved tabs · IG evergreen codes post = profile-only.

## Tomorrow's top priorities (Thu Nov 12), in order
Standing order: RESTOCK FIRST (rule c), then Google #1 (Tiffany Oct 29 11:03pm), then the newest ANSWERS (Nov 11: one working chat, FYM all-or-nothing, partner coverage, FB group intros, OMM VIP post, no swipe books), then DESK 'Never-ending'. **Restock check (c): no album-set RESTOCK is dated Thu Nov 12** (next album-set windows: Bam Bird Deco Indigo Nov 16-30, Sunday Blues Nov 23-30; Let's Mahj On new lineup window opens Nov 12 but is not an album set).

1. **Google (Main). First thing.** Wed's report (docs/reports/google-revenue/2026-11-11.md): MAHJMATCH named in **26 of 39** AI answers (Tue 30/38). NEW LOSSES Wed: **Anders Ruff** (top earner; MOCKINGBIRD10 now first), Charleston, Amahj, Yellow Mountain, Soirée. Still lost: Bam Bird (3rd check), Virora, Bespoke, I Love Mahj; OMM page 2 (~#9). (a) Indexing quota Thu: Anders Ruff + Charleston pages first, then Amahj, YMI, Soirée, then Bam Bird/Virora/Bespoke/I Love Mahj (15 requested Wed). (b) **Deco Lagoon has no hq/indexing row (3rd night)**: add it. (c) Fri M/W/F code report. (d) HQ Today #1 = 16 order screenshots (merged card).
2. **Social, rule d (Main, attended for Planoly writes): 0 IG posts SCHEDULED Nov 12-18** (every scheduled group sits in the Dec 7-10 review week). **Juniper launched Wed 10am CT with NO IG mat-ch**: the Juniper × Palm Royale It's a mat-ch! + story (groups …1d8d96 / …03eeae, Dec 9 slot) never moved back. Default on her yes (HQ Today #2): post it Thu after 10am CT. Then Thu 'New this week' carousel (draft 01a1c214), Fri 'Tiles first or mat first?' (01a1b20d-761e + story -77bc), Sat 'Tap a color' (01a1b20d-794b + -7b0e), and the **Deco Lagoon social launch kit for the week of Mon 11/16** (her Nov 11 9:12am). Target ≥4 IG posts in the window.
3. **jsDelivr 403 / FYM releases (Main).** Nothing new can pin (repo > 50 MB). Staged Nov 11: FYM 1.19 = Miss Mahjong racks + ALL current walls (282/282 visible sets) + 5 OMM retired mats; plus Lotus Cove photo, holiday-off mat-door bug, brand weights, plain-link conversions. Fix the asset host (slim repo/branch) → gate + independent QA → three places. Also FYM size ceiling (13 MB file, 20 MB jsDelivr cap) before any big-catalog import.
4. **Newest asks (Main, Nov 11).** (a) **OMM VIP group post TODAY Thu** (her 5:32pm: OMM-only rainbow of our OMM albums + 'hope you got Juniper'; draft assets/social/omm-vip-nov12/; she posts it, her Mahji Mentor account) — it sits inside the FB-intros Google Doc card. (b) FB group intros: her wording in the Google Doc; reminder Thu evening (HQ Today #3). (c) Fait à Main real code (UpPromote portal) + Sweet Jojo follow-up draft Fri if no approval. (d) Let's Be Besties feature-week reply draft for her yes.
5. **Match inbox (rule e) + Chrome backlog (Main).** MATCH-INBOX: **~120 dated lines older than 2 days have no DONE mark** (heuristic; ~96 Tue): mark each DONE with its build or fold into the next small release. Chrome (her computer on): **Black Friday deals page (her yes Nov 8; live before PLM Black Friday Mon Nov 16)**, Today-in-mahj 11/10 edit, Charleston + TdT link swaps, holiday blog lead image.

- **Tiffany's approved matches** (config/tiffany-matches.json): social picks come from this list FIRST.

## Handoffs (do first)
- **Found Wed Nov 11, given a home tonight:** Juniper launch passed with no IG post (priority 2); Juniper email send unconfirmed (HQ Today #2); OMM VIP post drafted for Thu (priority 4a); 2 new lint FAIL kinds (OVERDUE); Deco Lagoon hq/indexing row (priority 1b); App icon options + usage report built (b9828ecb) wait her look (HQ This week).
- **Launch watch Wed 11/11 6:05pm ET**: NEW Mahj Pit The Raven Tiles - Large ($395 tile set; likely the Nov 7 'Full Sizes Black' placeholder, which is gone) + 7 new partner mats (Mahj Pit Birds of a Feather / LaMarie / Evergreen; LBB Confetti Kaleidoscope, Sedona, Cajun Christmas, Blueberry Hill). Sheet rows (Raven + Confetti Kaleidoscope; the rest were already there) + NOW push sent; MATCH-INBOX lines for FYM; Raven on Albums tab as needs-tnt. OPS: search Tiles & Tablescapes for Mahj Pit The Raven Tiles. OPS: copy assets/launches/mahjpit-{the-raven-tiles-large,birds-of-a-feather,lamarie-mat,evergreen-mat}/ and assets/launches/letsbebesties-{confetti-kaleidoscope-ohbon-studios-artist-mahjong-ma,sedona-lillian-claire-designs-artist-mahjong-mat,cajun-christmas-lillian-claire-designs-artist-mahjong-mat,blueberry-hill-lillian-claire-designs-artist-mahjong-mat}/ to Dropbox /Mahj Matchmaker Albums/New releases/<brand>/ today. Also recorded only: Mahj Pit Commuter Christmas (travel tiles), 3 Splash of Color engraved tile sets.
- **Launch watch Wed 11/11 9:15am ET**: 6 new partner mats live (Mahjong Register Poppy & Prep / Tangerine & Twist / Blaire & Briar / Rosewater & Wine; Let's Be Besties Sleeping Tiger + Chinoiserie Cabbage Plates). Sheet rows added + push sent; MATCH-INBOX lines for FYM; no group post drafted, no swipe books built (non-OMM, waits its turn). OPS: copy assets/launches/mahjongregister-{poppy-prep,tangerine-twist,blaire-briar,rosewater-wine}-double-sided-neoprene-mahjong-mat/ and assets/launches/letsbebesties-{sleeping-tiger,chinoiserie-cabbage-plates}-wanda-viola-artist-mahjong-mat/ to Dropbox /Mahj Matchmaker Albums/New releases/<brand>/ today.
- **Main: Juniper launch kit** (priority 2). Reel files: assets/social/juniper-launch/reel/ (phone segment 16.0s), end frame MP4 (Canva Juniper folder), cover assets/covers/albums/reel-tall/juniper.jpg, caption assets/social/juniper-launch/reel-dating/ig-caption.txt (lint length FAIL, see priority 4).
- **Main: FYM racks-only release** (Miss Mahjong 5 acrylic racks; builder/fym_fix_nov10/racks119_missmahjong.py + release119.py; config/fym-rack-adds-nov10-missmahjong.json): blocked only by the jsDelivr 403 (priority 3). Version numbers: racks-only = **1.19 = site-app/fym-v119**; the staged bundle (Deco Lagoon, link routes, LBB Artist Collective 174, Mahjong Register relinks, racks119.py …) = **1.20 = site-app/fym-v120** ON TOP of 1.19, and per rule 0b each piece should ship as its own small release, not one bundle.
- **Main (was Matches & Catalog): Cabana Club tile set staged** (config/fym-adds-nov10-cabana.json, walls #91cad6, coordinated mat; u = SHOPMY_PIN_PENDING until the ShopMy pin exists). Swipe book https://claude.ai/artifact/XRpLKsiby4hFpvVQUMNcVM (book_gate PASS) waits her tile-photo yes + swipes. Double album with Après-Ski, slot week of Dec 7, ready by Fri Dec 4.
- **Main: Brand Watch website page** (OVERDUE, her 8:01am ask): preview artifact https://claude.ai/artifact/18JAJeZRLcZtcqVejgKHMs (scripts/site_brand_watch.py). Her 7:55pm brainstorm (photos/collage, hot vs minor, grouping by brand, consistent shop links, partner self-serve idea; partner vs non-partner open, lean like FYM): fold into v2 and show her; not on social yet.
- **Main: reel end frames**: scripts/social/animate.py (MP4 end frames for Canva) "not yet run to completion" (526f4d24): finish it for the next album (reusable per set).
- **Main: Juniper subscriber + album-requester emails**: Juniper list email is the draft above; the album-REQUESTER email (people who asked for Juniper) is still to send (docs/NEW-ALBUM-CHECKLIST.md 3-4).
- **Main: Mahjong by SI onboarding** (approved Nov 9): code-truth, brand page, hub, FYM, IG, newsletter. Not started.
- **Main: Partner feedback watch** trig_01RKw9eUwTYPo39gbYHb65gh ended its planned run Tue (0 real partner items Nov 1-10). HQ card partner-feedback-watch-end asks her OK to turn it off; on her yes, update_trigger enabled=false.
- **Main: HQ page bug** 'TypeError: rc.forEach is not a function' (since Nov 9 12:47pm, 2 sessions Tue): guard with `Array.isArray(rc) ? rc : Object.values(rc||{})` in the {path, why} link list and republish HQ (read the saved HTML first).
- **Main: TNT scans not merged**: project docs '81b TNT scan Nov 3' + '81c TNT scan Nov 10' hold JSON for config/tnt-recs.json (Nov 10: 15 mats for 5 sets incl. Deco Mulberry 25-comment thread, Sunday Blues Tala Midnight Wildflowers): merge, dropping mats already in a book.
- **Main: hq/launches** is ~248 KB of the 256 KiB cap: archive pre-Oct 25 items before the next add.
- **OPS (Chrome)**: see priority 5 for the order. Plus: follow + favorite @mahjonggmaven + @mahjpit.co (docs/IG-FAVORITES.md); Payout Tracker September check; copy flat renders to Dropbox (LBB Artist Collective 174, Let's Golf! ×2, Cabana Club tiles + mat, Fait à Main Texas Mon Amour, LBB Tidal Glass / Seasons / Nutcracker / Tropical Travels, Bam! teaser, Soirée Holiday Chintz, Wren Gingham and Wine).
- **Main: older handoffs still open**: blog posts that name album tile sets without linking them (list in git show 09006524:docs/DESK.md); revenue-alert cards → one Money summary; prompt fixes (sales-check mails, "close leftover tab groups", mat-edit-alert step, "wholesale customers only"); config/pinterest/queue.json vs Planoly resync; Mahj & Moon 'pending_fix' when the 7 Etsy ShopMy links land.

## In progress
| Item | Owner | Next step | Target |
|---|---|---|---|
| Google: 4 lost AI answers (Bam Bird, Virora, Bespoke, I Love Mahj) + OMM/My Fair/PLM/Mini Mahjer | Main / Ops | Indexing re-requests in that order; Bam Bird revenue investigation. | Thu Nov 12 (slipped from Wed Nov 11) |
| Google code report + scorecard | Main | Wed ran (26/39); next M/W/F run Fri. | Fri Nov 13 |
| Indexing: 23 changed brand pages left + Deco Lagoon row | Main / Ops | ~10/day; add the Lagoon row. | Fri Nov 13 |
| Juniper launch day | Main | Tiles + Lotus Cove LIVE Wed 10am CT. Left: IG It's a mat-ch! + story (parked Dec 9 slot) on her yes, email send (HQ Today #2), requester email. | Thu Nov 12 |
| jsDelivr 403 → slim asset host | Main + Main (was Matches & Catalog) | Priority 3; curl new pins. | Thu Nov 12 (slipped from Wed Nov 11) |
| FYM racks-only release (Miss Mahjong racks) — OVERDUE | Main | After the 403 fix: gate + independent QA + three places. | Thu Nov 12 (slipped from Wed Nov 11) |
| FYM small releases: holiday-off mat-door bug, Lotus Cove photo, Cabana, Deco Lagoon m-list, Register links, LBB Artist Collective | Main (was Matches & Catalog) | One small release each, same day as unblocked. | Thu Nov 12 |
| Search index rebuild (03402daa staged, NOT pasted) | Main (was Matches & Catalog) / Ops | Paste with the next gallery/FYM release. | Thu Nov 12 |
| Dear Santa push + holiday album reels (OVERDUE) | Main | Dynamic style; schedule auto-publish. | Thu Nov 12 |
| Brand Watch website page (OVERDUE) | Main | v2 from her brainstorm; her look; hidden page via Chrome. | Thu Nov 12 |
| Black Friday deals page (her yes Nov 8, OVERDUE) | Ops (Chrome) | README steps 1-6; index; link. | Fri Nov 13 (before Nov 16) |
| Match inbox: ~96 unmarked lines | Main (was Matches & Catalog) | Mark DONE or fold into a release. | Thu Nov 12 |
| Sunday Blues album (TNT redo first) | Main (was Matches & Catalog) | Album Playbook; launch slot = its ~Thanksgiving restock week. | Fri Nov 20 |
| Deco Mulberry + Indigo (may drip one per week) | Main (was Matches & Catalog) | Re-pull + discovery with the Nov 8 + Nov 10 TNT leads; slot each. | Fri Nov 13 |
| Cabana Club + Après-Ski double album | Main (was Matches & Catalog) | Her tile-photo yes + swipes; ShopMy pin. | Ready by Fri Dec 4 |
| Rackin' Rudolph cards → her Canva tile photo (OVERDUE) | Main (was Matches & Catalog) | Lock crop, re-render 36, paste. | Thu Nov 12 |
| Holiday completeness audit (year-round album pages) + yes-vs-live check (OVERDUE) | Main (was Matches & Catalog) / Main | OVERDUE lines. | Thu Nov 12 |
| Album wiring gaps (C1: 7 live albums not wired to FYM) | Main (was Matches & Catalog) | Gap audit C1. | Thu Nov 12 |
| Mahjong by SI onboarding | Main (+ Ops) | Code-truth, page, hub, FYM, IG, newsletter. | Thu Nov 12 |
| Mah Jongg Maven onboarding (page live; code-truth done tonight) | Ops / Main (was Matches & Catalog) | Hub logo, IG follow/favorite, FYM. | Thu Nov 12 |
| FB group week (Thu table thread, Sat help-me-match) | Tiffany yes → Main (Chrome) | Default: post both as drafted. | Thu Nov 12 |
| New arrivals carousel (Thu 11/12) | Tiffany yes → Main | Draft 01a1c214 in Planoly; schedule on yes. | Thu Nov 12 |
| Work With v3 + Brands form | Ops | Default: goes up HIDDEN next Chrome trip unless she says wait. | Next Chrome trip |
| Planoly roll-forward + story-caption fixes | Main (attended) | Unattended update_post refused (7th night); this run made no Planoly writes (no FB target missing). | Thu Nov 12 (slipped from Wed Nov 11) |
| ManyChat comment-for-links draft + trial reminder (OVERDUE) | Main (Chrome) | Low priority. | Fri Nov 13 |
| Discount links not converted (Britt Mills, Register, YMI, RMS, Hip Hip, Wren/Soirée/Amanda Toppe) | Main | Fold into link-routes. | Fri Nov 13 |
| PEACE LOVE → Level 2 ($5K/month → cash) | Main | Plan + PLM MTD in the report. | Fri Nov 13 |
| Affiliate applications: Haus of Charleston, Lemondrop, The Mahjong House, Bloomjong, Sweet Jojo | Partner watch | Watch mahjmatchmaker@; onboard on approval. | On approval |
| UpPromote accounts → mahjmatchmaker@ | Tiffany / Main | Screenshots before each switch. | Fri Nov 13 |

- REVIEW WEEK Dec 7-10 in Planoly (Tiffany Nov 9 1:09am): parked feed posts + single-frame stories. Real date = Dec date minus 28 days. Before Dec 6 EVERY one must be moved back (approved) or unscheduled, or it auto-posts. Owner: Main + nightly desk cleanup.

- Main: DECO LAGOON SOCIAL LAUNCH week of Mon 11/16 (Tiffany Nov 11 9:12am: true launch for social; album page already live). Build the Juniper-style kit: intro carousel (profile cards) -> It's a mat-ch -> reel + cover (FYM phones top 8, album racks), every-slide stories, FB Page targets, Planoly drafts; per-album Canva folder. Deco card was taken off /links Nov 11: re-add it (site/livepatch/links-nov11/README.md) on launch day.
## Blocked, approved (raise at the top of every attended reply until done)
- **Every new site pin (jsDelivr 403, repo over 50 MB)**: FYM racks release, FYM fixes, gallery, search, album images. Priority 3.
- **Planoly roll-forward + story-caption fixes**: unattended update_post refused (7th night, Nov 10). Attended Main: past-dated drafts (Mon 11/9 FYM how-to 01a1b20c + story 01a1b20d-690f = Papaya, held for rebuild per her Nov 9 1:15am call; old Nov 4-8 multi-frame story drafts 01a1a2b6-7c27/-73c7/-7717/-7a6d are superseded by the single-frame review-week stories: ask her once whether "superseded" = remove).
- **Chrome-only steps approved by her** (Today-in-mahj 11/10 edit, Black Friday page, Charleston + TdT link swaps, holiday blog lead image, Mahjong Row blog sentence): Chrome offline most of Nov 9-10.
- **Partner newsletters, 9 stores block automated signup (Shopify hCaptcha)**: Amahj, Bam! Let's Mahjong, Mahj Mood, Let's Be Besties, Mini Mahjer, My Fair, The Mahjong Press, Tigre de Tartán, Splash of Color. Her ~10s each on her phone; then mark docs/PARTNER-NEWSLETTERS.md.
- **Bing Webmaster Tools** (her yes Nov 6): one tap from her on Google's account chooser (OVERDUE line has the steps).
- **The Mahjong House affiliate**: her click on Confirm in their UpPromote verify email.

## Waiting on Tiffany (only things she can answer now)
**On HQ Today, in this order (5):**
1. **Google + sales: 16 order screenshots** (Bam Bird ×3, Bird & Bamboo ×3, Mini Mahjer ×3, Charleston ×2, My Fair ×2, Middle & Main ×2, +1); the Nov 10 + Nov 11 amounts cards and both Google alerts are merged into this one. Google's AI answer names MAHJMATCH for 26 of 39; Claude re-requests the lost pages.
2. **Juniper is live: send the Juniper email (Squarespace draft) + yes to post the Juniper It's a mat-ch! Thu** (default: post it Thu after 10am CT).
3. **Facebook group intros + OMM VIP post: her wording in the Google Doc** (reminder Thu evening).
4. **Facebook group: Thu table thread + Sat help-me-match: one yes** (default: post both as drafted).
5. **Work With page v3 + Brands form: live yes** (since Nov 1; default goes up hidden next Chrome trip).

**On HQ This week:** Holy Mahj full Canva image (moved from Today); Quick calls from Sunday (defaults in place); ShopMy 6 quick calls + 2 stray links; 1 hidden FYM photo (Grace Peacock); this week's posts in Planoly's review week; Brand Watch tab.

**Asked in chat, not yet answered (the owning chat RE-ASKS at the top of every reply, with its default):**
- Main (was Matches & Catalog) (Nov 10): OK to delete the separate 'Today in mahj, part 2' group post now that the 11/10 post was edited to include it (default: leave it; deleting needs her yes); Cabana Club tile photo yes + swipes; Juniper reel swipes re-timed to the beat if she gives timestamps.
- Main: Holly Jolly Red grid + Dear Santa reel v3 (Nov 9 11:23am; default: schedule both once she says yes); remove the old launch-reel draft + dropped Rudolph/Polo/Rattan drafts (default yes, archive record); 84 locked FYM colour changes (default apply); hide /bird-and-bamboo-discount-code-2 (default hide); Malachite how-to reel v2 OK + day; pinned reel v3 A or B; Brand Watch page partner vs non-partner (lean: like FYM).
- Main (was Matches & Catalog) (older): Seabreeze × LBB Aloha card into FYM m-lists? (default no); Lagoon + Mulberry splits vs new pile photos; Bam Bird Classic Tortoise match pick; Sunday Rattan = Blue Rattan?; Fruit Stand rack-edge (default a); brand-lock pricing (undecided, don't push).

## Banked (finished, held on purpose)
- **OMM Nantucket restock frames (Nov 9)**: assets/social/restock-nantucket-nov09/out/nan-A/B/C (live FYM screens); same-day window passed, HQ card archived (rule 9). Reuse at the next Nantucket restock/reshare.
- **Holiday album grids + 10s teaser reels (Nov 9 1:31am)**: assets/social/holiday-album-grids (11 albums): the base for the dynamic rebuild (OVERDUE line); not for use as-is (her 1:37am: must be dynamic + sell).
- **Juniper eye-candy grid**: full-mat version POSTED Nov 9 12:30pm (IG + FB Page + story); close-up version rejected.
- **Style of Your Life (My Fair Mahjong) album**: round 1 built Nov 7 (22 cards, site/livepatch/mfm-style-of-your-life-album-nov07); SKIPPED for now (her Nov 8 10:11am 'Skip My Fair Mahjong album for now'; set dropped Nov 7, Dillard's exclusive).
- **Deco review pages Nov 8 10:45am (Mulberry 8V74MMkepN9TnVCF5cRNAw, Indigo 9VjoeB1ejRB3wVvnMaKMqH)**: OUTDATED by the Nov 8 TNT/Silk redo; replaced in place when the re-pull is done. Don't send these links.
- **Petalée (Virora)**: 61 cards, RTS `l-final-petalee`, vault (her Oct 28). Nov 10 12:20pm: BACKUP album (a gap week, a Virora Petalée restock, or spring). Before publishing: colour card, 10% band sweep on the Amanda Toppe/Girly cards, cleaner Petalwing/Coralia photos. Table-view walls now staged (1.18).
- **Wren Christmas Village restock (Nov 8)**: first batch, reshare window passed; HQ card archived (rule 9).
- **Restock frames Nov 7**: Pearlescent (assets/social/restock-pearlescent-nov07/out/) + Florielle (assets/social/restock-florielle-nov07/out/): not posted; reuse at the next restock/reshare.
- **Launch reel redo (spotlight, no Mahjong Row)**: Planoly reminder 01a1b30e-67a2, superseded by the pinned reel 01a1b83b-fc22 (v2 in Planoly, v3 A/B built Nov 8); re-ask to remove.
- **Mahjong Row & Co. fall album**: parked (brand OUT, Nov 6). Parked site copy: archive/mahjong-row-parked-2026-11-06. MR mats may still enter new albums on merit (Nov 7 7:01pm).
- **Holiday intro reel v5** (46s): POSTED Nov 3; the reference standard for FYM reels (FYM-REEL-RULES 23-41).
- **Retro Rattan holiday table reel + 7-frame story**: undated Planoly drafts (01a16477-0588, -078d). Mood-board/table reels DROPPED (Nov 6 4:11pm).
- **Night of the Raven mood board reel + Halloween story + old Raven carousel**: next Halloween (docs/planoly-archive/2026-11-03-deleted-drafts.json).
- **Vivienne mat album (OMM)**: 16 cards, parked (no mat albums, Oct 23); its hearts go into the tile albums.
- **Season 2 tile-dating episode reels (Ep 1-13 + trailer)**: PARKED (Nov 3 "down the road"); captions fail lint: rewrite before reuse. Jade "Smith-style" reel parked (needs her song).
- **Holiday reels Nov 1** (assets/social/holiday-nov1/): rebuild to the v5 standard before use.
- **Face-to-camera script + Ask Me Anything carousel** (assets/social/next-week-talk/): drafts.
- **Poppins mat-alert set** (assets/social/mat-edit/poppins/): CONFIDENTIAL until OMM announces Poppins.
- **Partner kit explainer video v2 + launch explainer reel + tutorial reel**: built, not used.
- **Restock companion frames** (restock-oct27/, restock-huntclub-oct30/, restock-tinselle-oct31/): reuse at the next restock.
- **Brownstone Bloom group post**: not doing (fall is past).

## Later / ideas
- **Brand Watch page as a 3rd bookmark reason + partner self-serve updates** (Tiffany Nov 10 7:55pm brainstorm, no decisions): photos/collage (also a 'Brand Watch, updated daily' social piece), hot vs minor, grouping by brand, consistent shop links; partner vs non-partner open. Not on social until it's good.
- **Consolidating chats / Fable / Google Sheets of what Claude knows and does** (Tiffany Nov 10 12:15pm questions): she is staying in Main (was Matches & Catalog) for now; said-vs-done audit sheet started (12:21pm).
- **Anders Ruff bridal mat + tiles collab** (sneak peek Nov 10, no date): HQ Later card; watch for the drop.
- **RMS Heirloom Crown Jewels** (coming soon, no date) + **TdT Birdsong 'back soon'** + **OMM Gemma restock in 1-2 weeks** (watches Nov 10): record; Gemma has an album → restock-first rule when dated.
- **Discount-code presentation model** (Tiffany Nov 9 4:18am): @for_the_love_of_mahjong bio links + lourdesnorton.studio 'The Mahjong Edit' (tiered brand list, one code, linked from the IG bio). Main proposes a /links or hub variant when the Google work allows.
- **Second Dear Santa post ~Nov 20** (last call before it ships; her Nov 9 4:34am).
- **Story link-sticker lane in reels** (Tiffany Nov 8 4:05pm; Claude recommends yes): reserve a clear zone so a story repost can carry the link. Main adds it to FYM-REEL-RULES on her OK.
- **Mat Gallery filter hiding Etsy/Amazon-sold mats** (Tiffany Nov 8 3:06pm idea; goes by the actual store, not ShopMy): her call.
- **FYM opening to all brands** (Nov 8 2:03pm direction, paused while she does partner outreach); show-frequency caps per brand instead of catalog caps (Nov 8 4:51pm). Non-partner gates unchanged until she says.
- **Google AI insight log** (docs/research/google-ai-insights.md, Nov 8): every entry splits AI Overview vs AI Mode and marks VERIFIED vs UNRELIABLE; data before Nov 5 is skewed.
- **"Retired mats on retired tile sets" angle** (Tiffany Nov 7 8:24pm): OMM's Build Your Set can't show it; reel + caption line; she may mention it on the OMM VIP page. Main storyboards it for her yes (target Thu Nov 12).
- **FB Page growth** (21 followers) + **FB group low-effort engagement** (~7 new members/week, no welcome posts) (Tiffany Nov 7 5:00pm): research docs/social/fb-page-growth-2026-11-07.md; group week draft = Waiting on Tiffany.
- **AI-visibility tool** (docs/research/ai-visibility-tools-2026-11-07.md, Peec AI Starter $95/mo recommended): costs money = her call; Main brings it with the OMM-first plan, don't push (Nov 7).
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
- **Clean up 52 legacy caption lint warnings** (still 52 Nov 10) (config/social/content_lint_baseline.json; mostly missing #MahjMatch, '(affiliate)', 2 TdT captions) (rules audit E9, Oct 30). Also legacy repo FAILs in banked Season 2 / episode / holiday-table captions (Nov 10: length 42 legacy + 2 new plain_post, naming 36, brand-tag 2 new-check on S2 Smith). Planoly IG lint 51 FAIL under Tue's stricter lint (32 = profile-only codes post brand-tags; rest = story captions, New this week FB 361, banked Retro Rattan).
- **FYM Shuffle** idea for 1.15 (Main (was Matches & Catalog), Nov 3).
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
- **Mahjong Register** Crystal Palace acrylic racks + Solid Wood racks (launch watch Oct 31): FYM rack lists when Main (was Matches & Catalog) has room.
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

### Added during Wed Nov 11 (carried as-is)
- Main: TIKTOK on the radar (Tiffany Nov 11 9:14am). Plan: she creates @mahjmatchmaker (business account) + connects it in Planoly; Claude reposts the reel bank (FYM, holiday, album reels) 3-5x/week as Planoly drafts with TikTok-library sounds, captions with MAHJMATCH typed (never next to Tigre de Tartan), varied cuts/hooks rather than identical reposts. Waiting on the account.

### Idea (Tiffany Nov 11 11:46am): mahjong x weddings SEO, ride the Anders Ruff bridal launch
- Trigger: Anders Ruff bridal mat + tile set (collab with an OG Bachelorette, no date yet). She knows from Heritage Sign Co that the wedding market is huge; mahj x wedding has almost no competition.
- Search check Nov 11: "mahjong bridal shower" / "mahjong bachelorette party" / "mahjong wedding gift" return only Etsy listings, Anders Ruff's own party-theme post and one thin AI blog. Nobody owns it. Bam Bird bundles are sold at Crate & Barrel = registry-able (wedding registry angle).
- Plan (Main, needs her yes on the post): one guide page "Mahjong for weddings: bridal shower, bachelorette and registry gift sets" built ahead, live the day Anders Ruff launches; brides' palettes -> matched tiles + mats; add terms to the next Keyword Planner pull; Pinterest board "Mahjong bridal shower".

### Hanukkah + New Year's (Tiffany Nov 11 12:40pm; small, don't over-spend)
- ONE Hanukkah table piece (mood board + short blog section) before Dec 1 (Hanukkah = Dec 4-12): Noli June Eighth Night mat + Hanukkah dish, a blue tile set; partner Hanukkah tiles exist (Splash of Color Hanukkah sets, Sweet Jojo Judaica Pearl). Less competition than Christmas.
- New Year's phase (late Dec): Noli June Rochelle Didn't Make It to Midnight mat + NYE dice dish, Splash NYE Glitz Gold mat. config/seasonal-tags.json.
- Winter tile sets for ski/apres content: CMC Apres Ski Club, Virora Nivalee, Bespoke The Chalet (Frosty Pearl White / Lilac), Maison Mahj Apres Mahj (sold out).

### From Tiffany Nov 11 12:57pm
- **Charleston Mahjong Club Hunt Club vlog (Main, Chrome):** her review VIDEO of CMC Hunt Club tiles on Mahjong Moxie's Duck Camp mat sits in our PRIVATE Facebook group. Find the post (facebook.com/groups/mahjmatchmaker, search "Hunt Club"), note its date, grab stills, and publish it as a BACKDATED blog post / vlog with photos (SEO: Charleston Mahjong Club Hunt Club tiles review, + their other theme sets: Après Ski, Cocktail Club 2.0, Yacht Club, Country Club, Cabana Club; code MAHJMATCH). CMC likely doesn't know she ever featured them. Ask before downloading the video file.
- **Holiday-break TRAVEL week** (mid-Dec, when it's too late to ship holiday tiles): travel sets before vacations: Miss Mahjong Mini Miss Classic (new), Mini Miss Out of Office (sold out now, "coming back": watch), CMC Cabana Club travel bundle; Cabana Club album releases that week or EARLIER (as soon as it's done: leave shipping time, avoid sell-outs). Christmas Vacation theme.
- **Priority:** Bespoke + Charleston are her top two of the lineup. Bespoke = decent-sized brand with no representation: work harder for them.
- **CMC ShopMy vs code test (Tiffany Nov 11 1:04pm):** on the next Charleston order email, check whether the same order also appears in ShopMy earnings (Chrome, ShopMy dashboard) -> tells us if link + MAHJMATCH pays ShopMy 15%, the CMC program 10%, or both. Record in docs/LINK-ROUTES.md.
- **Album requests tracker (Tiffany Nov 11 1:19pm):** requests land in tiffanybrie@ Gmail ("Form Submission - Album Requests", label Site/Album requests) + Squarespace Contacts > Form submissions; this cloud session's Gmail is mahjmatchmaker@, so pull them in Chrome: every request (date, set, brand, email) -> config/album-requests.json + a count by set; surface the top requested sets on the album lineup page. Needed for My Fair Mahjong pick.
- **Miss Darling twin album (Cameo Blue + Lilac) (Tiffany Nov 11 1:34pm, top tier with CMC + Bespoke):** build before Lilac's preorder opens (store says coming soon, no date; partner watch flags the day it opens). Tile photos: Lilac store renders saved assets/launches/miss-darling-lilac/; Cameo Blue from the store.
- **OMM album card counts (CORRECTED Nov 11 2:30pm; the 1:38pm 'Lagoon 9' numbers were WRONG, Tiffany caught it).** Counted from the LIVE album pages (unique card images): Sunset 22, Limoncello 25, Taylor 31, Sorbet 34, Gemma 35, Luminaire 35, Pippa 35, Glitterville 36, Palm Royale 39, Sierra 40, Emerald 41, Seabreeze 42, Lagoon 50, Glow Wild 53, Solara 53, Willow 59 (max Heritage 2.0 92). No OMM album is thin; only Sunset and Limoncello sit in the low 20s. Thinnest overall are vault albums Lilac Soirée 12, Sunday Tile Set 12, Preppy Soirée 21, Spring Love 22. Thin-album rounds paused until she says which (if any) to grow. Source of truth = live pages, never HQ.
- **Sunday albums (corrected Nov 11):** all 4 already have cards built Nov 6 from her yeses (Nature Walk 42, Sunday Blues 56, Plum Panda 41, Hummingbird 41: assets/cards/<set>/). No more swiping. Sunday Blues = finish first (album_gate steps 3b-8: other FB groups, mat discovery, catalog check, by-sight left-outs, holiday, faces) then review page -> her final look -> staged hidden for Sunday's ~Thanksgiving restock. Then the other three, each timed to its restock.
- **Royal Mahjong Society shortlist (Tiffany Nov 11 1:47pm, no decision; out of season now):** Shore (sand/beige beachy neutral, underserved; "launching early November", sold out/coming soon) = summer; Newport (signature nautical, royal blue, lobster jokers; restock mid/late Nov) = Memorial Day / 4th of July; Cottage (peach + green, launching early Nov); Girly; Island (Seabreeze colours, bold reds). NOT Crown Jewels. All Heirloom, full size, $425.
- **Blog: favorite tile storage (Royal Tile Bag $58: twilly scarf, divider = display case, great for teaching the suits; + OMM tile bags).** No storage/bag article exists (checked sitemap).
- **Blog/Social: "Tiffany's Favorite Things" mahj gift guide (her idea Nov 11):** evergreen mahj gifts, fills December after holiday-tile season; Royal Tile Bag first. Ask her for the rest of her favorite things list.
- **Petalée readiness check (Tiffany Nov 11 2:03pm):** banked album (Virora's most popular set, $229) built Oct 20 under the old process: no config/album-records/petalee.json, album_gate fails [0]. Do a readiness pass (record, gate, card look, updated dragons in tile photo) in a spare-usage session; target February pinks/reds slot.
- **Spare-usage projects (her rule Nov 11):** when she says "use the spend" (e.g. 40% left before the weekly reset), do banked/reel work: album reels, Petalée check, OMM thin-album rounds. Never burn usage mid-project.


## Daily operations (Wed Nov 11)
| Operation | Done today? | Notes |
|---|---|---|
| Affiliate tracking (Money tab) | ✅ Done (12:04am close pending) | Wed by 12:45pm: 6 orders, $54.22 known + 3 '?'; MTD $2,655.01 known. Tue closed: 11 orders. Screenshots = HQ Today #1 (16). |
| Google & Revenue report | ✅ Done | docs/reports/google-revenue/2026-11-11.md: 26/39 named; lost Anders Ruff, Charleston, Amahj, YMI, Soirée; back Mini Mahjer; SC clicks -43% wk/wk. Alarm YES. TdT brand page 23 links → auto-apply. |
| Google code report + scorecard | ✅ Done | Scorecard 2026-11-11: AI Overview 26/39, Google top3 32/39, AI Mode 37/39. Next: Fri. |
| Verified dates (weekly, Mondays) | ⏭ Not due | Next Mon Nov 16. |
| Codes post (Mondays) | ⏭ Not due | Next Mon Nov 16. |
| Pinterest queue health | ✅ OK | 4/day scheduled Nov 12-26 (Nov 12: 3), more beyond, 0 errors. |
| Indexing | ✅ 15 requested (hq/indexing) | Deco Lagoon row still missing (3rd night) → priority 1b. |
| Planoly next-7-days (IG + FB Page) | ❌ 0 IG scheduled Nov 12-18 | All 36 scheduled groups are in the Dec 7-10 review week (every IG grid has its FB Page target + story groups) or are past-dated reminders (Oct 21 Papaya story, Nov 10 Juniper reminder grid: IG-only, past, left as-is). Tag people: all handles verified. content_lint --planoly --only-ig: 51 FAIL, same posts as Tue (brand-tag 32 = profile-only codes post; hashtag 8, mahjmatch-missing 7, length 4), no new kinds. No FB target needed adding. → priority 2. |
| New albums (last 7 days) (f) | ⚠️ 1 miss | **Juniper**: /mahjong-tile-matches ✅, Green ✅, OMM page ✅, /links ✅, hq/indexing ✅, Pinterest ✅. **Deco Lagoon**: index ✅, Blue ✅, Bam Bird page ✅, /links ✅ (card is back), Pinterest ✅; ❌ no hq/indexing row (3rd night, OVERDUE). |
| Repo caption lint (g) | ⚠️ 2 new kinds | 90 FAIL (length 45, naming 36, banned-phrase 5, brand-tag 2, mahjmatch-missing 1, hashtag 1). NEW kinds since Tue: **banned-phrase** (today's no-'every' rule hits the Juniper plain + reel-dating captions and banked S2/ep05 Heritage) and **mahjmatch-missing/hashtag** on assets/social/omm-vip-nov12/caption.txt (OMM-only VIP group post, MAHJMATCH left out on purpose: exempt it). OVERDUE line, Main. |
| Live codes check | ✅ PASS | 40 brand pages + hub (morning report). |
| Gallery sync check | ⚠️ Not run tonight | Live FYM still 1.18; nothing shipped (jsDelivr 403). Morning run. |
| Coverage + card sharpness | ✅ Ran (coverage.json committed 1:30pm) | partner_coverage now on the front door; 146 FYM readiness gaps baselined (gate [173]). |
| Restock first (c) | ✅ Checked | No album-set restock dated Thu Nov 12. |
| Match inbox (e) | ⚠️ ~120 old lines unmarked | Priority 5. |
| Launch + partner watch | ✅ Done | Partner watch 1:55pm + 6:30pm (6 restocks live, Mahj Pit holiday drop), launch watch 9:15am + 6:05pm (8 new handed to FYM), IG stories check 8:37pm (Brand Watch v21). |
| FYM + partner feedback | ✅ 0 new | Partner feedback watch ended; HQ ask to turn it off still open (HQ This week). |
| FYM releases | ❌ None | 1.19 (racks + walls) staged, blocked by jsDelivr 403 (priority 3). 1.18 still live. |
| Albums | ✅ Planning | Album Calendar + lineup v7, Merry Merry (Mahj Pit) quick-look page (21 picks), OMM counts corrected from live pages, Maven tile review page, no-swipe-books rule. |
| Social posted today | ⚠️ | Nothing auto-posted for the Juniper drop (priority 2). FB group plan/graphics built, nothing posted (her wording pending). |
| TNT scan (weekly) | ⏭ Not due (ran Tue), not merged | 15 mats for 5 sets in project docs 81c (+81b): Main merges into config/tnt-recs.json (Handoffs 'TNT scans not merged'), target Fri Nov 13. |
| HQ + Ready to Ship cleanup | ✅ Done | This run (HQ log). RTS: no new answers. |

## Never-ending projects
- **Find Your Mat-ch™ app** (artifact 6epA9HuEdT32zUp79Qv3kd; public **Version 1.18** (artifact Version 117, id 1794137165-e544; both FYM pages page-block @9d331637; Mat Gallery v8 r3 @78072ca0 + search @3afb680e; all live Nov 8 ~11:15am); **1.19 = racks-only (Miss Mahjong)** blocked by the jsDelivr 403; the rest of the staged bundle (Deco Lagoon m-list, link routes [172], catalog adds incl. non-partner whole lines, racks, walls, Cabana) ships as small releases per rule 0b: gate + independent QA before every publish (QA loads the WEBSITE copy as live: 0 broken images, gate [115]); artifact AND website copy AND README 0a pin in the same step; +0.1 version label (docs/FYM-VERSIONS.md); her feedback the same day with a gate check; when a publish/paste fails, MESSAGE HER right away. Artifact file budget: run builder/fym_artifact_fit.py and publish ONCE. Every nav/header change: screenshot live at 1280, 1440 and 390 with the phone menu OPEN. New partner catalog in FYM within 24h of its inbox line (gate [114]). Refresh config/fym-mats-snapshot.json after every publish.
- **Match inbox** (docs/MATCH-INBOX.md): any chat writes match/catalog misses there the same turn; Main (was Matches & Catalog) marks DONE when shipped.
- **Google / MAHJMATCH in AI answers (her #1)**: AI Overview + AI Mode per partner, code report (Mon/Wed/Fri), daily morning report, indexing (brand pages first), sitemap health, weekly verified dates + hub date, weekly codes post (FB GROUP only typed out; IG/FB Page = logos graphic + short caption), alarm on any lost citation.
- **Albums**: order (her Oct 28 3:31pm; Style of Your Life DROPPED Nov 7, Dillard's exclusive, MFM set TBD): Sunday Blues (her Nov 8 order: cuts the line) → Bam Bird Deco Mulberry + Indigo (Lagoon LIVE Nov 8) → Sunday Nature Walk, Plum Panda, Hummingbird → Sunday Nature Walk → Middle & Main Peach and Pine, Mac + Miller; Mahjong Row fall + OMM green set (Juniper, LIVE Nov 8) jumped the line; a known restock goes FIRST. Album Playbook doc (14oGH3ovycd2xMgrHbodJZ) is the source of truth; doc 86b (colour card FIRST), book_gate.py, PICKING-RULES.md, NEW-ALBUM-CHECKLIST.md (incl. the new-albums email).
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


## Log of this rewrite (Wed Nov 11 night)
- **Done today:** Google report (26/39) + scorecard; 15 indexing requests; TdT brand page links fixed; Mahjong by SI + Fait à Main (code coming soon) on the codes page; partner coverage check + daily owner task (trig_012DGkmgYqbH5ks6V9Dq9Ldz); FYM all-or-nothing gate [173]; Maven WooCommerce reader + tile review page; brand weights config; FB group intros plan + Google Doc + graphics; OMM VIP post draft; Album Calendar + lineup v7; Favorite Things doc; FYM App Roadmap doc; usage report + icon options; DESK drop check.
- **Found mid-way and given a home:** see Handoffs line 'Found Wed Nov 11'.
- **DESK: carried every open line (drop check 0).** Retired-chat owners read as Main. Lines added during the day (TikTok, weddings, Hanukkah, Nov 11 12:57pm notes) moved under Later / ideas, unchanged.

See CLAUDE.md.
