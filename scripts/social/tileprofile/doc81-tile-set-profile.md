# 81 Tile Set Profile = the set's dating PROFILE (Oct 19, v2)

**DRAFT until Tiffany approves the Papaya Spritz v2 example on Ready to Ship** (card "Papaya Spritz launch v2: her PROFILE + OMM-forward carousel and reel", id `l-papaya-v2`; v1 was `l-papaya-launch`).

## Naming (Tiffany, Oct 19 12:21pm)
- Call it the set's **PROFILE** (as in an online-dating profile). Not "color card", not "little black book" (dated). Captions say "swipe for her profile".
- The card keeps its look (cream ground, Alfa Slab name, tile pile, backs/faces, racks, top 3 mats, navy code pill). Only the wording turns into profile fields:
  header **HER PROFILE**, **HER COLORS · BACKS / FACES**, **RACKS SHE'S INTO**, **FIRST DATES**, and the profile line under the pile starts "Seeking:" (or "Her type:", "Looking for:").
- Two versions on RTS for her pick: **(a) minimal**, profile wording only; **(b) a bit more dating-app**: verified-match heart badge on the tile photo, small pink hearts on the field labels, a "50 MATCHES & COUNTING" pill, and refined pass / like buttons. Designer, not cartoony.
  Build: `python3 scripts/colorcards/build.py <key> --profile=a|b` (writes 00-<key>-mahjong-tiles-profile-a|b-desktop/mobile.jpg). Plain `build.py <key>` still makes the classic Tile Edit files.
- Papaya profile line = **C**: "Seeking: pink, peach or periwinkle. / Must be comfortable around bright color."

## OMM launches: OMM-forward, never OMM-only (Oct 19)
She earns 20% at Oh My Mahjong through Nov 25, and OMM buyers always ask "what mats go with?". So OMM tile launches add OMM sections, but her true top matches always stay (the card's mat section stays her true top 3, every brand).
Order for the reel and the carousel:
1. **Profile intro**: hero + profile line, her colors, racks she's into (+ dealbreaker).
2. **Made for each other**: the official OMM pair mat for the set (Papaya Spritz + Vivienne), tiles circle + heart + mat, and OMM's own photo of the pair when one exists.
3. **Her OMM sisters**: her top Oh My Mahjong mats from her album, album order, skipping the pair. Vault / retired OMM mats are fine ("from the vault", people already own them).
4. **Strong match potential** (label options: "Strong match potential" / "Playing the field" / "Her top matches, every brand"): her true top 3 across brands, with one-line whys.
5. **See all her matches + code** (end card).
**Non-OMM launches skip the OMM-sisters section** (and the made-for-each-other section unless the brand has an official pair mat). In config: no `omm_launch` block in config/profiles/<key>.json = 5-slide carousel without those slides.
Data: config/profiles/<key>.json `omm_launch` = {pair {mat, brand, img, together, why}, sisters [{mat, brand, vault, img, why}], strong_label, strong_label_options}.
Future angle (not now): sets whose pair mat already has its own full profile (Vivienne does) could get "pair episodes".

## Why (Tiffany, Oct 19)
- The color cards are "a designer's black book of color." Keep them mostly exactly as they are: driven by the colorway, the racks that match, the colors, the tiles. Nothing kitschy.
- Social had the cheek but not the value. "Merge the color profile and the dating profile in a beautiful way on social." Mood-boardy and beautiful, a twist of fun, never cartoony.
- The true value: we know the sets, we understand their colors, and we give shortcuts to the set/mat people will love.
- **Order of everything: designer black book first, cheek second.**

## The standard: what goes where

| | Profile card (was: color card / The Tile Edit) | Social profile (carousel / episode intro) |
|---|---|---|
| Job | Reference. A page from the black book. | Introduce her, teach her colors, then flirt. |
| Colors | Backs (squares, role) + faces (dots), our color words | Same colors as chips, with hex codes, plus one line on her tone (clean / earthy) |
| Racks | Her approved rack picks (config/tile-racks-picks.json final_lists) | Same racks, each with a one-line why |
| Mats | Top 3 mats (album order) | Same 3 as "First dates," plus one-line why each ("Her type") |
| Cheek | ONE short profile line, in the old motif/caption spot under the tile pile | Profile line, bio line, dealbreaker, skit |
| Code | Navy pill, code MAHJMATCH | Code MAHJMATCH at <brand> (I may earn a commission) |

## Tone rules
1. Every cheeky line must also be color-useful. "Her type: pink with a papaya streak" tells you which mats to shop. "She's a vibe" doesn't.
2. Classy dating language only: Her profile, Her colors, Seeking, Her type, Looking for, Open to, Dealbreaker, First dates, Racks she's into, Made for each other, Her OMM sisters, Strong match potential. No app or show names, no innuendo beyond the existing "nice rack" running joke.
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
1. **Profile card** (was color card): desktop + mobile, variant a or b once she picks (`python3 scripts/colorcards/build.py <key>`; spec in config/colorcards.json, with `profile_line`).
2. **Profile**: config/profiles/<key>.json, set up together with Tiffany.
3. **Introducing carousel** (1080x1350): OMM launch = 7 slides: hero + profile line / her colors / racks she's into / made for each other / her OMM sisters / strong match potential + dealbreaker / see all her matches + code. Non-OMM = 5 slides (no pair / sisters). `scripts/social/tileprofile/carousel.py` then `shot.js`.
4. **Episode reel** in the new episode model (below). `scripts/social/tileprofile/reel.py` then `render.js`.

## New episode model (Tiffany, Oct 19 11:34am; applies to Pippa, Smith, Coquette and Papaya)
Each episode = **(1) INTRO, value first**, then **(2) the fun skit**.
1. Season 2 tag card (2s): "Mahj Matchmaker 2.0 · Season 2" + episode hook.
2. Full-screen hero tile photo, "Introducing <set>" + bio line (4s).
3. Her colors, full-screen: back/layer color bands with names + hex, then face dots (4s).
4. Her profile card, full-screen (4s).
5. Profile details: profile line, racks she's into, dealbreaker (6s, lines revealed one at a time).
6. OMM launches: Made for each other (OMM's pair photo full-screen, then tiles + heart + pair mat, 5s), then Her OMM sisters (3 mats pop in, vault tag, 5s).
7. Skit: "Strong match potential" card, "<set> swipes right on…" her true top 3 (isolated tile + mat, MATCH stamp), then a fast flip of more album matches, "N matches and counting." (Non-OMM: "Help me match <set>" card instead.)
8. End card (brief rules): "Got a tile set looking for love?" / "Let the MAT-ching begin", tile + #1 mat circles dancing, "See all of <set>'s matches now · link in bio", code line, COMING 10.27 Find Your Match, logo.
Little photos dancing into each other are fine for the skit, but the visual wow is full-screen color and full-screen photos.

Re-cuts (after she approves the model on the Papaya example, not before): Pippa (Ep 6 "Two Suitors"), Smith (Ep 8 "Swipe Right on Smith"), Coquette (Ep 13 "Meet the Parents") each get the intro (steps 1-5) in front of their existing skit, trimmed so the whole episode stays about 45-55s. Each needs its profile set up with Tiffany first.

## Files (Papaya example, v2)
- Profile cards: assets/colorcards/papaya-spritz/00-papaya-spritz-mahjong-tiles-profile-a-desktop.jpg / -profile-a-mobile.jpg / -profile-b-desktop.jpg / -profile-b-mobile.jpg (classic Tile Edit files re-rendered with line C too)
- Profile: config/profiles/papaya-spritz.json (with `omm_launch`)
- Carousel: assets/social/papaya-spritz-launch/papaya-spritz-introducing-carousel-1..7.jpg + caption-carousel.txt
- Reel: assets/social/papaya-spritz-launch/papaya-spritz-new-girl-episode-v2.mp4 (48s) + caption-reel.txt
