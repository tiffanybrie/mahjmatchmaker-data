#!/bin/bash
# FYM v107 = public "Version 1.9.2" (Oct 31): code-only patch on v106 (logo breathing room, searched mat obeys filters,
# Noli June $100 min in the shop list only, no '(retired)' on the card, aerial tile inset = --onmat-w 40%).
# Usage: build107.sh <b106 dir> <b107 dir> <pub106 dir> <pub107 dir> <fym-site repo>
#  - app build:      <b107>/index.html (hardlinks of b106 + a NEW index)
#  - artifact copy:  <pub107>/index.html only (b24v1.js / mc/190.webp unchanged from 1.9.1 -> files map = index only)
#  - website copy:   <fym-site>/site-app/fym-v107/index.html (same absolute CDN photo paths as fym-v106)
set -eo pipefail; S=$1; D=$2; PS=$3; PD=$4; SITE=$5; H=$(dirname "$0")
rm -rf "$D"; cp -al "$S" "$D"; rm "$D/index.html"; python3 $H/patch107.py "$S/index.html" "$D/index.html"
mkdir -p "$PD"; python3 $H/patch107.py "$PS/index.html" "$PD/index.html"
mkdir -p "$SITE/site-app/fym-v107"; python3 $H/patch107.py "$SITE/site-app/fym-v106/index.html" "$SITE/site-app/fym-v107/index.html"
grep -c "Version 1.9.2" "$D/index.html"
