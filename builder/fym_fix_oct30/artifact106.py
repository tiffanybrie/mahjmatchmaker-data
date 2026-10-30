"""claude.ai artifact copy of v106 (artifact limit: 512 files / version; 1.9 already holds 511).
New files would be mc/190..195 (6 mat chunks) + t106 (1 tile photo) = 7. To fit:
 - the 6 new mat chunks are packed into ONE file mc/190.webp (same container format: images + JSON header {file: [offset, len]}
   + uint32 header length) and loadMC() fetches mc/190.webp for chunks 190-195
 - the Journey to the West full photo goes inline as a data: URL (one 1000px jpeg)
=> +1 file (mc/190.webp) -> 512. Writes <out>/index.html, <out>/mc/190.webp, <out>/b24v1.js and <out>/files.json.
Usage: python3 artifact106.py <b106 dir> <out dir>"""
import sys, os, json, re, struct, base64, shutil
B, O = sys.argv[1:3]
os.makedirs(O + '/mc', exist_ok=True)
h = open(B + '/index.html').read()
mb = re.search(r'MCB=new Set\(\[([0-9, ]+)\]\);', h).group(1); NEW = [c for c in (190, 191, 192, 193, 194, 195) if os.path.exists(f'{B}/mc/{c}.webp')]
body, hdr = b'', {}
for c in NEW:
    ab = open(f'{B}/mc/{c}.webp', 'rb').read(); n = struct.unpack('<I', ab[-4:])[0]; hh = json.loads(ab[-4 - n:-4])
    for f, (a, l) in hh.items(): hdr[f] = [len(body), l]; body += ab[a:a + l]
hj = json.dumps(hdr, separators=(',', ':')).encode()
open(O + '/mc/190.webp', 'wb').write(body + hj + struct.pack('<I', len(hj)))
a = "fetch('mc/'+c+'.webp')"; assert h.count(a) == 1, h.count(a)
h = h.replace(a, "fetch('mc/'+(c>=190&&c<=195?190:c)+'.webp')/*v106 artifact: chunks 190-195 packed in one file (512-file limit)*/", 1)
i = h.index('const D=') + 8; D, e = json.JSONDecoder().raw_decode(h[i:])
for t in D['tiles'].values():
    if t.get('full', '').startswith('t106/'):
        t['full'] = 'data:image/jpeg;base64,' + base64.b64encode(open(B + '/' + t['full'], 'rb').read()).decode()
h = h[:i] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + h[i + e:]
open(O + '/index.html', 'w').write(h); shutil.copy(B + '/b24v1.js', O + '/b24v1.js')
files = {'b24v1.js': os.path.basename(O) + '/b24v1.js', 'mc/190.webp': os.path.basename(O) + '/mc/190.webp'}
json.dump(files, open(O + '/files.json', 'w'), indent=1)
print('chunks packed', NEW, 'images', len(hdr), 'mc/190.webp', len(body) + len(hj) + 4, 'index', len(h.encode()), 'files', files)
