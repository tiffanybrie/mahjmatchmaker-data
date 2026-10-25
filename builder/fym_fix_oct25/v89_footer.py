"""FYM v89 (Tiffany Oct 25 16:52): on the Mood board card the navy 'Use code MAHJMATCH to save' bar ran the full card width.
Mood board only: the bar is as wide as the 'Matched with Find Your Mat-ch™ · mahjmatchmaker.com' line above it (heart flame to the
end of .com) and centred under it. Love triangle / Showcase keep the full-width bar.
Usage: python3 v89_footer.py <build_dir>"""
import sys
P = sys.argv[1] + '/index.html'; h = open(P).read()
old = "{const x=40,w=W-80;g.fillStyle=NAVY;"
new = ("{let x=40,w=W-80;if(S.view==='stack'){/* v89: bar spans the brand line (flame to .com) */g.font='700 27px Bitter, Georgia, serif';const wa=g.measureText('Matched with Find Your Mat-ch\\u2122').width;"
       "g.font='600 25px Bitter, Georgia, serif';const wb=g.measureText('mahjmatchmaker.com').width,iw=icon?icon.width*42/icon.height:0;w=iw+14+wa+34+wb;x=(W-w)/2;}g.fillStyle=NAVY;")
assert h.count(old) == 1; h = h.replace(old, new); open(P, 'w').write(h); print('ok')
