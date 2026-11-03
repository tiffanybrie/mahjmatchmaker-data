#!/bin/bash
# v114 claude.ai ARTIFACT copy: the QA'd pub113 artifact copy + Table view + price filter (no new files: pub113's mc/190.webp is the only
# non-index file it changes vs the live v112 artifact). Usage: artifact114.sh <pub113 dir> <pub114 dir>
set -eo pipefail; P=$1; O=$2; H=$(dirname "$0"); R=$H/../..
mkdir -p "$O/mc"; cp "$P/mc/190.webp" "$O/mc/190.webp"; cp "$P/files.json" "$O/files.json"
python3 $R/builder/table_view/preview_nov01.py "$P/index.html" "$O" --release 1.14
python3 $H/price114.py "$O"
python3 $H/ui114.py "$O"   # rack filter singles + Table tour step (Tiffany Nov 1 11:33pm)
python3 $H/ui114b.py "$O"   # rack filters below the rack deck (Tiffany Nov 3 2:27pm)
ls -l "$P/index.html" "$O/index.html" "$O/mc/190.webp"
