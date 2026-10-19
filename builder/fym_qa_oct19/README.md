# Find Your Match overnight QA (Oct 19)

**What was tested:** the exact published file set (version 1792354776-29f5, 393 files), served locally. Built from scratchpad/fymfix2/build plus the older unchanged files; sizes were checked against the artifact's file list.

## Flows run (390 and 1280)
- **Tile door → mats → racks → card,** all 3 views (Love triangle, Mood board, Shop): Papaya Spritz, Sunday, Coquette, Lagoon, Amara, Sierra, Drake, Heritage 2.0.
- **Mat door → tile set → racks → card:** Vivienne (33 sets, 15 hers), Goldie (31, 13), Larkspur (44, 28), Greenly (21, 3).
- **Results:** every flow completed and every view rendered a card. No sideways scroll and no broken images. All 34 shop links from the flows return 200. One stray 404 console line on the first Papaya load could not be reproduced.

## Bugs found
1. **Card subtitle said "tiles on the The Polo Club mat"** for mats whose name starts with "The". FIXED in source: `builder/card_build_oct18/card.js`, plus the staged build `scratchpad/fymfix2/build/index.html`. **Not published.**
2. **Greenly (Mahj & Vine), the #1 Papaya Spritz match, loads at 480px.** The brand's only photo is 4000px but has the tube overlapping the mat, so an automatic crop doesn't work. It needs a hand clean-up (or a flat photo from Mahj & Vine). Not fixed.
3. **Greenly door:** Sunshine (Middle & Main) shows a Tiffany's-match heart. Confirm that's really her pick (the Vivienne/Larkspur doors had a wrong Sunshine heart removed Oct 18).

## To publish the fix
Re-splice and patch (`builder/card_build_oct18/splice.py`, `builder/fym_mated_oct18/patch.py`), then run `builder/fym_publish_oct18/pack_bin.py BUILD_DIR` before publishing, or the version goes over the 256MB budget. Only index.html changes for this fix.
