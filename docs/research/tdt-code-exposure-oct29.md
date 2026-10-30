# Tigre de Tartán code exposure inventory (Oct 29-30, 2026)

**Why:** TdT affiliate policy (Caroline, affiliates@tigredetartan.com; ANSWERS 2026-10-29 11:42pm): on websites the brand name and the code may not appear in the same text (use the affiliate link, or show the code in an image); no codes in IG/TikTok captions (on-screen/in-video is OK); no coupon/deal sites; no reposting their reels with our code. Leaked codes get switched off.

**Tiffany's final call (Oct 30 12:04-12:06am, via Main):** change only what a visitor SEES. Keep SEO title, meta description, URL, Open Graph and FAQ JSON-LD exactly as they are (MAHJMATCH stays in them). Image alt text may carry brand + code.

**Method:** every URL in https://www.mahjmatchmaker.com/sitemap.xml (126 pages) fetched Oct 30 ~12:10am ET and parsed (BeautifulSoup): each visible MAHJMATCH was traced to its enclosing card/paragraph/list item and flagged when that unit names Tigre de Tartán or links tigredetartan.com; head tags + JSON-LD checked separately. FYM v103 (fym-site-preview `site-app/fym-v103/index.html`), Planoly IG workspace (55 post groups) + Pinterest workspace (newest 100), the codes-post draft, and the last 49 @mahjmatchmaker IG captions also checked.

## Counts by location type

| Location type | Items | Status |
|---|---|---|
| Hub /mahjong-discount-codes, visible TdT row + TdT section | 2 | **FIXED live Oct 30** (row code = image; section text reworded) |
| Hub JSON-LD (ItemList + FAQ brand list) | 2 | Kept on purpose (her call: back-end stays optimized) |
| TdT brand page, visible text (2 thank-you lines, 2 code FAQ questions) | 4 | **FIXED live Oct 30** (lines reworded + auto-apply link; 2 FAQ questions removed from the visible accordion only) |
| TdT brand page head (title, og/twitter title + description, meta description, itemprop, fullSiteTitle) | 9 tags | Kept on purpose (her call) |
| TdT brand page FAQ JSON-LD | 2 answers | Kept on purpose (her call) |
| Album pages: TdT mat match cards showing "code MAHJMATCH" | 97 cards on 28 pages | OPEN: visible pairing remains (card says "Mat by Tigre de Tartan" + "code MAHJMATCH") |
| Blog /blog/my-favorite-mahjong-racks: TdT box "Tigre de Tartán · Save 10% with code MAHJMATCH" | 1 | OPEN |
| /jade-mahjong-tile-matches meta/og/twitter description ("...Tigre de Tartan and more. ... save with code MAHJMATCH") | 4 tags | Head only: kept per her call |
| Mat Gallery /mahjong-mats: 11 TdT rows link to tigredetartan.com/discount/MAHJMATCH?redirect=... | 11 links | Code is in the link address only (not visible text): leave (her call on auto-apply links) |
| FYM app (v103) | 4 text spots + 33 links | OPEN for Matches & Catalog (see below) |
| Planoly IG drafts | 1 | OPEN (draft, not scheduled) |
| Codes post draft (HQ needs/codes-post-2026-10-29) | 3 lines (group comment, IG caption, FB Page) | OPEN: needs her decision before it posts |
| Published IG captions (last 49) | 0 | none name TdT |
| Pinterest (newest 100 pins) | 0 | none (one "red tartan cloth" false hit) |

## 1. Website

### 1a. Discount codes hub (FIXED live, Oct 30 ~12:30am ET)
- At-a-glance row, before: `Tigre de Tartan — 10% off with MAHJMATCH`. Now: same wording, the code is an image rendered in the row's own font (Bitter 16px, #f56b8b, transparent, 3x, data: URI, `height:1.5em;vertical-align:top`), alt `Tigre de Tartán discount code MAHJMATCH, 10% off`. Checked side by side with the neighbouring rows: identical. Repo copy: assets/brand-pages/tdt-code-pill-hub.png.
- Brand section text block, before: "...all made in small batches. Use **MAHJMATCH** for 10% off." Now: "...all made in small batches. Save 10% with my reader code, shown in the list above." (a Squarespace text block can't hold an inline image).
- Kept (back-end): ItemList `"Tigre de Tartan: 10% off with MAHJMATCH"`, FAQ "Which brands accept MAHJMATCH?" list entry, page title.

### 1b. /tigre-de-tartan-discount-code (FIXED live, Oct 30 ~12:40am ET)
| Where | Before | Now |
|---|---|---|
| Top perk line + section perk line | A thank-you for Mahj Matchmaker readers: use code MAHJMATCH for 10% off at Tigre de Tartán checkout. | A thank-you for Mahj Matchmaker readers: [save 10% at Tigre de Tartán](auto-apply link) |
| "Visit Tigre de Tartán" buttons (2) | https://tigredetartan.com/?sca_ref=11798386.tvil8GTGTp6s2 | https://tigredetartan.com/discount/MAHJMATCH?redirect=%2F%3Fsca_ref%3D11798386.tvil8GTGTp6s2 |
| Visible FAQ "Is there a Tigre de Tartán discount code?" + "Can I combine the code with other offers?" | Yes. Code MAHJMATCH saves 10%... / ...so MAHJMATCH usually can't be combined... | Both questions REMOVED from the visible accordion (Tiffany 12:10am). The visible accordion keeps 3 questions (made of, rules printed, racks); the FAQ JSON-LD keeps all 5 incl. both code questions, unchanged. |
| Verified line | ✓ Code verified October 27, 2026 | unchanged (no code text) |
| SEO title "Tigre de Tartan Discount Code: 10% Off with MAHJMATCH", meta description, OG, URL, FAQ JSON-LD | | unchanged (her call). The visible accordion is hand-written HTML, not rendered from the JSON-LD, so no decoupling was needed. |

Also fixed earlier the same night (typo, coordinator): FAQ question "Tigre de Tart&aacute;n" in JSON-LD and the visible summary.

Auto-apply link test (curl, no checkout): `302 → https://tigredetartan.com/?sca_ref=11798386.tvil8GTGTp6s2` with `Set-Cookie: discount_code=MAHJMATCH`. The UpPromote affiliate cookie is set by their on-page script from the `sca_ref` parameter (the page loads UpPromote's core script), so curl can't see it; Main's browser test (Oct 30) saw the cart drop $175 → $157.50 with the affiliate cookie set. The plain `?sca_ref=` link alone does NOT apply the 10%.

### 1c. Still open on the site (visible text, not changed tonight: not in her final scope)
**Album match cards (97 on 28 pages).** Each TdT mat card reads `Mat by Tigre de Tartan` + `Shop the <mat> Mat` (affiliate link) + `code MAHJMATCH`.
Proposed: on TdT-mat cards only, drop the `<span class="mm3-code">code MAHJMATCH</span>` (keep the link), or swap the span for the same image treatment as the hub. Same patch on every album page (one code-block edit per page). Note: rack-only mentions ("Racks shown: Tigre de Tartán ...") were not found next to a code.

| Page | TdT mat cards | Cards |
|---|---|---|
| /heritage-mahjong-tile-matches | 13 | Heritage + Cannage Blonde; Heritage + Chinoiserie Denim; Heritage + Domino Faded Carolina; Heritage + Domino Oxblood; Heritage + French Mural; Heritage + Handbook Plaid; Heritage + El Último Refresco; Heritage + Nantucket Basket; Heritage + Plum Peony; Heritage + Caned Trompe L'oeil; Heritage + El Tigre; Heritage + Hearts & Horseshoes; Heritage + Mantel Mates |
| /tortoise-mahjong-tile-matches | 13 | Tortoise + Cannage Blonde; Tortoise + Chinoiserie Denim; Tortoise + Domino Faded Carolina; Tortoise + Domino Oxblood; Tortoise + French Mural; Tortoise + Handbook Plaid; Tortoise + El Último Refresco; Tortoise + Nantucket Basket; Tortoise + Plum Peony; Tortoise + Caned Trompe L'oeil; Tortoise + El Tigre; Tortoise + Hearts & Horseshoes; Tortoise + Mantel Mates |
| /heritage-2-0-mahjong-tile-matches | 11 | Heritage 2.0 + Cannage Blonde; Heritage 2.0 + Chinoiserie Denim; Heritage 2.0 + Domino Faded Carolina; Heritage 2.0 + Domino Oxblood; Heritage 2.0 + French Mural; Heritage 2.0 + Handbook Plaid; Heritage 2.0 + El Último Refresco; Heritage 2.0 + Nantucket Basket; Heritage 2.0 + Caned Trompe L'oeil; Heritage 2.0 + El Tigre; Heritage 2.0 + Mantel Mates |
| /moonlight-mahjong-tile-matches | 5 | Moonlight + Chinoiserie Denim; Moonlight + Domino Faded Carolina; Moonlight + El Último Refresco; Moonlight + Plum Peony; Moonlight + Hearts & Horseshoes |
| /nantucket-mahjong-tile-matches | 5 | Nantucket + Handbook Plaid; Nantucket + Nantucket Basket; Nantucket + Caned Trompe L'oeil; Nantucket + Hearts & Horseshoes; Nantucket + Mantel Mates |
| /palm-royale-mahjong-tile-matches | 5 | Palm Royale + French Mural; Palm Royale + Nantucket Basket; Palm Royale + Bunny Love; Palm Royale + Caned Trompe L'oeil; Palm Royale + El Tigre |
| /drake-mahjong-tile-matches | 4 | Drake + Domino Oxblood; Drake + French Mural; Drake + Handbook Plaid; Drake + Caned Trompe L'oeil |
| /birdie-mahjong-tile-matches | 3 | Birdie + Chinoiserie Denim; Birdie + Domino Faded Carolina; Birdie + Shell Yeah |
| /coquette-mahjong-tile-matches | 3 | Coquette + Shell Yeah; Coquette + Cannage Blonde; Coquette + Bunny Love |
| /lola-mahjong-tile-matches | 3 | Lola + Chinoiserie Denim; Lola + Plum Peony; Lola + Hearts & Horseshoes |
| /luminaire-mahjong-tile-matches | 3 | Luminaire + Cannage Blonde; Luminaire + Domino Faded Carolina; Luminaire + Shell Yeah |
| /sierra-mahjong-tile-matches | 3 | Sierra + Nantucket Basket; Sierra + Caned Trompe L'oeil; Sierra + El Tigre |
| /willow-mahjong-tile-matches | 3 | Willow + French Mural; Willow + Handbook Plaid; Willow + Caned Trompe L'oeil |
| /emerald-mahjong-tile-matches | 2 | Emerald + Jardín de Los Jefes; Emerald + Bunny Love |
| /gatsby-mahjong-tile-matches | 2 | Gatsby + Plum Peony; Gatsby + Hearts & Horseshoes |
| /gemma-mahjong-tile-matches | 2 | Gemma + El Último Refresco; Gemma + Plum Peony |
| /glow-wild-mahjong-tile-matches | 2 | Glow Wild + El Tigre; Glow Wild + Mantel Mates |
| /jasmine-mahjong-tile-matches | 2 | Jasmine + Jardín de Los Jefes; Jasmine + Bunny Love |
| /la-fete-mahjong-tile-matches | 2 | La Fete + Cannage Blonde; La Fete + Bunny Love |
| /pearlescent-mahjong-tile-matches | 2 | Pearlescent + Cannage Blonde; Pearlescent + Shell Yeah |
| /solara-mahjong-tile-matches | 2 | Solara + Jardín de Los Jefes; Solara + Shell Yeah |
| /amara-mahjong-tile-matches | 1 | Amara + Jardín de Los Jefes |
| /dandy-mahjong-tile-matches | 1 | Dandy + Jardín de Los Jefes |
| /glitterville-mahjong-tile-matches | 1 | Glitterville + Jardín de Los Jefes |
| /malachite-mahjong-tile-matches | 1 | Malachite + Domino Oxblood |
| /sorbet-mahjong-tile-matches | 1 | Sorbet + Shell Yeah |
| /sunset-mahjong-tile-matches | 1 | Sunset + Jardín de Los Jefes |
| /taylor-mahjong-tile-matches | 1 | Taylor + Shell Yeah |
**Blog /blog/my-favorite-mahjong-racks** box: "Tigre de Tartán · Save 10% with code MAHJMATCH" + button to https://tigredetartan.com/mahjmatchmaker. Proposed: "Tigre de Tartán · Readers save 10% through my link" with the button on the auto-apply link (or the code as an image).

**Gallery /mahjong-mats:** 11 TdT rows use `tigredetartan.com/discount/MAHJMATCH?redirect=...` links. Code is only in the address; leave as is (same pattern she approved for the brand page).

**Head-only (kept per her call):** /jade-mahjong-tile-matches description tags name TdT + code; TdT page title/meta.

## 2. Find Your Mat-ch (v103 build source)
1. Brand-filter note `bnote(b)`: when a visitor filters to Tigre de Tartán it shows "✦ Save 10% or more at Tigre de Tartán with code MAHJMATCH". Proposed: for TdT, "✦ Save 10% at Tigre de Tartán through our link" (all TdT links already carry the code via /discount/ links).
2. Card code line `codeLine()`: "Use code MAHJMATCH to save" on a card that shows a TdT piece (and brand names on the card). Proposed: when every partner piece on the card is TdT, "Shop with our link to save"; when mixed, name only the non-TdT brands.
3. Share text: "Use code MAHJMATCH at <brands> to save" lists Tigre de Tartán by name, and people paste it into captions. Proposed: drop TdT from that brand list; add "Tigre de Tartán: through the link".
4. Shop-by-brand header "Partner brands · save 10% or more with code MAHJMATCH" above a list that includes TdT. Borderline; proposed: leave.
5. Links: 33 of 38 TdT items already use `tigredetartan.com/discount/MAHJMATCH?redirect=...sca_ref...` (code auto-applies); 5 do not. Leave the URLs.
Owner: Matches & Catalog (docs/MATCH-INBOX.md item added).

## 3. Social
- **Planoly IG draft** (post group 01a16476-2aa1-721a-bfc6-11f19879e53c, Ep 2 Jade "Missed Connections" reel, reminder post, no date yet): caption "Use code MAHJMATCH at Miss Mahjong, Amanda Toppe and Tigre de Tartán." Proposed: "Use code MAHJMATCH at Miss Mahjong and Amanda Toppe. Tigre de Tartán: shop through the link in bio." (No code in the caption next to TdT; on-screen is OK per their policy.)
- **Codes post draft** (docs/social/codes-post-2026-10-29.md + HQ needs/codes-post-2026-10-29, not posted): the line "Tigre de Tartán: 10% off with code MAHJMATCH" is in (a) the FB group first comment, (b) the Instagram caption (breaks the no-codes-in-IG-captions rule), (c) the FB Page post. @tigre_de_tartan is also in Tag people. Proposed: IG caption + FB Page: drop the TdT line (the graphic shows the logo; code on-screen is allowed). FB group comment: "Tigre de Tartán: 10% off through my link: https://tigredetartan.com/discount/MAHJMATCH?redirect=%2F%3Fsca_ref%3D11798386.tvil8GTGTp6s2". Needs her yes (it changes a draft waiting on her).
- Published IG captions: none of the last 49 name Tigre de Tartán. Pinterest: none.

## 4. Not checked
TikTok (no account connected), Facebook group past posts (doc 94 weekly codes posts may have listed TdT + code: search the group for "Tigre" before the next run), ShopMy/Amazon storefront text, emails/newsletters in Squarespace.
