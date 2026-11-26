"""Tiffany Nov 26 9:08-9:10am, all 3 Deco pages: no colour-wheel graphic, no standalone profile card (it is in the carousel),
dating-profile slides large and edge to edge (no tapping to read). Run on a built code block in place."""
import re,sys
p=sys.argv[1]; s=open(p).read(); n0=len(s)
s=re.sub(r'<figure class="mm3-g mm3-wheel">.*?</figure>','',s,flags=re.S)
s=re.sub(r'<figure class="mm3-g mm3-fav2">.*?</figure>','',s,flags=re.S)
s=re.sub(r'<style>\.mm3-car\{.*?</style>','<style>.mm3-car{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,440px),1fr));gap:20px;padding:6px 0 14px}'
 '.mm3-car img{width:100%;height:auto;display:block;border-radius:16px;box-shadow:0 8px 22px rgba(6,40,90,.14)}'
 '#dating-profile{max-width:1500px!important;padding:0 10px!important}@media(max-width:640px){#dating-profile{padding:0 4px!important}.mm3-car{gap:12px}}</style>',s,flags=re.S)
assert 'mm3-wheel"' not in s and 'mm3-fav2"' not in s and 'auto-fill' in s
open(p,'w').write(s); print(p,n0,'->',len(s))
