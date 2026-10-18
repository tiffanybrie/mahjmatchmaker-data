# Holiday card rack captions, regenerated (Oct 18)

The "Rack matches:" lines under the holiday match cards were written from an older rack list, so they didn't match the racks printed on the cards. Each caption is now rebuilt from that card's own rack list (scripts/albumcard/holiday_manifest.json). It's split the way the card shows it:
`Match the tiles: … <br>Match the mat: …`

- Only cards built from that manifest are touched: holiday-v4, polofix-v1 and their codefooter-v1 copies. I checked 14 of them by eye and the manifest matches the printed racks exactly.
- Older-layout cards (logofix-v2, Squarespace-hosted) are left alone. Their captions were written per card.
- Tigre de Tartan Oxblood Scallop is left out of captions because it isn't printed on the cards (no product photo).
- Nothing is live. Every page needs Tiffany's approval.

## The 13 code-footer pages (238 captions)
The fixed captions are already folded into `../codefooter/<slug>.html` (the whole block). Each `<slug>.json` there also has `caption_swaps`. Apply them AFTER that file's URL swaps, because each `old` segment starts at the card's new image URL. Each segment is unique in the block.

## Other album pages (caption-only swaps)
Each `<slug>.json` here has `caption_swaps`: `old` → `new`, each one a unique segment from the card's `<img src=…` to the end of its caption. They were built from the live page HTML captured Oct 18 ~08:40 ET, so re-check that `old` is still in the block before swapping.

| Page | Captions |
|---|---|
| /birdie-mahjong-tile-matches | 14 |
| /coquette-mahjong-tile-matches | 9 |
| /dandy-mahjong-tile-matches | 7 |
| /drake-mahjong-tile-matches | 4 |
| /emerald-mahjong-tile-matches | 8 |
| /gemma-mahjong-tile-matches | 4 |
| /glitterville-mahjong-tile-matches | 7 |
| /glow-wild-mahjong-tile-matches | 5 |
| /jasmine-mahjong-tile-matches | 8 |
| /lagoon-mahjong-tile-matches | 5 |
| /lola-mahjong-tile-matches | 9 |
| /luminaire-mahjong-tile-matches | 5 |
| /moonlight-mahjong-tile-matches | 15 |
| /osler-mahjong-tile-matches | 13 |
| /palm-royale-mahjong-tile-matches | 5 |
| /pearlescent-mahjong-tile-matches | 11 |
| /smith-mahjong-tile-matches | 13 |
| /solara-mahjong-tile-matches | 4 |
| /talulah-mahjong-tile-matches | 5 |
| /taylor-mahjong-tile-matches | 4 |
| /tortoise-mahjong-tile-matches | 4 |
| /willow-mahjong-tile-matches | 7 |

Total here: 166

Rebuild: `python3 scripts/albumcard/fix_rack_captions_oct18.py` (run on a clean checkout of site/livepatch/codefooter).

## LIVE progress — Oct 18 ~12:15 ET (Tiffany approved in chat: "Approve fixing the rack captions on the other 22 album pages.")
Before starting, every `old` segment on all 22 pages was re-checked against live HTML: each was found exactly once, and no page had drifted. The swaps were applied as caption-only edits inside the existing block, aborting if any segment wasn't exactly once.
- **Done, and verified by curl that all new captions are present and no old ones remain:**
  - taylor 4/4
  - birdie 14/14
  - coquette 9/9
  - dandy 7/7
- **Not done:** drake, emerald, gemma, glitterville, glow-wild, jasmine, lagoon, lola, luminaire, moonlight, osler, palm-royale, pearlescent, smith, solara, talulah, tortoise, willow.
  - On drake the editor didn't open, so nothing was changed there.
  - The Squarespace tab then stopped responding after navigating to emerald. It's probably waiting on a browser dialog.
- Block ids per page: scratchpad cflive/rc_blocks.json, or find the block that contains each `old` segment.
