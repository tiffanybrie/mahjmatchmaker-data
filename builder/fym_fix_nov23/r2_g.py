"""FYM round 2g (Tiffany Nov 23 8:30pm test): racks are remembered PER MAT whether or not it was hearted (switch mats and
back, the table shows the racks you last had on that mat); match card: racks labelled on Table view, story size lists
'On the table'; Phone view = a real white iPhone. Usage: python3 r2_g.py <index.html> (in place, idempotent)."""
import sys
p = sys.argv[1]; s = open(p, encoding='utf-8').read()
if 'R2GV1' in s: print('already applied'); sys.exit()
def rep(old, new):
    global s
    assert old in s, old[:90]; s = s.replace(old, new, 1)
rep("window.R2GETFACES=()=>TV.faces;", "window.R2GETFACES=()=>TV.faces;window.R2GETRACK=()=>TV.rack||null;/*R2GV1*/")
rep("let lastPeek=null;function peekRacks(){if(S.peek!==lastPeek){lastPeek=S.peek;const r=S.peek&&S.r2rk&&S.r2rk[S.peek];if(r&&r[0]&&window.R2SETRACK)window.R2SETRACK(r[0])}}",
    "let r2cur=null,r2rack;function peekRacks(){if(!document.body.classList.contains('tvmode')||!window.R2GETRACK)return;const c=document.querySelector('#s-mats .scard[id^=\"top-\"]');const x=c&&window.R2CTX(c);if(!x||!x.mat)return;S.r2rk=S.r2rk||{};"
    "if(x.mat!==r2cur){r2cur=x.mat;const m=S.r2rk[x.mat];if(typeof m==='string'&&m!==window.R2GETRACK()){window.R2SETRACK(m)}else if(m===undefined){S.r2rk[x.mat]=window.R2GETRACK()}r2rack=typeof m==='string'?m:window.R2GETRACK();return}"
    "const now=window.R2GETRACK();if(now!==r2rack){r2rack=now;S.r2rk[x.mat]=now}}")
# the old heart-only save stored arrays; drop it (per-mat memory now covers every mat)
rep("if(x&&x.mat){S.r2rk=S.r2rk||{};S.r2rk[x.mat]=[x.rack,x.rack2].filter(Boolean)}", "")


rep("let tvim=null;if(/^(table|phone)$/.test(S.view)&&window.R2TVURL){try{tvim=", "let tvim=null,lockup=null;if(/^(table|phone)$/.test(S.view)&&window.R2TVURL){try{if(S.view==='phone')lockup=await lk('https://cdn.jsdelivr.net/gh/tiffanybrie/mahjmatchmaker-data@1d194bd43b581f40d31bd0a5e2d71d510a7d4284/assets/brand/fym-lockup/find-your-mat-ch-lockup.png');tvim=")
# ---- match card: Table view gets rack labels; story/pin add an 'On the table' list; real phone
old_tbl = "logoChip(ml,mb,sx+sq-14,sy+14,56,{right:true,maxW:220});if(tb!==mb)logoChip(tl,tb,sx+14,sy+14,56,{maxW:220});}"
rep(old_tbl, "logoChip(ml,mb,sx+sq-14,sy+14,56,{right:true,maxW:220});if(tb!==mb)logoChip(tl,tb,sx+14,sy+14,56,{maxW:220});"
    "const rn=rp.map(r=>R[r]?(R[r].bn+' '+String(R[r].n).replace(new RegExp('^'+R[r].bn+'\\\\s*'),'')):'').filter(Boolean);"
    "if(rn.length&&!(H/W>1.3)){pill(sx+sq-16,sy+sq-14,'RACKS',rn.join(' + '),{up:true,right:true,maxW:sq*.42,fsN:18,fsK:12});}"
    "if(H/W>1.3){let ly=sy+sq+44;g.textAlign='left';g.fillStyle=PINK;g.font='700 22px Bitter, Georgia, serif';ls(3);g.fillText('ON THE TABLE',60,ly);ls(0);ly+=46;"
    "const rows=[['Tiles',s.name+(tb?' · '+tb:'')],['Mat',mName+(mb?' · '+mb:'')]].concat(rn.map((r,i)=>[rn.length>1?(i?'Racks (sides)':'Racks (ends)'):'Racks',r]));"
    "rows.forEach(([k,v])=>{if(ly>fby-8)return;g.fillStyle=MUTE;g.font='700 24px Bitter, Georgia, serif';g.fillText(k,60,ly);g.fillStyle=INK;g.font='600 28px Bitter, Georgia, serif';g.fillText(clip(v,W-300),230,ly);ly+=44;});}}")
# make the table square smaller on story so the list fits
rep("if(S.view==='table'){const sq=Math.min(W-72,ah),sx=(W-sq)/2,sy=top+(ah-sq)/2;", "if(S.view==='table'){const sq=Math.min(W-72,H/W>1.3?ah-250:ah),sx=(W-sq)/2,sy=H/W>1.3?top+10:top+(ah-sq)/2;")

# phone view: a real white iPhone (concentric corners, black glass bezel, titanium band, Dynamic Island, buttons)
i = s.find("  else{const ph=ah,pw="); j = s.find("}\n }else if(S.view==='stack')", i)
assert i > 0 and j > 0
PHONE = r"""  else{/* R2GV1 phone (Tiffany 8:32pm): a real white iPhone, big, running off the bottom; inside: FYM logo, the table, what is on it, matched-with + code */
   const pw=Math.min(W*.86,W-96),px=(W-pw)/2,py=STORY?290:44,ph=pw*2.06,fr=pw*.018,bz=pw*.028,R0=pw*.16;
   g.fillStyle=CREAM;g.fillRect(0,0,W,H);/* the phone IS the card: header + footer move inside it */
   g.save();shadow('rgba(30,30,50,.28)',36,14);g.fillStyle='#ececef';g.beginPath();g.roundRect(px,py,pw,ph,R0);g.fill();g.restore();
   const gr=g.createLinearGradient(px,py,px+pw,py);gr.addColorStop(0,'#d9dade');gr.addColorStop(.12,'#f4f4f6');gr.addColorStop(.88,'#f4f4f6');gr.addColorStop(1,'#d4d5da');g.fillStyle=gr;g.beginPath();g.roundRect(px,py,pw,ph,R0);g.fill();
   g.fillStyle='#cdced2';[[-1,.15,.05],[-1,.22,.08],[-1,.32,.08],[1,.25,.12]].forEach(([sd,t,h])=>{g.beginPath();g.roundRect(sd<0?px-4:px+pw-2,py+ph*t,6,ph*h,3);g.fill();});
   g.fillStyle='#0b0b0d';g.beginPath();g.roundRect(px+fr,py+fr,pw-2*fr,ph-2*fr,R0-fr);g.fill();
   const sx=px+fr+bz,sy=py+fr+bz,sw=pw-2*(fr+bz),sr=R0-fr-bz,sh=H-sy+40;
   g.save();g.beginPath();g.roundRect(sx,sy,sw,ph,sr);g.clip();g.fillStyle='#fff';g.fillRect(sx,sy,sw,sh);
   const f=n=>Math.round(n*sw/880);g.fillStyle='#111';g.textAlign='center';g.font=`600 ${f(30)}px -apple-system, Helvetica, Arial, sans-serif`;g.fillText('9:41',sx+f(110),sy+f(58));
   [[0,14],[1,20],[2,26],[3,32]].forEach(([i,h])=>g.fillRect(sx+sw-f(190)+i*f(12),sy+f(62)-f(h),f(8),f(h)));g.strokeStyle='#111';g.lineWidth=f(3);g.beginPath();g.roundRect(sx+sw-f(120),sy+f(36),f(50),f(26),f(7));g.stroke();g.fillRect(sx+sw-f(115),sy+f(41),f(38),f(16));
   g.fillStyle='#050506';g.beginPath();g.roundRect(sx+sw/2-f(125),sy+f(22),f(250),f(66),f(33));g.fill();
   let yy=sy+f(108);if(lockup){const lh=f(64),lw=lockup.width*lh/lockup.height;g.drawImage(lockup,sx+(sw-lw)/2,yy,lw,lh);yy+=lh+f(26);}else{g.fillStyle=NAVY;g.font=`${f(54)}px Caprasimo, Georgia, serif`;g.fillText('Find Your Mat-ch™',sx+sw/2,yy+f(52));yy+=f(84);}
   const textH=f(300),tq=Math.max(f(420),Math.min(sw-f(36),(STORY?H-400:H)-yy-textH));cover(tvim,sx+(sw-tq)/2,yy,tq,tq,f(26));yy+=tq+f(46);
   const rn=rp.map(r=>R[r]?(R[r].bn+' '+String(R[r].n).replace(new RegExp('^'+R[r].bn+'\\s*'),'')):'').filter(Boolean);
   const ln=(t,fnt,col)=>{g.font=fnt;g.fillStyle=col;g.fillText(clip(t,sw-f(70)),sx+sw/2,yy);};
   ln(`${s.name} tiles`+(tb?` · ${tb}`:''),`700 ${f(36)}px Bitter, Georgia, serif`,INK);yy+=f(46);
   ln(`on the ${mName} mat`+(mb?` · ${mb}`:''),`italic 500 ${f(32)}px "Playfair Display", Georgia, serif`,'#4a3d58');yy+=f(44);
   if(rn.length){ln('with '+rn.join(' + ')+' racks',`500 ${f(28)}px Bitter, Georgia, serif`,MUTE);yy+=f(52);}
   if(icon){const ih=f(40),iw=icon.width*ih/icon.height;g.font=`700 ${f(28)}px Bitter, Georgia, serif`;const t1='Matched with Find Your Mat-ch™';const tw=g.measureText(t1).width;const x0=sx+(sw-(iw+f(12)+tw))/2;g.drawImage(icon,x0,yy-ih+f(8),iw,ih);g.textAlign='left';g.fillStyle=NAVY;g.fillText(t1,x0+iw+f(12),yy);g.textAlign='center';yy+=f(30);}
   const ct=codeLine();if(ct&&yy+f(70)<H){g.fillStyle=NAVY;const bw=Math.min(sw-f(80),f(620));g.beginPath();g.roundRect(sx+(sw-bw)/2,yy,bw,f(62),f(31));g.fill();g.fillStyle='#fff';g.font=`700 ${f(30)}px Bitter, Georgia, serif`;g.fillText(clip(ct,bw-f(40)),sx+sw/2,yy+f(41));}
   g.restore();"""
s = s[:i] + PHONE + s[j:]
open(p, 'w', encoding='utf-8').write(s); print('ok')
