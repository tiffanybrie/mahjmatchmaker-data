# Mahjong Row & Co. OUT of the site (Tiffany Nov 6 1:19pm + 1:33pm scope). Approved: do it, no more asks.
Parked copy: archive/mahjong-row-parked-2026-11-06 (live HTML of every page, how to turn it back on).
Done = `python3 scripts/checks/live_codes_check.py` PASS (it crawls the sitemap; config/code-truth.json removed_brands).

## STAYS (her call): her album match cards of their mats (Amara, Gatsby, Heritage 2.0, Smith, Osler, Willow, Sunday, Brownstone Bloom),
## the Halloween table blog, and their 9 Mat Gallery mats (all are her album matches) with NO code claim.
On those pages only: re-point any link to /mahjong-row-and-co-discount-code or /cypress-forest-mahjong-tile-matches to the product page
on mahjongrowandco.com (no code text).

## Squarespace (Chrome), in this order
1. HIDE, never delete: /mahjong-row-and-co-discount-code and /cypress-forest-mahjong-tile-matches -> page settings: disable
   (or Not linked + password-free "disabled"). Settings > Developer > URL mappings, add (302 = temporary, easy to undo):
   /mahjong-row-and-co-discount-code -> /mahjong-discount-codes 302
   /cypress-forest-mahjong-tile-matches -> /mahjong-tile-matches 302
2. Hub /mahjong-discount-codes: remove their row/card + any FAQ/text mention.
3. Home: logo strip (a.b27 + its .dup copy), brand card (mmb-c), Cypress Forest album card (mmh-alb). Blog teaser for the Halloween post may stay.
4. "More brands I love" list on all 38 code pages (one <a> each) + the Mahjong Co. page sentence "...and from Mahjong Row & Co." and its footer link.
5. Album index /mahjong-tile-matches (Cypress card x3 sections), colour pages /brown-, /neutral-, /masculine-mahjong-tile-matches (Cypress card;
   masculine: promote another set there), /holiday-mahjong-matches + /bird-and-bamboo-rack-colors + /charleston + /britt-mills code pages (Cypress mentions).
6. /links: Cypress Forest album card.  7. /request-an-album: the mention.  8. /mahjong-mats: brand filter option + no code claim on their 9 rows.
9. Blogs: /blog/best-mahjong-sets-for-men, /blog/most-versatile-mahjong-tiles, /blog/most-versatile-mahjong-mats: take out their section/picks
   (swap in a partner where a list needs a number); /blog/mahjong-tile-set-details-to-know: drop the brand name from the sentence; /blog index teaser.
10. Facebook GROUP: featured codes post first comment (typed list) -> delete their line; group About/guides if listed.
FYM: builder/fym_fix_nov06/mr_out.py on the next build (gate [160] enforces); publish both copies.

## Home page order (Tiffany Nov 6 1:36pm, same paste as step 3)
In the #mmhome code block (block-yui_3_17_2_1_1791134152790_5194, see site/livepatch/home-oct21/README.md) move the Holiday Mahjong Matches
section to right under the hero/Find Your Mat-ch (above the MAHJMATCH callout and New Tile Match Albums), then New Tile Match Albums,
then From the Blog, then Shop by Color / Shop by Brand. Holiday section: add a line with how many partner brands are in the holiday sets
(count from /holiday-mahjong-matches) to showcase the brands. Edit in CodeMirror (move the <section> nodes), Save, verify at 390 + 1440.
