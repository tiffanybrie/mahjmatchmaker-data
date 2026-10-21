# Kerry match cards into 11 live albums (Oct 21). STAGED, NOT LIVE (waiting on independent QA)

Tiffany (Oct 21 3:39pm) loved the Kerry cards and wants them in the albums. Sets: Pearlescent, Moonlight, La Fete, Willow, Talulah, Coquette, Birdie, Dandy, Luminaire, Taylor, Sorbet (Jasmine dropped on her call).

## Checks done
- Racks = config/tile-racks-picks.json final_lists (tile racks) + config/mat-racks-picks.json `kerry` (B&B Ballet Pink, Miss Mahjong Scalloped Iridescent Opal, Mahj Mood Scalloped Clear Acrylic). Tile photo = assets/tiles/album/<set>.jpg (canonical, unchanged since render).
- Code band: re-rendered at commit 63f498e. 10 OMM sets: "10% OFF USE CODE : MAHJMATCH". Coquette (LoveShackFancy x OMM; no code on tiles or mat) keeps SHOP THE MATCH, the documented Coquette exception (brownstone_bloom_build.py).
- Shop link: her ShopMy Kerry link https://go.shopmy.us/p-96114928 (verified: redirects via Rakuten to etsy.com/listing/4493549326). No etsy.com link on the cards.
- Placement: #4 in the main grid, right after her top 3 (the three the FAQ names). Grid renumbered; "all N <Set> mat matches from M brands" bumped +1/+1 (FAQ + JSON-LD).
- All 11 card URLs (jsDelivr @63f498e) warmed: 200 and byte-identical to the repo.

## Files
- `kerry-<set>.html`: the figure for each album. `build.py <sha> <live dir>` rebuilds them; `manifest.json` set -> display name.
- `kerry_fix.js`: `kerryFix(src, setName, FIG)` -> {src, note}; idempotent (no-op if a Kerry card is already there).
- `live-before/<set>.html`: curl of each live page before the change (rollback reference).
- Previews (full pages with the patch applied): scratchpad `kerry/preview/<set>.html`.

## Publish (one tab, after QA)
For each album page /<set>-mahjong-tile-matches in /config: open the code block that contains "Every <Set> match", read the CodeMirror doc, run kerryFix with the raw `kerry-<set>.html` (jsDelivr at this folder's commit), diff (only the grid + 2 count strings change), `cmTile.view.dispatch` the new text, Escape, Save, Exit. Then curl: 1 `bettyjunejeannette-kerry-mat` img, `go.shopmy.us/p-96114928` present, no etsy.com/listing/4493549326, the Kerry card's `mm3-n` is 04.

## Mat Gallery (/mahjong-mats)
Row `betty-june-jeannette--the-kerry` url: etsy.com -> https://go.shopmy.us/p-96114928 (repo: matgallery-v5.html + new53_rows.json). Live fix = one string swap in the gallery code block.

## FYM (not published here)
Staged fym-oct21f: Kerry is NOT in the match list (m) of any of the 11 sets, and its mat `u` is still etsy.com. For v70/v71: add Kerry to these 11 sets' m (her real picks: the album cards) with the card racks, and set u = https://go.shopmy.us/p-96114928.
