# Mat-edition albums in Find Your Match (Oct 18)

`patch.py` adds Tiffany's mat-edition albums (Vivienne, Larkspur, Peony & Parasol) to the pending FYM build
(scratchpad/fymfix2/build/index.html). It is idempotent. Re-run it after any rebuild of that file, then publish as usual.

- Vivienne: 15 of her 16 yeses added as her matches; door order = her swipe ranking. Spring Love is a vault set, not in FYM yet.
- Larkspur: door order = her approved Larkspur order (config/larkspur-album-order.json); all sets already present.
- Peony & Parasol: door order = album spec order; all sets present.
- Removed the unsupported "Tiffany's match" label for Vivienne and Larkspur on the catalog set Sunshine (Middle & Main).
- setsForMat() sorts her sets by D.mord when the mat has a mat-edition order.
Report: report.json. Tested locally: the Vivienne door shows "Tiffany matched this mat with 15 tile sets" in her order, no page errors.
