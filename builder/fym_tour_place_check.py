"""FYM tour check (QA v72, Oct 21): at 390x664, 390x844 and 1280x800 (Chromium; phone sizes also WebKit) walk all 6 tour steps and
FAIL if a coach bubble intersects its bounce target, the target is not fully on screen, or elementFromPoint at the target is not the target.
Usage: python3 builder/fym_tour_place_check.py <build_dir> [shots_dir]   (serves the build itself on a free port). Exit 1 on any fail."""
import sys,time,json,os,socket,subprocess
from playwright.sync_api import sync_playwright
B=os.path.abspath(sys.argv[1]); OUT=sys.argv[2] if len(sys.argv)>2 else None
so=socket.socket(); so.bind(('127.0.0.1',0)); port=so.getsockname()[1]; so.close()
srv=subprocess.Popen([sys.executable,'-m','http.server',str(port),'--bind','127.0.0.1','--directory',B],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(1)
VPS=[(390,664),(390,844),(1280,800)]; fails=[]
CHK="""()=>{const r=coachRect();if(!r)return {none:true};const [a,b]=[r.c,r.b];const inter=!(a[2]<=b[0]||b[2]<=a[0]||a[3]<=b[1]||b[3]<=a[1]);
const s=TSTEPS[TOUR.step];const t=s.b.split(',').map(x=>document.querySelector(x)).find(Boolean);const cx=(b[0]+b[2])/2,cy=(b[1]+b[3])/2;const e=document.elementFromPoint(cx,cy);
return {step:TOUR.step,inter,hit:!!(e&&(t===e||t.contains(e))),hitId:e&&(e.id||e.className),vis:b[0]>=0&&b[2]<=document.documentElement.clientWidth&&b[1]>=0&&b[3]<=innerHeight,c:a.map(Math.round),b:b.map(Math.round),gap:Math.round(Math.min(Math.abs(a[3]-b[1]),Math.abs(b[3]-a[1])))}}"""
with sync_playwright() as p:
  for bt in ('chromium','webkit'):
    for (w,h) in VPS:
      if bt=='webkit' and w>400: continue
      b=getattr(p,bt).launch(); pg=b.new_page(viewport={'width':w,'height':h}); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
      pg.goto(f'http://localhost:{port}/index.html'); pg.wait_for_function('window.__imgsReady===true',timeout=60000); time.sleep(1.5)
      pg.click('[data-tq-yes]'); time.sleep(1.2)
      for k in range(6):
        time.sleep(.5); r=pg.evaluate(CHK); tag=f'{bt}-{w}x{h}-step{k+1}'
        OUT and pg.screenshot(path=f'{OUT}/{tag}.png')
        bad=r.get('none') or r['inter'] or not r['hit'] or not r['vis']
        print(tag,'OK' if not bad else 'FAIL',r)
        if bad: fails.append(tag)
        s=pg.evaluate("TSTEPS[TOUR.step].b"); sel=[x for x in s.split(',') if pg.query_selector(x)][0]
        if pg.evaluate("TSTEPS[TOUR.step].ev")=='next': pg.click('[data-tour-next]')
        else: pg.click(sel)
        time.sleep(.6)
        if not pg.evaluate("TOUR.on"): print(tag,'tour ended after step',k+1); break
      print(bt,w,h,'errors',errs)
      if errs: fails.append(f'{bt}-{w}x{h} page errors'); b.close()
srv.terminate()
print('FAILS',fails)
sys.exit(1 if fails else 0)
