"""FYM round 2f (Tiffany Nov 23 7:24pm + 7:14pm): match card views = Table view, Aerial (was Mood board),
Close up, Phone view (the table inside a white phone); the J in set names gets room; the tour points to
'Make my match card' (Adjust is gone). Usage: python3 r2_cards.py <index.html>  (edits in place, idempotent)."""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
if 'R2CARDS' in s:
    print('already applied'); sys.exit()

def rep(old, new, n=1):
    global s
    assert s.count(old) >= 1, old[:80]
    s = s.replace(old, new, n)

# 1. expose the table renderer to the match-card script
rep("/* QA / gate hook: one table, no UI (corner = as the app shows it) */",
    "/* QA / gate hook: one table, no UI (corner = as the app shows it) */"
    "window.R2TVURL=(mat,slug,rack,rack2,N)=>tableURL({mat,s:D.sets.find(x=>x.slug===slug),rack,rack2:rack2||null,corner:matCls(mat)==='B'},N);window.R2TVCLS=matCls;/*R2CARDS*/")

# 2. views
rep("const VIEWS=[['tri','Mood board'],['stack','Close up']];",
    "const VIEWS=[['table','Table view'],['tri','Aerial'],['stack','Close up'],['phone','Phone view']];/*R2CARDS*/")
rep("if(!VIEWS.some(v=>v[0]===S.view))S.view='tri';", "if(!VIEWS.some(v=>v[0]===S.view))S.view='table';")
rep("${VIEWS.map(v=>`<button type=\"button\" data-view=",
    "${VIEWS.filter(v=>!(/^(table|phone)$/.test(v[0])&&window.R2TVCLS&&window.R2TVCLS(S.fav)==='C')).map(v=>`<button type=\"button\" data-view=")

# 3. load the table image before drawing
rep(" if(job!==cardJob)return;\n const [wmn,seal]=",
    " if(job!==cardJob)return;\n if(/^(table|phone)$/.test(S.view)&&window.R2TVCLS&&window.R2TVCLS(S.fav)==='C')S.view='tri';\n"
    " let tvim=null;if(/^(table|phone)$/.test(S.view)&&window.R2TVURL){try{tvim=await lk(await window.R2TVURL(S.fav,s.slug,S.rpick[0]||null,S.rpick[1]||null,1600));}catch(e){tvim=null;}if(job!==cardJob)return;}\n"
    " const [wmn,seal]=")

# 4. the two new views
TV = r"""if(/^(table|phone)$/.test(S.view)&&tvim){ // R2CARDS: Table view + Phone view
  const top=y+26,bot=fby-14,ah=bot-top;
  if(S.view==='table'){const sq=Math.min(W-72,ah),sx=(W-sq)/2,sy=top+(ah-sq)/2;card(sx,sy,sq,sq,24);cover(tvim,sx,sy,sq,sq,24);
   pill(sx+16,sy+sq-14,'MAT',mName,{up:true,maxW:sq*.55,fsN:20,fsK:12});logoChip(ml,mb,sx+sq-14,sy+14,56,{right:true,maxW:220});if(tb!==mb)logoChip(tl,tb,sx+14,sy+14,56,{maxW:220});}
  else{const ph=ah,pw=Math.min(W*.62,ph*.56),px=(W-pw)/2,py=top,rr=pw*.15,b=pw*.04,sx=px+b,sy=py+b,sw=pw-2*b,sh=ph-2*b;
   g.save();shadow('rgba(40,20,30,.28)',30,14);g.fillStyle='#f3f3f5';g.beginPath();g.roundRect(px,py,pw,ph,rr);g.fill();g.restore();
   g.strokeStyle='#d6d6dc';g.lineWidth=3;g.beginPath();g.roundRect(px,py,pw,ph,rr);g.stroke();
   g.save();g.beginPath();g.roundRect(sx,sy,sw,sh,rr-b);g.clip();g.fillStyle='#fff';g.fillRect(sx,sy,sw,sh);
   g.fillStyle='#fbf1ec';g.fillRect(sx,sy,sw,sh*.15);g.textAlign='center';g.fillStyle=NAVY;g.font=`${Math.round(sw*.085)}px Caprasimo, Georgia, serif`;g.fillText('Find Your Mat-ch™',sx+sw/2,sy+sh*.115);
   const tq=sw-28,ty=sy+sh*.18;cover(tvim,sx+14,ty,tq,tq,18);
   g.fillStyle=INK;g.font=`600 ${Math.round(sw*.06)}px Bitter, Georgia, serif`;g.fillText(clip(s.name+' tiles',sw-36),sx+sw/2,ty+tq+sw*.1);
   g.fillStyle=MUTE;g.font=`italic 500 ${Math.round(sw*.052)}px "Playfair Display", Georgia, serif`;g.fillText(clip('on '+mName,sw-36),sx+sw/2,ty+tq+sw*.18);
   g.fillStyle=PINK;g.beginPath();g.roundRect(sx+sw*.2,ty+tq+sw*.25,sw*.6,sw*.13,sw*.065);g.fill();g.fillStyle='#fff';g.font=`700 ${Math.round(sw*.05)}px Bitter, Georgia, serif`;g.fillText('Make my match card ♥',sx+sw/2,ty+tq+sw*.335);
   g.restore();g.fillStyle='#121212';g.beginPath();g.roundRect(px+pw/2-pw*.14,sy+pw*.025,pw*.28,pw*.065,pw*.033);g.fill();}
 }else if(S.view==='stack'){ // Mood board: stacked close-ups"""
rep(" if(S.view==='stack'){ // Mood board: stacked close-ups", " " + TV)

# 5. Caprasimo capital J/Q drop below the line: give that line room so it never runs into the subtitle
rep("g.fillStyle=tc;g.fillText(l,W/2,y);});", "g.fillStyle=tc;g.fillText(l,W/2,y);if(/[JQ]/.test(l))y+=fs*.16;});")

# 6. tour: Adjust is gone; point to Make my match card
i = s.find("{k:'tv2',"); j = s.find("\n", i)
s = s[:i] + "{k:'tv2',t:'Make my match card',p:'Love what’s on the table? Tap Make my match card to finish, or keep swiping.',b:'#s-mats [data-r2make]',next:'Next',skip:()=>S.mode!=='table'||!document.querySelector('#s-mats [data-r2make]')}," + s[j:]
rep("Up close, Table or Aerial: tap one, or Next to stay.", "Table, Up close or Aerial: tap one, or Next to stay.")

open(p, 'w', encoding='utf-8').write(s); print('ok')
