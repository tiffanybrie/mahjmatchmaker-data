# Late partner holiday mats: holiday album shortlist (Oct 26)

These are **proposals only.** Album matches are Tiffany's call. Nothing has changed in any album, the FYM build or the site. Source: MATCH-INBOX items from Oct 26 5:39pm.

**How the list was made**
- **Candidates:** the 51 visible tile sets whose match list (`m`) already holds a holiday mat, meaning the albums that have a holiday section (FYM b97). None of the 12 late mats is in any album yet.
- **Scoring:** the same colour score the builder uses for FYM ranking, in `builder/fym_catalog_add_oct16.py`. That is 0.6·sim(tile→mat) + 0.4·sim(mat→tile), using CIEDE2000 on weighted swatches.
  - Mat colours come from the mat's `ms`.
  - Tile colours come from `config/tile-tones.json` palettes.
  - The 11 holiday-only sets (Dear Santa, Holly Jolly ×3, Tinselle ×2, Nivalee, Nutcracker Ballet, Après Ski, Rackin' Rudolph, December 1994) have no palette there. Their swatches were set by eye from `assets/tiles/holiday/` photos.
  - The list was then re-ordered by how close the tile **back** colour is to a main mat colour (doc 76: the back is dominant).
- **Why not the app's own ranking:** the app's `setsForMat` reads the precomputed `set.rank` arrays. Those still put these late mats at the very end, so they couldn't be used.
- **Final check:** every pick was looked at side by side (contact sheets below). Weak ones were dropped, for example December 1994 (cream tiles) for Toasty & Tipsy and Birdie (aqua) for the two blue mats.

Contact sheets: `assets/qa/holiday-late-oct26/NN-<mat>.jpg`. Each shows the mat first, then the candidate tile photos.

---

### 1. Soirée All Day · Toasty & Tipsy
Forest-green border, blush-pink striped centre, ornaments. Sheet: `01-soiree-toasty-and-tipsy.jpg`
- **Miss Classic Malachite** (Miss Mahjong): its deep-green marbled backs match the forest border, and the pink/red layer picks up the blush centre.
- **Dear Santa** (Anders Ruff): its dark-green backs match the border, and the vintage red/green Christmas faces match the ornament garland.
- **Nutcracker Ballet** (Mahj Squad): its blush-pink backs match the pink centre exactly, and the green and red accents tie in the border.

### 2. Soirée All Day · Poinsettia Party
Olive/chartreuse field, berry-magenta border, poinsettias. Sheet: `02-soiree-poinsettia-party.jpg`
- **Dandy** (Oh My Mahjong): its magenta backs plus olive layer are the mat's two colours exactly (her own read of Dandy is "magenta with an olive layer").
- **Palm Royale** (Oh My Mahjong): its olive/sage backs sit on the mat's green field, and the pink faces echo the berry border.
- **Limoncello** (Oh My Mahjong): its chartreuse backs match the field colour, and the pink faces tie in the poinsettias.

### 3. Soirée All Day · Color Me Merry
Cream, pastel pink, sage, red ribbon and confetti, green tree. Sheet: `03-soiree-color-me-merry.jpg`
- **Nutcracker Ballet** (Mahj Squad): soft pink backs with painted red/green holiday faces, the same storybook-pastel Christmas look.
- **Holly Jolly (Sugarplum Pink)** (Bam! Let's Mahjong): pink backs with red and green candy-cane faces, matching the mat's red scallop and green tree.
- **La Fête** (Oh My Mahjong): pastel pink backs with green/teal stripes, matching the sage and pink.
- **Miss Classic Jade** (Miss Mahjong): green marbled backs with pink/red faces, if she wants the green to lead.

### 4. Soirée All Day · Pretty in Pink
Pale pink, red scalloped frame, pink tree. Sheet: `04-soiree-pretty-in-pink.jpg`
- **Holly Jolly (Sugarplum Pink)** (Bam! Let's Mahjong): candy-pink backs with red faces, very close to the mat's pink-and-red frame.
- **Nutcracker Ballet** (Mahj Squad): blush backs match the mat's background pink.
- **La Fête** (Oh My Mahjong): its pale pink backs are the closest measured colour (back ΔE 2).
- **Luminaire** (Oh My Mahjong): peach-pink and lavender layers. A softer, all-pastel take.

### 5. Soirée All Day · Home for the Holidays
Cream, red wavy frame, vintage Santa / candy-cane / tree stripes. Sheet: `05-soiree-home-for-the-holidays.jpg`
- **Holly Jolly (Rudolph Red)** (Bam! Let's Mahjong): red backs with white faces painted in vintage red/green Christmas art, the same retro feel as the stripes.
- **Nutcracker Ballet** (Mahj Squad): blush backs pick up the mat's warm pink-cream, and the faces are painted Christmas scenes.
- **Hummingbird** (Sunday Mahjong): warm cream tiles with red/green faces, a quieter heirloom look. The mat is mostly cream, so this works.

### 6. Soirée All Day · Star of David Hanukkah
Pale blue stripes, blue star, green olive wreath. Sheet: `06-soiree-star-of-david-hanukkah.jpg`
- **Osler** (Oh My Mahjong): powder-blue backs match the stripes closely. Osler already holds Hip Hip Hanukkah.
- **Lola** (Oh My Mahjong): blue/white layered backs match the striped border and the blue star. Already holds Hip Hip Hanukkah.
- **Moonlight** (Oh My Mahjong): periwinkle backs with a green layer, matching the blue star and green wreath. Already holds Hip Hip Hanukkah.

### 7. House of Hearts Studio · Peace on Earth
Cobalt blue, folk-art border with red flowers and green leaves. Sheet: `07-hoh-peace-on-earth.jpg`
- **Lola** (Oh My Mahjong): its cobalt backs are the closest blue to the mat's field.
- **Moonlight** (Oh My Mahjong): its blue and green-striped backs echo the blue field and green leaves.
- **Osler** (Oh My Mahjong): powder-blue backs with a red layer that picks up the red folk flowers.

### 8. My Fair Mahjong · Plaid Tidings
Green/red/cream plaid scalloped border, emerald centre. Sheet: `08-mfm-plaid-tidings.jpg`
- **Tinselle (Emerald Green)** (Virora Mahjong): its emerald marbled backs match the centre (back ΔE 4), and the red/green faces match the plaid.
- **Dear Santa** (Anders Ruff): dark-green backs with red/green faces, a classic plaid-Christmas pairing.
- **Nantucket** (Oh My Mahjong): red backs with green/white stripe layers are the plaid's colours exactly.
- **Rackin' Rudolph** (Hip Hip Mahjong): red and green backs, a festive red-and-green match.

### 9. My Fair Mahjong · Peppermint Wishes
Hot-pink centre, red/pink/white peppermint stripes with red bows. Sheet: `09-mfm-peppermint-wishes.jpg`
- **Holly Jolly (Sugarplum Pink)** (Bam! Let's Mahjong): pink backs with red candy-cane faces. This is the peppermint theme on tiles.
- **Amara** (Oh My Mahjong): hot-pink backs are the closest strong pink to the centre.
- **Glitterville** (Oh My Mahjong): raspberry-to-pink backs and sparkly candy faces, for the bold red-pink side.
- **Nutcracker Ballet** (Mahj Squad): softer blush backs with red accents. Optional; the mat is brighter than these tiles.

### 10. Bespoke Mahjong · It's a Vibe Holiday
Busy cartoon bar scene in navy/blue, green and red bands. Sheet: `10-bespoke-its-a-vibe-holiday.jpg`
- **Nantucket** (Oh My Mahjong): red backs with green stripes match the green and red bands, and the white faces calm the busy print.
- **Osler** (Oh My Mahjong): blue backs with a red layer pick up the blue top band and the red bottom band.
- **Rackin' Rudolph** (Hip Hip Mahjong): red and green backs, the same playful, humorous holiday tone.
- Note: this mat is all over the colour wheel, and nothing scores very tightly. This one needs her gut check more than the others.

### 11. Bespoke × Gray Malin · A Very Merry Getaway, Side A: Lighthouse
Pink sky, olive grass, red jeep, tree. Sheet: `11-bespoke-graymalin-side-a-lighthouse.jpg`
- **Nutcracker Ballet** (Mahj Squad): blush-pink backs match the sky, and the red/green painted faces echo the jeep and tree. Ranked #1 by score.
- **La Fête** (Oh My Mahjong): pink backs match the sky, and the green/olive stripes match the grass.
- **Palm Royale** (Oh My Mahjong): olive/sage backs match the grass, and the pink faces match the sky.

### 12. Bespoke × Gray Malin · A Very Merry Getaway, Side B: Beach Tree
Sand, peach sunset, dark tree, brown dogs. Earthy and warm. Sheet: `12-bespoke-graymalin-side-b-beach-tree.jpg`
- **Pearlescent** (Oh My Mahjong): pearly cream/peach backs are the sand and sunset (back ΔE 6.5).
- **Classic Tortoise** (Bam Bird Boutique): tortoise browns match the dogs and the warm, earthy beach.
- **Hummingbird** (Sunday Mahjong): warm cream tiles are the closest colour to the sand.
- **Heritage 2.0** (Oh My Mahjong): burl/peach backs with a green layer, matching the sand and the tree.
- Note: Sides A and B are one product, so she may prefer to match the mat once by the side she'd show first.

---
Scores and palettes: scratchpad `hol/scores.json` (not committed). Re-run the full ranking with `score.py`. Next step if she approves: add her yeses to each set's `m` (her real picks), then run the NEW-ALBUM-CHECKLIST holiday-section steps.
