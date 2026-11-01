# v112 patch set: MATCH-INBOX sweep (Nov 1, overnight)

This folder holds everything the Nov 1 sweep of `docs/MATCH-INBOX.md` prepared for the next FYM build. Nothing here has been built or published. Line-by-line status is in `docs/research/inbox-sweep-nov01.md`.

**Tested:** the whole chain ran on a throwaway copy of b110 in a sandbox repo copy, so the real repo's flags and locks were untouched.
- `gate_nov01.py`: PASS.
- `builder/fym_gate.py`: **PASS** (328 sets / 283 visible / locks 1011 mats).
- The usual v97 warnings remain:
  - [89] lists 14 angled photos still left after `v98_matflat` (38 at v97).
  - [90] still lists 274 mats; `gallery_rows112.py` covers them.

## Order (on top of the v111 accounts build)

```
bash builder/fym_fix_nov01/build112_data.sh <b111 dir> <b112 dir>
```
Then do the usual tail from `build109.sh` / `build110.sh`:
1. Bump the version string.
2. `strip_inline_img.py` + `v105_imgout.py`.
3. Make the site + artifact copies.
4. Independent QA (phone + desktop).
5. Publish to BOTH places.

| step | script | what it does | inbox lines |
|---|---|---|---|
| 1 | `adds112.py` | Adds 16 mats (spec `config/fym-adds-nov01.json`, photos `assets/mats/v112/`): LBB Tropicana, Butterscotch Floral (+Simple Middle), Vibrant Vortex (+Simple Middle). Britt Mills Calista / Colorful Chinoiserie / Daphne / Aria / Bella leatherette + Emerald Mirage neoprene, with "Also available in …" on the twins. Sunday Green Gingham / Blue Gingham / Blue Rattan. Fait à Main Texas Mon Amour Chocolate Blue, and Round Top Mon Amour (HIDDEN + Questionable list: close-up photos only). Relinks Sunday Vegan Leather (the old URL 404s). Adds 12 racks HIDDEN with `pending_review` (spec `config/fym-rack-adds-nov01.json`). | Oct 31 Tropicana, Crystal Palace, Sunday relink, MR solid wood; Oct 30 Britt Mills ×5, LBB ×3; Oct 29 Sunday ×3; Oct 28 MFM Poppy Red; Oct 27 Bella; Oct 26 FAM Round Top |
| 2 | `fym_fix_oct30/v104rank.py` | Colour-ranks the new mats (gate [107]). | |
| 3 | `cr112.py` | Keeps each set's top 5 (gate [76]). | |
| 3b | by hand, before unhiding racks | For each `pending_review` rack: cut ONE rack from `src_img` (brand photo; the MR solid-wood photos are infographics, so crop the rack only) and look at it on white + navy (`builder/fym_rack_images.py <build> --sheet`, then `--approve`). Set `im`, drop `hid` + `pending_review`. Gate [137e] fails if a pending rack is visible. | rule 6b |
| 4 | `fixes112.py` | Retires Dapper 2. MRC Scalloped Tortoise loses `sm`. YMI Ivory ×3 become one "Ivory Stripes" set with a real photo, and the Oct 26 "coming soon" configs are updated at build time. PLM Sugarplum Plaid / Blue Stripes / Blue Blooms become holiday (Oct 29 calls) and their locks are updated. Chinoiserie Cheer is unhidden on its flat photo. Poppins goes onto her 15 swipe-YES sets that have an album/book. `ncn` is set on every non-partner brand ("No code available at this time"). The MS rack name is fixed. | Oct 26–31: Dapper, tortoise, Ivory, holiday calls, Chinoiserie Cheer, Poppins, ncn, (retired) |
| 5 | `rackfit112.py` | Sets `R.len` (rack length) and `T.tw` (tile width) from `config/fym-rack-fit-nov01.json`, drops every `sm`, and adds "(18.5 in rack)" to the shop list. | Oct 26 7:37 / 7:39pm |
| 6 | `ui112.py` | A: no white copy behind card titles. B: shop-by-colour partner / non-partner sections in both doors. C: brand-menu copy "Code MAHJMATCH works at brands marked ♥" + ♥ on partners. D: Tigre de Tartán is link-only, with no code text next to its name. E: rack fit by tile size. F: MRC tortoise before Hawksbill. G: BACKG loses the dead "Glitter Glow" and gains December 1994 in Holiday. | Oct 27 titles, Oct 31 colour sections, Oct 29 menu copy, Oct 30 TdT, Oct 26 racks, Oct 28 Glitter Glow / Dec 1994 |
| 7 | `fym_fix_oct25/v98_matflat.py` | The Oct 26 WIP: 21 angled mat photos flattened (all looked at back then). | Oct 26 6:25pm (gate [89]) |
| 8 | `gate_nov01.py` | New checks [130]–[137]. Merge them into `fym_gate.py` after v111 lands (it was mid-edit by the accounts build tonight). | |
| 9 | `fym_gate.py` | Full gate. | |
| 10 | `gallery_rows112.py <b112> --write` | **After** the FYM build passes: drafts 274 Mat Gallery rows (gate [90]) plus 640px photos. Then rebuild the staged gallery (`site/livepatch/matgallery/build_v5.py`), run gates [13] / [90], and paste it. The Mat Gallery build must also re-apply the Oct 29 holiday calls (Sugarplum Plaid / Blue Stripes / Blue Blooms in Holiday). | Oct 26 6:25pm (gate [90]) |

## Notes

**Rack lengths, researched Nov 1** from each product page (`/products/<handle>.json`); the source is per row in `config/fym-rack-fit-nov01.json`.
- **18.5":** Oh My Mahjong, Mahjong Row & Co. (except the Scalloped Tortoise), Bam Bird Lucite / acrylic, Bam! white acrylic with attached pusher, Virora hinged, Royal Mahjong Society.
- **18":** YMI.
- **19":** Bam Bird wood, Bam! white wood, Virora wood.
- **20":** everything else, including M&M (all 20" "extended length"), MR, MFM, PLM, B&B, Bespoke and Mahj Mood.

**The fit rule.** Tiles stand side by side, so it is the tile **width** that matters.
- OMM 0.87", MRC 0.91", Bam Bird / Virora / YMI ~0.9" and Mahjong Studios 24 mm are standard and fit 18.5" racks.
- Sunday, PLM, MFM, Mahj Mood, Amahj, M&M, B&B, Mac + Miller, LMO, Charleston, YOLO and Mahj Squad are 1"+. Mahj Squad's own page says "large tiles require racks at least 19 inches".
- Bespoke and Miss Mahjong (her call) are also large.
- Tonight's v110 offers 21 short racks with large-tile sets (Bam Bird lucite, YMI, Virora hinged, Royal Mahjong Society). Step 6E stops that.

**Tigre de Tartán copy.** Her Oct 30 wording was "save 10% through our link". Gate [4] / rule 7 forbids a hard-coded % in UI text, so the copy says "Save at Tigre de Tartán through our link" / "Save through our links".

**Not done here:**
- The two-colour coordination bonus (Oct 27 11am). It is a ranking change across every deck and needs its own build + QA.
- The OMM / TdT rack-photo format and the PLM chartreuse rack. Those need eyes on the photos.
- Etsy shop names. Etsy blocks the shell; this is a DESK item for a browser chat.
