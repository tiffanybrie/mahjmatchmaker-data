"""Oct 18 publish: the FYM version budget is 256MB. Mat chunks as base64 JSON were ~185MB; packing the same
webp bytes as binary (no re-encode, no quality loss) saves the base64 overhead. Format of mc/N.webp (artifacts only serve known types, so the file starts with a real webp):
raw webp bytes concatenated, then JSON header {key:[offset,length]}, then uint32 LE header length. Unreferenced keys dropped, dups shared.
Loader patched in index.html: chunks in MCB load .bin and become Blob URLs; others still load .json.
Usage: python3 pack_bin.py BUILD_DIR"""
import json,os,re,sys,base64,hashlib,struct
B=sys.argv[1]; s=open(B+'/index.html').read()
ref=set(re.findall(r'"f":"(m/\d+\.webp)"',s))
done=[]
for f in sorted(os.listdir(B+'/mc')):
    if not f.endswith('.json'): continue
    d=json.load(open(B+'/mc/'+f)); hdr={}; blob=bytearray(); seen={}
    for k,v in d.items():
        if k not in ref: continue
        b=base64.b64decode(v.split(',',1)[1]); h=hashlib.md5(b).hexdigest()
        if h not in seen: seen[h]=[len(blob),len(b)]; blob+=b
        hdr[k]=seen[h]
    if not hdr: os.remove(B+'/mc/'+f); continue
    hj=json.dumps(hdr,separators=(',',':')).encode()
    open(B+'/mc/'+f[:-5]+'.webp','wb').write(bytes(blob)+hj+struct.pack('<I',len(hj)))
    os.remove(B+'/mc/'+f); done.append(int(f[:-5]))
old="MCP[c]=fetch('mc/'+c+'.json').then(r=>r.json()).then(o=>{"
assert s.count(old)==1
new=("MCP[c]=(MCB.has(c)?fetch('mc/'+c+'.webp').then(r=>{if(!r.ok)throw 0;return r.arrayBuffer()}).then(ab=>{const n=new DataView(ab).getUint32(ab.byteLength-4,true);"
     "const h=JSON.parse(new TextDecoder().decode(new Uint8Array(ab,ab.byteLength-4-n,n)));const o={},u={};for(const k in h){const [a,l]=h[k],kk=a+'_'+l;"
     "o[k]=u[kk]||(u[kk]=URL.createObjectURL(new Blob([new Uint8Array(ab,a,l)],{type:'image/webp'})));}return o;})"
     ":fetch('mc/'+c+'.json').then(r=>r.json())).then(o=>{")
s=s.replace(old,new)
s=s.replace("const MC={},MCP={},MCN=12;","const MC={},MCP={},MCN=12,MCB=new Set(%s);"%json.dumps(sorted(done)),1)
assert 'MCB=new Set(' in s
open(B+'/index.html','w').write(s); print('packed',len(done))
