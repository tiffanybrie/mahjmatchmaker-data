"""FYM Version 1.19 WEBSITE copy (site-app/fym-v119 on fym-site-preview) = the live website copy site-app/fym-v118 r13 (@7817f04d)
+ the 5 Miss Mahjong scalloped acrylic racks (builder/fym_fix_nov10/racks119_missmahjong.py, run on the copy itself: D.racks,
D.tv fin/rt/price, inline 360px thumbnails after the last thumbs*.js tag) + full-size photos on the CDN (the website copy reads the
frozen fym-v100 hd/index.json, so the 5 rack entries are merged into it in the page as 'file:<absolute CDN url>')
+ release119.py (label Version 1.19 + tracking).
Two phases, like site118.py:
  assets : copy <build>/r119/missm-*.webp into <fym-site>/site-app/fym-v119/r119/   (commit + push = FC)
  <FC>   : write <fym-site>/site-app/fym-v119/index.html
Usage: python3 builder/fym_fix_nov10/site119.py <build dir with r119/> <fym-site repo dir> assets|<FC sha>"""
import sys, os, json, re, shutil, subprocess
B, SITE, FC = sys.argv[1:4]
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(H, '..', '..'))
CDN = 'https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@'
OUTD = SITE + '/site-app/fym-v119'; os.makedirs(OUTD + '/r119', exist_ok=True)
S = json.load(open(R + '/config/fym-rack-adds-nov10-missmahjong.json'))
names = [os.path.splitext(os.path.basename(x['img']))[0] for x in S['adds']]
if FC == 'assets':
    for n in names: shutil.copy(f'{B}/r119/{n}.webp', f'{OUTD}/r119/{n}.webp')
    print('site119 assets:', len(names), 'rack photos'); sys.exit()
src = subprocess.run(['git', '-C', SITE, 'show', '7817f04d2c907d1ea0d4fd01d857fa7a3cffb8bf:site-app/fym-v118/index.html'],
                     capture_output=True, text=True, check=True).stdout
tmp = OUTD + '/_tmp'; os.makedirs(tmp + '/hd', exist_ok=True)
open(tmp + '/index.html', 'w').write(src); json.dump({'t': {}, 'r': {}, 'l': {}, 'm': {}}, open(tmp + '/hd/index.json', 'w'))
subprocess.run([sys.executable, H + '/racks119_missmahjong.py', tmp], check=True)
h = open(tmp + '/index.html').read(); shutil.rmtree(tmp)
HDX = {x['key']: f"file:{CDN}{FC}/site-app/fym-v119/r119/{n}.webp" for x, n in zip(S['adds'], names)}
a = re.search(r"HDI=fetch\('(https://cdn\.jsdelivr\.net/gh/tiffanybrie/mahjmatchmaker-data@[0-9a-f]+/site-app/fym-v100/hd/index\.json)'\)\.then\(r=>r\.ok\?r\.json\(\):\{\}\)", h)
assert a and h.count(a.group(0)) == 1
h = h.replace(a.group(0), a.group(0) + f".then(x=>{{x.r=Object.assign(x.r||{{}},{json.dumps(HDX, separators=(',', ':'))});return x;}})/*v119 Miss Mahjong racks HD*/", 1)
open(OUTD + '/index.html', 'w').write(h)
subprocess.run([sys.executable, H + '/release119.py', OUTD + '/index.html'], check=True)
print('site119 index written', len(open(OUTD + '/index.html').read().encode()), 'bytes; hd extra', len(HDX))
