# 79 Mood Board Style: our standard layout (Oct 19)

**What this is:** the one layout we use for every "shop the look" board. Tiffany named it on Oct 19 after her Heron mat board ("Pinterest - Mahj Matchmaker - Heron Tablescape", Canva DAHFQIwAQjY). Her Mocha Bloom board is the other reference. Tile placement comes from her rentals deck (Canva DAHE1LGGXsM, page 3 "Pearlescent Tiles + Goldie Mat"). This is the North Star for Amazon, Instagram, Stories, Reels and Pinterest. **Make one board and reuse it everywhere. Don't redesign it for each channel.**

Scale and size order come from **doc 78 (Collage Rules: mat is the star)**: the mat is biggest, tiles sit over the mat, then racks, accessories stay visible, everything at believable scale. Styling rules come from **doc 71**. Fonts and colors come from **doc 38**. Use real product photos only, never generated tiles (**doc 66**).

Generator: `scripts/moodboard/render.py`, with zones in `scripts/moodboard/layouts.json` and boards in `scripts/moodboard/boards/*.json`. First board built with it: Rackin' Rudolph (`assets/moodboards/rackin-rudolph/`).

---

## 1. The look in one line
A Pinterest-style collage on a warm paper background. Real product cutouts overlap each other on purpose. The mat sits big and centered right. Every product has a short handwritten label with a little curved arrow pointing to it. It is never a grid and never a row of boxes.

## 2. Canvas sizes
| Use | Size | Notes |
|---|---|---|
| Amazon photo post, IG feed | **1080x1350** | master layout |
| Pinterest pin | **1000x1500** | its own zones (more air between items) |
| IG/FB Story, Reel | **1080x1920** | the 1080x1350 board centered, leaving about 285px clear top and bottom for the app's UI |

Background is paper `#faf3ea` (warm cream; white items like lamp shades and marble coasters show up on it). Per board you can switch to a lighter `#fffdfa` to match Heron.

## 3. Header (title and brand)
- Top center: **mahjmatchmaker wordmark** (navy `#054689`, the no-tag PNG).
- Board title in **Caprasimo**, using the season color (holiday: holly red `#b3202a`).
- Tagline in **Playfair Display italic** (holiday: pine `#1f5a3a`), e.g. "a reindeer holiday table".
- Kicker in small spaced-out **Bitter** caps, navy: Amazon "shop the look" · IG "shop the look · link in bio" · Pinterest "shop the look · mahjmatchmaker.com".
- No pill bars or banner buttons. The header stays light so the products are the design.

## 4. Zones by item count
Roles: `mat`, `tiles_pile`, `tiles_faces`, `rack`, `cloth`, `lamp`, `accent1-3` (dice box, coaster, dice dish, candles). The generator picks the layout that matches the item count (5, 7 or 9).

**7 items (standard; Rudolph uses this):**
- Mat: center right, about 57% of canvas width, just under the header.
- Tile pile (round crop): overlaps the mat's **upper-left** corner.
- Tile faces (flat rows): overlaps the mat's **lower-right** corner, tilted about 7°.
- Accent 1, the cute statement piece: big, down the left side.
- Bottom row: lamp in the bottom-left corner (small, never the dominant item), tablecloth as its own framed photo (about 340px, decent size), accent 2 (e.g. round coaster, about 236px).

**5 items:** mat, one tile shot (bottom-right corner), accent, lamp, cloth. Same positions with more air.

**9 items:** the 7-item layout plus a rack (angled, overlapping the mat's left edge, like the Heron racks) and accent 3 in the bottom-right. Everything shrinks about 5-10%. Cap labels at about 7. If it still feels crowded, cut an item; don't shrink the mat.

## 5. Tile placement (Tiffany, Oct 19)
- **Never** put tiles square in the middle or lower-center of the mat. That blocks the mat.
- Always offset tiles to a **corner**, overlapping the mat's edge, so the mat stays mostly visible and the board looks balanced.
- **Faces / "limited faces" shot** (flat rows of tile faces): always **bottom-right**.
- **Tile pile shot** (round crop): any corner. Bottom-right when it's the only tile shot; **upper-left** when the faces shot has bottom-right.
- Showing both (OMM always has a pile and a faces shot): pile upper-left, faces bottom-right. If that gets crowded, use one. Put faces upper-left only if space truly forces it.

## 6. Overlap rules
- Overlapping is the style: the tile pile, tile faces and rack overlap the mat's edges. Accessories may touch or overlap each other a little.
- **The mat is the star.** Keep at least about 75% of it visible. Never cover its center art. Don't put the cloth under the mat (doc 71: the 60x60 cloth is its own photo).
- Layering order, back to front: mat → accessories → tile pile → rack → tile faces → labels and arrows.
- Clean cutouts with no white halos (enclosed gaps, like the spaces inside antlers, must be removed too). Each item gets a soft drop shadow, not a hard outline.
- Round crops: tile piles and coasters (doc 71: one coaster, cropped round). Flat crops (tile faces) get softly rounded corners. Tablecloths get a white photo frame.
- One rack is enough (doc 71).

## 7. Labels and arrows
- Handwritten font for every product label. **Adventures Unlimited** is the Canva font Tiffany uses. The generator uses **Allison** (Google Fonts) as the closest free stand-in. In Canva, use Adventures Unlimited.
- Short and lowercase: "santa + reindeer mat", "gold bow lamp", "white marble coaster". Two lines at most. Never call Amazon items "vintage" (doc 71).
- Each label sits in empty space near its item, with a thin curved ink arrow (`#2b2623`, about 2.6px, open arrowhead) going **from the label to the item**. The arrow ends at the item's edge, not deep inside it.
- Labels next to tall items (lamp, tablecloth) can run vertically up the side, like Heron's "lamp" and "tablecloth". Those can skip the arrow.
- Leave breathing room: labels never overlap a product and keep about 15px from any item edge (doc 71).
- Label one tile shot per tile set. The second shot of the same tiles doesn't need its own label.

## 8. One board, every format
1. **Static (Amazon photo post / IG feed):** `--canvas 1080x1350`.
2. **Pinterest:** `--canvas 1000x1500` (kicker carries the URL).
3. **Story, tap to reveal:** `--canvas 1080x1920 --frames` writes frame 1 (header + mat), then one item and its label per tap. The item order in the board JSON is the reveal order: mat → tiles → statement piece → cloth → small accents → lamp.
4. **Reel (animated):** `--reel` writes an MP4: each item pops on (scale 0.82 → 1) with its label and arrow fading in, 0.7s apart, then holds 2.5s. Add music in IG per doc 43, end card per doc 45.
5. **Amazon version:** `--version amazon` uses the same board. Any item marked `"partner": true` is swapped for its `"amazon"` stand-in, or dropped if it has none. Partner pieces stay on the IG and Pinterest versions with our affiliate links.

## 9. How to make the next board (about 15 minutes)
1. Get product photos (official listing images). Cut out on transparent backgrounds, crop piles and coasters round, crop the faces shot tight. Save them to `assets/moodboards/<slug>/cutouts/`.
2. Copy `boards/rackin-rudolph.json`, then set the title, tagline, colors and items (role, kind, src, label, plus amazon or partner).
3. Run `python3 scripts/moodboard/render.py scripts/moodboard/boards/<slug>.json --version amazon --canvas 1080x1350` (add `--debug` to see zone boxes).
4. Adjust per board under `layout_overrides` in the board JSON. Don't edit the shared zones for one board.
5. Check the image yourself: no halos, labels clear of items, mat clearly the star, tiles in the corners, nothing tiny.

## 10. Condensed (on-mat) layout: only for small containers
Reference: OMM's Build Your Set tool (ohmymahjong.com/pages/shop-the-set). Vivienne mat fills a square box, tiles scattered over its upper-left, white racks lying over its lower-right.
- **Use it only** when everything has to fit inside one square container (some Find Your Match views, small mobile views). Everywhere else, use the full mood board style above. Rackin' Rudolph uses the full style.
- The mat fills the container at full size.
- **Tiles:** transparent cutout PNGs, deliberately **oversized** compared with real life so you can see them, offset to the **upper-left** corner.
- **Racks:** slightly **undersized** compared with real life so they don't overwhelm the mat, offset to the **bottom-right** corner.
- Goal: you see the products without the mat being hidden. This is the scale guide for tiles and racks against a mat in condensed containers.

---

## Amazon version rules
Checked Oct 19. Only things confirmed on Amazon's own pages are listed as rules. Everything else is marked **unverified, check**.

**Verified:**
- Influencer image uploads must be **.jpg/.jpeg/.png/.bmp, at least 105px wide, at most 5MB, over 72dpi.** Our 1080x1350 JPG is fine. ([Image upload guidelines for Amazon Influencer Program](https://affiliate-program.amazon.com/help/node/topic/G9NSHK62ULK4ZE2V))
- The Influencer Program Policy gives Amazon a license to the influencer's **"name, photo, logo and other trademarks"** in submitted content. So Amazon expects your own branding to appear; it is not banned. **We keep the mahjmatchmaker wordmark on the Amazon version.** ([Associates Program Policies / Influencer Program Policy](https://affiliate-program.amazon.com/help/operating/policies))
- **Amazon's own marks:** "You may not alter any Amazon Mark in any manner." Don't put an Amazon logo or smile on the board. Saying "Amazon" in plain words is fine. (same page, Trademark Guidelines)
- **Altering Amazon product images:** the Associates policy says "You will not add to, delete from, or otherwise alter any Program Content in any way", except resizing an image while keeping its original proportions. **This matters:** our boards cut out and round-crop Amazon listing photos. Program Content is defined as content from the Creators API, PA API, data feeds and Product Advertising Content. Whether a listing photo you downloaded and posted inside an Influencer photo post counts as "Program Content" is **unverified, check**. The safest version uses Tiffany's own photos of the products. ([Associates Program Policies, section 6(a)](https://affiliate-program.amazon.com/help/operating/policies))
- Community features (which may cover posts): no links to sites outside Amazon, no URLs with affiliate or referral tags, and no content whose main purpose is promoting an outside company or website. **So: no "mahjmatchmaker.com", no URLs, no discount codes on the Amazon version.** The kicker says only "shop the look". ([Amazon Community Guidelines](https://digprjsurvey.amazon.com/csad/help/node/GLHXEX85MENUE4XF))

**Unverified, check:**
- Whether Influencer photo posts must be photos you took yourself, or whether collages of listing images are allowed or get rejected.
- Whether text overlays or logos lower a photo post's reach or get it rejected in review.
- Whether a printed (non-clickable) URL counts as an "external link".

**Amazon list (what changes on the Amazon version):**
1. Amazon items only. Partner pieces get swapped for their Amazon stand-ins in the board JSON (`"partner": true` + `"amazon": {...}`).
2. No URL, no discount code, no "link in bio". Kicker = "shop the look".
3. No Amazon logo.
4. The wordmark stays (allowed per the license clause above).
5. Don't call items "vintage" (doc 71). Use the product's own name.
