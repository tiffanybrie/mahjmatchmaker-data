#!/bin/bash
# FYM 1.18 catalog adds from the Nov 7 ShopMy cross-check (config/shopmy-crosscheck-nov07.json). Run on the 1.18 build dir AFTER the
# 1.17 chain (build117.sh) and BEFORE fym_apply_locks / colour116 / gate. Stage only: publishing follows the normal release (gate,
# independent QA, artifact + website + gallery_sync v118 + search).
#  1. shopmy_nov07.py: 25 ShopMy mats (Mahj & Moon x5, Rebecca Illustrated x8 incl. 2 Questionable hidden, Waiting On Martha x3,
#     The Mahjong House Ruby Table, Southern Living x3, Case-Mate x4 colourways, OMM x Tuckernuck In Full Bloom) + fixes
#     (Luna Hummingbird Mint hidden/Questionable; ShopMy links for Blue Pastel Palm Beach + Rainbow Row).
#  2. v96_amazon_holiday.py: Tiffany's 28 Amazon holiday picks (Oct 26 11:16), held out of v96 and never re-added; colours by eye Nov 7.
# Usage: adds118.sh <build_dir>
set -eo pipefail; H=$(dirname "$0"); R=$(cd "$H/../.." && pwd)
python3 "$H/shopmy_nov07.py" "$1" | tail -3
python3 "$R/builder/fym_fix_oct25/v96_amazon_holiday.py" "$1" | tail -2
