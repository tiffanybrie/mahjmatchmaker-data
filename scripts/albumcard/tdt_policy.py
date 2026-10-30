"""Tigre de Tartan visible-code rule for album match cards (Tiffany Oct 30 12:04-12:10am, docs/ANSWERS.md).
TdT affiliate policy: their name and the code MAHJMATCH never appear together in VISIBLE text. On TdT mat cards
the code pill reads 'save 10% with my link' and the Shop button uses the auto-apply link (code inside the URL).
Every album-card generator imports card_code() / shop_url() from here so a rebuild can't bring the code back.
Check: python3 scripts/checks/tdt_visible_code.py"""
import re
from urllib.parse import quote, urlsplit

TDT_REF = 'sca_ref=11798386.tvil8GTGTp6s2'
CODE_SPAN = '<span class="mm3-code">code MAHJMATCH</span>'
TDT_SPAN = '<span class="mm3-code">save 10% with my link</span>'


def is_tdt(brand):
    return 'tigre de tart' in (brand or '').lower()


def tdt_link(url):
    """Any tigredetartan.com product/home URL -> https://tigredetartan.com/discount/MAHJMATCH?redirect=<path?sca_ref>."""
    if not url or 'tigredetartan.com' not in url or '/discount/' in url:
        return url
    p = urlsplit(url.replace('&amp;', '&'))
    path = p.path or '/'
    if path.rstrip('/') == '/mahjmatchmaker':
        path = '/'
    q = '&'.join(x for x in p.query.split('&') if x and not x.startswith('sca_ref='))
    q = (q + '&' if q else '') + TDT_REF
    return 'https://tigredetartan.com/discount/MAHJMATCH?redirect=' + quote(path + '?' + q, safe='')


def card_code(brand):
    return TDT_SPAN if is_tdt(brand) else CODE_SPAN


def shop_url(url, brand):
    return tdt_link(url) if is_tdt(brand) else url
