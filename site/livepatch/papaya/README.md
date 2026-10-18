# Papaya Spritz album: ready to go live (Oct 18)

**Approval:** Tiffany said Yes to the Papaya album in chat (2:31pm). It goes live once the title card and the Grand Garden Estate card are fixed, and both fixes are done.

## What's staged
- **`papaya-spritz-codeblock.html`:** the full album code block. Card images are pinned to commit `b3f23e5`.
  - 50 cards in her saved Ready to Ship order (db `c5-papaya-order`, saved 1:11pm). She cancelled 51–53 (Tropical Palm, Peaches 'n Cream, Sweet Marie) in `l-pap-order3`.
  - Tiers follow her cut lines: TOP 1–11, BEST 12–26, MORE 27–50.
  - Card fixes: Goldie uses her bright clean photo (`assets/mats/clean/goldie-omm.png`). The Mahj & Moon Grand Garden Estate, Retro Waves and Leopard American mats have the bamboo background cut out (`assets/mats/clean/mahj-and-moon-*.png`).
  - Every "Racks shown" caption comes from that card's own racks: tiles = PLM Oak, PLM Chartreuse, B&B Lavender, plus each card's mat racks.
  - The 4 retired OMM mats (Goldie, Enchanted, Zen Glow, Spring Fling) get the Retired tag and the "Shop Current OMM Mats" link.
  - All 51 jsDelivr URLs are warmed: 51 of 51 returned 200 on the first try (`../warm_result_papaya.json`).
- **Cover:** `assets/cards/papaya-spritz/00-papaya-spritz-mahjong-tiles-cover.jpg`, plus the grid size `assets/covers/albums/w800/00-papaya-spritz-mahjong-tiles-cover.jpg`. Both are the centered title version, commit `3091240`.

## Make the page /papaya-spritz-mahjong-tile-matches
1. **Duplicate an album page.** In /config/pages, duplicate a live album page with the current album layout, e.g. Jade (/jade-mahjong-tile-matches, newest in the sitemap): page gear → Duplicate Page → Confirm. It goes live right away as "(Copy)", so do steps 2 and 3 at once.
2. **Set the page settings** with the API in /config (doc 59 §4), using GetCollectionSettings, then SaveCollectionSettings:
   - **Title:** Papaya Spritz Mahjong Tile Matches
   - **Slug:** papaya-spritz-mahjong-tile-matches
   - **SEO title:** Papaya Spritz Mahjong Tile Matches: Mats & Racks for Oh My Mahjong Papaya Spritz
   - **SEO description:** Oh My Mahjong Papaya Spritz tiles matched to 50 mats, with rack picks and shop links. Top picks first. Save with code MAHJMATCH.
3. **Replace the code block.** Replace the duplicated album code block with `papaya-spritz-codeblock.html`, fetched from jsDelivr at the commit this README is in.
4. **Verify with curl:** 50 `mm3-c` figures, h1 "Papaya Spritz Mahjong Tile Matches", and the cover loading.

## Add the cover to the other pages (after the page is live)
- **/mahjong-tile-matches and the home page:** use the variants that already include Papaya under Yellow & Orange:
  - `../color/mtm_replace_with_papaya.html` in place of `mtm_replace.html`
  - `../color/home_insert_with_papaya.html` in place of `home_insert.html`
  - The block ids are in `../color/README.md`.
  - If the color sections went live without Papaya, add the same `mmalb-c` card, from the variant files, to the end of the Yellow & Orange grid.
- **/yellow-orange-mahjong-tile-matches:** add one `mmcol-card` after Tortoise, in the same format as the Pippa card:
  `<a class="mmcol-card" href="/papaya-spritz-mahjong-tile-matches"><img src="https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@3091240/assets/covers/albums/w800/00-papaya-spritz-mahjong-tiles-cover.jpg" alt="Oh My Mahjong Papaya Spritz mahjong tiles" loading="lazy"><div><b>Papaya Spritz</b><small>Oh My Mahjong · 50 matches</small><span>See the album →</span></div></a>`
- **Mahjong Matches album lists:** if they list albums anywhere outside the color sections, add Papaya there too.
- **Follow-ups:** update the What's Live ledger row. The FYM pending build should use the same 50-card order.
