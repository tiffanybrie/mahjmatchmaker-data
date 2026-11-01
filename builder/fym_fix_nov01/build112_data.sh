#!/bin/bash
# v112 DATA + UI layer from the Nov 1 MATCH-INBOX sweep (README.md here). Run it on top of the newest build (v111 accounts),
# (v112 final: + plm112 + ui112b, then version 1.12 / strip_inline_img / v105_imgout / site112.py / artifact112.py)
# then bump the version string / strip inline images / site + artifact copies the way build109.sh / build110.sh do.
# Usage: build112_data.sh <source build dir (b111)> <out dir (b112)>. Out = hardlinks of source + NEW files only.
set -eo pipefail; S=$1; D=$2; H=$(dirname "$0"); R=$H/../..
rm -rf "$D"; cp -al "$S" "$D"; rm "$D/index.html"; cp "$S/index.html" "$D/index.html"
python3 $H/adds112.py "$D"                                 # 16 mats + twins alt + Sunday relink + 12 racks (hidden, pending cut-out)
python3 $R/builder/fym_fix_oct30/v104rank.py "$D"           # colour-rank the new mats (gate [107])
python3 $H/cr112.py "$S/index.html" "$D"                 # keep each set's established top-5 (gate [76])
python3 $H/fixes112.py "$D"                                # Dapper 2, MRC tortoise, YMI Ivory merge, holiday calls, Chinoiserie Cheer, Poppins, ncn, MS name
python3 $H/rackfit112.py "$D"                              # rack lengths + tile widths
python3 $H/ui112.py "$D"                                   # titles, colour sections, brand copy, TdT, rack fit, tortoise order, BACKG
python3 $R/builder/fym_fix_oct25/v98_matflat.py "$D"        # angled mat photos flattened (gate [89]); WIP from Oct 26, every result was looked at
python3 $H/plm112.py "$D"                                 # PLM Chartreuse racks -> her shade A (186,212,96), Oct 26 8:53pm
python3 $H/ui112b.py "$D"                                  # In stock only toggle (config/fym-stock.json from scripts/fym_stock_check.py) + account sheet headings
python3 $H/gate_nov01.py "$D"
python3 $R/builder/fym_gate.py "$D"
