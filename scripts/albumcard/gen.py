"""Album match card generator (1080x1350) in Tiffany's album style.
Title band "TILE + MAT", zoomed mat, rack photos stacked left, tile pile bottom-right,
logo strip (rack brand badges + OMM certified + our logo), code footer.
Usage: python3 gen.py spec.json outdir"""
import json,sys,os,base64,io,subprocess
from PIL import Image
spec=json.load(open(sys.argv[1]));out=sys.argv[2];os.makedirs(out,exist_ok=True)
R='/home/claude/mahjmatchmaker-data/'
P=json.load(open('/tmp/mb/data_embed.json'))['prods']
byname={v['n']:k for k,v in P.items() if v.get('k')=='rack'}
logos=json.load(open(R+'builder/logos/map.json'))
def uri(path_or_img,fmt='JPEG',q=88,maxs=None):
    im=Image.open(path_or_img) if isinstance(path_or_img,str) else path_or_img
    if maxs: im=im.copy();im.thumbnail((maxs,maxs))
    b=io.BytesIO()
    if fmt=='PNG': im.save(b,'PNG')
    else: im.convert('RGB').save(b,'JPEG',quality=q)
    return f'data:image/{fmt.lower()};base64,'+base64.b64encode(b.getvalue()).decode()
mat=Image.open(R+spec['mat_file']).convert('RGB').crop(tuple(spec['mat_crop']))
MAT=uri(mat,maxs=1300)
STRIP=uri(R+'assets/brand/card_strip_omm_mm.png','PNG')
fonts='/tmp/cc/f/'
html_tpl=open(os.path.join(os.path.dirname(__file__),'card.html')).read()
cards=[]
for c in spec['cards']:
    racks=[]
    for rn in c['racks']:
        k=byname.get(rn)
        if not k: print('NO RACK',rn);continue
        p=P[k];racks.append({'n':rn,'img':p['cut'] if p.get('clean') else p['photo'],'brand':p.get('bn') or rn.split(' ')[0]})
    rb=[]
    for r in racks:
        b=next((bn for bn in logos if r['n'].startswith(bn)),None)
        if b and b not in rb: rb.append(b)
    badges=[uri(R+'builder/logos/'+logos[b],'PNG') for b in rb]
    tile=uri(R+c['tile_file'],maxs=700)
    h=html_tpl.replace('__DATA__',json.dumps({'title':c['title'],'col':c['col'],'mat':MAT,'tile':tile,'racks':racks,'badges':badges,'strip':STRIP,'tilefit':c.get('tilefit','cover'),'code':spec.get('code','10% OFF  USE CODE: MAHJMATCH')}))
    f=f'/tmp/lark/cards/{c["slug"]}.html';open(f,'w').write(h);cards.append((f,os.path.join(out,c['file'])))
js=os.path.join(os.path.dirname(__file__),'shot.js')
subprocess.run(['node',js]+[x for p in cards for x in p],check=True,env={**os.environ,'NODE_PATH':subprocess.run(['npm','root','-g'],capture_output=True,text=True).stdout.strip()})
