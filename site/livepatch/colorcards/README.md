Color cards for the albums that were missing them (Oct 19). NOT live.
One snippet per album page. Insert it right before `<section><h2>My <Name> matches</h2>` (after the FAQ ld+json script), the same spot Amara/Willow have `<section class="mm3-guides">`.
Images are jsDelivr pinned to the commit in index.json and were warmed (warm_result_colorcards.json).
Papaya Spritz is skipped: its card is waiting on the new profile line. When that style is approved, add `profile_line` to each set in config/colorcards.json, re-run `python3 scripts/colorcards/build.py <key>`, commit, and re-pin these snippets to the new commit.
