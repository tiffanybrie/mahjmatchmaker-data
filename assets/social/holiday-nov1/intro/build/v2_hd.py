"""v2: replace low-res (thumbnail) mat photos in /dev/shm/introv2/mats/map.json with the brand's own Shopify product image
(variant image when the FYM link names a variant), 800px."""
import json, subprocess, re, concurrent.futures as cf
W = '/dev/shm/introv2'
m = json.load(open(f'{W}/mats/map.json'))
for v in m.values():
    if len(v) < 4: v.append(int(subprocess.run(['identify', '-format', '%w', v[0] + '[0]'], capture_output=True, text=True).stdout or 0))
st = json.load(open(f'{W}/stock.json'))
def get(k):
    v = m[k]
    if v[3] >= 1000 or k not in st: return k, None
    url = st[k]['url']; vid = re.search(r'[?&]v(?:ariant)?=(\d+)', k + ' ' + url)
    base = url.split('#')[0].split('?')[0]
    try:
        j = json.loads(subprocess.run(['curl', '-sS', '-m', '20', '-A', 'Mozilla/5.0', base + '.json'], capture_output=True, text=True).stdout)['product']
        src = j['images'][0]['src']
        if vid:
            for var in j['variants']:
                if str(var['id']) == vid.group(1) and var.get('image_id'):
                    src = next(i['src'] for i in j['images'] if i['id'] == var['image_id'])
        fn = f"{W}/hd/{abs(hash(k))}.jpg"
        subprocess.run(['curl', '-sS', '-m', '30', '-A', 'Mozilla/5.0', '-o', fn + '.src', src + ('&' if '?' in src else '?') + 'width=1200'])
        subprocess.run(['convert', fn + '.src[0]', '-resize', '1200x1200>', '-quality', '90', fn])
        return k, fn
    except Exception as e:
        return k, None
with cf.ThreadPoolExecutor(16) as ex:
    for k, fn in ex.map(get, list(m)):
        if fn: m[k][0] = fn; m[k][3] = 1200
json.dump(m, open(f'{W}/mats/map.json', 'w'), indent=1)
print('still low:', [v[1] for v in m.values() if v[3] < 1000])
