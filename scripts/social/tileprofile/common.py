"""Shared look for Tile Set Profile social pieces (doc 81): cream black-book paper, navy ink, pink accents, the set's own colour.
Fonts: Caprasimo (display), Playfair Display italic (voice), Bitter (labels/body), Caveat (handwritten notes)."""
import json, os
R = '/home/claude/mahjmatchmaker-data/'
F = R + 'scripts/social/tileprofile/fonts/'
NAVY = '#064587'; PINK = '#d6608c'; CREAM = '#f7eee4'; PAPER = '#fbf6ef'

def css(w, h, accent):
    return f"""
@font-face{{font-family:Capra;src:url('file://{F}Caprasimo.ttf')}}
@font-face{{font-family:Hand;src:url('file://{F}Caveat-Bold.ttf')}}
@font-face{{font-family:PF;font-style:italic;font-weight:400;src:url('file://{F}playfair-display-latin-400-italic.woff2')}}
@font-face{{font-family:PF;font-style:italic;font-weight:600;src:url('file://{F}playfair-display-latin-600-italic.woff2')}}
@font-face{{font-family:Bit;font-weight:400;src:url('file://{F}bitter-latin-400-normal.woff2')}}
@font-face{{font-family:Bit;font-weight:600;src:url('file://{F}bitter-latin-600-normal.woff2')}}
@font-face{{font-family:Bit;font-weight:700;src:url('file://{F}bitter-latin-700-normal.woff2')}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:{w}px;height:{h}px;overflow:hidden;background:{CREAM};color:{NAVY};font-family:Bit,Georgia,serif}}
:root{{--acc:{accent};--navy:{NAVY};--pink:{PINK};--cream:{CREAM};--paper:{PAPER}}}
.caps{{font:700 22px Bit;letter-spacing:.22em;text-transform:uppercase}}
.cap{{font-family:Capra;font-weight:400;line-height:.95}}
.pf{{font-family:PF;font-style:italic}}
.hand{{font-family:Hand;color:var(--pink)}}
.rule{{height:2px;background:rgba(6,69,135,.18)}}
.chip{{background:#fff;border-radius:14px;box-shadow:0 6px 18px rgba(6,40,90,.10);overflow:hidden}}
.chip .sw{{width:100%}}
.chip .t{{padding:12px 14px 14px}}
.chip .n{{font:700 24px Bit;letter-spacing:.04em}}
.chip .r{{font:400 18px Bit;color:#5a6b85}}
.chip .h{{font:600 18px Bit;color:#8a94a6;letter-spacing:.06em;margin-top:2px}}
.pill{{display:inline-block;background:var(--navy);color:#fff;border-radius:999px;font:700 30px Bit;padding:18px 34px}}
.ph{{background-size:cover;background-position:center}}
"""

def url(p): return 'file://' + (p if p.startswith('/') else R + p)
def load(key): return json.load(open(R + f'config/profiles/{key}.json')), json.load(open(R + 'config/colorcards.json'))['sets'][key]
