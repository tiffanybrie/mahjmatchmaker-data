# Noli June onboarding (Oct 30): STAGED, waiting on one Chrome trip (OPS)

Tiffany approved Oct 30 9:04am (ANSWERS). Chrome was disconnected for the whole onboarding run (list_connected_browsers empty), so nothing below is live yet. Pins (jsDelivr, warmed 200 Oct 30): page + hub spec `https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@1515bc7af11ea37e1fa9ab1d264a72cc676dddfb/brand-pages/noli-june.html` and `.../@1515bc7af11ea37e1fa9ab1d264a72cc676dddfb/brand-pages/hub-noli-june-2026-10-30.json`; apply script + 38-logo graphic `@458613bda4066e549904a4b76167e48280ec1d27/site/livepatch/noli-june-oct30/apply-hub.js` and `.../assets/hub/partner-brands-2026-10-30.jpg`. (At 458613bd jsDelivr intermittently 403s the html with a 50 MB package limit, so keep the 1515bc7a pin for those two files; identical bytes.)

## 1. Brand page /noli-june-discount-code (new page)
1. /config → Pages → duplicate **/yolo-mahjong-discount-code** (gear → Duplicate Page → Confirm; it goes live as "(Copy)", do 2-3 right away).
2. Page settings (doc 59 §4 GetCollectionSettings → SaveCollectionSettings, AFTER the code-block save):
   - Title: Noli June
   - Slug: noli-june-discount-code
   - SEO title: Noli June Discount Code: 10% Off with MAHJMATCH
   - SEO description: Save 10% at Noli June with discount code MAHJMATCH ($100 minimum). Verified code for Noli June's founder-designed 33.5" leatherette mahjong mats and matching tablecloths, plus my favorites.
3. Replace the duplicated code block with `brand-pages/noli-june.html` fetched from jsDelivr at the pin (CM6: `v.dispatch({changes:{from:0,to:v.state.doc.length,insert:html}})`, wait ~4s after opening the block, confirm Save turns black).
4. curl: 200, contains "Noli June discount code: MAHJMATCH &middot; 10% off &middot; verified October 30, 2026", FAQPage JSON-LD, 12 `nolijune.com/discount/MAHJMATCH` links. Then `python3 scripts/checks/brand_page_text.py`.

## 2. Hub /mahjong-discount-codes
- Code block (holds `.mmtk` ticker + `#all-codes`): load `apply-hub.js` (jsDelivr pin) into the editor tab, then `await MMNOLI('<jsDelivr pin>/brand-pages/hub-noli-june-2026-10-30.json')`. It refuses unless every find occurs exactly once (drift check). Adds ticker logo b34 (+dup), glance row after Maison, heading 37→38, "Updated October 30, 2026", ItemList 38, FAQ count + brand list. Escape, Save, Exit.
- Text block `block-yui_3_17_2_1_1773264930191_635202`: append `textBlockAppendAfterMaison` (spec) after the Maison Mahj section (Shop link = https://nolijune.com/MAHJMATCH).
- Logo image block (still "Partner Brands Oct 28 2026.jpg", 36 logos): swap to `assets/hub/partner-brands-2026-10-30.jpg` (38 logos; also covers Maison's pending swap).
- curl: "All 38 mahjong discount codes", "numberOfItems": 38, `/noli-june-discount-code` in ticker + list.

## 3. Instagram (@mahjmatchmaker signed in only)
Follow @nolijunemahjong (footer-verified) + add to Favorites; log in docs/IG-FAVORITES.md.

## 4. After live
HQ brands/noli-june: status live, liveAt, steps.page/hub/logos true; hq/indexing: request /noli-june-discount-code first (pinned entry already there, waits for a 200).
Not done anywhere yet (applies to YOLO too): homepage logo ticker has no YOLO / Noli June items.
