"""RTS v102: add the 'how a look gets shopped' template card (Papaya Spritz example).
Usage: python3 rts_v101_add.py SRC.html OUT.html TILE.jpg
"""
import json, sys, base64
SRC, OUT, IMG = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(SRC, encoding='utf-8').read()
PAPD = 'data:image/jpeg;base64,' + base64.b64encode(open(IMG, 'rb').read()).decode()
ID = 'l-template-shop'
PAP = '__PAP__'
ALBUM = 'mahjmatchmaker.com/papaya-spritz-mahjong-tile-matches'

TPL0 = f'''
<div class="tp">
<p class="tpl-lead">No products picked yet. This is only the <b>layout</b>: where each kind of link goes. Once you say yes, every look I post follows it.</p>

<h4>The map</h4>
<div class="tflow" role="img" aria-label="How links flow from a post to the shop">
 <div class="tf-src">One look<small>tiles + mat + the rest of the table</small></div>
 <div class="tf-lanes">
  <div class="tf-lane">
   <div class="tf-h">Instagram reel</div>
   <div class="tf-n">Any comment</div><div class="tf-a">&darr;</div>
   <div class="tf-n">ManyChat DM</div><div class="tf-a">&darr;</div>
   <div class="tf-split"><div class="tf-n tf-p">Button 1<small>Oh My Mahjong direct link + MAHJMATCH</small></div><div class="tf-n tf-s">Button 2<small>ShopMy &ldquo;rest of the table&rdquo;</small></div></div>
  </div>
  <div class="tf-lane">
   <div class="tf-h">Pinterest: mixed look</div>
   <div class="tf-n">Pin (one link)</div><div class="tf-a">&darr;</div>
   <div class="tf-n tf-w">Album page on mahjmatchmaker.com<small>code + partner links + &ldquo;shop the rest&rdquo;</small></div>
  </div>
  <div class="tf-lane">
   <div class="tf-h">Pinterest: all-Amazon</div>
   <div class="tf-n">Holiday pin (evergreen)</div><div class="tf-a">&darr;</div>
   <div class="tf-n tf-z">Amazon storefront<small>the matching collage post</small></div>
  </div>
 </div>
 <div class="tf-key"><span class="k tf-p"></span>Partner brand: direct link + MAHJMATCH <span class="k tf-s"></span>ShopMy: non-partner extras <span class="k tf-w"></span>Your website <span class="k tf-z"></span>Amazon</div>
</div>

<h4>The 4 rules</h4>
<ol class="trules">
<li><b>Partner brands always get their direct link + code MAHJMATCH.</b> Oh My Mahjong, Mahjong Row, Bird &amp; Bamboo, Middle &amp; Main and the rest. Never ShopMy.</li>
<li><b>ShopMy holds only the extras.</b> One &ldquo;Shop the &lt;set&gt; table&rdquo; collection per look: lamp, coasters, dice dish, linens. Amazon items earn through your Associates code saved in ShopMy. Etsy finds can sit there too, even if they don't earn.</li>
<li><b>Reels: any comment gets a DM.</b> No keyword, so a simple &ldquo;this is stunning&rdquo; still gets the links. The DM text has the tile/mat brand lines + code. Button 1 = tiles + mat (partner link). Button 2 = the rest of the table (ShopMy). More partner brands = one short line each in the text, buttons stay at two.</li>
<li><b>Pinterest: one pin, one link.</b> Mixed looks go to the album page. All-Amazon holiday pins go to the matching Amazon storefront post.</li>
</ol>

<h4>1. The reel caption ends like this</h4>
<div class="tphones">
<div class="ph ph-reel">
 <div class="ph-scr reel" style="background-image:url({PAP})">
  <div class="reel-top">Reels</div>
  <div class="reel-side"><span>&#9825;<i>1.2K</i></span><span>&#128172;<i>86</i></span><span>&#10148;</span></div>
  <div class="reel-cap">
   <div class="reel-who"><span class="av">MM</span><b>mahjmatchmaker</b><span class="fol">Follow</span></div>
   <p>Papaya Spritz just dropped and she's a whole vibe &#127818;&#128156; (your usual caption here)</p>
   <p class="cta">Comment below for links &#128140;</p>
   <p class="tags">#mahjong #mahjongtiles #mahjongmat #mahjmatchmaker #mahjonglife #mahjongaddict #mahjongnight</p>
  </div>
 </div>
</div>
<div class="tnote">
 <p><b>The caption ends with the ask:</b> &ldquo;Comment below for links &#128140;&rdquo;, then our hashtags.</p>
 <div class="cmt"><span class="av av2">J</span><div><b>jen.plays.mahj</b> This is stunning &#128525;</div></div>
 <p class="mut">Any comment at all, and ManyChat sends the DM below automatically, and replies under her comment &ldquo;Sent! Check your DMs &#128140;&rdquo;.</p>
 <p class="tset"><b>ManyChat setting:</b> this post only, trigger = any comment (not a keyword). Every caption also ends with our hashtags.</p>
</div>
</div>

<h4>2. The DM they get</h4>
<div class="tphones">
<div class="ph">
 <div class="ph-scr dm">
  <div class="dm-top"><span class="bk">&lsaquo;</span><span class="av">MM</span><div><b>mahjmatchmaker</b><small>Mahj Matchmaker</small></div></div>
  <div class="dm-body">
   <div class="dm-me dm-cm">Commented: This is stunning &#128525;</div>
   <div class="dm-card">
    <img src="{PAP}" alt="Papaya Spritz tiles">
    <div class="dm-txt">
     <p>Thank you! &#128149; Here are the links from this table in case you want them:</p>
     <p><b>Papaya Spritz tiles by Oh My Mahjong — use code MAHJMATCH</b></p>
     <p class="ftc">(affiliate links — I may earn a commission)</p>
    </div>
    <div class="dm-btn">Shop Papaya Spritz tiles</div>
    <div class="dm-btn">Shop the rest of the table</div>
   </div>
  </div>
  <div class="dm-bar">Message...</div>
 </div>
</div>
<div class="tnote">
 <p><b>Button 1</b> &rarr; the Oh My Mahjong Papaya Spritz page, through your Oh My Mahjong affiliate link.</p>
 <p><b>Button 2</b> &rarr; the ShopMy collection below.</p>
 <p class="mut">If the mat is from a different partner brand, it gets one short line in the message instead of another button, like:<br><i>&ldquo;Mat: &lt;name&gt; by Mahjong Row &amp; Co. — code MAHJMATCH &rarr; link&rdquo;</i></p>
</div>
</div>

<h4>3. The ShopMy page (Button 2)</h4>
<div class="tphones">
<div class="ph">
 <div class="ph-scr sm">
  <div class="sm-top">shopmy.us/mahjmatchmaker</div>
  <div class="sm-head"><span class="av">MM</span><div><small>Mahj Matchmaker</small><b>Shop the Papaya Spritz Table</b></div></div>
  <p class="sm-blurb">Everything around the tiles: the lamp, the coasters, the little extras. The tiles and mat are in my DM (code MAHJMATCH).</p>
  <div class="sm-grid">
   <div class="sm-it"><div class="sm-ph">&#128161;</div><b>Amazon lamp (TBD)</b><small>Amazon</small></div>
   <div class="sm-it"><div class="sm-ph">&#9711;</div><b>Amazon coasters (TBD)</b><small>Amazon</small></div>
   <div class="sm-it"><div class="sm-ph">&#127922;</div><b>dice dish (TBD)</b><small>Amazon or Etsy</small></div>
   <div class="sm-it"><div class="sm-ph">&#10047;</div><b>Etsy find (TBD)</b><small>Etsy</small></div>
   <div class="sm-it"><div class="sm-ph">&#9638;</div><b>table linens (TBD)</b><small>Amazon</small></div>
   <div class="sm-it"><div class="sm-ph">&#127864;</div><b>drink cups (TBD)</b><small>Amazon</small></div>
  </div>
 </div>
</div>
<div class="tnote">
 <p><b>Only the extras live here.</b> No Oh My Mahjong (or any partner) products, so a shopper never lands on a partner item without your code.</p>
 <p class="mut">Gray boxes are placeholders. I'm not picking real products for this one.</p>
</div>
</div>

<h4>4. Pinterest: two kinds of pins</h4>
<div class="tpins">
 <div class="pin-col">
  <div class="pin"><img src="{PAP}" alt=""><div class="pin-ov">Papaya Spritz<br>mahjong table</div></div>
  <div class="pin-t">Mixed look</div>
  <div class="pin-a">&darr;</div>
  <div class="pin-d tf-w"><b>Album page</b><small>{ALBUM}</small><small>code MAHJMATCH + partner links + &ldquo;shop the rest of the table&rdquo;</small></div>
 </div>
 <div class="pin-col">
  <div class="pin pin-amz"><div class="pin-ph"><span>&#127876;</span><span>&#128367;</span><span>&#127873;</span><span>&#11088;</span></div><div class="pin-ov">Holiday mahj<br>table finds</div></div>
  <div class="pin-t">All-Amazon (holiday, evergreen)</div>
  <div class="pin-a">&darr;</div>
  <div class="pin-d tf-z"><b>Amazon storefront</b><small>the matching collage post</small><small>(example, nothing made)</small></div>
 </div>
</div>

<h4>Your yes</h4>
<p class="mut">Approve and I use this layout for everything I post. Want something different? Tap Change something and tell me in the box (or talk it).</p>
</div>'''
TPL = TPL0

CSS = ('<style>'
 '.tp h4{font:400 19px Caprasimo,serif;color:#064587;margin:20px 0 8px}.tp p{margin:6px 0}.tpl-lead{font-weight:600}.tp .mut{color:var(--mute);font-size:14px}'
 '.tflow{border:1px solid var(--line);border-radius:14px;padding:12px;background:var(--bg)}'
 '.tf-src{text-align:center;font-weight:700;background:#064587;color:#fff;border-radius:12px;padding:10px;margin:0 auto 10px;max-width:320px}.tf-src small,.tf-n small,.pin-d small{display:block;font-weight:400;font-size:12px;opacity:.85;line-height:1.3;margin-top:2px;word-break:break-word}'
 '.tf-lanes{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}@media(max-width:600px){.tf-lanes{grid-template-columns:1fr}}'
 '.tf-lane{border:1px dashed var(--line);border-radius:12px;padding:8px;text-align:center}.tf-h{font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.05em;color:var(--mute);margin-bottom:6px}'
 '.tf-n{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:7px 8px;font-size:14px;font-weight:600}.tf-a{color:var(--pink);font-weight:700;line-height:1.2}'
 '.tf-split{display:grid;grid-template-columns:1fr 1fr;gap:6px}'
 '.tf-p{background:#fde3ec;border-color:#e2468f;color:#7a1747}.tf-s{background:#e7e4fb;border-color:#7b6fd6;color:#33287a}.tf-w{background:#e1ecf8;border-color:#064587;color:#064587}.tf-z{background:#fff1dc;border-color:#e08a1e;color:#7a4500}'
 '.tf-key{display:flex;flex-wrap:wrap;gap:4px 12px;font-size:12px;color:var(--mute);margin-top:10px;align-items:center}.tf-key .k{display:inline-block;width:12px;height:12px;border-radius:3px;border:1px solid;vertical-align:-2px;margin-right:-6px}'
 '.trules{padding-left:22px;margin:4px 0}.trules li{margin:8px 0;font-size:15px}'
 '.tphones{display:flex;gap:16px;align-items:flex-start;flex-wrap:wrap}.tnote{flex:1 1 220px;min-width:0;font-size:15px}'
 '.ph{flex:0 0 auto;width:270px;max-width:100%;background:#111;border-radius:30px;padding:9px;box-shadow:0 6px 20px rgba(6,40,90,.18)}'
 '.ph-scr{border-radius:22px;overflow:hidden;min-height:480px;position:relative;font:14px/1.35 -apple-system,BlinkMacSystemFont,"DM Sans",sans-serif;color:#111;background:#fff}'
 '.av{display:inline-flex;align-items:center;justify-content:center;width:30px;height:30px;border-radius:50%;background:#e2468f;color:#fff;font:700 11px "DM Sans",sans-serif;flex:0 0 auto}.av2{background:#7b6fd6}'
 '.reel{height:480px;background-size:cover;background-position:center;color:#fff}.reel:after{content:"";position:absolute;inset:0;background:linear-gradient(to bottom,rgba(0,0,0,.25),rgba(0,0,0,0) 25%,rgba(0,0,0,0) 45%,rgba(0,0,0,.8))}'
 '.reel>*{position:relative;z-index:1}.reel-top{position:absolute;top:12px;left:14px;font-weight:700;font-size:17px}'
 '.reel-side{position:absolute;right:10px;bottom:120px;display:flex;flex-direction:column;gap:14px;font-size:22px;text-align:center}.reel-side i{display:block;font-size:11px;font-style:normal}'
 '.reel-cap{position:absolute;left:12px;right:52px;bottom:14px;font-size:13px}.reel-who{display:flex;align-items:center;gap:7px;margin-bottom:4px}.reel-who .av{width:26px;height:26px}.fol{border:1px solid #fff;border-radius:6px;padding:1px 7px;font-size:12px;font-weight:600}'
 '.reel-cap p{margin:4px 0}.reel-cap .tags{font-size:11px;color:#cfe3ff;margin-top:4px}.tset{background:var(--soft);border-radius:10px;padding:8px 10px;font-size:14px}.dm-cm{font-size:12px;font-weight:500;opacity:.9}.reel-cap .cta{font-weight:700;background:rgba(226,70,143,.9);border-radius:8px;padding:5px 7px;display:inline-block}'
 '.cmt{display:flex;gap:8px;align-items:center;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:8px 10px;margin:8px 0;font-size:14px}'
 '.dm{display:flex;flex-direction:column}.dm-top{display:flex;align-items:center;gap:8px;padding:12px 12px 10px;border-bottom:1px solid #eee}.dm-top small{display:block;color:#888;font-size:11px}.bk{font-size:26px;line-height:1;margin-right:2px}'
 '.dm-body{flex:1;padding:12px 10px;display:flex;flex-direction:column;gap:10px}'
 '.dm-me{align-self:flex-end;background:#7b5cff;color:#fff;border-radius:18px;padding:7px 13px;font-weight:600}'
 '.dm-card{align-self:flex-start;width:88%;background:#efefef;border-radius:18px;overflow:hidden}.dm-card img{display:block;width:100%;height:110px;object-fit:cover}'
 '.dm-txt{padding:8px 11px 4px}.dm-txt p{margin:0 0 6px;font-size:13px}.dm-txt .ftc{color:#666;font-size:11.5px}'
 '.dm-btn{background:#fff;margin:0 8px 6px;border-radius:10px;padding:8px;text-align:center;font-weight:700;color:#0a5bd8;font-size:13px}.dm-btn:last-child{margin-bottom:9px}'
 '.dm-bar{margin:8px 10px 12px;border:1px solid #ddd;border-radius:20px;padding:8px 12px;color:#999;font-size:13px}'
 '.sm{background:#fbfaf8}.sm-top{background:#eee;color:#555;font-size:11px;text-align:center;padding:7px}.sm-head{display:flex;gap:8px;align-items:center;padding:12px 12px 4px}.sm-head small{display:block;color:#888;font-size:11px}.sm-head b{font-family:Caprasimo,serif;font-weight:400;font-size:17px;line-height:1.15}'
 '.sm-blurb{font-size:12px;color:#555;padding:0 12px;margin:4px 0 8px!important}'
 '.sm-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:0 12px 14px}.sm-it{background:#fff;border:1px solid #eee;border-radius:10px;padding:6px;font-size:11.5px;line-height:1.25}.sm-it small{display:block;color:#999;font-size:10.5px}'
 '.sm-ph{height:52px;border-radius:7px;background:repeating-linear-gradient(45deg,#f1f0ee,#f1f0ee 6px,#e7e5e1 6px,#e7e5e1 12px);display:flex;align-items:center;justify-content:center;font-size:20px;color:#999;margin-bottom:4px}'
 '.tpins{display:grid;grid-template-columns:1fr 1fr;gap:12px;max-width:520px}.pin-col{text-align:center;min-width:0}'
 '.pin{position:relative;border-radius:16px;overflow:hidden;aspect-ratio:2/3;background:#ddd}.pin img{width:100%;height:100%;object-fit:cover;display:block}'
 '.pin-ov{position:absolute;left:8px;right:8px;bottom:10px;background:rgba(255,255,255,.92);color:#064587;border-radius:10px;padding:6px;font:400 15px/1.15 Caprasimo,serif}'
 '.pin-amz{background:linear-gradient(160deg,#b7312c,#7d1d1a)}.pin-ph{position:absolute;inset:10px 10px 70px;display:grid;grid-template-columns:1fr 1fr;gap:6px}.pin-ph span{background:rgba(255,255,255,.85);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:26px}'
 '.pin-t{font-weight:700;font-size:14px;margin-top:6px}.pin-a{color:var(--pink);font-size:22px;font-weight:700;line-height:1.1}'
 '.pin-d{border:1px solid;border-radius:10px;padding:8px;font-size:14px}'
 '</style>')

JS = ('<script>(function(){const ID=' + json.dumps(ID) + ',IMG=' + json.dumps(PAPD) + ',H=' + json.dumps(TPL) + '.split("__PAP__").join(IMG);'
 'function inject(){const el=document.querySelector(\'.item[data-id="\'+ID+\'"]\');if(!el||el.querySelector(".tp"))return;const d=el.querySelector(".desc");if(!d)return;const w=document.createElement("div");w.innerHTML=H;d.replaceWith(w.firstElementChild);'
 'const bs=el.querySelector(".btns");if(bs){bs.innerHTML=\'<button class="yes" data-v="ok" type="button">Approve template</button><button class="no" data-v="no" type="button">Change something</button>\'}'
 'const ta=el.querySelector("textarea");if(ta)ta.placeholder="What should change? (optional)"}'
 'inject();setInterval(inject,1500);})();</script>')

new_look = ["Template: how a look gets shopped (Papaya Spritz example)", "", "", ID]
assert s.count('LOOK=[[') == 1
s = s.replace('LOOK=[[', 'LOOK=[' + json.dumps(new_look) + ',[', 1)
old = 'NOW=["h-social", "s2-trailer", "s2-ep06", "s2-ep08", "s2-ep13", "s2-sched", "h-rest",'
assert s.count(old) == 1
s = s.replace(old, old + '"' + ID + '",', 1)
i = s.rfind('</body>')
s = s[:i] + CSS + JS + s[i:]
open(OUT, 'w', encoding='utf-8').write(s)
print('ok', len(s))
