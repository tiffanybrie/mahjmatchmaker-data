# Juniper album, round 3: what changed (Nov 6, offline, NOT published)

Source: Tiffany's notes, NOTES-round3-nov06.md (2:26am) + the Main chat's task list. Files rebuilt and committed only.
The review page (juniper-album.html, images pinned to 95ec1edf) and the self-contained copy are ready; Main publishes on her go.

| Note | What changed | Where |
|---|---|---|
| 1 Order | Palm Royale #1 (why line names the pink-centre contrast), Garden Glow #2, Lotus Cove #3. New group "Among the best" right after: Peonies Burst, Cherry Blossom Jade, Palm Beach Tropical Pink Lime, Zesty Plume. Colour card, profile "her type", first dates and slide-7 peek follow the new top 3. | scripts/albumcard/specs/juniper_round3.json, config/colorcards.json, config/profiles/juniper.json |
| 2 Out | Mahj In Bloom Mat and Sunday Premium removed (card files deleted). Real name of the Sunday mat: **Sunday Premium Mahjong Mat** (sundaymahjong.com), the mat Sunday Mahjong made for its own Sunday Tile Set, so "Sunday Premium" was the brand's name, not ours. | spec `out` |
| 3 Weak | Esme and Emerald Leopard in Bloom moved to the bottom under "Weak: yours to cut" with a note on each. | spec group `weak` |
| 4 Camellia | OMM Camellia (retired) added as "New candidate: your call", from the 1400px photo assets/mats/omm-retired/camellia.jpg; mat racks B&B Light Pink + Kelly Green. | card #30 |
| 5 Racks | Racks now drawn at TRUE relative length: config/rack-lengths.json (OMM 18.5" from OMM's pages + her word; PLM 20"), the rack BODY (trough, not the pusher) measured per PNG (scripts/albumcard/rack_body.py), card2.html scales and anchors every body at the same start. Hot Pink + Agate now end at the same point. Opt-in (`true_len` in the spec), so other albums' cards are unchanged. Mat-side racks share their own scale (they are a small legend top right, not the same scale as the big tile racks). OMM White Acrylic recut: holes filled, missing top of the trough rebuilt from the photo's own rack surface, checked on white and navy (scripts/albumcard/nov06/omm_white_recut.py); real_racks.py no longer overwrites hand-fixed cuts. | gen2.py, card2.html, assets/racks/card/ |
| 6 Pile photo | assets/tiles/album/juniper.jpg is now a square crop of OMM's PILE shot (06-Tile_Juniper_F), not the scatter. All 32 cards, the colour card circle and the profile use it. FYM picks it up at its next build (MATCH-INBOX). | assets/tiles/album/juniper.jpg |
| 7 Logo | The navy box on match cards had the OLD wordmark (flame on the j, no heart). New assets/brand/card_navy_logo_v3.png = the current flame-heart wordmark, same tagline line; Juniper cards use it (spec `navy`). Cover, colour wheel, profile and carousel already used the current wordmark. Other albums still use v2 (not touched). | scripts/albumcard/nov06/navy_logo_v3.py |
| 8 Cover | Rebuilt with frame3.png, the frame with DOUBLE white lines top and bottom (same as the uniform Papaya cover, Sierra, Talulah). album_cover_omm.py takes FRAME=frame3.png; default unchanged. | assets/covers/albums/00-juniper-mahjong-tiles-cover.jpg (+ w800) |
| 9 Tagline | Colour card: "Seeking: hot pink, kelly or forest green. / Must love a garden party." Sub line "Forest green jade with chartreuse & teal layers". | config/colorcards.json |
| 10 Prompts | Third prompt is now "Green flag I look for: A pink center. Opposites attract." (no irrational fear, no beige mat). Looking for / love language were already Juniper's own. | config/profiles/juniper.json swipe |
| 11 Wheel | wheel.py has a VALUE wheel (hue around; center light, middle ring full colour, rim dark). Used automatically when a set has a dark colour; Forest Green Jade now sits on dark green. Papaya's wheel is pixel-identical (checked). Mini wheel on slide 2 uses it too, with a new legend. | scripts/colorwheel/wheel.py |
| 12 Arrows | Slide 2 layer arrows now point at the joker tile from the photo she linked (saved as 11-juniper-joker-ohmymahjong-cdn.jpg, clean cutout), labels Teal layer / Chartreuse layer / Forest Green Jade. | scripts/colorwheel/juniper_joker_cutout.py |
| 13 Wording | No "jade-look green" anywhere (slide 3 chip = "Forest Green Jade"; back role "jade-look stone"). Lotus Cove: "Oh My Mahjong designed Lotus Cove to go with Juniper, and they're sold together in the starter kit." Also fixed: "Etsy, through ShopMy" -> "Sold on Etsy", "in OMM's own words", "Oh My Mahjong's own pair" (profile). | spec + profile + page |
| 14 Photos | Crane & Moon from YOLO's 3000px product image, Day Dreamer from BJ&J's 3000px Etsy image, both cropped to the mat. | assets/colorcards/juniper/mats/*-3000.jpg |
| 15 Faces | Not touched. Her hearts on the page are stored in her browser under the same key, so they survive a republish to the same URL. | |

Couldn't do / open:
- Project doc 93 (prompt + interests bank) lives in the claude.ai Project, which this agent can't read; the new prompt was written to the same dating-app style instead. Swap it if doc 93 has one she prefers.
- Mat-side racks (top right legend) are not on the same scale as the big tile racks; making them would not fit the card.
- The cover keeps the pink "MATCHING MAHJONG TILES, MATS & RACKS" ribbon; the uniform Papaya cover uses "FIND YOUR MATCH". Only the frame was in her note.
- Best-features draft graphic and slide 4 still show Claude's 4 proposals (faces untouched until her picks are pasted).
