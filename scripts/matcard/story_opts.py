"""IG story layout options for Mat Edit cards (Tiffany, Oct 13: racks on stories, bigger tiles). Safe zones: no text in top 200px / bottom 220px."""
import json,sys,os
sys.path.insert(0,os.path.dirname(__file__))
import matcard as M
c=json.load(open(sys.argv[1])); out=sys.argv[2]; variant=sys.argv[3] if len(sys.argv)>3 else 'all'
mat=M.b64(c['mat_path'],'JPEG',1100); logo=M.b64(M.ROOT+'/assets/brand/mahjmatchmaker-wordmark.png',size=700); flame=M.b64(M.ROOT+'/assets/brand/flame-heart.png',size=120)
tiles=c['tiles_omm'] if variant=='omm' else c['tiles_all']
rt=set(c.get('retired',[]))
def tl(sz):
    return ''.join(f"<figure><div class=tp style=\"width:{sz}px;height:{sz}px;background-image:url({M.TILE[t]['img']})\"></div><figcaption>{t.replace(' (retired)','')}{'<small>retired</small>' if (t in rt or '(retired)' in t) else ''}</figcaption></figure>" for t in tiles)
def racks(h=64,img_h=96):
    o=''
    for r in c['racks']:
        star='★ ' if (len(r)>4 and r[4]) else ''
        if len(r)>3 and r[3]:
            o+=f"<div class=rkp><div class=rki style=\"height:{img_h}px;background-image:url({M.b64(M.ROOT+'/'+r[3],'JPEG',700)})\"></div><span>{star}{r[0]}</span></div>"
        else:
            o+=f"<div class=rk style='height:{h}px;background:{r[1]};color:{'#fff' if r[2] else '#2a2036'}'><span>{star}{r[0]}</span><em>Bird &amp; Bamboo</em></div>"
    return o
pal=lambda: ''.join(f"<div class=sw><i style='background:{h}'></i><span>{n}</span></div>" for n,h in c['palette'])
F=M.F
base=f"""<!doctype html><html><head><meta charset=utf8><style>
{M.font('Alfa','fontsource-alfa-slab-one-5.3.0/package/files/alfa-slab-one-latin-400-normal.woff2')}
{M.font('PlayI','fontsource-playfair-display-5.3.0/package/files/playfair-display-latin-400-italic.woff2')}
{M.font('Bitter','fontsource-bitter-5.3.0/package/files/bitter-latin-400-normal.woff2')}
@font-face{{font-family:'BitterB';src:url(file://{F}fontsource-bitter-5.3.0/package/files/bitter-latin-700-normal.woff2)}}
*{{box-sizing:border-box;margin:0}}body{{width:1080px;height:1920px;background:#f6e9df;font-family:Bitter;color:#2a2036;overflow:hidden;position:relative}}
.wrap{{position:absolute;left:0;right:0;top:200px;bottom:220px;padding:0 48px;display:flex;flex-direction:column;align-items:center;justify-content:space-between}}
.hd{{display:flex;flex-direction:column;align-items:center}}.logo{{height:52px}}
.eb{{font-family:BitterB;letter-spacing:.32em;font-size:22px;color:#054689;margin-top:14px;display:flex;align-items:center;gap:12px}}.eb img{{height:28px}}
h1{{font-family:Alfa;font-size:118px;line-height:1;color:{c['color']};text-shadow:4px 4px 0 #fff;margin-top:6px;text-transform:uppercase}}
.by{{font-family:PlayI;font-size:36px;margin-top:4px}}
.mat{{border-radius:22px;background:url({mat}) center/cover;box-shadow:0 10px 30px rgba(42,32,54,.18);flex:none}}
.h{{font-family:BitterB;letter-spacing:.3em;font-size:20px;color:#054689;text-align:center;display:flex;align-items:center;justify-content:center;gap:10px;margin-bottom:10px}}.h img{{height:26px}}
.tiles .g{{display:grid;grid-template-columns:repeat(3,auto);gap:12px 22px;justify-content:center}}
figure{{text-align:center}}.tp{{border-radius:18px;background:center/cover;box-shadow:0 6px 16px rgba(42,32,54,.18)}}
figcaption{{font-family:BitterB;font-size:22px;margin-top:6px;line-height:1.1}}figcaption small{{display:block;font-family:Bitter;font-size:16px;color:#6b5a77}}
.rk{{border-radius:8px;padding:0 14px;display:flex;align-items:center;justify-content:space-between;font-family:BitterB;font-size:20px;box-shadow:inset 0 -5px 0 rgba(0,0,0,.12)}}.rk em{{font-style:normal;font-family:Bitter;font-size:14px;opacity:.75}}
.rkp{{display:flex;flex-direction:column;gap:4px}}.rki{{border-radius:8px;background:center/cover}}.rkp span{{font-family:BitterB;font-size:18px;text-align:center}}
.sw{{display:flex;align-items:center;gap:10px;font-family:BitterB;font-size:17px;letter-spacing:.06em;text-transform:uppercase}}.sw i{{width:40px;height:40px;border-radius:50%;flex:none;box-shadow:0 2px 6px rgba(0,0,0,.15)}}
.box{{background:#fff8f2;border-radius:18px;padding:14px 16px}}
.ft{{display:flex;flex-direction:column;align-items:center;gap:10px}}.web{{font-family:BitterB;font-size:30px;color:#054689;display:flex;align-items:center;gap:10px}}.web img{{height:32px}}
.cp{{background:#054689;color:#fff;font-family:BitterB;font-size:27px;padding:12px 32px;border-radius:40px}}
"""
hd=f"<div class=hd><img class=logo src='{logo}'><div class=eb><img src='{flame}'>THE MAT EDIT<img src='{flame}'></div><h1>{c['name']}</h1><div class=by>by {c['brand']}</div></div>"
ft=f"<div class=ft><div class=web><img src='{flame}'>www.mahjmatchmaker.com</div><div class=cp>First date's on us. Use code MAHJMATCH to save 10%.</div></div>"
tt="TIFFANY'S OMM TILE MATCHES" if variant=='omm' else "TIFFANY'S TILE MATCHES"
th=lambda t:f"<div class=h><img src='{flame}'>{t}<img src='{flame}'></div>"
# A: mat left + palette/racks right, big 3x2 tiles
A=base+f""".row{{display:flex;gap:24px;align-items:stretch;width:100%}}.col{{flex:1;display:flex;flex-direction:column;gap:10px}}.pal{{display:grid;grid-template-columns:1fr 1fr;gap:8px}}.rks{{display:flex;flex-direction:column;gap:8px}}</style></head><body><div class=wrap>{hd}
<div class=row><div class=mat style='width:500px;height:500px'></div><div class=col><div class='box pal'>{pal()}</div><div class='box rks'>{racks(46,74)}</div></div></div>
<div class=tiles>{th(tt)}<div class=g>{tl(222)}</div></div>{ft}</div></body></html>"""
# B: centered mat, palette dots strip, racks 2x2, tiles 3x2
B=base+f""".pal{{display:flex;gap:18px;justify-content:center;flex-wrap:wrap}}.pal .sw span{{display:none}}.pal .sw i{{width:54px;height:54px}}.rks{{display:grid;grid-template-columns:1fr 1fr;gap:10px;width:100%}}.rkp{{grid-row:span 2}}</style></head><body><div class=wrap>{hd}
<div class=mat style='width:440px;height:440px'></div><div class=pal>{pal()}</div>
<div class='box' style='width:100%'>{th('RACK MATCHES')}<div class=rks>{racks(44,100)}</div></div>
<div class=tiles>{th(tt)}<div class=g>{tl(178)}</div></div>{ft}</div></body></html>"""
# C: tiles first (bigger), mat + racks side by side below
C=base+f""".row{{display:flex;gap:22px;width:100%;align-items:center}}.col{{flex:1;display:flex;flex-direction:column;gap:8px}}.pal{{display:flex;gap:12px;justify-content:center}}.pal .sw span{{display:none}}.pal .sw i{{width:46px;height:46px}}</style></head><body><div class=wrap>{hd}
<div class=tiles>{th(tt)}<div class=g>{tl(238)}</div></div>
<div class=row><div class=mat style='width:440px;height:440px'></div><div class=col>{th('RACK MATCHES')}{racks(50,86)}<div class=pal style='margin-top:6px'>{pal()}</div></div></div>{ft}</div></body></html>"""
for k,h in (('A',A),('B',B),('C',C)): open(f"{out}-{variant}-story{k}.html",'w').write(h)
