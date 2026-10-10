# Find Your Match builder pipeline (snapshot Oct 10, 2026)

Builds the single-file prototype (`match-builder-prototype.html`, artifact "Find Your Match") from the repo data plus product photos.

The scripts expect to run from `/tmp/mb` (paths are hard-coded), with the repo at `/home/claude/mahjmatchmaker-data`:

    mkdir -p /tmp/mb/img /tmp/mb/cut && cp -r builder/* /tmp/mb/ && cp builder/bbracks.json work/bbracks.json
    cd /tmp/mb
    python3 -I pick.py     # which tile sets + Tiffany's top matches -> plan.json (edit `want` to add sets)
    python3 -I fetch.py    # product photo per tile/mat/rack (incremental) -> img/, fetched.json
    python3 -I pile.py     # tile-pile photo per tile set (incremental) -> pile.json
    python3 -I cut.py      # rembg cutouts (incremental) -> cut/
    python3 -I embed.py    # cutouts, rack fixes, title colors, logos -> data_embed.json + prototype HTML
    python3 -I shot.py     # quick desktop/mobile error check (Playwright)

Hand-made assets kept here:
- `rkalt/` OMM, Bam Bird Walnut and PLM Oak racks levelled from single-rack product photos (`straight.py`).
- `plm/r_*.png` Peace Love Mahjong racks (White and Mint are recolored previews).
- `ret/` retired tile sets: tile photo cropped from Tiffany's album color card.
- `edit/titlecol.json` title color per tile set, read from each album color card's title.
- `logos/` brand logos (map.json), our logo and the flame heart icon (from her Canva logo).

Docs: project docs 16-22 (design direction, card rules, UX feedback, playful copy).
