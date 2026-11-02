# Table View Sample (claude.ai artifact Ht5yLDGWFQhUCYaZeuxQy2)

A working prototype of the Find Your Mat-ch **Table view**: the step after you pick tiles + mat, same entry flow as the app.
It is NOT part of the live FYM build. Up close and Aerial copy the live v112 markup/CSS (split tile band + mat card; mat card
with the tile circle at 40% of the mat's short side). Only Table is new.

## Build
```
python3 builder/table_view/back_colors_nov01.py <fym b112 build dir>   # -> config/tableview-back-colors.json + assets/table-view/backs/*.webp
cd site/livepatch/tableview-sample-nov01
python3 build.py <fym b112 build dir>                                   # app.html (= head.part + script.part) + data -> index.html
python3 ../../../scripts/tableview_back_check.py                         # must PASS before publishing
```
Data: a light subset of the live v112 build (32 sets, 78 mats with photos, every rack with a clean single cut-out) plus a
photo-less index of the WHOLE visible catalog so search finds everything (items not in the sample / not usable in Table view
show grayed with the reason). Coverage classes: config/tableview-photo-class-nov01.json. Stock: config/fym-stock.json.

## Wall (tile back) colors: hard rule (Tiffany Nov 1 3:38pm, Brownstone Bloom bug)
Walls use ONLY a recorded back color from `config/tableview-back-colors.json` (`{slug: {back, type: solid|pattern|ivory, src, patch?}}`).
Never the match-card title color (`set.tc`): that is a face color and drew Brownstone Bloom's ivory backs in burgundy.
- solid: measured from a real back in the set's FYM tile photo (box picked by eye, `builder/table_view/back_boxes_nov01.json`).
- pattern: a texture patch cut from one real back (`assets/table-view/backs/<slug>.webp`); walls are built from it.
- ivory: Tiffany's call (Brownstone Bloom, Sunday Hummingbird; Dear Santa per tile-back-colors-proposed.json).
- Papaya Spritz: real back photo sprite.
- Not recorded = walls grayed "Back color not confirmed yet".
`scripts/tableview_back_check.py` fails if any set draws walls without a recorded back, if a source is the title color or missing,
or if the sample still ships `tc`. (`config/tile-back-colors.json` is an older, different file: color groups -> set names.)

## Phone behavior (Tiffany's iPhone test, Nov 1)
At 1x the table has `touch-action: pan-y`, so one finger scrolls the page; pinch needs two fingers; panning only when zoomed.
`html, body` never scroll sideways. The swap sheet is a non-modal half sheet (max 52dvh), drag the handle down or tap × to
close; its content scrolls on its own and the page gets bottom padding while it is open. Tested in WebKit `devices['iPhone 13']`
and Chromium 1280 with a scrollWidth <= innerWidth check after every step.

## Compare racks (Tiffany 3:48pm)
Default = all 4 seats the same rack (racks sell in sets of 4). "Compare racks" numbers the seats 1-4 (first one pulses),
tap a rack to try a different one there, legend under the table lists each with Shop + "Use this one for all 4" (ends compare).

## Full-flow preview (Nov 1): "Find Your Mat-ch Preview"
- Artifact: https://claude.ai/artifact/5QjNXjw15MuZTqzDT1ptbp (separate from live 6epA9HuEdT32zUp79Qv3kd; not on Squarespace).
- Base: v113 publish copy (scratchpad fym/pub113/index.html, b113 untouched). Build: `python3 builder/table_view/preview_nov01.py <pub index.html> <out dir>` injects builder/table_view/preview_tv.js (Table as 3rd view, Swap racks sheet with search/brand/color/finish/price/in stock, walls, players 4/3/2, tile faces center/corner/off).
- Files: 512 (index + the live 511). Every mc/* chunk except mc/190, every t* photo and b3/b9/b17/b22 were copied server-side from live, because the local re-encodes went over the 256 MiB version cap.
- Tested locally: WebKit iPhone 13 + Chromium 1280. Both doors run through to the card, plus the Table deck. No horizontal overflow, 0 errors.
- Fix carried in: WebKit `.top .stp` nav overflow (289px), CSS `min-width:0`. The same bug exists in live 1.12.

### Rebuild (Nov 1 ~8:30pm, after Tiffany 7:43pm + 7:45pm): preview Version 12
- Same artifact 5QjNXjw15MuZTqzDT1ptbp. Base = pub113 as rebuilt 18:50 (v113 QA round 2); its mc/190.webp re-uploaded with it.
- UX now matches the sample. The changes:
  - Adjust button by the View switch (below the card in the Racks step) opens the bottom sheet: Swap tiles / Swap mat / Swap racks, then Walls and Tile faces Center/Corner/Off.
  - The swap sheet has tabs Tiles · Mat · Racks with its own search per tab (Clear), brand, color, finish (racks), In stock only, Tiffany's picks and price chips. It is drag-to-close.
  - Always 4 players. The old inline Table bar is gone.
- A swapped mat, tile set or rack becomes the app's current card (S.tvforce / S.tfront / S.tvrf), so heart → Racks → Card works. Landing goes to the table after picks; the Card step keeps the app's jump.
- Zoom: the app's zoomer on Table cards (pinch, double-tap, + / −, persisted as S.zs.tvz), redrawn at 2600px once zoomed. The full-screen button shows the whole table at 3000px.
- Sizes come from config/tableview-sizecheck-nov01.json: 33in mat, racks 1in from the edge, 19-tile walls = 19 × tile width, tight against the rack, depth 1.55 × tile width.
- Fixed: html+body overflow-x:hidden made WebKit scroll the BODY, so window.scrollTo failed. Now html hidden, body clip.
- Tests: WebKit iPhone 13 with real taps, both doors, festive → heart → Racks → Card, Swap racks in the Racks step, zoom (double-tap 2.4×, pinch 3.7×, −/+) and the full-screen table: 0 errors, no sideways overflow. Shots are in the scratchpad pv5–pv7shots.
