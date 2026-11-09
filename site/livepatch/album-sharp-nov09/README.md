# Album-page soft cards (Nov 9 2026, ~5-6am): 35 of 41 fixed, LIVE

The tighter blur gate from holiday-qa-nov09 (`scripts/checks/card_sharpness.py`) failed 41 album-page cards.
35 are fixed live with tonight's method: re-render from the LIVE figure (same title, title colour, tile photo,
tile-brand logo, rack captions, footer), only the mat photo changes; then one src swap per page. 6 stay open (below).

## What changed (22 pages, one code block each, 35 src swaps; pin `3892844469cbe661ca5761e2bb9963b51e83de7c`)
- **PLM pink plaid x28** (Sugarplum Plaid x17 from missed-nov07 + Peace Love Holiday x11 from holiday-v4, same mat):
  brand 1512px variant photo (HolidayMat-SugarplumPlaid_1.jpg, the same source as the holiday page, pin e52f2827).
  r .203/.237 -> .253. Note: the whole-mat framing now shows PLM's own round logo printed top-left on the mat
  (the old Peace Love Holiday crops cut it off; the old Sugarplum cards already showed it).
- **Bespoke Holiday Love Red & Green x3** (Jade, Nantucket, Palm Royale): the 706px Side A screenshot (Tinselle source). r .233 -> .293.
- **Bespoke Holiday Love Blue x4** (Birdie, Moonlight, Osler, Smith): Side A screenshot 732x722
  (Screenshot2026-06-28at9.43.38AM.png). The 1500px "Untitled" image is both sides side by side, about 750px each, so it is no bigger. r .236 -> .299.
- Kept exactly as the old card (passed explicitly in `jobs.json`): Pippa title colour #e1ab13 (pairs.json tc, not in
  colorcards), Coquette + Peace Love Holiday footer "SHOP THE MATCH : MAHJMATCHMAKER.COM", Seabreeze + Peace Love Holiday
  tile-brand logo Oh My Mahjong. The other Seabreeze cards on the page show Yellow Mountain, so the page is not consistent. That was already so and is left for Matches & Catalog.
- Amara + Peace Love Holiday keeps its live caption rack "Mahjong Row & Co. Scalloped Tortoise". The card shows it too, as before.
  Mahjong Row has been out of the site since Nov 6, so Matches & Catalog should swap that rack.

## Files
- `mkjobs.py` (live figure -> job), `rerender.py` (copy of holiday-fix-nov09/rerender.py + loose tile mode for Tortoise),
  `jobs.json` (35 jobs incl. the col/code/tile_brand overrides), `swap.json` (page -> [old, new]), `swap_sharp.js`.
- Cards: `assets/cards/album-sharp-nov09/` (35). Contact sheets (old | new): every card was checked by eye, and the 5
  differences above were fixed and checked again.

## Paste (Chrome, one tab)
In /config/pages: search the page, Edit, select the one code block, then pencil. Then `sharpSwap(doc, pairs)`: every old src must match
exactly once and the length change must equal the expected sum. Dispatch, **wait 2s, click into the code, type a space then Backspace,
wait 2s**, Escape, Save. LESSON: an Escape straight after the dispatch dropped the change on 20 pages: Save
went grey and nothing was saved. They were redone with the waits. Check by curl, not by the Save button.

## Verify (curl, Nov 9 ~6am)
22/22 pages: 35/35 new srcs present, 0 old; every figure is identical to before (h3, brand, shop link, tile + mat racks,
holiday class) except the img; 35/35 new jsDelivr images 200. Full scan `card_sharpness_check.py`: 2178 cards, 41 -> 6 FAIL.

## Still open (6). No better brand photo was found, so each needs a flat file from the brand or an allow-list entry with a reason
- Amara + Chinoiserie (Britt Mills, old 750w gen.py card): brittmillsdesign.com has 3600px listing images (Colorful
  Chinoiserie neoprene + leatherette). A SIFT pixel-patch into the 1080 original measured r .291, but by eye it looked
  no sharper and showed seams in the coral border, so it was not shipped. A real fix means re-rendering the card in gen2 style. That would change
  its look and rack art (the old card has no rack captions), so it needs her OK or a Matches & Catalog decision.
- Papaya Spritz + Boots & Bubbles in Periwinkle (Bam Bird): every periwinkle photo on the brand site is <= 900px or a
  lifestyle shot; the 5472px shots show the periwinkle mat only half-covered by the other two colours.
- Solara + Vintage Floral Gingham (Mahj & Moon): the largest flat is 906/1024px (5000px image = a shipping-info graphic).
  The old card zooms in, so no gain is possible without changing the framing.
- The 3 old ones: Brownstone Bloom + Neutre Blanc, Coquette + Bejeweled Dream, Lagoon + Gray Malin.
