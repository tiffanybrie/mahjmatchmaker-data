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
