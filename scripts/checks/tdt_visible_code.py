#!/usr/bin/env python3
"""Tigre de Tartan visible-code check (added Oct 30, TdT affiliate policy; ANSWERS 2026-10-30 12:04-12:10am).
TdT rule: the code MAHJMATCH must never be VISIBLE as text near their name. Hidden text stays as is
(SEO title, meta, JSON-LD, alt text, link URLs), so this check only reads what a visitor sees:
<head>, <script>, <style>, <noscript>, <template> and every attribute are stripped first.
Fails if any sitemap page's visible text has MAHJMATCH within 200 chars of "Tigre de Tart" (case-insensitive)
inside the same text unit (the card / list item / paragraph / box that holds the code: nearest figure, li, tr, p,
blockquote, details, dd/dt, heading, or div whose class says box/card). Scoping to the unit keeps a neighbouring
brand's card or hub row (e.g. "Britt Mills - 15% off with MAHJMATCH" right under the TdT row) from counting.
Usage: python3 scripts/checks/tdt_visible_code.py [url ...]   (exit 1 on any hit; no args = whole sitemap)"""
import re, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup

WIN = 200


def get(u):
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
    return urllib.request.urlopen(req, timeout=40).read().decode('utf-8', 'replace')


UNIT_TAGS = {'figure', 'li', 'tr', 'p', 'blockquote', 'details', 'dd', 'dt', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}


def norm(t):
    return re.sub(r'\s+', ' ', t)


def unit_of(node):
    el = node.parent
    for _ in range(8):
        if el is None or el.name in ('body', '[document]'):
            break
        cls = ' '.join(el.get('class') or []).lower()
        if el.name in UNIT_TAGS or (el.name == 'div' and ('box' in cls or 'card' in cls)):
            return el
        el = el.parent
    p = node.parent
    return p.parent if p is not None and p.parent is not None else p


def hits(html):
    s = BeautifulSoup(html, 'html.parser')
    for t in s(['head', 'script', 'style', 'noscript', 'template']):
        t.decompose()
    body = s.body or s
    out, seen = [], set()
    for node in body.find_all(string=re.compile('mahjmatch', re.I)):
        u = unit_of(node)
        if id(u) in seen:
            continue
        seen.add(id(u))
        text = norm(u.get_text(' '))
        low = text.lower()
        for m in re.finditer(r'mahjmatch', low):
            a, b = max(0, m.start() - WIN), m.end() + WIN
            if 'tigre de tart' in low[a:b]:
                out.append(text[max(0, m.start() - 120):m.end() + 40])
    return out


def check(u):
    try:
        return u, hits(get(u)), None
    except Exception as e:  # network error = fail, not pass
        return u, [], str(e)


def main():
    urls = sys.argv[1:]
    if not urls:
        sm = get('https://www.mahjmatchmaker.com/sitemap.xml')
        urls = re.findall(r'<loc>([^<]+)</loc>', sm)
    fails = 0
    with ThreadPoolExecutor(8) as ex:
        for u, hs, err in ex.map(check, urls):
            if err:
                fails += 1; print('ERROR', u, err)
            for h in hs:
                fails += 1; print('FAIL', u, '|', h)
    print(f'{len(urls)} pages checked, {fails} problems')
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
