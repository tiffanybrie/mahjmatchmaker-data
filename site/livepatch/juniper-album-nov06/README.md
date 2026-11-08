# Juniper full album set (Nov 6): review page + where every piece lives
Tiffany Nov 6 1:11am: cover, colour card, colour wheel + colour theory, favourite faces run-through, dating profile + intro carousel, all the match cards.
ROUND 3 (Nov 6, her 2:26am notes) applied OFFLINE, not published: see CHANGES-round3.md. Page images now pinned @95ec1edfe5201e4c0198ab43f5400e68ba67b6da (88 URLs warmed 200); self-contained copy = scratchpad junalb/ (index.html + files.json). Cards = juniper_round3.json (32).
Page: juniper-album.html (phone-first, images = jsDelivr pinned SHA; racks = OMM Hot Pink + Agate per Tiffany Nov 6 2:11am, Agate card from scripts/albumcard/omm_agate_card.py). Rebuild: `python3 build.py <sha> juniper-album.html` (`local` instead of a sha = relative image paths).
Her one question: pick 4 faces (hearts -> "Copy my picks" -> paste in chat). Her picks are final; never swap them later. Then write them into config/profiles/juniper.json best_features (drop the PROPOSAL _status) and re-run `python3 scripts/colorwheel/favorites.py juniper` + `python3 scripts/social/tileprofile/intro.py juniper`.

PICKS DONE (Tiffany Nov 7 7:22pm, final, never swap): dragon-green (emerald dragon) + dragon-red (pink dragon) on top as a pair, then bam-1-peacock, flower-4a (green pagoda + hot pink lotus), bam-7. In config/profiles/juniper.json best_features.
- Final card: assets/social/juniper-launch/juniper-favorite-tiles.jpg (the -DRAFT.jpg is the old proposal). Intro carousel re-rendered: assets/social/juniper-launch/intro/1-7.jpg (slide 4 = her best features).
- Face resolution (Nov 7 check): every OMM Juniper image (tiles product, starter kit, ultimate starter kit; no retailer lists Juniper) was checked. The flat lay master is 3185x3982 (~266 px per tile) and is the ONLY straight-on shot; the 2048px corner close-up (juniper-starter-kit-2327595) is angled with depth-of-field blur (green dragon soft, no peacock). So the cutouts stay ~251-259 x 348-352 px from the flat lay; they show at ~1:1 on both cards. No upscaling. A sharper face needs a new straight-on photo (e.g. our own shot of the real tiles, or ask OMM for the original flat lay file).
- Crop fix Nov 7: bam-1-peacock re-cut with 3px extra top inset (a sliver of the shadow line showed at its top-right corner): `python3 scripts/colorwheel/cut_faces_juniper.py bam-1-peacock`. Other 4 unchanged.

Pieces:
- Cover: assets/covers/albums/00-juniper-mahjong-tiles-cover.jpg (+ w800/). `FRAME=frame3.png python3 scripts/covers/album_cover_omm.py assets/launches/omm-juniper-mahjong-tiles/06-Tile_Juniper_F.jpg scripts/covers/holiday/omm_white.png 112 "Juniper<br>Tiles" "34,93,54" <out>`.
- Colour card (existing): assets/colorcards/juniper/. Colour wheel: assets/colorwheels/juniper-color-wheel.jpg (`python3 scripts/colorwheel/wheel.py juniper`; papaya output unchanged, pixel-checked).
- Colour theory notes: on the page (section 3).
- Faces: 47 clean cutouts assets/tiles/faces/juniper/clean/ (scripts/colorwheel/cut_faces_juniper.py from OMM flat lay = product image 1 of /products/juniper-mahjong-tiles.json).
- Her best features DRAFT: assets/social/juniper-launch/juniper-favorite-tiles-DRAFT.jpg (favorites.py now takes a set key; papaya unchanged).
- Dating profile: assets/colorcards/juniper/00-juniper-mahjong-tiles-profile-d-story.jpg (swipe_profile.py juniper). Profile data: config/profiles/juniper.json.
- Intro carousel (7): assets/social/juniper-launch/intro/1-7.jpg (intro.py juniper; carousel.py/intro.py read launch_photos, rack_imgs, layers from the profile).
- Match cards (32, round-3 order): assets/cards/juniper/ + manifest.json (scripts/albumcard/specs/juniper_build.py -> gen2.py, spec navy v3 + true_len). Order = scripts/albumcard/specs/juniper_round3.json.
Nov 7: +6 holiday cards (#33-38) + The Kerry (#39), Camellia -> best, Esme -> faces-only (soft), new profile prompt; see NOTES-round3-nov06.md "Nov 7".
Open: pronoun for Juniper (brand guide s3: ask her once; drafts use "her"); match count 33 is the draft count; racks are Claude's picks pending her OK.
