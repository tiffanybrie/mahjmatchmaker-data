# Next week's "talk to them" pieces (drafts, Nov 1 2026)

From Tiffany's Nov 1 12:22am direction (docs/ANSWERS.md): (1) one FACE-TO-CAMERA video by her, (2) an "ASK ME ANYTHING" / FAQ post where we seed the questions ourselves. **DRAFTS ONLY: nothing posted, scheduled or in Planoly.** HQ: `needs/talk-and-ama-2026-11-01`.

Facts were checked against the LIVE tool on Nov 1 (mahjmatchmaker.com/find-your-match serves fym-v111, footer "Version 1.11"):
- Stars + **My stars** are live (saved on the device). The account / "Email me a sign-in code" button is on the page, but the sign-in email setup (Resend + Supabase, top of HQ) isn't done, so both pieces say sign-in is **coming**. If it works before posting: swap the ALT line in the script and slide 8's last sentence.
- The feedback link is the tool's footer: "Something look off or have an idea? Tell me here →" → /find-your-mat-ch-feedback (200).
- Holiday chip is on the start screen; /holiday-mahjong-matches is live (200).
- Partner label in the tool: "Partner brands come first. Save 10% or more at any of them with code MAHJMATCH". So the copy says "a discount, usually 10% or more" (Maison Mahj = free shipping on tile sets, Noli June = $100 minimum).
- Oct 31 brands as the tool spells them: Bougie Mahjong, Mahj & Moon, Hutch & Nook, Betty June & Jeannette, Piper Chase Studios (all non-partner).
- It's never called an app: "works right in your browser".

## 1. Face-to-camera video (75-85s)
`talk/face-to-camera-script.txt` has the hook line for the first 2 seconds, the script in short sayable lines with [cut] marks (one block per take), on-screen text per beat, B-roll file paths with timestamps, the cover-frame idea, 5 songs with start points (low, added in Edits), and the brands to tag.
Captions (content_lint: 0 FAIL): `captions/talk-ig-caption.txt`, `captions/talk-fb-caption.txt` (FB Page: brand names, URL).
Tag people (IG): @bougiemahjong @hutchandnook @piperchasestudios, plus the B-roll brands listed at the end of the script. Mahj & Moon and Betty June & Jeannette have no verified handle (name only).

## 2. Ask Me Anything carousel (10 slides) + stories (11 frames)
- Feed 1080x1350: `ama/feed/feed-01-cover.jpg` … `feed-10-end.jpg`. Stories 1080x1920: `ama/story/story-01-cover.jpg` … `story-10-end.jpg` + `story-11-question-sticker.jpg`.
- Contact sheet: `ama/ama-contact-sheet.jpg`. All the text: `ama/qa-text.txt`.
- Look: cream paper with pink/navy confetti and hearts, a navy "question" chat bubble and a white "answer from Tiffany" bubble (flame-heart avatar), Caprasimo questions, Bitter answers, Playfair italic "Your". Visuals are real product photos and **real crops of the live tool** (`src/ui/*.png`, captured Nov 1 from Version 1.11). No white-background phones.
- Framing: "Ask me anything", no claim that anyone asked. The end slide invites real questions in the comments.
- Q2 (partner vs non-partner) is her 12:22am answer nearly word for word ("10% off" → "a discount, usually 10% or more").
- Brands shown: Anders Ruff (Dear Santa, Tartan Tidings, Classic Very Merry Mahj), Virora Mahjong (Tinselle (Emerald Green)), Bespoke Mahjong (Holiday Love Red & Green, slide 5: a real Dear Santa album match). The 5 new brands are named on slide 9.
  Tag people: @andersruffdesignco @viroramahjongofficial @bespoke_mahjong @bougiemahjong @hutchandnook @piperchasestudios.
- Captions (content_lint 0 FAIL): `captions/ama-ig-caption.txt`, `captions/ama-fb-caption.txt`.
- Stories: frames 1-10 are the carousel at 9:16. Brand mentions make them a reminder story (mention @andersruffdesignco on frame 1). **Frame 11 = question sticker**: put Instagram's QUESTIONS sticker over the mat photo with "Ask me anything about Find Your Mat-ch 💌". Answer the replies as story frames later in the week.

## Rebuild
`python3 assets/social/next-week-talk/src/build_ama.py` (Playwright; fonts from scripts/social/tileprofile/fonts). It fits the text so nothing overflows and prints the final sizes. Re-crop `src/ui/` from the live tool if the UI changes before posting.
