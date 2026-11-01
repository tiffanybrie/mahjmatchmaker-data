"""v113 UI (Nov 1, Tiffany 4:50am):
 A. PER-BRAND CAP on colour-theory decks: BCAP(ids, keep, brandOf) only REORDERS (nothing is removed): in the first 30 cards no
    brand gets more than 6 and never two in a row while another brand is available; 'keep' items (her picks / her racks) are exempt.
    Applied in matDeck0 (tiles door step 2 mat deck; skipped when a brand is picked: brand view shows all its mats in order),
    setsForMat0 (mat door tile deck: album + catalog lists; her matches first, untouched) and rackDeck0 (her racks exempt).
    Searched mats (S.mfront) still jump to the front after the cap.
 B. Dapper explainer link (mat card + shop list) for mats with o.dfq: 'Not sure which Dapper? See the difference ›'. OFF until the
    site explainer exists (const DFQ=''): the link only renders when DFQ is set (Tiffany has to OK docs/drafts/dapper-1-vs-2.md first).
 C. Version 1.13.
Idempotent. Usage: python3 ui113.py <build_dir>"""
import sys, json
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
if '/*v113 brand cap*/' not in h:
    def rep(a, b, n=1):
        global h
        assert h.count(a) == n, (h.count(a), a[:100]); h = h.replace(a, b)
    BC = ("/*v113 brand cap*/const NOK=()=>false;function BCAP(ids,keep,bo){const out=[],pend=ids.slice(),cnt={},L=30,CAP=6;"
          "while(pend.length&&out.length<L){const last=out.length?bo(out[out.length-1]):null;"
          "let j=pend.findIndex(x=>keep(x)||((cnt[bo(x)]||0)<CAP&&bo(x)!==last));"
          "if(j<0)j=pend.findIndex(x=>keep(x)||(cnt[bo(x)]||0)<CAP);if(j<0)break;"
          "const x=pend.splice(j,1)[0];out.push(x);if(!keep(x)){const b=bo(x);cnt[b]=(cnt[b]||0)+1;}}return [...out,...pend];}"
          "const DFQ='';/*v113: Dapper explainer URL, set once the site page exists*/")
    rep('function matDeck0(){', BC + 'function matDeck0(){')
    rep("if(f.brand)ids=ids.filter(id=>M[id].bn===f.brand);if(S.mfront&&S.mfset===S.set",
        "if(!f.brand)ids=BCAP(ids,f.her?herMat:NOK,id=>M[id].bn);if(f.brand)ids=ids.filter(id=>M[id].bn===f.brand);if(S.mfront&&S.mfset===S.set")
    rep("cat=rows.filter(r=>!r.her&&r.s.cat&&ok(r)).sort((a,b)=>a.p-b.p);return {her,alb,cat};}",
        "cat=rows.filter(r=>!r.her&&r.s.cat&&ok(r)).sort((a,b)=>a.p-b.p);return {her,alb:BCAP(alb,NOK,r=>r.s.maker),cat:BCAP(cat,NOK,r=>r.s.maker)};}")
    rep("if(f.brand)ids=ids.filter(r=>R[r].bn===f.brand);/*v96 poor",
        "if(!f.brand)ids=BCAP(ids,r=>hr.includes(r),r=>R[r].bn);if(f.brand)ids=ids.filter(r=>R[r].bn===f.brand);/*v96 poor")
    # B
    rep("${mat&&o.alt?`<em class=\"alt\">${esc(o.alt)}</em>`:''}</div>",
        "${mat&&o.alt?`<em class=\"alt\">${esc(o.alt)}</em>`:''}${mat&&o.dfq&&DFQ?`<a class=\"dfq\" href=\"${esc(DFQ)}\" target=\"_blank\" rel=\"noopener\">Not sure which Dapper? See the difference ›</a>`:''}</div>")
    rep("${M[id]&&o.alt?`<em class=\"alt\">${esc(o.alt)}</em>`:''}",
        "${M[id]&&o.alt?`<em class=\"alt\">${esc(o.alt)}</em>`:''}${M[id]&&o.dfq&&DFQ?`<a class=\"dc\" href=\"${esc(DFQ)}\" target=\"_blank\" rel=\"noopener\">Not sure which Dapper? See the difference ›</a>`:''}")
    i = h.index('</style>'); h = h[:i] + '.dfq{display:block;font:600 12px var(--body);color:#1f3a6b;text-decoration:underline;margin-top:2px}' + h[i:]
# Dapper data + version (idempotent)
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
for k in ('www.ohmymahjong.com/dapper-mat-w-tube', 'alb:cypress-forest:Dapper 1'):
    o = D['mats'][k]; o['dfq'] = 1; o['wfh'] = True; o.pop('hid', None)
D['mats']['luxemahjong.com/coming-soon-the-polo-club-mahjong-mat']['wfh'] = True
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
h = h.replace('Version 1.12<', 'Version 1.13<').replace('(Version 1.12)', '(Version 1.13)')
assert h.count('Version 1.13') >= 1, 'version string'
open(P, 'w').write(h); print('ui113 ok', h.count('Version 1.13'))
