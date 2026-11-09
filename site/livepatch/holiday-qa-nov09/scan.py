import sys,json
sys.path.insert(0,'/home/claude/mahjmatchmaker-data/scripts/checks'); sys.path.insert(0,'/home/claude/mahjmatchmaker-data/site/livepatch/holiday-fix-nov09')
import card_sharpness_check as C, card_sharpness as CS, parsefig as P
t=open(sys.argv[1]).read(); S=P.holiday_sections(t); out=[]
for sid,fs in S.items():
  for i,f in enumerate(fs,1):
    try: im=C.load(f['img'])
    except Exception as e: print('ERR',sid,i,e); continue
    if im.size not in ((1080,1350),(750,938)): m={'e1':0,'e2':0,'r':0};b=0;sz=im.size
    else: m=CS.measure(im); b=C.tile_band(im); sz=im.size
    out.append(dict(sid=sid,i=i,h3=f['h3'],img=f['img'],sz=sz,band=round(b,3),**m))
json.dump(out,open(sys.argv[2],'w'),indent=0)
