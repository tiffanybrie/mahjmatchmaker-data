# Pinned Find Your Mat-ch reel, v3 A + B (Nov 8 2026, Tiffany's 4:05pm notes in FEEDBACK-nov08-v3.md)
fym-pinned-reel-v3A.mp4 / fym-pinned-reel-v3B.mp4: 1080x1920, 30fps, **58.9s** each, silent (Planet Mahjong added in the app; cheer ends at 59s).
**A** = v2 style with every fix. **B** = same, but leans into the views: the mat swipes AND the rack step happen in **Table view** (racks + tiles on the mat).
Covers: fym-pinned-reel-v3A-cover.jpg / -v3B-cover.jpg (18.6s, Find Your Mat-ch + 3 phones, same as v2).
Contact sheets (1 frame / 0.5s): fym-pinned-reel-v3A-contact-sheet.jpg, -v3B-contact-sheet.jpg. Safe-zone overlay sheets: -v3A-safezones.jpg, -v3B-safezones.jpg
(red = IG top 14% / bottom 20% / right icon rail, orange = bottom 35%, blue hatch = story link-sticker lane y 1450-1640, green box = text area y 270-1440).
**PICKED: B (Tiffany Nov 10 10:28pm).** Final = fym-pinned-reel-v3B-endcard.mp4 (58.9s): v3B 0-52.8 + the full-frame Find Your Mat-ch end card (scripts/social/endcard/fym_brands.py - + animate.py fym, 6.1s, cream, wordmark, 1,500+ line, MAHJMATCH pill, 6 scrolling logo rows to the bottom), replacing the navy end page with the empty bottom half. Cover = v3B-cover.jpg.

| Time | Scene (A) | B differs |
|---|---|---|
| 0-19.6 | v2 teaser, unchanged (cut from fym-pinned-reel.mp4) | same |
| 19.6-24.0 | Start with your tiles -> "Search your set": phone zoomed 1.4x on the search box, "Sunday" typed at real speed (280ms/letter, ~2s) -> "Tap your tiles" | same |
| 24.0-31.4 | View switcher: "View it up close" -> "From above" (Aerial) -> "Or at the table" (Table), taps ringed; back to Up close; swipes with tiles + mat both in frame, NO dimming: ♥ Brownstone Bloom, ✕ Chinoiserie Songbird, ♥ Carson Vintage, ♥ Knox | swipes stay in Table view (tiles circle + racks on each mat), 24.0-31.05 |
| 31.4-33.2 | Pick your favorite: straight zoom in on Brownstone Bloom | 31.05-32.85 |
| 33.2-39.6 | "Add racks" (mat + rack together, zoomed) -> "Find racks by color" (brown dot tapped) -> "Or by wood tone" (Wood tone tapped) -> "Love it": ♥ Bam Bird Boutique Walnut, ♥ Peace Love Mahjong Oak. YES racks only, no blue ✕ rack | "Add racks, at the table": Walnut and Oak shown ON the Brownstone Bloom mat around the Sunday tiles (Table view), 32.85-39.6 |
| 39.6-41.2 | Make it official (button zoomed 2.4x) | same |
| 41.2-45.6 | "Save + share your match card": the graphic changes Story close up -> Story mood board (selector not shown, Post skipped) | same |
| 45.6-50.2 | Shop your match: live stock check (Sunday sold out), 1-2-3 Shop rings on mat + 2 racks, "Use code MAHJMATCH" pill (moved up to y 440) | same |
| 50.2-52.8 | See it together. Save it. Share it. Shop it. (lifted to y 400-1230) | same |
| 52.8-58.9 | Find *Your* Mat-ch (96px, breathing room) / Match Tiles, Mats & Racks Across Brands (Title Case, brand-guide tagline) / LINK IN BIO / partner logo strip (ends y 1424) | same |

Build: build/cap3.py (+lib3.py) re-records the LIVE site app v118 (@7817f04d) -> /dev/shm/pin3/{rec0,SA,PA,KA,SB,PB,KB};
build/reel3.py A|B frames renders 19.6-58.9 (camera keyed to recording time; safe overlay: `reel3.py A safe <t>`); build/assemble3.sh concats.
Logo strip: assets/hub/build-2026-11-07/trim (no Tigre de Tartán, Sunday, YMI, Mahjong Row).

## Checklist v3A
- [x] Readable typing: "Sunday" types over ~2s, search box zoomed 1.4x
- [x] No greying of tiles during mat swipes (spotlight only on buttons: Start with tiles, pick, Make it official, shop rows)
- [x] Up close / Aerial / Table switcher shown (3 taps, labelled)
- [x] Blue ✕ rack cut; only the 2 yes racks
- [x] Zoom on mat + rack and the rack filters (color dot, Wood tone) — A shows the app's Up close rack step (mat thumbnail above the rack), so the rack sits under the mat, not on it; B is the version that shows racks ON the mat
- [x] "Save + share your match card" shows the graphic change, Story close up -> Story mood board
- [x] Live stock + 1-2-3 Shop highlight kept
- [x] All text/callouts inside y 270-1440 and x < 950 (checked on -v3A-safezones.jpg)
- [~] Link-sticker lane y 1450-1640: no text, callout, tap or code pill in it from 19.6s on; the phone SCREEN imagery still passes through it (lower app rows), and the unchanged 0-19.6 teaser has the album grid/phones crossing it (kept as asked)
- [x] End title with breathing room + Title Case tagline
- [x] 58.9s (<= 59)
## Checklist v3B
- same as A, plus: [x] swipes in Table view; [x] rack step in Table view, Walnut + Oak seen on the mat with the tiles. Same lane note.

# Pinned Find Your Mat-ch reel, v2 (Nov 8 2026, Tiffany's notes in FEEDBACK-nov08.md)
fym-pinned-reel.mp4: 1080x1920, 30fps, **58.9s**, silent (she adds Planet Mahjong by Mahjong King in the app, from the top; the cheer ends at 59s).
Cover: fym-pinned-reel-cover.jpg (18.6s, Find Your Mat-ch + 3 phones). Contact sheet (1 frame / 0.5s): fym-pinned-reel-contact-sheet.jpg.
Planoly draft group 01a1b83b-fc22 (IG reminder + FB Page reel draft).

| Time | Scene |
|---|---|
| 0-2.0 | We've been busy matching. (unchanged start) |
| 2.0-8.1 | count-up of the 44 REAL album covers (rainbow order, Juniper added), Classic Tortoise last, held ~0.65s |
| 8.1-11.7 | cover grid -> '44 tile set albums and counting… All free at mahjmatchmaker.com' (from 9.9) |
| 11.7-13.9 | Tiles. Mats. Racks. |
| 13.9-15.8 | Now it's your turn. |
| 15.8-19.6 | Find *Your* Mat-ch™ + 'Start with your tiles or your mat and find the perfect match across brands.' + phones easing in from 0.8x |
| 19.6-22.2 | Start with your tiles (home -> search Sunday -> tap) |
| 22.2-27.4 | Swipe the mats: ♥ Brownstone Bloom, ✕ Chinoiserie Songbird, ♥ Carson Vintage, ♥ Knox |
| 27.4-30.2 | Pick your favorite: straight-in zoom to Brownstone Bloom, then the mat close-up |
| 30.2-34.6 | Add racks (mat on top, rack right under it): ✕ Teal Wood, ♥ Bam Bird Boutique Walnut, ♥ Peace Love Mahjong Oak |
| 34.6-36.8 | Make it official (button zoomed ~2.9x) |
| 36.8-42.4 | Your match card big on the phone: Post 4:5 mood board -> Story close up -> Story mood board -> Post |
| 42.4-47.4 | Shop your match: live stock check (Sunday sold out), Shop on mat + 2 racks, 'Use code MAHJMATCH' pill |
| 47.4-51.8 | See it together. Save it. Share it. Shop it. (+ small 'code MAHJMATCH') |
| 51.8-58.9 | Find *Your* Mat-ch / tiles, mats and racks across brands / LINK IN BIO / partner logo ticker |

Build: build/render_teaser2.py (tpl_pin2.html, order2.json) -> teaser 0-19.6; build/cap2.py (+lib2.py) records the LIVE site app v118
(jsDelivr pin 7817f04d) -> /dev/shm/pin2/rec*; build/reel2.py renders 19.6-58.9; concat teaser + app (ffmpeg concat, crf 17).
Logos: holiday-nov1/intro/build/v5_prep.py logos (no TdT, Sunday, Mahjong Row, YMI).

## FEEDBACK-nov08 checklist (checked frame by frame on the 0.5s contact sheet at phone size)
| # | Note | Result |
|---|---|---|
| len | <= 59s | PASS 58.9s |
| 1 | Classic Tortoise = real album card, undistorted Bam Bird logo, ~1s shorter | PASS: all covers are now the real album covers (assets/covers/albums/*-cover.jpg, 'MATCHING MAHJONG TILES, MATS & RACKS'); the old uniform-v3 covers with 'FIND YOUR MATCH' + squashed logo are gone. Tortoise on screen ~0.65s (was ~1.3s) |
| 2 | real live album count, ~1s shorter hold | PASS: 44 (54 album pages on /mahjong-tile-matches minus 10 colour albums, Nov 8); panel hold 1.8s (was 2.7s) |
| 3 | cut 'You become the matchmaker'; FYM announced once | PASS: Tiles/Mats/Racks -> Now it's your turn -> Find Your Mat-ch phones -> app. No 'is HERE' card, no 'Today you're the matchmaker' plate |
| 4 | phones card dynamic, start a bit further out | PASS: phones glide in 0.8x -> 1.0x + slow push; title and subline animate in |
| 5 | phone centred, no left/right drift, straight-in zooms | PASS: drift removed; camera only zooms toward the action point (dolly), phone centred at rest |
| 6 | close zoom on Brownstone Bloom | PASS: 2.6x on the Brownstone Bloom suitor, then the mat close-up fills the frame |
| 7 | latest racks UI (rack under mat, menu below) | PASS: re-recorded from the live site app (v118) |
| 8 | 'Make it official' on the phone, big | PASS: button ~2.9x with spotlight and tap ring |
| 9 | phone and card BIG | PASS: phone base 1.25x (fills the width), card ~1.45x |
| 10 | shop list: in-stock mat + 2 racks shoppable, Sunday sold out, MAHJMATCH clear | PASS: plates 'Live stock check' / 'Shop each piece', rings on Sold out and the 3 Shop buttons, pink 'Use code MAHJMATCH' pill |
| 11 | optional: mock-up views | PASS: Post mood board, Story close up, Story mood board |
| 12 | 'See it together. Save it. Share it. Shop it.' + small code | PASS |
| 13 | end card without 'never ask again', 'Find Your Mat-ch: tiles, mats and racks across brands' big | PASS |
| keep | teaser start, spotlight style, ™ once, italic Your, no Mahjong Row/YMI | PASS (™ only on the phones card; the app's own home screen shows its ™ logo for 0.5s, that is the real UI) |
Known: the teaser cuts after 8.1s moved earlier by ~1-2s (her shortened holds), so re-check the Planet Mahjong beat when adding the song in the app.
