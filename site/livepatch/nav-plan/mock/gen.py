# Builds the nav-plan mockup pages (drafts only; nothing here touches the live site).
# Run: python3 gen.py  -> writes header.html, home-launch.html, home-prelaunch.html, shop.html
import os
D = os.path.dirname(os.path.abspath(__file__))
A = '../../../../assets'          # repo assets, relative to this folder
STORE = 'https://www.amazon.com/shop/heritagesig05'
SHOPMY = 'https://shopmy.us/shop/mahjmatchmaker'
FYM = '/find-your-match'

CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=Bitter:ital,wght@0,400;0,600;0,700;1,400&family=Shrikhand&display=swap');
:root{--pink:#f56a8b;--pinkdk:#d6537a;--navy:#1f3a6b;--foot:#013a5b;--blush:#fdf2f5;--sand:#faf5ef;--ink:#1f3a6b}
*{box-sizing:border-box}html,body{margin:0}
body{font-family:'Bitter',Georgia,serif;color:var(--ink);background:#fff;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
.sx{font-family:'Shrikhand',Georgia,serif;font-weight:400}
/* header */
.hd{position:relative;z-index:20;background:#fff;height:132px;display:flex;align-items:center;justify-content:space-between;padding:0 4.4vw;border-bottom:1px solid #f3e3e8}
.hd .logo img{height:72px;display:block}
.nav{display:flex;align-items:center;gap:30px;font-size:16.5px;color:var(--pink)}
.nav .it{position:relative;display:flex;align-items:center;gap:6px;padding:10px 0}
.nav .it .car{font-size:10px;opacity:.8;transform:translateY(1px)}
.nav .it.on{color:var(--pinkdk)}
.nav .it.on::after{content:"";position:absolute;left:0;right:0;bottom:2px;height:1.5px;background:var(--pink)}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;background:var(--pink);color:#fff;font-family:'Bitter',serif;font-size:16px;font-weight:600;border-radius:9px;padding:14px 26px;box-shadow:0 2px 0 rgba(0,0,0,.04)}
.btn.navy{background:var(--navy)}
.btn.ghost{background:#fff;color:var(--navy);border:2px solid var(--navy)}
.hd .cta{padding:12px 20px;font-size:15.5px;margin-left:6px}
.hd .cta .h{font-size:13px}
.drop{position:absolute;top:44px;left:-18px;min-width:230px;background:#fff;border-radius:6px;box-shadow:0 10px 30px rgba(31,58,107,.14);padding:12px 0;font-size:15.5px;color:var(--pink)}
.drop a{display:block;padding:7px 22px;white-space:nowrap}
.drop a.b{color:var(--navy);font-weight:600}
.drop a.soon{color:#b9a8b0;font-style:italic}
.drop .sep{height:1px;background:#f3e3e8;margin:7px 18px}
.drop .lab{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:#9aa5bb;padding:6px 22px 3px}
.burger{width:36px;display:flex;flex-direction:column;gap:9px}.burger i{display:block;height:2px;background:var(--pink)}
.mpill{display:none}
.hd .burger{display:none}
/* hero */
.hero{position:relative;overflow:hidden;background:url(A/hero/loveshackfancy-coquette-fleur-mat-hero.jpg) center/cover}
.hero.launch{background:radial-gradient(circle at 74% 56%,#fbe3ea 0 36%,transparent 36.2%),radial-gradient(circle at -4% 104%,#fbe3ea 0 20%,transparent 20.2%),#faf3ea}
.hero.launch::before{display:none}
.hero.launch h1 em{font-style:normal;color:#054689}
.hero.launch .eyebrow{background:#054689}
.hero.launch .fan{height:600px}.hero.launch .fan .c{width:330px}
.hero.launch .itsamatch{top:-22px}
.hero.launch .swipes{bottom:-30px}
.hero::before{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(255,255,255,.80) 0%,rgba(255,255,255,.62) 46%,rgba(255,255,255,.18) 100%)}
.hero .in{position:relative;display:grid;grid-template-columns:1.05fr .95fr;align-items:center;gap:30px;max-width:1180px;margin:0 auto;padding:64px 56px 70px;min-height:640px}
.eyebrow{display:inline-flex;align-items:center;gap:8px;background:var(--navy);color:#fff;font-size:12.5px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;border-radius:99px;padding:8px 15px}
.eyebrow .dot{width:7px;height:7px;border-radius:50%;background:var(--pink)}
.hero h1{font-family:'Shrikhand',serif;font-weight:400;color:var(--pink);font-size:86px;line-height:1.02;margin:20px 0 14px;letter-spacing:-.5px;text-shadow:0 2px 0 #fff}
.hero p.lede{font-size:21px;line-height:1.5;color:var(--navy);margin:0 0 26px;max-width:480px}
.hero .ctas{display:flex;align-items:center;gap:22px;flex-wrap:wrap}
.hero .ctas .btn{font-size:18px;padding:17px 34px}
.hero .ctas .tl{color:var(--navy);font-weight:600;font-size:16px;border-bottom:2px solid var(--pink);padding-bottom:2px}
.coupon{margin-top:26px;font-size:15px;color:var(--navy);background:rgba(255,255,255,.85);display:inline-block;border-radius:10px;padding:10px 14px}
.coupon b{letter-spacing:.06em}
.fan{position:relative;height:520px}
.fan .c{position:absolute;top:10px;left:50%;width:300px;border-radius:16px;overflow:hidden;box-shadow:0 18px 40px rgba(31,58,107,.28);border:6px solid #fff;background:#fff}
.fan .c img{display:block;width:100%}
.fan .c1{transform:translateX(-50%) translateX(-118px) rotate(-11deg) scale(.88);top:40px}
.fan .c2{transform:translateX(-50%) translateX(118px) rotate(10deg) scale(.88);top:40px}
.fan .c3{transform:translateX(-50%) rotate(-1.5deg)}
.fan .stamp{position:absolute;z-index:3;top:-8px;right:12%;width:124px;height:124px;border-radius:50%;background:var(--navy);color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;transform:rotate(9deg);box-shadow:0 8px 20px rgba(31,58,107,.3);border:4px solid #fff}
.fan .stamp small{font-size:11px;letter-spacing:.18em;text-transform:uppercase;font-weight:700}
.fan .stamp b{font-family:'Shrikhand',serif;font-weight:400;font-size:34px;line-height:1;color:var(--pink)}
.swipes{position:absolute;z-index:3;left:50%;bottom:-6px;transform:translateX(-50%);display:flex;gap:26px}
.swipes span{width:66px;height:66px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;font-size:30px;box-shadow:0 8px 20px rgba(31,58,107,.22)}
.swipes .no{color:#9aa5bb}.swipes .yes{color:var(--pink)}
.itsamatch{position:absolute;z-index:4;left:50%;top:6px;transform:translate(-50%,-50%) rotate(-5deg);font-family:'Shrikhand',serif;font-size:30px;color:#fff;background:var(--pink);padding:6px 20px 10px;border-radius:12px;box-shadow:0 8px 20px rgba(214,83,122,.4);white-space:nowrap}
.signup{display:flex;gap:10px;max-width:470px;margin-top:4px}
.signup input{flex:1;min-width:0;font:inherit;font-size:16px;border:2px solid #f2c6d3;background:#fff;border-radius:9px;padding:15px 16px;color:var(--navy)}
.signup .btn{font-size:16.5px;padding:15px 24px;white-space:nowrap}
.fine{font-size:13.5px;color:#55688c;margin-top:10px}
.blur .c img{filter:saturate(.9)}
/* albums */
.albums{padding:64px 4vw 70px;text-align:center}
.albums h2{font-family:'Shrikhand',serif;font-weight:400;font-size:40px;color:var(--navy);margin:0 0 8px}
.albums .sub{color:#3f5a8a;font-size:17px;margin:0 auto 28px;max-width:620px;line-height:1.5}
.strip{display:grid;grid-template-columns:repeat(6,1fr);gap:18px;max-width:1180px;margin:0 auto}
.strip .a img{width:100%;aspect-ratio:1;object-fit:cover;border-radius:10px;display:block}
.strip .a{position:relative}
.strip .a .new{position:absolute;top:8px;left:8px;background:#c84d75;color:#fff;font-size:11px;font-weight:700;letter-spacing:.1em;border-radius:99px;padding:5px 9px}
.strip .br{font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;color:#c84d75;font-weight:600;margin-top:12px}
.strip .nm{font-size:16.5px;font-weight:600;color:var(--navy);margin-top:4px}
.albums .more{margin-top:30px}
.rest{background:repeating-linear-gradient(45deg,#faf5ef,#faf5ef 14px,#f6eee6 14px,#f6eee6 28px);text-align:center;color:#8a7d75;font-size:14px;padding:26px 16px;font-style:italic}
/* footer */
.ft{position:relative;background:var(--foot);color:#fff;padding:70px 6vw 34px}
.ft::before{content:"";position:absolute;left:0;right:0;top:-38px;height:40px;background:var(--foot);clip-path:path('M0 30 C 300 0, 600 0, 960 34 S 1600 20, 2000 10 L 2000 40 L 0 40 Z')}
.ft .row{display:grid;grid-template-columns:1fr 1fr 1fr;align-items:start;text-align:center;max-width:1180px;margin:0 auto}
.ft .nm{font-family:'Shrikhand',serif;font-size:24px}
.ft .links{margin-top:16px;font-size:15.5px}.ft .links a{text-decoration:underline;text-underline-offset:3px}.ft .links .pipe{opacity:.7;margin:0 8px}
.ft .soc{display:flex;gap:18px;justify-content:center;font-size:24px;margin-top:6px}
.ft .soc svg{width:26px;height:26px;fill:none;stroke:#fff;stroke-width:2}
.ft .em{font-family:'Shrikhand',serif;font-size:22px;word-break:break-all}
.ft .disc{max-width:1180px;margin:34px auto 0;border-top:1px solid rgba(255,255,255,.22);padding-top:18px;text-align:center;font-size:13.5px;color:rgba(255,255,255,.82)}
.ft .new{outline:2px dashed #ffd36b;outline-offset:6px;border-radius:4px}
.newtag{display:inline-block;background:#ffd36b;color:#5a4300;font-size:11px;font-weight:700;letter-spacing:.08em;border-radius:99px;padding:2px 8px;margin-left:8px;vertical-align:2px}
/* shop page */
.shop{background:var(--sand)}
.shop .top{text-align:center;padding:64px 6vw 40px;max-width:860px;margin:0 auto}
.shop h1{font-family:'Shrikhand',serif;font-weight:400;font-size:62px;color:var(--pink);margin:0 0 12px;line-height:1.05}
.shop .top p{font-size:19px;line-height:1.55;color:var(--navy);margin:0 auto 26px;max-width:640px}
.shop .top .btns{display:flex;gap:14px;justify-content:center;flex-wrap:wrap}
.shop .tiny{font-size:13.5px;color:#55688c;margin-top:14px}
.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:22px;max-width:1180px;margin:0 auto;padding:10px 4vw 60px}
.card{background:#fff;border-radius:14px;overflow:hidden;box-shadow:0 6px 22px rgba(31,58,107,.08);display:flex;flex-direction:column}
.card img{width:100%;aspect-ratio:1;object-fit:cover;display:block}
.card .bd{padding:18px 20px 20px;display:flex;flex-direction:column;gap:6px;flex:1}
.card h3{font-family:'Shrikhand',serif;font-weight:400;font-size:23px;color:var(--navy);margin:0}
.card p{margin:0;font-size:15px;line-height:1.5;color:#3f5a8a}
.card .go{margin-top:auto;padding-top:10px;color:var(--pink);font-weight:700;font-size:15px}
.see{font-size:30px}
.band{background:var(--blush);text-align:center;padding:46px 6vw 52px}
.band h2{font-family:'Shrikhand',serif;font-weight:400;color:var(--navy);font-size:34px;margin:0 0 10px}
.band p{font-size:17px;color:var(--navy);margin:0 auto 22px;max-width:600px;line-height:1.5}
.band .code{display:inline-block;font-weight:700;letter-spacing:.08em;background:#fff;border:2px dashed var(--pink);border-radius:10px;padding:3px 10px;color:var(--pinkdk)}
/* mobile menu overlay */
.mm{position:relative;background:#fff;min-height:844px;display:flex;flex-direction:column}
.mm .hd{border:0}
.mm .list{flex:1;display:flex;flex-direction:column;align-items:center;gap:6px;padding:26px 0 0;font-size:27px;color:var(--pink)}
.mm .list a{padding:9px 0;display:flex;align-items:center;gap:10px}
.mm .list a .car{font-size:18px;opacity:.75}
.mm .back{align-self:flex-start;margin:0 0 4px 26px;font-size:18px;color:var(--navy);opacity:.75}
.mm .list.sub{font-size:21px;gap:0}
.mm .list.sub a{padding:7px 0}
.mm .list.sub a.b{color:var(--navy);font-weight:600}
.mm .list.sub a.soon{color:#b9a8b0;font-style:italic}
.mm .list.sub .lab{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:#9aa5bb;margin:10px 0 2px}
.mm .foot{padding:22px 24px 40px}
.mm .foot .btn{width:100%;font-size:19px;padding:18px}
.x{width:30px;height:30px;position:relative}.x::before,.x::after{content:"";position:absolute;left:0;right:0;top:14px;height:2px;background:var(--pink);transform:rotate(45deg)}.x::after{transform:rotate(-45deg)}
.note{position:absolute;z-index:50;background:#fff8e1;border:1.5px solid #ffd36b;color:#5a4300;font-size:12.5px;line-height:1.35;border-radius:8px;padding:6px 9px;max-width:230px;font-family:'Bitter',serif;box-shadow:0 4px 12px rgba(0,0,0,.08)}

@media (max-width:760px){
 .hd{height:96px;padding:0 22px}
 .hd .logo img{height:40px}
 .nav{display:none}
 .hd .burger{display:flex}
 .mpill{display:inline-flex;font-size:12.5px;padding:9px 12px;border-radius:99px;margin-right:14px;white-space:nowrap}
 .burger{width:30px}
 .hd .rt{display:flex;align-items:center}
 .hero{background-position:60% center}
 .hero::before{background:linear-gradient(180deg,rgba(255,255,255,.82) 0%,rgba(255,255,255,.7) 55%,rgba(255,255,255,.35) 100%)}
 .hero .in{grid-template-columns:1fr;padding:30px 22px 40px;min-height:0;gap:6px;text-align:center}
 .hero h1{font-size:58px;margin:16px 0 10px}
 .hero p.lede{font-size:18px;margin:0 auto 20px}
 .hero .ctas{flex-direction:column;gap:14px}
 .hero .ctas .btn{width:100%;font-size:18px}
 .coupon{font-size:14px;margin-top:18px}
 .fan{height:400px;margin-top:10px}
 .fan .c{width:210px;border-width:4px}
 .fan .c1{transform:translateX(-50%) translateX(-78px) rotate(-11deg) scale(.86);top:34px}
 .fan .c2{transform:translateX(-50%) translateX(78px) rotate(10deg) scale(.86);top:34px}
 .fan .stamp{width:96px;height:96px;right:2%;top:-4px}.fan .stamp b{font-size:26px}
 .swipes span{width:56px;height:56px;font-size:26px}
 .itsamatch{font-size:24px}
 .signup{flex-direction:column;margin:0 auto}
 .signup .btn{width:100%}
 .albums{padding:46px 16px 50px}.albums h2{font-size:31px}.albums .sub{font-size:16px}
 .strip{grid-template-columns:repeat(2,1fr);gap:14px}
 .strip .a:nth-child(n+5){display:none}
 .ft{padding:60px 22px 30px}.ft .row{grid-template-columns:1fr;gap:26px}
 .shop .top{padding:42px 22px 28px}.shop h1{font-size:46px}.shop .top p{font-size:17px}
 .shop .top .btns .btn{width:100%}
 .grid{grid-template-columns:1fr 1fr;gap:14px;padding:6px 16px 44px}
 .card .bd{padding:12px 13px 14px}.card h3{font-size:18px}.card p{font-size:13.5px}.card .go{font-size:14px}
 .see{font-size:22px}
 .band{padding:38px 22px 44px}.band h2{font-size:28px}
}
""".replace('url(A/', 'url(' + A + '/')

SOC = ('<svg viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".6"/></svg>'
       '<svg viewBox="0 0 24 24"><path d="M14 8h3V4h-3a4 4 0 0 0-4 4v3H7v4h3v7h4v-7h3l1-4h-4V8.5c0-.3.2-.5.5-.5z"/></svg>'
       '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M11 8c3-1 6 1 5 4s-4 3-5 1M11 9l-2 10"/></svg>')

MATCHES = [('All Tile Albums', '/mahjong-tile-matches'), ('Holiday Matches', '/holiday-mahjong-matches'),
           ('Pink Tiles', '/pink-mahjong-tile-matches'), ('Red Tiles', '/red-mahjong-tile-matches'), ('Purple Tiles', '/purple-mahjong-tile-matches'),
           ('Blue Tiles', '/blue-mahjong-tile-matches'), ('Green Tiles', '/green-mahjong-tile-matches'), ('Yellow & Orange Tiles', '/yellow-orange-mahjong-tile-matches'),
           ('Brown Tiles', '/brown-mahjong-tile-matches'), ('Ivory Tiles', '/ivory-mahjong-tile-matches'), ('Neutral Tiles', '/neutral-mahjong-tile-matches'),
           ('Masculine Sets', '/masculine-mahjong-tile-matches'), ('Mat Gallery (later)', '#', 'soon')]
COMMUNITY = [('About Tiffany', '/about'), ('Community', '/mahj-matchmaker-community'), ('Facebook Group', 'https://www.facebook.com/groups/mahjmatchmaker'),
             ('Share Your Table', '/share-your-table'), ('Request an Album', '/request-an-album')]


def drop(items):
    out = []
    for t in items:
        if t[0] == 'sep': out.append('<div class="sep"></div>')
        elif t[0] == 'lab': out.append(f'<div class="lab">{t[1]}</div>')
        else: out.append(f'<a class="{t[2] if len(t) > 2 else ""}" href="{t[1]}">{t[0].replace("&", "&amp;")}</a>')
    return '<div class="drop">' + ''.join(out) + '</div>'


def header(open_=None, pill=True):
    m = drop(MATCHES) if open_ == 'matches' else ''
    c = drop(COMMUNITY) if open_ == 'community' else ''
    return f'''<header class="hd"><a class="logo" href="/"><img src="img/logo.png" alt="Mahj Matchmaker"></a>
<nav class="nav"><div class="it{' on' if m else ''}">Mahjong Matches <span class="car">&#9662;</span>{m}</div><div class="it">Discount Codes</div><div class="it">Blog</div><div class="it">Shop</div><div class="it{' on' if c else ''}">Community <span class="car">&#9662;</span>{c}</div>
<a class="btn cta" href="{FYM}"><span class="h">&#9829;</span> Find your match</a></nav>
<div class="rt">{'<a class="btn mpill" href="'+FYM+'">Find your match</a>' if pill else ''}<div class="burger mob"><i></i><i></i></div></div></header>'''


FOOT = f'''<footer class="ft"><div class="row">
<div><div class="nm">Mahj Matchmaker</div><div class="links"><a href="/private-mahjong-lessons">Private Lessons</a><span class="pipe">|</span><a href="/rentals">Rentals</a></div></div>
<div><div class="soc">{SOC}</div></div>
<div><div class="em">mahjmatchmaker@gmail.com</div></div></div>
<div class="disc new">As an Amazon Associate I earn from qualifying purchases.<span class="newtag">NEW</span></div></footer>'''

ALB = [('papaya-spritz', 'Papaya Spritz', 'Oh My Mahjong'), ('coquette', 'Coquette', 'LoveShackFancy x OMM'), ('seabreeze', 'Seabreeze', 'Oh My Mahjong'),
       ('talulah', 'Talulah', 'Oh My Mahjong'), ('osler', 'Osler', 'Oh My Mahjong'), ('smith', 'Smith', 'Oh My Mahjong')]
ALBUMS = '''<section class="albums"><h2>New Tile Match Albums</h2><p class="sub">The newest tile sets I've matched with mats and racks, updated as each new album goes live.</p><div class="strip">''' + ''.join(
    f'<a class="a" href="/{s}-mahjong-tile-matches"><span class="new">NEW</span><img src="{A}/covers/albums/w800/00-{s}-mahjong-tiles-cover.jpg" alt=""><div class="br">{b}</div><div class="nm">{n}</div></a>' for s, n, b in ALB) + \
    '</div><div class="more"><a class="btn navy" href="/mahjong-tile-matches">See all tile match albums</a></div></section>'
REST = '<div class="rest">Rest of the homepage stays as it is today: Holiday Mahjong Matches, Shop by Color, All Albums by Color, Shop the Guides, Shop by Brand, How It Works, coupon band.</div>'


def page(title, body):
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>{CSS}</style></head><body>{body}</body></html>'


FAN = '''<div class="fan">{stamp}<div class="c c1"><img src="img/card-coquette.jpg" alt=""></div><div class="c c2"><img src="img/card-heritage2.jpg" alt=""></div><div class="c c3"><img src="img/card-papaya.jpg" alt="Papaya Spritz tiles on the Press for Mahjong mat"></div>{extra}<div class="swipes"><span class="no">&#10005;</span><span class="yes">&#9829;</span></div></div>'''

launch = page('Home - launch day (draft)', header() + f'''<section class="hero launch"><div class="in"><div>
<span class="eyebrow"><span class="dot"></span>New &middot; Find Your Mat-ch</span>
<h1>Find <em>Your</em> Mat-ch&trade; is here</h1>
<p class="lede">Start with your tiles or your mat and swipe your perfect match.</p>
<div class="ctas"><a class="btn" href="{FYM}">Start swiping</a><a class="tl" href="/mahjong-tile-matches">or browse the albums</a></div>
<div class="coupon">Use code <b>MAHJMATCH</b> to save at 30+ partner brands</div>
</div>{FAN.format(stamp='', extra='<div class="itsamatch">It&rsquo;s a mat-ch!</div>')}</div></section>''' + ALBUMS + REST + FOOT)

pre = page('Home - pre-launch (draft)', header() + f'''<section class="hero"><div class="in"><div>
<span class="eyebrow"><span class="dot"></span>Coming 10.27</span>
<h1>Find your match.</h1>
<p class="lede">Pick your tiles, then swipe through mats and racks that match them. Opens Tuesday, October 27.</p>
<form class="signup" onsubmit="return false"><input placeholder="Email address" aria-label="Email address"><button class="btn">Save my spot</button></form>
<div class="fine">I'll email you the minute it opens. Until then, <a href="/mahjong-tile-matches" style="border-bottom:2px solid var(--pink);font-weight:600">browse the albums</a>.</div>
</div>{FAN.format(stamp='<div class="stamp"><small>Opens</small><b>10.27</b></div>', extra='')}</div></section>''' + ALBUMS + REST + FOOT)

CARDS = [('cover-holiday-mahjong-tables.jpg', 'Holiday Mahjong Tables', 'Three holiday table looks, budget friendly.'),
         ('cover-polo-club-holiday.jpg', 'Polo Club Holiday', 'Tartan, brass lamps and cognac leather.'),
         ('cover-retro-rattan-holiday.jpg', 'Retro Rattan Holiday', 'Red plaid, a ceramic tree and amber glass.'),
         ('cover-rackin-rudolph.jpg', "Rackin' Rudolph", 'Santa red, gold bows and a reindeer dice box.'),
         ('cover-dice-dishes.jpg', 'Dice Dishes', 'Cute spots for your dice.'),
         ('cover-mahjong-table-lamps.jpg', 'Table Lamps', 'Cordless glow for game night.')]
cards = ''.join(f'<a class="card" href="{STORE}"><img src="{A}/amazon-store/{f}" alt=""><div class="bd"><h3>{t}</h3><p>{d}</p><span class="go">Shop the list &rsaquo;</span></div></a>' for f, t, d in CARDS)
cards += f'<a class="card" href="{STORE}"><img src="img/sweet-jojo.jpg" alt=""><div class="bd"><h3>Affordable Sets</h3><p>Sweet Jojo and other sets that won\'t break the bank.</p><span class="go">Shop the list &rsaquo;</span></div></a>'
cards += f'<a class="card" href="{STORE}" style="background:var(--navy);color:#fff;justify-content:center;text-align:center;padding:30px 22px"><div class="sx see" style="color:#fff;line-height:1.15">See everything</div><p style="color:#dfe6f3;margin:10px 0 18px;font-size:15px">Every idea list, all in one place.</p><span class="btn" style="padding:12px 16px">Amazon storefront</span></a>'

shop = page('Shop My Finds (draft)', header() + f'''<main class="shop"><div class="top">
<h1>Shop My Finds</h1>
<p>The little things that make a mahj table: holiday looks, dice dishes, lamps and sets that won't break the bank.</p>
<div class="btns"><a class="btn" href="{STORE}">Shop my Amazon storefront</a><a class="btn ghost" href="{SHOPMY}">Shop on ShopMy <span style="font-weight:400;font-size:13px;opacity:.7">(later)</span></a></div>
<div class="tiny">As an Amazon Associate I earn from qualifying purchases.</div></div>
<div class="grid">{cards}</div>
<section class="band"><h2>Shopping a partner brand?</h2><p>First date's on us. Use code <span class="code">MAHJMATCH</span> to save 10%.</p><a class="btn navy" href="/mahjong-discount-codes">See all discount codes</a></section>
</main>''' + FOOT)

# header states page: desktop dropdown open (?d=matches|community); mobile menu (?m=1 top, ?m=2 matches panel, ?m=3 community panel)
def mmenu(panel):
    if panel == 'top':
        lst = '<div class="list">' + ''.join(f'<a>{t}{" <span class=car>&rsaquo;</span>" if f else ""}</a>' for t, f in [('Mahjong Matches', 1), ('Discount Codes', 0), ('Blog', 0), ('Shop', 0), ('Community', 1)]) + '</div>'
    else:
        items = MATCHES if panel == 'matches' else COMMUNITY
        h = []
        for t in items:
            if t[0] == 'sep': continue
            if t[0] == 'lab': h.append(f'<div class="lab">{t[1]}</div>'); continue
            h.append(f'<a class="{t[2] if len(t) > 2 else ""}">{t[0].replace("&", "&amp;")}</a>')
        lst = '<div class="back">&lsaquo; Back</div><div class="list sub">' + ''.join(h) + '</div>'
    return f'''<div class="mm"><header class="hd"><a class="logo"><img src="img/logo.png" alt=""></a><div class="x"></div></header>{lst}
<div class="foot"><a class="btn" href="{FYM}">&#9829; Find your match</a></div></div>'''

for name, html in [('home-launch', launch), ('home-prelaunch', pre), ('shop', shop),
                   ('header-matches', page('Header - Mahjong Matches open', header('matches') + '<div style="height:400px;background:#faf5ef"></div>')),
                   ('header-community', page('Header - Community open', header('community') + '<div style="height:300px;background:#faf5ef"></div>')),
                   ('menu-top', page('Mobile menu', mmenu('top'))), ('menu-matches', page('Mobile menu - Matches', mmenu('matches'))),
                   ('menu-community', page('Mobile menu - Community', mmenu('community'))), ('footer', page('Footer', '<div style="height:60px;background:#f56a8b"></div>' + FOOT))]:
    open(os.path.join(D, name + '.html'), 'w').write(html)
print('ok')
