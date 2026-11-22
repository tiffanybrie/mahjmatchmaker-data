# Find Your Mat-ch: how products get chosen (handoff, Nov 19 2026)

Written by the Main / Matches chat for Claude Duet, before FYM product work moves to another assistant.
Sources: repo CLAUDE.md, config files, the gate (builder/fym_gate.py), docs/ANSWERS.md, saved memory and chat history.

**How to read the tags**
- **[T]** Tiffany told us, with the date where known.
- **[C]** Claude worked it out (a habit, a script default or an inference). She never said it.
- **[?]** Unsure, or two rules conflict. Ask her before relying on it.

The gate numbers in brackets (e.g. [140]) are the checks in `builder/fym_gate.py` that enforce a rule.

---

## 0. Rules that conflict, or that she should confirm first

1. **Shipping: preview first, or straight in?**
   - Nov 10 [T]: "ship continuously, never hold for a big release", the same day (CLAUDE.md 0b).
   - Nov 18 [T]: "No Find Your Mat-ch update goes to the live app without her seeing a preview first and saying yes; no open-ended yes to ship."
   - Nov 19 [T], newest: "New products/images in FYM and the Mat Gallery go live under the documented rules with no yes from her." She also wants a "what went into the app this week" page she can browse, which never holds anything back.
   - My reading [?]: catalog adds that pass every rule ship without her. Changes to how the app looks or works (like the 1.23 layout) need her preview and yes. Confirm with her.
2. **How many items a big-catalog brand gets per run.**
   - Nov 11 [T]: 10 products per brand per coverage run.
   - Nov 12 and Nov 17 [T]: about 50 items per brand per release, until she says otherwise.
   - [?] Both are on file and are probably different limits (per nightly run vs. per release). Unconfirmed.
3. **The per-brand cap in suggestions.**
   - Gate [140] (Nov 1 [T], after Let's Be Besties flooded the decks): at most 6 of the first 30 from one brand, never two in a row.
   - The private 1.23 catalog build caps Besties at 2 of the first 30 [C]. I can't find her saying 2. Treat 6 as the rule and 2 as a build choice.
4. **Splash of Color.**
   - Oct 26 [T]: pulled from FYM entirely, except the Splash mats on her own album matches (gate [67]).
   - Nov 11 [T]: whole inventory comes in, mats only, never tile sets, at half weight.
   - The Nov 11 rule is newer, so it's the one in force [C].
5. **Mahjong Studios.**
   - Oct 20 [T]: tiles and racks stay; every mat is out.
   - Oct 26 [T]: pulled from FYM "entirely for now".
   - Nov 11 [T]: given half weight, which only makes sense if their tiles are in.
   - [?] Whether their tile sets are visible today: check the live build before assuming.
6. **Racks to finish.** Nov 18 [T] she wrote "Pick 2 racks to finish". The app has always allowed finishing with 1 rack. Asked her Nov 18; no answer yet.

---

## 1. What gets in, and what keeps something out

### Who is allowed in at all
- **Partner brands only** [T Oct 20]. The partner list is the live /mahjong-discount-codes page (live plus "code coming soon") together with config/partners-pipeline.json [T Nov 11]. Removed brands (code-truth `removed_brands`, e.g. Mahjong Row & Co.) are not partners [T Nov 6] (gate [160]). Why: brands need a reason to sign up as affiliates.
- **Allowed non-partners** [T], listed in builder/fym_flags/nonpartner_allow.json; gate [9] fails on anything else:
  - Sunday Mahjong, whole line (her favorite).
  - Ozark Mahjongg, whole line.
  - Tala Mahj: only the 11 mats in her ShopMy "Tala Mahj Favorites".
  - Any ShopMy-linked mat (go.shopmy.us).
  - Mahj Tile Haus: only mats she matched, plus Imperial Lotus.
  - Mahjong Moxie: Duck Camp and Heron Landing only.
  - Mahj & Moon: the 4 fuzzy album mats.
  - Silk Mahjong: matchable mats including leatherettes [T Nov 8].
  - Any mat on her match lists or albums.
- **Never pull a non-partner's whole line** because she matched one of their mats [T Oct 20].
- **Catalog rule from Nov 8** [T]: a brand with no affiliate program gets its whole mat line in. A brand that has a program is held until she's approved, and then its line comes in.
- **Code first, then products** [T Nov 11]: a partner's products don't enter until its code works. Otherwise the app fills with plain links that earn nothing (gate [172b]; partner_coverage shows these as HELD).
- **Approved means on the codes page the same day**, plus in the partner pipeline [T Nov 11].
- **ShopMy picks** [T Oct 26]:
  - Etsy mats are curated, so they can go in.
  - Amazon mats go in only when she picks them.
  - A non-partner mat goes in only if she'd actually match it.

### Brand-specific blocks and exceptions
- **Mahjong Studios:** no mats anywhere [T Oct 20] (gate [12]). Their mats sort to the bottom of everything, and duplicate "Ships Rolled" listings are hidden [T Oct 20].
- **Splash of Color:** mats only, never tile sets [T Nov 11 5:13pm]. Far-away living-room renders are out [T Oct 25] (gate [50]).
- **Mah Jongg Maven tile sets** [T Nov 11 5:27pm]:
  - One per colour: drop a 2-layer set when an identical 3-layer colour exists.
  - No novelty or character sets (Peanuts, Coca-Cola, Siamese cat, koi, flamingos, dolphins, butterflies, leopard).
  - No multi-colour sets or bundles. Classic Ivory skipped.
  - Gray or dim photos get cut out or brightened without changing the tile colour.
  - Black sets first, because the app has no black tiles.
- **Mahj Tile Haus, Mahj & Moon, Hutch & Nook, Luxe, Maison Mahj (The Chalet only for now):** only the mats she matched [T Oct 20]. Note that Maison Mahj is a full partner now [T Nov 13] and its newer releases were flagged missing, so this rule may be out of date [?].
- **Removed outright** [T Oct 20]: The Mahjong Line, Mahj House Rules, and every Four Winds Social mat. The FWS x Mahj Mood collabs stay, filed as Mahj Mood.
- **Mahjong Co. mats** are hidden: retired, shop empty [T Nov 6] (gate [161]). Their Kaleidoscope tile set stays [T Oct 26].
- **Mini Mahjer** stays out: no mini or travel items in FYM [T Oct 15, Oct 26].
- **Paige Spearin x Tigre de Tartán collabs** earn no commission. They stay in the library but are never promoted or added to Holiday [T].
- **Bespoke:**
  - No Mega/XL sets [T Oct 23].
  - Double-sided mats are listed twice, one entry per side with one photo each [T Oct 26] (gate [78]).
  - Their "Mahjong Sets" product type includes $0 swatches and $4,250 table bundles. Real sets cost $380–590 [C, docs/catalog-naming-traps.md].
- **Mahjong Register:** no rack photo that shows a stack or an infographic [T Oct 26] (gate [92]).

### What counts as a product
- **No travel or mini** mats, tiles or racks [T Oct 15].
- **Same design, different material** (e.g. Britt Mills neoprene vs. leatherette) is one listing with an "also available in" note [T Oct 15]. Exception: Bespoke double-sided mats, which are two entries.
- **Tile sets** = partner brands plus any set she has matched in an album [T Oct 23].

### Photos (the most common reason something stays out)
- **The FYM bar is low** [T Oct 21]: the photo only has to show that it's a mat and let you match its colours. Tiles, racks, props or a room around it are fine.
- **What gets an item hidden:**
  - Too far away [T Oct 21] (flag `too_far`; gate [50]).
  - Pattern covered by tiles or racks (`covered`).
  - Packaging, a close-up of one corner, or a different product [T].
  - Watermarks across the mat [T]. Mac + Miller watermarked photos are allowed only inside cropped match cards [T].
  - A personalised sample, an ad graphic, card-game mats, duplicates [T Nov 17, docs/FYM-PHOTO-PROTOCOL.md].
  - Tile sets without backs, or with tiles too small to see [T].
- **Solid and vegan-leather mats** get a lower bar: even a rolled or angled shot shows the colour [T Oct 21].
- **When in doubt, pull it** and put it on her Questionable list (builder/fym_flags/fym_questionable.json) [T Oct 21] (gate [3d]).
- **Before hiding an item, look at every photo on the listing** (`/products/<handle>.json`) for a better one [T Oct 21, Oct 30, Nov 11]. Her words: "you can't just say you don't have a photo and not go to the website, look through all the photos" (gate [106]).
- **Room shots and wide margins get cropped** to the mat, and the colours are re-measured from the crop [T Oct 25] (gate [50]). A mat fills the frame with no white bands [T Oct 26] (gate [89]). A corner view must fill the whole square [T Nov 2] (gate [147]).
- **Nov 19 1:09am [T]:** the source photo must be cropped full frame or to a corner view. Never the brand's styled graphic with a background and text over it. Example: the Dreamframer Gold Fans mat with a "With Rules" box over it.
- **Tile photos must show tiles** with a back and layers plus faces at default framing [T Oct 20]. If the set has an album, use the album's photo (`assets/tiles/album/<set>`) [T Oct 20].
  - Brand-specific framing [T Oct 25–26]: Bam Bird faces|backs split (gate [58]); Charleston (gate [64]); Yellow Mountain (gate [63]); no Bespoke set on a dark background (gate [65]); PLM and My Fair Mahjong fill the circle (gate [66]).
  - Real brand photos only; never paste tiles in [T Oct 25].
- **Every rack photo is checked by eye on white and on navy** before it shows [T Oct 23, Oct 25] (gate [56]).
  - Horizontal racks only, never portrait [T Oct 26] (gate [70]).
  - One rack per photo, not a stack [T] (gate [73]).
  - Wood racks show real grain, never a flat fill [T Nov 3] (gate [154]).
- **Locks** [T Oct 20]: approved photos, crops, names and match lists can't be overwritten by a scrape. New items only go into a pending queue (builder/fym_flags/locks.json; "changed locked" must be 0).

### All or nothing (Nov 11, [T])
An item goes visible only when it's ready in every view and filter:
- photo flags, colours, Table view (tile walls, mat class, rack decision);
- price, card colour, link route and code.

A grayed-out Table view is fine only after every listing photo was looked at, with a reason that names what was checked. Table view uses the real mat photo, never a flat colour fill [T Nov 11]. Retired or sold-out pieces stay in and need no price. Anything without a price must be marked retired (gate [173], scripts/checks/fym_all_or_nothing.py).

### Partner coverage
- A partner counts as covered only when its whole store is in: every full-size tile set and mat, with 0 missing in partner_coverage.py [T Nov 11].
- Every partner store is watched, whether or not it's on Shopify [T Nov 11].
- **Non-Shopify partners** [T Nov 19]: Amanda Toppe, Wren Mats and Soirée All Day. Do one full manual check, then use their newsletters and social as triggers, plus a light site check about every 2 weeks. Never ask a brand whether they've added anything.

---

## 2. How Find Your Mat-ch suggests

**Two different things, one word each (Tiffany Nov 21 6:17pm).** SUGGESTIONS = how the app decides which mats, tile sets or racks it shows for a pick and how it sorts them. This section covers only that. ALBUM ORDER = the order she puts match cards in when she builds an album (1st, 2nd, 3rd). That is her decision per album and lives in the Album Playbook, not here. They touch in one place: for a tile set that has an album, with "Tiffany's Picks" turned ON, her album picks are shown in her album order; everything else is sorted by the suggestion rules below. "Rank" is not used for album order anywhere in this document.

**Her statement of how the app suggests (Nov 21 6:21pm), in order:**
1. Suggestions are based on what MATCHES the tile set.
2. Her picks appear ONLY when "Tiffany's Picks" is turned on; then they are included, in her album order. When it is off they do not lead.
3. The brand's own coordinating mats for that tile set are suggested.
4. Caps: a brand with a big catalog (Mahjong by SI, Splash, Besties, Maven) never gets more suggestions because it has more mats.
5. Use colour theory (Nov 21 6:31pm). Two ways a mat matches: tone on tone (one shared colour), and coordination across dominant colours (two or more of the mat's dominant colours each matching a dominant part of the tiles: back, layer, or dominant face colour). Coordination across dominant colours is the stronger match and goes ahead of a run of single-colour matches. Only colours that are substantial in the mat count: visible from a distance, not a small detail. No hard quota or forced variety rule: "let it do its thing and not white knuckle it into breaking". Learn from the first few cards of her albums.
6. Album order is separate and not covered here.

### Mats for a tile set (tiles first)
- **Colour theory decides** [T]. Order of what feeds the score:
  - The tile back colour weighs heavily [T Oct 26 11:37am: "The back color is a dominant color"] (gate [76]).
  - Then layers.
  - Then face colours by how many tiles carry them [T, colour card protocol].
- **"Tiffany's match"** comes only from her real picks (an album, or a swipe-book yes) [T Oct 20]. Catalog sets carry `m=[]`. Her picks are shown, in her album order, ONLY when "Tiffany's Picks" is on; with it off they do not lead [T Nov 21].
- **A brand's coordinated mats come first** for its own tile set (config/fym-coordinated.json) [T Oct 25] (gate [57]).
- **Partner brands keep priority over ShopMy-only items** [T Oct 26] (gate [74]).
- **Per-brand cap:** at most 6 of the first 30, never back to back [T Nov 1] (gate [140]). See conflict 3.
- **Brand weights** (config/brand-weights.json) [T Nov 11]:
  - Splash of Color, Mahjong Studios and Yellow Mountain Imports get half the slots and a stricter match bar ("if it matches, it's got to really match").
  - Maven and Mahjong by SI are at normal weight for now.
  - Weights change only on her word.
- **Big-catalog brands** (Splash, Let's Be Besties, Mah Jongg Maven, Mahjong by SI; config/curated-brands.json) [T Nov 11]:
  - Their whole inventory is searchable by name.
  - They must never crowd suggestions.
  - Their tile sets rank below other partners' sets.
  - Nov 17 [T]: Besties' value is that someone can search an obscure mat by name and find it. Beyond that they must not over-suggest.
- **Mahjong Studios mats** sort to the bottom of every deck (moot while their mats are out) [T Oct 20].
- **Retired mats** stay in but never lead; they go toward the end [T].
- **Holiday:**
  - Only Christmas, Hanukkah and winter snow or ski scenes count [T Oct 21 FINAL]. Fall, Halloween, Valentine's, patriotic and Derby are not holiday.
  - Holiday mats are left out of the DEFAULT results for a regular (non-holiday) tile set and never sit in single-colour chips. BUT whenever the person filters or searches for holiday mats, holiday mats are shown for ANY tile set, sorted by how well they match that set (e.g. Amara tiles + the holiday filter shows holiday mats matched to Amara). "We actually promote matching your own tiles to holiday mats" [T Nov 21 6:07pm].
  - Two exception lists, added only on her word: `also_year_round` and `works_for_holiday` (flags `ayr` and `wfh`) [T Oct 21].
- **Luxe Polo Club:** whenever it's suggested, also suggest Mahjong by SI Ralph [T Nov 17].

### Colour chips (browsing by colour)
- Her `lead` mats come first in her order. Then everything by score: the measured share of that colour, plus 20 if it's the mat's primary colour. Her `tail` mats go last [T Oct 20] (gate [8b]).
- Blue = blue + teal; Dark = dark + earthy [T].
- Never add a colour a mat doesn't visibly have. Album colours are only a hint, used where they measure 5% or more [T Oct 20].
- Cream or ivory backgrounds are not yellow [C, from a QA bug Oct 31] (gate [120]).
- Her colour calls always win and are locked (config/tiffany-color-notes/2026-10-20-late-calls.json) [T].

### Tile sets for a mat (mat first)
- Ranked by colour against the mat. Holiday tile sets only for holiday mats [T Nov 7] (gate [168]).
- "Photo coming soon" sets sort to the bottom [T Oct 26] (gate [61]).
- No default colour chip; the tile list runs A–Z when nothing is picked [T Oct 26] (gate [59]). The tiles door doesn't open on the alphabetical list [T Oct 30] (gate [105]).

### Racks
- **Racks follow the tile brand first, then the mat brand** [T Oct 26] (gate [75]).
- **Lower-left racks match the tiles; upper-right racks match the mat** [T].
- **Among equally good racks, the best-photographed one leads** [T Oct 26] (gate [60]). A poorly photographed rack never leads [C, QA] (gate [81]).
- **Rack length:** OMM and Mahjong Row racks are 18.5" and fit OMM-size tiles only. Never suggest them for oversized sets (Sunday, Miss Mahjong, Mahj Tile Haus). She recommends 20" racks generally [T].
- **Oh My Mahjong racks** are not recommended with other brands' tile sets. They ARE recommended for Oh My Mahjong's own work: an OMM tile release and above all an OMM album; with OMM mats they may be included. Outside OMM work, leave them out [T Nov 21 6:08pm, replaces "never suggest OMM racks in new work"]. Use Peace Love Acrylic Burl, not OMM Burl, outside OMM work [T Nov 17].
- **Tortoise leads with Middle & Main Hawksbill Heritage** [T Oct 25] (gate [52]).
- **Locked racks show their approved photo** [T Oct 26] (gate [94]).
- **Album rack rules are separate** from FYM, but she expects them to agree:
  - No black racks on year-round mats.
  - Bam Bird Indigo instead of Mahjong Register Navy.
  - B&B Wine is oxblood.
  - Reds only on holiday mats.
  - (Nov 17 [T], in ANSWERS.)

---

## 3. Prices, links, stock, sold-out and retired

- **Link routes** (config/link-routes.json, docs/LINK-ROUTES.md) [T Nov 8]. Every shop link is paid one of five ways:
  - `code-site`: the brand's own store, with an auto-apply `/discount/MAHJMATCH` link where the host supports it [T Nov 6] (gate [159]).
  - `shopmy-site`, `shopmy-etsy` or `shopmy-amazon`.
  - `none`.
  - A brand with no row fails the gate (gate [172]).
- **Route exceptions:**
  - Charleston goes through ShopMy (15% vs. 10%), and MAHJMATCH still shows on the card [T Nov 8].
  - Bam! Let's Mahjong stays `code-site` until she decides [T].
  - Mahj & Moon goes to Etsy through ShopMy only [T Nov 8].
  - Sweet Jojo uses Amazon affiliate links only [T].
  - LoveShackFancy collab items: no code, plain link [T].
- **Code pill:** MAHJMATCH appears on every card that has any partner piece, with no hard-coded percentage [T Oct 18, Oct 20]. Link-only brands (e.g. Tigre de Tartán) never get the code pill or the ♥ code mark [C, QA Nov 1] (gate [139]). Tigre de Tartán's code is shown as an image on the site, never as text [T].
- **Retired vs. sold out** [T Oct 19, project doc 90]:
  - Retired = the product page is gone (404, or missing from the store's product list) or the brand says it's discontinued. Only then.
  - Sold out = the page exists but nothing is available. Keep it linked; brands restock (OMM Holly Jolly did; Sunday sets come back).
  - Never mark something retired from one missed scrape.
  - Re-check retired items, and un-retire them if the page comes back (gate [162b]).
- **Retired and sold-out items stay in FYM** on purpose: people own them [T]. Retired items need no price. "(retired)" never prints on the match card [C, QA] (gate [117]).
- **Price filter:** "Under $X" must not silently hide mats with no price [C, from an audit Nov 7] (gate [166]).
- **The In stock chip** is off by default and never empties a deck silently [T Nov 1] (gate [138]).
- **Stock is re-checked from every partner store** before a release [C, habit; done Nov 17 for 1.20]. Product pages that 404 are kept as-is until confirmed retired [C].
- **Every FYM release also rebuilds the Mat Gallery and the site search** from the same build [T Nov 6] (gates [90], [159b]). A weekly `--links` check finds dead shop links [C].

---

## 4. Brand quirks

- **Oh My Mahjong:**
  - Every tile set has a pair mat (search "<tile> starter kit"). The pair mat is a match but never leads or ends social content [T].
  - Retired OMM tile sets stay in, marked Retired [T Oct 18].
  - OMM drops sold-out pieces from its own site, which is why we keep them [T].
- **Bam Bird Boutique:** "Deco" means their Deco set (Lagoon, Mulberry, Indigo), not OMM's Lagoon [T]. Tile photos are a faces|backs split [T].
- **Bespoke:** no Mega/XL; double-sided mats listed per side; no tile photo on a dark background [T].
- **Britt Mills and Amanda Toppe:** mats only, artist brands, and "we better have them all" [T]. Britt Mills has neoprene and leatherette versions of the same design: one listing [T].
- **Let's Be Besties:** big catalog, searchable by name, capped in suggestions. Its owner is friendly [T].
- **Mah Jongg Maven:** see the tile rules above. Feature its designer sets; never call it "the affordable brand" [T]. It is not MahjjMaven, an Etsy shop [T].
- **Mahjong by SI:** big catalog; every mat comes in 4 formats (one listing). Planned for 1.24 as a search-only catalog [per Duet's status; I haven't seen her say "search-only" ?].
- **Mahjong Register:** no stacked or infographic rack photos [T]. Her favorite mat is "The Peppi" [T].
- **Miss Mahjong:** a new tile set is huge news. Racks are more in demand than mats [T Nov 11].
- **Maison Mahj:** MAHJMATCH gives free shipping on tile sets, not a discount; never call it one [T Nov 13]. Releases sell out fast [T].
- **Peace Love Mahjong:** tile listings are named "Tiles + Tile Pouch + Dice", so a pouch/dice filter wrongly drops them [C, catalog-naming-traps]. Racks re-cut whole from the group photo [T Oct 26].
- **Catalog naming traps** [C, docs/catalog-naming-traps.md]: Charleston "… Edition™", Royal "Studio Series", Mahj Mood "… Collection", My Fair "THE … SERIES", Wren mats without "mat" in the title.
- **Tigre de Tartán:** code shown as an image only; Paige Spearin collabs earn nothing [T].
- **Yellow Mountain:** half weight; numeric code, not MAHJMATCH [T].
- **Mahjong Co.:** only Kaleidoscope remains; the brand is going out of business, so don't push it [T].
- **Brewtifully** (new Nov 18): she doesn't like its tile sets and never presents them as favorites. She likes a few mats [T]. Whether its tile sets go into FYM at all [?]: by the whole-store rule they would, as plain catalog entries.
- **Wren Mats** is not an affiliate: a group discount code only, and she earns nothing [T Nov 19].

---

## 5. Done by habit, never written down (all [C])

1. Before trusting a photo, I open `/products/<handle>.json` and look at every image, not just the first.
2. I crop to the mat and then measure colours. Measuring a room shot gives the wrong colours.
3. When a scrape doesn't find a product, I assume our check failed (bare domain vs. www, bot block, timeout) before assuming the brand removed it. This became her rule on Nov 8 for partners.
4. I give a matched-but-hidden mat a pass only if it's verified on the live album page (m_hidden_ok.json).
5. I put a new brand's items in a pending queue and run the gate before anything shows. I never edit the live build directly.
6. When a mat appears in a new material, I attach it to the existing listing as "also available in" rather than adding a second mat.
7. For holiday checks I look at the photo, not the store's "holiday" tag (the tags are wrong often).
8. I keep the website copy, the claude.ai artifact and the Mat Gallery on the same version. The artifact has fallen behind since Nov 17 (artifact 1.18, site 1.22).
9. I treat "Photo coming soon" tile sets as visible but sorted last, rather than hiding them.
10. I check the build size: jsDelivr refuses single files over 20 MB, so the site index stays under 15 MB (gate [119]). This limits how many items can come in per release, and it's the practical reason for the per-release caps.

---

## Current state (Nov 19, as far as this chat knows)

- **Live:** website 1.22 (via site-app/live.json). The claude.ai artifact still shows 1.18.
- **Not live:**
  - 1.23 private catalog build: 224 new mats and 7 tile sets.
  - 1.23 layout preview (her Nov 18 layout changes).
  - She hasn't approved either one.
- **RULE (Tiffany Nov 21 6:09pm):** only the redesign is ever held for her. New mats, tiles and racks always go out in the next update on the live design. A redesign in progress never holds the catalog.
- **What is still not in the app, as of Sun Nov 22 9:40am (live: 1.22.14).** The only allowed reasons for a missing product are: big-catalog brand caps, and Amazon pins she has not hand-picked. Everything else below is a miss with a next step (docs/OVERDUE.md, config/fym-prep-nov22/sync/report.md):
  - Building now as 1.22.15: Noli June Martini, Sweetheart, Mazel, Chinoiserie Luxe Lilac, Riviera Jet Set Portofino Blue; Mahjong Studios Easter Morning; Yellow Mountain Koi (Watercolor), Qilin Kirin Bone & Bamboo; Let's Be Besties Bamboo Butterfly Garden, Wildly Starstruck, Midnight Jubilee, Old Lady Funny with Border.
  - Album mats not in the app (15, all allowed because she matched them): Dreamframer Art Dark Blue Art Deco; Lemondrop Sapphire Blooms, Floral Affair; Ozark Baker Traditional, Trent Celadon, Trent Midnight; Mahjong by SI Ralph, Fall Lanterns; It's a Mahjong Life Lowcountry Horizon; Rack It! Kyoto Dreams; plus the rest listed in sync/gaps.json. (The Nov 18 "9 Origami Timber mats" line meant album mats like these; Duet has not confirmed its list.)
  - ShopMy pins not in the app: 56 Amazon (her Nov 8 answer: "if it's in ShopMy, bring it in"; staged in config/fym-shopmy-catalog-refresh-nov08.json, never built), 4 Etsy for Sadie Jane.
  - Stores the automatic read fails on (our check failing, not the store): Amanda Toppe, Wren Mats, I Love Mahj, Soirée All Day: read in Chrome on the laptop by the Partner watch.
  - Big catalogs, by rule 10 per run: Let's Be Besties, Mah Jongg Maven, Mahjong by SI, Splash; Brewtifully and Spools (new partners).
  - Mat Gallery: built from v120, about 286 visible app mats behind; being staged from 1.22.14.
