import base64,io,os
from PIL import Image
HERE=os.path.dirname(os.path.abspath(__file__));O=HERE+'/out'
def du(f,w=720):
    im=Image.open(os.path.join(O,f)).convert('RGB');h=int(im.height*w/im.width);im=im.resize((w,h),Image.LANCZOS)
    b=io.BytesIO();im.save(b,'JPEG',quality=80);return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
C=[('sunday','Sunday + Carson Vintage'),('papaya','Papaya Spritz + Regency Scalloped'),('pippa','Pippa + Hampton')]
def fig(f,cap):return f'<figure><button class="z" type="button" aria-label="Enlarge {cap}"><img src="{du(f)}" alt="{cap}" loading="lazy"></button><figcaption>{cap}</figcaption></figure>'
def row(d,fmt):return '<div class="grid">'+''.join(fig(f'{d}_{k}_{fmt}.jpg',n) for k,n in C)+'</div>'
OPTS=[('bands','A','Close-up bands','Your idea for the Table view: three zoomed-in bands stacked like a spliced screenshot. Tiles on top, a close-up of the mat filling the middle, racks laid out flat on the bottom. Every item gets a real look at its colors.'),
('spread','B','The spread','The love-triangle view, opened up. The mat is the hero, the tile pile sits big and out to the right, the racks sit out to the left, and the names move into small tags on the pictures so there is less text.'),
('split','C','Showcase','The full mat and a tile close-up side by side, with the racks laid out wide underneath. Good for a shopping view: every piece is big and has its brand logo.')]
sec=''
for d,L,t,desc in OPTS:
    extra=''
    if d=='spread':
        extra=f'<h3>Before and after: Papaya Spritz + Regency Scalloped</h3><div class="ba">{fig("before_tri_papaya_fb.jpg","Before: current love-triangle card")}{fig("spread_papaya_fb.jpg","After: option B")}</div>'
    sec+=f'''<section id="opt-{L.lower()}"><header class="oh"><span class="tag">Option {L}</span><h2>{t}</h2><p>{desc}</p></header>
<h3>Facebook post (4:5)</h3>{row(d,'fb')}<h3>Pinterest pin (2:3)</h3>{row(d,'pin')}{extra}</section>'''
html=f'''<title>Match Card Options</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Caprasimo&family=DM+Sans:wght@400;600;700&display=swap">
<style>
/* Layout: one long review page, each option a section of three real combos, tap any card to see it full size */
:root{{--bg:#fbf4ee;--surface:#ffffff;--ink:#2a2036;--muted:#6f6380;--navy:#054689;--pink:#c8325f;--line:#ecd9de;
--display:Caprasimo,Georgia,serif;--body:"DM Sans",system-ui,-apple-system,sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#1d1824;--surface:#2a2333;--ink:#f3eaf2;--muted:#b8aac4;--navy:#8db7ff;--pink:#ff8fb3;--line:#3d3348;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#1d1824;--surface:#2a2333;--ink:#f3eaf2;--muted:#b8aac4;--navy:#8db7ff;--pink:#ff8fb3;--line:#3d3348;color-scheme:dark}}
body{{background:var(--bg);color:var(--ink);font-family:var(--body);font-size:16px;line-height:1.5;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:28px 60px}}
.wrap{{max-width:1180px;margin:0 auto;display:flex;flex-direction:column;gap:48px}}
.top h1{{font-family:var(--display);font-weight:400;color:var(--pink);font-size:clamp(34px,6vw,56px);line-height:1.05;margin:0 0 10px;text-wrap:balance}}
.top p{{margin:0;max-width:62ch;color:var(--muted)}}
.jump{{display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}}.jump a{{color:var(--navy);text-decoration:none;font-weight:700;border:1.5px solid var(--line);border-radius:999px;padding:6px 14px;background:var(--surface)}}
.jump a:focus-visible,.z:focus-visible{{outline:3px solid var(--pink);outline-offset:3px}}
section{{display:flex;flex-direction:column;gap:14px;border-top:2px solid var(--line);padding-top:28px}}
.oh h2{{font-family:var(--display);font-weight:400;font-size:clamp(26px,4vw,38px);margin:4px 0 6px;color:var(--navy)}}.oh p{{margin:0;max-width:65ch}}
.tag{{font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--pink)}}
h3{{font-size:13px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin:14px 0 0}}
.grid{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}}.ba{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;max-width:800px}}
@media (max-width:720px){{.grid{{grid-template-columns:1fr 1fr}}}}@media (max-width:460px){{.grid,.ba{{grid-template-columns:1fr}}}}
figure{{margin:0;display:flex;flex-direction:column;gap:6px;min-width:0}}figcaption{{font-size:14px;color:var(--muted)}}
.z{{padding:0;border:0;background:none;cursor:zoom-in;border-radius:14px;overflow:hidden;box-shadow:0 6px 18px rgba(60,30,50,.14)}}.z img{{display:block;width:100%;height:auto}}
#lb{{position:fixed;inset:0;background:rgba(20,12,24,.88);display:flex;align-items:center;justify-content:center;padding:max(16px,env(safe-area-inset-top,0px)) max(16px,env(safe-area-inset-right,0px)) max(16px,env(safe-area-inset-bottom,0px)) max(16px,env(safe-area-inset-left,0px));z-index:20;cursor:zoom-out}}
#lb img{{max-height:100%;max-width:100%;border-radius:12px}}
</style>
<div class="wrap">
<div class="top"><h1>Match Card Options</h1><p>Three new directions for the Find Your Match card, each drawn with real tiles, mats and racks from the app on three of your combos. Pick the one you want, or mix them: for example, close-up bands for the Table view and the spread for the love triangle.</p>
<nav class="jump"><a href="#opt-a">A · Close-up bands</a><a href="#opt-b">B · The spread</a><a href="#opt-c">C · Showcase</a></nav></div>
{sec}
</div>
<div id="lb" hidden><img alt="Full-size card"></div>
<script>
const lb=document.getElementById('lb'),li=lb.querySelector('img');
document.querySelectorAll('.z').forEach(b=>b.addEventListener('click',()=>{{const i=b.querySelector('img');li.src=i.src;li.alt=i.alt;lb.hidden=false;}}));
lb.addEventListener('click',()=>{{lb.hidden=true;}});document.addEventListener('keydown',e=>{{if(e.key==='Escape')lb.hidden=true;}});
</script>'''
open(HERE+'/match-card-options.html','w').write(html);print(len(html)//1024,'KB')
