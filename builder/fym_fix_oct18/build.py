import json,os,re,subprocess
SP='/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/'
B=SP+'fymbuild/'
h=open(SP+'fymaudit/index.html').read(); i=h.index('const D=')+8; j=h.index('\n',i)
D=json.load(open('D_patched.json'))
h=h[:i]+json.dumps(D,separators=(',',':'),ensure_ascii=False)+';'+h[j:]
assert '<script src="b9v1.js"></script>' in h
h=h.replace('<script src="b9v1.js"></script>','<script src="b9v1.js"></script><script src="b11v1.js"></script>',1)
open(B+'index_pre.html','w').write(h)
r=subprocess.run(['python3','patch_js.py',B+'index_pre.html',B+'index.html'],capture_output=True,text=True); print(r.stdout,r.stderr[-2000:])
os.remove(B+'index_pre.html')
img=json.load(open('newIMG.json'))
open(B+'b11v1.js','w').write('window.IMG=Object.assign(window.IMG||{},'+json.dumps(img,separators=(',',':'))+');')
mc=json.load(open('newMC.json')); changed=set()
for f,u in mc.items():
    c=int(f.split('/')[1].split('.')[0])//12; p=B+f'mc/{c}.json'
    o=json.load(open(p)) if os.path.exists(p) else {}
    o[f]=u; json.dump(o,open(p,'w'),separators=(',',':')); changed.add(f'mc/{c}.json')
json.dump(sorted(changed),open('changed_mc.json','w')); print('mc changed',sorted(changed))
