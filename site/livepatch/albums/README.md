# Final album pages, ready to go live (Oct 18)

**Approval:** Tiffany approved each of these albums in Ready to Ship on Oct 18 (12:21–12:31pm). Lilac, Preppy and Spring Love were approved with changes, all now made; Shangri La was a plain Yes. Her standing rule (doc 74) is that a Yes in Ready to Ship counts as approval.

**What changed in every album:** the cards are re-rendered with the current generator. The OMM flag now sits in the approved spot beside the navy logo box, matching Amara and Malachite. Footers read 10% OFF USE CODE : MAHJMATCH, cards follow her saved drag order and the right fonts are used. Cards live in `assets/cards/from-the-vault/<set>-v3/` (built by `scripts/albumcard/specs/vault_oct18/rebuild.py`). Code blocks are pinned to commit `eda38ca` and built by `build_vault.py`. All 59 jsDelivr URLs are warmed, 0 failing.

**Per-album changes:**
- **Lilac Soiree:** Larkspur cancelled.
- **Preppy Soiree:** Larkspur and Cognac cancelled.
- **Spring Love:** Goldie now uses her bright clean photo (`assets/mats/clean/goldie-omm.png`).
- **Shangri La:** no changes.

## How to make each page
1. **Duplicate a live album page** with the current layout, e.g. /pearlescent-mahjong-tile-matches: page gear → Duplicate Page → Confirm. It goes live right away as "(Copy)", so do steps 2 and 3 at once.
2. **Set the page settings** with the API (doc 59 §4): title, slug, SEO title and SEO description from the table below.
3. **Replace the album code block** with the file from this folder, fetched at the commit this README is in (raw.githubusercontent works if jsDelivr refuses the html).
4. **Verify with curl:** the h1, the number of `mm3-c` figures, and that the cover loads.

| Page | Title | SEO title | SEO description | Block | Cards |
|---|---|---|---|---|---|
| /lilac-soiree-mahjong-tile-matches | Lilac Soiree Mahjong Tile Matches | Lilac Soiree Mahjong Tile Matches: Mats & Racks for Oh My Mahjong Lilac Soiree | Oh My Mahjong Lilac Soiree tiles (from the vault) matched to 9 mats, with rack picks and shop links. Top picks: Chantilly, Jade and Astor. Save with code MAHJMATCH. | `lilac-soiree.html` | 9 |
| /preppy-soiree-mahjong-tile-matches | Preppy Soiree Mahjong Tile Matches | Preppy Soiree Mahjong Tile Matches: Mats & Racks for Oh My Mahjong Preppy Soiree | Oh My Mahjong Preppy Soiree tiles (from the vault) matched to 13 mats, with rack picks and shop links. Top picks: Chantilly, Jade and Hawthorne. Save with code MAHJMATCH. | `preppy-soiree.html` | 14 |
| /shangri-la-mahjong-tile-matches | Shangri La Mahjong Tile Matches | Shangri La Mahjong Tile Matches: Mats & Racks for Oh My Mahjong Shangri La | Oh My Mahjong Shangri La tiles (from the vault) matched to 12 mats, with rack picks and shop links. Top picks: Jade, Camellia and Esme. Save with code MAHJMATCH. | `shangri-la.html` | 15 |
| /spring-love-mahjong-tile-matches | Spring Love Mahjong Tile Matches | Spring Love Mahjong Tile Matches: Mats & Racks for Oh My Mahjong Spring Love | Oh My Mahjong Spring Love tiles (from the vault) matched to 14 mats, with rack picks and shop links. Top picks: Zen Glow, Vivienne and Goldie. Save with code MAHJMATCH. | `spring-love.html` | 17 |

## Covers on /mahjong-tile-matches (grouped color block) and the color pages
There's no "From the Vault" section on the live site today (checked Oct 18), so each vault album goes into its color section like any other album.

**Proposed colors**, read from each set's tile backs. None of the four has a tag in `config/tile-back-colors.json` yet:
- **Lilac Soiree:** Purple
- **Preppy Soiree:** Blue
- **Shangri La:** Green
- **Spring Love:** Pink

Add this card at the end of that color's `mmalb-g` grid, both in the grouped block (block-yui_3_17_2_1_1791149521478_3720 on /mahjong-tile-matches, and the home page insert) and in the grid on the matching color page (e.g. /purple-mahjong-tile-matches):
- Lilac Soiree: `<a class="mmalb-c" href="/lilac-soiree-mahjong-tile-matches"><img src="https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@243ba72099cbaa2f455ba5502e37bd3a69f03862/assets/covers/albums/w800/00-lilac-soiree-mahjong-tiles-cover.jpg" alt="Oh My Mahjong Lilac Soiree mahjong tile matches" loading="lazy"><span><small>Oh My Mahjong</small>Lilac Soiree</span></a>`
- Preppy Soiree: `<a class="mmalb-c" href="/preppy-soiree-mahjong-tile-matches"><img src="https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@243ba72099cbaa2f455ba5502e37bd3a69f03862/assets/covers/albums/w800/00-preppy-soiree-mahjong-tiles-cover.jpg" alt="Oh My Mahjong Preppy Soiree mahjong tile matches" loading="lazy"><span><small>Oh My Mahjong</small>Preppy Soiree</span></a>`
- Shangri La: `<a class="mmalb-c" href="/shangri-la-mahjong-tile-matches"><img src="https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@243ba72099cbaa2f455ba5502e37bd3a69f03862/assets/covers/albums/w800/00-shangri-la-mahjong-tiles-cover.jpg" alt="Oh My Mahjong Shangri La mahjong tile matches" loading="lazy"><span><small>Oh My Mahjong</small>Shangri La</span></a>`
- Spring Love: `<a class="mmalb-c" href="/spring-love-mahjong-tile-matches"><img src="https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@243ba72099cbaa2f455ba5502e37bd3a69f03862/assets/covers/albums/w800/00-spring-love-mahjong-tiles-cover.jpg" alt="Oh My Mahjong Spring Love mahjong tile matches" loading="lazy"><span><small>Oh My Mahjong</small>Spring Love</span></a>`

## Papaya Spritz
Staged separately in `../papaya/` (README there). Its page steps and color-section variants are ready.

## Notes for Tiffany
- **Spring Love:** she suspects missing matches, since there are only 14 non-holiday ones. Not addressed here; it needs a missed-mats swipe round.
- **Spring Love tile photo:** only about 210px at the source, upscaled. It needs a bigger photo.

## Sunday Tile Set (approved; staged Oct 18 afternoon)
- **Code block:** `site/livepatch/albums/sunday-tile-set.html`. 35 cards in her saved Ready to Ship order (c5-sunday, 11:32am). Fall Flowers is removed (l-sunday-final, Yes 12:05pm).
- **Cards:** `assets/cards/sunday-tile-set-v4/` at commit a908626. These are the v3 cards with the "SAVE WITH CODE : MAHJMATCH" footer; the logo placement is unchanged, per her.
- **Captions:** brands with no code show a "No code for <brand>" chip. Those are Sunday Mahjong, Ozark Mahjongg, Mahjong by SI, Luxe Mahjong, Lucky Daughters and Mahj Tile Haus. The FAQ top picks were updated (Carson Vintage, Brownstone Bloom, Autumn Saffron).
- **Warmed:** all 36 URLs, 0 failing. Rendered at 390 and 1280 with no sideways scroll.
- **Page:** slug `/sunday-tile-set-mahjong-tile-matches`.
  - Title: "Sunday Tile Set Mahjong Tile Matches | Sunday Mahjong"
  - SEO title: "Sunday Mahjong Sunday Tile Set: 35 Mat & Rack Matches"
  - SEO description: "35 mahjong mats and racks that match the Sunday Mahjong Sunday Tile Set, picked by Tiffany at Mahj Matchmaker."
  - Duplicate the newest album page and swap its code block.
- **Cover:** `assets/cards/sunday-tile-set/00-sunday-tile-set-mahjong-tiles-cover.jpg` at e34138f, or the w800 cover in assets/covers/albums if present.
- **Yellow & Orange color section:** add an `mmalb-c` card. The second `<a>` below is the cover link and goes at the end of the Yellow & Orange grid in the color blocks:
  `<a class="mmalb-c" href="/sunday-tile-set-mahjong-tile-matches"><img src="https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@e34138fda6c04c9c524983f81e828305eb54531a/assets/cards/sunday-tile-set/00-sunday-tile-set-mahjong-tiles-cover.jpg" alt="Sunday Mahjong Sunday Tile Set mahjong tile matches" loading="lazy"><span><small>Sunday Mahjong</small>Sunday Tile Set</span></a>`
- **Open question:** she said she "took out another one" besides Fall Flowers. Her saved order still has all 36, so only Fall Flowers is removed. Ask her which other mat.
