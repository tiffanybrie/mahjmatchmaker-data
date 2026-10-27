#!/bin/bash
# FYM v101 = public "Version 1.5" (Oct 27) = v100d (Version 1.4, build100.sh) + v101_partneradds.py: partner mats the store sweep
# found missing (config/fym-partner-adds-oct27.json; gate [100] reads config/partner-mat-sweep.json) + PLM Spirit of Christmas tile
# set (sold out label T.so; her Spirit swipe book picks). Usage: build101.sh <b100d dir> <out dir>
set -eo pipefail; S=$1; D=$2; H=$(dirname "$0")
rm -rf "$D"; cp -r "$S" "$D"
python3 $H/v101_partneradds.py "$D"
python3 $H/strip_inline_img.py "$D/index.html" write
sed -i "s/(Version 1.4)/(Version 1.5)/g; s/Version 1.4/Version 1.5/g" "$D/index.html"; grep -c "Version 1.5" "$D/index.html"
ls -la "$D/index.html"
