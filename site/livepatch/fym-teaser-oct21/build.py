#!/usr/bin/env python3
"""Build the /find-your-match pre-launch teaser code block (STAGED, not live).

python3 build.py  ->  teaser-block.html

- Logo ticker: CSS + logos copied from ../home-oct21/new-block-mahjmatch-callout.html,
  re-scoped from #mmcode/.mmcb-* to #mmtz/.mmtz-* so the two blocks never clash.
- Teaser mats: partner brands only (no Mahjong Studios, no Paige Spearin collab, no non-partners),
  images from the live Mat Gallery's jsDelivr pin (already warmed).
- Countdown target: Tue Oct 27 2026, 9:00am CT = 14:00 UTC (same instant as site/livepatch/launch-oct27).
"""
import os, re, html
HERE = os.path.dirname(os.path.abspath(__file__))
CALLOUT = os.path.join(HERE, '..', 'home-oct21', 'new-block-mahjmatch-callout.html')

LAUNCH_UTC = '2026-10-27T14:00:00Z'
GAL = 'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@5dcf9bdd71515f5532cf83c9dd4f38c2760aec84/assets/mats/gallery/'
# (gallery image id, mat name, brand, action)  action: x = flicked away, h = gets a heart
MATS = [
    ('oh-my-mahjong--chantilly', 'Chantilly', 'Oh My Mahjong', 'x'),
    ('bespoke-mahjong--flirty-leopards-mint-julep', 'Flirty Leopards Mint Julep', 'Bespoke Mahjong', 'h'),
    ('anders-ruff--house-of-hydrangea', 'House of Hydrangea', 'Anders Ruff', 'x'),
    ('my-fair-mahjong--prism-pink', 'Prism Pink', 'My Fair Mahjong', 'h'),
    ('bird-bamboo--the-paradise-mahjong-mat-tropical-teal', 'The Paradise, Tropical Teal', 'Bird & Bamboo', 'x'),
    ('britt-mills--heiress', 'Heiress', 'Britt Mills', 'h'),
    ('let-s-be-besties--pink-orange-tie-dye', 'Pink & Orange Tie Dye', "Let's Be Besties", 'x'),
    ('virora-mahjong--petalwing', 'Petalwing', 'Virora Mahjong', 'h'),
    ('miss-mahjong--canopy-palm', 'Canopy Palm', 'Miss Mahjong', 'x'),
    ('mahj-vine--chinoiserie-citrus-grove', 'Chinoiserie Citrus Grove', 'Mahj & Vine', 'h'),
    ('mahj-mood--rally-in-pink', 'Rally in Pink', 'Mahj Mood', 'x'),
    ('virora-mahjong--liliora-mahjong-mat', 'Liliora', 'Virora Mahjong', 'h'),
]
# Counted Oct 21 from the live FYM build (fym-oct21d, v68): 757 visible mats, 50 mat brands
# (51 brand labels minus the generic "Etsy" label), 264 tile sets. See README.
SCALE = 'Hundreds of mats. 50 brands. 260+ tile sets.'

def ticker():
    s = open(CALLOUT).read()
    css = s[s.index('<style>') + 7:s.index('</style>')]
    # keep only the ticker rules
    keep = []
    for rule in re.findall(r'[^{}]+\{[^{}]*\}|@keyframes[^{]+\{[^{}]*\{[^{}]*\}\}|@media[^{]+\{(?:[^{}]*\{[^{}]*\})+\}', css):
        if 'mmcb-tk' in rule or 'mmcb-tt' in rule or 'mmcbscroll' in rule:
            if rule.startswith('@media'):
                inner = re.findall(r'[^{}]+\{[^{}]*\}', rule[rule.index('{') + 1:-1])
                inner = [r for r in inner if 'mmcb-tk' in r or 'mmcb-tt' in r]
                rule = rule[:rule.index('{') + 1] + ''.join(inner) + '}'
            keep.append(rule)
    css = ''.join(keep)
    css = css.replace('#mmcode', '#mmtz').replace('mmcbscroll', 'mmtzscroll').replace('mmcb-', 'mmtz-')
    i = s.index('<div class="mmcb-tk"')
    j = s.index('</div></div>', i) + 12
    tk = s[i:j].replace('mmcb-', 'mmtz-')
    assert 'b0' in tk and 'b32' in tk
    return css, tk

def build():
    tcss, thtml = ticker()
    cards = ''.join(
        f'<figure class="mmtz-c" data-a="{a}" aria-hidden="true"><img src="{GAL}{img}.webp" alt="" loading="lazy" decoding="async" width="640" height="640">'
        f'<span class="mmtz-x">&#10005;</span><span class="mmtz-h">&#9829;</span>'
        f'<figcaption><b>{html.escape(n)}</b>{html.escape(b)}</figcaption></figure>'
        for img, n, b, a in MATS)
    alt = ', '.join(f'{n} by {b}' for _, n, b, _ in MATS)
    css = r"""
#mmtz{--nv:#054689;--dn:#062a55;--pk:#c8325f;--hp:#d6336c;--ht:#f56c8c;--bl:#f7b6c8;--pc:#fbe3ea;--cr:#faf3ea;color:var(--nv);background:var(--cr);font-family:'Bitter',Georgia,serif;text-align:center;overflow:hidden;box-sizing:border-box;width:100%;border-radius:22px;padding:44px 0 34px}
#mmtz *{box-sizing:border-box}
#mmtz .mmtz-w{max-width:980px;margin:0 auto;padding:0 20px}
#mmtz .mmtz-k{display:inline-block;background:var(--pk);color:#fff;font:700 13px/1 'Bitter',Georgia,serif;letter-spacing:.16em;text-transform:uppercase;padding:9px 16px;border-radius:999px;margin:0 0 16px}
#mmtz h1.mmtz-t{font-family:'Caprasimo',Georgia,serif;font-weight:400;font-size:clamp(40px,7vw,72px);line-height:1.02;color:var(--nv);margin:0 0 12px;letter-spacing:0}
#mmtz h1.mmtz-t em{font-style:italic}
#mmtz h1.mmtz-t sup{font-size:.32em;vertical-align:super;font-family:'Bitter',Georgia,serif}
#mmtz .mmtz-d{font-family:'Playfair Display',Georgia,serif;font-style:italic;font-size:clamp(19px,2.3vw,24px);line-height:1.4;color:var(--dn);margin:0 auto 26px;max-width:640px}
#mmtz .mmtz-cd{display:flex;justify-content:center;gap:12px;margin:0 auto 10px}
#mmtz .mmtz-cd div{background:var(--nv);color:#fff;border-radius:16px;width:96px;padding:14px 0 10px}
#mmtz .mmtz-cd b{display:block;font-family:'Caprasimo',Georgia,serif;font-weight:400;font-size:44px;line-height:1}
#mmtz .mmtz-cd span{display:block;font:700 12px/1 'Bitter',Georgia,serif;letter-spacing:.14em;text-transform:uppercase;color:var(--bl);margin-top:8px}
#mmtz .mmtz-when{font:600 15px 'Bitter',Georgia,serif;color:var(--dn);margin:0 0 30px}
#mmtz .mmtz-live{display:none;font-family:'Caprasimo',Georgia,serif;font-size:30px;margin:6px 0 24px}
#mmtz .mmtz-live a{color:var(--pk)}
#mmtz.is-live .mmtz-cd,#mmtz.is-live .mmtz-when{display:none}
#mmtz.is-live .mmtz-live{display:block}
#mmtz .mmtz-st{position:relative;width:min(300px,76vw);aspect-ratio:1/1.16;margin:0 auto 22px}
#mmtz .mmtz-c{position:absolute;inset:0;margin:0;background:#fff;border-radius:20px;box-shadow:0 14px 34px rgba(6,42,85,.16);padding:10px 10px 0;opacity:0;transform:translateY(14px) scale(.96);transition:transform .7s cubic-bezier(.2,.8,.2,1),opacity .5s}
#mmtz .mmtz-c img{display:block;width:100%;aspect-ratio:1/1;object-fit:cover;border-radius:14px;background:var(--pc)}
#mmtz .mmtz-c figcaption{padding:10px 6px 0;font:600 13px/1.25 'Bitter',Georgia,serif;color:var(--dn);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#mmtz .mmtz-c figcaption b{display:block;font-family:'Lora',Georgia,serif;font-weight:700;font-size:16px;color:var(--nv);overflow:hidden;text-overflow:ellipsis}
#mmtz .mmtz-c.on{opacity:1;transform:none;z-index:2}
#mmtz .mmtz-c.nx{opacity:1;transform:translateY(10px) scale(.95) rotate(-2deg);z-index:1}
#mmtz .mmtz-c.out-x{opacity:0;transform:translateX(-130%) rotate(-18deg);z-index:3;transition:transform .75s cubic-bezier(.5,0,.75,0),opacity .75s}
#mmtz .mmtz-c.out-h{opacity:0;transform:translateX(130%) rotate(14deg);z-index:3;transition:transform .75s cubic-bezier(.5,0,.75,0),opacity .75s}
#mmtz .mmtz-x,#mmtz .mmtz-h{position:absolute;top:38%;left:50%;width:84px;height:84px;margin:-42px 0 0 -42px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:44px;line-height:1;opacity:0;transform:scale(.4);transition:transform .35s cubic-bezier(.3,1.6,.5,1),opacity .25s;pointer-events:none}
#mmtz .mmtz-x{background:#fff;color:var(--nv);border:3px solid var(--nv);font-family:Arial,sans-serif;font-weight:700;font-size:38px}
#mmtz .mmtz-h{background:var(--ht);color:#fff;box-shadow:0 8px 22px rgba(214,51,108,.35)}
#mmtz .mmtz-c.say-x .mmtz-x,#mmtz .mmtz-c.say-h .mmtz-h{opacity:1;transform:scale(1)}
#mmtz .mmtz-sc{font-family:'Lora',Georgia,serif;font-weight:700;font-size:clamp(19px,2.4vw,24px);line-height:1.35;color:var(--nv);margin:0 0 30px}
#mmtz .mmtz-n{background:#fff;border:2px solid var(--pc);border-radius:20px;max-width:640px;margin:0 auto 30px;padding:24px 22px}
#mmtz .mmtz-n h2{font-family:'Caprasimo',Georgia,serif;font-weight:400;font-size:clamp(26px,3.4vw,32px);line-height:1.15;color:var(--nv);margin:0 0 8px}
#mmtz .mmtz-n p{font-size:17px;line-height:1.5;color:var(--dn);margin:0 0 14px}
#mmtz .mmtz-slot:empty{display:none}
#mmtz .mmtz-slot .sqs-block{padding:0!important}
#mmtz .mmtz-ph{border:2px dashed var(--bl);border-radius:14px;padding:16px;font-size:15px;color:var(--pk);margin:0 0 14px}
#mmtz .mmtz-slot:not(:empty)+.mmtz-ph{display:none}
#mmtz .mmtz-fb{font-size:16px;margin:0}
#mmtz .mmtz-fb a{color:var(--pk);font-weight:700}
#mmtz .mmtz-tkh{font:700 13px/1 'Bitter',Georgia,serif;letter-spacing:.16em;text-transform:uppercase;color:var(--pk);margin:6px 0 0}
#mmtz .mmtz-tk{margin:0 0 6px}
#mmtz .mmtz-cw{margin:26px 0 0}
#mmtz .mmtz-cw p{font-family:'Caprasimo',Georgia,serif;font-size:24px;color:var(--nv);margin:0 0 12px}
#mmtz .mmtz-btn{display:inline-block;background:var(--pk);color:#fff!important;text-decoration:none!important;font:700 17px/1 'Bitter',Georgia,serif;padding:16px 28px;border-radius:999px}
#mmtz .mmtz-btn:hover{background:var(--hp)}
#mmtz .mmtz-sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
@media(max-width:600px){#mmtz{padding:32px 0 26px;border-radius:0}#mmtz .mmtz-w{padding:0 16px}#mmtz .mmtz-cd{gap:8px}#mmtz .mmtz-cd div{width:76px;padding:12px 0 9px;border-radius:14px}#mmtz .mmtz-cd b{font-size:34px}#mmtz .mmtz-cd span{font-size:11px;letter-spacing:.1em}#mmtz .mmtz-n{padding:20px 16px}}
@media(prefers-reduced-motion:reduce){#mmtz .mmtz-c,#mmtz .mmtz-x,#mmtz .mmtz-h{transition:none}}
"""
    js = r"""
(function(){
  var R=document.getElementById('mmtz');if(!R||R.getAttribute('data-on'))return;R.setAttribute('data-on','1');
  var T=Date.parse('""" + LAUNCH_UTC + r"""'),cd=R.querySelector('.mmtz-cd');
  function pad(n){return n<10?'0'+n:''+n}
  function tick(){var ms=T-Date.now();if(ms<=0){R.className+=' is-live';return false}
    var s=Math.floor(ms/1000),d=Math.floor(s/86400),h=Math.floor(s%86400/3600),m=Math.floor(s%3600/60);
    cd.querySelector('[data-u=d]').textContent=d;cd.querySelector('[data-u=h]').textContent=pad(h);
    cd.querySelector('[data-u=m]').textContent=pad(m);cd.querySelector('[data-u=s]').textContent=pad(s%60);return true}
  if(tick()){var iv=setInterval(function(){if(!tick())clearInterval(iv)},1000)}
  /* teaser loop: one mat at a time, flicked away (X) or given a heart */
  var C=[].slice.call(R.querySelectorAll('.mmtz-c')),i=0,n=C.length,red=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  function show(){C.forEach(function(c){c.className='mmtz-c'});C[i%n].className='mmtz-c on';C[(i+1)%n].className='mmtz-c nx'}
  show();
  function step(){var c=C[i%n],a=c.getAttribute('data-a');c.className+=' say-'+a;
    setTimeout(function(){c.className='mmtz-c out-'+a;C[(i+1)%n].className='mmtz-c on';C[(i+2)%n].className='mmtz-c nx';
      setTimeout(function(){c.className='mmtz-c';i=(i+1)%n},800)},red?900:850)}
  var timer=null;function go(){if(!timer)timer=setInterval(step,red?3400:2300)}function stop(){clearInterval(timer);timer=null}
  if('IntersectionObserver' in window){new IntersectionObserver(function(e){e[0].isIntersecting?go():stop()}).observe(R.querySelector('.mmtz-st'))}else go();
  document.addEventListener('visibilitychange',function(){document.hidden?stop():go()});
  /* Notify me: move the page's native Squarespace Newsletter block into the slot (add one anywhere on the page) */
  function mv(){var nb=document.querySelector('.sqs-block-newsletter'),sl=R.querySelector('.mmtz-slot');if(!nb||!sl||sl.contains(nb))return;
    var fe=nb.closest('.fe-block');sl.appendChild(nb);if(fe)fe.style.display='none'}
  mv();if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',mv);window.addEventListener('load',mv);
})();
"""
    body = f"""<div id="mmtz"><div class="mmtz-w">
<p class="mmtz-k">Coming 10.27</p>
<h1 class="mmtz-t">Find <em>Your</em> Mat-ch<sup>&trade;</sup></h1>
<p class="mmtz-d">Make your own matches. Pick your tiles, swipe through the mats that bring out their best colors, and shop it all with code MAHJMATCH.</p>
<div class="mmtz-cd" role="timer" aria-label="Countdown to launch"><div><b data-u="d">6</b><span>Days</span></div><div><b data-u="h">00</b><span>Hours</span></div><div><b data-u="m">00</b><span>Min</span></div><div><b data-u="s">00</b><span>Sec</span></div></div>
<p class="mmtz-when">Tuesday, October 27</p>
<p class="mmtz-live">It&rsquo;s live! <a href="/find-your-match">Start swiping</a></p>
<div class="mmtz-st" role="img" aria-label="Partner mats waiting to meet your tiles: {html.escape(alt)}">{cards}</div>
<p class="mmtz-sc">{SCALE}</p>
<div class="mmtz-n" id="notify"><h2>Save the date</h2><p>Get a note the minute it goes live.</p>
<div class="mmtz-slot"></div><div class="mmtz-ph">[Newsletter block goes here: add a Squarespace Newsletter block to this page. See README.]</div>
<p class="mmtz-fb">Or <a href="https://www.facebook.com/groups/mahjmatchmaker">join the Facebook group</a> to hear it first.</p></div>
</div>
<p class="mmtz-tkh">Mats from our partner brands</p>
{thtml}
<div class="mmtz-w mmtz-cw"><p>Can&rsquo;t wait?</p><a class="mmtz-btn" href="/mahjong-tile-matches">Browse the albums</a></div>
</div>"""
    fonts = "@import url('https://fonts.googleapis.com/css2?family=Caprasimo&family=Bitter:wght@600;700&family=Lora:wght@700&family=Playfair+Display:ital,wght@1,500&display=swap');"
    out = f"<style>{fonts}{css}{tcss}</style>{body}<script>{js}</script>\n"
    for bad in ('TEACHMAHJ', 'Mahjong Studios', '#8b', 'brown'):
        assert bad not in out, bad
    open(os.path.join(HERE, 'teaser-block.html'), 'w').write(out)
    print('teaser-block.html', len(out), 'bytes')

if __name__ == '__main__':
    build()
