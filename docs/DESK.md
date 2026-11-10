# The Desk
**Nov 10 12:20pm · FYM racks release: Main is building it (commit 'FYM 1.19 = racks-only release'); Matches & Catalog stopped its copy to avoid double work. Main: gate + QA + all 3 places today, then Matches & Catalog ships the Deco Lagoon matches (1.20) right after.**

**Main: brand watch Tue 9:58am ET: 8 NOW items ready (launch-actions.json), 6 group-post drafts for her yes in docs/social:** NEW since last run = CMC full-size Cabana Club tiles LIVE for email subscribers ($425, not public yet; cmc-cabana-club-2026-11-10.post.txt), Mahj Mood flash sale BOGO 1/2-off mats (mahj-mood-flash-sale-2026-11-10.post.txt), Virora Tinselle Ruby pre-order back (in virora-lilacee-yellow-2026-11-10.post.txt). Also drafted: Miss Mahjong racks 10am CT (miss-mahjong-scalloped-racks-2026-11-10.post.txt), Virora Lilacée Yellow 7pm CT, Mahj Pit Christmas + Confetti Wed (mahj-pit-christmas-tiles-2026-11-11.post.txt). Already Main's: TdT Domino Blonde 4pm CT (key fixed), OMM Juniper Wed 10am CT. Bring these to Tiffany; Miss Mahjong racks go live in ~1 hour.
Rewritten nightly by the end-of-day desk cleanup (9:23pm ET). The morning HQ cleanup (6:47am ET) reads it. Rules: CLAUDE.md ("THE DESK"), docs/CHATS.md (which chat owns what). During the day, when an agent stops, Chrome drops or a QA stalls, add the item here right away with its next step.

**Last rewrite:** Mon Nov 9, 2026, ~9:45pm ET (desk cleanup run, cloud, no computer linked). Covers the 62 commits of Nov 9 ET (84d6e138 … 70457a8c), docs/ANSWERS.md (Nov 9 lines 1240-1278), docs/OVERDUE.md, docs/MATCH-INBOX.md, Planoly (IG workspace 019fc27c…: 72 groups, export docs/social/planoly-exports/ig-2026-11-09-desk.json; Pinterest 019fc27b…: 83 pins scheduled Nov 10-30, 0 errors, export pin-2026-11-09-desk-scheduled.json), HQ needs (22 open) / hq/albums / hq/now / log, Ready to Ship (no new answers since Oct 24), list_triggers (disabled), config/release-calendar.json, content_lint (repo + Planoly IG export), gallery_sync_check (PASS v118), live_codes_check (PASS), curl checks (sitemap.xml, /mahjong-tile-matches, colour + brand pages, /links).

**Owners (three chats, Oct 22; she now talks to WHICHEVER chat, Nov 8 ~11pm, and that chat owns it):** Main (Opus) = social/Planoly, site pages, email, HQ/DESK, decisions, Google + SEO, money. Matches & Catalog (Opus) = Find Your Mat-ch, albums, gallery, catalog, search index. Ops (Sonnet) = the ONLY Chrome driver: Squarespace pastes, uploads, IG follows/checks.

**Repo note:** `partner-catalogs-sqsp` is huge. Tonight: `git fetch --depth=200 origin partner-catalogs-sqsp:refs/remotes/origin/partner-catalogs-sqsp` took ~6 min (run with a 500s timeout), then `git checkout -B partner-catalogs-sqsp origin/partner-catalogs-sqsp`. A plain fetch times out at 2 min.

**PARTNER SEND GATE (Oct 27, standing):** before scheduling ANY partner email or graphics drop, run `python3 scripts/partner_send_check.py`; it must exit 0.

**NEW TODAY (Nov 9, ANSWERS 1240-1278):** NO MORE REMINDER POSTS (every post auto-publishes; stories = one auto-post per frame; song reels via search_instagram_audio). REVIEW WEEK: this week's posts sit in Planoly Dec 7-13 (real date = Dec date minus 28 days) until she moves them back; before Dec 6 every one is moved back or unscheduled. Canva-template leftovers are OUT; templates are layout baselines only. Album content = eye-candy FULL-MAT grids (her top matches in album order, mats centred, title "Juniper" + "by Oh My Mahjong") and DYNAMIC selling reels (covers, photo-dump movement, FYM shown in use with a real screen recording). Push the 11 HOLIDAY ALBUMS now (people buy in November). Rackin' Rudolph uses HER Canva tile photo everywhere. Dear Santa = big push now (Anders Ruff collaborator, MAHJMATCH). No sell-out hype ("Set your alarms!"). Brand watch = launches/restocks/preorders/dates only, never giveaways. Group posts sell with product photos; drop minor items. Albums are always up before tiles drop. Never feature YOLO Journey to the West. Mahjong Co. stays in the codes list until truly closed. Album go-live = FB group post + email to the list, no checking by her. Claude does affiliate applications (emails scheduled ~7am, never at night). Revenue rule 4g: holidays are low days. Traffic changes are explained from Squarespace sources, never guessed. /links must feature Juniper.

**Standing (Nov 4):** A YES IS A YES · BLOCKED IS NOT DROPPED · REVENUE WATCH · NO 'ASK ONCE' · SOCIAL 13 (nothing disappears from Planoly) · partner launch → FB group post drafted the same day · payouts are CASH via PayPal (Bam Bird = bank transfer), only Maison Mahj + PLM Level 1 are store credit · ShopMy pickup DAILY 9:02am · Chrome: no saved tabs · IG evergreen codes post = profile-only.

## Tomorrow's top priorities (Tue Nov 10), in order
Standing order: RESTOCK FIRST (rule c), then Google #1 (Tiffany Oct 29 11:03pm), then the newest ANSWERS (Nov 9: holiday push + Dear Santa, Juniper drop Wed, no reminder posts, review week), then DESK 'Never-ending'. **Restock check (c): no album-set restock is dated Tue Nov 10** (Tue = TdT Domino Blonde mat 4pm CT, Virora Lilacée Yellow 5pm PT, Miss Mahjong acrylic racks 10am CT: none are album sets; covered in #2). Next album-set date: **OMM Juniper + Lotus Cove Wed Nov 11 10am CT** (album LIVE since Nov 8). Today's OMM Nantucket restock (album set, 52 matches) went live 12:35pm CT; its frames were built but the same-day window has passed (banked). The order is clear, so no "Set tomorrow's order" card.

1. **Google (Main; Ops for Chrome). First thing.** (a) Monday's Google & Revenue report ran PARTIAL twice (12:13pm: Chrome dropped after 28 of 38; 5:48pm catch-up: still offline; Search Console + dashboards unread) and the Mon code report is PARTIAL (Chrome kept disconnecting), so the 8:05pm scorecard was skipped. Tue 12:13pm run must finish all 38 + Search Console; if docs/reports/google-revenue/2026-11-10.md is missing or PARTIAL at 12:45pm, first line of every chat + fire_trigger trig_01LZjGfVneN3vKwweVXwbzub. (b) **4 brands LOST MAHJMATCH in the AI answer** since Nov 8 (My Fair, Peace Love, Mini Mahjer, Britt Mills) and OMM is still not named (page ~#15): indexing re-requests for those 4 brand pages + OMM first in Tuesday's quota (only 4 of 37 changed pages went in Mon). (c) **Deco (Lagoon) has no hq/indexing row**: add it + request indexing (Juniper row exists; both pages ARE in sitemap.xml now). (d) **Catch-up task trig_019StaM8LkmrxGKtK7xhXang is OFF** (suspension device_absent, since Nov 10 00:29 UTC): it is on the Quick calls card (default off), so leave it unless she says keep. (e) Chrome backlog that is Google work (Ops, first Chrome run): Mah Jongg Maven brand page + hub (built Nov 9, brand-pages/mah-jongg-maven.html), /links Juniper card above Deco (site/livepatch/links-nov09/README.md, OVERDUE), Black Friday deals page (her yes Nov 8; live before PLM BF Mon Nov 16), Charleston + TdT link swaps (OVERDUE). (f) **Mahjong by SI** approved as an affiliate Nov 9 (invite 9:27am): onboarding (code-truth, brand page, hub logo, FYM, IG follow, newsletter), owner Main.
2. **Social (Main), rule d: 0 IG posts SCHEDULED Nov 10-16** (by her own call: the week sits in Planoly's review week Dec 7-13). Default kit = album of the week **Juniper** (Wed 10am CT drop): the Wed Juniper It's a mat-ch + story are already in the review week (Dec 9 slot) and need only her "move it back". Waiting her yes in chat since Nov 9 11:23am: Holly Jolly Red grid + **Dear Santa reel v3** (live FYM recording). OVERDUE: Dear Santa push (reel + feed + every-frame stories, Anders Ruff collaborator) and the 11 holiday album reels rebuild (dynamic style). Tue same-day restock frames for her review: Virora Lilacée (assets/social/restock-lilacee-nov10/out/), TdT Domino Blonde (image-only reshare). FB group week: Tue Juniper poll needs her yes by Tue morning (HQ Today). Roll-forward / story-caption fixes refused a 6th night (update_post denied): attended Main. The Friday social prep task drafts storyboards for her yes.
3. **FYM 1.19 (Matches & Catalog).** Build with everything staged (Deco Lagoon m-list + album link, link routes BEFORE the gate, catalog adds incl. non-partner whole lines, racks + walls) PLUS Nov 9 adds: **LBB Artist Collective 174 mats** (17 holiday; config/lbb-artist-collective-nov09.json), Let's Mahj On Let's Golf! ×2 tile sets, Soirée Holiday Chintz, Wren Gingham and Wine, LBB Tropical Travels Simple Middle, **Mahjong Register 26 renamed mat URLs** (relink), stale "Stock checked Nov 1" label (refresh stock), Caroline in Navy image + gate, shop-click tracking bug, Mahjong Register auto-apply links (OVERDUE). Gate + independent QA + all three places the same day. Juniper "now available" wording on the album + FYM after Wed 10am CT.
4. **Match inbox (rule e) + Chrome backlog (Ops).** MATCH-INBOX: the 15 Oct 27-Nov 6 lines named on the Nov 8 desk are still unmarked (a keyword scan finds ~90 dated lines with no DONE mark, most likely shipped but never marked): Matches & Catalog marks each DONE with its build number or folds it into 1.19. Ops Chrome run (in this order): Maven page + hub, /links Juniper, Black Friday page, Charleston album links → ShopMy, TdT brand page auto-apply links, follow + favorite @mahjpit.co and @mahjonggmaven, Let's Golf! TNT search, Dropbox flat renders (incl. LBB Artist Collective).
5. **Albums (Matches & Catalog), her Nov 8 order:** Sunday Blues next (tile photo approved; TNT gate redo OVERDUE for sunday-blues / nature-walk / plum-panda / hummingbird before any cards render; launch kit before go-live; held for the ~Thanksgiving restock), then Deco Mulberry + Indigo (re-pull with the Nov 8 leads), then Nature Walk, Plum Panda, Hummingbird. Holiday leftovers: Rackin' Rudolph cards → HER Canva tile photo (36 cards, OVERDUE), 5 blurry cards with no better photo, holiday completeness audit on year-round album pages, yes-vs-live check script.

- **Tiffany's approved matches** (config/tiffany-matches.json): social picks come from this list FIRST.

## Handoffs (do first)
- **Nov 10 ~12:15pm ET · FYM VERSION NUMBERS (Matches & Catalog read this before building):** the 5 Miss Mahjong racks ship TODAY as their own racks-only release **Version 1.19 = site-app/fym-v119** on top of live 1.18 (OVERDUE line, Tiffany 12:02pm; builder/fym_fix_nov10/racks119_missmahjong.py + release119.py, in progress by a release agent). The staged bundle formerly called '1.19' (Deco Lagoon, link routes, LBB Artist Collective, racks119.py ...) becomes **Version 1.20 = site-app/fym-v120**, built ON TOP of 1.19 (keep the 5 Miss Mahjong racks; the script is idempotent). Do not create site-app/fym-v119.
- **OPS (Chrome): Mah Jongg Maven publish** (built Nov 9 3:20pm, Chrome offline): duplicate the Mahj Pit brand page → /mah-jongg-maven-discount-code, SEO title 'Mah Jongg Maven Discount Code: MAHJMATCH | Mahj Matchmaker', paste brand-pages/mah-jongg-maven.html (doc 59 §3); hub patch brand-pages/hub-mah-jongg-maven-2026-11-09.json + logo graphic assets/hub/partner-brands-2026-11-09.jpg; follow + favorite @mahjonggmaven; newsletter signup. The onboarding task trig_01C7xPrJVSgHBv1ysBekgJyh does it on its next run with Chrome up.
- **OPS (Chrome): /links Juniper card** above Deco (her 4:27pm ask; site/livepatch/links-nov09/README.md). Live /links has Juniper only in the album strip, after Deco (Lagoon).
- **OPS (Chrome): follow + favorite @mahjpit.co**, log in docs/IG-FAVORITES.md; read Sunday Mahjong's IG for the brand watch.
- **Main: Mahjong by SI onboarding** (approved Nov 9; HQ log l202611092027).
- **Main: Holly Jolly Red grid + Dear Santa reel v3**: shown in chat Nov 9, waiting her yes; on yes, schedule as auto-publish (song via search_instagram_audio) with FB Page target + every-frame stories.
- **Main: Tue restocks** (same day or never): Virora Lilacée Yellow 5pm PT (frames assets/social/restock-lilacee-nov10/out/lil-A/B/C, HQ needs/launch-virora-lilacee-nov10); TdT Domino Blonde 4pm CT (image-only reshare, needs/launch-tdt-domino-blonde); Miss Mahjong acrylic racks 10am CT (live; staged for FYM 1.19, see Nov 10 line). Miss Mahjong Día de Muertos mats back since Nov 9 5:36pm CT (needs/launch-miss-muertos-mats, This week).
- **Main: Deco (Lagoon) + Juniper launch kits**: Juniper announced in the Mon codes post + grid posted 12:30pm Nov 9; Juniper email to the list Wed with the tile launch; Lagoon announced in the codes post; 'new albums are live' email + album requesters (docs/NEW-ALBUM-CHECKLIST.md 3-4) still to send (Squarespace draft; her final read).
- Nov 10 · Matches & Catalog: FYM next release (1.19): 5 Miss Mahjong acrylic racks staged (config/fym-rack-adds-nov10-missmahjong.json + builder/fym_fix_nov10/racks119_missmahjong.py, photos assets/racks/v119/missm-*.jpg; run `python3 builder/fym_fix_nov10/racks119_missmahjong.py <b119>` AFTER racks119.py, then fym_rack_images.py must say 'all rack images reviewed ok'). Bombshell Pink, Butter Yellow, Pistachio, Peony, Chartreuse Scalloped: $150 set of 4, 20", in stock. Brand photos only crop the racks at the frame edge, so no clean single-rack cut-out: brand photo on white, c:false (rule 6b fallback), approved on white + navy.
- Nov 08 · Matches & Catalog: FYM 1.19 Deco (Lagoon): apply config/fym-catalog-adds-nov08-lagoon.json + Dreamframer add, THEN `python3 builder/fym_fix_nov08/deco_lagoon_m119.py <b119>`; `apply_link_routes.py <build>` BEFORE the gate. Decide if /teal-mahjong-tile-matches should list Lagoon (colour card says teal; today it's only on Blue).
- Nov 08 · Matches & Catalog: Deco Mulberry + Indigo leads in config/tnt-recs.json (redo.leads). New brands waiting on her OK: Mahjong Along With Me, Lotus Mahjong (Quick calls).
- Nov 08 · Mahj & Moon fixer: when the 7 Etsy ShopMy links land, delete 'pending_fix' on the Mahj & Moon row of config/link-routes.json.
- **Matches & Catalog: It's a Mahjong Life (4 mats) + non-partner whole lines** (Birdsong, Isabel Hart, Lucky Daughters, Mahjong Moxie, Mary Benson, Silk Mahjong) + Maison Mahj full partner line: in 1.19.
- **OPS: copy flat renders to Dropbox /Mahj Matchmaker Albums/New releases/<brand>/** (Fait à Main Texas Mon Amour Cream, LBB Tidal Glass / Seasons Mid-Century / Nutcracker / Tropical Travels, Bam! teaser, Soirée Holiday Chintz, Wren Gingham and Wine, LBB Artist Collective 174 mats, Let's Golf! ×2; assets/launches/<dir>/).
- **OPS: search Tiles & Tablescapes for Let's Golf!** (Celadon Mist + Magnolia Blush): TNT rec + colour card before any swipe book (hq/albums needs-tnt).
- **OPS: search Tiles & Tablescapes for Yellow Mountain Imports Aristo-Cat** (launch watch Nov 10 8:57am; listed Nov 9 as a $0 placeholder, no photos yet): once YMI adds photos, save them to assets/launches/ymimports-us-af036-a/ and copy to Dropbox /Mahj Matchmaker Albums/New releases/Yellow Mountain Imports/; then TNT rec + colour card before any swipe book (hq/albums needs-colourcard). Never feature YMI on social.
- **OPS: Payout Tracker September check** for 'Close October' (her 2-dashboard rule: Quick calls, default do it once by hand this week).
- **Main: blog posts name album tile sets but don't link them** (list in git show 09006524:docs/DESK.md). Slipped Nov 9 → Wed Nov 11.
- **Main: revenue-alert cards**: per-brand alert docs sit archived; fold into one Money summary in the report.
- **Main: prompt fixes still not applied**: sales-check prompt (all secomapp/goaffpro/backinstock mails, refunds on the refund date); "close leftover Claude tab groups" in every Chrome task; mat-edit-alert step in launch watch trig_01S2VsjwznnHev1uUbYmEwJq; launch/partner watch "wholesale customers only" + same-day FB group draft.
- **Main: hq/launches** is ~245 KB of the 256 KiB cap: archive pre-Oct 25 items before the next add.
- **Main: config/pinterest/queue.json** vs Planoly: resync (Planoly healthy, 83 scheduled through Nov 30).
- **OPS (standing): HQ ShopMy tab inbox** at the start of every Ops reply.
- **Partner feedback watch** trig_01RKw9eUwTYPo39gbYHb65gh: last planned run Tue Nov 10 (disable after unless feedback is coming in; 0 real partner notes so far).

## In progress
| Item | Owner | Next step | Target |
|---|---|---|---|
| Google & Revenue report: full run (Mon PARTIAL ×2) | Main | 12:13pm run; fire by hand at 12:45pm if missing/PARTIAL. | Tue Nov 10 |
| Google code report (Mon PARTIAL) + scorecard | Main | Wed 1:52pm run; scorecard after it. | Wed Nov 11 |
| 4 brands lost MAHJMATCH + OMM not named | Main / Ops | Indexing re-requests (My Fair, PLM, Mini Mahjer, Britt Mills, OMM) first in quota. | Tue Nov 10 |
| Deco Lagoon hq/indexing row + request | Main / Ops | Priority 1c. | Tue Nov 10 |
| Mah Jongg Maven onboarding (OVERDUE) | Ops (Chrome) | Publish page + hub + IG + newsletter. | Tue Nov 10 |
| Mahjong by SI onboarding | Main (+ Ops) | Code-truth, brand page, hub, FYM, IG, newsletter. | Wed Nov 11 |
| /links Juniper card (OVERDUE) | Ops (Chrome) | Paste site/livepatch/links-nov09. | Tue Nov 10 |
| Black Friday deals page (her yes Nov 8, OVERDUE) | Ops (Chrome) | Refresh deals, paste, index, link. | Thu Nov 12 (before Nov 16) |
| Juniper launch day (Wed 10am CT) | Main (social), Matches & Catalog (wording) | Move the Wed post back from review week on her OK; email to list; 'now available' copy after 10am. | Wed Nov 11 |
| Dear Santa push + holiday album reels (OVERDUE) | Main | Dynamic style; her yes on v3; schedule auto-publish. | Tue Nov 10 |
| Planoly roll-forward + story-caption fixes | Main (attended) | update_post refused unattended 6 nights. | Tue Nov 10 |
| FYM 1.19 | Matches & Catalog | Priority 3; gate + QA + three places. | Wed Nov 11 |
| Match inbox: old unmarked lines | Matches & Catalog | Priority 4. | Wed Nov 11 |
| Sunday Blues album (TNT redo first) | Matches & Catalog | Album Playbook; held for the ~Thanksgiving restock. | Fri Nov 20 |
| Deco Mulberry + Indigo | Matches & Catalog | Re-pull + discovery, fresh review pages. | Fri Nov 13 |
| Rackin' Rudolph cards → her Canva tile photo (OVERDUE) | Matches & Catalog | Lock crop, re-render 36 cards, paste. | Wed Nov 11 |
| Holiday completeness audit (year-round album pages) + yes-vs-live check | Matches & Catalog / Main | OVERDUE lines. | Wed Nov 11 |
| Album wiring gaps (C1: 7 live albums not wired to FYM) | Matches & Catalog | Gap audit C1. | Thu Nov 12 |
| FB group week Nov 9-15 | Tiffany yes → Main (Chrome) | Tue poll needs the yes by Tue morning. | Tue Nov 10 |
| New arrivals carousel (Thu 11/12) | Tiffany yes → Main | Draft 01a1c214-d8c2 in Planoly; schedule on yes. | Thu Nov 12 |
| ManyChat comment-for-links draft + trial reminder | Main (Chrome) | OVERDUE lines (low priority). | Thu Nov 12 |
| Work With v3 + Brands form | Ops | Default: goes up HIDDEN next Chrome trip unless she says wait. | Next Chrome trip |
| Holiday new-albums email | Main | Squarespace draft; names Juniper + Deco Lagoon; her final read. | Wed Nov 11 |
| Discount links not converted (Britt Mills, Register, YMI, RMS, Hip Hip, Wren/Soirée/Amanda Toppe) | Main | Fold into link-routes. | Thu Nov 12 |
| PEACE LOVE → Level 2 ($5K/month → cash) | Main | Plan + PLM MTD in the report (not readable Mon). | Tue Nov 10 |
| Affiliate applications: Haus of Charleston (emailed Nov 9 7am), Lemondrop, The Mahjong House, Bloomjong, Sweet Jojo | Partner watch | Watch mahjmatchmaker@; onboard on approval. | On approval |
| UpPromote accounts → mahjmatchmaker@ | Tiffany / Main | Screenshots before each switch. | Fri Nov 13 |

- REVIEW WEEK Dec 7-13 in Planoly (Tiffany Nov 9 1:09am): 3 feed + 27 single-frame stories + Juniper Wed parked 28 days out. Before Dec 6 EVERY one must be moved back (approved) or unscheduled, or it auto-posts. Owner: Main + nightly desk cleanup.

## Blocked, approved (raise at the top of every attended reply until done)
- **Planoly roll-forward + story-caption fixes**: the unattended desk run is refused for update_post (6th night, Nov 9). Attended Main: past-dated drafts (Mon 11/9 FYM how-to 01a1b20c-7bd9 + story 01a1b20d-690f are Papaya = held for rebuild per her 1:15am call; old Nov 4-8 multi-frame story drafts 01a1a2b6-7c1e/-73c0/-7707/-7a67 are superseded by the single-frame review-week stories: ask her once whether "superseded" = remove).
- **Chrome-only pastes approved by her** (Maven, /links Juniper, Black Friday page, Charleston + TdT link swaps): Chrome/Mac offline most of Nov 9.
- **Partner newsletters, 9 stores block automated signup (Shopify hCaptcha)**: Amahj, Bam! Let's Mahjong, Mahj Mood, Let's Be Besties, Mini Mahjer, My Fair, The Mahjong Press, Tigre de Tartán, Splash of Color. Her ~10s each on her phone; then mark docs/PARTNER-NEWSLETTERS.md.
- **Bing Webmaster Tools** (her yes Nov 6): one tap from her on Google's account chooser (OVERDUE line has the steps).
- **The Mahjong House affiliate**: her click on Confirm in their UpPromote verify email.

## Waiting on Tiffany (only things she can answer now)
**On HQ Today, in this order (5):**
1. **Google: laptop on + Claude app open by 12:13pm Tue** so the report and checks can finish (Mon ran partial twice). 4 brands dropped our code in Google's AI answer; Claude re-requests their pages.
2. **Facebook group week: one yes** (Tue Juniper poll, Thu table thread, Sat help-me-match).
3. **Virora Lilacée Yellow restock Tue 7pm CT: story frames yes?**
4. **Tigre de Tartán Domino Blonde Tue 4pm CT: reshare yes?**
5. **Bam Bird commission: one screenshot** (its UpPromote dashboard redirects to Mac+Miller).

**On HQ This week:** Quick calls from Sunday (defaults in place); this week's posts in Planoly's review week; new arrivals carousel (Thu); Miss Mahjong Día de Muertos mats (reshare); Let's Golf! tiles; Brand Watch tab; Holy Mahj full image; 1 hidden FYM photo (Grace Peacock); ShopMy 6 quick calls + 2 stray links; Work With v3 (default: goes up hidden); 44 new mats (green).

**Quick calls from Sunday (one HQ card, each with a default):** Bam! Let's Mahjong Printfresh vs code (default keep code) · Mahj & Vine + Miss Mahjong own-program % (default keep code links) · old catch-up task + newsletter task (default off; catch-up is OFF now, device_absent) · Mahjong Along With Me + Lotus Mahjong for albums (default outreach list only) · GoAffPro mailing address + Country (default: she adds it) · IG profile codes post Mahjong Register line (default: leave until she's in the app) · Payout Tracker September check (default: once by hand this week).

**Asked in chat, not yet answered (the owning chat RE-ASKS at the top of every reply, with its default):**
- Main: Holly Jolly Red grid + Dear Santa reel v3 (Nov 9 11:23am; default: schedule both once she says yes; nothing posts without it); remove the old launch-reel draft + dropped Rudolph/Polo/Rattan drafts (default yes, archive record); 84 locked FYM colour changes (default apply); hide /bird-and-bamboo-discount-code-2 (default hide); Malachite how-to reel v2 OK + day; pinned reel v3 A or B.
- Matches & Catalog: Seabreeze × LBB Aloha card into FYM m-lists? (default no, social list only); Lagoon + Mulberry splits vs new pile photos; Bam Bird Classic Tortoise match pick; Sunday Rattan = Blue Rattan?; Fruit Stand rack-edge (default a); brand-lock pricing (undecided, don't push).

## Banked (finished, held on purpose)
- **OMM Nantucket restock frames (Nov 9)**: assets/social/restock-nantucket-nov09/out/nan-A/B/C (live FYM screens); same-day window passed, HQ card archived (rule 9). Reuse at the next Nantucket restock/reshare.
- **Holiday album grids + 10s teaser reels (Nov 9 1:31am)**: assets/social/holiday-album-grids (11 albums): the base for the dynamic rebuild (OVERDUE line); not for use as-is (her 1:37am: must be dynamic + sell).
- **Juniper eye-candy grid**: full-mat version POSTED Nov 9 12:30pm (IG + FB Page + story); close-up version rejected.
- **Style of Your Life (My Fair Mahjong) album**: round 1 built Nov 7 (22 cards, site/livepatch/mfm-style-of-your-life-album-nov07); SKIPPED for now (her Nov 8 10:11am 'Skip My Fair Mahjong album for now'; set dropped Nov 7, Dillard's exclusive).
- **Deco review pages Nov 8 10:45am (Mulberry 8V74MMkepN9TnVCF5cRNAw, Indigo 9VjoeB1ejRB3wVvnMaKMqH)**: OUTDATED by the Nov 8 TNT/Silk redo; replaced in place when the re-pull is done. Don't send these links.
- **Petalée (Virora)**: 61 cards, RTS `l-final-petalee`, vault (her Oct 28). Before publishing: colour card, 10% band sweep on the Amanda Toppe/Girly cards, cleaner Petalwing/Coralia photos. Table-view walls now staged (1.18).
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
- **Clean up 52 legacy caption lint warnings** (still 52 Nov 9) (config/social/content_lint_baseline.json; mostly missing #MahjMatch, '(affiliate)', 2 TdT captions) (rules audit E9, Oct 30). Also 78 legacy FAILs (length 42, naming 36) in banked Season 2 captions: same kinds as yesterday, nothing new (Nov 9 recheck: 78 FAIL = length 42 + naming 36, 52 WARN; nothing new). Planoly IG lint 19 FAIL, same as Nov 7-8 (story captions 14, codes post length = her exception, New this week FB 361, Dear Santa IG 380, banked Retro Rattan).
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


## Daily operations (Mon Nov 9)
| Operation | Done today? | Notes |
|---|---|---|
| Affiliate tracking (Money tab) | ✅ Done | Sun Nov 8 closed: 18 orders / $339.52 (MTD $2,525.10). Mon: 1 sale (Bam Bird 2:43pm) by 3:17pm vs 4-6 expected (site-drop alert; dashboards also show none, so it's real; her mom's surgery day, not a holiday). Bam Bird amount needs her screenshot (dashboard redirects to Mac+Miller). New affiliate approved: Mahjong by SI. |
| Google & Revenue report | ⚠️ PARTIAL ×2 | 12:13pm: Chrome dropped after 28 of 38 (23 of 28 name MAHJMATCH; lost My Fair, PLM, Mini Mahjer, Britt Mills; OMM not named). 5:48pm catch-up: still offline. SC + dashboards unread. Priority 1a. |
| Google code report (Mon) | ⚠️ PARTIAL | Chrome kept disconnecting (log 9:15pm); 8:05pm scorecard skipped. Next Wed 1:52pm. |
| Verified dates (weekly, Mondays) | ✅ Done | 36 of 36 brand pages + hub, live-checked 9:06am; live_codes_check PASS tonight. |
| Codes post (Mondays) | ✅ Done | FB group 11:16am, 18 photos (Juniper first, no YOLO) + codes first comment; Juniper + Deco Lagoon announced. |
| Pinterest queue health | ✅ OK | 83 pins scheduled Nov 10-30 (3-4/day), 0 errors. |
| Indexing | ⚠️ Partial | 4 changed brand pages requested 5:25pm (quota). Juniper + Lagoon now IN sitemap.xml; Mahjong Row 302 pages OUT (OVERDUE line closed). Lagoon has no hq/indexing row. Priority 1b/1c. |
| Planoly next-7-days (IG + FB Page) | ❌ 0 scheduled Nov 10-16 | By her call (review week Dec 7-13). Juniper grid + story auto-posted 12:30pm Mon. Every live IG draft/review-week group has the FB Page target (IG-only = profile-only codes post + banked/dropped reminders). Planoly lint 19 FAIL, all legacy (same as Nov 7-8). Roll-forward refused (6th night). |
| New albums (last 7 days) (f) | ⚠️ 2 misses | **Juniper**: /mahjong-tile-matches ✅, Green ✅, OMM page ✅, sitemap ✅, Pinterest ✅, hq/indexing ✅; ❌ /links shows it in the strip AFTER Deco (featured card paste OVERDUE). **Deco (Lagoon)**: index ✅, Blue ✅, Bam Bird page ✅, /links ✅, sitemap ✅, Pinterest ✅; ❌ no hq/indexing row; ? Teal page (decision in 1.19 handoff). **December 1994** (31 holiday cards live on /holiday-mahjong-matches Nov 9 2:05am, redo kit 4:10am): page 200 ✅. |
| Repo caption lint (g) | ⚠️ Legacy only | 78 FAIL (length 42, naming 36), 52 legacy WARN. Same kinds as yesterday, nothing new. |
| Live codes check | ✅ PASS | 39 brand pages + hub. |
| Gallery sync check | ✅ PASS | App v118, gallery v118. |
| Coverage + card sharpness | ✅ Morning run | Coverage 10 OK / 19 GAP; card sharpness 41 → 6 FAIL after the 35 album-page swaps (6 have no better photo; OVERDUE). |
| Restock first (c) | ✅ Checked | OMM Nantucket (album set) restocked 12:35pm CT: frames built, window passed (banked). Nothing album-set dated Tue. Juniper drop Wed. |
| Match inbox (e) | ⚠️ Old lines unmarked | Priority 4. |
| Launch + partner watch | ✅ Done | Partner watch 9:30am, 1:30pm, 6:59pm; launch watch 8:57am + 5:57pm (177 new incl. LBB Artist Collective 174, Let's Golf! ×2; 176 handed to FYM). ShopMy check PASS. Release calendar 9 changes. |
| FYM + partner feedback | ✅ 0 new | Watch ends after Tue's run. |
| FYM releases | ⏭ None | 1.18 live; 1.19 staging. |
| Albums live today | ✅ Holiday fixes | December 1994 31 cards live; 85 holiday + 90 + 35 album-page cards re-rendered sharp; 6 missing holiday yeses added. |
| Scheduled tasks | ⚠️ 1 off | Catch-up retry task OFF (device_absent, Nov 10 00:29 UTC); on Quick calls (default off). Older Oct tasks off on purpose. |
| Social posted today | ✅ 2 | FB group codes post 11:16am; Juniper grid + story IG + FB Page 12:30pm. |
| HQ + Ready to Ship cleanup | ✅ Done | Morning run + this run (see HQ log). RTS: no new answers. |

## Never-ending projects
- **Find Your Mat-ch™ app** (artifact 6epA9HuEdT32zUp79Qv3kd; public **Version 1.18** (artifact Version 117, id 1794137165-e544; both FYM pages page-block @9d331637; Mat Gallery v8 r3 @78072ca0 + search @3afb680e; all live Nov 8 ~11:15am); **1.19** staging (Deco Lagoon m-list, link routes [172], catalog adds incl. non-partner whole lines, racks, walls): gate + independent QA before every publish (QA loads the WEBSITE copy as live: 0 broken images, gate [115]); artifact AND website copy AND README 0a pin in the same step; +0.1 version label (docs/FYM-VERSIONS.md); her feedback the same day with a gate check; when a publish/paste fails, MESSAGE HER right away. Artifact file budget: run builder/fym_artifact_fit.py and publish ONCE. Every nav/header change: screenshot live at 1280, 1440 and 390 with the phone menu OPEN. New partner catalog in FYM within 24h of its inbox line (gate [114]). Refresh config/fym-mats-snapshot.json after every publish.
- **Match inbox** (docs/MATCH-INBOX.md): any chat writes match/catalog misses there the same turn; Matches & Catalog marks DONE when shipped.
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

## Log of this rewrite (Mon Nov 9 night)
- **Done today:** Monday codes post live in the FB group (Juniper + Deco Lagoon announced); Juniper full-mat grid + story auto-posted (IG + FB Page); December 1994 31 holiday cards live; holiday page + 22 album pages re-rendered sharp (card gates tightened, card_sharpness wired into the front door); verified dates 36/36 + hub; sitemap now carries Juniper + Lagoon and drops the 2 Mahjong Row pages; Haus of Charleston affiliate email sent 7am; Mah Jongg Maven page/hub/logo built; review week set up in Planoly; single-frame auto-post stories; album grid + teaser reel builders; Dear Santa reel v2 → v3 with a live FYM recording; launch watch caught LBB Artist Collective (174) + Let's Golf!; Mahjong by SI approved.
- **Found mid-way and given a home:** Google report PARTIAL twice + code report PARTIAL (Chrome dropped) → priority 1a; 4 brands lost MAHJMATCH → priority 1b; Lagoon indexing row missing → 1c; catch-up task suspended → 1d (Quick calls default off); Maven + /links Juniper + Black Friday + link swaps blocked on Chrome → Blocked + Ops handoffs; Holly Jolly + Dear Santa v3 waiting her yes → Main re-asks; Dear Santa push + holiday reels rebuild → priority 2 (OVERDUE); Planoly roll-forward refused 6th night → Blocked; Mahjong by SI → priority 1f; LBB Artist Collective + Mahjong Register relink + stale stock label → 1.19; Nantucket frames → Banked.
- **HQ:** archived codes post (posted), report-missed (ran, partial; tomorrow's alarm comes from front_door), Nantucket + mat-restock cards (day passed, rule 9), Monday site-drop alert (Monday closed; investigation in Tue report). Today = Google, FB group week, Lilacée, Domino Blonde, Bam Bird screenshot. December 1994 → Live on the Albums tab.

See CLAUDE.md.
