# Launch-day homepage switch. Tue Oct 27, 2026, 9:00am CT (14:00 UTC). STAGED, not live

Tiffany approved Oct 21, 12:42pm: "yes to both the announcement bar and also to the 10/27 launch day switch".
A one-time scheduled task ("Launch day: switch homepage hero + remove announcement bar") runs these steps at 9:00am CT.

**Launch time source:** `docs/content-strategy-oct-dec.md`, Tue Oct 27 row: launch row post 1 "Find *Your* Mat-ch™ is live" carousel, IG feed, Auto **9am** (that doc's times are Central, CDT until Nov 1). HQ `hq/launchPlan` gives the date (Tue Oct 27) but no time.

## Where the hero lives
Homepage (`/`), first page section `69b1d01489d0f8016ee3d59f` (fluid engine, background image `loveshackfancy-coquette-mahjong-tiles-fleur-mat.jpg`). Two **native** Squarespace blocks, no code block:
| Block | Now | Launch |
|---|---|---|
| Text block `block-b79726a6f150a9dd219f` (H1 + H4, white 68% panel) | H1 `Find the Perfect Mahjong Match` / H4 `Match mahjong tiles, mats, and racks across brands` | H1 `Find Your Mat-ch™ is here` / H4 `Start with your tiles or your mat and swipe your perfect match.` |
| Button block `block-yui_3_17_2_1_1773260945246_2648` | `Find Your Match` → `/mahjong-tile-matches` | `Start swiping` → `/find-your-match` |

Layout, image, panel, fonts, colours and block positions do not change. Only the words and the button link change.

**Italic on "Your":** the hero H1 font is already a fully italic display face, so an `<em>` on "Your" does not show and squeezed the space after it in the test render. The headline therefore uses plain "Your" (brand guide: italic "where styling allows"). Do not add the italic in the editor.

**Tool URL:** `/find-your-match`. It already exists (teaser "Coming 10.27", page id `6ad6f62ad05b752bba9d1e8d`) and the header nav "Find Your Mat-ch™" already points there. Per `site/livepatch/nav-plan/README.md` and `site/livepatch/pages/README.md`, its content is swapped for the live tool on 10/27; the embed method is in the launch plan (Project doc 54). That swap is a separate job. If the final tool URL changes, update the button link only.

## Files
- `after-text-block.html`: the launch H1 + H4 (as the text block's HTML).
- `before/text-block-b79726a6f150a9dd219f.html`: the live H1 + H4 as of Oct 21 (rollback).
- `before/hero-section-69b1d01489d0f8016ee3d59f.html`: the whole live hero section markup as of Oct 21 (reference).
- `preview.py`: renders the live homepage with the swap applied (`after`) or as-is (`before`) at 390 and 1280.
- `qa/hero-after-390.png`, `qa/hero-after-1280.png`: staged preview. `qa/hero-before-*.png`: before.

## Steps on launch day
Use your OWN Chrome tab (tabs_create_mcp) at `https://hexaflexagon-denim-nhf4.squarespace.com/config`. Never type a password; never accept new terms. Type into fields with `document.execCommand('insertText', false, '...')` after focusing/selecting the field (keyboard typing drops a character). Code blocks (if any need touching) use CodeMirror 6: `document.querySelector('.cm-editor .cm-content').cmTile.view`, then Escape, Save, Exit.

0. **Pre-check the tool page.** `curl -s https://www.mahjmatchmaker.com/find-your-match` must return 200. If it still contains `Coming 10.27`, the tool is not live yet: the hero button would send people to a teaser. In that case re-check every 10 minutes for up to 60 minutes. If it is still the teaser after that, do NOT switch: leave the hero and the bar as they are, log the blocker in HQ and tell Tiffany in one line.
1. **Swap the hero copy.** Pages > Home > **Edit**. The page renders in the site frame (`#sqs-site-frame` iframe). Double-click the text block (`#block-b79726a6f150a9dd219f`).
   - Select the H1 text (triple-click, or a DOM Range over the h1's text node), then `execCommand('insertText', false, 'Find Your Mat-ch™ is here')`. It must stay Heading 1, centred.
   - Select the H4 text and insert `Start with your tiles or your mat and swipe your perfect match.`. It must stay Heading 4, centred.
   - Click outside the block.
2. **Swap the button.** Click the button block, then its pencil/Edit. Button text field: select all, insert `Start swiping`. Link: clear it and insert `/find-your-match` (or pick the "Find Your Mat-ch™" page from the list); open in new tab OFF. Close the panel.
3. **Save, then Exit** the editor (top left). Confirm the page reads "Published".
4. **Announcement bar OFF.** Pages > Website Tools > Announcement Bar (`/config/pages/announcement-bar`) > toggle **Enable Announcement Bar** off > **Save**. Leave its Custom CSS block alone.
5. **Verify** (logged out, with a cache-buster):
   - `curl -s "https://www.mahjmatchmaker.com/?v=$RANDOM"` contains `Find Your Mat-ch™ is here` (or `Mat-ch&trade;`), `Start with your tiles or your mat and swipe your perfect match.`, `Start swiping` and `href="/find-your-match"`; and does NOT contain `Find the Perfect Mahjong Match`.
   - `grep -o 'announcementBarSettings.\{0,40\}'` shows `"style":1` (off) and no `arrives 10.27`. Check a second page too (`/oh-my-mahjong-discount-code`).
   - `/find-your-match` returns 200.
   - Render with local Playwright (`PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`) at 390 and 1280, save to `qa/live-launch-390.png` / `qa/live-launch-1280.png`, and look at them: hero copy as in `qa/hero-after-*.png`, no bar, no sideways scroll at 390.

## Rollback
- Hero: put back the H1 `Find the Perfect Mahjong Match` and H4 `Match mahjong tiles, mats, and racks across brands` (`before/text-block-b79726a6f150a9dd219f.html`); button text `Find Your Match`, link `/mahjong-tile-matches`. Save, Exit.
- Bar (if it should come back): Website Tools > Announcement Bar > on; message `Find Your Mat-ch™ arrives 10.27 · Get notified` with "Your" italic; link `/find-your-match`; Save. (After launch, a bar would need new copy; don't restore "arrives 10.27".)

## After
- HQ log entry (artifact https://claude.ai/artifact/Cor6pKtesou4mFRQ41P6Ye, collection `log`, area "Site").
- Commit `qa/live-launch-*.png` and a "LIVE" note at the top of this README.
