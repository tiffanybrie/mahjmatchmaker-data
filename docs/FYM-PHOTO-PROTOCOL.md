# Find Your Mat-ch photo protocol (Tiffany Nov 17, 2026)

Her words: "You guys have to have the protocol to make sure that garbage doesn't get in there, that everything meets the image requirements of Find Your Match." She does not want to track which partner items come and go.

1. Every new partner item's photo is looked at (by eye, not only by script) before it is staged, against FYM rules 6/6b: you can tell it's a mat and you can see its colours.
2. Pulled (flagged in builder/fym_flags/mat_photo_flags.json or tile_photo_flags.json): packaging, watermarks across the mat, personalized/custom samples, ad graphics, fabric close-ups that hide the mat, card-game mats, duplicates, tile sets without tile backs or with tiles too small to see.
3. Room/table shots and brand cards around the mat are cropped to the mat, then looked at again.
4. When in doubt, pull it.
5. All or nothing (rule 0a): photo, colours, price, discount link all ready, or it stays hidden. Non-partners stay locked out unless on nonpartner_allow.json.
6. Each FYM release gets a preview page first (square tiles as the app shows them, pass / crop / pull). She sees it before it ships. 1.23 preview: https://claude.ai/artifact/VxiycRsum7K5sF9tzy72Qk (private review page; never link publicly). Verdicts: builder/fym_flags/fym123_photo_check.json.

1.23 check result (Nov 17): 326 items, 291 pass, 10 cropped, 25 pulled. Most passing mats (nov10/nov16 LBB + Mahjong Register adds) still need a price before rule 0a lets them go live.
