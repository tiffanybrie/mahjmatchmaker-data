# FYM v116 r2 = the FULL 1.16 build (Nov 6 evening, Matches & Catalog build for Main). NOT published.
NOTE: r1 (below) went LIVE as "Version 1.16" at ~6:42pm (commit 702eaa5a, pin @80d4f0b8) while r2 was being built, so r2 needs a new
label before it ships (e.g. Version 1.16.1 / 1.17: edit release116.py, re-run site116/artifact116 + gate).
r1 (below) was a narrower fork (Mahjong Row parked + Mahjong Co. mats hidden only). r2 contains r1's edits (its mr_out.py + mco_out.py)
PLUS: auto-apply discount links (gate [159]); 17 dead shop links with no shop button, not Retired (config/fym-dead-links.json, new gate
[162] curl-checks every visible shop link); colour fixes from the Mat Gallery v6 work on 17 visible unlocked mats (84 LOCKED mats the rule
would change are listed in config/fym-colour-fixes-v116.json 'skipped', untouched: need her OK); Juniper deck = Palm Royale, Garden Glow,
Lotus Cove (config/fym-coordinated.json _top3, gate [57]); Mahj Pit White Beech Wood rack (6b white+navy reviewed; the other 5 Mahj Pit racks
have no clean photo); her 41 thin-album hearts; MATCH-INBOX link/stock/album fixes. Build: builder/fym_fix_nov06/build116.sh <b115> <b116>.
Gate (build + website copy): PASS, docs/reports/fym/gate-v116-full-build-2026-11-06.txt.
- Website copy: fym-site-preview @fdcc1868e475c8fa393132b97e6d1c55475caf66 site-app/fym-v116/index.html (jsDelivr 200; no new asset files).
- Artifact copy: /tmp/claude-0/-home-claude/05549d34-8fe3-5ca9-a6a5-308991cb9a78/scratchpad/fym/pub116 (index.html + mc/190.webp = pub115's pack unchanged, files.json), made by artifact116.py from pub115.
- Mat Gallery: site/livepatch/matgallery/matgallery-v6.html stamped data-fym="v116" (rows data/matgallery-v116.json @8ed532e9, 1,455 rows;
  Mahjong Co. mats hidden, Mahjong Row's 9 matched mats kept with no code-page link). Staged, NOT pasted.
- Not done here (by request): artifact publish, README 0a pin, Squarespace paste, search rebuild. Independent QA still required (rule 2).

# FYM v116 = "Version 1.16" (Nov 6): Mahjong Row & Co. parked + Mahjong Co. mats hidden

Built from the LIVE artifact 6epA9HuEdT32zUp79Qv3kd (version 1793866353-792d = Version 1.15, artifact-slim copy) and from the live website
copy site-app/fym-v115 @57f0b4e6. Both copies got the SAME D edits:
1. builder/fym_fix_nov06/mr_out.py: Mahjong Row & Co. hidden + parked (mats 9, tiles 8, racks 7, sets 8 incl. Cypress); brand out of logo order.
2. builder/fym_fix_nov06/mco_out.py: every mahjongco.com MAT hidden (6: Gatsby, Highland Heritage Plaid, The Hunt Club, Tracing the Tides,
   Vintage Oxblood Leather, The Lodge; retired, shop empty). Kaleidoscope tiles stay. New gate [161].
3. Version 1.15 -> 1.16.
Flags/locks: locks.json hid=true on the 15 locked mats (her calls); m_hidden_ok.json +48 (her album/swipe-book picks stay in m, never render);
fym-partner-coverage.json exempts Mahjong Row ([114]); gate [8b]/[92] skip parked items; fym_matdoor_check.js Rattan path uses the next visible
album set when Cypress is parked (and fixes a .map(setIx) index-as-maker bug).

Gate: the artifact-slim copy has ~1,236 known problems by design (artifact-only hides, slim entries, data-URI tile photos; same on live 1.15).
v116 is judged as a DIFF against live 1.15: 0 new problems, [160] + [161] clean (scratchpad gate_base.txt vs gate_new3.txt).
Locks: artifact copy 856 changed = same as live 1.15 artifact copy (artifact-only slim); website copy 4 = same as v115 minus the 15 hid calls.

Local copies (this container): artifact build /home/claude/fymb116 (index.html is the only changed file; publish with Artifact url + file_path,
other files are kept); website index /home/claude/site116/index.html, pushed to fym-site-preview @80d4f0b8 (site-app/fym-v116/index.html,
jsDelivr 200).

## Independent QA (CLAUDE.md rule 2) - NOT the builder
Serve /home/claude/fymb116 (python3 -m http.server) or use the website copy via a page-block with
IDX=https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@80d4f0b8cd64ea22b209aa09bc25598484fd8c2c/site-app/fym-v116/index.html
(BASE unchanged @ad0675e4.../fym-v72/). Playwright 390px + 1440px: both doors (tiles first, mat first), colour filter switch + clear (never
locks), zoom persists across swipes, card + share, contact sheets of tile + mat photos. Plus: no Mahjong Row mat/tile/rack/set anywhere
(search 'Mahjong Row', 'Cypress', 'Ivy Reverie'); no Mahjong Co. mat (search 'The Lodge', 'Hunt Club'); Kaleidoscope tiles still there;
Gatsby / Heritage 2.0 / Smith / Osler / Sunday sets still show matches (no empty pick lists); Version 1.16 label.

## After QA passes
1. Artifact: publish /home/claude/fymb116/index.html to url 6epA9HuEdT32zUp79Qv3kd (page only).
2. Website: README step 0a pin -> IDX @80d4f0b8 (site-app/fym-v116/index.html); page-block.html IDX line; DESK 'OPS: paste FYM v116'.
3. Mat Gallery (rule 0, third place): gallery_sync.py + build_v6.py against the v116 website index -> data-fym="v116". Mahjong Co. mats go
   Retired/no button; Mahjong Row's 9 gallery mats STAY with NO code claim (autoapply-hosts.json has them ON HOLD; check build_v6 does not
   add /discount/MAHJMATCH to them) before pasting.

## r2 (Nov 6 ~8pm): @fdcc1868 = FULL 1.16, independent QA PASSED, artifact published
Website copy site-app/fym-v116/index.html @fdcc1868 (fym-site-preview). The r2 builder's b116 dir was not in the QA container, so the ARTIFACT copy was made with
builder/fym_fix_nov06/artifact116_r2.py: live r1 artifact (/home/claude/fymb116) + every field the r2 website D changed vs the r1 website D (ahid slim mats: link fields only;
rank/cr minus ahid indexes) + the Mahj Pit rack IMG script before b24v1.js; then --slim: u_plain/u_dead dropped (build metadata, 0 refs in app code) and u/u0 dropped on the
325 artifact-hidden slim mats, because the artifact version total must stay under 256 MiB (unslimmed = 268,484,358 bytes, refused). Every VISIBLE mat/rack/tile link and flag
equals the website copy (1,839 items, 0 mismatches). QA evidence: assets/qa/fym-v116-nov06/r2/. Open link findings: docs/MATCH-INBOX.md (Nov 6 8pm).
