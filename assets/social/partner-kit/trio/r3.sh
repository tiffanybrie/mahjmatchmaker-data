until [ -f amj3_card.png ] || ! pgrep -f "shot.*py" >/dev/null; do sleep 3; done
TCFIX='#7A5236' timeout 200 python3 shot.py "Radiant Mood Collection White Pearl" "Secret Garden Mat" "Mahj Mood" mmd4 "Mahj Mood" "mahjmood.com/white-wooden-racks-with-scalloped-pushers,mahjmood.com/scalloped-tortoise-acrylic-racks-and-pushers" "mmd_white_angle.png,mmd_tort.png" > mmd4.log 2>&1
timeout 200 python3 shot.py "Rackin" "Rackin' Rudolph !" "Hip Hip Mahjong" hip1 "" "mm:Hawksbill,bb:Cherry Red" > hip1.log 2>&1
for o in jubm jubr juba amj3 mmd4 hip1 bam1; do :; done
timeout 150 python3 comp.py amj3 "Amahj" >/dev/null 2>&1
timeout 150 python3 comp.py mmd4 "Mahj Mood" >/dev/null 2>&1
timeout 150 python3 comp.py hip1 "Hip Hip Mahjong" >/dev/null 2>&1
echo ALLDONE
