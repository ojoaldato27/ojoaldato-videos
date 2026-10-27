"""V02 · El hombre que vendió la Torre Eiffel (Victor Lustig, 1925)."""
from cine import *

TITLE = "El_hombre_que_vendio_la_Torre_Eiffel"
LINES = [
    "Un hombre consiguió *vender la Torre Eiffel*… sin que fuera suya.",
    "¿Cómo lo hizo… y por qué nadie lo denunció?",
    "París, 1925.",
    "Victor Lustig, un estafador muy elegante, lee el periódico.",
    "La noticia dice que mantener la torre *sale carísimo*.",
    "Y que podría acabar *desmontada*.",
    "Lustig ve una oportunidad de oro.",
    "Falsifica papeles del *Ministerio de Correos y Telégrafos*.",
    "Y reúne en un hotel de lujo a varios *chatarreros*.",
    "Les cuenta un secreto: el gobierno quiere *vender la torre* como chatarra.",
    "Y les pide *discreción absoluta*.",
    "Uno de ellos, *André Poisson*, muerde el anzuelo.",
    "Paga por la torre… y encima le da un *soborno* a Lustig.",
    "Lustig coge el dinero y huye a *Austria*.",
    "¿Y Poisson? Le da *tanta vergüenza*… que no lo denuncia.",
    "Así que Lustig vuelve a París… para *venderla otra vez*.",
    "Pero esta vez, uno de los compradores *avisa a la policía*.",
    "Lustig escapa a Estados Unidos.",
    "Allí llegó a engañar a *Al Capone*… y acabó en *Alcatraz*.",
    "El hombre que vendió la Torre Eiffel… que *nunca fue suya*.",
]
SHOTS = [("open", 0, 1, 0.3), ("paris", 2, 2, 0.2), ("reader", 3, 3, 0.2), ("news", 4, 5, 0.3), ("idea", 6, 6, 0.2),
         ("forgery", 7, 7, 0.3), ("hotel", 8, 8, 0.2), ("secret", 9, 10, 0.3), ("poisson", 11, 12, 0.3),
         ("escape", 13, 13, 0.2), ("shame", 14, 14, 0.3), ("again", 15, 16, 0.3), ("usa", 17, 17, 0.1),
         ("alcatraz", 18, 18, 0.4), ("final", 19, 19, 1.8)]
FOCUS = {"open": (540, 800), "paris": (560, 900), "reader": (600, 760), "news": (540, 760), "forgery": (540, 900),
         "hotel": (540, 1000), "secret": (540, 900), "poisson": (540, 860), "shame": (540, 900), "again": (540, 820),
         "alcatraz": (560, 1000), "final": (540, 760)}
NOTIF = ("forgery", 1.0)

GOLD = (214, 160, 70)


# ------------------------------------------------------------------ sprites
HYPE = {"line": 1, "text": ['¿CÓMO LO HIZO?', '¿POR QUÉ NADIE LO DENUNCIÓ?'], "delay": [0, 1.0]}
STICKER_EXTRA = [('torre', '🇫🇷'), ('eiffel', '🇫🇷'), ('denunc', '👮'), ('estafador', '🎩'), ('elegante', '🎩'), ('periodico', '📰'), ('carisimo', '💸'), ('desmont', '🔧'), ('oportunidad', '💰'), ('=oro', '💰'), ('falsifica', '📝'), ('papeles', '📝'), ('ministerio', '🏛️'), ('hotel', '🏨'), ('chatarr', '🔩'), ('secreto', '🤫'), ('discrecion', '🤫'), ('anzuelo', '🎣'), ('paga', '💰'), ('soborno', '💵'), ('dinero', '💰'), ('huye', '🏃'), ('verguenza', '😳'), ('policia', '🚓'), ('escapa', '🏃'), ('capone', '🕴️'), ('alcatraz', '⛓️')]

def eiffel(h=1500, col=(30, 26, 30), lines=(70, 60, 64), lit=False):
    w = int(h * 0.5)

    def fn(d, s):
        cx = w / 2

        def hw(u):  # semiancho a la altura u (0 suelo, 1 punta)
            if u < 0.17:
                return lerp(0.19, 0.115, u / 0.17)
            if u < 0.35:
                return lerp(0.115, 0.062, (u - 0.17) / 0.18)
            if u < 0.86:
                return lerp(0.062, 0.017, ((u - 0.35) / 0.51) ** 0.8)
            return lerp(0.017, 0.004, (u - 0.86) / 0.14)

        c = (220, 160, 70) if lit else col
        lc = (255, 214, 130) if lit else lines
        left = [(cx - hw(u) * h, h - u * h) for u in [k / 60 for k in range(61)]]
        right = [(cx + hw(u) * h, h - u * h) for u in [k / 60 for k in range(60, -1, -1)]]
        d.polygon(sc(left + right, s), fill=c)
        # celosía
        segs = [0.0, 0.08, 0.17, 0.26, 0.35, 0.45, 0.55, 0.65, 0.75, 0.86]
        for a, b in zip(segs, segs[1:]):
            for sgn in (-1, 1):
                x1, x2 = cx + sgn * hw(a) * h * 0.92, cx + sgn * hw(b) * h * 0.92
                xi1, xi2 = cx + sgn * hw(a) * h * 0.25, cx + sgn * hw(b) * h * 0.25
                y1, y2 = h - a * h, h - b * h
                d.line(sc([(x1, y1), (xi2, y2)], s), fill=lc, width=max(1, int(2 * s)))
                d.line(sc([(xi1, y1), (x2, y2)], s), fill=lc, width=max(1, int(2 * s)))
        for u, ext in ((0.17, 1.15), (0.35, 1.25), (0.86, 1.8)):
            y = h - u * h
            ww = hw(u) * h * ext
            d.rectangle(sb([cx - ww, y - 0.012 * h, cx + ww, y + 0.004 * h], s), fill=c)
            d.line(sc([(cx - ww, y - 0.004 * h), (cx + ww, y - 0.004 * h)], s), fill=lc, width=max(1, int(2 * s)))
        d.rectangle(sb([cx - 0.006 * h, 0, cx + 0.006 * h, 0.06 * h], s), fill=c)
        aw, ah = 0.118 * h, 0.125 * h
        d.ellipse(sb([cx - aw, h - ah, cx + aw, h + ah], s), fill=(0, 0, 0, 0))
        d.arc(sb([cx - aw, h - ah, cx + aw, h + ah], s), 180, 360, fill=lc, width=max(1, int(3 * s)))
    return sprite(("eiffel", h, col, lit), w, h + 4, fn)


def skyline(night=True, seed=3, h=520):
    def fn(d, s):
        rr = random.Random(seed)
        col = (16, 16, 26) if night else (70, 70, 90)
        x = -20
        while x < W + 20:
            bw = rr.uniform(90, 180)
            bh = rr.uniform(160, 300)
            y0 = h - bh
            d.rectangle(sb([x, y0, x + bw, h], s), fill=col)
            d.polygon(sc([(x - 6, y0), (x + bw + 6, y0), (x + bw - 18, y0 - 46), (x + 18, y0 - 46)], s), fill=col)
            for k in range(rr.randint(1, 3)):
                cxh = x + rr.uniform(20, bw - 20)
                d.rectangle(sb([cxh - 7, y0 - 70, cxh + 7, y0 - 40], s), fill=col)
            if night:
                for wy in range(int(y0 + 20), h - 20, 44):
                    for wx in range(int(x + 14), int(x + bw - 20), 30):
                        if rr.random() < 0.35:
                            d.rectangle(sb([wx, wy, wx + 12, wy + 18], s), fill=(255, 206, 130))
            x += bw - 4
        # cúpula
        d.ellipse(sb([760, h - 420, 900, h - 250], s), fill=col)
        d.rectangle(sb([760, h - 330, 900, h - 200], s), fill=col)
        d.line(sc([(830, h - 420), (830, h - 470)], s), fill=col, width=int(8 * s))
    return sprite(("sky", night, seed, h), W, h, fn)


def banknotes():
    def fn(d, s):
        for k in range(6):
            x, y = 40 + k * 8, 40 + k * 10
            d.rounded_rectangle(sb([x, y, x + 380, y + 190], s), radius=int(10 * s), fill=(150, 170, 120), outline=(90, 110, 70), width=int(4 * s))
            d.ellipse(sb([x + 140, y + 40, x + 240, y + 150], s), outline=(90, 110, 70), width=int(4 * s))
            d.text(((x + 30) * s, (y + 20) * s), "1000", font=f(F_SER, int(40 * s)), fill=(70, 90, 50))
    return sprite("notes", 480, 300, fn)


def chandelier():
    def fn(d, s):
        g = (230, 190, 110)
        d.line(sc([(250, 0), (250, 120)], s), fill=g, width=int(4 * s))
        d.ellipse(sb([150, 110, 350, 170], s), outline=g, width=int(6 * s))
        for k in range(7):
            x = 160 + k * 30
            d.line(sc([(x, 140), (x, 210)], s), fill=g, width=int(3 * s))
            d.polygon(sc([(x - 8, 210), (x + 8, 210), (x, 240)], s), fill=(255, 240, 200))
        for x in (150, 350, 250):
            d.ellipse(sb([x - 14, 90, x + 14, 118], s), fill=(255, 236, 190))
    return sprite("chand", 500, 260, fn)


def train(lit=True):
    def fn(d, s):
        c = (16, 16, 22)
        d.rectangle(sb([60, 120, 330, 260], s), fill=c)
        d.rectangle(sb([330, 60, 450, 260], s), fill=c)
        d.rectangle(sb([90, 70, 140, 120], s), fill=c)
        d.polygon(sc([(30, 260), (60, 200), (60, 260)], s), fill=c)
        for x in range(470, 1600, 290):
            d.rounded_rectangle(sb([x, 90, x + 270, 260], s), radius=int(10 * s), fill=c)
            if lit:
                for wx in range(x + 20, x + 250, 50):
                    d.rectangle(sb([wx, 120, wx + 32, 160], s), fill=(255, 210, 140))
        for x in list(range(100, 440, 90)) + list(range(500, 1600, 110)):
            d.ellipse(sb([x - 30, 240, x + 30, 300], s), fill=(30, 30, 36))
    return sprite(("train", lit), 1640, 310, fn)


def alcatraz():
    def fn(d, s):
        rock = (22, 24, 30)
        d.polygon(sc([(0, 420), (120, 300), (300, 250), (700, 240), (860, 300), (1000, 420)], s), fill=rock)
        d.rectangle(sb([280, 140, 720, 260], s), fill=(40, 42, 50))
        for x in range(300, 700, 26):
            for y in (165, 205):
                d.rectangle(sb([x, y, x + 10, y + 20], s), fill=(255, 210, 140) if (x // 26 + y) % 3 else (60, 60, 70))
        d.rectangle(sb([760, 40, 790, 250], s), fill=(40, 42, 50))
        d.rectangle(sb([748, 30, 802, 60], s), fill=(255, 236, 190))
    return sprite("alcatraz", 1000, 430, fn)


def nyc():
    def fn(d, s):
        rr = random.Random(9)
        c = (20, 22, 34)
        x = 0
        while x < W:
            bw = rr.uniform(60, 130)
            bh = rr.uniform(200, 620)
            d.rectangle(sb([x, 700 - bh, x + bw, 700], s), fill=c)
            for wy in range(int(700 - bh + 20), 680, 36):
                for wx in range(int(x + 10), int(x + bw - 14), 22):
                    if rr.random() < 0.3:
                        d.rectangle(sb([wx, wy, wx + 9, wy + 14], s), fill=(255, 220, 150))
            x += bw + rr.uniform(0, 8)
    return sprite("nyc", W, 700, fn)


def tag(txt="SE VENDE"):
    def fn(d, s):
        d.line(sc([(150, 0), (150, 70)], s), fill=(240, 230, 210), width=int(4 * s))
        d.polygon(sc([(30, 110), (150, 60), (270, 110), (270, 250), (30, 250)], s), fill=(236, 228, 210))
        d.ellipse(sb([138, 82, 162, 106], s), fill=(40, 30, 30))
        fnt = f(F_SER, int(52 * s))
        for i, wd in enumerate(txt.split()):
            tw = d.textlength(wd, font=fnt)
            d.text((150 * s - tw / 2, (126 + i * 58) * s), wd, font=fnt, fill=(180, 30, 36))
    return sprite(("tag", txt), 300, 270, fn)


# ------------------------------------------------------------------ planos
def paris_night(img, t, hz=1250, tower_s=0.6, tx=540, lit=True, sparkle=0.0):
    night_sky(img, t, hz, 0.9, (8, 10, 28), (40, 40, 80))
    paste(img, glow(520, (255, 180, 110), 0.35), tx, hz - 200)
    th = 1500
    paste(img, eiffel(th, lit=lit), tx, hz + 40 - th * tower_s / 2, tower_s)
    if sparkle > 0:
        d = ImageDraw.Draw(img, "RGBA")
        rr = random.Random(int(t * 12))
        for _ in range(int(70 * sparkle)):
            u = rr.random()
            hwid = 0.19 * th * tower_s * (1 - u) ** 1.6
            x = tx + rr.uniform(-hwid, hwid)
            y = hz + 40 - u * th * tower_s
            r = rr.uniform(2, 5)
            d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, 230))
    paste(img, skyline(True), 540, hz + 10)
    ground(img, hz + 270, (10, 10, 18), (4, 4, 8))


def sh_open(img, t, T, L):
    paris_night(img, t, 1300, 0.6)
    a0 = L[1][0] - 0.2
    if t > a0:
        k = ease(clamp((t - a0) / 0.6))
        sw = math.sin((t - a0) * 2.4) * 10 * math.exp(-(t - a0) * 0.4)
        paste(img, tag(), 650, 900 - 300 * (1 - k), 0.9, k, sw)
    title2(t, 0.25, "EL HOMBRE QUE VENDIÓ", "LA TORRE EIFFEL", 290, 58, 86, hold=max(1.5, L[1][0] - 0.4))
    vignette(img, 170)


def sh_paris(img, t, T, L):
    sky(img, (120, 150, 200), (250, 210, 170), 1.3)
    clouds(img, t, 500, (255, 255, 255), 120, 10, 3, 1.3)
    paste(img, eiffel(1000, (60, 56, 64), (90, 84, 92)), 830 - t * 6, 1250 - 500)
    paste(img, skyline(False, 4), 540, 1250)
    ground(img, 1500, (60, 56, 60), (30, 28, 30))
    d = ImageDraw.Draw(img, "RGBA")
    for i in range(5):
        x = (200 + i * 140 + t * 50) % (W + 100) - 50
        y = 420 + math.sin(t * 2 + i) * 20 + i * 30
        fl = math.sin(t * 9 + i) * 10
        d.line([(x - 22, y - fl), (x, y), (x + 22, y - fl)], fill=(40, 40, 50, 220), width=4)
    date_stamp(t, 0.3, "PARÍS · 1925", 310)
    vignette(img, 150)


def sh_reader(img, t, T, L):
    sky(img, (34, 26, 22), (14, 10, 8), 1.0)
    paste(img, glow(420, (255, 190, 110), 0.6), 760, 520)
    d = ImageDraw.Draw(img, "RGBA")
    d.line([(760, 0), (760, 420)], fill=(40, 30, 24), width=6)
    d.polygon([(680, 420), (840, 420), (800, 470), (720, 470)], fill=(200, 150, 70))
    d.rectangle([0, 1300, W, H], fill=(36, 24, 18))
    d.rectangle([0, 1290, W, 1310], fill=(70, 50, 34))
    paste(img, spr(person, 260, 640, (18, 14, 14), "bowler", True), 520, 1010, 1.25)
    np_ = paper(420, 300, "", 6, (230, 222, 200), (60, 50, 40), 3)
    paste(img, np_, 680, 930, 1.0, 1.0, 8 + math.sin(t) * 1.5)
    d.ellipse([820, 1220, 960, 1260], fill=(240, 236, 226))
    smoke(img, t, [(890, 1200, 0.5)], col=(220, 210, 200), alpha=60, spread=(-20, 260), grow=40, speed=0.25)
    lower_third(img, t, 0.4, "VICTOR LUSTIG", "ESTAFADOR · 1890-1947", 300, max(2.2, T - 1.0))
    vignette(img, 190)


def sh_news(img, t, T, L):
    sky(img, (30, 24, 20), (10, 8, 6), 1.0)
    spotlight(img, t, 540, 0, 1400, 160, 640, 50)
    npim = spr(newspaper, "LA TOUR EIFFEL\nCOÛTE TROP CHER", "L'entretien de la tour inquiète la ville", "PARIS · 1925")
    paste(img, npim, 540, 980, 1.0 + 0.04 * ease(clamp(t / T)), 1.0, -3)
    a1 = L[1][0] + 0.6
    if t > a1:
        k = ease(clamp((t - a1) / 0.35))
        big(t, a1, "¿DESMONTARLA?", 300, 100, RED)
    vignette(img, 200)


def sh_idea(img, t, T, L):
    sky(img, (14, 10, 10), (4, 3, 3), 1.0)
    rays(img, t, 540, 820, 14, (255, 210, 120), 26, 1400, 0.08, 0.05)
    paste(img, glow(360, (255, 200, 110), 0.8), 540, 820, 1.0, 0.8 + 0.2 * math.sin(t * 3))
    paste(img, eiffel(900, lit=True), 540, 820, 1.0, ease(clamp(t / 0.6)))
    d = ImageDraw.Draw(img, "RGBA")
    rr = random.Random(5)
    for k in range(18):
        ang = rr.uniform(0, 6.28)
        rad = 300 + rr.uniform(0, 180) + math.sin(t * 2 + k) * 20
        x, y = 540 + math.cos(ang + t * 0.3) * rad, 820 + math.sin(ang + t * 0.3) * rad * 0.8
        r = rr.uniform(18, 30)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(230, 180, 60, 230), outline=(160, 110, 30, 255), width=4)
    big(t, 0.3, "UNA OPORTUNIDAD", 300, 80, WHITE, sub="DE ORO", subcol=YEL, pop=False)
    vignette(img, 200)


def sh_forgery(img, t, T, L):
    sky(img, (30, 22, 16), (12, 8, 6), 1.0)
    spotlight(img, t, 540, 0, 1500, 140, 600, 55)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, 1250, W, H], fill=(60, 36, 22))
    pap = spr(paper, 640, 860, "MINISTÈRE DES POSTES", 0, (244, 238, 222), (40, 36, 30), 4,
              ("ET TÉLÉGRAPHES", "", "Monsieur,", "", "Le gouvernement doit", "vendre la tour Eiffel", "comme ferraille.",
               "", "Confidentiel.", "", "Le Directeur général", "adjoint"))
    paste(img, pap, 540, 880, 1.0, 1.0, -2)
    hit = 1.6
    if t < hit:
        yy = lerp(300, 1060, ease(clamp((t - 0.4) / (hit - 0.4))))
    else:
        yy = lerp(1060, 500, ease(clamp((t - hit - 0.25) / 0.6)))
    if t > hit:
        st = Image.new("RGBA", (420, 200), (0, 0, 0, 0))
        sd = ImageDraw.Draw(st)
        sd.rounded_rectangle([10, 30, 410, 170], radius=14, outline=(200, 40, 40, 230), width=8)
        tw = sd.textlength("OFFICIEL", font=f(F_SER, 76))
        sd.text(((420 - tw) / 2, 52), "OFFICIEL", font=f(F_SER, 76), fill=(200, 40, 40, 230))
        paste(img, st, 640, 1120, 1.0, ease(clamp((t - hit) / 0.1)), -14)
    d.rounded_rectangle([600, yy - 140, 700, yy - 20], radius=20, fill=(90, 50, 30))
    d.rectangle([560, yy - 20, 740, yy + 30], fill=(40, 30, 26))
    vignette(img, 200)


def sh_hotel(img, t, T, L):
    sky(img, (46, 20, 22), (14, 6, 8), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    for x in range(0, W, 180):
        d.rectangle([x + 20, 300, x + 160, 1100], fill=(70, 30, 30))
        d.rectangle([x + 40, 330, x + 140, 1080], fill=(90, 40, 36))
    paste(img, glow(500, (255, 200, 120), 0.6), 540, 640)
    ImageDraw.Draw(img).line([(540, 0), (540, 480)], fill=(200, 160, 90), width=4)
    paste(img, chandelier(), 540, 600, 1.3)
    d.rectangle([0, 1180, W, H], fill=(30, 14, 12))
    d.ellipse([140, 1100, 940, 1260], fill=(120, 90, 60))
    d.ellipse([140, 1090, 940, 1240], fill=(240, 232, 214))
    for i, x in enumerate((210, 360, 720, 870)):
        paste(img, spr(person, 220, 560, (16, 12, 12), "bowler" if i % 2 else "top", True), x, 1010, 0.95)
    paste(img, spr(person, 220, 560, (10, 8, 8), "bowler", True, False, -1.4), 540, 960, 1.05)
    lower_third(img, t, 0.4, "HOTEL DE LUJO", "PARÍS · 1925", 300, max(2.2, T - 1.0))
    vignette(img, 190)


def sh_secret(img, t, T, L):
    sky(img, (24, 18, 14), (8, 6, 4), 1.0)
    spotlight(img, t, 540, 0, 1500, 150, 620, 55)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, 1200, W, H], fill=(230, 222, 204))
    bp = Image.new("RGBA", (760, 900), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bp)
    bd.rectangle([0, 0, 759, 899], fill=(28, 60, 110, 255))
    for x in range(0, 760, 40):
        bd.line([(x, 0), (x, 900)], fill=(60, 100, 150, 255), width=1)
    for y in range(0, 900, 40):
        bd.line([(0, y), (760, y)], fill=(60, 100, 150, 255), width=1)
    paste(bp, eiffel(760, (28, 60, 110), (220, 236, 255)), 380, 470, 1.0)
    paste(img, bp, 540, 900, 1.0, 1.0, 3)
    big(t, 0.4, "¿CHATARRA?", 290, 100, WHITE, hold=max(1.5, L[1][0] - 0.8), pop=False)
    a1 = L[1][0] + 0.3
    if t > a1:
        k = ease(clamp((t - a1) / 0.25))
        st = Image.new("RGBA", (640, 220), (0, 0, 0, 0))
        sd = ImageDraw.Draw(st)
        sd.rounded_rectangle([10, 30, 630, 190], radius=16, outline=(210, 40, 40, 240), width=10)
        tw = sd.textlength("CONFIDENCIAL", font=f(F_SER, 82))
        sd.text(((640 - tw) / 2, 56), "CONFIDENCIAL", font=f(F_SER, 82), fill=(210, 40, 40, 240))
        paste(img, st, 540, 900, lerp(1.6, 1.0, k), k, -10)
    vignette(img, 200)


def sh_poisson(img, t, T, L):
    sky(img, (40, 18, 18), (12, 6, 6), 1.0)
    spotlight(img, t, 420, 0, 1500, 120, 420, 60)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, 1330, W, H], fill=(24, 12, 10))
    paste(img, spr(person, 240, 600, (20, 14, 14), "bowler", True), 420, 1040, 1.15)
    paste(img, spr(person, 240, 600, (10, 8, 8), "top", True, False, -1.2), 860, 1040, 1.15, 0.9, flip=True)
    lower_third(img, t, 0.4, "ANDRÉ POISSON", "EMPRESARIO DE CHATARRA", 300, max(2.0, L[0][1]))
    a1 = L[1][0] + 1.2
    if t > a1:
        k = ease(clamp((t - a1) / 0.8))
        x = lerp(470, 760, k)
        paste(img, banknotes(), x, 900 - math.sin(k * math.pi) * 80, 0.55, 1.0, -10 + 20 * k)
        big(t, a1 + 0.3, "+ SOBORNO", 300, 96, YEL, pop=True)
    vignette(img, 200)


def sh_escape(img, t, T, L):
    night_sky(img, t, 1250, 0.9, (6, 8, 20), (30, 34, 60))
    mountains(img, 1250, 260, (16, 18, 30), 4, 0.6)
    ground(img, 1250, (10, 10, 16), (4, 4, 6))
    d = ImageDraw.Draw(img, "RGBA")
    d.line([(0, 1340), (W, 1340)], fill=(60, 60, 70), width=6)
    x = 1100 - (t * 260)
    smoke(img, t, [(x + 120, 1080, 1.2)], col=(160, 160, 170), alpha=110, spread=(-260, 160), grow=60, speed=0.6)
    paste(img, train(True), x + 820, 1180, 1.0)
    big(t, 0.4, "PARÍS → AUSTRIA", 300, 80, WHITE, sub="CON EL DINERO", subcol=YEL, pop=False)
    vignette(img, 180)


def sh_shame(img, t, T, L):
    sky(img, (20, 22, 30), (6, 6, 10), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    rr = random.Random(3)
    for k in range(120):
        x = rr.uniform(0, W)
        y = (rr.uniform(0, H) + t * 900) % H
        d.line([(x, y), (x - 6, y + 34)], fill=(160, 170, 200, 120), width=2)
    spotlight(img, t, 540, 0, 1500, 120, 480, 40, (200, 210, 240), False)
    paste(img, spr(person, 240, 600, (12, 12, 16), "bowler", True), 540, 1080, 1.2, 1.0, 6)
    big(t, L[0][0] + 1.6, "NO LO DENUNCIÓ", 300, 92, WHITE, pop=False)
    vignette(img, 210)


def sh_again(img, t, T, L):
    paris_night(img, t, 1300, 0.6)
    a1 = L[1][0] + 0.4
    title2(t, 0.4, "", "OTRA VEZ", 270, 10, 110, hold=max(1.2, a1 - 0.9))
    if t > a1:
        u = t - a1
        blue = (int(u * 4) % 2) == 0
        overlay(img, (40, 80, 255) if blue else (255, 40, 40), 0.22)
        paste(img, glow(500, (60, 100, 255) if blue else (255, 60, 60), 0.9), 120 if blue else 960, 1500)
        big(t, a1 + 0.2, "¡POLICÍA!", 300, 110, WHITE)
    vignette(img, 180)


def sh_usa(img, t, T, L):
    night_sky(img, t, 1200, 0.8, (8, 10, 24), (50, 40, 70))
    paste(img, nyc(), 540, 1200 - 350 + 30)
    sea(img, t, 1230, (30, 30, 60), (8, 8, 18), (120, 110, 160), 0.8)
    big(t, 0.3, "ESTADOS UNIDOS", 300, 84, WHITE, pop=False)
    vignette(img, 170)


def sh_alcatraz(img, t, T, L):
    night_sky(img, t, 1150, 1.0, (4, 6, 16), (24, 30, 54))
    fog(img, t, 1080, 70, 14)
    a = 0.6 + math.sin(t * 0.8) * 0.5
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(im).polygon([(840, 760), (840 + math.cos(a) * 1600, 760 + math.sin(a) * 1600 - 900),
                                (840 + math.cos(a + 0.16) * 1600, 760 + math.sin(a + 0.16) * 1600 - 900)], fill=(255, 240, 200, 50))
    AC(img, im.filter(ImageFilter.GaussianBlur(10)))
    paste(img, alcatraz(), 540, 1150 - 200)
    sea(img, t, 1150, (14, 20, 36), (4, 6, 12), (70, 90, 120), 0.8)
    lower_third(img, t, 0.3, "AL CAPONE", "TAMBIÉN CAYÓ EN SU TRAMPA", 300, 2.6)
    big(t, L[0][0] + 3.2, "ALCATRAZ", 300, 120, YEL)
    vignette(img, 200)


def sh_final(img, t, T, L):
    paris_night(img, t, 1300, 0.6, sparkle=1.0)
    k = ease(clamp((t - 0.6) / 1.2))
    paste(img, tag(), 650, 900 + 900 * k * k, 0.9, 1 - k * 0.7, 20 * k)
    vignette(img, 170)


FNS = {k: globals()["sh_" + k] for k, *_ in SHOTS}
AUDIO = {
    "music": [("open", "noir"), ("shame", "drone"), ("again", "tension"), ("usa", "noir")],
    "gains": {"noir": 1.1},
    "duck": [("shame", "shame@end", 0.5)],
    "amb": {"city": ["paris", "open", "again", "final"], "room": ["reader", "news", "forgery", "hotel", "secret", "poisson"],
            "rain": ["shame"], "sea": ["usa", "alcatraz"], "wind": ["escape"]},
    "sfx": [("open@L1-0.2", "chime", 0.07), ("reader+0.4", "paper", 0.2), ("news", "paper", 0.25), ("news@L1+0.6", "impact", 0.25),
            ("idea+0.2", "swell", 0.2), ("idea+0.3", "chime", 0.06),
            ("forgery+0.5", "type", 0.18), ("forgery+1.6", "thud", 0.5),
            ("hotel+0.3", "ding", 0.06), ("secret@L1+0.3", "thud", 0.45),
            ("poisson@L1+1.2", "paper", 0.25), ("poisson@L1+1.5", "chime", 0.06),
            ("escape", "train", 0.2), ("escape+0.2", "clack", 0.25),
            ("again@L1+0.4", "riser", 0.12), ("again@L1+0.4", "beep", 0.1), ("again@L1+0.65", "beep", 0.1), ("again@L1+0.9", "beep", 0.1),
            ("alcatraz@L0+3.2", "thud", 0.4), ("alcatraz+0.3", "bigbell", 0.06),
            ("final+0.6", "whoosh_up", 0.1), ("final+0.3", "chime", 0.06)],
    "bed": [("paris", "shame"), ("usa", "final")],
    "bpm": 84,
}
