import sys,os,json
sys.path.insert(0,'/home/claude/mahjmatchmaker-data/scripts/matcard')
import matcard as M
F=M.F
head=f"""<!doctype html><html><head><meta charset=utf8><style>
{M.font('Alfa','fontsource-alfa-slab-one-5.3.0/package/files/alfa-slab-one-latin-400-normal.woff2')}
{M.font('PlayI','fontsource-playfair-display-5.3.0/package/files/playfair-display-latin-400-italic.woff2')}
@font-face{{font-family:'BitterB';src:url(file://{F}fontsource-bitter-5.3.0/package/files/bitter-latin-700-normal.woff2)}}
@font-face{{font-family:'Bitter';src:url(file://{F}fontsource-bitter-5.3.0/package/files/bitter-latin-400-normal.woff2)}}
*{{margin:0}}body{{width:1080px;height:1920px;background:transparent;position:relative}}
.eb{{position:absolute;left:0;right:0;font-family:BitterB;letter-spacing:.26em;font-size:34px;color:#054689;text-align:center}}
h1{{position:absolute;left:0;right:0;font-family:Alfa;color:#d9405d;text-shadow:5px 5px 0 #fff;text-align:center;text-transform:uppercase;line-height:1}}
.lab{{position:absolute;left:0;right:0;text-align:center;font-family:BitterB;font-size:60px;color:#2a2036}}.lab small{{display:block;font-family:Bitter;font-size:34px;color:#6b5a77}}
.tag{{display:inline-block;background:#6b5a77;color:#fff;font-family:BitterB;font-size:28px;letter-spacing:.18em;padding:6px 16px;border-radius:8px;margin-top:8px}}
</style></head><body>"""
o={}
o['title']=head+"<div class=eb style='top:205px'>NEW FROM OH MY MAHJONG</div><h1 style='top:255px;font-size:128px'>LARKSPUR</h1><div class=eb style='top:1560px;font-size:40px;letter-spacing:.06em'>What tiles go with it?</div></body></html>"
o['matches']=head+"<div class=eb style='top:205px'>TIFFANY'S TILE MATCHES</div><h1 style='top:255px;font-size:104px'>LARKSPUR +</h1></body></html>"
for n,ret in [('Moonlight',0),('Limoncello',1),('La Fete',0),('Luminaire',0),('Palm Royale',0),('Spring Love',1)]:
    o['lab-'+n]=head+f"<div class=lab style='top:1440px'>{n}<small>Oh My Mahjong tiles</small>{'<span class=tag>RETIRED</span>' if ret else ''}</div></body></html>"
for k,h in o.items(): open(f'ov-{k}.html','w').write(h)
