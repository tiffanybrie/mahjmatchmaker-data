# 89 Instagram grid rule: D, one row per tile set (DECIDED Oct 19)
Tiffany picked option D (mockup: assets/social/feed-mockup-D-row-per-set.png).

## The rule
- Every tile set launch adds **exactly 3 grid posts = 1 row**: **album cover | her dating profile | her best match**.
- Instagram shows newest first (top-left), so post in this order: **1. best match → 2. profile → 3. album cover (last)**.
- **What's underneath can be anything** (reel, carousel, mood board). The grid image is set as the post's cover, so the row always looks right.
- **Extra posts for the same set** (teasers, second promos, skits beyond 3) go to Reels/Stories with **"hide from grid"** (Planoly excludeFromGrid). Never a 4th grid post, or every row shifts.
- The existing 6 posts stay as the bottom "archive" rows.
- Non-launch content (Find Your Match launch, holiday, brand news) also goes in groups of 3, or off-grid.

## Who posts
- Planoly auto-posts anything silent or with a free-library track.
- Tiffany posts only reels with a popular song (e.g. Papaya's hotline reel with "This Will Be"), using the album cover as the reel cover.

## Papaya Spritz row (first row under this rule)
1. Best match: "It's a match!" Papaya + Heiress (graphic or mood board underneath). Planoly.
2. Profile: the dating-app profile card (the 7-slide profile carousel underneath). Planoly.
3. Album cover: the hotline reel, posted by Tiffany Wed Oct 21 at 10am CT launch, with the Papaya album cover as its cover.

## Update Oct 19 evening: what each tile in the row IS (Tiffany)
One "It's a match" graphic was too weak a first hello, so every set's row tells a 3-part story: **meet her → her matches → the skit**.
Posted in this order (Instagram puts newest on the left):
1. **Introduction carousel, "Meet <set>"** (posted first, lands on the right). Cover = her dating profile. Slides: profile / color wheel / her colors / her best features (favorite tiles) / racks she's into / made for each other (favorite match) / "Her album is ready · see all N of her matches · link in bio · code". Builder: scripts/social/tileprofile/intro.py.
2. **"It's a match!" carousel** (middle). Cover = the set ♥ her best match. Underneath = a "swipe right" carousel: one top match per slide as a dating-app card (mat, brand, its rack, MATCH stamp), last slide "See all N →".
3. **Album cover = the hotline/skit reel** (posted last, lands on the left), posted by Tiffany at launch with her song. The album cover is set as the reel's grid cover.
Row reads: album cover (reel) | It's a match | her profile.

## Highlight covers (Oct 19)
- Tiffany picked style A (cream background). Good enough, not loved. Parked idea for a future v2: softer pastel color-theory palette.

## Grid catch-up with Meta One (Oct 19 evening)
- Tiffany has Meta One Essential (free month from Oct 19; decide around day 25 before it renews). It gives Instagram "Post only to profile" (grid without followers' feeds) and "Share stories only to highlights."
- Catch-up rows: Tiffany posts them in the IG app with **Post only to profile** ON (Planoly can't set this). Instagram also lets her **reorder the grid** (Tiffany saw it Oct 19), so catch-up rows can be dragged into place after posting. No pinning workaround needed; pins are optional.
- Per-set highlights (Tiffany OK'd the idea, OMM-style): fixed highlights (Find Your Match, Codes, FB group, About) use cream style-A covers. Each tile set gets its own highlight with a cover in its colors, filled via "stories only to highlights." Claude builds a kit per set (cover + about 4 frames).
