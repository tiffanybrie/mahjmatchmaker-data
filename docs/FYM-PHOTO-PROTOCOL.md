# Find Your Mat-ch photo protocol (Tiffany Nov 17, 2026)

Her words: "You guys have to have the protocol to make sure that garbage doesn't get in there, that everything meets the image requirements of Find Your Match." She does not want to track which partner items come and go.

1. Every new partner item's photo is looked at (by eye, not only by script) before it is staged, against FYM rules 6/6b: you can tell it's a mat and you can see its colours.
2. Pulled (flagged in builder/fym_flags/mat_photo_flags.json or tile_photo_flags.json): packaging, watermarks across the mat, personalized/custom samples, ad graphics, fabric close-ups that hide the mat, card-game mats, duplicates, tile sets without tile backs or with tiles too small to see.
3. Room/table shots and brand cards around the mat are cropped to the mat, then looked at again.
4. When in doubt, pull it.
5. All or nothing (rule 0a): photo, colours, price, discount link all ready, or it stays hidden. Non-partners stay locked out unless on nonpartner_allow.json.
6. Each FYM release gets a preview page first (square tiles as the app shows them, pass / crop / pull). She sees it before it ships. 1.23 preview: https://claude.ai/artifact/VxiycRsum7K5sF9tzy72Qk (private review page; never link publicly). Verdicts: builder/fym_flags/fym123_photo_check.json.

1.23 check result (Nov 17): 326 items, 291 pass, 10 cropped, 25 pulled. Most passing mats (nov10/nov16 LBB + Mahjong Register adds) still need a price before rule 0a lets them go live.

## Big-catalog brands and app size (Tiffany Nov 12 + Nov 17)
- Nov 12, her call: keeping the app updating beats onboarding big catalogs; "take 50 of everything". Nov 17: Besties' only value is that a shopper can search an obscure mat by name and find it; beyond that they must not over-suggest or crowd albums, and we can't break the app getting them in.
- So: no more than 50 new items from one brand per release, until she says otherwise. 1.23 is held; the 230 staged Besties wait for her decision.
- Size facts (Nov 17, v122): app page 11.2 MB (plus ~35 MB of thumbnail bundles loaded at start: b*.js ~14.5 MB, thumbs.js 16.0 MB = largest single file, thumbs113/115/118 ~4.1 MB, b23 0.7 MB; ~46 MB total on open), served by jsDelivr, which refuses single GitHub files over 20 MB. Each mat adds ~1.5 KB to the page plus a ~9 KB inline thumbnail (thumbs113: 2.6 MB / 288) unless thumbs are made lighter, plus an image in the data repo (repo already past jsDelivr's package limit, so some new files need the raw.githubusercontent fallback). The old in-chat copy is stuck at 1.18 on its 512-file / 256 MB cap.
- Besties now: 322 visible of 1,789 mats. Raw colour ranking puts ~8 Besties in a tile set's top 30 (up to 19); BCAP trims to 6, and 209 of 336 sets hit the cap. Albums: 55 of 1,921 matches, in 21 of 49 albums.
