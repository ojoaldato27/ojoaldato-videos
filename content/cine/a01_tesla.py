"""⚡ A1 · Tesla Roadster (presentado el 15/10/2026 en la base de SpaceX de McGregor, Texas): el coche que sube boca abajo
por una rampa y salta por encima de otros coches. Estilo «docu» con ritmo rápido y la voz del canal.
Datos: The Next Web y Electrek (15-16/10/2026); el Brabham BT46B, del vídeo t11 (ya verificado)."""
import os
from gadgets import *
import docu as DC
import t12_brawn_v2 as B2
import t11_f1_ventilador as T11

GOLD, CREAM, CY_ = DC.GOLD, DC.CREAM, (110, 210, 255)
RED_T = (206, 24, 36)
REDC = (232, 70, 70)
GREENC = (90, 220, 140)
STEEL = (196, 202, 212)

STYLE = "docu"
BEATS = True
XF = 0.28
TITLE = "El_Tesla_que_salta_por_encima_de_los_coches"
_VZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voz", "a01_tesla")
VOICE = next((_VZ + e for e in (".mp3", ".m4a", ".wav") if os.path.exists(_VZ + e)), _VZ + ".mp3")
LINES = [
    "Tesla acaba de presentar un coche que sube por una rampa, se pone *boca abajo*… y salta por encima de otros coches.",
    "¿Cómo puede hacer eso un coche… y *cuándo* podrás tenerlo?",
    "Es el nuevo *Tesla Roadster*, presentado el 15 de octubre en una base de *SpaceX* en Texas.",
    "Primer truco: unos *ventiladores* que chupan el aire de debajo del coche…",
    "Y lo pegan al suelo con tanta fuerza que puede ir *boca abajo*.",
    "La Fórmula 1 ya lo probó en 1978: el Brabham «ventilador» ganó su única carrera… y después se *prohibió*.",
    "Segundo truco: *propulsores de gas frío*, diseñados con ingenieros de SpaceX.",
    "Diez toberas sueltan aire comprimido de unos tanques de *600 litros*: así salta, gira y aterriza.",
    "Sin fuego ni explosiones: es el mismo principio que usan algunos *cohetes* para orientarse.",
    "Según Tesla, acelera de 0 a 97 km/h en *0,81 segundos*… aunque nadie lo ha comprobado.",
    "Habrá tres versiones; la más extrema, *Rocket*, tiene un asiento y no puede ir por la calle.",
    "¿Y cuándo llega? Musk dice que en *2028*.",
    "Pero este coche se enseñó por primera vez en *2017*… y tenía que llegar en 2020.",
    "Y ha perdido cosas: de 4 plazas a *2*, y de 1.000 km de autonomía prometidos… a poco más de *480*.",
    "Para reservarlo hay que adelantar *50.000 dólares*… y todavía no tiene precio.",
    "A veces el futuro llega volando… y otras veces, simplemente, *llega tarde*.",
]
OUTRO_LINE = "Si no lo sabías… ahora ya lo sabes. Dale a like y sígueme para más."
SHOTS = [("open", 0, 0, 0), ("question", 1, 1, 0), ("present", 2, 2, 0), ("fans", 3, 3, 0), ("upside", 4, 4, 0),
         ("brabham", 5, 5, 0), ("thrusters", 6, 6, 0), ("tanks", 7, 7, 0), ("space", 8, 8, 0), ("accel", 9, 9, 0),
         ("versions", 10, 10, 0), ("y2028", 11, 11, 0), ("delays", 12, 12, 0), ("lost", 13, 13, 0), ("money", 14, 14, 0),
         ("final", 15, 15, 0)]
FOCUS = {}
NOTIF = ("accel", 1.8)           # banner de seguir hacia la mitad (~47 s), pedido por Iker
FOLLOW = None
NOTIF_TEXT = "Suscríbete para más cosas que no sabías"
HEAD = {
    0: ("Boca abajo", "EL NUEVO TESLA ROADSTER"),
    1: ("¿Cómo lo hace?", "Y CUÁNDO PODRÁS TENERLO"),
    2: ("Tesla Roadster", "15 DE OCTUBRE · BASE DE SPACEX"),
    3: ("Truco 1", "VENTILADORES DE SUCCIÓN"),
    4: ("Pegado al techo", "TANTA FUERZA QUE VA BOCA ABAJO"),
    5: ("Ya pasó en la F1", "BRABHAM BT46B · 1978"),
    6: ("Truco 2", "PROPULSORES DE GAS FRÍO"),
    7: ("600 litros", "DE AIRE COMPRIMIDO"),
    8: ("Como un cohete", "SIN FUEGO NI EXPLOSIONES"),
    9: ("0,81 segundos", "DE 0 A 97 KM/H, SEGÚN TESLA"),
    10: ("3 versiones", "PERFORMANCE · THRUST · ROCKET"),
    11: ("2028", "CUÁNDO LLEGA, SEGÚN MUSK"),
    12: ("8 años tarde", "SE ENSEÑÓ EN 2017"),
    13: ("Menos de lo prometido", "PLAZAS Y AUTONOMÍA"),
    14: ("50.000 $", "SOLO PARA RESERVARLO"),
    15: ("El futuro", "A VECES LLEGA VOLANDO… Y A VECES, TARDE"),
}
NARRATOR = {"open": None, "question": None, "present": ("point", "left"), "fans": ("point", "left"),
            "upside": None, "brabham": ("smirk", "left"), "thrusters": ("point", "left"), "tanks": None,
            "space": ("think", "left"), "accel": ("surprise", "left"), "versions": None, "y2028": ("think", "left"),
            "delays": ("smirk", "left"), "lost": None, "money": ("surprise", "left"), "final": ("think", "left")}
NARRATOR_POS = {"left": (138, 1446), "right": (940, 1446)}
NARRATOR_SCALE = 0.55
PUSH = {"open": (540, 900), "question": (540, 860), "present": (540, 900), "fans": (540, 960), "upside": (540, 760),
        "brabham": (540, 920), "thrusters": (540, 920), "tanks": (560, 880), "space": (540, 840), "accel": (540, 860),
        "versions": (540, 860), "y2028": (540, 860), "delays": (540, 880), "lost": (540, 860), "money": (540, 880),
        "final": (540, 860)}


def lt(L, i, fr=0.0):
    i = min(i, len(L) - 1)
    a, b = L[i]
    return a + (b - a) * fr


# ------------------------------------------------------------------ dibujos
def roadster(body=RED_T, glass=(22, 26, 38)):
    """Tesla Roadster de lado: bajo, morro largo y liso, techo de cristal, sin parrilla."""
    c = Cv(1000, 330)
    c.shadow((30, 278, 970, 326), 160, 12)
    hi, lo = shade(body, 1.18), shade(body, 0.55)
    c.poly([(30, 236), (70, 206), (190, 184), (330, 172), (420, 120), (520, 96), (640, 96), (740, 128), (850, 172),
            (950, 196), (975, 232), (962, 262), (40, 262)], grad=(hi, lo), power=0.9)
    c.poly([(440, 124), (525, 104), (640, 104), (726, 134), (700, 168), (452, 170)], grad=(shade(glass, 1.8), glass))
    c.line([(560, 104), (556, 168)], shade(body, 0.7) + (255,), 6)
    c.line([(80, 214), (330, 182), (470, 176)], (255, 255, 255, 110), 3)
    c.rect((30, 250, 975, 262), fill=(18, 18, 22, 255), r=4)
    c.poly([(36, 228), (90, 214), (96, 224), (40, 238)], fill=(255, 245, 230, 230))
    c.poly([(930, 204), (968, 212), (970, 224), (934, 220)], fill=(255, 60, 60, 240))
    for wx, r in ((208, 58), (790, 60)):
        c.ellipse((wx - r, 262 - r, wx + r, 262 + r), radial=((46, 46, 50), (10, 10, 12)), power=1.3)
        c.ellipse((wx - r * 0.6, 262 - r * 0.6, wx + r * 0.6, 262 + r * 0.6), radial=((210, 214, 222), (80, 84, 92)), center=(0.4, 0.35))
        for k in range(5):
            a = k * 2 * math.pi / 5
            c.line([(wx, 262), (wx + math.cos(a) * r * 0.55, 262 + math.sin(a) * r * 0.55)], (60, 62, 70), 6)
        c.ellipse((wx - r * 0.16, 262 - r * 0.16, wx + r * 0.16, 262 + r * 0.16), fill=(36, 38, 44))
    return c.done()


def ghost_roadster():
    return roadster((70, 78, 108), (40, 46, 70))


def car_sil(w=300, h=110, col=(58, 66, 96)):
    c = Cv(w, h)
    c.poly([(6, h - 24), (30, h - 54), (w * 0.3, h - 64), (w * 0.42, 14), (w * 0.72, 14), (w * 0.84, h - 60), (w - 8, h - 50),
            (w - 4, h - 24)], fill=col + (255,))
    for wx in (w * 0.22, w * 0.78):
        c.ellipse((wx - 22, h - 46, wx + 22, h - 2), fill=(20, 22, 30))
    return c.done()


def semi_sil(col=(58, 66, 96)):
    c = Cv(420, 200)
    c.rect((6, 40, 300, 160), fill=col + (255,), r=10)
    c.poly([(300, 70), (360, 70), (412, 120), (412, 160), (300, 160)], fill=shade(col, 1.15) + (255,))
    c.poly([(330, 80), (360, 80), (396, 118), (330, 118)], fill=(22, 26, 38))
    for wx in (60, 130, 360):
        c.ellipse((wx - 26, 140, wx + 26, 192), fill=(20, 22, 30))
    return c.done()


def puff(img, x, y, ang, k, size=60, n=7, seed=1):
    """Chorro de gas frío (blanco azulado) saliendo hacia el ángulo dado."""
    if k <= 0:
        return
    rr = random.Random(seed)
    for i in range(n):
        u = (i + 1) / n
        d = size * 2.2 * u
        px = x + math.cos(ang) * d + rr.uniform(-8, 8)
        py = y + math.sin(ang) * d + rr.uniform(-8, 8)
        DC.glow_at(img, px, py, int(size * (0.35 + 0.65 * u)), (225, 238, 255), 0.55 * k * (1 - u * 0.6))


def rocket_sil():
    c = Cv(220, 900)
    c.poly([(110, 0), (176, 120), (176, 820), (44, 820), (44, 120)], grad=((220, 224, 232), (120, 126, 140)), horizontal=True)
    c.poly([(44, 700), (0, 860), (44, 820)], fill=(150, 156, 170, 255))
    c.poly([(176, 700), (220, 860), (176, 820)], fill=(150, 156, 170, 255))
    c.rect((60, 820, 160, 880), fill=(60, 64, 74), r=6)
    return c.done()


def sat_sil():
    c = Cv(520, 260)
    c.rect((200, 70, 320, 190), grad=((220, 200, 120), (160, 130, 60)), r=10)
    for x0 in (10, 340):
        c.rect((x0, 100, x0 + 170, 160), grad=((60, 90, 160), (30, 50, 110)), r=4)
        for k in range(1, 6):
            c.line([(x0 + k * 28, 100), (x0 + k * 28, 160)], (90, 120, 190), 2)
    c.line([(180, 130), (200, 130)], (180, 184, 194), 6)
    c.line([(320, 130), (340, 130)], (180, 184, 194), 6)
    return c.done()


def tank(level=1.0):
    c = Cv(260, 520)
    c.rect((30, 30, 230, 490), grad=((210, 214, 224), (110, 116, 130)), horizontal=True, r=100)
    c.rect((60, 490 - 400 * level, 200, 470), fill=CY_ + (150,), r=50)
    c.rect((105, 0, 155, 40), fill=(80, 84, 94), r=8)
    return c.done()


def stopwatch():
    c = Cv(420, 480)
    c.rect((185, 10, 235, 60), fill=(170, 176, 190), r=8)
    c.ellipse((20, 60, 400, 440), radial=((250, 250, 252), (200, 204, 214)), center=(0.4, 0.35))
    c.ellipse((44, 84, 376, 416), fill=(20, 24, 40))
    for k in range(60):
        a = k * math.pi / 30
        r0 = 150 if k % 5 else 136
        c.line([(210 + math.cos(a) * r0, 250 + math.sin(a) * r0), (210 + math.cos(a) * 160, 250 + math.sin(a) * 160)], (200, 206, 220), 3)
    return c.done()


def dollars():
    c = Cv(520, 360)
    for i in range(6):
        y = 300 - i * 38
        c.rect((40 + i * 6, y - 60, 480 + i * 6, y), grad=((120, 190, 120), (60, 120, 70)), r=8)
        c.rect((60 + i * 6, y - 48, 460 + i * 6, y - 12), fill=(150, 210, 150, 120), r=6)
    c.text((260 + 30, 132), "$", 90, (30, 70, 40), font=F_SER)
    return c.done()


def ramp(img, k=1.0, cx=600, cy=900, r=330, col=(70, 80, 110)):
    """Rampa curva (cuarto de tubo) que termina en horizontal arriba: por ahí sube boca abajo."""
    d = ImageDraw.Draw(img, "RGBA")
    pts = [(cx + math.cos(a) * r, cy + math.sin(a) * r) for a in [math.pi / 2 - i * math.pi / 40 for i in range(41)]]
    d.line(pts, fill=col + (int(255 * k),), width=26, joint="curve")
    d.line(pts, fill=(140, 150, 180, int(200 * k)), width=4, joint="curve")
    d.line([(cx - 600, cy + r), (cx, cy + r)], fill=col + (int(255 * k),), width=26)


# ------------------------------------------------------------------ planos
def sh_open(img, t, T, L):
    DC.bg(img, t, 560, 860)
    cx, cy, r = 640, 860, 300
    ramp(img, 1.0, cx, cy, r)
    u = clamp(t / max(1.0, T * 0.55))
    u = ease(u)
    if u < 1:
        if u < 0.35:     # se acerca por el suelo
            x = lerp(-200, cx, u / 0.35)
            y, rot = cy + r - 62, 0
        else:            # sube por la rampa hasta ponerse boca abajo
            a = math.pi / 2 - (u - 0.35) / 0.65 * math.pi
            x = cx + math.cos(a) * (r - 62)
            y = cy + math.sin(a) * (r - 62)
            rot = -math.degrees(math.pi / 2 - a)
        paste(img, spr(roadster), x, y, 0.42, 1.0, rot)
    else:                # salta por encima de los coches y aterriza
        v = clamp((t - T * 0.55) / max(0.8, T * 0.45))
        x = lerp(cx, -60, v)
        y = cy - r + 60 + (math.sin(v * math.pi) * -160) + v * (2 * r - 120)
        rot = 180 - 180 * ease(clamp(v * 1.6))
        for i, xx in enumerate((150, 330, 520)):
            paste(img, spr(car_sil), xx, cy + r - 50, 0.8)
        paste(img, spr(roadster), x, y, 0.42, 1.0, rot)
        puff(img, x + 60, y + 30, math.pi * 0.5, 1 - v, 40, 6, int(t * 7))
    DC.pill(img, 620, 1240, "BASE DE SPACEX · TEXAS", ease(clamp((t - 0.5) / 0.4)))


def sh_question(img, t, T, L):
    DC.bg(img, t, 540, 880, seed=4)
    DC.glow_at(img, 540, 920, 460, (255, 214, 150), 0.12)
    paste(img, spr(ghost_roadster), 540, 960, 0.8, 1.0)
    DC.dotted(img, (160, 1040), (540, 520), (920, 1040), ease(clamp((t - 0.1) / 1.4)))
    DC.stamp_text(img, 540, 660, "?", 240, GOLD, ease(clamp((t - 0.3) / 0.4)))


def sh_present(img, t, T, L):
    DC.bg(img, t, 540, 900, seed=6)
    paste(img, spr(rocket_sil), 880, 760, 0.62, 0.35)
    DC.glow_at(img, 540, 960, 480, (255, 120, 120), 0.14)
    k = ease(clamp((t - 0.05) / 0.9))
    d = ImageDraw.Draw(img, "RGBA")
    d.ellipse([140, 1040, 940, 1090], fill=(0, 0, 0, 100))
    paste(img, spr(roadster), lerp(380, 540, k), 960, 0.82, k)
    DC.pill(img, 610, 1180, "15 DE OCTUBRE DE 2026", ease(clamp((t - 0.7) / 0.4)))
    DC.pill(img, 610, 1250, "McGREGOR, TEXAS", ease(clamp((t - 1.3) / 0.4)), col=GOLD)


def _fans_under(img, t, cx, cy, s, k):
    """Coche en corte con dos ventiladores bajo el suelo chupando aire."""
    paste(img, spr(roadster), cx, cy, s)
    for fx in (-150, 150):
        T11.fan_blades(img, cx + fx * s / 0.8, cy + 70 * s / 0.8, int(46 * s / 0.8), t, 14, (190, 196, 210))
    if k > 0:
        rr = random.Random(3)
        for i in range(36):
            u = (t * 0.9 + i / 36) % 1.0
            side = -1 if i % 2 else 1
            x = cx + side * lerp(380, 60, u) * s / 0.8
            y = cy + (120 - 40 * u) * s / 0.8 + rr.uniform(-6, 6)
            DC.glow_at(img, x, y, 12, CY_, 0.9 * k)


def sh_fans(img, t, T, L):
    DC.bg(img, t, 540, 960, seed=8)
    _fans_under(img, t, 540, 960, 0.8, ease(clamp((t - 0.4) / 0.5)))
    d = ImageDraw.Draw(img, "RGBA")
    d.line([(80, 1080), (1000, 1080)], fill=(120, 128, 150, 200), width=4)
    DC.pill(img, 620, 1210, "CHUPAN EL AIRE DE DEBAJO", ease(clamp((t - 0.8) / 0.4)))


def sh_upside(img, t, T, L):
    DC.bg(img, t, 540, 760, seed=10)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, 520, W, 548], fill=(70, 80, 110, 255))
    d.line([(0, 548), (W, 548)], fill=(140, 150, 180, 255), width=4)
    k = ease(clamp(t / 0.8))
    car = spr(roadster).rotate(180, expand=True)
    paste(img, car, lerp(1300, 540, k), 548 + 120, 0.8)
    for x in (300, 540, 780):
        q = ease(clamp((t - 0.6) / 0.5))
        d.line([(x, 860), (x, 860 - 150 * q)], fill=GOLD + (230,), width=10)
        if q > 0.1:
            yy = 860 - 150 * q
            d.polygon([(x - 22, yy + 6), (x + 22, yy + 6), (x, yy - 26)], fill=GOLD + (230,))
    DC.pill(img, 540, 1000, "LA SUCCIÓN LO SUJETA", ease(clamp((t - 1.0) / 0.4)))


def sh_brabham(img, t, T, L):
    DC.bg(img, t, 540, 920, seed=12)
    DC.glow_at(img, 540, 940, 440, (255, 140, 120), 0.12)
    k = ease(clamp(t / 0.7))
    paste(img, spr(T11.f1_side), lerp(-300, 540, k), 940, 0.85)
    T11.fan_blades(img, 540 + 400 * 0.85 + lerp(-840, 0, k), 940 - 10, 34, t, 14)
    DC.pill(img, 540, 1110, "1 CARRERA · 1 VICTORIA", ease(clamp((t - lt(L, 0, 0.45)) / 0.4)), col=GOLD)
    kk = ease(clamp((t - lt(L, 0, 0.8)) / 0.25))
    if kk > 0:
        st = Image.new("RGBA", (680, 200), (0, 0, 0, 0))
        sd = ImageDraw.Draw(st)
        sd.rounded_rectangle([20, 20, 660, 180], radius=18, outline=REDC + (240,), width=10)
        sd.text((340, 102), "PROHIBIDO", font=DC.caps_font(100, "ExtraBold"), fill=REDC + (240,), anchor="mm")
        paste(img, st.rotate(-8, expand=True, resample=Image.BICUBIC), 540, 720, lerp(1.4, 0.85, kk), kk)


NOZZ = [(-430, -10), (-300, -70), (-120, -110), (60, -112), (240, -80), (400, -20), (440, 40), (-440, 50), (-200, 60), (200, 60)]


def sh_thrusters(img, t, T, L):
    DC.bg(img, t, 540, 920, seed=14)
    paste(img, spr(roadster), 540, 920, 0.86)
    for i, (dx, dy) in enumerate(NOZZ):
        kk = ease(clamp((t - 0.3 - i * 0.12) / 0.25))
        if kk <= 0:
            continue
        x, y = 540 + dx * 0.86, 920 + dy * 0.86
        d = ImageDraw.Draw(img, "RGBA")
        d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=GOLD + (int(255 * kk),))
        ang = math.atan2(dy, dx)
        on = 0.5 + 0.5 * math.sin(t * 9 + i)
        puff(img, x, y, ang, kk * on, 34, 5, i)
    DC.pill(img, 620, 1170, "10 TOBERAS · AIRE A PRESIÓN", ease(clamp((t - 1.4) / 0.4)))


def sh_tanks(img, t, T, L):
    DC.bg(img, t, 560, 880, seed=16)
    lvl = 1.0 - 0.6 * clamp((t - lt(L, 0, 0.5)) / 2.0)
    paste(img, spr(tank, round(lvl, 2)), 260, 860, 0.9)
    DC.stamp_text(img, 260, 560, "600 L", 70, CY_, ease(clamp((t - 0.3) / 0.4)), glow=False)
    v = clamp((t - lt(L, 0, 0.45)) / 2.2)
    y = 980 - math.sin(v * math.pi) * 300
    rot = 360 * ease(v)
    paste(img, spr(roadster), 720, y, 0.45, 1.0, rot)
    if 0 < v < 1:
        puff(img, 720, y + 40, math.pi / 2, 1.0, 40, 6, int(t * 9))
    d = ImageDraw.Draw(img, "RGBA")
    d.line([(520, 1060), (1020, 1060)], fill=(120, 128, 150, 200), width=4)


def sh_space(img, t, T, L):
    DC.bg(img, t, 540, 840, dust_n=140, seed=18)
    rot = 25 * math.sin(t * 0.9)
    paste(img, spr(sat_sil), 560, 840, 1.1, 1.0, rot)
    side = 1 if math.sin(t * 0.9 + 1.2) > 0 else -1
    puff(img, 560 + side * 300, 840, 0 if side > 0 else math.pi, 0.8, 40, 6, int(t * 5))
    DC.pill(img, 610, 1120, "GAS A PRESIÓN, SIN COMBUSTIÓN", ease(clamp((t - 0.6) / 0.4)))


def sh_accel(img, t, T, L):
    DC.bg(img, t, 540, 860, seed=20)
    paste(img, spr(stopwatch), 540, 860, 1.0)
    run = clamp((t - 0.3) / 0.81)
    a = -math.pi / 2 + run * 2 * math.pi * 0.81
    d = ImageDraw.Draw(img, "RGBA")
    d.line([(540, 870), (540 + math.cos(a) * 140, 870 + math.sin(a) * 140)], fill=GOLD + (255,), width=8)
    d.ellipse([528, 858, 552, 882], fill=GOLD + (255,))
    DC.stamp_text(img, 540, 900, f"{0.81 * run:.2f} s".replace(".", ","), 64, CREAM, 1.0, glow=False)
    DC.pill(img, 620, 1170, "0 → 97 KM/H", ease(clamp((t - 0.8) / 0.4)), col=GOLD)
    DC.pill(img, 620, 1240, "SIN COMPROBAR", ease(clamp((t - lt(L, 0, 0.6)) / 0.4)), col=(255, 160, 150))


def sh_versions(img, t, T, L):
    DC.bg(img, t, 540, 860, seed=22)
    d = ImageDraw.Draw(img, "RGBA")
    cards = [("PERFORMANCE", "2 PLAZAS", "< 1,6 s"), ("THRUST", "2 PLAZAS", "< 0,9 s"), ("ROCKET", "1 PLAZA", "< 0,59 s")]
    for i, (nm, seats, acc) in enumerate(cards):
        k = ease(clamp((t - 0.2 - i * 0.35) / 0.35))
        if k <= 0:
            continue
        x, y = 240 + i * 300, 860
        hi = i == 2 and t > lt(L, 0, 0.45)
        col = GOLD if hi else (120, 128, 150)
        d.rounded_rectangle([x - 115, y - 210 + (1 - k) * 40, x + 115, y + 210 + (1 - k) * 40], radius=24,
                            fill=(20, 26, 48, int(235 * k)), outline=col + (int(255 * k),), width=5 if hi else 3)
        d.text((x, y - 140), nm, font=DC.caps_font(26, "ExtraBold"), fill=(246, 246, 250, int(255 * k)), anchor="mm")
        d.text((x, y - 40), acc, font=DC.title_font(56), fill=(GOLD if hi else CREAM) + (int(255 * k),), anchor="mm")
        d.text((x, y + 60), seats, font=DC.font(DC.F_UI, 26), fill=(200, 205, 220, int(255 * k)), anchor="mm")
        if i == 2:
            d.text((x, y + 130), "NO APTO", font=DC.font(DC.F_UI_B, 26), fill=REDC + (int(255 * k),), anchor="mm")
            d.text((x, y + 166), "PARA LA CALLE", font=DC.font(DC.F_UI_B, 26), fill=REDC + (int(255 * k),), anchor="mm")
    DC.pill(img, 540, 1180, "0 → 97 KM/H, SEGÚN TESLA", ease(clamp((t - 1.4) / 0.4)))


def sh_y2028(img, t, T, L):
    DC.bg(img, t, 540, 860, seed=24)
    DC.glow_at(img, 540, 840, 420, (255, 210, 120), 0.22)
    k28 = ease(clamp((t - lt(L, 0, 0.5)) / 0.4))
    if k28 < 1:
        DC.stamp_text(img, 540, 840, "¿?", 200, CREAM, ease(clamp(t / 0.3)) * (1 - k28) * (0.75 + 0.25 * math.sin(t * 6)))
    DC.stamp_text(img, 540, 840, "2028", 230, GOLD, k28)
    DC.pill(img, 610, 1060, "INICIO DE LA PRODUCCIÓN", ease(clamp((t - lt(L, 0, 0.6)) / 0.4)))


def sh_delays(img, t, T, L):
    DC.bg(img, t, 540, 880, seed=26)
    d = ImageDraw.Draw(img, "RGBA")
    pts = [(200, "2017", "SE ENSEÑA"), (540, "2020", "IBA A LLEGAR"), (880, "2028", "AHORA")]
    k = ease(clamp(t / 1.6))
    d.line([(160, 880), (160 + 760 * k, 880)], fill=(140, 150, 180, 255), width=6)
    for i, (x, yr, lb) in enumerate(pts):
        kk = ease(clamp((t - 0.2 - i * 0.6) / 0.3))
        if kk <= 0:
            continue
        col = GOLD if i == 2 else CREAM
        d.ellipse([x - 18, 862, x + 18, 898], fill=col + (int(255 * kk),))
        d.text((x, 800), yr, font=DC.title_font(70), fill=col + (int(255 * kk),), anchor="mm")
        d.text((x, 950), lb, font=DC.font(DC.F_UI, 24), fill=(200, 205, 220, int(255 * kk)), anchor="mm")
        if i == 1 and t > lt(L, 0, 0.75):
            q = ease(clamp((t - lt(L, 0, 0.75)) / 0.25))
            d.line([(x - 80, 830), (x - 80 + 160 * q, 770)], fill=REDC + (255,), width=10)
    DC.pill(img, 610, 1080, "LA FECHA SE HA RETRASADO VARIAS VECES", ease(clamp((t - lt(L, 0, 0.85)) / 0.3)))


def sh_lost(img, t, T, L):
    DC.bg(img, t, 540, 860, seed=28)
    d = ImageDraw.Draw(img, "RGBA")
    BW = 560
    rows = [("PLAZAS", 4, 2, 4, "", 0.0), ("AUTONOMÍA", 1000, 480, 1000, " km", 0.45)]
    for i, (lbl, a, b, mx, unit, fr) in enumerate(rows):
        k = ease(clamp((t - lt(L, 0, fr)) / 0.5))
        if k <= 0:
            continue
        y = 700 + i * 300
        d.text((170, y - 60), lbl, font=DC.font(DC.F_UI, 30), fill=(220, 224, 236, int(255 * k)), anchor="lm")
        d.rounded_rectangle([170, y, 170 + BW * a / mx, y + 70], radius=14, fill=(70, 78, 108, int(255 * k)))
        q = ease(clamp((t - lt(L, 0, fr) - 0.6) / 0.6))
        w2 = BW * lerp(a, b, q) / mx
        d.rounded_rectangle([170, y, 170 + w2, y + 70], radius=14, fill=GOLD + (int(255 * k),))
        txt = f"{int(round(lerp(a, b, q))):,}".replace(",", ".") + unit
        d.text((170 + w2 + 20, y + 36), txt, font=DC.caps_font(44, "Bold"), fill=(246, 246, 250, int(255 * k)), anchor="lm")
        d.text((170 + BW, y - 60), f"PROMETIDO: {a:,}".replace(",", ".") + unit, font=DC.font(DC.F_UI, 22),
               fill=(160, 166, 186, int(255 * k)), anchor="rm")


def sh_money(img, t, T, L):
    DC.bg(img, t, 540, 880, seed=30)
    k = ease(clamp((t - 0.1) / 0.6))
    paste(img, spr(dollars), 560, lerp(980, 900, k), 1.0, k)
    DC.stamp_text(img, 560, 640, "50.000 $", 120, GOLD, ease(clamp((t - 0.4) / 0.4)))
    DC.pill(img, 610, 1150, "PRECIO FINAL: SIN ANUNCIAR", ease(clamp((t - lt(L, 0, 0.6)) / 0.4)), col=(255, 160, 150))


def sh_final(img, t, T, L):
    DC.bg(img, t, 560, 900, seed=32)
    a, b = L[0]
    DC.glow_at(img, 560, 1000, 520, (255, 200, 140), 0.22)
    v = clamp(t / max(1.0, b))
    x = lerp(-160, 600, ease(v))
    y = 900 - math.sin(v * math.pi) * 120
    paste(img, spr(roadster), x, y, 0.62, 1.0, -6 * math.sin(v * math.pi))
    if v < 1:
        puff(img, x - 150, y + 40, math.pi * 0.85, 1 - v, 36, 6, int(t * 7))


FNS = {k: globals()["sh_" + k] for k, *_ in SHOTS}
AUDIO = {
    "music": [("open", "epic"), ("present", "premium"), ("fans", "exp"), ("brabham", "creative"), ("thrusters", "exp"),
              ("accel", "epic"), ("delays", "tension"), ("final", "premium")],
    "gains": {"exp": 0.6, "epic": 0.8, "tension": 0.75},
    "amb": {"hum": ["fans", "thrusters", "tanks"], "space": ["space"], "crowd": ["present"]},
    "sfx": [("open+0.2", "whoosh", 0.08), ("open+2.2", "whoosh_up", 0.07), ("question+0.3", "swell", 0.06),
            ("present+0.4", "whoosh", 0.07), ("fans+0.4", "swell", 0.06), ("upside+0.2", "whoosh", 0.07),
            ("brabham+0.2", "whoosh", 0.08), ("thrusters+0.3", "swell", 0.06), ("tanks+0.6", "whoosh_up", 0.07),
            ("accel+0.3", "tick", 0.06), ("versions+0.2", "pop", 0.06), ("y2028+0.4", "ding", 0.06),
            ("delays+0.3", "pop", 0.06), ("money+0.4", "chime", 0.05), ("final+0.4", "swell", 0.1)],
    "bed": [],
    "bpm": 100,
}
