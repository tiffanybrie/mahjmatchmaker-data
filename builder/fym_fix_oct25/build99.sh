#!/bin/bash
# FYM v99 = public "Version 1.3" = v98b (Version 1.2, build98.sh + v98b_fix.py) + RACK PHOTO pass (Tiffany Oct 26 10:07pm):
# every rack the card shows is ONE rack, HORIZONTAL, background removed wherever it cuts cleanly. Cut-outs are made once by
# v99_cut.py from the brands' own photos (config/fym-rack-singles-oct26.json -> assets/racks/v99/*.webp, looked at on white +
# navy); v99_racksingles.py puts them on the cards (r99/*.webp + rk99* thumbnails). Gate [97]. Usage: build99.sh <b98b dir> <out dir>
set -eo pipefail; S=$1; D=$2; H=$(dirname "$0")
rm -rf "$D"; cp -r "$S" "$D"
python3 $H/v99_racksingles.py "$D" | tail -1
python3 $H/strip_inline_img.py "$D/index.html" write
sed -i "s/(Version 1.2)/(Version 1.3)/g; s/Version 1.2/Version 1.3/g" "$D/index.html"; grep -c "Version 1.3" "$D/index.html"
ls -la "$D/index.html"
