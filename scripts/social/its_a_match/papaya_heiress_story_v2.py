"""Papaya + Heiress "It's a mat-ch!" as a 3-frame STORY, Tiffany's 1:11pm edits (Oct 21):
  1  slide 1 story layout; "Hooking up tiles, mats & racks" on ONE line; empty band at the bottom of the safe zone for the
     VISIBLE @ohmymahjong + @brittmillsdesign mentions.
  2  "Top match card / From Papaya's album" + the card only (no rack lists). Card = card-heiress-10pct.jpg: the album card
     re-rendered with gen2.py, current Beechwood racks, band "10% OFF USE CODE : MAHJMATCH" (10% is always safe; the live
     album cards are untouched).
  3  PRE-LAUNCH teaser: "Find Your Mat-ch(TM) · Coming 10.27", one short line, mahjmatchmaker.com, the FYM screenshot in a
     real iPhone frame (71.5 x 147 mm body, 19.5:9 screen, real bezel, rounded corners, dynamic island). Link-sticker band.
Stories 1080x1920. Oct 21 1:47pm (Tiffany): content is centred in the safe band (top 250 / bottom 340 clear) and scaled
as big as it fits (FIT below); no empty bands for stickers, stickers go over the cream margin.
Usage: python3 scripts/social/its_a_match/papaya_heiress_story_v2.py"""
import os, sys, asyncio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render as RD

R = RD.R
OUT = f'{R}/assets/social/its-a-match/papaya-heiress/story-v2'
c = RD.fill_defaults({'set_slug': 'papaya-spritz', 'tile': 'Papaya Spritz', 'short': 'Papaya', 'mat': 'Heiress',
                      'mat_brand': 'Britt Mills', 'count': 50,
                      'fym_img': 'assets/social/its-a-match/papaya-heiress/fym-screen.jpg',
                      'card_img': f'{R}/assets/social/its-a-match/papaya-heiress/card-heiress-10pct.jpg'})
NAVY, PINK, PINK2, BLUSH, SITE, u, e, poss = RD.NAVY, RD.PINK, RD.PINK2, RD.BLUSH, RD.SITE, RD.u, RD.e, RD.poss


def frame1():
    W, Ht, html = RD.slide1(c, 'story')
    html = html.replace('top:269px;height:1267px', 'top:250px;height:1330px')
    html = html.replace('line-height:1.18">Hooking up tiles,<br>mats &amp; racks',
                        'line-height:1.18;white-space:nowrap">Hooking up tiles, mats &amp; racks')
    return html


def frame2():
    body = f"""<div id=blk style="position:absolute;left:0;right:0;top:250px;bottom:340px;display:flex;flex-direction:column;align-items:center;justify-content:center">
<div class=c style="font:700 34px Bit;letter-spacing:.2em;color:{NAVY};text-transform:uppercase">Top match card</div>
<div class=c style="font-family:Hand;font-size:108px;color:{PINK};line-height:1;margin-top:6px;white-space:nowrap">From {poss(c['short'])} album</div>
<div id=frame style="flex:1;min-height:0;margin-top:30px;background:#fff;border-radius:32px;padding:22px;box-shadow:0 18px 44px rgba(200,80,90,.16),0 0 0 1px #f3dfe3;display:flex">
  <img id=card src="{u(c['card_img'])}" style="height:100%;width:auto;border-radius:14px;display:block"></div>
<div class=c style="font-family:Lo;font-weight:700;font-size:52px;color:{NAVY};margin-top:28px;line-height:1.1"><i>{e(c['mat'])}</i> <span style="color:{PINK2}">&middot;</span> {e(c['mat_brand'])}</div>
</div>"""
    return RD.shell(1080, 1920, body)


def frame3():
    # iPhone 14/15: body 71.5 x 147 mm, screen 1170 x 2532 px (19.5:9). Phone height 900px -> width 900*71.5/147.
    ph = 940; pw = round(ph * 71.5 / 147); bez = 22; sw = pw - 2 * bez; sh = ph - 2 * bez
    body = f"""<div id=blk style="position:absolute;left:0;right:0;top:250px;bottom:340px;display:flex;flex-direction:column;align-items:center;justify-content:center">
<div class=c style="font:700 34px Bit;letter-spacing:.2em;color:{PINK};text-transform:uppercase">Coming 10.27</div>
<div class=c style="font-family:Lo;font-weight:700;font-size:100px;color:{NAVY};line-height:1;white-space:nowrap;margin-top:12px">Find <i>Your</i> Mat-ch<span style="font-size:.34em;vertical-align:1.3em;margin-left:3px">&trade;</span></div>
<div class=c style="font-family:Lo;font-style:italic;font-size:44px;color:{NAVY};margin-top:18px">Swipe the mats that match your tiles.</div>
<div style="position:relative;margin-top:44px;width:{pw}px;height:{ph}px;border-radius:{round(pw*0.17)}px;background:linear-gradient(145deg,#2b2f38,#0d0f14 45%,#2a2d35);padding:{bez}px;box-shadow:0 30px 70px rgba(6,42,85,.28),inset 0 0 0 2px #4a4f5a,inset 0 0 0 6px #111">
  <div style="position:absolute;left:-4px;top:{round(ph*.2)}px;width:4px;height:{round(ph*.07)}px;border-radius:2px;background:#22252c"></div>
  <div style="position:absolute;left:-4px;top:{round(ph*.29)}px;width:4px;height:{round(ph*.07)}px;border-radius:2px;background:#22252c"></div>
  <div style="position:absolute;right:-4px;top:{round(ph*.25)}px;width:4px;height:{round(ph*.11)}px;border-radius:2px;background:#22252c"></div>
  <div style="width:{sw}px;height:{sh}px;border-radius:{round(pw*0.17)-bez+4}px;overflow:hidden;background:#fff;position:relative">
    <!-- Oct 21 QA: the dynamic island covered FYM's step bar, so the page sits below an iOS status bar (47pt of 390 = real safe area);
         plus the 34pt home-indicator area at the bottom; the 390x844 shot is contained (not cropped) so the X + heart row stays whole; the shot's edges are white like the screen -->
    <div style="height:{round(sw*47/390)}px;display:flex;align-items:center;justify-content:space-between;padding:0 {round(sw*.09)}px 0 {round(sw*.1)}px;font:600 {round(sw*.042)}px -apple-system,Helvetica,Arial,sans-serif;color:#000">
      <span>9:41</span><span style="display:flex;gap:{round(sw*.012)}px;align-items:center"><svg width="{round(sw*.045)}" height="{round(sw*.03)}" viewBox="0 0 18 12"><rect x="0" y="8" width="3" height="4" rx=".7"/><rect x="5" y="5.5" width="3" height="6.5" rx=".7"/><rect x="10" y="3" width="3" height="9" rx=".7"/><rect x="15" y="0" width="3" height="12" rx=".7"/></svg><svg width="{round(sw*.065)}" height="{round(sw*.03)}" viewBox="0 0 27 12"><rect x=".5" y=".5" width="22" height="11" rx="3" fill="none" stroke="#000" opacity=".4"/><rect x="2" y="2" width="19" height="8" rx="1.8"/><rect x="24" y="4" width="2" height="4" rx="1" opacity=".4"/></svg></span></div>
    <img src="{u(c['fym_img'])}" style="width:100%;height:{sh - round(sw*81/390)}px;object-fit:contain;object-position:top center;display:block">
    <div style="position:absolute;left:50%;bottom:{round(sw*8/390)}px;width:{round(sw*.35)}px;height:{max(4, round(sw*5/390))}px;margin-left:-{round(sw*.175)}px;border-radius:99px;background:#000"></div>
    <div style="position:absolute;left:50%;top:11px;width:{round(sw*.31)}px;height:{round(sw*.09)}px;margin-left:-{round(sw*.155)}px;border-radius:99px;background:#000"></div>
  </div>
</div>
<div class=c style="font:700 40px Bit;letter-spacing:.06em;color:{PINK};margin-top:40px">{SITE}</div>
</div>"""
    return RD.shell(1080, 1920, body)


# Scale the block's content (union of its children) up to fill the safe band, centred at (540, 915).
FIT = """()=>{const b=document.getElementById('blk');let t=1e9,l=1e9,r=-1e9,o=-1e9;
for(const c of b.children){const q=c.getBoundingClientRect();t=Math.min(t,q.top);l=Math.min(l,q.left);r=Math.max(r,q.right);o=Math.max(o,q.bottom)}
const s=Math.min(1010/(r-l),1310/(o-t));const cx=(l+r)/2,cy=(t+o)/2;const br=b.getBoundingClientRect();
b.style.transformOrigin=(cx-br.left)+'px '+(cy-br.top)+'px';b.style.transform='translate('+(540-cx)+'px,'+(915-cy)+'px) scale('+s+')';
const n=b.getBoundingClientRect();return [Math.round(s*1000)/1000]}"""


async def go():
    from playwright.async_api import async_playwright
    os.makedirs(OUT, exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for i, html in enumerate((frame1(), frame2(), frame3()), 1):
            pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
            tmp = f'/dev/shm/ph_story_{i}.html'; open(tmp, 'w').write(html)
            await pg.goto('file://' + tmp, wait_until='load'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(400)
            ov = await pg.evaluate("""()=>{const b=document.getElementById('blk');return b.scrollHeight-b.clientHeight}""")
            if ov > 1: print('OVERFLOW frame', i, ov)
            print('frame', i, 'fit scale', await pg.evaluate(FIT))
            await pg.screenshot(path=f'{OUT}/story-{i}.jpg', type='jpeg', quality=92); await pg.close()
        await b.close()
    print('ok', OUT)

asyncio.run(go())
