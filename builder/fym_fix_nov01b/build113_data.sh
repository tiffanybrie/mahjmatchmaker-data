#!/bin/bash
# FYM v113 = public "Version 1.13" (Nov 1, Tiffany 4:50am): Sunday Ruby + Forrest, Let's Be Besties full catalog, per-brand cap,
# Dapper explainer hook (off), Dapper 1/2 + Polo Club wfh. Usage: build113_data.sh <b112 dir> <b113 dir>. Out = hardlinks + NEW files.
set -eo pipefail; S=$1; D=$2; H=$(dirname "$0"); R=$H/../..
rm -rf "$D"; cp -al "$S" "$D"; rm "$D/index.html"; cp "$S/index.html" "$D/index.html"
python3 $H/adds113.py "$D"
python3 $R/builder/fym_fix_oct30/v104rank.py "$D"
python3 $R/builder/fym_fix_nov01/cr112.py "$S/index.html" "$D"
python3 $H/ui113.py "$D"
