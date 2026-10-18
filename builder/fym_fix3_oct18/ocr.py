import json,sys,subprocess,os,re,concurrent.futures as cf
from PIL import Image
P=json.load(open('f3/proc.json'))
PLAY=set('JOKER JOKERS DRAGON DRAGONS CHARLESTON EAST WEST NORTH SOUTH PASS RIGHT LEFT ACROSS SOAP CRAKS CRAK BAMS BAM DOTS FLOWERS FLOWER MAHJONG MAHJ GREEN RED WHITE OPTIONAL COURTESY BLIND STEAL FIRST SECOND THIRD PLAY SINGLES PAIRS MAY NOT USED WINDS'.split())
os.makedirs('f3/ocrtmp',exist_ok=True)
def job(k):
    v=P[k]
    if 'file' not in v or k[0]!='m': return k,None
    im=Image.open(v['file']).convert('L'); im.thumbnail((1000,1000))
    fn='f3/ocrtmp/'+str(abs(hash(k)))+'.png'; im.save(fn)
    out=subprocess.run(['tesseract',fn,'-','--psm','11','tsv'],capture_output=True,text=True).stdout
    os.remove(fn)
    words=[]
    for line in out.splitlines()[1:]:
        p=line.split('\t')
        if len(p)<12: continue
        try: conf=float(p[10])
        except: continue
        w=re.sub(r'[^A-Za-z]','',p[11])
        if conf>=80 and len(w)>=4 and w.upper() not in PLAY: words.append(w)
    return k,words
ks=[k for k in P if k[0]=='m']
with cf.ThreadPoolExecutor(8) as ex: res=dict(ex.map(job,ks))
res={k:v for k,v in res.items() if v and len(v)>=2}
json.dump(res,open('f3/ocr.json','w'),indent=0)
print(len(res))
