"""v4 (Nov 3): render cross-brand Find Your Mat-ch match cards with the app's own card renderer (renderCard/drawCard, Post 4:5)
for the reel's match-card wall. Tiffany 1:58pm + 2:11pm: Anders Ruff heavy, Malachite on a holiday mat, Heritage on The Polo Club,
Rackin' Rudolph on Candy Cane Lane, Amara (OMM) on Very Merry Wreath (Mahjong Register); racks = max ONE painted colour + wood/pearl/acrylic,
never orange. Output /dev/shm/introv4/xcards/NN.png"""
import sys, os, json, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v2_lib import *
O = '/dev/shm/introv4/xcards'; os.makedirs(O, exist_ok=True)
COMBOS = [  # (tile set name, mat name, mat brand, [rack names])
    ('Amara', 'Very Merry Wreath Premium', 'Mahjong Register', ['Mahjong Register Peony Blush Pearl Scalloped', 'Clear Acrylic Rack & Pushers Set']),
    ('Dear Santa', "Santa's Mahjong Mail", 'Anders Ruff', ['Anders Ruff Jade', 'Peace Love Mahjong Oak']),
    ('Miss Classic Malachite', 'Tartan Tidings', 'Anders Ruff', ['Miss Mahjong Jade & Brass', 'Bam Bird Boutique Walnut']),
    ('Heritage 1.0', 'The Polo Club', 'Luxe Mahjong', ['Miss Mahjong Blonde Tortoise', 'Yellow Mountain Classic Chestnut Wood']),
    ("Rackin' Rudolph", 'Candy Cane Lane', 'Anders Ruff', ['Peace Love Mahjong Red', 'Milk Glass Collection Mahjong Rack and Pusher, Set of 4']),
    ('Holly Jolly (Sugarplum Pink)', 'Color Me Merry', 'Soirée All Day', ['My Fair Mahjong Pearl Blush', 'Mahjong Register Ivory Oyster Pearl Scalloped']),
    ('Tinselle (Emerald Green)', 'Plaid Tidings', 'My Fair Mahjong', ['Mahjong Register Emerald Pearl Scalloped', 'Middle & Main Scalloped Beechwood']),
    ('Nutcracker Ballet', 'Very Merry Mahj', 'Anders Ruff', ['La Vie En Rose Mahjong Rack and Pusher, Set of 4', 'Peace Love Mahjong Oak']),
]
with sync_playwright() as p:
    b, ctx, pg = start(p, 1)
    for i, (sn, mn, mb, rn) in enumerate(COMBOS):
        r = pg.evaluate("""async([sn,mn,mb,rn])=>{const si=D.sets.findIndex(s=>s.name===sn);const mk=Object.keys(M).find(k=>M[k].n===mn&&M[k].bn===mb&&!M[k].hid);
          const rk=rn.map(n=>Object.keys(R).find(k=>R[k].n===n||R[k].n.startsWith(n)));if(si<0||!mk||rk.some(x=>!x))return ['missing',si,mk,rk];
          S.set=si;S.fav=mk;S.rpick=rk;S.made=true;S.fmt='post';try{renderCard()}catch(e){return ['err',String(e)]}
          for(let t=0;t<120;t++){await new Promise(r=>setTimeout(r,250));const im=document.querySelector('#prev img');if(im&&im.complete&&im.naturalHeight>1000)return ['ok',im.src.slice(0,30),im.naturalWidth,im.naturalHeight];}
          return ['timeout']}""", [sn, mn, mb, rn])
        print(i, sn, mn, r[:4] if isinstance(r, list) else r)
        if r[0] != 'ok': continue
        src = pg.evaluate("()=>document.querySelector('#prev img').src")
        if src.startswith('blob:'):
            d = pg.evaluate("async(u)=>{const ab=new Uint8Array(await (await fetch(u)).arrayBuffer());let s='';for(let i=0;i<ab.length;i+=32768)s+=String.fromCharCode.apply(null,ab.subarray(i,i+32768));return btoa(s)}", src)
        else: d = src.split(',', 1)[1]
        open(f'{O}/{i:02d}.png', 'wb').write(base64.b64decode(d))
    b.close()
