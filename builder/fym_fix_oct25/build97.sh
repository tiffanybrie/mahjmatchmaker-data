#!/bin/bash
# FYM v97 = public "Version 1.1" (docs/FYM-VERSIONS.md) = v96 (Version 1.0, built by build96.sh) + docs/MATCH-INBOX.md Oct 26 evening:
# sticky search + accent-blind search + mat-door Add racks (v97_ui), 5 hidden MFM sets + YMI Mojave unhidden and Jubilee Midnight
# Blue added (v97_mfm), PLM tile band framing (v97_plmfocus), MFM Natural Wood featured + PLM painted racks re-cut (v97_racks),
# mat photos without white bands (v97_matwhite). Usage: build97.sh <b96 dir> <out dir>
set -eo pipefail; S=$1; D=$2; H=$(dirname "$0")
rm -rf "$D"; cp -r "$S" "$D"
python3 $H/v97_ui.py "$D" | tail -1
python3 $H/v97_mfm.py "$D" | tail -3
python3 $H/v97_plmfocus.py "$D" | tail -1
python3 $H/v97_racks.py "$D" | tail -1
python3 $H/v97_matwhite.py "$D" | tail -1
python3 $H/strip_inline_img.py "$D/index.html" write
sed -i "s/(Version 1.0)/(Version 1.1)/g; s/Version 1.0/Version 1.1/g" "$D/index.html"; grep -c "Version 1.1" "$D/index.html"
ls -la "$D/index.html"
