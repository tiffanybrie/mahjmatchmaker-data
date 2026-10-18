# Bamboo-background cards: re-rendered Oct 18

**Why:** Mahj & Moon mat photos sat on a bamboo background, which read as part of the mat on cards. The cut-out mats are in `assets/mats/clean/bamboo-cut/`.

## Osler (live): ready to swap, 4 cards
- **New cards:** `assets/cards/bamboo-v1/` @ c607e6e, all warmed (200).
- **Cards:** Blue Floral Bird, Blue Heritage Toile, Blue Koi Chinoiserie, Equestrian.
- **Swap list:** `osler.json`. For each card it gives the exact old `<img src>` → new src, and the old "Rack matches" caption div → new caption. Apply both inside the same figure of the Osler code block.
- **Tile racks** now follow her approved Osler list (config/tile-racks-picks.json): Bam Bird Walnut, M&M Hawksbill Heritage Tortoise, B&B Wine. Tigre Oxblood Scallop has no product photo, so it's left off the card and the caption, as on the Larkspur cards.
- **Mat racks** keep the B&B picks printed on the old cards. The new caption reads "Match the tiles: … / Match the mat: …".
- **Rebuild:** `scripts/albumcard/specs/bamboo_oct18/build.py`, then gen2.py. The swap list comes from `build_swaps.py <pin> <live osler html>`.

## Solara: no change needed
Solara + Vintage Floral Gingham and Solara + Grand Garden are her original Squarespace-hosted cards. They're cropped tight into the mat, so no bamboo shows. Left as is (her originals are not re-rendered).

## Petalée (not live)
4 cards re-rendered in place in `assets/cards/petalee/` with the clean mats: Seashell American, Blue Pastel Palm Beach, Pastel Tie Dye American, Pastel Palm Beach. Not staged anywhere live.
