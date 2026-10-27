"""Launch carousel v4 (Oct 27 2:57am, Tiffany): phone-mock graphics with her picked series: Brownstone Bloom leads
(hero), then The Allure (B&B), Solara x Peppi Peach Cheetah (Mahjong Register), Talulah x Reba (Britt Mills).
Different matches + different views per slide. Our version: code cards (KEEPCODE renders l4_*C_*)."""
import sys
exec(open('comp.py').read().split('def slides(H):')[0])
def tilt(img,w,x,y,deg,z=1): return f'<div style="position:absolute;left:0;top:0;transform-origin:{x+w/2}px {y+w}px;transform:rotate({deg}deg);z-index:{z}">'+phone(img,w,x,y)+'</div>'
def slides(H):
    st=H>1500; T=230 if st else 70; Y=(T+500) if st else 470
    o={}
    o['1-hero']=f'''<div class="c" style="top:{T}px">{pill('NOW LIVE')}<div style="font:400 104px/1.02 Cap;margin-top:26px">{FYM(104)}<sup style="font-size:38px">™</sup><br>is here</div>
<div style="font:italic 400 38px PF;color:#4a3d58;margin-top:18px">Match mahjong tiles, mats &amp; racks across brands</div></div>'''+\
      tilt('home.png',270,120,Y+150,-8,1)+tilt('l4_arC_swipe.png',270,690,Y+150,8,1)+phone('l4_arC_card.png',360,360,Y+40).replace('position:absolute;left:340','position:absolute;z-index:5;left:340')+\
      f'<div class="c" style="top:{Y+(830 if st else 800)}px;font:italic 400 34px PF;color:#4a3d58">Brownstone Bloom by Anders Ruff</div>'
    o['2-swipe']=f'<div class="c" style="top:{T}px">{step(1,"Swipe mats","Pick your tiles, then ♥ the mats you love and ✕ the rest.")}</div>'+\
      tilt('l4_bbC_card.png',330,610,Y-20,7,1)+phone('l4_bbC_swipe.png',390,190,Y-60)+f'<div class="c" style="top:{Y+(800 if st else 760)}px;font:italic 400 32px PF;color:#4a3d58">The Allure + Paradise Island Green · Bird &amp; Bamboo</div>'
    o['3-racks']=f'<div class="c" style="top:{T}px">{step(2,"Add racks","Racks from brands across the table, right on your card.")}</div>'+\
      tilt('l4_mr1C_swipe.png',330,140,Y-20,-7,1)+phone('l4_mr1C_card.png',390,500,Y-60)+f'<div class="c" style="top:{Y+(800 if st else 760)}px;font:italic 400 32px PF;color:#4a3d58">Solara + Peppi Peach Cheetah · Mahjong Register</div>'
    o['4-card']=f'<div class="c" style="top:{T}px">{step(3,"Get your match card","Save it, share it, shop it. Code MAHJMATCH saves at partner brands.")}</div>'+\
      phone('l4_dbriC_card.png',390,345,Y-60)+f'<div class="c" style="top:{Y+(800 if st else 760)}px;font:italic 400 32px PF;color:#4a3d58">Talulah + Reba · Britt Mills</div>'
    o['5-cta']=slides_old(H)['5-cta']
    if st: o['6-link']=slides_old(H)['6-link'].replace('lag_card.png','l4_arC_card.png').replace('cyk_card.png','l4_arC_card.png')
    return o
exec('def slides_old'+open('comp.py').read().split('def slides')[1].split('mode=sys.argv[1]')[0])
mode=sys.argv[1]; H=1350 if mode=='post' else 1920
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1080,'height':H})
    for k,body in slides(H).items():
        open(f'_{mode}.html','w').write(f'<html><head><meta charset=utf8><style>{CSS}body{{width:1080px;height:{H}px}}</style></head><body>{body}</body></html>')
        pg.goto('file://'+D+f'/_{mode}.html'); pg.wait_for_timeout(900); pg.screenshot(path=f'launch-v4-{mode}-{k}.jpg',type='jpeg',quality=92)
    b.close()
