"""Capture Find Your Mat-ch screens (390x844 @3x) for social."""
import sys, os
from playwright.sync_api import sync_playwright
OUT = '/home/claude/fymapp/caps'; os.makedirs(OUT, exist_ok=True)
URL = 'http://localhost:8765/index.html'

def start(p):
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=3)
    pg.goto(URL); pg.wait_for_timeout(4000)
    try: pg.get_by_text('Skip tour').click(timeout=3000)
    except Exception: pass
    pg.wait_for_timeout(400)
    return b, pg

def pick(pg, name):
    pg.locator('input').first.fill(name); pg.wait_for_timeout(700)
    ok = pg.evaluate("""(n)=>{const el=[...document.querySelectorAll('button')].find(b=>b.offsetParent&&b.innerText.trim().startsWith(n)); if(!el) return false; el.scrollIntoView(); el.click(); return true}""", name)
    pg.wait_for_timeout(2800)
    return ok

def shot(pg, name):
    pg.screenshot(path=f'{OUT}/{name}.png'); print('saved', name)

jobs = sys.argv[1:]
with sync_playwright() as p:
    for job in jobs:
        kind, _, arg = job.partition(':')
        b, pg = start(p)
        try:
            if kind == 'home':
                pg.evaluate('window.scrollTo(0,0)'); pg.wait_for_timeout(400); shot(pg, 'home')
            elif kind == 'color':
                pg.get_by_text(arg, exact=True).first.click(); pg.wait_for_timeout(1200)
                pg.evaluate("""()=>{const g=[...document.querySelectorAll('button')].find(b=>b.offsetParent&&/Holiday|Pink/.test(b.innerText)); g&&g.scrollIntoView({block:'start'}); window.scrollBy(0,-90)}""")
                pg.wait_for_timeout(800); shot(pg, 'color-' + arg.replace(' ', '_').replace('&', 'and'))
            elif kind == 'set':
                if pick(pg, arg):
                    shot(pg, 'set-' + arg.replace(' ', '_'))
                    pass
                else: print('NOT FOUND', arg)
            elif kind == 'brand':
                pick(pg, arg); pg.get_by_text('Brand ▾').first.click(); pg.wait_for_timeout(1000); shot(pg, 'brand-menu')
            elif kind == 'wheel':
                pick(pg, arg); pg.locator('.dot').first.click(); pg.wait_for_timeout(1000); shot(pg, 'wheel')
            elif kind == 'pair':
                st, mat = arg.split('|')
                pick(pg, st)
                q = pg.locator('#msq'); q.fill(mat); pg.wait_for_timeout(1200)
                print(pg.evaluate("(m)=>[...document.querySelectorAll('button,li,[role=option]')].filter(e=>e.offsetParent&&e.innerText.includes(m)).map(e=>e.tagName+':'+e.innerText.slice(0,50))", mat))
                pg.evaluate("(m)=>{const el=[...document.querySelectorAll('button,li,[role=option]')].find(e=>e.offsetParent&&e.innerText.trim().startsWith(m)); if(el){el.click();}}", mat)
                pg.wait_for_timeout(2500)
                shot(pg, 'pair-' + st.replace(' ', '_') + '-' + mat.replace(' ', '_'))
            elif kind == 'swipe':
                st, mat = arg.split('|')
                pick(pg, st); found=False
                for i in range(80):
                    txt = pg.evaluate("()=>document.body.innerText")
                    names = pg.evaluate("()=>[...document.querySelectorAll('#yes')].length")
                    cur = pg.evaluate("()=>{const y=document.querySelector('button.yes');let c=y;for(let k=0;k<8&&c;k++)c=c.parentElement;return ''}")
                    vis = pg.evaluate("(m)=>{const y=document.querySelector('button.yes').getBoundingClientRect().top;const bs=[...document.querySelectorAll('b')].filter(e=>e.offsetParent&&(()=>{const r=e.getBoundingClientRect();return r.top>y-260&&r.top<y})());return bs.length&&bs[bs.length-1].innerText.trim()==m}", mat)
                    if vis: found=True; break
                    pg.locator('button.no').first.click(timeout=4000); pg.wait_for_timeout(700)
                print('found' if found else 'NOT FOUND', st, mat, i)
                for _ in range(int(os.environ.get('TZOOM','0'))):
                    pg.evaluate("()=>{const b=[...document.querySelectorAll('button')].filter(e=>e.offsetParent&&e.innerText.trim()=='+');b[0]&&b[0].click()}"); pg.wait_for_timeout(500)
                shot(pg, 'swipe-' + st.replace(' ', '_') + '-' + mat.replace(' ', '_'))
            elif kind == 'mat':
                pg.get_by_text('I have a mat').first.click(); pg.wait_for_timeout(1500); shot(pg, 'matdoor')
        except Exception as e:
            print('ERR', job, str(e)[:160])
        b.close()
