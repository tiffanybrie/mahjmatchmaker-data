# Social content: checks before anything goes into Planoly

Tiffany's standing rule (Oct 21): when one piece of content changes, check every other draft or final piece for the same problem.

## 1. Caption lint (gate-style, exits 1 on FAIL)

```
# repo caption files (assets/**/*caption*.txt + assets/reels/s2/captions.json)
python3 scripts/social/content_lint.py

# Planoly: save list_post_groups output (status draft and scheduled) to JSON files, then
python3 scripts/social/content_lint.py --planoly scheduled.json draft.json
```

What fails:
- **banned-word**: crush / nope / pass. The profile UI is an X and a heart only; "match" is fine.
- **code**: TEACHMAHJ (teacher-only) or any discount code other than MAHJMATCH.
- **naming**: "Find Your Match" (the tool is **Find *Your* Mat-ch™**) and "mat-ch card" (album cards are plain "match cards").
- **old-profile**: retired Papaya answers ("long-term mat partner", "coordinating racks", "beige tablecloth").
- **icons**: star, lightning or rewind glyphs (the old 5-button row).
- **length**: Instagram/Facebook captions over 350 characters before the hashtags. Pinterest gets 500.

The 🛑 reminder box (up to the ———— line) is checked for words and codes but is not counted toward length. Posted
captions go in `ARCHIVE` in the script and report as INFO. Past reminder posts (reminder sent, date passed) are skipped.

## 2. Look at the pictures (the lint can't read images or video)

```
python3 scripts/social/contact_sheet.py /path/sheet.jpg FILES_OR_DIRS... [--cols 8 --w 240 --frames 6]
```

Videos add evenly spaced frames. For reels, also extract every frame (`ffmpeg -i reel.mp4 -vf scale=108:192 f/%04d.png`)
and check the cuts: no empty or near-uniform frames, no one-frame flashes.

Reels end cards: `python3 scripts/social/titlecards/reels_overlay.py last_frame.png check.jpg` draws Instagram's Reels
UI over the frame. All text must sit inside x 90-860 and above y ~1150 on the right / y 1500 overall.

Look for: 5-button rows, star or lightning icons, NOPE/PASS stamps, "Find Your Match", old racks
(Papaya = B&B Lavender, PLM Chartreuse, Middle & Main Scalloped Beechwood; not PLM Oak).

## Shared assets

- Profile cards: `scripts/social/tileprofile/swipe_profile.py`. `buttons()` there is the only X + heart row; every
  feed, story and reel card uses it.
- The Beige Felt mat (recurring joke character): `assets/social/characters/beige-felt-mat.png`, made by
  `scripts/social/characters/beige_felt.py`. Use this one file wherever the beige mat appears.
- Hotline reel: `REEL_VER=v12 python3 scripts/social/titlecards/reel.py` writes
  `assets/social/titlecards/counseling-ep1-papaya/papaya-hotline-v12.mp4` (frames go to gitignored `frames/v12/`).
