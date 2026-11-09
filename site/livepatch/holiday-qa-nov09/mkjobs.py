import sys,json,os
sys.path.insert(0,'/home/claude/mahjmatchmaker-data/site/livepatch/holiday-fix-nov09'); sys.path.insert(0,'/home/claude/mahjmatchmaker-data/scripts/checks')
import parsefig as P, card_sharpness_check as C
os.chdir('/home/claude/mahjmatchmaker-data/site/livepatch/holiday-fix-nov09'); import photos as PH
PH.D='/tmp/claude-0/-home-claude/05549d34-8fe3-5ca9-a6a5-308991cb9a78/scratchpad/qa/ph/'
TB={'dear-santa':'Anders Ruff','rackin-rudolph':'Hip Hip Mahjong','holly-jolly-red':"Bam! Let's Mahjong",'holly-jolly-green':"Bam! Let's Mahjong",'holly-jolly-pink':"Bam! Let's Mahjong",'tinselle-emerald':'Virora Mahjong','tinselle-ruby':'Virora Mahjong','nutcracker-ballet':'Mahj Squad','cmc-apres-ski':'Charleston Mahjong Club','december-1994':'Sunday Mahjong'}
S=P.holiday_sections(open('/tmp/claude-0/-home-claude/05549d34-8fe3-5ca9-a6a5-308991cb9a78/scratchpad/qa/live.html').read())
spec=json.load(open(sys.argv[1]))  # [{sid,i,photo?,crop?}]
jobs=[]
for s in spec:
    f=S[s['sid']][s['i']-1]
    j={'sid':s['sid'],'i':s['i'],'img':f['img'],'h3':f['h3'],'brand':f['brand'],'hol':f['hol'],'tile':s['sid'],'tile_file':s.get('tile_file'),
       'tile_brand':TB[s['sid']],'tile_racks':f['tile_racks'],'mat_racks':f['mat_racks'],'file':f['img'].split('/')[-1].split('?')[0],'crop':s.get('crop')}
    if s.get('photo'): j['photo']=s['photo']; j['photo_info']='given'
    else:
        ref=C.load(f['img']).convert('RGB').resize((1080,1350)).crop((20,150,620,560))
        p,info=PH.best(f['shop'],ref); j['photo']=p; j['photo_info']=info
    jobs.append(j); print(s['sid'],s['i'],f['h3'],f['brand'],j['photo_info'] if isinstance(j['photo_info'],str) else (j['photo_info'].get('size') if isinstance(j['photo_info'],dict) else j['photo_info']))
json.dump(jobs,open(sys.argv[2],'w'),indent=1)
