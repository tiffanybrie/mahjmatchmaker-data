#!/bin/bash
# FYM v108 = public "Version 1.9.3" (Oct 31): non-partner brands Tiffany chose 'Bring in now' (Brands to Bring In page):
# Bougie Mahjong whole mat line (75) + Mahj & Moon whole line (22 new + Oct 20 brand-hidden unhidden) + Hutch & Nook whole line (unhidden).
# Usage: build108.sh <b107 dir> <b108 dir>. Out = hardlinks of b107 + NEW files only.
set -eo pipefail; S=$1; D=$2; H=$(dirname "$0"); R=$H/../..
rm -rf "$D"; cp -al "$S" "$D"; rm "$D/index.html"; cp "$S/index.html" "$D/index.html"
python3 $H/partneradds108.py "$D"
python3 $R/builder/fym_fix_oct30/v104rank.py "$D"
python3 $H/v108cr.py "$S/index.html" "$D"
python3 - "$D/index.html" <<'PY'
import sys; p=sys.argv[1]; h=open(p).read(); h=h.replace('Version 1.9.2<','Version 1.9.3<').replace('(Version 1.9.2)','(Version 1.9.3)'); assert h.count('Version 1.9.3')==2; open(p,'w').write(h)
PY
python3 $R/builder/fym_fix_oct25/strip_inline_img.py "$D/index.html" write
rm -f "$D/b24v1.js.tmp"; python3 $R/builder/fym_fix_oct30/v105_imgout.py "$D"
grep -c "Version 1.9.3" "$D/index.html"
