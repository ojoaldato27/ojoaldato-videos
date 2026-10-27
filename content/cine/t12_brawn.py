"""T12 · Brawn GP (2009): el equipo que costó una libra y ganó el Mundial en su único año — estilo microondas."""
from gadgets import *
import t02_microondas as T2
import t04_qr as T4
import t11_f1_ventilador as T11

xf, callout, glow_line, top_shade, check, sepia = T2.xf, T2.callout, T2.glow_line, T2.top_shade, T4.check, T2.sepia
track_bg, trophy = T11.track_bg, T11.trophy

TITLE = "El_equipo_de_F1_que_costo_una_libra"
LINES = [
    "En 2009, un equipo que tres meses antes *no existía* ganó el Mundial de Fórmula 1.",
    "¿Cómo lo consiguió… y por qué *desapareció* justo después?",
    "En diciembre de 2008, por *la crisis*, Honda abandona la F1… y su equipo se queda *sin dueño*.",
    "Su jefe, *Ross Brawn*, se lo compra a Honda… por *una libra*.",
    "Lo llama *Brawn GP* y, a contrarreloj, le mete un *motor Mercedes*.",
    "Casi sin patrocinadores, sale *blanco*, con detalles *amarillo flúor*.",
    "Pero detrás escondía un truco: el *doble difusor*.",
    "Un difusor de *dos pisos* que sacaba más aire de debajo… y lo *pegaba al suelo*.",
    "Los rivales *protestaron*, pero la FIA lo declaró legal.",
    "Primera carrera, Australia: *pole* y *doblete*.",
    "Button ganó *6 de las 7 primeras* carreras.",
    "Luego, con frío, *no calentaba los neumáticos*… y *Red Bull* empezó a ganar.",
    "Pero los puntos del principio *bastaron*.",
    "En Brasil, saliendo *14.º*, Button acabó quinto… y fue *campeón del mundo*.",
    "Y Brawn ganó también el *Mundial de constructores*.",
    "Un mes después, *Mercedes* compró la mayoría del equipo… por unos *110 millones de libras*, según se publicó.",
    "Ya como Mercedes, ganaría *8 Mundiales de constructores* seguidos.",
    "Un equipo vendido por una libra… A veces, lo que parece un final es solo el principio.",
]
SHOTS = [("open", 0, 1, 0.3), ("honda", 2, 2, 0.3), ("pound", 3, 3, 0.3), ("engine", 4, 4, 0.3), ("livery", 5, 5, 0.3),
         ("diffuser", 6, 7, 0.3), ("legal", 8, 8, 0.3), ("australia", 9, 9, 0.3), ("streak", 10, 10, 0.3), ("cold", 11, 12, 0.3),
         ("brazil", 13, 13, 0.3), ("titles", 14, 14, 0.3), ("mercedes", 15, 15, 0.3), ("eight", 16, 16, 0.3), ("final", 17, 17, 1.8)]
FOCUS = {"australia": (540, 950, 1.06)}
NOTIF = ("pound", 0.6)
HYPE = {"line": 1, "text": ["¿CÓMO LO CONSIGUIÓ?", "¿Y POR QUÉ DESAPARECIÓ?"], "delay": [0, 1.2]}
KW_OVERRIDE = {17: []}  # la reflexión final va sin palabra clave: ya la escribe la escena
STICKER_EXTRA = [("crisis", "📉"), ("economica", "📉"), ("libra", "🪙"), ("compra", "🤝"), ("motor", "🔧"), ("blanco", "⚪"),
                 ("amarillo", "💛"), ("patrocinador", "💸"), ("truco", "🤫"), ("difusor", "💨"), ("suelo", "⬇️"),
                 ("protestaron", "😡"), ("legal", "✅"), ("australia", "🦘"), ("pole", "🥇"), ("primero", "🥇"), ("segundo", "🥈"),
                 ("problemas", "⚠️"), ("frias", "🥶"), ("neumaticos", "🥶"), ("=ganar", "🏁"), ("bastaron", "😅"),
                 ("brasil", "🇧🇷"), ("campeon", "🏆"), ("titulos", "🏆"), ("millones", "💰"),
                 ("trucos", "🤫"), ("desaparecio", "💨")]
NOTIF_TEXT = "Suscríbete para más cosas que no sabías"
# El ojo-stickman cuenta la historia: pose por plano, siempre abajo a la izquierda
NARRATOR = {"open": ("wave", "left"), "honda": ("think", "left"), "pound": ("point", "left"), "engine": ("point", "left"),
            "livery": ("point", "left"), "diffuser": ("point", "left"), "legal": ("smirk", "left"), "australia": ("flag", "left"),
            "streak": ("flag", "left"), "cold": ("think", "left"), "brazil": ("flag", "left"), "titles": ("surprise", "left"),
            "mercedes": ("point", "left"), "eight": ("surprise", "left"), "final": ("think", "left")}

CHART = (206, 236, 28)      # amarillo flúor (chartreuse) de la decoración
INK = (18, 18, 22)
WHITE_CAR = (246, 246, 248)
SILVER = (186, 192, 202)
NAVY = (28, 36, 84)
CY_ = (110, 210, 255)
RED = (230, 60, 66)
GREEN = (90, 230, 130)


# ------------------------------------------------------------------ objetos
def bgp_side(body=WHITE_CAR, acc=CHART, dark=INK):
    """Fórmula 1 de 2009 visto de lado: alerón delantero ancho y bajo, alerón trasero alto y estrecho, neumáticos lisos (sin marcas)."""
    c = Cv(1080, 380)
    c.shadow((20, 318, 1060, 372), 170, 12)
    hi, lo = shade(body, 1.04), shade(body, 0.62)
    # alerón trasero (detrás de todo)
    c.poly([(915, 70), (1050, 58), (1060, 252), (940, 252)], grad=(shade(dark, 2.2), dark))
    c.rect((905, 56, 1062, 92), grad=(shade(dark, 2.6), dark), r=6)
    c.rect((905, 84, 1062, 92), fill=acc + (255,))
    c.rect((930, 150, 1050, 168), grad=(shade(dark, 2.0), dark), r=4)
    # suelo y fondo plano
    c.rect((150, 266, 935, 286), grad=((40, 40, 46), (10, 10, 12)), r=6)
    # carrocería principal
    c.poly([(40, 236), (130, 216), (300, 198), (430, 184), (480, 176), (560, 174), (600, 116), (660, 110), (700, 150),
            (800, 176), (900, 198), (915, 232), (900, 266), (60, 260)], grad=(hi, lo), power=0.9)
    # pontón lateral
    c.poly([(470, 262), (500, 214), (760, 210), (870, 236), (872, 264)], grad=(shade(body, 0.98), shade(body, 0.7)))
    # decoración flúor: punta del morro, línea del pontón y tapa del motor
    c.poly([(40, 236), (130, 216), (140, 238), (60, 252)], fill=acc + (255,))
    c.poly([(486, 222), (760, 216), (874, 240), (872, 252), (760, 230), (486, 236)], fill=acc + (255,))
    c.poly([(610, 118), (660, 112), (700, 152), (820, 182), (816, 192), (690, 164), (650, 128), (606, 132)], fill=acc + (255,))
    # franja negra inferior
    c.poly([(60, 252), (900, 258), (900, 268), (60, 262)], fill=dark + (255,))
    # caja de aire y arco antivuelco
    c.poly([(560, 174), (600, 116), (640, 114), (612, 176)], grad=(shade(body, 0.9), shade(body, 0.55)))
    c.ellipse((598, 120, 632, 150), fill=(24, 26, 32))
    # cabina y casco
    c.poly([(440, 184), (470, 160), (560, 158), (566, 176)], fill=(24, 28, 38))
    c.ellipse((486, 118, 552, 180), radial=((255, 255, 255), (200, 204, 214)), center=(0.38, 0.3))
    c.poly([(510, 136), (552, 136), (550, 156), (512, 156)], fill=(20, 24, 34))
    c.rect((486, 160, 552, 168), fill=acc + (255,))
    # alerón delantero: placa lateral y planos
    c.rect((0, 292, 160, 304), grad=(shade(dark, 2.4), dark), r=4)
    c.rect((0, 306, 150, 316), grad=(shade(dark, 2.0), dark), r=4)
    c.poly([(4, 262), (52, 262), (60, 320), (0, 320)], grad=(shade(dark, 2.4), dark))
    c.line([(4, 262), (52, 262)], acc + (255,), 4)
    c.line([(80, 252), (100, 292)], (60, 62, 70), 6)
    # suspensiones
    for x0, x1, y0 in ((200, 330, 230), (200, 330, 252), (842, 740, 236), (842, 740, 254)):
        c.line([(x0, y0), (x1, y0 - 8)], (60, 62, 70), 5)
    # neumáticos lisos
    for wx, wy, r in ((210, 270, 62), (842, 262, 70)):
        c.ellipse((wx - r, wy - r, wx + r, wy + r), radial=((46, 46, 50), (10, 10, 12)), power=1.3)
        c.ellipse((wx - r * 0.56, wy - r * 0.56, wx + r * 0.56, wy + r * 0.56), radial=((200, 204, 212), (70, 74, 82)), center=(0.4, 0.35))
        c.ellipse((wx - r * 0.2, wy - r * 0.2, wx + r * 0.2, wy + r * 0.2), fill=(40, 42, 48))
        c.arc((wx - r + 5, wy - r + 5, wx + r - 5, wy + r - 5), 200, 260, (255, 255, 255, 60), 4)
    c.line([(70, 228), (430, 188)], (255, 255, 255, 120), 3)
    return c.done()


def cover_car():
    """Coche tapado con una funda en el garaje."""
    c = Cv(1080, 380)
    c.shadow((20, 318, 1060, 372), 170, 12)
    c.poly([(10, 300), (60, 250), (300, 214), (520, 150), (640, 120), (760, 150), (960, 160), (1060, 120), (1070, 310), (10, 316)],
           grad=((120, 124, 134), (50, 52, 60)), power=0.9)
    for x in (180, 420, 640, 860):
        c.line([(x, 200), (x + 40, 312)], (40, 42, 48, 140), 6)
    c.line([(60, 252), (520, 154)], (255, 255, 255, 50), 4)
    return c.done()


def newspaper():
    c = Cv(700, 860)
    c.shadow((20, 800, 680, 860), 150, 14)
    c.rect((20, 20, 680, 820), grad=((246, 240, 224), (220, 212, 192)), r=6)
    c.rect((50, 60, 650, 130), fill=(30, 30, 34))
    c.text((350, 96), "DIARIO DEL MOTOR", 48, (246, 240, 224), font=F_SER)
    c.line([(50, 150), (650, 150)], (30, 30, 34), 3)
    c.text((350, 176), "DICIEMBRE · 2008", 26, (90, 84, 70), font=F_SER)
    c.text((350, 262), "HONDA DEJA", 92, (20, 20, 24), font=F_SER)
    c.text((350, 362), "LA FÓRMULA 1", 70, (20, 20, 24), font=F_SER)
    c.rect((50, 430, 330, 640), grad=((150, 150, 150), (110, 110, 110)))
    for k in range(9):
        y = 440 + k * 24
        c.line([(360, y), (650, y)], (120, 114, 100), 6)
    for k in range(6):
        y = 670 + k * 24
        c.line([(50, y), (650, y)], (120, 114, 100), 6)
    return c.done()


def coin(face=True):
    c = Cv(420, 420)
    c.ellipse((10, 10, 410, 410), radial=((255, 226, 120), (176, 120, 20)), center=(0.38, 0.32))
    c.ellipse((40, 40, 380, 380), radial=((255, 236, 150), (200, 150, 40)), center=(0.4, 0.35))
    for k in range(60):
        a = k * math.pi / 30
        c.line([(210 + math.cos(a) * 196, 210 + math.sin(a) * 196), (210 + math.cos(a) * 204, 210 + math.sin(a) * 204)], (150, 100, 20), 3)
    if face:
        c.text((210, 214), "1 £", 150, (140, 92, 10), font=F_SER)
    c.arc((60, 60, 360, 360), 200, 250, (255, 255, 255, 120), 10)
    return c.done()


def v8_engine():
    """Motor V8 en corte, visto de lado: bloque, culatas, trompetas de admisión y escapes."""
    c = Cv(820, 560)
    c.shadow((40, 500, 780, 556), 160, 12)
    c.rect((90, 230, 730, 470), grad=((150, 154, 164), (70, 72, 80)), r=24)
    c.poly([(110, 230), (270, 70), (720, 70), (720, 230)], grad=((178, 182, 192), (96, 100, 110)))
    c.poly([(140, 230), (300, 110), (690, 110), (690, 230)], grad=((70, 72, 80), (40, 42, 48)))
    for k in range(4):
        x = 330 + k * 92
        c.rect((x, 20, x + 56, 110), grad=((220, 224, 232), (130, 134, 144)), horizontal=True, r=10)
        c.ellipse((x - 4, 8, x + 60, 36), fill=(40, 42, 48))
        c.ellipse((x + 6, 150, x + 50, 200), radial=((255, 160, 70), (180, 60, 20)))
    for k in range(4):
        y0 = 300 + k * 36
        c.line([(150 + k * 30, 280), (60, y0 + 40), (10, y0 + 70)], (210, 120, 60), 16)
        c.line([(150 + k * 30, 280), (60, y0 + 40), (10, y0 + 70)], (255, 190, 120, 120), 5)
    c.rect((140, 470, 680, 500), fill=(40, 42, 48), r=6)
    c.line([(120, 240), (700, 240)], (255, 255, 255, 60), 4)
    return c.done()


def gavel():
    c = Cv(560, 420)
    c.shadow((60, 360, 520, 410), 150, 10)
    c.rect((150, 300, 470, 370), grad=((140, 90, 50), (80, 50, 26)), r=14)
    c.line([(150, 260), (470, 70)], (120, 76, 40), 22)
    c.rect((60, 190, 300, 280), grad=((170, 110, 60), (96, 60, 30)), r=24)
    c.rect((80, 190, 100, 280), fill=(220, 180, 90))
    c.rect((260, 190, 280, 280), fill=(220, 180, 90))
    return c.done()


def tyre_cold():
    c = Cv(520, 520)
    c.ellipse((10, 10, 510, 510), radial=((54, 56, 62), (12, 12, 14)), power=1.3)
    c.ellipse((130, 130, 390, 390), radial=((200, 204, 212), (70, 74, 82)), center=(0.4, 0.35))
    c.ellipse((215, 215, 305, 305), fill=(40, 42, 48))
    c.arc((24, 24, 496, 496), 200, 260, (255, 255, 255, 70), 8)
    return c.done()


def thermometer(level):
    c = Cv(160, 560)
    c.rect((50, 20, 110, 460), fill=(240, 244, 250, 230), r=30)
    c.ellipse((20, 420, 140, 540), fill=(240, 244, 250, 230))
    col = CY_ if level < 0.5 else (255, 120, 60)
    c.ellipse((36, 436, 124, 524), fill=col)
    c.rect((66, 440 - 400 * level, 94, 470), fill=col, r=12)
    for k in range(8):
        c.line([(112, 60 + k * 50), (128, 60 + k * 50)], (120, 130, 150), 3)
    return c.done()


def confetti(img, t, t0, seed=3, n=110):
    if t < t0 or t > t0 + 3.0:
        return
    d = ImageDraw.Draw(img, "RGBA")
    rng = random.Random(seed)
    cols = [WHITE_CAR, CHART, YEL, (255, 255, 255), (90, 160, 255)]
    u = t - t0
    for _ in range(n):
        x0 = rng.uniform(0, W)
        vy = rng.uniform(380, 760)
        x = x0 + rng.uniform(-90, 90) * u + math.sin(u * 5 + x0) * 22
        y = -60 + vy * u + 140 * u * u - rng.uniform(0, 500)
        if 0 < y < H:
            a = u * 7 + x0
            s = rng.uniform(10, 18)
            pts = [(x + s * math.cos(a), y + s * 0.45 * math.sin(a)), (x - s * math.sin(a) * 0.45, y + s * math.cos(a)),
                   (x - s * math.cos(a), y - s * 0.45 * math.sin(a)), (x + s * math.sin(a) * 0.45, y - s * math.cos(a))]
            d.polygon(pts, fill=rng.choice(cols) + (230,))


def garage_bg(img):
    sky(img, (26, 28, 36), (8, 8, 10), 1.0)
    for x in (200, 880):
        pass
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, 1250, W, H], fill=(40, 40, 46, 255))
    for x in range(0, W, 120):
        d.line([(x, 1250), (x - 200, H)], fill=(52, 52, 60, 255), width=3)


def board(img, k, lines, y=1300, w=740, cols=None, cx=540):
    if k <= 0:
        return
    d = ImageDraw.Draw(img, "RGBA")
    h = 70 + 58 * len(lines)
    d.rounded_rectangle([cx - w / 2, y, cx + w / 2, y + h], radius=20, fill=(10, 12, 18, int(235 * k)), outline=YEL + (int(255 * k),), width=4)
    for i, ln in enumerate(lines):
        col = (cols[i] if cols else (WHITE if i == 0 else YEL))
        d.text((cx, y + 62 + i * 58), ln, font=f(F_MONO, 44), fill=col + (int(255 * k),), anchor="mm")


# ------------------------------------------------------------------ planos
def sh_open(img, t, T, L):
    a1 = L[1][0]
    track_bg(img, t, 880, True, 1.0)
    paste(img, spr(bgp_side), 540, 880 + 160 + 130, 0.98)
    top_shade(img)
    if t < a1 + 0.2:
        title2(t, 0.3, "2009 · UN EQUIPO NUEVO", "CAMPEÓN DEL MUNDO", 250, 54, 84, hold=max(1.8, a1 - 0.3))
    vignette(img, 190)


def sh_honda(img, t, T, L):
    a1 = L[1][0] if len(L) > 1 else T * 0.5

    def A(im):
        sky(im, (40, 34, 30), (12, 10, 8), 1.0)
        spotlight(im, t, 540, 0, 1500, 80, 620, 40, dust=True)
        k = ease(clamp((t - 0.2) / 0.7))
        paste(im, spr(newspaper), 560, lerp(1500, 930, k), lerp(0.7, 0.95, k), k, lerp(-14, -4, k))

    def B(im):
        garage_bg(im)
        spotlight(im, t, 540, 0, 1300, 60, 480, 30, dust=True)
        paste(im, spr(cover_car), 540, 1130, 0.95)
        k = ease(clamp((t - a1 - 0.6) / 1.6))
        d = ImageDraw.Draw(im, "RGBA")
        hgt = 260 + 520 * k
        d.rectangle([0, 0, W, hgt], fill=(70, 74, 84, 255))
        for y in range(0, int(hgt), 40):
            d.line([(0, y), (W, y)], fill=(50, 52, 60, 255), width=4)
        d.rectangle([0, hgt - 16, W, hgt], fill=(40, 42, 48, 255))

    xf(img, t, a1, A, B, 0.6)
    if t < a1:
        date_stamp(t, 0.3, "DICIEMBRE · 2008", 250, hold=max(1.6, a1 - 0.6))
    else:
        big(t, a1 + 0.3, "¿Y AHORA QUÉ?", 300, 100, WHITE)
    vignette(img, 200)


def sh_pound(img, t, T, L):
    sky(img, (26, 22, 14), (6, 6, 4), 1.0)
    spotlight(img, t, 540, 0, 1400, 80, 560, 40, dust=True)
    paste(img, glow(520, (255, 210, 120), 0.4), 540, 900)
    u = t - 0.3
    spin = math.cos(max(0, u) * 9 * math.exp(-max(0, u) * 0.9)) if u < 3.0 else 1.0
    face = spin >= 0
    s = max(0.06, abs(spin))
    k = ease(clamp((t - 0.2) / 0.5))
    im = spr(coin, face)
    im2 = im.resize((max(2, int(im.size[0] * s)), im.size[1]), Image.LANCZOS)
    paste(img, im2, 540, lerp(700, 920, k), 1.3, k)
    d = ImageDraw.Draw(img, "RGBA")
    d.ellipse([340, 1210, 740, 1250], fill=(0, 0, 0, 90))
    lower_third(img, t, 0.6, "ROSS BRAWN", "JEFE DEL EQUIPO", 1300, hold=T)
    big(t, 0.4, "EL PRECIO", 300, 96, YEL, pop=False)
    vignette(img, 200)


def sh_engine(img, t, T, L):
    sky(img, (16, 20, 30), (4, 6, 10), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, 1250, W, H], fill=(36, 38, 46, 255))
    for x in range(0, W, 60):
        d.line([(x, 1250), (x, H)], fill=(44, 46, 54, 255), width=2)
    k = ease(clamp((t - 0.6) / 1.4))
    paste(img, spr(v8_engine), lerp(540, 755, k), lerp(760, 1135, k), lerp(0.9, 0.3, k))
    paste(img, spr(bgp_side), 540, 1130, 0.98, lerp(0.35, 0.72, k))
    if k > 0.98:
        paste(img, glow(220, CY_, 0.45), 755, 1135)
        paste(img, spr(v8_engine), 755, 1135, 0.3, 0.55)
    if k > 0.98:
        callout(img, t, 2.1, 755, 1110, 760, 760, "V8 · 2,4 LITROS", YEL, 38)
    big(t, 0.3, "BRAWN GP", 300, 110, WHITE, pop=False)
    vignette(img, 200)


def sh_livery(img, t, T, L):
    garage_bg(img)
    spotlight(img, t, 540, 0, 1300, 60, 520, 36, dust=True)
    k = ease(clamp((t - 0.4) / 1.6))
    grey = spr(bgp_side, (120, 124, 132), (90, 94, 102), (60, 62, 70))
    paint = spr(bgp_side)
    paste(img, grey, 540, 1100, 0.98)
    if k > 0:
        x_cut = int(paint.size[0] * k)
        part = paint.crop((0, 0, max(1, x_cut), paint.size[1]))
        im = Image.new("RGBA", paint.size, (0, 0, 0, 0))
        im.paste(part, (0, 0))
        paste(img, im, 540, 1100, 0.98)
        sx = 540 - paint.size[0] * 0.98 / 2 + x_cut * 0.98
        if k < 0.99:
            paste(img, glow(120, (255, 255, 255), 0.9), sx, 1100)
            rr = random.Random(int(t * 20))
            d = ImageDraw.Draw(img, "RGBA")
            for i in range(20):
                px, py = sx + rr.uniform(-30, 30), 1000 + rr.uniform(0, 200)
                d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 255, 255, 160))
    d = ImageDraw.Draw(img, "RGBA")
    for i, col in enumerate((WHITE_CAR, CHART, INK)):
        kk = ease(clamp((t - 1.6 - i * 0.35) / 0.35))
        x = 440 + i * 200
        if kk > 0:
            r = 62 * kk
            d.ellipse([x - r, 1420 - r, x + r, 1420 + r], fill=col + (255,), outline=(255, 255, 255, 200), width=4)
    big(t, 0.3, "CASI SIN PATROCINADORES", 300, 60, WHITE, pop=False)
    vignette(img, 190)


def diffuser_scene(img, t, t0, double_k, flow_k):
    """Corte de la parte trasera del suelo: difusor normal y segundo piso, con el aire saliendo."""
    sky(img, (12, 16, 24), (4, 6, 8), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    gy = 1180
    d.rectangle([0, gy, W, H], fill=(54, 54, 60, 255))
    for x in range(0, W, 40):
        d.line([(x, gy + 4), (x + 20, gy + 4)], fill=(80, 80, 88, 255), width=3)
    paste(img, spr(bgp_side), -60, gy - 270, 1.9, 0.35)
    d = ImageDraw.Draw(img, "RGBA")
    # suelo plano y rampa del difusor (piso 1)
    fl_y = gy - 80
    d.polygon([(0, fl_y), (620, fl_y), (980, fl_y - 170), (980, fl_y - 150), (630, fl_y + 18), (0, fl_y + 18)], fill=(40, 42, 50, 255))
    d.line([(0, fl_y), (620, fl_y), (980, fl_y - 170)], fill=(170, 176, 190, 255), width=5)
    # segundo piso
    if double_k > 0:
        A = int(255 * double_k)
        d.polygon([(560, fl_y - 70), (700, fl_y - 70), (980, fl_y - 300), (980, fl_y - 270), (700, fl_y - 50), (560, fl_y - 50)], fill=(60, 62, 72, A))
        d.line([(560, fl_y - 70), (700, fl_y - 70), (980, fl_y - 300)], fill=CHART + (A,), width=6)
    # flujo de aire
    if flow_k > 0:
        rr = random.Random(5)
        for i in range(44):
            u = (t * 0.7 + i / 44) % 1.0
            x = lerp(-40, 1060, u)
            lane = i % 3
            if lane < 2:
                y = fl_y + 40 + lane * 22 if x < 620 else fl_y + 40 + lane * 22 - (x - 620) * (0.47 + 0.08 * lane)
                col = CY_
                a = flow_k
            else:
                if double_k <= 0:
                    continue
                y = fl_y - 60 if x < 700 else fl_y - 60 - (x - 700) * 0.82
                col = CHART
                a = flow_k * double_k
            paste(img, glow(24, col, 1.0), x, y + rr.uniform(-6, 6), 1.0, a)
    callout(img, t, t0 + 0.6, 800, fl_y - 88, 820, 1300, "DIFUSOR", (170, 176, 190), 38)
    if double_k > 0.5:
        callout(img, t, t0 + 1.4, 880, fl_y - 240, 860, 640, "2.º PISO", CHART, 40)


def sh_diffuser(img, t, T, L):
    a1 = L[1][0]
    dk = ease(clamp((t - 1.6) / 0.8))
    diffuser_scene(img, t, 0, dk, ease(clamp((t - 0.4) / 0.8)))
    if t > a1 + 1.2:
        k = ease(clamp((t - a1 - 1.2) / 0.6))
        d = ImageDraw.Draw(img, "RGBA")
        for x in (180, 360, 540):
            y0 = 620
            d.line([(x, y0), (x, y0 + 240 * k)], fill=(255, 120, 80, 255), width=14)
            if k > 0.1:
                d.polygon([(x - 30, y0 + 240 * k - 10), (x + 30, y0 + 240 * k - 10), (x, y0 + 240 * k + 36)], fill=(255, 120, 80, 255))
    if t < a1:
        big(t, 0.3, "EL TRUCO", 290, 110, YEL, pop=False)
    else:
        big(t, a1 + 0.3, "MÁS AGARRE", 290, 104, WHITE)
    vignette(img, 200)


def sh_legal(img, t, T, L):
    sky(img, (30, 24, 20), (8, 6, 6), 1.0)
    spotlight(img, t, 540, 0, 1400, 80, 560, 36, dust=True)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, 1180, W, H], fill=(70, 46, 30, 255))
    for i, (x, y, r) in enumerate(((220, 640, -12), (860, 700, 10), (180, 1000, 8), (900, 1040, -6))):
        k = ease(clamp((t - 0.2 - i * 0.18) / 0.3))
        if k > 0:
            bub = Image.new("RGBA", (300, 150), (0, 0, 0, 0))
            bd = ImageDraw.Draw(bub)
            bd.rounded_rectangle([6, 6, 294, 120], radius=30, fill=(255, 255, 255, 235))
            bd.polygon([(70, 116), (110, 116), (60, 146)], fill=(255, 255, 255, 235))
            bd.text((150, 64), "¡ILEGAL!", font=f(F_CAP, 54), fill=(200, 40, 50), anchor="mm")
            paste(img, bub, x, y, lerp(0.5, 1.0, k), k * (1 - ease(clamp((t - 2.2) / 0.4))), r)
    tg = clamp((t - 2.0) / 0.5)
    ang = 0 if tg <= 0 else -30 * math.sin(min(1.0, tg) * math.pi)
    paste(img, spr(gavel), 540, 1060, 1.0, 1.0, ang)
    if t > 2.25:
        kk = ease(clamp((t - 2.25) / 0.25))
        st = Image.new("RGBA", (640, 220), (0, 0, 0, 0))
        sd = ImageDraw.Draw(st)
        sd.rounded_rectangle([20, 20, 620, 200], radius=18, outline=GREEN + (245,), width=12)
        sd.text((320, 110), "LEGAL", font=f(F_SER, 120), fill=GREEN + (245,), anchor="mm")
        paste(img, st.rotate(-7, expand=True, resample=Image.BICUBIC), 540, 760, lerp(1.5, 1.0, kk), kk)
    date_stamp(t, 0.3, "ABRIL · 2009", 270, hold=T)
    vignette(img, 200)


def sh_australia(img, t, T, L):
    track_bg(img, t, 760, False, 1.3)
    d = ImageDraw.Draw(img, "RGBA")
    for x in range(0, W, 26):
        d.rectangle([x, 760 + 90, x + 18, 760 + 130], fill=((x * 37) % 255, 80, 140, 200))
    # línea de meta
    for i in range(14):
        for j in range(2):
            col = (250, 250, 250, 255) if (i + j) % 2 else (20, 20, 24, 255)
            d.rectangle([840 + j * 22, 920 + i * 22, 862 + j * 22, 942 + i * 22], fill=col)
    k = ease(clamp((t - 0.2) / 1.2))
    paste(img, spr(bgp_side), lerp(-300, 700, k), 760 + 160 + 130, 0.66)
    paste(img, spr(bgp_side), lerp(-700, 260, k), 760 + 160 + 205, 0.58)
    board(img, ease(clamp((t - 1.4) / 0.4)), ["1.º  BUTTON", "2.º  BARRICHELLO"], 1300, 640, cx=620)
    date_stamp(t, 0.3, "AUSTRALIA · MARZO 2009", 260, hold=T)
    vignette(img, 190)


def sh_streak(img, t, T, L):
    sky(img, (20, 24, 34), (6, 8, 12), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    races = ["AUS", "MAL", "CHN", "BHR", "ESP", "MON", "TUR"]
    for i, r in enumerate(races):
        k = ease(clamp((t - 0.3 - i * 0.28) / 0.3))
        if k <= 0:
            continue
        col_i, row = i % 4, i // 4
        x = 180 + col_i * 240 if row == 0 else 300 + col_i * 240
        y = 720 + row * 330
        won = r != "CHN"
        rad = 100 * lerp(0.6, 1.0, k)
        fill = (36, 30, 10, int(240 * k)) if won else (30, 32, 40, int(240 * k))
        out = YEL if won else (130, 136, 150)
        d.ellipse([x - rad, y - rad, x + rad, y + rad], fill=fill, outline=out + (int(255 * k),), width=6)
        d.text((x, y - 18), r, font=f(F_CAP, 46), fill=(255, 255, 255, int(255 * k)), anchor="mm")
        d.text((x, y + 34), "1.º" if won else "3.º", font=f(F_MONO, 38), fill=out + (int(255 * k),), anchor="mm")
        if won and k > 0.9:
            paste(img, glow(90, YEL, 0.25), x, y)
    big(t, 0.3, "IMPARABLE", 290, 110, YEL, pop=False)
    vignette(img, 190)


def sh_cold(img, t, T, L):
    a1 = L[1][0]

    def A(im):
        sky(im, (60, 80, 110), (150, 170, 190), 1.0)
        particles(im, t, 70, 3, (240, 246, 255), 60, (2, 4), 160)
        paste(im, spr(tyre_cold), 420, 980, 1.0)
        paste(im, glow(300, CY_, 0.35), 420, 980)
        lv = 0.15 + 0.05 * math.sin(t * 2)
        paste(im, spr(thermometer, round(lv, 2)), 860, 960, 1.0)
        k = ease(clamp((t - 2.6) / 1.4))
        if k > 0:
            dd = ImageDraw.Draw(im, "RGBA")
            dd.rectangle([0, 1250, W, 1500], fill=(54, 54, 60, int(255 * k)))
            paste(im, spr(bgp_side), 540, 1360, 0.6, k)
            paste(im, spr(bgp_side, NAVY, (230, 40, 50)), lerp(-400, 760, k), 1430, 0.6, k)

    def B(im):
        sky(im, (14, 16, 24), (4, 6, 8), 1.0)
        dd = ImageDraw.Draw(im, "RGBA")
        x0 = 170
        for i, (lbl, pts, col) in enumerate((("BUTTON", 95, YEL), ("VETTEL", 84, (120, 140, 230)))):
            k = ease(clamp((t - a1 - 0.3 - i * 0.3) / 1.0))
            y = 820 + i * 220
            wbar = 700 * pts / 95 * k
            dd.rounded_rectangle([x0, y, x0 + wbar, y + 120], radius=16, fill=col + (255,))
            dd.text((x0, y - 34), lbl, font=f(F_SER, 40), fill=(230, 232, 240), anchor="lm")
            if k > 0.05:
                dd.text((x0 + wbar - 20, y + 60), f"{int(round(pts * k))} PTS", font=f(F_CAP, 54), fill=(16, 16, 20), anchor="rm")
        dd.text((540, 1340), "CLASIFICACIÓN FINAL", font=f(F_SER, 34), fill=(170, 176, 190), anchor="mm")

    xf(img, t, a1, A, B, 0.6)
    if t < a1:
        big(t, 0.3, "EL BAJÓN", 290, 110, CY_, pop=False)
    else:
        big(t, a1 + 0.2, "LA VENTAJA", 290, 104, YEL)
    vignette(img, 190)


def sh_brazil(img, t, T, L):
    track_bg(img, t, 760, False, 1.1)
    d = ImageDraw.Draw(img, "RGBA")
    for x in range(0, W, 26):
        d.rectangle([x, 760 + 90, x + 18, 760 + 130], fill=(40, 140 + (x * 13) % 80, 60, 200))
    paste(img, spr(bgp_side), 540, 760 + 160 + 130, 0.72)
    pos_k = clamp((t - 0.8) / 2.4)
    pos = int(round(lerp(14, 5, ease(pos_k))))
    board(img, ease(clamp((t - 0.5) / 0.4)), [f"POSICIÓN  {pos}.º"], 1300, 560, [YEL], cx=640)
    if t > 3.4:
        confetti(img, t, 3.4)
        top_shade(img, 200)
        big(t, 3.5, "JENSON BUTTON", 290, 96, YEL)
    else:
        date_stamp(t, 0.3, "BRASIL · 18 OCT 2009", 260, hold=2.8)
    vignette(img, 190)


def sh_titles(img, t, T, L):
    sky(img, (30, 26, 20), (8, 8, 6), 1.0)
    paste(img, glow(560, (255, 210, 120), 0.4), 540, 820)
    d = ImageDraw.Draw(img, "RGBA")
    for i, (x, lbl) in enumerate(((400, "PILOTOS"), (790, "CONSTRUCTORES"))):
        k = ease(clamp((t - 0.3 - i * 0.5) / 0.6))
        paste(img, spr(trophy), x, lerp(1020, 880, k), 0.95, k)
        if k > 0.5:
            d.text((x, 1190), lbl, font=f(F_SER, 40), fill=(255, 255, 255, int(255 * k)), anchor="mm")
            d.text((x, 1250), "2009", font=f(F_MONO, 36), fill=YEL + (int(255 * k),), anchor="mm")
    big(t, 1.4, "2 DE 2", 290, 130, YEL)
    vignette(img, 190)


def sh_mercedes(img, t, T, L):
    garage_bg(img)
    spotlight(img, t, 540, 0, 1300, 60, 520, 36, dust=True)
    k = ease(clamp((t - 0.6) / 1.6))
    paste(img, spr(bgp_side), 540, 1100, 0.98, 1.0)
    if k > 0:
        paste(img, spr(bgp_side, SILVER, (40, 200, 190), INK), 540, 1100, 0.98, k)
    d = ImageDraw.Draw(img, "RGBA")
    kk = ease(clamp((t - 2.4) / 0.5))
    if kk > 0:
        d.rounded_rectangle([320, 1300, 960, 1440], radius=24, fill=(10, 12, 18, int(235 * kk)), outline=(40, 200, 190, int(255 * kk)), width=4)
        d.text((640, 1370), "75,1 % DEL EQUIPO", font=f(F_CAP, 60), fill=(255, 255, 255, int(255 * kk)), anchor="mm")
    date_stamp(t, 0.3, "NOVIEMBRE · 2009", 270, hold=T)
    vignette(img, 190)


def sh_eight(img, t, T, L):
    sky(img, (16, 18, 22), (4, 4, 6), 1.0)
    spotlight(img, t, 540, 0, 1400, 80, 700, 26, (220, 230, 240), dust=True)
    d = ImageDraw.Draw(img, "RGBA")
    for i in range(8):
        k = ease(clamp((t - 0.3 - i * 0.22) / 0.3))
        if k <= 0:
            continue
        col_i, row = i % 4, i // 4
        x = 165 + col_i * 250
        y = 700 + row * 360
        paste(img, spr(trophy), x, lerp(y + 60, y, k), 0.5, k)
        d.text((x, y + 170), str(2014 + i), font=f(F_MONO, 38), fill=(230, 236, 244, int(255 * k)), anchor="mm")
    big(t, 0.3, "2014 – 2021", 290, 100, (190, 200, 214), pop=False)
    vignette(img, 190)


def sh_final(img, t, T, L):
    """Reflexión: el coche blanco se va volviendo plateado (Brawn → Mercedes) mientras sale la frase."""
    a, b = L[0]
    sky(img, (8, 8, 12), (2, 2, 4), 1.0)
    spotlight(img, t, 540, 0, 1300, 60, 420, 34, dust=True)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, 1200, W, H], fill=(30, 30, 34, 255))
    paste(img, spr(bgp_side), 540, 1100, 0.95)
    m = ease(clamp((t - a - (b - a) * 0.35) / ((b - a) * 0.6)))
    if m > 0:
        paste(img, spr(bgp_side, SILVER, (40, 200, 190), INK), 540, 1100, 0.95, m)
    paste(img, glow(420, (255, 255, 230), 0.22 + 0.12 * m), 540, 1040)
    top_shade(img)
    big(t, a + (b - a) * 0.42, "LO QUE PARECE UN FINAL", 250, 56, WHITE, pop=False)
    big(t, a + (b - a) * 0.70, "ES SOLO EL PRINCIPIO", 330, 76, YEL)
    vignette(img, 190)


FNS = {k: globals()["sh_" + k] for k, *_ in SHOTS}
AUDIO = {
    "music": [("open", "epic"), ("honda", "mystery"), ("pound", "creative"), ("diffuser", "exp"), ("australia", "epic"),
              ("cold", "tension"), ("brazil", "epic"), ("mercedes", "premium"), ("final", "premium")],
    "gains": {"exp": 0.7, "mystery": 0.8},
    "amb": {"road": ["open", "australia", "brazil"], "hum": ["engine", "livery", "diffuser", "mercedes"], "room": ["honda", "pound", "legal", "titles"],
            "wind": ["cold"], "crowd": ["streak", "eight", "final"]},
    "sfx": [("open+0.2", "whoosh", 0.12), ("honda+0.3", "paper", 0.15), ("honda+3.2", "rumble", 0.12),
            ("pound+0.3", "ding", 0.1), ("pound+0.6", "whoosh_up", 0.1),
            ("engine+0.6", "whoosh", 0.1), ("engine+1.8", "thud", 0.2), ("livery+0.4", "whoosh_up", 0.1),
            ("diffuser+0.5", "swell", 0.1), ("diffuser+1.6", "click", 0.2), ("diffuser@L1+1.2", "thud", 0.22),
            ("legal+0.2", "pop", 0.12), ("legal+2.25", "gavel", 0.4),
            ("australia+0.2", "whoosh", 0.14), ("australia+1.4", "ding", 0.08),
            ("streak+0.3", "pop", 0.1), ("streak+1.2", "pop", 0.1), ("streak+2.1", "pop", 0.1),
            ("cold+0.3", "swell", 0.08), ("cold+2.6", "whoosh", 0.12), ("cold@L1+0.3", "draw", 0.12),
            ("brazil+0.5", "blip_down", 0.1), ("brazil+3.4", "swell", 0.16),
            ("titles+0.3", "chime", 0.06), ("titles+1.4", "swell", 0.12), ("mercedes+0.6", "whoosh_up", 0.1),
            ("eight+0.3", "pop", 0.1), ("final+0.4", "swell", 0.14)],
    "bed": [("diffuser", "cold")],
    "bpm": 104,
}
