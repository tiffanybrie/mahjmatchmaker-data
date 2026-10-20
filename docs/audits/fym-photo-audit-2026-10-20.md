# Find Your Mat-ch: mat photo audit (Oct 20)

**Images audited:** the image the live build actually shows for each mat. For each mat, the `f` field in `index.html` (`m/N.webp`) was resolved through the live artifact's published `mc/` chunks (N//12; packed .webp chunks plus legacy .json chunks). All 677 resolved, so no raw-feed fallback was needed.

**Scope:** `catalog/fym_live_keys.json` has 825 keys. 677 of them are mats (in `D.mats`) and the other 148 are racks, which were skipped.

**Mats audited:** 677. **Fails:** 14. **Borderline:** 32 mats in 14 groups.

Each one was judged by eye on contact sheets (`sheet_00..14.jpg`, 48 per sheet), and borderline ones were re-checked larger (`cand_a.jpg`, `cand_b.jpg`). The fails are on `fails.jpg`.

Note: the example from the brief, Splash of Color "Peony-Powered Prosperity Pad", is not in the current live key list, so it looks like it's already been removed.

## FAILS

| # | Brand | Mat | Reason | Key | Product URL |
|---|---|---|---|---|---|
| 116 | Let's Be Besties | Sky Blue Florals | tiny/cropped - thin wide strip in a big empty frame; can't read it as a mat | `letsbebesties.com/sky-blue-florals-mahjong-mat` | https://letsbebesties.com/products/sky-blue-florals-mahjong-mat |
| 257 | Mahj Mood | Spring Fling Mat | angled - steep perspective shot on a table, mat cropped off the frame | `mahjmood.com/spring-fling-mat` | https://mahjmood.com/products/spring-fling-mat |
| 258 | Mahj Mood | The Bow and Bloom Mat: Collab with Four Winds Social \| Pre-Order, Ships End of September | graphic - 'Photo coming soon' placeholder card | `mahjmood.com/the-bow-and-bloom-mat-collab-with-four-winds-social-pre-order-estimated` | https://mahjmood.com/products/the-bow-and-bloom-mat-collab-with-four-winds-social-pre-order-estimated |
| 353 | Maison Mahj | The Signature House | covered - book box, card box, rack and tiles cover much of the mat | `maisonmahj.com/the-paris-mat-la-vie-en-mahj-edition` | https://maisonmahj.com/products/the-paris-mat-la-vie-en-mahj-edition |
| 355 | Miss Mahjong | After Party Mahjong Playing Mat | angled - steep cropped corner, no mat edges; reads as a print, not a mat | `missmahjong.com/after-party-mahjong-playing-mat` | https://missmahjong.com/products/after-party-mahjong-playing-mat |
| 451 | Splash of Color | Modern Nordic Scandinavian Folk Art Mahjong Mat Sleek Surface | table scene - mat on a table in a dining room (same problem as Peony-Powered Prosperity Pad) | `splashofcolorco.com/modern-nordic-scandinavian-folk-art-mahjong-mat-sleek-surface` | https://splashofcolorco.com/products/modern-nordic-scandinavian-folk-art-mahjong-mat-sleek-surface |
| 497 | Bam Bird Boutique | Origami Berry | graphic - 'Photo coming soon' placeholder card | `www.bambirdboutique.com/origami-neoprene-mat` | https://www.bambirdboutique.com/products/origami-neoprene-mat |
| 515 | Bespoke Mahjong | Bespoke X Gray Malin DOUBLE-SIDED MAT \| Double the Fun/Gray Malin Getaway Dogs Mat | graphic/can't tell - full-bleed ski-lift dog photo, no mat edges visible | `www.bespokemahjong.com/bespoke-x-gray-malin-double-sided-mat-double-the-fun-gray-malin-beach-club-mat-copy` | https://www.bespokemahjong.com/products/bespoke-x-gray-malin-double-sided-mat-double-the-fun-gray-malin-beach-club-mat-copy |
| 537 | Bespoke Mahjong | Gray Malin | angled - steep close-up of one corner with a few tiles; mostly blank teal | `www.bespokemahjong.com/graymalingamemat` | https://www.bespokemahjong.com/products/graymalingamemat |
| 543 | Bespoke Mahjong | GARDEN GLOW MAT - TURQUOISE | covered - gameplay scene: tiles, rack and cards across the mat | `www.bespokemahjong.com/preorder-garden-glow-mat-turquoise` | https://www.bespokemahjong.com/products/preorder-garden-glow-mat-turquoise |
| 588 | Mac + Miller Mahjong | Heirloom Collection: Chinoiserie Round Mahjong Mat | graphic - 'Photo coming soon' placeholder card | `www.macandmillermahjong.com/heirloom-collection-white-chinoiserie-round-mahjong-mat` | https://www.macandmillermahjong.com/products/heirloom-collection-white-chinoiserie-round-mahjong-mat |
| 594 | Mac + Miller Mahjong | Sweet Dreams | graphic - 'Photo coming soon' placeholder card | `www.macandmillermahjong.com/sweet-dreams-collection-mahjong-mat` | https://www.macandmillermahjong.com/products/sweet-dreams-collection-mahjong-mat |
| 595 | Mahjong Moxie | Bamboo Garden | table scene - mat draped on a table in a room, angled, chairs/floor showing | `www.mahjong-moxie.com/bamboo-garden-mat` | https://www.mahjong-moxie.com/products/bamboo-garden-mat |
| 608 | Middle & Main Mahjong | Painted Water Florentine Mat | graphic - 'Photo coming soon' placeholder card | `www.middleandmainmahjong.com/painted-water-mat` | https://www.middleandmainmahjong.com/products/painted-water-mat |

Summary by reason: 5 graphic placeholders ('Photo coming soon': 258, 497, 588, 594, 608), 1 full-bleed photo with no mat edges (515), 2 table/room scenes (451, 595), 3 steep angles (257, 355, 537), 2 covered (353, 543), 1 tiny/cropped (116).

## BORDERLINE (pass the test, but weaker photos; Tiffany's call)

- #0, #1, #2, #3, #4, #5: Amahj (all 6): perspective/angled renders. Colors clear, mat obvious. Mild angle only
- #65: Charleston Brown Vegan Leather: slight angle and crop. Color clear
- #70, #77: Four Winds Social Beyond the Ribbon / Preppy Poinsettia: text banner bleeding in at the top (cropped from a graphic). Mat visible
- #98: Let's Be Besties Forest Haze: reads like a watercolor painting more than a mat. Colors clear
- #106, #109, #124: Let's Be Besties Tobacco Leaves / Paint Feathers / Tobacco Leaves Blue: mat lying on a wood floor, slight angle. 109 is smallest in frame
- #202: Mahj & Moon Pink & Green Floral: tiles and a rack sit on the center. Pattern still readable
- #326, #331: Mahj Squad Blue Chinoiserie / Monet's Reflections: tilted perspective renders. 331 is the more extreme
- #345, #346: Maison Mahj Espresso City / Olive City: pile of tiles over the center. The plain brown/green ground is still clear
- #352: Maison Mahj Mayfair Stripe: book box prop in the middle. Stripes clear
- #356, #359, #363, #368, #369, #370, #371, #372: Miss Mahjong (Canopy Palm, Gingham Cornflower, Gingham, Oasis, Papel Picado, Toile de los Muertos, Wild West x2): angled corner crops, the brand's house style. Colors readable, but the whole mat isn't shown
- #471: Royal Mahjong Society Cottage: angled close crop of one corner
- #483: Tigre de Tartan Nantucket Basket Round: angled photo of a round mat. Color clear
- #600: Mahjong Moxie Oyster Confetti: several mats stacked/offset, edges look messy
- #447, #635: Splash of Color Asian Chinoiserie (racks and blurry backdrop) / Oh My Mahjong Preppy Soiree (cards, tiles, acrylic on one side): OK but busy

## Files
- Per-mat live images: `full/NNN.jpg` (NNN = audit index). Index-to-key map: `rows.json`
- Contact sheets: `sheet_00.jpg` .. `sheet_14.jpg`; larger borderline checks: `cand_a.jpg`, `cand_b.jpg`; fails only: `fails.jpg`
