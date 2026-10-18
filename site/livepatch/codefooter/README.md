# Code-footer swap: no more "SHOP THE MATCH" footers (Oct 18)

Her rule: every match card says SAVE WITH CODE : MAHJMATCH. Coquette and Maison Mahj cards get no code, and PAPERPARTNER never appears.

Nothing here is live yet. Each swap needs Tiffany's in-chat approval.

## What's in this folder
- `<slug>.html`: the page's current live code block (taken from the live page on Oct 18, ~08:40 ET), with only the old-footer card URLs swapped. It's ready to paste as a whole-block replacement.
- `<slug>.json`: the same change as a minimal list of old URL → new URL swaps, plus the block id. This is the safer way to apply it: run `__fix` with a regex per URL instead of replacing the whole block.
- New cards are pinned to commit d4ee12ce47f77d88d4806425ca83553db3dd28ed under `assets/cards/codefooter-v1/cards/`.
- jsDelivr sometimes returns a one-off 403 ("package size exceeded") on a file it hasn't cached yet; a retry gives 200. All 34 URLs returned 200 at 09:00 ET. Curl each one before swapping.
- The Polo Club cards point to the **corrected-rack** versions (`codefooter-v1/cards/polofix-v1/`). Applying this swap replaces the separate `site/livepatch/polofix/` swap; don't apply both.

## Pages → cards swapped (14 pages, 34 card slots)
| Page | Cards |
|---|---|
| /holiday-mahjong-matches | 16 |
| /cypress-forest-mahjong-tile-matches | 2 |
| /heritage-2-0-mahjong-tile-matches | 2 |
| /jade-mahjong-tile-matches | 2 |
| /malachite-mahjong-tile-matches | 2 |
| /nantucket-mahjong-tile-matches | 2 |
| /amara-mahjong-tile-matches | 1 |
| /gatsby-mahjong-tile-matches | 1 |
| /la-fete-mahjong-tile-matches | 1 |
| /limoncello-mahjong-tile-matches | 1 |
| /red-mahjong-tile-matches | 1 |
| /seabreeze-mahjong-tile-matches | 1 |
| /sierra-mahjong-tile-matches | 1 |
| /sorbet-mahjong-tile-matches | 1 |

## Not in these swaps
- **/blog/holiday-mahjong-table:** the pending new Polo post block (`site/livepatch/oct18b/tablescape.html`) already uses the `-code` card. Approving that post fixes it.
- **Coquette cards** (9 on /coquette-mahjong-tile-matches) and the **Maison Mahj Chalet** card (on /holiday-mahjong-matches): left as is, because they get no code. They still say "SHOP THE MATCH : MAHJMATCHMAKER.COM". Tiffany needs to decide what their footer should say instead.
- **Shop-the-look boards** (Polo board "shop the look · mahjmatchmaker.com"; the Raven board already says "code MAHJMATCH"): these are boards, not match cards.
- **Pending albums:** the cards for the Sunday Tile Set album (v3, 26 cards) and the Polo fix already have code-footer versions in `codefooter-v1/cards/`. Use those whenever those pages get pushed.

## Found while checking (not fixed here)
The "Rack matches" captions under the holiday cards don't match the racks printed on the cards. Example: Jade + The Polo Club. The caption says "B&B Light Pink · B&B Lavender · M&M Scalloped Beechwood". The card shows Peace Love Oak, Miss Mahjong Jade & Brass and Miss Mahjong Opal & Brass for the tiles, and B&B Dark Navy, Evergreen, Wine and Sunday Cola for the mat. Per doc 60, the captions need regenerating from the cards' rack lists.

## Update: rack captions fixed (Oct 18)
The holiday "Rack matches" captions in these 13 blocks are now rebuilt from each card's racks: "Match the tiles: … / Match the mat: …". That's 238 captions:
- holiday 109
- nantucket 24
- jade 19
- malachite 16
- heritage-2-0 15
- gatsby 12
- amara 10
- la-fete 9
- cypress-forest 8
- seabreeze 6
- sorbet 4
- limoncello 3
- sierra 3

Whole-block paste: the .html already has the fixed captions.

Swap-list route: run `caption_swaps` after the URL `swaps`.

Other pages are in ../rackcaptions/.

Unrelated typo, not fixed: the Polo button reads "Shop the The Polo Club Mat".
- The .html blocks fix the button text 'Shop the The Polo Club Mat' to 'Shop The Polo Club Mat'. The .json swap lists don't include that fix, so prefer the whole-block paste.
