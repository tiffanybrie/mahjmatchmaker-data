"""RTS: add 'Site menu + Find Your Match as the star (desktop + mobile drafts)' to Ready for you now.
Usage: python3 rts_navplan_add.py SRC.html OUT.html
Screenshots are already in the artifact's asset store (/_blob/ urls below).
"""
import json, sys
SRC, OUT = sys.argv[1], sys.argv[2]
s = open(SRC, encoding='utf-8').read()
ID = 'l-navplan-fym'
TITLE = 'Site menu + Find Your Match as the star (desktop + mobile drafts)'
SHOTS = [  # (full, thumb, label)
 ('9fb0925b3b76736793f886d698b18c8c', 'adbca4e82b66abd3d089d41f6026feb5', 'Homepage on 10/27 · desktop'),
 ('8bb5a084bfae672f6e657817195bb263', 'b41ff9686949a24be4967595bacee43a', 'Homepage on 10/27 · phone'),
 ('0ea4b4226d5b0ca567ef22dcc60fca76', '12453411868d9726e4ba70815a264b1b', 'Homepage now: Coming 10.27 · desktop'),
 ('961fc7d7bf7f0ecadd784816b9fb767c', 'dd40be87a7abfc36142a71fbb727a687', 'Homepage now: Coming 10.27 · phone'),
 ('de724247598f8b1ce5cca9fda25e5225', '3005703828c56a6a6695700deaca423f', 'Mahjong Matches menu · desktop'),
 ('ac56d2aa4b04ba532b38a854908fce4f', '3f00b8c3f5254709b9ac242dd56b2681', 'Community menu · desktop'),
 ('a8b2b40d344703d110d840b9826724c7', '23e93aa9e464444f20e67f37b853412f', 'Phone menu (tap a folder, it opens)'),
 ('7913825fe7d5fefbff5c324f4f3d0277', '2e9752aed25832ad15926e75d462f468', 'Shop My Finds · desktop'),
 ('182ce527227988557bd5cdec5dba2dc8', '8e098120d41daec2e401d60e4c093fa6', 'Shop My Finds · phone'),
 ('88fb59e9b41f540d63010ca384f29349', '6d6b7eaf41cce285b116e661fbe18221', 'Footer'),
]
esc = lambda t: t.replace('&', '&amp;').replace('<', '&lt;')
thumbs = ''.join(f'<button type="button" class="np-t" data-np="{i}"><img src="/_blob/{t}" alt="" loading="lazy"><span><b>{i+1}</b> {esc(l)}</span></button>' for i, (f, t, l) in enumerate(SHOTS))
HTML = f'''<div class="np">
<ul class="np-sum">
<li><b>Header:</b> Mahjong Matches &#9662; &middot; Discount Codes &middot; Blog &middot; Shop &middot; Community &#9662;, with a pink <b>Find your match</b> button where Private Lessons was.</li>
<li><b>Mahjong Matches &#9662;</b> holds All Tile Albums, Holiday Matches and every color page (Mat Gallery later). <b>Community &#9662;</b> holds About, Community, Facebook Group, Share Your Table, Request an Album.</li>
<li><b>Homepage:</b> Find Your Match is the hero (&ldquo;Find your match.&rdquo; + swipe cards). Albums stay right under it. Until 10/26 it says <b>Coming 10.27</b> with an email signup.</li>
<li><b>New Shop page</b> (&ldquo;Shop My Finds&rdquo;): your Amazon idea lists (holiday tables, dice dishes, lamps, affordable sets) + a button to the full storefront. ShopMy button later.</li>
<li><b>Footer:</b> Private Lessons | Rentals + &ldquo;As an Amazon Associate I earn from qualifying purchases.&rdquo; Events stays hidden.</li>
</ul>
<div class="np-g">{thumbs}</div>
<p class="np-h">Tap any picture to open it big, then use the arrows.</p>
<p class="np-m">This replaces the menu part of &ldquo;Menu, About and Community.&rdquo; Your About and Community pages there still stand. Squarespace steps for every change are written up, so going live is quick.</p>
<p><b>On your yes, I set up the menu and the pre-launch homepage; the launch-day version goes live on 10/27.</b></p>
</div>'''
CSS = ('<style>.np-sum{margin:6px 0 10px;padding-left:20px}.np-sum li{margin:5px 0;font-size:15px}'
 '.np-g{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:10px;margin:8px 0 4px}@media(max-width:480px){.np-g{grid-template-columns:repeat(2,1fr)}}'
 '.np-t{border:0;padding:0;background:#fff;border-radius:10px;overflow:hidden;box-shadow:0 2px 8px rgba(6,40,90,.12);cursor:zoom-in;text-align:left;font:inherit;color:#064587}'
 '.np-t img{display:block;width:100%;aspect-ratio:1;object-fit:cover;object-position:top}.np-t span{display:block;padding:6px 8px;font-size:12.5px;line-height:1.3}.np-t b{color:#d6608c}'
 '.np-h{font-size:13px;color:var(--mute);margin:2px 0 8px}.np-m{font-size:14px;color:var(--mute)}'
 '.nplb{position:fixed;inset:0;background:rgba(10,8,14,.95);display:none;flex-direction:column;z-index:60}.nplb.on{display:flex}'
 '.nplb .t{display:flex;justify-content:space-between;align-items:center;color:#fff;padding:10px 14px;font-size:14px;gap:10px}'
 '.nplb .t button,.nplb .n button{background:rgba(255,255,255,.15);color:#fff;border:0;border-radius:999px;padding:9px 16px;font:700 14px "DM Sans",sans-serif;cursor:pointer}'
 '.nplb .st{flex:1;overflow:auto;-webkit-overflow-scrolling:touch;padding:0 8px;text-align:center}.nplb .st img{max-width:100%;border-radius:8px}'
 '.nplb .n{display:flex;gap:8px;padding:10px 14px calc(14px + env(safe-area-inset-bottom,0px))}.nplb .n button{flex:1;border-radius:12px;padding:12px}</style>')
JS = ('<div class="nplb" id="nplb" role="dialog" aria-label="Screenshot viewer"><div class="t"><span id="nplbc"></span><button type="button" id="nplbx">Close</button></div>'
 '<div class="st" id="nplbs"><img id="nplbi" alt=""></div><div class="n"><button type="button" id="nplbp">&lsaquo; Prev</button><button type="button" id="nplbn">Next &rsaquo;</button></div></div>'
 '<script>(function(){const ID=' + json.dumps(ID) + ',H=' + json.dumps(HTML) + ',S=' + json.dumps([[f'/_blob/{f}', l] for f, t, l in SHOTS]) + ';let cur=0;'
 'function inject(){const el=document.querySelector(\'.item[data-id="\'+ID+\'"]\');if(!el||el.querySelector(".np"))return;const d=el.querySelector(".desc");if(!d)return;const w=document.createElement("div");w.innerHTML=H;d.replaceWith(w.firstElementChild);'
 'const bs=el.querySelector(".btns");if(bs){bs.innerHTML=\'<button class="yes" data-v="ok" type="button">Yes, set it up</button>\'}const ta=el.querySelector("textarea");if(ta)ta.placeholder="What should change? (optional)"}'
 'const lb=document.getElementById("nplb"),im=document.getElementById("nplbi"),cap=document.getElementById("nplbc"),st=document.getElementById("nplbs");'
 'function show(){im.src=S[cur][0];cap.textContent=(cur+1)+" of "+S.length+" · "+S[cur][1];st.scrollTop=0}'
 'document.addEventListener("click",e=>{const t=e.target.closest("[data-np]");if(!t)return;e.preventDefault();e.stopPropagation();cur=+t.dataset.np;lb.classList.add("on");show()},true);'
 'document.getElementById("nplbx").onclick=()=>lb.classList.remove("on");document.getElementById("nplbp").onclick=()=>{cur=(cur+S.length-1)%S.length;show()};document.getElementById("nplbn").onclick=()=>{cur=(cur+1)%S.length;show()};'
 'document.addEventListener("keydown",e=>{if(!lb.classList.contains("on"))return;if(e.key==="Escape")lb.classList.remove("on");if(e.key==="ArrowRight")document.getElementById("nplbn").click();if(e.key==="ArrowLeft")document.getElementById("nplbp").click()});'
 'inject();setInterval(inject,1500);})();</script>')

assert ID not in s, 'already added'
assert s.count('LOOK=[[') == 1
s = s.replace('LOOK=[[', 'LOOK=[' + json.dumps([TITLE, '', '', ID]) + ',[', 1)
assert s.count('NOW=[') == 1
s = s.replace('NOW=[', 'NOW=["' + ID + '",', 1)
i = s.rfind('</body>')
s = s[:i] + CSS + JS + s[i:] if i >= 0 else s + CSS + JS
open(OUT, 'w', encoding='utf-8').write(s)
print('ok', len(s))
