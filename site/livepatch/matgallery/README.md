# Mat Gallery: /mahjong-mats (draft, Oct 19)
Every mat in the Find Your Match catalog (889 shown; hidden and photo-coming-soon mats left out), product photos only, grouped by color, with color chips and a brand filter. Retired mats show a grey "Retired" pill and no shop link. Same look as the live Christmas mat gallery (/christmas-mahjong-mats).
- **Block:** `matgallery.html` (code block; renders cards from inline JSON). Rebuild: `python3 build.py <D.json> manifest.json <commit>`; D.json is `const D` from the FYM build index.html.
- **Images:** `assets/mats/gallery/<brand>--<mat>.webp` (640px) at commit 3e8af50; all 889 jsDelivr URLs warmed, 0 failing.
- **Colors (Oct 19, reviewed):** each mat's MAIN color from scripts/colors/matcolors.py: Tiffany's Mat Color Tagger taps (config/mat-color-overrides.json) win, then Claude's look at every photo (config/mat-color-guesses.json, with conf high/medium/low and the old computer read in `prev`). Sections: Pink, Red, Orange & Peach, Yellow & Mustard (gold sits here), Green, Teal & Aqua, Blue, Purple & Lilac, Brown & Tan, Neutral & Ivory, Black & White, Dark & Moody, Multicolor, Holiday (holiday flag wins). **Do not put live until Tiffany has checked the low+medium list in the Tagger (Check these tab) and said yes in Ready to Ship (item l-matgallery-colors).** After her check: pull taps with apply_matcolors.py, then rebuild with build.py.
- **Color check (Tagger v5):** https://claude.ai/artifact/RoHrY1LHAj8bgZx2aL4bLW
- **Page:** slug `/mahjong-mats`, title "Mahjong Mats by Color".
  - SEO title: "Mahjong Mats by Color: Shop 800+ Mats From 40+ Brands | Mahj Matchmaker"
  - SEO description: "Browse every mahjong mat in my matching library by color and brand: pink, blue, green, neutral, holiday and more. Tap any mat to shop it."
  - Add it to the main menu (her approval covers this).
- **Note:** the intro links to /mahjong-tile-matches and mentions Find Your Match "coming 10.27"; swap in a link to Find Your Match once it's live.
