# Missed album picks (Nov 7): her yeses that never reached the album pages. STAGED, NOT PASTED

**Why.** Tiffany hearted mats in MAT swipe books and her yeses never reached the album pages. Larkspur was approved Oct 25 for 28 tile sets and sits on 2 of them. The other books were Poppins, Vivienne, Peony & Parasol and the holiday mat books. The yeses went into Find Your Mat-ch m-lists and stopped there (ANSWERS Oct 25 8:17pm; gap audit C2). Her words: "So much time spent on that single mat... and then you guys just let it fall on the floor." The Nov 7 missed-mats round-1 yeses (config/picks/missed-mats-round1-2026-11-07.txt) are included too. A YES IS A YES: every pair becomes a match card on the album page. Nothing needs her OK.

## The list (definitive, Nov 7 ~10pm)
`pairs.json` has 463 (page, mat) pairs, one card each. 233 go in main grids and 230 in holiday sections. 462 are staged for paste; 1 is held (see below). By source: 321 come from FYM m-lists and 142 from round-1 (4 more round-1 pairs were already on their pages).
- **Sources:**
  - FYM website copy `site-app/fym-v117/index.html` (fym-site-preview @8a3081f2): every set's `m`. Live /find-your-match = v117.
  - Round-1 yeses. Mapped to FYM keys through docs/audits/album-missed-mats-2026-11-07.json, with v118 for new catalog mats. All 146 lines mapped.
- **Minus what is already on the page.** Each live page was curled Nov 7 ~10pm.
  - The matcher compares card by card: the mat-name tokens of each `<h3>` plus its "Mat by" brand. The coverage_check normaliser alone gave 127 false misses ("Caned Trompe L'oeil Natural" vs "Caned Trompe L'oeil", "Very Merry Wreath Premium" vs "Very Merry Wreath").
  - A different mat with the same word still counts as missing (OMM Sugarplum ≠ PLM Sugarplum Plaid).
- **Holiday section.** A pair goes in the page's holiday section when:
  - the mat is a holiday mat (FYM `hol`; CLAUDE.md holiday rule), or
  - the round-1 line said "(holiday)", or
  - the page is a /holiday-mahjong-matches section (dear-santa, tinselle-ruby, ...).
- **Not mappable** (`not_mappable.json`):
  - **Hummingbird** (42 FYM picks): album drafted in site/livepatch/sunday-albums-nov06, not live; #hummingbird hidden. Goes in with that album.
  - **Spirit of Christmas** (PLM holiday set, 10 picks): no album or holiday section exists.
  - **Cypress** (37): Mahjong Row is out of the site (Nov 6).
  - **1 Mahjong Row mat pair dropped.**
- **HELD (1): Malachite + Green Malachite (Mahj Squad).** The only photo (FYM's) carries MAHJ SQUAD watermarks all over it. The card is built (`assets/cards/missed-nov07/malachite-...-green-malachite-mat.jpg`) but `build.py` HOLD keeps it out of the paste. It goes in once there is a clean photo: drop it from HOLD, re-run `build.py html <sha>` and paste Malachite again (missedFix is idempotent).
- **Flags:** 3 December 1994 picks are mats hidden in FYM (Mahjong by SI Highland Heritage Plaid, The Hunt Club, Vintage Oxblood Leather). They are her yeses, so they stay.
- **Finder scripts:** `finder/` (diff2.py → refine.py → getmats.py → make_pairs.py). Run them in a work dir with `live/` curls, D117.json/D118.json dumps and mcfiles.txt.

Pairs per page: see `manifest.json` (main / holiday counts). Top: December 1994 25, Tinselle Ruby 23, Tinselle Emerald 21, Jade 16, La Fete 16, Malachite 16, Amara 14, Coquette 14, Moonlight 14, Nantucket 14, Brownstone Bloom 13, Talulah 13, Heritage 12, Lola 12, Rackin' Rudolph 11.

## The cards
- **Images.** `build.py cards` renders them to `assets/cards/missed-nov07/` (1080x1350, scripts/albumcard/gen2.py + card2.html). It uses the Juniper/Deco pipeline:
  - the album's tile PILE photo (assets/tiles/album; holiday sets assets/tiles/holiday);
  - the current navy wordmark card_navy_logo_v3.png;
  - racks at true relative length;
  - the tile-brand logo flag;
  - the full mat name in the title, with "(retired)", a trailing "Mat"/"Premium" and the TdT x Miss Mahjong prefix dropped. Six very long names use the short names the live pages already use (`SHORT`: Holiday Love Red & Green / Blue, Ski Club Red Sweater / Periwinkle, Betty Floral, Holly Jolly Leatherette). Noli June's "Lena Took Seven Months to Needlepoint a Pillow" keeps its full name in the caption; only the card title band reads "Lena Took Seven Months" (`CARDTITLE`).
- **Racks**
  - Year-round, tile side: the album's approved list (config/tile-racks-picks.json final_lists, else colorcards racks). Mahjong Row & Co. racks are dropped from new cards because the brand is out of the site (Nov 6). Only Amara was affected: Mahjong Row Scalloped Tortoise left the tile side.
  - Year-round, mat side: the mat's saved racks when it has any. config/mat-racks-picks.json covers Larkspur (Lime Green + Cornflower Blue Scalloped) and Vivienne. config/matcard covers Poppins (B&B Hot Pink Metallic, Turquoise Blue, Periwinkle Blue). Otherwise matpick: 2 B&B colours that are not tile racks.
  - Holiday cards follow the Nov 3 standing rules (late_holiday_build): one painted colour on the tile side, one B&B colour (never orange) + one neutral real rack on the mat side, and the holiday band + flame.
- **Mat photos**
  - Larkspur and Vivienne use the launch photos with their approved crops. Poppins uses config/matcard/poppins_mat.jpg, and Scalloped Bow Garden uses the clean v108 photo.
  - Everything else uses the FYM photo (`matphotos/`, from the v117 mc chunks; v118 for new adds). Big photos get a 72% zoom; holiday cards show the whole mat.
  - Curled-corner photos are turned 90° so the corner sits under the tile box.
- **Known photo limits** (best photo we have): the Mahj & Moon mats (Bird & Pear Blossom, Italian Villa, Summer Bloom, Pastel Christmas Tree) are the brand's styled shots with tiles and racks on the mat. Sunday Vegan Leather (Chestnut) is a table shot. Mahj Squad Green Malachite is an angled table shot (the clean one is watermarked).
- **Figure HTML.** `build.py html <sha>` writes `pages/<page>.json` = {main:[...], holiday:[...]}. The markup is the same as the live cards:
  - `mm3-c` (+ `mm3-hc` on holiday cards), a jsDelivr image pinned at <sha>, "Mat by" linked to the brand's discount page when there is one;
  - a Retired tag + note for retired mats;
  - a Shop button with the FYM affiliate link (TdT via tdt_policy);
  - `code MAHJMATCH` for code partners;
  - "Match the tiles / Match the mat" rack links.
  - No blurb, so nothing she hasn't approved goes up.
- **Contact sheets** (looked at, every card): `qa/sheet-01..08.jpg`, page by page. Fixed after looking:
  - curled black corners on 11 Etsy/YOLO/Amazon photos now turn under the tile box;
  - long titles;
  - Mahjong Row racks.
  Page check: `preview.js` patched Amara, screenshotted at 390px, and the new main + holiday cards render like the live ones.
- **Image commit:** aa72f943 (jsDelivr 200 checked). `manifest.json` "sha" = the pin in every figure.

## OPS PASTE (Chrome; one tab, one page at a time; close the tab after). Claude does NOT paste in this run.
0. **Warm jsDelivr first.** Fetch every `https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@<SHA>/assets/cards/missed-nov07/<file>` until it returns 200; docs 59/73. If one stays 403, use `https://raw.githubusercontent.com/tiffanybrie/mahjmatchmaker-data/<SHA>/<path>` for it. SHA = `manifest.json` "sha".
1. **Get the code.** Load `missed_fix.js`, `holcss.html` and `pages/<page>.json` from `https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@<README commit>/site/livepatch/missed-album-picks-nov07/...`. Then: `window.PAGE=<json>; window.HOLCSS=<holcss text>`.
2. **Open the block.** In /config, open the page (`/<page>-mahjong-tile-matches`; holiday sections: `/holiday-mahjong-matches`) and click Edit. Open the code block that holds the grid:
   - album pages: the block with "Every <Set> match" (or "My <Set> matches");
   - holiday page: the block with `id="<sid>"`.
   After the pencil, **wait ~4s**.
3. **Run the fix:**
   `const v=document.querySelector('.cm-content').cmTile.view; const r=missedFix(v.state.doc.toString(), PAGE, <opt>);`
   - Album pages: `<opt>` = `{css: HOLCSS}`.
   - Holiday page: `<opt>` = `{sid:'<sid>'}`, e.g. `{sid:'tinselle-ruby'}`.
   Check `r.note`:
   - main +N / holiday +N match `manifest.json`;
   - the counts line was found (x1-x2 on album pages; vault albums have "N <Set> mat matches").
   Diff: only the grid tails, mm3-n numbers, count strings and (Brownstone Bloom, Papaya Spritz, Sunset) the new holiday section change.
4. **Apply.** `v.dispatch({changes:{from:0,to:v.state.doc.length,insert:r.src}})`. Type a space and then Backspace so Save turns black. Then Escape, Save, Exit.
5. **Verify with curl:**
   - the page carries the expected count of `assets/cards/missed-nov07/` images (`manifest.json` main + holiday);
   - the last main card's mm3-n = the grid total.
   Holiday sections: `python3 scripts/checks/holiday_numbering.py` (NEW-ALBUM-CHECKLIST holiday line).
6. **Re-check the whole list.** After all pages: re-run the finder (or `scripts/checks/coverage_check.py --refresh`, line album_picks). The missing count should drop to the not-mappable rest.

**Dry run.** `node preview.js <dir of live curls> <out>` applies missedFix to Nov 7 curls of every page and checks three things: +N cards, idempotent re-run, and a holiday section created where missing. All 52 pages pass (Nov 7, on the ~10pm curls). Count strings were found on every page except Sunday Tile Set, which has no count string.

**Order** (task priority): Larkspur pages first, i.e. every album in the Larkspur list (27). Poppins and Vivienne ride along on the same pages. Then the holiday sections, then the rest. Every page is one paste that carries all of its cards, so the order is just the page order in `manifest.json` "order".

**December 1994.** DESK has a "December 1994 redo (her RTS notes)" for Matches & Catalog (target Wed Nov 11). These 25 cards are her FYM yeses for the set; paste them with or before that redo, not instead of it.

## After the paste
- **FYM.** Nothing to do for the FYM pairs; they are already in the m-lists. Round-1 pairs go into FYM m-lists in 1.18 (builder/fym_fix_nov07/picks118.py, Matches & Catalog).
- **Racks.** The card racks for round-1 pairs live in `cards.json` if 1.18+ wants them.
- **Counts on /holiday-mahjong-matches.** The page-level stats (`mmhol-stats`) are not bumped by missedFix. Recount them by hand after the holiday sections go in.
