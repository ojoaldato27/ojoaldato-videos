"""Objetos ilustrados con volumen para los vídeos cotidianos (estilo Titanic)."""
from illus import *

# ------------------------------------------------------------------ coche
CAR_BODY = [(40, 250), (40, 196), (62, 166), (190, 150), (258, 96), (330, 72), (560, 70), (686, 142), (820, 164), (868, 188),
            (874, 240), (850, 262), (40, 262)]
WHEELS = ((212, 262), (690, 262))


def car_side(col=(196, 30, 36), night=False):
    c = Cv(920, 360)
    c.shadow((90, 270, 840, 320), 150, 10)
    for wx, wy in WHEELS:
        c.ellipse((wx - 86, wy - 86, wx + 86, wy + 86), fill=(12, 12, 14))
    hi, lo = shade(col, 1.35), shade(col, 0.42)
    if night:
        hi, lo = shade(col, 0.7), shade(col, 0.25)
    c.poly(CAR_BODY, grad=(hi, lo), power=0.9)
    for wx, wy in WHEELS:
        c.ellipse((wx - 86, wy - 86, wx + 86, wy + 86), fill=(12, 12, 14))
    c.poly([(48, 236), (868, 236), (872, 244), (850, 262), (40, 262), (40, 240)], fill=shade(col, 0.3))
    glass = [(268, 100), (336, 80), (548, 79), (656, 142), (268, 146)]
    c.poly(glass, grad=((70, 96, 130), (14, 20, 32)) if not night else ((30, 40, 60), (6, 8, 14)))
    c.poly([(380, 80), (430, 80), (330, 146), (280, 146)], fill=(255, 255, 255, 46 if not night else 18))
    c.poly([(470, 80), (492, 80), (420, 146), (398, 146)], fill=(255, 255, 255, 30 if not night else 12))
    c.rect((448, 78, 462, 148), fill=shade(col, 0.3))
    c.line([(80, 178), (300, 156), (840, 176)], shade(col, 1.7) if not night else shade(col, 0.95), 3)
    for x in (330, 600):
        c.line([(x, 150), (x - 4, 240)], shade(col, 0.32), 2)
    for x in (380, 640):
        c.rect((x, 172, x + 40, 180), fill=shade(col, 1.6) if not night else shade(col, 0.8), r=3)
    c.poly([(816, 168), (862, 180), (858, 196), (812, 190)], fill=(255, 250, 230) if not night else (255, 248, 220))
    c.poly([(42, 172), (74, 166), (74, 190), (42, 194)], fill=(220, 30, 30))
    c.rect((520, 120, 560, 132), fill=(30, 30, 34), r=4)
    if night:
        c.glow(840, 184, 40, (255, 240, 200), 0.9)
        c.glow(56, 182, 26, (255, 40, 40), 0.9)
    return c.done()


def wheel(rot=0.0, r=86):
    c = Cv(2 * r + 4, 2 * r + 4)
    cx = cy = r + 2
    c.ellipse((cx - r * 0.84, cy - r * 0.84, cx + r * 0.84, cy + r * 0.84), radial=((46, 46, 50), (14, 14, 16)), power=1.4)
    c.ellipse((cx - r * 0.56, cy - r * 0.56, cx + r * 0.56, cy + r * 0.56), radial=((236, 238, 242), (96, 100, 108)), power=1.2,
              center=(0.4, 0.35))
    for k in range(5):
        a = rot + k * 2 * math.pi / 5
        c.line([(cx + math.cos(a) * r * 0.14, cy + math.sin(a) * r * 0.14), (cx + math.cos(a) * r * 0.52, cy + math.sin(a) * r * 0.52)],
               (60, 62, 68), 7)
    c.ellipse((cx - r * 0.13, cy - r * 0.13, cx + r * 0.13, cy + r * 0.13), fill=(70, 72, 78))
    return c.done()


def paste_car(img, x, y, s=1.0, col=(196, 30, 36), night=False, rot=0.0, flip=False):
    """x, y = centro inferior del coche (suelo)."""
    sp = spr(car_side, col, night)
    w_, h_ = sp.size
    cx = x
    cy = y - (262 - h_ / 2) * s
    paste(img, sp, cx, cy, s, 1.0, 0, flip)
    rq = round(rot % (2 * math.pi / 5), 2)
    wh = spr(wheel, rq)
    for wx, wy in WHEELS:
        dx = (wx - w_ / 2) * s * (-1 if flip else 1)
        paste(img, wh, cx + dx, y, s)


def car_rear(col=(170, 26, 30), brake=0.0):
    c = Cv(620, 420)
    c.shadow((40, 360, 580, 420), 160, 12)
    c.rect((60, 330, 150, 410), fill=(10, 10, 12), r=16)
    c.rect((470, 330, 560, 410), fill=(10, 10, 12), r=16)
    c.poly([(50, 360), (40, 250), (110, 200), (170, 110), (450, 110), (510, 200), (580, 250), (570, 360)], grad=(shade(col, 0.55), shade(col, 0.18)))
    c.poly([(186, 126), (434, 126), (480, 196), (140, 196)], grad=((40, 50, 70), (8, 10, 16)))
    c.poly([(220, 126), (260, 126), (200, 196), (160, 196)], fill=(255, 255, 255, 18))
    k = 0.55 + 0.45 * brake
    red = (int(255 * k), int(30 * k), int(30 * k))
    c.rect((60, 222, 220, 252), fill=red, r=10)
    c.rect((400, 222, 560, 252), fill=red, r=10)
    c.rect((250, 230, 370, 246), fill=shade(red, 0.7), r=6)
    c.glow(140, 237, 90 + 60 * brake, (255, 40, 40), 0.6 + 0.4 * brake)
    c.glow(480, 237, 90 + 60 * brake, (255, 40, 40), 0.6 + 0.4 * brake)
    c.rect((250, 286, 370, 318), fill=(220, 220, 214), r=4)
    c.text((310, 302), "1234 NLS", 18, (30, 30, 40))
    return c.done()


def _deer_sil():
    c = Cv(400, 450)
    k = (255, 255, 255)
    c.ellipse((112, 178, 352, 292), fill=k)
    c.ellipse((92, 168, 196, 290), fill=k)
    c.ellipse((272, 166, 364, 288), fill=k)
    c.poly([(112, 214), (70, 112), (104, 96), (168, 206)], fill=k)
    c.ellipse((40, 72, 112, 122), fill=k)
    c.poly([(48, 88), (8, 108), (14, 122), (62, 120)], fill=k)
    c.poly([(92, 80), (128, 56), (112, 90)], fill=k)
    c.poly([(74, 78), (52, 52), (84, 72)], fill=k)
    for x0, x1, x2 in ((122, 116, 120), (154, 160, 150), (300, 312, 300), (334, 346, 340)):
        c.line([(x0, 262), (x1, 350), (x2, 436)], k, 11)
        c.ellipse((x2 - 8, 428, x2 + 8, 444), fill=k)
    c.poly([(352, 186), (382, 196), (360, 222)], fill=k)
    for bx, sgn in ((84, -1), (100, 1)):
        c.line([(bx, 76), (bx + sgn * 10, 40), (bx + sgn * 26, 8)], k, 5)
        c.line([(bx + sgn * 8, 48), (bx + sgn * 34, 38)], k, 4)
        c.line([(bx + sgn * 16, 26), (bx + sgn * 40, 22)], k, 3)
    return c.done()


def deer(lit=0.8):
    """Ciervo iluminado de lado por los faros (luz desde la izquierda), mirando a la izquierda."""
    sil = spr(_deer_sil)
    w_, h_ = sil.size
    hi = (int(lerp(40, 196, lit)), int(lerp(30, 150, lit)), int(lerp(24, 104, lit)))
    lo = (20, 15, 12)
    u = np.linspace(0, 1, w_) ** 0.8
    row = np.array(hi, float)[None, :] + (np.array(lo, float) - np.array(hi, float))[None, :] * u[:, None]
    arr = np.broadcast_to(row[None, :, :], (h_, w_, 3)).copy()
    yy = np.linspace(0, 1, h_)[:, None, None]
    arr = arr * (1.0 - 0.35 * np.clip((yy - 0.62) / 0.38, 0, 1))
    out = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
    out.putalpha(sil.getchannel("A"))
    c = Cv(w_, h_)
    c.im = out.resize((w_ * 3, h_ * 3), Image.BILINEAR)
    c.d = ImageDraw.Draw(c.im)
    c.ellipse((40, 112, 70, 124), fill=(232, 226, 214, 200))
    c.ellipse((10, 104, 22, 116), fill=(16, 12, 10))
    c.glow(62, 92, 16, (255, 250, 220), lit)
    c.ellipse((58, 88, 66, 96), fill=(255, 255, 240))
    return c.done()


def pine_row(img, y, col, n=24, hmin=120, hmax=260, seed=7, xs=None):
    rr = random.Random(seed)
    d = ImageDraw.Draw(img, "RGBA")
    for i in range(n):
        x = xs[i] if xs else rr.uniform(-40, W + 40)
        h = rr.uniform(hmin, hmax)
        w = h * rr.uniform(0.34, 0.44)
        tiers = 4
        for k in range(tiers):
            ty = y - h + k * h / (tiers + 0.6)
            bw = w * (0.35 + 0.65 * (k + 1) / tiers) / 2
            d.polygon([(x, ty), (x + bw, ty + h / tiers * 1.25), (x - bw, ty + h / tiers * 1.25)], fill=col)
        d.rectangle([x - 4, y - 14, x + 4, y], fill=col)


def streetlight(h=700):
    c = Cv(260, h)
    c.rect((116, 40, 132, h), grad=((90, 94, 104), (30, 32, 38)), horizontal=True)
    c.line([(124, 50), (220, 20)], (70, 74, 84), 8)
    c.rect((190, 10, 250, 34), fill=(60, 62, 70), r=8)
    c.rect((196, 30, 244, 40), fill=(255, 196, 110), r=4)
    return c.done()


# ------------------------------------------------------------------ escenarios de carretera
def highway_night(img, t, speed=1.0, hz=900, lights=True, lane_off=0.0):
    sky(img, (6, 10, 26), (60, 46, 70), 1.6, 0, hz)
    stars(img, t, hz - 200, 0.6, 120, 9)
    paste(img, glow(520, (255, 150, 90), 0.35), 540, hz)
    mountains(img, hz, 70, (18, 18, 30), 12, 0.4, peaks=3)
    city_lights(img, t, hz - 12, 6, 200)
    vx = 540
    ground(img, hz, (16, 16, 22), (6, 6, 8))
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.polygon([(vx - 8, hz), (vx + 8, hz), (W + 700, H), (-700, H)], fill=(34, 34, 40, 255))
    for sgn in (-1, 1):
        d.line([(vx + sgn * 8, hz), (vx + sgn * 1000, H)], fill=(220, 220, 210, 230), width=8)
    for k in range(14):
        u = ((k / 14) + t * 0.45 * speed + lane_off) % 1.0
        z0, z1 = u ** 2.4, min(1.0, (u + 0.03) ** 2.4)
        y0, y1 = hz + (H - hz) * z0, hz + (H - hz) * z1
        w0, w1 = 2 + 18 * z0, 2 + 18 * z1
        d.polygon([(vx - w0, y0), (vx + w0, y0), (vx + w1, y1), (vx - w1, y1)], fill=(240, 230, 200, 255))
    AC(img, im)
    if lights:
        for k in range(6):
            u = ((k / 6) + t * 0.25 * speed) % 1.0
            z = u ** 2.2
            for sgn in (-1, 1):
                x = vx + sgn * (40 + 1500 * z)
                y = hz + (H - hz) * z
                s_ = 0.08 + 1.6 * z
                if s_ > 0.05 and -400 < x < W + 400:
                    paste(img, spr(streetlight), x - sgn * 0, y - 330 * s_, s_, 1.0, 0, sgn < 0)
                    paste(img, glow(int(60 + 260 * z), (255, 180, 100), 0.8), x + sgn * 60 * s_, y - 650 * s_, 1.0, 0.9)


def highway_day(img, t, hz=1180, speed=1.0, sunset=False):
    if sunset:
        sky(img, (40, 50, 110), (255, 160, 100), 1.4, 0, hz)
        paste(img, glow(420, (255, 190, 120), 0.8), 820, hz - 80)
    else:
        sky(img, (86, 140, 210), (220, 230, 240), 1.3, 0, hz)
    clouds(img, t * speed, hz - 420, (255, 255, 255) if not sunset else (255, 200, 180), 120, 6 * speed, 8, 1.1)
    mountains(img, hz - 10, 160, (110, 130, 150) if not sunset else (80, 60, 90), 3, 0.5)
    mountains(img, hz, 80, (80, 110, 90) if not sunset else (50, 40, 60), 5, 0.6)
    ground(img, hz, (100, 120, 80) if not sunset else (60, 50, 50), (60, 80, 50) if not sunset else (30, 26, 30))
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, hz + 140, W, hz + 330], fill=(50, 50, 56))
    d.rectangle([0, hz + 140, W, hz + 148], fill=(230, 230, 220))
    d.rectangle([0, hz + 322, W, hz + 330], fill=(230, 230, 220))
    off = (t * 900 * speed) % 240
    for x in range(-240, W + 240, 240):
        d.rectangle([x - off, hz + 232, x - off + 120, hz + 240], fill=(240, 236, 220))
    off2 = (t * 700 * speed) % 160
    d.rectangle([0, hz + 96, W, hz + 106], fill=(180, 184, 190))
    for x in range(-160, W + 160, 160):
        d.rectangle([x - off2, hz + 96, x - off2 + 8, hz + 140], fill=(150, 154, 160))
