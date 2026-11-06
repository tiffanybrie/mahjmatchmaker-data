"""Wed Nov 11 (Juniper launch): single-image "It's a mat-ch!" (slide 1 only, like the Papaya post that earned the
most follows) + its 9:16 story. Pair = Tiffany's #1 from her Nov 6 2:26am round-3 notes: Palm Royale (Mahj Tile Haus,
a matched non-partner = allowed). Tile circle = OMM's PILE photo (her note 12: never the scatter shot).
Slide 2 (album card) is left out on purpose until her round-3 card fixes land."""
import asyncio, os, sys, tempfile
sys.path.insert(0, '/home/claude/mahjmatchmaker-data/scripts/social/its_a_match')
import render as R
c = dict(tile='Juniper', short='Juniper', tile_brand='Oh My Mahjong', mat='Palm Royale', mat_brand='Mahj Tile Haus',
         count=int(os.environ.get('COUNT', 31)),
         tile_img=f'{R.R}/assets/launches/omm-juniper-mahjong-tiles/06-Tile_Juniper_F.jpg',
         mat_img=f'{R.R}/assets/colorcards/juniper/mats/palm-royale-mahj-tile-haus.jpg')
od = f'{R.R}/assets/social/week-2026-11-09/final/wed-juniper'
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for name, (W, Ht, html) in [('slide1', R.slide1(c, 'feed')), ('story-1', R.slide1(c, 'story'))]:
            pg = await b.new_page(viewport={'width': W, 'height': Ht})
            # Caveat's slant/'!' overhang pulls the headline right ~16px: nudge it back (center_check)
            html = html.replace('class=c style="font-family:Hand;', 'class=c style="position:relative;left:%dpx;font-family:Hand;' % (-15 if Ht == 1350 else -18), 1)
            t = os.path.join(tempfile.gettempdir(), f'jun_{name}.html'); open(t, 'w').write(html)
            await pg.goto('file://' + t, wait_until='load'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(400)
            br = await pg.evaluate("[...document.images].filter(i=>!i.naturalWidth).length")
            ov = await pg.evaluate("(()=>{const b=document.getElementById('blk');return b.scrollHeight-b.clientHeight})()")
            print(name, 'broken imgs', br, 'overflow', ov)
            await pg.screenshot(path=f'{od}/{name}.jpg', type='jpeg', quality=92); await pg.close()
        await b.close()
asyncio.run(main())
