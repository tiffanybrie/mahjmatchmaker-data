# System failures, Nov 25 2026

## Tiny tagline on title cards and card logo boxes (Tiffany 2:42am, Deco Indigo review)
- Miss: the "Matching mahjong tiles, mats & racks" ribbon was unreadable on album title cards and every match card logo box; the Nov 18 rule ("ribbon only where readable") lived only in BRAND-GUIDE.
- Fix (mechanical): new assets assets/brand/card_navy_logo_v4.png + scripts/covers/tagbar_fym.png read "Find Your Mat-ch"; gen2.py default = v4 and REFUSES the v1/v2/v3 ribbon logos; album_cover_omm.py uses the new bar; every specs/*_build.py switched.

## Card titles shrank to unreadable on long mat names (Tiffany 2:51am)
- Fix (mechanical): scripts/albumcard/shortname.py + config/card-short-names.json; gen2.py runs every card title through short_title() before drawing.

## FYM 1.23: my "View row into the bar" change hid the View switch in Up close/Aerial (independent QA, 3:40am)
- Why: the bar is hidden outside Table view, and I moved the row into it without a mode check. QA caught it (the step worked).
- Fix: row only moves in Table view; bar() puts it back otherwise; + zoom pulls the corner tile photo to the middle (QA fail 3). Re-QA run.

## Review page lost its remove buttons in round 2 (Tiffany 2:51am)
- Not yet fixed: OVERDUE line (review_template.html round 2 must keep X on every card).
- MISS: grid view (the Nov 17 default on every album review page) let her pick up a card to reorder it, but gave no way to keep or remove it — only "Move to #" and "Cancel". Tiffany hit this on Deco Indigo round 2 ("there's no longer an option for me to take things out").
  WHY: when grid view became the default (Nov 17), the per-card ♥/✕ buttons that live on the old list/card view (.mc) were never ported to the grid's tap-to-select panel (#gsel) — the panel only ever had Move-to-# and Cancel.
  FIX: scripts/albumreview/review_template.html #gsel now has its own ♥ Keep / ✕ Remove buttons that act on whichever card is picked up, in grid view, without losing the selection (she can keep tapping spots to move it after). Every review page already gets this for free since build_review.py always pulls the current template.
  GATE: scripts/albumreview/selftest.py now fails any review page where grid view's selection panel lacks a working Keep/Remove (added as part of build_review.py's pre-publish selftest, so a page can't go out without it).

## Review page publish refused: "must be HTML (detected text/plain)" (Deco Mulberry round 2, caught by Claude before she saw it)
- Why: scripts/albumreview/review_template.html has never opened with `<!DOCTYPE html>` (starts straight at `<meta charset="utf-8">`). publish_files now sniffs content-type and refuses an index.html that doesn't sniff as HTML, so the round-2 publish failed outright.
- Fix (mechanical): added `<!DOCTYPE html>` as line 1 of review_template.html, so every review page build_review.py produces from here on publishes cleanly. GATE: scripts/albumreview/selftest.py now reads the first 100 bytes of the built page and fails the build if it doesn't start with `<!doctype html>` (case-insensitive) — so a template edit that drops it again fails at build time, not at publish time in front of her.

## Color wheel footer hardcoded to "Oh My Mahjong" for every 3-pin set (found building Mahj Pit Merry Merry's wheel)
- Why: scripts/colorwheel/wheel.py's main() (the <=3-pin branch, used whenever a set has only its 3 back colors and no listed faces in WHEEL_FACES) had the Nov 6 brand-attributed footer line hardcoded as a literal string ("Sampled from Oh My Mahjong's tile back photo...") instead of using the `note` parameter the CLI entry point already computes correctly per-brand (f"From {cc['brand']}'s photos..."). _rest_many (the >3-pin branch) got the per-brand note treatment on Nov 6-7; this branch never did, so every album whose wheel used only 3 backs (no faces listed) silently credited Oh My Mahjong regardless of its real brand. Papaya Spritz (the original set, actually Oh My Mahjong) never showed the bug, which is likely why it went unnoticed.
- Fix (mechanical): main()'s footer now reads `note or 'Angle = hue · distance from center = how vivid.'` the same way _rest_many already does, so the brand name the CLI already computes actually reaches the image. No new gate (cosmetic copy, not a gated field) — worth a glance next time a 3-pin wheel is built for a new brand.

## Album record clobbered by a concurrent background script (Merry Merry: discovery/faces/research_deferred lost)
- Why: scripts/albumreview/catalog_refresh.py is a long-running (slow, ~2 min) script that reads config/album-records/<set>.json at the start and writes its own full copy back at the end. I added discovery, research_deferred and faces to the same record while it was running in the background; its final write silently overwrote those additions (classic read-modify-write race on a shared JSON file), caught only because album_gate.py was re-run right after and the already-passing checks failed again.
- Fix (mechanical, partial): caught and reapplied the lost edits this time by re-running the gate immediately after any background record-writing script finishes, before trusting the record as current. Not yet fixed at the root (catalog_refresh.py still does a blind overwrite, not a merge) -- flagging for a real fix: have it re-read the record right before its own write and only update the keys it owns (catalog_checked, pool.new_candidates), never round-trip the whole file. Left on OVERDUE rather than done now, since it needs care across every other script that writes these records the same way (pull.py already had a related bug fixed earlier today).

## HQ albums document nearly corrupted by a leftover copy/paste placeholder (Merry Merry review-page send, 3:38pm)
- Why: when merging the Merry Merry item + row into the hq/albums db document, I wrote the literal placeholder string "__FILE__" into the items/rows fields instead of the actual arrays -- a slip in constructing the db_write call, not a tool or script bug. The write succeeded (version 109), so for about 3 minutes the live HQ page's album list and rows were replaced with two useless string literals.
- Caught: by reading the document back immediately after every db_write (standing practice, not yet a hard rule) rather than trusting the write result alone.
- Fix (mechanical): re-wrote the full correct items+rows arrays in one db_write (version 110), verified by a second db_get read showing real data restored. No gate exists for this because it's a one-off authoring mistake in a chat-driven tool call, not a reproducible script bug -- the real fix is procedural: after ANY db_write to a shared HQ/album-record document, always db_get the same path back before moving on, and eyeball that the values are real, not placeholders. Logged here per the FIX THE STEP rule even though there's no code to patch.
