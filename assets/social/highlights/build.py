# Instagram highlight covers for Mahj Matchmaker 2.0 (Oct 19).
# Two style options (A: cream + navy line, B: rotating brand colors + cream line).
# Renders 1080x1920 PNG covers + a simulated profile-row preview per style.
# Run: python3 build.py   (needs playwright + chromium)
import os, base64
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '../../..'))
FONT = os.path.join(REPO, 'scripts/social/tileprofile/fonts/Caprasimo.ttf')
NAVY, PINK, ROSE, CREAM = '#054689', '#f56c8c', '#c8325f', '#f6e9df'

# All icons: 240x240 viewBox, stroke 11, round caps/joins. .a = accent fill, .as = accent stroke.
ICONS = {
 'find-your-match': '''
  <path d="M120 222C70 222 38 188 38 146C38 118 50 98 64 82C66 98 73 108 84 113C82 78 102 44 152 20C142 50 152 70 168 90C186 112 202 128 202 152C202 192 168 222 120 222Z"/>
  <path class="a" d="M120 192C95 175 86 162 86 148C86 135 96 126 107 126C113 126 117 129 120 134C123 129 127 126 133 126C144 126 154 135 154 148C154 162 145 175 120 192Z"/>''',
 'new-tiles': '''
  <g transform="translate(120 124) scale(.93) translate(-120 -124)" style="stroke-width:12.9">
  <rect x="22" y="72" width="54" height="132" rx="13"/><line x1="22" y1="176" x2="76" y2="176"/>
  <rect x="93" y="52" width="54" height="132" rx="13"/><line x1="93" y1="156" x2="147" y2="156"/>
  <rect x="164" y="72" width="54" height="132" rx="13"/><line x1="164" y1="176" x2="218" y2="176"/>
  <line x1="49" y1="104" x2="49" y2="146"/><line x1="191" y1="104" x2="191" y2="146"/>
  <circle class="a" cx="120" cy="104" r="16"/>
  <path class="a" d="M196 24L201 35L212 40L201 45L196 56L191 45L180 40L191 35Z"/></g>''',
 'albums': '''
  <rect x="44" y="42" width="116" height="146" rx="14" transform="rotate(-10 102 115)"/>
  <rect class="bgfill" x="82" y="58" width="116" height="146" rx="14" transform="rotate(7 140 131)"/>
  <path class="a" d="M140 162C121 149 114 139 114 129C114 119 121 112 130 112C134 112 138 114 140 118C142 114 146 112 150 112C159 112 166 119 166 129C166 139 159 149 140 162Z"/>''',
 'mats': '''
  <rect x="36" y="36" width="168" height="168" rx="16"/>
  <rect x="64" y="64" width="112" height="112" rx="6"/>
  <path class="a" d="M120 92C128 92 132 100 132 108C140 108 148 112 148 120C148 128 140 132 132 132C132 140 128 148 120 148C112 148 108 140 108 132C100 132 92 128 92 120C92 112 100 108 108 108C108 100 112 92 120 92Z"/>''',
 'tablescapes': '''
  <!-- Oct 20 (Tiffany): a MAHJONG table seen from above, not a fork + knife. Square table, a rack on each side, tiles in the middle -->
  <rect x="28" y="28" width="184" height="184" rx="20"/>
  <rect x="78" y="50" width="84" height="16" rx="6"/><rect x="78" y="174" width="84" height="16" rx="6"/>
  <rect x="50" y="78" width="16" height="84" rx="6"/><rect x="174" y="78" width="16" height="84" rx="6"/>
  <rect class="a" x="92" y="98" width="26" height="36" rx="5"/><rect class="a" x="122" y="106" width="26" height="36" rx="5"/>''',
 'codes': '''
  <g transform="translate(120 120) scale(.92) translate(-120 -120)" style="stroke-width:13">
  <path d="M130 30H196Q210 30 210 44V108Q210 116 204 122L124 202Q114 212 104 202L38 136Q28 126 38 116L118 36Q123 30 130 30Z"/>
  <circle cx="176" cy="64" r="11"/>
  <line class="as" x1="146" y1="98" x2="94" y2="150"/>
  <circle class="a" cx="100" cy="104" r="11"/>
  <circle class="a" cx="140" cy="144" r="11"/></g>''',
 'fb-group': '''
  <path d="M168 104H196Q212 104 212 120V164Q212 180 196 180H190V204L166 180H140Q124 180 124 164V158"/>
  <path class="bgfill" d="M44 40H148Q166 40 166 58V122Q166 140 148 140H90L58 168V140H44Q28 140 28 122V58Q28 40 44 40Z"/>
  <circle class="a" cx="66" cy="90" r="10"/><circle class="a" cx="97" cy="90" r="10"/><circle class="a" cx="128" cy="90" r="10"/>''',
 'about-2-0': '''
  <text class="t" x="118" y="160" text-anchor="middle">2.0</text>
  <path class="a" d="M196 26L203 47L224 54L203 61L196 82L189 61L168 54L189 47Z"/>
  <path class="a" d="M42 170L46 182L58 186L46 190L42 202L38 190L26 186L38 182Z"/>''',
}
LINEUP = [  # (key, label shown under the circle)
 ('find-your-match', 'Find Match'), ('new-tiles', 'New Tiles'), ('albums', 'Albums'),
 ('mats', 'Mats'), ('tablescapes', 'Tablescapes'), ('codes', 'Codes'),
 ('fb-group', 'FB Group'), ('about-2-0', 'About 2.0'),
]
B_BG = [PINK, NAVY, ROSE, PINK, NAVY, ROSE, PINK, NAVY]
# Style C (Oct 19, Tiffany): cute pastel colour-theory covers, each its own colour (bg, deep ink of same hue, accent)
C_PAL = [('#f9d3dc', '#b8466a', '#f2a65a'),   # find your match: blush
         ('#fcdcc6', '#c0602a', '#f56c8c'),   # new tiles: peach
         ('#fbefc2', '#a07f1e', '#f56c8c'),   # albums: butter
         ('#d5ecd8', '#3d8656', '#f56c8c'),   # mats: mint
         ('#d2e7f4', '#36709f', '#f56c8c'),   # tablescapes: sky
         ('#dcdcf6', '#5359ad', '#f56c8c'),   # codes: periwinkle
         ('#e9d9f3', '#7a50ad', '#f56c8c'),   # fb group: lavender
         ('#f7d4e6', '#ad4680', '#f2a65a')]   # about 2.0: rose

def colors(style, i):
    if style == 'A':
        return CREAM, NAVY, PINK
    if style == 'C':
        return C_PAL[i]
    bg = B_BG[i]
    return bg, CREAM, (PINK if bg == NAVY else NAVY)

def font_css():
    b = base64.b64encode(open(FONT, 'rb').read()).decode()
    return f"@font-face{{font-family:Capra;src:url(data:font/ttf;base64,{b})}}"

def cover_html(key, bg, ink, acc, guide=False):
    g = ('<div style="position:absolute;left:240px;top:660px;width:600px;height:600px;border-radius:50%;'
         'border:4px dashed rgba(255,0,0,.8)"></div><div style="position:absolute;left:0;top:420px;width:1080px;'
         'height:1080px;border-radius:50%;border:4px solid rgba(0,160,0,.8)"></div>') if guide else ''
    return f'''<!doctype html><html><head><style>{font_css()}
html,body{{margin:0;width:1080px;height:1920px;background:{bg};overflow:hidden}}
svg{{position:absolute;left:250px;top:670px;width:580px;height:580px}}
svg{{fill:none;stroke:{ink};stroke-width:12;stroke-linecap:round;stroke-linejoin:round}}
svg .a{{fill:{acc};stroke:none}} svg .as{{stroke:{acc}}} svg .bgfill{{fill:{bg}}}
svg .t{{font-family:Capra;font-size:112px;fill:{ink};stroke:none}}
</style></head><body><svg viewBox="0 0 240 240">{ICONS[key]}</svg>{g}</body></html>'''

def row_html(style, files):
    items = ''.join(f'''<div class="h"><div class="ring"><img src="file://{f}"></div><span>{lab}</span></div>'''
                    for (k, lab), f in zip(LINEUP, files))
    flame = os.path.join(REPO, 'assets/brand/flame-heart.png')
    name = {'A': 'A · cream + navy line', 'B': 'B · brand colors + cream line', 'C': 'C · pastel color theory'}[style]
    return f'''<!doctype html><html><head><style>
body{{margin:0;background:#fff;font:14px -apple-system,"Helvetica Neue",Arial,sans-serif;color:#000;width:760px}}
.top{{display:flex;align-items:center;gap:22px;padding:22px 20px 8px}}
.av{{width:86px;height:86px;border-radius:50%;background:{CREAM};display:flex;align-items:center;justify-content:center}}
.av img{{width:54px}} .nm b{{font-size:17px;display:block}} .nm small{{color:#737373;font-size:13px}}
.bio{{padding:4px 20px 14px;font-size:13.5px;line-height:1.35}}
.row{{display:flex;gap:14px;padding:6px 18px 18px}}
.h{{width:76px;text-align:center}} .ring{{width:70px;height:70px;border-radius:50%;border:1px solid #dbdbdb;padding:3px;margin:0 auto}}
.ring img{{width:70px;height:70px;border-radius:50%;object-fit:cover;display:block}}
.h span{{display:block;font-size:11.5px;margin-top:6px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.tag{{padding:10px 20px;background:#fafafa;border-top:1px solid #efefef;color:#737373;font-size:12px}}
</style></head><body><div class="top"><div class="av"><img src="file://{flame}"></div><div class="nm"><b>mahjmatchmaker</b><small>Mahj Matchmaker</small></div></div>
<div class="bio">Matching mahjong tiles with their perfect mats &amp; racks 💘<br>Find Your Match · code MAHJMATCH</div>
<div class="row">{items}</div><div class="tag">Preview · Style {name}</div></body></html>'''

def main():
    out = HERE
    with sync_playwright() as p:
        br = p.chromium.launch()
        pg = br.new_page(viewport={'width': 1080, 'height': 1920})
        for style in os.environ.get('STYLES', 'ABC'):
            d = os.path.join(out, f'style-{style}'); os.makedirs(d, exist_ok=True)
            files = []
            for i, (key, lab) in enumerate(LINEUP):
                bg, ink, acc = colors(style, i)
                pg.set_content(cover_html(key, bg, ink, acc)); pg.wait_for_timeout(150)
                f = os.path.join(d, f'{i+1:02d}-{key}.png'); pg.screenshot(path=f); files.append(f)
                if os.environ.get('GUIDE'):
                    pg.set_content(cover_html(key, bg, ink, acc, True)); pg.wait_for_timeout(100)
                    pg.screenshot(path=os.path.join(os.environ['GUIDE'], f'{style}-{i+1:02d}-guide.png'))
            rp = br.new_page(viewport={'width': 760, 'height': 400}, device_scale_factor=2)
            tmp = os.path.join(d, '_row.html'); open(tmp, 'w').write(row_html(style, files))
            rp.goto('file://' + tmp); rp.wait_for_timeout(300); os.remove(tmp)
            rp.locator('body').screenshot(path=os.path.join(out, f'preview-profile-row-{style}.png'))
            rp.close()
        br.close()

if __name__ == '__main__':
    main()
