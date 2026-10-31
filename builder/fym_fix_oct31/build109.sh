#!/bin/bash
# FYM v109 = public "Version 1.9.4" (Oct 31 eve): Etsy non-partner brands Tiffany chose 'Bring in now': Betty June & Jeannette (new
# listings beyond the 23 in FYM) + Piper Chase Studios (whole mat line), ShopMy links (spec109.py -> config/fym-nonpartner-adds-oct31b.json).
# Usage: build109.sh <b108 dir> <b109 dir>. Out = hardlinks of b108 + NEW files only.
set -eo pipefail; S=$1; D=$2; H=$(dirname "$0"); R=$H/../..
rm -rf "$D"; cp -al "$S" "$D"; rm "$D/index.html"; cp "$S/index.html" "$D/index.html"
python3 $H/partneradds109.py "$D"
python3 $H/v109cream.py "$D"
python3 $R/builder/fym_fix_oct30/v104rank.py "$D"
python3 $H/v109cr.py "$S/index.html" "$D"
python3 - "$D/index.html" <<'PY'
import sys; p=sys.argv[1]; h=open(p).read(); h=h.replace('Version 1.9.3<','Version 1.9.4<').replace('(Version 1.9.3)','(Version 1.9.4)'); assert h.count('Version 1.9.4')==2; open(p,'w').write(h)
PY
python3 $R/builder/fym_fix_oct25/strip_inline_img.py "$D/index.html" write
rm -f "$D/b24v1.js.tmp"; python3 $R/builder/fym_fix_oct30/v105_imgout.py "$D"
grep -c "Version 1.9.4" "$D/index.html"
