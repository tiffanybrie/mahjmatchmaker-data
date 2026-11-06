# Juniper full album set (Nov 6): review page + where every piece lives
Tiffany Nov 6 1:11am: cover, colour card, colour wheel + colour theory, favourite faces run-through, dating profile + intro carousel, all the match cards.
Page: juniper-album.html (phone-first, images = jsDelivr @1eeb2e1a728bc1eba84ee746ba6c5476bc1bd659, all 89 URLs warmed 200; racks = OMM Hot Pink + Agate per Tiffany Nov 6 2:11am, Agate card from scripts/albumcard/omm_agate_card.py). Rebuild: `python3 build.py <sha> juniper-album.html`.
Her one question: pick 4 faces (hearts -> "Copy my picks" -> paste in chat). Her picks are final; never swap them later. Then write them into config/profiles/juniper.json best_features (drop the PROPOSAL _status) and re-run `python3 scripts/colorwheel/favorites.py juniper` + `python3 scripts/social/tileprofile/intro.py juniper`.

Pieces:
- Cover: assets/covers/albums/00-juniper-mahjong-tiles-cover.jpg (+ w800/). scripts/covers/album_cover_omm.py, bg 06-Tile_Juniper_F, panel 34,93,54, omm_white logo.
- Colour card (existing): assets/colorcards/juniper/. Colour wheel: assets/colorwheels/juniper-color-wheel.jpg (`python3 scripts/colorwheel/wheel.py juniper`; papaya output unchanged, pixel-checked).
- Colour theory notes: on the page (section 3).
- Faces: 47 clean cutouts assets/tiles/faces/juniper/clean/ (scripts/colorwheel/cut_faces_juniper.py from OMM flat lay = product image 1 of /products/juniper-mahjong-tiles.json).
- Her best features DRAFT: assets/social/juniper-launch/juniper-favorite-tiles-DRAFT.jpg (favorites.py now takes a set key; papaya unchanged).
- Dating profile: assets/colorcards/juniper/00-juniper-mahjong-tiles-profile-d-story.jpg (swipe_profile.py juniper). Profile data: config/profiles/juniper.json.
- Intro carousel (7): assets/social/juniper-launch/intro/1-7.jpg (intro.py juniper; carousel.py/intro.py read launch_photos, rack_imgs, layers from the profile).
- Match cards (33, DRAFT order): assets/cards/juniper/ + manifest.json (scripts/albumcard/specs/juniper_build.py -> gen2.py). Order = scripts/albumcard/specs/juniper_round2.json.
Open: pronoun for Juniper (brand guide s3: ask her once; drafts use "her"); match count 33 is the draft count; racks are Claude's picks pending her OK.
