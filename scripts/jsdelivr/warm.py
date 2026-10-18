import re, glob, sys, time, json, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
import os
D = os.environ.get('WARM_DIR', os.getcwd()) + '/'
RX = re.compile(r"https://cdn\.jsdelivr\.net/gh/tiffanybrie/mahjmatchmaker-data@[0-9a-f]+/[^\"'\s)<>\\,]+")
urls = set()
for f in glob.glob(D + (sys.argv[1] if len(sys.argv)>1 else 'live') + '/*.html'):
    urls |= set(RX.findall(open(f, errors='ignore').read()))
UA = {'User-Agent': 'Mozilla/5.0'}

def get(u, tries=8):
    last = None
    for i in range(tries):
        try:
            r = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40)
            return 200, r.read(), i
        except urllib.error.HTTPError as e:
            last = e.code
        except Exception as e:
            last = str(e)[:40]
        time.sleep(3 + 2 * i)
    return last, b'', tries

# expand nested: text assets fetched by code blocks
seen = set(); results = {}
queue = list(urls)
while queue:
    batch = [u for u in queue if u not in seen]; queue = []
    seen |= set(batch)
    with ThreadPoolExecutor(8) as ex:
        for u, (code, body, n) in zip(batch, ex.map(get, batch)):
            results[u] = (code, n)
            if code == 200 and re.search(r'\.(html|js|json|css|txt)$', u):
                for v in RX.findall(body.decode('utf-8', 'ignore')):
                    if v not in seen: queue.append(v)
first_fail = sum(1 for c, n in results.values() if c == 200 and n > 0)
bad = {u: c for u, (c, n) in results.items() if c != 200}
json.dump({'total': len(results), 'ok_first_try': sum(1 for c, n in results.values() if c == 200 and n == 0),
           'ok_after_retry': first_fail, 'still_failing': bad}, open(D + ('warm_result_'+(sys.argv[1] if len(sys.argv)>1 else 'live')+'.json'), 'w'), indent=1)
print(len(results), 'urls;', first_fail, 'needed retries;', len(bad), 'still failing')
