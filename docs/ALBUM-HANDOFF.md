# 00l Album handoff: how match albums get built and kept up (Nov 19 2026)

Written by the Main chat for Claude Duet, before match album work moves to another assistant.

**What I went through:** the Album Playbook doc (Tiffany's own copy, which she edits), docs/NEW-ALBUM-CHECKLIST.md, CLAUDE.md, docs/ANSWERS.md, the album scripts and configs, the Project docs, her saved memory and chat history.

**How each rule is tagged:**
- **[T]** Tiffany told us, with the date where I have it.
- **[C]** Claude worked it out (a habit or a script default). She never said it.
- **[?]** Unsure, or two rules disagree. Ask her before relying on it.

**The two sources to read first.** Everything below adds detail to these; it doesn't replace them.
- **The Album Playbook doc:** https://claude.ai/artifact/14oGH3ovycd2xMgrHbodJZ. It is the order of operations she sees and edits. Read it at the start of every album, and add a Changelog row the same day any rule changes [T Nov 8].
- **The go-live checklist:** docs/NEW-ALBUM-CHECKLIST.md in the repo. Run it top to bottom on the day an album goes live [T Oct 26].

---

## 0. Rules that disagree. Settle these with her first

1. **How fast albums go live**
   - Nov 7 [T]: "Release the album ASAP."
   - Nov 10 [T]: one album a week. A finished album is staged on a hidden page and goes live only in its slot in config/album-launch-slots.json, with its launch kit ready. The go-live check (`album_gate --golive`, check [10c]) enforces this.
   - Nov 18 [T]: for the 12 Christmas albums, "push them as albums daily now". On Dec 12 she plans a "12 Tiles of Christmas" post; don't mention the 12 days before then.
   - Her saved memory (Nov) [T]: a finished album is held until she says release, and email subscribers must be the first to know.
   - My reading [?]: Christmas albums go out daily until Dec 12, and the one-a-week rule covers everything else. Each go-live still needs her word. The launch-slot file has only 3 entries and nothing for the Christmas run.
2. **Album size**
   - Oct 17 [T]: at least 20 matches, ideally 25–30.
   - Nov 8, in the Playbook [T]: "no set album size. If it matches, it's in."
   - Nov 18 [T]: at least 15, ideally 20+. She said this about the thin holiday albums (Grinch Green 4, Nivalee 8, Après Ski 9).
   - My reading [?]: aim for 20+, treat 15 as the floor, and never pad with weak matches.
3. **Swipe books vs. review pages**
   - Retired Nov 8 [T]: Claude picks, and she reviews on the review page ("those ended 2 albums ago").
   - CLAUDE.md still has a swipe-book gate (scripts/swipe/book_gate.py), and her saved preferences still say swipe books lead with TNT recs.
   - On Nov 18 she was sent a holiday "pick sheet" and a Mahjong by SI picks page. Those are pick pages, not swipe books.
   - My reading [?]: no swipe books. Treat the gate as legacy.
4. **Where TNT recs go**
   - Her saved preference: TNT recs (posts recommending mats in the Tiles & Tablescapes Facebook group) lead the deck, labelled "TNT rec · mat · brand".
   - The Playbook, Nov 8 [T]: in albums, TNT recs get no automatic front spot. That rule was only ever for swipe books.
   - Follow the Playbook for albums.
5. **Which chat builds albums**
   - Her memory [T]: "Albums are built in her social chat, not the reel/main chat."
   - CLAUDE.md, Nov 11 [T]: one chat (Main) does everything.
   - It's moot now that album work is moving to another assistant [?].
6. **How the review should flow (Nov 18) [T]**
   - The racks are nailed the first time.
   - She does ONE picks pass and is never sent back through the page again.
   - The final ordering happens on a grid page she can see all at once (she can't scroll 80+ matches). Then she says yes or no.
   - The current review page still supports round 2, round 3 and so on, and the Origami and Deco Indigo albums each went through two or more rounds.
   - Treat Nov 18 as the new rule [T]. The page and the steps haven't been changed to match it yet [C].
7. **Sister (pair) mat**
   - Albums, Nov 8 [T]: the sister mat is ordered like any other mat and can be #1 if it really is the best match.
   - Social [T]: the sister mat is never first, never the last card, never alone.
   - Both rules stand; they apply to different things.
8. **Amazon bring-ins**
   - The Playbook (step 10b) says Ops imports Amazon mats into ShopMy.
   - Ops (Sonnet) is still named for "moving Amazon links into ShopMy" (Nov 11) [T].
   - Whether the Ops chat is still running after Nov 18 [?].

---

## 1. Building a new album, start to finish

The Playbook steps are in brackets. Code-enforced steps name their check.

**Before anything else**
- **[0] Her yes on the tile photo** [T Nov 8]. Show her the tile pile or matching shot in chat, with the photo, as a yes/no. Log `tile_photo.approved_at` in the record.
  - Cards won't build without it (scripts/checks/tile_photo_check.py).
  - Never recolour a tile photo [T Nov 7]. Pick the photo by which colour the brand's listing attaches it to, never by eye.
  - Covers show no packaging or bags [T].
- **Wait for the brand's own page** [T Oct 19]: don't start an album until the tiles are on the brand's website. Start from the brand's photos and description, and never contradict OMM's colour words.

**[1] Tiles in Find Your Mat-ch (FYM) first** [T Nov 7]
- The FYM entry needs the tile photo, the back colour (the "walls" in Table view) and the colours.
- Add the back box to config/tableview-back-boxes-nov07.json and run `builder/table_view/back_colors_nov07.py <build> --sheet`. Look at it.
- Map the set in config/album-fym-sets.json.
- FYM gate [165] and album_gate [1] fail until this is done.
- The album tile photo is the canonical tile photo for the set: assets/tiles/album/<set>.*, mapped in scripts/swipe/canon_tiles.py.

**[2] Colour card** [T Oct 19: "colour card FIRST"]
- Order: back colour first, then layers, then face colours weighted by how many tiles carry them (bams, craks and dots count most).
- Spec: config/colorcards.json `sets.<key>`.
- Build: `python3 scripts/colorcards/build.py <key>` makes the desktop 2000x1125 and mobile 2000x3000 versions into assets/colorcards/<set>/.
- Colour wheel: scripts/colorwheel/wheel.py.
- The card's top 3 mats come from the album's standouts [T Nov 8].
- Project docs: 86 (protocol), 86b (colour card before the swipe), 96 (albums missing colour cards).

**[3] Facebook research** [T Nov 8]
- Search Tiles & Tablescapes and every other mahjong group over 30,000 members for the set name, colourway and brand.
- Scroll each search to the end and read every slide plus the full caption.
- Save config/tnt-recs.json `sets.<set>` with {scanned, source, posts_read > 0, terms[], scrolled_to_end, recs[], other_groups}, even when nothing turns up.
- Brands named in the posts go on the discovery and outreach lists.
- Enforced by scripts/checks/tnt_check.py (cards refuse to build) and album_gate [3]/[3b].
- This is done in her Facebook, in a browser. The Playbook's open question, which other groups count, was answered in practice with Mahjong Community (123K), The Mahj Lounge (46K), The Mahjong Table (37K) and Ask the Mah Jongg Teacher (36K) [C]. I don't know if she approved that list [?].

**[3b] Mat discovery** [T Nov 8]
- About 10–15 targeted searches on Google, Google Images, Etsy and Amazon, using colour, mood and motif terms.
- Always include the complementary, high-contrast side, not just tonal mats.
- Goal: at least one rare or special match per album.
- Record `discovery {at, searches[]}`.
- Finds show on the review page as "New finds", with Bring it in / Skip.

**[4] Refresh the catalog, then pull**
- `python3 scripts/albumreview/catalog_refresh.py <set>` checks every ShopMy collection, including her new Amazon pins, and sweeps the partner stores. It must run the same day as the pull (album_gate [4a]) [T Nov 8].
- Then `python3 scripts/albumreview/pull.py <set>` pulls from the whole FYM catalog plus staged adds, scored by measured colour shares.
- It starts from her own matches of the sister and similar sets [T].
- The pull must not drop pool mats that have no gallery image. That is the bug that missed Britt Mills Scarlett and Flora; album_gate [4b] checks `no_photo = 0` [T Nov 8].

**[5] By-sight pass**
- Claude looks at every candidate next to the tiles.
- Cuts go on the Left out list (in the record's `leftout`), each with a reason [T Oct 24].
- Big catalogs (Let's Be Besties, YOLO, Bougie): put only the best few in the album. The rest go in a collapsed "More from <brand>" list [T Nov 7–8]. Bougie is used only through her picks [T].
- Never in an album: Mahjong Studios mats, Mahjong Row (a removed partner), Paige Spearin x Tigre de Tartán in Holiday [T].
- A non-partner mat that truly matches goes in ("if it matches, it matches"). Partners don't score higher, but prefer a partner in the top 3 when it's close [T Nov 8].
- **Tonal rule** [T Nov 17]: navy-on-navy (tonal) is allowed. Diversify beyond tonal, but never ignore it, especially the brand's own pair mat.
- **Solid mats** [T]: match a layer colour or the complement of the back, not the back itself.
- Brand-specific always-checks:
  - Colourful mats that match many sets (OMM Enchanted, Spring Fling) get checked for every album [T].
  - OMM's pair mat must always be in the album [T].

**[6] Holiday section**
- Every album gets one [T].
- Holiday means only Christmas, Hanukkah and winter snow or ski scenes [T Oct 21].
- Holiday mats go at the bottom in their own section (`#holiday-matches`), numbered 01, 02 and so on [T].
- album_gate [6] passes with holiday cards, or with a "none fit" note.

**[7] Order** [T Nov 8]
- Colour theory decides how well a mat matches.
- Card order: standouts first, the 5–6 that make her say "ooh".
- Her past pairings and TNT recs add a little weight; their main job is catching misses.
- Motif only lifts a mat that already fits.
- Retired mats stay in the album but go toward the end, never leading [T].

**[8] Build the cards**
- Spec: scripts/albumcard/specs/<set>_<date>.json, written by a per-album builder:
  - deco_build.py for the Bam Bird Deco sets;
  - origami_build.py, juniper_build.py and others for their albums.
- Renderer: `python3 scripts/albumcard/gen2.py spec.json assets/cards/<set>`, which uses the card2.html template.
- The commands for each album are listed in the record's `card_build` field.
- Card rules:
  - **Code band:** "SAVE WITH CODE : MAHJMATCH" on every card with a partner piece (card_code_band_check.py). "No code" notes go in captions only [T Oct 18, Nov 8].
  - **Sharpness:** card_sharpness.py; album_gate [8b] [C Nov 9].
  - **Mat fills the frame:** no borders, no over-crop to the center [T]. The Nov 19 rule: crop full frame or to a corner view, never a brand's styled graphic with a background and text over it [T].
  - **Tile brand logo:** in a white tab at the BOTTOM, left of the navy mahjmatchmaker box ("gave this feedback ~10 times") [T].
  - **No drop shadows** or other effects on text [T].
  - **Card titles** follow the pattern "Deco Indigo + <mat>": no parentheses, never lead with the colourway, use "&" instead of "and", no 6-word names [T Nov 17].
- **Racks** [T Nov 8, Nov 17]. Lower left = racks that match the tiles; upper right = racks that match the mat.
  - Order of choice: the tile brand's own matching racks first, then that partner's racks, then any brand.
  - Proportional lengths, using config/rack-lengths.json.
  - Before picking, check what's new (Brand Watch and partner stores).
  - Lean on partners with big rack lines (Anders Ruff, Mahjong Register). No Etsy racks.
  - Once a mat's racks are approved, they are that mat's racks on every card, and they're never re-asked [T].
  - Never render an OMM rack; Bird & Bamboo is the only rack drawn, from its colour gallery [T].
  - Rack length: no 18.5" OMM or Mahjong Row racks with oversized tiles [T].
  - Nov 17 rack calls [T]:
    - no black racks on year-round mats;
    - Bam Bird Indigo instead of Mahjong Register Navy (except Midnight Garden);
    - B&B Wine is oxblood;
    - Peace Love Acrylic Burl, not OMM Burl;
    - reds only on holiday mats;
    - Middle & Main Milk Glass instead of B&B White;
    - B&B Provincial and Dark Walnut are banned finishes.
  - Commission rule: on non-paying brands' albums (e.g. Sunday Mahjong), commission-earning racks go on the tile side [T].
- Tile racks for each set: config/colorcards.json `racks` and config/tile-racks-picks.json [C].

**[7 faces] Favorite faces**
- Claude pre-picks 5, from the brand's limited-faces shot at the highest resolution available [T Oct 19].
- Cutouts: scripts/colorwheel/cut_faces_*.py into assets/tiles/faces/<set>/clean/.
- Graphic: scripts/colorwheel/favorites.py, which makes favorites-<set>.html.
- album_gate [7].
- Sister colourways share their faces (all three Deco colourways use Lagoon's picks) [T Nov 17].
- Spelling: "favorite", never "favourite" [T Nov 17].

**Covers**
- Regular albums: scripts/covers/album_cover.py; uniform restyles: scripts/covers/uniform_v2.py; holiday: scripts/covers/holiday/; Origami: scripts/covers/origami/.
- Every cover has the tile brand's logo above the title [T].
- Her yes on the cover comes on the review page ("Cover · tap to pick").

**[9] Review page**
- `python3 scripts/albumreview/build_review.py <set> [outdir]` writes index.html and files.json. It refuses unless album_gate passes and selftest.py passes.
- Publish it as a claude.ai artifact with the files map and the db capability `{db:{rules:[{path:"",read:"view",write:"admin"}]}}`.
- Save the URL in the record's `review_url`. Older ones go in `old_review_urls`.
- Mid-review changes [T]: don't touch the page while she's reviewing. Send changes as a new round instead (it costs her place otherwise).
  - Exception: a fix she asks for directly, like the Nov 19 Gold Fans crop. Swap only that card's file in place [C].

**[10] Apply her answers**
- Read the saved doc with ArtifactData: `get url=<review page> collection=review doc_id=<set>`.
- Then run `python3 scripts/albumreview/read_review.py <set> <file>`.
- "A yes is a yes": never re-ask [T Nov 4].
- Her round notes sometimes say "notes only, apply after I'm done" (Deco Indigo, Nov 17). Respect that [T].

**[10b] Bring-ins**
- Every mat she brings in gets a paid link before go-live, tracked in the record's `bringins` list (scripts/albumreview/bringins.py):
  - **Etsy:** a ShopMy link, filed in an "(Etsy)" collection.
  - **Brand site:** the code link, or ShopMy where it pays more or the brand isn't a partner.
  - **Amazon:** saved in Associates, then Ops imports it to ShopMy.
- Then it goes into the catalog: FYM staging plus the Mat Gallery.
- `album_gate --golive` [10b] blocks go-live otherwise [T Nov 8]. docs/LINK-ROUTES.md has the routes.

**Final view**
- scripts/albumreview/final_view.py <set> <out.html> makes a read-only page: album order, 5 across on a phone [T Nov 17].
- The Nov 18 ask is a grid for the final ordering. The current page has a Grid toggle; there is no separate grid-only step yet [C].

**[11] Stage it hidden, give it a slot, build the launch kit**
- Assign the week in config/album-launch-slots.json [T Nov 10].
- **The album page**
  - Duplicate the most recent live album page in Squarespace (Juniper was the template for Deco Lagoon). It goes live as "(Copy)" right away, so set it Not Linked or hide it at once [C].
  - Set the title, slug, SEO title and SEO description through the Squarespace API (Project doc 59 §4).
  - Paste the code block.
- **The code block**
  - Built by site/livepatch/<set>-album-<date>/build_block.py, which copies the LIVE previous block (CSS, hero, FAQ + JSON-LD, the Colors & racks guide, a lightbox with the pinch fix, the Pinterest script).
  - Order: colour card first [T, doc 86b], then cards in her order, then the holiday section.
  - Images are pinned to a commit on jsDelivr and warmed. The code block is pinned too.
  - Paste with the CodeMirror dispatch method, and check that the doc length equals the file length [C].
  - Check with curl: 200, the card count, every image 200, no leftover old album name. Run `scripts/checks/holiday_numbering.py`.
  - Example README with every step: site/livepatch/deco-lagoon-album-nov08/README.md.
- **Launch kit [11b]** [T Nov 11], built before the launch week as Planoly drafts (each with an every-slide story and a Facebook Page target):
  1. The catalog carousel, posted first.
  2. The single-brand "It's a mat-ch!" share card, made for the brand to reshare. No circle-in-circle.
  3. The reel, built in Canva as far as Claude can take it: its own folder, slides in order, several music ideas.
  - Plus: the FB group announcement (Project doc 82 format), the "new albums are live" email (template `new-albums` in site/email/build.py, a Squarespace campaign) and the album-request emails (doc 54).
  - Captions come only from scripts/social/plain_post.py: facts, no cute copy [T Nov 10].
- **[11c] Last step** [T Nov 11]: tell her the reel is ready to finish only when everything else is done. She finishes the reel while Duet checks every other step.

**Go-live day** (NEW-ALBUM-CHECKLIST §2)
- Publish the page.
- /mahjong-tile-matches:
  - add the album first in "Our Latest Albums" (newest first) [T];
  - add it to the end of its colour grid [C].
- Colour page (e.g. /blue-mahjong-tile-matches): put the album's colour card first [C, as done for Deco Lagoon]. Albums may appear on more than one colour page when that helps people find matches [T Oct 2026].
- /links: the "latest album" card goes second; FYM stays first (scripts/covers/holiday/links_build.py) [T].
- The brand's /<brand>-discount-code page: add the album to its albums list.
- Request Google indexing.
- HQ Albums row; Pinterest queue (config/pinterest/queue.json).
- Retired OMM vault sets go into the colour sections as if they'd always been there, never as "latest" [T Oct 18].
- Social and email per the launch kit.

**[12] Find Your Mat-ch**
- Her final picks become the set's "Tiffany's match" list (`m`), and the set links to the album, in the next FYM release.
- Use a small per-album script, e.g. builder/fym_fix_nov08/deco_lagoon_m119.py.
- Her saved preference (Nov 18) [T]: no FYM update goes live without her preview and yes. See the conflict list in the FYM handoff (doc 00k).

---

## 2. Updating an existing album

- **Add or remove a mat**
  - Edit the album's spec (scripts/albumcard/specs/<set>_*.json) or apply her review answers with read_review.py.
  - Rebuild only the changed cards: filter the spec to the card(s) and run gen2.py. Rebuilding everything can sweep in other pending changes [C].
  - Rebuild the code block (build_block.py), re-pin to the new commit, warm jsDelivr, re-paste and curl-check.
  - Update the FYM `m` list in the next release.
  - Mats added after she finished are flagged `added_after_review` and land in a "New since you finished" box [C, build_review.py].
- **Re-order:** her order lives in the review db (`order.main` / `order.hol`). read_review.py writes it to the spec, then rebuild the block.
- **Retired and vault**
  - Retired mats stay in, marked Retired, toward the end [T].
  - Retired = the product page is gone, never just sold out (Project doc 90) [T Oct 19].
  - Every retired tile set is flagged "Retired"; don't single some out as "From the Vault" [T Oct 18].
  - Vault albums take any brand's mats; she adds them as she spots them, with no big pull [T Oct 19].
  - Vault pages: site/livepatch/albums/ (build_vault.py; README has the page steps).
- **Holiday albums**
  - Christmas sets get their own holiday albums and appear in the holiday sections on /holiday-mahjong-matches. Run holiday_numbering.py after any paste [T Nov 4].
  - Nov 11 [T]: no new Christmas albums for brands that don't have one (Mahj Pit Merry Merry was the exception she made). Newer partners' holiday mats still go into the existing holiday albums.
  - Nov 18 [T]:
    - 12 Christmas albums, pushed daily;
    - Grinch Green, Nivalee and Après Ski need 15+, ideally 20+;
    - every Etsy holiday mat goes in;
    - Soirée All Day's painterly Christmas tree mat (her favorite) goes in the holiday albums;
    - Dear Santa should have about as many as Rackin' Rudolph;
    - a Spirit of Christmas album goes to her for review.
  - Pick sheet: https://claude.ai/artifact/Wb8hHKV7d217u19UNReQTo (scripts/albumreview/holiday_nov18/build_picks.py + candidates.json; her answers are saved in the db at picks/holiday-nov18).
  - Holiday page builders: site/livepatch/holiday-backlog-nov17/build.py and the earlier holiday-fix-nov09 / holiday-qa-nov09 folders.
  - I'm not sure which of the 12 Christmas albums are live and which are staged [?]. Check /holiday-mahjong-matches and the album calendar.
- **Thin albums:** site/livepatch/thin-albums-oct26 (Oct 26 work) [C].

---

## 3. Scripts, templates and files: where each lives

**GitHub repo** tiffanybrie/mahjmatchmaker-data, branch `partner-catalogs-sqsp`, unless noted.

| What | Where |
|---|---|
| Album record, one per album (proof for steps 1–8, faces, covers, review URLs, bring-ins, card build commands) | config/album-records/<set>.json (read its `_about`) |
| Gate (steps 1–8; `--golive` adds 10b/10c) | scripts/checks/album_gate.py |
| TNT check / code band / sharpness / tile photo | scripts/checks/tnt_check.py, card_code_band_check.py, card_sharpness.py, tile_photo_check.py |
| Catalog refresh, pull, review page, apply answers, bring-ins, final view, calendar | scripts/albumreview/{catalog_refresh,pull,build_review,read_review,bringins,final_view,album_calendar,fym_images,selftest}.py + review_template.html |
| Card renderer + template | scripts/albumcard/gen2.py + card2.html; rack helpers racks.py, real_racks.py, matpick.py, rack_body.py |
| Per-album card builders and specs | scripts/albumcard/specs/*_build.py + *_<date>.json (deco, origami, juniper, cabana, kerry, larkspur, papaya_spritz, december_1994, brownstone_bloom, jasmine…) |
| Holiday card builders | scripts/albumcard/gen_hol*.py, hol_page.py, holiday_*.json |
| Cards (output) + manifest | assets/cards/<set>/ |
| Colour cards | scripts/colorcards/build.py; config/colorcards.json; assets/colorcards/<set>/ |
| Colour wheel + favorite faces | scripts/colorwheel/{wheel,favorites,cut_faces_*}.py; assets/tiles/faces/<set>/clean/ |
| Covers | scripts/covers/{album_cover,album_cover_omm,uniform_v2}.py, scripts/covers/holiday/, scripts/covers/origami/ |
| Canonical tile photos | assets/tiles/album/<set>.*; map scripts/swipe/canon_tiles.py |
| Album page code blocks + README per launch | site/livepatch/<set>-album-<date>/ (build_block.py, codeblock.html, README.md) |
| Vault album pages | site/livepatch/albums/ |
| Album lineup / calendar pages | site/livepatch/album-lineup/, site/livepatch/album-calendar/ |
| /links builder | scripts/covers/holiday/links_build.py; assets/links/v2/ |
| Launch slots / release calendar | config/album-launch-slots.json; config/release-calendar.json (+ scripts/release_calendar/) |
| TNT recs | config/tnt-recs.json |
| Album to FYM set map | config/album-fym-sets.json |
| Plain captions | scripts/social/plain_post.py; docs/social/PLAIN-POSTS.md |
| New-album email template | site/email/build.py (`new-albums`); docs/EMAIL.md |
| Go-live checklist | docs/NEW-ALBUM-CHECKLIST.md |
| Older process notes | docs/86-new-album-protocol.md, docs/album-process-oct24.md |
| Holiday pick sheet builder | scripts/albumreview/holiday_nov18/ |
| **Rescued today from my scratchpad** (Deco pull/spec/crop helpers, Juniper order data, Sunday swipe-book shots, holiday page check) | scripts/albumcard/rescued-from-scratchpad-nov19/ (README inside). One-off; the standard pipeline doesn't need them |

**Claude artifacts** (claude.ai, private):
- the Album Playbook: 14oGH3ovycd2xMgrHbodJZ;
- each album's review page (URL in its record);
- the holiday pick sheet: Wb8hHKV7d217u19UNReQTo;
- HQ: Cor6pKtesou4mFRQ41P6Ye.

Her review answers live in each artifact's database (collection `review`, doc `<set>`). The review page is the only copy of those answers until read_review.py has applied them, so apply them promptly [C].

**Project docs** (the Mahj Matchmaker Project):
- 00a Brand guide (read before any design);
- 86 / 86b album protocol;
- 89 Instagram row rule;
- 82 FB group post format;
- 54 album-request emails;
- 59 Squarespace API;
- 90 retired vs. sold out;
- 96 albums missing colour cards;
- 00e album and content plan.

**Lost already** [C]: the Oct 7–18 colour-card generator lived in /home/claude/newalb/ in an earlier session. scripts/colorcards/build.py replaced it on Oct 19. Other sessions' scratchpads (e.g. the session that built Deco Indigo round 2, Origami Timber and the holiday pick sheet) can't be reached from here. Anything that wasn't committed there is gone, but the commits show the pipeline scripts were committed [C].

---

## 4. Sign-ins, tools and accounts

| Tool | What it's for | How it's reached |
|---|---|---|
| GitHub (tiffanybrie/mahjmatchmaker-data) | Everything above | The session's git access |
| jsDelivr | Serves the pinned images and code blocks for album pages; no account | Pin to a 40-character commit, then "warm" (fetch every URL once). Single files over 20 MB are refused |
| Squarespace (mahjmatchmaker.com) | Album pages, Latest Albums, colour pages, /links, brand pages, email campaigns | Her signed-in browser (Claude in Chrome or the built-in browser). Never type passwords. One Chrome driver at a time; close every tab [T] |
| Facebook | Tiles & Tablescapes and the other big groups (step 3); the group announcement | Her signed-in browser. Posting needs her yes [T] |
| ShopMy | Paid links for Etsy and non-partner bring-ins; "(Etsy)" collections | Her signed-in browser |
| Amazon Associates | Amazon bring-ins, tag heritagesig05-20 | Ops / her browser |
| Planoly | Launch-kit drafts, IG workspace 019fc27c-0bef-7533-bc3f-030acc19a135 plus the FB Page channel | Planoly connector |
| Canva | The album reel (own folder per album, like Juniper) | Canva connector |
| Dropbox | Her "Mahj Matchmaker Albums" folder; new-release images saved as soon as they appear | Dropbox connector / her computer link |
| Google Search Console | Request indexing for each new album page | Her signed-in browser |
| claude.ai artifacts | Review pages, pick sheets, final view, Playbook | The Artifact tool; answers read with ArtifactData |
| Etsy / brand stores | Product photos (brand's `/products/<handle>.json` for every image) | Public web |

---

## 5. Done by habit, never written down (all [C])

1. Read the live previous album block and copy it as the template for the next one, rather than starting from a template file. That keeps fixes like the lightbox pinch fix.
2. Re-render a single card by filtering the spec to that card (gen2.py on a one-card spec), so a fix doesn't rebuild 50 cards and drag in pending changes.
3. Swap one file on a review page in place with an Artifact `files` publish (after reading it), so her saved taps and her place aren't disturbed.
4. Crop the source mat photo itself, not just the card, so the clean version flows into FYM and the gallery too.
5. After pasting a code block, compare the length of what's in the Squarespace editor with the file, then curl the live page: card count, every image 200, no old album name.
6. Name card files `<set>-mahjong-tiles-<mat-slug>-mat.jpg`. The review page and the gallery key off that pattern.
7. Before blaming a brand's site for a missing mat or a dead link, re-check with and without www, and in a real browser (now her rule for partners) [T Nov 8].
8. Keep sister colourway albums (the Deco trio) consistent: same faces, same card title pattern, same tile-rack logic.
9. Pick `lowres` mats deliberately and tag them "Small brand photo" on the review page, so she knows why a card looks soft.
10. Log every answer of hers in docs/ANSWERS.md before replying, and put anything not finished today in docs/OVERDUE.md. These are written rules; I'm listing them because they're the parts that slip most [T].
