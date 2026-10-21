# Pre-launch homepage: Find *Your* Mat-ch™ hero + How it works (Oct 21). PREVIEW LIVE, homepage NOT yet

Tiffany approved the menu + pre-launch homepage plan (RTS `l-navplan-fym`) at 3:22pm Oct 21 with voice-note changes. This folder holds the homepage part and the footer disclosure.

## What is live now
- **Footer disclosure (site-wide, LIVE ~4:00pm).** Code Injection > Footer, appended block `<!-- mm-disclosure -->` (`footer-disclosure.inject.html`). One line on desktop, 11.5px, footer text colour at 72% opacity, no badge, no box: "Some links on this site are affiliate links, which means I may earn a commission at no extra cost to you. All opinions are my own. As an Amazon Associate I earn from qualifying purchases." Rollback = delete that block from Code Injection > Footer.
- **Mobile footer email:** already gone on the live site (the footer email block `e8109705861a998b09f0` was deleted earlier; desktop and phone share it). The email + "NEW" badge she saw were only in the Oct 19 mockups (`site/livepatch/nav-plan/mock`). Nothing left to remove live.
- **Hidden preview page `/home-preview`** (Not Linked, noindex): a duplicate of the live homepage plus one new Code block in its hero section (`block-yui_3_17_2_1_1792611402612_5282`) holding `block-home-prelaunch-fym.html`. Byte-identical to the repo file (curl check).

## The block (`block-home-prelaunch-fym.html`)
- Hero: pill "Coming 10.27", H1 Find *Your* Mat-ch™ (the page's only ™), line, "Save my spot ♥" (scrolls to the homepage Newsletter block in "Get New Matches First", focuses its email field) + "or browse the albums". Visual = the FYM promo agent's real app phones (`scripts/fym_promo/render.py`, copied to `assets/site/home-prelaunch/`, jsDelivr @bc461bd): Papaya Spritz on Heiress (her #1), ✕ and ♥ only, no %, no undo, Beechwood racks in step 5. "Opens 10.27" stamp.
- "How it works" with the same 6 tutorial screens: pick your door, swipe ✕/♥, my picks on/off, shop by color, choose your racks, save your match card. 3×2 grid on desktop, swipe row on phone.
- Its script moves it above the page's first section and hides that section (the old "Find the Perfect Mahjong Match" hero). It pads for the absolute header.
- **Self-expiring:** at Tue Oct 27 14:00 UTC (9:00am CT, the launch-day switch time in `site/livepatch/launch-oct27/README.md`) it removes itself and the original hero shows again, so the launch-day hero swap is untouched. The launch-day task should still delete this code block from the homepage.

## QA status
Self-checked on the live preview with Playwright at 390 and 1280: block on top, old hero hidden, all 7 images load (200, jsDelivr pinned + warmed), no page errors, no sideways scroll at 390 (1280 has the old header-nav overflow, 1494px, not caused by this block). **Independent QA still needed** before it goes on the live homepage.

## Go-live steps (after QA passes)
1. Pages > Home > Edit. Hero section `69b1d01489d0f8016ee3d59f` > Add Block > Code. Pencil, then in the console: `const html=await (await fetch('https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@06e5c9e02b91e887d9cba373bacfb7f46152696f/site/livepatch/home-prelaunch-fym/block-home-prelaunch-fym.html')).text(); const v=document.querySelector('.cm-editor .cm-content').cmTile.view; v.dispatch({changes:{from:0,to:v.state.doc.length,insert:html}})`. Escape, Save (check that the Save button greys out; one save on Oct 21 didn't take), Exit.
2. curl `https://www.mahjmatchmaker.com/?v=$RANDOM` contains the block byte for byte (`first!==b`).
3. Menu naming (coordinator, Oct 21): ™ once per page, on the H1/hero. Nav link "Find Your Mat-ch™" → **"Find Your Mat-ch"** (Pages > Find Your Mat-ch™ > ⚙ > Navigation Title), announcement bar text drops ™ too. Italic "Your" in the nav needs a small script (the announcement bar already has it).
4. Delete the `/home-preview` page afterwards (or leave it Not Linked + noindex).

## Not done here (flagged)
- The approved Oct 19 menu plan (Mahjong Matches ▾ and Community ▾ dropdowns) predates today's live menu (Mahjong Matches · Mat Gallery · Holiday ▾ · Find Your Mat-ch™ · Discount Codes · Shop My Finds · Blog · Community · About). Restructuring would move Mat Gallery and Holiday. Not changed; needs main's/Tiffany's call on the target menu.
- The launch-day hero (`launch-oct27/hero-graphic`) still uses the match-card fan, which her 3:13pm rule (FYM promotion shows the TOOL) now argues against. Not touched per instructions.
- The header "button" (Squarespace header CTA) is off on the live site; the hero button on the old hero read "Find Your Match" (now hidden by this block).
