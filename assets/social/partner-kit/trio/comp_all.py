import subprocess,os,json
from PIL import Image
M=[('omm','omm','oh-my-mahjong','Oh My Mahjong'),('mmj','mmj','miss-mahjong','Miss Mahjong'),('mrc','mrc','mahjong-row-co','Mahjong Row & Co.'),('bb','bb','bird-and-bamboo','Bird & Bamboo'),('ar','ar','anders-ruff','Anders Ruff'),('amj3','amj','amahj','Amahj'),
('bspB','bsp','bespoke-mahjong','Bespoke Mahjong'),('mm','mm','middle-and-main','Middle & Main Mahjong'),('cmc3','cmc3','charleston-mahjong-club','Charleston Mahjong Club'),('mmd5','mmd','mahj-mood','Mahj Mood'),('bam1','bam','bam-lets-mahjong',"Bam! Let's Mahjong"),('hip1','hip','hip-hip-mahjong','Hip Hip Mahjong'),('lmo1','lmo','lets-mahj-on',"Let's Mahj On"),('mac2','mac2','mac-and-miller','Mac + Miller Mahjong'),('lbb1','lbb','lets-be-besties',"Let's Be Besties"),('mv2','mv','mahj-and-vine','Mahj & Vine'),('mr1','mr','mahjong-register','Mahjong Register'),('sad1','sad','soiree-all-day','Soirée All Day'),('wren1','wren','wren-mats','Wren Mats'),('jubm','jub-m','my-fair-mahjong','My Fair Mahjong'),
('dbam','dbam','bam-bird-boutique','Bam Bird Boutique'),('dtdt','dtdt','tigre-de-tartan','Tigre de Tartán'),('dsq','dsq','mahj-squad','Mahj Squad'),('droy','droy','royal-mahjong-society','Royal Mahjong Society'),('dtop','dtop','amanda-toppe','Amanda Toppe'),('dbri','dbri','britt-mills','Britt Mills'),('dvir','dvir','virora-mahjong','Virora Mahjong'),('dymi','dymi','yellow-mountain-imports','Yellow Mountain Imports'),('dfam','dfam','fait-a-main','Fait à Main'),('kal','kal','the-mahjong-co','The Mahjong Co.')]
D='/home/claude/mahjmatchmaker-data/assets/social/partner-kit/final'
man=[]
for o,n,slug,b in M:
    if o!='kal': subprocess.run(['timeout','150','python3','comp.py',o,b],capture_output=True)
    i=Image.open(f'{o}_card.png').convert('RGB');w,h=i.size;i.crop((0,int(h*0.22),w,int(h*0.8))).save(f'review/img/{n}-card.jpg',quality=86)
    if n!='jub-m': Image.open(f'{o}-story.png').convert('RGB').save(f'review/img/{n}-story.jpg',quality=88)
    for k in ('story','post'): Image.open(f'{o}-{k}.png').convert('RGB').save(f'{D}/{slug}-{k}.jpg',quality=88)
    man.append({'slug':slug,'brand':b,'story':f'{slug}-story.jpg','post':f'{slug}-post.jpg','src':o})
json.dump(man,open('/home/claude/mahjmatchmaker-data/site/livepatch/partner-kit-oct27/manifest.json','w'),indent=1,ensure_ascii=False)
print('ok',len(man))
