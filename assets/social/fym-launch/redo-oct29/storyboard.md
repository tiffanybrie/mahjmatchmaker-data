# Launch reel REDO: storyboard (Oct 29, stills only, NOT rendered)

Replaces the Oct 27 launch reel ("the ever-burning question") on the grid, so it has to work on its own as the launch piece and the tutorial.
One match from start to finish: **Sunday** tiles (Sunday Mahjong) × **Brownstone Bloom** mat (Anders Ruff), racks **Bam Bird Boutique Walnut** + **Peace Love Mahjong Oak**.

- Contact sheet: `storyboard.jpg` (31 numbered frames, each with time range and a 1-line caption)
- Frames: `frames/01.jpg` … `frames/31.jpg` (540x960 previews of the 1080x1920 frame), timings in `frames/timing.json`
- Captures: `cap_redo.py` takes real app screens from the LIVE artifact build (Version 1.5, artifact 6epA9HuEdT32zUp79Qv3kd, served on :8766 with the asset folders from /home/claude/fymlive). `storyboard.py <capdir>` builds the stills. To capture at render quality, run `DSF=3 python3 cap_redo.py <dir>`.
- **How the frames are built (rule 20).** The phone sits at ONE fixed spot on a 1080x1920 stage in every frame. The "camera" only scales about a point (push in / pull back) and never slides sideways. On a swipe, the only thing that moves is the cut-out card (`<id>-card.png`, placed at its real on-screen position), with the next real card underneath. The render should reuse how_tinder.py's swipe engine on this geometry (`SW=700, PX=190, PY=330`), keeping the camera still during each swipe.

## Timing: ~38s, 31 frames
Pacing follows the Oct 26 "We've been busy matching" reel: a hard cut on every beat and no shot longer than 2.5s. The time ranges below are cut lengths at roughly 1.0-1.2s per swipe.

| # | time (s) | camera / what moves / stamp / on-screen text |
|---|---|---|
| 01 | 0.0-1.5 | Navy title slams in on beat 1: "The ever-burning question." |
| 02 | 1.5-2.9 | The real Sunday tile photo pops up (tilted -3°). Text: "What mat goes with *these* tiles?" Label on the tiles: Sunday @sunday_mahjong |
| 03 | 2.9-4.1 | The real Brownstone Bloom mat photo (tilted +3°). Text: "What tiles go with *this* mat?" Label on the mat: @andersruffdesignco |
| 04 | 4.1-5.6 | "Asked in every mahj Facebook group." The 2nd line SLAMS: "Every. Single. Day." |
| 05 | 5.6-7.1 | 3-2-1 countdown, 0.5s per number, pink ring pulses |
| 06 | 7.1-8.9 | DROP: "Find *Your* Mat-ch™ is HERE." + heart sparks + "WATCH ONE MATCH, START TO FINISH ↓" |
| 07 | 8.9-10.1 | FULL PHONE. STEP 1 "Pick your tiles": "Sunday" typed, ring taps the Sunday set. Label: Sunday · Sunday Mahjong @sunday_mahjong |
| 08 | 10.1-11.1 | PUSH IN to the tile strip + mat card together (rule 22). STEP 2 "Swipe the mats". Label on the tiles: "Your tiles · Sunday @sunday_mahjong" |
| 09 | 11.1-12.3 | HOLD (phone still). ♥ Ozark **Carson Vintage** tilts RIGHT and flies off, ♥ stamp on the card, app ♥ button visible. Label on the card: @ozarkmahjongg. Suitor tray at the bottom: "1 SUITOR", "+1 suitor!" |
| 10 | 12.3-13.3 | HOLD. ✕ Mahj & Vine **Chinoiserie Songbird** tilts LEFT and is gone, ✕ stamp. Label: @mahjandvine. Underneath: "next: Sunday Premium @sunday_mahjong" |
| 11 | 13.3-14.2 | PULL BACK to the full phone. MENU: the Brand ▾ "Shop by brand" sheet slides up, ring on Anders Ruff, "50+ brands", sheet closes |
| 12 | 14.2-15.2 | PUSH IN on the colour chips: the colour wheel opens into dots, ring taps GREEN, "tap Green" |
| 13 | 15.2-16.0 | Pull back to tiles + mat. The deck changes: "21 green mats for Sunday" (was 42) |
| 14 | 16.0-17.0 | HOLD. ✕ Mahjong Row & Co. **Osmanthus Grove** flies LEFT, ✕ stamp. Label: @mahjongrowandco. Brownstone Bloom underneath |
| 15 | 17.0-18.1 | PUSH IN on the mat card. ZOOM: "Tap + to zoom in", two rings on the app's own + (the image really zooms) |
| 16 | 18.1-18.9 | HOLD close. A finger drags/pans across the leaves |
| 17 | 18.9-19.7 | "Tap − to zoom out": rings on −, the camera pulls back WITH the zoom to tiles + mat |
| 18 | 19.7-20.9 | HOLD. ♥ **Brownstone Bloom** flies RIGHT, ♥ stamp. Label: @andersruffdesignco. Tray: "2 SUITORS", "2 suitors!" |
| 19 | 20.9-22.2 | PUSH IN on the suitor row + "Which suitor is the one?". Both suitors labelled (@andersruffdesignco, @ozarkmahjongg). Tap Brownstone Bloom |
| 20 | 22.2-23.6 | STEP 4 "Add racks: + + +". PUSH IN on the mat preview ABOVE the racks: 3 rings on +, 3 real zoom levels. "Brownstone Bloom, zoomed: stays on while you pick racks" |
| 21 | 23.6-24.4 | HOLD close: drag-pan to the leaves. "dark walnut brown · golden oak + olive" (the colours the racks must match, rule 18) |
| 22 | 24.4-25.4 | PUSH IN on the rack-type chips. MENU: ring taps WOOD (the chip turns brown). "Wood · Tortoise · Metallic · Clear" |
| 23 | 25.4-26.4 | HOLD, mat still zoomed. ✕ Bam Bird **Teal Wood** flies LEFT, ✕ stamp: "no teal in this mat". Big ✕ button pulses |
| 24 | 26.4-27.5 | HOLD. ♥ Bam Bird **Walnut** flies RIGHT, ♥ stamp. @bambirdboutique |
| 25 | 27.5-28.6 | HOLD. ♥ PLM **Oak** flies RIGHT, ♥ stamp. @peacelovemahjong. Underneath: "next: Natural Wood · My Fair Mahjong @myfairmahjong" |
| 26 | 28.6-29.3 | "Zoom back out": − − − on the mat preview, the camera pulls back |
| 27 | 29.3-30.3 | STEP 5 "Make it official". PUSH IN on the 2 rack suitors, ring taps "Make it official ♥". "Walnut + Oak @bambirdboutique · @peacelovemahjong" (Natural Wood labelled at the top) |
| 28 | 30.3-31.8 | Navy dating-app moment. "It's a match!" (Playfair italic) with a tiles circle and a mat circle, heart pops between them, sparks. "Sunday × Brownstone Bloom + Bam Bird Walnut & Peace Love Mahjong Oak". "**4 brands. 1 match.**" |
| 29 | 31.8-34.0 | The TALL Story 9:16 match card, full size (real app render 2160x3840, `61-card-story-full.png`), slow push-in |
| 30 | 34.0-35.6 | SHOP: PUSH IN on the shop list. "code MAHJMATCH · Anders Ruff · Bam Bird · PLM" on the Discount code lines. Sunday row: "No code available" |
| 31 | 35.6-38.1 | END CARD (copy below) |

## Opener copy
1. The ever-burning question.
2. What mat goes with *these* tiles? *(Sunday tile photo)*
3. What tiles go with *this* mat? *(Brownstone Bloom photo)*
4. Asked in every mahj Facebook group. / **Every. Single. Day.**
5. 3 · 2 · 1
6. Find *Your* Mat-ch™ **is HERE.** / WATCH ONE MATCH, START TO FINISH ↓

## End card copy
**Never ask again.**
[ Find *Your* Mat-ch ] (pill pulses)
LINK IN BIO
mahjmatchmaker.com · code MAHJMATCH

(™ appears only once, on the most prominent use: frame 06. "Your" is in Playfair italic inside the Caprasimo headlines, per the Oct 26 social rule.)

## Every brand on screen: label + Tag people (config/social/ig-handles.json)
| brand | product(s) on screen | handle | frames |
|---|---|---|---|
| Sunday Mahjong | Sunday tiles; Sunday Premium mat (under card 10) | @sunday_mahjong | 02, 07, 08, 10 |
| Anders Ruff | Brownstone Bloom mat | @andersruffdesignco | 03, 18, 19 |
| Bam Bird Boutique | Walnut ♥, Teal Wood ✕ | @bambirdboutique | 23, 24, 27 |
| Peace Love Mahjong | Oak ♥ | @peacelovemahjong | 25, 27 |
| Ozark Mahjongg | Carson Vintage ♥ (suitor) | @ozarkmahjongg | 09, 19 |
| Mahj & Vine | Chinoiserie Songbird ✕ | @mahjandvine | 10 |
| Mahjong Row & Co. | Osmanthus Grove ✕ | @mahjongrowandco | 14 |
| My Fair Mahjong | Natural Wood rack (next card after Oak) | @myfairmahjong | 25, 27 |

Collab invites (rule 9): Anders Ruff, Sunday Mahjong, Bam Bird Boutique, Peace Love Mahjong (the 4 brands on the match).
Frame 11, the Shop-by-brand sheet, shows brand NAMES only, not products. Don't tag those brands (Amahj, Amanda Toppe, Bam! Let's Mahjong, Bespoke, Betty June & Jeannette, Bird & Bamboo, Birdsong, Britt Mills, Charleston Mahjong Club, Fait à Main, Hip Hip, House of Hearts, Hutch & Nook); it's the "50+ brands" moment.

## Song shortlist (upbeat, love / matchmaking)
Planned with the edit: the countdown 3-2-1 lands on the build, and "is HERE." (frame 06, 7.1s) lands on the drop/hook. Start points are approximate; set them by ear at render.
1. **Can't Take My Eyes Off You** (Frankie Valli): her earlier pick, and still the recommendation. Start so the horn build plays under 3-2-1 and "I love you, baby" hits at "is HERE."
2. **Signed, Sealed, Delivered I'm Yours** (Stevie Wonder): the bright intro riff carries the swipe montage; "Here I am, baby" on the drop.
3. **Love On Top** (Beyoncé): the key changes work for the swipe → It's a match escalation.
4. **Higher Love** (Kygo & Whitney Houston): the most modern/hype choice; the drop lines up with "is HERE."
(We're not reusing "This Will Be", which went on the hotline reel. No Planoly/IG library music.)

## Self-check against FYM-REEL-RULES 14-22 (checked on the stills)
| rule | result | evidence |
|---|---|---|
| 14 ✕ and ♥ every step | PASS | Mats: ♥ Carson, ✕ Songbird, ✕ Osmanthus, ♥ Brownstone. Racks: ✕ Teal Wood, ♥ Walnut, ♥ Oak. The app's ✕/♥ buttons are visible on every mat swipe (09, 10, 14, 18); big ✕/♥ on rack swipes (23-25) |
| 15 show the choices | PASS | Colour filter (12-13, deck 42 → 21), brand menu (11), rack-type chips with Wood tapped (22) |
| 16 full flow in order | PASS | tiles (07) → mat swipes + colour filter (08-18) → suitors (19) → racks + + + zoom on the mat (20-21) → rack type (22) → rack swipes with the mat zoomed (23-25) → match (28-29) |
| 17 Tinder vibe | PASS | Cards tilt and fly with a ♥/✕ stamp, big round buttons, dating-app "It's a match!" (28). Only ✕/♥, never nope/crush/pass |
| 18 racks match a colour you can SEE in the zoomed mat | PASS | Zoomed preview (20-21) shows dark brown + golden/olive leaves. Walnut = the dark brown (mat swatches #5a4948 / #654c3d), Oak = the golden olive (#8c795b). Teal ✕ because there's no teal in the mat |
| 19 match card = tall Story 9:16, full size | PASS | Frame 29 uses the app's own Story render (2160x3840) |
| 20 PHONE NEVER MOVES on a swipe | PASS (by construction) | One fixed phone position on the stage. Swipe frames (09, 10, 14, 18, 23-25) move only the cut-out card. The camera only zooms between scenes and holds still during swipes. Render check: compare the phone-frame bbox across every swipe scene's frames |
| 21 every brand shown is named + tagged | PASS | See the table above. Cards that appear underneath (Sunday Premium, Natural Wood) got labels too |
| 22 tiles AND mat together, big | PASS | Every mat-swipe frame (08-10, 13-14, 17-18) has the Sunday tile strip (labelled "Sunday tiles", ~17% of frame height) above the mat card (~750px wide). Rack frames keep the zoomed mat above the rack (racks step, per rule 4) |
| 1 labels on their item | PASS | Tile label on the tiles, card labels ride on the flying card, chip/zoom rings on the real buttons |
| 6 camera moves | PASS | Full phone → push in (tiles + mat) → pull back (brand menu) → push in (chips) → push in (mat zoom) → push in (suitor row) → push in (mat preview) → chips → pull back → card |
| 11 centred | PASS | center_check on the text frames 01, 04, 06, 28, 31: 0 off-centre bands |

## Notes / open items for the render
- **Sunday "No code available"**: the live shop list (v1.5) shows nothing under Sunday. Per her Oct 27 9:25am call, the render adds the "No code available at this time" line under Sunday (already in MATCH-INBOX for the live app).
- **Match card title**: the live Story card renders a clean solid "SUNDAY" title, so there's no outline-text problem in this capture.
- **Swipe sound**: each ♥ can land on a beat. The swipe frames are 1.0-1.2s, so the card flies off on the beat and the stamp lands 0.35s before it.
- The rack swipe labels on the far right (Oak) partly leave the frame mid-flight. That's fine in motion, but keep the label anchored to the card's left edge in the render.
- Not rendered, not posted, nothing in Planoly. Waiting on her OK on these stills + a song pick.
