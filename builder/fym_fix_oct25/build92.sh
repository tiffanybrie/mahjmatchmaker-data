#!/bin/bash
# FYM v92 = v91 (b91f) + Bespoke re-cuts + rack defringe + Bam Bird splits + Splash batch 2 + coordinated first + version label
set -e; S=$1; D=$2; H=$(dirname "$0")
rm -rf "$D"; cp -r "$S" "$D"
python3 $H/v92_bespokeracks.py "$D"; python3 $H/v92_rackdefringe.py "$D"; python3 $H/v92_tilesplits.py "$D" >/dev/null
python3 $H/v92_splash.py "$D" | tail -1; python3 $H/v92_coordinated.py "$D"
sed -i 's/Version 91/Version 92/g' "$D/index.html"; grep -c "Version 92" "$D/index.html"
