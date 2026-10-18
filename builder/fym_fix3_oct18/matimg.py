import json,os,base64,io
from PIL import Image
FX='/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/fymfix2/'
_c={}
def matimg(f):
    n=int(f.split('/')[1].split('.')[0]); c=n//12
    if c not in _c:
        d={}
        for p in (FX+'site/mc/%d.json'%c, FX+'site2/mc/%d.json'%c, FX+'build/mc/%d.json'%c):
            if os.path.exists(p): d.update(json.load(open(p)))
        _c[c]=d
    u=_c[c].get(f)
    if not u: return None
    return Image.open(io.BytesIO(base64.b64decode(u.split(',',1)[1]))).convert('RGB')
def loadD():
    h=open(FX+'build/index.html').read(); i=h.index('const D=')+8; j=h.index('\n',i)
    return json.loads(h[i:j].rstrip()[:-1])
