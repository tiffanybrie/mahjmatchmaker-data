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

---

# Round 2: Tiffany's review of the live homepage (Oct 21, 12:22). STAGED, not live yet

**What to paste:** `live-paste_block-yui_3_17_2_1_1791134152790_5194.html`. It replaces ALL of block 5194's code, which is the callout pasted on top of the big block. `build.py` now writes this file too.
**Rollback:** `source/oct21-1222/before_live_block-yui_3_17_2_1_1791134152790_5194.html`. This is the exact code live at 12:25, taken from the rendered page, and it matches the 9:42 callout + "\n" + block byte for byte.

| # | Change | Where |
|---|---|---|
| 1 | Callout now reads exactly "Use code MAHJMATCH to save at 30+ partner brands", with no %. Button: "Meet our partner brands →", still linking to /mahjong-discount-codes. | build.py callout |
| 2 | Shop by Brand: "...saves you 10% or more." "10% or more" never splits across lines (nowrap), and `text-wrap:balance` keeps it from orphaning. At both 390 and 1280 the wrap is "...each with a guide and the / MAHJMATCH code that saves you 10% or more." | build.py step 5 |
| 3 | "Spring & summer table" chip removed. The other 9 chips stay. | MORE list |
| 4 | Featured Halloween card uses the new board v7 web card (1200x900), shown whole (4:3, contain) at every width. | `assets/blog/night-of-the-raven/night-of-the-raven-shop-the-look-v7-card-1200x900.jpg` (jsDelivr @9b3b68f) |
| 5 | How It Works step 3 gets an image. It's injected into the step 3 fluid grid at the same size and position as step 1's image block (desktop cols 2-13, 522x382 at 1280). On phones it sits on top like steps 1 and 2 (343 wide). It shows a fan of the newest album covers on blush. | `assets/site/home/how-it-works-3-new-matches-first.jpg`, made by `make_step3_image.py` |

Board v7: `scripts/moodboard/boards/night-of-the-raven.json` plus the new `1200x900` canvas in `scripts/moodboard/layouts.json`. Cutouts are in `assets/moodboards/night-of-the-raven/cutouts/` (MRow product images, Amazon listing images, and the plum cloth crop from v6). The render follows doc 79/78:
- The mat is the star.
- One rack.
- Tile pile upper-left, faces lower-right.
- The lamp and raven dice dish are full-size and far apart.
- The lace and deep plum cloths are shown separately (her Oct 17 pin note).
- Handwritten labels, Title Case title.

Render commands:
- `python3 scripts/moodboard/render.py scripts/moodboard/boards/night-of-the-raven.json --version web --canvas 1080x1350`
- the same command with `--canvas 1200x900`

**Blog post image (staged, NOT published):** /blog/halloween-mahjong-table shows v6 from jsDelivr @e4d8ced. To swap it, replace that `src` with
`https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@9b3b68fe8ca3ab3c045a8e0f5563c8ca9045069b/assets/blog/night-of-the-raven/night-of-the-raven-shop-the-look-v7.jpg` (1080x1350, warmed, 200).
Its og:image, the Pinterest pin (`config/pinterest/queue.json`) and the ShopMy cover still use v3.

## Footer / bottom section (Squarespace text blocks, edit in the UI)
Rollback copies are in `source/oct21-1222/before_text_block-*.html`.
- **Album link list:** text block `yui_3_17_2_1_1773273860714_22142` (homepage only, section `69b21b055acd7b7710c89838`, "Looking for the perfect mat and rack..."). Replace its third paragraph (the 8 inline "X Mahjong Tile Matches" names, only Jade linked) with one centered link: "Browse all tile match albums →" pointing to /mahjong-tile-matches.
- **Site footer email:** delete the text block `e8109705861a998b09f0` (`<h4>mahjmatchmaker@gmail.com</h4>`) from the site footer.
- **Contact link:** in footer text block `bb7bd9c8aa5441149846`, the line becomes `Private Lessons | Rentals | Contact`, with Contact linking to /contact.
- **/contact page:** none exists today (/contact and /contact-us both return 404). Create a page "Contact" at /contact, not in the main nav. Add a heading ("Say hi!" / "Contact Mahj Matchmaker") and one Form block with Name, Email and Message (all required). Set Storage to Email → mahjmatchmaker@gmail.com and the submit button to "Send". Post-submit message: "Thanks! I'll get back to you soon. 💗 Tiffany".

## Round 2 LIVE (Oct 21, ~1:00pm)
- Block 5194 replaced with `live-paste_...5194.html` (commit 0731398, includes the QA fix: Raven blurb now "Terracotta marble tiles (those backs!) on the Mahjong Row & Co. Mocha Bloom Dark mat, with translucent plum racks and black lace. ..."). curl of the live page: block content is byte-identical to the staged file.
- Album list text block (22142): 8 inline names replaced by one centered link "Browse all tile match albums →" to /mahjong-tile-matches.
- Site footer: email block e8109705861a998b09f0 deleted; footer line now "Private Lessons | Rentals | Contact" (Contact → /contact).
- New page /contact (Not Linked): "Say hi!" + form (First/Last Name, Email, Message, all required), button "Send", post-submit "Thanks! I'll get back to you soon. 💗 Tiffany". Notifications go to the account default email (tiffanybrie@gmail.com), not mahjmatchmaker@gmail.com.
- Hero section 69b1d01489d0f8016ee3d59f not touched.
- Staged, not applied: `header-nav-overflow-fix.css` (desktop sideways scroll).
- Screenshots: qa/round2_live_*.

## Holiday banner centered on desktop (Tiffany Oct 21 1:16pm). LIVE ~1:40pm
- Cause: `#mmhome section{margin:0 0 64px}` (id specificity) overrode `.mhx{margin:0 auto 38px}`, so the 1020px card sat flush left in the 1180px column (50px left / 210px right at 1280). Inside it, the heading was centered by `#mmhome h2` but the eyebrow, count, blurb and button were left aligned.
- Fix (build.py step 7): `@media(min-width:761px){#mmhome section.mhx{margin-left:auto;margin-right:auto}.mhx-txt{text-align:center}}`. Phone (<=760px) unchanged; bottom margin stays 64px, so no section changes height (page height 10666 / 8333 / 8502 at 390 / 1280 / 1440, same as before).
- Published as a one-line insert into block 5194 in the editor; the editor content hash matched the rebuilt file, and curl of the live page contains the file byte for byte.
- Screenshots: qa/holiday_center_{before,after,live}_{390,1280,1440}.jpg
