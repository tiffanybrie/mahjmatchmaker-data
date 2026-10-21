# "It's a mat-ch!" carousel: the middle post of every set's launch row

Every tile set's Instagram launch row has 3 grid posts (doc 89): **profile carousel, then It's a mat-ch!, then the reel**. This is the standard template for the middle post. It is not a standalone series (Tiffany, Oct 21). Upgraded to a 3-slide carousel on Oct 21 (Tiffany approved the direction); first example: `papaya-heiress/` (`preview.jpg` shows all four images side by side).

Why it works: Britt Mills reshared the Papaya + Heiress card within hours on Oct 21. Tiffany: "highly shareable for those secondary mat brands... very easy content for them to reshare."

## Settled (Tiffany, Oct 21)
- Headline **"It's a mat-ch!"** is FINAL. It is the only headline the builder makes (variant B is gone). Caveat's own hyphen, spaced slightly off the t's crossbar.
- **No pronouns on short pieces.** Use the set's name: "Papaya's matches", never "her matches" (`--short Papaya`). So this post never needs a set's gender.
- **Always say where the albums live.** Slide 1 stands on its own (brands reshare it to their stories), so its pill carries mahjmatchmaker.com.
- Bigger wordmark + "Hooking up tiles, / mats & racks" (two lines). No @handle line.
- Navy and pink, never brown. One cream paper background (`#faf3ea`) on every slide.

## The slides (1080x1350 each)
1. **It's a mat-ch! card** (`slide1.jpg`): tile circle ♥ mat square; "Set ♥ *Mat*" in navy Lora; "TILE BRAND · MAT BRAND" in pink Bitter caps; navy pill "Swipe all N of <Short>'s matches" / "mahjmatchmaker.com"; wordmark; tagline. Content stays inside y 120-1230, so the 3:4 grid crop keeps it.
2. **The match card** (`slide2.jpg`): the real album card (`assets/cards/<set>/`, found via `manifest.json`) big in a soft white frame. Header "TOP MATCH CARD" / "From <Short>'s album". Under it: "*Mat* · Brand", then the racks in two columns, MATCH THE TILES / MATCH THE MAT, named exactly as on the card. No colour theory. It's a "match card", never "mat-ch card".
3. **Find *Your* Mat-ch™ preview** (`slide3.jpg`): a navy phone showing the real FYM swipe view (tiles door, the set + the top mat only), with "Swipe your own matches" and "MAHJMATCHMAKER.COM". **No dates in the template** (Tiffany, Oct 21): these carousels run after the Oct 27 launch, when the tool is live. ™ appears here because it's the full tool name's most prominent use.

Plus **`story.jpg`** (1080x1920): slide 1 for brand reshares. Key content stays inside the safe zone: the top 14% (269px) and bottom 20% (384px) are kept clear.

## Build one
1. Phone screen for slide 3: a real screenshot of the FYM build (the published artifact's files, e.g. the folder with its `index.html`, `b*.js`, `m/`, `mc/`). It serves the folder locally, opens the tiles door at 390px, searches the set, and taps ✕ (never ♥) until the mat is the top card. The undo arrow is hidden in the shot, so it shows ✕ and ♥ only.
```
python3 scripts/social/its_a_match/fym_shot.py --build-dir <fym build dir> --set "Papaya Spritz" --mat Heiress \
  --out assets/social/its-a-match/papaya-heiress/fym-screen.jpg
```
2. The carousel:
```
python3 scripts/social/its_a_match/render.py --set-slug papaya-spritz --tile "Papaya Spritz" --short Papaya \
  --mat Heiress --mat-brand "Britt Mills" --count 50 \
  --current-racks "Bird & Bamboo Lavender" "Peace Love Mahjong Chartreuse" "Middle & Main Scalloped Beechwood" \
  --fym-img assets/social/its-a-match/papaya-heiress/fym-screen.jpg \
  --out-dir assets/social/its-a-match/papaya-heiress
```
This writes `slide1.jpg`, `slide2.jpg`, `slide3.jpg`, `story.jpg` and `preview.jpg` into `--out-dir`. Many sets at once: `--json list.json` (a list of dicts with the same keys, underscores for dashes).

Defaults it reads from the repo (override with `--tile-img`, `--mat-img`, `--card-img`, `--tile-racks`, `--mat-racks`):
- tile photo: `assets/tiles/album/<set-slug>.*`
- mat photo: `assets/colorcards/<set-slug>/mats/<mat>-<brand>.jpg`
- match card + its racks: the card for that mat in `assets/cards/<set-slug>/manifest.json`

Checks it prints (fix every one before showing Tiffany):
- `OVERFLOW/BROKEN`: content outside the safe band, or an image that didn't load.
- `WARN ... the album card still shows ...`: the card's tile racks aren't in `--current-racks`. Slide 2 follows the card (never relabel a card), so get the card fixed and re-render.

Then LOOK at every slide at full size and at phone size (390px wide).

Rules for the inputs:
- **Pair:** only her real picks. Use the top of the live album order (or her swipe-book stars). Skip official pairs (same brand as the tiles). The point is to spotlight another brand's mat. That brand must be a partner, or allowed per CLAUDE.md. No Mahjong Studios, The Mahjong Line, Mahj House Rules, Four Winds Social (except the Mahj Mood collabs) or Amore. No Paige Spearin x TdT. Prefer brands with a verified handle in `config/social/ig-handles.json`.
- **Tile photo:** the canonical album photo, `assets/tiles/album/<set>.*`. Tortoise = `classic-tortoise-zoom.jpg`.
- **Mat photo:** the mat-only card image. Use `assets/colorcards/<set>/mats/` if it exists. Otherwise use the FYM photo for that mat: the `f` path in reference-picks.json, read from the live FYM artifact's published files.
- **Count:** the number of cards on the live album page. Never round it.
- **Short name:** the set's first name for the pill and slide 2 header (`--short`), e.g. Papaya. No pronouns.
- **Caption:** one funny line about the pair, both brands' @handles, "link in bio", Code MAHJMATCH, and 4-5 hashtags ending #affiliate. No colour theory. Run `python3 scripts/social/content_lint.py <captions file>` before Planoly.
- **Planoly (per the CLAUDE.md social rules):** the 3-slide carousel auto-posts as part of the row, after her approval. Put the story version in the same row's Planoly drafts, with both brands tagged.

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
