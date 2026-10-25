# Catalog naming traps (Oct 25, after Bespoke went missing twice)

A title search for "tiles" / "mat" misses whole product lines. Every catalog harvest and audit must classify by product type,
description and photo, and must check these brands by hand:

- **Bespoke Mahjong**: tile sets are named by design + colour only ("LUCKY CHARMS - MARSHMALLOW PINK"), product_type "Mahjong Sets",
  which also holds ~40 $0 table-top design swatches and $4,250+ table bundles. Real sets cost $380–$590. No Mega/XL (Tiffany Oct 23).
- **Peace Love Mahjong**: "Tiles + Tile Pouch + Dice" (a pouch/dice filter throws them out).
- **Charleston Mahjong Club**: "… Edition™".
- **The Royal Mahjong Society**: "Studio Series".
- **Mahj Mood**: "… Collection".
- **My Fair Mahjong**: "THE … SERIES".
- **Wren Mats**: mat titles without "mat".

Full Oct 25 audit: docs/catalog-audit-oct25.md (machine list: config/catalog-audit-oct25-missing.json). Rerun scripts were in the
Matches chat scratchpad (catalog-audit/v2.py, final.py, report.py).
