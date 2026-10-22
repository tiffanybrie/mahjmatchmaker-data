import json,re
R='/home/claude/mahjmatchmaker-data/'; S=R+'assets/reels/s2/'
def ep(slug, live):
    c=open(S+slug+'-caption.txt').read().strip()
    c=c.replace('Coming 10.27: Find Your Match at mahjmatchmaker.com.', 'Find Your Mat-ch™ is live at mahjmatchmaker.com.' if live else 'Coming 10.27: Find Your Mat-ch™ at mahjmatchmaker.com.')
    c=c.replace('Find Your Match','Find Your Mat-ch')
    return c
def box(title,when,tags,extra=''):
    return (f"👀 REVIEW: {title}, {when} — reply yes/changes to Claude\n🛑 TIFFANY: DELETE THIS BOX BEFORE YOU POST 🛑\n"
            f"1) Song: the video is silent. Add one of your love-song picks in Instagram (never library music).\n"
            f"2) Tag people: {' '.join('@'+t for t in tags)}\n{extra}"
            f"3) Delete this box, then share.\n————————————\n")
P=[]
def reel(key,slug,date,live,title,when,tags,cover=None,extra=''):
    P.append(dict(key=key,date=date,type='reel',video=f'assets/reels/s2/{slug}.mp4',cover=cover,caption=box(title,when,tags,extra)+ep(slug,live)))
reel('heritage','ep05-heritage-s2','2026-10-23T16:00:00Z',False,'Ep 5 Heritage "The Ex Is Back" reel (fall, cuffing season; Heritage 2.0 in stock)','Fri 10/23 11am CT',['ohmymahjong'])
reel('brownstone','ep11-brownstone-s2','2026-10-24T16:00:00Z',False,'Ep 11 Brownstone Bloom "Love at First Tile" reel (fall). NOTE: needs the Brownstone album live first (your tap in Ready to Ship)','Sat 10/24 11am CT',['andersruffdesignco','mahjongrowandco'])
reel('cypress','ep12-cypress-s2','2026-10-26T16:00:00Z',False,'Ep 12 Cypress Forest "Will You Accept This Rack?" reel (fall greens)','Mon 10/26 11am CT',['mahjongrowandco'])
reel('pippa','ep06-pippa-s2-v2','2026-10-27T14:30:00Z',True,'LAUNCH DAY Pippa reel (v2)','Tue 10/27 9:30am CT',['ohmymahjong','middleandmainmahjong'],cover='assets/reels/s2/ep06-pippa-s2-v2-cover.jpg')
reel('osler','ep09-osler-s2','2026-10-29T16:00:00Z',True,'Ep 9 Osler "Speed Dating" reel','Thu 10/29 11am CT',['ohmymahjong'])
reel('smith','ep08-smith-s2-v2','2026-10-30T16:00:00Z',True,'Ep 8 Smith reel (v2, "three for three")','Fri 10/30 11am CT',['ohmymahjong','bambirdboutique','mahjongmoxie'],cover='assets/reels/s2/ep08-smith-s2-v2-cover.jpg')
reel('willow','ep04-willow-s2','2026-11-01T17:00:00Z',True,'Ep 4 Willow "Blind Date" reel','Sun 11/1 11am CT',['ohmymahjong'])
reel('seabreeze','ep07-seabreeze-s2','2026-11-02T17:00:00Z',True,'Ep 7 Seabreeze "The Final Five" reel','Mon 11/2 11am CT',['ohmymahjong'])
reel('malachite','ep01-malachite-s2','2026-11-03T17:00:00Z',True,'Ep 1 Malachite "Cupid\'s Arrow" reel. Date moves to Miss Mahjong\'s real drop day (week of Nov 3)','Tue 11/3 11am CT (placeholder)',['missmahjongofficial','amandatoppeliving','brittmillsdesign'])
reel('jade','ep02-jade-s2','2026-11-05T17:00:00Z',True,'Ep 2 Jade "Missed Connections" reel. Follows the Miss Classic drop','Thu 11/5 11am CT (placeholder)',['missmahjongofficial','amandatoppeliving','tigre_de_tartan'])
reel('talulah','ep10-talulah-s2','2026-11-08T17:00:00Z',True,'Ep 10 Talulah "The Photo Dump" reel','Sun 11/8 11am CT',['ohmymahjong','viroramahjongofficial'])
reel('solara','ep03-solara-s2','2026-11-10T17:00:00Z',True,'Ep 3 Solara "The Little Black Book" reel','Tue 11/10 11am CT',['ohmymahjong','wrenmats'])
reel('coquette','ep13-coquette-s2-v2',None,True,'Ep 13 Coquette finale reel (v2). HELD: Coquette is sold out; dated when LoveShackFancy restocks','undated',['loveshackfancy','ohmymahjong','middleandmainmahjong'])
reel('trailer','ep00-trailer-s2-v4',None,True,'Season 2 trailer (v4 video, v5 caption). Held per the plan; your call whether it runs','undated',['ohmymahjong','loveshackfancy'],cover='assets/reels/s2/ep00-trailer-s2-v4-cover.jpg')
P[-1]['caption']=P[-1]['caption'].split('————————————\n')[0]+'————————————\n'+open(S+'ep00-trailer-s2-v5-caption.txt').read().strip()
def ht(name):
    t=open(R+f'assets/social/holiday-tables/{name}/caption.txt').read()
    notes,cap=t.split('=== CAPTION ===')
    return notes.replace('=== NOTES FOR TIFFANY (not part of the caption) ===','').strip(),cap.strip()
for name,date,when,title in [('polo','2026-11-04T17:00:00Z','Wed 11/4 11am CT','Polo Club holiday table reel'),('rudolph','2026-11-06T17:00:00Z','Fri 11/6 11am CT',"Rackin' Rudolph holiday table reel"),('rattan',None,'undated',"Retro Rattan holiday table reel. HELD until Sunday Mahjong relists the Rattan mat")]:
    n,c=ht(name)
    P.append(dict(key=name,date=date,type='reel',video=f'assets/social/holiday-tables/{name}/{name}-holiday-table-reel.mp4',caption=f"👀 REVIEW: {title}, {when} — reply yes/changes to Claude\n🛑 TIFFANY: DELETE THIS BOX BEFORE YOU POST 🛑\n{n}\nDelete this box, then share.\n————————————\n{c}"))
    P.append(dict(key=name+'-story',date=(date[:11]+'17:30:00Z') if date else None,type='story',auto=False,images=[f'assets/social/holiday-tables/{name}/{name}-story-0{i}.jpg' for i in range(1,8)],caption=f"👀 REVIEW: {title.replace(' reel','')} 7-frame story (goes up with the reel), {when} — reply yes/changes to Claude\n🛑 TIFFANY: DELETE THIS BOX BEFORE YOU POST 🛑\nPost frames 1 → 7 as one story. Frame 1: @mention the main brand. Frame 7: LINK sticker to the blog post in the clear space under \"tap the link\". Frame 5 (Polo only): poll sticker. Delete this box, then share."))
raven="""Night of the Raven 🖤🦇 A Halloween mahjong table that doesn't scream Halloween.

@mahjongrowandco's Mocha Bloom Dark mat (inky black, dusty-rose blooms), Terracotta Marble tiles with veined backs that look like spiderwebs once the wall goes up, translucent plum racks and black plum shufflers. Black lace over a deep plum cloth, a raven tealight for the dice.

Shop the whole look on the blog (link in bio).
Code MAHJMATCH at Mahjong Row & Co. 💕

#mahjong #halloweenmahjong #mahjongtable #mahjmatch #affiliate"""
P.append(dict(key='raven',date='2026-10-28T16:00:00Z',type='feed',auto=True,images=['assets/blog/night-of-the-raven/night-of-the-raven-halloween-mahjong-table.jpg','assets/blog/night-of-the-raven/night-of-the-raven-shop-the-look-v7.jpg'],tags=['mahjongrowandco'],caption="👀 REVIEW: Halloween \"Night of the Raven\" carousel (table + shop the look), auto Wed 10/28 11am CT — reply yes/changes to Claude. Claude deletes this line on your yes.\n\n"+raven))
P.append(dict(key='raven-story',date='2026-10-31T15:00:00Z',type='story',auto=True,images=['assets/blog/night-of-the-raven/night-of-the-raven-halloween-mahjong-table.jpg','assets/blog/night-of-the-raven/night-of-the-raven-shop-the-look-v7.jpg'],caption="👀 REVIEW: Happy Halloween story: the Night of the Raven table, 2 plain frames, auto Sat 10/31 10am CT — reply yes/changes to Claude"))
hc=json.load(open(R+'assets/social/its-a-match/captions.json'))
P.append(dict(key='papaya-heiress',date='2026-10-25T16:00:00Z',type='feed',auto=True,images=[f'assets/social/its-a-match/papaya-heiress/slide{i}.jpg' for i in (1,2,3)],tags=['ohmymahjong','brittmillsdesign'],caption="👀 REVIEW: \"It's a mat-ch!\" Papaya Spritz × Heiress carousel (3 slides), auto Sun 10/25 11am CT — reply yes/changes to Claude. Claude deletes this line on your yes.\n\n"+next((v for k,v in hc.items() if 'papaya' in k.lower()),"It's a mat-ch! 💗 Papaya Spritz by @ohmymahjong + Heiress by @brittmillsdesign. Use code MAHJMATCH 💕\n#mahjong #mahjongtiles #mahjmatch #affiliate")))
json.dump(P,open('/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/planoly/posts.json','w'),indent=1,ensure_ascii=False)
for p in P: print(p['key'],p['date'],p['type'],len(p['caption']))
