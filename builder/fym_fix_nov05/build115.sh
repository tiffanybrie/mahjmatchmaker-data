#!/bin/bash
# FYM v115 = public "Version 1.15" (Nov 5): b114 + usage tracking ON (TRK_URL, gate [157]) + catalog adds (DESK 2b): Mahj Pit, OMM Juniper +
# Lotus Cove (coordinated), Noli FA LA LADIES x4, LBB x10 (+ Camellia leatherette twin), Bespoke Sunshine Glow + Glitter Glow Green,
# 33 ShopMy Etsy mats, Britt Mills Isla, Santa Baby's Cocktail Hour + late-holiday m-lists, Esme retired, House Tigers Oyster in stock.
# Usage: build115.sh <b114 dir> <b115 dir>. Out = hardlinks to b114 + NEW files (b114 is never modified).
set -eo pipefail; S=$1; D=$2; H=$(dirname "$0"); R=$H/../..
rm -rf "$D"; cp -al "$S" "$D"; rm "$D/index.html"; cp "$S/index.html" "$D/index.html"
python3 $H/spec115.py
python3 $H/adds115.py "$D"
python3 $R/builder/fym_fix_nov03/etsy_shopmy_nov03.py "$D"           # 33 ShopMy Etsy mats (weekly ShopMy check Nov 3)
python3 $R/builder/fym_fix_oct30/v104rank.py "$D"                     # colour-rank the new mats (gate [107])
python3 $H/cr115.py "$S/index.html" "$D"                              # new mats never push a set's top 5 out (gate [76])
python3 $R/builder/fym_fix_oct25/v92_coordinated.py "$D"              # Juniper -> Lotus Cove first (config/fym-coordinated.json, gate [57])
python3 $H/misc115.py "$D"                                            # late holiday m-lists, Esme retired, Oyster in stock, Camellia twin
python3 $H/release115.py "$D"                                         # Version 1.15 + TRK_URL
python3 $R/builder/fym_apply_locks.py "$D"
