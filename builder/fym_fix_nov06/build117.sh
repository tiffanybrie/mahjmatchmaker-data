#!/bin/bash
# FYM v117 = "Version 1.17" (Nov 6 night) = the full build116.sh content (1.16 r1 went live first) + by-eye colour fixes from 1.17 QA
# item d (config/fym-colour-fixes-v116.json 'eye', applied by colour116.py; gate [163]). Usage: build117.sh <b115 dir> <b117 dir>
set -eo pipefail; H=$(dirname "$0")
"$H/build116.sh" "$1" "$2"
python3 $H/release117.py "$2"
