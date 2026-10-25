"""FYM v85 BUG FIX (Tiffany Oct 25 14:39, husband on the website: "Couldn't draw the card here", Terracotta Marble + The Country House).
Cause: on the website copy the app runs inside the mahjmatchmaker.com page and its photos come from cdn.jsdelivr.net. The card
loader (lk) loaded them WITHOUT crossOrigin, so one cross-origin photo (here the Terracotta Marble tile photo, which has no HD card
photo, so the plain t71 file was used) tainted the canvas and toDataURL threw. The artifact never showed it (same origin).
Fix: lk() loads every image that is not data:/blob: (relative paths resolve to jsDelivr on the website) with crossOrigin='anonymous' (jsDelivr sends Access-Control-Allow-Origin: *); if that fails (e.g. a
cached non-CORS copy in Safari) it retries once with a cache-busting query. Gate [43] checks this stays in place.
Usage: python3 v85_cardcors.py <build_dir>  (in place)"""
import sys
P = sys.argv[1] + '/index.html'; h = open(P).read()
a = "const lk=src=>new Promise(r=>{if(!src)return r(null);const i=new Image();i.onload=()=>r(i);i.onerror=()=>r(null);i.src=src;});"
assert h.count(a) == 1
b = ("const lk=src=>new Promise(r=>{if(!src)return r(null);const web=!/^(data|blob):/i.test(src);const go=(u,again)=>{const i=new Image();"
     "if(web)i.crossOrigin='anonymous';i.onload=()=>r(i);i.onerror=()=>{if(web&&!again)go(u+(u.includes('?')?'&':'?')+'cors=1',true);else r(null);};i.src=u;};go(src,false);});")
h = h.replace(a, b)
open(P, 'w').write(h); print('ok')
