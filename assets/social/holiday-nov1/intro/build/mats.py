import sys,json,base64; sys.path.insert(0,'/tmp/claude-0/-home-claude/f4da3022-6ec8-595a-90aa-668aea191899/scratchpad')
from fymlib import *
st=json.load(open('/dev/shm/holiday-intro/stock.json'))
ids=[k for k,v in st.items() if v['avail']]
with sync_playwright() as p:
    b,ctx,pg=start(p,1)
    out={}
    for k in ids:
        r=pg.evaluate("""async(id)=>{try{const f=M[id].f;await loadMC(f);const u=MC[f]||IMG[M[id].th];const bl=await (await fetch(u)).blob();const ab=new Uint8Array(await bl.arrayBuffer());let s='';for(let i=0;i<ab.length;i+=32768)s+=String.fromCharCode.apply(null,ab.subarray(i,i+32768));return [bl.type,btoa(s)]}catch(e){return ['err',String(e)]}}""",k)
        if r[0]=='err': print('ERR',st[k]['n'],r[1]); continue
        ext={'image/webp':'webp','image/jpeg':'jpg','image/png':'png'}.get(r[0],'bin')
        fn=f"/dev/shm/holiday-intro/mats/{st[k]['f'].split('/')[1].split('.')[0]}.{ext}"
        open(fn,'wb').write(base64.b64decode(r[1])); out[k]=fn
    json.dump(out,open('/dev/shm/holiday-intro/mats/map.json','w'),indent=1); print(len(out))
    b.close()
