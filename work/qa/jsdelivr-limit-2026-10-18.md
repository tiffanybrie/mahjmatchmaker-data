# jsDelivr "Package size exceeded 50 MB" — findings (Oct 18, 2026)

## What's happening
- The data repo is about 1.4 GB checked out (about 1.9 GB on GitHub). That's far above jsDelivr's 50 MB limit for GitHub packages.
- jsDelivr still serves single files from it. But the **first** request for a file that hasn't been requested before *sometimes* comes back 403 "Package size exceeded the configured limit of 50 MB". A retry seconds later returns 200, and from then on the file stays cached.
- At the newest commit, 3 of 10 never-requested files 403'd on the first try (README.md, kit.html, pins.csv). All 3 returned 200 on retry.

## How bad it is on the live site
- I scanned all 112 live pages from the sitemap, plus the nested code-block content they load: **760 jsDelivr URLs**.
- **All 760 returned 200 on the first try.** Everything the live site uses today was already cached, so visitors aren't seeing broken images right now.
- I also checked the pending files: the livepatch blocks, the FYM builds and the Pinterest pins (1,074 real URLs). 14 of them (about 1.3%) 403'd on the first try and returned 200 on retry. Nothing still fails.

## What I did (stopgap, option d)
- Warmed every URL: each one was requested with retries until it returned 200, so jsDelivr now has it cached. Nothing on the site was edited.
- Script: `scripts/jsdelivr/warm.py <subfolder>` (set WARM_DIR to the parent folder). It pulls every jsDelivr URL out of the pages, follows any nested .html/.js/.json, and retries up to 8 times.
- **Rule from now on:** before any new pinned-commit block goes live, warm its URLs with this script first. The risk is only on the very first request for a file at a new commit.

## Options weighed for a durable fix
| Option | Verdict |
|---|---|
| (a) Slim assets repo on jsDelivr | **Doesn't fix it alone.** The assets the live pages use come to about 374 MB, still over 50 MB, so jsDelivr would behave the same way. |
| (b) raw.githubusercontent.com | Works and the CORS header is fine, but HTML comes back as text/plain, the cache is only 5 minutes, and it's rate-limited. Not for production. statically.io just returned a 301 redirect. |
| (c) Squarespace asset library | The most robust option (Squarespace's own CDN), but it means uploading by hand or by script through her editor, 1,200+ files, with new URLs for everything. Too heavy before launch. |
| **(a+) Slim public repo + GitHub Pages** | **Recommended.** A new public repo `mahjmatchmaker-assets` holds only the web assets (about 400 MB, under Pages' 1 GB limit). GitHub Pages serves them over Fastly with correct content types and no package limit. It can go on a subdomain such as `assets.mahjmatchmaker.com`. Blocks would then point at `https://tiffanybrie.github.io/mahjmatchmaker-assets/...` (or the subdomain), with versioned file names in place of commit pins. |

## Recommendation
1. **Before launch (Oct 27):** keep jsDelivr and warm every new URL before it goes live. This is in place now and costs nothing.
2. **After launch:** move to the slim Pages repo, one page at a time, then swap each block's URLs.

Approval lines Tiffany would need:
- "Approve creating a public GitHub repo mahjmatchmaker-assets and turning on GitHub Pages for it."
- Optional: "Approve adding assets.mahjmatchmaker.com as a DNS record for the assets site." (This is a domain/DNS change.)
- Later, per batch of pages: "Approve switching the live pages' images to the new assets site."

The jsDelivr documentation page wasn't reachable from here: the permission request for jsdelivr.com/documentation timed out. These findings are empirical.
