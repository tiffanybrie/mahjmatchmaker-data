# Album zoom crash (Tiffany Nov 8 10:15am: "zoom in, little white lines flash, then the site crashes to a blank page")

## Cause
Every match-album page carries the same tap-to-enlarge lightbox script (`.mm3-lb`, copied from the Papaya template). Its swipe
handler read only `touches[0]` on touchstart and `changedTouches[0]` on touchend, so a PINCH inside the open lightbox counted as a
swipe: each pinch flipped to the next photo and loaded a fresh 1080x1350 card while Safari was rendering the page zoomed in.
Repeated pinches = image swaps at high zoom (the flashing white lines) until iOS Safari runs out of memory and reloads the tab blank.
Reproduced with Playwright (chromium, iPhone 14, CDP two-finger pinch): 5 pinches on live Juniper went 5/46 -> 9/46; Papaya the same
(4/59 -> 8/59). Not a DOM/listener leak: DOM stays 1,337 nodes on Juniper through 30 viewport resizes + a full lightbox pass, no page
errors from our code (WebKit + chromium), no resize/scroll/visualViewport handlers in the block or search.js. Juniper and Papaya are
otherwise equivalent (same CSS/JS, same image sizes; Papaya is heavier), so this is not Juniper-only.

## Fix (layout identical)
Swipe only on a ONE-finger gesture at normal zoom:
`touchstart: x0 = (touches.length===1 && !(visualViewport.scale>1.05)) ? clientX : null; touchmove: 2+ fingers -> x0=null;
touchend: ignore while fingers remain down`.
- Juniper block (site/livepatch/juniper-album-nov07/juniper-codeblock.html @44f61ea5): LIVE Nov 8 ~11am. Live re-test: 5 pinches stay
  on 5/46; one-finger swipe still goes 5 -> 6 -> 5; DOM stable after zoom/resize.
- Template for future albums: site/livepatch/juniper-album-nov07/papaya_live_template.html patched.
- **Every other album page still has the bug (44 live pages, pages-with-bug-nov08.txt, Papaya Spritz included).** One site-wide fix,
  no page edits: `header-snippet.html` (a capture-phase touch guard for `.mm3-lb`, tested on live Papaya with the snippet injected:
  pinches stay on 4/59, swipe still works) appended to Settings > Code Injection > HEADER after the search lines. NOT INSTALLED:
  the Nov 8 session's attempt to add it was blocked by the permission check (site-wide script = new production change), so it
  needs Tiffany's yes. Alternative: re-paste each page's block with the one-line script change (44 Chrome edits).
Tests: zt.py (resize/zoom/lightbox, DOM + console), pinch2.py / pinch3.py (pinch inside the lightbox; pinch3 takes an init script),
swipe3.py (one-finger swipe still works).

## INSTALLED Nov 8 2026 ~1:30pm ET (Tiffany 1:00pm yes)
header-snippet.html appended to Code Injection > HEADER right after the search lines (diffed in the editor: old 588 chars unchanged + newline +
snippet; footer untouched). curl: Papaya Spritz, /holiday-mahjong-matches, Brownstone Bloom all carry it. Playwright chromium iPhone 14 (live_pinch.py
/ swipe_fresh.py in this folder): 5 pinches stay on the same photo on all 3 (baseline with the snippet stripped: 4->8, 1->5, 3->7); one-finger
swipe at normal zoom still flips (4->5->6->5 etc.); after a pinch the page is zoomed (scale 4.49) and a one-finger drag pans instead of flipping (by design).
Console errors identical with/without the snippet (0 new). Juniper (block fix + header): pinches stay 5/46, swipes 5->6->7->6, 0 new errors:
both guards run harmlessly (the header one stops the event first on pinch/zoom; at scale 1 one-finger events pass to the block), so Juniper's copy stays.
