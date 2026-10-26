#!/bin/bash
# FYM v94 = v93 + tile door A-Z (no default chip) + Photo coming soon last / Blue Studio / Aloha split + CMC uniform photos
# + Mahjong Studios per-set photos + rack lead rules + YMI splits + Bespoke tiles off black + missing partner products
# (+ Virora grid3 only with her yes: pass VIRORA=1). Thin-album picks are NOT here (they wait for the album pages to go live).
set -e; S=$1; D=$2; H=$(dirname "$0"); H6=$H/../fym_fix_oct26
rm -rf "$D"; cp -r "$S" "$D"
python3 $H/v94_tiledefault.py "$D"; python3 $H/v94_soonlast.py "$D"
python3 $H/v94_cmc.py "$D" >/dev/null
if [ -n "$MS" ]; then python3 $H/v94_mstudios.py "$D" | tail -2; fi
if [ -n "$YMI" ]; then python3 $H/v94_ymi.py "$D" | tail -2; fi
if [ -n "$BESPOKE" ]; then python3 $H/v94_bespoketiles.py "$D" | tail -2; fi
if [ -n "$PARTNERS" ]; then python3 $H/v94_partneradds.py "$D" | tail -2; fi
if [ -n "$VIRORA" ]; then python3 $H/v94_virora_grid3.py "$D" | tail -2; fi
if [ -n "$ZOOM" ]; then python3 $H/v94_tilezoom.py "$D" | tail -2; fi
python3 $H/v95_gatsby_hummingbird.py "$D" | tail -2
python3 $H6/v94_rackquality.py "$D" | tail -2
grep -c "Version 94" "$D/index.html"
