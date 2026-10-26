#!/bin/bash
# FYM v96 = v95 chain (build95.sh) + rack cleanup (QA v95 item 2c: clean cutouts, poor-photo racks never lead, Bird & Bamboo
# Clear Wood Stain = wood) + version label 96. v96_amazon_holiday.py stays OUT until those mats are colour-matched.
set -e; S=$1; D=$2; H=$(dirname "$0")
bash $H/build95.sh "$S" "$D"
python3 $H/v96_rackclean.py "$D" | tail -1
python3 $H/strip_inline_img.py "$D/index.html" write
sed -i 's/Version 95/Version 96/g' "$D/index.html"; grep -c "Version 96" "$D/index.html"
