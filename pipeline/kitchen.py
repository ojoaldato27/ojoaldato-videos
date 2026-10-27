"""Cocina, microondas y piezas internas ilustradas (estilo Titanic con volumen)."""
from objs import *
from PIL import ImageChops

MW_W, MW_H = 820, 500
WIN = (66, 70, 552, 420)  # ventana de la puerta (coordenadas del sprite)


# ------------------------------------------------------------------ microondas
def mw_body():
    c = Cv(MW_W, MW_H)
    c.rect((60, 470, 130, 492), fill=(20, 20, 22), r=4)
    c.rect((690, 470, 760, 492), fill=(20, 20, 22), r=4)
    c.rect((8, 8, 812, 478), grad=((214, 218, 226), (110, 114, 124)), r=26)
    c.rect((16, 12, 804, 26), fill=(255, 255, 255, 80), r=8)
    c.rect((26, 30, 598, 458), grad=((56, 60, 66), (20, 22, 26)), r=16)
    c.rect((40, 44, 584, 444), fill=(12, 13, 16), r=12)
    c.rect((562, 118, 584, 370), grad=((236, 238, 242), (112, 116, 124)), horizontal=True, r=9)
    c.rect((610, 30, 796, 458), grad=((64, 68, 76), (28, 30, 36)), r=14)
    c.rect((630, 54, 776, 124), fill=(6, 12, 10), r=8)
    c.rect((632, 56, 774, 70), fill=(255, 255, 255, 18), r=6)
    for i in range(4):
        for j in range(3):
            x, y = 640 + j * 46, 148 + i * 42
            col = ((96, 100, 110), (50, 54, 60)) if (i, j) != (3, 2) else ((90, 200, 120), (30, 110, 60))
            c.rect((x, y, x + 38, y + 32), grad=col, r=6)
            c.rect((x + 3, y + 2, x + 35, y + 8), fill=(255, 255, 255, 30), r=3)
    c.ellipse((654, 330, 754, 430), radial=((210, 214, 222), (66, 70, 78)), center=(0.38, 0.32))
    c.ellipse((664, 340, 744, 420), radial=((180, 184, 192), (92, 96, 104)), center=(0.4, 0.35))
    c.rect((700, 344, 708, 372), fill=(40, 42, 48), r=3)
    for x in range(660, 790, 12):
        c.rect((x, 440, x + 6, 448), fill=(18, 20, 24), r=2)
    im = c.done()
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle(WIN, radius=10, fill=255)
    im.putalpha(ImageChops.subtract(im.getchannel("A"), m))
    return im


def mw_glass():
    w, h = WIN[2] - WIN[0], WIN[3] - WIN[1]
    yy, xx = np.mgrid[0:h, 0:w].astype(float)
    sp = 9.0
    row = np.round(yy / (sp * 0.866))
    gx = xx - (row % 2) * sp / 2
    dx = gx - np.round(gx / sp) * sp
    dy = yy - row * sp * 0.866
    dist = np.sqrt(dx ** 2 + dy ** 2)
    a = np.where(dist < 3.2, 0, 92).astype(float)
    arr = np.zeros((h, w, 4), np.uint8)
    arr[..., :3] = (8, 8, 10)
    arr[..., 3] = a.astype(np.uint8)
    im = Image.fromarray(arr, "RGBA")
    c = Cv(w, h)
    c.im = im.resize((w * 3, h * 3), Image.NEAREST)
    c.d = ImageDraw.Draw(c.im)
    c.poly([(w * 0.12, 0), (w * 0.34, 0), (w * 0.12, h), (-w * 0.1, h)], fill=(255, 255, 255, 26))
    c.poly([(w * 0.42, 0), (w * 0.48, 0), (w * 0.26, h), (w * 0.2, h)], fill=(255, 255, 255, 16))
    return c.done()


def bowl(phase=0, soup=(214, 120, 52), w=280):
    """Cuenco de cerámica con sopa, visto de frente y un poco desde arriba."""
    h = int(w * 0.62)
    c = Cv(w, h)
    c.shadow((w * 0.08, h * 0.82, w * 0.92, h * 1.0), 140, 8)
    c.poly([(w * 0.03, h * 0.28), (w * 0.97, h * 0.28), (w * 0.86, h * 0.72), (w * 0.66, h * 0.9), (w * 0.34, h * 0.9), (w * 0.14, h * 0.72)],
           grad=((250, 248, 242), (176, 170, 160)), power=1.2)
    c.poly([(w * 0.6, h * 0.3), (w * 0.95, h * 0.3), (w * 0.84, h * 0.72), (w * 0.66, h * 0.88)], fill=(0, 0, 0, 40))
    # franja decorativa que se desplaza (da sensación de giro)
    for k in range(9):
        x = ((k / 9 + phase / 12) % 1.0)
        px = lerp(w * 0.1, w * 0.9, x)
        sz = w * 0.022 * (0.5 + math.sin(x * math.pi))
        c.ellipse((px - sz, h * 0.5 - sz, px + sz, h * 0.5 + sz), fill=(40, 90, 170, int(220 * math.sin(x * math.pi))))
    c.ellipse((w * 0.03, h * 0.12, w * 0.97, h * 0.44), fill=(238, 234, 226))
    c.ellipse((w * 0.08, h * 0.16, w * 0.92, h * 0.41), radial=(shade(soup, 1.25), shade(soup, 0.7)), center=(0.45, 0.4))
    rr = random.Random(3)
    for i in range(10):
        x, y = rr.uniform(0.18, 0.82), rr.uniform(0.21, 0.36)
        col = rr.choice([(240, 160, 60), (90, 160, 70), (250, 230, 200)])
        c.ellipse((w * x - 7, h * y - 4, w * x + 7, h * y + 4), fill=col)
    c.ellipse((w * 0.25, h * 0.2, w * 0.45, h * 0.26), fill=(255, 255, 255, 50))
    return c.done()


def mw_interior(on=True, phase=0):
    """Lo que se ve tras el cristal: cavidad en perspectiva, plato y cuenco."""
    w, h = WIN[2] - WIN[0], WIN[3] - WIN[1]
    c = Cv(w, h)
    if on:
        wall, wall2, flo = ((250, 214, 140), (196, 140, 64)), ((214, 166, 90), (140, 92, 36)), ((200, 150, 80), (110, 70, 30))
    else:
        wall, wall2, flo = ((52, 52, 56), (30, 30, 34)), ((40, 40, 44), (22, 22, 26)), ((36, 36, 40), (16, 16, 18))
    bx0, by0, bx1, by1 = 60, 40, 426, 270
    c.rect((0, 0, w, h), grad=wall2)
    c.poly([(0, 0), (w, 0), (bx1, by0), (bx0, by0)], grad=(shade(wall2[0], 0.9), wall2[0]))
    c.poly([(0, h), (w, h), (bx1, by1), (bx0, by1)], grad=flo[::-1])
    c.poly([(0, 0), (bx0, by0), (bx0, by1), (0, h)], grad=wall2, horizontal=True)
    c.poly([(w, 0), (bx1, by0), (bx1, by1), (w, h)], grad=wall2[::-1], horizontal=True)
    c.rect((bx0, by0, bx1, by1), grad=wall)
    if on:
        c.glow(bx1 - 40, by0 + 30, 140, (255, 240, 200), 0.9)
    c.rect((bx1 + 6, 70, bx1 + 40, 120), fill=shade(wall2[1], 0.8))
    cx, cy = w / 2, h - 40
    c.ellipse((cx - 190, cy - 34, cx + 190, cy + 30), fill=(255, 255, 255, 50 if on else 20))
    c.arc((cx - 190, cy - 34, cx + 190, cy + 30), 0, 180, (255, 255, 255, 120 if on else 40), 3)
    b = spr(bowl, phase)
    c.im.alpha_composite(b.resize((b.size[0] * 3, b.size[1] * 3), Image.BILINEAR), (int((cx - b.size[0] / 2) * 3), int((cy - b.size[1] + 22) * 3)))
    if not on:
        c.rect((0, 0, w, h), fill=(0, 0, 0, 70))
    return c.done()


def mw_guts():
    """Componentes internos (para la vista de rayos X), en coordenadas del sprite del microondas."""
    c = Cv(MW_W, MW_H)
    c.rect((610, 30, 796, 458), fill=(14, 16, 22), r=14)
    for x in range(620, 796, 22):
        c.line([(x, 34), (x, 454)], (40, 70, 90, 60), 1)
    for y in range(40, 458, 22):
        c.line([(614, y), (792, y)], (40, 70, 90, 60), 1)
    c.rect((470, 36, 706, 86), grad=((190, 196, 206), (86, 90, 100)), r=6)
    c.rect((474, 40, 702, 48), fill=(255, 255, 255, 60), r=3)
    c.rect((470, 80, 520, 96), fill=(60, 50, 40))
    for y in range(108, 234, 9):
        c.rect((632, y, 768, y + 5), grad=((236, 238, 244), (120, 124, 134)), horizontal=True, r=2)
    c.rect((668, 96, 732, 246), grad=((240, 168, 104), (132, 72, 34)), horizontal=True, r=6)
    c.rect((650, 90, 750, 106), grad=((96, 98, 106), (46, 48, 54)), r=4)
    c.rect((650, 236, 750, 252), grad=((96, 98, 106), (46, 48, 54)), r=4)
    c.ellipse((686, 70, 714, 98), radial=((250, 250, 255), (140, 144, 152)), center=(0.4, 0.3))
    c.line([(700, 252), (700, 280), (730, 280), (730, 296)], (200, 60, 50), 5)
    c.line([(690, 252), (690, 286), (644, 286), (644, 300)], (60, 60, 64), 5)
    c.rect((624, 300, 664, 392), grad=((110, 116, 132), (44, 48, 58)), horizontal=True, r=16)
    c.rect((636, 290, 652, 302), fill=(180, 180, 186), r=3)
    c.rect((678, 296, 786, 446), grad=((92, 94, 100), (40, 42, 46)), r=6)
    c.rect((694, 310, 770, 432), grad=((236, 150, 80), (150, 74, 30)), horizontal=True, r=8)
    for y in range(314, 430, 7):
        c.line([(696, y), (768, y)], (120, 56, 20, 140), 2)
    return c.done()


def mw_display(img, x, y, s, txt, k=1.0):
    d = ImageDraw.Draw(img, "RGBA")
    d.text((x, y), txt, font=f(F_MONO, int(46 * s)), fill=(110, 255, 190, int(255 * k)), anchor="mm")
    paste(img, glow(int(70 * s), (80, 255, 170), 0.35), x, y, 1.0, k)


def mw_pos(ox, oy, s, x, y):
    """Coordenadas del sprite → pantalla, con el microondas centrado en (ox, oy) y escala s."""
    return ox + (x - MW_W / 2) * s, oy + (y - MW_H / 2) * s


def microwave(img, ox, oy, s=1.0, t=0.0, on=True, rot_speed=1.0, guts=0.0, display="0:30", steam=True):
    if on:
        paste(img, glow(int(420 * s), (255, 190, 100), 0.45), *mw_pos(ox, oy, s, 309, 300))
    ph = int(t * 3 * rot_speed) % 12
    wx, wy = mw_pos(ox, oy, s, (WIN[0] + WIN[2]) / 2, (WIN[1] + WIN[3]) / 2)
    paste(img, spr(mw_interior, on, ph), wx, wy, s)
    if on and steam:
        bx, by = mw_pos(ox, oy, s, 309, 250)
        smoke(img, t, [(bx, by, 0.5 * s)], col=(255, 240, 220), alpha=40, spread=(60 * s, 20 * s), grow=40 * s, speed=0.6)
    paste(img, spr(mw_glass), wx, wy, s)
    paste(img, spr(mw_body), ox, oy, s)
    if guts > 0:
        paste(img, spr(mw_guts), ox, oy, s, guts)
    dx, dy = mw_pos(ox, oy, s, 703, 89)
    if guts < 0.4 and display:
        mw_display(img, dx, dy, s, display, (1.0 if on else 0.6) * (1 - guts / 0.4))


# ------------------------------------------------------------------ cocina
COUNTER_Y = 1010


def _kitchen(night=True):
    c = Cv(W, H, 2)
    wall = ((70, 56, 46), (40, 32, 28)) if night else ((236, 226, 210), (190, 176, 158))
    c.rect((0, 0, W, H), grad=wall)
    # azulejos tipo metro
    ty0, ty1 = 430, 968
    tw, th = 120, 60
    for r_ in range((ty1 - ty0) // th + 1):
        y = ty0 + r_ * th
        off = (tw / 2) if r_ % 2 else 0
        for k in range(-1, W // tw + 2):
            x = k * tw + off
            base = (176, 164, 148) if night else (246, 242, 234)
            g = 0.62 + 0.38 * (1 - (y - ty0) / (ty1 - ty0)) ** 0.6
            col1 = shade(base, g)
            c.rect((x + 3, y + 3, x + tw - 3, y + th - 3), grad=(shade(col1, 1.08), shade(col1, 0.86)), r=6)
            c.rect((x + 8, y + 6, x + tw - 20, y + 12), fill=(255, 255, 255, 28), r=3)
    # armarios superiores
    c.rect((0, 0, W, 420), grad=((84, 58, 40), (52, 34, 24)))
    for x0 in (20, 290, 560, 830):
        c.rect((x0, 20, x0 + 250, 396), grad=((112, 78, 54), (66, 44, 30)), r=8)
        c.rect((x0 + 24, 44, x0 + 226, 372), grad=((92, 64, 44), (74, 50, 34)), r=6)
        c.rect((x0 + 28, 48, x0 + 222, 56), fill=(255, 255, 255, 18), r=3)
        hx = x0 + 214 if x0 in (20, 560) else x0 + 36
        c.rect((hx - 5, 300, hx + 5, 372), grad=((220, 220, 226), (110, 112, 120)), horizontal=True, r=4)
    c.rect((0, 404, W, 430), grad=((60, 40, 28), (40, 26, 18)))
    c.rect((40, 424, W - 40, 432), fill=(255, 230, 180))
    # encimera
    c.poly([(0, 948), (W, 948), (W, COUNTER_Y), (0, COUNTER_Y)], grad=((130, 124, 120), (96, 92, 90)) if night else ((220, 216, 210), (180, 176, 170)))
    c.rect((0, COUNTER_Y, W, COUNTER_Y + 52), grad=((80, 76, 74), (40, 38, 38)))
    c.rect((0, COUNTER_Y, W, COUNTER_Y + 4), fill=(255, 255, 255, 60))
    rr = random.Random(2)
    for i in range(220):
        x, y = rr.uniform(0, W), rr.uniform(952, COUNTER_Y - 4)
        c.ellipse((x - 2, y - 1, x + 2, y + 1), fill=(255, 255, 255, rr.randint(10, 40)))
    # armarios inferiores
    c.rect((0, COUNTER_Y + 52, W, H), grad=((70, 48, 34), (24, 16, 12)))
    for x0 in (20, 560):
        c.rect((x0, COUNTER_Y + 80, x0 + 500, H - 40), grad=((92, 64, 44), (34, 22, 16)), r=8)
        c.rect((x0 + 150, COUNTER_Y + 110, x0 + 350, COUNTER_Y + 122), grad=((220, 220, 226), (110, 112, 120)), r=5)
    # bote de utensilios (izquierda) y planta (derecha)
    c.line([(84, 900), (60, 760)], (150, 104, 60), 10)
    c.ellipse((40, 740, 80, 790), fill=(160, 112, 66))
    c.line([(104, 900), (120, 740)], (120, 84, 50), 8)
    c.line([(124, 900), (150, 770)], (90, 90, 96), 6)
    c.rect((50, 860, 160, 1000), grad=((60, 120, 140), (24, 60, 76)), horizontal=True, r=12)
    c.rect((60, 868, 76, 990), fill=(255, 255, 255, 40), r=6)
    for k in range(9):
        a = -2.4 + k * 0.32
        x1, y1 = 1000 + math.cos(a) * 130, 880 + math.sin(a) * 110
        c.poly([(1000, 880), (x1 - 18, y1), (x1 + 18, y1 + 6)], grad=((90, 160, 80), (40, 90, 40)))
    c.rect((950, 880, 1060, 1000), grad=((200, 110, 70), (120, 60, 36)), horizontal=True, r=10)
    im = c.done().convert("RGBA")
    if night:
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        light_cone(ov, 540, 430, 540, 960, 520, 620, (255, 220, 160), 70, 40)
        im.alpha_composite(ov)
    return im


def kitchen(img, night=True):
    AC(img, cached(("kitchen", night), lambda: _kitchen(night)))


# ------------------------------------------------------------------ moléculas
def water_mol(size=1.0):
    c = Cv(300, 270)
    for sx in (-1, 1):
        hx, hy = 150 + sx * 92, 120 + 74
        c.ellipse((hx - 48, hy - 48, hx + 48, hy + 48), radial=((255, 255, 255), (140, 148, 164)), power=1.1, center=(0.4, 0.32))
    c.ellipse((70, 34, 230, 194), radial=((255, 150, 140), (150, 18, 22)), power=1.05, center=(0.38, 0.3))
    c.ellipse((104, 58, 140, 84), fill=(255, 255, 255, 120))
    return c.done()


def magnifier(r=230):
    c = Cv(int(r * 2 + 60), int(r * 2 + 260))
    cx = cy = r + 30
    c.line([(cx + r * 0.62, cy + r * 0.62), (cx + r * 0.62 + 150, cy + r * 0.62 + 170)], (60, 40, 30), 46)
    c.line([(cx + r * 0.62 + 8, cy + r * 0.62), (cx + r * 0.62 + 150, cy + r * 0.62 + 160)], (120, 84, 60), 14)
    c.ellipse((cx - r - 22, cy - r - 22, cx + r + 22, cy + r + 22), radial=((60, 62, 70), (20, 20, 24)), power=0.5)
    c.ellipse((cx - r - 16, cy - r - 16, cx + r + 16, cy + r + 16), grad=((240, 240, 246), (110, 114, 124)))
    m = Image.new("L", c.im.size, 0)
    ImageDraw.Draw(m).ellipse([(cx - r) * 3, (cy - r) * 3, (cx + r) * 3, (cy + r) * 3], fill=255)
    c.im.putalpha(ImageChops.subtract(c.im.getchannel("A"), m))
    c.d = ImageDraw.Draw(c.im)
    c.arc((cx - r + 20, cy - r + 20, cx + r - 20, cy + r - 20), 200, 250, (255, 255, 255, 120), 6)
    return c.done()
