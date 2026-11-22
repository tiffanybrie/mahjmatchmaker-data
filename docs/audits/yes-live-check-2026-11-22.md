# Yes vs live check, 2026-11-22

Every yes Tiffany has given (swipe books, picks pages, late picks, review rounds) compared with the cards on the live album pages. Built by `python3 scripts/checks/yes_live_check.py`; data in `docs/status/yes-live-check.json`.

- Yes records read: **951** (869 unique tile set + mat pairs; the same yes is often recorded in two files)
- Checked against live albums: **637**
- Live: **543** (38 of them by a loose match, listed at the bottom)
- **Not live: 94**
- For albums that are not live yet (not misses): 232
- Live pages read: 56 (2212 cards)

Matching is by tile set, mat name and brand together.

## Yes records by source

| Source file | Yes records | Not live |
|---|---|---|
| `config/album-records/deco-indigo.json` | 27 | 0 |
| `config/album-records/deco-lagoon.json` | 38 | 0 |
| `config/album-records/deco-mulberry.json` | 33 | 0 |
| `config/album-records/holiday-nov18-picks.json` | 45 | 36 |
| `config/album-records/origami-timber.json` | 83 | 0 |
| `config/album-records/sadie-jane.json` | 59 | 0 |
| `config/fym-thin-picks-oct26.json` | 41 | 0 |
| `config/late-holiday-picks-nov03.json` | 33 | 0 |
| `config/picks/deco-lagoon-fym-m-2026-11-08.json` | 41 | 0 |
| `config/picks/juniper-final-order-2026-11-07.json` | 42 | 0 |
| `config/picks/juniper-fym-m-2026-11-07.json` | 42 | 0 |
| `config/picks/missed-mats-round1-2026-11-07.txt` | 146 | 3 |
| `config/picks/missed-mats-round2-partial-2026-11-07.json` | 28 | 27 |
| `config/swipe-yeses/holiday-oct21.json` | 293 | 28 |

## Yes, not live (per album)

### Nivalee (`nivalee-blue`): 16

| Mat | Brand | Holiday | Source | Note |
|---|---|---|---|---|
| Blue & White Snowflake | Amazon | yes | `config/album-records/holiday-nov18-picks.json` (holiday pick sheet keep (answered 2026-11-22, done=True)) |  |
| Gray Malin Getaway Dogs (Side B: Ski Lift) | Bespoke Mahjong | yes | `config/album-records/holiday-nov18-picks.json` (holiday pick sheet keep (answered 2026-11-22, done=True)) |  |
| Apres Skiing in Teal | Let's Be Besties | yes | `config/album-records/holiday-nov18-picks.json` (holiday pick sheet keep (answered 2026-11-22, done=True)) |  |
| Apres Skiing in Teal with Skiers | Let's Be Besties | yes | `config/album-records/holiday-nov18-picks.json` (holiday pick sheet keep (answered 2026-11-22, done=True)) |  |
| Fair Isle Pink Snowflakes | Let's Be Besties | yes | `config/album-records/holiday-nov18-picks.json` (holiday pick sheet keep (answered 2026-11-22, done=True)) |  |
| Winter Jewel | Let's Be Besties | yes | `config/album-records/holiday-nov18-picks.json` (holiday pick sheet keep (answered 2026-11-22, done=True)) |  |
| Snowflake Lodge Premium | Mahjong Register | yes | `config/album-records/holiday-nov18-picks.json` (holiday pick sheet keep (answered 2026-11-22, done=True)) |  |
| The Alpine Mat | Maison Mahj | yes | `config/album-records/holiday-nov18-picks.json` (holiday pick sheet keep (answered 2026-11-22, done=True)) |  |
| The Chalet | Maison Mahj | yes | `config/album-records/holiday-nov18-picks.json` (holiday pick sheet keep (answered 2026-11-22, done=True)) | same mat name on the page from another brand: Bespoke Mahjong "The Chalet" |
| The Winter Garland Mat | Maison Mahj | yes | `config/album-records/holiday-nov18-picks.json` (holiday pick sheet keep (answered 2026-11-22, done=True)) |  |
| Clara | Oh My Mahjong | yes | `config/album-records/holiday-nov18-picks.json` (holiday pick sheet keep (answered 2026-11-22, done=True)) |  |
| Merriment | Oh My Mahjong | yes | `config/album-records/holiday-nov18-picks.json` (holiday pick sheet keep (answered 2026-11-22, done=True)) |  |
| Sugarplum | Oh My Mahjong | yes | `config/album-records/holiday-nov18-picks.json` (holiday pick sheet keep (answered 2026-11-22, done=True)) |  |
| Frosted Flowers | Peace Love Mahjong | yes | `config/album-records/holiday-nov18-picks.json` (holiday pick sheet keep (answered 2026-11-22, done=True)) |  |
| Color Me Merry | Soirée All Day | yes | `config/album-records/holiday-nov18-picks.json` (holiday pick sheet keep (answered 2026-11-22, done=True)) |  |
| Winter Ski Resort | YOLO Mahjong | yes | `config/album-records/holiday-nov18-picks.json` (holiday pick sheet keep (answered 2026-11-22, done=True)) |  |

### Après Ski Club (`cmc-apres-ski`): 8

| Mat | Brand | Holiday | Source | Note |
|---|---|---|---|---|
| Blue & White Snowflake | Amazon | yes | `config/album-records/holiday-nov18-picks.json` (holiday pick sheet keep (answered 2026-11-22, done=True)) |  |
| Gray Malin Getaway Dogs (Side B: Ski Lift) | Bespoke Mahjong | yes | `config/album-records/holiday-nov18-picks.json` (holiday pick sheet keep (answered 2026-11-22, done=True)) |  |
| Apres Skiing in Teal | Let's Be Besties | yes | `config/album-records/holiday-nov18-picks.json` (holiday pick sheet keep (answered 2026-11-22, done=True)) |  |
| Apres Skiing in Teal with Skiers | Let's Be Besties | yes | `config/album-records/holiday-nov18-picks.json` (holiday pick sheet keep (answered 2026-11-22, done=True)) |  |
| Green Apres Skiing with Skiers | Let's Be Besties | yes | `config/album-records/holiday-nov18-picks.json` (holiday pick sheet keep (answered 2026-11-22, done=True)) |  |
| Winter Jewel | Let's Be Besties | yes | `config/album-records/holiday-nov18-picks.json` (holiday pick sheet keep (answered 2026-11-22, done=True)) |  |
| The Alpine Mat | Maison Mahj | yes | `config/album-records/holiday-nov18-picks.json` (holiday pick sheet keep (answered 2026-11-22, done=True)) |  |
| Winter Ski Resort | YOLO Mahjong | yes | `config/album-records/holiday-nov18-picks.json` (holiday pick sheet keep (answered 2026-11-22, done=True)) |  |

### Dear Santa (`dear-santa`): 8

| Mat | Brand | Holiday | Source | Note |
|---|---|---|---|---|
| The Evergreen Mat | Maison Mahj | yes | `config/album-records/holiday-nov18-picks.json` (holiday pick sheet keep (answered 2026-11-22, done=True)) |  |
| Merry Mahjong | Oh My Mahjong |  | `config/swipe-yeses/holiday-oct21.json` (swipe book "omm" yes [merry-mahjong, hol-dear-santa]) |  |
| Peace Love & Mistletoe | Peace Love Mahjong | yes | `config/album-records/holiday-nov18-picks.json` (holiday pick sheet keep (answered 2026-11-22, done=True)) |  |
| Spirit of Christmas | Peace Love Mahjong | yes | `config/album-records/holiday-nov18-picks.json` (holiday pick sheet keep (answered 2026-11-22, done=True)) |  |
| Color Me Merry | Soirée All Day | yes | `config/album-records/holiday-nov18-picks.json` (holiday pick sheet keep (answered 2026-11-22, done=True)) |  |
| Holiday Chintz | Soirée All Day | yes | `config/album-records/holiday-nov18-picks.json` (holiday pick sheet keep (answered 2026-11-22, done=True)) |  |
| Home for the Holidays | Soirée All Day | yes | `config/album-records/holiday-nov18-picks.json` (holiday pick sheet keep (answered 2026-11-22, done=True)) |  |
| Evergreen Christmas Plaid | YOLO Mahjong | yes | `config/album-records/holiday-nov18-picks.json` (holiday pick sheet keep (answered 2026-11-22, done=True)) |  |

### Heritage (`heritage`): 6

| Mat | Brand | Holiday | Source | Note |
|---|---|---|---|---|
| L'Été Indien Studio Print No. 1 | Fait à Main |  | `config/picks/missed-mats-round2-partial-2026-11-07.json` (round 2 heart 7b91814b99|heritage) |  |
| Tabitha | House of Hearts Studio |  | `config/picks/missed-mats-round2-partial-2026-11-07.json` (round 2 heart 79a09985ae|heritage) |  |
| Merry Mahjong | Oh My Mahjong |  | `config/swipe-yeses/holiday-oct21.json` (swipe book "omm" yes [merry-mahjong, heritage]) |  |
| Miracle | Oh My Mahjong |  | `config/swipe-yeses/holiday-oct21.json` (swipe book "omm" yes [miracle, heritage]) |  |
| Twilight Waltz | Oh My Mahjong |  | `config/swipe-yeses/holiday-oct21.json` (swipe book "omm" yes [twilight-waltz, heritage]) |  |
| Vegan Leather (Chestnut) | Sunday Mahjong |  | `config/picks/missed-mats-round1-2026-11-07.txt` (Heritage) |  |

### Sunday Tile Set (`sunday-tile-set`): 6

| Mat | Brand | Holiday | Source | Note |
|---|---|---|---|---|
| Blossom Pavilion Waterscape | Luna EK Studio |  | `config/picks/missed-mats-round2-partial-2026-11-07.json` (round 2 heart 6f4f6d21cc|sunday-tile-set) |  |
| Fern Berry Wreath | Luna EK Studio |  | `config/picks/missed-mats-round2-partial-2026-11-07.json` (round 2 heart 4a4ddcbcea|sunday-tile-set) |  |
| Forest Bird Bloom | Luna EK Studio |  | `config/picks/missed-mats-round2-partial-2026-11-07.json` (round 2 heart f427d69494|sunday-tile-set) |  |
| Herbal Drawing Butterfly Border | Luna EK Studio |  | `config/picks/missed-mats-round2-partial-2026-11-07.json` (round 2 heart 3e21c737b1|sunday-tile-set) |  |
| Terracotta Floral Tapestry | Luna EK Studio |  | `config/picks/missed-mats-round2-partial-2026-11-07.json` (round 2 heart 856b1960df|sunday-tile-set) |  |
| Miracle | Oh My Mahjong |  | `config/swipe-yeses/holiday-oct21.json` (swipe book "omm" yes [miracle, sunday]) |  |

### Heritage 2.0 (`heritage-2-0`): 5

| Mat | Brand | Holiday | Source | Note |
|---|---|---|---|---|
| Blossom Pavilion Waterscape | Luna EK Studio |  | `config/picks/missed-mats-round2-partial-2026-11-07.json` (round 2 heart 6f4f6d21cc|heritage-2-0) |  |
| Fern Berry Wreath | Luna EK Studio |  | `config/picks/missed-mats-round2-partial-2026-11-07.json` (round 2 heart 4a4ddcbcea|heritage-2-0) |  |
| Herbal Drawing Butterfly Border | Luna EK Studio |  | `config/picks/missed-mats-round2-partial-2026-11-07.json` (round 2 heart 3e21c737b1|heritage-2-0) |  |
| Terracotta Floral Tapestry | Luna EK Studio |  | `config/picks/missed-mats-round2-partial-2026-11-07.json` (round 2 heart 856b1960df|heritage-2-0) |  |
| Bird & Pear Blossom | Mahj & Moon |  | `config/picks/missed-mats-round2-partial-2026-11-07.json` (round 2 heart 7f51f5938f|heritage-2-0) |  |

### Holly Jolly (`holly-jolly-green`): 5

| Mat | Brand | Holiday | Source | Note |
|---|---|---|---|---|
| Very Merry Mahj | Anders Ruff | yes | `config/album-records/holiday-nov18-picks.json` (holiday pick sheet keep (answered 2026-11-22, done=True)) |  |
| Merry & Bright, Holiday Prism | Let's Be Besties | yes | `config/album-records/holiday-nov18-picks.json` (holiday pick sheet keep (answered 2026-11-22, done=True)) |  |
| Holly Jolly Christmas | Mahjong Register | yes | `config/album-records/holiday-nov18-picks.json` (holiday pick sheet keep (answered 2026-11-22, done=True)) | same mat name on the page from another brand: Bam! Let's Mahjong "Holly Jolly Christmas" |
| Merry & Striped | Peace Love Mahjong | yes | `config/album-records/holiday-nov18-picks.json` (holiday pick sheet keep (answered 2026-11-22, done=True)) |  |
| Color Me Merry | Soirée All Day | yes | `config/album-records/holiday-nov18-picks.json` (holiday pick sheet keep (answered 2026-11-22, done=True)) |  |

### Hummingbird (`hummingbird`): 4

| Mat | Brand | Holiday | Source | Note |
|---|---|---|---|---|
| Twilight Waltz | Oh My Mahjong |  | `config/swipe-yeses/holiday-oct21.json` (swipe book "omm" yes [twilight-waltz, hummingbird]) |  |
| Merry Mix | Peace Love Mahjong |  | `config/swipe-yeses/holiday-oct21.json` (swipe book "plmmats" yes [plm-merry-mix, hummingbird]) |  |
| Nutcracker Noel - Red & Green | Peace Love Mahjong |  | `config/swipe-yeses/holiday-oct21.json` (swipe book "plmmats" yes [plm-nutcracker-noel-red-green, hummingbird]) |  |
| Vintage Noel | Peace Love Mahjong |  | `config/swipe-yeses/holiday-oct21.json` (swipe book "plmmats" yes [plm-vintage-noel, hummingbird]) |  |

### Willow (`willow`): 4

| Mat | Brand | Holiday | Source | Note |
|---|---|---|---|---|
| Blossom Pavilion Waterscape | Luna EK Studio |  | `config/picks/missed-mats-round2-partial-2026-11-07.json` (round 2 heart 6f4f6d21cc|willow) |  |
| Fern Berry Wreath | Luna EK Studio |  | `config/picks/missed-mats-round2-partial-2026-11-07.json` (round 2 heart 4a4ddcbcea|willow) |  |
| Forest Bird Bloom | Luna EK Studio |  | `config/picks/missed-mats-round2-partial-2026-11-07.json` (round 2 heart f427d69494|willow) |  |
| Herbal Drawing Butterfly Border | Luna EK Studio |  | `config/picks/missed-mats-round2-partial-2026-11-07.json` (round 2 heart 3e21c737b1|willow) |  |

### Brownstone Bloom (`brownstone-bloom`): 3

| Mat | Brand | Holiday | Source | Note |
|---|---|---|---|---|
| Fern Berry Wreath | Luna EK Studio |  | `config/picks/missed-mats-round2-partial-2026-11-07.json` (round 2 heart 4a4ddcbcea|brownstone-bloom) |  |
| Forest Bird Bloom | Luna EK Studio |  | `config/picks/missed-mats-round2-partial-2026-11-07.json` (round 2 heart f427d69494|brownstone-bloom) |  |
| Herbal Drawing Butterfly Border | Luna EK Studio |  | `config/picks/missed-mats-round2-partial-2026-11-07.json` (round 2 heart 3e21c737b1|brownstone-bloom) |  |

### Lola (`lola`): 2

| Mat | Brand | Holiday | Source | Note |
|---|---|---|---|---|
| Deep Blue Floral with Instructions | Let's Be Besties |  | `config/picks/missed-mats-round2-partial-2026-11-07.json` (round 2 heart 0755c26fab|lola) |  |
| Merry Mahjong | Oh My Mahjong |  | `config/swipe-yeses/holiday-oct21.json` (swipe book "omm" yes [merry-mahjong, lola]) |  |

### Papaya Spritz (`papaya-spritz`): 2

| Mat | Brand | Holiday | Source | Note |
|---|---|---|---|---|
| Spirit of Christmas | Peace Love Mahjong |  | `config/swipe-yeses/holiday-oct21.json` (swipe book "plmmats" yes [plm-spirit-of-christmas, papaya-spritz]) |  |
| Cheeky Cockatoo | Sophie Clima |  | `config/picks/missed-mats-round2-partial-2026-11-07.json` (round 2 heart 1f7d6a0e86|papaya-spritz) |  |

### Pearlescent (`pearlescent`): 2

| Mat | Brand | Holiday | Source | Note |
|---|---|---|---|---|
| Merry Mahjong | Oh My Mahjong |  | `config/swipe-yeses/holiday-oct21.json` (swipe book "omm" yes [merry-mahjong, pearlescent]) |  |
| Cheeky Cockatoo | Sophie Clima |  | `config/picks/missed-mats-round2-partial-2026-11-07.json` (round 2 heart 1f7d6a0e86|pearlescent) |  |

### Sunday Blues (`sunday-blues`): 2

| Mat | Brand | Holiday | Source | Note |
|---|---|---|---|---|
| Miracle | Oh My Mahjong |  | `config/swipe-yeses/holiday-oct21.json` (swipe book "omm" yes [miracle, sunday-blues]) |  |
| Twilight Waltz | Oh My Mahjong |  | `config/swipe-yeses/holiday-oct21.json` (swipe book "omm" yes [twilight-waltz, sunday-blues]) |  |

### December 1994 (`december-1994`): 1

| Mat | Brand | Holiday | Source | Note |
|---|---|---|---|---|
| Merry Mahjong | Oh My Mahjong |  | `config/swipe-yeses/holiday-oct21.json` (swipe book "omm" yes [merry-mahjong, hol-december-1994]) |  |

### Emerald (`emerald`): 1

| Mat | Brand | Holiday | Source | Note |
|---|---|---|---|---|
| Green Malachite | Mahj Squad |  | `config/picks/missed-mats-round1-2026-11-07.txt` (Emerald) |  |

### Glitterville (`glitterville`): 1

| Mat | Brand | Holiday | Source | Note |
|---|---|---|---|---|
| Pink Blooms | Let's Be Besties |  | `config/picks/missed-mats-round2-partial-2026-11-07.json` (round 2 heart 22bc81a9b7|glitterville) |  |

### Holly Jolly (`holly-jolly-pink`): 1

| Mat | Brand | Holiday | Source | Note |
|---|---|---|---|---|
| Merry Mahjong | Oh My Mahjong |  | `config/swipe-yeses/holiday-oct21.json` (swipe book "omm" yes [merry-mahjong, hol-holly-jolly-pink]) |  |

### Holly Jolly (`holly-jolly-red`): 1

| Mat | Brand | Holiday | Source | Note |
|---|---|---|---|---|
| Merry Mahjong | Oh My Mahjong |  | `config/swipe-yeses/holiday-oct21.json` (swipe book "omm" yes [merry-mahjong, hol-holly-jolly-red]) |  |

### Jasmine (`jasmine`): 1

| Mat | Brand | Holiday | Source | Note |
|---|---|---|---|---|
| Twilight Waltz | Oh My Mahjong |  | `config/swipe-yeses/holiday-oct21.json` (swipe book "omm" yes [twilight-waltz, jasmine]) |  |

### La Fete (`la-fete`): 1

| Mat | Brand | Holiday | Source | Note |
|---|---|---|---|---|
| Cheeky Cockatoo | Sophie Clima |  | `config/picks/missed-mats-round2-partial-2026-11-07.json` (round 2 heart 1f7d6a0e86|la-fete) |  |

### Limoncello (`limoncello`): 1

| Mat | Brand | Holiday | Source | Note |
|---|---|---|---|---|
| Merry Mahjong | Oh My Mahjong |  | `config/swipe-yeses/holiday-oct21.json` (swipe book "omm" yes [merry-mahjong, limoncello]) |  |

### Malachite (`malachite`): 1

| Mat | Brand | Holiday | Source | Note |
|---|---|---|---|---|
| Forest Bird Bloom | Luna EK Studio |  | `config/picks/missed-mats-round2-partial-2026-11-07.json` (round 2 heart f427d69494|malachite) |  |

### Nantucket (`nantucket`): 1

| Mat | Brand | Holiday | Source | Note |
|---|---|---|---|---|
| Candy Cane Lane | Peace Love Mahjong |  | `config/swipe-yeses/holiday-oct21.json` (swipe book "plmmats" yes [plm-candy-cane-lane, nantucket]) | same mat name on the page from another brand: Anders Ruff "Candy Cane Lane" |

### Nutcracker Ballet (`nutcracker-ballet`): 1

| Mat | Brand | Holiday | Source | Note |
|---|---|---|---|---|
| Merry Mahjong | Oh My Mahjong |  | `config/swipe-yeses/holiday-oct21.json` (swipe book "omm" yes [merry-mahjong, hol-nutcracker-ballet]) |  |

### Osler (`osler`): 1

| Mat | Brand | Holiday | Source | Note |
|---|---|---|---|---|
| Miracle | Oh My Mahjong |  | `config/swipe-yeses/holiday-oct21.json` (swipe book "omm" yes [miracle, osler]) |  |

### Palm Royale (`palm-royale`): 1

| Mat | Brand | Holiday | Source | Note |
|---|---|---|---|---|
| Merry Mahjong | Oh My Mahjong |  | `config/swipe-yeses/holiday-oct21.json` (swipe book "omm" yes [merry-mahjong, palm-royale]) |  |

### Rackin' Rudolph (`rackin-rudolph`): 1

| Mat | Brand | Holiday | Source | Note |
|---|---|---|---|---|
| Merry Mahjong | Oh My Mahjong |  | `config/swipe-yeses/holiday-oct21.json` (swipe book "omm" yes [merry-mahjong, hol-rackin-rudolph]) |  |

### Shangri La (`shangri-la`): 1

| Mat | Brand | Holiday | Source | Note |
|---|---|---|---|---|
| Festive Frost | Let's Be Besties | yes | `config/picks/missed-mats-round2-partial-2026-11-07.json` (round 2 heart fa53d06550|shangri-la) |  |

### Smith (`smith`): 1

| Mat | Brand | Holiday | Source | Note |
|---|---|---|---|---|
| Vegan Leather (Chestnut) | Sunday Mahjong |  | `config/picks/missed-mats-round1-2026-11-07.txt` (Smith) |  |

### Solara (`solara`): 1

| Mat | Brand | Holiday | Source | Note |
|---|---|---|---|---|
| Pink Blooms | Let's Be Besties |  | `config/picks/missed-mats-round2-partial-2026-11-07.json` (round 2 heart 22bc81a9b7|solara) |  |

### Sorbet (`sorbet`): 1

| Mat | Brand | Holiday | Source | Note |
|---|---|---|---|---|
| Miracle | Oh My Mahjong |  | `config/swipe-yeses/holiday-oct21.json` (swipe book "omm" yes [miracle, sorbet]) |  |

### Spring Love (`spring-love`): 1

| Mat | Brand | Holiday | Source | Note |
|---|---|---|---|---|
| Pretty Little Christmas | Peace Love Mahjong |  | `config/swipe-yeses/holiday-oct21.json` (swipe book "plmmats" yes [plm-pretty-little-christmas, vault-spring-love]) |  |

### Talulah (`talulah`): 1

| Mat | Brand | Holiday | Source | Note |
|---|---|---|---|---|
| Miracle | Oh My Mahjong |  | `config/swipe-yeses/holiday-oct21.json` (swipe book "omm" yes [miracle, talulah]) |  |

### Tinselle (`tinselle-ruby`): 1

| Mat | Brand | Holiday | Source | Note |
|---|---|---|---|---|
| Merry Mahjong | Oh My Mahjong |  | `config/swipe-yeses/holiday-oct21.json` (swipe book "tinselle" yes [tinselle-ruby, omm-merry-mahjong]) |  |

## Not live yet (staged hidden or queued, not misses)

### Origami Timber (Bam Bird Boutique) (`origami-timber`): 83 yeses

Status: album record exists, no go-live slot yet (config/album-records). Sources: `config/album-records/origami-timber.json`

Bam Bird Boutique Vegan Leather Navy, Lets Be Besties Teal Dots And Stripes With Instructions, Mahjong Register Emerald Teal And Celadon Green Double Sided Leatherette Mahjong Mat 33, Sunday Mahjong Vegan Leather Chestnut, Evergreen & Tartan (Anders Ruff), Tartan Tidings (Anders Ruff), Bandana – Holiday Green/Pink accents (Bam Bird Boutique), Blue Abstract Neoprene (Bam Bird Boutique), Holiday Neoprene (Bam Bird Boutique), Plaid Neoprene – Green and Blue (Bam Bird Boutique), Plaid Neoprene – Green with Pink (Bam Bird Boutique), Vegan Leather – Caramel (Bam Bird Boutique), Jungle Turquoise (Bespoke Mahjong), Emerald Society (Bougie Mahjong), Imperial Koi Pond (Bougie Mahjong), Dabney Leatherette (Britt Mills), Eden Leatherette (Britt Mills), Enchanted Leatherette (Britt Mills), Huntley Leatherette (Britt Mills), Merrywood (Britt Mills), Novella Leatherette (Britt Mills), Peacock Garden Leatherette (Britt Mills), Ruby (Britt Mills), SOIRÉE Leatherette (Britt Mills), Savannah Leatherette (Britt Mills), Winter Berry Leatherette (Britt Mills), Wren (Britt Mills), Brown Vegan Leather (Charleston Mahjong Club), The Hunt Club (Charleston Mahjong Club), L'Été Indien Studio Print No. 1 (Fait à Main), Rackin' Rudolph ! (Hip Hip Mahjong), Floral Scrolls (Let's Be Besties), Tartan Tweed (Let's Be Besties), Winter Jewel (Let's Be Besties), Cloud Crane Floral Frame (Luna EK Studio), Crane Lantern Pattern (Luna EK Studio), Lotus Breeze Koi (Luna EK Studio), Lotus Garden Koi (Luna EK Studio), Terracotta Floral Tapestry (Luna EK Studio), Umbrella Koi Pond (Luna EK Studio), The Polo Club (Luxe Mahjong), Caroline in Peacock (Mahj & Vine), Duck Camp (Mahjong Moxie), Heron Landing (Mahjong Moxie), Emerald Teal & Celedon Green Double-Sided Leatherette (Mahjong Register), Autumn Saffron (Mahjong Row & Co.), Ellington Navy (Mahjong Row & Co.), Foxhill Plaid (Mahjong Row & Co.), Marigold (Mahjong Row & Co.), Marlowe Green (Mahjong Row & Co.), Midnight Garden (Mahjong Row & Co.), Ralph (Mahjong by SI), Cherry Blossom Malachite (Miss Mahjong), Astor (Oh My Mahjong), Dapper 1 (retired) (Oh My Mahjong), Dapper 2 (retired) (Oh My Mahjong), Hawthorne (Oh My Mahjong), Isla (Oh My Mahjong), Jade (Oh My Mahjong), KY Derby (retired) (Oh My Mahjong), Palomino (Oh My Mahjong), SoHo (retired) (Oh My Mahjong), Veranda (Oh My Mahjong), Winterberry (Oh My Mahjong), Yuletide (Oh My Mahjong), Baker Traditional (Ozark Mahjongg), Carson Vintage (Ozark Mahjongg), Trent Celadon (Ozark Mahjongg), Trent Midnight (Ozark Mahjongg), Winslow 1920 Navy (Ozark Mahjongg), Winslow 1920 Noir (Ozark Mahjongg), Winslow 1920 Rouge (Ozark Mahjongg), Dark Teal Cocktail Hour (Peace Love Mahjong), Vegan Leather – Cognac (Peace Love Mahjong), Festive Plaid Premium (Sunday Mahjong), Golden Gingham Premium (Sunday Mahjong), Rattan (Sunday Mahjong), Retro Plaid Premium (Sunday Mahjong), Boho Wildflower (Sweet Jojo Designs), Nantucket Basket, Rope (Tigre de Tartan), Nantucket Basket, Round (Tigre de Tartan), Cottage Core (Wren Mats), Crane & Moon (YOLO Mahjong)

### Sadie Jane (Oh My Mahjong) (`sadie-jane`): 58 yeses

Status: album record exists, no go-live slot yet (config/album-records). Sources: `config/album-records/sadie-jane.json`

Blue Willow (Amanda Toppe), Blue & White Snowflake (Amazon), Blue and Pink Floral (Amazon), Pink & Blue Christmas Village (Amazon), Pink Blue Bow Floral (Amazon), Botanical Garden (Anders Ruff), Hamptons Hydrangea (Anders Ruff), The Pink Classic Neoprene (Bam Bird Boutique), Grandmillennial (Bam! Let's Mahjong), Gigi (Canvas Art) (Betty June & Jeannette), Grace Watercolor (Betty June & Jeannette), Julia (Blush) (Betty June & Jeannette), Livy (Betty June & Jeannette), Nichole (Betty June & Jeannette), The Kerry (Betty June & Jeannette), Nutcracker (Britt Mills), Ski Club Mat - Periwinkle Center (Charleston Mahjong Club), Blue and Pink Chinoiserie Trellis (CraftinMy), Plum Lotus (Let's Be Besties), Rose Water Dots and Stripes (Let's Be Besties), Talulah Panda (Let's Be Besties), Watercolor Lilies (Let's Be Besties), Let's Be Refined! – Refined Blue/Soft Blue Border (Let's Mahj On), Chinoiserie Citrus Grove (Mahj & Vine), Pink Lemonade (Mahj Mood), Pink Hydrangea Preppy Floral (MahjAuraStudio), Butterfly Belle Premium (Mahjong Register), Peppermint Patty Premium (Mahjong Register), Sunday Sherbert Double-Sided Mahjong Mat – Leatherette 31.5" (Mahjong Register), Peony Keepsake (Mahjong by SI), Peony Reverie (Mahjong by SI), The Afternoon Tea (Maison Mahj), Anastasia (Oh My Mahjong), Birdie Pink (retired) (Oh My Mahjong), Camellia (Oh My Mahjong), Chantilly (Oh My Mahjong), Citrus Songbird (Oh My Mahjong), Elysium (Oh My Mahjong), Garden Party (Oh My Mahjong), Heron (Oh My Mahjong), Imperial (Oh My Mahjong), Jade (Oh My Mahjong), La Fete (Oh My Mahjong), Lotus Cove (Oh My Mahjong), Merriment (Oh My Mahjong), Peri-twinkle (retired) (Oh My Mahjong), Serendipity (Oh My Mahjong), Vivara (Oh My Mahjong), Year of the Horse (Oh My Mahjong), Love & Light (Peace Love Mahjong), Vegan Leather – Dusty Rose (Peace Love Mahjong), Christmas Tree Trellis (Piper Chase Studios), Hydrangea (Royal Mahjong Society), Chinoiserie Denim (Tigre de Tartan), Parrotia (Virora Mahjong), Petalwing (Virora Mahjong), Vintage Twinkle Double Sided (Waiting On Martha), Christmas Cat (YOLO Mahjong)

### Deco (Mulberry) (Bam Bird Boutique) (`deco-mulberry`): 33 yeses

Status: album queue, week of 2026-12-14 (proposed). Sources: `config/album-records/deco-mulberry.json`

Burgundy Grove (Anders Ruff), Purple & Aqua Marble (Anders Ruff), Deco Dragon (Lagoon) (Bam Bird Boutique), Deco Neoprene (Bam Bird Boutique), YOTD Raspberry (Bespoke Mahjong), Gilded Peacock (Bougie Mahjong), Flourish Neoprene (Britt Mills), Regal Bloom Neoprene (Britt Mills), Viola (Britt Mills), Wren (Britt Mills), Ocean Florals (Let's Be Besties), Peacock Flair (Let's Be Besties), The Mariner (Let's Be Besties), Winter Jewel (Let's Be Besties), Caroline in Peacock (Mahj & Vine), Emerald Cove Mat (Mahj Mood), Fall Fling Mat (Mahj Mood), Mahj In Bloom Mat (Mahj Mood), Peony Sociale Premium (Mahjong Register), Pretty in Plum Premium (Mahjong Register), Garden Party – Mulberry (My Fair Mahjong), Hawthorne (Oh My Mahjong), Jade (Oh My Mahjong), Yuletide (Oh My Mahjong), Dark Teal Cocktail Hour (Peace Love Mahjong), Tiger Fans (Piper Chase Studios), Crown Jewels (Royal Mahjong Society), Poinsettia Party (Soirée All Day), Spring Blooms Premium (Sunday Mahjong), Evergreen (That Mahjong Moment), Mulberry and Sage (Wren Mats), Year of the Snake (Wren Mats), Plum Scallop (YOLO Mahjong)

### Deco (Indigo) (Bam Bird Boutique) (`deco-indigo`): 27 yeses

Status: album queue, week of 2026-12-28 (proposed). Sources: `config/album-records/deco-indigo.json`

Deco Dragon (Lagoon) (Bam Bird Boutique), Deco Dragon (Mulberry) (Bam Bird Boutique), Darjeeling Peacock (Navy Floral) (Bespoke Mahjong), Sapphire Blue Garden Mat (Bespoke Mahjong), Gilded Peacock (Bougie Mahjong), Calista Leatherette (Britt Mills), Peacock Garden (Britt Mills), Scarlett (Britt Mills), Tilly Neoprene (Britt Mills), Butterscotch Floral Simple Middle (Let's Be Besties), Gatsby Glow (Let's Be Besties), Winter Jewel (Let's Be Besties), Caroline in Navy (Mahj & Vine), Caroline in Peacock (Mahj & Vine), The Speakeasy (Mahj Squad), Pretty in Plum Premium (Mahjong Register), Snowflake Reindeer Lodge Double-Sided Leatherette (Mahjong Register), Garden Party – Mulberry (My Fair Mahjong), Astor (Oh My Mahjong), Elysium (Oh My Mahjong), Hawthorne (Oh My Mahjong), SoHo (Oh My Mahjong), Vanderbilt (Oh My Mahjong), Yuletide (Oh My Mahjong), Love & Light (Peace Love Mahjong), Crown Jewels (Royal Mahjong Society), Midnight Garden Club (Soirée All Day)

### Spirit of Christmas (Peace Love Mahjong) (`spirit-of-christmas`): 17 yeses

Status: no live album page or holiday section for this tile set. Sources: `config/album-records/holiday-nov18-picks.json`, `config/swipe-yeses/holiday-oct21.json`

Classic Very Merry Mahj (Anders Ruff), Watercolor Christmas Tree (Anders Ruff), Holiday Neoprene (Bam Bird Boutique), Merry Mahjong (Oh My Mahjong), Candy Cane Lane (Peace Love Mahjong), Merry & Striped (Peace Love Mahjong), Merry Mix (Peace Love Mahjong), Nutcracker Noel - Gold (Peace Love Mahjong), Nutcracker Noel - Red & Green (Peace Love Mahjong), Peace Love & Mistletoe (Peace Love Mahjong), Perfectly Wrapped (Peace Love Mahjong), Poinsettia & Peace (Peace Love Mahjong), Pretty Little Christmas (Peace Love Mahjong), Spirit of Christmas (Peace Love Mahjong), Tied With A Bow (Peace Love Mahjong), Vintage Noel (Peace Love Mahjong), Evergreen Christmas Plaid (YOLO Mahjong)

### Nutcracker (Peace Love Mahjong) (`plm-nutcracker`): 11 yeses

Status: no live album page or holiday section for this tile set. Sources: `config/swipe-yeses/holiday-oct21.json`

Merry Mahjong (Oh My Mahjong), Candy Cane Lane (Peace Love Mahjong), Merry & Striped (Peace Love Mahjong), Merry Mix (Peace Love Mahjong), Nutcracker Noel - Gold (Peace Love Mahjong), Peace Love & Mistletoe (Peace Love Mahjong), Perfectly Wrapped (Peace Love Mahjong), Pretty Little Christmas (Peace Love Mahjong), Spirit of Christmas (Peace Love Mahjong), Sugarplum Plaid (Peace Love Mahjong), Tied With A Bow (Peace Love Mahjong)

### Cypress Forest (`cypress-forest`): 2 yeses

Status: no live album page or holiday section for this tile set. Sources: `config/swipe-yeses/holiday-oct21.json`

Twilight Waltz (Oh My Mahjong), Nutcracker Noel - Red & Green (Peace Love Mahjong)

### Plum Panda (Sunday Mahjong) (`plum-panda`): 1 yeses

Status: album queue, week of 2027-02-22 (proposed). Sources: `config/swipe-yeses/holiday-oct21.json`

Miracle (Oh My Mahjong)

## Matched loosely (counted live, worth a look)

| Album | Yes | Live card | Why it counted | Source |
|---|---|---|---|---|
| Après Ski Club (`cmc-apres-ski`) | Snowflake Reindeer Lodge Double-Sided Leatherette (Mahjong Register) | Snowflake Lodge (Mahjong Register) on /holiday-mahjong-matches | same brand, close name; live card is "Snowflake Lodge" | `config/album-records/holiday-nov18-picks.json` |
| Gemma (`gemma`) | Allie (Purple) (Betty June & Jeannette) | Allie (Betty June & Jeannette) on /gemma-mahjong-tile-matches | same brand, the live card has the short name (colour / side / variant not on the card); live card is "Allie" | `config/fym-thin-picks-oct26.json` |
| Holly Jolly (`holly-jolly-green`) | Bespoke x Corey Paige - Holiday Love Mat - Red/Green (Side B: Heart Frame) (Bespoke Mahjong) | Holiday Love Red & Green (Bespoke Mahjong) on /holiday-mahjong-matches | same brand, close name; live card is "Holiday Love Red & Green" | `config/album-records/holiday-nov18-picks.json` |
| Jasmine (`jasmine`) | Chinoiserie Citrus Grove (Mahj & Vine) | Citrus Grove (Mahj & Vine) on /jasmine-mahjong-tile-matches | same shop link (citrus-grove); live card is "Citrus Grove" by Mahj & Vine | `config/fym-thin-picks-oct26.json` |
| Jasmine (`jasmine`) | Cheetah in Chinoiserie (Sophie Clima) | Chinoiserie Cheetah (Sophie Clima) on /jasmine-mahjong-tile-matches | same brand, close name; live card is "Chinoiserie Cheetah" | `config/fym-thin-picks-oct26.json` |
| Jasmine (`jasmine`) | Whimsical Chinoiserie Meeting in the Pavilion (Sophie Clima) | Whimsical Chinoiserie (Sophie Clima) on /jasmine-mahjong-tile-matches | same brand, close name; live card is "Whimsical Chinoiserie" | `config/fym-thin-picks-oct26.json` |
| Limoncello (`limoncello`) | Chinoiserie Elephant with Pagodas (Sophie Clima) | Chinoiserie Elephant (Sophie Clima) on /limoncello-mahjong-tile-matches | same brand, close name; live card is "Chinoiserie Elephant" | `config/fym-thin-picks-oct26.json` |
| Limoncello (`limoncello`) | Cabana - Pink & Ivory with Citrus Fringe (Tala Mahj) | Pink Cabana (Tala Mahj) on /limoncello-mahjong-tile-matches | same brand, close name; live card is "Pink Cabana" | `config/fym-thin-picks-oct26.json` |
| Limoncello (`limoncello`) | Cabana - Seafoam Blue & Ivory with Citrus Fringe (Tala Mahj) | Seafoam Cabana (Tala Mahj) on /limoncello-mahjong-tile-matches | same brand, close name; live card is "Seafoam Cabana" | `config/fym-thin-picks-oct26.json` |
| Luminaire (`luminaire`) | Nutcracker Leatherette (Britt Mills) | Nutcracker (Britt Mills) on /luminaire-mahjong-tile-matches | same brand, close name; live card is "Nutcracker" | `config/picks/missed-mats-round1-2026-11-07.txt` |
| Malachite (`malachite`) | Merrywood Leatherette (Britt Mills) | Merrywood (Britt Mills) on /malachite-mahjong-tile-matches | same brand, close name; live card is "Merrywood" | `config/picks/missed-mats-round1-2026-11-07.txt` |
| Nivalee (`nivalee-blue`) | The Chalet Mat (Side B: Ski Lift) (Bespoke Mahjong) | The Chalet (Bespoke Mahjong) on /holiday-mahjong-matches | same brand, the live card has the short name (colour / side / variant not on the card); live card is "The Chalet" | `config/album-records/holiday-nov18-picks.json` |
| Osler (`osler`) | Winslow 1920 Navy (Ozark Mahjongg) | Winslow Navy (Ozark Mahjongg) on /osler-mahjong-tile-matches | same shop link (winslow-1920-original-navy-blue-mat); live card is "Winslow Navy" by Ozark Mahjongg | `config/fym-thin-picks-oct26.json` |
| Osler (`osler`) | Winslow 1920 Rouge (Ozark Mahjongg) | Winslow Rouge (Ozark Mahjongg) on /osler-mahjong-tile-matches | same shop link (winslow-1920-rouge-mat); live card is "Winslow Rouge" by Ozark Mahjongg | `config/fym-thin-picks-oct26.json` |
| Osler (`osler`) | The Pavilion - Bamboo Neutral with Blue Fringe (Tala Mahj) | Pavilion (Tala Mahj) on /osler-mahjong-tile-matches | same brand, the live card has the short name (colour / side / variant not on the card); live card is "Pavilion" | `config/fym-thin-picks-oct26.json` |
| Pippa (`pippa`) | Caroline (Preppy) (Betty June & Jeannette) | Caroline (Betty June & Jeannette) on /pippa-mahjong-tile-matches | same brand, the live card has the short name (colour / side / variant not on the card); live card is "Caroline" | `config/fym-thin-picks-oct26.json` |
| Pippa (`pippa`) | Chinoiserie Citrus Grove (Mahj & Vine) | Citrus Grove (Mahj & Vine) on /pippa-mahjong-tile-matches | same shop link (citrus-grove); live card is "Citrus Grove" by Mahj & Vine | `config/fym-thin-picks-oct26.json` |
| Pippa (`pippa`) | Cabana - Pink & Ivory with Citrus Fringe (Tala Mahj) | Pink Cabana (Tala Mahj) on /pippa-mahjong-tile-matches | same brand, close name; live card is "Pink Cabana" | `config/fym-thin-picks-oct26.json` |
| Pippa (`pippa`) | Colony - Chartreuse & Petal Pink (Tala Mahj) | Colony (Tala Mahj) on /pippa-mahjong-tile-matches | same brand, the live card has the short name (colour / side / variant not on the card); live card is "Colony" | `config/fym-thin-picks-oct26.json` |
| Sierra (`sierra`) | Blue Rattan Premium (Sunday Mahjong) | Blue Rattan (Sunday Mahjong) on /sierra-mahjong-tile-matches | same brand, close name; live card is "Blue Rattan" | `config/picks/missed-mats-round1-2026-11-07.txt` |
| Solara (`solara`) | Betty (Floral Monogram Game Surface) (Betty June & Jeannette) | Betty Floral (Betty June & Jeannette) on /solara-mahjong-tile-matches | same brand, close name; live card is "Betty Floral" | `config/picks/missed-mats-round1-2026-11-07.txt` |
| Sorbet (`sorbet`) | Caroline (Preppy) (Betty June & Jeannette) | Caroline (Betty June & Jeannette) on /sorbet-mahjong-tile-matches | same brand, the live card has the short name (colour / side / variant not on the card); live card is "Caroline" | `config/fym-thin-picks-oct26.json` |
| Sorbet (`sorbet`) | Katelyn (Yellow) (Betty June & Jeannette) | Katelyn (Betty June & Jeannette) on /sorbet-mahjong-tile-matches | same brand, the live card has the short name (colour / side / variant not on the card); live card is "Katelyn" | `config/fym-thin-picks-oct26.json` |
| Sorbet (`sorbet`) | Chinoiserie Citrus Grove (Mahj & Vine) | Citrus Grove (Mahj & Vine) on /sorbet-mahjong-tile-matches | same shop link (citrus-grove); live card is "Citrus Grove" by Mahj & Vine | `config/fym-thin-picks-oct26.json` |
| Sorbet (`sorbet`) | Cabana - Pink & Ivory with Citrus Fringe (Tala Mahj) | Pink Cabana (Tala Mahj) on /sorbet-mahjong-tile-matches | same brand, close name; live card is "Pink Cabana" | `config/fym-thin-picks-oct26.json` |
| Sorbet (`sorbet`) | Cabana - Seafoam Blue & Ivory with Citrus Fringe (Tala Mahj) | Seafoam Cabana (Tala Mahj) on /sorbet-mahjong-tile-matches | same brand, close name; live card is "Seafoam Cabana" | `config/fym-thin-picks-oct26.json` |
| Sorbet (`sorbet`) | Colony - Chartreuse & Petal Pink (Tala Mahj) | Colony (Tala Mahj) on /sorbet-mahjong-tile-matches | same brand, the live card has the short name (colour / side / variant not on the card); live card is "Colony" | `config/fym-thin-picks-oct26.json` |
| Sunset (`sunset`) | Betty Floral (Monogrammed Neoprene) (Betty June & Jeannette) | Betty Floral (Betty June & Jeannette) on /sunset-mahjong-tile-matches | same brand, close name; live card is "Betty Floral" | `config/fym-thin-picks-oct26.json` |
| Taylor (`taylor`) | Caroline (Preppy) (Betty June & Jeannette) | Caroline (Betty June & Jeannette) on /taylor-mahjong-tile-matches | same brand, the live card has the short name (colour / side / variant not on the card); live card is "Caroline" | `config/fym-thin-picks-oct26.json` |
| Tinselle (`tinselle-emerald`) | Holiday Neoprene (Bam Bird Boutique) | Bam Bird Holiday (Bam Bird Boutique) on /holiday-mahjong-matches | same shop link (holiday-neoprene-mahjong-mat); live card is "Bam Bird Holiday" by Bam Bird Boutique | `config/swipe-yeses/holiday-oct21.json` |
| Tinselle (`tinselle-emerald`) | Bespoke x Corey Paige - Holiday Love Mat - Red/Green (Side A: All-Over Hearts) (Bespoke Mahjong) | Holiday Love Red & Green (Bespoke Mahjong) on /holiday-mahjong-matches | same shop link (holidayloveredgreen); live card is "Holiday Love Red & Green" by Bespoke Mahjong | `config/swipe-yeses/holiday-oct21.json` |
| Tinselle (`tinselle-emerald`) | Letters to Santa Premium (Mahjong Register) | Letters to Santa (Mahjong Register) on /holiday-mahjong-matches | same shop link (preorder-letters-to-santa-premium-mahjong-mat-33-estimated-ship-oct-1st-2026); live card is "Letters to Santa" by Mahjong Register | `config/swipe-yeses/holiday-oct21.json` |
| Tinselle (`tinselle-emerald`) | Peace Love Mahjong holiday mat, variant not recorded (listing mahjong-mats-holiday) (Peace Love Mahjong) | Candy Cane Lane (Peace Love Mahjong) on /holiday-mahjong-matches | same shop link (mahjong-mats-holiday); live card is "Candy Cane Lane" by Peace Love Mahjong | `config/swipe-yeses/holiday-oct21.json` |
| Tinselle (`tinselle-ruby`) | Holiday Neoprene (Bam Bird Boutique) | Bam Bird Holiday (Bam Bird Boutique) on /holiday-mahjong-matches | same shop link (holiday-neoprene-mahjong-mat); live card is "Bam Bird Holiday" by Bam Bird Boutique | `config/swipe-yeses/holiday-oct21.json` |
| Tinselle (`tinselle-ruby`) | Ski Club Red Sweater Border (Charleston Mahjong Club) | Ski Club Red Sweater (Charleston Mahjong Club) on /holiday-mahjong-matches | same brand, close name; live card is "Ski Club Red Sweater" | `config/swipe-yeses/holiday-oct21.json` |
| Tinselle (`tinselle-ruby`) | Holly Jolly Double-Sided Leatherette (Mahjong Register) | Holly Jolly Leatherette (Mahjong Register) on /holiday-mahjong-matches | same shop link (pre-order-very-merry-wreath-double-sided-leatherette-mahjong-mat-31-5-x-31-5-copy); live card is "Holly Jolly Leatherette" by Mahjong Register | `config/swipe-yeses/holiday-oct21.json` |
| Tinselle (`tinselle-ruby`) | Peace Love Mahjong holiday mat, variant not recorded (listing mahjong-mats-holiday) (Peace Love Mahjong) | Candy Cane Lane (Peace Love Mahjong) on /holiday-mahjong-matches | same shop link (mahjong-mats-holiday); live card is "Candy Cane Lane" by Peace Love Mahjong | `config/swipe-yeses/holiday-oct21.json` |
| Willow (`willow`) | Merrywood Leatherette (Britt Mills) | Merrywood (Britt Mills) on /willow-mahjong-tile-matches | same brand, close name; live card is "Merrywood" | `config/picks/missed-mats-round2-partial-2026-11-07.json` |

## Notes

- config/swipe-yeses/holiday-oct21.json book tinselle: mat id "mahjong-mats-holiday" is one store listing for 13 different mats; the yes cannot say which, so any live card from that listing counts (loose)
