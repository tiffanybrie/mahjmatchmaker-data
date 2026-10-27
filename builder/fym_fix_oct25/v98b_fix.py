"""FYM v98b (still Version 1.2) fixes from independent QA of v98 (Oct 26 ~9pm):
1. Card title: keep the ASSIGNED set colour s.tc, but light colours (contrast < 2 vs the cream card) get a NAVY outline instead of
   a white one, so near-white / pale titles (The Classic, The Empress, Mod Chartreuse, Desert Dreams) stay readable. 2-3 keeps white.
2. Mahjong Register Pearl Scalloped racks (Navy, Capri Blue, Emerald, Sea Glass, Peony Blush) were drawn in a white box (c:false),
   so they rendered ~25% shorter than other racks. Clean cut-outs from the brand's front-view photos (assets/racks/v98/mr/*-pearl.webp,
   checked on white + navy) -> r98b/, HD index file entries, c:true. Gate [97].
Usage: v98b_fix.py <build>"""
import sys, json, os, shutil, re
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read(); R = '/home/claude/mahjmatchmaker-data/assets/racks/v98/mr/'
o = "if(tcLow){/*v98 white outline for light colours*/g.save();g.lineJoin='round';g.strokeStyle='#fff';g.lineWidth=10;"
n = ("if(tcLow){/*v98 white outline for light colours*//*v98b navy outline when very light*/g.save();g.lineJoin='round';"
     "g.strokeStyle=tcVL?'#062a55':'#fff';g.lineWidth=tcVL?7:10;")
if '/*v98b navy outline when very light*/' not in h:
    assert h.count(o) == 1, h.count(o); h = h.replace(o, n)
    o2 = "return /^#[0-9a-f]{6}$/i.test(tc)&&(.8534+.05)/(l+.05)<3;})();"
    assert h.count(o2) == 1
    h = h.replace(o2, o2 + "const tcVL=(()=>{const L_=x=>{const c=parseInt(tc.slice(x,x+2),16)/255;return c<=.03928?c/12.92:Math.pow((c+.055)/1.055,2.4);};"
                  "const l=.2126*L_(1)+.7152*L_(3)+.0722*L_(5);return /^#[0-9a-f]{6}$/i.test(tc)&&(.8534+.05)/(l+.05)<2;})();")
    # the white offset shadow under a very light title only adds glare
    o3 = "g.fillStyle='rgba(255,255,255,.9)';g.fillText(l,W/2+4,y+4);if(tcLow)"
    assert h.count(o3) == 1; h = h.replace(o3, "if(!tcVL){g.fillStyle='rgba(255,255,255,.9)';g.fillText(l,W/2+4,y+4);}if(tcLow)")
V = {53016959156536: 'navy', 53016959189304: 'capri-blue', 53016959222072: 'emerald', 53016959254840: 'sea-glass', 53016959287608: 'peony-blush'}
base = 'mahjongregister.com/signature-collection-acrylic-mahjong-racks-set-of-4-20-luxury-tile-holders-copy?v='
os.makedirs(B + '/r98b', exist_ok=True); ix = json.load(open(B + '/hd/index.json')); nc = 0
for vid, nm in V.items():
    k = base + str(vid); f = 'mr-%s-pearl.webp' % nm; shutil.copy(R + f, B + '/r98b/' + f); ix['r'][k] = 'file:r98b/' + f
    pat = '"' + k.replace('?', '\\?') + '":\\{"n":"[^"]*","bn":"Mahjong Register"[^}]*?"c":false'
    m = re.search(pat, h)
    if m: h = h[:m.start()] + m.group(0)[:-len('"c":false')] + '"c":true' + h[m.end():]; nc += 1
json.dump(ix, open(B + '/hd/index.json', 'w'), separators=(',', ':'))
open(P, 'w').write(h); print('v98b: title navy outline; pearl racks c:true', nc)
