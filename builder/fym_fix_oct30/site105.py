"""Website copy of v105 (site-app/fym-v105/index.html on fym-site-preview), refreshed from a rebuilt b105:
 - code: the same QA-fix replacements as patch105b.py (site index keeps its CDN path rewrites)
 - data: const D from b105 (rankings, side-B orders, new/changed mats)
 - thumbs: any window.IMG id in b105 (index + b24v1.js) missing from the site index goes in as one inline block
 - chunk 189 URL pinned to the fym-site-preview commit that holds the new mc/189.webp
Usage: python3 site105.py <site index in> <b105 dir> <out> <chunk189 commit>"""
import sys, json, re, subprocess, os
SI, B, OUT, C189 = sys.argv[1:5]
h = open(SI).read()
tmp = OUT + '.tmp'; open(tmp, 'w').write(h)
subprocess.check_call([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'patch105b.py'), tmp])
h = open(tmp).read(); os.remove(tmp)
b = open(B + '/index.html').read(); j = b.index('const D=') + 8; D2, e2 = json.JSONDecoder().raw_decode(b[j:])
i = h.index('const D=') + 8; D1, e1 = json.JSONDecoder().raw_decode(h[i:])
h = h[:i] + json.dumps(D2, ensure_ascii=False, separators=(',', ':')) + h[i + e1:]
def img_ids(s):
    out = {}
    for m in re.finditer(r'window\.IMG=Object\.assign\(window\.IMG\|\|\{\},', s):
        o, _ = json.JSONDecoder().raw_decode(s[m.end():]); out.update(o)
    return out
have = img_ids(h); src = img_ids(b); src.update(img_ids(open(B + '/b24v1.js').read()))
need = {k: v for k, v in src.items() if k not in have and k in b}
if need:
    a = '<script>window.IMG=Object.assign(window.IMG||{},'
    h = h.replace(a, '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(need, separators=(',', ':')) + ');</script>' + a, 1)
old = re.search(r"c===189\?'https://cdn\.jsdelivr\.net/gh/tiffanybrie/mahjmatchmaker-data@([0-9a-f]{40})/site-app/fym-v105/'", h)
assert old, 'no chunk 189 mapping'
h = h.replace(old.group(0), old.group(0).replace(old.group(1), C189))
open(OUT, 'w').write(h)
print('site105: D replaced, thumbs added', len(need), 'chunk189 @', C189[:8], 'size', len(h))
