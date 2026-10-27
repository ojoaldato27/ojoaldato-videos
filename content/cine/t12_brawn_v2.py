"""T12 v2 · Brawn GP con la edición «docu» que pidió Iker el 19/10 (copiando su vídeo de referencia de Julio César):
fondo azul noche, título serif cursiva arriba, subtítulos de 1-3 palabras con la clave en dorado, tarjeta Seguir a mitad.
Si hay locución (VOICE), todo se sincroniza con ella; si no, va con los tiempos estimados."""
import os
from gadgets import *
import docu as DC
import t12_brawn as B
import t11_f1_ventilador as T11

bgp_side, coin, newspaper, v8_engine, gavel = B.bgp_side, B.coin, B.newspaper, B.v8_engine, B.gavel
tyre_cold, thermometer, confetti = B.tyre_cold, B.thermometer, B.confetti
trophy = T11.trophy
CHART, INK, WHITE_CAR, SILVER, NAVY, CY_ = B.CHART, B.INK, B.WHITE_CAR, B.SILVER, B.NAVY, B.CY_
GOLD, CREAM = DC.GOLD, DC.CREAM
REDC = (232, 70, 70)
GREENC = (90, 220, 140)
TEAL = (40, 200, 190)

STYLE = "docu"
TITLE = "El_equipo_de_F1_que_costo_una_libra_v2"
_VZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voz", "t12_brawn")
VOICE = next((_VZ + e for e in (".mp3", ".m4a", ".wav") if os.path.exists(_VZ + e)), _VZ + ".mp3")   # MP3 de Iker o voz del canal
LINES = B.LINES
OUTRO_LINE = "Si no lo sabías… ahora ya lo sabes. Dale a like y sígueme para más."
SHOTS = B.SHOTS
FOCUS = {}
NOTIF = ("pound", 0.6)
FOLLOW = None            # Iker prefiere la notificación tipo iPhone de antes (20/10)
NOTIF_TEXT = B.NOTIF_TEXT
HEAD = {
    0: ("Brawn GP", "EL EQUIPO QUE NO EXISTÍA"),
    1: ("¿Cómo lo hizo?", "Y POR QUÉ DESAPARECIÓ DESPUÉS"),
    2: ("Diciembre de 2008", "LA CRISIS SE LLEVA A HONDA"),
    3: ("Una libra", "LO QUE PAGÓ ROSS BRAWN"),
    4: ("Brawn GP", "CON MOTOR MERCEDES"),
    5: ("Blanco y flúor", "CASI SIN PATROCINADORES"),
    6: ("El truco", "EL DOBLE DIFUSOR"),
    7: ("Dos pisos", "MÁS AIRE DEBAJO, MÁS AGARRE"),
    8: ("Legal", "LA FIA LE DA LA RAZÓN"),
    9: ("Australia", "POLE Y DOBLETE"),
    10: ("6 de 7", "LAS PRIMERAS CARRERAS"),
    11: ("El bajón", "NEUMÁTICOS FRÍOS"),
    12: ("La ventaja", "BUTTON 95 · VETTEL 84"),
    13: ("Brasil", "DE 14.º A CAMPEÓN DEL MUNDO"),
    14: ("2 de 2", "PILOTOS Y CONSTRUCTORES"),
    15: ("110 millones", "MERCEDES SE QUEDA EL EQUIPO"),
    16: ("8 títulos", "2014 – 2021, SEGUIDOS"),
    17: ("Una libra", "LO QUE COSTÓ AL PRINCIPIO"),
    17.45: ("Solo el principio", "LO QUE PARECE UN FINAL…"),
}
# La mascota sale cuando explica algo (None = ese plano va limpio, como en la referencia)
NARRATOR = {"open": ("wave", "left"), "honda": None, "pound": ("point", "left"), "engine": None, "livery": None,
            "diffuser": ("point", "left"), "legal": ("smirk", "left"), "australia": None, "streak": None, "cold": ("think", "left"),
            "brazil": None, "titles": ("surprise", "left"), "mercedes": None, "eight": None, "final": ("think", "left")}
NARRATOR_POS = {"left": (138, 1446), "right": (940, 1446)}
NARRATOR_SCALE = 0.55
PUSH = {"open": (540, 900), "diffuser": (600, 900), "australia": (560, 1000)}


def lt(L, i, fr=0.0):
    i = min(i, len(L) - 1)
    a, b = L[i]
    return a + (b - a) * fr


def car_ghost():
    return bgp_side((70, 78, 108), (96, 104, 136), (36, 40, 58))


# ------------------------------------------------------------------ planos
def sh_open(img, t, T, L):
    DC.bg(img, t, 540, 900)
    q1 = lt(L, 1)
    DC.glow_at(img, 540, 930, 520, (255, 214, 150), 0.22)
    k = ease(clamp((t - 0.1) / 1.4))
    x = lerp(660, 540, k)
    ghost = ease(clamp((t - q1 - 0.2) / 0.9))
    d = ImageDraw.Draw(img, "RGBA")
    d.ellipse([200, 1040, 900, 1085], fill=(0, 0, 0, 90))
    paste(img, spr(bgp_side), x, 930, 0.78, k * (1 - ghost))
    if ghost > 0:
        paste(img, spr(car_ghost), x, 930, 0.78, ghost)
        # el equipo «se desvanece»: polvo dorado que sale del coche
        rr = random.Random(4)
        for i in range(70):
            u = clamp((t - q1 - 0.2 - rr.uniform(0, 0.8)) / 2.2)
            if u <= 0:
                continue
            px, py = rr.uniform(160, 920), rr.uniform(840, 1050)
            yy = py - u * rr.uniform(120, 320)
            xx = px + math.sin(u * 4 + i) * 30
            a = int(200 * math.sin(u * math.pi))
            d.ellipse([xx - 3, yy - 3, xx + 3, yy + 3], fill=(255, 214, 140, a))
    DC.pill(img, 610, 1170, "2009 · MUNDIAL DE FÓRMULA 1", ease(clamp((t - 0.9) / 0.5)) * (1 - ghost))


def sh_honda(img, t, T, L):
    DC.bg(img, t, 540, 860, seed=3)
    DC.glow_at(img, 540, 860, 420, (255, 200, 150), 0.16)
    k = ease(clamp((t - 0.1) / 0.9))
    paste(img, spr(newspaper), 540, lerp(980, 840, k), lerp(0.56, 0.64, k), k, lerp(-10, -3, k))
    # la bolsa cayendo
    q = ease(clamp((t - 0.9) / 1.6))
    if q > 0:
        d = ImageDraw.Draw(img, "RGBA")
        pts = [(180, 1170), (300, 1150), (400, 1190), (520, 1180), (640, 1240), (760, 1230), (900, 1300)]
        n = max(2, int(len(pts) * q + 1))
        seg = pts[:n]
        d.line(seg, fill=REDC + (230,), width=8, joint="curve")
        x, y = seg[-1]
        d.polygon([(x + 18, y + 10), (x - 10, y - 14), (x - 4, y + 22)], fill=REDC + (230,))
    DC.pill(img, 540, 1360, "HONDA SE VA · EL EQUIPO SE QUEDA SIN DUEÑO", ease(clamp((t - lt(L, 0, 0.55)) / 0.4)))


def sh_pound(img, t, T, L):
    DC.bg(img, t, 560, 860, seed=5)
    DC.glow_at(img, 560, 860, 460, (255, 205, 110), 0.3)
    u = t - 0.3
    spin = math.cos(max(0, u) * 9 * math.exp(-max(0, u) * 0.9)) if u < 3.0 else 1.0
    s = max(0.06, abs(spin))
    k = ease(clamp((t - 0.15) / 0.5))
    im = spr(coin, spin >= 0)
    im2 = im.resize((max(2, int(im.size[0] * s)), im.size[1]), Image.LANCZOS)
    paste(img, im2, 580, lerp(760, 860, k), 1.05, k)
    DC.dotted(img, (980, 520), (900, 760), (790, 840), ease(clamp((t - 0.5) / 1.2)))
    DC.pill(img, 580, 1200, "ROSS BRAWN · JEFE DEL EQUIPO", ease(clamp((t - 0.7) / 0.4)))


def sh_engine(img, t, T, L):
    DC.bg(img, t, 540, 960, seed=7)
    DC.glow_at(img, 540, 980, 480, (150, 200, 255), 0.14)
    k = ease(clamp((t - 0.5) / 1.5))
    paste(img, spr(bgp_side), 540, 1000, 0.9, lerp(0.45, 1.0, k))
    paste(img, spr(v8_engine), lerp(540, 738, k), lerp(640, 1004, k), lerp(0.75, 0.27, k), 1.0 if k < 0.97 else 0.0)
    if k >= 0.97:
        DC.glow_at(img, 738, 1004, 110, CY_, 0.45)
        paste(img, spr(v8_engine), 738, 1004, 0.27, 0.6)
    DC.pill(img, 540, 1260, "MOTOR MERCEDES · V8 2,4 L", ease(clamp((t - 2.0) / 0.4)))


def sh_livery(img, t, T, L):
    DC.bg(img, t, 540, 900, seed=9)
    DC.glow_at(img, 540, 930, 480, (230, 255, 150), 0.12)
    k = ease(clamp((t - 0.3) / 1.6))
    grey = spr(bgp_side, (96, 102, 120), (80, 86, 104), (52, 56, 70))
    paint = spr(bgp_side)
    paste(img, grey, 540, 930, 0.8)
    if k > 0:
        x_cut = int(paint.size[0] * k)
        im = Image.new("RGBA", paint.size, (0, 0, 0, 0))
        im.paste(paint.crop((0, 0, max(1, x_cut), paint.size[1])), (0, 0))
        paste(img, im, 540, 930, 0.8)
        if k < 0.99:
            sx = 540 - paint.size[0] * 0.8 / 2 + x_cut * 0.8
            DC.glow_at(img, sx, 930, 90, (255, 255, 255), 0.8)
    d = ImageDraw.Draw(img, "RGBA")
    for i, (col, lbl) in enumerate(((WHITE_CAR, "BLANCO"), (CHART, "AMARILLO FLÚOR"), (INK, "NEGRO"))):
        kk = ease(clamp((t - 1.7 - i * 0.3) / 0.35))
        if kk > 0:
            x = 300 + i * 240
            r = 34 * kk
            d.ellipse([x - r, 1200 - r, x + r, 1200 + r], fill=col + (255,), outline=(255, 255, 255, 150), width=3)
            d.text((x, 1268), lbl, font=DC.font(DC.F_UI, 22), fill=(205, 210, 224, int(255 * kk)), anchor="mm")


def _diffuser(img, t, dk, fk, press):
    DC.bg(img, t, 600, 900, seed=11)
    d = ImageDraw.Draw(img, "RGBA")
    gy = 1090
    d.line([(60, gy), (1020, gy)], fill=(120, 128, 150, 200), width=4)
    for x in range(60, 1020, 46):
        d.line([(x, gy + 10), (x + 22, gy + 10)], fill=(80, 88, 110, 200), width=3)
    paste(img, spr(bgp_side), 40, gy - 250, 1.7, 0.12)
    fl = gy - 70
    d.polygon([(60, fl), (620, fl), (980, fl - 170), (980, fl - 150), (630, fl + 16), (60, fl + 16)], fill=(52, 58, 80, 255))
    d.line([(60, fl), (620, fl), (980, fl - 170)], fill=(196, 202, 220, 255), width=5)
    if dk > 0:
        A = int(255 * dk)
        d.polygon([(560, fl - 70), (700, fl - 70), (980, fl - 300), (980, fl - 272), (700, fl - 50), (560, fl - 50)], fill=(70, 78, 50, A))
        d.line([(560, fl - 70), (700, fl - 70), (980, fl - 300)], fill=CHART + (A,), width=6)
    if fk > 0:
        rr = random.Random(5)
        for i in range(48):
            u = (t * 0.6 + i / 48) % 1.0
            x = lerp(40, 1060, u)
            lane = i % 3
            if lane < 2:
                y = fl + 38 + lane * 20 if x < 620 else fl + 38 + lane * 20 - (x - 620) * (0.47 + 0.08 * lane)
                col, a = CY_, fk
            else:
                if dk <= 0:
                    continue
                y = fl - 60 if x < 700 else fl - 60 - (x - 700) * 0.82
                col, a = CHART, fk * dk
            DC.glow_at(img, x, y + rr.uniform(-5, 5), 16, col, 0.9 * a)
    DC.pill(img, 800, fl + 110, "DIFUSOR", ease(clamp((t - 0.7) / 0.4)), size=22)
    if dk > 0.5:
        DC.pill(img, 820, fl - 360, "2.º PISO", ease(clamp((dk - 0.5) / 0.5)), size=22, col=CHART)
    if press > 0:
        for x in (330, 520, 710):
            y0 = 520
            d.line([(x, y0), (x, y0 + 200 * press)], fill=GOLD + (230,), width=10)
            if press > 0.1:
                yy = y0 + 200 * press
                d.polygon([(x - 24, yy - 6), (x + 24, yy - 6), (x, yy + 30)], fill=GOLD + (230,))


def sh_diffuser(img, t, T, L):
    a1 = lt(L, 1)
    _diffuser(img, t, ease(clamp((t - 1.4) / 0.8)), ease(clamp((t - 0.3) / 0.8)), ease(clamp((t - lt(L, 1, 0.55)) / 0.6)))


def sh_legal(img, t, T, L):
    DC.bg(img, t, 600, 860, seed=13)
    tg_t = lt(L, 0, 0.5)
    for i, (x, y, r) in enumerate(((260, 560, -10), (840, 600, 8), (250, 960, 7), (850, 1000, -6))):
        k = ease(clamp((t - 0.15 - i * 0.16) / 0.3))
        if k > 0:
            bub = Image.new("RGBA", (300, 150), (0, 0, 0, 0))
            bd = ImageDraw.Draw(bub)
            bd.rounded_rectangle([6, 6, 294, 120], radius=30, fill=(246, 241, 230, 235))
            bd.polygon([(70, 116), (110, 116), (60, 146)], fill=(246, 241, 230, 235))
            bd.text((150, 64), "¡ILEGAL!", font=DC.caps_font(46, "ExtraBold"), fill=(190, 40, 50), anchor="mm")
            paste(img, bub, x, y, lerp(0.5, 0.95, k), k * (1 - ease(clamp((t - tg_t - 0.1) / 0.4))), r)
    tg = clamp((t - tg_t) / 0.5)
    ang = 0 if tg <= 0 else -30 * math.sin(min(1.0, tg) * math.pi)
    DC.glow_at(img, 600, 900, 380, (255, 210, 150), 0.14)
    paste(img, spr(gavel), 600, 960, 0.9, 1.0, ang)
    if t > tg_t + 0.25:
        kk = ease(clamp((t - tg_t - 0.25) / 0.25))
        st = Image.new("RGBA", (640, 220), (0, 0, 0, 0))
        sd = ImageDraw.Draw(st)
        sd.rounded_rectangle([20, 20, 620, 200], radius=18, outline=GREENC + (240,), width=10)
        sd.text((320, 112), "LEGAL", font=DC.caps_font(110, "ExtraBold"), fill=GREENC + (240,), anchor="mm")
        paste(img, st.rotate(-7, expand=True, resample=Image.BICUBIC), 600, 720, lerp(1.4, 0.9, kk), kk)
    DC.pill(img, 600, 1250, "ABRIL DE 2009", ease(clamp((t - 0.6) / 0.4)))


def _track(img, y0=900, y1=1130):
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, y0, W, y1], fill=(22, 26, 40, 255))
    d.line([(0, y0), (W, y0)], fill=(120, 128, 150, 160), width=3)
    d.line([(0, y1), (W, y1)], fill=(120, 128, 150, 160), width=3)
    for x in range(-40, W, 120):
        d.line([(x, (y0 + y1) / 2), (x + 60, (y0 + y1) / 2)], fill=(200, 205, 220, 90), width=4)


def sh_australia(img, t, T, L):
    DC.bg(img, t, 540, 1000, seed=15)
    _track(img)
    d = ImageDraw.Draw(img, "RGBA")
    for i in range(10):
        for j in range(2):
            col = (240, 240, 244, 255) if (i + j) % 2 else (18, 20, 28, 255)
            d.rectangle([860 + j * 23, 900 + i * 23, 883 + j * 23, 923 + i * 23], fill=col)
    k = ease(clamp((t - 0.1) / 1.4))
    paste(img, spr(bgp_side), lerp(-300, 640, k), 975, 0.5)
    paste(img, spr(bgp_side), lerp(-700, 320, k), 1060, 0.46)
    DC.pill(img, 640, 860, "1.º BUTTON", ease(clamp((t - 1.4) / 0.4)), col=GOLD)
    DC.pill(img, 320, 1190, "2.º BARRICHELLO", ease(clamp((t - 1.7) / 0.4)))
    DC.pill(img, 540, 1290, "AUSTRALIA · MARZO DE 2009", ease(clamp((t - 0.5) / 0.4)))


def sh_streak(img, t, T, L):
    DC.bg(img, t, 540, 860, seed=17)
    d = ImageDraw.Draw(img, "RGBA")
    races = ["AUS", "MAL", "CHN", "BHR", "ESP", "MON", "TUR"]
    for i, r in enumerate(races):
        k = ease(clamp((t - 0.2 - i * 0.24) / 0.3))
        if k <= 0:
            continue
        col_i, row = i % 4, i // 4
        x = 180 + col_i * 240 if row == 0 else 300 + col_i * 240
        y = 640 + row * 270
        won = r != "CHN"
        rad = 92 * lerp(0.6, 1.0, k)
        if won and k > 0.9:
            DC.glow_at(img, x, y, 140, (255, 200, 90), 0.25)
        d.ellipse([x - rad, y - rad, x + rad, y + rad], fill=(20, 26, 48, int(240 * k)),
                  outline=(GOLD if won else (120, 128, 150)) + (int(255 * k),), width=5)
        d.text((x, y - 16), r, font=DC.caps_font(40, "Bold"), fill=(246, 246, 250, int(255 * k)), anchor="mm")
        d.text((x, y + 32), "1.º" if won else "3.º", font=DC.font(DC.F_UI, 30), fill=(GOLD if won else (150, 156, 176)) + (int(255 * k),), anchor="mm")


def sh_cold(img, t, T, L):
    a1 = lt(L, 1)

    def A(im):
        DC.bg(im, t, 540, 860, seed=19)
        DC.dust(im, t, 60, 8, (230, 240, 255), 140, (0, 420, W, 1400), 40, (1.5, 3.5))
        DC.glow_at(im, 430, 860, 300, CY_, 0.25)
        paste(im, spr(tyre_cold), 430, 860, 0.85)
        lv = 0.15 + 0.05 * math.sin(t * 2)
        paste(im, spr(thermometer, round(lv, 2)), 820, 860, 0.85)
        k = ease(clamp((t - lt(L, 0, 0.6)) / 1.3))
        if k > 0:
            paste(im, spr(bgp_side, NAVY, (230, 40, 50)), lerp(1500, 560, k), 1190, 0.5, k)

    def Bf(im):
        DC.bg(im, t, 540, 860, seed=21)
        dd = ImageDraw.Draw(im, "RGBA")
        x0 = 170
        for i, (lbl, pts, col) in enumerate((("BUTTON", 95, GOLD), ("VETTEL", 84, (120, 140, 230)))):
            k = ease(clamp((t - a1 - 0.2 - i * 0.3) / 1.0))
            y = 700 + i * 230
            wbar = 740 * pts / 95 * k
            dd.rounded_rectangle([x0, y, x0 + max(24, wbar), y + 110], radius=18, fill=col + (255,))
            dd.text((x0, y - 34), lbl, font=DC.font(DC.F_UI, 32), fill=(220, 224, 236), anchor="lm")
            if k > 0.08:
                dd.text((x0 + wbar - 22, y + 56), f"{int(round(pts * k))} pts", font=DC.caps_font(50, "Bold"), fill=(16, 18, 28), anchor="rm")
        DC.pill(im, 620, 1250, "CLASIFICACIÓN FINAL 2009", ease(clamp((t - a1 - 1.2) / 0.4)))

    T2.xf(img, t, a1, A, Bf, 0.6)


def sh_brazil(img, t, T, L):
    DC.bg(img, t, 540, 960, seed=23)
    _track(img, 960, 1180)
    paste(img, spr(bgp_side), 560, 1060, 0.56)
    q = clamp((t - lt(L, 0, 0.36)) / max(0.6, lt(L, 0, 0.62) - lt(L, 0, 0.36)))   # sale 14.º y remonta cuando lo dice
    pos = int(round(lerp(14, 5, ease(q))))
    champ = t > lt(L, 0, 0.72)
    if not champ:
        DC.stamp_text(img, 540, 700, f"{pos}.º", 170, CREAM, ease(clamp((t - 0.3) / 0.4)))
        DC.pill(img, 540, 840, "POSICIÓN DE BUTTON", ease(clamp((t - 0.5) / 0.4)))
    else:
        kk = ease(clamp((t - lt(L, 0, 0.72)) / 0.4))
        DC.glow_at(img, 540, 720, 360, (255, 210, 110), 0.3 * kk)
        DC.stamp_text(img, 540, 700, "Campeón", 150, GOLD, kk)
        DC.pill(img, 540, 840, "JENSON BUTTON · 2009", kk)
        confetti(img, t, lt(L, 0, 0.72))
    DC.pill(img, 540, 1290, "BRASIL · 18 DE OCTUBRE DE 2009", ease(clamp((t - 0.4) / 0.4)))


def sh_titles(img, t, T, L):
    DC.bg(img, t, 560, 860, seed=25)
    DC.glow_at(img, 560, 860, 520, (255, 205, 120), 0.24)
    for i, (x, lbl) in enumerate(((400, "PILOTOS"), (740, "CONSTRUCTORES"))):
        k = ease(clamp((t - 0.2 - i * 0.45) / 0.6))
        paste(img, spr(trophy), x, lerp(940, 830, k), 0.85, k)
        DC.pill(img, x, 1100, lbl, k, size=22)


def sh_mercedes(img, t, T, L):
    DC.bg(img, t, 540, 900, seed=27)
    DC.glow_at(img, 540, 930, 480, (170, 230, 230), 0.14)
    k = ease(clamp((t - lt(L, 0, 0.25)) / 1.6))
    paste(img, spr(bgp_side), 540, 940, 0.82)
    if k > 0:
        paste(img, spr(bgp_side, SILVER, TEAL, INK), 540, 940, 0.82, k)
    DC.pill(img, 820, 520, "MERCEDES-BENZ", ease(clamp((t - 0.2) / 0.4)), col=TEAL)
    DC.dotted(img, (820, 560), (900, 700), (700, 840), ease(clamp((t - 0.4) / 1.2)), col=TEAL)
    DC.pill(img, 540, 1200, "75,1 % DEL EQUIPO", ease(clamp((t - lt(L, 0, 0.45)) / 0.4)))
    DC.stamp_text(img, 540, 1320, "≈ 110 M£", 70, GOLD, ease(clamp((t - lt(L, 0, 0.62)) / 0.4)), glow=False)


def sh_eight(img, t, T, L):
    DC.bg(img, t, 540, 860, seed=29)
    d = ImageDraw.Draw(img, "RGBA")
    for i in range(8):
        k = ease(clamp((t - 0.2 - i * 0.2) / 0.3))
        if k <= 0:
            continue
        col_i, row = i % 4, i // 4
        x = 165 + col_i * 250
        y = 660 + row * 380
        DC.glow_at(img, x, y, 120, (220, 230, 240), 0.12 * k)
        paste(img, spr(trophy), x, lerp(y + 50, y, k), 0.46, k)
        d.text((x, y + 160), str(2014 + i), font=DC.font(DC.F_UI, 32), fill=(214, 220, 234, int(255 * k)), anchor="mm")


def sh_final(img, t, T, L):
    DC.bg(img, t, 560, 900, seed=31)
    a, b = L[0]
    m = ease(clamp((t - a - (b - a) * 0.35) / ((b - a) * 0.6)))
    DC.glow_at(img, 560, 960, 460, (255, 240, 210), 0.14 + 0.1 * m)
    d = ImageDraw.Draw(img, "RGBA")
    d.ellipse([200, 1080, 960, 1130], fill=(0, 0, 0, 80))
    paste(img, spr(bgp_side), 580, 960, 0.86)
    if m > 0:
        paste(img, spr(bgp_side, SILVER, TEAL, INK), 580, 960, 0.86, m)
    ck = ease(clamp((t - 0.2) / 0.6)) * (1 - m)
    if ck > 0:
        paste(img, spr(coin), 580, 620, 0.36, ck)
        DC.dotted(img, (580, 690), (600, 780), (590, 860), ease(clamp((t - 0.5) / 0.9)))


import t02_microondas as T2  # noqa: E402  (fundido A→B dentro de un plano)

FNS = {k: globals()["sh_" + k] for k, *_ in SHOTS}
AUDIO = {
    "music": [("open", "premium"), ("honda", "mystery"), ("pound", "creative"), ("diffuser", "exp"), ("australia", "epic"),
              ("cold", "tension"), ("brazil", "epic"), ("mercedes", "premium")],
    "gains": {"exp": 0.6, "mystery": 0.7, "epic": 0.8, "tension": 0.75},
    "amb": {"road": ["australia", "brazil"], "hum": ["engine", "diffuser"], "wind": ["cold"], "crowd": ["brazil"]},
    "sfx": [("open+0.2", "whoosh", 0.07), ("honda+0.3", "paper", 0.1), ("pound+0.3", "ding", 0.07),
            ("engine+1.9", "thud", 0.12), ("livery+0.3", "whoosh_up", 0.07), ("diffuser+1.4", "click", 0.12),
            ("legal+0.2", "pop", 0.07), ("australia+0.1", "whoosh", 0.1), ("streak+0.2", "pop", 0.06),
            ("cold+0.3", "swell", 0.06), ("titles+0.2", "chime", 0.05), ("mercedes+0.6", "whoosh_up", 0.07),
            ("eight+0.2", "pop", 0.06), ("final+0.4", "swell", 0.1)],
    "bed": [],
    "bpm": 96,
}
