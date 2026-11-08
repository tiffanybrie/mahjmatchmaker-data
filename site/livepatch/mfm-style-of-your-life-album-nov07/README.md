# My Fair Mahjong: The Style of Your Life Series (Pearl Green), album set (Nov 7, built like Juniper)
Tiffany Nov 7 7:03pm: "My Fair Mahjong (the set that looks like Juniper) next" + asked whether to do it together with Juniper or apart.
Set = THE STYLE OF YOUR LIFE SERIES | Pearl Green (myfairmahjong.com/products/style-of-your-life-series, Dillard's exclusive, Grand size).
Her Oct 28 3:31pm album order had it #1 and she said it looks like the OMM green set (= Juniper). No other MFM set is close (Park = mint melamine, Crystal Confetti Citrus Green = clear/lime).
Status: DRAFT, NOT published. myfairmahjong.com shows it SOLD OUT online (available=false, Nov 7); pair mat Parquet Petal = "coming soon".

Page: style-of-your-life-album.html (built `python3 build.py <sha|local> <out>`; pinned version uses jsDelivr @ the commit SHA).
Self-contained copy: scratchpad mfm-album/ (index.html + files.json, relative paths).

Pieces:
- Album tile photo (PILE): assets/tiles/album/style-of-your-life.jpg (MFM image StyleofYourLifeSeries_11, square crop). Index entry added.
- Colour card: config/colorcards.json sets.style-of-your-life -> assets/colorcards/style-of-your-life/ (`python3 scripts/colorcards/build.py style-of-your-life`).
  Colours measured from the pile + flat lay: Pearl Green #0e9a5a (malachite swirl), Deep Green #0a4a25 (middle layer); faces Indigo #393c90 (main ink), Wine #902836, Bubblegum Pink #f590b8, Cornflower #80acdf, Marigold #e79d15, Fern Green #4f9a60.
  Tagline: "Seeking: navy with a pink streak. / Retail therapy a plus." (new, not Juniper's or Papaya's).
- Colour wheel: assets/colorwheels/style-of-your-life-color-wheel.jpg (wheel.py: WHEEL_FACES + new WHEEL_EXTRA_BACKS = White Face so the 3+3 legend reads backs/faces correctly).
- Cover: assets/covers/albums/00-style-of-your-life-mahjong-tiles-cover.jpg (+ w800). `FRAME=frame3.png python3 scripts/covers/album_cover_omm.py <MFM _11 full> scripts/covers/holiday/mfm_white.png 150 "Style of<br>Your Life" "11,107,58" <out>`. mfm_white.png = white version of MFM's site logo.
- Faces: 50 cutouts assets/tiles/faces/style-of-your-life/clean/ (grid cut from MFM flat lay StyleofYourLifeSeries_2). Claude's 4: dragons pair, 1 Bam hummingbird, lipstick joker, 9 Crak pink hobo.
- Match cards: 22, assets/cards/style-of-your-life/ + manifest.json. Spec = scripts/albumcard/specs/style_of_your_life_round1.json; `python3 scripts/albumcard/specs/style_of_your_life_build.py <wd> && python3 scripts/albumcard/gen2.py <wd>/spec.json assets/cards/style-of-your-life`.
  Navy v3 logo, true_len racks. Hi-res mat photos from the brands' product JSON: assets/colorcards/style-of-your-life/mats/.
- Tile racks: My Fair Mahjong Indigo Blue + Magenta (same solid acrylic rack, 20in; FYM v99 cutouts -> assets/racks/card/, index + rack-lengths entries). Malachite Dapple skipped: black with neon green dapple, stack photo only.

Picks method: hue-family measurement over 1,705 gallery/retired mat photos (green + indigo/pink/wine/cornflower/marigold, minus chartreuse/teal/coral), then 3 by-sight passes with the tile pile inset on each mat. Mahjong Row mats checked on merit: none fit (earthy). Amahj Pink, Blue + Green dropped (angled photo on white).
Juniper overlap: 3 shared mats (Green Malachite, Garden Glow Emerald, Cheetah in Chinoiserie) sit at the bottom as "Also in Juniper"; none of Juniper's top 7 is used.
Open: TNT (Tiles & Tablescapes) search for this set not done (needs Chrome; book_gate requires it before any swipe book). Dating profile + intro carousel not built yet (follow her face picks, as Juniper). Pronoun: drafts say "her".
