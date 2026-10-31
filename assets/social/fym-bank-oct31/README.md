# Find Your Mat-ch content bank (Oct 31, for Tiffany's OK on HQ needs/content-bank-2026-10-31)
DRAFTS ONLY: nothing posted or scheduled. Every piece shows the app IN USE on real Version 1.9.2 (v107) phone screens (her Oct 30 "sell the tool" rule). Overview: bank-overview.jpg. Week plan: assets/social/week-2026-11-09/.

| Piece | Folder | What | Brands (IG Tag people) |
|---|---|---|---|
| 1 How it works | p1-how-it-works/ (feed-01..06 4:5, story-01..06 9:16) | pick tiles → swipe mats → racks → match card | @ohmymahjong @brittmillsdesign @middleandmainmahjong |
| 2 Christmas table in 30 seconds | p2-holiday-30s/ (7 + 7) | Tinselle (Emerald Green) → Holiday + Green chips → ♥ Evergreen & Tartan → B&B racks → Story card | @viroramahjongofficial @andersruffdesignco @bird_and_bamboo (Polo Club by Luxe Mahjong on screen: no verified handle, name only) |
| 3 Tap a color | p3-color-filter/ (6 + 6) | Papaya Spritz, Orange / Blue / Green chips change the deck | @ohmymahjong @andersruffdesignco @mahjandvine |
| 4 Tiles first or mat first? | p4-two-doors/ (4 + 4) | tiles door vs mat door, Papaya Spritz ↔ Heiress | @ohmymahjong @brittmillsdesign |
| 5 Reel (real screen recording) | reel/fym-how-it-works-reel.mp4 (32s, 1080x1920, silent-capable captions) + cover reel/fym-how-it-works-reel-cover.jpg | same flow as piece 2, real taps (✕ Polo Club, ♥ Evergreen & Tartan, racks ♥/✕/♥, card) | as piece 2 + @sunday_mahjong (Festive Plaid Premium on screen) |
| 6 Own Tartan Tidings? | p6-tartan-tidings-matdoor/ (5 + 5) | mat door: Tartan Tidings → swipe Tinselle (Emerald Green), Dear Santa, Rackin' Rudolph | @andersruffdesignco @viroramahjongofficial (Hip Hip: no verified handle, name only) |
| Pins | pins/ (8, 1000x1500) | keyword-first FYM pins, queued in config/pinterest/queue.json (kind fym, status pending, prio 12; holiday ones notBefore Nov 1) | – |

🛑 REEL reminder box (piece 5, Planoly reminder post): 1st line = "Add your love song, then post". Song: TBD by Tiffany (never Planoly/IG library music). Cover: reel/fym-how-it-works-reel-cover.jpg. Tag people: @viroramahjongofficial @andersruffdesignco @bird_and_bamboo @sunday_mahjong. Collab invite: Virora + Anders Ruff. Caption: assets/social/week-2026-11-09/captions/tue-holiday-reel-ig-caption.txt.

Stock checked Oct 31 ~2:30pm ET: Tinselle Emerald Green (Virora) in stock; Evergreen & Tartan + Tartan Tidings (Anders Ruff) in stock; Papaya Spritz (OMM) in stock. Recheck the morning of.
Not done (budget): rack-step +zoom on the mat (FYM-REEL-RULES 4) and suitor-row landing shots (rule 2) are not in the reel; camera push-ins not added (rule 6). Song is hers.
Rebuild: serve the v107 website copy (git show c7ab351a:site-app/fym-v107/index.html + its b*.js chunks + t* photo folders) on :8777, then `python3 cap.py`, `python3 cap_color.py`, `python3 cap_matdoor.py`, `python3 rec.py` (CDP screencast → /dev/shm/w/rec/raw.mp4 via the concat list), `python3 reel.py`, `python3 build.py`.
center_check: stills PASS outside the phone screens (the only flagged bands are left-aligned app UI inside the screenshots); reel PASS outside the phone + --phone-still PASS (--phone-color f7f7f5).
