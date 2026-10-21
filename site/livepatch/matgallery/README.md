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

## v2 (Oct 20): `matgallery-v2.html`, built by `build_v2.py`
Rebuild: `python3 build_v2.py <mat-audit report.csv> <phash pairs.json> > matgallery-v2.html` (rewrites Tiffany's calls from config/tiffany-color-notes/2026-10-20-*.json into config/mat-color-overrides.json, then builds).
- A mat shows in every section it belongs to: primary + Tiffany's `also` colors + Claude's photo cross-tags (config/mat-gallery-crosstags.json: extra Red and peachy-pink -> Orange & Peach). Multicolor = any mat tagged multi. Holiday mats appear in Holiday only.
- Retired mats (incl. the "(retired)"-named album mats) live in a "Retired mats" section at the bottom; "Hide retired" (on by default) keeps them out of the color sections.
- Duplicates collapsed (dedupe_oct20.csv); placeholders / wrong images / no-mat photos hidden (hidden_oct20.csv). Raw store titles cleaned; brand spellings fixed.
- STANDING RULE: Mahjong Studios always sorts to the bottom of every section.

## v3 (Oct 20 late): `matgallery-v3.html`, built by `build_v3.py` (same args as v2)
- New sections: Earthy (muted, low-saturation), Multi-Pastel, Animal Prints (extra tags; color tags kept). Picks in config/mat-gallery-crosstags.json; her calls in config/tiffany-color-notes/2026-10-20-v3-calls.json.
- Within every section: primary-color mats first, "also" mats below, Mahjong Studios last.
- Blue vs Teal & Aqua kept separate; her "blue" calls routed by shade (borderline ones measured: hue ~195 deg is the line).
- Dead links: 6 Mahjong by SI mats (Mahjong Co no longer sells mats; no other store found) show no shop button but are not retired; OMM Cognac retired; Confetti Lemon Lime folded into Confetti – Green.

## v4 (Oct 20 late): `matgallery-v4.html`, built by `build_v4.py` (same args)
- Brown & Tan merged into Earthy. Tonal re-check of every Neutral/Earthy/Dark/B&W mat (crosstags `tonal_fix`, plus `also.dark` for jewel-tone darks).
- Plain Multicolor retired; mood tags Pastels (soft/light, single or multi) and Brights (bold, saturated). Every mat without a Neutral/Earthy/Dark/B&W tag is in one of them. Multicolor Florals kept.
- Holiday = real holiday motifs only; 14 year-round red/green/plaid mats moved to their colors (crosstags `holiday_off`). Jungle mats are Green first (crosstags `jungle`).
- OMM Cognac: not retired; no shop button; "One to watch" badge. Rule: label Retired only when confirmed gone.
- Chip order: colors, Neutral & Ivory, Earthy, Dark & Moody, Black & White, Pastels, Brights, Multicolor Florals, Animal Prints, Holiday, Retired.
- FYM family mapping for the new sections is written up in config/tiffany-color-notes/2026-10-20-v4-calls.json (`fym_family_map`); FYM code not changed.

## v5 (Oct 20 night): `matgallery-v5.html`, built by `build_v5.py` (NOT live; the main session publishes)
- **Late Oct 20 order rule (Tiffany 22:31 + 22:45)**: inside every colour section: her lead mats first (late-calls `lead`), then primaries by measured share of that colour high to low, then ALL secondaries (also + accent merged) by measured share high to low (config/mat-accent-colors.json `shares`; no measurement = 0); Mahjong Studios last within each tier. This replaces the three-tier order below for single sections; multi-select combos keep primary > also > accent.
- **Late Oct 20 removals**: crosstags remove_mats imgs (non-partner brand decisions) + `brands: ["Mahjong Studios"]` (whole brand; also applied to new53 + retired additions). Holiday mats: holiday_off emptied; late-calls holiday calls force Holiday only. Rows are positional: [img, name, brand, url, ret, secs, code, watch, acc, coprimary, hacc, shares].
Rebuild: `python3 ../../../scripts/colors/build_accents.py` then `python3 build_v5.py ../../../builder/fym_fix_oct20/mat_audit_report.csv phash_pairs_oct20.json <image commit> > matgallery-v5.html` (writes v5_counts.json, config/mat-also-claude-v5.json); `python3 build_check_these.py` -> v5_check_these.json.
- Images: jsDelivr base pinned at 5dcf9bd (adds the 53 new + 2 retired webps); all 805 card image URLs warmed, 0 failing.
- **53 new mats** (Tiffany's ShopMy shop: Etsy / Betty June & Jeannette / Sophie Clima, plus Tala Mahj, Mahj & Vine Citrus Grove, CMC Cabana umbrella): rows in new53_rows.json, ShopMy links kept for Etsy rows. Colors from Claude looking at each photo: config/tiffany-color-notes/2026-10-20-new53-claude-tags.json (by claude-photo-review; never a Tiffany call). 42 shown; 10 hidden (text overlay / lifestyle / props on the mat) + 1 duplicate (CMC Cabana umbrella = existing Cabana Club). "Etsy shop (name TBD)" shows as brand "Etsy".
- **Simple** (chip "Simple", between Black & White and Pastels): solids, or a border with a clean plain middle. Replaces Pastels/Brights; color sections kept. crosstags `simple` (Amahj = Tiffany, rest = Claude photo review of every v4 Pastels/Brights mat + the 53).
- **Pastels -> Brights re-check** (soft background + bold saturated graphics reads Brights): crosstags `mood_fix`; her Lucky Charms Watercolor call in the v5 calls file.
- **Tiffany's v5 calls**: config/tiffany-color-notes/2026-10-20-v5-calls.json. `final_sections` win over every crosstag (jungle, primary_fix...), keep mood + tonal tags; `mood_calls`, `accent_calls` (hers replace measured accents), `coprimary` (Darjeeling sorts with Green primaries), `photo_flags`.
- **Three tiers per color section**: primary, then also, then accent-only (Mahjong Studios last within each tier; also-tier sorted by tag position). Accents: config/mat-accent-colors.json (claude-measured, built by scripts/colors/build_accents.py: >=12% of measured area, Teal >=15%, Dark >=20%, Neutral >=45%; tan/cream/jade remapped; B&W never an accent). A color Tiffany removed never comes back as an accent. Holiday mats: measured colors count only in combos.
- **Claude second colors**: for mats she hasn't called, a color covering >=15% becomes an also-color unless it's a neighbouring hue of the primary (config/mat-also-claude-v5.json).
- **Multi-select (AND)**: tap 2+ chips -> one list "Mats with A + B" (all three tiers, primary first), tap again to unselect, "All / Clear" resets, friendly empty message. Retired chip + Hide retired unchanged.
- **Retired additions**: Holy Mahj + Queen Bee (stopgap crops) added; Peri-twinkle + Garden Party unheld. Other retired corrections not applied (wait on Tiffany).
- **Excluded forever**: crosstags `remove_mats` (Amore Mahjong Manor Garden, Tiffany).
- Tested at 390px in Playwright: no console errors, no sideways scroll, every new mat in its sections, combos/unselect/clear OK.
