#!/bin/bash
# FYM v104 = public "Version 1.8" (Oct 30) = v103 + brand-logo opening view + partner sweep mats + tile photo fills + Brownstone racks.
# Usage: build104.sh <b103 dir> <out dir>. Out = hardlinks of b103 + new index / new files only (never edits b103 files).
set -eo pipefail; S=$1; D=$2; H=$(dirname "$0"); R=$H/../..
rm -rf "$D"
python3 $R/builder/fym_fix_oct30_logos.py "$S" "$D"
python3 $H/partneradds.py "$D"
python3 $R/builder/fym_fix_oct25/strip_inline_img.py "$D/index.html" write
python3 $H/v104data.py "$D"
grep -c "Version 1.8" "$D/index.html"
