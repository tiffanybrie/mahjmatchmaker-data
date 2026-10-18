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

## LIVE — Oct 18, ~11:20–12:05 ET (Tiffany approved in chat: "Approve swapping in the MAHJMATCH cards on the 14 live pages.")
All 14 pages swapped as whole-block replacements, using the blocks at commit e593f10. That's the c3ae3a3 card pins (current logo tab, banned B&B woods patched) plus 23 rack captions updated to match the wood-patched cards.
- Before each swap, the live block matched the base: same cards and titles apart from the planned swaps.
- After each swap, curl confirmed every figcaption and every card URL in the block is on the live page:
  - amara 49/49
  - cypress 39/39
  - gatsby 67/67
  - heritage-2-0 81/81
  - holiday 109/109
  - jade 59/59
  - la-fete 30/30
  - limoncello 16/16
  - malachite 53/53
  - nantucket 41/41
  - red 5 imgs
  - seabreeze 33/33
  - sierra 34/34
  - sorbet 18/18
- Holiday, Amara and Red were checked in a browser at 390 and 1280: no broken images, no sideways scroll.
- Red and Sorbet were first swapped with the older f94d4a1 pin, then re-applied with e593f10.
- Some cards still print a banned wood, and their captions still name it to match, because those cards weren't wood-patched yet:
  - Amara + Clara's Dream (Almond)
  - Jade + Blue Christmas (Tudor)
  - Heritage 2.0, Dear Santa and December 1994 + Festive Plaid (codefooter-v1/holiday-v4, Tudor)
  - Nantucket + Hearts & Horseshoes (Almond)
- Fetching block text from jsDelivr sometimes returns "Package size exceeded"; the block text now comes from raw.githubusercontent.com at the same commit. Card images are on jsDelivr and all returned 200 on retry.

- Oct 18 (later): 5 more live cards had their banned wood racks patched at commit 7a470d6: Amara + Clara's Dream, Nantucket + Hearts & Horseshoes, Jade + Blue Christmas, Heritage 2.0 + Festive Plaid and Dear Santa + Festive Plaid. The .html blocks for amara, nantucket, jade, heritage-2-0 and holiday are re-pinned and their captions now match the cards. The holiday December 1994 + Festive Plaid caption was copied from the Dear Santa card; it now mirrors its own card (tiles: B&B Red, B&B Evergreen, PLM Oak; mat: B&B Pink Coral). Re-apply these 5 blocks as whole-block pastes; the .json swap lists don't include this change.

## Re-apply at 02d3765 — LIVE Oct 18 ~14:55 ET (amara, nantucket, jade, heritage-2-0, holiday)
- The 5 wood-patched cards and the December 1994 caption fix are live.
- **Drift check:** before each swap, the editor source was compared with the e593f10 block, ignoring leading and trailing whitespace. All 5 matched, so nothing had drifted.
- **Verified by curl** (every figcaption and card image in the 02d3765 block is on the live page):
  - amara: 49 captions, 16 images
  - nantucket: 41 captions, 30 images
  - jade: 59 captions, 21 images
  - heritage-2-0: 81 captions, 27 images
  - holiday: 109 captions, 154 images
- No "Bird & Bamboo Almond" or "Tudor" text is left on these pages.
- All 413 jsDelivr URLs in the codefooter blocks were warmed first: 412 returned 200 on the first try and 1 after a retry, so none were still failing.
