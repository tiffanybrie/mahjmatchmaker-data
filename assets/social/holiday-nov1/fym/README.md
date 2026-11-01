# Holiday Find Your Mat-ch reel: "Nutcracker Ballet needs a holiday date" (Nov 1 2026, fym-holiday)

DRAFT for Tiffany's OK. Nothing posted, nothing in Planoly. Replaces the flat Oct 31 screen recording (`assets/social/fym-bank-oct31/reel/fym-how-it-works-reel.mp4`, now marked superseded there).

## Files
| File | What |
|---|---|
| `fym-holiday-reel-nutcracker.mp4` | **The reel.** 30.0 s, 1080x1920, silent (she adds the song in IG) |
| `fym-holiday-hook-nutcracker.mp4` | **Story cut-down hook**, 7.9 s |
| `*-BEATTEST-click160.mp4` | Same videos + a click track I generated (160 BPM, high click = bar downbeat). For lining up the song only, never post these |
| `fym-holiday-reel-cover.jpg` | Reel cover: the ♥ on Clara with the Nutcracker Ballet tiles above it |
| `fym-holiday-reel-contact-sheet.jpg`, `fym-holiday-hook-contact-sheet.jpg` | Frames every 0.5 s |
| `caption-ig.txt`, `caption-fb.txt` | Captions (both pass `content_lint.py`) |
| `cap.py` + `cap_tail.py` + `lib.py` | Capture of the real FYM **Version 1.10** screens (fym-v110 @f11610cb, served locally with the v72 base, like the live page block) |
| `build.py` | Renderer (Playwright frame by frame). `python3 build.py full` / `hook`. `beats-*.json` = scene start times |
| `phone_still.py`, `click.py` | Rule-20 bezel check; click-track maker |

## Concept
**A sugar-plum night stage, not a white background.** Red velvet curtains open on the beat, then everything plays on a navy-to-berry night with falling snow, gold twinkles and a string of warm lights. The app moments sit **zoomed in**: the phone runs off the edges of the frame, so the Nutcracker Ballet tiles and the mat card fill the screen together (rule 22). The camera then pushes in on every tap. Three full-screen **photo-dump bursts** of real product photos are spliced between the app moments (her 12:22am update).

The story is a holiday date. **Nutcracker Ballet (Mahj Squad)** needs a date for the holidays → tap Holiday → ♥ / ✕ / ♥ / ♥ → the hearts land in the suitors row → pick the one: **Clara (Oh My Mahjong)**, a Nutcracker mat for a Nutcracker tile set → racks step, + + + zoom on Clara → rack-type chips → ✕ wood, ♥ Magenta, ♥ Light Blue → "It's a match!" → the tall Story match card (the output, shown after you've seen how she got there) → shop list → **Shop now · use code MAHJMATCH**.

## Beat sheet (160 BPM; 1 beat = 0.375 s; a bar = 4 beats = 1.5 s)
| Time | Beat | Scene |
|---|---|---|
| 0:00.0 | 0 | HOOK: "Nutcracker Ballet / needs a date for the holidays", curtains part on beat 1, tiles pop in a gold frame on beat 2 |
| 0:01.9 | 5 | PHOTO DUMP A "Try her on.": tiles on top, a new mat underneath on every beat (Clara's Dream Christmas, Pretty Little Christmas, Tied With A Bow, Clara) |
| 0:03.4 | 9 | APP: camera pushes in on the filters, tap **Holiday** (the chip turns on) |
| 0:04.9 | 13 | ♥ Clara's Dream Christmas · Mahj Squad (stamp on beat 14, flies right on beat 14.5) |
| 0:06.0 | 16 | It **lands in the suitors row** (camera pushes in) · "1 suitor" |
| 0:07.1 | 19 | ✕ Yuletide · Oh My Mahjong (flies left) |
| 0:08.3 | 22 | Tap the **blue** colour dot → the deck changes |
| 0:09.8 | 26 | ♥ Pretty Little Christmas · Peace Love Mahjong |
| 0:10.9 | 29 | ♥ Clara · Oh My Mahjong ("Clara, for a Nutcracker?") |
| 0:12.0 | 32 | Clara lands → "3 suitors. One holiday date." |
| 0:13.1 | 35 | "Which suitor is the one?" tap Clara |
| 0:14.3 | 38 | PHOTO DUMP B "Now, racks.": Clara full screen, Bird & Bamboo Magenta / Light Blue / Ballet Pink / Mulberry slam in one per beat |
| 0:15.8 | 42 | APP racks: tap + + + on beats 43-45, the mat zooms, then the camera pushes in on her blues and magentas |
| 0:18.0 | 48 | Rack-type chips: tap Wood |
| 0:19.1 | 51 | ✕ Peace Love Mahjong Oak |
| 0:20.3 | 54 | ♥ Bird & Bamboo Magenta (her magenta border) |
| 0:21.4 | 57 | ♥ Bird & Bamboo Light Blue (her sky blue) |
| 0:22.5 | 60 | PHOTO DUMP C "150+ holiday mats": Very Merry Mahj (Anders Ruff), Holly Jolly Christmas (Bam! Let's Mahjong), Candy Cane Lane (Anders Ruff), Nutcracker Noel (Peace Love Mahjong), one per beat |
| 0:24.0 | 64 | "It's a match!" Tiles ♥ Clara circles |
| 0:25.5 | 68 | The tall Story 9:16 match card from the app, full height |
| 0:27.0 | 72 | Shop list (push in) + "code MAHJMATCH saves at our partners" |
| 0:28.5 | 76 | End card: Find *Your* Mat-ch™ · "150+ holiday mats. Your tiles. Racks to match." · **Shop now · use code MAHJMATCH** · Link in bio |

Hook cut (7.9 s): hook 0:00 → ✕ Yuletide 0:01.5 → ♥ Clara 0:02.6 → lands in suitors 0:03.8 → It's a match 0:04.9 → Shop now · use code MAHJMATCH 0:06.4.

## Music (she adds it by hand in IG, never library music)
**Primary: Kelly Clarkson, "Underneath the Tree", 160 BPM** (CopperKnob lists 160; AcousticBrainz measures the half-time feel at 80. Both give the same grid). Upbeat, brassy, and a love song ("you're here where you should be"), which suits a holiday date. **Start point:** put a bar downbeat at reel 0:00. The big brass-and-drums intro at the very top of the track works, and so does the first "Underneath the tree" chorus downbeat (roughly 0:45-0:50 in the album version; check by ear). Every cut is on the 160 grid, so any downbeat start stays in sync. To check, play `fym-holiday-reel-nutcracker-BEATTEST-click160.mp4` against the song.
Shortlist (not re-timed to these): Ariana Grande "Santa Tell Me" (dating lyrics), Mariah Carey "All I Want for Christmas Is You", Brenda Lee "Rockin' Around the Christmas Tree", Pentatonix "Dance of the Sugar Plum Fairy" (a nod to the Nutcracker; slower, so it suits the hook better).

## Brands on screen (IG Tag people = all; FB uses names)
@mahj_squad (Nutcracker Ballet tiles, Clara's Dream Christmas mat) · @ohmymahjong (Clara, Yuletide) · @bird_and_bamboo (Magenta, Light Blue, Ballet Pink, Mulberry racks) · @peacelovemahjong (Pretty Little Christmas, Tied With A Bow, Nutcracker Noel, Oak racks) · @andersruffdesignco (Very Merry Mahj, Candy Cane Lane) · @bamletsmahjong (Holly Jolly Christmas). All handles are from config/social/ig-handles.json.
**Collab invites: Mahj Squad + Oh My Mahjong.** Mahj Squad's tile set is the star, and its own Clara's Dream mat is the first ♥, so the reel shows their set with a whole deck of holiday dates. OMM's Clara wins the match, a Nutcracker mat for a Nutcracker set, which is the pairing their customers will want. Bird & Bamboo is a strong third: two of their racks are hearted and four show in the burst.
🛑 Reminder box (first line): **Add "Underneath the Tree" at a downbeat, then post.** Cover: `fym-holiday-reel-cover.jpg`. Captions: `caption-ig.txt` / `caption-fb.txt` (FB Page = brand names).

## Stock (checked Nov 1, 12:15-12:45am ET, Shopify product JSON)
In stock: Nutcracker Ballet tiles (Mahj Squad), Clara's Dream Christmas (Mahj Squad), Clara + Yuletide (OMM), Peace Love Mahjong holiday mats (Pretty Little Christmas, Tied With A Bow, Nutcracker Noel), Candy Cane Lane + Very Merry Mahj (Anders Ruff), Holly Jolly Christmas (Bam!), Bird & Bamboo Magenta / Light Blue / Ballet Pink / Mulberry (20" and 19" sets), PLM Oak racks.
Skipped: Peace Love Mahjong Spirit of Christmas tiles (pre-order, and FYM labels it "sold out"), Mahj Squad Candy Cane Pink Wonderland (sold out), Britt Mills Nutcracker mat (sold out). **OMM Sugarplum is gone from ohmymahjong.com** (404, not in products.json) but is still a visible holiday match in v110. For the capture I hid it in my local session only, so it never shows on screen. It is logged in docs/MATCH-INBOX.md for Matches & Catalog.

## Counts used (from data, not guessed)
- **"150+ holiday mats"**: FYM v110 (site-app/fym-v110 @f11610cb) has 152 visible mats with the holiday flag (`M[k].hol && !M[k].hid`, of 1,189 visible mats). That is 151 once Sugarplum is retired, so "150+" stays true.
- Nutcracker Ballet: 18 of Tiffany's matches, 17 of them holiday (16 without Sugarplum). The reel shows no count for these, because the live app still counts Sugarplum.
- Rack match (rule 18): Clara measures #28bcef sky blue 37.5% and magentas #b3286a / #e41a68 about 31% (FYM `ms`), so the hearted racks are Bird & Bamboo Light Blue and Magenta. Both are her picks for this set, and the Oak ✕ is the wood option.

## QA
- Contact sheets every 0.5 s were looked at. Every product on screen is named and tagged (rule 21). Tiles and mat are big together on every swipe (rule 22). Swipes show ♥ right / ✕ left with stamps, and at least one ✕ in both the mats and racks steps (rule 14). Hearts land in the suitors row (rule 2). The racks step has the + + + zoom (rule 4) and the chips (rule 15). The match card is the tall Story card (rule 19), and it comes after the flow.
- Rule 20, the phone never moves on a swipe: `phone_still.py` on a no-snow render. The bezel edge moved 0 px in all 7 swipes (PASS). `center_check --phone-still` mistakes the white flying card for the phone, so the bezel edge is measured instead.
- `center_check`: the snow and twinkles make every band read as "off". On a no-snow render, the only flags are the zoomed app UI itself (left-aligned app text, plus push-ins centred on a chip, which is deliberate), sparks mid-flight, and the match circles mid-pop. The settled hook, match, card and end frames are centred. The hook's "Mahj Squad tiles" label was re-centred.
- Safe zones: titles start at y=250. Key stickers sit at y≤1440, and the bottom 400 px has only app UI or photos.
