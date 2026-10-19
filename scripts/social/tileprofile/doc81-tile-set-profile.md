# 81 Tile Set Profile = color profile + dating profile (Oct 19)

**DRAFT until Tiffany approves the Papaya Spritz example on Ready to Ship** (card "Papaya Spritz launch: color card + dating profile + Introducing carousel", id `l-papaya-launch`).

## Why (Tiffany, Oct 19)
- The color cards are "a designer's black book of color." Keep them mostly exactly as they are: driven by the colorway, the racks that match, the colors, the tiles. Nothing kitschy.
- Social had the cheek but not the value. "Merge the color profile and the dating profile in a beautiful way on social." Mood-boardy and beautiful, a twist of fun, never cartoony.
- The true value: we know the sets, we understand their colors, and we give shortcuts to the set/mat people will love.
- **Order of everything: designer black book first, cheek second.**

## The standard: what goes where

| | Color card (The Tile Edit) | Social profile (carousel / episode intro) |
|---|---|---|
| Job | Reference. A page from the black book. | Introduce her, teach her colors, then flirt. |
| Colors | Backs (squares, role) + faces (dots), our color words | Same colors as chips, with hex codes, plus one line on her tone (clean / earthy) |
| Racks | Her approved rack picks (config/tile-racks-picks.json final_lists) | Same racks, each with a one-line why |
| Mats | Top 3 mats (album order) | Same 3 as "First dates," plus one-line why each ("Her type") |
| Cheek | ONE short profile line, in the old motif/caption spot under the tile pile | Profile line, bio line, dealbreaker, skit |
| Code | Navy pill, code MAHJMATCH | Code MAHJMATCH at <brand> (I may earn a commission) |

## Tone rules
1. Every cheeky line must also be color-useful. "Her type: pink with a papaya streak" tells you which mats to shop. "She's a vibe" doesn't.
2. Classy dating language only: Her type, Looking for, Open to, Dealbreaker, First dates, Racks she's into. No app or show names, no innuendo beyond the existing "nice rack" running joke.
3. Never cartoony: real product photos, our brand fonts (Caprasimo, Playfair italic, Bitter, Caveat for handwritten notes), cream paper, navy ink, pink accents, the set's own color for her name.
4. Never make anything up: colors from the color card spec, tone from config/tile-tones.json (her call), racks from her final lists, mats from her album order. Mat color chips are sampled from the mat photo.
5. Dealbreakers are said helpfully (what fights her colors and why), never knocking a real product.
6. Never sound final: "50 matches and counting."
7. Isolated characters on social: tile pile photo + flat mat photo, no match cards (Oct 17 rule).

## Profile template (config/profiles/<set>.json)
- **Name & brand**, status line (e.g. "The new girl on the block")
- **Profile line** (2 short lines; also goes on the color card). Offer her 3 options per set.
- **Her colors**: backs (name, hex, role) + faces (name, hex) + tone in one line
- **Her type**: 3 entries, each = label (color logic) + mat + brand + 2 color chips + one-line why
- **Dealbreaker**: one color/approach that fights her, stated helpfully
- **Racks she's into**: her approved racks, one-line why each
- **First dates**: top 3 mats (album order)
- **Bio**: one cheeky line
- Match count (say "and counting")

## Every tile set launch gets
1. **Color card**: desktop Tile Edit moodboard + mobile color guide (`python3 scripts/colorcards/build.py <key>`; spec in config/colorcards.json, with `profile_line`).
2. **Profile**: config/profiles/<key>.json, set up together with Tiffany.
3. **Introducing carousel** (1080x1350, 6 slides): hero + profile line / her colors (black-book chips) / her type + why + dealbreaker / racks she's into / first dates / see all her matches + code. `scripts/social/tileprofile/carousel.py` then `shot.js`.
4. **Episode reel** in the new episode model (below). `scripts/social/tileprofile/reel.py` then `render.js`.

## New episode model (Tiffany, Oct 19 11:34am; applies to Pippa, Smith, Coquette and Papaya)
Each episode = **(1) INTRO, value first**, then **(2) the fun skit**.
1. Season 2 tag card (2s): "Mahj Matchmaker 2.0 · Season 2" + episode hook.
2. Full-screen hero tile photo, "Introducing <set>" + bio line (4s).
3. Her colors, full-screen: back/layer color bands with names + hex, then face dots (4s).
4. Her color card, full-screen (4s).
5. Dating profile card: profile line, her type + why, racks she's into, dealbreaker (7s, lines revealed one at a time).
6. Skit: "Help me match <set>" / "<set> swipes right on…" with her top matches (isolated tile + mat), then a fast flip of more album matches, "N matches and counting."
7. End card (brief rules): "Got a tile set looking for love?" / "Let the MAT-ching begin", tile + #1 mat circles dancing, "See all of <set>'s matches now · link in bio", code line, COMING 10.27 Find Your Match, logo.
Little photos dancing into each other are fine for the skit, but the visual wow is full-screen color and full-screen photos.

Re-cuts (after she approves the model on the Papaya example, not before): Pippa (Ep 6 "Two Suitors"), Smith (Ep 8 "Swipe Right on Smith"), Coquette (Ep 13 "Meet the Parents") each get the intro (steps 1-5) in front of their existing skit, trimmed so the whole episode stays about 45-55s. Each needs its profile set up with Tiffany first.

## Files (Papaya example)
- Color cards: assets/colorcards/papaya-spritz/00-papaya-spritz-mahjong-tiles-tile-edit-moodboard.jpg, ...-color-guide-mobile.jpg
- Profile: config/profiles/papaya-spritz.json
- Carousel: assets/social/papaya-spritz-launch/papaya-spritz-introducing-carousel-1..6.jpg + caption-carousel.txt
- Reel: assets/social/papaya-spritz-launch/papaya-spritz-new-girl-episode.mp4 + caption-reel.txt
