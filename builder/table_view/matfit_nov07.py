"""Table view mat fit helpers (Nov 7, Tiffany 10:22pm 'get table view completely updated'). Vendor photos only, never AI.
analyze(img) finds the mat in a product photo shot on a plain studio backdrop: background = the colour of the photo's outer ring,
flood-filled from the edges; mat = the largest remaining shape (holes filled). Returns the mat's 4 corners (minimum-area
rectangle, or the convex-hull quad when the shot has a little keystone) plus measures used to decide by eye:
  ring_uniform  share of the outer ring that is backdrop (low = full-bleed mat or a room/scene photo: no crop needed / look)
  fill          mask area / quad area (1.0 = a clean flat rectangle; < .95 = rolled, angled, props sticking out)
  aspect        short / long side of the quad (a mat is square; < .93 = angled or cropped)
  margin        largest backdrop margin as a share of the photo side
warp_square(img, quad, px, inset) straightens (perspective) a top-down shot into a square that is all mat: used for vendor
photos that become the Table view image (D.tv.mo). affine(quad, W, H, inset) = canvas transform (photo 0..1 -> card 0..1) that
crops/straightens the app's OWN FYM photo with no new bytes (D.tv.fa)."""
import numpy as np, cv2
from PIL import Image
from scipy import ndimage

def flatten(im):
    """transparent PNG/WebP product shots (Let's Mahj On) -> on white, so the backdrop is found (RGBA -> RGB alone makes it black)"""
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA'); bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[3]); return bg
    return im.convert('RGB')

def _ring(a, r):
    return np.concatenate([a[:r].reshape(-1, 3), a[-r:].reshape(-1, 3), a[:, :r].reshape(-1, 3), a[:, -r:].reshape(-1, 3)]).astype(float)

def order_quad(q):
    q = np.asarray(q, float); c = q.mean(0); ang = np.arctan2(q[:, 1] - c[1], q[:, 0] - c[0]); q = q[np.argsort(ang)]
    i = np.argmin(q.sum(1)); q = np.roll(q, -i, 0)  # start top-left, clockwise (y down): tl, tr, br, bl
    if q[1][0] < q[3][0]: q = q[[0, 3, 2, 1]]
    return q

def analyze(im, tol=26):
    im = flatten(im); a = np.asarray(im).astype(float); H, W = a.shape[:2]; r = max(2, int(.015 * min(W, H)))
    ring = _ring(a, r); bgc = np.median(ring, 0)
    ring_uniform = float((np.sqrt(((ring - bgc) ** 2).sum(1)) < tol).mean())
    out = {'W': W, 'H': H, 'ring_uniform': round(ring_uniform, 3), 'bg': [int(x) for x in bgc]}
    if ring_uniform < .6:
        out.update(kind='bleed', quad=[[0, 0], [W, 0], [W, H], [0, H]], fill=1.0, aspect=round(min(W, H) / max(W, H), 3), margin=0.0)
        return out
    d = np.sqrt(((a - bgc) ** 2).sum(2)); near = d < tol
    lb, n = ndimage.label(near); edge = set(np.unique(np.r_[lb[0], lb[-1], lb[:, 0], lb[:, -1]])) - {0}
    bg = np.isin(lb, list(edge)); m = ~bg
    m = ndimage.binary_opening(m, iterations=2); lb, n = ndimage.label(m)
    if not n:
        out.update(kind='none'); return out
    sz = ndimage.sum(m, lb, range(1, n + 1)); m = ndimage.binary_fill_holes(lb == (np.argmax(sz) + 1))
    ys, xs = np.nonzero(m); pts = np.c_[xs, ys].astype(np.float32)
    rect = cv2.minAreaRect(pts); box = cv2.boxPoints(rect)
    hull = cv2.convexHull(pts); peri = cv2.arcLength(hull, True); quad = None
    for eps in (.01, .015, .02, .03, .04):
        ap = cv2.approxPolyDP(hull, eps * peri, True)
        if len(ap) == 4: quad = ap.reshape(4, 2); break
    q = order_quad(quad if quad is not None else box)
    area = cv2.contourArea(q.astype(np.float32)); fill = float(m.sum() / max(area, 1))
    sides = [np.linalg.norm(q[i] - q[(i + 1) % 4]) for i in range(4)]
    aspect = min((sides[0] + sides[2]) / 2, (sides[1] + sides[3]) / 2) / max((sides[0] + sides[2]) / 2, (sides[1] + sides[3]) / 2)
    margin = max(q[:, 0].min() / W, 1 - q[:, 0].max() / W, q[:, 1].min() / H, 1 - q[:, 1].max() / H)
    bbox_fill = float(m.sum() / (W * H))
    out.update(kind='studio', quad=q.round(1).tolist(), fill=round(min(fill, 1.5), 3), aspect=round(float(aspect), 3),
               margin=round(float(margin), 3), mat_share=round(bbox_fill, 3))
    return out

def _inset(q, inset):
    q = np.asarray(q, float); c = q.mean(0); return c + (q - c) * (1 - 2 * inset)

def warp_square(im, quad, px=900, inset=.006):
    q = _inset(quad, inset).astype(np.float32); dst = np.float32([[0, 0], [px, 0], [px, px], [0, px]])
    Mx = cv2.getPerspectiveTransform(q, dst); a = np.asarray(flatten(im))
    w = cv2.warpPerspective(a, Mx, (px, px), flags=cv2.INTER_AREA if max(a.shape[:2]) > 2 * px else cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return Image.fromarray(w)

def affine(quad, W, H, inset=.008):
    """canvas setTransform (a,b,c,d,e,f) in 0..1 units: photo unit coords -> card unit coords, so the quad's tl/tr/bl land on the
    card's corners (an affine: right for straight or rotated shots, the small keystone of a near-top-down shot is ignored)."""
    q = _inset(quad, inset) / np.array([W, H], float); P0, P1, P3 = q[0], q[1], q[3]
    A = np.linalg.inv(np.c_[P1 - P0, P3 - P0]); t = -A @ P0
    return [round(float(x), 6) for x in (A[0, 0], A[1, 0], A[0, 1], A[1, 1], t[0], t[1])]
