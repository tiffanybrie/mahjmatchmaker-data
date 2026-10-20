"""Re-apply approved (locked) FYM values after any rebuild / catalog refresh.
Usage: python3 builder/fym_apply_locks.py <build_dir | index.html> [--check]
  default : rewrites index.html with locked values restored, prints "changed locked items: N" and what changed
  --check : report only, never writes (exit 1 if N>0)
Locks live in builder/fym_flags/locks.json (tiles: album photo src/full/pile; sets: m list, sb, hid, fp, fz; mats: n, f, th, rt)."""
import sys, os, json
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')) + '/'

def load(path):
    p = os.path.join(path, 'index.html') if os.path.isdir(path) else path
    h = open(p).read(); i = h.find('const D=') + 8
    D, end = json.JSONDecoder().raw_decode(h, i)
    return p, h, i, end, D

def diffs(D, locks):
    out = []
    sets = {}
    for s in D['sets']: sets.setdefault(s['slug'], s)
    for kind, objs in (('tiles', D['tiles']), ('mats', D['mats'])):
        for k, lv in locks.get(kind, {}).items():
            o = objs.get(k)
            if o is None: out.append((kind, k, '*', 'missing', None)); continue
            for f, v in lv.items():
                if f in ('set',): continue
                cur = o.get(f, False if f in ('hid', 'rt', 'sb') else None)
                if cur != v: out.append((kind, k, f, cur, v))
    for slug, lv in locks.get('sets', {}).items():
        s = sets.get(slug)
        if s is None: out.append(('sets', slug, '*', 'missing', None)); continue
        for f, v in lv.items():
            if f == 'name': continue
            cur = s.get(f, False if f in ('sb', 'hid') else None)
            if cur != v: out.append(('sets', slug, f, cur, v))
    return out

def apply(D, locks):
    sets = {}
    for s in D['sets']: sets.setdefault(s['slug'], s)
    for kind, objs in (('tiles', D['tiles']), ('mats', D['mats'])):
        for k, lv in locks.get(kind, {}).items():
            if k in objs: objs[k].update({f: v for f, v in lv.items() if f != 'set'})
    for slug, lv in locks.get('sets', {}).items():
        if slug in sets: sets[slug].update({f: v for f, v in lv.items() if f != 'name'})

if __name__ == '__main__':
    path = sys.argv[1]; check = '--check' in sys.argv
    locks = json.load(open(REPO + 'builder/fym_flags/locks.json'))
    p, h, i, end, D = load(path)
    d = diffs(D, locks)
    for x in d[:200]: print('  locked value differs:', x[0], x[1], x[2], 'build=', json.dumps(x[3], ensure_ascii=False)[:80], 'locked=', json.dumps(x[4], ensure_ascii=False)[:80])
    print('changed locked items:', len(d))
    if check: sys.exit(1 if d else 0)
    if d:
        apply(D, locks)
        h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[end:]
        open(p, 'w').write(h)
        print('re-applied; after re-apply changed locked items:', len(diffs(D, locks)))
