"""T09 · ¿Por qué el móvil carga lento después del 80 %? (estilo Titanic, ilustración detallada)."""
from gadgets import *
import t02_microondas as T2
import t04_qr as T4

xf, callout, glow_line, top_shade, check = T2.xf, T2.callout, T2.glow_line, T2.top_shade, T4.check

TITLE = "Por_que_el_movil_carga_lento_despues_del_80"
LINES = [
    "El móvil carga rapidísimo hasta el *80 %*… y luego va a paso de tortuga.",
    "¿Fallo del cargador? No: *es a propósito*.",
    "Dentro de tu batería hay *iones de litio* que viajan de un lado a otro.",
    "Al cargar, *la corriente los empuja* hacia un lado de la batería.",
    "Al principio hay mucho sitio libre, así que entra *mucha corriente*: es la fase rápida.",
    "Pero cada celda tiene un límite de voltaje: unos *4,2 voltios*.",
    "Si se pasa, la batería se *degrada*… y hasta puede *hincharse*.",
    "Así que, al llegar a ese límite, el móvil *cambia de modo*.",
    "Mantiene el voltaje fijo… y baja la corriente *poco a poco*.",
    "Es como *llenar un vaso*: al principio chorro fuerte, y al final despacio para no derramar.",
    "Por eso ese último 20 % puede tardar *casi lo mismo* que todo lo anterior.",
    "Y si la batería se calienta, el móvil *frena la carga*.",
    "Muchos móviles *se paran en el 80 %* por la noche… y terminan justo antes de que te levantes.",
    "Así que ese frenazo final no es un fallo… es tu móvil *cuidándose*.",
]
SHOTS = [("open", 0, 1, 0.3), ("ions", 2, 4, 0.3), ("limit", 5, 6, 0.3), ("cv", 7, 8, 0.3), ("glass", 9, 9, 0.3),
         ("curve", 10, 11, 0.3), ("night", 12, 12, 0.3), ("final", 13, 13, 1.8)]
FOCUS = {"ions": (540, 880, 1.1), "glass": (540, 900, 1.1)}
NOTIF = ("limit", 0.8)
HYPE = {"line": 1, "text": ['¿FALLO DEL CARGADOR?', 'NO: ES A PROPÓSITO'], "delay": [0, 1.15]}
NOTIF_TEXT = "Suscríbete para entender cómo funciona todo"

GREEN = (90, 230, 130)
LI = (255, 200, 80)
ORANGE = (255, 150, 60)


# ------------------------------------------------------------------ piezas
def battery_overlay(scr, pct, t, bolt=True, note=None):
    dd = ImageDraw.Draw(scr, "RGBA")
    w = scr.size[0]
    x0, y0, x1, y1 = 104, 420, 324, 560
    dd.rounded_rectangle([x0, y0, x1, y1], radius=24, outline=(255, 255, 255, 230), width=8)
    dd.rounded_rectangle([x1 + 6, y0 + 44, x1 + 22, y1 - 44], radius=6, fill=(255, 255, 255, 230))
    fw = (x1 - x0 - 24) * pct / 100
    col = GREEN if pct > 20 else (255, 80, 80)
    dd.rounded_rectangle([x0 + 12, y0 + 12, x0 + 12 + fw, y1 - 12], radius=14, fill=col + (255,))
    if bolt:
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        dd.polygon([(cx + 10, cy - 50), (cx - 30, cy + 8), (cx - 2, cy + 8), (cx - 14, cy + 50), (cx + 30, cy - 10), (cx + 2, cy - 10)], fill=(255, 255, 255, 255))
    dd.text((w / 2, 650), f"{int(pct)} %", font=f(F_CAP, 96), fill=(255, 255, 255), anchor="mm")
    if note:
        dd.rounded_rectangle([40, 740, w - 40, 820], radius=24, fill=(0, 0, 0, 150))
        dd.text((w / 2, 780), note, font=f(F_CAP, 26), fill=(255, 255, 255), anchor="mm")


def _nightstand():
    c = Cv(W, H, 2)
    c.rect((0, 0, W, H), grad=((30, 30, 52), (14, 14, 24)))
    c.rect((640, 420, 1000, 900), fill=(40, 34, 30), r=6)
    c.rect((656, 436, 984, 884), grad=((10, 14, 40), (34, 30, 70)))
    c.ellipse((850, 470, 930, 550), radial=((255, 250, 220), (220, 210, 170)))
    c.line([(820, 436), (820, 884)], (40, 34, 30), 8)
    c.rect((0, 1180, W, 1230), grad=((130, 90, 56), (90, 60, 36)))
    c.rect((0, 1230, W, H), grad=((80, 54, 34), (30, 20, 12)))
    c.rect((60, 1300, 1020, 1320), fill=(60, 40, 26))
    c.ellipse((480, 1310, 600, 1340), fill=(180, 150, 90))
    c.poly([(80, 1180), (280, 1180), (230, 820), (130, 820)], grad=((250, 220, 160), (200, 160, 100)))
    c.rect((170, 1100, 190, 1180), fill=(60, 50, 40))
    c.glow(180, 900, 300, (255, 220, 150), 0.7)
    return c.done().convert("RGBA")


def tortoise():
    c = Cv(300, 200)
    c.ellipse((40, 30, 230, 160), radial=((160, 190, 90), (70, 100, 40)), center=(0.4, 0.3))
    for x, y in ((90, 70), (140, 60), (190, 80), (110, 115), (165, 115)):
        c.ellipse((x - 24, y - 20, x + 24, y + 20), fill=(110, 140, 60))
    c.ellipse((220, 90, 290, 140), fill=(170, 160, 110))
    c.ellipse((262, 104, 272, 114), fill=(20, 20, 20))
    for x in (70, 120, 170, 210):
        c.ellipse((x - 18, 140, x + 18, 180), fill=(170, 160, 110))
    return c.done()


def charger():
    c = Cv(300, 360)
    c.shadow((30, 320, 270, 360), 150, 10)
    c.rect((40, 60, 260, 320), grad=((250, 250, 252), (196, 198, 204)), horizontal=True, r=30)
    c.rect((110, 10, 130, 70), fill=(200, 200, 206), r=4)
    c.rect((170, 10, 190, 70), fill=(200, 200, 206), r=4)
    c.rect((120, 250, 180, 290), fill=(40, 40, 44), r=8)
    return c.done()


def cell(img, t, fill_k, rate=1.0, cx=540, cy=860):
    d = ImageDraw.Draw(img, "RGBA")
    x0, x1, y0, y1 = cx - 440, cx + 440, cy - 300, cy + 300
    d.rounded_rectangle([x0 - 20, y0 - 20, x1 + 20, y1 + 20], radius=40, fill=(150, 156, 166, 255))
    d.rounded_rectangle([x0, y0, x1, y1], radius=30, fill=(26, 28, 36, 255))
    ax0, ax1 = x0 + 30, cx - 50
    for k in range(10):
        y = y0 + 40 + k * 54
        d.rounded_rectangle([ax0, y, ax1, y + 30], radius=8, fill=(70, 72, 82, 255))
    for k in range(6):
        y = y0 + 20 + k * 100
        d.line([(cx, y), (cx, y + 50)], fill=(220, 220, 230, 160), width=4)
    cx0, cx1 = cx + 50, x1 - 30
    for i in range(7):
        for j in range(10):
            x, y = cx0 + 30 + i * 52, y0 + 40 + j * 56
            d.ellipse([x - 16, y - 16, x + 16, y + 16], fill=(90, 120, 200, 255))
    spaced(d, (ax0 + ax1) / 2, y1 + 70, "GRAFITO", f(F_SER, 34), (210, 214, 225, 230), 5)
    spaced(d, (cx0 + cx1) / 2, y1 + 70, "ÓXIDO METÁLICO", f(F_SER, 34), (180, 200, 255, 230), 4)
    slots = [(ax0 + 30 + i * 46, y0 + 70 + k * 54) for k in range(10) for i in range(8)]
    rr = random.Random(3)
    n_in = int(len(slots) * fill_k)
    for i, (x, y) in enumerate(slots):
        if i < n_in:
            paste(img, glow(22, LI, 1.0), x, y)
    for i in range(18):
        u = ((t * 0.6 * rate) + i / 18 + rr.random() * 0.1) % 1.0
        x = lerp(cx1 - 30, ax1 - 10, u)
        y = y0 + 40 + (i * 37) % 540 + math.sin(u * 8 + i) * 8
        paste(img, glow(30, LI, 1.0), x, y)
        d = ImageDraw.Draw(img, "RGBA")
        d.text((x, y), "+", font=f(F_CAP, 20), fill=(60, 30, 0), anchor="mm")


def gauge(img, t, v, cx=540, cy=860, r=330):
    d = ImageDraw.Draw(img, "RGBA")
    d.ellipse([cx - r - 20, cy - r - 20, cx + r + 20, cy + r + 20], fill=(60, 62, 70, 255))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(244, 240, 228, 255))
    a0, a1 = 150, 390
    vmin, vmax = 3.0, 4.6
    ang = lambda vv: a0 + (vv - vmin) / (vmax - vmin) * (a1 - a0)
    d.arc([cx - r + 30, cy - r + 30, cx + r - 30, cy + r - 30], ang(4.2), a1, fill=(220, 50, 50, 255), width=36)
    for k in range(17):
        vv = vmin + k * 0.1
        a = math.radians(ang(vv))
        l = 40 if k % 5 == 0 else 22
        d.line([(cx + math.cos(a) * (r - 30), cy + math.sin(a) * (r - 30)), (cx + math.cos(a) * (r - 30 - l), cy + math.sin(a) * (r - 30 - l))], fill=(40, 40, 44), width=5)
        if k % 5 == 0:
            d.text((cx + math.cos(a) * (r - 110), cy + math.sin(a) * (r - 110)), f"{vv:.1f}".replace(".", ","), font=f(F_SER, 40), fill=(40, 40, 44), anchor="mm")
    a = math.radians(ang(v))
    d.line([(cx, cy), (cx + math.cos(a) * (r - 60), cy + math.sin(a) * (r - 60))], fill=(200, 30, 30), width=10)
    d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=(40, 40, 44))
    d.text((cx, cy + 130), f"{v:.2f} V".replace(".", ","), font=f(F_MONO, 60), fill=(40, 40, 44), anchor="mm")


def pouch(img, t, swell):
    sky(img, (40, 20, 18), (12, 8, 8), 1.0)
    cx, cy = 540, 880
    c = Cv(700, 900)
    bw = 260 + 80 * swell
    c.ellipse((350 - bw, 450 - 360 - 30 * swell, 350 + bw, 450 + 360 + 30 * swell), radial=((236, 236, 240), (150, 154, 162)), power=1.2 - 0.4 * swell, center=(0.4, 0.35))
    c.rect((350 - 260, 90, 350 + 260, 810), fill=(200, 204, 212, int(255 * (1 - swell))), r=30)
    c.rect((300, 40, 330, 100), fill=(200, 160, 60))
    c.rect((370, 40, 400, 100), fill=(160, 160, 166))
    c.text((350, 450), "Li-ion", 60, (60, 60, 70))
    paste(img, c.done(), cx, cy, 1.0)
    if swell > 0.3:
        d = ImageDraw.Draw(img, "RGBA")
        k = clamp((swell - 0.3) / 0.3)
        d.polygon([(880, 520), (960, 660), (800, 660)], fill=(255, 210, 63, int(255 * k)))
        d.text((880, 615), "!", font=f(F_CAP, 70), fill=(40, 30, 0, int(255 * k)), anchor="mm")


def graph_cccv(img, t, t0, k):
    sky(img, (12, 16, 24), (4, 6, 8), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    x0, x1, y0, y1 = 120, 980, 520, 1240
    d.rounded_rectangle([x0 - 30, y0 - 40, x1 + 30, y1 + 60], radius=20, fill=(10, 14, 20, 230), outline=(60, 80, 100, 255), width=3)
    xm = lerp(x0, x1, 0.55)
    d.line([(xm, y0), (xm, y1)], fill=(255, 255, 255, 60), width=3)
    vp, ip = [], []
    for i in range(0, 201):
        u = i / 200
        if u > k:
            break
        x = lerp(x0, x1, u)
        v = 0.55 + 0.4 * (1 - math.exp(-u * 5)) if u < 0.55 else 0.95
        if u < 0.55:
            v = lerp(0.45, 0.95, (u / 0.55) ** 0.7)
        cur = 0.85 if u < 0.55 else 0.85 * math.exp(-(u - 0.55) * 6)
        vp.append((x, y1 - v * (y1 - y0)))
        ip.append((x, y1 - cur * (y1 - y0) * 0.9))
    if len(vp) > 1:
        glow_line(img, vp, (255, 210, 63), 5, 8, 240)
        glow_line(img, ip, (90, 200, 255), 5, 8, 240)
    d = ImageDraw.Draw(img, "RGBA")
    d.text((x0 + 10, y0 + 10), "VOLTAJE", font=f(F_SER, 34), fill=(255, 210, 63))
    d.text((x0 + 10, y0 + 56), "CORRIENTE", font=f(F_SER, 34), fill=(90, 200, 255))
    d.text(((x0 + xm) / 2, y1 + 30), "RÁPIDA", font=f(F_SER, 32), fill=(220, 220, 230), anchor="mm")
    d.text(((xm + x1) / 2, y1 + 30), "LENTA (4,2 V FIJOS)", font=f(F_SER, 32), fill=(220, 220, 230), anchor="mm")


def glass_fill(img, t, t0, T):
    sky(img, (40, 46, 56), (12, 14, 18), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, 1240, W, H], fill=(70, 60, 54, 255))
    d.rounded_rectangle([420, 440, 760, 500], radius=20, fill=(180, 184, 192, 255))
    d.rounded_rectangle([600, 480, 660, 560], radius=10, fill=(160, 164, 172, 255))
    u = clamp((t - t0) / max(1.0, T - 0.8))
    lvl = 1 - (1 - u) ** 2.2 if u < 1 else 1
    lvl = min(0.96, 0.8 * clamp(u / 0.35) + 0.16 * clamp((u - 0.35) / 0.65))
    stream = 44 if u < 0.35 else max(6, 44 * (1 - (u - 0.35) / 0.65 * 0.85))
    gx0, gx1, gy0, gy1 = 400, 860, 700, 1240
    wy = gy1 - (gy1 - gy0) * lvl
    d.polygon([(gx0 + 30, wy), (gx1 - 30, wy), (gx1 - 50, gy1 - 10), (gx0 + 50, gy1 - 10)], fill=(90, 160, 230, 200))
    d.line([(630 - stream / 2 + stream / 2, 560), (630, wy)], fill=(140, 200, 255, 220), width=int(stream))
    d.polygon([(gx0, gy0), (gx1, gy0), (gx1 - 40, gy1), (gx0 + 40, gy1)], outline=(230, 240, 255, 220), width=8)
    d.line([(gx0 + 60, gy0 + 40), (gx0 + 90, gy1 - 60)], fill=(255, 255, 255, 80), width=14)
    d.text((gx1 + 30, wy), f"{int(lvl * 104)} %", font=f(F_MONO, 44), fill=(255, 255, 255), anchor="lm")


def curve(img, t, t0, k, hot=0.0):
    sky(img, (12, 16, 24), (4, 6, 8), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    x0, x1, y0, y1 = 140, 980, 520, 1220
    d.line([(x0, y1), (x1, y1)], fill=(200, 200, 210), width=4)
    d.line([(x0, y1), (x0, y0)], fill=(200, 200, 210), width=4)
    xm = lerp(x0, x1, 0.5)
    y80 = y1 - 0.8 * (y1 - y0)
    d.rectangle([xm, y0, x1, y1], fill=(255, 210, 63, 30))
    pts = []
    for i in range(201):
        u = i / 200
        if u > k:
            break
        p = 0.8 * (u / 0.5) if u < 0.5 else 0.8 + 0.2 * (1 - math.exp(-(u - 0.5) * 7)) / (1 - math.exp(-3.5))
        pts.append((lerp(x0, x1, u), y1 - p * (y1 - y0)))
    if len(pts) > 1:
        glow_line(img, pts, GREEN, 6, 8, 240)
    d = ImageDraw.Draw(img, "RGBA")
    d.line([(x0, y80), (x1, y80)], fill=(255, 255, 255, 70), width=2)
    d.text((x0 - 20, y80), "80 %", font=f(F_SER, 34), fill=(255, 255, 255), anchor="rm")
    d.text((x0 - 20, y0), "100 %", font=f(F_SER, 34), fill=(255, 255, 255), anchor="rm")
    d.text(((x0 + xm) / 2, y1 + 40), "0 → 80 %", font=f(F_SER, 34), fill=(220, 220, 230), anchor="mm")
    d.text(((xm + x1) / 2, y1 + 40), "80 → 100 %", font=f(F_SER, 34), fill=(255, 210, 63), anchor="mm")
    if hot > 0:
        overlay(img, (255, 70, 30), 0.2 * hot)
        d = ImageDraw.Draw(img, "RGBA")
        tx, ty = 900, 640
        d.rounded_rectangle([tx - 26, ty - 160, tx + 26, ty + 140], radius=26, fill=(250, 250, 250, 255), outline=(80, 80, 90, 255), width=4)
        d.rounded_rectangle([tx - 10, ty + 60 - 180 * hot, tx + 10, ty + 120], radius=10, fill=(220, 40, 40, 255))
        d.ellipse([tx - 38, ty + 110, tx + 38, ty + 186], fill=(220, 40, 40, 255))


# ------------------------------------------------------------------ planos
def stand(img, t, pct, note=None, morning=0.0):
    AC(img, cached("nightstand", _nightstand))
    if morning > 0:
        overlay(img, (255, 200, 140), 0.25 * morning)
    d = ImageDraw.Draw(img, "RGBA")
    d.line([(500, 1220), (500, 1290), (300, 1320), (0, 1310)], fill=(240, 240, 244, 255), width=10)
    phone(img, 500, 930, 0.62, "lock", 0, 1.0, lambda scr: battery_overlay(scr, pct, t, True, note))


def sh_open(img, t, T, L):
    a1 = L[1][0]
    if t < a1:
        u = clamp((t - 0.4) / max(1.0, a1 - 0.8))
        pct = 80 * clamp(u / 0.6) + 4 * clamp((u - 0.6) / 0.4)
        pct = max(12, pct) if u < 0.12 else pct
        stand(img, t, max(12, pct))
        if u > 0.6:
            k = ease(clamp((u - 0.6) / 0.3))
            paste(img, spr(tortoise), lerp(1200, 860, k), 1150, 0.9)
    else:
        sky(img, (24, 26, 34), (8, 8, 10), 1.0)
        paste(img, spr(charger), 540, 860, 1.4)
        k = ease(clamp((t - a1 - 0.6) / 0.4))
        if k > 0:
            st = Image.new("RGBA", (700, 200), (0, 0, 0, 0))
            sd = ImageDraw.Draw(st)
            sd.rounded_rectangle([20, 20, 680, 180], radius=16, outline=(90, 230, 130, 240), width=8)
            sd.text((350, 100), "A PROPÓSITO", font=f(F_SER, 76), fill=(90, 230, 130, 240), anchor="mm")
            paste(img, st.rotate(-8, expand=True, resample=Image.BICUBIC), 540, 880, lerp(1.4, 1.0, k), k)
    top_shade(img)
    if t < a1:
        title2(t, 0.3, "RÁPIDO HASTA EL 80 %", "Y LUEGO… LENTO", 250, 58, 82, hold=max(1.8, a1 - 0.3))
    vignette(img, 190)


def sh_ions(img, t, T, L):
    a1, a2 = L[1][0], L[2][0]
    sky(img, (12, 14, 22), (4, 4, 8), 1.0)
    fill_k = 0.15 if t < a1 else 0.15 + 0.5 * ease(clamp((t - a1) / (T - a1)))
    rate = 0.4 if t < a1 else (1.0 if t < a2 else 2.0)
    cell(img, t, fill_k, rate)
    if t > a2:
        d = ImageDraw.Draw(img, "RGBA")
        k = ease(clamp((t - a2 - 0.4) / 0.5))
        for i in range(3):
            y = 680 + i * 160
            d.polygon([(560, y - 26), (560, y + 26), (500, y)], fill=(255, 255, 255, int(200 * k)))
    if t < a1:
        big(t, 0.3, "IONES DE LITIO", 290, 92, LI, pop=False)
    elif t < a2:
        big(t, a1 + 0.2, "LA CORRIENTE LOS EMPUJA", 290, 64, WHITE, pop=False)
    else:
        big(t, a2 + 0.3, "FASE RÁPIDA", 290, 100, GREEN)
    vignette(img, 190)


def sh_limit(img, t, T, L):
    a1 = L[1][0]

    def A(im):
        sky(im, (16, 18, 24), (6, 6, 8), 1.0)
        v = 3.3 + 0.9 * ease(clamp((t - 0.3) / 2.2))
        gauge(im, t, v)

    xf(img, t, a1, A, lambda im: pouch(im, t, ease(clamp((t - a1 - 0.8) / 1.8))), 0.6)
    if t < a1:
        big(t, 0.4, "LÍMITE: 4,2 V", 280, 100, YEL)
    else:
        big(t, a1 + 0.2, "SE DEGRADA", 270, 92, (255, 110, 100), sub="Y PUEDE HINCHARSE")
    vignette(img, 190)


def sh_cv(img, t, T, L):
    a1 = L[1][0]
    k = clamp((t - 0.3) / (T - 0.8))
    graph_cccv(img, t, 0, 0.55 * clamp(t / max(0.5, a1)) if t < a1 else 0.55 + 0.45 * clamp((t - a1) / (T - a1 - 0.4)))
    if t < a1:
        big(t, 0.3, "CAMBIA DE MODO", 290, 90, WHITE, pop=False)
    else:
        big(t, a1 + 0.2, "MENOS CORRIENTE", 290, 84, (90, 200, 255), sub="POCO A POCO")
    vignette(img, 190)


def sh_glass(img, t, T, L):
    glass_fill(img, t, 0.3, T)
    big(t, 0.3, "COMO LLENAR UN VASO", 290, 70, WHITE, pop=False)
    vignette(img, 190)


def sh_curve(img, t, T, L):
    a1 = L[1][0]
    curve(img, t, 0, clamp((t - 0.2) / 2.6), ease(clamp((t - a1 - 0.2) / 1.2)) if t > a1 else 0.0)
    if t < a1:
        big(t, 1.4, "EL ÚLTIMO 20 %", 290, 92, YEL, sub="CASI LO MISMO")
    else:
        big(t, a1 + 0.4, "SI SE CALIENTA, FRENA", 290, 66, (255, 120, 90), pop=False)
    vignette(img, 190)


def sh_night(img, t, T, L):
    k = ease(clamp((t - 1.6) / (T - 2.4)))
    pct = 80 if t < 1.6 else 80 + 20 * k
    stand(img, t, pct, "Carga optimizada" if pct < 100 else "Cargado", k)
    d = ImageDraw.Draw(img, "RGBA")
    hh, mm = (2, 0) if t < 1.6 else (2 + int(k * 4.9), int((k * 4.9 % 1) * 60))
    d.rounded_rectangle([700, 1060, 980, 1180], radius=16, fill=(20, 20, 24, 255))
    d.text((840, 1120), f"{hh:02d}:{mm:02d}", font=f(F_MONO, 64), fill=(255, 90, 60), anchor="mm")
    d.text((840, 1030), "ALARMA 7:00", font=f(F_SER, 28), fill=(220, 220, 230, 220), anchor="mm")
    top_shade(img)
    big(t, 0.3, "SE PARA EN EL 80 %", 270, 76, WHITE, hold=1.6, pop=False)
    if t > 2.2:
        big(t, 2.2, "Y TERMINA ANTES", 270, 80, YEL, sub="DE QUE TE LEVANTES", pop=False)
    vignette(img, 190)


def sh_final(img, t, T, L):
    AC(img, cached("nightstand", _nightstand))
    overlay(img, (255, 200, 140), 0.2)
    phone(img, 500, 930, 0.62, "lock", 0, 1.0, lambda scr: battery_overlay(scr, 100, t, False, "Salud de la batería"))
    d = ImageDraw.Draw(img, "RGBA")
    k = ease(clamp((t - 0.6) / 0.6))
    cx, cy = 820, 760
    d.polygon([(cx, cy - 80), (cx + 70, cy - 50), (cx + 60, cy + 40), (cx, cy + 90), (cx - 60, cy + 40), (cx - 70, cy - 50)], fill=(90, 230, 130, int(230 * k)))
    d.line([(cx - 30, cy), (cx - 6, cy + 26), (cx + 34, cy - 24)], fill=(255, 255, 255, int(255 * k)), width=12, joint="curve")
    top_shade(img)
    title2(t, 0.3, "NO ES UN FALLO", "SE ESTÁ CUIDANDO", 250, 58, 84, hold=max(2.0, T - 1.2))
    vignette(img, 190)


FNS = {k: globals()["sh_" + k] for k, *_ in SHOTS}
AUDIO = {
    "music": [("open", "playful"), ("ions", "exp"), ("limit", "tension"), ("cv", "creative"), ("glass", "warm"), ("curve", "doc"),
              ("night", "warm"), ("final", "premium")],
    "gains": {"exp": 0.7},
    "amb": {"room": ["open", "night", "final"], "hum": ["ions", "cv"]},
    "sfx": [("open+0.4", "blip", 0.12), ("open+2.6", "blip_down", 0.1), ("open@L1+0.6", "thud", 0.25),
            ("ions+0.3", "whoosh", 0.12), ("ions@L1", "zap", 0.08), ("ions@L2+0.3", "whoosh_up", 0.14),
            ("limit+0.3", "riser", 0.1), ("limit+2.5", "beep", 0.06), ("limit@L1+0.8", "swell", 0.12), ("limit@L1+1.8", "pop", 0.18),
            ("cv+0.3", "click", 0.3), ("cv@L1+0.2", "blip_down", 0.12),
            ("glass+0.4", "swell", 0.1),
            ("curve+0.3", "draw", 0.12), ("curve@L1+0.4", "riser", 0.08),
            ("night+1.6", "whoosh", 0.1), ("night+3.5", "chime", 0.06), ("final+0.6", "ding", 0.08), ("final+0.8", "swell", 0.14)],
    "bed": [("ions", "limit")],
    "bpm": 96,
}
