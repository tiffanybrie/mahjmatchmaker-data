"""v112 QA round 2 (Nov 1): (1) sold-out badge was overridden by `.scard .meta b{display:block;16px}` -> higher-specificity pill rule;
(2) Tigre de Tartan 'Save through our link' logo pill too narrow at 360-390px -> class lo, tighter type, may grow past the tile width.
Usage: python3 qa112b.py <index.html> [more index.html ...] (idempotent)"""
import sys
CSS = ('.scard .meta b.sob,.meta b.sob{display:inline-block;margin-left:6px;padding:0 7px;border-radius:999px;background:#fde7ee;'
       'color:#c8325f;font:700 11px/1.6 var(--body);letter-spacing:.02em;white-space:nowrap;width:auto;vertical-align:middle}'
       '.tgrid .blg em.lo,.blg em.lo{font-size:8px;letter-spacing:-.01em;padding:3px 5px;max-width:none;white-space:nowrap}')
for p in sys.argv[1:]:
    h = open(p).read()
    if 'em.lo{' in h: print(p, 'already'); continue
    n = h.count("'<em>Save through our link</em>'"); assert n >= 1, (p, n)
    h = h.replace("'<em>Save through our link</em>'", "'<em class=\"lo\">Save through our link</em>'")
    i = h.index('</style>'); h = h[:i] + CSS + h[i:]
    open(p, 'w').write(h); print(p, 'patched', n)
