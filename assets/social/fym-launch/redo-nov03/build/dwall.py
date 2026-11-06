"""Depth-wall mats (19.20-20.68s, right after 'Find Your Mat-ch is HERE'): 48 everyday partner mats from the live v113 catalog
(visible, not holiday, not retired, code partner: no Tigre de Tartan / Sunday / Mahjong Studios / Paige Spearin; square photos; max 3 per brand).
Photos are pulled from the app's own full-size bundles (MC) in headless Chromium -> /dev/shm/lr/dwall/NN.jpg + sel.json"""
import json, random, collections, subprocess, os, sys, base64
sys.path.insert(0, '/home/claude/mahjmatchmaker-data/assets/social/holiday-nov1/intro/build')
from v2_lib import *
D = json.load(open('/dev/shm/introv2/D.json')); M = D['mats']; O = '/dev/shm/lr/dwall'; os.makedirs(O, exist_ok=True)
BAD = ('tigre', 'sunday', 'studios', 'paige', 'mahjong line', 'four winds', 'mahjong row', 'yellow mountain', 'mahjong by si', 'mahjong co')  # Nov 6: Mahjong Row out; YMI never on social; Mahjong Co. mats hidden
c = [(k, v) for k, v in M.items() if v.get('pa') and not v.get('hol') and not v.get('hid') and not v.get('rt') and not v.get('nc') and not v.get('ml')
     and not any(b in (v['bn'] + v['n']).lower() for b in BAD) and 0.9 <= v['w'] / v['h'] <= 1.1 and v['w'] >= 900]
random.seed(27); random.shuffle(c)
with sync_playwright() as p:
    b, ctx, pg = start(p, 1)
    sel = []; n = collections.Counter()
    for k, v in c:
        if n[v['bn']] >= 3: continue
        d = pg.evaluate("async(f)=>{try{await loadMC(f)}catch(e){};const u=MC[f];if(!u)return '';const ab=new Uint8Array(await (await fetch(u)).arrayBuffer());let s='';for(let i=0;i<ab.length;i+=32768)s+=String.fromCharCode.apply(null,ab.subarray(i,i+32768));return btoa(s)}", v['f'])
        if not d: continue
        i = len(sel); out = f'{O}/{i:02d}.jpg'; open(out + '.webp', 'wb').write(base64.b64decode(d))
        subprocess.run(['convert', out + '.webp[0]', '-resize', '360x360^', '-gravity', 'center', '-extent', '360x360', '-quality', '90', out]); os.remove(out + '.webp')
        if os.path.exists(out): sel.append([i, v['n'], v['bn'], k]); n[v['bn']] += 1
        if len(sel) == 48: break
    b.close()
json.dump(sel, open(f'{O}/sel.json', 'w'), indent=1); print(len(sel), 'mats', len(n), 'brands')
