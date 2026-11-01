# Holiday Nov 2 launch: canonical counts (checked Nov 1 2026, ~1:40am ET)

Every holiday piece (reels, carousels, story frames, captions, HQ cards) uses only these numbers. They are deliberately rounded DOWN so they stay true while stock changes. Never "every"/"all", never 404.

| Say this | Exact today | Source |
|---|---|---|
| **400+ holiday matches** | 488 in-stock holiday tile + mat pairs in FYM; 404 match cards on the live holiday page | FYM v111 `const D` (`sets[].m` pairs whose mat is `hol`, visible, not sold out / gone). Live /holiday-mahjong-matches: 109 cards on the page + 295 in the 34 linked albums = 404 (the page's own stat says "400+") |
| **140+ holiday mats** | 144 | FYM v111 (live on /find-your-match, pinned `site-app/fym-v111` @0c0da351): 152 visible `hol` mats, minus OMM Sugarplum (gone: 404 + not in products.json) and 7 sold out tonight (Britt Mills Merrywood / Nutcracker / Winter Berry neoprene, Virora Hiverelle, Mahj Mood Sleigh All Day, Mahj Squad Candy Cane Pink Wonderland, OMM Sweet Marie retired). 55 are non-Shopify (Etsy, Piper Chase, BJ&J, Soirée, Mahj & Moon, Wren, Tala, House of Hearts) and count as in stock. Double-sided mats count per side (each side is its own card in the app); de-duplicated by product it is 139, so "140+" is only true counting designs. |
| **40+ holiday albums** | 45 | Live /holiday-mahjong-matches: 11 new holiday tile set sections + 34 existing albums with a holiday section (49 incl. 4 small extra sections) |
| **10+ holiday tile sets** | 11 on the page, 13 in FYM | Live page "new holiday tile sets" grid (Dear Santa, Rackin' Rudolph, Holly Jolly x3, Tinselle x2, Nivalee, Nutcracker Ballet, December 1994, Après Ski Club); FYM v111 `BACKG.Holiday` minus hidden (Christmas Kiss, Nativity) and Glitter Glow (no set). In stock: 11 (Tinselle Ruby Red and PLM Spirit of Christmas sold out) |
| **30+ albums with a holiday section** (vault carousel slide 9 only) | 34 | Live page "Holiday matches for the tiles you already own" |

Per-piece sub-counts that stay as they are (per-set facts from FYM v111, re-checked Nov 1): Dear Santa 27 matches; Anders Ruff 8 Christmas mats matched 93 times with 35 tile sets; Tinselle (Emerald Green) 23 matches; Holly Jolly 21 + 4 + 19 = 44 matches; vault album slides use each album's own count on the live page (Dear Santa 19, Rackin' Rudolph 22, Holly Jolly 26, Nutcracker Ballet 12, Nivalee 7, Après Ski Club 9).

Retired numbers (do not use): 152, 156, 150+, 13, 45, 42, 49, 34, 11, "40 Christmas & winter mats".

Known mismatch outside the reels: the live /holiday-mahjong-matches stat strip still says "42 holiday mats · 49 tile sets · 17 brands" (album-curated counts). The vault reel spotlights only its "400+" box. Handoff to Ops on DESK to change the strip to the forms above.

Stock method: `/products/<handle>.js` `available` per Shopify store, falling back to `/products.json` (OMM blocks `.js`); script and full table: /dev/shm only (re-run `scripts/fym_stock_check.py` for the repo copy). Recheck Monday morning.
