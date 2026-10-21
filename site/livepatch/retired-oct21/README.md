# Retired tile-set labels (Oct 21)

Approval: Tiffany tapped Yes on Ready to Ship `l-retired-tiles2` (Oct 19, 3:46am; `l-retired-tiles` Oct 18 "Good to go"). Plan as approved: grey Retired label at the top of each retired album page and on its covers, shop button swapped. List = `config/tile-retired.json` `recommend: "retired"` (Sunday Mahjong never retired; sold out != retired, doc 90).

Audit Oct 21: 9 album pages already had the header pill (Birdie, Dandy, Glitterville, Limoncello, Lola, Sorbet, Sunset, Taylor + text). Missing: the album index covers (0 "Retired"), the color-page covers, and 5 album headers (Heritage 1.0, Lilac Soiree, Preppy Soiree, Shangri La, Spring Love).

`transforms.js` (same code runs in node for previews and in the Squarespace editor on the CodeMirror doc):
- `coverPills(code)`: adds `<em class="mm-retpill">Retired</em>` inside each retired cover link (`mmalb-c` on /mahjong-tile-matches, `mmcol-card` on color pages) + one `<style id="mm-retpill-css">`.
- `albumHeader(code, slug)`: kicker pill `Retired tile set` (existing `.mm3-ret` style) + the same "X is retired" paragraph as the 9 live pages. Heritage: shop button `products/heritage-tiles` (now sells 2.0) -> "Shop Current Oh My Mahjong Mats", paragraph links the Heritage 2.0 album.

Pages: /mahjong-tile-matches (block-yui_3_17_2_1_1791149521478_3720), /heritage, /lilac-soiree, /preppy-soiree, /shangri-la, /spring-love (-mahjong-tile-matches), color pages pink, blue, green, purple, yellow-orange, brown, neutral, masculine. Homepage NOT touched (another agent was editing it).

before/ = live HTML Oct 21 (rollback reference). after/ = previews. qa/ = screenshots (390 + 1280).
