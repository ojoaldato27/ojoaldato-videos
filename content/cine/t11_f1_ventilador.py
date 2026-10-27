"""T11 · El F1 con ventilador (Brabham BT46B, 1978) — estilo microondas: objetos detallados, cortes y etiquetas."""
from gadgets import *
import t02_microondas as T2
import t04_qr as T4
import t06_nevera as T6

xf, callout, glow_line, top_shade, check, heat_arrows, sepia = T2.xf, T2.callout, T2.glow_line, T2.top_shade, T4.check, T6.heat_arrows, T2.sepia

TITLE = "El_F1_que_tuvieron_que_quitar"
LINES = [
    "En 1978, un Fórmula 1 ganó su primera carrera… y *nunca más corrió* en el Mundial.",
    "¿Qué escondía en la parte de atrás… y por qué lo *quitaron*?",
    "Era el *Brabham BT46B*, y detrás llevaba un *ventilador gigante*.",
    "Oficialmente, servía para *refrigerar el motor*.",
    "Pero en realidad hacía otra cosa: *chupaba el aire* de debajo del coche.",
    "Unas faldillas a los lados *sellaban* el hueco con el suelo.",
    "Y si debajo hay *menos presión* que encima, el aire empuja el coche contra el asfalto.",
    "Como una *ventosa*.",
    "Los alerones también pegan el coche al suelo… pero necesitan *velocidad*.",
    "En las curvas lentas, *pierden fuerza*.",
    "El ventilador iba conectado al motor: succionaba *aunque el coche fuera despacio*.",
    "Es como una *cometa*, que necesita viento… frente a una *aspiradora*, que solo hay que encender.",
    "Debutó en el Gran Premio de Suecia, con *Niki Lauda* al volante.",
    "Y ganó con *más de medio minuto* de ventaja.",
    "Los rivales protestaron: decían que *lanzaba suciedad y piedras* a los de detrás.",
    "El jefe del equipo, *Bernie Ecclestone*, acabó retirándolo… y luego se *prohibieron* los coches con ventilador.",
    "Una carrera, una victoria: *un 100 % de victorias*.",
    "Y la idea sigue viva: el superdeportivo *Gordon Murray T.50*, del mismo diseñador, lleva un ventilador detrás.",
    "Un coche tan bueno… que *tuvieron que quitarlo*.",
]
SHOTS = [("open", 0, 1, 0.3), ("fan", 2, 3, 0.3), ("suck", 4, 5, 0.3), ("pressure", 6, 7, 0.3), ("wings", 8, 10, 0.3),
         ("kite", 11, 11, 0.3), ("race", 12, 13, 0.3), ("protest", 14, 15, 0.3), ("stats", 16, 16, 0.3), ("today", 17, 18, 1.8)]
FOCUS = {"race": (540, 950, 1.08)}
NOTIF = ("suck", 1.0)
HYPE = {"line": 1, "text": ["¿QUÉ ESCONDÍA DETRÁS?", "¿POR QUÉ LO QUITARON?"], "delay": [0, 1.5]}
KW_OVERRIDE = {3: [], 5: ["FALDILLAS"], 13: [], 14: ["PROTESTARON"], 15: ["BERNIE ECCLESTONE"], 16: []}
STICKER_EXTRA = [("ventilador", "🌀"), ("formula", "🏎️"), ("carrera", "🏁"), ("gano", "🏆"), ("victoria", "🏆"), ("chupaba", "🌀"), ("ventosa", "🐙"), ("piedras", "🪨"), ("protestaron", "😡"), ("=100", "💯"), ("minuto", "⏱️"), ("superdeportivo", "🏎️"), ("motor", "🔧")]
NOTIF_TEXT = "Suscríbete para más cosas que no sabías"

RED = (200, 30, 40)
CY_ = (110, 210, 255)
ORANGE = (255, 150, 60)
GREEN = (90, 230, 130)


# ------------------------------------------------------------------ objetos
FAN_DX, FAN_DY = 965 - 520, 198 - 180   # centro del ventilador respecto al centro del sprite


def f1_side(col=RED):
    """Fórmula 1 de 1978 visto de lado: ruedas descubiertas, piloto asomando y caja del ventilador detrás (sin marcas)."""
    c = Cv(1040, 360)
    c.shadow((20, 310, 1020, 356), 170, 12)
    hi, lo = shade(col, 1.3), shade(col, 0.45)
    c.rect((900, 150, 1030, 250), grad=((70, 72, 80), (26, 26, 30)), r=16)
    c.ellipse((921, 154, 1009, 242), radial=((36, 38, 44), (8, 8, 10)))
    c.poly([(30, 238), (60, 226), (340, 206), (440, 180), (500, 172), (560, 170), (620, 176), (700, 182), (790, 190), (880, 196),
            (910, 228), (890, 252), (40, 252)], grad=(hi, lo), power=0.9)
    c.poly([(60, 228), (880, 198), (884, 210), (60, 240)], fill=(250, 250, 252, 220))
    c.poly([(570, 174), (612, 108), (662, 108), (652, 178)], grad=((90, 94, 104), (40, 42, 48)))
    c.poly([(470, 176), (500, 150), (560, 150), (580, 174)], fill=(26, 30, 40))
    c.ellipse((496, 112, 566, 178), radial=((255, 230, 120), (210, 140, 20)), center=(0.38, 0.3))
    c.poly([(524, 132), (566, 132), (564, 152), (526, 152)], fill=(20, 24, 34))
    c.rect((0, 238, 120, 254), grad=((70, 72, 80), (24, 24, 28)), r=4)
    c.rect((0, 222, 14, 258), fill=(40, 40, 44))
    for x0, x1, y0 in ((200, 330, 230), (200, 330, 250), (820, 720, 232), (820, 720, 250)):
        c.line([(x0, y0), (x1, y0 - 6)], (60, 62, 70), 5)
    for wx, wy, r in ((200, 262, 64), (820, 250, 98)):
        c.ellipse((wx - r, wy - r, wx + r, wy + r), radial=((44, 44, 48), (10, 10, 12)), power=1.3)
        c.ellipse((wx - r * 0.5, wy - r * 0.5, wx + r * 0.5, wy + r * 0.5), radial=((210, 214, 222), (90, 94, 102)), center=(0.4, 0.35))
        c.arc((wx - r + 6, wy - r + 6, wx + r - 6, wy + r - 6), 200, 260, (255, 255, 255, 60), 4)
        c.ellipse((wx - 10, wy - 10, wx + 10, wy + 10), fill=(60, 62, 70))
    c.line([(70, 228), (430, 186)], (255, 255, 255, 90), 3)
    return c.done()


def f1_rear(col=RED):
    c = Cv(900, 640)
    c.shadow((40, 580, 860, 640), 170, 14)
    for x0 in (20, 640):
        c.rect((x0, 300, x0 + 240, 600), grad=((50, 50, 56), (14, 14, 16)), horizontal=True, r=40)
        for k in range(6):
            c.line([(x0 + 20 + k * 40, 310), (x0 + 20 + k * 40, 590)], (40, 40, 44), 3)
    c.poly([(240, 300), (660, 300), (620, 120), (280, 120)], grad=(shade(col, 1.2), shade(col, 0.5)))
    c.poly([(300, 60), (600, 60), (580, 120), (320, 120)], grad=((80, 84, 94), (40, 42, 48)))
    c.rect((300, 250, 600, 560), grad=((70, 72, 80), (30, 30, 34)), r=30)
    c.ellipse((320, 270, 580, 530), radial=((24, 26, 30), (6, 6, 8)))
    c.rect((240, 560, 660, 580), fill=(30, 30, 34))
    c.rect((100, 600, 160, 620), fill=(20, 20, 22))
    return c.done()


def fan_blades(img, cx, cy, r, t, speed=12, col=(150, 154, 166)):
    d = ImageDraw.Draw(img, "RGBA")
    for k in range(10):
        a = t * speed + k * math.pi / 5
        p = [(cx, cy), (cx + math.cos(a - 0.12) * r, cy + math.sin(a - 0.12) * r), (cx + math.cos(a + 0.18) * r * 0.95, cy + math.sin(a + 0.18) * r * 0.95)]
        d.polygon(p, fill=col + (230,))
    d.ellipse([cx - r * 0.18, cy - r * 0.18, cx + r * 0.18, cy + r * 0.18], fill=(200, 204, 214, 255))
    if speed > 6:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255, 40), width=6)


def suction_cup():
    c = Cv(420, 360)
    c.shadow((40, 300, 380, 350), 140, 10)
    c.rect((170, 20, 250, 160), grad=((240, 200, 60), (190, 140, 20)), horizontal=True, r=30)
    c.poly([(60, 300), (360, 300), (290, 150), (130, 150)], grad=((255, 110, 90), (190, 40, 30)))
    c.ellipse((40, 280, 380, 330), radial=((230, 80, 60), (150, 30, 20)))
    c.poly([(140, 160), (180, 160), (110, 290), (80, 290)], fill=(255, 255, 255, 60))
    return c.done()


def kite():
    c = Cv(400, 560)
    c.poly([(200, 20), (370, 200), (200, 400), (30, 200)], grad=((255, 210, 63), (255, 120, 60)))
    c.line([(200, 20), (200, 400)], (160, 80, 20), 5)
    c.line([(30, 200), (370, 200)], (160, 80, 20), 5)
    c.poly([(200, 20), (370, 200), (200, 200)], fill=(255, 255, 255, 50))
    pts = [(200, 400)] + [(200 + math.sin(k * 0.9) * 30, 400 + k * 16) for k in range(1, 10)]
    c.line(pts, (240, 240, 244), 4)
    for k in range(3):
        y = 440 + k * 40
        c.poly([(200 + math.sin(y * 0.05) * 30 - 16, y), (200 + math.sin(y * 0.05) * 30 + 16, y), (200 + math.sin(y * 0.05) * 30, y + 20)], fill=(90, 200, 255))
    return c.done()


def vacuum():
    c = Cv(460, 560)
    c.shadow((40, 500, 420, 556), 150, 10)
    c.rect((120, 280, 420, 500), grad=((255, 90, 90), (170, 30, 40)), r=60)
    c.ellipse((160, 430, 240, 510), radial=((60, 60, 66), (16, 16, 18)))
    c.ellipse((330, 430, 410, 510), radial=((60, 60, 66), (16, 16, 18)))
    c.rect((180, 300, 380, 360), fill=(255, 255, 255, 60), r=20)
    c.line([(130, 330), (60, 200), (100, 60)], (90, 94, 104), 26)
    c.rect((60, 30, 170, 70), grad=((70, 72, 80), (30, 30, 34)), r=14)
    c.ellipse((300, 360, 360, 420), fill=(90, 255, 140))
    return c.done()


def trophy():
    c = Cv(360, 480)
    c.shadow((40, 430, 320, 480), 160, 10)
    c.rect((90, 400, 270, 450), grad=((90, 60, 40), (50, 32, 20)), r=8)
    c.rect((150, 300, 210, 400), grad=((255, 220, 100), (190, 140, 30)), horizontal=True)
    c.poly([(60, 40), (300, 40), (260, 230), (180, 300), (100, 230)], grad=((255, 230, 120), (200, 140, 30)), horizontal=True)
    c.arc((10, 60, 110, 200), 90, 270, (230, 180, 60), 16)
    c.arc((250, 60, 350, 200), 270, 90, (230, 180, 60), 16)
    c.poly([(100, 50), (140, 50), (130, 220), (110, 210)], fill=(255, 255, 255, 80))
    return c.done()


def hypercar():
    c = Cv(1040, 340)
    c.shadow((40, 280, 1010, 336), 170, 12)
    col = (40, 44, 54)
    c.poly([(30, 230), (60, 190), (240, 160), (420, 110), (600, 100), (760, 120), (900, 150), (1000, 190), (1010, 240), (30, 246)],
           grad=((120, 130, 150), col), power=0.9)
    c.poly([(440, 116), (600, 106), (700, 140), (440, 150)], grad=((70, 90, 120), (14, 18, 26)))
    c.ellipse((880, 150, 990, 240), radial=((30, 32, 38), (8, 8, 10)))
    for k in range(8):
        a = k * math.pi / 4
        c.line([(935, 195), (935 + math.cos(a) * 46, 195 + math.sin(a) * 38)], (140, 144, 154), 5)
    c.line([(80, 196), (980, 186)], (255, 255, 255, 70), 3)
    for wx in (230, 820):
        c.ellipse((wx - 70, 246 - 70, wx + 70, 246 + 70), fill=(16, 16, 18))
        c.ellipse((wx - 44, 246 - 44, wx + 44, 246 + 44), radial=((190, 194, 204), (80, 84, 92)), center=(0.4, 0.35))
    c.rect((60, 200, 140, 214), fill=(255, 60, 50))
    return c.done()


def track_bg(img, t, hz=880, dusk=True, speed=1.0):
    if dusk:
        sky(img, (40, 40, 90), (255, 150, 100), 1.4, 0, hz)
        paste(img, glow(440, (255, 190, 120), 0.8), 820, hz - 40)
    else:
        sky(img, (90, 150, 220), (210, 228, 240), 1.3, 0, hz)
    mountains(img, hz, 80, (60, 50, 70) if dusk else (90, 120, 96), 4, 0.5)
    ground(img, hz, (70, 90, 60) if not dusk else (50, 50, 50), (30, 40, 30))
    d = ImageDraw.Draw(img, "RGBA")
    y0, y1 = hz + 160, hz + 420
    d.rectangle([0, y0, W, y1], fill=(54, 54, 60, 255))
    off = (t * 1400 * speed) % 120
    for x in range(-120, W + 120, 120):
        d.rectangle([x - off, y0 - 30, x - off + 60, y0], fill=(230, 40, 40, 255))
        d.rectangle([x - off + 60, y0 - 30, x - off + 120, y0], fill=(250, 250, 250, 255))
        d.rectangle([x - off, y1, x - off + 60, y1 + 30], fill=(230, 40, 40, 255))
        d.rectangle([x - off + 60, y1, x - off + 120, y1 + 30], fill=(250, 250, 250, 255))
    for k in range(10):
        x = (k * 170 - t * 2400 * speed) % (W + 300) - 150
        d.line([(x, y0 + 60 + k % 3 * 60), (x + 140, y0 + 60 + k % 3 * 60)], fill=(255, 255, 255, 40), width=3)
    return y1


# ------------------------------------------------------------------ planos
def sh_open(img, t, T, L):
    a1 = L[1][0]
    y1 = track_bg(img, t, 880, True, 1.0)
    paste(img, spr(f1_side), 540, 880 + 160 + 130, 1.0)
    fan_blades(img, 540 + FAN_DX, 880 + 160 + 130 + FAN_DY, 42, t, 30, (110, 114, 124))
    top_shade(img)
    title2(t, 0.3, "1978 · UN F1 QUE SOLO", "CORRIÓ UNA VEZ", 250, 56, 90, hold=max(1.8, a1 - 0.3))
    vignette(img, 190)


def sh_fan(img, t, T, L):
    a1 = L[1][0]
    sky(img, (26, 28, 36), (8, 8, 10), 1.0)
    for x in (200, 880):
        spotlight(img, t, x, 0, 1300, 40, 300, 30, dust=True)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, 1250, W, H], fill=(40, 40, 46, 255))
    paste(img, spr(f1_rear), 540, 960, 1.05)
    fx, fy, fr = 540, 960 + (400 - 320) * 1.05, 130 * 1.05
    fan_blades(img, fx, fy, fr, t, 16)
    callout(img, t, 0.9, fx + fr * 0.7, fy - fr * 0.7, 860, 520, "VENTILADOR", YEL, 40)
    if t > a1:
        k = ease(clamp((t - a1 - 0.2) / 0.5))
        d = ImageDraw.Draw(img, "RGBA")
        d.rounded_rectangle([120, 1300, 960, 1400], radius=20, fill=(0, 0, 0, int(190 * k)), outline=CY_ + (int(255 * k),), width=3)
        d.text((540, 1350), "VERSIÓN OFICIAL: «ES PARA REFRIGERAR»", font=f(F_SER, 38), fill=(255, 255, 255, int(255 * k)), anchor="mm")
        if t > a1 + 1.4:
            kk = ease(clamp((t - a1 - 1.4) / 0.3))
            d.ellipse([880 - 70, 1250 - 70, 880 + 70, 1250 + 70], fill=(230, 60, 66, int(240 * kk)))
            d.text((880, 1248), "?", font=f(F_CAP, 100), fill=(255, 255, 255, int(255 * kk)), anchor="mm")
    if t < a1:
        big(t, 0.3, "BRABHAM BT46B", 300, 92, WHITE, pop=False)
    else:
        big(t, a1 + 0.2, "¿REFRIGERAR?", 300, 100, CY_)
    vignette(img, 200)


def cross_section(img, t, suck_k, skirts_k, cx=540, gy=1120):
    sky(img, (18, 22, 30), (6, 6, 8), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, gy, W, H], fill=(54, 54, 60, 255))
    for x in range(0, W, 40):
        d.line([(x, gy + 4), (x + 20, gy + 4)], fill=(80, 80, 88, 255), width=3)
    car = spr(f1_side)
    paste(img, car, cx, gy - 100, 1.0, 0.92)
    fx, fy = cx + FAN_DX, gy - 100 + FAN_DY
    fan_blades(img, fx, fy, 42, t, 30, (110, 114, 124))
    if skirts_k > 0:
        A = int(255 * skirts_k)
        d.rectangle([cx - 400, gy - 40, cx + 360, gy - 2], fill=(255, 210, 63, int(A * 0.85)))
        if skirts_k > 0.5:
            spaced(d, cx - 20, gy - 21 - 24, "FALDILLAS", f(F_SER, 30), (30, 30, 34, A), 4, shadow=False)
    if suck_k > 0:
        rr = random.Random(4)
        for i in range(34):
            u = ((t * 0.9 + i / 34) % 1.0)
            x = lerp(cx - 420, fx - 20, u)
            y = gy - 16 - rr.uniform(0, 22) if u < 0.9 else lerp(gy - 20, fy, (u - 0.9) / 0.1)
            paste(img, glow(26, CY_, 1.0), x, y, 1.0, suck_k)
        for i in range(10):
            u = ((t * 1.2 + i / 10) % 1.0)
            x = fx + 40 + u * 260
            y = fy + math.sin(u * 8 + i) * 20
            paste(img, glow(28, (200, 230, 255), 1.0), x, y, 1.0, suck_k * (1 - u))


def sh_suck(img, t, T, L):
    a1 = L[1][0]
    cross_section(img, t, ease(clamp((t - 0.5) / 0.8)), ease(clamp((t - a1 - 0.2) / 0.6)) if t > a1 else 0.0)
    if t < a1:
        big(t, 0.3, "CHUPABA EL AIRE", 290, 90, CY_, sub="DE DEBAJO DEL COCHE", pop=False)
    else:
        big(t, a1 + 0.3, "SELLADO", 290, 110, YEL)
    vignette(img, 200)


def pressure_scene(img, t, t0):
    cross_section(img, t, 1.0, 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    rr = random.Random(7)
    for i in range(70):
        x = rr.uniform(60, 1020)
        y = rr.uniform(520, 880) + math.sin(t * 2 + i) * 6
        d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=(255, 150, 100, 200))
    k = ease(clamp((t - t0 - 0.5) / 0.6))
    for x in (260, 540, 820):
        y0 = 640
        d.line([(x, y0), (x, y0 + 260 * k)], fill=(255, 120, 80, 255), width=14)
        if k > 0.1:
            d.polygon([(x - 30, y0 + 260 * k - 10), (x + 30, y0 + 260 * k - 10), (x, y0 + 260 * k + 36)], fill=(255, 120, 80, 255))
    spaced(d, 540, 500, "MÁS PRESIÓN ARRIBA", f(F_SER, 40), (255, 200, 170, 240), 5)
    spaced(d, 540, 1210, "MENOS PRESIÓN DEBAJO", f(F_SER, 40), (170, 220, 255, 240), 5)


def cup_scene(img, t, t0):
    sky(img, (24, 28, 36), (8, 8, 10), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, 1120, W, H], fill=(70, 74, 84, 255))
    k = ease(clamp((t - t0 - 0.2) / 0.5))
    paste(img, spr(suction_cup), 540, lerp(700, 960, k), 1.4)
    if k > 0.95:
        for i in range(3):
            r = 220 + ((t - t0) * 200 + i * 80) % 240
            d.arc([540 - r, 1110 - r * 0.3, 540 + r, 1110 + r * 0.3], 180, 360, fill=(255, 255, 255, 80), width=4)


def sh_pressure(img, t, T, L):
    a1 = L[1][0]
    xf(img, t, a1, lambda im: pressure_scene(im, t, 0), lambda im: cup_scene(im, t, a1), 0.6)
    if t < a1:
        big(t, 0.3, "MENOS PRESIÓN DEBAJO", 290, 66, WHITE, pop=False)
    else:
        big(t, a1 + 0.2, "UNA VENTOSA", 290, 110, YEL)
    vignette(img, 200)


def downforce_graph(img, t, t0, show_fan):
    sky(img, (12, 16, 24), (4, 6, 8), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    x0, x1, y0, y1 = 150, 980, 520, 1220
    d.line([(x0, y1), (x1, y1)], fill=(200, 200, 210), width=4)
    d.line([(x0, y1), (x0, y0)], fill=(200, 200, 210), width=4)
    d.text(((x0 + x1) / 2, y1 + 50), "VELOCIDAD →", font=f(F_SER, 36), fill=(220, 220, 230), anchor="mm")
    d.text((x0 - 20, y0 - 30), "AGARRE", font=f(F_SER, 34), fill=(220, 220, 230), anchor="lm")
    k = clamp((t - t0 - 0.2) / 1.6)
    pts = [(lerp(x0, x1, u), y1 - (u ** 2) * (y1 - y0) * 0.95) for u in np.linspace(0, k, 60)]
    if len(pts) > 1:
        glow_line(img, pts, (255, 150, 60), 6, 8, 240)
    d = ImageDraw.Draw(img, "RGBA")
    if k > 0.9:
        d.text((x1 - 10, y0 + 20), "ALERONES", font=f(F_SER, 38), fill=(255, 170, 90), anchor="rm")
    d.rectangle([x0, y0, lerp(x0, x1, 0.3), y1], fill=(90, 160, 255, 30))
    d.text((lerp(x0, x1, 0.15), y1 - 40), "CURVAS LENTAS", font=f(F_SER, 28), fill=(170, 210, 255), anchor="mm")
    if show_fan > 0:
        kk = ease(show_fan)
        pts = [(lerp(x0, x1, u), y1 - (0.62 + 0.3 * u * u) * (y1 - y0) * 0.95) for u in np.linspace(0, kk, 60)]
        glow_line(img, pts, GREEN, 6, 8, 240)
        d = ImageDraw.Draw(img, "RGBA")
        d.text((x0 + 30, y1 - 0.62 * (y1 - y0) * 0.95 - 40), "VENTILADOR", font=f(F_SER, 38), fill=GREEN, anchor="lm")


def hairpin(img, t, t0):
    sky(img, (60, 90, 50), (40, 70, 36), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    cx, cy = 540, 760
    d.arc([cx - 360, cy - 360, cx + 360, cy + 360], 180, 360, fill=(54, 54, 60, 255), width=170)
    d.rectangle([cx - 445, cy, cx - 275, 1400], fill=(54, 54, 60, 255))
    d.rectangle([cx + 275, cy, cx + 445, 1400], fill=(54, 54, 60, 255))
    for a in range(180, 361, 10):
        r = 445
        x, y = cx + math.cos(math.radians(a)) * r, cy + math.sin(math.radians(a)) * r
        d.ellipse([x - 8, y - 8, x + 8, y + 8], fill=(230, 40, 40, 255) if (a // 10) % 2 else (250, 250, 250, 255))
    u = clamp((t - t0 - 0.2) / 2.0)
    a = math.radians(180 + 180 * u)
    gx, gy = cx + math.cos(a) * 360, cy + math.sin(a) * 360
    wr = 360 + 140 * u ** 1.5
    rx, ry = cx + math.cos(a) * wr, cy + math.sin(a) * wr
    d.ellipse([gx - 26, gy - 26, gx + 26, gy + 26], fill=GREEN + (255,), outline=(255, 255, 255, 255), width=4)
    d.ellipse([rx - 26, ry - 26, rx + 26, ry + 26], fill=(255, 120, 60, 255), outline=(255, 255, 255, 255), width=4)
    d.text((gx, gy - 60), "VENTILADOR", font=f(F_SER, 30), fill=(255, 255, 255), anchor="mm")
    d.text((rx, ry + 60), "ALERONES", font=f(F_SER, 30), fill=(255, 255, 255), anchor="mm")


def sh_wings(img, t, T, L):
    a1, a2 = L[1][0], L[2][0]
    if t < a2 - 0.3:
        xf(img, t, a1, lambda im: downforce_graph(im, t, 0, 0.0), lambda im: hairpin(im, t, a1), 0.6)
    else:
        xf(img, t, a2, lambda im: hairpin(im, t, a1), lambda im: downforce_graph(im, t, -10, clamp((t - a2 - 0.3) / 1.2)), 0.6)
    if t < a1:
        big(t, 0.3, "LOS ALERONES", 290, 92, ORANGE, sub="NECESITAN VELOCIDAD", pop=False)
    elif t < a2:
        big(t, a1 + 0.2, "EN CURVAS LENTAS…", 290, 76, WHITE, pop=False)
    else:
        big(t, a2 + 0.3, "SUCCIÓN SIEMPRE", 290, 90, GREEN, pop=False)
    vignette(img, 190)


def sh_kite(img, t, T, L):
    sky(img, (110, 160, 220), (200, 225, 245), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([540, 0, W, H], fill=(40, 34, 30, 255))
    d.rectangle([538, 0, 542, H], fill=(255, 255, 255, 255))
    k1 = ease(clamp((t - 0.2) / 0.6))
    paste(img, spr(kite), 270, 760 + math.sin(t * 2) * 30, 0.8, k1, math.sin(t * 1.6) * 8)
    for i in range(4):
        x = (t * 300 + i * 160) % 600 - 60
        d.line([(x, 980 + i * 30), (x + 90, 980 + i * 30)], fill=(255, 255, 255, 160), width=4)
    k2 = ease(clamp((t - 1.6) / 0.6))
    paste(img, spr(vacuum), 810, 900, 0.85, k2)
    d = ImageDraw.Draw(img, "RGBA")
    spaced(d, 270, 1250, "NECESITA VIENTO", f(F_SER, 34), (30, 40, 60, int(255 * k1)), 3, shadow=False)
    spaced(d, 810, 1250, "SOLO SE ENCIENDE", f(F_SER, 34), (255, 255, 255, int(255 * k2)), 3)
    big(t, 0.3, "COMETA VS ASPIRADORA", 290, 64, WHITE, pop=False)
    vignette(img, 170)


def sh_race(img, t, T, L):
    a1 = L[1][0]
    y1 = track_bg(img, t, 760, False, 1.3)
    d = ImageDraw.Draw(img, "RGBA")
    for x in range(0, W, 26):
        d.rectangle([x, 760 + 90, x + 18, 760 + 130], fill=((x * 37) % 255, 80, 140, 200))
    gap = 0 if t < a1 else ease(clamp((t - a1) / 1.6))
    paste(img, spr(f1_side), 640, 760 + 160 + 130, 0.72)
    fan_blades(img, 640 + FAN_DX * 0.72, 760 + 160 + 130 + FAN_DY * 0.72, 36, t, 30, (110, 114, 124))
    paste(img, spr(f1_side, (40, 90, 200)), lerp(140, -700, gap), 760 + 160 + 200, 0.6)
    sepia(img, 0.35)
    if t > a1 + 0.4:
        k = ease(clamp((t - a1 - 0.4) / 0.5))
        d = ImageDraw.Draw(img, "RGBA")
        d.rounded_rectangle([170, 1300, 910, 1430], radius=20, fill=(10, 12, 18, int(235 * k)), outline=YEL + (int(255 * k),), width=4)
        d.text((540, 1340), "1.º  LAUDA", font=f(F_MONO, 44), fill=(255, 255, 255, int(255 * k)), anchor="mm")
        d.text((540, 1395), "2.º  + MÁS DE 30 S", font=f(F_MONO, 40), fill=YEL + (int(255 * k),), anchor="mm")
    date_stamp(t, 0.3, "GP DE SUECIA · 1978", 260, hold=max(1.8, a1 - 0.6))
    if t > a1:
        big(t, a1 + 0.2, "+30 SEGUNDOS", 290, 104, YEL)
    vignette(img, 190)


def sh_protest(img, t, T, L):
    a1 = L[1][0]
    if t < a1:
        y1 = track_bg(img, t, 760, False, 1.0)
        paste(img, spr(f1_side), 300, 760 + 160 + 130, 0.66)
        fan_blades(img, 300 + FAN_DX * 0.66, 760 + 160 + 130 + FAN_DY * 0.66, 33, t, 30, (110, 114, 124))
        paste(img, spr(f1_side, (40, 140, 90)), 980, 760 + 160 + 150, 0.62, 1.0, 0, True)
        rr = random.Random(int(t * 12))
        d = ImageDraw.Draw(img, "RGBA")
        for i in range(26):
            u = rr.random()
            x = 300 + 330 * 0.66 + u * 380
            y = 760 + 160 + 110 + rr.uniform(-60, 40) - math.sin(u * math.pi) * 80
            r = rr.uniform(4, 10)
            d.ellipse([x - r, y - r, x + r, y + r], fill=(150, 120, 90, 230))
        big(t, 0.4, "«LANZA PIEDRAS»", 290, 92, (255, 150, 120))
    else:
        sky(img, (24, 26, 32), (8, 8, 10), 1.0)
        d = ImageDraw.Draw(img, "RGBA")
        d.rectangle([0, 1250, W, H], fill=(40, 40, 46, 255))
        paste(img, spr(f1_side), 540, 1180, 0.95)
        k = ease(clamp((t - a1 - 0.3) / 1.4))
        d = ImageDraw.Draw(img, "RGBA")
        d.rectangle([0, 0, W, 300 + 900 * k], fill=(70, 74, 84, 255))
        for y in range(0, int(300 + 900 * k), 40):
            d.line([(0, y), (W, y)], fill=(50, 52, 60, 255), width=4)
        if t > a1 + 1.8:
            kk = ease(clamp((t - a1 - 1.8) / 0.3))
            st = Image.new("RGBA", (760, 200), (0, 0, 0, 0))
            sd = ImageDraw.Draw(st)
            sd.rounded_rectangle([20, 20, 740, 180], radius=16, outline=(230, 60, 66, 240), width=10)
            sd.text((380, 100), "PROHIBIDO", font=f(F_SER, 96), fill=(230, 60, 66, 240), anchor="mm")
            paste(img, st.rotate(-8, expand=True, resample=Image.BICUBIC), 540, 800, lerp(1.4, 1.0, kk), kk)
        big(t, a1 + 0.2, "RETIRADO", 290, 110, WHITE, hold=1.5)
    vignette(img, 190)


def sh_stats(img, t, T, L):
    sky(img, (30, 26, 20), (8, 8, 6), 1.0)
    paste(img, glow(500, (255, 210, 120), 0.4), 540, 780)
    k = ease(clamp((t - 0.2) / 0.6))
    paste(img, spr(trophy), 540, lerp(1000, 820, k), 1.0, k)
    d = ImageDraw.Draw(img, "RGBA")
    for i, (lbl, val) in enumerate((("CARRERAS", "1"), ("VICTORIAS", "1"))):
        kk = ease(clamp((t - 0.8 - i * 0.4) / 0.4))
        x = 300 + i * 480
        d.rounded_rectangle([x - 190, 1150, x + 190, 1330], radius=24, fill=(10, 12, 18, int(235 * kk)), outline=YEL + (int(255 * kk),), width=4)
        d.text((x, 1200), lbl, font=f(F_SER, 40), fill=(255, 255, 255, int(255 * kk)), anchor="mm")
        d.text((x, 1275), val, font=f(F_CAP, 80), fill=YEL + (int(255 * kk),), anchor="mm")
    big(t, 1.6, "100 %", 290, 140, YEL, sub="DE VICTORIAS")
    vignette(img, 190)


def sh_today(img, t, T, L):
    a1 = L[1][0]

    def A(im):
        sky(im, (14, 16, 24), (4, 4, 6), 1.0)
        for x in (200, 880):
            spotlight(im, t, x, 0, 1300, 40, 300, 26, dust=False)
        d = ImageDraw.Draw(im, "RGBA")
        d.rectangle([0, 1180, W, H], fill=(36, 36, 42, 255))
        d.ellipse([60, 1150, 1020, 1230], fill=(255, 255, 255, 30))
        paste(im, spr(hypercar), 540, 1080, 1.0)
        fan_blades(im, 540 + (935 - 520), 1080 + (195 - 170), 44, t, 26, (130, 134, 144))
        callout(im, t, 1.2, 540 + 415, 1100, 820, 700, "VENTILADOR", YEL, 38)

    def B(im):
        sky(im, (8, 8, 12), (2, 2, 4), 1.0)
        spotlight(im, t, 540, 0, 1300, 60, 420, 34, dust=True)
        d = ImageDraw.Draw(im, "RGBA")
        d.rectangle([0, 1200, W, H], fill=(30, 30, 34, 255))
        paste(im, spr(f1_side), 540, 1110, 0.95)
        fan_blades(im, 540 + FAN_DX * 0.95, 1110 + FAN_DY * 0.95, 48, t, 4, (110, 114, 124))
        paste(im, glow(400, (255, 220, 160), 0.25), 540, 1050)

    xf(img, t, a1, A, B, 0.8)
    top_shade(img)
    if t < a1:
        big(t, 0.4, "LA IDEA SIGUE VIVA", 280, 80, WHITE, pop=False)
    else:
        title2(t, a1 + 0.3, "TAN BUENO QUE", "TUVIERON QUE QUITARLO", 260, 60, 70, track=4, hold=max(2.0, T - a1 - 0.8), c1=WHITE, c2=YEL)
    vignette(img, 190)


FNS = {k: globals()["sh_" + k] for k, *_ in SHOTS}
KW_ZONES = {"open": [1, 4], "fan": [8, 9, 5], "suck": [9, 4, 5], "pressure": [5, 9, 4], "wings": [9, 4, 5], "kite": [5, 9],
            "race": [0, 3], "protest": [1, 4, 5], "stats": [5, 4], "today": [5, 9, 4]}
AUDIO = {
    "music": [("open", "epic"), ("fan", "mystery"), ("suck", "exp"), ("wings", "creative"), ("race", "epic"), ("protest", "tension"),
              ("stats", "premium")],
    "gains": {"exp": 0.7, "mystery": 0.8},
    "amb": {"road": ["open", "race", "protest"], "hum": ["fan", "suck", "pressure", "today"], "wind": ["kite"], "crowd": ["stats"]},
    "sfx": [("open+0.2", "whoosh", 0.12), ("fan+0.9", "pop", 0.15), ("fan@L1+1.4", "blip_down", 0.12),
            ("suck+0.5", "whoosh_up", 0.12), ("suck@L1+0.2", "click", 0.2), ("pressure+0.5", "swell", 0.1), ("pressure@L1+0.4", "thud", 0.25),
            ("wings+0.3", "draw", 0.12), ("wings@L1+0.2", "whoosh", 0.1), ("wings@L2+0.3", "draw", 0.12),
            ("kite+0.3", "pop", 0.14), ("kite+1.6", "hum_on", 0.12),
            ("race+0.3", "paper", 0.12), ("race@L1+0.4", "ding", 0.08),
            ("protest+0.4", "crackle", 0.1), ("protest@L1+0.3", "whoosh", 0.1), ("protest@L1+1.8", "thud", 0.25),
            ("stats+0.3", "chime", 0.06), ("stats+1.6", "swell", 0.12), ("today@L1+0.3", "swell", 0.14)],
    "bed": [("suck", "wings")],
    "bpm": 104,
}
