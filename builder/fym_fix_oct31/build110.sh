#!/bin/bash
# FYM v110 = public "Version 1.10" (Oct 31 night): stars (per-device favourites) + Mahj & Moon ShopMy links.
# Usage: build110.sh <b109f dir> <b110 dir> <pub109f dir> <pub110 dir> <site fym-v109 index> <site fym-v110 index>
set -eo pipefail; H=$(dirname "$0")
rm -rf "$2"; cp -al "$1" "$2"; rm "$2/index.html"; python3 $H/patch110.py "$1/index.html" "$2/index.html"
mkdir -p "$4"; python3 $H/patch110.py "$3/index.html" "$4/index.html"; cp "$3/files.json" "$4/files.json"
mkdir -p "$(dirname "$6")"; python3 $H/patch110.py "$5" "$6"
