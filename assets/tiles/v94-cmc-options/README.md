# Charleston Mahjong Club uniform tile photo OPTIONS (Tiffany Oct 26 8:23am) — not in the app yet
All 1600x700 canvases from CMC's own listing photos (products/<handle>.json full res), nothing edited in.
- A_<set>.jpg: angled close-up as shot (brand background kept), framed so the back tile sits inside the Mood board circle (x 450-1150).
  Sources: Country 13, Apres 01, Hunt 01, Cocktail 12, Yacht 01.
- B_<set>.jpg: flat full set + its back tile, cut out onto white (grabCut, seg2.py), back tile centred at x~1010.
  Sources: Country 03, Apres 02, Hunt 02, Cocktail 13, Yacht 16. Hunt Club is shot on leather and does not isolate cleanly (leather stays).
- C_<set>.jpg: Bam Bird-style split: faces from the flat photo (left) | the single back tile close-up (right), white centre line.
backbox.json = back-tile boxes (in the 1600-wide 'full' downloads). build.py rebuilds the options from the scratchpad sources.
