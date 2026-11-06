# Site-wide search (Tiffany, Oct 21 2026). INSTALLED Nov 1 ~12:55am ET (Code Injection header, index @6a8c3490)

Oct 22: index refreshed @c6e395f (Kerry, Vivienne, Soiree holiday mats; Mahjong Studios / Four Winds album-only mats excluded), snippet pinned + warmed. QA run by the builder session (a separate agent could not be spawned): Chromium + WebKit at 390/1280 on home, /mahjong-mats, an album, a brand page, /find-your-match: icon visible, burger not displaced, no search-caused sideways scroll (desktop 1494px overflow is the pre-existing nav), all 8 test searches OK, photos load, Esc/Close/Back close, deep link scrolls + pulses, no search console errors, no italic headings.

A search button in the site header (desktop and phone). Type a mat name, a brand ("Sunday Mahjong"), a tile set ("Papaya Spritz"), a colour ("pink"), a theme ("halloween", "leopard") or a code ("MAHJMATCH") and results show instantly with photos.

## Files
- `assets/search/search.js`, `assets/search/search.css`: the UI (vanilla JS, no libraries). Loaded site-wide from Code Injection.
- `assets/search/mat-cards.json`: the All matches panel data (see below).
- `assets/search/search-index.json` (~270 KB, ~47 KB gzipped) + `assets/search/thumbs/` (small webp thumbs: `m/` gallery mats, `a/` album covers, `x/` album-only mat cards). Loaded only when search is first opened.
- `scripts/search/build_index.py`: builds the index from the LIVE site (curl only).
- `config/search-photo-themes.json`: theme words Claude read off mat photos (hearts, dragons, lobsters...). Edit freely.
- `site/livepatch/search/header-injection.html`: the pinned snippet to paste. `pin.py <sha>` re-pins it and warms every jsDelivr URL (doc 73), writing `urls.txt` + `warm_result.json`.
- `site/livepatch/search/apps-script-search-log.gs`: search log for a Google Sheet (see Tracking).

## What it searches
- Every mat in the live Mat Gallery (`/mahjong-mats` code block rows, same as `site/livepatch/matgallery/matgallery-v5.html`): photo, name, brand, colour chips, Retired pill, Shop link, "See in gallery", and which albums it is in.
- Every tile set album (`/…-mahjong-tile-matches` from the sitemap; colour hub pages are marked "Colour guide"), each holiday tile set section on `/holiday-mahjong-matches` (anchor links), plus album-only mats: mats in an album caption that are not in the gallery (shown with their match card photo and "See the match").
- Brand/code pages (with the code + %), the codes hub, blog posts, Find Your Match, the Mat Gallery, the Christmas mat gallery and the other main pages.
- Silent theme keywords (no filter needed): halloween/fall/pumpkin, valentine/hearts, patriotic/4th of July, St Patrick's, easter/bunny, Kentucky Derby/horse, christmas/holiday/hanukkah/winter/ski/snow for holiday mats, colour words, and synonyms (leopard/cheetah -> animal print, gingham/plaid/tartan/check). Rules: `THEMES` in build_index.py (name words only, so "Peace LOVE Mahjong" or "Tigre de TARTAN" never trigger a theme) + `config/search-photo-themes.json`.

## How it behaves
- Instant, accent-insensitive ("apres" finds "Après"), word-prefix ("papa"), typo-tolerant ("papya sprtz") only when a word is not on the site at all (so "tala" does not drag in "Talk").
- Groups: Tile set albums, Mats, Brands & codes, Articles & pages, ordered by best hit. A tile set search lists that album's mats first in Tiffany's caption order (top picks first). A brand search puts the brand + code card first.
- Tap a mat photo or name: big photo with Shop + See in gallery. Opens with the header icon, `/` or Cmd/Ctrl+K; Esc, Close or the phone Back button closes it.
- Deep link: any page + `?mmq=<query>` opens search with that query, e.g. `https://www.mahjmatchmaker.com/?mmq=papaya%20spritz` (Claude can send these in chat).
- "See in gallery" goes to `/mahjong-mats#<image key>`. The gallery block has no anchors, so search.js itself (it runs on every page) finds that card, resets filters if the card is hidden (shows retired if needed), scrolls to it and pulses a pink outline. **No change to the gallery code block is needed.**
- Phones: the header icon sits left of the burger. To make room the mobile logo shrinks slightly (about 254 -> 222 px wide at 390 px) instead of pushing the burger off-screen. Desktop: the icon sits in the gap right of the logo (absolutely placed, the nav does not move).

## All matches for one mat (Tiffany approved Nov 6 2026 1:03am; built Nov 6, pinned @720659bd, warmed; Code Injection swap pending independent QA)
Readers want every match card for one mat in one place (e.g. Dapper 2 is in 9 albums). No per-mat albums or cover cards: ONE data-driven panel inside search.js, hidden from the nav.
- **Opens from:** a search result for a mat in more than 2 albums ("See all N match cards", under the "+N more" line, which stays); Mat Gallery cards for mats in 2+ albums ("See its matches", added by search.js itself to every `.mmg-card`, incl. after filters re-render; no gallery code-block change); `?mmmat=<slug>` on any page (slug = the mat name, e.g. `?mmmat=dapper-2`, `?mmmat=sugarplum`; brand-name slug only when two mats share a name, e.g. `?mmmat=oh-my-mahjong-garden-party`; the gallery img key works too, e.g. `?mmmat=oh-my-mahjong--dapper-2`); `window.MMSearch.openMat(slug)`.
- **Panel:** "All matches for <Mat> · <Brand>", N match cards, one card per album = that album's own match card image (mat full, tiles inset bottom-right, racks), the tile set name and "See the album" (holiday sections: "See the holiday album", anchor link). Tap a card = zoom (1000w) with prev/next, arrow keys and swipe. Shop the mat + See in the Mat Gallery at the bottom. Close: ✕, Esc (zoom first), phone Back. Background scroll locked. Full names, never truncated. Cards are ordered by how high the mat sits in each album (her top picks first).
- **Data:** `assets/search/mat-cards.json` (~290 KB, ~44 KB gzipped), loaded only when the panel opens or a page has gallery cards. Built by `build_index.py` (`mat_views()`) from the album pages' own match-card figures; slugs also go into the index (`m[10]`, `x[8]`). Nov 6 build: 230 mats (216 gallery + 14 album-only), 1,534 match cards, 0 album-cover fallbacks.
- **Same design, two colourways:** an album caption like "Lagoon + Birdie" or "Brownstone Bloom + Dapper" fuzzy-matches 2 gallery mats; `config/search-card-variants.json` names the mat each such card really shows (Claude looked at each card). Add a line there when a new album caption is ambiguous (`--debug` does not flag these; check mats whose view shares a card image). Premium / Double-Sided variants of one design stay on both.

## Tracking (what people search, and empty searches)
The live site has **no Google Analytics 4** (no gtag / G- ID found Oct 21), only Squarespace analytics, which cannot see these searches. So search.js POSTs `{q, results_count, page, ts}` to `window.MM_SEARCH_LOG_URL` when that is set (a search is logged after 1.2 s without typing, on Enter, or when search closes; never twice in a row; nothing personal). If GA4 is ever added, `search` and `search_no_results` gtag events fire automatically too.
1. Tiffany: follow the 4 steps at the top of `apps-script-search-log.gs` (new Sheet > Extensions > Apps Script > paste > Deploy as Web app, Anyone) and send Claude the /exec URL.
2. Put the URL between the quotes in `window.MM_SEARCH_LOG_URL = '';` in the Code Injection snippet. Until then search works, it just is not logged.
The Sheet gets three tabs: `searches` (one row each), `top searches`, `no results`.

## Install (main session, after independent QA)
1. Push, then pin: `python3 site/livepatch/search/pin.py <commit>` (warms every URL; `still_failing` must be empty).
2. Squarespace: Settings > Developer Tools (Advanced) > Code Injection > **Header**. It is a CodeMirror 5 editor (doc 59): click at the very END of the existing header code (do not replace the Pinterest verification or anything else), paste the contents of `header-injection.html`, Save.
3. Check on a phone and a desktop: icon in header, burger still opens, search "papaya spritz", tap a mat, See in gallery jumps to it.
Undo: delete those lines from Code Injection.

## Refresh the index (after the gallery, an album or a brand page changes)
```
python3 scripts/search/build_index.py            # rebuilds index + only the changed thumbs
git add assets/search scripts/search config/search-photo-themes.json && git commit && git pull -q --rebase && git push -q
python3 site/livepatch/search/pin.py <new commit>  # re-pin + warm
```
Then replace the two jsDelivr lines in Code Injection with the new pinned ones (the URL changes because it is pinned to a commit). `--debug` lists album captions that did not match a gallery mat.

## QA (builder's own run, Oct 21; independent QA still to do)
Playwright on the curl'd live homepage + Mat Gallery with the snippet (390 px phone and 1280 px desktop): header icon visible, burger opens/closes, no sideways scroll at 390, index not loaded until search opens, all test searches return sensible results, lightbox, Esc, Back, `/`, Ctrl+K, `?mmq=`, See in gallery (incl. a retired mat), and the log POST. No console errors from the search files (the only errors are the preview server lacking Squarespace's own relative files).

## Found while building (not changed)
- **Desktop nav overflows on the live site**: at 1024-1440 px wide the last nav items (Blog, Community, About at 1280) sit off the right edge and the page scrolls sideways (page width 1492 px at a 1280 px window). Pre-existing; search does not change it. Fix options: fewer top-level nav items, a smaller nav font/spacing in Site Styles, or moving Blog/Community/About into a folder.
