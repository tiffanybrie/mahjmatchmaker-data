"""v112 claude.ai artifact copy (artifact 6epA9HuEdT32zUp79Qv3kd is at its 512-file limit; text files <= 16 MB).
Same method as fym_fix_oct31/artifact109.py, extended:
 - every mat chunk 190..217 in the build is packed into ONE mc/190.webp (container: images + JSON header {file:[off,len]} +
   uint32 header length); loadMC() fetches mc/190.webp for chunks 190-217 (was 190-212)
 - tile full photos in t106/ and t112/ go inline as data: URLs (no new files)
 - b24v1.js stays the PUBLISHED v111 one (pub109d/b24v1.js, 15.76 MB): the 41 thumbnails it lacks (new mats + PLM Chartreuse A)
   go inline in index.html in one window.IMG block before the b24v1.js script tag (b24v1.js would pass 16 MB otherwise)
 - hd/index.json: only shipped if the build adds inline HD (none since the PLM revert): the live one stays
Writes <out>/index.html, <out>/mc/190.webp, <out>/hd/index.json, <out>/files.json (only files that change vs v111).
Usage: python3 artifact112.py <b112 dir> <published b24v1.js (pub109d/b24v1.js)> <out dir>"""
import sys, os, json, re, struct, base64, shutil, mimetypes
B, PB24, O = sys.argv[1:4]
os.makedirs(O + '/mc', exist_ok=True); os.makedirs(O + '/hd', exist_ok=True)
h = open(B + '/index.html').read()
NEW = [c for c in range(190, 218) if os.path.exists(f'{B}/mc/{c}.webp')]
body, hdr = b'', {}
for c in NEW:
    ab = open(f'{B}/mc/{c}.webp', 'rb').read(); n = struct.unpack('<I', ab[-4:])[0]; hh = json.loads(ab[-4 - n:-4])
    for f, (a, l) in hh.items(): assert f not in hdr, f; hdr[f] = [len(body), l]; body += ab[a:a + l]
hj = json.dumps(hdr, separators=(',', ':')).encode()
open(O + '/mc/190raw.webp', 'wb').write(body + hj + struct.pack('<I', len(hj)))
# 256 MiB budget (live v111 = 251.43 MiB / 512 files): the pack is re-encoded per sub-image at q66 (from the raw build chunks, not
# compounding) -> ~12.4 MB (raw 22.2 MB; v111's pack was 11.6 MB at q72)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')); import fym_artifact_fit as _fit
_fit.shrink_chunk(O + '/mc/190raw.webp', O + '/mc/190.webp', 66); os.remove(O + '/mc/190raw.webp')
a = "fetch('mc/'+c+'.webp')"; assert h.count(a) == 1, h.count(a)
h = h.replace(a, f"fetch('mc/'+(c>=190&&c<={NEW[-1]}?190:c)+'.webp')/*v112 artifact: chunks 190-{NEW[-1]} packed in one file (512-file limit)*/", 1)
i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:]); ninl = 0
for t in D['tiles'].values():
    p = t.get('full', '')
    if isinstance(p, str) and p.startswith(('t106/', 't112/')):
        t['full'] = f'data:{mimetypes.guess_type(p)[0] or "image/jpeg"};base64,' + base64.b64encode(open(B + '/' + p, 'rb').read()).decode(); ninl += 1
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[i + e:]
def ids(s):
    out = {}
    for m in re.finditer(r'window\.IMG=Object\.assign\(window\.IMG\|\|\{\},', s):
        o, _ = json.JSONDecoder().raw_decode(s[m.end():]); out.update(o)
    return out
pub, mine = ids(open(PB24).read()), ids(open(B + '/b24v1.js').read())
assert all(mine[k] == pub[k] for k in pub if k in mine), 'a published thumbnail changed value'
miss = {k: v for k, v in mine.items() if k not in pub}
tag = '<script src="b24v1.js">'; assert h.count(tag) == 1
h = h.replace(tag, '<script>window.IMG=Object.assign(window.IMG||{},' + json.dumps(miss, separators=(',', ':')) + ');</script>' + tag, 1)
open(O + '/index.html', 'w').write(h)
# hd/index.json: ship it only when it carries inline HD (file:data:) the live one lacks. The live v111 artifact runs an OLDER
# hd/index.json; the build's lists file:r98/... zoom photos that are not artifact files (they would 404), so it stays as is.
HDNEW = any(v.startswith('file:data:') for v in json.load(open(B + '/hd/index.json')).get('r', {}).values())
if HDNEW: shutil.copy(B + '/hd/index.json', O + '/hd/index.json')
# chunk 153 still carries 3 mat images nothing references any more (superseded photos): drop them, bytes of the rest unchanged
PRUNE = []
for c in (153,):
    ab = open(f'{B}/mc/{c}.webp', 'rb').read(); n = struct.unpack('<I', ab[-4:])[0]; hh = json.loads(ab[-4 - n:-4])
    keep = {k: v for k, v in hh.items() if k in h}
    if len(keep) == len(hh): continue
    bd, nh = b'', {}
    for k, (a, l) in keep.items(): nh[k] = [len(bd), l]; bd += ab[a:a + l]
    j2 = json.dumps(nh, separators=(',', ':')).encode(); open(f'{O}/mc/{c}.webp', 'wb').write(bd + j2 + struct.pack('<I', len(j2))); PRUNE.append(c)
files = {'mc/190.webp': os.path.basename(O) + '/mc/190.webp'}
if HDNEW: files['hd/index.json'] = os.path.basename(O) + '/hd/index.json'
for c in PRUNE: files[f'mc/{c}.webp'] = os.path.basename(O) + f'/mc/{c}.webp'
json.dump(files, open(O + '/files.json', 'w'), indent=1)
sz = len(h.encode()); assert sz < 16 * 10**6 - 30000, sz
print('artifact112: chunks packed', NEW, 'images', len(hdr), 'mc/190.webp', os.path.getsize(O + '/mc/190.webp'), 'pruned', PRUNE, 'inline tiles', ninl,
      'inline thumbs', len(miss), 'index', sz, 'files', files)
