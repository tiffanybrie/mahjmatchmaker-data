# FYM 1.23 layout preview: independent QA (Nov 18)

Build tested: site-app/fym-v123-preview/index.html (fym-site-preview @5e5a111e, loaded through preview.html exactly as the website does: fetch, then iframe srcdoc with base fym-v72). Compared with site-app/fym-v122.
Playwright Chromium + WebKit at 390x844, 390x664, 1440x900 (plus 375 and 340 for page width). Tracking calls to the Google script were blocked by the test harness, so nothing reached her stats.
Totals: about 57-61 scripted checks per browser/size. All pass except the bugs listed below. No real console or page errors.

| # | Item | Result |
|---|------|--------|
| 1 | Table/Aerial: X + heart under the photo, photo full width (card 366 / img 362 at 390), swipe R = heart pop + added, swipe L = X pop, buttons pop too | PASS (both browsers, all sizes, tiles door + mat door tile deck) |
| 2 | Up close same size as v122 (card 366x420, tiles 366x160 at 390) | PASS |
| 3 | View order Up close, Table, Aerial | PASS |
| 4 | Pulse + hint on first pairing step, gone after ~8s, stops on tap, does not come back | PASS |
| 5 | Shortlist "Pick your mat": 2 per row (164px) on phone, tap shows that mat in the current mode (close/table/aerial), "Showing ✓", scrolls the view into sight, Keep swiping works | PASS |
| 6 | Racks in the same frame: big view kept (366px), suggested racks shown, glowing "Choose your racks", chooser with colour/type/brand/price filters + search, pick updates the view at once, Table = rack 1 N/S, rack 2 E/W | PASS (see note A) |
| 7 | Finish button "Pick your racks to finish" until 1 rack, then "Make it official ♥"; tapping it early opens the chooser | PASS |
| - | Both doors, colour filter switch + clear, zoom persists (Up close + Table), card + share, MAHJMATCH on the card, X/heart wording only, no sideways scroll at 390/375/340, tour targets real elements | PASS |
| - | Photo contact sheets (48 mats, Table/Aerial/Up close, Gatsby + Juniper) | PASS: nothing blank or cropped wrong |

## Bugs / notes
1. **Shared preview link opens as code, not as the app.** jsDelivr serves preview.html as `text/plain` with `nosniff`, so https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@5e5a111e/site-app/fym-v123-preview/preview.html shows HTML source in a browser. Repro: open the URL in any browser. For her review use the Squarespace preview page or an artifact instead. (QA ran by serving the same file as text/html.)
2. **The Table note for a no-Table mat gives the wrong reason.** Repro: Gatsby, Table, shortlist Tigre de Tartán "El Tigre" (class C), Choose your racks. The line under the photo says "This mat has no top-down photo for Table view yet", but the card note on the photo says "its photo has its own colored racks on it". The line should use the real reason (matWhy).
3. **Note A (short phones):** at 390x664, after "Choose your racks" only 2-11% of the first rack card shows above the fold. Once you scroll to the rack cards, only about 30% of the Table/Aerial photo is still on screen, so you don't see a pick land unless you scroll back up. At 390x844 it's fine (77-82% of the photo stays visible, with the rack overlay). This is a layout limit, not a crash.
4. Minor: in the rack frame the mat card still shows the "Tiffany's match · picks off" toggle. It belongs to the mat deck and means nothing at this step.
5. Minor wording: when 2 racks are already picked, picking a rack from the rack search shows the toast "saved to your rack suitors". The mat door's tile tray still says "suitors" and "Add racks ›". Both are older text, not new in 1.23.

Screenshots (2x): assets/fym-preview-v123/qa/
