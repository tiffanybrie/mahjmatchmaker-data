#!/bin/bash
# v114 WEBSITE copy (site-app/fym-v114 on fym-site-preview): b114 = b113 + Table view + price filter, nothing else, so the site
# copy = the QA'd site v113 index + the same two steps (its CDN routing, thumbs113.js, hd index and absolute photo URLs carry over).
# No new chunks or thumbnails (v114 adds no catalog items). Usage: site114.sh <fym-site repo dir>
set -eo pipefail; SITE=$1; H=$(dirname "$0"); R=$H/../..
mkdir -p "$SITE/site-app/fym-v114"
python3 $R/builder/table_view/preview_nov01.py "$SITE/site-app/fym-v113/index.html" "$SITE/site-app/fym-v114" --release 1.14
python3 $H/price114.py "$SITE/site-app/fym-v114"
python3 $H/ui114.py "$SITE/site-app/fym-v114"   # rack filter singles + Table tour step (Tiffany Nov 1 11:33pm)
python3 $H/ui114b.py "$SITE/site-app/fym-v114"   # rack filters below the rack deck (Tiffany Nov 3 2:27pm)
ls -l "$SITE/site-app/fym-v114/index.html"
