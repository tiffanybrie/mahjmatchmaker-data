# FYM door parity matrix (Nov 7 2026, FYM 1.18)

Why: Tiffany, Nov 7 at 10:24pm. She wanted to pick the Lotus Cove mat and see only Oh My Mahjong tiles, but the mat door's tiles step had no brand dropdown and no colour filter. It only had a brand text search, price and view. Her words: "You need to make sure everything is mirrored up so that everybody can get to whatever they want to get to, however they want to get to it."

**Rule (standing):** each item type (tile sets, mats, racks) gets the same filters wherever it is chosen. That covers the first step of its own door, the second step of the other door, the racks step and the Table view swap sheet. Any step that comes after an earlier pick also gets two more controls: **Tiffany's picks** and **Same brand as my mat/tiles** (the brand lock).

- Patch: `builder/fym_fix_nov07/doors_v118.py <build>`. Run it after the data patches and after `zoomswipe_v118.py`, and before `release118.py`.
- Gate: [167] runs `builder/fym_fix_nov07/doors_check.py`. It reads the build's own render code and fails if a filter is missing anywhere. For example, it fails if the mat door's tiles step has no colour filter.
- Browser QA: `builder/fym_fix_nov07/doors_pw.py <build> <shots>` runs at 390px with touch and at 1440px.

Legend: Y = there before 1.18 · **ADDED** = added in 1.18 · n/a = does not apply.

## Tile sets

| Control | Tiles door, step 1 (tile grid) | Mat door, step 2 (tile swipe) | Mat door, step 2 ('See all' grid) | Table view sheet (Tiles tab) |
|---|---|---|---|---|
| Search by name / brand | Y | Y | uses the swipe view's search | Y |
| Brand | Y (dropdown + logos) | **ADDED** (Brand ▾ sheet with logos) | **ADDED** | Y (menu) |
| Same brand as my mat | n/a (nothing picked yet) | **ADDED** | **ADDED** | **ADDED** (top of the Brand menu) |
| Colour groups | Y (chips) | **ADDED** (dots, same groups, tap again to clear) | **ADDED** | Y |
| Holiday | Y (group chip) | **ADDED** (chip) | **ADDED** | Y |
| In stock only | **ADDED** | **ADDED** | **ADDED** | Y |
| Price | **ADDED** | Y | **ADDED** (price line on the cards) | Y |
| Tiffany's picks | n/a | **ADDED** (shown when she matched this mat) | **ADDED** | Y |
| Finish / material | n/a: tile sets carry no finish data | n/a | n/a | n/a |
| Sort | brand logos, colour groups, All A-Z | ranking: her picks, then colour match (unchanged; another agent owns ranking) | same | her picks, then partners, then A-Z |

## Mats

| Control | Mat door, step 1 (mat grid) | Tiles door, step 2 (mat deck) | Table view sheet (Mat tab) |
|---|---|---|---|
| Search | Y | Y | Y |
| Brand | Y (dropdown) | Y (Brand ▾ sheet) | Y |
| Same brand as my tiles | n/a | **ADDED** | **ADDED** |
| Colour | Y | Y | Y |
| + Add a colour (two colours together) | Y | Y | not offered (the sheet picks one colour at a time); allowed exception in the gate |
| Holiday | Y | Y | **ADDED** |
| In stock only | Y | Y | Y |
| Price | **ADDED** (price line on the mats) | Y | Y |
| Tiffany's picks | n/a | Y | Y |
| Retired | no control: retired mats show only when Tiffany matched them, with a Retired label | same rule | same rule |

## Racks (step 3 is shared by both doors)

| Control | Racks step | Table view sheet (Racks tab) |
|---|---|---|
| Search | Y (+ Search any rack) | Y |
| Brand | Y | Y |
| Same brand as my tiles / mat | **ADDED** (two chips when the brands differ) | **ADDED** |
| Colour | Y | Y |
| Type (wood, acrylic and so on) | Y | Y |
| In stock only | Y | Y |
| Price | Y | Y |
| Tiffany's picks | Y | Y |

## Behaviour notes

- **Filters never lock.** Tapping a colour, the brand chip (it reads "Brand ✕") or the same-brand chip a second time clears it, and there is also a Clear link. If a combination leaves no tile sets, the deck shows all of them with a note saying "No tile sets fit all of those, so showing all" and a Clear link. The mat door's tile filters reset when you change the mat.
- **Tiles door, step 1:** the brand logos are still the first thing you see. Turning on In stock or picking a price shows the filtered A-Z list.
- **Not changed:** ranking (another agent owns tile ranking, gate [168]), X and heart, zoom, and the swipe itself.
- **Holiday on the tiles step** only appears when the mat has holiday tile sets in its list. A non-holiday mat such as Lotus Cove never lists holiday sets (the existing holiday rule), so it shows no Holiday chip there.
- **Collab sets count for both brands.** 'LoveShackFancy x Oh My Mahjong' sets count as Oh My Mahjong for 'Same brand as my mat'.
- **The patch keeps the code text older gates read:** [8] (no `fam:''`), [19]/[105] (the brand-logo line, the colour-branch sort), [61], and [153] (no star glyph).
