export SRCPATCH='rh=Math.min(bot-top-lch-30,Math.max(2*r+40,n*170)),rx=30,ry=Math.max(top+110,Math.min(cy-rh/2+48,bot-rh-lch-10))|||rh=Math.min(bot-top-lch-30,n*150),rx=30,ry=bot-rh-lch+20'
timeout 220 python3 shot.py "Hunt Club Edition" "The Hunt Club" "Charleston Mahjong Club" cmc "Charleston Mahjong Club" "www.bambirdboutique.com/wooden-mahjong-rack-pusher-set" ""
TCFIX='#DE8A6C' TZOOM=1.6 timeout 220 python3 shot.py "Peach & Pine" "SOIRÉE Leatherette" "Britt Mills" mm "Middle & Main Mahjong" "www.middleandmainmahjong.com/golden-grain-beechwood-mahjong-rack-and-pusher-set-of-4,www.middleandmainmahjong.com/milk-glass-collection-mahjong-rack-and-pusher-set-of-4" ",mm_milk_cut.png"
timeout 220 python3 shot.py "Hunt Club Edition" "The Hunt Club" "Charleston Mahjong Club" cmc3 "Charleston Mahjong Club" "www.bambirdboutique.com/wooden-mahjong-rack-pusher-set,plm:Dark Green" ""
timeout 220 python3 shot.py "Holly Jolly (Rudolph" "Holly Jolly Christmas" "Bam! Let's Mahjong" bam1 "Bam! Let's Mahjong" "www.bamletsmahjong.com/mahjong-acrylic-racks-and-ruffle-pushers-pre-order,www.bamletsmahjong.com/white-wooden-racks-set-4" ",../bamr/w4rack.png"
timeout 220 python3 shot.py "Rackin" "Rackin' Rudolph !" "Hip Hip Mahjong" hip1 "" "mm:Hawksbill,bb:Cherry Red"
timeout 220 python3 shot.py "Let's Garden Party" "Let’s Mahj-On! Floral Mat" "Let's Mahj On" lmo1 "" "mahjmood.com/baby-blue-wooden-racks-with-scalloped-pushers,bb:Peony" "../lmo/bb_one3.png,"
for p in "cmc|Charleston Mahjong Club|cmc" "cmc3|Charleston Mahjong Club|cmc3" "mm|Middle \& Main Mahjong|mm" "bam1|Bam! Let's Mahjong|bam" "hip1|Hip Hip Mahjong|hip" "lmo1|Let's Mahj On|lmo" "bspB|Bespoke Mahjong|bsp"; do IFS='|' read o b n <<< "$p"; timeout 150 python3 comp.py $o "$b" >/dev/null 2>&1; python3 -c "
from PIL import Image
Image.open('$o-story.png').convert('RGB').save('review/img/$n-story.jpg',quality=88)
i=Image.open('${o}_card.png').convert('RGB');w,h=i.size;i.crop((0,int(h*0.22),w,int(h*0.8))).save('review/img/$n-card.jpg',quality=86)"; done
echo ALLDONE
