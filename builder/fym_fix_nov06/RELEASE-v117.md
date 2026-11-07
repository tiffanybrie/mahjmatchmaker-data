# FYM v117 = "Version 1.17" (Nov 6 night): the FULL build from RELEASE-v116.md "r2", relabelled because 1.16 r1 went live first
Same content as v116 r2 (on top of live 1.16 r1): auto-apply links, 17 dead links with no shop button (gate [162]), colour fixes on 17
unlocked mats (84 LOCKED left untouched; Main is asking Tiffany), Juniper pair mat in top 3, Mahj Pit White Beech Wood rack, 41 thin-album
hearts, MATCH-INBOX link/stock/album fixes. Only the label differs: builder/fym_fix_nov06/release117.py.
- Build: scratchpad fym/b117 (= b116 + release117). Gate (build + website copy): PASS, docs/reports/fym/gate-v117-2026-11-06.txt.
- Website copy: fym-site-preview @4cd5d2c34cc8ac32d3d07624c600ac42dcd5d329 site-app/fym-v117/index.html (jsDelivr 200; no new asset files).
- Artifact folder: /tmp/claude-0/-home-claude/05549d34-8fe3-5ca9-a6a5-308991cb9a78/scratchpad/fym/pub117 (index.html + mc/190.webp = pub115's pack unchanged + files.json).
- Mat Gallery: site/livepatch/matgallery/matgallery-v7.html (data-fym="v117"), rows data/matgallery-v117.json @d692877b (jsDelivr 200).
  The v116 block matgallery-v6.html @ba6479d0 is untouched.
- NOT done: independent QA, artifact publish, README 0a pin, Squarespace paste (FYM + gallery), search rebuild.

## r2 (Nov 6 night, after QA failed only on item d, colour fixes)
- By-eye colours (LOOKED at each photo), kept in config/fym-colour-fixes-v116.json 'eye' and applied by colour116.py: Spring Fling (dark, blue,
  pink, purple), Le Madeline (yellow, pink), Chinoiserie Citrus Grove (orange kept), Celestial Sun (yellow kept), Wildflower American (yellow +
  blue), The Sun Tarot (blue added AND yellow kept: the yellow suns are real), Hummingbird Floral Frame Blue (neutral, blue, dark), plus Wren
  Sitting Sea Side (yellow, blue, neutral), which the new gate [163] flagged (rule left it neutral-only).
- Gate [163]: a mat the rule leaves neutral-only, or cuts to one colour from several, FAILS until it has an 'eye' entry; eye entries must match the build.
- Gallery v117 rows rebuilt with the same corrections (@c90f4aaf), block matgallery-v7.html @46c47075 (data-fym="v117"; v116 block untouched).
- Website copy fym-site-preview @8a3081f2a0d177914c45fc621778230ab4b84efd site-app/fym-v117 (jsDelivr 200). Artifact folder pub117 rebuilt.
- Gate (build + website copy): PASS, docs/reports/fym/gate-v117-r2-2026-11-06.txt. Build: builder/fym_fix_nov06/build117.sh <b115> <b117>.
