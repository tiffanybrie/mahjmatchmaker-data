import json,glob,base64,io
from PIL import Image
SP='/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/'
IMG={}
for f in sorted(glob.glob(SP+'fymaudit/b*.js')+glob.glob(SP+'fympub/b*.js')):
    s=open(f).read(); i=s.index(',{')+1; j=s.rindex('}'); IMG.update(json.loads(s[i:j+1]))
def dec(uri): return Image.open(io.BytesIO(base64.b64decode(uri.split(',',1)[1])))
MC={}
for f in glob.glob(SP+'fymaudit/mc/*.json')+glob.glob(SP+'fympub/mc/*.json'): MC.update(json.load(open(f)))
