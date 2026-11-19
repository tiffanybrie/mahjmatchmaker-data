# Rescued from the Nov 7-18 session scratchpad (Nov 19, for the album handoff)

These are ONE-OFF helpers used while building albums. They were never in the repo and would have been lost when the
session ended. They are NOT part of the standard pipeline (that is scripts/albumreview/ + scripts/albumcard/gen2.py +
scripts/albumcard/specs/*_build.py). They hard-code the old scratchpad path in `S=`; point S at this folder to re-run.

- deco/: how the three Bam Bird Deco albums (Lagoon, Mulberry, Indigo) were first pulled and specced on Nov 7, before
  scripts/albumreview/pull.py existed: picks.py (hand-picked keys per section from contact sheets), mkspec.py (writes the
  deco-*_nov07.json specs with Claude's "why" lines), cropmats*.py (crops mat photos to the mat), fetchhd*/fetchmi* (pull the
  brand's highest-resolution images), sheets.py / pairs.py (contact sheets of mat + tiles to judge by eye), *.json inputs.
- juniper-order/: Juniper (OMM) album ordering data (rows, her order, new rows) from Nov 6-7.
- sundaybook/: Playwright screenshot scripts for the Sunday Mahjong swipe book (swipe books are retired since Nov 8).
- holpage/: screenshot + data for the holiday matches page check.
