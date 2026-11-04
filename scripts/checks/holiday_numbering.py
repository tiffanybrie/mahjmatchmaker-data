"""Holiday-section numbering check (QA Nov 4 2026: Spring Love read 15,16,17,04 and Shangri-La 13,14,15,04 after the
late-picks paste; same-day bug rule). For every live album page with a holiday section (id="holiday-matches") and every
section on /holiday-mahjong-matches: card numbers (mm3-n) must run up by exactly 1, and the section must not sit inside
the .mm3-faq wrapper (Sunday Tile Set bug) and must have the holcss style block on the page.
Usage: python3 scripts/checks/holiday_numbering.py [slug ...]   (default: every *-mahjong-tile-matches page in the sitemap)
Exit 1 on any problem."""
import re, sys, os, subprocess, random

def get(u):
    return subprocess.run(['curl', '-s', '--max-time', '40', f'{u}?nc={random.randint(1, 10**9)}'], capture_output=True, text=True).stdout

def check_section(name, seg, bad):
    nums = [int(x) for x in re.findall(r'<span class="mm3-n">(\d+)</span>', seg)]
    for a, b in zip(nums, nums[1:]):
        if b != a + 1:
            bad.append(f'{name}: numbering {nums}'); return

def main():
    pages = sys.argv[1:]
    if not pages:
        sm = get('https://www.mahjmatchmaker.com/sitemap.xml')
        pages = sorted(set(re.findall(r'mahjmatchmaker\.com/([a-z0-9-]+-mahjong-tile-matches)<', sm)))
    bad = []; n = 0; dom = []
    for p in pages:
        t = get(f'https://www.mahjmatchmaker.com/{p}')
        i = t.find('id="holiday-matches"')
        if i < 0: continue
        n += 1
        check_section(p, t[i:t.find('</section>', i)], bad)
        if '.mm3-hol{' not in t and '.mm3-hol {' not in t: bad.append(f'{p}: holiday section style (.mm3-hol) missing')
        dom.append(p)
    t = get('https://www.mahjmatchmaker.com/holiday-mahjong-matches')
    for m in re.finditer(r'<section class="mm3-hol" id="([a-z0-9-]+)"', t):
        n += 1; check_section('holiday#' + m.group(1), t[m.end():t.find('</section>', m.end())], bad)
    # DOM check in a real browser (unclosed tags make string counting unreliable): the holiday section must not sit
    # inside the .mm3-faq wrapper (Sunday Tile Set, Nov 4: centred caption, narrow cards)
    js = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'holiday_dom_check.js')
    r = subprocess.run(['node', js] + dom, capture_output=True, text=True, timeout=1800,
                       env={**os.environ, 'NODE_PATH': subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True).stdout.strip()})
    bad += [l[5:] for l in r.stdout.splitlines() if l.startswith('FAIL ')]
    if r.returncode not in (0, 1): bad.append('dom check crashed: ' + r.stderr[-200:])
    print(f'{n} holiday sections checked, {len(bad)} problems')
    for b in bad: print('  FAIL', b)
    sys.exit(1 if bad else 0)

main()
