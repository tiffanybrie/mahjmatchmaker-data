# Find Your Mat-ch launch reel REDO (Nov 3 2026)
Swap-in for the Oct 27 launch post, to be **pinned at the top of Reels** (replaces the old one). Song: **Dancing On My Own**, 58.0s.
Not published anywhere. Built on app **v113** (/find-your-match = fym-v113, app @3c0b8ceb), 2x screen recordings, mc/ routing fix.

## Files
| File | What |
|---|---|
| `launch-reel-redo.mp4` | the reel, 1080x1920, 30fps, 58.0s, silent (song goes on in Instagram) |
| `launch-reel-redo-beat-test.mp4` | 540p check copy: click every 0.5s (the original cut's 120 bpm grid, accent each bar) + high clicks at 27.71 (♥) and 30.31 (✕) |
| `launch-reel-redo-cover.jpg` | cover (41.5s: match card + "See it together, share it or shop it") |
| `launch-reel-redo-contact-sheet.jpg` | a frame every 0.5s |
| `launch-reel-redo-safezones.jpg` | key frames with the IG safe zones drawn (green = y 250-1500 content band) |
| `caption-ig.txt` / `caption-fb.txt` | captions (content_lint PASS). FB uses brand names, no @handles |
| `tag-people.txt` | Tag people list (17 verified handles) |
| `build/` | prep.py (rebuilds every /dev/shm input; `--render` also renders), cap.py, cards.py, cards_pick.json, dwall.py, reel.py, finish.py |

## Song sync map (same cuts as the original calm cut up to 24.06s; ♥ held at 27.7s)
| Time | Scene | Source |
|---|---|---|
| 0.00 | "The ever-burning question." | original |
| 2.70 | tiles + "What mat goes with these tiles?" | original |
| 6.08 | mat + "What tiles go with this mat?" | original |
| 8.78 | "Asked in every mahj Facebook group. Every. Single. Day." | original |
| 12.15 | catalog wall 800+ mats / 300+ tile sets / 50+ brands | original |
| 16.63 | Find *Your* Mat-ch is HERE | original |
| **19.20** | **NEW depth wall**: 48 everyday partner mats, a tilted floor the camera glides over, edge to edge | new |
| 20.68 | "Today, you're the matchmaker" (tool intro) | original |
| 24.06 | **Start with your tiles**: tap Start with tiles, type Sunday, tap Sunday | new, rec0 |
| 26.76 | **Swipe the mats**: ♥ Brownstone Bloom (Anders Ruff) lands **27.71** on "watching you kiss her" | new, recA |
| 29.46 | ✕ Chinoiserie Songbird (Mahj & Vine) stamp 30.24, card flies 30.31, card flies left | recA |
| 31.62 | ♥ Carson Vintage (Ozark) 32.00, ♥ Midnight Garden (Mahjong Row) 32.75, deck ends ("That's all the mats...") and the 3 suitors show | recA |
| 33.40 | **Pick your favorite**: "Which suitor is the one?" tap Brownstone Bloom | recP |
| 36.06 | **Add racks**: + + zoom on the mat, tap Wood, ✕ Teal Wood, ♥ Bam Bird Walnut, ♥ PLM Oak, deck ends | recB |
| 40.03 | match card (Story 9:16, full) with a gentle push: **See it together, share it or shop it** | storycard |
| 43.73 | full-frame cross-brand match-card wall (15 of Tiffany's real everyday picks) | cards.py |
| 47.00 | **Shop it with code MAHJMATCH**: shop list, Discount code under each partner piece, Sunday "No code available" | recB |
| 51.50-58.00 | end card: Never ask again · Find *Your* Mat-ch™ · Match tiles, mats & racks across brands · Shop now · use code MAHJMATCH · LINK IN BIO · 4 full-width ticker rows of 37 code-partner logos (no Sunday, no Tigre de Tartán) | new |

## Fixes vs the Oct 27 reel
- Every card on screen is acknowledged: the deck holds only the 4 swiped mats (the app's own "That's all the mats" end state shows after the last ♥), the rack deck only the 3 swiped racks. No Carson Vintage flash; Ozark is hearted, named, tagged.
- The phone never moves on a swipe: the frame is fixed, only the card flies (real app animation), stamp on the card, gone before the next card shows.
- Racks deck opens on Teal Wood with Tiffany's picks turned off by the real chip (no unacknowledged tortoise card).
- Dropped the dating "It's a match!" moment; added depth wall, app tutorial with moving camera, match-card wall, end card.
