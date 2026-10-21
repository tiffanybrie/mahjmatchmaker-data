# Announcement bar: Find Your Mat-ch countdown. LIVE Oct 21, 2026 (~1pm ET)

Tiffany approved Oct 21, 12:42pm ("yes to both the announcement bar and also to the 10/27 launch day switch").

## What is live
- Squarespace built-in Announcement Bar (Pages > Website Tools > Announcement Bar, URL `/config/pages/announcement-bar`). Enabled, site-wide.
- Message (rich text): `Find <em>Your</em> Mat-ch™ arrives 10.27 · Get notified`. The italic on "Your" was applied with the editor's I button.
- Link: `/find-your-match` (the "Coming 10.27" teaser page with the signup; returns 200). Same window.
- Colours: navy `#062a55` background, white text and close X. Set in **Custom CSS** (appended at the very end, under the comment `/* Announcement bar: Find Your Mat-ch launch countdown (Oct 21, Claude) ... */`). The block is in `custom-css-snippet.css`.
- One line on phone: 390px renders 1 line at 13px, no sideways scroll. 1280px renders 1 line at 14.4px.

## Verify
- `curl -s https://www.mahjmatchmaker.com/ | grep -o 'announcementBarSettings.\{0,230\}'` shows `"style":2` (on) and the text + `/find-your-match`. Same on `/oh-my-mahjong-discount-code` and `/find-your-match`.
- `curl -s https://www.mahjmatchmaker.com/site.css | grep -o 'sqs-announcement-bar{background-color:#062a55[^}]*}'`
- Screenshots: `qa/home-390.png`, `qa/home-1280.png`, `qa/brand-omm-390.png`, `qa/brand-omm-1280.png`. Note: the 1280px scrollWidth of 1494 is the existing header nav overflow, not the bar.

## Turn it off (launch day, Tue 10/27, see ../launch-oct27/README.md)
Website Tools > Announcement Bar > toggle **Enable Announcement Bar** off > Save. Leave the CSS block in place (harmless when the bar is off; reusable for the next announcement).
