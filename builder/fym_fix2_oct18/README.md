# FYM fix 2 (Oct 18) — independent-audit fixes on top of v53

Build: `python3 fix.py` (scratchpad fymfix2/). Base = live v53 index.html. Output in fymfix2/build/:
index.html, b13v1.js (new thumbs), mc/85-87.json (new mat images), t14/0.jpg (Nature Walk crop).
Publish to FYM 6epA9HuEdT32zUp79Qv3kd with those 5 files (others unchanged).

Verified locally with the audit scripts (fymfix2/ascripts, pointed at the new build):
- cmp_order: 0 order divergences, 0 missing album mats on all 55 album sets (only extras = pending repo cards, appended after her album order; holiday sets keep pair-mat-first)
- t_door_data: 344 album mats, 0 "hasn't matched yet", 0 missing sets
- rule2: 0 album cards not shown as hers; 4 "unsupported" on Dec 1994 are in her saved Dec 1994 album order
- racks_eval: 0 B&B woods, 0 hidden racks, 0 OMM-on-non-OMM, 0 18" on large tiles
- flows: undo clears mocked mat (390+1280); swipe-card full-screen opens (390+1280); no console errors; no sideways scroll

## Oct 18 afternoon: mat-edition patch
After building, run `python3 builder/fym_mated_oct18/patch.py` (Vivienne/Larkspur/Peony door order + Vivienne pairings). Already applied once to build/index.html (backup: scratchpad/fymfix2/index_pre_mated.html).

## Oct 18 afternoon: match card redesign (approved)
`builder/card_build_oct18/`: new step-4 card (Love triangle / Mood board / Shop, 2x exports, HD tiles/racks/logos).
Adds `hd/` (index.json + 21 chunks, ~25 MB) to the publish list. After any rebuild: `python3 builder/card_build_oct18/splice.py` then `python3 builder/fym_mated_oct18/patch.py`.
