#!/bin/bash
# FYM v100 = public "Version 1.4" (Oct 27 night): full chain v97 -> build98 (with the PLM Chartreuse = her album rack) -> build99
# (rack pass + QA reverts) -> v100_title (no outline/darkening) -> v100b_title (album colours, her calls). Usage: build100.sh <b97> <out>
set -eo pipefail; S=$1; D=$2; H=$(dirname "$0"); T=$(mktemp -d)
bash $H/build98.sh "$S" "$T/b98" | tail -1
bash $H/build99.sh "$T/b98" "$D" | tail -1
python3 $H/v100_title.py "$D"; python3 $H/v100b_title.py "$D" dark
sed -i "s/(Version 1.3)/(Version 1.4)/g; s/Version 1.3/Version 1.4/g" "$D/index.html"; grep -c "Version 1.4" "$D/index.html"; rm -rf "$T"
python3 $H/v100c_sheet.py "$D"
python3 $H/v100d_sheet.py "$D"
