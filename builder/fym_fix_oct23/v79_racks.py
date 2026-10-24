"""FYM v79 (Tiffany Oct 23 3:55pm + 8:01pm + 8:35-8:37pm, "go ahead and start building the rack changes").
Racks mirror the mats:
 1. Hearting a rack never picks it (it only becomes a rack suitor). Nothing is preselected.
 2. Tapping a rack suitor shows it on the deck right under the mat; a second pick splits the frame into both racks.
    Max 2. While racks are picked the deck is locked (no swiping): "Tap a check to unpick it and keep swiping".
 3. Notes: "Pick 1 or 2 racks for your mock-up" / "1 of 2 picked..." / "2 of 2 picked. Tap a check to unpick it."
    "swipe for more" hint once the suitor row overflows.
 4. Heading back to "Make it a love triangle" with "Pick your racks" under it (no "All couples need a wingman").
 5. Tiffany's picks OFF on racks = colour ranking only (her racks + goes-with-everything mixed in by score);
    a non-partner rack is never ranked ahead of a partner rack. ON = her racks + goes-with-everything, as before.
 6. Mat screen: a tapped suitor shows "Back to the deck to keep swiping" and "Remove from suitors" (she got stuck).
 7. Tour: step 1 text; racks split into "Swipe the racks" + "Pick 1 or 2 racks" (9 steps); step 7 text.
Usage: python3 v79_racks.py <build_dir>"""
import sys
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
def rep(old, new, n=1):
    global h
    c = h.count(old); assert c == n, f'expected {n} x {old[:100]!r}, found {c}'; h = h.replace(old, new)

# 1. no auto-pick on heart
rep("if(yes&&!S.rliked.includes(id)){S.rliked.push(id);if(S.rpick.length<2)S.rpick.push(id);}renderRacks();}}",
    "if(yes&&!S.rliked.includes(id))S.rliked.push(id);renderRacks();}}")

# 2. picked racks shown on the deck, deck locked while picked
rep("function deck(k){const q=queue(k);",
    "function rpickView(){const P=S.rpick.filter(id=>R[id]);return `<div class=\"deck r\"><div class=\"peekbar\"><span>${P.length===2?'Your 2 racks':'Your rack'}</span></div><div class=\"scard rk rpv n${P.length}\" id=\"rpv\">${P.map(id=>`<div class=\"rpi\"><img src=\"${rackSrc(id)}\" alt=\"${esc(R[id].n)}\" draggable=\"false\"><span>${esc(shortR(id))} \\u00b7 ${esc(R[id].bn)}</span></div>`).join('')}</div></div>`;}\n"
    "function deck(k){if(k==='r'&&S.rpick.length)return rpickView();const q=queue(k);")
rep("function acts(k){if(k==='m'&&S.peek)return `<div class=\"acts\"><button type=\"button\" class=\"pill\" data-unpeek>‹ Back to the deck</button></div>`;",
    "function acts(k){if(k==='m'&&S.peek)return `<div class=\"acts pk\"><button type=\"button\" class=\"pill\" data-unpeek>‹ Back to the deck to keep swiping</button><button type=\"button\" class=\"pill gh\" data-unlike=\"${esc(S.peek)}\">✕ Remove from suitors</button></div>`;\n"
    " if(k==='r'&&S.rpick.length)return `<div class=\"acts pk\"><p class=\"rlock\">Tap a \\u2713 rack below to unpick it and keep swiping.</p></div>`;")

# 3. rack tray notes + more hint
rep("<div class=\"tray rtr\" id=\"rtray\"><div class=\"tl\"><b>${L.length}</b>${L.length===1?'suitor':'suitors'}</div>",
    "<div class=\"tray rtr\" id=\"rtray\"><div class=\"tl\"><b>${L.length}</b>${L.length===1?'suitor':'suitors'}${L.length>3?'<span class=\"more\">swipe for more \\u203a</span>':''}</div>")
rep("on racks you like. Pick up to 2 for each mat; they wait here.</div>",
    "on racks you like. They\\u2019ll wait here so you can compare.</div>")
rep("${P.length===2?'2 of 2 picked: tap a \\u2713 rack to unpick it, then tap another to swap it in.':P.length+' of 2 picked: tap a rack suitor to pick it.'}",
    "${P.length===2?'2 of 2 picked. Tap a \\u2713 to unpick it.':P.length===1?'1 of 2 picked. Tap another suitor to see both, or Make it official.':'Pick 1 or 2 racks for your mock-up: tap a rack suitor to see it with your mat.'}")

# 4. headings
rep("head(3,'Pick your mat','All couples need a wingman.')", "head(3,'Make it a love triangle','First, pick your mat.')")
rep("head(3,'Rack-ing','All couples need a wingman. Tap \\u2665 if you love it, \\u2715 if it\\u2019s not the one')",
    "head(3,'Make it a love triangle','Pick your racks. Tap \\u2665 if you love it, \\u2715 if it\\u2019s not the one.')")

# 5. picks off = colour ranking, partners ahead of non-partners
rep(" const U=uni();const rest=Object.keys(R).filter(r=>!hr.includes(r)&&!U.includes(r)&&rackOK(r)).map(r=>[sc(r)+(R[r].lo?1e4:0),r]).sort((a,b)=>a[0]-b[0]).map(x=>x[1]);\n return [...new Set([...hr,...U,...rest])];}",
    " const U=uni();const pen=r=>(R[r].pa?0:1e5)+(R[r].lo?1e4:0);\n"
    " if(!S.f.r.her)return [...new Set([...hr,...U,...Object.keys(R).filter(rackOK)])].filter(r=>R[r]).map(r=>[sc(r)+pen(r),r]).sort((a,b)=>a[0]-b[0]).map(x=>x[1]);\n"
    " const rest=Object.keys(R).filter(r=>!hr.includes(r)&&!U.includes(r)&&rackOK(r)).map(r=>[sc(r)+pen(r),r]).sort((a,b)=>a[0]-b[0]).map(x=>x[1]);\n return [...new Set([...hr,...U,...rest])];}")

# 6. remove a mat suitor
rep(" if(b=q('[data-rx]')){",
    " if(b=q('[data-unlike]')){const id=b.dataset.unlike;S.liked=S.liked.filter(x=>x!==id);if(S.peek===id)S.peek=null;if(S.fav===id){resetFrom(2);renderAll();}else{renderMats();renderRacks();}steps();toast('Removed from your suitors');return;}\n if(b=q('[data-rx]')){")

# 7. tour
rep("p:'Start with what you have: tap \\u201cI have tiles\\u201d or \\u201cI have a mat\\u201d, then pick yours just below.'",
    "p:'Start with what you have: tap \\u201cI have tiles\\u201d or \\u201cI have a mat\\u201d, then pick yours just below: shop by color or search a specific set.'")
rep(" {k:'racks',t:'Step 5 · Swipe the racks',p:'Same as the mats: \\u2665 or swipe right, \\u2715 or swipe left. Pick up to two rack suitors for each mat; they fall below.',b:'#top-r',hand:'r',done:()=>S.rpick.length>0},\n {k:'make',t:'Step 6 · Make it official',p:'Happy with your racks? Tap Make it official to build your match card.',b:'#rtray [data-make]',done:()=>!!S.made},\n {k:'share',t:'Step 7 · Save or share'",
    " {k:'racks',t:'Step 5 · Swipe the racks',p:'Same as the mats: \\u2665 or swipe right, \\u2715 or swipe left. Hearted racks fall below as your rack suitors. Own racks? Search yours under the suitors.',b:'#top-r',hand:'r',done:()=>S.rliked.length>0||S.rpick.length>0},\n"
    " {k:'rpick',t:'Step 6 · Pick 1 or 2 racks',p:'Tap a rack suitor to see it with your mat. Tap a second one to see both. Tap a \\u2713 to unpick it.',b:'#rtray .th button',done:()=>S.rpick.length>0},\n"
    " {k:'make',t:'Step 7 · Make it official',p:'Happy with your 1 or 2 racks? Tap Make it official to build your match card.',b:'#rtray [data-make]',done:()=>!!S.made},\n {k:'share',t:'Step 8 · Save or share'")
rep("{k:'shop',t:'Step 8 · Shop the look'", "{k:'shop',t:'Step 9 · Shop the look'")

# CSS
css = """.rpv{flex-direction:column;padding:22px 14px 8px;gap:6px}
.rpv .rpi{flex:1;min-height:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px}
.rpv .rpi img{flex:1;min-height:0;max-width:100%;object-fit:contain}
.rpv .rpi span{font:600 11px var(--body);color:var(--mute);text-align:center}
.acts.pk{padding-left:0;flex-wrap:wrap;gap:8px}
.rlock{margin:4px 0;font:600 13px var(--body);color:var(--navy);text-align:center}
.tl .more{display:block;font:600 10px var(--body);color:var(--mute);margin-top:2px}
.coach button.sk"""
rep(".coach button.sk", css)
open(P, 'w').write(h); print('v79 racks applied')
