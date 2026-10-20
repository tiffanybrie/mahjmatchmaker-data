# Brownstone Bloom (Anders Ruff) album, staged Oct 20 (NOT live)

**Source:** Ready to Ship `c5-brownstone` (Oct 18, 12:20pm). It saved her order of 41 (cover + 40 mats) with the note "Check resolution of all cards, some are not great. Missing AR logo and missing racks for both tiles and mat". Also `l-final-brownstone` (same time), which cancelled 9 mats.

## Her notes, applied
- **9 cancels:** Jardín de los Jefes, Sedona, Fall Fling, Saddles & Silk, Handbook Plaid, Nantucket Basket, Nantucket Rope, Harvest Plaid, Midnight Garden. That leaves **31 cards in her saved order.**
- **AR logo:** the tile-brand flag is now the Anders Ruff logo (`assets/brand/partner-logos/ar.png`).
- **Resolution, checked card by card** (`crop_px` in the manifest = how many source pixels fill the 1080px mat area):
  - **Brand hi-res photo, same shot but larger** (from the brand's Shopify page, matched by image comparison): Dapper, Vanderbilt, Hawthorne, Marigold, Radiance.
  - **EDSR x4 super-resolution** (the brand's largest photo is only 745px): Brownstone Bloom (her #1), Burgundy Grove, Moss Grove, Autumn Bloom, Chinoiserie Round (624px).
  - **No more upscaled zoom-ins:** photos too small for the 72% lower-left close-up now show the whole mat (Rattan, The Hunt Club, YOTD White/Black/Periwinkle, Scarlett, Tova, Flourish, Palomino, Regency Scalloped, Cognac, Hydrangea). Every card now has at least 900 source pixels.
- **Racks (PROPOSAL, waiting on her OK; triage B21 "Brownstone tile and mat rack picks").** Brownstone Bloom has no approved tile-rack list.
  - **Match the tiles:** PLM Oak + the face colors: B&B Lilac (butterflies), B&B Moss (olive leaves and the E), B&B Wine (protea and berries).
  - **Match the mat:** her saved registry pick where the mat has one, otherwise `matpick.py`, which never uses B&B woods. A few auto-picks need her eye: Dapper (Blackboard Black + Graphite), Marigold (True Black), Mocha Bloom Light (True Black + White).
  - **Rule to check:** the 4 Mahjong Row mats (Autumn Saffron, Mocha Bloom Light, Marigold, Ivy Reverie) should get Mahjong Row racks under MATCH THE MAT *only if* the Brownstone Bloom tiles fit 18.5" racks. Brownstone Bloom tile size is not in our data, so they have B&B/PLM picks for now.
- **Link fix:** the Oct 18 staged block linked Mocha Bloom **Light** to the Mocha Bloom **Dark** product. It now links `mocha-bloom-light-mat`.

## What's staged
- **Cards:** `assets/cards/brownstone-bloom-oct20/` (31 + manifest), commit `d00eae0`. Build: `scripts/albumcard/oct20/brownstone_build.py` then `gen2.py`, using hi-res photos from `hd_fetch.py`.
- **Full album code block:** `brownstone-bloom-codeblock.html`. It has the same structure, CSS and lightbox as the staged Papaya block. It contains:
  - the hero (cover `00-brownstone-bloom-mahjong-tiles-cover.jpg`, unchanged), and the FAQ plus JSON-LD with her top 3: Brownstone Bloom, Autumn Saffron, Mocha Bloom Light;
  - "31 mat matches from 11 brands";
  - 31 `mm3-c` figures, with Match the tiles / Match the mat captions and every shop link and brand page filled. Images are pinned to `@d00eae00022c8319849d96ebf1966e74e7bbe5f2`.
  - Built by `scripts/albumcard/oct20/brownstone_block.py <sha>`.
- **jsDelivr warmed:** 40 of 40 URLs returned 200 (`../warm_result_owed_oct20.json`, which also covers Malachite).

## Still owed (not in this build)
- **"One more round of missing mats" (her l-final-brownstone note):** she thinks Amanda Toppe's full catalog wasn't in the swipe book, plus other mats added to the catalog since. That needs a new swipe round built from the partner catalogs. It is not done here.
- **Color card** for Brownstone Bloom (doc 86/96: every album gets one). There isn't one yet.

## Live step (only after her Yes on the cards and racks)
1. Duplicate a live album page (e.g. Jade), then set its title, slug and SEO with GetCollectionSettings / SaveCollectionSettings (doc 59 §4):
   - **Title:** Brownstone Bloom Mahjong Tile Matches
   - **Slug:** brownstone-bloom-mahjong-tile-matches
   - **SEO title:** Brownstone Bloom Mahjong Tile Matches: Mats & Racks for Anders Ruff Brownstone Bloom
   - **SEO description:** Anders Ruff Brownstone Bloom tiles matched to 31 mats, with rack picks and shop links. Top picks first. Save with code MAHJMATCH.
2. Replace the duplicated code block with `brownstone-bloom-codeblock.html`, fetched from jsDelivr at this README's commit.
3. Verify with curl: 31 `mm3-c` figures, the h1, and the cover loading. Then add the album cover to /mahjong-tile-matches, the home page and its color page, using the same pattern as Papaya (`site/livepatch/papaya/README.md`).
