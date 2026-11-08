# Juniper album: Tiffany's notes, Nov 6 2:26am (partial: she ran out of battery mid-review)
DO NOT rebuild/republish until she says go (she was kicked out of the page by the 2:2x republish).

1. Order: Palm Royale #1 (pink centre = max contrast with green; pink is a tint of red, green's complement). Garden Glow great but not #1 (low contrast).
2. Peonies Burst, Cherry Blossom Jade, Palm Beach Tropical Pink Lime, Zesty Plume: rank higher, some of the best matches.
3. Cover: missing the white lines on the top portion (frame ornament).
4. Racks: OMM Hot Pink + Pink Quartz are both 18.5" but the card made Pink Quartz look shorter (racks must render at true relative size). [Tile racks since changed to Hot Pink + Agate; same rule applies.]
5. Fix OMM White Acrylic rack image: "photoshop hack job".
6. Colour card tagline "A lush lantern-lit garden…" -> should be the matchmaker dating-app voice like Papaya Spritz ("Seeking: …").
7. Profile prompts: can't reuse "irrational fear" or "beige felt mat" (just used for Papaya Spritz). New prompts/answers.
8. Colour wheel: Forest Green Jade sits where the colour isn't shown; need a wheel that shows dark AND light colours (value dimension).
9. Layer-arrows graphic: she likes the arrows; use the joker tile photo instead: https://ohmymahjong.com/cdn/shop/files/juniper-mahjong-tiles-9588574.jpg?v=1793772313&width=1946
10. Wording: "jade-look green" sounds weird. It's a jade-look STONE PATTERN; the colour is Forest Green Jade.
11. Add candidate: OMM Camellia (retired) may be a match.
12. Match cards used the tile SCATTER shot; must use the tile PILE shot. ("Truly baffles me.")
13. Wrong Mahj Matchmaker logo used multiple times.
14. Copy: "Oh My Mahjong's own pair for Juniper (starter kit, Nov 11)" reads bot/AI; write like a human.
15. Esme: weak (no forest green, no lime; only teal layer + face pink) -> likely out / low.
16. Emerald Leopard in Bloom: not wowing her, may be taken out.
17. Mahj In Bloom Mat: OUT (X).
18. Sunday mat: why "Sunday Premium"? (check real name) and take it OUT: tiles too bright for it, rack picks looked ridiculous.
19. Crane & Moon and Day Dreamer: low resolution; she needs to see them again (find better photos).
(She did not finish the page: the rest of the mats, faces pick and other sections still to review.)

## Nov 7 (Tiffany 7:38-7:42pm, docs/ANSWERS.md) applied in files, NOT published (she is working in the ordering page NcjAba5oRhBEZB2rfiJx1H)
- #15 superseded: Esme STAYS IN, matched on the faces only (group soft, why rewritten). Camellia: her call, the deep leaves ARE forest green, a great match (group best; "no forest green" was wrong and is gone from manifest/spec/page source).
- Holiday matches (she wants every tile set to show holiday matches): cards #33-38, group "holiday", holiday-coded card (HOLIDAY MATCH band + flame-heart), spec scripts/albumcard/specs/juniper_holiday_nov07.json (JUNIPER_ORDER_START=33). Mahj Mood Holly Berry, OMM Yuletide, PLM Peace Love & Mistletoe, Anders Ruff Watercolor Christmas Tree, Mahjong Register Very Merry Wreath Premium, PLM Perfectly Wrapped. Full-size brand photos in assets/colorcards/juniper/mats/.
- The Kerry (Betty June & Jeannette, her question): good soft match, card #39 (group soft), mat racks = her Oct 20 Kerry registry picks.
- Profile prompt "Green flag I look for" (sounded weird) -> "We'll get along if / You bring the pink. I've got the green covered." Profile story + intro slide 1 re-rendered.
- Crane & Moon: she is questioning it; no change.
- Review page juniper-album.html NOT rebuilt (images pinned to @95ec1edf; the new cards need a new pin): build.py text updated, rebuild with a new sha when the page is next published.

## Nov 7 8:24pm (Tiffany, docs/ANSWERS.md) applied in files, NOT published
- OUT of the album: Midori Shadows (Golden Pond), Crane & Moon (YOLO), Day Dreamer (Pink and Green) (BJ&J). Card files kept; manifest rows #9/#14/#17 and juniper_round3.json carry `out: true` + out_reason; juniper_build.py carries `out` into the manifest and build.py skips `out` rows, so no rebuild brings them back.
- "Your adds" (group 'Your adds'), cards #54-58, spec scripts/albumcard/specs/juniper_omm_nov07.json (JUNIPER_ORDER_START=54): OMM Lorelei, Darjeeling (retired), Anastasia, Hampton, Birdie Green (retired). Full-size OMM flat shots (2400x3000; Birdie Green 1952px retired asset) in assets/colorcards/juniper/mats/. Lorelei + Darjeeling whys in her words.
- build.py GROUPS gained 'to see' (was missing: the page build would have failed on the Nov 7 'to see' cards) and 'Your adds'.
