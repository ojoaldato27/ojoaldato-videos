"""Motor «pixel 3D» (21/10/2026, Iker: «modo pixel 3D»): mundos de vóxeles (cubitos) en perspectiva isométrica,
dibujados a 270×480 y ampliados ×4 sin suavizar, con contorno oscuro y sombreado por caras, como un videojuego.

Model(G, N, pivot): G uint8 (X, Y, Z) con el material de cada vóxel (0 = vacío), N uint8 con un tono fijo por vóxel
(textura que gira con el modelo) y un pivote (punto que se coloca en el mundo).
rot(M, yaw, pitch, roll) gira el modelo (re-muestreo al vóxel más cercano, con caché por ángulo).
Canvas(s, cx, cy): lienzo de baja resolución con z-buffer; put() coloca modelos en coordenadas del mundo."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

LW, LH, PX = 270, 480, 4
FONT = "/home/claude/shorts-ingenieria/fonts/pixel/PressStart2P.ttf"
OUTLINE = np.array((16, 14, 26), np.float32)
LIGHT = (1.0, 0.80, 0.60)              # cara de arriba, cara izquierda (+z), cara derecha (+x)

# ------------------------------------------------------------------ materiales
PAL = np.zeros((256, 3), np.float32)
EMIT = np.zeros(256, bool)
_NAMES = {}


def mat(name, rgb=None, emit=False):
    if name in _NAMES and rgb is None:
        return _NAMES[name]
    i = _NAMES.setdefault(name, len(_NAMES) + 1)
    PAL[i] = rgb
    EMIT[i] = emit
    return i


STEEL = mat("steel", (182, 187, 194))
GLASS = mat("glass", (36, 44, 62))
TIRE = mat("tire", (30, 30, 34))
HUB = mat("hub", (132, 136, 146))
CLAD = mat("clad", (62, 64, 70))
WELL = mat("well", (20, 20, 24))
LAMP = mat("lamp", (255, 250, 232), True)
TAIL = mat("tail", (240, 44, 50), True)
SEAM = mat("seam", (150, 155, 163))


# ------------------------------------------------------------------ modelos
class Model:
    def __init__(self, G, N=None, pivot=None, seed=1):
        self.G = G
        if N is None:
            N = np.random.default_rng(seed).integers(0, 256, G.shape).astype(np.uint8)
        self.N = N
        X, Y, Z = G.shape
        self.pivot = pivot if pivot is not None else ((X - 1) / 2, -0.5, (Z - 1) / 2)


def box(G, x0, x1, y0, y1, z0, z1, m):
    G[max(0, x0):x1, max(0, y0):y1, max(0, z0):z1] = m


def fn_model(shape, f, seed=1, pivot=None):
    """Modelo a partir de una función f(x, y, z) → material (arrays de índices)."""
    x, y, z = np.meshgrid(np.arange(shape[0]), np.arange(shape[1]), np.arange(shape[2]), indexing="ij")
    return Model(f(x, y, z).astype(np.uint8), seed=seed, pivot=pivot)


def _R(yaw, pitch, roll):
    cy, sy = math.cos(yaw), math.sin(yaw)
    cp, sp = math.cos(pitch), math.sin(pitch)
    cr, sr = math.cos(roll), math.sin(roll)
    Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    Rz = np.array([[cp, -sp, 0], [sp, cp, 0], [0, 0, 1]])        # cabeceo: el morro (+x) sube con pitch > 0
    Rx = np.array([[1, 0, 0], [0, cr, -sr], [0, sr, cr]])        # vuelco lateral
    return Ry @ Rz @ Rx


_ROT = {}


def rot(M, yaw=0.0, pitch=0.0, roll=0.0, q=4):
    """Gira el modelo (grados) alrededor de su centro; devuelve otro Model con el pivote girado."""
    qy, qp, qr = (int(round(a / q)) * q % 360 for a in (yaw, pitch, roll))
    if qy == qp == qr == 0:
        return M
    key = (id(M), qy, qp, qr)
    if key in _ROT:
        return _ROT[key]
    R = _R(math.radians(qy), math.radians(qp), math.radians(qr))
    X, Y, Z = M.G.shape
    c = np.array([(X - 1) / 2, (Y - 1) / 2, (Z - 1) / 2])
    corners = np.array([[a, b, d] for a in (-0.5, X - 0.5) for b in (-0.5, Y - 0.5) for d in (-0.5, Z - 0.5)]) - c
    rc = corners @ R.T
    lo, hi = np.floor(rc.min(0)), np.ceil(rc.max(0))
    shp = (hi - lo + 1).astype(int)
    o = np.stack(np.meshgrid(*[np.arange(n) for n in shp], indexing="ij"), -1).reshape(-1, 3) + lo
    src = np.rint(o @ R + c).astype(int)                          # inversa: R^T aplicada por la derecha
    ok = np.all((src >= 0) & (src < np.array([X, Y, Z])), 1)
    G2 = np.zeros(len(o), np.uint8)
    N2 = np.zeros(len(o), np.uint8)
    s_ = src[ok]
    G2[ok] = M.G[s_[:, 0], s_[:, 1], s_[:, 2]]
    N2[ok] = M.N[s_[:, 0], s_[:, 1], s_[:, 2]]
    G2 = G2.reshape(shp)
    N2 = N2.reshape(shp)
    pv = (np.array(M.pivot) - c) @ R.T - lo
    out = Model(G2, N2, tuple(pv))
    _ROT[key] = out
    return out


# ------------------------------------------------------------------ render (cubos rígidos, cámara ortográfica libre)
class Sprite:
    pass


_SPR = {}
_FACES = {}
DIRS = np.array([(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)], np.float32)
LVEC = np.array((-0.1, 0.3, 0.1), np.float32)          # luz fija del mundo: arriba 1,0 · +z 0,8 · +x 0,6 · −x 0,8 · −z 0,6


class Cam:
    """Cámara ortográfica: yaw (giro alrededor del eje vertical), elev (inclinación), k (píxeles por vóxel)."""
    def __init__(self, yaw=45.0, elev=30.0, k=5.6):
        self.yaw, self.elev, self.k = yaw, elev, k
        t, f = math.radians(yaw), math.radians(elev)
        self.right = np.array((math.cos(t), 0, -math.sin(t)), np.float32)
        self.fh = np.array((math.sin(t), 0, math.cos(t)), np.float32)
        self.sf, self.cf = math.sin(f), math.cos(f)
        self.view = self.fh * self.cf + np.array((0, 1, 0), np.float32) * self.sf

    def key(self):
        return (round(self.yaw * 2) / 2, round(self.elev * 2) / 2, round(self.k, 2))

    def proj(self, p):
        """p: (..., 3) → sx, sy, depth (más grande = más cerca)."""
        p = np.asarray(p, np.float32)
        h = p @ self.fh
        return self.k * (p @ self.right), self.k * (h * self.sf - p[..., 1] * self.cf), h * self.cf + p[..., 1] * self.sf


def _faces(M):
    if id(M) not in _FACES:
        G = M.G > 0
        P = np.pad(G, 1)
        out = []
        for di, (a, b, c) in enumerate(DIRS.astype(int)):
            nb = P[1 + a:P.shape[0] - 1 + a, 1 + b:P.shape[1] - 1 + b, 1 + c:P.shape[2] - 1 + c]
            xs, ys, zs = np.nonzero(G & ~nb)
            out.append((xs, ys, zs, np.full(len(xs), di)))
        xs, ys, zs, di = (np.concatenate(v) for v in zip(*out))
        _FACES[id(M)] = (xs, ys, zs, di, M.G[xs, ys, zs], M.N[xs, ys, zs])
    return _FACES[id(M)]


def render(M, cam, yaw=0.0, pitch=0.0, roll=0.0, q=2, outline=True, edge=True, grid=True):
    qy, qp, qr = (int(round(a / q)) * q % 360 for a in (yaw, pitch, roll))
    k = (id(M), cam.key(), qy, qp, qr, outline, edge, grid)
    if k in _SPR:
        return _SPR[k]
    R = _R(math.radians(qy), math.radians(qp), math.radians(qr)).astype(np.float32)
    xs, ys, zs, di, m, tone = _faces(M)
    nrm = DIRS[di] @ R.T
    vis = nrm @ cam.view > 1e-3
    xs, ys, zs, di, m, tone, nrm = xs[vis], ys[vis], zs[vis], di[vis], m[vis], tone[vis], nrm[vis]
    sp = Sprite()
    if len(xs) == 0:
        sp.rgb, sp.mask, sp.dep = np.zeros((1, 1, 3), np.float32), np.zeros((1, 1), bool), np.zeros((1, 1), np.float32)
        sp.ax = sp.ay = 0
        _SPR[k] = sp
        return sp
    n = max(3, int(math.ceil(cam.k * 1.45)))
    g = (np.arange(n, dtype=np.float32) + 0.5) / n - 0.5
    ga, gb = np.meshgrid(g, g, indexing="ij")
    ga, gb = ga.ravel(), gb.ravel()
    border = (np.abs(ga) > 0.5 - 1.0 / n) | (np.abs(gb) > 0.5 - 1.0 / n)
    base = DIRS[di]
    t1 = np.roll(base, 1, 1)
    t2 = np.roll(base, 2, 1)
    cen = np.stack([xs, ys, zs], 1).astype(np.float32) + 0.5 * base - np.array(M.pivot, np.float32)
    pts = (cen[:, None, :] + ga[None, :, None] * t1[:, None, :] + gb[None, :, None] * t2[:, None, :]).reshape(-1, 3) @ R.T
    sx, sy, dep = cam.proj(pts)
    ix, iy = np.floor(sx).astype(np.int32), np.floor(sy).astype(np.int32)
    x0, y0 = ix.min() - 2, iy.min() - 2
    w, h = int(ix.max() - x0 + 3), int(iy.max() - y0 + 3)
    idx = (iy - y0) * w + (ix - x0)
    order = np.lexsort((-dep, idx))
    ids = idx[order]
    sel = order[np.r_[True, ids[1:] != ids[:-1]]]
    fi = sel // len(ga)
    si = sel % len(ga)
    mm = m[fi]
    lf = 0.7 + nrm[fi] @ LVEC
    lf = np.where(EMIT[mm], 0.97, lf)
    gf = np.where(border[si], 0.9, 1.0) if grid else 1.0
    col = PAL[mm] * (lf * gf * (1 + (tone[fi].astype(np.float32) - 128) / 128 * 0.035))[:, None]
    rgb = np.zeros((h * w, 3), np.float32)
    D = np.full(h * w, -1e9, np.float32)
    rgb[idx[sel]] = col
    D[idx[sel]] = dep[sel]
    sp = _post(rgb.reshape(h, w, 3), D.reshape(h, w), outline, edge)
    sp.ax, sp.ay = -x0, -y0
    _SPR[k] = sp
    return sp


def _post(rgb, D, outline, edge):
    mask = D > -1e8
    if edge:                                   # línea oscura donde hay un salto de profundidad (siluetas internas)
        e = np.zeros_like(mask)
        for dy, dx in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            Dn = np.roll(np.roll(D, dy, 0), dx, 1)
            e |= mask & (Dn > D + 3.5)
        rgb[e] *= 0.58
    if outline:                                # contorno exterior de 1 píxel
        dil = mask.copy()
        Dd = D.copy()
        for dy, dx in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            dil |= np.roll(np.roll(mask, dy, 0), dx, 1)
            Dd = np.maximum(Dd, np.roll(np.roll(D, dy, 0), dx, 1))
        ring = dil & ~mask
        rgb[ring] = OUTLINE
        D = np.where(ring, Dd - 0.2, D)
        mask = dil
    sp = Sprite()
    sp.rgb, sp.mask, sp.dep = rgb, mask, D
    return sp


# ------------------------------------------------------------------ lienzo con z-buffer
class Canvas:
    def __init__(self, cam=None, cx=135, cy=240, bg=None):
        self.cam = cam or Cam()
        self.cx, self.cy = cx, cy
        self.c = np.zeros((LH, LW, 3), np.float32) if bg is None else np.array(bg, np.float32).copy()
        self.d = np.full((LH, LW), -1e9, np.float32)

    def P(self, x, y, z):
        sx, sy, _ = self.cam.proj(np.array((x, y, z), np.float32))
        return float(sx) + self.cx, float(sy) + self.cy

    def depth(self, x, y, z):
        return float(self.cam.proj(np.array((x, y, z), np.float32))[2])

    def blit(self, sp, ox, oy, dofs, tint=None, alpha=1.0):
        h, w = sp.mask.shape
        X0, Y0 = max(0, ox), max(0, oy)
        X1, Y1 = min(LW, ox + w), min(LH, oy + h)
        if X1 <= X0 or Y1 <= Y0:
            return
        m = sp.mask[Y0 - oy:Y1 - oy, X0 - ox:X1 - ox]
        dd = sp.dep[Y0 - oy:Y1 - oy, X0 - ox:X1 - ox] + dofs
        zone = self.d[Y0:Y1, X0:X1]
        ok = m & (dd > zone)
        src = sp.rgb[Y0 - oy:Y1 - oy, X0 - ox:X1 - ox]
        if tint is not None:
            src = src * np.array(tint, np.float32) / 255
        dst = self.c[Y0:Y1, X0:X1]
        if alpha < 1:
            dst[ok] = dst[ok] * (1 - alpha) + src[ok] * alpha
        else:
            dst[ok] = src[ok]
            zone[ok] = dd[ok]

    def put(self, M, x, y, z, yaw=0, pitch=0, roll=0, tint=None, alpha=1.0, **kw):
        sp = render(M, self.cam, yaw, pitch, roll, **kw)
        X, Y = self.P(x, y, z)
        self.blit(sp, int(round(X - sp.ax)), int(round(Y - sp.ay)), self.depth(x, y, z), tint, alpha)

    def dot(self, x, y, z, col, size=2, alpha=1.0):
        X, Y = self.P(x, y, z)
        X, Y = int(round(X - size / 2)), int(round(Y - size / 2))
        dep = self.depth(x, y, z)
        ys, xs = slice(max(0, Y), min(LH, Y + size)), slice(max(0, X), min(LW, X + size))
        zone = self.d[ys, xs]
        ok = dep > zone
        dst = self.c[ys, xs]
        dst[ok] = dst[ok] * (1 - alpha) + np.array(col, np.float32) * alpha

    def shadow(self, pts, k=0.4):
        """Sombra: polígono de puntos del mundo (x, y, z) que oscurece lo ya dibujado."""
        im = Image.new("L", (LW, LH), 0)
        ImageDraw.Draw(im).polygon([self.P(*p) for p in pts], fill=255)
        m = np.asarray(im) > 0
        self.c[m] *= 1 - k

    def car_shadow(self, M, x, y, z, yaw=0, k=0.38, grow=1.0):
        X, _, Z = M.G.shape
        hx, hz = X / 2 * grow, Z / 2 * grow
        c, s_ = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
        pts = []
        for a, b in ((-hx, -hz), (hx, -hz), (hx, hz), (-hx, hz)):
            pts.append((x + a * c + b * s_, y, z - a * s_ + b * c))
        self.shadow(pts, k)

    def text(self, xy, txt, col, size=8, anchor="mm", shadow=True):
        im = Image.new("L", (LW, LH), 0)
        d = ImageDraw.Draw(im)
        d.fontmode = "1"
        fo = font(size)
        if shadow:
            sh = Image.new("L", (LW, LH), 0)
            sd = ImageDraw.Draw(sh)
            sd.fontmode = "1"
            sd.text((xy[0] + 1, xy[1] + 1), txt, font=fo, fill=255, anchor=anchor)
            self.c[np.asarray(sh) > 0] = OUTLINE
        d.text(xy, txt, font=fo, fill=255, anchor=anchor)
        self.c[np.asarray(im) > 0] = col

    def image(self):
        return Image.fromarray(np.clip(self.c, 0, 255).astype(np.uint8)).resize((LW * PX, LH * PX), Image.NEAREST)


# ------------------------------------------------------------------ fondos
BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]], np.float32) / 16


def sky(cols, y0=0, y1=LH):
    """Degradado por bandas con tramado 4×4 (como las consolas de 16 bits). cols: lista de colores de arriba a abajo."""
    ys = np.arange(LH, dtype=np.float32)[:, None]
    u = np.clip((ys - y0) / max(1, y1 - y0), 0, 1) * (len(cols) - 1)
    xs = np.arange(LW)[None, :]
    th = BAYER[(ys.astype(int) % 4), xs % 4]
    i = np.floor(u).astype(int)
    f = u - i
    i2 = np.minimum(i + (f > th), len(cols) - 1)
    C = np.array(cols, np.float32)
    return C[i2]


def stars(bg, n=90, seed=3, t=0.0):
    rng = np.random.default_rng(seed)
    out = bg.copy()
    for k in range(n):
        x, y = rng.integers(0, LW), rng.integers(0, LH)
        b = rng.uniform(0.5, 1.0) * (0.75 + 0.25 * math.sin(t * 3 + k))
        out[y, x] = np.array((255, 255, 255)) * b
        if rng.random() < 0.08:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                if 0 <= x + dx < LW and 0 <= y + dy < LH:
                    out[y + dy, x + dx] = np.array((160, 170, 220)) * b
    return out


_F = {}


def font(size):
    if size not in _F:
        _F[size] = ImageFont.truetype(FONT, size)
    return _F[size]


# ------------------------------------------------------------------ Cybertruck (Tesla), 0,15 m por vóxel
def cybertruck(r=0.15, body=None, ex=1.28):
    """Cybertruck con las proporciones un poco exageradas en altura (estilo juguete) para que se reconozca el triángulo:
    una sola línea recta del morro al vértice del techo y otra del vértice a la cola, pasos de rueda trapezoidales con
    moldura oscura, barra de luz de lado a lado delante y detrás, laterales planos."""
    L, Wd, Ht = 5.68, 2.03, 1.86 * ex
    X, Y, Z = int(round(L / r)), int(math.ceil(Ht / r)) + 1, int(round(Wd / r))
    i, j, k = np.meshgrid(np.arange(X), np.arange(Y), np.arange(Z), indexing="ij")
    x, y, z = (i + 0.5) * r, (j + 0.5) * r / ex, (k + 0.5) * r - Wd / 2      # y en metros «reales»
    AP = 2.62                                                     # vértice del techo
    top = np.where(x < AP, 0.94 + (1.86 - 0.94) * x / AP, 1.86 - (1.86 - 1.28) * (x - AP) / (L - AP))
    bot = np.interp(x, [0, 0.35, 0.8, L - 0.6, L], [0.96, 0.52, 0.40, 0.40, 0.62])
    hw = np.where(y < 1.14, Wd / 2, Wd / 2 - (y - 1.14) * 0.55)
    G = np.zeros((X, Y, Z), np.uint8)
    B = body or STEEL
    solid = (y >= bot) & (y <= top + r * 0.3) & (np.abs(z) <= hw)
    G[solid] = B
    WR = 0.47
    for wx in (1.05, 4.78):
        cut = (np.abs(x - wx) <= 0.74 - np.maximum(0, y - 0.55) * 0.7) & (y <= 1.02)
        rim = (np.abs(x - wx) <= 0.74 + r * 1.2 - np.maximum(0, y - 0.55) * 0.7) & (y <= 1.02 + r * 0.9)
        G[rim & solid & ~cut] = CLAD
        G[cut] = 0
        G[cut & (np.abs(z) < 0.5) & (y > 0.28)] = WELL
        d2 = (x - wx) ** 2 + (y - WR) ** 2
        tire = (d2 <= WR ** 2) & (np.abs(z) >= 0.5) & (np.abs(z) <= Wd / 2 - 0.03)
        G[tire] = TIRE
        G[tire & (d2 <= 0.29 ** 2) & (np.abs(z) >= Wd / 2 - 0.03 - r * 1.1)] = HUB
    above = np.roll(solid, -1, 1)
    above[:, -1, :] = False
    surf_top = solid & ~above
    side = solid & (np.abs(z) > hw - r * 1.05)
    # parabrisas enorme + techo de cristal; ventanillas laterales con pilar B de acero
    G[surf_top & (x > 1.30) & (x < 3.30) & (np.abs(z) < hw - r * 0.9)] = GLASS
    win = side & (y > 1.20) & (y < top - 0.10) & (x > 1.62) & (x < 3.95 - (y - 1.2) * 1.1)
    win &= ~((x > 2.70) & (x < 2.86))
    G[win] = GLASS
    G[surf_top & (x < 0.62)] = LAMP                            # barra de luz delantera (fina, de lado a lado)
    G[solid & (x < 0.2) & (y > top - 0.3)] = LAMP
    G[solid & (x > L - 0.2) & (y > top - 0.24)] = TAIL         # piloto trasero de lado a lado
    G[side & (np.abs(x - 2.78) < r * 0.5) & (y < 1.12) & (y > 0.5) & (G == B)] = SEAM
    rng = np.random.default_rng(4)
    N = (128 + rng.normal(0, 22, (X, 1, Z)) + rng.normal(0, 8, (X, Y, Z))).clip(0, 255).astype(np.uint8)
    G, N = G[::-1].copy(), N[::-1].copy()                          # el morro mira hacia +x (hacia donde avanza)
    return Model(G, N, pivot=((X - 1) / 2, -0.5, (Z - 1) / 2))
