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

## Oct 24 revision (her RTS note Oct 23 ~10:46pm + chat 2:56am)
- Tile racks: Anders Ruff Tortoise + Bam Bird Boutique Olive + Bird & Bamboo Wine (config/tile-racks-picks.json final_lists brownstone-bloom). Brownstone Bloom mat racks: AR Tortoise + PLM Acrylic Burl (config/mat-racks-picks.json).
- Order: Scarlett #2, Autumn Saffron #4; her 9 round-2 hearts appended (#32-40).
- Cards: assets/cards/brownstone-bloom-oct24/ (40 + manifest), commit bdd6934, built by scripts/albumcard/oct20/brownstone_oct24.py + gen2.py. Oct 20 sources were gone, so mats were re-sourced (brand Shopify image matched to the FYM photo, else the FYM photo) and photos under 900px EDSR x4 (opencv dnn_superres). Chinoiserie Round: every brand image carries a "(c) 2026 Mac and Miller" watermark, so the card uses a watermark-free top-left crop.
- Her ordering page: artifact WNjXTGjxfdqoa1tzUiYgQ4 (db doc review/order {order, left_out, savedAt}). HQ need brownstone-shortlist points there.
- NEXT on her Save: rename files in her order, brownstone_block.py at the new commit, warm jsDelivr, then the live step above.

## Oct 31 night: REBUILT + PINNED, ready to paste (supersedes the Oct 20/21 pins above)
Tiffany Oct 29 8:04am (HQ answer): remove B&B Wine; swap the Anders Ruff tortoise (messy mock-up) for the best tortoise; order is good.
- **Cards:** `assets/cards/brownstone-bloom-oct31/` (40 + manifest), commit `b63ce533a067002730a27790f012ace4a83ac3e2`. Tile racks on every card = Middle & Main Hawksbill Heritage Tortoise + Bam Bird Boutique Olive (no B&B Wine, no AR Tortoise). Brownstone Bloom mat's mat racks = M&M Hawksbill + PLM Acrylic Burl. Order = her Oct 24 order (order page never re-saved; "order is good"). Long title shortened on the card only: #40 reads "Brownstone Bloom + Midnight Wildflowers".
- **Photos:** Oct 24 sources were gone again. Each mat re-sourced and matched to its approved Oct 24 card by image correlation in the card's un-overlaid window (same shot + framing; corr 0.86-1.0): brand Shopify image, else repo gallery photo (assets/mats/gallery), else round-2 candidate. Crops under 750px EDSR x4 (tiled). Build: `scripts/albumcard/oct20/brownstone_oct31.py <work> <srcdir>` then `gen2.py`. Contact sheet (all 40, looked at card by card): `review/brownstone-40-cards-oct31-contact-sheet.jpg`.
- **Colour card** rebuilt with the new racks + "40 mat matches" (`assets/colorcards/brownstone-bloom/`, config/colorcards.json) and placed FIRST in the block (Colors & racks section before the matches).
- **Code block:** `brownstone_block.py b63ce533a067002730a27790f012ace4a83ac3e2` → `brownstone-bloom-codeblock.html`, 40 `mm3-c` figures, "40 Brownstone Bloom mat matches from 14 brands", top 3 = Brownstone Bloom, Scarlett, Mocha Bloom Light (FAQ + JSON-LD). TdT card: "save 10% with my link" + auto-apply link (tdt_policy).
- **PIN (paste this):** https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@b57c01d19ab5cfee43a571897a0c6e23db5ae3c3/site/livepatch/brownstone-bloom-oct20/brownstone-bloom-codeblock.html
- **Warmed:** 45/45 URLs 200 (block + 40 cards + colour card x2 + hero cover + w800 cover): `warm_result_oct31.json`.
- **Flag (not blocking):** OMM no longer sells Dapper (#8), Vanderbilt (#22), Cognac (#28): product pages 404 and not in ohmymahjong.com/products.json (Oct 31 night). Their cards stay in her order with NO Shop button (no dead links). Her keep/drop call is in MATCH-INBOX; dropping = remove the 3 figures + renumber.

### Ops paste steps (Chrome; one driver)
1. New page per "Live step" above (duplicate a live album page, e.g. Jade): Title "Brownstone Bloom Mahjong Tile Matches", slug `brownstone-bloom-mahjong-tile-matches`, SEO title "Brownstone Bloom Mahjong Tile Matches: Mats & Racks for Anders Ruff Brownstone Bloom", SEO description "Anders Ruff Brownstone Bloom tiles matched to 40 mats, with rack picks and shop links. Top picks first. Save with code MAHJMATCH." Replace the code block with the PIN above (diff before save). Publish.
2. Curl the live page: 200, 40 `mm3-c`, h1, `mm3-guides` present, cover loads.
3. **/mahjong-tile-matches** (newest first) **and the home page** album grid: add at the top
   `<a class="mmalb-c" href="/brownstone-bloom-mahjong-tile-matches"><img src="https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@b57c01d19ab5cfee43a571897a0c6e23db5ae3c3/assets/covers/albums/w800/00-brownstone-bloom-mahjong-tiles-cover.jpg" alt="Anders Ruff Brownstone Bloom mahjong tile matches" loading="lazy"><span><small>Anders Ruff</small>Brownstone Bloom</span></a>`
4. **Colour page /neutral-mahjong-tile-matches** (ivory tiles; lavender butterfly backs, so /purple-mahjong-tile-matches too if that page lists two-colour sets): add one card in the Pippa/Papaya format:
   `<a class="mmcol-card" href="/brownstone-bloom-mahjong-tile-matches"><img src="https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@b57c01d19ab5cfee43a571897a0c6e23db5ae3c3/assets/covers/albums/w800/00-brownstone-bloom-mahjong-tiles-cover.jpg" alt="Anders Ruff Brownstone Bloom mahjong tiles" loading="lazy"><div><b>Brownstone Bloom</b><small>Anders Ruff · 40 matches</small><span>See the album →</span></div></a>`
5. Then /links latest-album card (docs/NEW-ALBUM-CHECKLIST.md §2: links_build.py NEWSET, feature + album images, pin + warm, paste) and the rest of the checklist (FYM album link, Anders Ruff brand page albums section, Google indexing, HQ Albums → live, social).
