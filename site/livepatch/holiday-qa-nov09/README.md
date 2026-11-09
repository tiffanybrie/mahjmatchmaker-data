# Holiday page QA fix (Nov 9 2026, ~3-4am): older soft cards, Apres Ski inset margin, Pink Wonderland room shot. LIVE

Independent QA of /holiday-mahjong-matches after holiday-fix-nov09 found problems on OLDER cards. Fixed live, changing
nothing else (same order, titles, tile side, rack captions, links: parsefig diff of before/after = identical).
One code block (block-84960a4f67d03b1b89be), 28 image src swaps (`swap.json`, pin `e52f2827`), every old src matched
exactly once, reverse-swap restores the original byte for byte.

## Cards (28)
- **Re-rendered with gen2 via holiday-fix-nov09/rerender.py (`jobs.json`, built by `mkjobs.py` from the live figure):**
  - PLM pink plaid (Peace Love Holiday = Sugarplum Plaid mat), from the brand's 1512px variant photo instead of the ~500px one:
    Peace Love Holiday on Holly Jolly Pink #1, Holly Jolly Red #8, Nutcracker #6, Rudolph #5, December 1994 #29;
    Sugarplum Plaid on Holly Jolly Pink #21, Holly Jolly Red #21, Dear Santa #27, Rudolph #33, Nutcracker #22. r .203/.237 -> .253.
  - Bespoke Holiday Love Red & Green (newly flagged by the tighter threshold) on Dear Santa #12, Rudolph #4, Holly Jolly Red #1,
    Holly Jolly Green #1: brand 706px photo (the Tinselle source), r .233 -> .293.
  - Anders Ruff Candy Cane Lane (zoomed, JPEG-blocky) on Dear Santa #1, Holly Jolly Red #6, Rudolph #1, Nutcracker #3: the
    same 1200px flat as December 1994 #3, whole mat. r .40 -> .456 (soft by eye; the meter cannot see JPEG-block softness).
  - Candy Cane Pink Wonderland (Holly Jolly Pink #5, Nutcracker #4): Mahj Squad has NO flat photo (5 images, all room/angled;
    the close angled ones measure soft, r .07-.17). Used the room shot ms-781 cropped to the mat [60,400,786,1000] (FYM
    mat-focus style), x1.85 upscale, r .231: the mat (pink lattice, teal border, candy-cane bows) now fills the mat area.
- **Apres Ski #1-#8 tile inset**: pixel patch of the inset rect (667,592)-(1080,1107) from #9 (gen2 render of the locked
  `cmc-apres-ski-fill.jpg`); mats untouched. Cream margin 12.6% -> 1.9%.

## Gates changed
- `scripts/checks/card_sharpness.py`: blurry = r < 0.21 (was 0.20), or r < 0.24 when e2 >= 5 (strong patterns).
  Calibration Nov 9 live scan (2178 cards): 3 -> 41 album-page FAILs after this fix (all the same soft photos: PLM Sugarplum/
  Peace Love Holiday 28, Bespoke Holiday Love Blue/R&G 7, Britt Mills Chinoiserie, B&B Boots & Bubbles Periwinkle, M&M Vintage
  Floral Gingham, + the 3 old). Holiday page: 0 FAIL. See docs/OVERDUE.md.
- `scripts/checks/tile_fill_check.py` (gen2): cream band test on top/left (min >= 215, chroma <= 18), max 5%: the original
  cmc-apres-ski.jpg now fails (top 12.5%, left 8.7%); all 68 tile files in use pass.
- `scripts/checks/card_sharpness_check.py` (live): tile_cream() top/left > 7% FAILs (old Apres Ski cards 12.6%; old Dear Santa
  pile cards 5.8% pass). Only the 8 Apres Ski cards tripped it on the whole site.
