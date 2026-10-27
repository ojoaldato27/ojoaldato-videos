"""V10 · El disco de oro de la Voyager: el mensaje que mandamos a los extraterrestres."""
from cine import *

TITLE = "El_mensaje_que_mandamos_a_los_extraterrestres"
LINES = [
    "Ahora mismo, un disco de oro viaja por el espacio interestelar con un *mensaje para extraterrestres*.",
    "¿Qué les contamos sobre nosotros?",
    "5 de septiembre de 1977. Despega la sonda *Voyager 1*.",
    "Su misión: visitar Júpiter y Saturno… y seguir hacia las estrellas.",
    "Lleva pegado un *disco de cobre bañado en oro*.",
    "Un equipo dirigido por el astrónomo *Carl Sagan* eligió su contenido.",
    "Por si alguien lo encuentra, la tapa explica *cómo reproducirlo*.",
    "Y lleva *uranio*, para calcular cuánto tiempo lleva viajando.",
    "En 1990, la Voyager giró su cámara y fotografió la Tierra desde *6.000 millones de kilómetros*.",
    "Salimos como un puntito más pequeño que *un píxel*.",
    "Hoy sigue viajando… y el 18 de noviembre de 2026 estará a *un día luz* de nosotros.",
    "Su señal tardará *un día entero* en llegar.",
    "Dentro de unos *40.000 años*, pasará cerca de otra estrella.",
    "Entonces… ¿qué hay en el disco?",
    "Saludos en *55 idiomas*.",
    "*116 imágenes* de la Tierra y de nosotros.",
    "Música de todo el mundo… y *sonidos* de nuestro planeta.",
    "Un mensaje en una botella… lanzado al *océano cósmico*.",
]
SHOTS = [("open", 0, 1, 0.3), ("launch", 2, 3, 0.3), ("record", 4, 5, 0.3), ("cover", 6, 7, 0.3), ("pale", 8, 9, 0.5),
         ("lightday", 10, 11, 0.4), ("star", 12, 12, 0.3), ("question", 13, 13, 0.3), ("contents", 14, 16, 0.4),
         ("final", 17, 17, 1.8)]
FOCUS = {"open": (540, 900), "launch": (540, 900), "record": (560, 900), "cover": (540, 900), "pale": (600, 1000),
         "lightday": (520, 900), "contents": (540, 900), "final": (540, 900)}
NOTIF = ("record", 1.0)

GOLD = (222, 176, 76)


# ------------------------------------------------------------------ sprites
HYPE = {"line": 1, "text": ['¿QUÉ LES CONTAMOS', 'SOBRE NOSOTROS?'], "delay": [0, 0.7]}
STICKER_EXTRA = [('disco', '📀'), ('espacio', '🌌'), ('extraterrestre', '👽'), ('mensaje', '✉️'), ('sonda', '🛰️'), ('voyager', '🛰️'), ('jupiter', '🪐'), ('saturno', '🪐'), ('estrellas', '✨'), ('cobre', '📀'), ('astronomo', '🔭'), ('sagan', '🔭'), ('reproducir', '▶️'), ('uranio', '☢️'), ('tiempo', '⏳'), ('camara', '📸'), ('fotografi', '📸'), ('tierra', '🌍'), ('pixel', '🔍'), ('puntito', '🔍'), ('idiomas', '🗣️'), ('saludos', '👋'), ('imagenes', '🖼️'), ('musica', '🎵'), ('sonidos', '🔊'), ('botella', '🍾'), ('oceano', '🌊')]

def disc(r=360, cover=False):
    def fn(d, s):
        c = r + 10
        base, light, dark = ((150, 104, 40), (250, 214, 130), (120, 84, 30)) if cover else ((190, 140, 50), (250, 214, 130), (150, 104, 40))
        d.ellipse(sb([c - r, c - r, c + r, c + r], s), fill=base)
        if not cover:
            for i, k in enumerate(range(int(r * 0.3), int(r), 9)):
                d.ellipse(sb([c - k, c - k, c + k, c + k], s), outline=(165, 116, 38) if i % 2 else (236, 196, 112), width=max(1, int(2 * s)))
            d.ellipse(sb([c - r * 0.28, c - r * 0.28, c + r * 0.28, c + r * 0.28], s), fill=(220, 170, 70))
            d.ellipse(sb([c - 10, c - 10, c + 10, c + 10], s), fill=(40, 30, 20))
            for k in (0.55, 0.7, 0.85):
                d.arc(sb([c - r * k, c - r * k, c + r * k, c + r * k], s), 205, 245, fill=(255, 244, 210), width=int(5 * s))
        else:
            ln = (250, 220, 150)
            w_ = max(1, int(2.5 * s))
            d.ellipse(sb([c - r * 0.85, c - r * 0.85, c - r * 0.15, c - r * 0.15], s), outline=ln, width=w_)
            d.ellipse(sb([c - r * 0.55, c - r * 0.55, c - r * 0.45, c - r * 0.45], s), outline=ln, width=w_)
            d.line(sc([(c - r * 0.5, c - r * 0.5), (c - r * 0.2, c - r * 0.75)], s), fill=ln, width=w_)
            d.ellipse(sb([c + r * 0.15, c - r * 0.85, c + r * 0.85, c - r * 0.15], s), outline=ln, width=w_)
            for k in range(6):
                d.line(sc([(c + r * 0.25, c - r * (0.8 - k * 0.11)), (c + r * 0.75, c - r * (0.8 - k * 0.11))], s), fill=ln, width=w_)
            cx2, cy2 = c - r * 0.4, c + r * 0.45
            rr = random.Random(4)
            for k in range(14):
                a = rr.uniform(0, 2 * math.pi)
                L_ = rr.uniform(0.15, 0.38) * r
                d.line(sc([(cx2, cy2), (cx2 + math.cos(a) * L_, cy2 + math.sin(a) * L_)], s), fill=ln, width=w_)
            for dx in (0.25, 0.45):
                d.ellipse(sb([c + r * dx - 16, c + r * 0.45 - 16, c + r * dx + 16, c + r * 0.45 + 16], s), outline=ln, width=w_)
            d.line(sc([(c + r * 0.25, c + r * 0.45), (c + r * 0.45, c + r * 0.45)], s), fill=ln, width=w_)
    return sprite(("disc", r, cover), 2 * r + 20, 2 * r + 20, fn)


def voyager():
    def fn(d, s):
        wh, gr, dk = (236, 236, 232), (170, 172, 180), (60, 62, 70)
        d.line(sc([(420, 380), (900, 160)], s), fill=gr, width=int(5 * s))
        d.line(sc([(380, 420), (80, 640)], s), fill=gr, width=int(9 * s))
        d.rectangle(sb([60, 620, 120, 700], s), fill=dk)
        d.polygon(sc([(330, 360), (460, 360), (500, 430), (460, 500), (330, 500), (290, 430)], s), fill=(120, 110, 90))
        d.ellipse(sb([450, 420, 520, 490], s), fill=GOLD)
        d.ellipse(sb([170, 120, 620, 360], s), fill=wh)
        d.ellipse(sb([200, 140, 590, 330], s), fill=(214, 214, 210))
        d.line(sc([(395, 240), (395, 360)], s), fill=gr, width=int(6 * s))
        d.line(sc([(395, 240), (395, 160)], s), fill=gr, width=int(4 * s))
    return sprite("voyager", 920, 720, fn)


def jupiter(r=300):
    def fn(d, s):
        c = r
        cols = [(214, 180, 140), (190, 140, 100), (230, 210, 180), (170, 120, 90), (220, 190, 150), (200, 150, 110)]
        d.ellipse(sb([0, 0, 2 * r, 2 * r], s), fill=cols[0])
        for i in range(12):
            y0 = i * 2 * r / 12
            d.rectangle(sb([0, y0, 2 * r, y0 + 2 * r / 12], s), fill=cols[i % len(cols)] + (255,))
        m = Image.new("L", (2 * r * s, 2 * r * s), 0)
        ImageDraw.Draw(m).ellipse([0, 0, 2 * r * s, 2 * r * s], fill=255)
        d.ellipse(sb([r * 1.1, r * 1.25, r * 1.45, r * 1.42], s), fill=(200, 110, 80))
        d._image.putalpha(m)
    return sprite(("jup", r), 2 * r, 2 * r, fn)


def saturn(r=170):
    def fn(d, s):
        cx, cy = 3 * r, 1.4 * r
        d.ellipse(sb([cx - r * 2.6, cy - r * 0.7, cx + r * 2.6, cy + r * 0.7], s), outline=(220, 200, 160), width=int(r * 0.22 * s))
        d.ellipse(sb([cx - r, cy - r, cx + r, cy + r], s), fill=(226, 200, 150))
        d.rectangle(sb([cx - r, cy - r * 0.2, cx + r, cy - r * 0.05], s), fill=(200, 170, 120))
        d.chord(sb([cx - r * 2.6, cy - r * 0.7, cx + r * 2.6, cy + r * 0.7], s), 0, 180, outline=(220, 200, 160), width=int(r * 0.22 * s))
    return sprite(("sat", r), 6 * r, int(2.8 * r), fn)


def titan_rocket():
    def fn(d, s):
        wh, rd = (230, 230, 226), (60, 60, 66)
        d.rectangle(sb([90, 200, 150, 900], s), fill=wh)
        d.polygon(sc([(90, 200), (150, 200), (120, 80)], s), fill=wh)
        for sgn in (-1, 1):
            x = 120 + sgn * 60
            d.rectangle(sb([x - 22, 420, x + 22, 900], s), fill=rd)
            d.polygon(sc([(x - 22, 420), (x + 22, 420), (x, 360)], s), fill=rd)
    return sprite("titan", 240, 910, fn)


# ------------------------------------------------------------------ planos
def sh_open(img, t, T, L):
    space_bg(img, t, 21, ((60, 40, 120), (20, 70, 120)), 420, (-10, 0))
    rot = t * 6
    paste(img, glow(400, (255, 210, 130), 0.4), 540, 900)
    paste(img, disc(), 540, 900, 1.05, 1.0, rot)
    title2(t, 0.25, "UN MENSAJE PARA", "EXTRATERRESTRES", 260, 56, 84, hold=max(1.5, L[1][0] - 0.3))
    vignette(img, 180)


def sh_launch(img, t, T, L):
    a1 = L[1][0]
    if t < a1:
        sky(img, (40, 50, 110), (250, 150, 100), 1.3)
        q = ease(clamp((t - 0.4) / max(1, a1 - 0.4)))
        ry = 1260 - 700 * q * q
        smoke(img, t, [(440, 1500, 2.2), (640, 1500, 2.2)], col=(230, 220, 210), alpha=190, spread=(0, -40), grow=140, speed=0.25)
        from v05_apolo import flame
        flame(img, t, 540, ry + 460, 1.0)
        paste(img, titan_rocket(), 540, ry)
        ground(img, 1500, (40, 40, 44), (14, 14, 16))
        date_stamp(t, 0.3, "05 · 09 · 1977", 300)
    else:
        space_bg(img, t, 22)
        u = t - a1
        paste(img, jupiter(), 1100 - u * 120, 760, 1.0)
        paste(img, saturn(), 300 - u * 60, 1320, 0.8)
        paste(img, voyager(), 520 + u * 30, 1000 - u * 20, 0.6, 1.0, -8)
        lower_third(img, t, a1 + 0.3, "JÚPITER · SATURNO", "Y DESPUÉS, LAS ESTRELLAS", 300, 3.2)
    vignette(img, 160)


def sh_record(img, t, T, L):
    space_bg(img, t, 23)
    paste(img, voyager(), 300, 1300, 1.0, 0.6)
    paste(img, glow(380, (255, 210, 130), 0.5), 580, 860)
    paste(img, disc(), 580, 860, 0.95, 1.0, t * 5)
    lower_third(img, t, 0.3, "30 CM · COBRE Y ORO", "", 300, max(2.0, L[1][0] - 0.6))
    lower_third(img, t, L[1][0] + 0.3, "CARL SAGAN", "DIRIGIÓ LA SELECCIÓN", 300, 3.4)
    vignette(img, 180)


def sh_cover(img, t, T, L):
    space_bg(img, t, 24)
    paste(img, disc(360, True), 540, 900, 1.0)
    a1 = L[1][0]
    big(t, 0.3, "INSTRUCCIONES", 300, 90, YEL, hold=max(1.4, a1 - 0.6), pop=False)
    if t > a1:
        cx, cy = 540 + 360 * 0.35, 900 + 360 * 0.45
        paste(img, glow(90, (120, 255, 140), 1.0), cx, cy, 1.0, 0.6 + 0.4 * math.sin(t * 5) ** 2)
        big(t, a1 + 0.3, "URANIO-238", 300, 96, (140, 255, 160), sub="UN RELOJ DE MILLONES DE AÑOS", subcol=WHITE)
    vignette(img, 180)


def sh_pale(img, t, T, L):
    sky(img, (6, 4, 4), (2, 2, 2), 1.0)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for k, (x, col, a) in enumerate(((240, (190, 120, 70), 90), (480, (170, 110, 80), 70), (760, (200, 140, 90), 80))):
        d.polygon([(x - 50, 0), (x + 50, 0), (x + 170, H), (x + 60, H)], fill=col + (a,))
    AC(img, im.filter(ImageFilter.GaussianBlur(26)))
    stars(img, t, H, 0.25, 50, 9)
    q = ease(clamp((t - 0.4) / 2.0))
    px, py = 560 + 180 * 0.4, 1060
    paste(img, glow(40, (140, 180, 255), 1.0), px, py, 1.0, 0.5 + 0.5 * math.sin(t * 3) ** 2)
    d2 = ImageDraw.Draw(img)
    d2.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(170, 200, 255))
    if t > 1.2:
        k = ease(clamp((t - 1.2) / 0.6))
        d3 = ImageDraw.Draw(img, "RGBA")
        d3.ellipse([px - 46, py - 46, px + 46, py + 46], outline=(255, 255, 255, int(200 * k)), width=4)
        d3.line([(px + 34, py - 34), (px + 140, py - 140)], fill=(255, 255, 255, int(200 * k)), width=4)
        dd = td()
        dd.text((px + 130, py - 200), "LA TIERRA", font=f(F_SER, 42), fill=(255, 255, 255, int(255 * k)))
    date_stamp(t, 0.3, "14 · 02 · 1990", 300, max(1.6, L[1][0] - 0.4))
    big(t, L[1][0] + 0.3, "MENOS DE 1 PÍXEL", 300, 90, YEL, pop=False)
    vignette(img, 160)


def sh_lightday(img, t, T, L):
    space_bg(img, t, 25, ((40, 30, 80), (20, 40, 80)), 420, (-14, 0))
    paste(img, glow(60, (255, 240, 200), 1.0), 140, 1300)
    paste(img, voyager(), 620 + t * 10, 840, 0.75, 1.0, -6)
    a1 = L[1][0]
    if t < a1:
        big(t, 0.4, "1 DÍA LUZ", 290, 120, YEL, sub="18 · 11 · 2026")
        dd = td()
        k = ease(clamp((t - 1.4) / 0.6))
        spaced(dd, W / 2, 1270, "≈ 25.900 MILLONES DE KM", f(F_SER, 44), (230, 230, 240, int(255 * k)), 4)
    else:
        d = ImageDraw.Draw(img, "RGBA")
        for k in range(6):
            ph = ((t - a1) * 0.35 + k / 6) % 1.0
            x = lerp(560, 160, ph)
            y = lerp(900, 1300, ph)
            r = 30 + ph * 80
            d.arc([x - r, y - r, x + r, y + r], 100, 200, fill=(120, 220, 255, int(230 * (1 - ph))), width=6)
        big(t, a1 + 0.2, "24 HORAS", 300, 120, (140, 220, 255), sub="TARDA SU SEÑAL")
    vignette(img, 170)


def sh_star(img, t, T, L):
    space_bg(img, t, 26, ((60, 30, 70), (30, 30, 70)), 420, (-20, 0))
    k = ease(clamp(t / T))
    paste(img, glow(int(120 + 160 * k), (255, 200, 160), 1.0), 760, 760)
    paste(img, voyager(), 380, 1100, 0.45, 1.0, -6)
    big(t, 0.3, "40.000 AÑOS", 300, 110, YEL, sub="HASTA OTRA ESTRELLA")
    vignette(img, 170)


def sh_question(img, t, T, L):
    space_bg(img, t, 27)
    paste(img, glow(380, (255, 210, 130), 0.6), 540, 900, 1.0, 0.6 + 0.4 * math.sin(t * 4) ** 2)
    paste(img, disc(), 540, 900, 0.9, 1.0, t * 8)
    vignette(img, 190)


HELLOS = ["HOLA", "HELLO", "BONJOUR", "CIAO", "OLÁ", "PRIVET", "SALAAM", "NAMASTE", "KONNICHIWA", "NI HAO", "SHALOM", "JAMBO",
          "HALLO", "AHOJ", "MERHABA", "ANNYEONG"]


def sh_contents(img, t, T, L):
    space_bg(img, t, 28)
    paste(img, disc(), 540, 900, 0.8, 0.35, t * 4)
    a1, a2 = L[1][0], L[2][0]
    dd = td()
    if t < a1:
        rr = random.Random(3)
        for i, h_ in enumerate(HELLOS):
            t0 = 0.3 + i * 0.12
            k = ease(clamp((t - t0) / 0.4))
            if k <= 0:
                continue
            ang = rr.uniform(0, 2 * math.pi)
            rad = rr.uniform(160, 420)
            x, y = 540 + math.cos(ang) * rad, 900 + math.sin(ang) * rad * 1.1
            sz = rr.choice([40, 48, 56])
            tw = dd.textlength(h_, font=f(F_SER, sz))
            dd.rounded_rectangle([x - tw / 2 - 18, y - 12, x + tw / 2 + 18, y + sz + 12], radius=20, fill=(255, 255, 255, int(220 * k)))
            dd.text((x - tw / 2, y), h_, font=f(F_SER, sz), fill=(30, 30, 40, int(255 * k)))
        big(t, 0.2, "55 IDIOMAS", 260, 96, YEL, pop=False)
    elif t < a2:
        n = int(clamp((t - a1) / 1.6) * 116)
        rr = random.Random(5)
        for i in range(n):
            col_, row = i % 10, i // 10
            x, y = 130 + col_ * 84, 520 + row * 74
            c = rr.choice([(90, 150, 210), (110, 170, 90), (210, 160, 90), (200, 110, 110), (160, 120, 200)])
            dd.rounded_rectangle([x, y, x + 70, y + 58], radius=6, fill=c + (255,))
            dd.rectangle([x + 8, y + 30, x + 62, y + 50], fill=tuple(min(255, v + 40) for v in c) + (255,))
        big(t, a1 + 0.1, counter(t, a1, a1 + 1.6, 0, 116) + " IMÁGENES", 300, 92, YEL, pop=False)
    else:
        d = ImageDraw.Draw(img, "RGBA")
        for k in range(5):
            pts = [(x, 900 + math.sin(x / 40 + t * 4 + k) * (40 + k * 18) * math.sin(x / W * math.pi)) for x in range(80, W - 80, 10)]
            d.line(pts, fill=(255, 210, 120, 200 - k * 30), width=6 - k)
        rr = random.Random(8)
        for k in range(8):
            ph = ((t - a2) * 0.4 + k / 8) % 1.0
            x = rr.uniform(150, 930)
            y = 1300 - ph * 700
            a = int(255 * (1 - ph))
            dd.ellipse([x - 22, y - 16, x + 10, y + 12], fill=(255, 255, 255, a))
            dd.line([(x + 8, y), (x + 8, y - 70)], fill=(255, 255, 255, a), width=6)
            dd.line([(x + 8, y - 70), (x + 34, y - 54)], fill=(255, 255, 255, a), width=6)
        big(t, a2 + 0.1, "MÚSICA", 300, 100, YEL, sub="Y SONIDOS DE LA TIERRA")
    vignette(img, 180)


def sh_final(img, t, T, L):
    space_bg(img, t, 29, ((40, 30, 90), (20, 60, 110)), 420, (-12, 0))
    paste(img, voyager(), 560 + t * 14, 900, 0.8, 1.0, -6 + t)
    vignette(img, 170)


FNS = {k: globals()["sh_" + k] for k, *_ in SHOTS}
AUDIO = {
    "music": [("open", "space"), ("launch", "epic"), ("record", "space"), ("pale", "drone"), ("lightday", "space"),
              ("question", "drone"), ("contents", "warm"), ("final", "space")],
    "gains": {"warm": 1.0},
    "amb": {"space": ["open", "record", "cover", "pale", "lightday", "star", "question", "contents", "final"]},
    "sfx": [("open+0.3", "chime", 0.06), ("launch+0.4", "boom", 0.4), ("launch+0.5", "rumble", 0.35), ("launch@L1", "whoosh", 0.15),
            ("record+0.2", "swell", 0.15), ("cover+0.3", "ding", 0.06), ("cover@L1+0.3", "beep", 0.08), ("cover@L1+0.6", "beep", 0.08),
            ("pale+0.4", "static", 0.08), ("pale+1.2", "shutter", 0.25), ("pale@L1+0.3", "swell", 0.15),
            ("lightday+0.4", "riser", 0.12), ("lightday+1.4", "impact", 0.2), ("lightday@L1+0.2", "beep", 0.1),
            ("lightday@L1+1.2", "beep", 0.1), ("lightday@L1+2.2", "beep", 0.1),
            ("star+0.3", "swell", 0.15), ("question", "heart", 0.3), ("question+0.75", "heart", 0.3),
            ("contents+0.2", "pop", 0.15), ("contents+0.6", "pop", 0.15), ("contents+1.0", "pop", 0.15),
            ("contents@L1", "shutter", 0.15), ("contents@L2", "chime", 0.06), ("final+0.3", "chime", 0.05)],
    "bed": [("record", "pale"), ("contents", "end")],
    "bpm": 88,
}
