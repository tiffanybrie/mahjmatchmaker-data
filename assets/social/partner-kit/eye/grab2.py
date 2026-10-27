from playwright.sync_api import sync_playwright
import base64,json,sys
with sync_playwright() as p:
  b=p.chromium.launch(); pg=b.new_page(); pg.goto('http://localhost:8766/index.html?tour=off'); pg.wait_for_timeout(5000)
  for dom,tag in [('letsbebesties','lbb'),('mahjongregister','mr'),('soireeallday','sad'),('mahjandvine','mv'),('faitamain','fam')]:
    lst=pg.evaluate("(b)=>{const her=new Set();D.sets.forEach(s=>s.m.forEach(x=>her.add(x[0])));return Object.entries(M).filter(([k,m])=>k.replace(/-/g,'').toLowerCase().includes(b)&&!m.hid&&!m.rt).map(([k,m])=>[k,m.n,her.has(k),m.hol||false,(m.fam||m.c||[])])}",dom)
    print(dom,len(lst)); out=[]
    for i,(k,n,her,hol,fam) in enumerate(lst):
      u=pg.evaluate("async(k)=>{let u=await matFull(k);if(u&&u.startsWith('blob:')){const bl=await (await fetch(u)).blob();u=await new Promise(r=>{const fr=new FileReader();fr.onload=()=>r(fr.result);fr.readAsDataURL(bl)})}return u}",k)
      if u and u.startswith('data:'):
        h,d=u.split(',',1); ext='webp' if 'webp' in h else ('png' if 'png' in h else 'jpg')
        fn=f'{tag}_{i:02d}.{ext}'; open(fn,'wb').write(base64.b64decode(d)); out.append([fn,k,n,her,hol])
      elif u:
        out.append([u,k,n,her,hol])
    json.dump(out,open(f'{tag}.json','w'),indent=0,ensure_ascii=False)
  b.close()
