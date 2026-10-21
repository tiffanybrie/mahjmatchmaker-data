"""FYM v71 UI part 3 (Tiffany 6:44pm test). Run after v71_ui2.py. Usage: python3 builder/fym_fix_oct21/v71_ui3.py <build_dir>
 - "Holiday" chip in the mat colour filters (tiles-door deck + mat-door chips): Holiday = hol || wfh (also_year_round mats are hol);
   combined with colours it uses the holiday combo colours (ha) like the gallery
 - racks step: "Pick 2 racks" up front; the Your racks tray (2 slots) sits right under the mat, above the swipe deck, so the
   preview IS the tray; the swipe card is labelled "Browsing" so it never looks chosen; search picks land in the tray
 - "Photo coming soon" tile card (T[tile].soon): brand-style card with the set name, still selectable"""
import sys, json
B = sys.argv[1]; P = B + '/index.html'
h = open(P).read(); i = h.index('const D=') + 8
_, end = json.JSONDecoder().raw_decode(h[i:]); end += i
H, data, t = h[:i], h[i:end], h[end:]
def rep(s, a, b, n=1):
    c = s.count(a); assert c == n, (c, a[:100]); return s.replace(a, b)

H = rep(H, ".sheet .box p{margin:0 0 12px;color:var(--mute);font-size:14px;line-height:1.4}\n</style>",
        ".sheet .box p{margin:0 0 12px;color:var(--mute);font-size:14px;line-height:1.4}\n.chip.holc{border-color:#c8202f;color:#a3192e}.chip.holc[aria-pressed=\"true\"]{background:linear-gradient(135deg,#c8202f 50%,#1f6b3a 50%);color:#fff;border-color:#a3192e}\n.deck.r .peekbar span{background:#7a6a85}\n</style>")
# holiday chip (deck filter + mat door)
t = rep(t, "function matDeck(){const f=S.f.m;let ids=MSL(matPool());if(f.her)ids=ids.filter(herMat);if(f.fam.length){const C=f.fam;ids=ids.filter(id=>HASC(id,C));ids=[...ids.filter(herMat),...CSORT(ids.filter(id=>!herMat(id)),C)];}",
        "const isHolM=id=>!!(M[id]&&(M[id].hol||M[id].wfh));/* v71: Holiday chip = hol || wfh (also_year_round mats are hol) */\nfunction matDeck(){const f=S.f.m;let ids=MSL(matPool());if(f.her)ids=ids.filter(herMat);if(f.fam.length){const HF=f.fam.includes('holiday'),C=f.fam.filter(c=>c!=='holiday');if(HF)ids=ids.filter(isHolM);if(C.length){ids=ids.filter(id=>HF?C.every(c=>MTI(id,c)<9):HASC(id,C));ids=[...ids.filter(herMat),...CSORT(ids.filter(id=>!herMat(id)),C)];}}")
t = rep(t, "function doorMats(){const c=matCounts();let ids=Object.keys(M).filter(id=>!M[id].hid&&(!M[id].rt||c[id]));const C=S.dfams||[];if(C.length)ids=ids.filter(id=>HASC(id,C));\n ids=MSL(ids.sort((a,b)=>(c[b]||0)-(c[a]||0)||M[a].n.localeCompare(M[b].n)));return C.length?CSORT(ids,C):ids;}",
        "function doorMats(){const c=matCounts();let ids=Object.keys(M).filter(id=>!M[id].hid&&(!M[id].rt||c[id]));const C0=S.dfams||[],HF=C0.includes('holiday'),C=C0.filter(x=>x!=='holiday');if(HF)ids=ids.filter(isHolM);if(C.length)ids=ids.filter(id=>HF?C.every(x=>MTI(id,x)<9):HASC(id,C));\n ids=MSL(ids.sort((a,b)=>(c[b]||0)-(c[a]||0)||M[a].n.localeCompare(M[b].n)));return C.length?CSORT(ids,C):ids;}")
t = rep(t, "<button type=\"button\" class=\"dot\" data-fam=\"\" data-k=\"${k}\" aria-pressed=\"${!f.fam.length}\" title=\"All colors\" aria-label=\"All colors\"><i style=\"background:${RAINBOW}\"></i></button>",
        "<button type=\"button\" class=\"dot\" data-fam=\"\" data-k=\"${k}\" aria-pressed=\"${!f.fam.length}\" title=\"All colors\" aria-label=\"All colors\"><i style=\"background:${RAINBOW}\"></i></button>${k==='m'&&pool.some(isHolM)?`<button type=\"button\" class=\"chip holc\" data-fam=\"holiday\" data-k=\"m\" aria-pressed=\"${f.fam.includes('holiday')}\">Holiday</button>`:''}")
t = rep(t, "if(b=q('.frow [data-fam]')){", "if((b=q('.frow [data-fam]'))||(b=q('[data-fam=\"holiday\"]'))){")
t = rep(t, "+FAMS.map(f=>`<button type=\"button\" data-dfam=\"${f}\" aria-pressed=\"${(S.dfams||[]).includes(f)}\" style=\"--c:${FAMC[f]}\">${FAMN[f]}</button>`).join('')+`</div>`;}",
        "+`<button type=\"button\" data-dfam=\"holiday\" aria-pressed=\"${(S.dfams||[]).includes('holiday')}\" style=\"--c:#a3192e\">Holiday</button>`+FAMS.map(f=>`<button type=\"button\" data-dfam=\"${f}\" aria-pressed=\"${(S.dfams||[]).includes(f)}\" style=\"--c:${FAMC[f]}\">${FAMN[f]}</button>`).join('')+`</div>`;}")
# racks step: Pick 2 up front, tray right under the mat (the preview), browsing label on the deck card
t = rep(t, "el.innerHTML=head(3,'Love triangle','All couples need a wingman. '+(queue('r').length>1?'Swipe on racks.':'Tap \\u2665 on the racks you like.'))+filters('r')+\n `<div class=\"cmp\">${tileView('r')}<div class=\"matv\"><img src=\"${matSrc(S.fav)}\" alt=\"${esc(m.n)}\" class=\"${m.c?'':'photo'}\" data-lbx=\"${esc(S.fav)}\"><button type=\"button\" class=\"chip mini\" data-back-mats>Change mat</button><button type=\"button\" class=\"xz\" data-lbx=\"${esc(S.fav)}\" aria-label=\"See this mat full screen\">⤢</button></div>${deck('r')}</div>`+herBar('r')+acts('r')+tray('r');",
        "el.innerHTML=head(3,'Pick 2 racks','All couples need a wingman. '+(queue('r').length>1?'Swipe on racks below; your first 2 hearts fill these slots.':'Tap \\u2665 on the racks you like.'))+\n `<div class=\"cmp\">${tileView('r')}<div class=\"matv\"><img src=\"${matSrc(S.fav)}\" alt=\"${esc(m.n)}\" class=\"${m.c?'':'photo'}\" data-lbx=\"${esc(S.fav)}\"><button type=\"button\" class=\"chip mini\" data-back-mats>Change mat</button><button type=\"button\" class=\"xz\" data-lbx=\"${esc(S.fav)}\" aria-label=\"See this mat full screen\">⤢</button></div></div>`+tray('r')+filters('r')+`<div class=\"cmp\">${deck('r')}</div>`+herBar('r')+acts('r');")
t = rep(t, " return `<div class=\"deck ${k}\">${q[1]?card(q[1],k,true):''}${card(q[0],k)}</div>`;}",
        " return `<div class=\"deck ${k}\">${k==='r'?'<div class=\"peekbar\"><span>Browsing racks</span></div>':''}${q[1]?card(q[1],k,true):''}${card(q[0],k)}</div>`;}")
# photo coming soon tile card
t = rep(t, "pile=s=>IMG[T[s.tile].pile];", "pile=s=>T[s.tile].soon?SOON(s):IMG[T[s.tile].pile];")
t = rep(t, "const tileFull=s=>T[s.tile].full||pile(s);", "const tileFull=s=>T[s.tile].soon?SOON(s,1):(T[s.tile].full||pile(s));")
t = rep(t, "const IMG=window.IMG||{};", """const IMG=window.IMG||{};
/* v71: "Photo coming soon" tile card (T[tile].soon), brand style, still selectable */
const SOONC={};function SOON(s,wide){const k=s.slug+(wide?'w':'');if(SOONC[k])return SOONC[k];const x=v=>String(v).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));const w=wide?800:400,hh=wide?350:400,ws=String(s.name).split(/\\s+/),L=[''];ws.forEach(q=>{if((L[L.length-1]+' '+q).trim().length>(wide?22:13)&&L[L.length-1])L.push(q);else L[L.length-1]=(L[L.length-1]+' '+q).trim();});const ln=L.slice(0,3),fs=wide?58:(ln.some(l=>l.length>10)?48:60),y0=hh/2-(ln.length-1)*fs*.55-14;
 const svg=`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${hh}"><rect width="${w}" height="${hh}" fill="#f6e9df"/><rect x="12" y="12" width="${w-24}" height="${hh-24}" rx="26" fill="none" stroke="#ecd5df" stroke-width="4" stroke-dasharray="10 8"/>${ln.map((l,j)=>`<text x="${w/2}" y="${y0+j*fs*1.1}" text-anchor="middle" font-family="Alfa Slab One, Georgia, serif" font-weight="700" font-size="${fs}" fill="#c8325f">${x(l)}</text>`).join('')}<text x="${w/2}" y="${y0+(ln.length-1)*fs*1.1+fs*.95}" text-anchor="middle" font-family="Bitter, Georgia, serif" font-weight="700" font-size="${wide?26:24}" letter-spacing="2" fill="#7a6a85">PHOTO COMING SOON</text><text x="${w/2}" y="${hh-34}" text-anchor="middle" font-family="Bitter, Georgia, serif" font-size="${wide?22:22}" fill="#054689">${x(s.maker||'')}</text></svg>`;
 return SOONC[k]='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(svg);}""")
open(P, 'w').write(H + data + t)
print('v71 ui3 patched')
