# Mahjong Row & Co.: PARKED (Nov 6, 2026)

Tiffany, Nov 6 1:19pm: "Remove them from the site completely. Remove their Cypress album. Keep it all bookmarked somewhere so it's not lost, but take them out and take them off the partner page completely... park somewhere else so that if we want to turn it back on, we can."

Nothing is deleted. Everything is hidden or unlinked, and this folder holds what is needed to turn it back on.

## What's parked here
- `live-pages/`: the full live HTML of every page that mentioned them on Nov 6 (66 pages + the list in `_pages-with-mentions.txt`), including the brand code page, the Cypress Forest album and the Halloween table blog. Each page's code blocks can be pasted back from these.
- `repo-files.txt`: every repo file about them (album cards, rack cutouts, catalog, swipe books), as of commit 62a310e908ab5fe5f554f33309689cdc6e8b5120. They stay in the repo untouched.
- `fym-hidden.json`: every FYM mat / tile set / rack / set that builder/fym_fix_nov06/mr_out.py hid (flag `parked: mahjong-row-nov06`).
- Their code was 10% with MAHJMATCH (config/code-truth.json `removed_brands` keeps it).

## How it is turned off
1. Squarespace: the brand code page (/mahjong-row-and-co-discount-code) and the album (/cypress-forest-mahjong-tile-matches) are DISABLED (page settings, not deleted) with 302 redirects to /mahjong-discount-codes and /mahjong-tile-matches (302 = temporary, so turning it back on is clean).
2. Every other page: their links, cards, logos, match cards (their mats on other albums) and blog mentions are removed from the code blocks.
3. FYM: hidden with mr_out.py; gate [160] fails if any of it shows. Mat Gallery: crosstags remove_mats.brands.
4. config/fym_held_brands.json keeps catalog refreshes from re-adding them.
5. scripts/checks/live_codes_check.py crawls the whole sitemap and FAILS on any mention (shows at the top of every chat until it is clean).

## How to turn it back on
1. Delete the 2 URL redirects and re-enable the 2 pages in Squarespace.
2. Paste the parked code blocks back from `live-pages/` (or re-add the brand link/card on each page in the list).
3. FYM: set `hid` false on the items in `fym-hidden.json` (or rebuild without mr_out.py), and remove the brand from config/fym_held_brands.json and crosstags remove_mats.brands.
4. Remove `removed_brands` from config/code-truth.json and put "Mahjong Row & Co.": 10 back in `pct`.
