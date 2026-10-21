# Papaya Spritz: PLM Oak → Middle & Main Scalloped Beechwood (Oct 21). STAGED, NOT LIVE

Tiffany's decision: Papaya Spritz tile racks are now B&B Lavender, PLM Chartreuse and M&M Scalloped Beechwood (`config/tile-racks-picks.json` final_lists, commit 306d7f5). This folder carries that change to the album page. The FYM part is at the end.

## What changed
- **50 match cards** (`assets/cards/papaya-spritz/`, commit `fbf7ec953d379647212f69722c3cf90239c09b8b`). They were re-rendered with gen2.py from the saved v1 spec, and only the tile racks changed. A control render of the old spec matched the live v1 cards pixel for pixel. Every pixel that changed sits in the lower-left rack area (x 0–492, y 685–1268).
  - Rack order on the card follows final_lists: Lavender at the top, then Chartreuse, then Beechwood at the bottom. v1 had Oak, Chartreuse, Lavender.
  - Mats, titles, mat racks and code footers did not change. That includes the nine "15% OFF USE CODE : MAHJMATCH" cards, which another agent is auditing.
- **2 colour-guide images** (`assets/colorcards/papaya-spritz/…-tile-edit-moodboard.jpg` and `…-color-guide-mobile.jpg`) were rebuilt with Beechwood in 306d7f5. The live page still pins them at `5a04f77`, where they show Oak. They are re-pinned to `fbf7ec9`.
- **Captions:** each card's "Racks shown" line now starts with Lavender · Chartreuse · Beechwood, with the M&M affiliate link `sca_ref=10574197.BKiJ48vXYfYfD31E`. The line no longer mentions Oak. Vivienne's caption also lists her mat-rack registry, which repeats Beechwood and Chartreuse, so the duplicates were removed from that one line.
- The cover is unchanged and stays at `b3f23e5`.

## Files
- `live-block-before.html`: the live code block taken with curl on Oct 21 from block `block-c06750fe09c093c1aba1` on /papaya-spritz-mahjong-tile-matches. Use it for rollback.
- `papaya-spritz-codeblock.html`: the same block after the change. Paste it as a whole-block replacement.
- `swaps.json`: the same change as a minimal list. It has 52 URL swaps and 46 unique caption swaps, and applying them to `live-block-before.html` gives exactly `papaya-spritz-codeblock.html`.
- `../warm_result_papaya_beechwood.json`: all 54 jsDelivr URLs in the new block returned 200, and every body was byte-identical to the repo file. The first pass had 16 one-off 503s, which a retry cleared.

## Publish steps (main session, after Tiffany's OK)
1. **Re-check the live block.** Curl the page (`curl -sS -A "Mozilla/5.0" https://www.mahjmatchmaker.com/papaya-spritz-mahjong-tile-matches`). Confirm that block `block-c06750fe09c093c1aba1` still equals `live-block-before.html`, which means it still holds 50 "Peace Love Mahjong Oak" and 51 `@b3f23e5` URLs. If someone has edited it since, apply `swaps.json` (URL swaps first, then caption swaps) instead of pasting the whole block.
2. **Re-warm.** Curl each URL in the new block and expect 200 (jsDelivr can return a one-off 503 or 403, so retry).
3. **Replace the block.** In Squarespace /config, edit the code block on /papaya-spritz-mahjong-tile-matches. Either paste `papaya-spritz-codeblock.html` from jsDelivr at this README's commit, or run the `__fix` regex route with `swaps.json`. Save, then publish.
4. **Verify with curl:**
   - 50 `mm3-c` card figures
   - 0 "Peace Love Mahjong Oak"
   - exactly 50 "Middle &amp; Main Scalloped Beechwood"
   - 50 `@fbf7ec953d37` card URLs
   - 2 `@fbf7ec953d37` colorcard URLs
   - 1 `@b3f23e5` URL (the cover)
   - The "15% OFF" text lives inside the card images, not the HTML, so the block itself has no code strings to check.
5. **Socials and other copies.** The Papaya "It's a mat-ch" and profile assets were already rebuilt in 306d7f5. Search-index thumbs (`assets/search/thumbs.json`) only point to card filenames, which did not change.

## FYM (Find Your Match)
- Staged build: `/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/fym-oct21e/` (built from fym-oct21d = live v68 by `builder/fym_fix_oct21/papaya_beechwood.py`).
- Change: in 53 Papaya match-list entries, the rack key `peacelovemahjong.com/mahjong-racks-racks-pushers-set-of-4` (PLM Oak) is replaced in place by `www.middleandmainmahjong.com/golden-grain-beechwood-mahjong-rack-and-pusher-set-of-4` (M&M Scalloped Beechwood). The 54th entry, Peony & Parasol, has no racks. `builder/fym_flags/locks.json` was updated to match, and the change is recorded in `_changes`.
- Gate: PASS. `fym_apply_locks.py --check` reports 0 changed locked items. Against the old locks it reported 1, the Papaya `m` field, which covers the 53 swaps.
- **Do not republish v68 after this commit.** v68 now fails gate [6] against the new locks, so any FYM publish must start from fym-oct21e or a later build.
- Publish only after independent QA passes (CLAUDE.md rule 2). Run the gate again, then publish `fym-oct21e/index.html` to artifact 6epA9HuEdT32zUp79Qv3kd.
