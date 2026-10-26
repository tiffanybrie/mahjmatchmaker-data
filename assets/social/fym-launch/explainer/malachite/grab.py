import json,base64,re
from playwright.sync_api import sync_playwright
SET='Miss Classic Malachite'
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':844})
    pg.goto('http://localhost:8766/index.html?tour=off'); pg.wait_for_timeout(4000)
    res=pg.evaluate("""async (SET)=>{const st=D.sets.find(x=>x.name===SET);const out={tile:null,mats:[],racks:{}};
      const ids=st.m.map(x=>x[0]).filter(id=>M[id]&&!M[id].hid);
      for(const id of ids){ const f=M[id].f; for(let k=0;k<60&&!MC[f];k++){loadMC(f);await new Promise(r=>setTimeout(r,150));} out.mats.push({id,n:M[id].n,bn:M[id].bn,src:MC[f]||IMG[M[id].th],racks:(st.m.find(x=>x[0]===id)[1]||[])}); }
      for(const m of out.mats) for(const r of m.racks) if(R[r]) out.racks[r]={n:R[r].n,bn:R[r].bn,src:IMG[R[r].im]};
      out.tilepath=T[st.tile].full;
      const toData=async u=>{if(!u||u.startsWith('data:'))return u;const bl=await (await fetch(u)).blob();return await new Promise(r=>{const fr=new FileReader();fr.onload=()=>r(fr.result);fr.readAsDataURL(bl);});};
      for(const m of out.mats) m.src=await toData(m.src); for(const k in out.racks) out.racks[k].src=await toData(out.racks[k].src);
      return out;}""",SET)
    b.close()
def save(src,fn):
    if not src: return None
    if src.startswith('data:'):
        open(fn,'wb').write(base64.b64decode(src.split(',',1)[1])); return fn
    return None
meta={'tile':res['tilepath'],'mats':[],'racks':{}}
for i,m in enumerate(res['mats']):
    fn=save(m['src'],f'mat{i:02d}.img'); meta['mats'].append({'n':m['n'],'bn':m['bn'],'file':fn,'racks':m['racks'],'src':None if fn else m['src'][:120]})
for k,r in res['racks'].items():
    fn=save(r['src'],'rack_'+re.sub(r'[^a-z0-9]+','-',r['n'].lower())+'.img'); meta['racks'][k]={'n':r['n'],'bn':r['bn'],'file':fn}
json.dump(meta,open('meta.json','w'),indent=1); print(len(meta['mats']),sum(1 for m in meta['mats'] if m['file']),len(meta['racks']))
