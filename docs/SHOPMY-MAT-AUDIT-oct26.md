# ShopMy mat audit: what's not in Find Your Mat-ch / Mat Gallery yet (Oct 26)

Asked by Tiffany Oct 26 10:22am ("bring in my Etsy shop mats... at minimum Etsy. We could talk about Amazon. I don't want to clutter holiday with mats that aren't great"). **Audit only: nothing added to the app or gallery.**

**Source:** her public ShopMy shop (shopmy.us/mahjmatchmaker), read Oct 26 ~10:25am via the public collections API (read-only), checked against FYM build b94 (`D.mats`, by `go.shopmy.us/p-<id>` link and by name) and the staged Mat Gallery (matgallery-v5.html, which has the same 41 ShopMy links as FYM). Shelves read: Etsy & Amazon Holiday Mats (65 pins), Etsy Mahjong Mats (25), Amazon Mahjong Mats (34), Betty June Jeannette (26), Rebecca Illustrated Mats (10), Halloween Mahjong Table, Merry Mahjong, The Mahjong House, and every other shelf scanned for mats.

**Photo bar used:** FYM rule 6 (low bar). *photo OK* = usable as is; *crop needed* = mat is clear but there's a carry bag/roll beside it, a text banner, or a room/people around it (crop to the mat per gate [50]); *Questionable* = mat angled/covered/too small, or no usable image. Holiday = Christmas, Hanukkah, winter snow/ski only.

**Contact sheets** (numbers below = tile numbers on the sheet): `assets/qa/shopmy-oct26/etsy-yr-1.jpg`, `assets/qa/shopmy-oct26/etsy-hol-1.jpg`, `assets/qa/shopmy-oct26/amz-yr-1.jpg`, `assets/qa/shopmy-oct26/amz-yr-2.jpg`, `assets/qa/shopmy-oct26/amz-hol-1.jpg` (1-20), `assets/qa/shopmy-oct26/amz-hol-2.jpg` (21-40), `assets/qa/shopmy-oct26/amz-hol-3.jpg` (41-49), `assets/qa/shopmy-oct26/other-1.jpg`. Full data incl. image URLs: `assets/qa/shopmy-oct26/outstanding.json`.

## Counts

| Group | Outstanding | Photo OK / crop / Questionable |
|---|---|---|
| (a) Etsy year-round | 7 | {'crop needed': 3, 'Questionable': 1, 'photo OK': 3} |
| (a) Etsy holiday | 14 | {'photo OK': 11, 'crop needed': 2, 'Questionable': 1} |
| (b) Amazon year-round | 35 | grades {'A': 12, 'B': 17, '?': 1, 'C': 5} |
| (b) Amazon holiday | 48 | grades {'A': 18, 'B': 19, 'C': 11} |
| Other ShopMy-only mats (not Etsy/Amazon) | 14 | {'photo OK': 6, 'Questionable': 4, 'crop needed': 4} |

Already in (not outstanding): all 11 Sophie Clima Etsy mats + Chinese Landscape (Etsy), 18 BJ&J mats incl. Allie, Benjamin and Hippie Holiday (her Etsy & Amazon Holiday shelf has a second pin of Hippie Holiday), Tala 11, Sweet Jojo Boho Wildflower (Amazon link), Rebecca Rainbow Row. The Etsy Mahjong Mats shelf also holds 10 Sophie Clima **art prints** (not mats, skipped). Two Amazon **tablecloths** on the holiday shelf (Irenare, Hunnmingre) are skipped.

Things to know before adding:
- Most Amazon photos have the carry bag or rolled mat beside the mat: crop-to-mat (config/fym-mat-focus) is needed on almost all of them, not a reason to drop them.
- Etsy year-round #1-3 and BJ&J Kristen / Julia / Gigi / Chinoiserie Cheer were looked at on Oct 20 and hidden under the stricter photo bar. Under the Oct 21 low bar, Lemon Lime, Julia and Gigi pass.
- Amazon year-round #7-10 are pink-tiger lookalikes of YOLO Mahjong's Pink Tiger (in FYM). Suggest at most one of them, or none.
- Plain plaids on the holiday shelf (Amazon holiday #4, 5, 7) have no holiday graphic. Amazon holiday #18 (green/blue stripe) is year-round.
- Brand name for Etsy shops: each listing needs its shop name filled in (the "Etsy shop (name TBD)" gap from Oct 20).

## (a) Etsy outstanding

### Etsy year-round (7)
| # | Mat | Photo | Note | ShopMy link |
|---|---|---|---|---|
| 1 | Savannah Soiree Mahjong Mat – Multi Color Game Mat, Neoprene Mahjong T | crop needed | Mahjong Made Chic (Etsy). "NEW ARRIVAL" banner + "Premium Bag" badge on the photo: crop the corners off or check the listing for a clean image. Hidden Oct 20 for the overlay. | https://go.shopmy.us/p-96122920 |
| 2 | Palm Beach Chic Custom Monogram Mahjong Mat / Neoprene Game Surface | Questionable | Lifestyle shot: people playing, mat at an angle. Check the Etsy listing for a flat shot; hidden Oct 20 for the same reason. | https://go.shopmy.us/p-96136953 |
| 3 | Lemon Lime Floral Mahjong Mat / Custom Monogram Neoprene Table Game Ma | photo OK | Flat-lay with racks and a drink on it, colours clear (fine under the Oct 21 low bar). Hidden Oct 20 under the old bar. | https://go.shopmy.us/p-96137022 |
| 4 | Neoprene Mahjong Mat Smooth Surface Wicker Frame Plaid Dark Green Plum | crop needed | New (added Oct 24ish). Wicker frame + plaid border; chairs around it: crop to the mat. | https://go.shopmy.us/p-96922692 |
| 5 | The "Kristen" Sweater Weather Mahjong Mat | crop needed | BJ&J Kristen (Sweater Weather). Angled on a table with tiles: crop/straighten, or Questionable if it will not crop cleanly. Not holiday: sweater-weather florals. | https://go.shopmy.us/p-96114198 |
| 6 | Blush Mahjong Mat / The "Julia" Mahjong Mat / Palm Beach meets Savanna | photo OK | BJ&J Julia (Blush). Tiles + racks scattered on it but pink/green colours fully readable. | https://go.shopmy.us/p-96123529 |
| 7 | Canvas Art inspired Mahjong Mat | photo OK | BJ&J Gigi (Canvas Art). Racks on the edges, colours clear. | https://go.shopmy.us/p-96126343 |

### Etsy holiday (14, all Christmas/winter)
| # | Mat | Photo | Note | ShopMy link |
|---|---|---|---|---|
| 1 | DECK THE HALLS Mahjong Game Mat / Preppy Christmas Ornaments / Travel/ | photo OK | Deck the Halls: preppy blue/pink/green ornaments. Strong. | https://go.shopmy.us/p-97343512 |
| 2 | Hand-Painted Christmas Mahjong Mat, Festive Holiday Game Night Decor ( | photo OK | Hand-painted pink/red garland border. | https://go.shopmy.us/p-97558178 |
| 3 | Christmas Nutcracker Mahjong Mat - Festive Holiday Toyland Design Game | photo OK | Nutcracker harlequin, hot pink/green. | https://go.shopmy.us/p-97557928 |
| 4 | Christmas Mahjong Mat, Whimsical Holiday Mah Jongg Table Mat, Colorful | crop needed | Whimsical skaters; feature call-out text + tiles on the photo: crop to the mat. | https://go.shopmy.us/p-97558047 |
| 5 | Personalized Christmas Mahjong Mat: Winter Village Tree, Red Bow Holid | photo OK | Winter village tree, red bows, gingham border (personalized). | https://go.shopmy.us/p-97343386 |
| 6 | Christmas Mahjong Mat | photo OK | Red/green holly + bow border on cream. | https://go.shopmy.us/p-97558867 |
| 7 | Mahjong Mat Gift for Her, Scandi Folk Christmas Theme  Mah Jongg Table | photo OK | Scandi folk, dark green. | https://go.shopmy.us/p-97559259 |
| 8 | Custom Mahjong Mat Gift for Her, Scandi Folk Christmas Theme  Mah Jong | photo OK | Scandi folk, white/cream (same shop as #7). | https://go.shopmy.us/p-97559200 |
| 9 | Christmas Ice Pond Vegan Leather Mahjong Mat Holiday Table Cover | photo OK | Ice pond skaters, vegan leather (winter scene). | https://go.shopmy.us/p-97558916 |
| 10 | Christmas Ice Skaters Vegan Leather Mahjong Mat Holiday Table Cover | photo OK | Ice skaters, vegan leather (winter scene). | https://go.shopmy.us/p-97558989 |
| 11 | Mahjong Mat, Green Christmas Watercolor Print - American Mahjong Gifts | photo OK | Green holly watercolor; tiles/racks around the edge only. | https://go.shopmy.us/p-97557757 |
| 12 | Nutcracker Merry and Bright MAHJONG Mat, Size 31.5" x 31.5", Sleek Sur | crop needed | Nutcracker trio, green lattice; "Printed & Shipped" banner at top-left: crop. | https://go.shopmy.us/p-97557636 |
| 13 | Mahjong Chinoiserie Christmas Tree Game Mat / 31.5" or 33" / Preppy St | photo OK | Chinoiserie Christmas tree in ginger jar, pink/green scallop. Very on-brand. | https://go.shopmy.us/p-97739404 |
| 14 | Chinoiserie Cheer Mahjong Mat | Questionable | BJ&J Chinoiserie Cheer: room shot, mat small + angled. Check listing for a flat shot. Hidden Oct 20. | https://go.shopmy.us/p-96124861 |

**Recommendation:** bring in all Etsy holiday mats except #14 (Questionable). #4 and #12 go in after cropping. Bring in the Etsy year-round mats marked OK or crop. Hold #2 Palm Beach Chic until there's a better photo.

## (b) Amazon outstanding

Grade = how well it fits the brand (Tiffany's taste: preppy, grandmillennial, chinoiserie, pink/green, clean pattern), not photo quality. A = bring in, B = fine if she wants volume, C = skip (casino/felt look, rules-text mats, novelty, washed out).

### Amazon year-round (35)
| # | Mat | Photo | Grade | Note | ShopMy link |
|---|---|---|---|---|---|
| 1 | Teal Green Chinoiserie Landscape Mahjong Mats For Table | crop needed | A | Teal/green chinoiserie landscape. Bag beside: crop. | https://go.shopmy.us/p-96196014 |
| 2 | Sage Green Chinoiserie Floral Mahjong Mats For Table | crop needed | A | Sage chinoiserie birds. Bag: crop. | https://go.shopmy.us/p-96196096 |
| 3 | Colorful Watercolor Floral Mahjong Mat 31.5" X 31.5" | photo OK | B | Watercolor wildflowers, rules text in border. | https://go.shopmy.us/p-96196170 |
| 4 | Green Tropical Animal Mahjong Mat 31.5" X 31.5" | Questionable | ? | Green Tropical Animal: ShopMy image is dead (403). Need a new photo before we can judge. | https://go.shopmy.us/p-96210384 |
| 5 | Coquette Pink Bow Mahjong Mat 31.5" X 31.5" | photo OK | A | Coquette pink bows. | https://go.shopmy.us/p-96210535 |
| 6 | Leopard Botanical Jungle Mahjong Mat 31.5 Inch | photo OK | A | Leopard botanical, cream/green. | https://go.shopmy.us/p-96210704 |
| 7 | Pink Tiger Moon Floral Mahjong Mat For Table | crop needed | A | Pink tiger + moon. Looks like a YOLO Mahjong Pink Tiger lookalike (YOLO is in FYM): her call. | https://go.shopmy.us/p-96210831 |
| 8 | Pink Tiger Floral Mahjong Mat For Table | crop needed | A | Pink tiger floral, red scallop. Same YOLO lookalike note. | https://go.shopmy.us/p-96210981 |
| 9 | Nuanchu Pink Tiger Mahjong Mat For Table | crop needed | B | Nuanchu pink tiger: third pink-tiger variant; pick one. | https://go.shopmy.us/p-96211090 |
| 10 | Mahjong Mat Set | crop needed | C | Pink tiger "Mat Set": scorecards/dice/bag props, mat smaller. Same design family as #8. | https://go.shopmy.us/p-96211229 |
| 11 | Mahjong Mat With Rules | crop needed | C | Floral "With Rules": props + bag, mat ~60% of frame, Charleston rules text. | https://go.shopmy.us/p-96211335 |
| 12 | Turquoise Floral Bird Chinoiserie Mahjong Mat 31.5 X 31.5 Inch | crop needed | A | Turquoise chinoiserie birds. | https://go.shopmy.us/p-96211453 |
| 13 | Blue Chinoiserie Almond Blossom Mahjong Mat 31.5 X 31.5 Inch | crop needed | A | Blue almond blossom (Van Gogh). | https://go.shopmy.us/p-96211598 |
| 14 | Green Mahjong Mat 31.5 X 31.5 Inch | crop needed | A | Green birds + trellis centre. | https://go.shopmy.us/p-96211720 |
| 15 | Vintage Floral Hummingbird Mahjong Mat | crop needed | B | Dark green vintage floral hummingbird. | https://go.shopmy.us/p-96211852 |
| 16 | Grandmillennial Blue Gray Floral Mahjong Mat 31.5x31.5 Inch | photo OK | B | Grandmillennial blue-grey damask (neutral). | https://go.shopmy.us/p-96212194 |
| 17 | Chinoiserie Lemon Tree Hummingbird Mahjong Mat 31.5x31.5 Inch | photo OK | A | Lemon tree hummingbird chinoiserie. | https://go.shopmy.us/p-96212656 |
| 18 | Emerald Green Chinoiserie Floral Bird Mahjong Mat 31.5x31.5 Inch | photo OK | B | Emerald chinoiserie, dark. | https://go.shopmy.us/p-96212791 |
| 19 | Drydiet American Mahjong Mat For Table 31.5x31.5 Inch | photo OK | B | Leopard + tropical, dark green/red. | https://go.shopmy.us/p-96213166 |
| 20 | Boho Dark Black Red Floral Mahjong Mat For Table 31.5"x31.5" | crop needed | C | Title says "Boho Dark Black Red Floral" but photo is a beige mountain landscape with rules text: listing/photo mismatch. | https://go.shopmy.us/p-96213291 |
| 21 | Vintage Green Chinoiserie Floral Mahjong Table Mat 31.5" X 31.5" | crop needed | B | Green vintage floral, Greek key. | https://go.shopmy.us/p-96213424 |
| 22 | Green Tropical Plants Mahjong Mats 31.5" X 31.5" | crop needed | B | Green tropical plants, sage centre. | https://go.shopmy.us/p-96213709 |
| 23 | Mahjong Mat 31.5" X 31.5" | crop needed | B | Rust/terracotta bird floral. | https://go.shopmy.us/p-96213841 |
| 24 | Beige And White Floral Chinoiserie Mahjong Mat 31.5" X 31.5" | crop needed | A | Beige/white floral chinoiserie (neutral). | https://go.shopmy.us/p-96213996 |
| 25 | Vintage Chinoiserie Cherry Blossom Mahjong Mat 31.5 X 31.5 In | crop needed | B | Cherry blossom, sage/tan. | https://go.shopmy.us/p-96214256 |
| 26 | Vintage Chinoiserie Mahjong Mat For Table | crop needed | B | Chinoiserie landscape, green Greek key. | https://go.shopmy.us/p-96214366 |
| 27 | Turquoise Pastel Floral Mahjong Mat For Table 31.5"x31.5" | crop needed | B | Iris watercolor border, turquoise. | https://go.shopmy.us/p-96214480 |
| 28 | Pale Turquoise Blue Mahjong Mat For Table 31.5"x31.5" | crop needed | C | Pale turquoise wash, dotted centre; weak pattern. | https://go.shopmy.us/p-96214696 |
| 29 | Chinoiserie Mahjong Mat For Table | crop needed | B | Pagoda + lotus. | https://go.shopmy.us/p-96214854 |
| 30 | L-Spoutto Pink Floral Mahjong Mat For Table | crop needed | B | Pink folk floral (L-Spoutto). | https://go.shopmy.us/p-96215791 |
| 31 | L-Spoutto Pink Mahjong Mat For Table | crop needed | C | Very pale wildflower, washed out. | https://go.shopmy.us/p-96215914 |
| 32 | Yellow Floral Mahjong Mat For Table 31.5x31.5 | crop needed | B | Bright yellow floral. | https://go.shopmy.us/p-96216016 |
| 33 | Navy Blue Citrus Orange Mahjong Mat 31.5x31.5inch | crop needed | A | Navy/citrus orange watercolor. | https://go.shopmy.us/p-96216110 |
| 34 | Gothic Raven Mahjong Mat 31.5" | crop needed | B | Gothic Raven (Halloween shelf). Halloween = year-round colour sections, NOT Holiday. | https://go.shopmy.us/p-96237389 |
| hol-18 | Stripes Mahjong Mat Non-Slip Neoprene Mat (on the holiday shelf, amz-hol sheet #18) | photo OK | B | Green + light blue stripes, scalloped. No holiday graphic: YEAR-ROUND, not Holiday. | https://go.shopmy.us/p-97609639 |

### Amazon holiday (48)
| # | Mat | Photo | Grade | Note | ShopMy link |
|---|---|---|---|---|---|
| 1 | Pink And Blue Christmas Mahjong Mat 31.5 X 31.5 In | crop needed | A | Pink/blue stripe, snowy village. Very on-brand. | https://go.shopmy.us/p-97606528 |
| 2 | Folk Christmas Reindeer Mahjong Mat Gifts 31.5x31.5 | crop needed | A | Folk reindeer, coral/cream. | https://go.shopmy.us/p-97607360 |
| 3 | Pink Christmas Tree Mahjong Mat For Table | photo OK | A | Pink gingham, pink trees + bows. | https://go.shopmy.us/p-97610459 |
| 4 | Christmas Plaid Mahjong Mat Set With Carrying Bag | crop needed | B | Red tartan, scalloped. Plain plaid: holiday or year-round is her call. | https://go.shopmy.us/p-97606175 |
| 5 | Green Scottish Plaid Mahjong Mat 31.5"x31.5" | crop needed | C | Green Scottish plaid, plain. Generic; reads year-round, not holiday. | https://go.shopmy.us/p-97606940 |
| 6 | Lewtemi Scalloped Mahjong Mat Set Noise Reduction Mat | crop needed | B | Red tartan scalloped + scorecard props (same as #4 style). | https://go.shopmy.us/p-97607568 |
| 7 | Mahjong Mat 31.5" X 31.5" Christmas Dark Tartan Plaid Red Green Gold C | crop needed | B | Dark green/red tartan. Plain plaid. | https://go.shopmy.us/p-97607737 |
| 8 | Winter Christmas Tree Mahjong Mat 31.5" X 31.5" | crop needed | A | Three snowy pines, sage stripe. | https://go.shopmy.us/p-97607894 |
| 9 | 31.5" Christmas Mahjong Mat | crop needed | C | Red felt-look centre, plaid border: casino look. | https://go.shopmy.us/p-97608672 |
| 10 | Tegeme Christmas Mahjong Mat For Table 31.5 X 31.5 Inch Red Snowflake | photo OK | B | Red snowflake/reindeer Fair Isle, scalloped. | https://go.shopmy.us/p-97608517 |
| 11 | Ngugr Vintage Boho Reindeer Christmas Rolled Mahjong Mat | photo OK | A | Boho folk reindeer, red on cream. | https://go.shopmy.us/p-97608051 |
| 12 | Mahjong Mat 31.5" X 31.5" Christmas Holly Leaves Red Berries Dark Gree | crop needed | A | Dark holly + berries, rich. | https://go.shopmy.us/p-97609005 |
| 13 | Christmas Golden Retriever Dog Mahjong Mat 31.5x31.5in | photo OK | C | Golden retrievers in Santa hats. Novelty. | https://go.shopmy.us/p-97607154 |
| 14 | Hspd Christmas Red Nose Reindeer American Mahjong Mat 31.5x31.5 | crop needed | C | Photo-real red-nose reindeer. Novelty. | https://go.shopmy.us/p-97608842 |
| 15 | Anydesign Christmas Scalloped Mahjong Mat | photo OK | A | Green/white cabana stripe, red bow scallop. | https://go.shopmy.us/p-97609169 |
| 16 | Drydiet American Mahjong Mat For Table With Bag | photo OK | C | Holly Jolly string lights clip art, flat green centre. | https://go.shopmy.us/p-97609333 |
| 17 | Mahjong Mat For Table Christmas Nutcracker Soldiers Festive Greenery B | crop needed | A | Nutcrackers + pink bows, green. | https://go.shopmy.us/p-97609502 |
| 19 | Red Christmas Soldier Poinsettia Plaid Mahjong Mats For Table | crop needed | B | Nutcracker + poinsettia, red gingham. | https://go.shopmy.us/p-97609805 |
| 20 | Christmas Mahjong Mat 33"x33" | crop needed | A | Blue toile nutcrackers, 33". | https://go.shopmy.us/p-97609985 |
| 21 | Christmas Mahjong Mat | crop needed | C | Red/green felt card-table look. | https://go.shopmy.us/p-97610188 |
| 22 | Green Plaid Christmas Tree Mahjong Mat 31.5 X 31.5 Inch | crop needed | A | Pink/red/green trees, green plaid centre. | https://go.shopmy.us/p-97610315 |
| 23 | Christmas American Mahjong Mat With Rules 31.5"x31.5" Non-Slip Table M | crop needed | C | Gingerbread border, rules/wind text, mostly blank. | https://go.shopmy.us/p-97610638 |
| 24 | Pink And Green Christmas Tree Mahjong Mat 31.5" X 31.5" | crop needed | A | Pink trees, green/pink plaid centre. | https://go.shopmy.us/p-97610762 |
| 25 | Pink Bow Christmas Tree Mahjong Mat Gifts 31.5" X 31.5" | crop needed | A | Pink bows, ornament cameos. | https://go.shopmy.us/p-97638780 |
| 26 | Winter Village Christmas Mahjong Mat For Table With Bag | photo OK | A | Pink snowy village, snowflake centre. | https://go.shopmy.us/p-97638966 |
| 27 | Pink Green Gingham Plaid Mahjong Mat For Table | crop needed | A | Pink/green gingham, teacups + holly. | https://go.shopmy.us/p-97639136 |
| 28 | Christmas Tree Plaid Mahjong Mat With Rules | crop needed | B | Red gingham centre, tree toile. | https://go.shopmy.us/p-97639286 |
| 29 | Red And Green Christmas Village Mahjong Mat 31.5x31.5in | crop needed | B | Red/white village toile. | https://go.shopmy.us/p-97639458 |
| 30 | Bearcake Red And Green Christmas Floral Mahjong Mat For Table 31.5x31. | crop needed | B | Dark floral medallion, cream. | https://go.shopmy.us/p-97639622 |
| 31 | Christmas Santa Nutcracker Mahjong Mat For Table 31.5 X 31.5 Inch | photo OK | B | Ornaments + nutcracker, green stripe centre. Busy. | https://go.shopmy.us/p-97639775 |
| 32 | Christmas Mahjong Mat With Rules Without Creases | crop needed | C | Rules mat, props. | https://go.shopmy.us/p-97639950 |
| 33 | Coquette Red And Green Christmas Mahjong Mat For Table 31.5in | crop needed | A | Coquette green gingham + red bows. | https://go.shopmy.us/p-97640123 |
| 34 | Cute Brown Beige Gingerbread Man Christmas Mahjong Mat 31.5" X 31.5" | crop needed | B | Gingerbread, peach gingham. | https://go.shopmy.us/p-97640320 |
| 35 | Red Blue Christmas Tree Santa Claus Mahjong Mat 31.5 X 31.5 Inch | crop needed | A | Red/blue Christmas toile, candy-stripe edge. | https://go.shopmy.us/p-97640537 |
| 36 | Shipped Rolled Cottagecore Christmas Mahjong Mat 31.5 X 31.5 Inch | crop needed | B | Cottagecore green, snowy centre. | https://go.shopmy.us/p-97640747 |
| 37 | Green Christmas Mahjong Mat For Table | crop needed | C | Wreath + rules text, dice prop. | https://go.shopmy.us/p-97640938 |
| 38 | Christmas Mahjong Mat With Festive Wreath | crop needed | B | Vintage wreath, busy. | https://go.shopmy.us/p-97641123 |
| 39 | Mahjong Mat For Table Festive Christmas Holly Red Berries Green Bow Sn | crop needed | A | Holly + green bow on cream. Clean. | https://go.shopmy.us/p-97641275 |
| 40 | Christmas Mahjong Mat | crop needed | B | Pine + cardinal border, cream centre. | https://go.shopmy.us/p-97641470 |
| 41 | Christmas Mahjong Mat For Table 31.5in | crop needed | B | Pine/pinecone border, plain cream centre. | https://go.shopmy.us/p-97641648 |
| 42 | Green And Red Christmas Mahjong Mat 31.5x31.5in | crop needed | B | Red/green chevron + wreath. | https://go.shopmy.us/p-97641830 |
| 43 | Drydiet American Mahjong Mat For Table With Bag | photo OK | B | Candy-stripe border + wreath. | https://go.shopmy.us/p-97642042 |
| 44 | Jolov 31.5" Christmas Mahjong Mat With Carrying Bag | crop needed | C | Red casino look + chips/dice props. | https://go.shopmy.us/p-97642223 |
| 45 | Mahjong Mat For Table Winter Berry Evergreen Foliage Snowflakes Light  | crop needed | B | Light blue winter berries/foliage (snowflakes in title). | https://go.shopmy.us/p-97642382 |
| 46 | Hspd Blue Hanukkah Menorah American Mahjong Mat 31.5x31.5 | crop needed | A | Hanukkah: folk menorah, blue/red. Holiday has very few Hanukkah mats. | https://go.shopmy.us/p-97642555 |
| 47 | Blue And White Winter Mahjong Mat 31.5x31.5in | crop needed | B | Blue snowflakes, navy centre. | https://go.shopmy.us/p-97642719 |
| 48 | Mahjong Mat 31.5"x31.5" | crop needed | C | Hanukkah: plain aqua, white Star of David. Thin pattern. | https://go.shopmy.us/p-97642845 |
| 49 | Drydiet American Mahjong Mat For Table With Bag | photo OK | B | Hanukkah: menorah, dreidels, peacocks, navy/blue. | https://go.shopmy.us/p-97643009 |

**Top Amazon holiday picks (A):** #1, #2, #3, #8, #11, #12, #15, #17, #20, #22, #24, #25, #26, #27, #33, #35, #39, #46. **Skip (C):** #5, #9, #13, #14, #16, #21, #23, #32, #37, #44, #48.

## Other ShopMy-only mats not in FYM/gallery (14)
These aren't Etsy or Amazon, but they're ShopMy-linked (allowed as ShopMy-affiliated). Rebecca Illustrated is already on the Desk ("whole mat line into gallery + FYM"). Most Rebecca photos show the mat held up or in play, so the brand's own flat renders would be better.
| # | Mat | Photo | Note | ShopMy link |
|---|---|---|---|---|
| 1 | Holiday Lights Double Sided Mahjong Mat | photo OK | Waiting On Martha Home: Holiday Lights, double-sided. | https://go.shopmy.us/p-97202826 |
| 2 | Vintage Twinkle Double Sided Mahjong Mat | photo OK | Waiting On Martha Home: Vintage Twinkle (pink/green trees), double-sided. | https://go.shopmy.us/p-97201863 |
| 3 | Apres Ski Double Sided Mahjong Mat- PRE ORDER | photo OK | Waiting On Martha Home: Apres Ski (ski scene = holiday). Pre-order. | https://go.shopmy.us/p-97201286 |
| 4 | The Mahjong House - Green Flower Border Mahjong Mat | photo OK | Waiting On Martha Home x The Mahjong House: Green Flower Border, solid mint. | https://go.shopmy.us/p-97202654 |
| 5 | Ruby Table Double-Sided Mahjong Mat | photo OK | The Mahjong House: Ruby Table, solid red double-sided. Added Oct 26. | https://go.shopmy.us/p-97678570 |
| 6 | POOL PAWTY-MAHJONG MAT | Questionable | Rebecca Illustrated Pool Pawty: hands + tiles on it, angled. Check rebeccaillustrated site for a flat render. | https://go.shopmy.us/p-96620624 |
| 7 | CANARIES-MAHJONG MAT | crop needed | Rebecca Canaries: held up by a person: crop to mat. | https://go.shopmy.us/p-96620667 |
| 8 | CHINOISERIE & CITRUS-MAHJONG MAT | crop needed | Rebecca Chinoiserie & Citrus: held up: crop. | https://go.shopmy.us/p-96620673 |
| 9 | WHITE SAILBOATS-MAHJONG MAT | Questionable | Rebecca White Sailboats: hands, tiles, angled. | https://go.shopmy.us/p-96620684 |
| 10 | MAXINE-MAHJONG MAT | photo OK | Rebecca Maxine: flat art, fills frame. | https://go.shopmy.us/p-96620690 |
| 11 | REBECCA ILLUSTRATED / Mahjong Mat  | crop needed | Rebecca (pink house, title generic): held up: crop. | https://go.shopmy.us/p-96620593 |
| 12 | REBECCA ILLUSTRATED / Mahjong Mat | crop needed | Rebecca (pink gingham palms + leopard, title generic): held up: crop. | https://go.shopmy.us/p-96620594 |
| 13 | GIRLY BAR CART-MAHJONG MAT | Questionable | Rebecca Girly Bar Cart: hands + tiles, angled. | https://go.shopmy.us/p-96620635 |
| 14 | PICKLE BALL-MAHJONG MAT | Questionable | Rebecca Pickle Ball: hands + tiles. | https://go.shopmy.us/p-96620638 |

## No regular ShopMy check exists yet
Suggested: a weekly read of the public collections API (`api.shopmy.us/api/Collections/<id>`) for new pins on the mat shelves, diffed against FYM `go.shopmy.us` links. Shelf ids: Etsy & Amazon Holiday 8507446, Etsy Mats 8392222, Amazon Mats 8398332, BJ&J 8391624, Rebecca 8431929.
