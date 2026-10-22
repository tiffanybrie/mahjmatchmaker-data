# Find Your Mat-ch page (one code block)

Tiffany, Oct 21 2:19pm: "you have approval to change whatever needs to happen over on the Find Your Match preview page. I'd like that looking a lot better."

- **Now (block @8dd3d49 = app v72, Oct 21 night; before that @d68a319 = app v71; @4b7f8c9 (H1 "Your" plain Oct 21 6:45pm); LIVE since Oct 21 ~5:15pm: app first, annotated tutorial at the bottom, QA passed):** hidden page `/find-your-mat-ch-preview` (Not Linked). Its only section holds ONE code block; paste `page-block.html` into it.
- **10/27 launch:** the same `page-block.html` replaces the teaser code block on `/find-your-match` (page id `6ad6f62ad05b752bba9d1e8d`, section `6ad6f62ad05b752bba9d1e91`, code block `#block-2da981e143ed2cc4bb76`). This is step 0a in `site/livepatch/launch-oct27/README.md`. It runs before the homepage hero switch, whose step 0 checks that `/find-your-match` no longer says "Coming 10.27".

## What's on the page
1. Hero: "New from Mahj Matchmaker", **Find Your Mat-ch™** (Caprasimo, plain, no italic in headlines; ™ only here), one line, big **Start swiping ♥** button (scrolls to the app and fits the whole app stage in the window), and "browse the match albums" link. On the right sits a fan of her live Papaya Spritz top-3 match cards: #1 Heiress in front, then Press for Mahjong and Greenly. The cards are cropped above their code band, so no % shows. It also has the "It's a mat-ch!" stamp and ✕ ♥. The site header already carries the wordmark with the tagline ribbon, so the hero doesn't repeat it.
2. How it works: three steps with real screenshots of the live v69 app. (1) The doors and color chips. (2) Swiping Papaya Spritz on Heiress, ✕ ♥ only (the undo ↺ is hidden in the shot). (3) The match card the app made for that pair.
3. The app: a full-bleed stage on phones (viewport height minus 48px, so the page can still be scrolled past it). On desktop, a 580px framed panel with tips on the left, and on the right the code card, **Open full screen** and Browse the albums. Open full screen pins the same iframe to the whole window, so the app keeps its state. Close it with the ✕ Close button or Esc.
4. Good to know: an FAQ (who picks, mat first, how to save, free) plus a trust line.
5. The match albums: the first 6 covers from the live albums page and **See all match albums**.
6. Quiet affiliate disclosure line.

## App embed
A static copy of the live artifact `6epA9HuEdT32zUp79Qv3kd` (v69 = build fym-oct21e, gate PASS). Its `index.html` is on branch `fym-site-preview` @`474dd62` (`site-app/fym-oct21e/index.html`). Every other file is identical to `fym-oct21d`, so `<base>` points at `site-app/fym-oct21d/` on the same commit. jsDelivr serves .html as text/plain with nosniff, so the block fetches the HTML and runs it in a same-origin `srcdoc` iframe. It also injects a thin pink scrollbar and `text-wrap:balance` on the door buttons. The app's sheets, toasts and zoom lightbox use `position:fixed`, which is why the iframe has a fixed height and isn't sized to its content.

**When FYM ships a new build:** push its `index.html` (and any changed files) to `fym-site-preview`, warm the jsDelivr URL, set `APP_COMMIT`/`APP_INDEX`/`APP_BASE` in `build.py`, rebuild, and re-paste the block on whichever page is live.

## Files
- `build.py` → `page-block.html`. It holds the pinned asset URLs (`assets/site/fym-page/` @`44563dd`, warmed) and all copy.
- `preview.py [outdir] [url]` swaps the block into the LIVE page in the browser only, then saves stitched page shots (Chromium `full_page` drops some lazy images on this site) plus app and full-screen shots at 390/1280/1440, and prints checks. Pass `--live` to check the published page without swapping.
- `shots/`: the Playwright scripts that took the step screenshots from the local v69 build.
- `code-block.html`: the previous agent's app-only block (rollback).

## Publish (Claude in Chrome)
Your own tab → `https://hexaflexagon-denim-nhf4.squarespace.com/config` → Pages → the page → Edit → double-click the code block → CodeMirror 6: `const v=document.querySelector('.cm-editor .cm-content').cmTile.view; v.dispatch({changes:{from:0,to:v.state.doc.length,insert:html}})`. Get `html` with `await (await fetch('<pinned jsDelivr page-block.html>')).text()`; never retype it. Then Escape, Save, Exit. Verify with curl that the page contains `id="fymx"` and `site-app/fym-v72/index.html` (v72 = full app folder on fym-site-preview @ad0675e; BASE = the same folder). Editor tip: after Pages > page > Edit, wait ~8s until the section shows EDIT SECTION on hover, then double-click the block.
