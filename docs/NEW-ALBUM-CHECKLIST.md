# New album: order of operations (Tiffany, Oct 26 12:46pm: "I can't be the one who's expected to remember all these things")
Run this list top to bottom the day an album goes live. Every item is Claude's job unless marked YOU. Tick each one in the album's HQ Albums row (hq/albums) and log in docs/ANSWERS.md.

## 1. Before it's live
- [ ] **Before the swipe book (code-enforced):** colour card built (config/colorcards.json / assets/colorcards/<set>/), TNT recs searched and saved in config/tnt-recs.json, book built from the WIDEST pool (full FYM catalog, measured colour shares) with FYM photos; `python3 scripts/swipe/book_gate.py <book>` = PASS (build_book.py / finish_patch.py refuse otherwise).
- [ ] Her card order saved (order page) and her yes on the cover.
- [ ] Album page built + warmed on jsDelivr; color card first (doc 86b).

## 2. Go live (same hour)
- [ ] Album page published on Squarespace; curl 200; title/SEO set.
- [ ] /mahjong-tile-matches: album tile added at the top (newest first).
- [ ] Its color pages (e.g. /brown-mahjong-tile-matches) list it.
- [ ] **/links "latest album" card:** scripts/covers/holiday/links_build.py → `NEWSET=(slug, name, brand, 'Our latest album, now available · code MAHJMATCH')`, add `assets/links/v2/feature-<slug>.jpg` (896x492) + `album-<slug>.jpg`, put the album first in links_pop.json, rebuild, pin + warm jsDelivr, paste the /links code block (Squarespace page "Mahj Squad Discount Code (Copy)", url /links). Find Your Mat-ch stays FIRST, the album card second.
- [ ] Find Your Mat-ch: the set's `album` link points to the new page; tile photo = album photo (canon_tiles.py); gate + QA; publish to artifact AND website copy.
- [ ] The brand's guide page (/<brand>-discount-code): album link added to its albums section.
- [ ] Google: request indexing for the album page (+ the brand page if changed).
- [ ] HQ Albums tab: stage → live.

## 3. Social (Planoly; reminders = one key line first, full steps sent in chat)
- [ ] Instagram row (doc 89 Rule D): intro carousel → "It's a mat-ch!" → reel (album cover as reel cover). Every slide also to stories, brand @tags + Tag people + collaborator invite.
- [ ] Story with a link sticker to the album.
- [ ] Pinterest: album pins queued (docs/PINTEREST.md).
- [ ] Facebook group announcement (doc 82 format): EVERY album cover as its own photo (each album gets its moment), plus a Find Your Mat-ch screenshot/promo graphic of the set in the app.
- [ ] A separate Find Your Mat-ch tie-in post (group + IG/FB Page): the set in the app, "try it in Find Your Mat-ch" (Tiffany Nov 3 2:15pm: don't make her ask for every marketing angle).
- [ ] Album "now available" wording swapped everywhere the old album said "coming".

## 4. People who asked
- [ ] Album-request contacts for this set get the "your album is live" email (Squarespace automation; doc 54).
- [ ] **"New albums are live" email to All subscribers (the homepage "Get New Matches First" signups)** the same day: template `new-albums` in site/email/build.py (Tiffany Nov 3 1:59pm: Brownstone Bloom went live and no email went out). Build it as a Squarespace campaign; once she has approved the template, Claude sends (docs/EMAIL.md). Batches (e.g. holiday albums) = one email. The album launch is NOT done until this line is checked and logged in HQ.

## 5. The album it replaces
- [ ] The previous "latest album" card leaves /links (it stays in the album strip).
