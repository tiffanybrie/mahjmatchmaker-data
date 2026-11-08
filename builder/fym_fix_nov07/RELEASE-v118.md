# FYM v118 = "Version 1.18" (Nov 7 night), staged, NOT published (independent QA first)
Build: `builder/fym_fix_nov07/build118.sh <b117> <b118> <backs json>` (backs = `git show 1d46af69:config/tableview-back-colors.json`,
290 backs). The release build was made by that chain on Nov 8 ~12:20am, then (same order as the chain now has them) fixes118 (Deco
titles), albumlive118 (Juniper album photo locked + t118/juniper.jpg + rack picks) and fym_apply_locks were re-run on it.
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
- Juniper (album LIVE): m = her final 42 (juniper_m118), album link /juniper-mahjong-tile-matches, FYM tile photo = album pile shot
  (t118/juniper.jpg), her rack picks lead Flora Belle / The Kerry / Zesty Plume. Doors: door parity (doors_v118, gate [167]).
- Table rack held: Mahjong Register Peony Blush Pearl Scalloped (light rim on navy; rackhold118.py) until re-cut.
- Tile ranking for a mat (tilerank_v118, D.tso, gate [168]); zoom swipe (zoomswipe_v118, gate [164]); Deco titles = back colour ([103]);
  Amazon picks below the first 6 on holiday sets ([74]).
- Gate changes: [90] compares with the BUILT gallery via gallery_cov.py (same definition as coverage_check), FAIL when the staged gallery
  is this release; [162b], [166], [169] new; [145] reads the new price note.

Website copy: fym-site-preview @e0a6a233 site-app/fym-v118/index.html (r10; assets @0d56bec7: mc 251-258 + thumbs118.js + t118),
produced by site118.py (r9 @1eb284bc was the copy the Nov 8 independent QA blocked).
Mat Gallery: site/livepatch/matgallery/matgallery-v8.html (data-fym="v118"), rows data/matgallery-v118.json. build_v6 now drops cards
whose FYM mat is hidden (Mahjong Row album picks kept, Nov 6 1:33pm).
Search: assets/search built with --gallery-block=<v8 block commit>, pinned + warmed (site/livepatch/search/header-injection.html).
Artifact: scratchpad fym/pub118 (index.html + mc/190.webp pack + 16 re-packed chunks + mc/171 re-shipped + t118 + files.json with 11
deletions; 265,266,131 bytes = 3,169,325 free, 503 files) + fym/pub118.manifest.json (gate [170]), artifact118.py with the live mirror
scratchpad qa118/live as its 7th argument.
NOT in 1.18: Ozark new mats (ozark_v119.py -> 1.19).
NOT done: independent QA, artifact publish, page-block build + README 0a pin, Squarespace paste (FYM + gallery), search Code Injection swap.

## QA fixes (Nov 8, after independent QA docs/reports/fym/qa-v118-2026-11-08.md = BLOCK)
Rebuilt through build118.sh (two new steps wired in: qafix118.py before fym_apply_locks, tiledeckprice118.py after price118), website
copy r10 via site118.py (tiledeckprice118 applied after the tilerank JS), artifact folder via artifact118.py. Nothing published.
- **F1 picks (Juniper 42/42 on all three copies).** artifact118.py never slims a mat that is in any set's m list (33 picks the artifact
  had as 'ahid' come back in full, incl. Juniper's Color Me Birdie, Peonies Burst, Paradise, Botanical Jewel, Tropical Travels, Grand
  Rose Medallion Chinoiserie, Green Bamboo Blossoms). It also re-ships live chunk mc/171.webp, which had lost 4 Soiree All Day pick photos
  in an earlier re-pack (Poinsettia Party, Pretty in Pink, Star of David Hanukkah, Toasty and Tipsy). Room: 16 chunk files re-packed
  without photos of hidden mats (lossless, 3.9 MB), then 39 lowest-ranked non-partner, non-pick mats slimmed in the artifact only (ShopMy /
  Amazon / Bougie (dead links) / Betty June / Piper Chase / Mahj & Moon non-partner; full list in scratchpad fym/pub118.out.json); the
  website copy keeps all of them. Artifact visible mats: 1,267 (was 1,274; website 1,574).
- **F1 Paint Feathers (LBB).** Every LBB product image was checked (products/paint-feathers-neoprene-mahjong-mat.json): IMG-3212,
  IMG-3213 (close-up), Paint_Feathers_33_small_file.png (pattern close-up), IMG-3341. IMG-3212 is a straight-down shot of the whole mat
  on the floor; perspective-corrected and cropped to the mat (rule 3b) = assets/mats/qafix-nov08/lbb-paint-feathers-flat.jpg (whole mat,
  colours clear). Used (m/3096, chunk 258), off the Questionable list, mat_photo_flags ok, hid lock + m_hidden_ok line removed, mf
  pink + green (re-measured; the floor shot had given ['pink'], sh 0). Reversible: re-add the hid lock if Tiffany dislikes the crop.
- **F2 price order.** tiledeckprice118.py: with a tile price chosen the mat-door deck is her priced picks, album+catalog priced (tile
  rank, brand cap), her unpriced picks, album+catalog unpriced. Lotus Cove 'Under $175': first unpriced card is now #37 of 45 (was #6
  with 31 priced after it). 'See all' sections already kept priced-first inside each section (now tested). Gate [166b] runs the page's
  own code in node (Lotus Cove + the 4 most-picked mats x every price option, deck + See all) on the build; the same check passed on the
  website r10 and artifact copies.
- **F3 photos.** YMI Outlaws of the Marsh: set hidden + no_tiles flag (the brand has only a single-tile face/side/back shot and a
  full-set layout strip). Watermarks, no clean image found, left as is and listed in builder/fym_flags/watermark_flags.json (accepted):
  Mac + Miller Fire + Fortune (Verdant) t15/144.jpg, Fire + Fortune (Ember) t15/143.jpg, Red White & Blues t71/... (every product image,
  12/12/16, and the store's /products.json (36 products) carry "(c) 2026 Mac and Miller Mahjong"); Mahj Tile Haus Palm Royale m/1644
  (Juniper #2, never hidden): mahjtilehaus.com answers products.json with a bot check (not retried), our only other copy (album colour
  card) is the same watermarked image.
- **Gates:** [166b] tile-deck price order (node), [170] every m-list mat shown with a loadable photo in build / website copy /
  artifact folder (+ manifest), [171] visible watermarked photos unless accepted.
- **Not done (needs the gallery chain):** Paint Feathers is now visible in FYM, so the staged Mat Gallery v8 / search index do not
  carry it until the next gallery rebuild (build_v6 drops hidden FYM mats).
