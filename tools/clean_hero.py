"""Region-aware stain removal for the LaundryKings hero photograph.

Every garment in the photo is a hand-mapped band; inside each band, dirt is
detected relative to that garment's own dominant colour (or its lightness for
same-hue soiling), then filled from the garment's clean pixels. The logo is
protected by a mask seeded on its flat red and navy and never touched.

Usage: python3 tools/clean_hero.py <source.jpg>   (writes into the current dir:
       laundrykings-hero-clean.jpg, og-card.png and review crops)
"""
import cv2, numpy as np, sys

im = cv2.imread(sys.argv[1] if len(sys.argv) > 1 else 'src.jpg'); H, W = im.shape[:2]
f = im.astype(np.float32)
lab = cv2.cvtColor(im, cv2.COLOR_BGR2LAB).astype(np.float32)
L = lab[..., 0] * 100 / 255; A = lab[..., 1] - 128; B = lab[..., 2] - 128
C = np.hypot(A, B)
hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV); Hh, S, V = [hsv[..., i].astype(int) for i in range(3)]
E = lambda k: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))
b8 = lambda m: m.astype(np.uint8); bb = lambda m: m.astype(bool)
def rect(x0, y0, x1, y1):
    m = np.zeros((H, W), np.uint8); m[max(0, y0):y1, x0:x1] = 1; return m

red = np.array([48, 67, 215], np.float32); navy = np.array([95, 38, 10], np.float32)
seed = ((np.linalg.norm(f - red, axis=2) < 70) | (np.linalg.norm(f - navy, axis=2) < 70)) & bb(rect(200, 125, 720, 450))
logo = bb(cv2.morphologyEx(cv2.dilate(b8(seed), E(15)), cv2.MORPH_CLOSE, E(9)))

def boundary(x0, x1, ys, ye, cond, run=4, default=None, win=41):
    arr = []
    for x in range(x0, x1):
        yy, c = (default if default is not None else ye), 0
        for y in range(ys, ye):
            if cond(y, x):
                c += 1
                if c >= run: yy = y - run + 1; break
            else: c = 0
        arr.append(yy)
    arr = np.array(arr, float); k = win // 2
    out = [np.median(arr[max(0, i - k):i + k + 1]) for i in range(len(arr))] if win > 1 else arr
    return {x0 + i: int(out[i]) for i in range(len(out))}

isnavy = lambda y, x: 100 <= Hh[y, x] <= 132 and S[y, x] > 55 and V[y, x] < 135
white_ = lambda y, x: S[y, x] < 30 and V[y, x] > 175
XL0, XL1 = 0, 312
h_top = boundary(XL0, XL1, 20, 120, lambda y, x: 95 <= Hh[y, x] <= 130 and S[y, x] > 80, default=50)
# the hoodie's top edge is never above this line; stops the band grabbing the wall sign
h_top = {x: max(y, 42 if x < 130 else int(40 + (x - 130) * 56 / 170)) for x, y in h_top.items()}
r_top = boundary(XL0, XL1, 130, 215, lambda y, x: A[y, x] > 25 and S[y, x] > 100, default=160)
p_top = boundary(XL0, XL1, 190, 270, lambda y, x: L[y, x] > 58 and A[y, x] > 15 and B[y, x] < 20, default=222)
d_top = boundary(XL0, XL1, 255, 320, lambda y, x: B[y, x] < -8 and 95 <= Hh[y, x] <= 128, default=285)
t_top = boundary(XL0, XL1, 315, 375, lambda y, x: A[y, x] < -8 and B[y, x] < -5, default=340)
g_top = boundary(XL0, 245, 360, 405, lambda y, x: C[y, x] < 12 and L[y, x] > 55, default=385)
box_top = boundary(XL0, 152, 405, 445, lambda y, x: C[y, x] > 20 and B[y, x] > 15 and L[y, x] < 78, run=5, default=432)
XC0, XC1 = 150, 745
ct_top = boundary(XC0, XC1, 340, 470, lambda y, x: (not logo[y, x]) and S[y, x] < 28 and V[y, x] > 200, run=6, default=380, win=9)
k_top  = boundary(XC0, XC1, 436, 482, lambda y, x: C[y, x] > 17 and B[y, x] > 12 and L[y, x] < 84, default=462)
n_top  = boundary(XC0, XC1, 500, 550, isnavy, default=530)
XR0 = 708
tw_top = boundary(XR0, W, 78, 140, white_, run=5, default=96)
o_top  = boundary(700, W, 165, 225, lambda y, x: C[y, x] > 35, default=200)
g2_top = boundary(700, W, 240, 300, lambda y, x: A[y, x] < -10, default=270)
n2_top = boundary(700, W, 300, 360, isnavy, default=328)
tw2_top = boundary(700, W, 350, 400, white_, run=5, default=372)
rk_top = boundary(700, W, 470, 522, lambda y, x: C[y, x] > 17 and B[y, x] > 12 and L[y, x] < 82, default=496)
rn_top = boundary(700, W, 520, 557, isnavy, default=541)

def band(x0, x1, top, bot):
    m = np.zeros((H, W), np.uint8)
    for x in range(x0, x1):
        t = top[x] if isinstance(top, dict) else top; b = bot[x] if isinstance(bot, dict) else bot
        if b > t: m[t:b, x] = 1
    return m

regions = [
 ('cool',  'hoodie',   band(XL0, XL1, h_top, r_top)),
 ('warm',  'rust',     band(XL0, XL1, r_top, p_top)),
 ('tcool', 'pink',     band(XL0, XL1, p_top, d_top)),
 ('cool',  'denim',    band(XL0, XL1, d_top, t_top)),
 ('cool',  'teal',     band(XL0, 245, t_top, g_top) | band(245, XL1, t_top, 386)),
 ('white', 'grey',     band(XL0, 152, g_top, box_top) | band(152, 245, g_top, 430)),
 ('white', 'c-towel',  band(XC0, XC1, ct_top, k_top)),
 ('khaki', 'c-shirt',  band(XC0, XC1, k_top, n_top)),
 ('cool',  'c-navy',   band(XC0, XC1, n_top, H)),
 ('white', 'r-towel1', band(XR0, W, tw_top, o_top)),
 ('lum',   'orange',   band(700, W, o_top, g2_top)),
 ('cool',  'green',    band(700, W, g2_top, n2_top)),
 ('cool',  'r-navy',   band(700, W, n2_top, tw2_top)),
 ('white', 'r-towel2', band(700, W, tw2_top, rk_top)),
 ('khaki', 'r-khaki',  band(XC1, W, rk_top, rn_top)),
 ('cool',  'r-navy2',  band(XC1, W, rn_top, H)),
]
DIRT = np.array([10.0, 24.0])

def mode_ab(m):
    hist, ae, be = np.histogram2d(A[m], B[m], bins=[np.arange(-128, 130, 3)] * 2)
    i, j = np.unravel_index(np.argmax(hist), hist.shape)
    return np.array([ae[i] + 1.5, be[j] + 1.5])

def tvec(base):
    d = DIRT - base; dd = float(d @ d) + 1e-6
    v = np.stack([A - base[0], B - base[1]], -1)
    return (v @ d) / dd, np.hypot(v[..., 0], v[..., 1])

def fabric_mask(kind, R):
    Rb = bb(R)
    if kind in ('cool', 'tcool', 'warm', 'lum'):
        m = Rb & ((S > 55) | (V < 170))
    elif kind == 'white':
        t, vn = tvec(np.array([0.0, 0.0]))
        m = Rb & (((S < 35) & (V > 150)) | ((t > 0.3) & (L > 45) & (C < 34) & (V > 110)))
    else:
        m = Rb & (C > 10) & (V > 45)
    m = bb(cv2.morphologyEx(b8(m), cv2.MORPH_OPEN, E(3)))
    if kind != 'white':
        # keep the garment body only: drop stray blobs (screw heads, sign lettering)
        n, lbl, stats, _ = cv2.connectedComponentsWithStats(b8(m), connectivity=8)
        if n > 1:
            areas = stats[1:, cv2.CC_STAT_AREA]; keep = np.where(areas >= 0.05 * areas.max())[0] + 1
            m = np.isin(lbl, keep)
    return m

WARM_T = {'orange': (0.17, 6), 'rust': (0.33, 10)}
def stain(kind, fm, name=''):
    base = mode_ab(fm) if kind != 'white' else np.array([0.0, 0.0])
    t, vn = tvec(base)
    if kind == 'cool':
        m = ((t > 0.18) & (vn > 5)) | ((Hh >= 5) & (Hh <= 40) & (S > 40) & (V < 185))
        clean = t < 0.08
    elif kind == 'tcool':
        m = (t > 0.26) & (vn > 7); clean = t < 0.12
    elif kind == 'warm':
        tt, vv = WARM_T.get(name, (0.33, 10))
        m = (t > tt) & (vn > vv); clean = t < 0.12
    elif kind == 'lum':
        # dirt on this fabric is the same hue, only darker: work on lightness alone
        bl = np.percentile(L[fm], 78)
        m = L < bl - 5; clean = L >= bl - 3
    elif kind == 'white':
        loc = B - cv2.GaussianBlur(B, (0, 0), 14)
        m = (((t > 0.30) & (vn > 7)) | ((loc > 3.5) & (B > 6) & (vn > 5))) & (L > 62)
        clean = (t < 0.12) & (loc < 2)
    else:
        bl = np.percentile(L[fm], 75)
        top = fm & (L >= bl - 3)
        base = mode_ab(top)
        m = (L < bl - 6) | (A > base[0] + 5) | (B > base[1] + 7)
        clean = (L >= bl - 3) & (np.abs(A - base[0]) <= 4) & (np.abs(B - base[1]) <= 5)
    return m & fm, clean & fm & ~m, base

def nc(img, w, sg):
    num = cv2.GaussianBlur(img * w[..., None], (0, 0), sg); den = cv2.GaussianBlur(w, (0, 0), sg)
    return num / np.maximum(den, 1e-6)[..., None], den

def fill(img, clean, st):
    w = clean.astype(np.float32)
    # smooth multi-scale normalised convolution: local detail where clean pixels are near,
    # falling back to broader averages without hard seams between scales
    base, den = nc(img, w, 150); base[den < 1e-3] = img[den < 1e-3]
    for sg in (40, 14, 6):
        b, d = nc(img, w, sg)
        a = np.clip(d * 2.2, 0, 1)[..., None]
        base = a * b + (1 - a) * base
    g = cv2.cvtColor(np.clip(img, 0, 255).astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32)
    hf = g - cv2.GaussianBlur(g, (0, 0), 1.4)
    return base + (hf * 0.3)[..., None]

out = f.copy(); allst = np.zeros((H, W), bool); allfab = np.zeros((H, W), bool)
for kind, name, R in regions:
    fm = fabric_mask(kind, R) & ~logo
    if fm.sum() < 200: print(name, 'empty'); continue
    st, clean, base = stain(kind, fm, name)
    st = bb(cv2.morphologyEx(b8(st), cv2.MORPH_OPEN, np.ones((2, 2), np.uint8)))
    st = bb(cv2.dilate(b8(st), E(5))) & fm
    if kind in ('cool', 'tcool', 'warm', 'lum'):
        # leave the soft out-of-focus garment edge alone so it stays soft
        st &= bb(cv2.erode(b8(fm), E(5)))
    elif kind == 'white':
        # keep the natural shadow line along a towel's top and bottom edge
        st &= bb(cv2.erode(b8(fm), np.ones((9, 1), np.uint8)))
    clean &= ~st
    if clean.sum() < 300: clean = fm & ~st
    print(f'{name:9s} {kind:5s} base ab=({base[0]:+.0f},{base[1]:+.0f}) fabric={int(fm.sum()):6d} stain={100*st.sum()/fm.sum():4.1f}% clean-ref={100*clean.sum()/fm.sum():4.1f}%')
    if not st.any(): continue
    filled = fill(out, clean, st)
    alpha = np.clip(cv2.GaussianBlur(st.astype(np.float32), (0, 0), 2.0) * fm * 1.2, 0, 1); alpha[logo] = 0
    out = out * (1 - alpha[..., None]) + filled * alpha[..., None]
    allst |= st; allfab |= fm

res = np.clip(out, 0, 255).astype(np.uint8)
cv2.imwrite('laundrykings-hero-clean.jpg', res, [cv2.IMWRITE_JPEG_QUALITY, 94])
cv2.imwrite('zoom7_right.png', cv2.resize(np.hstack([im[80:557, 690:980], res[80:557, 690:980]]), None, fx=1.6, fy=1.6, interpolation=cv2.INTER_CUBIC))
cv2.imwrite('compare7.png', np.vstack([im, res]))
# Open Graph card 1200x630: scale to width, centre-crop height (logo sits mid-frame)
og = cv2.resize(res, (1200, round(H * 1200 / W)), interpolation=cv2.INTER_LANCZOS4)
y0 = (og.shape[0] - 630) // 2
cv2.imwrite('og-card.png', og[y0:y0 + 630])
print('og-card', og[y0:y0 + 630].shape)
