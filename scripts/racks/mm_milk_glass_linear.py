"""Middle & Main white scalloped acrylic rack, LINEAR + CLOSED for album cards (Tiffany Nov 23 2026: 'it's always open... it gets
really tall when the pusher is open and it starts to interfere with the mat'; she wants every card rack straight like the Miss
Mahjong scallops). Made from the REAL brand photo cut-out only: the pusher strip and the rack body are each straightened
(perspective) and the pusher is set down on the rack. No drawing, no AI. Usage: python3 scripts/racks/mm_milk_glass_linear.py"""
from PIL import Image
import numpy as np, os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..') + '/'
src = Image.open(R + 'assets/racks/card/middle--main-milk-glass-scalloped-acrylic.png').convert('RGBA')
def coeffs(dst, sq):
    A, B = [], []
    for (x, y), (u, v) in zip(dst, sq):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); A.append([0, 0, 0, x, y, 1, -v * x, -v * y]); B += [u, v]
    return np.linalg.solve(np.array(A, float), np.array(B, float))
def warp(q, w, h): return src.transform((w, h), Image.PERSPECTIVE, coeffs([(0, 0), (w, 0), (w, h), (0, h)], q), Image.BICUBIC)
W = 1400
body = warp([(28, 212), (1345, 190), (1400, 358), (72, 477)], W, 240)
push = warp([(0, 0), (1345, 138), (1345, 186), (0, 92)], W, 84)
out = Image.new('RGBA', (W, 290), (0, 0, 0, 0)); out.alpha_composite(push, (0, 0)); out.alpha_composite(body, (0, 48))
out.save(R + 'assets/racks/card/middle--main-milk-glass-scalloped-linear.png', optimize=True)
