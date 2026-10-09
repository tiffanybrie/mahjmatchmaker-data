#!/usr/bin/env bash
# Daily refresh: partner catalogs + album matches -> data.json, catalog.json
set -euo pipefail
R="$(cd "$(dirname "$0")/.." && pwd)"; W="$R/work"; S="$R/scripts"
mkdir -p "$W/raw" "$W/thumbs" "$W/albums"; cd "$W"
cp "$R"/config/*.tsv "$R"/config/*.json "$R"/config/hub-at-a-glance.html .
cp "$S"/*.py .
python3 pull.py
python3 normalize.py >/dev/null
python3 -c "
import json,hashlib
it=json.load(open('items.json'))
with open('thumb-list.txt','w') as f:
  for i in it:
    if i['i']:
      h=hashlib.md5(i['i'].encode()).hexdigest()[:16]
      f.write(i['i']+('&' if '?' in i['i'] else '?')+'width=120 thumbs/'+h+'.jpg\n')"
sort -u thumb-list.txt | xargs -P 8 -n 2 sh -c 'test -s "$1" || curl -sS -m 30 -o "$1" "$0" || true'
python3 colors.py
python3 bbracks.py
python3 compact.py
curl -sS -m 30 https://www.mahjmatchmaker.com/sitemap.xml | grep -o '<loc>[^<]*-mahjong-tile-matches</loc>' | sed 's/<[^>]*>//g' | grep -v -E '/(pink|blue|green|yellow-orange|purple|neutral|masculine)-mahjong-tile-matches$' > album-urls.txt
rm -f albums/*.html
while read u; do curl -sS -m 30 -o "albums/$(basename "$u").html" "$u"; done < album-urls.txt
python3 parse.py && python3 data.py && python3 link.py
cp data.json catalog.json "$R/"
date -u +"%Y-%m-%dT%H:%M:%SZ" > "$R/updated.txt"
