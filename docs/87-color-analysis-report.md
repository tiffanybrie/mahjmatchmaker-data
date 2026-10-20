# 87 Color Analysis Report: measured mat colors vs tags (Oct 19)
Report only. **No tags were changed.** config/mat-color-guesses.json, Find Your Match and the live site are untouched.
Data:
- `config/mat-color-measured.json` (per mat: top clusters + family areas)
- `config/tile-color-measured.json` (tile sets)
- Contact sheet: `assets/social/color-audit-flags.jpg`
- Script: `scripts/color/measure.py`

## Method
- Each of the **889** gallery mat photos is shrunk to 160px.
- The flat product-shot border is detected and removed, along with near-white and near-black pixels.
- Every remaining pixel is put in one of our families (pink, red, orange, yellow, gold, green, teal, blue, purple, brown, neutral, bw, dark) by hue, chroma and lightness, in Lab color space.
- k-means (6) gives the top colors with hex, hue, saturation, lightness and % area.
- The **dominant** family is the largest chromatic family. Cream, grey or black grounds count as the "ground", not the dominant color.
- Flags:
  - (a) the measured dominant isn't tagged, and isn't a neighbor of a tag (pink~red~purple, teal~blue~green, gold~yellow~brown…)
  - (b) the primary tag covers under 5% of the measured area
  - (c) a secondary tag covers under 5%

## Totals
- 889 mats measured. **707 clean** (no flag).
- Flagged: 37 likely-wrong-tag (flag a or b), 138 ambiguous (only a weak secondary), 7 measurement-unreliable (lifestyle photos).
- Flag kinds: 152 weak secondary, 28 dominant not tagged, 17 primary under 5%.
- Weak secondaries by family: pink 43, green 33, blue 26, red 15, teal 14, neutral 11, orange 10. These are mostly small accents in fine patterns, the hardest thing to measure.

## After an eye check of the top 40 (contact sheet)
- **Only about 6 are real tag problems:**
  - Birthday (Hip Hip): pink + light blue, not neutral
  - Strawberry Thief (Mahj & Moon): blue/teal, not green/neutral
  - Pumpkin Patch (Bam Let's Mahjong): add orange
  - Imperial (OMM, retired): add blue
  - Freedom Isn't Free (Hip Hip): add neutral, drop brown
  - Lilac Green Squiggle (Amahj): lilac ground, so purple rather than pink
- **The rest are measurement limits, not tag errors:**
  - Lifestyle photos: wood tables, racks and tile props read orange or brown. That's about 10 of the 40.
  - Olive greens read as gold (Art Deco ×2, Moss Grove).
  - Blush or grey-blue grounds read neutral (LMO Petal, Christmas Village).
  - Brown leather reads red (OMM Cognac).
  - Chartreuse sits on the yellow/green line.
- **Bottom line:** the Claude-look tags are in good shape. Measurement is a strong **cross-check**, not yet a replacement for an eye.

## Top 40 flagged (current tag vs measured)
| # | mat | current tags | measured dominant | grade | eye check |
|---|---|---|---|---|---|
| 1 | oh-my-mahjong--cognac | brown | red 74% | likely-wrong-tag | measurement: brown leather reads red; tag brown is right |
| 2 | tigre-de-tartan--domino-faded-carolina | blue/neutral | orange 25% | likely-wrong-tag | measurement: tortoise rack props in the photo; tag ok |
| 3 | splash-of-color--preppy-animal-print | pink/purple/teal | brown 19% | likely-wrong-tag | measurement: lifestyle room photo; tag plausible |
| 4 | splash-of-color--art-deco-green-and-blue-mahjong-mat-26x26 | green/dark/blue | gold 54% | likely-wrong-tag | measurement: olive green reads as gold; tag ok (could add neutral/olive) |
| 5 | splash-of-color--art-deco-designed-mahjong-mat-green-blue-speakeasy-collection | green/dark/blue | gold 51% | likely-wrong-tag | measurement: olive reads gold; tag ok |
| 6 | hip-hip-mahjong--freedom-isn-t-free-mahjong-mat | green/blue/brown | orange 14% | likely-wrong-tag | REAL: mostly grey camo + navy; tag should include neutral, brown is weak |
| 7 | let-s-be-besties--butterscotch-birdie-mahj-game | blue/pink/gold | pink 6% | likely-wrong-tag | measurement: pastels wash out; tag ok |
| 8 | let-s-mahj-on--lmo-floral-border-mat-petal | pink/blue | orange 7% | likely-wrong-tag | measurement: blush ground reads neutral/orange; tag ok |
| 9 | wren-mats--christmas-village | blue/pink/red | pink 11% | likely-wrong-tag | measurement: grey-blue ground reads neutral; tag ok |
| 10 | wren-mats--winter-wreaths | green/neutral/gold | neutral 71% | likely-wrong-tag | tag ok (sage + cream) |
| 11 | hip-hip-mahjong--birthday-mahjong-mat | neutral/pink/teal | blue 41% | likely-wrong-tag | REAL: pink + light blue; primary "neutral" is wrong, add blue |
| 12 | anders-ruff--moss-grove-mahjong-mat | green/purple/neutral | gold 50% | likely-wrong-tag | measurement: olive reads gold; tag ok |
| 13 | mahj-squad--the-study-mahjong-mat | green/brown | brown 14% | likely-wrong-tag | tag ok (dark green + tortoise) |
| 14 | mahj-squad--oushak-mahjong-mat | pink/teal/green | teal 24% | likely-wrong-tag | tag ok |
| 15 | let-s-be-besties--the-speakeasy | blue/red/gold | brown 25% | likely-wrong-tag | tag ok (navy + red) |
| 16 | amahj--lilac-green-squiggle-mahjong-game-mat | pink/green/teal | green 20% | likely-wrong-tag | REAL-ish: ground is pale lilac; consider purple instead of pink |
| 17 | mahj-moon--orchard-songbird | pink/green/blue | orange 27% | likely-wrong-tag | tag ok |
| 18 | let-s-be-besties--forest-haze | neutral/blue/dark | orange 27% | likely-wrong-tag | tag ok |
| 19 | britt-mills--soir-e-leatherette | green/pink/blue | orange 26% | likely-wrong-tag | tag ok |
| 20 | maison-mahj--the-checkmate-house | bw/red | green 26% | likely-wrong-tag | tag ok (black/grey + burgundy) |
| 21 | let-s-be-besties--tobacco-leaves-blue | pink/blue/green | brown 20% | likely-wrong-tag | measurement: on a wood table; tag ok |
| 22 | mahj-mood--sleigh-all-day-mat | red/green | brown 25% | likely-wrong-tag | tag ok (red tartan) |
| 23 | mahj-moon--celestial-dragon-chinoiserie | neutral/pink/teal | orange 24% | likely-wrong-tag | tag ok |
| 24 | mahj-moon--strawberry-thief-inspired | green/neutral | blue 24% | likely-wrong-tag | REAL: blue/teal dominant; tagged green/neutral, add blue + teal |
| 25 | hip-hip-mahjong--the-house-mahjong-mat | brown/pink/green | blue 23% | likely-wrong-tag | tag ok (leopard + pink + green) |
| 26 | let-s-be-besties--tobacco-leaves | pink/blue/green | brown 17% | likely-wrong-tag | measurement: on a wood table; tag ok |
| 27 | tigre-de-tartan--cannage-blonde-w-rules | neutral/pink | orange 16% | likely-wrong-tag | measurement: lifestyle props; tag ok |
| 28 | bam-let-s-mahjong--pumpkin-patch-mahjong-mat-fall-halloween-mahjong-mat | pink/green/dark | orange 20% | likely-wrong-tag | REAL: orange pumpkins missing from tags; add orange |
| 29 | tigre-de-tartan--french-mural | dark/neutral | orange 15% | likely-wrong-tag | measurement: lifestyle with racks; tag ok |
| 30 | let-s-be-besties--paint-feathers | pink/green/teal | brown 15% | likely-wrong-tag | measurement: on a wood table; tag ok |
| 31 | britt-mills--enchanted-leatherette | blue/pink/orange | green 18% | likely-wrong-tag | tag ok (navy ground, multi florals) |
| 32 | bespoke-mahjong--year-of-the-dragon-mat-amped-up-grey | neutral/pink/red/blue | green 12% | likely-wrong-tag | tag ok |
| 33 | mahjong-row-co--spring-awakening-p | blue/neutral | orange 16% | likely-wrong-tag | tag ok |
| 34 | oh-my-mahjong--imperial-retired | neutral/yellow/pink | blue 13% | likely-wrong-tag | REAL: mint/light blue reads clearly; add blue |
| 35 | let-s-mahj-on--let-s-mahj-on-floral-mat | pink/blue/green | orange 16% | likely-wrong-tag | tag ok (blush + blue florals) |
| 36 | tigre-de-tartan--paige-spearin-shell-yeah | neutral/teal/pink | orange 5% | likely-wrong-tag | measurement: lifestyle props; tag ok |
| 37 | tigre-de-tartan--plum-peony | dark/neutral/brown | yellow 8% | likely-wrong-tag | tag ok |
| 38 | middle-main-mahjong--grandmother-martha-vintage-quilt | pink/blue/green | pink 10% | ambiguous | measurement: lifestyle, pastel quilt; tag ok |
| 39 | middle-main-mahjong--grandmother-kathryn-vintage-quilt | blue/yellow | blue 15% | ambiguous | measurement: lifestyle, pastel quilt; tag ok |
| 40 | bespoke-mahjong--chartreuse-garden | green/yellow/pink | yellow 62% | ambiguous | measurement: chartreuse sits on the yellow/green line; tag ok |

## Mats per family: tags vs measured
"Primary" = the first tag. "Any tag" = in primary or secondary. "Measured dominant" = largest chromatic family. "Measured present" = family ≥8% of the mat.

| family | primary tag | any tag | measured dominant | measured present |
|---|---|---|---|---|
| pink | 192 | 470 | 221 | 388 |
| red | 36 | 149 | 23 | 92 |
| orange | 24 | 96 | 101 | 205 |
| yellow | 16 | 106 | 21 | 80 |
| gold | 6 | 52 | 7 | 25 |
| green | 140 | 373 | 142 | 309 |
| teal | 64 | 203 | 94 | 224 |
| blue | 185 | 368 | 205 | 363 |
| purple | 49 | 103 | 19 | 52 |
| brown | 39 | 82 | 32 | 71 |
| neutral | 70 | 195 | 18 | 508 |
| bw | 16 | 19 | 1 | 96 |
| dark | 33 | 71 | 5 | 149 |
| multi | 19 | 19 | 0 | 0 |

How to read it:
- **Orange is inflated by measurement** (101 dominant vs 24 tagged), from wood tables, tortoise and peach or blush grounds. Don't trust measured orange yet.
- **Purple is under-measured** (19 vs 49). Lilac and lavender are low-chroma and fall into pink, blue or neutral. Purple is the thinnest family either way. The color wheel draft showed the same gap.
- **Neutral, bw and dark** are present on most mats as grounds (508 have ≥8% neutral). That's correct, but it means "neutral" as a *filter* should use the tag, not the measurement.
- **Over-full:** pink and blue (≈200 primary each). A pink or blue filter returns a lot, so sort by measured % so the truest pinks or blues come first.
- **Thin:** gold (6), yellow (16), orange (24 true), bw (16), purple (49). Real gaps in the catalog, and worth noting for brands.

## Tile sets (assets/tiles/album, white faces masked)
- **Color cards vs measured backs** (ΔE under 10 is close):
  - Shangri-La EMERALD 4.4 and Preppy Soirée SLATE BLUE 4.3: close.
  - Papaya PAPAYA 10.6, LAVENDER 8.8, LIGHT LIME 14.2 (photo slightly duller).
  - Spring Love LIME 28.4: the photo is much duller than the chip.
  - Preppy Soirée PLUM 28.7: no plum found in the photo, since the layer is too thin to measure.
  - Lilac Soirée BLUSH 20.2: measured greyer.
  - Navy chips vary 9–22.
- **Site back-color families vs measured:** most agree. Ones to look at:
  - Solara (site "Yellow & Orange", measured coral red/pink, which matches Tiffany's "don't call her orange")
  - Coquette and Taylor (measured more purple or pink than the site family)
  - Lagoon, Birdie and Seabreeze (site "Blue", measured teal, a blue/teal naming choice)
  - Glow Wild, Emerald, Drake and Talulah (dark photos, so the measurement is unreliable)

## Is it good enough to drive the Find Your Match color filter?
**Not on its own yet.**
- Good for: dominant color on flat product shots, ranking within a filter (sort pinks by measured pink %), and catching outliers like the ~6 real fixes above.
- Weak on: lifestyle photos, lilac/lavender, olive, blush grounds, and small accent colors in busy patterns.

Recommended:
1. Keep tags as the filter.
2. Use measured % to **order** results.
3. Fix the 6 real tag errors after Tiffany's yes.
4. Re-measure lifestyle-photo mats from the flat product render when available.
5. Tune hue boundaries (olive→green, cognac→brown, blush→pink) before using it for more.

## FIXED Oct 19 night (Tiffany: "fix the 6 tags")
Updated in config/mat-color-guesses.json (old values kept under `prev`) and in Find Your Match (v59, mat filter families):
- Birthday (Hip Hip): pink + blue (neutral dropped)
- Strawberry Thief (Mahj & Moon): blue/teal (was green/neutral)
- Pumpkin Patch (Bam Let's Mahjong): orange added as primary
- Imperial (OMM, retired): blue added
- Freedom Isn't Free (Hip Hip): neutral + blue + green (brown dropped)
- Lilac Green Squiggle (Amahj): purple instead of pink
