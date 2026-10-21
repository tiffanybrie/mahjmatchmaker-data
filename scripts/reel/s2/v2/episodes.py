"""Season 2 episodes, v2 rebuild (Oct 21): Ep 6 Pippa, Ep 8 Smith, Ep 13 Coquette.
Why a rebuild and not a patch: the Oct 19 episodes baked in rules that changed through the Papaya launch (Oct 21):
brown text/pills/hearts (never brown), album match cards with OLD racks on social (reels use separate tile + mat
characters; racks = config/tile-racks-picks.json final_lists), "FIND YOUR MATCH" / "MAT-ching" naming, a red NOPE
stamp + green heart (UI is navy X + pink heart only), a pronoun for a mat ("bringing him home"), innuendo beyond
"nice rack", the official pair as the last card, and end cards that weren't the hotline v12 card. The episode
scripts, jokes and pacing are kept; the S2 opener (first 3.0 s, scripts/reel/s2/tpl.html) is reused frame-exact.
Silent like the originals: her song goes on in Edits from 0:00.
Usage: python3 scripts/reel/s2/v2/episodes.py pippa|smith|coquette   -> assets/reels/s2/epNN-<set>-s2-v2.mp4"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit
from kit import u, HEAD, R, WORK, DEEP, ROSE, HEART_SVG, FYM

RK = os.environ.get('S2RACKS', '/tmp/claude-0/-home-claude/801d31e6-4a74-59be-8637-eb67bfa0e99e/scratchpad/s2w/assets/')
MAT = lambda f: f'assets/mats/gallery/{f}'
PICKS = json.load(open(R + '/config/tile-racks-picks.json'))['final_lists']
RACK_FILE = {'Miss Mahjong Scalloped Iridescent Opal': 'miss-mahjong-scalloped-iridescent-opal.png', 'Bird & Bamboo Magenta': 'bird-bamboo-magenta.png',
             'Bird & Bamboo Icy Mint': 'bird-bamboo-icy-mint.png', 'Oh My Mahjong Pink Quartz': 'oh-my-mahjong-pink-quartz-rack.png',
             'Middle & Main White Lace Acrylic': 'middle-main-white-lace-acrylic.png', 'Bird & Bamboo Lilac': 'bird-bamboo-lilac.png',
             'Bam Bird Boutique Walnut': 'bam-bird-boutique-walnut.png', 'Peace Love Mahjong Oak': 'peace-love-mahjong-oak.png',
             'Bird & Bamboo Dark Navy': 'bird-bamboo-dark-navy.png'}
esc = lambda s: s.replace('&', '&amp;')


def racks_of(key):
    """The set's CURRENT rack picks, in her order (config/tile-racks-picks.json final_lists)."""
    return [(RK + RACK_FILE[n], esc(n)) for n in PICKS[key]]


ENGINE = """<script>
const cl=x=>x<0?0:x>1?1:x, ease=x=>{x=cl(x);return 1-Math.pow(1-x,3)};
const back=x=>{x=cl(x);const c1=1.70158,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2)};
const EL=[...document.querySelectorAll('[data-in]')];
let rs=7;const rnd=()=>{rs=(rs*16807)%2147483647;return rs/2147483647};
const mk=n=>{let h=[];for(let k=0;k<n;k++)h.push({a:rnd()*Math.PI*2,r:160+rnd()*360,s:.5+rnd()*1.1,c:HC[k%HC.length],d:rnd()*.15});return h};
const HB=BURSTS.map(()=>mk(24));
function hp(x,y,s){return `<path transform="translate(${x},${y}) scale(${s})" d="M0 18S-18 7-18-5c0-6 4-10 9-10 4 0 7 2 9 6 2-4 5-6 9-6 5 0 9 4 9 10C18 7 0 18 0 18z"/>`}
function burstAt(hs,cx,cy,p){let s='';if(p<=0||p>=1)return s;hs.forEach(h=>{const q=ease((p-h.d)/(1-h.d));if(q<=0)return;const x=cx+Math.cos(h.a)*h.r*q,y=cy+Math.sin(h.a)*h.r*q-q*140;s+=`<g fill="${h.c}" opacity="${1-q}">${hp(x,y,h.s*2.2)}</g>`});return s}
window.render=function(t){
 EL.forEach(e=>{const a=+e.dataset.in,b=e.dataset.out?+e.dataset.out:999,k=e.dataset.a||'fade',base=e.dataset.base||'';
  const dur=k==='stamp'?.28:k==='slideR'||k==='slideL'?.55:.4;
  const pi=ease((t-a)/dur), po=ease((t-b)/.3);
  if(t<a||t>b+.3){e.style.opacity=0;return}
  let o=Math.min(pi,1-po), tr='';
  if(k==='fade')tr=`translateY(${(1-pi)*40}px)`;
  else if(k==='fadeD')tr=`translateY(${(1-pi)*-30}px)`;
  else if(k==='pop')tr=`scale(${.6+.4*back((t-a)/.45)})`;
  else if(k==='slideR')tr=`translateX(${(1-pi)*820}px) rotate(${(1-pi)*12}deg)`;
  else if(k==='slideL')tr=`translateX(${(1-pi)*-820}px) rotate(${(1-pi)*-12}deg)`;
  else if(k==='stamp'){tr=`scale(${1.6-.6*pi})`;o=Math.min(cl((t-a)/.12),1-po)}
  else if(k==='none'){o=1-po}
  e.style.opacity=o;e.style.transform=tr+' '+base});
 let s='';BURSTS.forEach(([t0,x,y],i)=>{s+=burstAt(HB[i],x,y,(t-t0)/1.1)});document.getElementById('burst').innerHTML=s;
};
render(0);
</script>"""

CSS = """<style>
body{background:linear-gradient(170deg,#fff7f4,#fde3ec)}
.dots{position:absolute;inset:0;background-image:radial-gradient(#f6c9d6 2.2px,transparent 2.6px);background-size:46px 46px;opacity:.55}
[data-in]{position:absolute;opacity:0}
.kick{font:700 30px Bit;letter-spacing:.14em;color:#c8325f;text-transform:uppercase;display:flex;align-items:center;gap:14px;white-space:nowrap}
.pillk{background:#c8325f;color:#fff;border-radius:999px;padding:6px 18px;font:700 26px Bit;letter-spacing:.14em}
.cap{left:90px;width:770px;text-align:center;font:700 54px/1.1 Lo;color:#062a55;letter-spacing:-.01em}
.cap i{font-style:italic;font-weight:600;color:#c8325f}
.tab{display:flex;align-items:center;gap:16px;background:#fff;border-radius:999px;padding:12px 30px 12px 14px;box-shadow:0 10px 26px rgba(6,42,85,.16);white-space:nowrap}
.tab .pre{background:#c8325f;color:#fff;border-radius:999px;padding:6px 18px;font:700 24px Bit;letter-spacing:.12em}
.tab .nm{font:58px/1 Cap;color:#062a55}.tab .br{font:600 28px Bit;color:#062a55}
.mat{border-radius:30px;border:14px solid #fff;background-size:cover;background-position:center;box-shadow:0 24px 60px rgba(6,40,90,.28)}
.rk{display:flex;align-items:center;gap:18px;margin-top:10px}.rk img{width:220px;height:42px;object-fit:contain}.rk span{font:600 25px Bit;color:#062a55;text-align:left;white-space:nowrap}
.rkl{font:700 24px Bit;letter-spacing:.16em;color:#c8325f;text-transform:uppercase}
.mstamp{border:8px solid #c8325f;color:#c8325f;background:rgba(255,255,255,.9);font:700 84px Lo;letter-spacing:.08em;padding:0 24px;border-radius:16px}
.mm{background:#062a55;color:#f7b6c8;border-radius:40px;padding:44px 50px 46px;text-align:center;box-shadow:0 24px 60px rgba(6,40,90,.3)}
.mm .s{font:italic 500 52px Lo;opacity:.9}.mm .b{font:700 92px/1.04 Lo;margin-top:10px;color:#fff}.mm .b i{color:#f7b6c8;font-weight:600}
.mm .who{display:flex;align-items:center;justify-content:center;gap:14px;margin-top:26px;font:600 32px Bit;color:#f7b6c8}
.mm .who span{width:62px;height:62px;border-radius:50%;background:#f7b6c8 url(FLAME) center/62% no-repeat}
.bub{background:#fff;border:6px solid #062a55;border-radius:48px;padding:34px 40px 40px;text-align:center;box-shadow:0 16px 40px rgba(6,40,90,.16)}
.bub .q{display:inline-block;background:#c8325f;color:#fff;font:700 28px Bit;letter-spacing:.14em;border-radius:99px;padding:6px 22px;margin-bottom:16px}
.bub .b{font:700 84px/1.04 Lo;color:#062a55}.bub .b i{color:#c8325f;font-weight:600}.bub .s{font:italic 44px Pf;color:#062a55;margin-top:14px}
#burst{position:absolute;inset:0;pointer-events:none;z-index:50}
</style>""".replace('FLAME', u('assets/brand/flame-heart.png'))


def header(ep_kicker, name, by, pills, col, tile, t_in, finale=False):
    """Persistent header: kicker + profile row. Lives in x 90-900, y 200-470."""
    fin = '<span class="pillk" style="background:#062a55">FINALE</span>' if finale else ''
    pl = ''.join(f'<span style="background:#fff;color:#062a55;border-radius:999px;padding:8px 20px;font:600 26px Bit;box-shadow:0 4px 12px rgba(6,42,85,.08);white-space:nowrap">{p}</span>' for p in pills)
    return (f'<div data-in="{t_in}" data-a="fadeD" class="kick" style="left:90px;width:810px;top:200px;justify-content:center">'
            f'<img src="{u("assets/brand/flame-heart.png")}" style="width:44px">{ep_kicker}{fin}</div>'
            f'<div data-in="{t_in + .1}" data-a="fadeD" style="left:90px;top:268px;width:810px;display:flex;gap:28px;align-items:center">'
            f'<div style="flex:none;width:190px;height:190px;border-radius:50%;border:10px solid #fff;background:url({u(tile)}) center/cover;box-shadow:0 12px 30px rgba(6,40,90,.22)"></div>'
            f'<div style="text-align:left"><div style="font:700 24px Bit;letter-spacing:.16em;color:#c8325f">NOW MATCHING</div>'
            f'<div style="font:88px/1.02 Cap;color:{col}">{name}</div><div style="font:600 30px Bit;color:#062a55;margin-top:4px">{by}</div>'
            f'<div style="display:flex;gap:10px;margin-top:12px;flex-wrap:nowrap">{pl}</div></div></div>')


def title(pills_top, by, name, col, tile, sub, t_out):
    return (f'<div data-in="-0.2" data-out="{t_out}" data-a="fade" style="left:90px;width:810px;top:300px;display:flex;flex-direction:column;align-items:center;text-align:center">'
            f'<div style="display:flex;gap:12px">{pills_top}</div>'
            f'<div style="font:italic {56 if len(by) < 20 else 46}px Pf;color:#062a55;margin-top:36px;white-space:nowrap">{by}</div>'
            f'<div style="font:170px/1 Cap;color:{col};margin-top:10px">{name}</div>'
            f'<div style="width:500px;height:500px;margin-top:40px;border-radius:50%;border:16px solid #fff;background:url({u(tile)}) center/cover;box-shadow:0 24px 60px rgba(6,40,90,.28)"></div>'
            f'<div style="font:italic 84px Pf;color:#c8325f;margin-top:46px">{sub}</div></div>')


def cap(text, a, b, top=1292):
    return f'<div class="cap" data-in="{a}" data-out="{b}" data-a="fade" style="top:{top}px">{text}</div>'


def mmcard(small, big, a, b, top=600, z=20):
    return (f'<div class="mm" data-in="{a}" data-out="{b}" data-a="pop" data-base="rotate(-1.5deg)" style="left:120px;width:730px;top:{top}px;z-index:{z}">'
            f'<div class="s">{small}</div><div class="b">{big}</div><div class="who"><span></span>The Matchmaker</div></div>')


def matcard(img, pre, nm, br, a, b, racks=None, rack_label='Her racks', stamp_at=None, side='R', top=600, size=480):
    left = 485 - size // 2
    out = (f'<div class="mat" data-in="{a}" data-out="{b}" data-a="slide{side}" style="left:{left}px;top:{top}px;width:{size}px;height:{size}px;background-image:url({u(img)})"></div>'
           f'<div class="tab" data-in="{a + .2}" data-out="{b}" data-a="fadeD" style="left:{left - 40}px;top:{top - 46}px;z-index:5"><span class="pre">{pre}</span><span class="nm">{nm}</span><span class="br">{br}</span></div>')
    if stamp_at is not None:
        out += f'<div class="mstamp" data-in="{stamp_at}" data-out="{b}" data-a="stamp" data-base="rotate(-10deg)" style="left:{left + 20}px;top:{top + 40}px;z-index:6">MATCH</div>'
    if racks:
        rows = ''.join(f'<div class="rk"><img src="{u(f)}"><span>{n}</span></div>' for f, n in racks)
        out += (f'<div data-in="{a + .45}" data-out="{b}" data-a="fade" style="left:110px;top:{top + size + 16}px;width:780px;text-align:left">'
                f'<div class="rkl">{rack_label}</div>{rows}</div>')
    return out


def page(body, bursts, heart_cols):
    return (HEAD + CSS + '<div class="dots"></div>' + body + '<svg id="burst" viewBox="0 0 1080 1920"></svg>'
            + f'<script>const BURSTS={json.dumps(bursts)};const HC={json.dumps(heart_cols)};</script>' + ENGINE + '</body></html>')


# ------------------------------------------------------------------ Ep 6 Pippa
def pippa():
    col = '#e08600'; tile = 'assets/tiles/album/pippa.jpg'; rk = racks_of('pippa')
    HAM, DEL, FRU = MAT('oh-my-mahjong--hampton.webp'), MAT('oh-my-mahjong--delilah.webp'), MAT('middle-main-mahjong--fruit-stand.webp')
    b = []
    b.append(title('<span class="pillk">EPISODE 6</span>', 'Oh My Mahjong', 'Pippa', col, tile, 'Two suitors', 2.05))
    b.append(header('Episode 6 &middot; Two suitors', 'Pippa', 'by Oh My Mahjong', ['sunny yellow', 'coral + mint', 'party girl'], col, tile, 2.4))
    b.append(mmcard("Pippa's at the party.", 'Two suitors <i>walk in&hellip;</i>', 2.45, 4.4))
    b.append(matcard(HAM, 'SUITOR 1', 'Hampton', 'Oh My Mahjong', 4.7, 7.5, rk))
    b.append(cap('&ldquo;Lime, turquoise, garden party. I make your backs <i>pop.</i>&rdquo;', 5.2, 7.5))
    b.append(matcard(DEL, 'SUITOR 2', 'Delilah', 'Oh My Mahjong', 7.8, 10.2, rk))
    b.append(cap('&ldquo;Turquoise and red. I&rsquo;m basically a <i>fiesta.</i>&rdquo;', 8.3, 10.2))
    # Pippa thinks it over
    b.append(f'<div class="bub" data-in="10.5" data-out="12.2" data-a="pop" data-base="rotate(-1.5deg)" style="left:110px;width:750px;top:560px">'
             f'<div class="q">PIPPA</div><div class="b">Garden party <i>or fiesta?</i></div><div class="s">Somebody pour me a margarita.</div></div>')
    for k, (img, nm) in enumerate(((HAM, 'Hampton'), (DEL, 'Delilah'))):
        x = 150 + k * 360
        b.append(f'<div data-in="{10.75 + k * .15}" data-out="12.2" data-a="fade" data-base="rotate({-4 + 8 * k}deg)" style="left:{x}px;top:960px;width:310px;background:#fff;border-radius:22px;padding:12px 12px 16px;box-shadow:0 16px 36px rgba(6,40,90,.2)">'
                 f'<div style="height:286px;border-radius:14px;background:url({u(img)}) center/cover"></div><div style="font:44px/1 Cap;color:#062a55;margin-top:12px">{nm}</div></div>')
    b.append(mmcard('Hold my margarita.', 'I brought the <i>limes.</i>', 12.4, 14.0))
    b.append(matcard(FRU, 'PLUS ONE', 'Fruit Stand', 'Middle &amp; Main', 14.3, 17.2, rk, stamp_at=15.7))
    b.append(cap('&ldquo;Lemons, limes, sunny stripes. I showed up with <i>snacks.</i>&rdquo;', 14.8, 17.2))
    # trio: why choose?
    trio = [(FRU, 'Fruit Stand', 315, 520, 340, 17.5), (HAM, 'Hampton', 135, 935, 290, 17.65), (DEL, 'Delilah', 545, 935, 290, 17.8)]
    for img, nm, x, y, s, a in trio:
        b.append(f'<div data-in="{a}" data-a="pop" style="left:{x}px;top:{y}px;width:{s}px;background:#fff;border-radius:24px;padding:12px 12px 14px;box-shadow:0 16px 36px rgba(6,40,90,.2)">'
                 f'<div style="height:{s - 24}px;border-radius:14px;background:url({u(img)}) center/cover"></div><div style="font:{40 if s < 400 else 48}px/1 Cap;color:#062a55;margin-top:10px">{nm}</div></div>')
        b.append(f'<div class="mstamp" data-in="{a + .55}" data-a="stamp" data-base="rotate(-10deg)" style="left:{x + 18}px;top:{y + 26}px;font-size:{50 if s < 400 else 60}px;border-width:6px;z-index:6">MATCH</div>')
    b.append(cap('Why choose? <i>It&rsquo;s a party.</i>', 18.1, 99))
    bursts = [[15.75, 485, 860], [18.35, 485, 900]]
    html = page(''.join(b), bursts, ['#e08600', '#f3a9c4', '#5fb39a', '#e2604f', '#ffffff', '#062a55'])
    return dict(tag='ep06-pippa', key='06', body=html, secs=20.6, src='ep06-pippa-s2.mp4',
                end=dict(name='Pippa', tile=tile, mat=FRU, code='Code <span style="color:#d6336c">MAHJMATCH</span> at Middle &amp; Main',
                         hook_bg='#e2604f', hook_fg='#fff3e6', hearts=['#fff3e6', '#ffd84d', '#8fd6bd', '#f7b6c8', '#ffffff'], mat_bg='4% 4%/300%'))


# ------------------------------------------------------------------ Ep 13 Coquette
def coquette():
    col = '#c8467a'; tile = 'assets/tiles/album/coquette.jpg'; rk = racks_of('coquette')
    FLE, CHA, MAE = MAT('loveshackfancy--fleur.webp'), MAT('oh-my-mahjong--chantilly.webp'), MAT('middle-main-mahjong--martha-mae-vintage-quilt.webp')
    LACE = RK + RACK_FILE['Middle & Main White Lace Acrylic']
    b = []
    b.append(title('<span class="pillk">EPISODE 13</span><span class="pillk" style="background:#062a55">FINALE</span>', 'LoveShackFancy x Oh My Mahjong', 'Coquette', col, tile, 'Meet the parents', 2.4))
    b.append(header('Episode 13 &middot; Meet the parents', 'Coquette', 'LoveShackFancy x Oh My Mahjong', ['ribbon pink', 'lilac + powder blue', 'romantic'], col, tile, 2.55, finale=True))
    b.append(mmcard("Coquette's bringing a mat home.", 'Meet the <i>parents.</i>', 2.75, 4.3))
    b.append(f'<div class="bub" data-in="4.6" data-out="6.3" data-a="pop" data-base="rotate(-1.5deg)" style="left:110px;width:750px;top:640px">'
             f'<div class="q">THE PARENTS</div><div class="b">So&hellip; who&rsquo;s the <i>lucky mat?</i></div><div class="s">LoveShackFancy &amp; Oh My Mahjong</div></div>')
    b.append(matcard(FLE, 'THE STEADY ONE', 'Fleur', 'LoveShackFancy', 6.6, 9.9, stamp_at=8.3, top=620, size=600))
    b.append(cap('&ldquo;The official pair mat. A garden of <i>pinks.</i>&rdquo;', 7.1, 8.35))
    b.append(cap('Parents: <i>obsessed.</i>', 8.65, 9.9))
    b.append(mmcard('Wait. One more guest.', 'The rack is <i>here.</i>', 10.1, 11.6))
    # White Lace, the #1 rack
    b.append(f'<div class="tab" data-in="11.95" data-out="15.6" data-a="fadeD" style="left:150px;top:560px;z-index:5"><span class="pre">#1 RACK</span><span class="nm">White Lace</span><span class="br">Middle &amp; Main</span></div>')
    b.append(f'<div data-in="11.8" data-out="15.6" data-a="slideL" style="left:125px;top:610px;width:720px;height:620px;border-radius:40px;background:linear-gradient(160deg,#f9c6d4,#ec93ad);box-shadow:0 24px 60px rgba(6,40,90,.22);display:flex;align-items:center;justify-content:center">'
             f'<img src="{u(LACE)}" style="width:660px;transform:rotate(-8deg);filter:drop-shadow(0 18px 22px rgba(6,40,90,.35))"></div>')
    b.append(cap('The one everybody <i>wants.</i>', 12.3, 13.3))
    b.append(mmcard('*wink*', 'Nice <i>rack.</i>', 13.45, 14.55, top=700))
    b.append(cap('Soft, sweet &amp; a little bit <i>extra.</i>', 14.6, 15.6))
    # Her racks (current picks)
    rows = ''.join(f'<div style="display:flex;align-items:center;gap:22px;margin-top:22px"><span style="font:64px/1 Cap;color:#c8325f;width:50px">{i + 1}</span>'
                   f'<img src="{u(f)}" style="width:330px;height:80px;object-fit:contain"><span style="text-align:left;white-space:nowrap"><span style="display:block;font:700 42px/1.05 Lo;color:#062a55">{n}</span>'
                   f'<span style="font:600 26px Bit;color:#c8325f">{BR}</span></span></div>'
                   for i, (f, n, BR) in enumerate([(rk[1][0], 'White Lace', 'Middle &amp; Main'), (rk[0][0], 'Pink Quartz', 'Oh My Mahjong'), (rk[2][0], 'Lilac', 'Bird &amp; Bamboo')]))
    b.append(f'<div data-in="15.85" data-out="18.2" data-a="pop" style="left:110px;top:590px;width:750px;background:#fff;border-radius:40px;padding:36px 40px 44px;box-shadow:0 24px 60px rgba(6,40,90,.2)">'
             f'<div style="font:76px/1 Cap;color:#062a55">Her racks</div>{rows}</div>')
    b.append(cap('White Lace leads. The family <i>follows.</i>', 16.3, 18.2))
    # Happily ever after: her matches, official pair in the middle
    b.append(f'<div data-in="18.45" data-out="23.4" data-a="fadeD" style="left:90px;width:790px;top:560px;text-align:center"><span class="pillk" style="font-size:30px;padding:8px 26px">HAPPILY EVER AFTER</span></div>')
    fan = [(CHA, 'Chantilly', 92, 700, 252, -4, 18.6), (MAE, 'Martha &amp; Mae', 626, 700, 252, 4, 18.9), (FLE, 'Fleur', 351, 660, 268, 0, 18.75)]
    for img, nm, x, y, s, r, a in fan:
        b.append(f'<div data-in="{a}" data-out="23.4" data-a="pop" data-base="rotate({r}deg)" style="left:{x}px;top:{y}px;width:{s}px;background:#fff;border-radius:24px;padding:12px 12px 14px;box-shadow:0 16px 36px rgba(6,40,90,.22);z-index:{3 if s > 260 else 2}">'
                 f'<div style="height:{s - 24}px;border-radius:14px;background:url({u(img)}) center/cover"></div><div style="font:{38 if s > 260 else 34}px/1 Cap;color:#062a55;margin-top:10px;white-space:nowrap">{nm}</div></div>')
    rrow = ''.join(f'<img src="{u(f)}" style="width:230px;height:60px;object-fit:contain">' for f, n in [rk[1], rk[0], rk[2]])
    b.append(f'<div data-in="19.2" data-out="23.4" data-a="fade" style="left:90px;width:790px;top:1060px;text-align:center"><div class="rkl">+ her racks</div><div style="display:flex;justify-content:center;gap:24px;margin-top:10px">{rrow}</div></div>')
    b.append(cap('And they lived happily ever <i>after.</i>', 19.4, 21.25))
    b.append(cap('Some matches are made in heaven. Others are made by the <i>Mahj Matchmaker.</i>', 21.55, 23.4))
    bursts = [[8.35, 485, 900], [18.95, 485, 900], [21.4, 485, 880]]
    html = page(''.join(b), bursts, ['#c8467a', '#f3a9c4', '#a99bd0', '#ffffff', '#062a55', '#9fc3e6'])
    return dict(tag='ep13-coquette', key='13', body=html, secs=23.7, src='ep13-coquette-s2.mp4',
                end=dict(name='Coquette', tile=tile, mat=CHA, code='Code <span style="color:#d6336c">MAHJMATCH</span> at Oh My Mahjong',
                         hook_bg='#c8467a', hook_fg='#fff3f7', hearts=['#fff3f7', '#f7b6c8', '#a99bd0', '#9fc3e6', '#ffffff'], mat_bg='center/cover'))


# ------------------------------------------------------------------ Ep 8 Smith (swipe deck, hotline v12 card design)
def smith():
    tile = 'assets/tiles/album/smith.jpg'; rk = racks_of('smith'); navy = '#1f2a5a'
    cards = [('oh-my-mahjong--hampton.webp', 'Hampton', 'Oh My Mahjong', 'x', 2.6, 6.4, 7.15, 7.65),
             ('oh-my-mahjong--hawthorne.webp', 'Hawthorne', 'Oh My Mahjong', 'm', 7.65, 9.4, 10.15, 10.65),
             ('bam-bird-boutique--vegan-leather-navy.webp', 'Navy Vegan Leather', 'Bam Bird Boutique', 'm', 10.65, 12.4, 13.15, 13.65),
             ('mahjong-moxie--duck-camp.webp', 'Duck Camp', 'Mahjong Moxie', 'm', 13.65, 15.2, 99, 99)]
    rows = ''.join(f'<div style="display:flex;align-items:center;gap:16px;margin-top:6px"><img src="{u(f)}" style="width:220px;height:32px;object-fit:contain"><span style="font:600 25px Bit;color:#062a55;white-space:nowrap">{n}</span></div>' for f, n in rk)
    X = ('<div class="st" style="position:absolute;top:44px;right:44px;transform:rotate(10deg);width:180px;height:180px;border-radius:50%;border:8px solid #062a55;'
         'background:rgba(255,255,255,.92);display:flex;align-items:center;justify-content:center;opacity:0">'
         '<svg width="92" height="92" viewBox="0 0 48 48"><path d="M13 13 L35 35 M35 13 L13 35" stroke="#062a55" stroke-width="7" stroke-linecap="round"/></svg></div>')
    M = ('<div class="st" style="position:absolute;top:56px;left:40px;transform:rotate(-10deg);border:8px solid #c8325f;color:#c8325f;background:rgba(255,255,255,.9);'
         'font:700 88px Lo;letter-spacing:.08em;padding:0 24px;border-radius:16px;opacity:0">MATCH</div>')
    deck = ''
    for i, (img, nm, br, v, a, s, sw0, sw1) in reversed(list(enumerate(cards))):
        deck += (f'<div class="sc" id="c{i}" style="position:absolute;left:0;top:0;width:820px;background:#fff;border-radius:40px;overflow:hidden;box-shadow:0 26px 60px rgba(6,42,85,.20);text-align:left;transform-origin:50% 120%">'
                 f'<div style="width:820px;height:560px;background:url({u(MAT(img))}) center/cover"></div>{X if v == "x" else M}'
                 f'<div style="position:absolute;top:478px;left:34px;width:160px;height:160px;border-radius:50%;background:url({u(tile)}) center/cover;box-shadow:0 0 0 10px #fff,0 10px 24px rgba(0,0,0,.2)"></div>'
                 f'<div style="padding:84px 40px 30px"><div style="font:700 58px/1 Lo;color:#062a55;white-space:nowrap">{nm}</div>'
                 f'<div style="font:600 25px Bit;letter-spacing:.2em;text-transform:uppercase;color:#c8325f;margin-top:10px">{br} &middot; mat</div>'
                 f'<div style="font:600 23px Bit;letter-spacing:.16em;text-transform:uppercase;color:#062a55;margin-top:16px">His racks</div>{rows}</div></div>')
    caps = [[2.6, 4.3, 'Smith is single &amp; ready to <i>mingle.</i>'], [4.3, 6.4, 'First up&hellip; <i>Hampton?</i>'], [6.4, 7.65, 'Gorgeous, just not his type. <i>Next!</i>'],
            [7.65, 9.4, 'Hawthorne. His <i>official pair.</i>'], [9.4, 10.65, 'Obviously a <i>match.</i>'], [10.65, 12.4, 'Tall, dark and <i>tailored.</i>'],
            [12.4, 13.65, 'Swiped <i>right!</i>'], [13.65, 15.2, 'A duck-blind date? <i>Yes please.</i>'], [15.2, 99, 'Three for <i>three!</i>']]
    tl = [[v, a, s, sw0, sw1] for (_, _, _, v, a, s, sw0, sw1) in cards]
    TITLE = title('<span class="pillk">EPISODE 8</span>', 'Oh My Mahjong', 'Smith', navy, tile, 'Swipe right on Smith', 2.4)
    html = (HEAD + CSS + '<div class="dots"></div>' + TITLE +
            f'<div id="deck" style="position:absolute;left:0;top:0;width:1080px;height:1920px;opacity:0">'
            f'<div style="position:absolute;left:90px;width:820px;top:196px;display:flex;align-items:center;justify-content:center;gap:16px">'
            f'<img src="{u("assets/brand/flame-heart.png")}" style="width:58px"><span style="font:700 60px/1 Lo;color:#062a55;white-space:nowrap">{FYM}</span></div>'
            f'<div id="ctr" style="position:absolute;left:90px;width:820px;top:278px;text-align:center;font:600 28px Bit;color:#c8325f;letter-spacing:.14em;text-transform:uppercase">swiping&hellip;</div>'
            f'<div style="position:absolute;left:90px;top:330px;width:820px;height:960px">{deck}</div>'
            f'<div style="position:absolute;left:90px;width:820px;top:1266px;display:flex;justify-content:center;gap:44px">'
            f'<div id="bx" style="width:104px;height:104px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;font:400 64px Bit;color:#062a55;box-shadow:0 8px 20px rgba(0,0,0,.12)">&times;</div>'
            f'<div id="bh" style="width:104px;height:104px;border-radius:50%;background:#f56c8c;display:flex;align-items:center;justify-content:center;box-shadow:0 8px 20px rgba(0,0,0,.12)"><div style="width:58px;height:58px">{HEART_SVG.format(c="#fff")}</div></div></div>'
            f'<div id="cap" class="cap" style="position:absolute;top:1388px;font-size:50px"></div></div>'
            '<svg id="burst" viewBox="0 0 1080 1920"></svg>'
            f'<script>const BURSTS={json.dumps([[9.45, 500, 700], [12.45, 500, 700], [15.25, 500, 700]])};const HC={json.dumps(["#062a55", "#f56c8c", "#9caec2", "#f7b6c8", "#ffffff"])};'
            f'const TL={json.dumps(tl)};const CAPS={json.dumps(caps)};</script>' + ENGINE.replace('render(0);\n</script>', '') + """
const _r=window.render;
window.render=function(t){_r(t);
 const dk=document.getElementById('deck');dk.style.opacity=t<2.45?0:ease((t-2.45)/.35);
 let bx=1,bh=1,lab='swiping&hellip;';const top=TL.findIndex(c=>t<c[4]);const cur=top<0?TL.length-1:top;
 TL.forEach(([v,a,s,w0,w1],i)=>{const el=document.getElementById('c'+i);const st=el.querySelector('.st');
  if(t<w0){const depth=Math.max(0,i-cur-(t>=TL[cur][3]?ease((t-TL[cur][3])/(TL[cur][4]-TL[cur][3])):0));
   el.style.opacity=i<cur?0:Math.max(0,Math.min(1,3-depth));el.style.transform=`translateY(${depth*20}px) scale(${1-depth*.04})`;
   const sk=cl((t-s)/.28);st.style.opacity=t<s?0:Math.min(1,sk*3);st.style.transform=(v==='x'?'rotate(10deg)':'rotate(-10deg)')+` scale(${1.6-.6*ease(sk)})`;
   if(i===cur&&t>=s){const pr=.12*Math.max(0,1-Math.abs((t-s-.15)/.25));if(v==='x')bx=1-pr;else bh=1-pr}
   if(i===cur)lab=t<s?'swiping&hellip;':(v==='x'?'not his type':'it&rsquo;s a match');}
  else if(t<w1){const k=ease((t-w0)/(w1-w0)),dir=v==='x'?-1:1;el.style.opacity=1;el.style.transform=`translateX(${dir*1400*k}px) rotate(${dir*10*k}deg)`;st.style.opacity=1}
  else el.style.opacity=0});
 document.getElementById('ctr').innerHTML=lab;
 document.getElementById('bx').style.transform=`scale(${bx})`;document.getElementById('bh').style.transform=`scale(${bh})`;
 const c=CAPS.find(c=>t>=c[0]&&t<c[1]);const ce=document.getElementById('cap');
 if(c){ce.innerHTML=c[2];const p=ease((t-c[0])/.3);ce.style.opacity=p;ce.style.transform=`translateY(${(1-p)*24}px)`}else ce.style.opacity=0;
};
render(0);
</script></body></html>""")
    return dict(tag='ep08-smith', key='08', body=html, secs=17.6, src='ep08-smith-s2.mp4',
                end=dict(name='Smith', tile=tile, mat=MAT('mahjong-moxie--duck-camp.webp'), code='Code <span style="color:#d6336c">MAHJMATCH</span> at Oh My Mahjong',
                         hook_bg='#1f2a5a', hook_fg='#fff3e6', hearts=['#fff3e6', '#9caec2', '#f7b6c8', '#7fa0d6', '#ffffff'], mat_bg='center/cover'))


EPS = {'pippa': pippa, 'smith': smith, 'coquette': coquette}

if __name__ == '__main__':
    which = sys.argv[1]; stills = '--stills' in sys.argv
    sp = EPS[which]()
    if stills:   # quick look: one frame every 0.5 s
        print(kit.shoot_js(sp['body'], f'{sp["tag"]}-stills', sp['secs'], every=15)); sys.exit()
    src = f'{R}/assets/reels/s2/{sp["src"]}'
    opener = kit.cut(src, f'{WORK}/{sp["tag"]}-opener.mp4', 0, 84)            # S2 opener frames 0-83 (before its fade to white)
    body = kit.shoot_js(sp['body'], f'{sp["tag"]}-body', sp['secs'])
    e = sp['end']
    ends = kit.ending(sp['tag'], e['name'], e['tile'], e['mat'], e['code'], e['hook_bg'], e['hook_fg'], e['hearts'], mat_bg=e['mat_bg'])
    out = f'{R}/assets/reels/s2/{sp["src"].replace(".mp4", "-v2.mp4")}'
    head = kit.xfade(opener, body, f'{WORK}/{sp["tag"]}-head.mp4', 84 / 30 - .2, .2)   # 0.2 s crossfade opener -> episode, no white frames
    kit.concat([head] + ends, out); print(out)
