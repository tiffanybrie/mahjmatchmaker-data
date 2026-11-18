# Week Nov 16-22: finals in Planoly as DRAFTS (Friday next-week prep, Fri Nov 13)
Tiffany reviews in Planoly (CLAUDE.md SOCIAL 12). Nothing scheduled or published. Every group carries "📅 Planned: <Day M/D>" as its first caption line (SOCIAL 13).
Album of the week = Deco (Lagoon) (DESK: social launch week of Mon 11/16, Tiffany Nov 11 9:12am). Source = existing kit only (assets/social/deco-lagoon-launch): intro-framed slides, mats, fym-phones, fym-table, reel end card, tall cover.

| Day | Piece | Feed group (IG + FB Page) | Story group |
|---|---|---|---|
| Mon 11/16 | Intro carousel, 8 slides (intro-framed 1-6, 6b, 7) | 01a1d616-a13a | 01a1d617-41dc |
| Tue 11/17 | It's a mat-ch! Deco (Lagoon) x Pretty in Plum (Mahjong Register) | 01a1d617-439b | 01a1d617-4572 |
| Wed 11/18 | Carousel reel 28.6s (tall cover + 8 slides + animated end card), REMINDER post: add At Last (Etta James) in Edits | 01a1d617-4740 (IG reminder + FB reel) | 01a1d617-6662 |
| Thu 11/19 | Deco (Lagoon) on Gilded Peacock (Bougie): Table view / Aerial / Up close phones | 01a1d617-492e | 01a1d617-4b31 |
| Fri 11/20 | It's a mat-ch! Deco (Lagoon) x Wren (Britt Mills) | 01a1d617-4d10 | 01a1d617-4f01 |
| Sat 11/21 | Story only: Table view on 4 in-stock mats | – | 01a1d617-50ad |
| Sun 11/22 | Story only: recap (5 frames reused) | – | 01a1d617-52b9 |

FB group plan (Claude Doc): https://claude.ai/artifact/Bx2MxUDPzh56vr9LA6deRW

Decisions (Claude defaults, reversible):
- Brand mix: (c) one brand's tiles + other brands' mats for the It's a mat-ch posts. Her album order: #1 Deco Dragon Mulberry is Bam Bird's own pair (already slide 6), #2 Reba no longer on brittmillsdesign.com, #3 Viola sold out, #4 Splash (half weight), #5 Lemondrop (no code yet) -> #6 Pretty in Plum (Mahjong Register, in stock, 10%) and #14 Wren (Britt Mills, in stock, 15%). Stock checked by products.json Nov 13 ~1pm ET.
- Dear Santa reel v3 NOT used for Fri: it says "the tiles that match every Christmas mat" (no-'every' rule Nov 11) and "24" vs 29 live. The Dear Santa push stays with the Canva kit order (her Nov 11 11:51).
- Collab invites not set (SOCIAL 9: ask her first). Mahjong Register has no verified IG handle: named, not tagged.
- Slide 8 (approved graphic) says "See all 30 of her match cards"; live album has 41. Not changed (never change an approved graphic); flagged on HQ.
Checks: content_lint 16 captions 0 FAIL (captions/); center_check PASS on both It's a mat-ch slides; Thu phone slides flag only the app's own UI rows inside the screenshot (justified). Caption source: scripts/social/plain_post.py (captions/plain-post-source), shortened to pass the 350-char lint.
Script fix: plain_post.py falls back to code-truth `terms[brand].pct` (Anders Ruff, Mahjong Register had no `pct` row).
Builder: build_week.py.
