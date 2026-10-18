# FYM fix 3 (Oct 18 afternoon): mat + tile image quality pass, mat-image rules, wrong-image fixes

Applied on top of the pending fix-2 build in scratchpad `fymfix2/build/` (still waiting on Tiffany's publish OK).
`builder/fym_mated_oct18/patch.py` was re-run afterwards (Vivienne / Larkspur / Peony & Parasol mat-door matches kept).

## Pipeline (scratchpad fymfix2/f3/)
1. `refetch1.py`: product JSON image lists for every visible mat + tile set (990 of 1180 found).
2. `refetch2.py` / `proc.py`: find the store photo that IS the current picture (also inside listing graphics), fetch it full size, crop out solid panels, trim to the mat, re-encode. `overrides.json` = hand-picked images, `forcecur.json` = keep current (store photo was a different picture).
3. `bamboo_all.py` (+ `bamboo.py`): cut Mahj & Moon / Mahj Mood mats out of the bamboo surface (81 mats). Clean copies in `assets/mats/clean/bamboo-cut/`.
4. `ocr.py`: text/watermark scan; flagged items checked by eye.
5. `fix3.py`: writes the build (mats stored 1200px webp q85 in mc chunks; changed thumbnails in b14v1.js; catalog tiles in t15/).

## Publish file list (on top of the fix-2 list)
index.html, b13v1.js, b14v1.js, mc/*.json (77 chunks rewritten, ~177MB total; publish in several batches to the same url), t14/0.jpg, t15/* (217 files, ~44MB).
Version budget: 511 files / 256MB per version, 64MB per publish.

## What changed
- 888 visible mats re-stored, trimmed to the mat edges. Under 800px on the short side: 832 before, 303 after (brand-store max for most of those; see low.json). Britt Mills: median 433px → 1400px (cropped out of their 3600px listing graphics).
- 217 catalog tile photos re-fetched full size; 3 wrong tile photos replaced (Country Club, 90s Pool Party, Park Series).
- Wrong images: Chinoiserie Songbird now the full Mahj & Vine mat (was a cropped half); Goldie = goldie-color-corrected; OMM Spring Fling = her photo; 19 retired OMM mats locked to assets/mats/omm-retired/.
- Colorway remaps: Coquette + Bandana → Blue/Pink; PLM Hanukkah cards → Frosted Flowers; Glow Wild + Caroline → Caroline in Peacock (new entry).
- Tubes removed (mirrored clean half): Chinoiserie Elephant, Chinoiserie Blue and Green, Caroline in Peacock. Limoncea: brand flat photo. Petalwing: "Mat only" caption cut.
- No-text rule → placeholder (on her cards): Sweet Dreams, Chinoiserie Round (Mac + Miller watermark), Imperial Lotus (Tile Haus watermark), Painted Water Florentine (racks/tiles in every photo), Bow & Bloom (logo graphic), Origami Berry (retired colorway). Hidden (not hers): 6 other Mac + Miller mats, FWS Bow & Bloom.
- Retired flags: OMM Liberty, OMM Holly Jolly.
- Glitter Glow (Bespoke teaser, no design released) removed from FYM and the color tags.
- Checked at 390 and 1280: no sideways scroll, no broken images, mat door finds Knox (4 of her sets), Chinoiserie Songbird (7), Goldie (13), Caroline in Peacock (1), Savannah Leatherette (2); Papaya Spritz still leads with Greenly.

## Live cards that use bamboo-background Mahj & Moon mats (need re-render, not done here)
Osler + Blue Koi Chinoiserie, Osler + Blue Heritage Toile, Osler + Blue Floral Bird, Osler + Equestrian, Solara + Vintage Floral Gingham, Solara + Grand Garden,
Petalée + Seashell American, Petalée + Blue Pastel Palm Beach, Petalée + Pastel Tie Dye American, Petalée + Pastel Palm Beach.
(Papaya Spritz's three were already re-done in b3f23e5.)
