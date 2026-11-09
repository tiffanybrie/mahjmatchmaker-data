# Holiday page fix (Nov 9 2026, 2-4am): blurry cards, white-boxed Virora tiles, missing yeses. LIVE

Tiffany, Nov 9 1:39-1:44am, on /holiday-mahjong-matches:
1. December 1994 + Festive Plaid card showed a pixelated mat (she had flagged blurry Festive Plaid in reels on Nov 3).
2. Virora tile insets (Tinselle) showed the tiles shrunk inside a white box with a tile-width margin.
3. Holiday sections looked underpopulated (Dec 1994 had 5).

## What went live (one code block holds all 15 holiday sections: block-84960a4f67d03b1b89be)
- **85 cards re-rendered** (`assets/cards/holiday-fix-nov09/`, pin `25ec7f94`) from the LIVE figure (same title, same tile
  side, same rack captions) with `rerender.py` -> `scripts/albumcard/gen2.py`:
  - all 48 Tinselle cards (Emerald 23, Ruby 25): tile inset = locked filled crop `assets/tiles/holiday/tinselle-*-fill.jpg`;
  - every card whose mat measured blurry (Polo Club x9, PLM Candy Cane Lane, Merry & Striped) or came from a ~500px photo
    (PLM holiday mats, Plaid Tidings): brand full-size photos (`photo_res.json`; PLM variant images 1512px; Polo Club is the
    brand's only flat photo, 1170px, soft: x2 Lanczos + unsharp mask, measured sharp after);
  - Merry Mix: tight crop (the PLM render's shadow left a white strip).
- **December 1994 = the Oct 20 redo kit** (her Oct 16 RTS notes: locked tile racks PLM Dark Green / B&B Brick Red / M&M
  Hawksbill, no B&B woods, EDSR Festive Plaid #1). All 31 images now point at `assets/cards/december-1994-oct20/` (pin
  `25ec7f94`); Polo Club + Cognac re-rendered sharp (`holiday-fix-nov09/`); 5 rack captions changed to the kit's (Festive
  Plaid, Tartan Tidings, Evergreen & Tartan, Polo Club, Tartan Toile Noel). Her order and 31 count unchanged. The staged
  missed-nov07 Dec 1994 kit (25) is fully covered: 24 already live by name; its "Sugarplum Plaid" = the live "Peace Love
  Holiday" card (same PLM plaid mat), so nothing was added.
- **6 missing yeses added** (FYM v118 m-lists vs live, name + brand checked by eye): PLM Candy Cane Lane on Dear Santa,
  Rackin' Rudolph, Holly Jolly (Rudolph Red), Nutcracker Ballet; Bam Bird Holiday on Tinselle Emerald + Ruby (pin `d5dd2b4a`,
  Ruby image pinned `fe74daf1` because jsDelivr cached a 404). Section counts bumped (28->29, 35->36, 22->23, 23->24, 23->24, 25->26).
- Method: `swap.json` (old src -> new src, Dec 1994 caption swaps) + `swap_fix.js` in the code editor (every pair matched
  exactly once), then `adds.json` figures inserted after each section's last card. curl: 244 figures, 289/289 images 200,
  holiday_numbering.py 0 problems, card_sharpness_check.py 0 blurry on the page.

## Gates added (same day, bug rule 8)
- `scripts/checks/card_sharpness.py` + gen2.py: REFUSES a card whose mat source is too small for the crop (> x2.0 upscale)
  or whose rendered mat is soft (e2 >= 0.6 and r < 0.2; calibrated on 627 live mats by eye). Exceptions only with a reason
  in `config/card-sharpness-ok.json`.
- `scripts/checks/tile_fill_check.py` + gen2.py: REFUSES a tile inset with a white/near-white border band > 3%; locked filled
  crops in `config/tile-fill-locks.json` replace padded originals automatically (Tinselle x2, Petalee, Apres Ski, Dear Santa,
  PLM Spirit of Christmas).
- `scripts/checks/card_sharpness_check.py`: live scan of /holiday-mahjong-matches + every album page (blur + white-boxed tile
  inset > 5%), writes docs/status/card-sharpness.json; front_door.py shows FAILs on every message; morning HQ cleanup runs it.
- `scripts/checks/album_gate.py` [8b]: no built album card may have a blurry mat.

## Not changed / open
- Rackin' Rudolph cards still use the brand tile photo (Tiffany 1:37am: her Canva photo canva-v2.png on cards too). canva-v2 is
  1600x700 landscape with a duplicated seam column; needs a hand-picked portrait crop + all 36 Rudolph cards re-rendered.
- Liberty (OMM, retired): 3 holiday cards keep the 472px photo (no larger photo exists anywhere); they measure sharp enough.
- Hidden sections (sunday, hummingbird, nature-walk, sunday-blues: display:none until those albums launch) were not audited for
  missing yeses.
