#!/bin/bash
# FYM v95 = v94 (published, scratchpad/fym/b94) + Add racks button under chosen mat + 19 Etsy ShopMy mats + Bam Bird tortoise
# scatter + vertical racks rotated + title/subtitle/contrast card polish + tiny-rack fixes + version label 95.
set -e; S=$1; D=$2; H=$(dirname "$0")
rm -rf "$D"; cp -r "$S" "$D"
python3 $H/v92_tilesplits.py "$D" | grep -i tortoise || true
python3 $H/v95_addracks.py "$D" | tail -1
python3 $H/v95_etsy.py "$D" | tail -1
python3 $H/v92_coordinated.py "$D" | tail -1
python3 $H/v95_rackrotate.py "$D" | tail -1
if [ -f $H/v95_racksize.py ]; then python3 $H/v95_racksize.py "$D" | tail -1; fi
python3 $H/v95_titlewidth.py "$D" | tail -1
if [ -f $H/v95_cardpolish.py ]; then python3 $H/v95_cardpolish.py "$D" | tail -1; fi
if [ -f $H/v95_mahjmoon.py ] && [ -n "$MOON" ]; then python3 $H/v95_mahjmoon.py "$D" | tail -1; fi
python3 $H/v95_rackbrand.py "$D" | tail -1
for x in v95_matrank v95_rackphotos v95_qafix; do if [ -f $H/$x.py ]; then python3 $H/$x.py "$D" | tail -1; fi; done
sed -i 's/Version 94/Version 95/g' "$D/index.html"; grep -c "Version 95" "$D/index.html"
