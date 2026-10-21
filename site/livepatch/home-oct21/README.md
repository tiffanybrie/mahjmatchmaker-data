# Homepage fix, Oct 21 (Tiffany 9:17, 9:18, 9:19). STAGED, not live

Page: https://www.mahjmatchmaker.com/ (Squarespace home page).

## Files
| File | What to do with it |
|---|---|
| `block-yui_3_17_2_1_1791134152790_5194.html` | **Replace** the entire code of the existing code block `block-yui_3_17_2_1_1791134152790_5194` (the big "#mmhome" block: New Tile Match Albums, Holiday, Shop by Color, Guides, Shop by Brand). It is in page section `69b2303d5670f85709f47c87` (the "3. Get New Matches First" section). Its script moves it on screen to just under the hero. |
| `new-block-mahjmatch-callout.html` | **New** code block: the MAHJMATCH callout plus the partner logo ticker. |
| `source/before_block-...5194.html` | The live code as of Oct 21 9:20, for rollback. |
| `build.py` | Rebuilds both files from `source/`. |
| `qa/` | Screenshots. |

## Steps (main session, in Squarespace)
1. Edit the home page. Open code block `block-yui_3_17_2_1_1791134152790_5194` and select all of its code. Paste the full contents of `block-yui_3_17_2_1_1791134152790_5194.html` in its place. Save.
2. Add a new **Code** block in the same section (`69b2303d5670f85709f47c87`). Drop it on top of block 5194 or any small empty spot; its fe-block hides itself (`.fe-block:has(.mmcb-mark){display:none}`), so it takes no room in the grid. Paste `new-block-mahjmatch-callout.html`. Turn off "Display Source". Save.
   - Simpler option that also works: paste `new-block-mahjmatch-callout.html` at the **very top** of block 5194's code, above everything else, and skip the new block. Both files are self-contained.
   - The new block can go anywhere on the page. On DOMContentLoaded its script moves `#mmcode` to just before `#mmhome`, which puts it right under the hero. If `#mmhome` is missing, it goes after the first page section instead.
3. No Squarespace block moves are needed. The blog section moved up inside block 5194's own code.
4. Log out (or use a private window) and check at phone width:
   - Order is: hero, MAHJMATCH callout with logo ticker, New Tile Match Albums, From the Blog, Holiday Mahjong Matches, Shop by Color, Shop by Brand.
   - "All Albums by Color" is gone.
   - The Pink swatch opens /mahjong-tile-matches#color-pink.

## What changed
- **All Albums by Color removed** from the home page: the whole `div.mmalb-home`, 71 album cards and its CSS.
- **Shop by Color is kept.** Each swatch now goes to its colour section on the Mahjong Matches page: `/mahjong-tile-matches#color-pink`, `#color-red`, `#color-blue`, `#color-green`, `#color-purple`, `#color-yellow-orange`, `#color-brown`, `#color-ivory`, `#color-neutral`. Every anchor exists on the live page, and a test landed exactly on the heading. **Holiday** still goes to `/holiday-mahjong-matches`, because the `#color-holiday` anchor on the matches page only links on to that page. The subtitle now reads "Tap a color to jump to every tile set I've matched in it."
- **"Shop the Guides" is replaced by "From the Blog"** and moved up to sit right under New Tile Match Albums, above the Holiday banner, so Halloween comes before Christmas. Contents:
  - Featured wide card: Night of the Raven, the Halloween table on the Mocha Bloom Dark mat.
  - Four cards: Holiday Table Without a Christmas Mat, Christmas Tiles/Mats/Racks, Buying Guide, Most Versatile Tile Sets.
  - "More on the blog" chips linking the other 10 posts.
  - A "Read the blog →" button.
- **Shop by Brand:** its old sprite logo ticker ("Plus more partner brands") is removed, because the new callout carries the full ticker near the top. The 8 brand cards and the "All mahjong discount codes" button stay.
- **New MAHJMATCH callout:** "Use code MAHJMATCH to save 10% or more at our partner brands", linking to /mahjong-discount-codes. Under it is the same 33-logo ticker as /mahjong-discount-codes: same logos, order, links and aspect ratios, with a main row plus a `.dup` row.
  - Classes are prefixed `mmcb-` and scoped to `#mmcode`, so they don't clash with `.mmtk` or `.mmh-*`.
  - The logos are the discount page's inline webps saved as files under `assets/brands/ticker/` and served from jsDelivr pinned to commit `604c093c` (warmed, all 200). The I Love Mahj png is a local copy. This keeps about 390KB of base64 out of the home page HTML.
  - It pauses on hover/focus. With prefers-reduced-motion it stops scrolling and wraps into a static logo grid with the dup row hidden.

## QA (Playwright, local copy of the live page with the blocks swapped)
- Page height at 390px: 16922 → 10422 px. At 1280px: 14265 → 8286 px.
- At 390px there is no sideways scroll (scrollWidth 390).
- At 1280px the scrollWidth is 1492 both before and after. That overflow comes from the site header nav (`.header-nav-list`) and is **not** caused by these blocks.
- Console: only the existing Squarespace message `requestStorageAccess: Permission denied` (also there before).
- All 58 image URLs and all 58 internal links in the two files return 200.
- Shop by Brand card photos (Shopify CDN) show blank in headless screenshots before and after. Their markup is unchanged and curl gets 200 for each.
- Fix to make on /mahjong-discount-codes (not done here): its ticker titles show "Let&amp;rsquo;s" (double-escaped). The home copy uses &rsquo;.
