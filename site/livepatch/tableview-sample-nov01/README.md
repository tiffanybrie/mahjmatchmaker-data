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
