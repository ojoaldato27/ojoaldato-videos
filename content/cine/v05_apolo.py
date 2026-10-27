"""V05 · El discurso que Nixon nunca leyó (Apolo 11)."""
from cine import *

TITLE = "El_discurso_que_Nixon_nunca_leyo"
LINES = [
    "El presidente Nixon tenía preparado un discurso que *nunca leyó*.",
    "¿Para qué era… y qué decía?",
    "Julio de 1969. El *Apolo 11* despega rumbo a la Luna.",
    "A bordo van Neil Armstrong, Buzz Aldrin y Michael Collins.",
    "El 20 de julio, Armstrong y Aldrin *se posan* en la Luna.",
    "Pero el gran peligro venía después: *despegar de allí*.",
    "Si el motor del módulo lunar fallaba, no había *ningún rescate posible*.",
    "Y encima, se les rompió un interruptor muy importante.",
    "Aldrin lo arregló… *con un rotulador*.",
    "Mientras, en la Tierra, lo tenían todo previsto por si salía mal.",
    "El 18 de julio, el redactor William Safire había escrito un discurso…",
    "…titulado *«En caso de desastre lunar»*.",
    "Empezaba así:",
    "«El destino ha querido que los hombres que fueron a la Luna a explorar en paz… *se queden en la Luna para descansar en paz*».",
    "Antes de leerlo, Nixon debía llamar a *sus futuras viudas*.",
    "Y al cortar la comunicación, un sacerdote los despediría *como en un entierro en el mar*.",
    "Por suerte, el motor *funcionó*.",
    "Y aquel discurso no se hizo famoso hasta *30 años después*.",
    "El discurso más triste de Nixon… es el que *nunca tuvo que leer*.",
]
SHOTS = [("open", 0, 1, 0.3), ("launch", 2, 3, 0.3), ("landing", 4, 4, 0.2), ("danger", 5, 6, 0.3), ("pen", 7, 8, 0.4),
         ("safire", 9, 11, 0.3), ("quote", 12, 13, 0.6), ("widows", 14, 15, 0.5), ("liftoff", 16, 16, 0.4), ("archive", 17, 18, 1.8)]
FOCUS = {"open": (540, 960), "launch": (540, 1000), "landing": (520, 1080), "danger": (540, 900), "pen": (560, 900),
         "safire": (540, 900), "quote": (540, 1150), "widows": (520, 1000), "liftoff": (540, 900), "archive": (540, 960)}
NOTIF = ("landing", 1.0)


# ------------------------------------------------------------------ sprites
HYPE = {"line": 1, "text": ['¿PARA QUÉ ERA?', '¿Y QUÉ DECÍA?'], "delay": [0, 0.9]}
STICKER_EXTRA = [('nixon', '🎙️'), ('discurso', '📜'), ('leyo', '📜'), ('apolo', '🚀'), ('despega', '🚀'), ('luna', '🌕'), ('posan', '🌕'), ('peligro', '⚠️'), ('motor', '🔧'), ('rescate', '🆘'), ('interruptor', '🔌'), ('rompio', '⚠️'), ('rotulador', '🖊️'), ('tierra', '🌍'), ('redactor', '✍️'), ('escrito', '✍️'), ('desastre', '😱'), ('=paz', '🕊️'), ('descansar', '🕊️'), ('viudas', '💔'), ('comunicacion', '📡'), ('sacerdote', '⛪'), ('=mar', '🌊'), ('funciono', '✅'), ('suerte', '🍀'), ('famoso', '⭐'), ('triste', '😢')]

def saturn():
    def fn(d, s):
        wh, bk = (236, 236, 232), (24, 24, 28)
        cx = 120
        d.rectangle(sb([cx - 50, 300, cx + 50, 1100], s), fill=wh)
        for y in (420, 700, 960):
            d.rectangle(sb([cx - 50, y, cx + 50, y + 40], s), fill=bk)
        for y in range(320, 1100, 120):
            d.rectangle(sb([cx - 50, y, cx - 30, y + 60], s), fill=bk)
        d.polygon(sc([(cx - 40, 300), (cx + 40, 300), (cx + 26, 200), (cx - 26, 200)], s), fill=wh)
        d.polygon(sc([(cx - 26, 200), (cx + 26, 200), (cx, 110)], s), fill=(200, 200, 196))
        d.line(sc([(cx, 110), (cx, 30)], s), fill=wh, width=int(6 * s))
        for sgn in (-1, 1):
            d.polygon(sc([(cx + sgn * 50, 1000), (cx + sgn * 90, 1100), (cx + sgn * 50, 1100)], s), fill=bk)
        d.rectangle(sb([cx - 50, 1100, cx + 50, 1120], s), fill=(60, 60, 64))
    return sprite("saturn", 240, 1130, fn)


def lem(stage="full"):
    def fn(d, s):
        gold, gold2, grey, grey2 = (214, 168, 70), (170, 126, 44), (190, 192, 196), (130, 132, 140)
        if stage == "full":
            for sgn in (-1, 1):
                d.line(sc([(250 + sgn * 110, 330), (250 + sgn * 200, 470)], s), fill=grey2, width=int(10 * s))
                d.ellipse(sb([250 + sgn * 200 - 36, 460, 250 + sgn * 200 + 36, 482], s), fill=grey)
            d.line(sc([(250, 360), (250, 470)], s), fill=grey2, width=int(10 * s))
            d.polygon(sc([(130, 260), (370, 260), (390, 360), (110, 360)], s), fill=gold)
            d.polygon(sc([(130, 260), (200, 260), (190, 360), (110, 360)], s), fill=gold2)
            d.polygon(sc([(220, 360), (280, 360), (300, 410), (200, 410)], s), fill=(80, 80, 86))
        d.polygon(sc([(150, 260), (350, 260), (380, 190), (330, 90), (190, 90), (130, 170)], s), fill=grey)
        d.polygon(sc([(150, 260), (220, 260), (210, 120), (190, 90), (130, 170)], s), fill=grey2)
        d.polygon(sc([(240, 140), (300, 140), (290, 190), (250, 190)], s), fill=(40, 44, 56))
        d.line(sc([(320, 90), (340, 30)], s), fill=grey2, width=int(4 * s))
        d.ellipse(sb([330, 14, 360, 40], s), fill=grey)
        if stage == "ascent":
            d.polygon(sc([(220, 260), (280, 260), (295, 300), (205, 300)], s), fill=(80, 80, 86))
    return sprite(("lem", stage), 500, 500, fn)


def moon_ground():
    def fn(d, s):
        d.polygon(sc([(0, 120), (300, 80), (700, 110), (1080, 70), (1080, 700), (0, 700)], s), fill=(150, 150, 154))
        rr = random.Random(3)
        for _ in range(40):
            x, y = rr.uniform(0, 1080), rr.uniform(140, 680)
            r = rr.uniform(10, 60) * (0.5 + y / 700)
            d.ellipse(sb([x - r, y - r * 0.35, x + r, y + r * 0.35], s), fill=(120, 120, 126))
            d.ellipse(sb([x - r * 0.8, y - r * 0.25, x + r * 0.9, y + r * 0.3], s), fill=(136, 136, 142))
    return sprite("mground", 1080, 700, fn)


def astronaut(flag=False):
    def fn(d, s):
        wh, sh_ = (240, 240, 236), (200, 200, 200)
        d.rounded_rectangle(sb([60, 80, 160, 250], s), radius=int(30 * s), fill=wh)
        d.rounded_rectangle(sb([40, 90, 80, 210], s), radius=int(14 * s), fill=sh_)
        d.ellipse(sb([70, 10, 150, 100], s), fill=wh)
        d.ellipse(sb([86, 30, 140, 80], s), fill=(214, 168, 70))
        d.rectangle(sb([70, 240, 104, 360], s), fill=wh)
        d.rectangle(sb([116, 240, 150, 360], s), fill=wh)
        d.line(sc([(150, 110), (200, 200)], s), fill=wh, width=int(26 * s))
        if flag:
            d.line(sc([(210, 40), (210, 360)], s), fill=(200, 200, 200), width=int(6 * s))
            d.rectangle(sb([210, 40, 330, 110], s), fill=(230, 230, 236))
            for k in range(4):
                d.rectangle(sb([210, 40 + k * 18, 330, 49 + k * 18], s), fill=(200, 40, 50))
            d.rectangle(sb([210, 40, 260, 76], s), fill=(40, 60, 140))
    return sprite(("astro", flag), 340, 370, fn)


def phone():
    def fn(d, s):
        blk = (20, 20, 24)
        d.polygon(sc([(60, 300), (340, 300), (300, 140), (100, 140)], s), fill=blk)
        d.ellipse(sb([130, 160, 270, 300], s), fill=(50, 50, 56))
        d.ellipse(sb([175, 205, 225, 255], s), fill=(220, 220, 220))
        for k in range(10):
            a = math.radians(-60 + k * 28)
            x, y = 200 + math.cos(a) * 52, 230 + math.sin(a) * 52
            d.ellipse(sb([x - 9, y - 9, x + 9, y + 9], s), fill=(200, 200, 200))
        d.rounded_rectangle(sb([40, 70, 360, 130], s), radius=int(30 * s), fill=blk)
        d.ellipse(sb([30, 50, 120, 140], s), fill=blk)
        d.ellipse(sb([280, 50, 370, 140], s), fill=blk)
    return sprite("phone", 400, 320, fn)


def panel(broken=True):
    def fn(d, s):
        d.rectangle(sb([0, 0, 900, 700], s), fill=(70, 74, 80))
        for r in range(6):
            for c in range(8):
                x, y = 60 + c * 105, 60 + r * 105
                d.ellipse(sb([x, y, x + 60, y + 60], s), fill=(30, 30, 34))
                if broken and (r, c) == (3, 4):
                    d.rectangle(sb([x + 22, y + 30, x + 38, y + 48], s), fill=(150, 150, 150))
                else:
                    d.rectangle(sb([x + 24, y - 6, x + 36, y + 30], s), fill=(220, 220, 220))
                d.text((x * s, (y + 66) * s), "CB", font=f(F_MONO, int(18 * s)), fill=(200, 200, 200))
    return sprite(("panel", broken), 900, 700, fn)


def pen():
    def fn(d, s):
        d.rounded_rectangle(sb([0, 20, 420, 70], s), radius=int(20 * s), fill=(30, 30, 36))
        d.rectangle(sb([300, 20, 420, 70], s), fill=(220, 220, 224))
        d.polygon(sc([(420, 25), (470, 40), (470, 50), (420, 65)], s), fill=(30, 30, 36))
        d.rectangle(sb([60, 10, 200, 22], s), fill=(200, 200, 204))
    return sprite("pen", 480, 90, fn)


def flame(img, t, cx, cy, scale=1.0, up=False):
    d = ImageDraw.Draw(img, "RGBA")
    for k in range(10):
        ph = (t * 6 + k / 10) % 1.0
        r = (30 + ph * 70) * scale
        y = cy + (ph * 260 * scale) * (-1 if up else 1)
        x = cx + math.sin(k * 3.1 + t * 10) * 10 * scale
        col = (255, int(lerp(240, 120, ph)), int(lerp(180, 40, ph)), int(230 * (1 - ph)))
        d.ellipse([x - r, y - r, x + r, y + r], fill=col)
    paste(img, glow(int(220 * scale), (255, 180, 90), 1.0), cx, cy + 60 * scale * (-1 if up else 1))


# ------------------------------------------------------------------ planos
def desk(img, t, lamp=True):
    sky(img, (16, 14, 22), (6, 5, 8), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([640, 520, 1000, 960], fill=(18, 22, 44))
    d.rectangle([630, 510, 1010, 520], fill=(60, 44, 34))
    d.line([(820, 520), (820, 960)], fill=(60, 44, 34), width=8)
    d.line([(640, 740), (1000, 740)], fill=(60, 44, 34), width=8)
    paste(img, glow(60, (240, 240, 220), 1.0), 900, 620)
    d.ellipse([880, 600, 920, 640], fill=(236, 236, 226))
    d.rectangle([0, 1180, W, H], fill=(70, 40, 26))
    d.rectangle([0, 1170, W, 1190], fill=(110, 70, 44))
    if lamp:
        paste(img, glow(380, (255, 210, 140), 0.7), 280, 1050)
        d.line([(200, 1180), (200, 900)], fill=(170, 130, 60), width=10)
        d.polygon([(110, 900), (290, 900), (250, 800), (150, 800)], fill=(30, 90, 50))


def sh_open(img, t, T, L):
    desk(img, t)
    doc = spr(paper, 600, 700, "IN EVENT OF", 0, (244, 240, 228), (30, 30, 30), 1,
              ("   MOON DISASTER", "", "Fate has ordained that", "the men who went to the", "moon to explore in peace", "will stay on the moon",
               "to rest in peace.", "", "..."))
    paste(img, doc, 600, 1180, 1.0, 1.0, -6)
    title2(t, 0.25, "EL DISCURSO QUE", "NIXON NUNCA LEYÓ", 290, 60, 86, hold=max(1.5, L[1][0] - 0.4))
    vignette(img, 200)


def sh_launch(img, t, T, L):
    sky(img, (70, 120, 190), (220, 220, 230), 1.2)
    q = ease(clamp((t - 0.6) / (T - 0.6)))
    ry = 1300 - 900 * q * q
    sx, sy = shake(t, 0.6, 6, 0.3)
    smoke(img, t, [(540 - 200, 1500, 2.4), (540 + 200, 1500, 2.4)], col=(230, 226, 220), alpha=200, spread=(0, -40), grow=140, speed=0.25)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([700, 600, 740, 1500], fill=(160, 60, 40))
    for y in range(620, 1500, 60):
        d.line([(700, y), (740, y + 60)], fill=(120, 40, 30), width=4)
    flame(img, t, 540 + sx, ry + 560 + sy, 1.3)
    paste(img, saturn(), 540 + sx, ry + sy)
    ground(img, 1500, (60, 66, 50), (30, 34, 26))
    smoke(img, t * 1.3, [(300, 1520, 2.0), (780, 1520, 2.0)], col=(240, 236, 230), alpha=210, spread=(-120, 60), grow=160, speed=0.3)
    date_stamp(t, 0.3, "16 · 07 · 1969", 300, max(1.6, L[1][0] - 0.3))
    lower_third(img, t, L[1][0] + 0.2, "ARMSTRONG · ALDRIN · COLLINS", "TRIPULACIÓN DEL APOLO 11", 300, max(2.0, L[1][1] - L[1][0] - 0.4))
    vignette(img, 150)


def sh_landing(img, t, T, L):
    space_bg(img, t, 4, ((30, 30, 60), (20, 30, 50)), 300)
    paste(img, spr(globe_sprite, -40.0, 20.0, 110, ()), 820, 480)
    paste(img, moon_ground(), 540, 1520)
    q = ease(clamp(t / 2.5))
    paste(img, lem(), 520, lerp(900, 1110, q), 1.0)
    if q < 1:
        flame(img, t, 520, lerp(900, 1110, q) + 190, 0.5)
    date_stamp(t, 0.3, "20 · 07 · 1969", 300)
    vignette(img, 170)


def sh_danger(img, t, T, L):
    space_bg(img, t, 6, ((30, 30, 60), (20, 30, 50)), 300)
    paste(img, moon_ground(), 540, 1520)
    paste(img, lem(), 540, 1020, 1.5)
    a1 = L[1][0]
    if t > a1:
        bl = (int((t - a1) * 2.5) % 2) == 0
        overlay(img, (200, 20, 20), 0.18 if bl else 0.08)
        big(t, a1 + 0.3, "SIN RESCATE", 300, 104, RED, sub="POSIBLE", subcol=WHITE)
    else:
        big(t, 0.4, "DESPEGAR DE LA LUNA", 300, 72, WHITE, pop=False)
    vignette(img, 200)


def sh_pen(img, t, T, L):
    sky(img, (20, 20, 24), (8, 8, 10), 1.0)
    paste(img, panel(True), 540, 900, 1.0)
    cx, cy = 540 - 450 + 60 + 4 * 105 + 30, 900 - 350 + 60 + 3 * 105 + 30
    a1 = L[1][0]
    if t < a1:
        k = 0.6 + 0.4 * math.sin(t * 6) ** 2
        paste(img, glow(90, (255, 80, 60), 1.0), cx, cy, 1.0, k)
    else:
        q = ease(clamp((t - a1 - 0.2) / 0.9))
        paste(img, pen(), cx + 250 - 230 * q, cy - 10, 1.0)
        if q > 0.95:
            paste(img, glow(90, (120, 255, 140), 1.0), cx, cy, 1.0, 0.8)
        big(t, a1 + 1.0, "UN ROTULADOR", 300, 100, YEL)
    vignette(img, 200)


def sh_safire(img, t, T, L):
    a1 = L[1][0]
    if t < a1:
        space_bg(img, t, 7)
        paste(img, spr(globe_sprite, -80.0, 30.0, 360, ()), 540, 900)
        paste(img, glow(40, (255, 230, 160), 1.0), 540 - 40, 900 - 120, 1.0, 0.8)
    else:
        desk(img, t)
        lines_ = ["IN EVENT OF MOON DISASTER:", "", "Fate has ordained that the", "men who went to the moon to", "explore in peace will stay",
                  "on the moon to rest in peace."]
        q = clamp((t - a1 - 0.3) / 3.0)
        nchar = int(q * sum(len(x) for x in lines_))
        shown = []
        for ln in lines_:
            shown.append(ln[:max(0, nchar)])
            nchar -= len(ln)
        doc = paper(640, 760, "", 0, (244, 240, 228), (30, 30, 30), 2, tuple(shown))
        paste(img, doc, 540, 1080, 1.0, 1.0, -2)
        date_stamp(t, a1 + 0.1, "18 · 07 · 1969", 300, 2.0)
        lower_third(img, t, a1 + 2.4, "WILLIAM SAFIRE", "REDACTOR DE DISCURSOS", 300, 2.6)
        big(t, L[2][0] + 0.3, "«EN CASO DE", 300, 80, WHITE, sub="DESASTRE LUNAR»", subcol=YEL, pop=False)
    vignette(img, 200)


def sh_quote(img, t, T, L):
    space_bg(img, t, 9, ((30, 30, 60), (20, 30, 50)), 300)
    paste(img, spr(globe_sprite, -40.0, 20.0, 90, ()), 900, 800)
    paste(img, moon_ground(), 540, 1520)
    paste(img, lem(), 380, 1150, 0.7)
    paste(img, astronaut(True), 700, 1200, 0.8)
    paste(img, astronaut(False), 840, 1220, 0.75, flip=True)
    a1 = L[1][0]
    if t > a1:
        d = td()
        k = ease(clamp((t - a1) / 0.8))
        A = int(255 * k)
        rows = ["«EL DESTINO HA QUERIDO", "QUE LOS HOMBRES QUE", "FUERON A EXPLORAR EN PAZ…", "", "…DESCANSEN EN PAZ", "EN LA LUNA»"]
        for i, ln in enumerate(rows):
            kk = ease(clamp((t - a1 - (0 if i < 3 else (L[1][1] - a1) * 0.55)) / 0.7))
            spaced(d, W / 2, 230 + i * 74, ln, f(F_SER, 56), (YEL if i >= 4 else WHITE) + (int(255 * kk),), 3)
    vignette(img, 190)


def sh_widows(img, t, T, L):
    a1 = L[1][0]
    if t < a1 - 0.2:
        desk(img, t)
        rg = (int(t * 3) % 2) == 0 and t > 0.6
        dx = math.sin(t * 60) * 4 if rg else 0
        paste(img, phone(), 560 + dx, 1100, 1.2)
        big(t, 0.5, "LLAMAR A", 300, 80, WHITE, sub="SUS FUTURAS VIUDAS", subcol=YEL, pop=False)
    else:
        night_sky(img, t, 1150, 1.0)
        paste(img, glow(160, (240, 240, 230), 1.0), 760, 720)
        ImageDraw.Draw(img).ellipse([710, 670, 810, 770], fill=(236, 236, 228))
        sea(img, t, 1150, (14, 20, 40), (4, 6, 12), (90, 100, 140), 0.5)
        d = ImageDraw.Draw(img, "RGBA")
        for k in range(14):
            y = 1170 + k * 22
            w_ = 30 + k * 6
            d.line([(760 - w_, y), (760 + w_, y)], fill=(230, 230, 220, max(0, 150 - k * 10)), width=4)
        big(t, a1 + 0.2, "COMO UN ENTIERRO", 300, 80, WHITE, sub="EN EL MAR", subcol=YEL, pop=False)
    vignette(img, 200)


def sh_liftoff(img, t, T, L):
    space_bg(img, t, 11, ((30, 30, 60), (20, 30, 50)), 300)
    paste(img, spr(globe_sprite, -40.0, 20.0, 110, ()), 860, 720)
    paste(img, moon_ground(), 540, 1520)
    q = ease(clamp((t - 0.5) / (T - 0.5)))
    y = lerp(1030, 640, q)
    d = ImageDraw.Draw(img, "RGBA")
    gold, gold2, grey2 = (214, 168, 70), (170, 126, 44), (130, 132, 140)
    for sgn in (-1, 1):
        d.line([(540 + sgn * 110, 1110 + 80), (540 + sgn * 200, 1110 + 220)], fill=grey2, width=10)
    d.polygon([(420, 1010), (660, 1010), (680, 1110), (400, 1110)], fill=gold)
    if t > 0.5:
        flame(img, t, 540, y + 70, 0.45)
    paste(img, lem("ascent"), 540, y - 30, 1.0)
    rays(img, t, 540, y, 10, (255, 230, 180), 14, 900, 0.06, 0.1) if q > 0.1 else None
    big(t, 0.5, "¡FUNCIONÓ!", 300, 110, YEL)
    vignette(img, 170)


def sh_archive(img, t, T, L):
    sky(img, (24, 22, 26), (8, 7, 9), 1.0)
    spotlight(img, t, 540, 0, 1400, 140, 560, 50)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([140, 820, 940, 1400], fill=(110, 80, 50))
    d.rectangle([160, 840, 920, 1380], fill=(130, 96, 60))
    q = ease(clamp((t - 0.8) / 1.0))
    doc = spr(paper, 600, 700, "IN EVENT OF", 0, (244, 240, 228), (30, 30, 30), 1,
              ("   MOON DISASTER", "", "Fate has ordained that", "the men who went to the", "moon to explore in peace"))
    paste(img, doc, 540, lerp(700, 1150, q), 0.8, 1.0, -4)
    d.rectangle([140, 1100, 940, 1400], fill=(100, 72, 44))
    d.rectangle([460, 1180, 620, 1220], fill=(200, 160, 70))
    big(t, L[0][0] + 1.6, "30 AÑOS", 300, 120, YEL, sub="EN UN ARCHIVO", hold=max(1.6, L[1][0] - L[0][0] - 1.8))
    if t > L[1][0]:
        overlay(img, (0, 0, 0), ease(clamp((t - L[1][0]) / 1.0)) * 0.7)
        paste(img, spr(globe_sprite, -40.0, 20.0, 140, ()), 540, 760, 1.0, ease(clamp((t - L[1][0]) / 1.0)))
    vignette(img, 200)


FNS = {k: globals()["sh_" + k] for k, *_ in SHOTS}
AUDIO = {
    "music": [("open", "drone"), ("launch", "epic"), ("danger", "tension"), ("safire", "drone"), ("quote", "space"),
              ("liftoff", "epic"), ("archive", "space")],
    "duck": [("quote@L1", "widows@end", 0.5)],
    "amb": {"room": ["open", "safire", "widows"], "space": ["landing", "danger", "pen", "quote", "liftoff"], "sea": ["widows"]},
    "sfx": [("open+0.3", "type", 0.12), ("launch+0.6", "boom", 0.45), ("launch+0.6", "rumble", 0.4), ("launch+2.0", "rumble", 0.35),
            ("landing+0.2", "static", 0.12), ("landing+2.5", "thud", 0.3), ("landing+2.6", "beep", 0.12),
            ("danger@L1", "beep", 0.12), ("danger@L1+0.4", "beep", 0.12), ("danger@L1+0.8", "beep", 0.12), ("danger@L1+0.3", "impact", 0.3),
            ("pen@L1+1.1", "click", 0.4), ("pen@L1+1.15", "chime", 0.06),
            ("safire@L1+0.3", "type", 0.18), ("safire@L1+1.6", "type", 0.18), ("safire@L2+0.3", "impact", 0.2),
            ("quote@L1", "swell", 0.18),
            ("widows+0.7", "beep", 0.08), ("widows+1.4", "beep", 0.08), ("widows+2.1", "beep", 0.08),
            ("widows@L1", "static", 0.1),
            ("liftoff+0.5", "boom", 0.35), ("liftoff+0.6", "riser", 0.15), ("liftoff+0.9", "chime", 0.07),
            ("archive+1.6", "thud", 0.4)],
    "bed": [("launch", "safire")],
    "bpm": 96,
}
