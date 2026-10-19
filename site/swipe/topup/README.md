# Top-up swipe books: PARKED (Oct 19, ~1:30am)

Tiffany paused matching and album creation until after the Oct 27 launch, so the team can focus on QA and finishing the site. Nothing was built or published, and nothing was added to Ready to Ship.

## Goal
Every live album has at least 20 matches, ideally 25–30. Live counts, Oct 19 (album_counts_2026-10-19.txt):
- Under 25: Sunset 9, Sorbet 11, Gemma 12, Jasmine 12, Limoncello 12, Nantucket 12, Taylor 12, Luminaire 14, Emerald 16, Glitterville 16, Sierra 16, Birdie 18, La Fête 18, Lola 19, Osler 19, Palm Royale 19, Pippa 19, Dandy 20, Talulah 22, Moonlight 24, Seabreeze 24.
- Skip the 4 vault albums.

## How to resume after launch
1. **Pool.** Use the match pool, not the full catalog: docs 51, 36 and 55, with the brand gates, skip list, no travel or holiday mats, and bamboo-cut photos.
2. **Exclusions.** Leave out mats already in the album, plus every mat she saw for that set in earlier books. She already passed on those; read each old book's db.
3. **Specs.** Build with scripts/swipe/build_book.py.
   - The FYM mats input: /tmp/claude-0/-home-claude-mahjmatchmaker-data/.../scratchpad/fym_mats.json may be gone by then. If so, regenerate it from the FYM build's mc/ chunks.
   - Set order: Sorbet, Sunset, Gemma, Jasmine, Nantucket, then thinnest first. 40–60 mats per set, color pull on tile back and layer colors first, and always include Britt Mills and Amanda Toppe.
   - Then run finish_patch.py, which also applies the yes-only patch.
4. **Ready to Ship.** Add a "Top-up swipes: get every album to 25" item with links and counts. On her Done, build the cards and add them to the album.
