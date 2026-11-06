# Sunday Sets albums (Nov 6): 4 album card drafts + ONE new-mats-only review page

DESK item 3. Tiffany Nov 5 12:21am (HQ box sunday-moody-mats): "Just send me what needs to be added on. Why aren't these albums made if I swiped over a week ago."

## 1. Album match cards (DRAFT), from her EXISTING yeses only
Source: Sunday Sets swipe book WJT7jTYfXX45917UkEqKyq, db `sundaysets` (read Nov 6; snapshot scripts/albumcard/specs/sunday_sets_votes_nov06.json).
Build: `scripts/albumcard/specs/sunday_sets_build.py` -> `scripts/albumcard/gen2.py` (Juniper pipeline, card2.html). Crop fixes: scripts/albumcard/specs/sunday_sets_box.json.

| Set | Yes votes | Cards | Notes |
|---|---|---|---|
| Nature Walk | 44 | 42 | Evergreen Tartan (holiday) -> holiday section, not a year-round card; Rattan old-id duplicate vote |
| Sunday Blues | 61 | 56 | Peacock Garden + Dabney neoprene/leatherette twins merged (caption note); Festive Plaid = also_year_round card; 2 TNT duplicate votes |
| Plum Panda | 46 | 41 | Savannah twins merged; Vintage Oxblood (old-id yes) kept; Clara + Heirloom White Chinoiserie Round (holiday) -> holiday section |
| Hummingbird | 44 | 41 | Legacy twins merged; Festive Plaid = also_year_round card; Bunny Love = Paige Spearin x TdT (no commission, her yes kept, flagged) |

Cards: assets/cards/{nature-walk,sunday-blues,plum-panda,hummingbird}/ + manifest.json each (order, vote id, full name, brand, racks, caption notes, holiday_yes list).
- Order (draft): TNT recs first, then Sunday Mahjong's own mats, then the rest in book (colour-score) order.
- Tile photo: canonical assets/tiles/album/<set>.png (canon_tiles.py). Passed as a data URI because assets/tiles/album/index.json marks hummingbird.png as a LOOSE pile (old cut-out), which drew the Oct 29 fill-frame photo across the whole card.
- Tile racks (MATCH THE TILES), Peace Love Mahjong only, same shape on every card (Tiffany Nov 6 2:11am rule): Nature Walk = Acrylic Burl + Oak; Sunday Blues = Navy + Oak; Plum Panda = Dark Green + Acrylic Burl; Hummingbird = Navy + Acrylic Burl. Sunday's own rack (Cola) only has a render, no real photo (racks.py: real photos only). PENDING HER OK, like Juniper.
- Mat racks (MATCH THE MAT): config/mat-racks-picks.json when listed, else matpick B&B colours; no Carrot/Radish/Red/Persimmon on moody/leather mats (Oct 18 rule).
- Code band: Juniper rule (10% floor; SAVE WITH CODE for Anders Ruff / Mahjong Register / The Mahjong Press).
- Looked at every card on contact sheets. Known photo limits (best photo we have): Sunday Vegan Leather + Dapper 1 + El Ultimo Refresco shown as the full lifestyle/album photo (props); Lowcountry Horizon (It's a Mahjong Life) + Sapphire Blooms (Lemondrop) brand photos carry watermarks (Sapphire cropped to the corner away from it).
- Mahjong Row mats (Autumn Saffron, Osmanthus Grove, Midnight Garden, Marigold, Spring Awakening, Mocha Bloom) carry the normal code band: Mahjong Row is ON HOLD (DESK), check before these albums go live.

Still to do before live (NEW-ALBUM-CHECKLIST): her OK on racks + order, album pages, holiday sections (un-hide /holiday-mahjong-matches #hummingbird), FYM m-lists from these yeses, /links card.

## 2. New-mats-only review page (index.html)
31 mats added to Find Your Mat-ch AFTER her Oct 29 swipe (FYM v103 -> v115), colour-ranked against each colour card with the Oct 29 book scorer (newmats_score.py), novelty filtered (pick_new.py), max 2 per brand, then picked by eye from contact sheets. Sunday Mahjong's own new mats lead (Vegan Leather Ruby + Forrest, Green / Blue Gingham, Blue Rattan).
Nature Walk 8 · Sunday Blues 7 · Plum Panda 7 · Hummingbird 9. Not the 121-mat book; her old book votes are untouched.
Each mat is shown WITH the set's tiles (mat full, tiles inset bottom-right, tap to zoom), full names + brands. Hearts/X stay on her phone (localStorage); "Copy my picks" gives one line to paste in chat. Photos: FYM mc chunks (getimg.py).
Not a swipe book (book_gate.py not applicable).
Publish: Artifact publish file_path=site/livepatch/sunday-albums-nov06/index.html, root=/home/claude/mahjmatchmaker-data, files = files.json `files` map. Self-contained copy for the scratchpad: index.html + images/ + files.json.
Leftover: Calista Leatherette (new) = twin of her Sunday Blues yes Calista: noted on that card, not re-asked.
