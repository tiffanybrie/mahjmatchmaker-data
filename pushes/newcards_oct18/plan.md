# Live swap plan: new album cards, Oct 18 (main session only)

FINAL (Tiffany, 00:40): 28 approved, 12 of them TOP matches.
Removed: Solara + Preppy Pink Garden, Jasmine + Rainbow Row, Pippa + Pink Floral Chinoiserie. Jasmine gets no new cards.
Still waiting on her review (not in this plan yet): Papaya Spritz + Preppy Pink Garden; Pearlescent + Rainbow Row, Pink Floral Chinoiserie, Secret Garden (commit 8f0c09a).
Card image URLs are pinned to commit 5a2c009.

Files: `live/<set>.top.html` holds that page's TOP cards, already in order. `live/<set>.html` holds its regular cards. The lists are also in `final_lists.json` and `top.json`.

## Placement
- TOP cards go in the top-match section near the front of the "Every <Set> match" grid. Pages have no top tag; her albums lead with her top 5 ("My top picks come first"). So insert TOP cards right after card 05, unless the page clearly shows a different top block (a take saying "top pick" past 05: go after that one).
- **Seabreeze + Rainbow Row goes FIRST on Seabreeze (new card 01)**, before her existing top picks. She called it "possibly its best match I've seen".
- Regular cards go at the end of the main grid, right after the anchor card's `</figure>` (the last card before the holiday section).
- Then renumber every `mm3-n` in the block in order (01, 02, …) with a JS pass over the CM6 doc text.

## Method (same as the holiday logo fix)
1. `__go('/<set>-mahjong-tile-matches')`
2. double_click (360,175)
3. Insert through the CM6 dispatch, then renumber.
4. Escape, Save, Exit, Save.
5. Verify with curl: the new image URLs are present, the card count went up by the right number, and the title and holiday section are intact.

| page | code block | main cards now | TOP (in order) | regular: insert after | regular cards |
|---|---|---|---|---|---|
| /amara-mahjong-tile-matches | block-yui_3_17_2_1_1791139920995_3786 | 30 | Rally in Pink, Palm Court, Rainbow Row | Amara + KY Derby | Posy Pop Watercolor |
| /dandy-mahjong-tile-matches | block-bb3c7eb94a98ffc34df5 | 17 | Pink Floral Chinoiserie | Dandy + Camellia | Posy Pop Watercolor, Preppy Pink Garden |
| /gemma-mahjong-tile-matches | block-2a1159fb3efe958b0dc7 | 11 | – | Gemma + Mirage | Preppy Pink Garden |
| /jade-mahjong-tile-matches | block-yui_3_17_2_1_1791056111953_4057 | 37 | Secret Garden | Jade + KY Derby | – |
| /la-fete-mahjong-tile-matches | block-d7182860a5846d83e0d3 | 14 | – | La Fete + KY Derby | Pink Floral Chinoiserie, Posy Pop Watercolor, Rainbow Row, Secret Garden |
| /limoncello-mahjong-tile-matches | block-338ca23c325e0dfc291f | 10 | Rainbow Row | Limoncello + Serengeti | Secret Garden |
| /luminaire-mahjong-tile-matches | block-b0414b987e089d56a474 | 13 | Secret Garden | Luminaire + Camellia | – |
| /moonlight-mahjong-tile-matches | block-3324ec522fc28d2aeda7 | 23 | Cottage Bloom | Moonlight + KY Derby | – |
| /pearlescent-mahjong-tile-matches | block-yui_3_17_2_1_1791140193799_3782 | 21 | Rally in Pink | Pearlescent + Regal Bloom | – |
| /pippa-mahjong-tile-matches | block-8e8777a5f38ef6a1e805 | 17 | – | Pippa + Spring Fling | Posy Pop Watercolor, Secret Garden |
| /seabreeze-mahjong-tile-matches | block-599192ab173b19805adb | 21 | Rainbow Row | Seabreeze + Sweet Dreams | Pink Floral Chinoiserie, Posy Pop Watercolor |
| /solara-mahjong-tile-matches | block-0f03ccbc2ae47110664e | 35 | Chinoiserie Elephant | Solara + Imperial | – |
| /sorbet-mahjong-tile-matches | block-87733dd2d43f1f49e208 | 8 | – | Sorbet + Capri | Posy Pop Watercolor, Preppy Pink Garden, Rainbow Row |
| /taylor-mahjong-tile-matches | block-24646adc2b61a5241fac | 11 | Secret Garden | Taylor + Peri-Twinkle | – |

## Notes
- Pearlescent + Rally in Pink caption now uses her words: "that sandy color running through it, plus the pinks and the peaches".
- Shop links carry our refs: Mahj Mood ?ref=Mahjmatchmaker; Mahj & Vine, Bespoke and Mahj Squad use sca_ref. Bam! links are plain, the same as the live Bam! cards.
- Rebecca Illustrated: no brand page and no code ("Note that we do not have a code for this brand.").
- Pink Floral Chinoiserie (Mahj Squad) is watermarked: album only, never social.
- Hampton was NOT added: Limoncello and Sorbet already have live Hampton cards.
- After going live: update work/albums.json and the FYM album matches, then mark the HQ need review-new-cards-oct18 done.

## Added 00:48: Pearlescent extras (approved)
- `live/pearlescent2.top.html`: Pearlescent + Rainbow Row (TOP) and Pearlescent + Pink Floral Chinoiserie (TOP). Insert them with Pearlescent + Rally in Pink in Pearlescent's top section: Rally in Pink first, then these two.
- `live/pearlescent2.html`: Pearlescent + Secret Garden (regular), at the end of the grid after Pearlescent + Regal Bloom.
- These images are pinned to commit 8f0c09a. Pearlescent now gets 3 TOP + 1 regular, so the totals are 31 approved and 14 TOP.
- Papaya Spritz + Preppy Pink Garden goes on the Papaya album, which isn't built yet. It's in Papaya's TOP 3.
