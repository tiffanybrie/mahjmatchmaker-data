"""Caprasimo MM: straight CAPITAL J (Tiffany Nov 23 2026: 'There's an alternate J... I don't like the wobbly J', said about
'Sadie Jane'). The lowercase j was straightened Nov 18; this redraws the capital the same way: Caprasimo's own top slab and
ball hook, with a straight stem between them. Writes assets/fonts/CaprasimoMM.ttf + .woff2 and the copies listed in BRAND-GUIDE.
Usage: python3 scripts/fonts_caprasimo_capJ.py"""
import os, shutil
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..') + '/'
def draw(pen):
    pen.moveTo((1034, 330))
    pen.qCurveTo((1034, 183), (960, 58), (838, -10), (650, -36), (575, -36))
    pen.qCurveTo((486, -36), (304, -1), (152, 81), (59, 223), (59, 330))
    pen.qCurveTo((59, 428), (173, 567), (276, 567))
    pen.qCurveTo((379, 567), (487, 436), (487, 338))
    pen.qCurveTo((487, 270), (505, 236), (520, 236))
    pen.qCurveTo((535, 236), (542, 262), (542, 300))
    pen.lineTo((542, 1057))
    pen.qCurveTo((542, 1096), (502, 1132), (442, 1150), (383, 1173), (343, 1224), (343, 1275))
    pen.qCurveTo((343, 1333), (411, 1384), (465, 1384))
    pen.lineTo((1070, 1384))
    pen.qCurveTo((1123, 1384), (1191, 1332), (1191, 1275))
    pen.qCurveTo((1191, 1221), (1144, 1171), (1081, 1142), (1034, 1101), (1034, 1057))
    pen.closePath()
def patch(path, out=None):
    f = TTFont(path); pen = TTGlyphPen(f.getGlyphSet()); draw(pen); f['glyf']['J'] = pen.glyph()
    f['hmtx']['J'] = (1224, 59)  # stem ends at 1034+ (was 1125 bulge): tighten the right side a touch
    f.save(out or path); return f
if __name__ == '__main__':
    import sys
    src = R + 'assets/fonts/CaprasimoMM.ttf'; patch(src)
    f = TTFont(src); f.flavor = 'woff2'; f.save(R + 'assets/fonts/CaprasimoMM.woff2')
    for c in ('scripts/social/tileprofile/fonts/Caprasimo.ttf',):
        if os.path.exists(R + c): shutil.copy(src, R + c)
    for c in ('scripts/moodboard/fonts/Caprasimo.woff2',):
        if os.path.exists(R + c): shutil.copy(R + 'assets/fonts/CaprasimoMM.woff2', R + c)
    print('Caprasimo MM capital J straightened')
