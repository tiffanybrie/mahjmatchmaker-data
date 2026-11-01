"""v112b: In-stock toggle (Tiffany Nov 1 12:04am) + v111 QA notes (account sheet headings).
- Data: config/fym-stock.json (scripts/fym_stock_check.py) -> M/R .oos=1, tiles T.so=1 + T.oos=1 for sold-out (store says unavailable);
  retired (rt) always counts as sold out. D.stk = 'Mon D' of the check.
- UI: 'In stock only' chip (default off = All) by the colour filters: tiles door mats (filters('m')), racks (filters('r')),
  mat door (doorChips). Small 'Stock checked Nov 1'. Decks (matDeck / rackDeck / doorMats / setsForMat) drop sold-out items
  only while the chip is on; if that would empty a deck, the full deck stays and 'No in-stock matches here, so showing all.' shows.
- Badges: 'Sold out' on mat / rack cards and tile cards. Shop list: 'Sold out ›' only for real sold-out flags (fixes the old
  bug where mats with a set-order array in .so read 'Sold out').
- Account sheet <h2> headings in Caprasimo (v111 QA note).
Usage: python3 ui112b.py <build dir>"""
import sys, os, json, datetime
B = sys.argv[1]; R0 = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
p = B + '/index.html'; h = open(p).read()
i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:])
st = json.load(open(os.path.join(R0, 'config/fym-stock.json'))); n = {'m': 0, 'r': 0, 't': 0}
for key, v in st['items'].items():
    k, id_ = key.split(':', 1); o = {'m': D['mats'], 'r': D['racks'], 't': D['tiles']}[k].get(id_)
    if o is None or v['in']: continue
    o['oos'] = 1; n[k] += 1
    if k == 't': o['so'] = 1
d = datetime.date.fromisoformat(st['checked']); D['stk'] = d.strftime('%b ') + str(d.day)
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[i + e:]
def rep(a, b, cnt=1):
    global h
    assert h.count(a) == cnt, (h.count(a), a[:80]); h = h.replace(a, b)
HELP = ("/*v112 in-stock*/function OOS(k,id){const o=k==='m'?M[id]:k==='r'?R[id]:T[id];return !!(o&&(o.oos||o.rt));}"
        "function INSF(k,ids){if(!S.ins)return ids;const f=ids.filter(x=>!OOS(k,x));if(!f.length&&ids.length){S.insE=1;return ids;}return f;}"
        "function INSG(g){if(!S.ins)return g;const f=a=>(a||[]).filter(r=>!OOS('t',r.s.tile));const n=Object.assign({},g,{her:f(g.her),alb:f(g.alb),cat:f(g.cat)});"
        "if(!(n.her.length+n.alb.length+n.cat.length)&&((g.her||[]).length+(g.alb||[]).length+(g.cat||[]).length)){S.insE=1;return g;}return n;}"
        "function INSB(k){S.insE=0;try{(k==='d'?doorMats:k==='r'?rackDeck:matDeck)();}catch(x){}"
        "return `<div class=\"insw\"><button type=\"button\" class=\"chip insb\" data-ins aria-pressed=\"${!!S.ins}\">${S.ins?'\\u2713 ':''}In stock only</button><small>Stock checked ${esc(D.stk||'')}</small>${S.ins&&S.insE?'<small class=\"inse\">No in-stock matches here, so showing all.</small>':''}</div>`;}\n")
rep('function matDeck(){', HELP + "function matDeck(){return INSF('m',matDeck0());}function matDeck0(){")
rep('function rackDeck(){', "function rackDeck(){return INSF('r',rackDeck0());}function rackDeck0(){")
rep('function doorMats(){', "function doorMats(){return INSF('m',doorMats0());}function doorMats0(){")
rep('function setsForMat(id){', "function setsForMat(id){return INSG(setsForMat0(id));}function setsForMat0(id){")
rep('return `<div class="frow" role="group" aria-label="Filters">', 'return INSB(k)+`<div class="frow" role="group" aria-label="Filters">')
j = h.index('function doorChips(){'); e2 = h.index('\n', j); body = h[j:e2]; assert body.endswith("+`</div>`;}"), body[-40:]
h = h[:j] + body[:-len("`</div>`;}")] + "INSB('d')+`</div>`;}" + h[e2:]
rep("if(b=q('[data-dfam]'))", "if(b=q('[data-ins]')){S.ins=!S.ins;trk('instock',{on:S.ins});try{DOOR.lim=36;}catch(x){}renderTiles();renderMats();renderRacks();return;}/*v112 in-stock*/\n   if(b=q('[data-dfam]'))")
rep("${o.rt&&!/retired/i.test(o.n)?' · retired':''}", "${o.rt&&!/retired/i.test(o.n)?' · retired':''}${o.oos&&!o.rt?' · <b class=\"sob\">Sold out</b>':''}")
rep('<div class="tx"><b>${esc(s.name)}</b><span>${esc(s.maker)}</span></div>${peek?\'\':STB(\'t\',s.slug)}',
    '<div class="tx"><b>${esc(s.name)}</b><span>${esc(s.maker)}${(T[s.tile]||{}).oos?\' · <b class="sob">Sold out</b>\':\'\'}</span></div>${peek?\'\':STB(\'t\',s.slug)}')
rep("o.so?'Sold out ›':'Shop ›'", "(o.oos||(o.so&&!Array.isArray(o.so)))?'Sold out ›':'Shop ›'")
CSS = ("\n.insw{display:flex;flex-wrap:wrap;align-items:center;gap:4px 10px;margin:6px 0 8px}.insw small{font:400 12px var(--body);color:var(--mute)}"
       ".insw .inse{flex-basis:100%;color:#c8325f;font-weight:700}.chip.insb[aria-pressed=\"true\"]{background:#1f3a6b;color:#fff;border-color:#1f3a6b}"
       ".sob{color:#c8325f;font-weight:700}\n#starsov .ac h2{font:400 26px/1.15 Caprasimo,Georgia,serif;color:var(--navy);margin:6px 0 10px;letter-spacing:.2px}\n")
rep('#starsov .ac{max-width:440px;margin:0 auto}', '#starsov .ac{max-width:440px;margin:0 auto}' + CSS)
open(p + '.tmp', 'w').write(h); os.remove(p); os.rename(p + '.tmp', p)
print('ui112b: sold out mats', n['m'], 'racks', n['r'], 'tiles', n['t'], 'stock date', D['stk'])
