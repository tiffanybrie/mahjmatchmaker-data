"""v5 (Nov 3): rebuild EVERY render input from scratch (the /dev/shm dirs vanish on a container restart).
python3 v5_prep.py [all|data|wall|tiles|brand|logos]  -> /dev/shm/introv2 (app data, mats, hd), /dev/shm/introv3 (wall, tiles, brand), /dev/shm/introv4 (logos)
Recordings: then run v4_capture.py rec0 (v3_capture.py rec0) / recA / recB, and v5_cards.py."""
import json, os, re, subprocess, sys, random, collections, concurrent.futures as cf
R = '/home/claude/mahjmatchmaker-data'; B = f'{R}/assets/social/holiday-nov1/intro/build'
W2, W3, W4 = '/dev/shm/introv2', '/dev/shm/introv3', '/dev/shm/introv4'
for d in [f'{W2}/fym', f'{W2}/tmp', f'{W2}/dbg', f'{W2}/hd', f'{W2}/mats', f'{W3}/wall', f'{W3}/tiles', f'{W3}/brand', f'{W4}/logos', f'{W4}/xc']:
    os.makedirs(d, exist_ok=True)
run = lambda *a, **k: subprocess.run(a, check=True, **k)
WHAT = sys.argv[1] if len(sys.argv) > 1 else 'all'
def dims(f): return [int(x) for x in subprocess.run(['identify', '-format', '%w %h', f + '[0]'], capture_output=True, text=True).stdout.split()]
if WHAT in ('all', 'data'):
    open(f'{W2}/fym/index.html', 'wb').write(subprocess.run(['git', '-C', R, 'show', '3c0b8ceb:site-app/fym-v113/index.html'], capture_output=True, check=True).stdout)
    h = open(f'{W2}/fym/index.html', encoding='utf8').read(); i = h.index('const D=') + 8
    dep = 0; ins = False; esc = False; q = ''
    for j in range(i, len(h)):
        c = h[j]
        if ins:
            if esc: esc = False
            elif c == '\\': esc = True
            elif c == q: ins = False
        elif c in '"\'': ins = True; q = c
        elif c == '{': dep += 1
        elif c == '}':
            dep -= 1
            if dep == 0: break
    open(f'{W2}/D.js', 'w').write('process.stdout.write(JSON.stringify(' + h[i:j + 1] + '))')
    open(f'{W2}/D.json', 'w').write(subprocess.run(['node', f'{W2}/D.js'], capture_output=True, text=True).stdout)
    run('convert', f'{R}/assets/mats/soiree-all-day/color-me-merry-mahjong-mat.jpg', '-fuzz', '6%', '-trim', '+repage', f'{W2}/cmm-trim.jpg')
    subprocess.run(['python3', f'{B}/v2_stock.py'], capture_output=True)
    run('python3', f'{B}/v3_capture.py', 'mats', capture_output=True)
    run('python3', f'{B}/v2_hd.py', capture_output=True)
    m = json.load(open(f'{W2}/mats/map.json'))
    j = json.loads(subprocess.run(['curl', '-sS', '-A', 'Mozilla/5.0', 'https://sundaymahjong.com/products/festive-plaid-premium-mahjong-mat.json'], capture_output=True, text=True).stdout)['product']
    run('curl', '-sS', '-A', 'Mozilla/5.0', '-o', f'{W2}/hd/fp.src', j['images'][0]['src'] + '&width=1600')
    run('convert', f'{W2}/hd/fp.src[0]', '-quality', '92', f'{W2}/hd/fp.jpg')
    m['sundaymahjong.com/festive-plaid-premium-mahjong-mat'] = [f'{W2}/hd/fp.jpg', 'Festive Plaid Premium', 'Sunday Mahjong', 888]
    json.dump(m, open(f'{W2}/mats/map.json', 'w'), indent=1); print('data ok', len(m))
if WHAT in ('all', 'wall'):  # mat wall: trimmed, square-ish, >=360px, max 6 per brand, 66 cells
    m = json.load(open(f'{W2}/mats/map.json'))
    def prep(item):
        k, (fn, n, bn, *_) = item
        if n == 'Color Me Merry': fn = f'{W2}/cmm-trim.jpg'
        out = f"{W3}/wall/{abs(hash(k))}.jpg"
        subprocess.run(['convert', fn + '[0]', '-background', 'white', '-flatten', '-fuzz', '8%', '-trim', '+repage', out + '.t.png'])
        w, h = dims(out + '.t.png'); ar = w / h
        subprocess.run(['convert', out + '.t.png', '-gravity', 'center', '-resize', '400x400^', '-extent', '400x400', '-quality', '90', out]); os.remove(out + '.t.png')
        return dict(k=k, n=n, bn=bn, f=out, ar=round(ar, 2), w=w, h=h, ok=0.8 <= ar <= 1.25 and min(w, h) >= 360)
    with cf.ThreadPoolExecutor(12) as ex: Rr = list(ex.map(prep, m.items()))
    json.dump(Rr, open(f'{W3}/wall.json', 'w'), indent=1)
    ok = [r for r in Rr if r['ok']]; random.seed(11); random.shuffle(ok)
    key = ['Color Me Merry', 'Festive Plaid Premium', 'Candy Cane Lane', 'Tartan Tidings', 'Hip Hip Hanukkah', 'Snowflake Lodge Premium', "Santa's Mahjong Mail", 'Very Merry Wreath Premium', 'Merry & Striped', 'Winterberry', 'Alpine Snowflakes', 'Festival of Lights']
    ok.sort(key=lambda r: r['n'] not in key); sel = []; c = collections.Counter()
    for r in ok:
        if c[r['bn']] >= 6: continue
        sel.append(r); c[r['bn']] += 1
        if len(sel) == 66: break
    random.shuffle(sel); ks = {r['k'] for r in sel}
    for r in ok:
        if len(sel) >= 66: break
        if r['k'] not in ks and r['bn'] in ("Peace Love Mahjong", "Let's Be Besties", 'Oh My Mahjong'): sel.insert(len(sel) // 2, r); ks.add(r['k'])
    json.dump(sel, open(f'{W3}/wall_sel.json', 'w'), indent=1); print('wall', len(sel))
if WHAT in ('all', 'tiles'):
    T = f'{R}/assets/tiles/holiday'
    for n, f in [('dear-santa', 'dear-santa.jpg'), ('rackin-rudolph', 'rackin-rudolph.jpg'), ('hj-red', 'holly-jolly-red-pile.jpg'), ('hj-green', 'holly-jolly-green.jpg'),
                 ('hj-pink', 'holly-jolly-pink-pile.jpg'), ('tin-ruby', 'tinselle-ruby-3x3.jpg'), ('tin-emerald', 'tinselle-emerald-3x3.jpg'), ('niv-blue', 'nivalee-blue.jpg'),
                 ('nutcracker', 'nutcracker-ballet.jpg'), ('apres', 'cmc-apres-ski.jpg'), ('spirit', 'plm-spirit-of-christmas-faces-back.jpg')]:
        run('convert', f'{T}/{f}[0]', '-gravity', 'center', '-resize', '540x540^', '-extent', '540x540', '-quality', '90', f'{W3}/tiles/{n}.jpg')
    for n, u, idx, crop in [('niv-emerald', 'https://www.viroramahjong.com/products/christmas-collection-ii-nivalee', 3, None),
                            ('merry-nutcracker', 'https://peacelovemahjong.com/products/nutcracker-mahjong-tiles', 5, None),
                            ('dec1994', 'https://sundaymahjong.com/products/december-1994-tile-set-preorder-est-nov-27', 1, '100%x78%+0+0')]:
        j = json.loads(subprocess.run(['curl', '-sS', '-A', 'Mozilla/5.0', u + '.json'], capture_output=True, text=True).stdout)['product']
        src = f'{W3}/tiles/{n}.src'; run('curl', '-sS', '-A', 'Mozilla/5.0', '-o', src, j['images'][idx]['src'] + '&width=700')
        a = ['convert', src + '[0]'] + (['-gravity', 'north', '-crop', crop, '+repage'] if crop else []) + ['-gravity', 'center', '-resize', '540x540^', '-extent', '540x540', f'{W3}/tiles/{n}.jpg']
        run(*a); os.remove(src)
    print('tiles', len(os.listdir(f'{W3}/tiles')))
if WHAT in ('all', 'brand'):
    run('convert', f'{R}/assets/brand/flame-heart.png', '-filter', 'Lanczos', '-resize', '200%', f'{W3}/brand/fl.png')
    run('convert', f'{W3}/brand/fl.png', '-fuzz', '22%', '-fill', '#1F5A3C', '-opaque', '#054689', '-fuzz', '25%', '-fill', '#BF293A', '-opaque', '#E96B8D', f'{W3}/brand/flh.png')
    print('brand ok')
if WHAT in ('all', 'logos'):  # 38 code-partner logos cropped from the Oct 30 hub graphic
    G = f'{R}/assets/hub/partner-brands-2026-10-30.jpg'
    xs = [145, 276, 408, 540, 672, 804, 935]; ys = [300, 467, 637, 805, 972, 1140]
    names = [['omm', 'mrc', 'missm', 'myfair', 'middlemain', 'bb', 'bambird'], ['squad', 'tdt', 'britt', 'plm', 'cmc', 'bespoke', 'virora'],
             ['ar', 'mood', 'minimahjer', 'macmiller', 'toppe', 'amahj', 'mahjon'], ['vine', 'hiphip', 'bam', 'ymi', 'mahjongco', 'studios', 'ilovemahj'],
             ['splash', 'wren', 'press', 'royal', 'soiree', 'register', 'lbb'], [None, None, 'yolo', 'maison', 'noli', None, None]]
    for r, y in enumerate(ys):
        for c, x in enumerate(xs):
            n = names[r][c]
            if not n: continue
            run('convert', G, '-crop', f'128x150+{x - 64}+{y - 75}', '+repage', '-fuzz', '7%', '-fill', 'white', '-opaque', '#fdf5f6', '-trim', '+repage',
                '-bordercolor', 'white', '-border', '6', '-filter', 'Lanczos', '-resize', '200%', f'{W4}/logos/{n}.png')
    print('logos', len(os.listdir(f'{W4}/logos')))
