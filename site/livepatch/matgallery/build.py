"""Mat Gallery code block (/mahjong-mats). Data = FYM catalog mats (scratchpad fymfix2/build/index.html const D),
images = assets/mats/gallery/<name>.webp (commit pinned). Hidden (hid) and photo-coming-soon (ph) mats are left out.
Usage: python3 build.py D.json manifest.json COMMIT > matgallery.html"""
import json,sys,html,re
D=json.load(open(sys.argv[1]));M=D['mats'];man=json.load(open(sys.argv[2]));C=sys.argv[3]
COL=[('pink','Pink'),('red','Red'),('blue','Blue'),('green','Green'),('purple','Purple'),('yellow','Yellow & Orange'),('neutral','Neutral & Ivory'),('dark','Dark & Moody'),('holiday','Holiday')]
def col(v):
    if v.get('hol'):return 'holiday'
    f=(v.get('mf') or ['neutral'])[0]
    return 'yellow' if f in('orange','yellow') else f
rows=[];brands=set()
for name,k in man.items():
    v=M[k];c=col(v);brands.add(v['bn'])
    nm=re.sub(r'\s+(Mahjong|Mahj)?\s*Mats?$','',v['n'],flags=re.I).strip() or v['n']
    rows.append([name,nm,v['bn'],'' if v.get('rt') else v['u'],1 if v.get('rt') else 0,c,(v.get('dc') or '').replace('https://mahjmatchmaker.com','')])
order={c:i for i,(c,_) in enumerate(COL)}
rows.sort(key=lambda r:(order.get(r[5],99),r[2].lower(),r[1].lower()))
cnt={c:sum(1 for r in rows if r[5]==c) for c,_ in COL}
chips='<button type="button" class="mmg-chip" data-f="all" aria-pressed="true">All mats</button>'+''.join(f'<button type="button" class="mmg-chip" data-f="{c}" aria-pressed="false">{html.escape(l)}</button>' for c,l in COL if cnt[c])
opts='<option value="">All brands</option>'+''.join(f'<option>{html.escape(b)}</option>' for b in sorted(brands,key=str.lower))
secs=''.join(f'<section class="mmg-sec" data-c="{c}"><h2 class="mmg-h">{html.escape(l)} mahjong mats</h2><ul class="mmg-grid"></ul><p class="mmg-empty">No mats here from that brand yet.</p></section>' for c,l in COL if cnt[c])
CSS=open(__file__.replace('build.py','style.css')).read()
data=json.dumps(rows,separators=(',',':'),ensure_ascii=False).replace('</','<\\/')
JS=r"""(function(){var r=document.currentScript.parentNode,R=JSON.parse(r.querySelector('script[type="application/json"]').textContent),B='https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@__C__/assets/mats/gallery/',f='all',br='';
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
r.querySelectorAll('.mmg-sec').forEach(function(s){var c=s.dataset.c,h='';R.forEach(function(x){if(x[5]!==c)return;var shop=x[3]?'<a class="mmg-shop" href="'+esc(x[3])+'" target="_blank" rel="sponsored noopener">Shop the mat</a>':'<span class="mmg-ret">Retired</span>';var img='<img src="'+B+x[0]+'.webp" alt="'+esc(x[2]+' '+x[1])+' mahjong mat" loading="lazy" decoding="async" width="640" height="640">';h+='<li class="mmg-card" data-b="'+esc(x[2])+'">'+(x[3]?'<a class="mmg-img" href="'+esc(x[3])+'" target="_blank" rel="sponsored noopener">'+img+'</a>':'<span class="mmg-img">'+img+'</span>')+'<div class="mmg-body"><span class="mmg-brand">'+esc(x[2])+'</span><span class="mmg-name">'+esc(x[1])+'</span>'+(x[6]?'<a class="mmg-code" href="'+esc(x[6])+'">'+esc(x[2])+' guide</a>':'')+shop+'</div></li>'});s.querySelector('.mmg-grid').innerHTML=h});
var chips=r.querySelectorAll('.mmg-chip'),sel=r.querySelector('.mmg-brand-sel'),tot=r.querySelector('.mmg-total');
function go(){var all=0;chips.forEach(function(x){x.setAttribute('aria-pressed',x.dataset.f===f?'true':'false')});r.querySelectorAll('.mmg-sec').forEach(function(s){var on=f==='all'||s.dataset.c===f,n=0;s.hidden=!on;if(!on)return;s.querySelectorAll('.mmg-card').forEach(function(c){var ok=!br||c.dataset.b===br;c.hidden=!ok;if(ok)n++});s.querySelector('.mmg-empty').style.display=n?'none':'block';if(br&&!n)s.hidden=true;all+=n});tot.textContent=all+' mats'}
chips.forEach(function(x){x.addEventListener('click',function(){f=x.dataset.f;go()})});sel.addEventListener('change',function(){br=sel.value;go()});go()})();""".replace('__C__',C)
print(f"""<style>{CSS}</style>
<div class="mmg"><span class="mmg-eyebrow">The Mat Library</span>
<h1 class="mmg-title">Mahjong Mats by Color</h1>
<p class="mmg-intro">Every mat in my matching library, all in one place. Browse by color or pick a brand, then tap any mat to shop it. Want to see which tiles go with a mat? <a href="/mahjong-tile-matches">See my tile matches</a>, and watch for Find Your Match, coming 10.27.</p>
<div class="mmg-chips" role="group" aria-label="Filter mats by color">{chips}</div>
<div class="mmg-tools"><label for="mmg-brand">Brand</label><select id="mmg-brand" class="mmg-brand-sel">{opts}</select><span class="mmg-total" aria-live="polite"></span></div>
{secs}
<script type="application/json">{data}</script>
<script>{JS}</script></div>""")
