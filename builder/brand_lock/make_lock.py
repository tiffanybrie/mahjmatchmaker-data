"""Brand-locked Find Your Mat-ch (SAMPLE, Oct 29; Tiffany 12:41pm). Not public.
Usage: python3 make_lock.py <fym build index.html> <out index.html>
Lock = URL ?brand=<brand name> (or window.FYM_LOCK set by the embed snippet). Only that brand's tile sets,
mats and racks stay visible; shop links go straight to the brand's own product pages (no code, no affiliate ref);
brand menus hidden; a 'Powered by Mahj Matchmaker' badge stays on screen; the match card keeps our branding."""
import sys
SRC, OUT = sys.argv[1:3]
h = open(SRC).read()
L = h.split('\n')
i = [n for n, l in enumerate(L) if l.startswith('const D=')]
assert len(i) == 1
LOCK = r''';(function(){var q=new URLSearchParams(location.search);var B=q.get('brand')||window.FYM_LOCK;if(!B)return;window.LOCKB=B;
function prod(o){var u=o.u0||o.u||'';try{var x=new URL(u);var r=x.searchParams.get('redirect');if(r){x=new URL(decodeURIComponent(r),x.origin);}x.search='';x.hash='';return x.toString();}catch(e){return u;}}
function fix(o){o.u=prod(o);o.dc=null;o.nc=true;o.ncn=false;}
['mats','racks','tiles'].forEach(function(k){var X=D[k]||{};Object.keys(X).forEach(function(id){var o=X[id];if(!o)return;if(o.bn===B)fix(o);else o.hid=true;});});
(D.sets||[]).forEach(function(s){if(s.maker!==B)s.hid=true;});
if(D.uni)D.uni=D.uni.filter(function(r){return D.racks[r]&&D.racks[r].bn===B;});
document.documentElement.classList.add('locked');
window.addEventListener('DOMContentLoaded',function(){var a=document.createElement('a');a.className='pwr';a.href='https://www.mahjmatchmaker.com/find-your-match';a.target='_blank';a.rel='noopener';a.innerHTML='Powered by <b>Mahj Matchmaker</b> ♥';document.body.appendChild(a);});
})();'''
L.insert(i[0] + 1, LOCK)
h = '\n'.join(L)
CSS = '''html.locked .tbrw,html.locked .bnote,html.locked [data-brands]{display:none!important}
.pwr{position:fixed;right:10px;bottom:10px;z-index:80;background:#054689;color:#fff;font:600 12px Bitter,Georgia,serif;padding:6px 12px;border-radius:999px;text-decoration:none;box-shadow:0 4px 12px rgba(5,40,90,.25)}.pwr b{font-weight:700}
'''
j = h.rindex('</style></head>'); h = h[:j] + CSS + h[j:]
n = h.count('<div class="eb">mahjmatchmaker.com</div>'); assert n >= 2, n
h = h.replace('<div class="eb">mahjmatchmaker.com</div>', '<div class="eb">${window.LOCKB?esc(LOCKB)+\' \\u00d7 Mahj Matchmaker\':\'mahjmatchmaker.com\'}</div>')
open(OUT, 'w').write(h); print('ok', len(h), 'eb', n)
