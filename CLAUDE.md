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

## Non-partner brands are locked out (Tiffany, Oct 20)
Only partner brands (and ShopMy-affiliated mats) come into the Mat Gallery and FYM. A non-partner mat comes in ONLY if Tiffany matched it or explicitly allowed it. Reason: brands need an incentive to affiliate once the app launches. Allowed non-partners so far: Sunday Mahjong (whole line, personal favorite), Ozark Mahjongg (whole line, she likes them; Oct 20), Mahj Tile Haus mats she matched (e.g. White Lotus), Mahjong Moxie Duck Camp + Heron Landing. Never pull a non-partner brand's whole line because one mat was matched. Removed list: config/mat-gallery-crosstags.json `remove_mats` + builder/fym_flags (locked hidden).
Oct 20 brand decisions (applied in gallery remove_mats + FYM hid/locks/flags): Mahj & Moon, Maison Mahj (The Chalet), Hutch & Nook, Luxe, Mahj Tile Haus keep ONLY her matched mats; The Mahjong Line, Mahj House Rules and every Four Winds Social mat removed (the FWS x Mahj Mood collabs Beyond the Ribbon / Rally in Pink / Eloise stay as Mahj Mood, a partner). Still pending: Tala Mahj (ShopMy link swap), The Kerry, 4 fuzzy Mahj & Moon mats (builder/fym_flags/nonpartner_pending.json).
**No Mahjong Studios mats anywhere (Tiffany, Oct 20 22:31).** Mahjong Studios tile sets and racks stay; every Mahjong Studios mat is out of the Mat Gallery (crosstags remove_mats.brands) and hidden + locked in FYM. Gate [12] fails if one is visible in FYM or the staged gallery.
Hidden or removed mats never sit in a set's match list (m) unless they are her real picks verified on the live album page / swipe book (builder/fym_flags/m_hidden_ok.json); gate [11].

## Colour rules (Tiffany, Oct 20 late)
- Order inside every colour section (gallery) and colour chip (FYM): her `lead` mats first (config/tiffany-color-notes/2026-10-20-late-calls.json), then primaries sorted by measured share of that colour (config/mat-accent-colors.json shares) high to low, then ALL secondary mats (also + accent merged) by measured share high to low. No measurement = 0 (bottom of its tier). Mahjong Studios last within each tier.
- Holiday mats live only in Holiday (gallery) and never in single-color chips (FYM). Never move a holiday-tagged mat out without Tiffany. (crosstags holiday_off emptied Oct 20.)
- Her late colour calls (floral:false, holiday, primary/also, yellow also-colours, lead) live in config/tiffany-color-notes/2026-10-20-late-calls.json and build_v5.py re-applies them last, so no rebuild undoes them.
