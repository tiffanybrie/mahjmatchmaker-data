# Launch-day homepage switch. Tue Oct 27, 2026, 9:00am CT (14:00 UTC). STAGED, not live

**Oct 21 afternoon update:** the switch now also swaps the hero GRAPHIC (Tiffany 12:55pm). Previews: `hero-graphic/previews/hero-launch-1280.png` and `hero-launch-390.png`.

Tiffany approved Oct 21, 12:42pm: "yes to both the announcement bar and also to the 10/27 launch day switch".
A one-time scheduled task ("Launch day: switch homepage hero + remove announcement bar") runs these steps at 9:00am CT.

**Launch time source:** `docs/content-strategy-oct-dec.md`, Tue Oct 27 row: launch row post 1 "Find *Your* Mat-ch™ is live" carousel, IG feed, Auto **9am** (that doc's times are Central, CDT until Nov 1). HQ `hq/launchPlan` gives the date (Tue Oct 27) but no time.

## Where the hero lives
Homepage (`/`), first page section `69b1d01489d0f8016ee3d59f` (fluid engine, background image `papaya-spritz-mahjong-tiles-vivienne-mat-hero.jpg` since Oct 21 afternoon, focal point 0.62,0.5; was `loveshackfancy-coquette-mahjong-tiles-fleur-mat.jpg`, 0.5,0.5). Two **native** Squarespace blocks, no code block.

## The launch hero (updated Oct 21 afternoon)
Tiffany, Oct 21 12:55pm: "The Find Your Match hero cannot just be over the Coquette LoveShackFancy graphic. The homepage has to be completely a new graphic there that showcases Find Your Match." So launch day swaps the **background image** too, not just the words.

The design is the one already shown to her in Ready to Ship (`site/livepatch/nav-plan`, rts/01 + 02: the "It's a mat-ch!" fan of match cards, text on the left), brought up to date in `hero-graphic/`:
- **Fan:** the live Papaya Spritz + Press for Mahjong album card in front (Beechwood racks, `@fbf7ec9`; "Save with code", no %), live Heritage 2.0 + Isla card behind (photo identity check OK: Heritage 2.0, not Heritage 1; its "10% OFF" line cut off), live Coquette + Fleur card behind (no code line). ✕ and ♥ under the fan; pink tag "It's a mat-ch!".
- **Background:** brand cream `#faf3ea` with blush `#fbe3ea` circles. No LoveShackFancy photo. No brown.
- **Text stays live Squarespace text** (not baked into the image): pill `NEW · FIND YOUR MAT-CH` (CSS), H1 `Find Your Mat-ch™ is here` with "Your" emphasised (navy), line `Start with your tiles or your mat and swipe your perfect match.`, button `Start swiping` → `/find-your-match`, then `or browse the albums` → `/mahjong-tile-matches` and `Use code MAHJMATCH to save at 30+ partner brands` (the count the live codes page uses). No % anywhere.
- **Layout:** ≥1200px wide, text column on the left, fan on the right (desktop image). Under 1200px (tablets and phones), text stacks on top and the fan sits under it (portrait mobile image). Squarespace has one background image per section and one focal point, so the phone/tablet image and the left-column layout come from one scoped Custom CSS block (`hero-graphic/launch-hero.paste.css`). The old white 68% frosted panel is turned off by that CSS.

| Piece | Now | Launch |
|---|---|---|
| Section background image | Papaya Spritz on Vivienne photo (OMM, since Oct 21; was Coquette Fleur) | `find-your-match-mahjong-hero-desktop.jpg` (2400×1500, uploaded) |
| Text block `block-b79726a6f150a9dd219f` | H1 `Find the Perfect Mahjong Match` / H4 `Match mahjong tiles, mats, and racks across brands` | H1 `Find Your Mat-ch™ is here` ("Your" in italics = `<em>`) / H4 `Start with your tiles or your mat and swipe your perfect match.` (`after-text-block.html`) |
| Button block `block-yui_3_17_2_1_1773260945246_2648` | `Find Your Match` → `/mahjong-tile-matches` | `Start swiping` → `/find-your-match` |
| NEW text block in the hero | (none) | `or browse the albums` (link `/mahjong-tile-matches`) + `Use code MAHJMATCH to save at 30+ partner brands` (`hero-graphic/links-block.html`) |
| Design > Custom CSS | (announcement bar CSS etc.) | append `hero-graphic/launch-hero.paste.css` at the END (scoped to this section only) |

**Italic on "Your":** the H1 font (Shrikhand) is already slanted, and a plain `<em>` squeezed the space after it. The CSS sets that `<em>` upright and navy, so "Your" stands out and the markup still carries the italic. So DO add the italic to "Your" in the editor (select "Your", press the italic button or Ctrl/Cmd+I).

**Pinned images (jsDelivr, warmed Oct 21, both 200 and byte-identical to the repo):**
- Desktop (upload into the section): `https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@237f0fff5e35d8f1cbf36beee833c2c0269b0971/site/livepatch/launch-oct27/hero-graphic/find-your-match-mahjong-hero-desktop.jpg`
- Custom CSS to append: `https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@845b8c0f4d1e999baa16374e5188f9fc8c029944/site/livepatch/launch-oct27/hero-graphic/launch-hero.paste.css`
- Mobile/tablet (used by the CSS): `https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@237f0fff5e35d8f1cbf36beee833c2c0269b0971/site/livepatch/launch-oct27/hero-graphic/find-your-match-mahjong-hero-mobile.jpg`

**Tool URL:** `/find-your-match`. It already exists (teaser "Coming 10.27", page id `6ad6f62ad05b752bba9d1e8d`) and the header nav "Find Your Mat-ch™" already points there. Per `site/livepatch/nav-plan/README.md` and `site/livepatch/pages/README.md`, its content is swapped for the live tool on 10/27; the embed method is in the launch plan (Project doc 54). That swap is a separate job. If the final tool URL changes, update the button link only.

## Files
- `hero-graphic/find-your-match-mahjong-hero-desktop.jpg`, `…-mobile.jpg`: the two graphics. Built by `hero-graphic/build.py bg` from the live album cards in `site/livepatch/nav-plan/mock/img/`.
- `hero-graphic/launch-hero.paste.css`: the Custom CSS block to append on launch day (mobile URL pinned). `launch-hero.css` is the template (MOBILE_URL placeholder).
- `hero-graphic/links-block.html`: the new small text block. `after-text-block.html` (= `hero-graphic/text-block.html`): the launch H1 + H4.
- `hero-graphic/previews/hero-launch-{1280,390}.png` (main previews) plus 360, 768, 1100, 1200, 1440, 1920: the LIVE homepage rendered with the new image, CSS and text swapped in (`build.py preview`). These are what launch day must match.
- `before/text-block-b79726a6f150a9dd219f.html`: the live H1 + H4 as of Oct 21 (rollback). `before/hero-section-69b1d01489d0f8016ee3d59f.html`: the whole live hero section as of Oct 21.
- `preview.py`, `qa/hero-after-*.png`: the earlier words-only switch (superseded by `hero-graphic/`). `qa/hero-before-*.png`: before.
- `site/livepatch/nav-plan/assets/hero-fan-launch.png` + `rts/01-02`: the Ready to Ship mock, re-rendered with the same cards and copy.

## Steps on launch day
Use your OWN Chrome tab (tabs_create_mcp) at `https://hexaflexagon-denim-nhf4.squarespace.com/config`. Never type a password; never accept new terms. Type into fields with `document.execCommand('insertText', false, '...')` after focusing/selecting the field (keyboard typing drops a character). Code blocks (if any need touching) use CodeMirror 6: `document.querySelector('.cm-editor .cm-content').cmTile.view`, then Escape, Save, Exit.

0a. **Put the tool on `/find-your-match` (added Oct 21 afternoon).** Before this, nothing swapped the teaser out, so step 0 would always have blocked. Pages > "Find Your Mat-ch™" (`/find-your-match`, page id `6ad6f62ad05b752bba9d1e8d`) > Edit. Double-click its one code block (`#block-2da981e143ed2cc4bb76`, the "Coming 10.27" teaser) and replace ALL of its content with the Find Your Mat-ch page block. Fetch it in the page: `const html = await (await fetch('https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@2735fb4321f3b25efef3e9173c8f299556214f09/site/livepatch/fym-preview-oct21/page-block.html')).text();` then `const v=document.querySelector('.cm-editor .cm-content').cmTile.view; v.dispatch({changes:{from:0,to:v.state.doc.length,insert:html}})`. Then Escape, Save, Exit. This is the same block that has been live on the hidden `/find-your-mat-ch-preview` page since Oct 21 (`site/livepatch/fym-preview-oct21/page-block.html`, README there). Then DELETE the page's Newsletter block if there is one (form "FYM Teaser Signup", button "Save my spot ♥"; teaser v2, `site/livepatch/fym-teaser-oct21/teaser-v2-block.html`, moves it into its hero). If any other block in that section still says "Coming 10.27", "Save the date" or holds a newsletter form, delete it; the page should be just the code block. Verify: `curl -s "https://www.mahjmatchmaker.com/find-your-match?v=$RANDOM"` contains `id="fymx"`, `site-app/fym-v90/index.html` and `fcf9fd12d382b6fa2aad7be5e83a0114033003da/assets/site/fym-tutorial/tut6.webp` (v72 6-step tutorial), and no `Coming 10.27`, `newsletter-block` or `FYM Teaser Signup`. Then render it with `python3 site/livepatch/fym-preview-oct21/preview.py site/livepatch/launch-oct27/qa https://www.mahjmatchmaker.com/find-your-match --live` and LOOK: the app loads in the stage, the app sits at the top, How it works ↓ jumps to the annotated tutorial at the bottom, and the tutorial images load. The hidden preview page can stay as it is (Not Linked).
0. **Pre-check the tool page.** `curl -s https://www.mahjmatchmaker.com/find-your-match` must return 200. If it still contains `Coming 10.27`, the tool is not live yet: the hero button would send people to a teaser. In that case re-check every 10 minutes for up to 60 minutes. If it is still the teaser after that, do NOT switch: leave the hero and the bar as they are, log the blocker in HQ and tell Tiffany in one line.
1. **Swap the hero copy.** Pages > Home > **Edit**. The page renders in the site frame (`#sqs-site-frame` iframe). Double-click the text block (`#block-b79726a6f150a9dd219f`).
   - Select the H1 text (triple-click, or a DOM Range over the h1's text node), then `execCommand('insertText', false, 'Find Your Mat-ch™ is here')`. It must stay Heading 1. Then select just the word `Your` and make it italic (the editor's italic button or `execCommand('italic')`). Check the H1's HTML is `Find <em>Your</em> Mat-ch™ is here`.
   - Select the H4 text and insert `Start with your tiles or your mat and swipe your perfect match.`. It must stay Heading 4.
   - Leave the alignment as it is (centred); the CSS left-aligns it on wide screens. Click outside the block.
2. **Swap the button.** Click the button block, then its pencil/Edit. Button text field: select all, insert `Start swiping`. Link: clear it and insert `/find-your-match` (or pick the "Find Your Mat-ch™" page from the list); open in new tab OFF. Close the panel.
3. **Add the small links block.** In the same hero section: **Add Block > Text**. Line 1 `or browse the albums`, linked to `/mahjong-tile-matches` (select it, link button, type the URL, same window). Line 2 (new paragraph) `Use code MAHJMATCH to save at 30+ partner brands`, with `MAHJMATCH` bold. Paragraph style (Paragraph 2 or 3). Where it lands in the grid does not matter: the CSS places it under the button (it finds the block by its `/mahjong-tile-matches` link). If adding this block fails, skip it: the hero still works without it.
4. **Swap the background image.** Hover the hero section > **Edit Section** (pencil) > **Background** > the image > **Replace** (or Remove, then Add Image). Squarespace needs a FILE; use the proven method from the editor frame's JS context:
   ```js
   const r = await fetch('https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@237f0fff5e35d8f1cbf36beee833c2c0269b0971/site/livepatch/launch-oct27/hero-graphic/find-your-match-mahjong-hero-desktop.jpg');
   const f = new File([await r.blob()], 'find-your-match-mahjong-hero-desktop.jpg', {type: 'image/jpeg'});
   const inp = [...document.querySelectorAll('input[type=file]')].pop();   // the background picker's hidden input (check the parent doc AND the iframe)
   const dt = new DataTransfer(); dt.items.add(f); inp.files = dt.files; inp.dispatchEvent(new Event('change', {bubbles: true}));
   ```
   Wait for the upload to finish and the new image to show in the editor. Focal point: leave it in the centre (0.5, 0.5). Image overlay: none / 0%. Close the panel.
5. **Save, then Exit** the editor (top left). Confirm the page reads "Published".
6. **Custom CSS.** Design (or Website > Website Tools) > **Custom CSS**. It is CodeMirror 6: `const v = document.querySelector('.cm-editor .cm-content').cmTile.view;` then append the WHOLE content of `hero-graphic/launch-hero.paste.css` at the end: `v.dispatch({changes: {from: v.state.doc.length, insert: '\n\n' + css}})` (get `css` with `await (await fetch('https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@845b8c0f4d1e999baa16374e5188f9fc8c029944/site/livepatch/launch-oct27/hero-graphic/launch-hero.paste.css')).text()` in the page; pinned + warmed Oct 21, byte-identical to the repo file; don't retype it). Do not touch any existing CSS. Escape, **Save**.
7. **Announcement bar OFF.** Pages > Website Tools > Announcement Bar (`/config/pages/announcement-bar`) > toggle **Enable Announcement Bar** off > **Save**. Leave its Custom CSS block alone.
8. **Verify** (logged out, with a cache-buster):
   - `curl -s "https://www.mahjmatchmaker.com/?v=$RANDOM"` contains `Find Your Mat-ch™ is here` (or `Mat-ch&trade;`), `Start with your tiles or your mat and swipe your perfect match.`, `Start swiping` and `href="/find-your-match"`; and does NOT contain `Find the Perfect Mahjong Match`.
   - `grep -o 'announcementBarSettings.\{0,40\}'` shows `"style":1` (off) and no `arrives 10.27`. Check a second page too (`/oh-my-mahjong-discount-code`).
   - `/find-your-match` returns 200.
   - The homepage HTML references the new background (`find-your-match-mahjong-hero-desktop` in the hero section) and no longer `papaya-spritz-mahjong-tiles-vivienne-mat-hero` (nor the old `loveshackfancy-coquette-mahjong-tiles-fleur-mat`) in that section; it contains `<em>Your</em>`, `or browse the albums` and `30+ partner brands`.
   - The custom CSS file (the `static/custom-css/…/custom.css` link in the page head) contains `Launch hero: Find Your Mat-ch` and the pinned mobile jsDelivr URL.
   - Render with local Playwright (`PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`, temp in /dev/shm) at 390x844 and 1280x800 (full section height), save to `qa/live-launch-390.png` / `qa/live-launch-1280.png`, and LOOK at them next to `hero-graphic/previews/hero-launch-390.png` / `-1280.png`: same layout (1280: pill + headline + line + button + links on the left, card fan on the right; 390: text stacked, fan under it), no white panel, no Papaya/Vivienne (or Coquette) photo, no bar, no sideways scroll at 390. (The header nav already overflows sideways at 1280 today; that is not from this change.)

## Rollback
- Hero: put back the H1 `Find the Perfect Mahjong Match` and H4 `Match mahjong tiles, mats, and racks across brands` (`before/text-block-b79726a6f150a9dd219f.html`); button text `Find Your Match`, link `/mahjong-tile-matches`; delete the small links block; background image back to the Papaya Spritz on Vivienne photo that was live from Oct 21 (`assets/hero/papaya-spritz-mahjong-tiles-vivienne-mat-hero.jpg`, pinned `https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@a0183ef7ce15d25aa44cefffb72a1d6abf483afb/assets/hero/papaya-spritz-mahjong-tiles-vivienne-mat-hero.jpg`, focal point 0.62,0.5, same upload method). Save, Exit. (The older Coquette Fleur photo, `assets/hero/loveshackfancy-coquette-fleur-mat-hero.jpg`, is retired; don't restore it.)
- CSS: delete everything from `/* ===== Launch hero: Find Your Mat-ch` to `/* ===== end launch hero ===== */` in Custom CSS, Save. (Removing only the CSS while the new image stays leaves a cream hero with the fan behind centred text: fix the image too.)
- Bar (if it should come back): Website Tools > Announcement Bar > on; message `Find Your Mat-ch™ arrives 10.27 · Get notified` with "Your" italic; link `/find-your-match`; Save. (After launch, a bar would need new copy; don't restore "arrives 10.27".)

## After
- HQ log entry (artifact https://claude.ai/artifact/Cor6pKtesou4mFRQ41P6Ye, collection `log`, area "Site").
- Commit `qa/live-launch-*.png` and a "LIVE" note at the top of this README.
