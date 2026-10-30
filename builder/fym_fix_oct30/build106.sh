#!/bin/bash
# FYM v106 = public "Version 1.9.1" (Oct 30 eve) = v105 + racks-step brand filter shows ALL the brand's racks (Tiffany 5:14pm)
# + B&B wood stains get the Wood chip + White Wood Stain + YOLO Mahjong catalog (63 mats, 2 racks, Journey to the West tiles)
# + Noli June 5 mats (missed NEW PARTNER handoffs, Tiffany 5:16pm). Usage: build106.sh <b105 dir> <out dir>.
# Out = hardlinks of b105 + NEW files only (never writes through a hardlink).
set -eo pipefail; S=$1; D=$2; H=$(dirname "$0"); R=$H/../..
rm -rf "$D"; cp -al "$S" "$D"; rm "$D/index.html"; cp "$S/index.html" "$D/index.html"
python3 $H/partneradds106.py "$D"
python3 $H/v104rank.py "$D"
python3 $H/v106extra.py "$D"
python3 $R/builder/fym_fix_oct25/strip_inline_img.py "$D/index.html" write
python3 $H/v105_imgout.py "$D"
grep -c "Version 1.9.1" "$D/index.html"
