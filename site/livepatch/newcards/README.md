# The 32 approved Oct 18 cards (Ready to Ship: "28 approved · 12 top matches" + "4 more cards", Yes at 13:11)

Checked against the live pages on Oct 18 at about 2:55pm:
- **Already live (28):** Amara 4, Dandy 3, Gemma 1, Jade 1, La Fête 4, Limoncello 2, Luminaire 1, Moonlight 1, Pippa 2, Seabreeze 3, Solara 1, Sorbet 3, Taylor 1, Pearlescent 1 (Rally in Pink). TOP cards sit at #6, and Seabreeze + Rainbow Row is #1 as she asked. Removed cards are not on the site: Solara + Preppy Pink Garden, Jasmine + Rainbow Row, Pippa + Pink Floral Chinoiserie.
- **Papaya + Preppy Pink Garden:** in the Papaya album, which is staged in site/livepatch/papaya/.
- **Still missing (3, all Pearlescent):**
  - Rainbow Row (TOP, #7)
  - Pink Floral Chinoiserie (TOP, #8)
  - Secret Garden (regular, end of the main grid, #25)

## To apply on /pearlescent-mahjong-tile-matches
1. Open the main code block (the one containing "Every Pearlescent match").
2. Load `pearlescent_fix.js` and the two snippets `pearlescent-top.html` and `pearlescent-end.html`. Fetch them raw from GitHub at the commit below.
3. Run `pearlFix(src, TOP, END)`. It inserts the cards, renumbers the main grid (the holiday grid is untouched) and updates "all 25 Pearlescent mat matches from 6 brands". It's idempotent.
4. Save, then curl-verify.

All image URLs are warmed with 0 failing. Racks in the captions match each card's spec (scripts/albumcard/specs/new_oct18/extra/*.json). Rainbow Row uses the code-footer version of the card, with "no code for this brand" in the caption.
