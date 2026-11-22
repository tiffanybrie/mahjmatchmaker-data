# Holiday completeness audit, year-round album pages (2026-11-22)

Closes the "HOLIDAY COMPLETENESS AUDIT, REMAINING PART" line in docs/OVERDUE.md (the /holiday-mahjong-matches part was done Nov 9, site/livepatch/holiday-fix-nov09/README.md). Read-only audit: nothing on the site or in the repo was changed.

## Method

- Pages: every `*-mahjong-tile-matches` URL in https://www.mahjmatchmaker.com/sitemap.xml, fetched with curl on 2026-11-22 (56 pages, all HTTP 200, ~350ms apart). 44 are tile-set album pages with a holiday section (`<section class="mm3-hol" id="holiday-matches">`). Lilac Soiree has no holiday section and no yeses in the sources. The index and the 10 colour/style pages (pink, blue, green, yellow-orange, purple, neutral, masculine, red, brown, ivory) carry no cards and are not tile-set albums.
- Yeses: `config/swipe-yeses/holiday-oct21.json` books `omm` (55 yeses), `plmmats` (187), `santababy` (12), all mode "mat" (pair = [mat, tile set]); plus `config/late-holiday-picks-nov03.json` (33 picks). The `tinselle` and `spirit` books are holiday tile sets (holiday page, already audited).
- Match = mat name AND brand, read from each card's `<h3>` ("Set + Mat") and "Mat by" line. PLM Candy Cane Lane and Anders Ruff Candy Cane Lane are different mats. "Peace Love Holiday" (PLM) is counted as PLM Sugarplum Plaid. Santa Baby's Cocktail Hour has no brand in the yes file; the live cards say Splash of Color.
- Each MISSING was re-checked with a plain text search of the whole page (not only the holiday section): the mat name appears 0 times on the page, except Nantucket, where "Candy Cane Lane" appears only as the Anders Ruff mat.
- "Cards not in her yeses" means not in these four sources only. Most album holiday sections were built from other approved sources (album picks, FYM m-lists), so that list is information, not a removal list. Nothing should be removed on the strength of it.
- Out of scope here: yeses whose tile set is a holiday set (Dear Santa, Rackin' Rudolph, Holly Jolly x3, Tinselle x2, Nivalee, Nutcracker Ballet, December 1994, PLM Nutcracker, PLM Spirit): those live on /holiday-mahjong-matches, audited Nov 9.

## Summary

- Album pages checked: **44** with a holiday section (+ Lilac Soiree, no section, nothing expected).
- Yes pairs for those pages: 176. Present: 161. **Missing: 15**, on 13 pages.
- 12 of the 15 are the three retired Oh My Mahjong mats (Miracle 5, Merry Mahjong 5, Twilight Waltz 2). The other 3 are Peace Love Mahjong mats.
- Every late-holiday pick (Nov 3) for a year-round set with a live page is present.

### All missing cards

| Album page | Mat | Brand | Source (file + key) | Product URL |
|---|---|---|---|---|
| /heritage-mahjong-tile-matches | Merry Mahjong | Oh My Mahjong | config/swipe-yeses/holiday-oct21.json books.omm.yes ["merry-mahjong","heritage"] | retired at OMM, no product page (other live cards link https://www.ohmymahjong.com/collections/mahjong-mats) |
| /heritage-mahjong-tile-matches | Twilight Waltz | Oh My Mahjong | config/swipe-yeses/holiday-oct21.json books.omm.yes ["twilight-waltz","heritage"] | retired at OMM, no product page (other live cards link https://www.ohmymahjong.com/collections/mahjong-mats) |
| /heritage-mahjong-tile-matches | Miracle | Oh My Mahjong | config/swipe-yeses/holiday-oct21.json books.omm.yes ["miracle","heritage"] | retired at OMM, no product page (other live cards link https://www.ohmymahjong.com/collections/mahjong-mats) |
| /jasmine-mahjong-tile-matches | Twilight Waltz | Oh My Mahjong | config/swipe-yeses/holiday-oct21.json books.omm.yes ["twilight-waltz","jasmine"] | retired at OMM, no product page (other live cards link https://www.ohmymahjong.com/collections/mahjong-mats) |
| /limoncello-mahjong-tile-matches | Merry Mahjong | Oh My Mahjong | config/swipe-yeses/holiday-oct21.json books.omm.yes ["merry-mahjong","limoncello"] | retired at OMM, no product page (other live cards link https://www.ohmymahjong.com/collections/mahjong-mats) |
| /lola-mahjong-tile-matches | Merry Mahjong | Oh My Mahjong | config/swipe-yeses/holiday-oct21.json books.omm.yes ["merry-mahjong","lola"] | retired at OMM, no product page (other live cards link https://www.ohmymahjong.com/collections/mahjong-mats) |
| /nantucket-mahjong-tile-matches | Candy Cane Lane | Peace Love Mahjong | config/swipe-yeses/holiday-oct21.json books.plmmats.yes ["plm-candy-cane-lane","nantucket"] | https://peacelovemahjong.com/discount/MAHJMATCH?redirect=%2Fproducts%2Fmahjong-mats-holiday%3Fvariant%3D67570557354276 |
| /osler-mahjong-tile-matches | Miracle | Oh My Mahjong | config/swipe-yeses/holiday-oct21.json books.omm.yes ["miracle","osler"] | retired at OMM, no product page (other live cards link https://www.ohmymahjong.com/collections/mahjong-mats) |
| /palm-royale-mahjong-tile-matches | Merry Mahjong | Oh My Mahjong | config/swipe-yeses/holiday-oct21.json books.omm.yes ["merry-mahjong","palm-royale"] | retired at OMM, no product page (other live cards link https://www.ohmymahjong.com/collections/mahjong-mats) |
| /papaya-spritz-mahjong-tile-matches | Spirit of Christmas | Peace Love Mahjong | config/swipe-yeses/holiday-oct21.json books.plmmats.yes ["plm-spirit-of-christmas","papaya-spritz"] | https://peacelovemahjong.com/discount/MAHJMATCH?redirect=%2Fproducts%2Fmahjong-mats-holiday%3Fvariant%3D67570521473316 |
| /pearlescent-mahjong-tile-matches | Merry Mahjong | Oh My Mahjong | config/swipe-yeses/holiday-oct21.json books.omm.yes ["merry-mahjong","pearlescent"] | retired at OMM, no product page (other live cards link https://www.ohmymahjong.com/collections/mahjong-mats) |
| /sorbet-mahjong-tile-matches | Miracle | Oh My Mahjong | config/swipe-yeses/holiday-oct21.json books.omm.yes ["miracle","sorbet"] | retired at OMM, no product page (other live cards link https://www.ohmymahjong.com/collections/mahjong-mats) |
| /spring-love-mahjong-tile-matches | Pretty Little Christmas | Peace Love Mahjong | config/swipe-yeses/holiday-oct21.json books.plmmats.yes ["plm-pretty-little-christmas","vault-spring-love"] | https://peacelovemahjong.com/discount/MAHJMATCH?redirect=%2Fproducts%2Fmahjong-mats-holiday%3Fvariant%3D67570521375012 |
| /sunday-tile-set-mahjong-tile-matches | Miracle | Oh My Mahjong | config/swipe-yeses/holiday-oct21.json books.omm.yes ["miracle","sunday"] | retired at OMM, no product page (other live cards link https://www.ohmymahjong.com/collections/mahjong-mats) |
| /talulah-mahjong-tile-matches | Miracle | Oh My Mahjong | config/swipe-yeses/holiday-oct21.json books.omm.yes ["miracle","talulah"] | retired at OMM, no product page (other live cards link https://www.ohmymahjong.com/collections/mahjong-mats) |

Count by mat: Merry Mahjong 5, Miracle 5, Twilight Waltz 2, Candy Cane Lane 1, Spirit of Christmas 1, Pretty Little Christmas 1.

Notes on the missing ones:
- Nantucket: her yes is **Peace Love Mahjong** Candy Cane Lane; the page shows **Anders Ruff** Candy Cane Lane instead (not in these yes files). Looks like the brand mix-up the OVERDUE line warns about. The PLM card is missing; whether the Anders Ruff card stays is her call or needs another source.
- Heritage is missing all three retired OMM mats (Miracle, Merry Mahjong, Twilight Waltz) while 29 other cards with those mats are live on other album pages, so retired status alone is not why.
- Sunday Tile Set: see the Sunday section below.

## Hidden / not-yet-live sets: "goes in with the album"

No album page exists for these sets (not in the sitemap), so their holiday yeses go in when the album is built. The Hummingbird, Nature Walk and Sunday Blues sections on /holiday-mahjong-matches are still `display:none`.

### Hummingbird (Sunday Mahjong)
Hidden section on the holiday page today (3 cards): Festive Plaid (Sunday Mahjong); The Polo Club (Luxe Mahjong); Home for the Holidays (Soirée All Day).

| Holiday yes (mat) | Brand | Source | Product URL | Already in hidden section? |
|---|---|---|---|---|
| Twilight Waltz | Oh My Mahjong | config/swipe-yeses/holiday-oct21.json books.omm.yes ["twilight-waltz","hummingbird"] | retired at OMM, no product page | no |
| Vintage Noel | Peace Love Mahjong | config/swipe-yeses/holiday-oct21.json books.plmmats.yes ["plm-vintage-noel","hummingbird"] | https://peacelovemahjong.com/discount/MAHJMATCH?redirect=%2Fproducts%2Fmahjong-mats-holiday%3Fvariant%3D67570521407780 | no |
| Merry Mix | Peace Love Mahjong | config/swipe-yeses/holiday-oct21.json books.plmmats.yes ["plm-merry-mix","hummingbird"] | https://peacelovemahjong.com/discount/MAHJMATCH?redirect=%2Fproducts%2Fmahjong-mats-holiday%3Fvariant%3D67570521276708 | no |
| Nutcracker Noel - Red & Green | Peace Love Mahjong | config/swipe-yeses/holiday-oct21.json books.plmmats.yes ["plm-nutcracker-noel-red-green","hummingbird"] | https://peacelovemahjong.com/discount/MAHJMATCH?redirect=%2Fproducts%2Fmahjong-mats-holiday%3Fvariant%3D67570521309476 | no |
| Home for the Holidays | Soirée All Day | config/late-holiday-picks-nov03.json picks["Soirée All Day \| Home for the Holidays"] -> "Hummingbird" | https://www.soireeallday.co/the-mahjong-collection/p/home-for-the-holidays-mahjong-mat?ref=MAHJMATCH | yes |

### Sunday Blues (Sunday Mahjong)
Hidden section on the holiday page today (1 cards): The Polo Club (Luxe Mahjong).

| Holiday yes (mat) | Brand | Source | Product URL | Already in hidden section? |
|---|---|---|---|---|
| Miracle | Oh My Mahjong | config/swipe-yeses/holiday-oct21.json books.omm.yes ["miracle","sunday-blues"] | retired at OMM, no product page | no |
| Twilight Waltz | Oh My Mahjong | config/swipe-yeses/holiday-oct21.json books.omm.yes ["twilight-waltz","sunday-blues"] | retired at OMM, no product page | no |

### Plum Panda (Sunday Mahjong)
No hidden section on the holiday page and no album page.

| Holiday yes (mat) | Brand | Source | Product URL | Already in hidden section? |
|---|---|---|---|---|
| Miracle | Oh My Mahjong | config/swipe-yeses/holiday-oct21.json books.omm.yes ["miracle","plum-panda"] | retired at OMM, no product page | no |

### Cypress Forest
No hidden section on the holiday page and no album page.

| Holiday yes (mat) | Brand | Source | Product URL | Already in hidden section? |
|---|---|---|---|---|
| Twilight Waltz | Oh My Mahjong | config/swipe-yeses/holiday-oct21.json books.omm.yes ["twilight-waltz","cypress-forest"] | retired at OMM, no product page | no |
| Nutcracker Noel - Red & Green | Peace Love Mahjong | config/swipe-yeses/holiday-oct21.json books.plmmats.yes ["plm-nutcracker-noel-red-green","cypress-forest"] | https://peacelovemahjong.com/discount/MAHJMATCH?redirect=%2Fproducts%2Fmahjong-mats-holiday%3Fvariant%3D67570521309476 | no |

### Nature Walk (Sunday Mahjong)
No holiday yeses in the four sources. Hidden section on the holiday page: The Polo Club (Luxe Mahjong). (docs/ANSWERS.md Oct 29 mentions a Nature Walk yes on Anders Ruff Evergreen & Tartan in the Sunday Sets swipe book; that book is not one of the sources of this audit.)

### Sunday Tile Set: page is LIVE, not hidden
The task listed `sunday` as hidden, but /sunday-tile-set-mahjong-tile-matches is in the sitemap, returns 200 and is linked from /mahjong-tile-matches, with a holiday section of 8 cards. It is audited as a live page below: 6 of 7 yeses present, missing OMM Miracle. Its section on /holiday-mahjong-matches is still `display:none` (2 cards: Festive Plaid, The Polo Club), so the holiday page does not show Sunday Tile Set even though the album is live.

## Per album page

### /amara-mahjong-tile-matches
Holiday cards on page: 16. Yeses in sources: 6. Present: 6. Missing: 0. Cards not in her yeses: 9.

- **Present:** Sugarplum Plaid (Peace Love Mahjong) [card title: "Peace Love Holiday"]; Pretty Little Christmas (Peace Love Mahjong); Perfectly Wrapped (Peace Love Mahjong); Merry Mix (Peace Love Mahjong); Santa Baby's Cocktail Hour (Splash of Color); Peppermint Wishes (My Fair Mahjong)
- **MISSING:** none
- **Cards not in her yeses (these sources):** Clara (Oh My Mahjong); Clara's Dream Christmas (Mahj Squad); Merriment (Oh My Mahjong); Sugarplum (Oh My Mahjong); Very Merry Mahj (Anders Ruff); Very Merry Wreath (Mahjong Register); Yuletide (Oh My Mahjong); Candy Cane Pink Wonderland (Mahj Squad); Watercolor Christmas Tree (Anders Ruff)
- Note: the same PLM plaid mat appears twice on this page, once as "Peace Love Holiday" and once as "Sugarplum Plaid".

### /birdie-mahjong-tile-matches
Holiday cards on page: 18. Yeses in sources: 3. Present: 3. Missing: 0. Cards not in her yeses: 15.

- **Present:** Twilight Waltz (Oh My Mahjong); Nutcracker Noel - Gold (Peace Love Mahjong); Tied With A Bow (Peace Love Mahjong)
- **MISSING:** none
- **Cards not in her yeses (these sources):** Holly Jolly (Oh My Mahjong); Merriment (Oh My Mahjong); Winterberry (Oh My Mahjong); Alpine Ski Lodge Winter (Splash of Color); Candy Cane Pink Wonderland (Mahj Squad); Clara (Oh My Mahjong); Clara's Dream Christmas (Mahj Squad); Hanukkah (Peace Love Mahjong); Holiday Love Blue (Bespoke Mahjong); Liberty (Oh My Mahjong); Santa's Mahjong Mail (Anders Ruff); Ski Club Periwinkle (Charleston Mahjong Club); Ski Club Red Sweater (Charleston Mahjong Club); Sugarplum (Oh My Mahjong); Frosted Flowers (Peace Love Mahjong)

### /brownstone-bloom-mahjong-tile-matches
Holiday cards on page: 1. Yeses in sources: 0. Present: 0. Missing: 0. Cards not in her yeses: 1.

- **Present:** none
- **MISSING:** none
- **Cards not in her yeses (these sources):** Christmas Tree Gingham (Amazon)

### /coquette-mahjong-tile-matches
Holiday cards on page: 17. Yeses in sources: 6. Present: 6. Missing: 0. Cards not in her yeses: 11.

- **Present:** Miracle (Oh My Mahjong); Vintage Noel (Peace Love Mahjong); Candy Cane Lane (Peace Love Mahjong); Pretty Little Christmas (Peace Love Mahjong); Perfectly Wrapped (Peace Love Mahjong); Tied With A Bow (Peace Love Mahjong)
- **MISSING:** none
- **Cards not in her yeses (these sources):** Candy Cane Pink Wonderland (Mahj Squad); Clara's Dream Christmas (Mahj Squad); Merriment (Oh My Mahjong); Nutcracker (Britt Mills); Sugarplum (Oh My Mahjong); Peace Love Holiday (Peace Love Mahjong); Sugarplum Plaid (Peace Love Mahjong); Holly Jolly Christmas (Bam! Let's Mahjong); Very Merry Mahj (Anders Ruff); Very Merry Wreath (Mahjong Register); Pink Christmas Tree Gingham (Amazon)
- Note: the same PLM plaid mat appears twice on this page, once as "Peace Love Holiday" and once as "Sugarplum Plaid".

### /dandy-mahjong-tile-matches
Holiday cards on page: 12. Yeses in sources: 4. Present: 4. Missing: 0. Cards not in her yeses: 7.

- **Present:** Sugarplum Plaid (Peace Love Mahjong) [card title: "Peace Love Holiday"]; Perfectly Wrapped (Peace Love Mahjong); Santa Baby's Cocktail Hour (Splash of Color); Poinsettia Party (Soirée All Day)
- **MISSING:** none
- **Cards not in her yeses (these sources):** Clara (Oh My Mahjong); Very Merry Mahj (Anders Ruff); Very Merry Wreath (Mahjong Register); Sugarplum (Oh My Mahjong); Watercolor Christmas Tree (Anders Ruff); Yuletide (Oh My Mahjong); Chinoiserie Christmas Tree (Etsy)
- Note: the same PLM plaid mat appears twice on this page, once as "Peace Love Holiday" and once as "Sugarplum Plaid".

### /deco-lagoon-mahjong-tile-matches
Holiday cards on page: 3. Yeses in sources: 0. Present: 0. Missing: 0. Cards not in her yeses: 3.

- **Present:** none
- **MISSING:** none
- **Cards not in her yeses (these sources):** Winter Jewel (Let's Be Besties); Yuletide (Oh My Mahjong); Poinsettia Party (Soirée All Day)

### /drake-mahjong-tile-matches
Holiday cards on page: 6. Yeses in sources: 1. Present: 1. Missing: 0. Cards not in her yeses: 5.

- **Present:** Merry Mahjong (Oh My Mahjong)
- **MISSING:** none
- **Cards not in her yeses (these sources):** Merrywood (Britt Mills); Winter Berry (Britt Mills); Tartan Tidings (Anders Ruff); Winterberry (Oh My Mahjong); Scandi Folk Christmas (Green) (Etsy)

### /emerald-mahjong-tile-matches
Holiday cards on page: 15. Yeses in sources: 5. Present: 5. Missing: 0. Cards not in her yeses: 10.

- **Present:** Miracle (Oh My Mahjong); Twilight Waltz (Oh My Mahjong); Tied With A Bow (Peace Love Mahjong); Candy Cane Lane (Peace Love Mahjong); Santa Baby's Cocktail Hour (Splash of Color)
- **MISSING:** none
- **Cards not in her yeses (these sources):** Clara (Oh My Mahjong); Merriment (Oh My Mahjong); Very Merry Wreath (Mahjong Register); Candy Cane Pink Wonderland (Mahj Squad); Peace Love Holiday (Peace Love Mahjong); Sugarplum Plaid (Peace Love Mahjong); Sugarplum (Oh My Mahjong); Very Merry Mahj (Anders Ruff); Yuletide (Oh My Mahjong); Festive Frost (Let's Be Besties)
- Note: the same PLM plaid mat appears twice on this page, once as "Peace Love Holiday" and once as "Sugarplum Plaid".

### /gatsby-mahjong-tile-matches
Holiday cards on page: 12. Yeses in sources: 0. Present: 0. Missing: 0. Cards not in her yeses: 12.

- **Present:** none
- **MISSING:** none
- **Cards not in her yeses (these sources):** Merrywood (Britt Mills); Winterberry (Oh My Mahjong); Alpine Ski Lodge Winter (Splash of Color); Holly Jolly (Oh My Mahjong); Rackin' Rudolph (Hip Hip Mahjong); Ski Club Red Sweater (Charleston Mahjong Club); Tartan Tidings (Anders Ruff); Tartan Toile Noël (Anders Ruff); The Polo Club (Luxe Mahjong); Very Merry Wreath (Mahjong Register); Winter Berry (Britt Mills); Yuletide (Oh My Mahjong)

### /gemma-mahjong-tile-matches
Holiday cards on page: 5. Yeses in sources: 1. Present: 1. Missing: 0. Cards not in her yeses: 4.

- **Present:** Miracle (Oh My Mahjong)
- **MISSING:** none
- **Cards not in her yeses (these sources):** Clara (Oh My Mahjong); Merriment (Oh My Mahjong); Ski Club Periwinkle (Charleston Mahjong Club); Winter Berry (Britt Mills)

### /glitterville-mahjong-tile-matches
Holiday cards on page: 12. Yeses in sources: 5. Present: 5. Missing: 0. Cards not in her yeses: 6.

- **Present:** Merry Mahjong (Oh My Mahjong); Sugarplum Plaid (Peace Love Mahjong) [card title: "Peace Love Holiday"]; Perfectly Wrapped (Peace Love Mahjong); Santa Baby's Cocktail Hour (Splash of Color); Peppermint Wishes (My Fair Mahjong)
- **MISSING:** none
- **Cards not in her yeses (these sources):** Clara (Oh My Mahjong); Very Merry Mahj (Anders Ruff); Very Merry Wreath (Mahjong Register); Candy Cane Pink Wonderland (Mahj Squad); Sugarplum (Oh My Mahjong); Yuletide (Oh My Mahjong)
- Note: the same PLM plaid mat appears twice on this page, once as "Peace Love Holiday" and once as "Sugarplum Plaid".

### /glow-wild-mahjong-tile-matches
Holiday cards on page: 9. Yeses in sources: 4. Present: 4. Missing: 0. Cards not in her yeses: 4.

- **Present:** Merry Mix (Peace Love Mahjong); Sugarplum Plaid (Peace Love Mahjong) [card title: "Peace Love Holiday"]; Tied With A Bow (Peace Love Mahjong); Pretty Little Christmas (Peace Love Mahjong)
- **MISSING:** none
- **Cards not in her yeses (these sources):** Clara (Oh My Mahjong); Very Merry Mahj (Anders Ruff); Sugarplum (Oh My Mahjong); Very Merry Wreath (Mahjong Register)
- Note: the same PLM plaid mat appears twice on this page, once as "Peace Love Holiday" and once as "Sugarplum Plaid".

### /heritage-mahjong-tile-matches
Holiday cards on page: 9. Yeses in sources: 12. Present: 9. Missing: 3. Cards not in her yeses: 0.

- **Present:** Peace Love & Mistletoe (Peace Love Mahjong); Pretty Little Christmas (Peace Love Mahjong); Spirit of Christmas (Peace Love Mahjong); Nutcracker Noel - Red & Green (Peace Love Mahjong); Vintage Noel (Peace Love Mahjong); Nutcracker Noel - Gold (Peace Love Mahjong); Merry & Striped (Peace Love Mahjong); Perfectly Wrapped (Peace Love Mahjong); Santa Baby's Cocktail Hour (Splash of Color)
- **MISSING:**
  - Merry Mahjong (Oh My Mahjong). Source: config/swipe-yeses/holiday-oct21.json books.omm.yes ["merry-mahjong","heritage"]. URL: retired at OMM, no product page
  - Twilight Waltz (Oh My Mahjong). Source: config/swipe-yeses/holiday-oct21.json books.omm.yes ["twilight-waltz","heritage"]. URL: retired at OMM, no product page
  - Miracle (Oh My Mahjong). Source: config/swipe-yeses/holiday-oct21.json books.omm.yes ["miracle","heritage"]. URL: retired at OMM, no product page
- **Cards not in her yeses (these sources):** none

### /heritage-2-0-mahjong-tile-matches
Holiday cards on page: 24. Yeses in sources: 9. Present: 9. Missing: 0. Cards not in her yeses: 15.

- **Present:** Twilight Waltz (Oh My Mahjong); Merry Mahjong (Oh My Mahjong); Pretty Little Christmas (Peace Love Mahjong); Peace Love & Mistletoe (Peace Love Mahjong); Nutcracker Noel - Gold (Peace Love Mahjong); Nutcracker Noel - Red & Green (Peace Love Mahjong); Spirit of Christmas (Peace Love Mahjong); Merry & Striped (Peace Love Mahjong); Merry Mix (Peace Love Mahjong)
- **MISSING:** none
- **Cards not in her yeses (these sources):** Festive Plaid (Sunday Mahjong); Bam Bird Holiday (Bam Bird Boutique); Holly Jolly (Oh My Mahjong); Letters to Santa (Mahjong Register); Santa's Mahjong Mail (Anders Ruff); Blue Christmas (Mahj Squad); Candy Cane Lane (Anders Ruff); Evergreen & Tartan (Anders Ruff); Rackin' Rudolph (Hip Hip Mahjong); Sleigh All Day (Mahj Mood); The Polo Club (Luxe Mahjong); Very Merry Mahj (Anders Ruff); Winter Berry (Britt Mills); Winterberry (Oh My Mahjong); Yuletide (Oh My Mahjong)

### /jade-mahjong-tile-matches
Holiday cards on page: 31. Yeses in sources: 11. Present: 11. Missing: 0. Cards not in her yeses: 20.

- **Present:** Twilight Waltz (Oh My Mahjong); Merry Mahjong (Oh My Mahjong); Perfectly Wrapped (Peace Love Mahjong); Sugarplum Plaid (Peace Love Mahjong); Spirit of Christmas (Peace Love Mahjong); Merry & Striped (Peace Love Mahjong); Nutcracker Noel - Gold (Peace Love Mahjong); Merry Mix (Peace Love Mahjong); Nutcracker Noel - Red & Green (Peace Love Mahjong); Tied With A Bow (Peace Love Mahjong); Color Me Merry (Soirée All Day)
- **MISSING:** none
- **Cards not in her yeses (these sources):** Blue Christmas (Mahj Squad); Bam Bird Holiday (Bam Bird Boutique); Holly Jolly (Oh My Mahjong); Very Merry Mahj (Anders Ruff); Very Merry Wreath (Mahjong Register); Winterberry (Oh My Mahjong); Clara (Oh My Mahjong); Clara's Dream Christmas (Mahj Squad); Classic Very Merry Mahj (Anders Ruff); Festive Plaid (Sunday Mahjong); Holiday Love Red & Green (Bespoke Mahjong); Holly Berry (Mahj Mood); Merrywood (Britt Mills); Santa's Mahjong Mail (Anders Ruff); Sugarplum (Oh My Mahjong); The Polo Club (Luxe Mahjong); Watercolor Christmas Tree (Anders Ruff); Winter Berry (Britt Mills); Yuletide (Oh My Mahjong); Festive Frost (Let's Be Besties)

### /jasmine-mahjong-tile-matches
Holiday cards on page: 15. Yeses in sources: 7. Present: 6. Missing: 1. Cards not in her yeses: 9.

- **Present:** Peace Love & Mistletoe (Peace Love Mahjong); Perfectly Wrapped (Peace Love Mahjong); Sugarplum Plaid (Peace Love Mahjong); Merry & Striped (Peace Love Mahjong); Tied With A Bow (Peace Love Mahjong); Candy Cane Lane (Peace Love Mahjong)
- **MISSING:**
  - Twilight Waltz (Oh My Mahjong). Source: config/swipe-yeses/holiday-oct21.json books.omm.yes ["twilight-waltz","jasmine"]. URL: retired at OMM, no product page
- **Cards not in her yeses (these sources):** Blue Christmas (Mahj Squad); Holly Jolly (Oh My Mahjong); Very Merry Wreath (Mahjong Register); Clara (Oh My Mahjong); Classic Very Merry Mahj (Anders Ruff); Holly Berry (Mahj Mood); Very Merry Mahj (Anders Ruff); Yuletide (Oh My Mahjong); Festive Frost (Let's Be Besties)

### /juniper-mahjong-tile-matches
Holiday cards on page: 5. Yeses in sources: 0. Present: 0. Missing: 0. Cards not in her yeses: 5.

- **Present:** none
- **MISSING:** none
- **Cards not in her yeses (these sources):** Holly Berry Mat (Mahj Mood); Yuletide (Oh My Mahjong); Watercolor Christmas Tree (Anders Ruff); Very Merry Wreath Premium (Mahjong Register); Perfectly Wrapped (Peace Love Mahjong)

### /la-fete-mahjong-tile-matches
Holiday cards on page: 24. Yeses in sources: 13. Present: 13. Missing: 0. Cards not in her yeses: 10.

- **Present:** Merry Mahjong (Oh My Mahjong); Miracle (Oh My Mahjong); Sugarplum Plaid (Peace Love Mahjong) [card title: "Peace Love Holiday"]; Vintage Noel (Peace Love Mahjong); Nutcracker Noel - Gold (Peace Love Mahjong); Tied With A Bow (Peace Love Mahjong); Perfectly Wrapped (Peace Love Mahjong); Peace Love & Mistletoe (Peace Love Mahjong); Merry Mix (Peace Love Mahjong); Candy Cane Lane (Peace Love Mahjong); Santa Baby's Cocktail Hour (Splash of Color); Color Me Merry (Soirée All Day); Pretty in Pink (Soirée All Day)
- **MISSING:** none
- **Cards not in her yeses (these sources):** Merriment (Oh My Mahjong); Sugarplum (Oh My Mahjong); Very Merry Wreath (Mahjong Register); Candy Cane Pink Wonderland (Mahj Squad); Clara (Oh My Mahjong); Clara's Dream Christmas (Mahj Squad); Holly Jolly Christmas (Bam! Let's Mahjong); Very Merry Mahj (Anders Ruff); Pink Christmas Tree Gingham (Amazon); Poinsettia Ornament (Piper Chase Studios)
- Note: the same PLM plaid mat appears twice on this page, once as "Peace Love Holiday" and once as "Sugarplum Plaid".

### /lagoon-mahjong-tile-matches
Holiday cards on page: 6. Yeses in sources: 0. Present: 0. Missing: 0. Cards not in her yeses: 6.

- **Present:** none
- **MISSING:** none
- **Cards not in her yeses (these sources):** Clara (Oh My Mahjong); Merriment (Oh My Mahjong); Sugarplum (Oh My Mahjong); Very Merry Mahj (Anders Ruff); Winter Berry (Britt Mills); Winter Jewel (Let's Be Besties)

### /limoncello-mahjong-tile-matches
Holiday cards on page: 4. Yeses in sources: 2. Present: 1. Missing: 1. Cards not in her yeses: 3.

- **Present:** Poinsettia Party (Soirée All Day)
- **MISSING:**
  - Merry Mahjong (Oh My Mahjong). Source: config/swipe-yeses/holiday-oct21.json books.omm.yes ["merry-mahjong","limoncello"]. URL: retired at OMM, no product page
- **Cards not in her yeses (these sources):** Sugarplum (Oh My Mahjong); Very Merry Mahj (Anders Ruff); Watercolor Christmas Tree (Anders Ruff)

### /lola-mahjong-tile-matches
Holiday cards on page: 14. Yeses in sources: 4. Present: 3. Missing: 1. Cards not in her yeses: 11.

- **Present:** Spirit of Christmas (Peace Love Mahjong); Star of David Hanukkah (Soirée All Day); Peace on Earth (House of Hearts Studio)
- **MISSING:**
  - Merry Mahjong (Oh My Mahjong). Source: config/swipe-yeses/holiday-oct21.json books.omm.yes ["merry-mahjong","lola"]. URL: retired at OMM, no product page
- **Cards not in her yeses (these sources):** Clara (Oh My Mahjong); Holly Jolly (Oh My Mahjong); Merriment (Oh My Mahjong); Sugarplum (Oh My Mahjong); Hanukkah (Peace Love Mahjong); Hip Hip Hanukkah (Hip Hip Mahjong); Liberty (Oh My Mahjong); Ski Club Periwinkle (Charleston Mahjong Club); Winterberry (Oh My Mahjong); Blue & White Snowflake (Amazon); Frosted Flowers (Peace Love Mahjong)

### /luminaire-mahjong-tile-matches
Holiday cards on page: 7. Yeses in sources: 2. Present: 2. Missing: 0. Cards not in her yeses: 5.

- **Present:** Miracle (Oh My Mahjong); Pretty in Pink (Soirée All Day)
- **MISSING:** none
- **Cards not in her yeses (these sources):** Merriment (Oh My Mahjong); Nutcracker (Britt Mills); Candy Cane Pink Wonderland (Mahj Squad); Clara's Dream Christmas (Mahj Squad); Sugarplum (Oh My Mahjong)

### /malachite-mahjong-tile-matches
Holiday cards on page: 23. Yeses in sources: 5. Present: 5. Missing: 0. Cards not in her yeses: 18.

- **Present:** Twilight Waltz (Oh My Mahjong); Merry Mahjong (Oh My Mahjong); Merry Mix (Peace Love Mahjong); Merry & Striped (Peace Love Mahjong); Toasty & Tipsy (Soirée All Day)
- **MISSING:** none
- **Cards not in her yeses (these sources):** Candy Cane Lane (Anders Ruff); Classic Very Merry Mahj (Anders Ruff); Evergreen & Tartan (Anders Ruff); Merrywood (Britt Mills); Santa's Mahjong Mail (Anders Ruff); Sleigh All Day (Mahj Mood); Tartan Tidings (Anders Ruff); Tartan Toile Noël (Anders Ruff); Alpine Ski Lodge Winter (Splash of Color); Festive Plaid (Sunday Mahjong); Holly Jolly (Oh My Mahjong); Letters to Santa (Mahjong Register); Nutcracker (Britt Mills); The Polo Club (Luxe Mahjong); Winterberry (Oh My Mahjong); Yuletide (Oh My Mahjong); Green Christmas Watercolor (Etsy); Plaid Tidings (My Fair Mahjong)

### /moonlight-mahjong-tile-matches
Holiday cards on page: 25. Yeses in sources: 7. Present: 7. Missing: 0. Cards not in her yeses: 18.

- **Present:** Miracle (Oh My Mahjong); Merry Mahjong (Oh My Mahjong); Twilight Waltz (Oh My Mahjong); Pretty Little Christmas (Peace Love Mahjong); Spirit of Christmas (Peace Love Mahjong); Star of David Hanukkah (Soirée All Day); Peace on Earth (House of Hearts Studio)
- **MISSING:** none
- **Cards not in her yeses (these sources):** Blue Christmas (Mahj Squad); Clara (Oh My Mahjong); Holly Jolly (Oh My Mahjong); Merriment (Oh My Mahjong); Sugarplum (Oh My Mahjong); Winter Berry (Britt Mills); Winterberry (Oh My Mahjong); Alpine Ski Lodge Winter (Splash of Color); Hanukkah (Peace Love Mahjong); Hip Hip Hanukkah (Hip Hip Mahjong); Holiday Love Blue (Bespoke Mahjong); Liberty (Oh My Mahjong); Ski Club Periwinkle (Charleston Mahjong Club); Snowflake Lodge (Mahjong Register); Tartan Toile Noël (Anders Ruff); Blue & White Snowflake (Amazon); Flaming Dreidels (Let's Be Besties); Frosted Flowers (Peace Love Mahjong)

### /nantucket-mahjong-tile-matches
Holiday cards on page: 38. Yeses in sources: 14. Present: 13. Missing: 1. Cards not in her yeses: 24.

- **Present:** Twilight Waltz (Oh My Mahjong); Merry Mahjong (Oh My Mahjong); Peace Love & Mistletoe (Peace Love Mahjong); Sugarplum Plaid (Peace Love Mahjong) [card title: "Peace Love Holiday"]; Merry Mix (Peace Love Mahjong); Nutcracker Noel - Red & Green (Peace Love Mahjong); Tied With A Bow (Peace Love Mahjong); Merry & Striped (Peace Love Mahjong); Perfectly Wrapped (Peace Love Mahjong); Spirit of Christmas (Peace Love Mahjong); Santa Baby's Cocktail Hour (Splash of Color); Plaid Tidings (My Fair Mahjong); It's a Vibe Holiday (Bespoke Mahjong)
- **MISSING:**
  - Candy Cane Lane (Peace Love Mahjong). Source: config/swipe-yeses/holiday-oct21.json books.plmmats.yes ["plm-candy-cane-lane","nantucket"]. URL: https://peacelovemahjong.com/discount/MAHJMATCH?redirect=%2Fproducts%2Fmahjong-mats-holiday%3Fvariant%3D67570557354276
- **Cards not in her yeses (these sources):** Candy Cane Lane (Anders Ruff); Classic Very Merry Mahj (Anders Ruff); Holiday Love Red & Green (Bespoke Mahjong); Bam Bird Holiday (Bam Bird Boutique); Holly Jolly Christmas (Bam! Let's Mahjong); Letters to Santa (Mahjong Register); Liberty (Oh My Mahjong); Rackin' Rudolph (Hip Hip Mahjong); Santa's Mahjong Mail (Anders Ruff); Tartan Tidings (Anders Ruff); Very Merry Wreath (Mahjong Register); Winterberry (Oh My Mahjong); Yuletide (Oh My Mahjong); Clara (Oh My Mahjong); Evergreen & Tartan (Anders Ruff); Festive Plaid (Sunday Mahjong); Holly Jolly (Oh My Mahjong); Merrywood (Britt Mills); Ski Club Red Sweater (Charleston Mahjong Club); Tartan Toile Noël (Anders Ruff); The Polo Club (Luxe Mahjong); Very Merry Mahj (Anders Ruff); Watercolor Christmas Tree (Anders Ruff); Red Tartan Scalloped (Lewtemi) (Amazon)
- Note: the same PLM plaid mat appears twice on this page, once as "Peace Love Holiday" and once as "Sugarplum Plaid".

### /osler-mahjong-tile-matches
Holiday cards on page: 16. Yeses in sources: 3. Present: 2. Missing: 1. Cards not in her yeses: 14.

- **Present:** Star of David Hanukkah (Soirée All Day); Peace on Earth (House of Hearts Studio)
- **MISSING:**
  - Miracle (Oh My Mahjong). Source: config/swipe-yeses/holiday-oct21.json books.omm.yes ["miracle","osler"]. URL: retired at OMM, no product page
- **Cards not in her yeses (these sources):** Blue Christmas (Mahj Squad); Holly Jolly (Oh My Mahjong); Snowflake Lodge (Mahjong Register); Alpine Ski Lodge Winter (Splash of Color); Hanukkah (Peace Love Mahjong); Hip Hip Hanukkah (Hip Hip Mahjong); Holiday Love Blue (Bespoke Mahjong); Liberty (Oh My Mahjong); Merriment (Oh My Mahjong); Santa's Mahjong Mail (Anders Ruff); Ski Club Periwinkle (Charleston Mahjong Club); Tartan Toile Noël (Anders Ruff); Winterberry (Oh My Mahjong); Frosted Flowers (Peace Love Mahjong)

### /palm-royale-mahjong-tile-matches
Holiday cards on page: 7. Yeses in sources: 3. Present: 2. Missing: 1. Cards not in her yeses: 5.

- **Present:** Nutcracker Noel - Gold (Peace Love Mahjong); Poinsettia Party (Soirée All Day)
- **MISSING:**
  - Merry Mahjong (Oh My Mahjong). Source: config/swipe-yeses/holiday-oct21.json books.omm.yes ["merry-mahjong","palm-royale"]. URL: retired at OMM, no product page
- **Cards not in her yeses (these sources):** Very Merry Mahj (Anders Ruff); Clara's Dream Christmas (Mahj Squad); Holiday Love Red & Green (Bespoke Mahjong); Sugarplum (Oh My Mahjong); Watercolor Christmas Tree (Anders Ruff)

### /papaya-spritz-mahjong-tile-matches
Holiday cards on page: 1. Yeses in sources: 1. Present: 0. Missing: 1. Cards not in her yeses: 1.

- **Present:** none
- **MISSING:**
  - Spirit of Christmas (Peace Love Mahjong). Source: config/swipe-yeses/holiday-oct21.json books.plmmats.yes ["plm-spirit-of-christmas","papaya-spritz"]. URL: https://peacelovemahjong.com/discount/MAHJMATCH?redirect=%2Fproducts%2Fmahjong-mats-holiday%3Fvariant%3D67570521473316
- **Cards not in her yeses (these sources):** Sweet Marie (Oh My Mahjong, retired)

### /pearlescent-mahjong-tile-matches
Holiday cards on page: 14. Yeses in sources: 4. Present: 3. Missing: 1. Cards not in her yeses: 10.

- **Present:** Candy Cane Lane (Peace Love Mahjong); Perfectly Wrapped (Peace Love Mahjong); Sugarplum Plaid (Peace Love Mahjong) [card title: "Peace Love Holiday"]
- **MISSING:**
  - Merry Mahjong (Oh My Mahjong). Source: config/swipe-yeses/holiday-oct21.json books.omm.yes ["merry-mahjong","pearlescent"]. URL: retired at OMM, no product page
- **Cards not in her yeses (these sources):** Clara's Dream Christmas (Mahj Squad); Sugarplum (Oh My Mahjong); Candy Cane Pink Wonderland (Mahj Squad); Clara (Oh My Mahjong); Holly Berry (Mahj Mood); Holly Jolly Christmas (Bam! Let's Mahjong); Merriment (Oh My Mahjong); Nutcracker (Britt Mills); Very Merry Mahj (Anders Ruff); Very Merry Wreath (Mahjong Register)
- Note: the same PLM plaid mat appears twice on this page, once as "Peace Love Holiday" and once as "Sugarplum Plaid".

### /pippa-mahjong-tile-matches
Holiday cards on page: 3. Yeses in sources: 3. Present: 3. Missing: 0. Cards not in her yeses: 0.

- **Present:** Spirit of Christmas (Peace Love Mahjong); Sugarplum Plaid (Peace Love Mahjong); Santa Baby's Cocktail Hour (Splash of Color)
- **MISSING:** none
- **Cards not in her yeses (these sources):** none

### /preppy-soiree-mahjong-tile-matches
Holiday cards on page: 5. Yeses in sources: 3. Present: 3. Missing: 0. Cards not in her yeses: 2.

- **Present:** Miracle (Oh My Mahjong); Twilight Waltz (Oh My Mahjong); Spirit of Christmas (Peace Love Mahjong)
- **MISSING:** none
- **Cards not in her yeses (these sources):** Blue & White Snowflake (Amazon); Flaming Dreidels (Let's Be Besties)

### /seabreeze-mahjong-tile-matches
Holiday cards on page: 8. Yeses in sources: 0. Present: 0. Missing: 0. Cards not in her yeses: 8.

- **Present:** none
- **MISSING:** none
- **Cards not in her yeses (these sources):** Peace Love Holiday (Peace Love Mahjong); Sugarplum Plaid (Peace Love Mahjong); Candy Cane Pink Wonderland (Mahj Squad); Clara (Oh My Mahjong); Merriment (Oh My Mahjong); Sugarplum (Oh My Mahjong); Very Merry Mahj (Anders Ruff); Winter Jewel (Let's Be Besties)
- Note: the same PLM plaid mat appears twice on this page, once as "Peace Love Holiday" and once as "Sugarplum Plaid".

### /shangri-la-mahjong-tile-matches
Holiday cards on page: 12. Yeses in sources: 7. Present: 7. Missing: 0. Cards not in her yeses: 5.

- **Present:** Twilight Waltz (Oh My Mahjong); Peace Love & Mistletoe (Peace Love Mahjong); Tied With A Bow (Peace Love Mahjong); Vintage Noel (Peace Love Mahjong); Sugarplum Plaid (Peace Love Mahjong); Nutcracker Noel - Red & Green (Peace Love Mahjong); Santa Baby's Cocktail Hour (Splash of Color)
- **MISSING:** none
- **Cards not in her yeses (these sources):** Merriment (Oh My Mahjong); Yuletide (Oh My Mahjong); Winterberry (Oh My Mahjong); Emerald Night Christmas (Let's Be Besties); Plaid Tidings (My Fair Mahjong)

### /sierra-mahjong-tile-matches
Holiday cards on page: 3. Yeses in sources: 1. Present: 1. Missing: 0. Cards not in her yeses: 2.

- **Present:** Spirit of Christmas (Peace Love Mahjong)
- **MISSING:** none
- **Cards not in her yeses (these sources):** Festive Plaid (Sunday Mahjong); Rackin' Rudolph (Hip Hip Mahjong)

### /smith-mahjong-tile-matches
Holiday cards on page: 17. Yeses in sources: 3. Present: 3. Missing: 0. Cards not in her yeses: 14.

- **Present:** Miracle (Oh My Mahjong); Twilight Waltz (Oh My Mahjong); Spirit of Christmas (Peace Love Mahjong)
- **MISSING:** none
- **Cards not in her yeses (these sources):** Hanukkah (Peace Love Mahjong); Liberty (Oh My Mahjong); Merrywood (Britt Mills); Rackin' Rudolph (Hip Hip Mahjong); Snowflake Lodge (Mahjong Register); Tartan Toile Noël (Anders Ruff); Winterberry (Oh My Mahjong); Yuletide (Oh My Mahjong); Hip Hip Hanukkah (Hip Hip Mahjong); Holiday Love Blue (Bespoke Mahjong); Holly Jolly (Oh My Mahjong); Santa's Mahjong Mail (Anders Ruff); Tartan Tidings (Anders Ruff); Frosted Flowers (Peace Love Mahjong)

### /solara-mahjong-tile-matches
Holiday cards on page: 4. Yeses in sources: 0. Present: 0. Missing: 0. Cards not in her yeses: 4.

- **Present:** none
- **MISSING:** none
- **Cards not in her yeses (these sources):** Holly Berry (Mahj Mood); Winter Berry (Britt Mills); Clara's Dream Christmas (Mahj Squad); Holly Jolly (Oh My Mahjong)

### /sorbet-mahjong-tile-matches
Holiday cards on page: 6. Yeses in sources: 3. Present: 2. Missing: 1. Cards not in her yeses: 3.

- **Present:** Sugarplum Plaid (Peace Love Mahjong) [card title: "Peace Love Holiday"]; Santa Baby's Cocktail Hour (Splash of Color)
- **MISSING:**
  - Miracle (Oh My Mahjong). Source: config/swipe-yeses/holiday-oct21.json books.omm.yes ["miracle","sorbet"]. URL: retired at OMM, no product page
- **Cards not in her yeses (these sources):** Clara's Dream Christmas (Mahj Squad); Blue Christmas (Mahj Squad); Clara (Oh My Mahjong)
- Note: the same PLM plaid mat appears twice on this page, once as "Peace Love Holiday" and once as "Sugarplum Plaid".

### /spring-love-mahjong-tile-matches
Holiday cards on page: 4. Yeses in sources: 2. Present: 1. Missing: 1. Cards not in her yeses: 3.

- **Present:** Santa Baby's Cocktail Hour (Splash of Color)
- **MISSING:**
  - Pretty Little Christmas (Peace Love Mahjong). Source: config/swipe-yeses/holiday-oct21.json books.plmmats.yes ["plm-pretty-little-christmas","vault-spring-love"]. URL: https://peacelovemahjong.com/discount/MAHJMATCH?redirect=%2Fproducts%2Fmahjong-mats-holiday%3Fvariant%3D67570521375012
- **Cards not in her yeses (these sources):** Clara (Oh My Mahjong); Sugarplum (Oh My Mahjong); Yuletide (Oh My Mahjong)

### /sunday-tile-set-mahjong-tile-matches
Holiday cards on page: 8. Yeses in sources: 7. Present: 6. Missing: 1. Cards not in her yeses: 2.

- **Present:** Sugarplum Plaid (Peace Love Mahjong); Nutcracker Noel - Gold (Peace Love Mahjong); Peace Love & Mistletoe (Peace Love Mahjong); Poinsettia & Peace (Peace Love Mahjong); Vintage Noel (Peace Love Mahjong); Santa Baby's Cocktail Hour (Splash of Color)
- **MISSING:**
  - Miracle (Oh My Mahjong). Source: config/swipe-yeses/holiday-oct21.json books.omm.yes ["miracle","sunday"]. URL: retired at OMM, no product page
- **Cards not in her yeses (these sources):** Festive Plaid (Sunday Mahjong); Green Scottish Plaid (Amazon)

### /sunset-mahjong-tile-matches
Holiday cards on page: 1. Yeses in sources: 1. Present: 1. Missing: 0. Cards not in her yeses: 0.

- **Present:** Spirit of Christmas (Peace Love Mahjong)
- **MISSING:** none
- **Cards not in her yeses (these sources):** none

### /talulah-mahjong-tile-matches
Holiday cards on page: 11. Yeses in sources: 6. Present: 5. Missing: 1. Cards not in her yeses: 6.

- **Present:** Nutcracker Noel - Gold (Peace Love Mahjong); Tied With A Bow (Peace Love Mahjong); Sugarplum Plaid (Peace Love Mahjong); Peace Love & Mistletoe (Peace Love Mahjong); Perfectly Wrapped (Peace Love Mahjong)
- **MISSING:**
  - Miracle (Oh My Mahjong). Source: config/swipe-yeses/holiday-oct21.json books.omm.yes ["miracle","talulah"]. URL: retired at OMM, no product page
- **Cards not in her yeses (these sources):** Candy Cane Pink Wonderland (Mahj Squad); Sugarplum (Oh My Mahjong); Winter Berry (Britt Mills); Clara's Dream Christmas (Mahj Squad); Merriment (Oh My Mahjong); Pastel Christmas Tree (Mahj & Moon)

### /taylor-mahjong-tile-matches
Holiday cards on page: 5. Yeses in sources: 1. Present: 1. Missing: 0. Cards not in her yeses: 4.

- **Present:** Miracle (Oh My Mahjong)
- **MISSING:** none
- **Cards not in her yeses (these sources):** Nutcracker (Britt Mills); Clara's Dream Christmas (Mahj Squad); Sugarplum (Oh My Mahjong); Very Merry Mahj (Anders Ruff)

### /tortoise-mahjong-tile-matches
Holiday cards on page: 11. Yeses in sources: 7. Present: 7. Missing: 0. Cards not in her yeses: 4.

- **Present:** Twilight Waltz (Oh My Mahjong); Miracle (Oh My Mahjong); Candy Cane Lane (Peace Love Mahjong); Spirit of Christmas (Peace Love Mahjong); Sugarplum Plaid (Peace Love Mahjong); Peace Love & Mistletoe (Peace Love Mahjong); Pretty Little Christmas (Peace Love Mahjong)
- **MISSING:** none
- **Cards not in her yeses (these sources):** Very Merry Mahj (Anders Ruff); Clara (Oh My Mahjong); Sugarplum (Oh My Mahjong); Very Merry Wreath (Mahjong Register)

### /willow-mahjong-tile-matches
Holiday cards on page: 7. Yeses in sources: 0. Present: 0. Missing: 0. Cards not in her yeses: 7.

- **Present:** none
- **MISSING:** none
- **Cards not in her yeses (these sources):** Merrywood (Britt Mills); Winterberry (Oh My Mahjong); Blue Christmas (Mahj Squad); Candy Cane Lane (Anders Ruff); Bam Bird Holiday (Bam Bird Boutique); Holly Berry (Mahj Mood); Very Merry Mahj (Anders Ruff)

## Other things seen (not fixed, for whoever works the fix)

- Duplicate card, same mat under two names ("Peace Love Holiday" + "Sugarplum Plaid", both Peace Love Mahjong) on 11 pages: amara, coquette, dandy, emerald, glitterville, glow-wild, la-fete, nantucket, pearlescent, seabreeze, sorbet.
- Card names to check by eye against the holiday definition (Christmas, Hanukkah, winter snowy/ski only); this audit read names, not photos: Liberty (Oh My Mahjong, retired; 6 cards), Sweet Marie (Oh My Mahjong, retired; 1 card, the only holiday card on Papaya Spritz), Green Scottish Plaid (Amazon; Sunday Tile Set). The Polo Club (Luxe) and Festive Plaid (Sunday) are on the approved works-for-holiday / also-year-round lists.
- Naming drift: "Holly Berry Mat" vs "Holly Berry" (Mahj Mood), "Very Merry Wreath Premium" vs "Very Merry Wreath" (Mahjong Register).
- Sets with holiday yeses but no album and no hidden section anywhere: Cypress Forest, Plum Panda.
