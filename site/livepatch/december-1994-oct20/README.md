# December 1994 (Sunday Mahjong) holiday cards, staged Oct 20 (NOT live)

**Source:** Ready to Ship `c5-dec1994` (Oct 16, 12:04pm, "chg"). It saved her order of all 31 cards with the note "You have Bird & Bamboo wood racks matched to the mat, revise. There are low res images in some of these, including my #1 pick". Also `c4-dec1994` (don't overcrowd the mat, keep racks down and to the left, logos only where wanted). The current card layout already handles that.

## Her notes, applied
- **No B&B wood racks.** Every mat-side pick that was a B&B wood (Red Mahogany ×6, Provincial, Weathered Oak) was re-picked with `matpick.py`, which bans woods and won't repeat the red/green tile racks.
  - Vintage Oxblood Leather uses her standing rule: B&B Wine + PLM Acrylic Burl.
  - Brown Vegan Leather uses its saved registry pick: PLM Acrylic Burl.
  - The two old cards that still showed **B&B Almond** on the tile side (Festive Plaid, Polo Club) are rebuilt.
- **Low-res fixed, card by card** (`crop_px` in the manifest = source pixels behind the 1080px mat area; every card is 900 or more now):
  - **Her #1, Festive Plaid:** EDSR x4 super-resolution. Sunday's largest photo is only 867px.
  - **EDSR x4 also on:** Cognac (479px), Hollivia, Vegan Leather, Crimson Harvest, Bam Bird Holiday, Sleigh All Day, Merrywood, Letters to Santa, Liberty, Peace Love Holiday.
  - **Brand hi-res, same photo but larger:** Tartan Tidings, Tartan Toile Noël, Candy Cane Lane, Evergreen & Tartan, Santa's Mahjong Mail (all 1200px), Polo Club, Ski Club, Winterberry, Holly Jolly, Yuletide, Tartan Tweed (3312px). Plus `assets/mats/holiday/hd` for Rackin' Rudolph, Classic Very Merry Mahj and Rattan.
  - Photos too small for the 72% album close-up now show the whole mat instead of an upscaled corner.
- **Tile racks, consistent on all 31:** her **locked Holiday Tile Racks picker picks** (`config/holiday-picker-picks.json`, exported Oct 16 at 3:22pm, after her Oct 15 Red/Evergreen/Oak call): **PLM Dark Green, B&B Brick Red, Middle & Main Hawksbill Heritage Tortoise.** The 5 live cards already use these. The 26 newer cards had B&B Red/Evergreen/PLM Oak.
- Footers follow the Oct 18 rule (every card carries MAHJMATCH).

## Still open with her
- **Festive Plaid mat rack** stays B&B Pink Coral. Decision `o-pinkcoral` (Dec 1994 + Festive Plaid rack) is still open.
- Auto re-picks worth a glance: Tartan Tidings and Tartan Toile Noël (B&B Magenta + Wine), Santa's Mahjong Mail (Magenta), Tartan Tweed (Acrylic Burl + Basil).

## What's staged
- **Cards:** `assets/cards/december-1994-oct20/` (31 + manifest), commit `803e04e`. Build: `scripts/albumcard/oct20/dec1994_build.py`, then `gen2.py`.
- **Holiday page grid:** `december-1994-holiday-grid.html`. It has 31 `mm3-c mm3-hc` figures in her order, with "Match the tiles / Match the mat" captions that match the cards. Images are pinned to `@803e04efc6f6253766cfe2a2186dc0f948e1b384`. Built by `scripts/albumcard/oct20/dec1994_snippet.py <sha>`.
- **jsDelivr warmed:** 31 of 31 URLs return 200. One URL needed a manual retry after six 403s (`../warm_result_owed_oct20.json`).

## Live step (after her Yes)
1. On /holiday-mahjong-matches, find `<section class="mm3-hol" id="december-1994">`. It currently has "5 mat matches" and the 5 old cards: Evergreen & Tartan, Festive Plaid, Tartan Tidings, Tartan Toile Noël, Polo Club.
2. Replace everything inside its `<div class="mm3-grid">…</div>` with the contents of `december-1994-holiday-grid.html` (minus the comment line). Change "5 mat matches" to "31 mat matches".
3. Curl the page and check that section has 31 `mm3-hc` figures. Card #1 must be Festive Plaid, and "Almond" must not appear in the section.
4. Any other page that shows a December 1994 card (FYM, the Sunday Mahjong brand page, the Dec 1994 cover links) should point at the `december-1994-oct20` files in the same swap.
