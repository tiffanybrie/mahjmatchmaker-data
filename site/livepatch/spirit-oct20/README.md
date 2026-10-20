# Spirit of Christmas (Peace Love Mahjong) holiday cards, staged Oct 20 (NOT live)

**Source:** Ready to Ship `c5-spirit` (Oct 18, 1:12pm, "chg"). It saved her **order** for the 10 cards. Her note says "Already sent this", which means her actual feedback went into chat, and **that text is not in any saved record available to this build** (RTS answers, RTS item text, Needs list, repo). The feedback itself is not applied. Paste the chat note (or point to where it's saved) and the cards can be redone the same day.

## What's staged
- **10 cards** in `assets/cards/spirit-of-christmas-oct20/`, commit `7a6706c`, renumbered in her order:
  01 Spirit of Christmas, 02 Vintage Noel, 03 Merry Mix, 04 Pretty Little Christmas, 05 Merry & Striped, 06 Tied With A Bow, 07 Peace Love & Mistletoe, 08 Poinsettia & Peace, 09 Nutcracker Noel Red & Green, 10 Nutcracker Noel Gold.
- **Only rule-based changes:** the mat photos are trimmed of their white product-photo background so the mat fills more of the card. Some photos have a soft grey shadow edge, and a thin frame still shows on a few. Each mat keeps its Oct 17 racks (MATCH THE MAT). The footer is 10% OFF · MAHJMATCH, and the PLM logo stays.
- **Still missing tile racks** (lower left). Spirit of Christmas has no approved tile-rack list, and that decision is open with her (triage B21).
- Build: `scripts/albumcard/oct20/spirit_build.py`, then `gen2.py`.

## Live step
None until she sends or confirms her feedback and picks the tile racks. After that the cards go on /holiday-mahjong-matches, in a Spirit of Christmas section (add one if the page has none), using the same per-card swap pattern as `site/livepatch/codefooter/holiday-mahjong-matches.json`. Warm the jsDelivr URLs first (doc 73).
