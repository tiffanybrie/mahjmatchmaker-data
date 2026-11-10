#!/usr/bin/env python3
"""Animated reel end frames (MP4, 1080x1920, 30fps) for dropping into the end of a Canva reel (Tiffany Nov 10 6:19pm).
Takes the same HTML as hooked_up.py / fym_brands.py (they write /tmp/hooked.html, /tmp/fymend.html) and drives a
render(t) timeline frame by frame. Usage: animate.py hooked|fym <out.mp4> [seconds]"""
import sys, os, subprocess, shutil
from playwright.sync_api import sync_playwright
kind, out = sys.argv[1], sys.argv[2]; DUR = float(sys.argv[3]) if len(sys.argv) > 3 else 5.0; FPS = 30
src = {'hooked': '/tmp/hooked.html', 'fym': '/tmp/fymend.html'}[kind]
JS = r'''
const cl=x=>Math.min(Math.max(x,0),1), eo=x=>1-Math.pow(1-cl(x),3), eb=x=>{x=cl(x);const c1=1.70158,c3=c1+1;return 1+c3*Math.pow(x-1,3)+c1*Math.pow(x-1,2)};
const A=[...document.body.querySelectorAll(':scope > *')]; A.forEach(e=>{e.dataset.t0=e.style.transform||'';});
function pop(e,t,a,d){const k=eb((t-a)/d);e.style.opacity=cl((t-a)/(d*0.5));e.style.transform=(e.dataset.t0+' scale('+Math.max(k,0)+')');}
function up(e,t,a,d){const k=eo((t-a)/d);e.style.opacity=k;e.style.transform=e.dataset.t0+' translateY('+(60*(1-k))+'px)';}
function slide(e,t,a,d,dx,dy){const k=eo((t-a)/d);e.style.opacity=cl((t-a)/(d*0.4));e.style.transform=e.dataset.t0+' translate('+(dx*(1-k))+'px,'+(dy*(1-k))+'px)';}
'''
TL = {
 'hooked': r'''
window.render=function(t){const E=A.filter(e=>e.tagName!=='STYLE');
 // order: 4 corners, logo, tagline, mat, bubble1, bubble2, tile, pill, pill2
 for(let i=0;i<4;i++) up(E[i],t,0.0+i*0.05,0.5);
 up(E[4],t,0.15,0.5); up(E[5],t,0.35,0.5);
 slide(E[6],t,0.55,0.6,-500,0); pop(E[7],t,0.9,0.45); pop(E[8],t,1.15,0.45); slide(E[9],t,0.75,0.6,500,-200);
 pop(E[10],t,1.45,0.5); up(E[11],t,1.9,0.5);
 if(t>2.4){const s=1+0.035*Math.sin((t-2.4)*Math.PI*2/1.2);E[10].style.transform=E[10].dataset.t0+' scale('+s+')';}
}''',
 'fym': r'''
const g=document.getElementById('g'); const chips=[...g.children];
// turn the static wall into 6 ticker rows, alternating direction
g.style.display='block'; g.innerHTML=''; const rows=[];
for(let r=0;r<6;r++){const row=document.createElement('div');row.style.cssText='display:flex;gap:18px;margin-bottom:18px;width:max-content';
 let L=chips.filter((c,i)=>i%6===r); L=L.concat(L.map(c=>c.cloneNode(true))).concat(L.map(c=>c.cloneNode(true)));L.forEach(c=>row.appendChild(c));g.appendChild(row);rows.push(row);}
window.render=function(t){const E=A.filter(e=>e.tagName!=='STYLE');
 pop(E[0],t,0.0,0.45); up(E[1],t,0.25,0.5); pop(E[2],t,0.5,0.5); up(E[3],t,0.8,0.5); pop(E[4],t,1.1,0.5); up(E[5],t,1.35,0.5);
 g.style.opacity=cl((t-0.4)/0.5);
 rows.forEach((row,r)=>{const w=row.scrollWidth/3; const dir=r%2?1:-1; const x=((t*70*(1+0.15*r))%w); row.style.transform='translateX('+(dir>0? -w+x : -x)+'px)';});
 if(t>1.7){const s=1+0.04*Math.sin((t-1.7)*Math.PI*2/1.0);E[4].style.transform='scale('+s+')';}
}'''}
d = '/tmp/endanim_' + kind; shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.goto('file://' + src); pg.wait_for_load_state('networkidle'); pg.evaluate('document.fonts.ready')
    pg.add_script_tag(content=JS + TL[kind])
    for n in range(int(DUR * FPS)):
        pg.evaluate(f'render({n / FPS})'); pg.screenshot(path=f'{d}/{n:04d}.png')
    b.close()
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-framerate', str(FPS), '-i', f'{d}/%04d.png', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-movflags', '+faststart', out], check=True)
print(out)
