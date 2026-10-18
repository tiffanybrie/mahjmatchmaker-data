# Match card redesign, built into FYM (Oct 18)

Tiffany approved the three directions from the "Match Card Options" page. They are now FYM step 4:
- **Love triangle** = the spread (hero mat, big tile pile out right, racks card out left).
- **Mood board** (renamed from "Table") = stacked close-ups: tiles / mat / racks.
- **Shop** = showcase: full mat + tile close-up side by side, racks laid out wide underneath.
- Facebook post (4:5) and Pinterest pin (2:3) for each.

Her notes, applied:
- Rack labels on the image are short colour names only ("Oak", "Chartreuse", "Opal & Brass", "Sunshine", "Tortoise", "Walnut"), one under each rack, never on top of a rack. `rackLabel()` in card.js; full names stay in the shop list.
- No extra tiles/mat/rack labels on the logo row.
- Crisp: the canvas is drawn at 2x (2160x2700 / 2000x3000 exports). Tiles, racks and logos come from HD chunks; mats use the fix-3 1200px mats.

## Files
- `card.js`: the card renderer (spliced into the build by `splice.py`, which also adds the Caprasimo font).
- `hd_tiles.py`: finds each set's approved pile photo inside higher-res sources (T.full, repo tile photos, brand Shopify photos at 2000px) with SIFT + homography and crops the same framing. `hd_tiles_color.py` matches colour to the approved pile (e.g. Sunday's warmer mustard). `tile_plan.py` uses the already-published full photo where it is the same framing (no new bytes).
- `hd_racks.py`: album-card rack cutouts (assets/racks/card, 1400px), Bird & Bamboo colours re-rendered from bb-blank.png, otherwise the brand photo located by SIFT.
- `hd_logos.py`, `logo_fetch.py`, `logo_final.py`: largest clean logo per brand (repo, partner-logos, brand sites); Britt Mills' pale script tinted slate so it shows on white chips.
- `hd_mats.py`: not used in the final build (fix 3 already stores mats at 1200px).
- `pack_hd.py`: writes `<build>/hd/index.json` + chunk files (`t*.json` tiles, `r*.json` racks, `l*.json` logos), about 25 MB.
- `test_cards.py` (6 combos x 3 views x 2 sizes through the real drawCard), `test_ui.py` (step 4 at 390 and 1280), `sheet.py`.
- `out/`: exports (downscaled copies; full-res set in scratchpad `card_exports_full/`, two full-res kept here: papaya_tri_fb.jpg, sunday_stack_fb.jpg).

## Publishing
Add `hd/` (22 files, ~25 MB) to the pending fix-2/fix-3 publish list. Order after any rebuild of index.html: fix build -> `python3 splice.py` -> `python3 ../fym_mated_oct18/patch.py`.
Budget warning: fix-3's mc chunks are ~177 MB, so the artifact version is close to the 256 MB / 511-file limit.
