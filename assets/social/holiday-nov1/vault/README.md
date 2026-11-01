# Holiday Vault: reel tour + holiday albums carousel (Nov 1, 2026; agent vault-tour)

Drafts for Tiffany's OK. Nothing has been posted, scheduled or put in Planoly.
This follows the brief (docs/HOLIDAY-REELS-BRIEF-nov1.md) and the 12:22am, 12:24am and 12:28am updates: the app is shown making a match before any match card appears, it ends on "Shop now · use code MAHJMATCH", the carousel is about holiday ALBUMS, and it never says "you didn't know", "every" or "all".

## Files
- `holiday-vault-tour-reel.mp4`: the reel, 1080x1920, 24.75s, 30fps, silent.
- `holiday-vault-tour-reel-BEAT-CLICK-TEST.mp4`: the same reel with a generated click on every beat (a higher click on each bar downbeat). Use it to line up the song.
- `holiday-vault-tour-reel-cover.jpg` (2.2s, "The Holiday Vault is open" over the gift box) and `holiday-vault-tour-reel-contact.jpg` (a frame every 0.5s).
- `carousel/01-10-slide.jpg`: 10 feed slides at 1080x1350. `carousel/story/01-10-story.jpg`: the same slides as 1080x1920 story frames, one per slide. `holiday-vault-carousel-contact.jpg` is a contact sheet.
- Captions: `reel-caption-ig.txt`, `reel-caption-fb.txt`, `carousel-caption-ig.txt`, `carousel-caption-fb.txt`. All four pass content_lint.
- `build/`: the HTML sources and capture scripts. They read images from /dev/shm, so re-capture before re-rendering.

## Music (song first)
**Primary song: "Underneath the Tree" by Kelly Clarkson, 160 BPM.** CopperKnob lists 160 BPM and AcousticBrainz lists 80 (the half-time count of the same tempo).
- The theme fits: presents waiting underneath the tree = the holiday content hidden on the site.
- The cuts land on a 160 BPM grid: one beat every 0.375s and one bar every 1.5s. The reel is 66 beats long.
- Start point: start at the first chorus ("You're here where you should be…"). In Instagram, drag the song until a strong drum hit lands at 0:00 of the reel, then check against the click-test file. The exact chorus timestamp is approximate, so set it by ear.

Shortlist (all real, upbeat; she adds the song by hand):
1. Kelly Clarkson, "Underneath the Tree" (160): primary
2. Mariah Carey, "All I Want for Christmas Is You" (about 150; sfrbeats lists 76 half-time). Start at the full-band entry after the slow intro.
3. Ariana Grande, "Santa Tell Me" (96, from Wikipedia). It's slower, so the cuts would land on every other beat.
4. Brenda Lee, "Rockin' Around the Christmas Tree"
5. Wham!, "Last Christmas"

## Beat map (beat N = N × 0.375s)
| Beats | Time | What happens |
|---|---|---|
| 0-8 | 0-3.0s | Gift box. "Merry Mahjong." (b0) and "unwrap the holiday albums" (b2). "The Holiday" (b4), "Vault" (b5) and "is open." (b5.6) punch in. The lid flies off (b6) and the phone rises out of the box. |
| 8-13 | 3.0-4.9s | The real /christmas-mahjong-mats page at 390px. Scroll bursts land on b9-b12. A gift tag counts up to 40 Christmas & winter mats. |
| 13-20 | 4.9-7.5s | A storybook page flip (b13) to /holiday-mahjong-matches. A punch-zoom on its own stat boxes (b14.3) shows "400+ holiday matches". Scroll bursts go through the new holiday tile sets, and a tag counts up to 11. |
| 20-28 | 7.5-10.5s | A ribbon wipe into a full-screen photo dump, one real brand photo per beat: Dear Santa tiles, Candy Cane Lane, Nutcracker Ballet tiles, Clara's Dream Christmas, Rackin' Rudolph tiles on racks, Festive Plaid, Nivalee on racks, Holly Jolly tiles on racks. |
| 28-42 | 10.5-15.75s | **The real Find Your Mat-ch app, zoomed in.** Dear Santa tiles and the Candy Cane Lane mat fill the frame. ♥ is tapped (b29.75) and the mat card flies right with a ♥ stamp; the phone frame never moves. The suitor is tapped (b32.4). Racks: the mat is zoomed with +, B&B Brick Red gets ✕ (b33.4), Matcha gets ♥ (b34.5), Flamingo gets ♥ (b35.7). "Make it official ♥" (b37.7) produces the "It's a match!" Story 9:16 card, then scrolls to "Use code MAHJMATCH". These are real app screens captured on Nov 1 (Version 1.11). |
| 42-46 | 15.75-17.25s | "400+ holiday matches": 4 album match cards are dealt in on beats, each with tiles × mat brands named. |
| 46-50 | 17.25-18.75s | Album holiday sections cut on each beat (Nantucket, Jade, Malachite, Smith). A tag counts up to 34 albums with a holiday section. |
| 50-57 | 18.75-21.4s | Find Your Mat-ch, "Start with a mat": Holiday is tapped with a punch-zoom on the chip, then the holiday mat grid scrolls. A tag counts up to 156. |
| 57-66 | 21.4-24.75s | The end gift tag drops in: "The Holiday Vault is open. Holiday match albums + Find *Your* Mat-ch™. Tiles, mats & racks, together." Then **"Shop now · use code MAHJMATCH"**, "LINK IN BIO" and the logo. |

## Counts (real, with sources)
- **400+ holiday matches, 42 holiday mats, 49 tile sets, 17 brands**: the live header of mahjmatchmaker.com/holiday-mahjong-matches (fetched Nov 1). The repo has 430 holiday match card images in assets/cards/holiday-v4.
- **40 Christmas & winter mats**: /christmas-mahjong-mats lists 32 Christmas and 8 Winter & Hanukkah mats ("Shop the mat" ×40).
- **11 new holiday tile sets**: the "new holiday tile sets" grid on /holiday-mahjong-matches.
- **10 holiday tile sets, matched**: the sets in that grid that have a match section. Tinselle (Emerald Green) has no matches yet. Per-set counts from the page: Dear Santa 19, Rackin' Rudolph 22, Holly Jolly Red 13 + Green 3 + Pink 10 = 26, Tinselle Ruby 2, Nivalee 7, Nutcracker Ballet 12, December 1994 5, Après Ski Club 9.
- **34 albums with a holiday section**: the "Holiday matches for the tiles you already own" list on the same page (Nantucket through Sierra).
- **156 holiday mats to swipe**: Find Your Mat-ch v1.10 data (`const D` in site-app/fym-v110, pinned on the live page). There are 152 visible mats flagged `hol` plus 4 `wfh` mats. With "Start with a mat" and Holiday tapped, the live app shows 156 cards.

## Stock check (Nov 1 ~12:40am, Shopify `/products/<handle>.js` `available`)
These are in stock:
- Mats: AR Candy Cane Lane, Classic Very Merry Mahj and Evergreen & Tartan; Sunday Festive Plaid; Bespoke Holiday Love Red/Green; CMC Ski Club Red Sweater; Mahj Squad Blue Christmas and Clara's Dream; Splash Alpine Ski Lodge; Mahjong Register Very Merry Wreath; Hip Hip Hanukkah; Bam! Holly Jolly Christmas mat; OMM Winterberry and Clara.
- Tiles: Dear Santa, Rackin' Rudolph, Holly Jolly (all 3 colorways), Nivalee Glacier Blue, Nutcracker Ballet, Après Ski Club, OMM Smith/Gatsby/Moonlight, Miss Classic Jade.

These were left out:
- Sold out: Virora Hiverelle, Britt Mills Merrywood neoprene, Sunday December 1994 preorder, Mahj Squad Candy Cane Pink Wonderland, Miss Mahjong Classic Jade Numbered Flower.
- OMM Sugarplum mat: its product page returns 404.
- Maison Mahj The Chalet: a Maison mat never carries a discount promise.

The page recordings show the real site as it is, so sold-out items can appear in a scroll, but none is featured, named or zoomed.

## Brand-guide calls I made
- **Match cards are never panned or zoomed.** They enter whole and hold still. The punch-zooms are on the app, the stat boxes and the Holiday chip.
- **Real photos only.** Product photos come from each brand's own store. Screens are real headless captures of mahjmatchmaker.com at 390px.
- No Tigre de Tartán, Paige Spearin, Mahjong Studios mats or Yellow Mountain is featured. The FYM holiday grid scroll does flash past every holiday mat in the app for a split second, including a Paige Spearin x TdT tile. That is the real app; tell me if you want that scroll cropped.
- Find *Your* Mat-ch™ uses "Your" in Playfair Display italic inside the Caprasimo headlines.
- center_check reports 112 off-centre bands. These come from the plaid background, the snow and the deliberate side gift tags, not from off-centre headlines (the headlines, pills and end card are centred). I looked at every frame of the contact sheet.

## Collaborators to invite (and why they'd reshare)
- **Anders Ruff (@andersruffdesignco)**: Dear Santa leads both pieces, and the in-app match is Dear Santa + Candy Cane Lane (preorders are open now; mats ship Nov 17). They have already reshared our reel.
- **Mahj Squad (@mahj_squad)**: their Nutcracker Ballet gets an album slide, and Clara's Dream is in the photo dump.
- **Charleston Mahjong Club (@charlestonmahjongclub)**: Après Ski Club gets an album slide, and Ski Club Red Sweater is shown with both winter sets.
- **Virora Mahjong (@viroramahjongofficial)**: Nivalee gets an album slide.
- **Bam! Let's Mahjong (@bamletsmahjong)**: Holly Jolly in 3 colorways gets 26 matches on one slide.
- **Hip Hip Mahjong**: Rackin' Rudolph gets an album slide. There is **no verified handle**: the footer of hiphipmahjong.com has none, and config/social/ig-handles.json lists them as unverified. Add the handle by hand if you know it.
- Splash of Color and Mahjong Register also have no verified handle. Their names appear on the cards.

Why they'd share: each brand gets its own slide or beat showing how many ways its holiday set is styled, plus its mat used with other brands' tiles. They can't show that themselves.

## Carousel (10 slides, 4:5; one story frame per slide)
1. "Holiday albums are here", with 8 holiday album covers and "10 holiday tile sets, matched · 400+ holiday matches".
2. "How we make a match in Find Your Mat-ch": 3 real app screens (tiles + ♥ mat, racks with the mat zoomed, the match card). This shows where the cards come from before any card appears.
3-8. One album per slide: the album cover plus 3 of its match cards (in-stock mats only) and its match count.
   - Dear Santa 19 · Rackin' Rudolph 22 · Holly Jolly 26 · Nutcracker Ballet 12 · Nivalee 7 · Après Ski Club 9
   - Every one of these slides carries "Shop now · use code MAHJMATCH".
9. "34 albums now have a holiday section", with 12 album covers.
10. A CTA gift tag: Find *Your* Mat-ch™, "Shop now · use code MAHJMATCH", LINK IN BIO and the logo.

## Update Nov 1 ~2am (polish)
Opener is now "Merry Mahjong. / unwrap the holiday albums" (no secret framing). Gift-tag counters use ../COUNTS.md: 140+ holiday mats (Christmas page + FYM grid), 10+ holiday tile sets, 40+ holiday albums; the punch-zoom on the /holiday-mahjong-matches stat strip now spotlights only its "400+" box (the strip's other boxes still say 42 / 49 / 17, handed to Ops). URL pills replaced with "Christmas & winter mats" / "Holiday matches, by tile set". Carousel slides 1, 9, 10 (+ story frames) and all captions re-rendered with 10+ / 30+ / 140+. Paige Spearin x TdT check: the FYM holiday grid scroll stops at strip y 9,788 px; the first Tigre de Tartan tile (Ditsy Christmas Maraschino) sits at y 12,462 and Après Mahj at 16,459, so neither is ever on screen (OCR of every frame in the scroll confirmed; the "Corey Paige" mats shown are Bespoke Mahjong, not Paige Spearin). Known: OMM Sugarplum (gone from OMM) still shows in the real app grid capture, since v111 still lists it (MATCH-INBOX).
