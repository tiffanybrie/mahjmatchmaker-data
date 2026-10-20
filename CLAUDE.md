# Mahj Matchmaker repo: rules for any Claude session (read first)

## Find Your Match (FYM) is the top project. These are hard rules.
Live app: claude.ai artifact 6epA9HuEdT32zUp79Qv3kd. Its published index.html (`const D={...}`) is the build source of truth.

1. **Gate before every publish.** Run `python3 builder/fym_gate.py <build_dir>`. If it fails, do not publish. No exceptions.
2. **Independent QA before Tiffany sees it.** A separate agent that did not build the change tests phone (390px) and desktop: both doors (tiles first, mat first), color filter (switch + clear), zoom persists across swipes, card + share, and VIEWS tile and mat photos via contact sheets. Tiffany is never the QA team.
3. **Album tile photos are canonical.** Every set with a match album uses its album photo `assets/tiles/album/<set>.*` (map: scripts/swipe/canon_tiles.py). Default framing shows a tile back/layers + faces.
4. **"Tiffany's match" only from her real picks** (album or swipe-book yes). Catalog sets: `m=[]`. The mat-door "Tiffany matched this mat with N sets" counts only those.
5. **Locks.** `builder/fym_flags/locks.json` holds approved photos/crops/names/match lists. Catalog scrapes and refreshes may only ADD to a pending queue; run `builder/fym_apply_locks.py`; "changed locked items" must be 0.
6. **New products** become visible only after their photo passes the flags (`builder/fym_flags/*_photo_flags.json`): mats must show the mat (not lifestyle/packaging), tiles must show tiles.
7. **UX:** X and heart only (never crush/nope/pass). Zoom persists. Color filter never locks. Code MAHJMATCH on every card with a partner piece (no hard-coded %).
8. When she reports a bug, add a gate check for that bug type the same day.

## Working rules
- Never sit idle; finish one task, start the next. Project docs (claude.ai Project "Mahj Matchmaker") doc 00 = top rules.
- Commit trailer: `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` + session line; push with `git pull -q --rebase && git push -q`.
