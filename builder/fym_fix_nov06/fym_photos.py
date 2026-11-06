"""Read Find Your Mat-ch mat photos (D.mats[k].f, e.g. 'm/1145.webp') straight out of the website copy's mc/<chunk>.webp packs,
from the fym-site-preview git checkout (no network). The pack for chunk c sits at the jsDelivr commit/dir the page's own loadMC()
names (parsed from index.html); chunks with no absolute pin load relative to the page-block <base> (site-app/fym-v72 at the
branch HEAD). Pack format: concatenated webps + JSON header {file: [offset, length]} + 4-byte little-endian header length.
Usage (module): P = FymPhotos('/home/claude/fym-site', 'site-app/fym-v115/index.html'); raw = P.get('m/1145.webp')"""
import json, re, struct, subprocess, os


class FymPhotos:
    def __init__(self, checkout, index_rel, base_rel='site-app/fym-v72'):
        self.repo, self.base = checkout, base_rel
        h = open(os.path.join(checkout, index_rel)).read()
        j = h.find("'mc/'+c+'.webp'")
        k = h.rfind('MCB.has(c)?fetch((', 0, j)
        expr = h[k + len('MCB.has(c)?fetch(('):j]
        self.rules = []  # (lo, hi, commit, dir)
        for cond, url in re.findall(r"((?:\(?c(?:>=|===)\d+(?:&&c<=\d+|\|\|c===\d+)*\)?))\?'(https://[^']+)'", expr):
            m = re.search(r'@([0-9a-f]{40})/(site-app/[^/]+)/', url)
            nums = list(map(int, re.findall(r'\d+', cond)))
            if '>=' in cond:
                self.rules.append((nums[0], nums[1], m.group(1), m.group(2)))
            else:
                for n in nums: self.rules.append((n, n, m.group(1), m.group(2)))
        self.MCN = int(re.search(r'MCN=(\d+)', h).group(1))
        self.cache = {}

    def where(self, c):
        for lo, hi, commit, d in self.rules:
            if lo <= c <= hi: return commit, d
        return 'HEAD', self.base

    def pack(self, c):
        if c not in self.cache:
            commit, d = self.where(c)
            try:
                raw = subprocess.run(['git', '-C', self.repo, 'show', f'{commit}:{d}/mc/{c}.webp'], capture_output=True, check=True).stdout
                n = struct.unpack('<I', raw[-4:])[0]
                self.cache[c] = (raw, json.loads(raw[-4 - n:-4]))
            except Exception:
                self.cache[c] = None
        return self.cache[c]

    def get(self, f):
        c = int(f.split('/')[1].split('.')[0]) // self.MCN
        p = self.pack(c)
        if not p or f not in p[1]: return None
        a, l = p[1][f]
        return p[0][a:a + l]
