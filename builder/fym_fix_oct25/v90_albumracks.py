"""FYM v90 rack picks per mat (Tiffany Oct 25 17:10: Birdie + Luna led with Hot Pink, a Birdie TILE rack, though her Luna pick on
the album page is Peace Love Oak + Oh My Mahjong White Acrylic). Every set's match list had the tile-level racks pasted onto every mat.
Now:
 - s.m[mat][1] = her racks for THAT mat, in album order (config/album-rack-picks.json from scripts/album_rack_picks.py: "Rack matches"
   / "Racks shown" / holiday "Match the mat"); mats not on an album page keep their own list minus the tile-level racks.
 - D.ltc[slug] = the set's tile-level racks (album "Match the tiles", else the racks common to every mat of the set).
 - herRacks() = mat picks first, then tile-level racks ONLY when the mat carries that colour (or the rack is neutral / wood / tortoise /
   clear / metallic), then D.lm. ("Yes, but ..." 17:10 = yes to the rule.)
Locks (sets m) updated in the same run. Gate [51] checks app == album.
Usage: python3 v90_albumracks.py <build_dir>"""
import sys, os, json
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')) + '/'
B = sys.argv[1]; P = B + '/index.html'; h = open(P).read()
i = h.index('const D=') + 8; D, end = json.JSONDecoder().raw_decode(h[i:]); end += i
AL = json.load(open(REPO + 'config/album-rack-picks.json')); LP = REPO + 'builder/fym_flags/locks.json'; L = json.load(open(LP))
ltc, nch = {}, 0
for s in D['sets']:
    if not s['m']: continue
    al = AL.get(s['slug']) or {}
    tiles = []
    for e in al.values():
        for r in e.get('tiles') or []:
            if r not in tiles: tiles.append(r)
    if not tiles and len(s['m']) >= 3:
        common = set(s['m'][0][1]).intersection(*[set(x[1]) for x in s['m'][1:]])
        tiles = [r for r in s['m'][0][1] if r in common]
    if tiles: ltc[s['slug']] = tiles
    for x in s['m']:
        e = al.get(x[0])
        new = list(dict.fromkeys(e['mat'])) if e and e.get('mat') else [r for r in x[1] if r not in tiles]
        if e and e.get('shown'): new = [r for r in new if r not in tiles] or new   # 'Racks shown' lists the tile racks first: keep her mat picks first
        if e and not e.get('mat') and e.get('tiles'): new = []          # holiday card with only tile racks
        lmp = [r for r in (D.get('lm') or {}).get(x[0], []) if r in D['racks']]   # her stated picks for this mat (config/mat-racks-picks.json) lead (Oct 22 rule)
        new = list(dict.fromkeys((new + lmp) if (e and e.get('mat')) else (lmp + new)))   # QA v90: this album's own picks first; other albums' picks for the mat (D.lm) after
        if new != x[1]: x[1] = new; nch += 1
    lk = L['sets'].get(s['slug'])
    if lk and 'm' in lk:
        mm = {k: r for k, r in s['m']}
        lk['m'] = [[k, mm.get(k, r)] for k, r in lk['m']]
D['ltc'] = ltc
L.setdefault('_changes', []).append('2026-10-25: sets m rack lists = her per-mat album racks (tile-level racks moved to D.ltc), Tiffany 17:10 Birdie + Luna')
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
old = "const herRacks=()=>{const x=set().m.find(x=>x[0]===S.fav);const a=[...(x?x[1]:[]),...((D.lt||{})[set().slug]||[]),...((D.lm||{})[S.fav]||[])];"
new = ("/* v90: her racks for this mat first; the set's tile racks only when the mat carries that colour (or the rack is neutral/wood/tortoise/clear/metallic) */"
       "const rackFits=r=>{const o=R[r];if(!o)return false;const rf=o.rf||[];if(rf.some(c=>['neutral','wood','tortoise','clear','metallic'].includes(c)))return true;"
       "const mc=new Set([...(M[S.fav].mf||[]),...(M[S.fav].ha||[])]);if(mc.has('dark')){mc.add('brown');mc.add('black');}return rf.some(c=>mc.has(c));};"
       "const herRacks=()=>{const x=set().m.find(x=>x[0]===S.fav);const own=(x?x[1]:[]).filter(r=>R[r]&&!R[r].hid&&!R[r].rt);/* her album picks win over the OMM-racks-only-with-OMM-tiles rule */const a=[...own,...((D.ltc||{})[set().slug]||[]).filter(rackFits),...((D.lt||{})[set().slug]||[]).filter(rackFits),...((D.lm||{})[S.fav]||[])];")
assert h.count(old) == 1; h = h.replace(old, new)
old2 = "return [...new Set(a)].filter(r=>typeof rackOK==='function'?rackOK(r):!!R[r]);};"
assert h.count(old2) == 1; h = h.replace(old2, "return [...new Set(a)].filter(r=>own.includes(r)||(typeof rackOK==='function'?rackOK(r):!!R[r]));};")
open(P, 'w').write(h); json.dump(L, open(LP, 'w'), indent=1, ensure_ascii=False)
print('mat rack lists changed', nch, '| sets with tile racks', len(ltc))
