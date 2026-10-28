# Picking gap study: why Tiffany's top mats beat our colour ranking (Oct 28 2026)

Context: docs/PICKING-RULES.md (Tiffany, Oct 28 3pm). Our picks are **tonal** (same colour on same colour) or **obvious** (the brand's own pair mat). She wants 2-colour coordination between the tile (back, layers, faces) and the mat, with a 3rd colour only inside a working pair.

This is a data-only study. Nothing in FYM, the locks, the builds or the site was changed.

## Data used
- **Her ordered albums:** FYM v96 build (`origin/fym-site-preview:site-app/fym-v96/index.html`), `D.ao` (album order) for 39 tile sets. Top of the order = best of the best. Cross-checked with assets/cards/papaya-spritz/manifest.json (Heiress #1).
- **Our colour ranking:** `s.cr` in the same build (builder/fym_fix_oct25/v85_colorrank.py: CIEDE2000 palette distance, vividness gap, BACKG group, theme and holiday tweaks).
- **Tile colours:** config/tile-tones.json (back_hex, layer_hex, palette) plus config/fym-colour-oct25.json `sets.sw` (pile photo: faces and accents). Weights: back 35%, layers 15%, palette 25%, photo accents 25%.
- **Mat colours:** `D.mats[*].ms` (unblended k-means swatches, v85).
- **Families:** hue buckets (pink, red, orange, yellow, green, teal, blue, purple, brown). Neutral = Lab chroma < 8. A tile family counts at 6% or more of its chromatic share; a mat family counts at 10% or more.
- **Groups compared (all 39 albums):** her top 5 (195 picks), her next 10 (368), our colour-rank top 5 (195), and a random pool from our ranks 20–300 (1,170).
- **Focus albums:** Papaya Spritz, Miss Classic Malachite, Miss Classic Jade, Lagoon, Amara, Coquette, Heritage 2.0, Gatsby, Willow and Classic Tortoise.
- **Deco:** no Deco tile set has an ordered album yet, so Lagoon stands in for the Deco Lagoon complaint. Our rank for Gatsby already puts Bam Bird **Deco Dragon (Lagoon)** in its top 5.

## Headline: how far apart we are
- Of her top 5 per album, on average only **0.28 of 5** land in our top 20.
- The median position of her top-5 picks in our ranking is **196**.
- **34%** (67 of 195) fall outside our top 300 entirely: 57 because they score low on colour, 9 because they're retired and 1 because it's hidden.

## The rules that explain her top picks

### 1. She does NOT put the tile's main colour on the mat (anti-tonal)
| | Her top 5 | Our top 5 | Random mat |
|---|---|---|---|
| Mat's main colour = tile's main colour | 20% | **47%** | 19% |
| Share of the mat in the tile's main colour | 18% | **41%** | 18% |

- Her tonal rate is the same as a random mat's. She doesn't seek the main colour; our ranking does, about 2.5x too often.
- In the 10 focus albums it's 14% (hers) vs 52% (ours).
- **Amara** (pink and kelly green): our top 5 are all pink-dominant mats (Cocktail Club 96% pink, Charming Blooms 96% pink, Pink Amahj). Her top 5 are Chinoiserie Songbird (pink + green), Asian Chinoiserie (orange/blue/green), Palm Springs, Lorelei and Elysium.

### 2. She leads with the tile's ACCENT colour (layer or face), not the back
- "Mat carries a tile accent colour but not the main colour": **34%** of her top 5 vs 25% of ours. In the 10 focus albums it's **40% vs 8%**.
- **Malachite** (pink back, green layers, a blue tint): all of her top 4 lead with green or blue (Heaven Scent blue/green, Petalwood blue, Legacy green, Darjeeling blue/green) and carry no pink. Our top 3 lead with pink or red (Revelry, Revelry Leatherette, Crimson Harvest).
- **Jade** (green back, pink and lavender faces): her top picks are Pink Winds (lavender/blue) and Sparrow's Nest (lavender/pink/yellow with a touch of green). Our top 3 are green-on-green: Oasis (green/teal), Southern Stained Glass and Emerald Leopard.
- **Papaya** (orange back, lime and lavender layers): Heiress (blush, tan, coral) and Greenly (blue/yellow/green) are accent-led. Our top 5 contain no lavender or lime lead at all.
- The 2-colour coordination she describes ("pink + green working for them") reads in the data as: **the mat's lead colour is a tile accent, and the tile's main colour shows up only as a supporting colour or not at all.**

### 3. Multi-colour mats, less neutral ground
- Her top 5 average **2.6 colour families** per mat vs 2.07 for ours, with **13%** neutral ground vs 19%.
- Our ranking prefers near-solid single-colour mats, because palette distance is easiest to minimise with one colour.

### 4. Some light/dark contrast
- The average lightness gap between tile and mat is **0.16** for her picks vs 0.11 for ours (0–1 scale).
- She wants the tiles to pop off the mat. Our distance score rewards matching value, which is part of why it reads flat and tonal.

### 5. "Workhorse" mats carry her top slots
- Just **8 mats fill 37%** of all her top-5 slots: Jade 13x, The Kerry 11x, Lorelei 9x, Elysium 9x, Heron 8x, Isla 8x, Vivara 7x and Astor 7x.
- Our colour rank puts them at a median position of **190–300** for those same sets.
- They are layered, multi-colour mats, mostly blue/teal/green with a pink or yellow note (her "dark, layered analogous" section in the Versatile Mats article, ANSWERS Oct 25). They coordinate with almost any set's accents.

### 6. Pair and same-brand mats
- Same-brand mats make up 70% of her top 5 in OMM albums but only 20% in non-OMM albums.
  - The OMM figure is mostly the workhorse mats above (an OMM line, used across sets), not the named pair.
- True "designed-for" pairs sit below her real #1. Vivienne for Papaya is #6 (Heiress is #1); the Sunday mat for Sunday is #4. This matches PICKING-RULES: the pair sits high out of respect but isn't her true top pick.

## Where the naive ranking goes wrong (summary)
- It minimises colour distance, so it lands on **same-hue, same-value, single-colour** mats: the tonal pick. 47% of our top 5 are tonal.
- It weighs the tile back most heavily, so it **misses the layer and face accents** she actually matches to (Malachite, Jade).
- It has **no memory of proven coordinators**: the 8 workhorse mats are buried at rank ~200+.
- Mat measurements are coarse.
  - Pink Winds measures lavender/blue.
  - Heiress measures 63% brown/tan, from its tan scallop ground.
  - So family logic needs a by-eye check before any public pick (PICKING-RULES: "check by eye").

## Proposed scoring tweak (not applied; for the blind test first)
Starting from today's `cr` score (lower = better), add:

| Term | Adjustment |
|---|---|
| Accent-led (mat has a tile accent family ≥10% and the tile's main family < 10%) | −40 |
| Main + accent both on the mat (the 2-colour set) | −20 |
| Single-family tonal (mat main = tile main and only 1 shared family) | **+40** |
| Each mat colour family (up to 4) | −10 |
| Each 0.1 of lightness gap between tile and mat | −5 |
| Each 0.1 of mat share in the tile's main colour | **+5** |
| Workhorse prior: each time the mat is in her top 15 of OTHER albums (cap 6) | −60 |
| Same-brand pair mat (fym-coordinated.json, or same brand + same collection name), "Tiffany's top pick" content only | Skip it. Keep it in the album/FYM order. |

Back-test on the 39 albums (each album's workhorse count leaves that album out):

| | Her top 5 in our top 20 | Median position of her picks | In our top 50 | Our top 5 tonal |
|---|---|---|---|---|
| Today | 0.28 / 5 | 196 | 16% | 47% |
| Colour terms only | 0.44 / 5 | 197 | 19% | **3%** |
| Colour + workhorse | **2.2 / 5** | **23** | **70%** | 16% |

- Holding out every other album: today 0.21/5 in our top 20, median 211 and 12% in our top 50; with the full tweak 1.84/5, median 29 and 67% in our top 50.
- The colour terms alone kill the tonal habit but barely move recall. The workhorse prior does most of the recall work.
- **Caution:** the workhorse prior favours OMM mats (more "obvious" picks) and would repeat the same 8 mats everywhere.
  - Use it to build the **swipe book / shortlist**.
  - Use the colour terms (accent-led, anti-tonal, multi-colour, contrast) to choose the **"top pick" / wow** card.
  - Prefer a cross-brand mat for that card.

## Blind-test protocol (next album, e.g. Brownstone Bloom, Petalée or Vivienne when ordered)
1. **Before** her order exists, Claude writes its top 5 to `docs/research/blind-tests/<set>.json` (committed, timestamped).
   - Each pick carries a one-line reason: which tile accent it leads with, and the 2-colour pair it makes.
   - Use the tweak above, then a by-eye contact-sheet check: tile pile next to each mat, small sheet only.
   - Rules: max 1 workhorse mat, max 1 same-brand mat, 0 single-family tonal.
2. After she orders the album, score it.
   - **Overlap@5:** how many of our 5 are in her top 5.
   - **Hit@15:** how many are in her top 15.
   - Median position of our 5 in her order.
   - Whether our #1 is in her top 5.
3. Log one line per album in this doc (date, set, overlap@5, hit@15, notes on misses).
4. Show her Claude's picks only once overlap@5 ≥ 2 and hit@15 ≥ 4 on two albums in a row (PICKING-RULES: "only show her picks once the score is good").

## Blind-test log
| Date | Set | Overlap@5 | Hit@15 | Notes |
|---|---|---|---|---|
| (none yet) | | | | |
