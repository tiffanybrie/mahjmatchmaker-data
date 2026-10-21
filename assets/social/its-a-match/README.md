# "It's a match!" post: the middle post of every set's launch row

Every tile set's Instagram launch row has 3 grid posts (doc 89): **profile carousel, then It's a match, then the reel**. This is the standard template for the middle post. It is not a standalone series (Tiffany, Oct 21).

Each set gets two images:
- **Feed post** (1080x1350). Content stays inside y 120-1230, so the 3:4 grid crop keeps everything.
- **Story version** (1080x1920) that the mat brand can reshare. Key content stays inside the safe zone: the top 14% (269px) and bottom 20% (384px) are kept clear.

Why it works: Britt Mills reshared the Papaya + Heiress card within hours on Oct 21. Tiffany: "highly shareable for those secondary mat brands... very easy content for them to reshare."

## Layout (navy and pink, never brown)
"It's a match!" in pink Caveat script, then the tile circle, a heart and the mat square. Below those:
- "Set ♥ Mat" in navy Lora
- "TILE BRAND · MAT BRAND" in pink caps
- a navy pill: "All N of her/his matches are live"
- the wordmark (2x the original Papaya card)
- the tagline "Hooking up tiles, mats & racks"
- **@mahjmatchmaker** in navy, so people who see a brand's reshare and can't tap through can still find us

The tile and mat images are the largest elements on both sizes.

**Headline pending Tiffany's pick (Oct 21):** A = "It's a mat-ch!" or B = "It's a match!" (`--variant`, default B). Samples: `samples/papaya-A-*.jpg`, `samples/papaya-B-*.jpg`, `samples/papaya-A-vs-B-compare.jpg`. For A we use Caveat's own hyphen, spaced slightly off the t's crossbar. Unspaced, it touches the t. A drawn bar looked pasted on.

## Build one
```
python3 scripts/social/its_a_match/render.py --tile "Papaya Spritz" --mat Heiress \
  --tile-brand "Oh My Mahjong" --mat-brand "Britt Mills" \
  --tile-img assets/tiles/album/papaya-spritz.jpg \
  --mat-img assets/colorcards/papaya-spritz/mats/heiress-britt-mills.jpg \
  --count 50 --pron her --variant B --out assets/social/<set>-launch/grid/<set>-grid-2-its-a-match-<mat>
```
This writes `<out>-feed.jpg` and `<out>-story.jpg`. The script prints `OVERFLOW` if any content falls outside the safe band. If you see that, shorten the text or check the names.

Rules for the inputs:
- **Pair:** only her real picks. Use the top of the live album order (or her swipe-book stars). Skip official pairs (same brand as the tiles). The point is to spotlight another brand's mat. That brand must be a partner, or allowed per CLAUDE.md. No Mahjong Studios, The Mahjong Line, Mahj House Rules, Four Winds Social (except the Mahj Mood collabs) or Amore. No Paige Spearin x TdT. Prefer brands with a verified handle in `config/social/ig-handles.json`.
- **Tile photo:** the canonical album photo, `assets/tiles/album/<set>.*`. Tortoise = `classic-tortoise-zoom.jpg`.
- **Mat photo:** the mat-only card image. Use `assets/colorcards/<set>/mats/` if it exists. Otherwise use the FYM photo for that mat: the `f` path in reference-picks.json, read from the live FYM artifact's published files.
- **Count:** the number of cards on the live album page. Never round it.
- **Pronoun:** "his" for Malachite, Heritage, Heritage 2.0, Smith, Cypress, Gatsby and Drake. "her" otherwise. If the gender is unclear, ask before building.
- **Caption:** one funny line about the pair, both brands' @handles, "link in bio", Code MAHJMATCH, and 4-5 hashtags ending #affiliate. No colour theory. Run `python3 scripts/social/content_lint.py <captions file>` before Planoly.
- **Planoly (per the CLAUDE.md social rules):** the feed post auto-posts as part of the row, after her approval. Put the story version in the same row's Planoly drafts, with both brands tagged.

## Reference data for future rows (Oct 21 snapshot, not rendered, not in Planoly)
- `reference-picks.json`: one pick per album set (45 cards), plus a second pick for the 10 OMM sets with the most matches. Each entry has the album order, count, pronoun, FYM mat key and photo, handles and a caption draft. Sets skipped, and why, are listed at the bottom.
- `captions.json`: the same caption drafts, keyed `<set>--<mat>`.
- Rebuild steps:
  1. Fetch the live album pages into `<dir>/albums/`.
  2. Run `scripts/social/its_a_match/parse_albums.py <dir>`.
  3. Save the live FYM `const D` as `D.json`.
  4. Run `pick.py albums_live.json D.json <out>`.
  5. Run `captions.py <out>/picks.json <out>/skipped.json`.
- Before using a pick, re-check the live album, because order and counts change.

Open items in the reference data:
- Tigre de Tartan has no verified IG handle yet (Birdie, Emerald, Glitterville, Lola, Nantucket, Palm Royale and Sierra picks).
- Miss Mahjong has no verified handle either (Jade and Malachite tile tags).
