# Juniper (Oh My Mahjong) album: LIVE Nov 8, ~12:30am ET

Tiffany finished her order Nov 7 11:21pm ("done"); 11:26pm she moved the go-live from Nov 11 to ASAP (the album builds interest before
the tiles go on sale Wed Nov 11 10am CT). Copy is pre-launch: "Launches Wed 11/11", no "available now" wording for the tiles.

## What is live
- **Page** https://www.mahjmatchmaker.com/juniper-mahjong-tile-matches (collection 6aeffe202f132f1815eaf376, duplicated from Papaya Spritz).
  Title "Juniper Mahjong Tile Matches", nav "Juniper Tile Matches", SEO title "Juniper Mahjong Tile Matches: Mats & Racks for Oh My Mahjong
  Juniper", SEO description "Oh My Mahjong Juniper tiles (launching November 11) matched to 42 mats, with rack picks and shop links. Top
  picks first. Save with code MAHJMATCH." (Set in the Page Settings panel; /api/commondata/SaveCollectionSettings returned 500 every try.)
- **Code block** = `juniper-codeblock.html` (pin @5132eff0; images @4d61e0df). Built by `build_block.py <image sha>` from the LIVE Papaya
  block (`papaya_live_template.html`): hero with cover + "Launches Wed 11/11" pill, FAQ + JSON-LD (top 3 Palm Royale, Flora Belle, Lotus
  Cove; 42 matches from 16 brands incl. 5 holiday), Colors & racks (colour card desktop/mobile, favourite faces, colour wheel + 2 short
  colour-theory paragraphs), 37 year-round cards, holiday section `#holiday-matches` (5 cards, 01-05, her relative order; holcss), footer.
  Captions: full mat name, "Mat by" brand page link (partners), Retired tag + "Shop Current OMM Mats" (Camellia, Birdie Green, Esme),
  Shop button = FYM 1.18 links (Mahjong Register = plain product link), `code MAHJMATCH` chip for partners, "No code for <brand>" for
  non-partners, "10% off at Mahjong Register with MAHJMATCH (excludes racks and other brands' products)" (was "No code at Mahjong Register right now" until Nov 8), Match the tiles / Match the mat rack links. Lotus Cove: Papaya-style pair note.
  No "Tiffany's take" blurbs: the review-page "why" notes were written TO her (e.g. "Your #1", "so it's #2"), not for readers.
- curl: 200, 42 `mm3-c` (5 `mm3-hc`), h1, title/description = SEO, 47/47 images 200; holiday_numbering.py 0 problems; Papaya page untouched (56 cards).
- **/mahjong-tile-matches**: Juniper first in "Our Latest Albums" + end of Green grid (block ...1478_3720; the home page album strip renders from it).
- **/green-mahjong-tile-matches**: `mmcol-card` first ("Oh My Mahjong · 42 matches").
- **/oh-my-mahjong-discount-code**: album card between Jasmine and La Fete; counts 38 -> 39 albums, 907 -> 949 mat matches, "(39 so far)" x2.
- **/links**: latest-album card = Juniper ("Oh My Mahjong · Our latest album · tiles launch Nov 11 · code MAHJMATCH"), Brownstone feature
  removed (stays in the strip); Juniper first in the album strip. FYM card stays first.
- **Pinterest**: config/pinterest/queue.json album-juniper + card-juniper-01..04 (guide-juniper already existed); uniform cover assets/covers/albums/uniform-v3/juniper.jpg.
- **Google**: URL Inspection = unknown to Google; Request indexing clicked (result in docs/ANSWERS.md).

## Nov 8 ~11am: code bands + zoom fix LIVE (Tiffany 10:11am HARD RULE + 10:15am zoom crash)
- 9 cards re-rendered with **SAVE WITH CODE : MAHJMATCH** (were NOT A PARTNER : NO CODE x6 / NO CODE AT THIS TIME x3): Palm Royale,
  The Kerry, Merrye, Evergreen, Cheetah in Chinoiserie, Whimsical Chinoiserie Meeting in the Pavilion, Emerald Leopard in Bloom,
  Emerald Teal & Celadon Leatherette, Very Merry Wreath Premium (holiday card keeps its holiday band colours). Pixel diff vs the old
  cards: only the band strip changed, the other 33 cards identical. juniper_final.py no longer sets no-code bands; gen2.py refuses one
  on any card with a partner piece (scripts/checks/card_code_band_check.py; CLI scans every spec + manifest). Caption notes
  ("No code for <brand>", Mahjong Register note) unchanged on the page.
- Block rebuilt `build_block.py 3ad554c9...` (images @3ad554c9) + lightbox pinch fix (site/livepatch/lightbox-zoom-nov08/README.md),
  block @44f61ea5, pasted in Chrome (editor confirmed Juniper's block: 105 x "Juniper", 0 x Papaya, old pin @4d61e0df).
- curl live: 42 mm3-c (5 holiday), 47/47 images @3ad554c9 = 200, the 9 new cards md5 = repo files, pinch fix present.

## Cards (assets/cards/juniper-final/, 42 + manifest.json, her order 1..42)
Spec scripts/albumcard/specs/juniper_final_nov07.json (built by juniper_final.py from the round-3 / holiday / to-see / OMM-adds specs),
`JUNIPER_SPEC=... python3 scripts/albumcard/specs/juniper_build.py <work> && python3 scripts/albumcard/gen2.py <work>/spec.json assets/cards/juniper-final`.
Pixel diff vs the reviewed cards: only the code bands changed (9 cards) + Green Malachite's photo:
- NOT A PARTNER : NO CODE: Palm Royale (Mahj Tile Haus), The Kerry + Merrye (Betty June & Jeannette), Evergreen (That Mahjong Moment),
  Cheetah in Chinoiserie + Whimsical Chinoiserie Meeting in the Pavilion (Sophie Clima).
- NO CODE AT THIS TIME: the 3 Mahjong Register cards (Emerald Leopard in Bloom, Emerald Teal & Celadon Leatherette, Very Merry Wreath
  Premium): MAHJMATCH does not apply there (cart test Nov 7, docs/OVERDUE.md). Re-render these 3 when their code works.
- Green Malachite (Mahj Squad): every Mahj Squad photo but one has MAHJ SQUAD overlay watermarks; card uses the only clean product image
  (mats-191, library table shot, navy racks sit on the mat), cropped to the mat and EDSR x4 (assets/colorcards/juniper/mats/green-malachite-mahj-squad.jpg).
- Holiday cards (38-42) keep the HOLIDAY MATCH band + flame-heart.
The same 42 files were copied over assets/cards/juniper/ so the review/intro tools pick up the final bands.

## Also updated
- Colour card (config/colorcards.json juniper: top 3 = Palm Royale, Flora Belle, Lotus Cove; 42) re-rendered.
- Profile (config/profiles/juniper.json: matches 42, first_dates/album_peek/her_type #2 = Flora Belle): profile story + intro carousel re-rendered ("See all 42").
- FYM: config/picks/juniper-fym-m-2026-11-07.json (42 keys in her order) + builder/fym_fix_nov07/juniper_m118.py, wired into build118.sh after picks118.py (m + locks + m_hidden_ok for LBB Paint Feathers neoprene, hidden in FYM).

## Still to do (NEW-ALBUM-CHECKLIST)
- FYM: Juniper `album` link + m-list ship with the 1.18 build (three places + gallery).
- Social row (Planoly drafts), FB group post, FYM tie-in, "new albums" email to subscribers: Main / social owners.
- ~~Mahjong Register: re-render 3 bands + page chips~~ DONE Nov 8 (bands @3ad554c9; chips '10% off at Mahjong Register with MAHJMATCH (excludes racks and other brands' products)' block @34502290, pasted in Chrome, curl 0 old / 3 new, 42 cards, 47/47 images 200).
