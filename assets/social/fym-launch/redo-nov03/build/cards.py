"""Launch reel redo (Nov 3): 15 everyday cross-brand Find Your Mat-ch match cards from Tiffany's real picks (D.sets[].m with her
rack picks; max ONE painted rack + wood/pearl/acrylic/tortoise; no holiday, retired, hidden, orange; mat brand != tile brand),
rendered by the app's own card renderer (Post 4:5). Picks list: build/cards_pick.json (copied to /dev/shm/lr by prep.py). Out: /dev/shm/lr/xcards/NN.png"""
import sys, os, json, base64
sys.path.insert(0, '/home/claude/mahjmatchmaker-data/assets/social/holiday-nov1/intro/build')
from v2_lib import *
O = '/dev/shm/lr/xcards'; os.makedirs(O, exist_ok=True)
P = json.load(open('/dev/shm/lr/cards_pick.json'))
with sync_playwright() as p:
    b, ctx, pg = start(p, 1)
    for i, (si, sn, smk, mk, mn, mb, rk) in enumerate(P):
        r = pg.evaluate("""async([si,mk,rk])=>{S.set=si;S.fav=mk;S.rpick=rk;S.made=true;S.fmt='post';try{renderCard()}catch(e){return ['err',String(e)]}
          for(let t=0;t<120;t++){await new Promise(r=>setTimeout(r,250));const im=document.querySelector('#prev img');if(im&&im.complete&&im.naturalHeight>1000)return ['ok'];}return ['timeout']}""", [si, mk, rk])
        print(i, sn, mn, r)
        if r[0] != 'ok': continue
        src = pg.evaluate("()=>document.querySelector('#prev img').src")
        if src.startswith('blob:'):
            d = pg.evaluate("async(u)=>{const ab=new Uint8Array(await (await fetch(u)).arrayBuffer());let s='';for(let i=0;i<ab.length;i+=32768)s+=String.fromCharCode.apply(null,ab.subarray(i,i+32768));return btoa(s)}", src)
        else: d = src.split(',', 1)[1]
        open(f'{O}/{i:02d}.png', 'wb').write(base64.b64decode(d))
    b.close()
