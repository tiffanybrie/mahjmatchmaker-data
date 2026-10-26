export TCAUTO=1
export SRCPATCH='rh=Math.min(bot-top-lch-30,Math.max(2*r+40,n*170)),rx=30,ry=Math.max(top+110,Math.min(cy-rh/2+48,bot-rh-lch-10))|||rh=Math.min(bot-top-lch-30,n*150),rx=30,ry=bot-rh-lch+20'
TCFIX= timeout 220 python3 shot.py Cypress "Marigold" "Mahjong Row & Co." mrc "Mahjong Row & Co." "mahjongrowandco.com/autumn-brown-rack-pusher-set,mahjongrowandco.com/scalloped-deluxe-tortoise-rack" "mrc_ab.png,mrc_st.png"
TZOOM=1.7 timeout 220 python3 shot.py "The Allure" "The Paradise - Island Green" "Bird & Bamboo" bb "Bird & Bamboo" "bb:Tiffany Dusk,bb:Peony" ""
timeout 220 python3 shot.py "Papaya Spritz" "Vivienne" "Oh My Mahjong" omm "Oh My Mahjong" "www.ohmymahjong.com/pink-quartz-rack-and-pusher-set,www.ohmymahjong.com/tortoise-shell-rack-pusher" ""
timeout 220 python3 shot.py "Miss Classic Jade" "Festival Jade" "Miss Mahjong" mmj "Miss Mahjong" "missmahjong.com/iridescent-opal-scalloped-acrylic-racks,missmahjong.com/jade-and-brass-acrylic-racks" ""
timeout 220 python3 shot.py "Brownstone Bloom" "Brownstone Bloom" "Anders Ruff" ar "" "www.bambirdboutique.com/wooden-mahjong-rack-pusher-set,www.bambirdboutique.com/wooden-mahjong-rack-pusher-set?v=53195340972341" ""
for p in "mrc|Mahjong Row \& Co.|mrc" "bb|Bird \& Bamboo|bb" "omm|Oh My Mahjong|omm" "mmj|Miss Mahjong|mmj" "ar|Anders Ruff|ar"; do IFS='|' read o b n <<< "$p"; timeout 150 python3 comp.py $o "$b" >/dev/null 2>&1; mkdir -p final; cp $o-story.png final/$n-story.png; cp $o-post.png final/$n-post.png; python3 -c "
from PIL import Image
i=Image.open('${o}_card.png').convert('RGB');w,h=i.size;i.crop((0,int(h*0.22),w,int(h*0.8))).save('review/img/$n-card.jpg',quality=86)
Image.open('$o-story.png').convert('RGB').save('review/img/$n-story.jpg',quality=88)"; done
echo ALLDONE
