# Deco (Mulberry) full album set (Nov 7): review page + where every piece lives
Tiffany Nov 7 7:03pm: "You take them, just like you did this one. Just run with it." Built like Juniper (site/livepatch/juniper-album-nov06), Juniper lessons applied (pile photo, v3 navy logo, true rack length, one-brand same-shape tile racks, pair mat never #1, "Seeking:" tagline, new prompt, light/dark wheel, human copy). NOT published: Main publishes on her go.
Page: deco-mulberry-album.html (phone-first; images = jsDelivr pinned eee80bfd). Rebuild: `python3 site/livepatch/deco-lagoon-album-nov07/build.py deco-mulberry <sha|local> <out.html> [files.json]` (one builder for both colourways). Self-contained copy: scratchpad deco-mulberry-album/ (index.html + files.json, paths relative to the repo root, Juniper junalb format).
Her one question: pick 4 faces (hearts -> "Copy my picks" -> paste in chat). The Deco faces are the same on every colourway, so her picks can serve both albums. Then write them into config/profiles/deco-mulberry.json best_features (drop the PROPOSAL _status) and re-run `python3 scripts/colorwheel/favorites.py deco-mulberry` + `python3 scripts/social/tileprofile/intro.py deco-mulberry`.

Pieces:
- Tile photo (PILE): assets/tiles/album/deco-mulberry.jpg = crop of Bam Bird listing image 14 (two velvet bags; no loose pile shot exists). Source kept: assets/launches/bambird-deco-tile-set/14-deco-two-bags-FULL.jpg.
- Cover: assets/covers/albums/00-deco-mulberry-mahjong-tiles-cover.jpg (+ w800). `FRAME=frame3.png python3 scripts/covers/album_cover_omm.py <bag crop> scripts/covers/holiday/bambird_white.png 150 "Mulberry<br>Deco Tiles" "<rgb>" <out>`.
- Colour card: assets/colorcards/deco-mulberry/ (config/colorcards.json sets.deco-mulberry). Colour wheel: assets/colorwheels/deco-mulberry-color-wheel.jpg (light/dark wheel).
- Colour theory notes: on the page (section 3).
- Faces: 40 clean cutouts assets/tiles/faces/deco/clean/ (scripts/colorwheel/cut_faces_deco.py from Bam Bird listing image 16, 4000x6000, 274px-wide tiles). Shared by all Deco colourways (profiles carry faces_dir).
- Best features DRAFT: assets/social/deco-mulberry-launch/deco-mulberry-favorite-tiles-DRAFT.jpg.
- Dating profile: assets/colorcards/deco-mulberry/00-deco-mulberry-mahjong-tiles-profile-d-story.jpg. Profile data: config/profiles/deco-mulberry.json.
- Intro carousel (7): assets/social/deco-mulberry-launch/intro/1-7.jpg. Slide 6 = Bam Bird's own photo (assets/launches/bambird-deco-dragon-mat/).
- Match cards (30): assets/cards/deco-mulberry/ + manifest.json (scripts/albumcard/specs/deco_build.py deco-mulberry -> gen2.py). Picks/order/reasons: scripts/albumcard/specs/deco-mulberry_nov07.json. Left out + reasons: scripts/albumcard/specs/deco_leftout_nov07.json.
- Tile racks: Bam Bird Boutique Lagoon Wood + Mulberry Wood (new cutouts assets/racks/card/bam-bird-boutique-{lagoon,mulberry}-wood.png from Bam Bird's rack variant photos; 19in in config/rack-lengths.json). Mat racks = matpick nearest Bird & Bamboo colours.
Open: pronoun (brand guide s3: ask her once; drafts use "her"); TNT recs not searched (no Chrome in this run); Indigo album still to do (restock mid/late Nov); low-res brand photos flagged on the page (SoHo, Evergreen, Tiger Fans, Mulberry and Sage, Year of the Snake, Burgundy Grove, Midnight Peacock).
