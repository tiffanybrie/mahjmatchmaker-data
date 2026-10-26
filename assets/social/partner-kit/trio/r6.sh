export SRCPATCH='rh=Math.min(bot-top-lch-30,Math.max(2*r+40,n*170)),rx=30,ry=Math.max(top+110,Math.min(cy-rh/2+48,bot-rh-lch-10))|||rh=Math.min(bot-top-lch-30,n*150),rx=30,ry=bot-rh-lch+20'
timeout 220 python3 shot.py "Classic Tortoise" "Vegan Leather – Caramel" "Bam Bird Boutique" dbam "" "www.bambirdboutique.com/wooden-mahjong-rack-pusher-set,www.bambirdboutique.com/wooden-mahjong-rack-pusher-set?v=53195340972341"
timeout 220 python3 shot.py "House Hearts Warm White" "Jardín de Los Jefes" "Tigre de Tartan" dtdt "" "bb:Retro Mustard,bb:Matcha"
timeout 220 python3 shot.py "Nutcracker Ballet" "Clara's Dream Christmas" "Mahj Squad" dsq "" "bb:Bronze Metallic,bb:Matcha"
timeout 220 python3 shot.py "Heirloom Collection Crown Jewels" "Crown Jewels" "Royal Mahjong Society" droy "" "bb:Harbor Blue,bb:Gold Metallic"
timeout 220 python3 shot.py "Lagoon" "Pink Winds" "Amanda Toppe" dtop "" "bb:French Blue,bb:Peony"
timeout 220 python3 shot.py "Heritage 2.0" "Walk in the Park" "Britt Mills" dbri "" "bb:Jade,bb:Peach Metallic"
timeout 220 python3 shot.py "Floréa" "Aurelia" "Virora Mahjong" dvir "" "bb:Cornflower Blue,bb:Lavender"
timeout 220 python3 shot.py "Toucan" "Seabee Avenue Monstera Plant Mat" "Middle & Main Mahjong" dymi "" "bb:Turks Blue,bb:Mermaid"
timeout 220 python3 shot.py "East Meets West Tortoise" "Saint-Rémy" "Fait à Main" dfam "" "bb:Ocean Slate,bb:Weathered Oak"
for p in "dbam|Bam Bird Boutique" "dtdt|Tigre de Tartán" "dsq|Mahj Squad" "droy|Royal Mahjong Society" "dtop|Amanda Toppe" "dbri|Britt Mills" "dvir|Virora Mahjong" "dymi|Yellow Mountain Imports" "dfam|Fait à Main"; do IFS='|' read o b <<< "$p"; [ -f ${o}_card.png ] || continue; timeout 150 python3 comp.py $o "$b" >/dev/null 2>&1; python3 -c "
from PIL import Image
i=Image.open('${o}_card.png').convert('RGB');w,h=i.size;i.crop((0,int(h*0.22),w,int(h*0.8))).save('review/img/$o-card.jpg',quality=86)
Image.open('$o-story.png').convert('RGB').save('review/img/$o-story.jpg',quality=88)"; done
echo ALLDONE
