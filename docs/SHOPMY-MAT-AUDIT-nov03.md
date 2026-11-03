# ShopMy mat check: Nov 3 (weekly, Tuesday)

Scheduled task trig_01NpQoJYSYh2GCLwcHNpkDiU, run Tue Nov 3 ~9:30am ET. **Nothing published. Nothing edited on ShopMy.**

**Source:** her public ShopMy shop read through the public API (api.shopmy.us/api/Users/username/mahjmatchmaker for the collection list, apiv3.shopmy.us/api/Collections/<id> for pins), 33 public collections, 637 pins. Compared by `go.shopmy.us/p-<id>`, Etsy listing id and Amazon ASIN against FYM 1.13 (artifact 6epA9HuEdT32zUp79Qv3kd, `D.mats`, 1664 mats), config/mat-gallery-extra-rows.json, every config/*.json, and the Oct 26 audit list (assets/qa/shopmy-oct26/outstanding.json).

**Method notes for next week:**
- Pin photos: `https://static.shopmy.us/pins/<file name of the pin image>` downloads from the shell (the S3 URL in the API is 403). No browser needed for photos.
- Etsy listing pages: DON'T fetch them in a loop from her Chrome. Six quick fetches tripped Etsy's "Access is temporarily restricted" page on her browser today (it clears on its own). One listing at a time, or skip Etsy and use the ShopMy pin photo.
- Full gate can't run in a cloud clone (it needs work/albums.json and scripts/social/its_a_match/albums-live-oct21.json, which aren't in git). Ran the patch on a copy of 1.13 + targeted checks instead (see below).

## Counts

| Group | New | Result |
|---|---|---|
| Etsy (incl. Etsy brands) | 34 | 33 staged for the next build (32 visible, 1 Questionable hidden), 1 held for her call |
| Amazon | 3 | 1 mat to pick (Santa & Reindeer), 2 are tablecloth-style table covers |
| Skipped | | 10 Sophie Clima art prints (Etsy Mats shelf, not mats, same as Oct 26), 3 Amazon tablecloths, Sweet Jojo Boho Wildflower (already in FYM), Mahj & Moon 13 (already in FYM via the Oct 31 ShopMy links), partner-brand shelves (CMC, Mahj & Vine, BAM, OMM x LSF: partner mats come in on store links) |

Biggest new item: **Luna EK Studio Mats (Etsy)**, the 28-mat collection she made Oct 29. None of it was in FYM.

## (a) Etsy: staged, not published

Spec: `config/fym-etsy-shopmy-nov03.json`. Patch: `builder/fym_fix_nov03/etsy_shopmy_nov03.py <build_dir>` (copy of v95_etsy.py with this spec; packs new mc chunks, inline thumbs, measured colours, appends to D.order + every set's rank, writes mat_photo_flags + fym_questionable). Photos: `assets/mats/shopmy-nov03/` (ShopMy pin photo, 600px; Luna mockups cropped to the mat). Contact sheets: `assets/qa/shopmy-nov03/etsy-1.jpg` (as on ShopMy, numbered) and `assets/qa/shopmy-nov03/etsy-cropped.jpg` (the photos FYM will use; LOOKED at, all show the mat and its colours).

None are holiday (no Christmas, Hanukkah or winter scene). No code claim; link = her go.shopmy.us link.

| # | Brand | Mat | Photo | Shelf | ShopMy link |
|---|---|---|---|---|---|
| 1 | Betty June & Jeannette | Grace (Peacock) | Questionable (added hidden) | Betty June Jeannette (Etsy) | https://go.shopmy.us/p-96128868 |
| 2 | Betty June & Jeannette | Grace Watercolor | crop to mat | Betty June Jeannette (Etsy) | https://go.shopmy.us/p-96126993 |
| 3 | Betty June & Jeannette | Grace Abstract | photo OK | Betty June Jeannette (Etsy) | https://go.shopmy.us/p-96126603 |
| 4 | MahjjMaven | Strawberry Thief | photo OK | Etsy Mahjong Mats | https://go.shopmy.us/p-98960851 |
| 5 | AussieHannaGift | Pink Hummingbird | photo OK | Etsy Mahjong Mats | https://go.shopmy.us/p-98951063 |
| 7 | Luna EK Studio | Sage Green Botanical | crop to mat | Luna EK Studio Mats (Etsy) | https://go.shopmy.us/p-98960232 |
| 8 | Luna EK Studio | Forest Bird Bloom | crop to mat | Luna EK Studio Mats (Etsy) | https://go.shopmy.us/p-98959997 |
| 9 | Luna EK Studio | Herbal Drawing Butterfly Border | crop to mat | Luna EK Studio Mats (Etsy) | https://go.shopmy.us/p-98959494 |
| 10 | Luna EK Studio | Fern Berry Wreath | crop to mat | Luna EK Studio Mats (Etsy) | https://go.shopmy.us/p-98957729 |
| 11 | Luna EK Studio | Spring Pond Dream | crop to mat | Luna EK Studio Mats (Etsy) | https://go.shopmy.us/p-98957374 |
| 12 | Luna EK Studio | Dark Wood Butterfly Fungi | crop to mat | Luna EK Studio Mats (Etsy) | https://go.shopmy.us/p-98957208 |
| 13 | Luna EK Studio | Lotus Breeze Koi | crop to mat | Luna EK Studio Mats (Etsy) | https://go.shopmy.us/p-98956920 |
| 14 | Luna EK Studio | Crane Square Panel | crop to mat | Luna EK Studio Mats (Etsy) | https://go.shopmy.us/p-98956801 |
| 15 | Luna EK Studio | Umbrella Koi Pond | crop to mat | Luna EK Studio Mats (Etsy) | https://go.shopmy.us/p-98956702 |
| 16 | Luna EK Studio | Swallow Peony Dance | crop to mat | Luna EK Studio Mats (Etsy) | https://go.shopmy.us/p-98956581 |
| 17 | Luna EK Studio | Meadow Butterfly Border | crop to mat | Luna EK Studio Mats (Etsy) | https://go.shopmy.us/p-98956499 |
| 18 | Luna EK Studio | Japanese Sakura Scene | crop to mat | Luna EK Studio Mats (Etsy) | https://go.shopmy.us/p-98956123 |
| 19 | Luna EK Studio | Crane Lantern Pattern | crop to mat | Luna EK Studio Mats (Etsy) | https://go.shopmy.us/p-98954388 |
| 20 | Luna EK Studio | Pondside Bloom Ripple | crop to mat | Luna EK Studio Mats (Etsy) | https://go.shopmy.us/p-98954311 |
| 21 | Luna EK Studio | Terracotta Botanicals | crop to mat | Luna EK Studio Mats (Etsy) | https://go.shopmy.us/p-98954133 |
| 22 | Luna EK Studio | Blossom Pavilion Waterscape | crop to mat | Luna EK Studio Mats (Etsy) | https://go.shopmy.us/p-98953996 |
| 23 | Luna EK Studio | Jade Bamboo Garden Frame | crop to mat | Luna EK Studio Mats (Etsy) | https://go.shopmy.us/p-98953916 |
| 24 | Luna EK Studio | Hummingbird Floral Frame (Blue) | crop to mat | Luna EK Studio Mats (Etsy) | https://go.shopmy.us/p-98953643 |
| 25 | Luna EK Studio | Celadon Blossom Garden | crop to mat | Luna EK Studio Mats (Etsy) | https://go.shopmy.us/p-98953433 |
| 26 | Luna EK Studio | Terracotta Floral Tapestry | crop to mat | Luna EK Studio Mats (Etsy) | https://go.shopmy.us/p-98953325 |
| 27 | Luna EK Studio | Cloud Crane Floral Frame | crop to mat | Luna EK Studio Mats (Etsy) | https://go.shopmy.us/p-98953246 |
| 28 | Luna EK Studio | Purple Bellflower Moths | crop to mat | Luna EK Studio Mats (Etsy) | https://go.shopmy.us/p-98953119 |
| 29 | Luna EK Studio | Lotus Garden Frame | crop to mat | Luna EK Studio Mats (Etsy) | https://go.shopmy.us/p-98953050 |
| 30 | Luna EK Studio | Koi Flower Pond | crop to mat | Luna EK Studio Mats (Etsy) | https://go.shopmy.us/p-98952869 |
| 31 | Luna EK Studio | Lotus Garden Koi | crop to mat | Luna EK Studio Mats (Etsy) | https://go.shopmy.us/p-98952727 |
| 32 | Luna EK Studio | Black Gold Koi | crop to mat | Luna EK Studio Mats (Etsy) | https://go.shopmy.us/p-98952607 |
| 33 | Luna EK Studio | Moth Floral Wreath | crop to mat | Luna EK Studio Mats (Etsy) | https://go.shopmy.us/p-98952381 |
| 34 | Luna EK Studio | Hummingbird Floral Frame (Mint) | crop to mat | Luna EK Studio Mats (Etsy) | https://go.shopmy.us/p-98952008 |

**Held, not staged:** #6 Custom Football Mahjong Mat (BettyJuneJeannette, For The Guys shelf, https://go.shopmy.us/p-96129391): a team-colour custom stadium graphic with no fixed colourway to match. Her call.

**Test on a copy of FYM 1.13:** patch ran clean (1664 → 1697 mats, 3 new chunks mc/244-246). Targeted checks PASS: no existing mat changed, every new link is go.shopmy.us ([9]), no code claim, none holiday, Questionable ⇔ hidden ([3d]), every new mat has a photo flag ([6]), in D.order and every set rank, chunk images decode, MCB registers 244-246. **The Matches & Catalog build must still run the full `builder/fym_gate.py` and independent QA (rules 1-2).**

**Colours to check by eye in the build** (the measurer folds earthy/brown into "dark", and muted greens read neutral): Sage Green Botanical measured neutral only (it's sage green); Terracotta Floral Tapestry measured dark only (terracotta/red); Purple Bellflower Moths has no purple; Cloud Crane Floral Frame measured dark only (cream/orange/navy). Luna mats in general skew "dark".

## (b) Amazon: never auto-added

Contact sheet `assets/qa/shopmy-nov03/amz-1.jpg`. These three sit on her styled holiday-table shelves (pinned Oct 20) and weren't listed on Oct 26.

| # | Mat | Grade | Suggest | Note | ShopMy link |
|---|---|---|---|---|---|
| 1 | Tartan Plaid All-in-One Mahjong Mat (A Classic Plaid Holiday Table) | C | skip | It's a full-drop green tartan table cover, not a mat. | https://go.shopmy.us/p-96237159 |
| 2 | Santa & Reindeer Mahjong Mat (A Reindeer Holiday Table) | B | skip | Vintage Santa + reindeer on sage stripe, candy-cane border with "walls left / play right" text. Flat photo, holiday. Novelty-leaning. | https://go.shopmy.us/p-96233460 |
| 3 | Red Plaid All-in-One Mahjong Mat (A Retro Holiday Table) | C | skip | Red tartan table cover with a green wreath top; same ASIN as the Hunnmingre tablecloth. | https://go.shopmy.us/p-96234587 |

HQ needs card: `amazon-picks-2026-11-03`.

## Full data
`assets/qa/shopmy-nov03/new.json` (all 37 with image URLs).
