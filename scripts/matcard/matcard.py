"""Mat Edit color cards for OMM mats (Tiffany, Oct 12, 2026).
Usage: python3 scripts/matcard/matcard.py spec.json out/prefix  -> prefix-{omm,all}-{fb,pin}.html, then screenshot.
spec: name, brand, tag, color (title hex), mat_path (flat mat photo cropped square, see palette.py crop_mat), palette [[name,hex]...6], racks [[name,hex,dark?]...5] (nearest Bird & Bamboo colors, work/bbracks.json), tiles_omm [...], tiles_all [...], retired [...] (album tile names from assets/tiles/album/index.json)."""
import json,base64,io,sys,os
from PIL import Image
ROOT=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
F=os.environ.get('MATCARD_FONTS','/tmp/cc/f/')  # npm pack @fontsource/alfa-slab-one @fontsource/playfair-display @fontsource/bitter, untar into this dir
def b64(p,fmt=None,size=None):
    im=Image.open(p); 
    if size: im.thumbnail((size,size))
    fmt=fmt or ('PNG' if im.mode=='RGBA' else 'JPEG'); b=io.BytesIO(); (im if fmt=='PNG' else im.convert('RGB')).save(b,fmt,**({'quality':90} if fmt=='JPEG' else {}))
    return f'data:image/{fmt.lower()};base64,'+base64.b64encode(b.getvalue()).decode()
def font(n,p): return f"@font-face{{font-family:'{n}';src:url(file://{F}{p})}}"
# album tile shots from the Larkspur book (same as album cards)
IDX=json.load(open(ROOT+'/assets/tiles/album/index.json'))
TILE={k:{'img':b64(ROOT+'/'+v['file'],size=300)} for k,v in IDX.items()}
STORY='''.wrap{padding:200px 60px 220px}  /* IG story safe zones: keep text out of the top 200px and bottom 220px */
.mid{flex-direction:column;align-items:center;gap:26px;margin-top:26px}.mat{width:620px!important;height:620px!important}
.side{flex:none;width:860px}.pal{grid-template-columns:1fr 1fr 1fr}.side .h~.h,.rks{display:none}
.tiles{margin-top:22px}h1{font-size:124px}'''
def card(c,W,H,out):
    rt=set(c.get('retired',[]))
    c=dict(c,racks=sorted(c['racks'],key=lambda r:1 if (len(r)>3 and r[3]) else 0))  # Bird & Bamboo bars stack together; other brands' rack photos go below (Tiffany, Oct 13)
    tiles=''.join(f"<figure><div class='tp' style=\"background-image:url({TILE[t]['img']})\"></div><figcaption>{t.replace(' (retired)','')}{'<small>retired</small>' if (t in rt or '(retired)' in t) else ''}</figcaption></figure>" for t in c['tiles'])
    pal=''.join(f"<div class='sw'><i style='background:{h}'></i><span>{n}</span></div>" for n,h in c['palette'])
    rk=''.join((f"<div class='rkp'><div class='rki' style=\"background-image:url({b64(ROOT+'/'+r[3],'JPEG',700)})\"></div><span>{r[0]}</span></div>" if len(r)>3 and r[3] else f"<div class='rk' style='background:{r[1]};color:{'#fff' if r[2] else '#2a2036'}'>{r[0]}</div>") for r in c['racks'])  # Bird & Bamboo = painted color bar (generated); any other brand's rack = its REAL product photo (Tiffany, Oct 13)
    pin=H/W>1.4
    story=H/W>1.7
    html=f"""<!doctype html><html><head><meta charset=utf8><style>
{font('Alfa','fontsource-alfa-slab-one-5.3.0/package/files/alfa-slab-one-latin-400-normal.woff2')}
{font('PlayI','fontsource-playfair-display-5.3.0/package/files/playfair-display-latin-400-italic.woff2')}
{font('Bitter','fontsource-bitter-5.3.0/package/files/bitter-latin-400-normal.woff2')}
@font-face{{font-family:'BitterB';src:url(file://{F}fontsource-bitter-5.3.0/package/files/bitter-latin-700-normal.woff2)}}
*{{box-sizing:border-box;margin:0}}body{{width:{W}px;height:{H}px;background:#f6e9df;font-family:Bitter;color:#2a2036;overflow:hidden;position:relative}}
.wrap{{position:absolute;inset:0;padding:{44 if pin else 40}px 56px;display:flex;flex-direction:column;align-items:center}}
.logo{{height:{66 if pin else 58}px}}
.eb{{font-family:BitterB;letter-spacing:.32em;font-size:22px;color:#054689;margin-top:{26 if pin else 18}px;display:flex;align-items:center;gap:14px}}.eb img{{height:30px}}
h1{{font-family:Alfa;font-size:{c.get('ts',118)}px;line-height:1;color:{c['color']};text-shadow:4px 4px 0 #fff;margin-top:8px;text-transform:uppercase;letter-spacing:.01em}}
.by{{font-family:PlayI;font-size:38px;color:#2a2036;margin-top:6px}}.tag{{font-family:PlayI;font-size:26px;color:#6b5a77;margin-top:4px}}
.mid{{display:flex;gap:30px;margin-top:{30 if pin else 22}px;align-items:flex-start;width:100%;justify-content:center}}
.mat{{width:{560 if not pin else 520}px;height:{560 if not pin else 520}px;border-radius:22px;background:url({c['mat']}) center/cover;box-shadow:0 10px 30px rgba(42,32,54,.18)}}
.side{{flex:0 0 340px;display:flex;flex-direction:column;gap:14px}}
.h{{font-family:BitterB;letter-spacing:.24em;font-size:19px;color:#054689;text-align:center;display:flex;align-items:center;justify-content:center;gap:10px}}.h img{{height:24px}}
.pal{{display:grid;grid-template-columns:1fr 1fr;gap:12px 10px;background:#fff8f2;border-radius:18px;padding:16px}}
.sw{{display:flex;align-items:center;gap:10px;font-family:BitterB;font-size:16px;text-transform:uppercase;letter-spacing:.04em}}.sw i{{width:44px;height:44px;border-radius:50%;flex:none;box-shadow:inset 0 0 0 2px rgba(255,255,255,.6)}}
.rks{{display:flex;flex-direction:column;gap:7px;background:#fff8f2;border-radius:18px;padding:14px 16px}}.rk{{font-family:BitterB;font-size:17px;padding:7px 12px;border-radius:6px;box-shadow:inset 0 -4px 0 rgba(0,0,0,.12)}}
.rkp{{display:flex;flex-direction:column;gap:4px}}.rki{{height:92px;border-radius:8px;background:center/cover;box-shadow:inset 0 0 0 1px rgba(0,0,0,.06)}}.rkp span{{font-family:BitterB;font-size:15px;color:#2a2036;text-align:center}}.rks small{{font-size:13px;color:#6b5a77;text-align:center;margin-top:2px}}
.tiles{{margin-top:{30 if pin else 22}px;width:100%}}.trow{{display:flex;justify-content:center;gap:16px;margin-top:12px}}
figure{{width:132px;text-align:center}}.tp{{width:132px;height:132px;border-radius:16px;background-size:cover;background-position:center;background-color:#efe2d6;box-shadow:0 4px 12px rgba(42,32,54,.15)}}
figcaption{{font-family:BitterB;font-size:17px;margin-top:8px;line-height:1.15}}figcaption small{{display:block;font-family:Bitter;font-size:13px;color:#6b5a77}}
.web{{margin-top:auto;font-family:BitterB;font-size:28px;color:#054689;display:flex;align-items:center;gap:10px}}.web img{{height:34px}}
.cp{{margin-top:16px;background:#054689;color:#fff;border-radius:999px;padding:14px 34px;font-family:BitterB;font-size:24px}}
{STORY if story else ''}</style></head><body><div class=wrap>
<img class=logo src="{c['logo']}">
<div class=eb><img src="{c['flame']}">THE MAT EDIT<img src="{c['flame']}"></div>
<h1>{c['name']}</h1><div class=by>by {c['brand']}</div><div class=tag>{c['tag']}</div>
<div class=mid><div class=mat></div><div class=side>
<div class=h>THE PALETTE</div><div class=pal>{pal}</div>
{("<div class=h>RACK MATCHES</div><div class=rks>"+rk+"<small>"+c.get('rackNote','Bird &amp; Bamboo painted wood racks')+"</small></div>") if c['racks'] else ""}
</div></div>
{"<div class=tiles><div class=h><img src='"+c['flame']+"'>"+c.get('tilesTitle',"TIFFANY'S TILE MATCHES")+"<img src='"+c['flame']+"'></div><div class=trow>"+tiles+"</div></div>" if c['tiles'] else ""}
<div class=web><img src="{c['flame']}">www.mahjmatchmaker.com</div>
<div class=cp>First date's on us. Use code MAHJMATCH to save 10%.</div>
</div></body></html>"""
    open(out,'w').write(html)
if __name__=='__main__':
    c=json.load(open(sys.argv[1]))
    c['mat']=b64(c['mat_path'],'JPEG',1100)
    c['logo']=b64(ROOT+'/assets/brand/mahjmatchmaker-wordmark.png',size=700); c['flame']=b64(ROOT+'/assets/brand/flame-heart.png',size=120)
    # two versions (Tiffany, Oct 12): OMM-only (current + retired OMM sets, for OMM to reshare) and all album tile sets
    for v,tl,tt in (('omm',c.get('tiles_omm',[]),"TIFFANY'S OMM TILE MATCHES"),('all',c.get('tiles_all',[]),"TIFFANY'S TILE MATCHES")):
        cc=dict(c,tiles=tl,tilesTitle=tt)
        if v=='omm': cc['racks']=c.get('racks_omm',c['racks'])  # OMM-only card shows only OMM products
        card(cc,1080,1350,f"{sys.argv[2]}-{v}-fb.html"); card(cc,1000,1500,f"{sys.argv[2]}-{v}-pin.html"); card(cc,1080,1920,f"{sys.argv[2]}-{v}-story.html")  # IG story 9:16 (Tiffany Oct 12: stories on mat launch days)
    print('render the .html files with playwright (1080x1350 / 1000x1500 screenshots)')
