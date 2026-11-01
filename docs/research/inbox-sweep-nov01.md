# MATCH-INBOX sweep, Nov 1 (overnight, against FYM v110)

Every open line in `docs/MATCH-INBOX.md` was checked against the live v110 data (`const D`) and code, and against the brand stores (`/products/<handle>.json`, read Nov 1). The patch set is in `builder/fym_fix_nov01/`, with the order in its README.

It was tested end to end on a throwaway copy of b110: `gate_nov01.py` PASS and **`fym_gate.py` PASS**. Nothing has been built or published.

**Counts**

| Status | Lines |
|---|---|
| Prepared for v112 | 38 |
| Done / verified in v110 | 7 |
| Needs Tiffany | 8 questions (below) |
| Left open (not prepared) | 4 |

## Line by line

| Inbox line | Status | Files / question |
|---|---|---|
| Oct 31 Shop by colour: partners on top, labelled | prepared | `ui112.py` B, gate [131] |
| Oct 31 LBB Tropicana | prepared | `adds112.py`, `config/fym-adds-nov01.json` |
| Oct 31 MR Crystal Palace rack | prepared (hidden until cut-out) | `config/fym-rack-adds-nov01.json` |
| Oct 31 Sunday Vegan Leather relink | prepared | `fym-adds-nov01.json` relink → Regular Chestnut. Ruby/Forrest = Tiffany Q1 |
| Oct 31 MR Solid Wood racks ×10 | prepared (hidden until cut-outs) | `config/fym-rack-adds-nov01.json` |
| Oct 30 Britt Mills Calista / Colorful Chinoiserie / Daphne / Aria leatherette, Emerald Mirage neoprene | prepared | `adds112.py` (own cards + "Also available in …" on twins) |
| Oct 30 LBB Butterscotch Floral, + Simple Middle, Vibrant Vortex Simple Middle | prepared | `adds112.py` (+ the original Vibrant Vortex as its twin) |
| Oct 30 TdT code next to its name | prepared | `ui112.py` D, gate [133]. Copy has no "%": rule 7 / gate [4] forbids hard-coded % |
| Oct 29 Sunday Green Gingham / Blue Gingham / Blue Rattan | prepared | `adds112.py` |
| Oct 29 Holiday calls (11 mats) | prepared | v110 had 3 PLM mats non-holiday → `fixes112.py` 4 (+ locks), gate [137c]. The wfh group stays in the albums only (FYM wfh is tied to late-calls, gate [13h]) |
| Oct 29 Chinoiserie Cheer flat photo | prepared | `fixes112.py` 5, `config/fym-mat-replace-nov01.json` |
| Oct 29 YOLO sca_ref | done | 64/64 visible YOLO mats carry it |
| Oct 28 / Oct 28 Main: OMM Dapper 2 gone | prepared | `fixes112.py` 1 (404 re-checked). Replacement = Tiffany Q2 |
| Oct 28 MFM Poppy Red rack | prepared (hidden until cut-out) | `config/fym-rack-adds-nov01.json` |
| Oct 27 Britt Mills Bella leatherette | prepared | `adds112.py` |
| Oct 27 partner-sweep questions (Estate Sale, more LBB) | needs Tiffany | Q3, Q4 |
| Oct 27 Spirit of Christmas album cards | open (album work) | Rebuild when the album goes live; not FYM |
| Oct 27 title outlines / white copy (×2) | prepared | v110 drawCard still draws a white copy at +4,+4 → `ui112.py` A, gate [130] |
| Oct 26 Britt Mills / Fait à Main "we better have them all" | prepared | Round Top Mon Amour added HIDDEN + Questionable (close-ups only). Also found Texas Mon Amour Chocolate Blue (Oct 30) → added |
| Oct 26 OMM rack format / TdT racks level / Virora pearl | open | Needs eyes on the rack photos (next QA). Not verified tonight |
| Oct 26 38 angled mat photos | prepared | `build112_data.sh` runs `v98_matflat.py` (21 flat); 14 left on [89] |
| Oct 26 Peppermint Wishes / Plaid Tidings + late holiday mats in albums | needs Tiffany | Q7: her 30 picks never reached the picks page's database |
| Oct 26 Mat Gallery rows (gate [90]) | prepared | Now 274 → `gallery_rows112.py` (run after the FYM build) |
| Oct 26 MFM Jubilee album idea | her pick (already on HQ) | — |
| Oct 26 MRC Scalloped Tortoise for all sets | prepared | `fixes112.py` 2 + `rackfit112.py`, gate [134] |
| Oct 26 rack length by tile size (×2) | prepared | `config/fym-rack-fit-nov01.json`, `rackfit112.py`, `ui112.py` E |
| Oct 26 tortoise order | prepared | `ui112.py` F, gate [135] |
| Oct 26 MRC single racks | done | v98 |
| Oct 26 Bam! white wooden cut-out | open | File exists (`assets/racks/bam-white-wooden-single.png`); wiring not verified |
| Oct 26 PLM chartreuse rack colour | needs Tiffany | Q8 |
| Oct 27 "No code available" (ncn) | prepared | v110 had it on House of Hearts only → `fixes112.py` 7, gate [137d] |
| Oct 27 two-colour coordination bonus | open | Ranking change across every deck; own build + QA |
| Oct 28 Glitter Glow / December 1994 | prepared | `ui112.py` G (Dec 1994 = nutcracker / poinsettia / cardinal tiles), gate [136] |
| Oct 29 Sunday book colour cards | open (swipe book work) | Not FYM |
| Oct 29 TNT recs not in FYM | checked | None live (TdT / OMM retired; "Summer Bloom" is Mahj & Moon, in FYM) |
| Oct 29 TdT Holy Mahj / Queen Bee photos | needs Tiffany | Q6 |
| Oct 29 Mahj & Moon ShopMy | done | 106/114 in v110 |
| Oct 29 v103 QA list | partly | Ivory prepared. Etsy shop names blocked (Etsy refuses the shell → browser chat). Peaches 'n Cream / Empress / step indicator not re-checked |
| Oct 29 brand menu copy | prepared | `ui112.py` C. No conflict: 3:32pm approval is after the 1:57pm pink callout |
| Oct 29 default tile order proposal | her OK pending (HQ) | — |
| Oct 30 Poppins picks | prepared | `fixes112.py` 6 (15 sets; 3 vault; Petalée has no album/book) |
| Oct 30 YMI Ivory merge | prepared | v110 still had 3 "coming soon" sets → `fixes112.py` 3, gate [137b] |
| Oct 30 "(retired)" + MS rack name | done + prepared | `fixes112.py` 8 |
| Oct 30 v106 QA (mfront, Noli) | done | v107 |
| Oct 31 logo breathing room | done | v107 |
| Oct 31 Festive Citrus Chinoiserie | needs Tiffany | Q5 |
| Oct 31 My stars button | v111 accounts build scope | — |

## Needs Tiffany (one line each)

1. Sunday Mahjong now sells full-size vegan leather in Ruby and Forrest too. Should they get their own cards next to Chestnut?
2. Dapper 2 is gone (retired). Which masculine mat should take its "works for the holidays" spot?
3. Tigre de Tartán Estate Sale (red amaryllis, no Christmas graphic): should it also show under Holiday as "works for the holidays"?
4. Let's Be Besties has ~300 more mat designs that aren't in FYM. Bring them in?
5. Mahj & Moon Festive Citrus Chinoiserie is tagged holiday by the store but shows no Christmas graphic. Keep it in Holiday?
6. Holy Mahj + Queen Bee (TdT, retired): can you send the full flat mat images? We only have corner crops.
7. Late holiday mats: please open the Late Holiday Picks page and tap "Send final answers". Your 30 picks never reached its database.
8. Peace Love Mahjong chartreuse rack: which photo shows the true chartreuse? It needs your eye.
