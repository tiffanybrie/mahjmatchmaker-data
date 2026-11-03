# Holiday intro hero reel + carousel ("We made a holiday list"), Mon Nov 2 2026

## v2.1 (Nov 3, 10:35am ET): CURRENT, per Tiffany Nov 3 10:20am: removed the 'Our holiday favorite.' Color Me Merry hero (it's an overview; the hook grid now holds 0-4.4s with a slow push-in, Color Me Merry stays in the grid + the app heart, no longer mid-quilt) and the racks are now a painted RED rack (Bird & Bamboo Red, #942934, picked by sight against Festive Plaid's red) + Walnut (Bam Bird Boutique); Persimmon read orange. Picks toggle is off for the rack step because Red isn't one of her saved picks. Festive Plaid Premium (Sunday) is 'Coming soon' on Sunday's site (preorder, not buyable yet) - caption says (coming soon). Same files below, re-rendered.

## v2 (Nov 2, ~11am ET): superseded by v2.1. The v1 reel files below (`holiday-intro-reel*.mp4/jpg`) are SUPERSEDED (kept for reference).
Built from her Nov 1 6:09pm + Nov 2 9:23am notes (docs/ANSWERS.md). She posts it today and adds the song in Edits.
| What | File |
|---|---|
| Reel v2, silent, 1080x1920, 30.0s, 30fps | `holiday-intro-reel-v2.mp4` |
| Beat test (click on every 150 BPM beat, loud click = bar downbeat) | `holiday-intro-reel-v2-beat-test.mp4` |
| Cover (hook grid + "It's holiday time.") | `holiday-intro-reel-v2-cover.jpg` |
| Contact sheet, every 0.5s | `holiday-intro-reel-v2-contact-sheet.jpg` |
| Captions (lint PASS) | `captions/reel-v2-ig-caption.txt`, `captions/reel-v2-fb-caption.txt` |
| Builders | `build/v2_stock.py` → `build/v2_capture.py all` → `build/v2_hd.py` → `build/v2_reel.py frames` → `build/v2_finish.py` (inputs in /dev/shm/introv2; app = live site copy fym-v113 @3c0b8ceb via `build/v2_lib.py`) |

**What changed vs v1**
1. Pacing: only the app tutorial slows down (swipe flights ~1.5x slower, ~0.8-1.2s holds on Holiday tapped, each card, favorites row, mat zoom, match card). Everything else stays quick and varied (12-mat pop-in grid, 1.2s quilt), cuts on the 0.4s beat grid.
2. Text: ONE centred cream plate at a time, 2-5 words, Caprasimo 78px navy, at y 270 (clear of the top 250px and the app's own text), held 1.2-2.4s: "It's holiday time." / "Our holiday favorite." / "Pick tiles. Tap Holiday." / "Swipe holiday mats." / "Your favorites, saved." / "Zoom in on your mat." / "Swipe racks to match." / "See it together. Shop it."
3. Spotlight: on every app moment the screen is dimmed ~58% with a soft-edged cut-out on what matters (Holiday chip, tiles + mat card, favorites row, zoomed mat, zoomed mat + rack card). The phone never moves during a swipe.
4. Margins: mat grids are designed for 9:16 (hook 3x4 grid, 80px sides; quilt 4x5 grid, 90px sides, centred vertically; counter thumbnails in a 3-up row). No edge-to-edge bursts.
5. Color Me Merry (Soirée All Day, @soireeallday.co) is the hero: centre of the hook grid, flies up to a full-size "Our holiday favorite." moment, is hearted in the app (a favorites-row pick) and sits mid-quilt. Stock: both sizes available (Squarespace `?format=json`, unlimited stock, Nov 2 ~10am).
6. Counters: digits are centred as a group; the "+" hangs outside so it never pushes the number off-centre. 140+ holiday mats · 14 holiday tile sets · 40+ holiday albums (COUNTS.md + ANSWERS Nov 1 6:00pm).
7. No dating language (no "suitors", no "It's a match!" pill). End card: Find *Your* Mat-ch™ ("Your" Playfair italic) · "Holiday tiles, mats & racks across brands, together." · Shop now · use code MAHJMATCH · Link in bio. No URL.
8. App footage re-recorded from the live site copy (v113): Dear Santa → tap Holiday (Tiffany's picks on) → ✕ The Polo Club (Luxe Mahjong) → ♥ Color Me Merry → ♥ Festive Plaid Premium (Sunday) → favorites row → racks step: + + + zoom on Festive Plaid → ♥ Persimmon, ✕ Basil (Bird & Bamboo), ♥ Walnut (Bam Bird Boutique) → the app's own Story 9:16 match card. The deck order was queued in the capture script (`matDeck0` wrapper); Candy Cane Lane (Anders Ruff) is the card under Festive Plaid.

**Beat map v2 (150 BPM, 1 beat = 0.4s, 75 beats).** 0.0 hook grid · 2.4 Color Me Merry hero · 4.4 / 6.4 / 8.4 counters · 10.4 tap Holiday · 12.4 swipes (✕ 13.1, ♥ 14.6, ♥ 16.0) · 16.8 favorites row · 18.0 mat zoom · 20.0 rack swipes · 23.2 match card · 25.6 quilt · 26.8 end card. Song start as v1: the drop on "I don't want a lot for Christmas" (~0:51) at reel 0:00; she fine-tunes in Edits.

**Every brand on screen (Tag people, 14):** @soireeallday.co @andersruffdesignco @sunday_mahjong @bird_and_bamboo @bambirdboutique @peacelovemahjong @ohmymahjong @letsbebestiesmahjong @mahj_squad @myfairmahjong @bougiemahjong @viroramahjongofficial @bamletsmahjong @charlestonmahjongclub. Shown, no verified handle (name only): Luxe Mahjong (The Polo Club ✕), Mahjong Register (Very Merry Wreath, Snowflake Lodge, Peppermint Patty), Hip Hip Mahjong (Hip Hip Hanukkah), Mahj & Moon (Candy Cane Christmas Village). Mats shown are in stock (Shopify `.js` check Nov 2 ~10am, 108 in stock; Color Me Merry checked on Squarespace). Tiles/covers in the counters: Dear Santa, Holly Jolly Sugarplum Pink, Nivalee; albums Dear Santa, Nutcracker Ballet, Après Ski Club.

---
## v1 (Nov 1), superseded
DRAFT for Tiffany's OK. Nothing is posted, scheduled or in Planoly.

## Files
| What | File |
|---|---|
| Reel, silent, 1080x1920, 28.8s, 30fps | `holiday-intro-reel.mp4` |
| Same reel with a click on every beat (accent = bar downbeat), to line up the song | `holiday-intro-reel-beat-test.mp4` |
| Reel grid cover (9:16; centre 3:4 crop keeps the card) | `holiday-intro-reel-cover.jpg` |
| Contact sheet, one frame every 0.5s | `holiday-intro-reel-contact-sheet.jpg` |
| Monday feed carousel, 7 slides 1080x1350 | `carousel/feed-01..07.jpg` |
| Every slide as a story frame 1080x1920 | `stories/story-01..07.jpg` |
| Captions (IG + FB Page), lint PASS | `captions/` |
| Builders | `build/` (reel.py, stills.py; inputs: stock.py, mats.py, rec.py, rec2.py, fymlib.py) |

## Concept
Santa made a list; so did we. A gift box pops and real holiday mats burst out, then slot-machine counters roll to the real numbers. After that it cuts between full-screen photo-dump splices and real Find Your Mat-ch v1.10 moments, zoomed in on a phone that never moves during a swipe. In the app: Dear Santa tiles, tap Holiday, ✕ / ♥ / ♥ mats, suitors, + + + zoom on the mat, ♥ / ✕ / ♥ racks, and the app makes the match card. Next a quilt of 54 in-stock holiday mats fills up, doubling on every beat. It ends with "Holiday tiles + mats + racks together" over the card the app just made, then the Find *Your* Mat-ch™ lockup and **Shop now · use code MAHJMATCH**. Per her 12:22am update, no match card appears until the app has made it.

## Song (music-first; she adds it by hand in Edits, never library music)
**Primary: Mariah Carey, "All I Want for Christmas Is You" (150 BPM, after the rubato intro; sources: Wikipedia "indicated 150 BPM" + Mixmeister 150.2).** The love-song theme suits a matchmaker. The reel is cut to 150 BPM: 1 beat = 0.4s, 1 bar = 1.6s, 72 beats = 18 bars = 28.8s.
**Start point:** begin the song at the up-tempo drop, the first downbeat where the drums/bells kick in on "I don't want a lot for Christmas" (about 0:50 to 0:52 into the album version). Put that downbeat at reel 0:00. Check it against the beat-test version: every click should sit on a beat, with the loud clicks on the bar downbeats.
Shortlist (other BPMs are approximate and not cut-checked):
1. Mariah Carey, All I Want for Christmas Is You (150): PRIMARY
2. Kelly Clarkson, Underneath the Tree (~160; a double-time feel at 80 shows up in databases): close tempo, so cuts stay on beat if she starts at the first chorus
3. Ariana Grande, Santa Tell Me: poppy, but slower; cuts land on the half-beat
4. Brenda Lee, Rockin' Around the Christmas Tree: classic, fun
5. Wham!, Last Christmas: love theme, slower

## Beat map (reel time = beat × 0.4s)
| Beats | Time | Scene |
|---|---|---|
| 0-4 | 0.0-1.6 | Hook "We made a holiday list." → "And checked it twice." box shakes on each beat, lid pops on beat 3, real mats burst out |
| 4-16 | 1.6-6.4 | Slot counters, landing on beats 6 / 10 / 14: **140+** holiday mats in Find Your Mat-ch™ · **10+** holiday tile sets · **40+** holiday albums full of match cards |
| 16-20 | 6.4-8.0 | Photo dump, 1 per beat: Dear Santa tiles, Tartan Tidings mat, Rackin' Rudolph tiles, Very Merry Wreath mat |
| 20-32 | 8.0-12.8 | APP: push in on the Holiday chip, tap on beat 21; ✕ The Polo Club (beat 23.5), ♥ Candy Cane Lane (25.5), ♥ Festive Plaid Premium (27.5); push in on "2 suitors" |
| 32-40 | 12.8-16.0 | Quilt doubles each beat (1→2→4…54 mats); "Christmas." "Hanukkah." "Snow days." on beats 37/38/39 |
| 40-50 | 16.0-20.0 | APP racks step: + + + zoom on the mat (beats 40/41/42), ♥ Persimmon, ✕ Basil, ♥ Walnut, then the app makes the card |
| 50-52 | 20.0-20.8 | "It's a match!" Story card |
| 52-60 | 20.8-24.0 | Photo dump on 8th notes (tiles / mats / Milk Glass racks), then **400+** holiday matches and counting |
| 60-64 | 24.0-25.6 | "Holiday tiles / + mats / + racks / together." over the card the app made |
| 64-72 | 25.6-28.8 | Lockup: Merry Mahjong · Find *Your* Mat-ch™ · "The only place to see holiday tiles, mats & racks together, then shop them." · **Shop now · use code MAHJMATCH** · LINK IN BIO |

## Counts used (from data, Nov 1 ~12:10am ET)
- **152 holiday mats in Find Your Mat-ch:** the published FYM v1.10 artifact (6epA9HuEdT32zUp79Qv3kd) `const D`, mats with `hol` true and not `hid` (166 hol minus 14 hidden).
- **13 holiday tile sets:** the FYM v1.10 `BACKG.Holiday` list (16) minus the 2 hidden sets (Christmas Kiss, Nativity) and Glitter Glow, which has no entry in `D.sets`.
- **45 tile set albums with holiday matches:** the live mahjmatchmaker.com/holiday-mahjong-matches page has 11 new holiday tile set sections plus 34 "tiles you already own" sets with holiday matches. The page's own stat strip says "49 tile sets", so 45 is the conservative count of sections actually on the page.
- **400+ holiday matches and counting:** the live page's own stat ("400+ holiday matches & counting"). The section counts add up to 404, a number we never write, so "400+" is used.

## Stock (checked Nov 1 ~12:10-12:30am ET, Shopify `/products/<handle>.js` `available`)
Only confirmed in-stock products are featured: 83 in-stock holiday mats (the quilt, bursts and photo dump use these only; Etsy, Tigre de Tartán, Splash of Color, Mahjong Studios and Paige Spearin are excluded, and so are out-of-stock mats such as Britt Mills Merrywood / Nutcracker / Winter Berry, Mahj Mood Sleigh All Day, Mahj Squad Candy Cane Pink Wonderland and Virora Hiverelle). Tiles in stock: Dear Santa, Rackin' Rudolph, Holly Jolly (all 3), Tinselle Emerald, Nivalee Blue, Nutcracker Ballet, Après Ski Club. Tinselle Ruby is OUT, so it isn't used. Racks in stock: Bird & Bamboo Persimmon + Basil, Bam Bird Boutique Walnut, Middle & Main Milk Glass. The one exception is The Polo Club (Luxe Mahjong), shown only as the ✕ swipe and not stock-checked. OMM blocks `.js`, so OMM mats come from the FYM list. Recheck Monday morning.

## Every product on screen (named in the reel; tag in Tag people)
App: Dear Santa tiles (Anders Ruff), The Polo Club (Luxe Mahjong, ✕, no verified handle), Candy Cane Lane + Classic Very Merry Mahj (Anders Ruff), Festive Plaid Premium (Sunday Mahjong), Persimmon + Basil racks (Bird & Bamboo), Walnut racks (Bam Bird Boutique). Photo dump: Tartan Tidings (Anders Ruff), Rackin' Rudolph tiles (Hip Hip Mahjong, no verified handle), Very Merry Wreath + Snowflake Lodge (Mahjong Register, no verified handle), Holly Jolly Sugarplum tiles + Holly Jolly Christmas mat (Bam! Let's Mahjong), Merriment (Oh My Mahjong), Milk Glass racks (Middle & Main), Nutcracker Ballet tiles + Clara's Dream Christmas (Mahj Squad), Après Ski Club tiles (Charleston Mahjong Club), Nivalee tiles (Virora). Quilt/bursts: also Peace Love Mahjong, Britt Mills, Let's Be Besties, My Fair Mahjong, Mahj Mood, YOLO Mahjong.

## Captions (copy-paste; lint PASS)
**IG reel** (`captions/reel-ig-caption.txt`):
> We made a holiday list and checked it twice 🎄💗 140+ holiday mats in Find Your Mat-ch: pick your tiles, swipe mats, add racks, then shop the whole look. Dear Santa by @andersruffdesignco on Festive Plaid by @sunday_mahjong, link in bio
> Code MAHJMATCH 💗
> #mahjong #mahjongmat #christmasmahjong #mahjmatch #affiliate

**FB Page reel:** `captions/reel-fb-caption.txt` (brand names, no @). **Carousel IG/FB:** `captions/carousel-ig-caption.txt` / `carousel-fb-caption.txt`.

**Tag people (16):** @andersruffdesignco @sunday_mahjong @bird_and_bamboo @bambirdboutique @middleandmainmahjong @ohmymahjong @mahj_squad @charlestonmahjongclub @viroramahjongofficial @bamletsmahjong @peacelovemahjong @brittmillsdesign @letsbebestiesmahjong @myfairmahjong @mahj_mood @yolomahjong. Named in the reel but without a verified handle (name only): Luxe Mahjong, Hip Hip Mahjong, Mahjong Register.

## Collaborator invites (why they'd reshare)
1. **Anders Ruff:** their Dear Santa tiles and Candy Cane Lane mat drive the in-app moment, and their preorders are open now. They reshared the launch reel, and the Merry Mahjong brief says to reward them.
2. **Sunday Mahjong:** Festive Plaid Premium is the mat that "wins" and lands on the final match card, so their product is the hero of the payoff.
3. **Bird & Bamboo:** their Persimmon rack is hearted with the mat zoomed in, then shown on the card. This is the rack-matching story they never get to tell themselves.
(The quilt and photo dump give 13 more brands a visible moment, which makes each a reason to share to stories.)

## Reminder-box first line (for Planoly, when approved)
"Add All I Want for Christmas Is You at the drop (~0:51), then post". Cover: `holiday-intro-reel-cover.jpg`.

## QA
- center_check: the text scenes (hook, counters, end card) PASS once snow and the mosaic background are turned off. The only flags are the gift box's beat shake (9px) and the asymmetric plaid background behind the centred card. The photo, quilt and app frames flag because the content itself is busy (left-aligned app UI), not because of layout.
- Phone still: the camera is fixed through every swipe (rule 20). `--phone-still --phone-color 14121a` PASSES on the racks swipes (16.9-18.25s). On the mat swipes the phone bezel sits off-frame at that zoom, so the tool can't find it, but the camera transform is a constant there by construction.
- Safe zones: key text sits between y 250 and 1520; labels avoid the right 15%.
- The card is the app's own Story 9:16 output (rule 19). ✕ and ♥ appear in both steps (rule 14). The tile strip and mat show big together on the mat swipes (rule 22).

## Update Nov 1 ~2am (polish)
Counts now follow ../COUNTS.md (140+ holiday mats, 10+ holiday tile sets, 40+ holiday albums, 400+ holiday matches); captions, carousel slides 2 + 6, story frames 2 + 6 and the cover re-rendered to match. End card: mahjmatchmaker.com removed (no URL in reels; "Link in bio" stays). PLM Spirit of Christmas tiles (sold out) dropped from the tile-sets counter mosaic. Quilt/400+ background stock re-checked: all 54 quilt mats are in stock tonight (the Britt Mills Winter Berry / Merrywood / Nutcracker shown are the in-stock LEATHERETTE versions, not the sold-out neoprene ones; Virora Hollivia, not Hiverelle). The app moments (8.0-12.8 s, 16.0-20.0 s) are spliced from the previous render because the recording frames in /dev/shm were gone; they are unchanged. Counts section above is superseded by ../COUNTS.md.
