"""V04 · Hachikō, el perro que nunca dejó de esperar."""
from cine import *

TITLE = "Hachiko_el_perro_que_nunca_dejo_de_esperar"
LINES = [
    "En una de las estaciones más concurridas del mundo hay una estatua… de un *perro*.",
    "¿Qué hizo para merecerla?",
    "Tokio, 1924.",
    "El profesor *Hidesaburō Ueno* adopta un cachorro de raza akita.",
    "Lo llama *Hachikō*.",
    "Cada tarde, Hachikō le espera a la vuelta del trabajo en la estación de *Shibuya*.",
    "Hasta que un día de mayo de 1925… el profesor *no vuelve*.",
    "Había muerto de repente, en el trabajo.",
    "Pero Hachikō no lo sabía.",
    "Al día siguiente volvió a la estación… y al otro… y al otro.",
    "Llovía, nevaba… y él seguía *esperando*.",
    "En 1932, un periódico cuenta su historia.",
    "Y todo Japón *se enamora* de él.",
    "En 1934 le hacen una estatua… y *él mismo* asiste a la inauguración.",
    "Hachikō murió en marzo de 1935.",
    "Había esperado *casi diez años*.",
    "En 2015, en la universidad del profesor, pusieron otra estatua…",
    "…en la que, por fin, *se reencuentran*.",
    "La historia del perro que *nunca dejó de esperar*.",
]
SHOTS = [("open", 0, 1, 0.3), ("tokyo", 2, 4, 0.3), ("station", 5, 5, 0.3), ("notcome", 6, 7, 0.4), ("waiting", 8, 10, 0.4),
         ("news", 11, 12, 0.3), ("statue", 13, 13, 0.4), ("death", 14, 15, 0.8), ("reunion", 16, 17, 0.6), ("final", 18, 18, 2.0)]
FOCUS = {"open": (540, 1080), "tokyo": (600, 1050), "station": (620, 1120), "notcome": (600, 1150), "waiting": (560, 1150),
         "news": (540, 900), "statue": (560, 1000), "death": (540, 1050), "reunion": (540, 960), "final": (540, 1080)}
NOTIF = ("station", 1.0)

CREAM = (236, 222, 196)
BRONZE = (120, 92, 54)


# ------------------------------------------------------------------ sprites
HYPE = {"line": 1, "text": ['¿QUÉ HIZO', 'PARA MERECERLA?'], "delay": [0, 0.6]}
STICKER_EXTRA = [('perro', '🐕'), ('estatua', '🗿'), ('estacion', '🚉'), ('tokio', '🏯'), ('profesor', '🎓'), ('cachorro', '🐶'), ('akita', '🐕'), ('tarde', '🌇'), ('trabajo', '💼'), ('muerto', '💔'), ('llovia', '🌧️'), ('nevaba', '❄️'), ('esperando', '⏳'), ('espera', '⏳'), ('periodico', '📰'), ('enamora', '❤️'), ('inaugura', '🎉'), ('murio', '🕯️'), ('anos', '⏳'), ('universidad', '🎓'), ('reencuentran', '🤝')]

def dog(col=CREAM, shade=None, w=400, h=420):
    sh_ = shade or tuple(max(0, c - 40) for c in col)

    def fn(d, s):
        d.ellipse(sb([70, 220, 250, 380], s), fill=sh_)
        d.polygon(sc([(150, 230), (215, 110), (275, 120), (290, 250), (250, 330), (160, 330)], s), fill=col)
        d.ellipse(sb([215, 60, 320, 160], s), fill=col)
        d.polygon(sc([(295, 100), (366, 118), (362, 150), (300, 156)], s), fill=col)
        d.ellipse(sb([350, 112, 372, 132], s), fill=(30, 26, 24))
        d.polygon(sc([(230, 92), (244, 26), (276, 82)], s), fill=col)
        d.polygon(sc([(268, 78), (292, 30), (306, 92)], s), fill=col)
        d.polygon(sc([(240, 80), (247, 46), (264, 78)], s), fill=sh_)
        d.ellipse(sb([290, 92, 302, 104], s), fill=(30, 26, 24))
        d.rectangle(sb([238, 240, 262, 392], s), fill=col)
        d.rectangle(sb([268, 236, 292, 392], s), fill=sh_)
        d.ellipse(sb([226, 378, 272, 402], s), fill=col)
        d.ellipse(sb([258, 378, 304, 402], s), fill=sh_)
        d.ellipse(sb([90, 360, 190, 404], s), fill=sh_)
        d.arc(sb([50, 150, 160, 260], s), 160, 380, fill=col, width=int(26 * s))
        d.line(sc([(240, 160), (300, 170)], s), fill=(160, 40, 40), width=int(8 * s))
    return sprite(("dog", col), w, h, fn)


def pedestal():
    def fn(d, s):
        d.rectangle(sb([20, 0, 380, 260], s), fill=(90, 86, 84))
        d.rectangle(sb([0, 240, 400, 300], s), fill=(70, 66, 64))
        d.rectangle(sb([40, 20, 360, 30], s), fill=(120, 116, 112))
    return sprite("ped", 400, 300, fn)


def sakura(seed=1):
    def fn(d, s):
        trunk = (40, 28, 30)
        d.polygon(sc([(280, 900), (320, 900), (330, 500), (300, 380), (270, 500)], s), fill=trunk)
        for a, L_ in ((-0.9, 260), (-0.4, 220), (0.3, 240), (0.8, 260)):
            d.line(sc([(300, 520), (300 + math.sin(a) * L_, 520 - math.cos(a) * L_)], s), fill=trunk, width=int(22 * s))
        rr = random.Random(seed)
        for _ in range(140):
            x, y = rr.gauss(300, 170), rr.gauss(300, 110)
            r = rr.uniform(30, 70)
            c = rr.choice([(244, 184, 200), (250, 206, 216), (232, 160, 182)])
            d.ellipse(sb([x - r, y - r, x + r, y + r], s), fill=c)
    return sprite(("sakura", seed), 600, 900, fn)


def old_station():
    def fn(d, s):
        wall, roof, wood = (150, 120, 90), (50, 44, 48), (90, 64, 44)
        d.rectangle(sb([60, 260, 1020, 640], s), fill=wall)
        d.polygon(sc([(20, 270), (1060, 270), (980, 180), (100, 180)], s), fill=roof)
        d.polygon(sc([(380, 190), (700, 190), (540, 70)], s), fill=roof)
        d.ellipse(sb([500, 110, 580, 190], s), fill=(240, 236, 220))
        d.line(sc([(540, 150), (540, 124)], s), fill=(30, 30, 30), width=int(4 * s))
        d.line(sc([(540, 150), (560, 156)], s), fill=(30, 30, 30), width=int(4 * s))
        for x in range(100, 1000, 120):
            d.rectangle(sb([x, 320, x + 70, 430], s), fill=(255, 214, 150))
            d.rectangle(sb([x - 8, 260, x, 640], s), fill=wood)
        d.rectangle(sb([420, 460, 660, 640], s), fill=(40, 30, 26))
    return sprite("station", 1080, 640, fn)


def shibuya():
    def fn(d, s):
        rr = random.Random(5)
        x = -20
        while x < W:
            bw = rr.uniform(130, 260)
            bh = rr.uniform(450, 760)
            d.rectangle(sb([x, 1100 - bh, x + bw, 1100], s), fill=(20, 18, 32))
            for wy in range(int(1100 - bh + 30), 1080, 40):
                for wx in range(int(x + 14), int(x + bw - 20), 28):
                    if rr.random() < 0.25:
                        d.rectangle(sb([wx, wy, wx + 12, wy + 18], s), fill=(240, 230, 255))
            if rr.random() < 0.8:
                c = rr.choice([(255, 60, 140), (60, 200, 255), (255, 200, 60), (140, 255, 120)])
                sy = 1100 - bh + rr.uniform(60, 300)
                d.rectangle(sb([x + 10, sy, x + bw - 10, sy + rr.uniform(80, 200)], s), fill=c)
            x += bw + rr.uniform(6, 20)
    return sprite("shibuya", W, 1100, fn)


# ------------------------------------------------------------------ utilidades
def crowd_walk(img, t, y, n=14, seed=3, speed=60, col=(10, 10, 16), scale=0.7):
    rr = random.Random(seed)
    for i in range(n):
        x0 = rr.uniform(0, W)
        v = rr.choice([-1, 1]) * rr.uniform(0.6, 1.2) * speed
        x = (x0 + v * t) % (W + 200) - 100
        yy = y + rr.uniform(-20, 40)
        paste(img, spr(person, 200, 520, col, rr.choice([None, "cap", None]), rr.random() < 0.5, rr.random() < 0.3, 0.0,
                       round((t * 5 + i) % 6.28, 1)), x, yy, scale * (0.9 + (yy - y) / 400), flip=v < 0)


def weather(img, t, kind, k=1.0):
    d = ImageDraw.Draw(img, "RGBA")
    rr = random.Random(9 if kind == "rain" else 10)
    if kind == "rain":
        for _ in range(int(220 * k)):
            x = rr.uniform(0, W)
            y = (rr.uniform(0, H) + t * 1100) % H
            d.line([(x, y), (x - 10, y + 44)], fill=(190, 200, 230, 190), width=3)
    elif kind == "snow":
        for _ in range(int(140 * k)):
            x0 = rr.uniform(0, W)
            y = (rr.uniform(0, H) + t * rr.uniform(60, 140)) % H
            x = x0 + math.sin(t + x0) * 20
            r = rr.uniform(2, 6)
            d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, 220))
    elif kind == "petals":
        for _ in range(int(60 * k)):
            x0 = rr.uniform(0, W)
            y = (rr.uniform(0, H) + t * rr.uniform(50, 110)) % H
            x = x0 + math.sin(t * 1.3 + x0) * 40
            r = rr.uniform(4, 8)
            d.ellipse([x - r, y - r * 0.6, x + r, y + r * 0.6], fill=(250, 196, 210, 230))


# ------------------------------------------------------------------ planos
def _topshade():
    ys = np.arange(H)
    a = (np.clip((760 - ys) / 760, 0, 1) ** 1.3 * 235).astype(np.uint8)
    v = Image.new("RGBA", (W, H), (8, 6, 20, 0))
    v.putalpha(Image.fromarray(np.repeat(a[:, None], W, axis=1), "L"))
    return v


def sh_open(img, t, T, L):
    night_sky(img, t, 400, 0.4, (10, 6, 24), (40, 20, 60))
    paste(img, shibuya(), 540, 900)
    ground(img, 1200, (34, 30, 44), (14, 12, 18))
    d = ImageDraw.Draw(img, "RGBA")
    for k in range(9):
        x = -40 + k * 140
        d.polygon([(x, 1520), (x + 80, 1520), (x + 60, 1400), (x + 10, 1400)], fill=(200, 200, 210, 120))
    AC(img, cached(("topshade",), lambda: _topshade()))
    crowd_walk(img, t, 1300, 16, 3, 70)
    spotlight(img, t, 540, 600, 1300, 60, 260, 70, dust=False)
    paste(img, pedestal(), 540, 1260 - 150, 0.7)
    paste(img, dog(BRONZE), 540, 1260 - 300 - 140, 0.75)
    title2(t, 0.25, "SHIBUYA · TOKIO", "UN PERRO DE BRONCE", 280, 50, 80, hold=max(1.6, L[1][0] - 0.3))
    vignette(img, 170)


def sh_tokyo(img, t, T, L):
    sky(img, (150, 180, 220), (250, 226, 214), 1.2)
    clouds(img, t, 640, (255, 255, 255), 110, 8, 3, 1.0)
    ground(img, 1300, (120, 140, 90), (70, 84, 56))
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([520, 900, 1080, 1300], fill=(170, 140, 110))
    d.polygon([(480, 910), (1120, 910), (1040, 780), (560, 780)], fill=(50, 44, 50))
    d.rectangle([640, 1050, 760, 1300], fill=(80, 60, 44))
    d.rectangle([840, 980, 980, 1100], fill=(230, 220, 190))
    paste(img, sakura(), 200, 1300 - 450, 1.0)
    weather(img, t, "petals", 0.6)
    paste(img, spr(person, 240, 600, (40, 34, 38), "bowler", True, False, 0.5), 480, 1230, 1.1)
    paste(img, dog(), 590, 1290, 0.32)
    date_stamp(t, 0.3, "TOKIO · 1924", 300, max(1.4, L[1][0] - 0.2))
    lower_third(img, t, L[1][0] + 0.2, "HIDESABURŌ UENO", "PROFESOR DE AGRICULTURA", 300, L[1][1] - L[1][0] - 0.9)
    big(t, L[2][0] + 0.1, "HACHIKŌ", 300, 140, YEL)
    vignette(img, 150)


def station_scene(img, t, dusk=True, lights=True):
    if dusk:
        sky(img, (60, 50, 100), (255, 160, 110), 1.3)
        paste(img, glow(380, (255, 180, 120), 0.7), 860, 900)
    else:
        night_sky(img, t, 900, 0.8, (6, 8, 22), (30, 30, 60))
    paste(img, old_station(), 540, 1300 - 320)
    ground(img, 1300, (90, 80, 76), (40, 36, 34))
    if lights:
        for x in (120, 960):
            ImageDraw.Draw(img).line([(x, 1300), (x, 1000)], fill=(30, 26, 26), width=10)
            paste(img, glow(110, (255, 220, 160), 1.0), x, 990)


def sh_station(img, t, T, L):
    station_scene(img, t, True)
    paste(img, dog(), 700, 1270, 0.56)
    a0 = 1.6
    x = lerp(1200, 820, ease(clamp((t - a0) / 2.2)))
    paste(img, spr(person, 240, 600, (40, 34, 38), "bowler", True, False, 0.0, round((t * 5) % 6.28, 1)), x, 1180, 1.0, flip=True)
    lower_third(img, t, 0.3, "ESTACIÓN DE SHIBUYA", "CADA TARDE", 300, max(2.2, T - 1.0))
    vignette(img, 160)


def sh_notcome(img, t, T, L):
    station_scene(img, t, False)
    crowd_walk(img, t, 1240, 8, 4, 90, (12, 12, 18), 0.75) if t < L[0][1] else None
    paste(img, dog(), 700, 1270, 0.56)
    date_stamp(t, 0.3, "MAYO DE 1925", 300, max(2.0, L[0][1] - 0.3))
    vignette(img, 210)


def sh_waiting(img, t, T, L):
    a1, a2 = L[1][0], L[2][0]
    night = t < a1
    station_scene(img, t, not night)
    snow_k = clamp((t - a2 - 1.4) / 1.0)
    if snow_k > 0:
        ground(img, 1300, (220, 224, 236), (170, 176, 196))
    paste(img, dog(), 700, 1270, 0.56)
    if a1 <= t:
        weather(img, t, "rain", 1 - snow_k)
        weather(img, t, "snow", snow_k)
        overlay(img, (30, 40, 70), 0.25)
    days = counter(t, a1, T - 0.5, 1, 3500)
    if t > a1:
        big(t, a1, "DÍA " + days, 300, 100, YEL, pop=False)
    vignette(img, 200)


def sh_news(img, t, T, L):
    sky(img, (30, 26, 22), (10, 8, 6), 1.0)
    spotlight(img, t, 540, 0, 1400, 150, 620, 50)
    paste(img, spr(newspaper, "EL PERRO\nQUE ESPERA", "Diario de Tokio", "TOKIO · 1932", 700, 900, 4), 540, 940, 1.0, 1.0, -3)
    if t > L[1][0]:
        d = ImageDraw.Draw(img, "RGBA")
        rr = random.Random(2)
        for k in range(14):
            ph = ((t - L[1][0]) * 0.4 + k / 14) % 1.0
            x = rr.uniform(120, 960) + math.sin(t * 2 + k) * 20
            y = 1400 - ph * 1100
            r = 24 * (1 - ph * 0.3)
            a = int(230 * (1 - ph))
            d.ellipse([x - r, y - r, x, y], fill=(240, 80, 110, a))
            d.ellipse([x, y - r, x + r, y], fill=(240, 80, 110, a))
            d.polygon([(x - r, y - r / 2), (x + r, y - r / 2), (x, y + r * 0.8)], fill=(240, 80, 110, a))
        big(t, L[1][0] + 0.2, "TODO JAPÓN", 300, 96, WHITE, pop=False)
    vignette(img, 200)


def sh_statue(img, t, T, L):
    station_scene(img, t, True)
    paste(img, pedestal(), 460, 1290 - 105, 0.7)
    paste(img, dog(BRONZE), 460, 1290 - 210 - 140, 0.75)
    q = ease(clamp((t - 0.8) / 1.0))
    if q < 1:
        d = ImageDraw.Draw(img, "RGBA")
        d.rectangle([300, 820 + 420 * q, 620, 1260], fill=(160, 30, 40, 255))
    paste(img, dog(), 780, 1270, 0.52)
    for x in (120, 960):
        paste(img, spr(person, 220, 560, (24, 20, 26), "bowler", True), x, 1180, 0.85)
    date_stamp(t, 0.3, "ABRIL DE 1934", 300)
    vignette(img, 160)


def sh_death(img, t, T, L):
    station_scene(img, t, False)
    weather(img, t, "petals", 1.0)
    paste(img, glow(160, (255, 230, 200), 0.6), 700, 1240, 1.0, 0.5)
    k = 1 - ease(clamp((t - 0.6) / 1.6))
    paste(img, dog(), 700, 1270, 0.56, k)
    date_stamp(t, 0.3, "MARZO DE 1935", 300, max(1.4, L[1][0] - 0.4))
    big(t, L[1][0] + 0.3, "CASI 10 AÑOS", 300, 110, YEL)
    vignette(img, 210)


def sh_reunion(img, t, T, L):
    sky(img, (110, 140, 190), (250, 214, 180), 1.3)
    paste(img, glow(460, (255, 220, 170), 0.8), 540, 900)
    ground(img, 1330, (110, 120, 90), (60, 66, 50))
    paste(img, sakura(3), 120, 1330 - 450, 0.9)
    paste(img, pedestal(), 540, 1330 - 120, 0.9)
    paste(img, spr(person, 260, 640, BRONZE, "bowler", True, False, -0.6), 640, 1330 - 240 - 300, 1.15, flip=True)
    paste(img, dog(BRONZE), 420, 1330 - 240 - 200, 0.7, 1.0, 28)
    rays(img, t, 540, 820, 12, (255, 236, 200), 20, 1200, 0.07, 0.03)
    lower_third(img, t, 0.3, "UNIVERSIDAD DE TOKIO", "2015", 300, max(2.4, L[0][1]))
    big(t, L[1][0] + 0.4, "POR FIN JUNTOS", 300, 96, YEL, pop=False)
    vignette(img, 160)


def sh_final(img, t, T, L):
    sh_open(img, t + 8, T, [(-9, -8), (-9, -8)])
    weather(img, t, "petals", 0.5)


FNS = {k: globals()["sh_" + k] for k, *_ in SHOTS}
AUDIO = {
    "music": [("open", "warm"), ("notcome", "drone"), ("waiting", "doc"), ("news", "warm"), ("death", "drone"), ("reunion", "warm")],
    "gains": {"warm": 1.2},
    "duck": [("death", "death@end", 0.55)],
    "amb": {"city": ["open", "final"], "birds": ["tokyo", "station", "reunion"], "crowd": ["notcome", "statue"],
            "rain": ["waiting"], "wind": ["death"]},
    "sfx": [("open+0.3", "chime", 0.05), ("tokyo@L2", "chime", 0.06), ("station+1.0", "train", 0.12), ("station+1.6", "clack", 0.12),
            ("notcome+0.3", "train", 0.1), ("notcome@L1", "heart", 0.25), ("notcome@L1+1.0", "heart", 0.25),
            ("waiting@L1", "tick", 0.15), ("waiting@L1+0.8", "tick", 0.15), ("waiting@L1+1.6", "tick", 0.15),
            ("news", "paper", 0.25), ("news@L1+0.2", "swell", 0.18),
            ("statue+0.8", "whoosh", 0.15), ("statue+1.0", "chime", 0.06),
            ("death@L1+0.3", "swell", 0.15), ("reunion@L1+0.4", "chime", 0.07), ("reunion+0.2", "swell", 0.15)],
    "bed": [],
    "bpm": 80,
}
