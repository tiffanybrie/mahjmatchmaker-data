"""Load a mat's full photo from a built FYM folder (mc/<chunk>.webp packs or mc/<chunk>.json), like the app's matFull()."""
import json, io, os, struct, base64
from PIL import Image
_cache = {}
def load_D(B):
    h = open(os.path.join(B, 'index.html')).read(); i = h.index('const D=') + 8; return json.JSONDecoder().raw_decode(h[i:])[0]
def mat_full(B, f, MCN=12):
    c = int(f.split('/')[1].split('.')[0]) // MCN
    if (B, c) not in _cache:
        p = os.path.join(B, 'mc', f'{c}.webp')
        if os.path.exists(p):
            ab = open(p, 'rb').read(); n = struct.unpack('<I', ab[-4:])[0]; hd = json.loads(ab[-4 - n:-4].decode())
            _cache[(B, c)] = {k: ab[a:a + l] for k, (a, l) in hd.items()}
        else:
            j = json.load(open(os.path.join(B, 'mc', f'{c}.json'))); _cache[(B, c)] = {k: base64.b64decode(v.split(',', 1)[1]) for k, v in j.items()}
    b = _cache[(B, c)].get(f)
    return Image.open(io.BytesIO(b)).convert('RGB') if b else None
