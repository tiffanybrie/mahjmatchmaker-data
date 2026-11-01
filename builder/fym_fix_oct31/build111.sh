#!/bin/bash
# FYM v111 = public "Version 1.11" (Oct 31 late night): accounts (Supabase email sign-in) + top-bar My stars + My match cards.
# Usage: build111.sh <b110 dir> <b111 dir> <pub110 dir> <pub111 dir> <site fym-v110 index> <site fym-v111 index>
set -eo pipefail; H=$(dirname "$0")
rm -rf "$2"; cp -al "$1" "$2"; rm "$2/index.html"; python3 $H/patch111.py "$1/index.html" "$2/index.html"
mkdir -p "$4"; python3 $H/patch111.py "$3/index.html" "$4/index.html"; cp "$3/files.json" "$4/files.json"
mkdir -p "$(dirname "$6")"; python3 $H/patch111.py "$5" "$6"
