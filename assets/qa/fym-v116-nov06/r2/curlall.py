import subprocess,json,sys,threading,collections,time
from concurrent.futures import ThreadPoolExecutor
Q=sys.argv[1]; urls=[l.strip() for l in open(Q+'/urls.txt') if l.strip()]
UA='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
sem=collections.defaultdict(lambda: threading.Semaphore(3))
def one(u):
  h=u.split('/')[2]
  with sem[h]:
    for attempt in range(3):
      try:
        r=subprocess.run(['curl','-s','-o','/dev/null','-L','--max-redirs','8','-m','30','-A',UA,'-D','-','-w','\n@@%{http_code} %{url_effective} %{num_redirects}',u],capture_output=True,text=True,timeout=45)
        out=r.stdout; last=out.rsplit('@@',1)[-1].strip().split(' ')
        code=int(last[0] or 0); final=last[1] if len(last)>1 else ''
        hdr=out.rsplit('@@',1)[0]
        first=[l for l in hdr.splitlines() if l.startswith('HTTP/')]
        cookie='discount_code=' in hdr.lower() or 'discount_code' in hdr.lower()
        res={'u':u,'code':code,'first':first[0].split(' ')[1] if first else '','final':final,'cookie':cookie,'hops':[l.split(' ')[1] for l in first]}
        if code in (429,0) or code>=500: time.sleep(4*(attempt+1)); continue
        return res
      except Exception as e: res={'u':u,'code':0,'err':str(e)}
    return res
with ThreadPoolExecutor(24) as ex: R=list(ex.map(one,urls))
json.dump(R,open(Q+'/curl_results.json','w'),indent=0)
c=collections.Counter(r['code'] for r in R);print(c)
