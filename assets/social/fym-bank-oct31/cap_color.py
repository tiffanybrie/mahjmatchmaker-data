"""Colour-chip demo captures for Papaya Spritz (deck narrows per chip)."""
import sys,json; sys.path.insert(0,'/home/claude/mahjmatchmaker-data/assets/social/fym-bank-oct31')
from lib import *
m={}
with sync_playwright() as p:
    b,pg=start(p); search_pick(pg,'Papaya','Papaya Spritz')
    for t in ['Orange & coral','Green','Blue & teal']:
        pg.evaluate("(t)=>[...document.querySelectorAll('button.dot')].find(b=>b.title===t&&b.offsetParent).click()",t); pg.wait_for_timeout(1500)
        m[t]=[pg.evaluate("()=>matDeck().length"),pg.evaluate("()=>matDeck().slice(0,3).map(k=>M[k].n+'/'+M[k].bn)")]
        deck(pg); shot(pg,'c-'+t.split()[0].lower())
        pg.evaluate("()=>{const d=document.querySelector('button.holc');window.scrollTo(0,d.getBoundingClientRect().top+scrollY-330)}"); pg.wait_for_timeout(800); shot(pg,'c-'+t.split()[0].lower()+'-chips')
        pg.evaluate("(t)=>[...document.querySelectorAll('button.dot')].find(b=>b.title===t&&b.offsetParent).click()",t); pg.wait_for_timeout(1000)
    b.close()
print(json.dumps(m))
