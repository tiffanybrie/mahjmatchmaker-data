# FYM flags and locks

Files here guard the Find Your Match data against bad refreshes.

- `locks.json`: values Tiffany approved. Each album set's tile photo (`src`, `full`, `pile`), every set's "Tiffany's match" list (`m`, `sb`), hidden sets (`hid`), photo framing (`fp`, `fz`), and the name/photo/retired flag of every mat in her lists.
- `tile_photo_flags.json`: verdict on each catalog tile photo, keyed by set slug. `no_tiles` means the set stays hidden. `faces_only` and `watermark` mean it stays visible but needs a better photo.
- `mat_photo_flags.json`: the same for mats, keyed by mat id. `no_mat` means hidden.

## Rules for every rebuild or catalog refresh

1. A refresh may only ADD new products, and only into a pending queue. It never edits an existing tile, mat, set or match list.
2. A new product goes live only after its photo passes a flag check. Mats must show the mat, not a lifestyle or packaging shot. Tiles must show tiles: a back or its layers, plus faces.
3. Run `python3 builder/fym_apply_locks.py <build_dir>` after any rebuild. It restores locked values and prints `changed locked items: N`. Run it again with `--check`. N must be 0.
4. Run `python3 builder/fym_gate.py <build_dir>`. It must print PASS before anyone publishes.
5. Print a change report with every publish: products added, locked items changed (should be 0), and items still pending.

To change a locked value, get Tiffany's OK first. Then edit `locks.json` in the same commit as the data change.
