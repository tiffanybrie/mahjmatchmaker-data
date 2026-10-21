# Petalée (Virora Mahjong): cards from her finished swipe, staged Oct 20 (NOT live, no album page yet)

**Source:** her Petalée swipe book (artifact JMaCDUwEZf528PX13x9mKa). She marked it done on Oct 18 at 3:18pm ET (`petalee_status/done`), and on Ready to Ship `l-petalee-swipe` she said "I already finished". The Oct 18, 7am draft (`assets/cards/petalee/`, 38 cards) was built before she finished.

## What's staged
- **61 cards** in `assets/cards/petalee-oct20/`, commit `7a6706c`, one per **yes** (`v == 'y'`) in db `petalee`. That's 62 yeses minus 1 held. Build: `scripts/albumcard/oct20/petalee_build.py`, then `gen2.py`. The manifest lists the order, stars, notes, photo source and racks for each card.
- **23 new yeses since the 38-card draft:** Amanda Toppe Limelight, Petalwood, Pink Orchids and Pink Winds; Beyond the Ribbon; Lovely Lavender Double-Sided (Mahjong Register); Color Splash; Coralia; Lavender Garden Party; Limoncea; Paisley Jubilee Premium; Petalwing; The Eloise Collection; Vivara; Year of the Horse; Bloomjong Lakeside (Side A); and retired OMM Amethyst, Birdie Pink, Camellia, Citrus Songbird, Garden Party, La Fete and Zen Glow.
- **Order (a draft for her to reorder in Ready to Ship):** her 15 starred yeses first, in deck order (cards 1–15). Next come the 2 yeses whose note says "Top pick" but aren't starred (Girly, Chinoiserie Songbird, cards 16–17). The rest follow in deck order.
- **Tile racks (Claude's pick from Oct 18, still waiting on her OK):** MMSIO, B&B Lavender, PLM Chartreuse. **Mat racks:** her saved registry where the mat has one (Rainbow Row, Pink Floral Chinoiserie, Chinoiserie Songbird, Deep Green Garden Party, Rally in Pink, Posy Pop Watercolor), otherwise `matpick.py`.
- Footers follow the existing Petalée rule, so Amanda Toppe cards say 20% OFF and Anders Ruff cards say SAVE WITH CODE. Note: the Malachite Serenity card says 10% for Amanda Toppe, so the two sets are inconsistent. Her call which is right.

## Needs her
1. **Held, no photo:** `cc-boots-bubbles-neoprene-mahjong-mat` (Bam Bird Boutique). The Boots & Bubbles Soft Blue variant has a card (#30).
2. **Starred but not a yes** (she starred them, then the vote ended as skip): Porcelain Bloom (Mahj & Vine), Blue Willow (Amanda Toppe), Imperial (OMM retired), Lorelei (OMM), Aria (Britt Mills). Are these yeses? They are not in the set.
3. **Photo notes:** Petalwing (#49) and Coralia (#54) are Virora book photos, and a size-ruler mark shows at the left edge. Pink Floral Chinoiserie (#3) carries her note "Need better pic if possible", and it is still the registry close-up.
4. Approve the tile racks, then put the cards in order.
5. Her end-of-swipe note lists other tile sets that matched some of these mats (e.g. Bloomjong Lakeside → Taylor, Luminaire, Limoncello, Sorbet, Moonlight, La Fete, Amara, Pearlescent, Coquette). It is saved in the db `petalee_status/done` for the expanded-matches pass.

## Live step
None yet. The album page is built after she orders the cards and OKs the racks (doc 86 steps 6–7). Then follow the Papaya page steps (`site/livepatch/papaya/README.md`) with `scripts/albumcard/oct20/album_block.py`. A Virora Petalée tile-set shop URL is also needed for the hero button, since none is in our data.

## Oct 21: waiting on her one tap (still NOT live)
- Checked: no approval anywhere. RTS `ship` has only `l-petalee-swipe` ("I already finished", the swipe), HQ need `petalee-swipe` was closed with "album build paused until after launch", and no `l-final-petalee` existed. The live URL 404s.
- RTS: the stale "Finish swiping Petalée" item was replaced in place by **`l-final-petalee`** "Petalée album: approve your 61 cards" (card group `c5-petalee`, cover + 61 cards as RTS assets, contact sheet `qa/contact-sheet.jpg` as the item image). It is #2 in `NOW`. Looks good = approve the draft order, tile racks (MMSIO, B&B Lavender, PLM Chartreuse) and per-mat racks; the 5 starred-skips and Boots & Bubbles Periwinkle stay out unless she names them.
- HQ: need `petalee-swipe` reopened as "Approve the Petalée album (61 cards)", This week, due Fri Oct 23. `hq/albums` has a Petalée row (owner tiffany).
- Before publishing after her yes (our job): re-render only if the 10% band sweep hasn't reached these cards (Amanda Toppe cards say 20%, Girly/RMS says 15%); look for cleaner Petalwing/Coralia photos (ruler mark) and a better Pink Floral Chinoiserie; independent QA on the contact sheet; then the Papaya page steps with `scripts/albumcard/oct20/album_block.py`. Still need a Virora Petalée shop URL for the hero button.
