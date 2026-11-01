# /christmas-mahjong-mats stock labels (Nov 1 2026, ~night ET)

Standing authority (CLAUDE.md: broken links / stale product info). Source of the block: site/livepatch/oct18b/gallery.html (live == repo before this change, sha256 4073ec7c…; after ac2ce629…, + 1 trailing space live).

Stock re-checked tonight for all 40 cards (/products/<handle>.js `available`, products.json fallback):
- RETIRED (gone: /products/sugarplum-mat 404 + not in ohmymahjong.com/products.json, 243 products): OMM Sugarplum. Grey "Retired" pill, image + "Shop the mat" links removed (no dead link), text "Retired · no longer sold"; her match line (22 tile sets · See matches) kept.
- SOLD OUT (store says unavailable; may restock, so shop link stays, text "Sold out · see the mat", grey "Sold out" pill): Mahj Squad Candy Cane Pink Wonderland; Britt Mills Merrywood, Winter Berry, Nutcracker (neoprene); Mahj Mood Sleigh All Day; Virora Hiverelle.
- Everything else in stock (PLM Holiday 13 designs: every variant available; Mahjong Register preorders available).

transform.js = the exact function run in node and on the Squarespace CodeMirror doc (apply.js for node). live-before.html = rollback copy.
Restock: remove the card from SOLD in transform.js (or hand-edit the card: drop `is-sold`, the pill, restore "Shop the mat"). No layout change; no jsDelivr assets added.
