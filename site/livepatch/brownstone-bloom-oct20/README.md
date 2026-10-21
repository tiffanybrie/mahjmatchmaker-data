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

## Oct 21 update: everything owed is built (still NOT live)
Tiffany, Oct 21 1:00pm: "we haven't even released Brownstone Bloom from Anders Ruff... we got to get ahead of this."
- **Color card** (doc 86): `assets/colorcards/brownstone-bloom/` (desktop Tile Edit + phone guide), spec `config/colorcards.json` → `brownstone-bloom`. Classic Tile Edit labels (no gender set for this set). Colours measured from the album pile + AR's NEWS close-up: Ivory #eee3cf, Lavender butterfly back #ae9ca9, Wine #5b3838, Olive #5c512a, Dusty Rose #bb7c71. Gate [14] photo identity: OK on both.
- **Canonical album photo:** `assets/tiles/album/brownstone-bloom.jpg` (= the colour-corrected pile; index.json entry). The CARD-ONLY E-tile edit stays inside card tile boxes only.
- **Missing mats round 2:** `review/missing-mats-round2.json` (15 candidates + what was checked and left out). Pool = visible FYM partner/allowed mats not in the Oct 18 swipe book (123 mats) + Amanda Toppe's 9 full-size mats (none were in the book).
- **Racks:** AR lists the tile at 0.98" W, so 19 tiles = 18.6" > Mahjong Row's 18.5" racks. The 4 Mahjong Row mats keep their B&B/PLM picks. Option offered: Mahjong Row Scalloped Tortoise (20") as a 5th tile rack.
- **Codes:** AR's page says the tile set takes no promo codes (Indigo Pruitt special edition). Code MAHJMATCH goes on mats/racks only.
- **Review:** Ready to Ship item `l-brownstone-v2` (contact sheet `review/brownstone-31-cards-contact-sheet.jpg`, colour cards, 15 ♥/✕ taps saved to ship doc `picks`, choice `now` | `wait` saved as `choice` with v=ok). HQ need `brownstone-shortlist` reopened as the Today item, held (`status: parked`, `qaHold: true`) until independent QA passes; then set it open and add `l-brownstone-v2` to RTS `NOW`.
- Her ♥ mats need cards built with `scripts/albumcard/oct20/brownstone_build.py` (append after #31 unless she reorders) + `brownstone_block.py <sha>`, then warm jsDelivr.

## Oct 21 3:30pm: independent QA fixes (released to her)
- **Code band:** the 6 Britt Mills cards (4 Scarlett, 6 Walk in the Park, 12 Flourish, 18 Tova, 21 Regency Scalloped, 26 Eden) said "15% OFF"; re-rendered as "10% OFF USE CODE : MAHJMATCH" (10% floor rule). Only the band changed (pixel diff). Contact sheet updated in place.
- **Code block:** rebuilt with `brownstone_block.py 0f8738b3fd161c23cfa8a705e06e87e4fd25efe6` (identical to the previous block except the pinned SHA); 31/31 card URLs warmed (200). The script now falls back to the previous block's shop links when the scratch `staged_urls.json` is gone.
- **Round-2 candidates (13 now):** Britt Mills promo graphics replaced with clean mat shots from brittmillsdesign.com (Novella image 8, Knox image 7, Regal Bloom + Legacy listing renders cropped to the mat, no text). Rose Wreath room shot replaced with Splash of Color's flat shot (product image 2, bag cropped out). Dropped: Glory (patriotic palette), Mocha Kaleidoscope (real product shot is black/white/grey, not mocha).
- **Color card pill:** desktop now matches mobile, "Code MAHJMATCH on partner mats & racks" (build.py shrinks long pill text to fit).
