# Table view photo coverage (Nov 1, 2026)

Question: how many FYM items have photos that can build the new top-down **Table view** (mat flat from above, single rack cut-outs on 4 sides, tile-back walls, tile-faces circle)? This is to help decide how prominent Table view should be.

**Method: measured, not extrapolated.** Source is the live build b112 (`const D`), visible items only (`hid` excluded). Every visible mat photo (1,204 of 1,205; one photo file, `m/111.webp`, is missing from the build) was checked by eye on 48-up contact sheets, with zoomed sheets for unclear ones. Every visible rack cut-out (299) and every visible tile-set photo (283 sets, merged sets excluded) was checked the same way. Existing flags did not answer the top-down question: `mat_photo_flags.json` only has ok/ok_fym_props for visible mats, and `fym-mat-flat-oct26.json` covers 10 already-fixed mats. So the classifications here come from looking at the photos. Per-item results: `config/tableview-photo-class-nov01.json`.

## Summary

| | Count | % |
|---|---|---|
| **Mats (visible)** | **1,205** | |
| A: full mat, flat/top-down | 1,048 | 87.0% |
| B: top-down but cropped / corner / peel-corner / rolled edge (Corner view only) | 125 | 10.4% |
| C: angled, room, rolled, folded (not usable) | 32 | 2.7% |
| Racks ON the mat: none | 1,155 | 95.9% |
| Racks ON the mat: clear/tinted acrylic (OK) | 13 | 1.1% |
| Racks ON the mat: colored/wood/tortoise (omit) | 37 | 3.1% |
| **Full table ready** (A, no colored racks) | **1,015** | **84.2%** |
| Corner view ready (A or B, no colored racks) | 1,137 | 94.4% |
| Full table if the 90 peel-corner renders get a corner fill | 1,105 | 91.7% |
| Holiday mats Full-table ready (A) | 141 of 156 | 90% |
| **Racks (visible)** | **299** | |
| S: clean straight single cut-out | 176 | 58.9% |
| Sbg: single straight, but on a white box (needs a cut) | 13 | 4.3% |
| **Usable single cut-out (S + Sbg)** | **189** | **63.2%** |
| P: single rack, but in perspective (with pusher at an angle) | 38 | 12.7% |
| G: group/stack/lifestyle photo (not usable) | 72 | 24.1% |
| **Tile sets (visible)** | **283** | |
| Back clearly in photo (wall-ready) | 195 | 68.9% |
| Backs only partly visible / small / angled | 27 | 9.5% |
| No back in photo | 61 | 21.6% |
| Back type: solid / pattern / unknown | 174 / 68 / 41 | 61% / 24% / 14% |
| **Wall-ready** (clean back photo, or solid back colour-fillable from the tile body) | **237** | **83.7%** |
| Pattern back with no clean back photo | 5 | 1.8% |
| Back type unknown (no back in photo) | 41 | 14.5% |

What these mean:
- **B is mostly fixable.** 90 of the 125 B photos are flat product renders that show the whole mat except one curled "peel" corner showing the black underside: all 58 YOLO, 15 Betty June & Jeannette, plus Mahjong Register, Sophie Clima, Etsy and others. Fill that corner by mirroring the opposite corner and they become Full table ready. The remaining B photos are true crops: corner close-ups and partial frames (Miss Mahjong 11, Tigre de Tartan 5, Mahj Squad 4, Mahj Tile Haus 2, Anders Ruff 2) and rolled edges (5).
- **C is small (32).** It's 11 rolled Let's Mahj On product shots, 10 angled shots, 4 folded vegan-leather mats, and a few room or table scenes (Tigre de Tartan, Charleston Mahjong Club, Mahj Squad).
- **Colored racks on the mat (37)** come from Mahj & Moon's lifestyle renders (16, pastel racks stacked with tiles), Tigre de Tartan's styled shots (9, tortoise or dark-wood frames), Betty June & Jeannette's mats shown with matching pink/blue/yellow/red racks (7), Bird & Bamboo (3), Sunday (1) and Oh My Mahjong (1). The 13 clear-rack photos are Virora's clear-acrylic renders (11), one Bespoke mat with tinted teal acrylic (Garden Glow Turquoise), and one Tigre de Tartan mat.
- **Racks:** the 299 visible racks include 176 clean straight cut-outs: Bird & Bamboo's whole line (93), most of Peace Love, My Fair Mahjong macarons, Mahjong Register, Virora, Mahjong Row and Bam Bird. Group shots are concentrated in Miss Mahjong (10), Mahj Mood (9), My Fair Mahjong pearl/tortoise (8), Bam! (6), and Bespoke, OMM, Sunday and TdT (5 each). The 13 Peace Love "Wavy" racks and the OMM rack+pusher sets are single racks in perspective; they could work with a skew correction.
- **Tile walls:** Bam Bird, Yellow Mountain and Virora are faces|backs split photos (ideal). Most OMM, Royal, Let's Mahj On, Mahjong Row and Hip Hip pile photos show plenty of backs. The 21 "no back, solid" sets are sets whose body colour is the back colour (Amahj, Peace Love Mod/OG coloured, My Fair Mahjong coloured series), so they can be colour-filled.

## Mats lost from Full table, by brand (worst coverage first)

"Lost" = B + C + A-with-colored-racks.

| Brand | Visible mats | Full table OK | B corner-only (of which peel-corner) | C unusable | Colored racks on mat | Lost from Full table |
|---|---|---|---|---|---|---|
| That Mahjong Moment | 1 | 0 | 1 (0) | 0 | 0 | **1 (100%)** |
| YOLO Mahjong | 64 | 6 | 58 (58) | 0 | 0 | **58 (91%)** |
| Let's Mahj On | 19 | 5 | 3 (0) | 11 | 0 | **14 (74%)** |
| Splash of Color | 5 | 2 | 2 (2) | 1 | 0 | **3 (60%)** |
| Tigre de Tartan | 29 | 13 | 5 (0) | 5 | 9 | **16 (55%)** |
| Miss Mahjong | 21 | 10 | 11 (0) | 0 | 0 | **11 (52%)** |
| Mahj Squad | 20 | 12 | 4 (0) | 4 | 0 | **8 (40%)** |
| Sophie Clima | 10 | 6 | 4 (4) | 0 | 0 | **4 (40%)** |
| Mahj Tile Haus | 5 | 3 | 2 (0) | 0 | 0 | **2 (40%)** |
| Mahj & Vine | 16 | 10 | 5 (0) | 1 | 0 | **6 (38%)** |
| Charleston Mahjong Club | 15 | 10 | 0 (0) | 5 | 0 | **5 (33%)** |
| Betty June & Jeannette | 73 | 51 | 15 (15) | 0 | 7 | **22 (30%)** |
| Bird & Bamboo | 16 | 13 | 0 (0) | 0 | 3 | **3 (19%)** |
| Etsy | 16 | 13 | 3 (3) | 0 | 0 | **3 (19%)** |
| Mahjong Register | 33 | 27 | 6 (6) | 0 | 0 | **6 (18%)** |
| Mahj & Moon | 114 | 98 | 0 (0) | 0 | 16 | **16 (14%)** |
| Amahj | 8 | 7 | 0 (0) | 1 | 0 | **1 (12%)** |
| Royal Mahjong Society | 8 | 7 | 0 (0) | 1 | 0 | **1 (12%)** |
| Hutch & Nook | 9 | 8 | 1 (1) | 0 | 0 | **1 (11%)** |
| Virora Mahjong | 12 | 11 | 1 (1) | 0 | 0 | **1 (8%)** |
| Mahj Mood | 15 | 14 | 0 (0) | 1 | 0 | **1 (7%)** |
| Sunday Mahjong | 15 | 14 | 0 (0) | 1 | 1 | **1 (7%)** |
| Let's Be Besties | 53 | 51 | 1 (0) | 1 | 0 | **2 (4%)** |
| Piper Chase Studios | 27 | 26 | 1 (0) | 0 | 0 | **1 (4%)** |
| Anders Ruff | 59 | 57 | 2 (0) | 0 | 0 | **2 (3%)** |
| Oh My Mahjong | 58 | 57 | 0 (0) | 0 | 1 | **1 (2%)** |

The other 31 brands lose nothing (484 mats, all Full-table ready).

## Pattern-back sets with no usable back photo (5)

- Bespoke Mahjong: Corey Paige Color Crush (Pearl Crush) (pearl marble backs, only angled)
- My Fair Mahjong: Crystal Confetti, Crystal Prism (marbled backs, only seen edge-on in a pile)
- My Fair Mahjong: The Jubilee Series (Midnight Blue) (blue marble, two angled tiles)
- Virora Mahjong: Iriselle (pastel layered back, only a corner)

## Sets whose back type is unknown (41; the photo shows faces only)

These need a back photo from the brand, or a confirmed solid colour, before they can get walls:

- Bespoke Mahjong (14): Corey Paige Color Crush (Bright White), Grateful Dead (Rose Pink Tie Dye Pearl), Grateful Dead (Stealie Blue Tie Dye Pearl), Grateful Dead (Sunshine Daydream Tie Dye Pearl), Gray Malin Beach Club (Cabana Blue), Gray Malin Getaway Dogs (Beverly Hills Pink), Gray Malin Getaway Dogs (Bright White), Gray Malin Getaway Dogs (Icy Blue), Lucky Charms (Marshmallow Pink), Pop Diva (Bright White), Springtime Safari (Petal Pink), The Chalet (Frosty Lilac), Year of the Horse (Pearl Cream), Year of the Horse (Saddle Pink)
- My Fair Mahjong (5): Florida Series, NYC Series, The New England Series, The Scandinavian Folk Art Series, The Texas Series
- Middle & Main Mahjong (4): Barrier Island, Charleston, Palmetto, Sunshine
- Peace Love Mahjong (4): Merry Nutcracker, OG Desert Dreams, OG Vibrant Vibes, Spirit of Christmas
- Tigre de Tartan (3): House Clovers, House Hearts Warm White, House Tigers Oyster
- Amahj (2): On the Water Signature, Round Top Stamped
- Anders Ruff (2): Brownstone Bloom, Green Light Gatsby
- Bam! Let's Mahjong (2): Art Deco, Hocus Pocus Halloween
- Bird & Bamboo (2): The Belle, The Boho Chic
- Mahj Squad (1): Just Peachy
- Sunday Mahjong (1): Hummingbird
- YOLO Mahjong (1): Journey to the West

## Racks with only group/lifestyle photos (72), by brand

- Miss Mahjong: 10
- Mahj Mood: 9
- My Fair Mahjong: 8
- Bam! Let's Mahjong: 6
- Bespoke Mahjong: 5
- Oh My Mahjong: 5
- Sunday Mahjong: 5
- Tigre de Tartan: 5
- Hip Hip Mahjong: 4
- Bam Bird Boutique: 3
- Middle & Main Mahjong: 3
- Yellow Mountain Imports: 3
- Anders Ruff: 2
- Royal Mahjong Society: 2
- Charleston Mahjong Club: 1
- Let's Mahj On: 1

## Notes
- Contact sheets I looked at are in the session scratchpad (`tv-count/sheet_*.jpg`, `rsheet_*.jpg`, `tsheet_*.jpg`). They are not committed. Examples: `sheet_1152.jpg` shows peel-corner renders, `sheet_0528.jpg` shows rolled Let's Mahj On shots, `rsheet_180.jpg` shows rack group shots, and `tsheet_000.jpg` shows split back photos.
- Round mats (Mahj & Moon x4, YOLO x3) count as A. They are flat from above, but Table view will need a round-mat layout.
- Some A mats show tiles or props lying on the mat with no racks (e.g. Bespoke Garden Glow, the Virora renders). These are counted as racks "none" or "clear"; a tile-scatter filter is a separate question.
- 10 Piper Chase Studios renders have a rack graphic printed above the mat, not on it. These count as A, racks none (crop the top strip).
