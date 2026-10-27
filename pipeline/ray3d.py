"""Render 3D sencillo por «raymarching» de campos de distancia (numpy), para la muestra tipo Zack D. Films (21/10).
Coche tipo Tesla Roadster: casco bajo y redondeado, cabina en burbuja, ruedas grandes con llanta, pintura con brillo y
reflejos, suelo que refleja, sombras suaves y luz de estudio. Se usa para pre-renderizar sprites (no fotograma a fotograma)."""
import numpy as np
from PIL import Image


def _len(v):
    return np.sqrt(np.sum(v * v, axis=-1))


def sd_roundbox(p, b, r):
    q = np.abs(p) - b
    return _len(np.maximum(q, 0)) + np.minimum(np.max(q, axis=-1), 0) - r


def sd_ellipsoid(p, r):
    k0 = _len(p / r)
    k1 = _len(p / (r * r))
    return k0 * (k0 - 1.0) / np.maximum(k1, 1e-6)


def sd_cyl_z(p, r, h):
    d = np.stack([np.sqrt(p[..., 0] ** 2 + p[..., 1] ** 2) - r, np.abs(p[..., 2]) - h], -1)
    return np.minimum(np.max(d, -1), 0) + _len(np.maximum(d, 0))


def smin(a, b, k):
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0, 1)
    return b * (1 - h) + a * h - k * h * (1 - h)


WX, WY, WZ, WR = 1.32, 0.36, 0.84, 0.36


def car(p):
    """Devuelve (distancia, material). Materiales: 1 pintura, 2 cristal, 3 neumático, 4 llanta, 0 suelo."""
    x, y, z = p[..., 0], p[..., 1], p[..., 2]
    hull = sd_roundbox(p - np.array([-0.05, 0.46, 0.0]), np.array([1.90, 0.15, 0.84]), 0.20)
    nose = sd_ellipsoid(p - np.array([1.55, 0.40, 0.0]), np.array([0.85, 0.22, 0.86]))
    hull = smin(hull, nose, 0.22)
    hull = np.maximum(hull, (y + 0.16 * np.maximum(x - 0.4, 0)) - 0.86)        # capó que baja hacia el morro
    cab = sd_ellipsoid(p - np.array([-0.40, 0.80, 0.0]), np.array([1.20, 0.33, 0.70]))
    body = smin(hull, cab, 0.30)
    for sx in (-1, 1):                                                  # aletas sobre las ruedas (como el Roadster real)
        for sz in (-1, 1):
            fe = sd_ellipsoid(p - np.array([sx * WX, 0.50, sz * 0.72]), np.array([0.70, 0.38, 0.32]))
            body = smin(body, fe, 0.18)
    body = np.maximum(body, 0.20 - y)                                   # fondo plano
    body = np.maximum(body, (y - 0.12 * np.maximum(-x - 0.6, 0) * 0) - 1.12)
    # pasos de rueda
    for sx in (-1, 1):
        for sz in (-1, 1):
            q = p - np.array([sx * WX, WY, sz * WZ])
            body = np.maximum(body, -sd_cyl_z(q, WR + 0.05, 0.42))
    d = body
    mat = np.ones(d.shape, np.int8)
    glass = (y > 0.74) & (cab < 0.02) & (x > -1.35) & (x < 0.72)
    mat[glass] = 2
    lamp = (x > 1.75) & (y > 0.42) & (y < 0.56) & (np.abs(z) > 0.35) & (np.abs(z) < 0.80) & (body < 0.02)
    mat[lamp] = 6
    tail = (x < -1.95) & (y > 0.55) & (y < 0.66) & (body < 0.02)
    mat[tail] = 7
    for sx in (-1, 1):
        for sz in (-1, 1):
            q = p - np.array([sx * WX, WY, sz * WZ])
            tire = sd_cyl_z(q, WR, 0.13) - 0.03
            rim = sd_cyl_z(q - np.array([0, 0, sz * 0.03]), WR * 0.62, 0.135)
            wheel = np.minimum(tire, rim)
            sel = wheel < d
            ang = np.arctan2(q[..., 1], q[..., 0])
            rr = np.sqrt(q[..., 0] ** 2 + q[..., 1] ** 2)
            spoke = (np.cos(10 * ang + rr * 6) > 0.1) | (rr < WR * 0.18) | (rr > WR * 0.55)
            rim_m = np.where(spoke, 4, 5).astype(np.int8)
            mat[sel] = np.where(rim[sel] < tire[sel] + 0.01, rim_m[sel], 3)
            d = np.minimum(d, wheel)
    return d, mat


def scene(p):
    d, m = car(p)
    g = p[..., 1]
    sel = g < d
    m = m.copy()
    m[sel] = 0
    return np.minimum(d, g), m


def _normal(p):
    e = 0.002
    ex, ey, ez = np.array([e, 0, 0]), np.array([0, e, 0]), np.array([0, 0, e])
    n = np.stack([scene(p + ex)[0] - scene(p - ex)[0], scene(p + ey)[0] - scene(p - ey)[0], scene(p + ez)[0] - scene(p - ez)[0]], -1)
    return n / np.maximum(_len(n)[..., None], 1e-9)


def _march(ro, rd, steps=110, tmax=30.0):
    t = np.zeros(ro.shape[:-1])
    hit = np.zeros(t.shape, bool)
    alive = np.ones(t.shape, bool)
    for _ in range(steps):
        idx = np.nonzero(alive)
        if idx[0].size == 0:
            break
        pp = ro[idx] + rd[idx] * t[idx][..., None]
        d, _ = scene(pp)
        t[idx] += d * 0.9
        h = d < 0.0015
        hit[tuple(a[h] for a in idx)] = True
        dead = h | (t[idx] > tmax)
        alive[tuple(a[dead] for a in idx)] = False
    return t, hit


def _shadow(p, l, k=10.0):
    res = np.ones(p.shape[:-1])
    t = np.full(res.shape, 0.03)
    for _ in range(40):
        d, _ = scene(p + l * t[..., None])
        res = np.minimum(res, np.clip(k * d / t, 0, 1))
        t += np.clip(d, 0.02, 0.4)
    return np.clip(res, 0, 1)


def _sky(rd, top=(0.35, 0.62, 0.98), hor=(0.92, 0.95, 1.0)):
    u = np.clip(rd[..., 1], 0, 1)[..., None] ** 0.6
    return np.array(hor) * (1 - u) + np.array(top) * u


PAINT = np.array([0.72, 0.03, 0.06])


def shade(ro, rd, t, hit, sky_top=(0.35, 0.62, 0.98), ground=(0.42, 0.44, 0.48), depth=0):
    col = _sky(rd, sky_top)
    if not hit.any():
        return col
    p = ro + rd * t[..., None]
    idx = np.nonzero(hit)
    ph = p[idx]
    _, mat = scene(ph)
    n = _normal(ph)
    L = np.array([0.45, 0.8, 0.35]); L = L / np.linalg.norm(L)
    sh = _shadow(ph + n * 0.004, L)
    dif = np.clip(np.sum(n * L, -1), 0, 1) * sh
    v = -rd[idx]
    hvec = (L + v); hvec /= np.maximum(_len(hvec)[..., None], 1e-9)
    spec = np.clip(np.sum(n * hvec, -1), 0, 1)
    amb = 0.35 + 0.25 * n[..., 1]
    fres = 0.04 + 0.96 * (1 - np.clip(np.sum(n * v, -1), 0, 1)) ** 5
    refl_dir = rd[idx] - 2 * np.sum(rd[idx] * n, -1)[..., None] * n
    env = _sky(refl_dir, sky_top)
    out = np.zeros(ph.shape)
    for m_id, base, sp_pow, sp_k, refl in ((1, PAINT, 120, 1.4, 0.55), (2, np.array([0.02, 0.025, 0.04]), 200, 1.6, 0.9),
                                            (3, np.array([0.03, 0.03, 0.035]), 12, 0.15, 0.05), (4, np.array([0.55, 0.57, 0.6]), 60, 1.0, 0.6), (5, np.array([0.06, 0.06, 0.07]), 20, 0.3, 0.2), (6, np.array([3.0, 3.0, 2.8]), 10, 0.0, 0.0), (7, np.array([2.2, 0.1, 0.15]), 10, 0.0, 0.0),
                                            (0, np.array(ground), 30, 0.2, 0.25)):
        s = mat == m_id
        if not s.any():
            continue
        c = base * (dif[s][..., None] * 0.95 + amb[s][..., None] * 0.35)
        c += sp_k * (spec[s] ** sp_pow)[..., None] * sh[s][..., None]
        r = refl * (fres[s] if m_id != 0 else 0.35 + 0.0 * fres[s])
        c = c * (1 - r[..., None] * 0.6) + env[s] * r[..., None]
        out[s] = c
    # reflejo del coche en el suelo (un rebote)
    g = mat == 0
    if g.any() and depth == 0:
        gp = ph[g] + n[g] * 0.01
        rdir = refl_dir[g]
        t2, h2 = _march(gp, rdir, 70, 12.0)
        if h2.any():
            c2 = shade(gp, rdir, t2, h2, sky_top, ground, 1)
            cc = out[g]
            cc[h2] = cc[h2] * 0.62 + c2[h2] * 0.38
            out[g] = cc
        # oclusión de contacto bajo el coche
        dcar, _ = car(gp + np.array([0, 0.0, 0]))
        ao = np.clip(dcar / 0.6, 0, 1) ** 0.6
        out[g] *= (0.45 + 0.55 * ao)[..., None]
    col[idx] = out
    return col


def render(w=540, h=960, cam=(9.6, 1.75, 4.3), look=(0.55, 0.5, 0.0), fov=30, sky_top=(0.35, 0.62, 0.98), ground=(0.42, 0.44, 0.48)):
    ro = np.array(cam, float)
    fw = np.array(look, float) - ro; fw /= np.linalg.norm(fw)
    rt = np.cross(fw, [0, 1, 0]); rt /= np.linalg.norm(rt)
    up = np.cross(rt, fw)
    ys, xs = np.mgrid[0:h, 0:w].astype(float)
    k = np.tan(np.radians(fov) / 2)
    u = (xs / w * 2 - 1) * k * (w / h)
    v = -(ys / h * 2 - 1) * k
    rd = fw[None, None] + u[..., None] * rt[None, None] + v[..., None] * up[None, None]
    rd /= _len(rd)[..., None]
    ro_ = np.broadcast_to(ro, rd.shape).copy()
    t, hit = _march(ro_, rd)
    col = shade(ro_, rd, t, hit, sky_top, ground)
    col = 1 - np.exp(-col * 1.6)                                          # tono «filmic»
    col = col ** (1 / 1.1)
    return Image.fromarray(np.clip(col * 255, 0, 255).astype(np.uint8))
