import glob,json,re,pytesseract,sys
from PIL import Image
from multiprocessing import Pool
PAT={'Almond':r'a[il1|]m[o0]n[dce]|lmond|almon','Tudor':r'tud[o0]r','Provincial':r'pr[o0]vinc','Dark Walnut':r'walnu','Red Mahogany':r'mahog','Weathered Oak':r'weather'}
DIRS=['logofix-v2','new-oct18','malachite-new','holiday','holiday-v4','larkspur-v6','codefooter-v1','polofix-v1','papaya-spritz','petalee','peony-and-parasol','brownstone-bloom','from-the-vault','spirit-of-christmas','sunday-tile-set-v3']
fs=[f for d in DIRS for f in sorted(glob.glob(f'assets/cards/{d}/**/*.jpg',recursive=True))]
def w(f):
    im=Image.open(f).convert('L')
    if im.size!=(1080,1350): return f,[]
    c=im.crop((440,60,1080,620)).resize((1280,1120))
    d=pytesseract.image_to_data(c,config='--psm 11',output_type=pytesseract.Output.DICT)
    words=[x.strip() for x in d['text']]
    style='B' if any(x.upper() in ('RACK','MATCHES') for x in words) else 'A'
    hits=[]
    for i,x in enumerate(words):
        for k,p in PAT.items():
            if x and re.search(p,x,re.I):
                hits.append([k,440+d['left'][i]//2,60+d['top'][i]//2,d['width'][i]//2,d['height'][i]//2,style])
    return f,hits
if __name__=='__main__':
    out={}
    with Pool(2) as p:
        for f,h in p.imap(w,fs,chunksize=8):
            if h: out[f]=h
    json.dump(out,open(sys.argv[1],'w'),indent=0)
    from collections import Counter
    print(len(fs),len(out),Counter(f.split('/')[2] for f in out),Counter(h[0] for v in out.values() for h in v))
