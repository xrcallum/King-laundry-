"""Cut the logo badge out of the source photo as a clean transparent PNG.

The badge is a flat-colour sticker (red crown/wordmark, navy wordmark/tagline
plate, white outline and letter counters) sitting on top of the photo, not
blended into it. Its outer edge is a closed navy/red silhouette, so instead of
trying to classify every colour inside it, we find that silhouette and treat
everything it encloses as foreground -- the white outline, the white plate
under the tagline and the white letter counters all come along for free.
"""
import cv2, numpy as np

im = cv2.imread('src.jpg'); H, W = im.shape[:2]
f = im.astype(np.float32)

red = np.array([48, 67, 215], np.float32)   # BGR
navy = np.array([95, 38, 10], np.float32)
# tight box: excludes the blurred wall sign above and the folded fabric either side
bbox = np.zeros((H, W), np.uint8); bbox[144:440, 210:705] = 1

seed = ((np.linalg.norm(f - red, axis=2) < 65) | (np.linalg.norm(f - navy, axis=2) < 65)).astype(np.uint8) * bbox

E = lambda k: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))
DIL = 13
grown = cv2.dilate(seed, E(DIL))
n, lbl, stats, cent = cv2.connectedComponentsWithStats(grown, connectivity=8)
# the badge is whichever component contains this point, known to sit inside the crown
seed_pt = (455, 190)  # (x, y)
main = int(lbl[seed_pt[1], seed_pt[0]])
assert main != 0, 'seed point missed the badge — check seed_pt'
blob = (lbl == main).astype(np.uint8)
blob = cv2.erode(blob, E(DIL))
blob = cv2.morphologyEx(blob, cv2.MORPH_CLOSE, E(9))

# fill everything enclosed by the silhouette (outline ring, letter counters,
# the white plate under the tagline) by flood-filling the OUTSIDE and taking
# the complement
pad = cv2.copyMakeBorder(blob, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=0)
ff_mask = np.zeros((pad.shape[0] + 2, pad.shape[1] + 2), np.uint8)
outside = pad.copy()
cv2.floodFill(outside, ff_mask, (0, 0), 1)
filled = 1 - outside[1:-1, 1:-1]
mask = np.clip(blob | filled, 0, 1).astype(np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, E(5))
# snap any thin bridge into a stray fragment of nearby fabric (thinner than
# every real stroke in the wordmark) without eating into the letterforms
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, E(11))
# drop any disconnected speck (stray colour match elsewhere in the crop) —
# keep only the component the badge seed point belongs to
n2, lbl2 = cv2.connectedComponents(mask, connectivity=8)
mask = (lbl2 == lbl2[seed_pt[1], seed_pt[0]]).astype(np.uint8)
# crop to crown + wordmark only: below y=402 is the "We Wash It Well" tagline
# plate, whose thin italic strokes erode away unevenly under this mask radius,
# and the hero heading already carries that line as real text
mask[403:, :] = 0

# tidy the silhouette edge and feather it for antialiasing
mask_f = cv2.GaussianBlur(mask.astype(np.float32), (0, 0), 1.1)
alpha = np.clip(mask_f * 1.4 - 0.15, 0, 1)

ys, xs = np.where(mask > 0)
y0, y1, x0, x1 = ys.min() - 6, ys.max() + 7, xs.min() - 6, xs.max() + 7
y0, x0 = max(0, y0), max(0, x0); y1, x1 = min(H, y1), min(W, x1)
print('bbox', x0, y0, x1, y1, 'size', x1 - x0, y1 - y0)

crop_bgr = im[y0:y1, x0:x1]
crop_a = (alpha[y0:y1, x0:x1] * 255).astype(np.uint8)
rgba = cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2BGRA)
rgba[:, :, 3] = crop_a
cv2.imwrite('logo-mark-raw.png', rgba)

# de-halo: pull edge-pixel colour toward the nearest fully-opaque neighbour so
# no photo-background fringe survives on the cutout edge
core = (crop_a > 250).astype(np.uint8)
dist, idx = cv2.distanceTransformWithLabels(1 - core, cv2.DIST_L2, 5, labelType=cv2.DIST_LABEL_PIXEL)
ys_c, xs_c = np.where(core > 0)
label_map = np.zeros(core.shape, np.int32)
lbl_ids = np.arange(1, len(ys_c) + 1)
seed_lbl = np.zeros(core.shape, np.int32); seed_lbl[ys_c, xs_c] = lbl_ids
_, lbls = cv2.distanceTransformWithLabels((1 - core).astype(np.uint8), cv2.DIST_L2, 5)
nearest_y = ys_c[lbls - 1]; nearest_x = xs_c[lbls - 1]
clean_bgr = crop_bgr.copy().astype(np.float32)
edge = (crop_a > 0) & (crop_a <= 250)
clean_bgr[edge] = crop_bgr[nearest_y[edge], nearest_x[edge]].astype(np.float32)
rgba2 = cv2.cvtColor(np.clip(clean_bgr, 0, 255).astype(np.uint8), cv2.COLOR_BGR2BGRA)
rgba2[:, :, 3] = crop_a
cv2.imwrite('logo-mark.png', rgba2)

# checkerboard preview so transparency is visible without a viewer that supports it
ch = 12
board = (np.indices(rgba2.shape[:2]) // ch).sum(0) % 2
bg = np.where(board[..., None] == 0, 235, 255).astype(np.uint8)
bg = np.repeat(bg, 3, axis=2) if bg.shape[2] == 1 else bg
a = rgba2[:, :, 3:4].astype(np.float32) / 255
preview = (rgba2[:, :, :3].astype(np.float32) * a + bg.astype(np.float32) * (1 - a)).astype(np.uint8)
cv2.imwrite('logo-mark-preview.png', preview)
print('cutout size', rgba2.shape)
