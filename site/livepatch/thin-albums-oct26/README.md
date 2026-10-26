# Thin albums: Tiffany's 41 hearts → match cards on 9 live albums (Oct 26). READY FOR OPS PASTE

Source: her hearts in the thin-album review (artifact UQy4YpGD2RR5Z1WqswJWYM, db `votes`, Oct 23-24). Tiffany, Oct 26 8:01am: "my additional picks for the thin albums that I picked a week ago have not gone into the match album." Why they were late: the Oct 24 desk cleanup parked them as "After launch". This is a standing job, not a new decision, so no OK is needed. Each heart is a match card appended at the END of that album's main grid.

| Album | Adds | Cards file |
|---|---|---|
| Sorbet | 8: Colony, Pink Cabana, Katelyn, Seafoam Cabana, Caroline, Nora, Citrus Grove, Brinkley | sorbet-cards.html |
| Pippa | 7: Peony & Parasol, Colony, Pink Cabana, Nora, Caroline, Watercolor Floral, Citrus Grove | pippa-cards.html |
| Sunset | 5: Pink Tiger, Brooke, Betty Floral, Elizabeth, Cheeky Cockatoo | sunset-cards.html |
| Limoncello | 5: Seafoam Cabana, Pink Cabana, Kerry, Brinkley, Chinoiserie Elephant | limoncello-cards.html |
| Osler | 4: Winslow Navy, Winslow Rouge, Gatsby, Pavilion | osler-cards.html |
| Jasmine | 4: Chinoiserie Cheetah, Whimsical Chinoiserie, Citrus Grove, Nichole | jasmine-cards.html |
| Taylor | 4: Livy, Nora, Caroline, Elizabeth | taylor-cards.html |
| Gemma | 3: Livy, Allie, Pink Orchids | gemma-cards.html |
| Nantucket | 1: Midori Shadows | nantucket-cards.html |

## What's in each card
- **Image:** `scripts/albumcard/gen2.py` (live album style), `assets/cards/thin-oct26/*.jpg`, jsDelivr pinned at **e718949b**.
  - Tile photo: `assets/tiles/album/<set>.jpg`.
  - Lower left: the album's tile racks (config/tile-racks-picks.json final_lists). Osler drops Tigre de Tartán Oxblood Scallop, which has no photo and isn't sold.
  - Upper right: the mat's racks. Kerry uses its registry entry in config/mat-racks-picks.json; the other 27 mats are a Claude matpick kept in the card spec (`specs/*.json` mat_racks), NOT in config/mat-racks-picks.json, because that file feeds FYM D.lm and would change those mats' other pairings (gate [36]/[51]).
  - Code band: 10% OFF MAHJMATCH.
  - Specs: `specs/*.json`; `build.py` re-renders.
- **Mat photos:** brand flat renders where we have them (Pink Tiger, Midori Shadows, Peony & Parasol, Watercolor Floral, Winslow, Gatsby, Kerry). The rest come from the FYM photo (`assets/mats/thin-oct26`).
  - Four Etsy photos had a curled black corner: Katelyn, Brooke, Pink Orchids, Chinoiserie Elephant. They are turned 90° so the corner sits under the tile photo (`*-r90.jpg`).
  - Pink Orchids and Chinoiserie Elephant therefore read sideways. Swap in a flat photo when we can get one (Etsy blocks us).
- **Links:**
  - ShopMy for Betty June & Jeannette, Sophie Clima and Tala.
  - Brand + sca_ref for Mahj & Vine and Splash of Color.
  - Brand site for Wren Mats, Ozark, Mahjong by SI and YOLO.
  - Midori Shadows has no shop link anywhere, so no button (same as the live Malachite card).
  - Code line `code MAHJMATCH` + "Mat by" link to the discount page for the code brands: Mahj & Vine, Wren Mats, Splash of Color.
  - No-code brands get the Kerry wording: "We do not have a code for X; code MAHJMATCH works on <Set> tiles." Retired Sorbet/Taylor say "Oh My Mahjong's current tiles and mats." instead.
  - All brand links curl 200 (Oct 26).
- **Blurbs:** the one-line "take" on each card was written by Claude (`build.py` TAKE). Edit there and re-run `python3 build.py e718949b` if she wants different words.
- **Counts:** `thin_fix.js` bumps "all N <Set> mat matches from M brands" (FAQ + JSON-LD, 2 hits per page) by the cards added and by brands new to the page.
  - Several pages already disagreed with their grid before this change (e.g. Sorbet 12 cards vs "9"), because the counts include holiday sections and older drift. We bump; we don't recount.

## Files
- `<set>-cards.html`: the new figures for that album, numbered NN (thin_fix renumbers).
- `manifest.json`: set → display name, album URL, n, brands.
- `thin_fix.js`: `thinFix(src, setName, CARDS)` → {src, note}. Appends after the last card of the main grid (holiday sections untouched), renumbers 2-digit, bumps counts. Idempotent: it skips any card whose image is already on the page.
- `live-before/<set>.html`: curl of each live page before the change (rollback).
- Previews with the patch applied (node, from live-before): scratchpad `thin/preview/<set>.html`. Checked in Playwright at 390 and 1280: the cards render.

## OPS PASTE (one Chrome tab, one album at a time; close the tab after)
0. Warm jsDelivr first. jsDelivr can intermittently return 403 "Package size exceeded" for an edge it hasn't cached; docs 59/73.
   - Fetch every `cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@e718949b/assets/cards/thin-oct26/*.jpg` until each returns 200 and matches the repo bytes.
   - On Oct 26, 41/41 were seen 200 at least once (2 flapped between edges).
   - If one stays 403, swap that URL to `https://raw.githubusercontent.com/tiffanybrie/mahjmatchmaker-data/e718949b/<path>`.
1. Get the code: `thin_fix.js` + `<set>-cards.html` from `https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@<README commit>/site/livepatch/thin-albums-oct26/...`. raw.githubusercontent at the same commit works too.
2. In /config, open `/<set>-mahjong-tile-matches` and click Edit. Open the code block containing "Every <Set> match" and **wait ~4s** after the pencil.
3. Read the doc and run the fix:
   `const v=document.querySelector('.cm-content').cmTile.view; const r=thinFix(v.state.doc.toString(), '<Set>', CARDS);`
   Check `r.note`: added = expected n; counts line x2.
   Diff: only the grid tail, the mm3-n numbers and 2 count strings change.
4. Apply it: `v.dispatch({changes:{from:0,to:v.state.doc.length,insert:r.src}})`. Then type a space and Backspace so Save turns black, Escape, Save, Exit.
5. Verify with curl:
   - the page has the expected number of `assets/cards/thin-oct26/<set>-` images;
   - the last card's `mm3-n` = new total;
   - the count string is updated.
6. After all 9 are live, Matches & Catalog runs the FYM patch in the next build (below).

Set names for thinFix: Sorbet, Pippa, Sunset, Limoncello, Osler, Jasmine, Taylor, Gemma, Nantucket.

## FYM (NOT published here)
- `builder/fym_fix_oct26/v94_thinpicks.py <build>` + `config/fym-thin-picks-oct26.json`:
  - appends the 41 to each set's `m` (her real picks) with the card racks;
  - updates locks.json sets.m;
  - appends the cards to the live-album snapshot (albums-live-oct21.json) and recomputes D.ao.
- Run it only once the cards are live: gates [16]/[51] compare with the live album pages.
- Do NOT run fym_fix_oct22/rack_picks.py --locks with it (older than the v90 per-album rack rule; rewrote ~60 other pairings in the Oct 26 test).
- Tested Oct 26 in an isolated copy of the repo on b93 + this patch: added 41, every rack label resolved; gate failed only on [59] tile door default chip and [61] 'Photo coming soon' sort, both newer UI gates that the unpatched b93 also fails (not this patch).
- Non-partners allowed as her picks (builder/fym_flags/nonpartner_allow.json mats, "her thin-album ♥ Oct 23-24"): YOLO Pink Tiger, Golden Pond Midori Shadows, Mahjong by SI Gatsby.
- Ozark (whole line), Tala (ShopMy), BJ&J and Sophie Clima (ShopMy) were already allowed.
