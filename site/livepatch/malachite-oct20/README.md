# Malachite: 8 new matches, staged Oct 20 (NOT live)

**Source:** Ready to Ship `l-mal-cards2` (Oct 18, 12:58pm, "chg") and `c5-malachite-new` (her saved order). She never tapped a plain Yes on this item, so ask once ("Malachite new cards: live?") before the live step.

## Her 3 changes, applied
1. **Brighten the Jardín needlepoint photo, everywhere on the site.** The muted photo is the needlepoint canvas shot `assets/mats/tigre-de-tartan/jardin-de-los-jefes-canvas.jpg`. The brightened copy is `assets/mats/clean/jardin-de-los-jefes-canvas-bright.jpg` (blue-grey cast removed, levels stretched, saturation +25%; script `scripts/albumcard/specs/malachite-new/brighten_jardin.py`).
   - Where that photo is used: the Malachite card (rebuilt here), the Brownstone Bloom card (she cancelled it, so it's dropped), and the Mat Gallery tile for the needlepoint-canvas listing. A brightened replacement for that tile is in this folder: `tigre-de-tartan--mahjong-mat-printed-needlepoint-canvas-14-mesh-jard-n-de-los-jefes.webp`.
   - The 7 older album cards (Amara, Dandy, Emerald, Glitterville, Jasmine, Solara, Sunset) use the brand's bright illustrated render, not this photo. They were left alone.
   - **Not done:** the Find Your Match photo for the key `tigredetartan.com/jardin-de-los-jefes-printed-needlepoint-canvas-14-mesh`. Swap it in the next FYM build.
2. **Manor Garden cancelled.** It has no card and is not in the snippet.
3. **White Lotus mat racks use MMSIO** (Miss Mahjong Scalloped Iridescent Opal) + B&B Moss, replacing Dijon.

## Also changed (rules, not her notes)
- **Garden Party Deep Green** mat racks now use her Oct 20, 9:33am registry pick (config/mat-racks-picks.json `miss-mahjong-deep-green-garden-party`): B&B Brick Red, Miss Mahjong Jade & Brass, MMSIO. The rule is one set of racks per mat. The Oct 17 card had Evergreen + Lilac.
- Tile racks stay her final list for Malachite: PLM Oak, Miss Mahjong Jade & Brass, Miss Mahjong Brass & Tortoise.

## What's staged
- **Cards (8, her order):** `assets/cards/malachite-oct20/`, commit `7a6706c`:
  1 Serenity, 2 Midori Shadows, 3 Garden Party Deep Green, 4 White Lotus, 5 Garden Party Powder Blue, 6 Jardín de los Jefes, 7 Garden Party Lavender, 8 Pink Tiger.
  Build: `scripts/albumcard/oct20/malachite_build.py`, then `gen2.py`. The manifest is in the same folder.
- **Insert snippet:** `malachite-new-cards-insert.html`. These are 8 `mm3-c` figures numbered 35–42, with Match the tiles / Match the mat captions and images pinned to jsDelivr `@7a6706c19a9d4d0483b295db57b97777ebf30c81`.
- **Gap:** Midori Shadows (Golden Pond Mahjong) has no shop link anywhere in our data or on the web, so its card has no Shop button. Add the URL if she has it.

## Live step (after her Yes)
1. Warm the 8 jsDelivr URLs (doc 73). Curl each one until it returns 200.
2. On /malachite-mahjong-tile-matches, open the album code block (`block-yui_3_17_2_1_1791139519149_3785`). In the `<section><h2>Every Malachite match</h2>…<div class="mm3-grid">` grid, paste the snippet right before that grid's closing `</div></section>`. That is after card 34 (Holy Mahj) and before the Holiday section.
3. In the same block, change the FAQ line "Below are all 34 Malachite mat matches from 15 brands" to say 42 matches. Recount the brands in the live block after inserting the cards. The new cards bring Amanda Toppe, Golden Pond Mahjong, Miss Mahjong, Mahj Tile Haus, Tigre de Tartan and YOLO Mahjong, and some of these are probably already counted. Update the JSON-LD only if its text includes the count.
4. Verify with curl: 42 `mm3-c` figures in the main grid, and "Pink Tiger" and "Midori" both appear.
5. Mat Gallery: replace the Jardín needlepoint tile image with the brightened webp from this folder.
