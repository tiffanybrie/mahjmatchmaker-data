# FYM v118 = "Version 1.18" (Nov 7 night), staged, NOT published (independent QA first)
Build: `builder/fym_fix_nov07/build118.sh <b117> <b118> <backs json>` (backs = `git show 1d46af69:config/tableview-back-colors.json`,
290 backs), then `tableview_racks_v118.py <b118>` was re-run once on the release build for the final racks (22011001, 233/293).
Build dir: scratchpad fym/b118. On top of 1.17 (b117):
- Adds: 25 ShopMy mats (2 hidden + Questionable), 28 Amazon holiday picks (amazon118.py: v96 adds without its stale s.cr placement;
  photos re-packed one chunk per 12, v96 had all 28 in one chunk so 16 photos never loaded), Mahj Mood Playing For Keeps + Fait a Main
  Texas Mon Amour Green (partner sweep, gate [100]); Mac + Miller "Perfectly Imperfect" seconds on the sweep ignore list.
- Links: Pearlescent shop link back ($475; revive_links.py + linkcheck "LIVE AGAIN" + gate [162b]); LSF Fleur ShopMy pin; Ozark ->
  ozarkmahjongg.com/product-page (Tiffany 10:45pm); no shop button (not Retired): 9 Bougie Mahjong mats (404), Splash Peony and Parasol.
  NOT applied: Mahj & Moon Vintage Garden Floral -> p-98067023 (that pin is Etsy 4371281339 = Vintage Floral Gingham, paired Oct 31).
- Tiffany's missed-mats round-1 yeses: 134 pairs into m (+ locks); 12 on retired vault sets with no FYM set (Shangri-la, Preppy Soiree,
  Spring Love).
- Table view: walls 255/283 visible sets; mats usable 1,492/1,573 (tableview_v118, Lotus Cove vendor photo); racks 233/293.
- Prices: price filter shows no-price items last with "Price not listed" (price118.py, gate [166]); prices_v118: mats 1,446/1,573,
  tile sets 274/283, racks 293/293.
- Tile ranking for a mat (tilerank_v118, D.tso, gate [168]); zoom swipe (zoomswipe_v118, gate [164]); Deco titles = back colour ([103]);
  Amazon picks below the first 6 on holiday sets ([74]).
- Gate changes: [90] compares with the BUILT gallery via gallery_cov.py (same definition as coverage_check), FAIL when the staged gallery
  is this release; [162b], [166], [169] new; [145] reads the new price note.

Website copy: fym-site-preview site-app/fym-v118/index.html (assets @4c236353: mc 251-257 + thumbs118.js), produced by site118.py.
Mat Gallery: site/livepatch/matgallery/matgallery-v8.html (data-fym="v118"), rows data/matgallery-v118.json. build_v6 now drops cards
whose FYM mat is hidden (Mahjong Row album picks kept, Nov 6 1:33pm).
Search: assets/search built with --gallery-block=<v8 block commit>, pinned + warmed (site/livepatch/search/header-injection.html).
Artifact: scratchpad fym/pub118 (index.html + mc/190.webp pack + 8 re-packed chunks + files.json with 11 deletions), artifact118.py.
NOT in 1.18: doors_v118.py (not committed when built), Ozark new mats (ozark_v119.py -> 1.19).
NOT done: independent QA, artifact publish, page-block build + README 0a pin, Squarespace paste (FYM + gallery), search Code Injection swap.
