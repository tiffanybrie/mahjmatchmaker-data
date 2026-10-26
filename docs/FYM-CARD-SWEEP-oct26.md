# FYM match-card variability sweep (Oct 26)

Read-only audit. One post card was rendered for every visible tile set (276) on build b95t (b94 + title-width fix), using her first pick or the top of the mat deck plus the top 2 racks. Canvas calls were logged to measure the circle, titles, labels and racks. Sheets: assets/qa/card-sweep-oct26/ (all_01-10.jpg = every card in order, worst25.jpg).

## Issue types (cards affected)
| Issue | Cards | Notes |
|---|---|---|
| Rack photo drawn tiny on the card | 53 | Mostly 4 racks: Bespoke Ultimate CRYSTAL CLEAR (21) and BRIGHT WHITE (12), MRC White Rack & Pusher Set (8), Mac + Miller Heirloom Ivory (7). Their photos are stacks or angled sets, so the trimmed image comes out tiny. Same root cause as the vertical-rack job (v95_rackrotate). |
| Title colour washed out on cream (contrast < 2.2:1) | 27 | Bright yellow, teal, mint and lime titles: Pippa, Sorbet, Garden Stamped, Birthday, Lilacée, Mod Chartreuse, Verdant Spring, Teal Coastal, Harbor Mint, Seabreeze, MFM California/Hawaii/Scandinavian, Palm Royale Lemon Drop/Tangerine, Nivalee Emerald, etc. Fix idea: darken the title colour to at least 3:1 (same hue). |
| Long mat name: subtitle overruns the mat and gets truncated with … | 23 subtitle + 22 truncated pills | 13 mats with very long names, e.g. 'Beyond the Ribbon: Four Winds Social Collab Mat Benefitting Pink Fund', 'Emerald Teal & Celedon Green Double-Sided Leatherette', 'Year of the Dragon Mat - Amped-Up Grey', 'Van Gogh Sunflowers & Irises Reversible'. Fix idea: a short display name per mat, and the subtitle capped to the mat column like the title. |
| Photo coming soon circle clips the set name | 19 | e.g. 'nd Top Stam', 'Bam Gratef'. Fix: shrink/wrap the name inside the circle. |
| Generic rack name 'Racks' on the pill | 18 | Bam Bird and Amahj 'Mahjong Rack & Pusher Set' shows as just 'Racks' once the brand is stripped. Fix: give them real names (Bam Bird rename already in v95_addracks). |
| Mat photos that are rolled or angled product shots | visual | Let's Mahj On LMO Floral Border and Signature Logo mats (Garden Party Sky Blue, Let's Garden Party!, Let's Be Iconic Brilliant Pink, Let's Cocktail Party!) look weak on the card. Truncated mat names in the data: 'Spring Awakening P', 'Mocha Bloom LT'. |
| Tile circle mostly white | not reliable | The automatic measure counted white tile faces as empty, so it isn't reported. By eye, the circles are filled except the known Bespoke white corners and the Bam Bird tortoise split, which is fixed by the scatter. |

No render errors (276/276). The title width is fixed on every card by v95_titlewidth. Brand logo chips rendered on every card checked by eye; none blank.

## Worst 25 (by issue score)
| # | Set | Brand | Mat on card | Issues |
|---|---|---|---|---|
| 1 | Sweet Dreams Collection | Mac + Miller Mahjong | Emerald Teal & Celedon Green Double-Sided Leatherette | Photo coming soon circle (name text clipped); subtitle wider than mat (955 vs 692px); truncated label: tiles on the Emerald Teal & Celedon Green Double-Sided Leatheret…; truncated label: Emerald Teal & Celedon Green Double-…; rack tiny on card: Mac + Miller Heirloom Ivory |
| 2 | Round Top Stamped | Amahj | Vegan Leather – Cream | Photo coming soon circle (name text clipped); title colour #9eb04f low contrast (2.1:1); generic rack name "Racks" |
| 3 | Laissez Les Bons Temps Rouler Collection | Mac + Miller Mahjong | Sunday Sherbert Double-Sided Leatherette | Photo coming soon circle (name text clipped); subtitle wider than mat (819 vs 750px); rack tiny on card: Mac + Miller Heirloom Ivory |
| 4 | Corey Paige Color Crush (Bright White) | Bespoke Mahjong | Year of the Dragon Mat - Amped-Up Grey | subtitle wider than mat (806 vs 743px); rack tiny on card: The Ultimate Rack - CRYSTAL CLEAR; rack tiny on card: The Ultimate Rack - BRIGHT WHITE |
| 5 | Gray Malin Getaway Dogs (Beverly Hills Pink) | Bespoke Mahjong | Lucky Charms Mat | truncated label: Gray Malin Getaway Dogs (Beverly Hills Pi…; rack tiny on card: The Ultimate Rack - CRYSTAL CLEAR; rack tiny on card: The Ultimate Rack - BRIGHT WHITE |
| 6 | Cypress | Mahjong Row & Co. | Midnight Garden | rack tiny on card: White Rack & Pusher Set; rack tiny on card: Mahjong Row & Co. Translucent Plum |
| 7 | Lyla | Mahjong Row & Co. | Spring Awakening P | rack tiny on card: White Rack & Pusher Set; rack tiny on card: Mahjong Row & Co. Porcelain Blue |
| 8 | Laken | Mahjong Row & Co. | Spring Awakening P | rack tiny on card: White Rack & Pusher Set; rack tiny on card: Mahjong Row & Co. Porcelain Blue |
| 9 | Terracotta Marble | Mahjong Row & Co. | Mocha Bloom LT | rack tiny on card: White Rack & Pusher Set; rack tiny on card: Mahjong Row & Co. Translucent Plum |
| 10 | The California Series | My Fair Mahjong | Color Wave – Cobalt Center- Light Blue Scallop | title colour #24badb low contrast (2.0:1); subtitle wider than mat (892 vs 704px); truncated label: Color Wave – Cobalt Center- Light Blue S… |
| 11 | Gray Malin Beach Club (Cabana Blue) | Bespoke Mahjong | Bams & Bees | rack tiny on card: The Ultimate Rack - BRIGHT WHITE; rack tiny on card: The Ultimate Rack - CRYSTAL CLEAR |
| 12 | Lucky Charms (Marshmallow Pink) | Bespoke Mahjong | Lucky Charms Mat | rack tiny on card: The Ultimate Rack - CRYSTAL CLEAR; rack tiny on card: The Ultimate Rack - BRIGHT WHITE |
| 13 | Pop Diva (Bright White) | Bespoke Mahjong | Argyle Girl | rack tiny on card: The Ultimate Rack - CRYSTAL CLEAR; rack tiny on card: The Ultimate Rack - BRIGHT WHITE |
| 14 | Springtime Safari (Petal Pink) | Bespoke Mahjong | Year of the Horse Mat - Bubblegum | rack tiny on card: The Ultimate Rack - BRIGHT WHITE; rack tiny on card: The Ultimate Rack - CRYSTAL CLEAR |
| 15 | Springtime Safari (Sky Blue) | Bespoke Mahjong | Gray Malin | rack tiny on card: The Ultimate Rack - CRYSTAL CLEAR; rack tiny on card: The Ultimate Rack - BRIGHT WHITE |
| 16 | The Chalet (Frosty Lilac) | Bespoke Mahjong | Tilly Neoprene | rack tiny on card: The Ultimate Rack - CRYSTAL CLEAR; rack tiny on card: The Ultimate Rack - BRIGHT WHITE |
| 17 | Year of the Horse (Saddle Pink) | Bespoke Mahjong | Year of the Horse Mat - Bubblegum | rack tiny on card: The Ultimate Rack - BRIGHT WHITE; rack tiny on card: The Ultimate Rack - CRYSTAL CLEAR |
| 18 | Gray Malin Getaway Dogs (Icy Blue) | Bespoke Mahjong | Gray Malin | rack tiny on card: The Ultimate Rack - CRYSTAL CLEAR; rack tiny on card: The Ultimate Rack - BRIGHT WHITE |
| 19 | Gray Malin Getaway Dogs (Bright White) | Bespoke Mahjong | Floral Mat | rack tiny on card: The Ultimate Rack - CRYSTAL CLEAR; rack tiny on card: The Ultimate Rack - BRIGHT WHITE |
| 20 | Tradewind (Petal) | Tala Mahj | Tartan Plaid in Preppy Pink | rack tiny on card: The Ultimate Rack - CRYSTAL CLEAR; rack tiny on card: The Ultimate Rack - BRIGHT WHITE |
| 21 | Let's Game. Set. Mahj! | Let's Mahj On | Bandana – Olive Green/Dusty Lilac accents | subtitle wider than mat (838 vs 683px); truncated label: Bandana – Olive Green/Dusty Lilac acc…; generic rack name "Racks" |
| 22 | Red White & Blues Collection | Mac + Miller Mahjong | Heirloom Collection: Chinoiserie Classic Mahjong Mat | subtitle wider than mat (781 vs 715px); rack tiny on card: Mac + Miller Heirloom Ivory |
| 23 | Year of the Horse (Pearl Cream) | Bespoke Mahjong | Year of the Dragon Mat - Amped-Up Grey | subtitle wider than mat (806 vs 730px); rack tiny on card: The Ultimate Rack - CRYSTAL CLEAR |
| 24 | Corey Paige Color Crush (Pearl Crush) | Bespoke Mahjong | Year of the Dragon Mat - Amped-Up Grey | subtitle wider than mat (806 vs 743px); rack tiny on card: The Ultimate Rack - CRYSTAL CLEAR |
| 25 | Grateful Dead (Rose Pink Tie Dye Pearl) | Bespoke Mahjong | Year of the Dragon Mat - Amped-Up Pink | subtitle wider than mat (805 vs 742px); rack tiny on card: The Ultimate Rack - CRYSTAL CLEAR |
