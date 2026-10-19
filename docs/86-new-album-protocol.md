# 86 New Tile Set Launch Protocol: color analysis FIRST (Oct 19, rewritten Oct 19 evening)
Tiffany, Oct 19: "We need to establish the protocol for a new album and make sure that we follow it next time." The Papaya album got built before anyone looked closely at the tile photos or the brand's description. Then she laid out the full order of operations herself. This is the order from now on. Read alongside doc 77 (The Gut Check), doc 76 (Color Theory), doc 88 (Color System) and docs 48/55/57 (Rack Rules).

**Wording:** layered tiles have **layers**, never "stripes."

## Order of operations

### 1. Grab the images (Claude, the moment they appear)
- Save every product image of the new set to her Dropbox right away. Brands swap flat renders for photoshoot images later, and the flat render is her clean card image.
- No album is built from teasers or Instagram stories alone. Wait for the brand's product page, which is our source of truth.
- Save the brand's own color words from the product description (e.g. OMM on Papaya: "papaya orange, soft lavender, and fresh green"). Our public copy never contradicts them. Also save any "behind the tiles" layer graphic if the brand posts one.

### 2. Color analysis (Claude, the first real step)
- Measure the colors from the brand's photos: backs, every layer, and faces.
- **Sampling rule:** use the brand's back + side tile photo from their website (the one shoppers see). Take 3 spots per layer (top, middle, bottom) and use the median. Save the photo to assets/tiles/backs/. Don't sample our own darker photos: Papaya's lavender came out subdued that way.
- Output: **color card** (brand color names, hex, our nuance in small text) + **color wheel** (where each color sits) + a short notes page: clean vs earthy (doc 76), warm vs cool, which mat colors should work, and anything odd in the photos.
- Watch for brightened brand photos. If the tiles are in hand, the real tiles win.

### 3. Auto-generated starter content (Claude, right after the color analysis)
Everything that only needs the colors gets drafted straight away:
- Color card, color wheel, and the "her best features" favorite-tiles graphic.
- Dating profile (story) + introducing carousel, with **3 placeholder matches** picked from the color analysis and clearly marked as placeholders.
- Countdown story frame, if the launch date is known.
Placeholders get swapped for her real top matches after step 6.

### 4. Tiffany reviews the color analysis
- She studies the notes and zooms in on the brand's images herself. We go back and forth on the color read only. Once she's happy, the color analysis is **locked**, and every later piece reads from it.

### 5. Match album: mats (Claude curates, Tiffany decides)
- Claude pre-sorts the mat swipe book using the measured mat colors (config/mat-color-measured.json) plus the color tags, so the book opens with the strongest candidates instead of everything.
- Swipe book order: TNT (Tiles & Tablescapes) recommended mats first, labeled "TNT rec · mat name · brand", then the color-profile matches (doc 51).
- Tiffany swipes and adds anything Claude missed, anything that looks off, or anything she remembers that isn't in the catalog. Missing mats go on the partner catalog list (doc 65).

### 6. Order the album + pick best matches (Tiffany, with the doc 77 Gut Check)
- Final order, lead image, and top matches ("Tiffany's matches").
- The placeholders from step 3 get replaced with these.

### 7. Racks for every final mat (Claude matches, Tiffany approves)
- Claude matches racks to each final mat using the Rack Rules (docs 48, 55, 57; e.g. no B&B woods).
- This gets faster over time: saved mat→rack pairs are reused, so only new mats need fresh rack matches.
- Tiffany checks and approves the rack picks.
- If racks change later, redo EVERY asset that shows them (doc 60).

### 8. Final checks (Claude)
- Current logo only (no old Mahjong Social Club badge), branding, set and brand names spelled right, color words match the brand, code MAHJMATCH correct, and affiliate links work. No "I may earn a commission" on visuals (#affiliate goes in hashtags only).

### 9. Publish the album (Tiffany's yes in Ready to Ship)
- Album page on mahjmatchmaker.com + album cover. Do the jsDelivr warm-up before any block goes live (doc 73). A Yes in Ready to Ship approves only that item (doc 74).

### 10. Find Your Match entry (Claude)
- Add the set to Find Your Match with Tiffany's matches, color tags (doc 50), and racks.

### 11. Social content gets built (docs 69, 89)
- Instagram grid row (Rule D): best match → dating profile → album cover. Grid posts can go up as short reels with the still as the cover, for reach.
- Stories: share each grid post to stories with a link sticker (Tiffany does this, since Planoly can't add link stickers), plus the countdown and "She's live!" frames.
- Hotline/skit reel with her song (Tiffany adds the music).
- Pinterest pins (auto, via Planoly), a Facebook Page post (links are clickable there), and a Facebook group post (from her account, her yes per post).
- Captions end with "link in bio" + code + #affiliate. The bio link points to the new set during launch week.
- Everything goes into Planoly as drafts. Nothing is scheduled without her yes.

### 12. After launch (Claude)
- Watch the Find Your Match swipe/save data for the set (doc 64).
- When new mats come out later, check them against this set's color analysis and suggest additions.

## Who does what (short version)
- **Claude:** images, color analysis, starter content, pre-sorted swipe book, rack matches, checks, website/FYM entries, and all social drafts.
- **Tiffany:** approve the color read, swipe + order the album, approve racks, say yes in Ready to Ship, post the music reels and link-sticker stories, and say yes to scheduling.

## Future idea (Tiffany)
- Buy launch tiles early when cash allows (resell after) so colors can be checked in hand. OMM photos can run bright.

## Papaya Spritz check (Oct 19)
- From OMM's back + side photo (3 spots per layer, median): Papaya #DE7E30 (27°) · Lavender #A8A3E1 (245°) · Light lime #C8D7A5 (78°). The color wheel, color cards and dating profile all use these.
- The purple layer is a soft, blue-leaning lavender. Lavender vs periwinkle is semantics; we publish "lavender" (OMM: "soft lavender").
- The green layer was renamed "Light lime" (OMM: "fresh green").
- Matches unchanged: periwinkle mats still work because the layer leans blue.
