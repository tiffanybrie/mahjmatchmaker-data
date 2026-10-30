#!/usr/bin/env python3
"""FYM artifact budget check (Oct 30). Run BEFORE any Artifact publish of the FYM app.

The claude.ai artifact (6epA9HuEdT32zUp79Qv3kd) has hard limits per version:
  index.html <= 16 MB, <= 512 files, <= 256 MiB total.
Every publish attempt prompts Tiffany for approval, so never "try and see":
compute the budget here and publish ONCE when it clearly fits (3 MB margin).

Usage:
  python3 builder/fym_artifact_fit.py LISTING.txt INDEX.html FILES_MAP.json [--js-dir DIR]

LISTING.txt   paste of an Artifact `list scope=files` result (lines like
              - "mc/100.webp"  image/webp  1154281 bytes)
INDEX.html    the index you will publish
FILES_MAP.json the publish `files` map {path: source|null}; sources resolve
              relative to the map's own directory's parent (the publish `root`).
--js-dir      dir holding the b*v1.js / hd / mc json the index loads, used to
              find files in the artifact that nothing references (deletion
              candidates). Defaults to the INDEX dir.

Notes learned Oct 30:
- mc/*.webp are packed chunks: concatenated images + JSON header + 4-byte
  length. Never re-encode a chunk as one image. To shrink one, re-encode each
  sub-image and rebuild the header (see shrink_chunk below).
- Inline window.IMG thumb blocks count against the 16 MB index limit; append
  them to an existing b*v1.js instead of adding a new file (file-count cap).
"""
import json, os, re, struct, sys, io, glob

LIM_TOTAL, LIM_FILES, LIM_INDEX, MARGIN = 256 * 2**20, 512, 16 * 10**6, 3 * 10**6


def parse_listing(p):
    out = {}
    for m in re.finditer(r'-\s+"([^"]+)"\s+\S+\s+(\d+) bytes', open(p).read()):
        out[m.group(1)] = int(m.group(2))
    return out


def shrink_chunk(src, dst, quality=72):
    from PIL import Image
    d = open(src, 'rb').read(); n = struct.unpack('<I', d[-4:])[0]; hdr = json.loads(d[-4 - n:-4])
    body, nh = b'', {}
    for k, (o, l) in hdr.items():
        raw = d[o:o + l]; im = Image.open(io.BytesIO(raw)); im.load()
        b = io.BytesIO(); im.save(b, 'WEBP', quality=quality, method=6); new = b.getvalue()
        if len(new) >= len(raw): new = raw
        nh[k] = [len(body), len(new)]; body += new
    hj = json.dumps(nh, separators=(',', ':')).encode()
    open(dst, 'wb').write(body + hj + struct.pack('<I', len(hj)))
    return len(d), os.path.getsize(dst)


def main():
    a = sys.argv[1:]
    if len(a) < 3: print(__doc__); sys.exit(2)
    listing, index, fmap = a[0], a[1], a[2]
    jsdir = a[a.index('--js-dir') + 1] if '--js-dir' in a else os.path.dirname(index)
    live = parse_listing(listing)
    root = os.path.dirname(os.path.dirname(os.path.abspath(fmap)))
    M = json.load(open(fmap))
    new = dict(live)
    new['index.html'] = os.path.getsize(index)
    for k, v in M.items():
        if v is None: new.pop(k, None)
        else: new[k] = os.path.getsize(os.path.join(root, v))
    tot = sum(new.values())
    print(f'live:  {len(live)} files, {sum(live.values())/2**20:.1f} MiB')
    print(f'after: {len(new)} files (cap {LIM_FILES}), {tot/2**20:.1f} MiB (cap 256), index {new["index.html"]/1e6:.2f} MB (cap 16)')
    ok = len(new) <= LIM_FILES and tot <= LIM_TOTAL - MARGIN and new['index.html'] <= LIM_INDEX - 30000
    # unreferenced files = deletion candidates
    txt = open(index).read()
    for f in glob.glob(os.path.join(jsdir, '*.js')) + glob.glob(os.path.join(jsdir, 'hd', '*.json')) + glob.glob(os.path.join(jsdir, 'mc', '*.json')):
        txt += open(f, errors='ignore').read()
    cand = [k for k in new if re.match(r't\d+r?/', k) and k not in txt]
    if cand:
        print(f'unreferenced photo files ({len(cand)}, {sum(new[k] for k in cand)/2**20:.1f} MiB) — add as null to the files map:')
        for k in sorted(cand): print('  ', k, new[k])
    big = sorted(((s, k) for k, s in new.items() if k.startswith('mc/') and k.endswith('.webp')), reverse=True)[:10]
    print('largest mat chunks (shrink_chunk candidates):', [(k, s) for s, k in big])
    print('FITS — publish once' if ok else 'DOES NOT FIT — shrink/delete before publishing')
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
