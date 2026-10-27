"""V06 · La explosión de Tunguska (1908): un bosque arrasado sin cráter."""
from cine import *

TITLE = "La_explosion_que_no_dejo_crater"
LINES = [
    "En 1908, algo arrasó un bosque entero en Siberia… y *no dejó cráter*.",
    "¿Qué pudo tumbar *millones de árboles* sin tocar el suelo?",
    "30 de junio de 1908, siete de la mañana.",
    "Junto al río Tunguska, en plena Siberia.",
    "Una bola de fuego cruza el cielo… y *estalla en el aire*.",
    "A 65 kilómetros, un hombre sintió tanto calor que creyó que *su camisa ardía*.",
    "Y la onda expansiva lo lanzó varios metros.",
    "El bosque quedó tumbado en un área de *2.150 kilómetros cuadrados*.",
    "Más de *tres veces* la ciudad de Madrid.",
    "Y durante varios días, el cielo de Europa y Asia *brilló de noche*.",
    "En Suecia y Escocia se llegaron a hacer *fotos a medianoche*.",
    "La primera expedición científica no llegó hasta *1927*.",
    "Y lo más raro: allí *no había cráter*.",
    "Entonces… ¿qué fue?",
    "La explicación más aceptada: un asteroide de unos *50 o 60 metros*.",
    "Estalló a varios kilómetros de altura, con la fuerza de *cientos de bombas de Hiroshima*.",
    "Por eso no hubo cráter: *nunca llegó a tocar el suelo*.",
    "Si hubiera estallado sobre una gran ciudad… la habría *arrasado*.",
    "Por suerte, cayó en uno de los lugares *más vacíos del planeta*.",
    "Catástrofe o curiosidad… a veces, solo depende de dónde caiga.",
]
SHOTS = [("open", 0, 1, 0.3), ("dawn", 2, 3, 0.2), ("fireball", 4, 4, 0.5), ("witness", 5, 6, 0.4), ("area", 7, 8, 0.3),
         ("nightglow", 9, 10, 0.3), ("expedition", 11, 12, 0.3), ("question", 13, 13, 0.3), ("asteroid", 14, 16, 0.4),
         ("city", 17, 19, 1.8)]
FOCUS = {"open": (540, 1050), "dawn": (540, 1050), "fireball": (600, 800), "witness": (560, 1050), "area": (540, 900),
         "nightglow": (560, 1000), "expedition": (540, 1100), "asteroid": (540, 800), "city": (540, 1000)}
NOTIF = ("witness", 1.0)

PINE = (16, 30, 26)
PINE2 = (26, 44, 36)


# ------------------------------------------------------------------ sprites
HYPE = {"line": 1, "text": ['¿QUÉ TUMBÓ MILLONES', 'DE ÁRBOLES SIN TOCAR EL SUELO?'], "delay": [0, 1.2]}
STICKER_EXTRA = [('arraso', '🌲'), ('bosque', '🌲'), ('siberia', '🥶'), ('crater', '🕳️'), ('arboles', '🌲'), ('suelo', '⬇️'), ('manana', '🌅'), ('=rio', '🏞️'), ('bola', '☄️'), ('cielo', '☄️'), ('estalla', '💥'), ('camisa', '👕'), ('expansiva', '💨'), ('metros', '📏'), ('tumbado', '🌲'), ('cuadrados', '📐'), ('madrid', '🏙️'), ('brillo', '✨'), ('fotos', '📸'), ('medianoche', '🌙'), ('expedicion', '🧭'), ('raro', '🤨'), ('asteroide', '☄️'), ('hiroshima', '💣'), ('altura', '⬆️'), ('ciudad', '🏙️'), ('suerte', '🍀'), ('vacios', '🏜️'), ('planeta', '🌍')]
KW_OVERRIDE = {16: [], 19: []}
NARRATOR = {"open": ("wave", "left"), "dawn": ("think", "left"), "fireball": ("surprise", "left"), "witness": ("point", "left"),
            "area": ("surprise", "left"), "nightglow": ("point", "left"), "expedition": ("think", "left"), "question": ("think", "left"),
            "asteroid": ("point", "left"), "city": ("think", "left")}

def hut():
    def fn(d, s):
        log, logd = (110, 74, 44), (80, 52, 30)
        d.rectangle(sb([40, 160, 560, 400], s), fill=log)
        for y in range(170, 400, 26):
            d.line(sc([(40, y), (560, y)], s), fill=logd, width=int(4 * s))
        d.polygon(sc([(0, 170), (300, 20), (600, 170)], s), fill=(70, 46, 30))
        d.rectangle(sb([250, 250, 340, 400], s), fill=(40, 26, 18))
        d.rectangle(sb([400, 230, 490, 310], s), fill=(255, 210, 140))
        d.rectangle(sb([0, 400, 600, 420], s), fill=(60, 40, 26))
    return sprite("hut", 600, 420, fn)


def rock(seed=1):
    def fn(d, s):
        rr = random.Random(seed)
        pts = []
        for k in range(14):
            a = k / 14 * 2 * math.pi
            r = 150 * rr.uniform(0.75, 1.0)
            pts.append((180 + math.cos(a) * r, 180 + math.sin(a) * r * 0.85))
        d.polygon(sc(pts, s), fill=(90, 80, 74))
        d.polygon(sc(pts[3:9] + [(180, 180)], s), fill=(64, 56, 52))
        for _ in range(7):
            x, y, r = rr.uniform(90, 270), rr.uniform(90, 260), rr.uniform(10, 28)
            d.ellipse(sb([x - r, y - r, x + r, y + r], s), fill=(70, 62, 58))
    return sprite(("rock", seed), 360, 360, fn)


def taiga(img, t, hz, fallen=0.0, cx=540, light=1.0):
    fq = round(fallen, 1)
    mountains(img, hz - 40, 160, (int(40 * light), int(50 * light), int(60 * light)), 6, 0.5)
    forest(img, hz - 30, PINE2, 70, 90, 170, 5, fq, cx)
    ground(img, hz + 40, (30, 40, 30), (12, 16, 12))
    forest(img, hz + 30, PINE, 40, 180, 330, 9, fq, cx)


# ------------------------------------------------------------------ planos
def sh_open(img, t, T, L):
    sky(img, (40, 60, 90), (230, 170, 130), 1.3)
    paste(img, glow(400, (255, 200, 150), 0.7), 540, 1100)
    fog(img, t, 1080, 60, 10)
    a1 = L[1][0]
    taiga(img, t, 1150, 0.0 if t < a1 + 0.4 else 1.0)
    fog(img, t * 1.4, 1250, 50, 18)
    title2(t, 0.25, "LA EXPLOSIÓN", "QUE NO DEJÓ CRÁTER", 290, 64, 80, hold=max(1.5, L[1][0] - 0.4))
    vignette(img, 170)


def sh_dawn(img, t, T, L):
    sky(img, (50, 70, 110), (250, 180, 130), 1.4)
    paste(img, glow(360, (255, 210, 150), 0.8), 760, 1050)
    taiga(img, t, 1150)
    d = ImageDraw.Draw(img, "RGBA")
    left = [(500 + math.sin(k * 0.5) * 60 - k * 18, 1200 + k * 30) for k in range(15)]
    right = [(600 + math.sin(k * 0.5) * 60 + k * 26, 1200 + k * 30) for k in range(14, -1, -1)]
    d.polygon(left + right, fill=(90, 120, 150, 255))
    for k in range(1, 14):
        y = 1200 + k * 30
        d.line([(530 + math.sin(k * 0.5) * 60 - k * 10, y), (580 + math.sin(k * 0.5) * 60 + k * 16, y)], fill=(170, 200, 220, 110), width=3)
    date_stamp(t, 0.3, "30 · 06 · 1908 · 7:14", 300, max(1.6, L[1][0] - 0.3))
    lower_third(img, t, L[1][0] + 0.1, "RÍO TUNGUSKA", "SIBERIA · IMPERIO RUSO", 300, max(1.8, L[1][1] - L[1][0]))
    vignette(img, 160)


def sh_fireball(img, t, T, L):
    q = clamp(t / 2.2)
    sky(img, (60, 80, 120), (250, 190, 140), 1.3)
    hit = 2.2
    x = lerp(-100, 640, q)
    y = lerp(200, 700, q)
    d = ImageDraw.Draw(img, "RGBA")
    if t < hit:
        for k in range(30):
            u = k / 30
            tx, ty = lerp(-100, x, u), lerp(200, y, u)
            r = 6 + 40 * u
            d.ellipse([tx - r, ty - r, tx + r, ty + r], fill=(255, 220, 160, int(30 + 150 * u)))
        paste(img, glow(160, (255, 230, 170), 1.0), x, y)
    taiga(img, t, 1250, 0.0)
    if t >= hit:
        u = t - hit
        overlay(img, (255, 248, 230), math.exp(-u * 2.2))
        paste(img, glow(int(300 + 500 * min(1, u)), (255, 200, 120), 1.0), 640, 700, 1.0, max(0, 1 - u / 2.4))
    vignette(img, 160)


def sh_witness(img, t, T, L):
    sky(img, (70, 70, 100), (240, 170, 120), 1.2)
    a1 = L[1][0]
    heat = clamp((t - 0.5) / 2.0) * (1 - clamp((t - a1 - 1.0) / 2.0))
    overlay(img, (255, 120, 40), heat * 0.35)
    paste(img, glow(600, (255, 160, 80), 0.8), 980, 300, 1.0, heat)
    taiga(img, t, 1180, 0.0)
    sx, sy = shake(t, a1 + 0.2, 20, 3)
    paste(img, hut(), 380 + sx, 1250 + sy, 1.0)
    if t < a1 + 0.2:
        px, py, rot = 760, 1290, 0
    else:
        u = ease(clamp((t - a1 - 0.2) / 0.7))
        px, py, rot = lerp(760, 960, u), 1290 - math.sin(u * math.pi) * 120 + u * 60, -80 * u
    paste(img, spr(person, 220, 560, (20, 16, 18), "cap", True), px, py, 0.8, 1.0, rot)
    if t > a1 + 0.2:
        overlay(img, (255, 240, 220), 0.6 * math.exp(-(t - a1 - 0.2) * 4))
    lower_third(img, t, 0.3, "VANAVARA", "A 65 KM DE LA EXPLOSIÓN", 300, max(2.4, a1 - 0.6))
    vignette(img, 180)


def sh_area(img, t, T, L):
    sky(img, (26, 34, 26), (14, 18, 14), 1.0)
    d = ImageDraw.Draw(img, "RGBA")
    cx, cy = 540, 900
    rr = random.Random(4)
    R_ = 420
    q = ease(clamp((t - 0.2) / 1.6))
    for _ in range(900):
        ang = rr.uniform(0, 2 * math.pi)
        dist = math.sqrt(rr.uniform(0, 1)) * 520
        x, y = cx + math.cos(ang) * dist, cy + math.sin(ang) * dist * 1.0
        L_ = rr.uniform(14, 26)
        inside = dist < R_ * q * (1 + 0.15 * math.sin(ang * 2))
        if inside:
            d.line([(x, y), (x + math.cos(ang) * L_, y + math.sin(ang) * L_)], fill=(110, 90, 60, 255), width=4)
        else:
            d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=(40, 80, 50, 255))
    big(t, 0.3, counter(t, 0.3, 1.9, 0, 2150) + " KM²", 300, 116, YEL)
    a1 = L[1][0]
    if t > a1:
        k = ease(clamp((t - a1) / 0.5))
        rm = R_ / math.sqrt(3.56)
        for i, (ox, oy) in enumerate(((-110, -60), (120, -40), (0, 130))):
            kk = ease(clamp((t - a1 - i * 0.35) / 0.4))
            if kk > 0:
                d.ellipse([cx + ox - rm * 0.55, cy + oy - rm * 0.55, cx + ox + rm * 0.55, cy + oy + rm * 0.55],
                          outline=(255, 255, 255, int(230 * kk)), width=6)
                dd = td()
                spaced(dd, cx + ox, cy + oy - 20, "MADRID", f(F_SER, 34), (255, 255, 255, int(255 * kk)), 3)
    vignette(img, 190)


def sh_nightglow(img, t, T, L):
    sky(img, (30, 40, 90), (240, 200, 170), 1.0)
    stars(img, t, 500, 0.4, 60, 3)
    d = ImageDraw.Draw(img, "RGBA")
    rr = random.Random(2)
    x = 0
    while x < W:
        bw, bh = rr.uniform(120, 200), rr.uniform(160, 300)
        d.rectangle([x, 1300 - bh, x + bw, 1300], fill=(20, 18, 26))
        d.polygon([(x - 6, 1300 - bh), (x + bw / 2, 1300 - bh - 80), (x + bw + 6, 1300 - bh)], fill=(20, 18, 26))
        x += bw
    ground(img, 1300, (70, 64, 80), (30, 28, 36))
    paste(img, spr(person, 220, 560, (12, 10, 14), "cap", True, False, -1.2), 420, 1240, 0.95)
    d.line([(560, 1430), (600, 1190)], fill=(20, 18, 20), width=6)
    d.line([(640, 1430), (600, 1190)], fill=(20, 18, 20), width=6)
    d.rectangle([555, 1130, 660, 1200], fill=(20, 18, 20))
    if t > L[1][0] + 0.6:
        fl = math.exp(-(t - L[1][0] - 0.6) * 5)
        overlay(img, (255, 255, 255), fl * 0.6)
    date_stamp(t, 0.3, "MEDIANOCHE · JULIO DE 1908", 300)
    vignette(img, 160)


def sh_expedition(img, t, T, L):
    sky(img, (100, 120, 150), (220, 210, 190), 1.2)
    taiga(img, t, 1150, 1.0)
    for i, x0 in enumerate((200, 330, 460)):
        x = x0 + t * 40
        paste(img, spr(person, 220, 560, (24, 20, 20), "cap", True, False, 0.0, round((t * 5 + i) % 6.28, 1)), x, 1300, 0.8)
    date_stamp(t, 0.3, "1927 · EXPEDICIÓN DE KULIK", 300, max(1.8, L[1][0] - 0.4))
    big(t, L[1][0] + 0.8, "NI RASTRO", 300, 100, WHITE, sub="DE UN CRÁTER", subcol=YEL)
    vignette(img, 170)


def sh_question(img, t, T, L):
    space_bg(img, t, 12)
    paste(img, rock(2), 540 + t * 20, 900, 1.2, 1.0, t * 12)
    big(t, 0.2, "¿QUÉ FUE?", 320, 110, WHITE, pop=False)
    vignette(img, 200)


def sh_asteroid(img, t, T, L):
    a1, a2 = L[1][0], L[2][0]
    hz = 1350
    sky(img, (30, 40, 70), (200, 150, 120), 1.3)
    burst = a1 + 0.2
    if t < burst:
        q = clamp(t / burst)
        x, y = lerp(900, 560, q), lerp(200, 560, q)
        d = ImageDraw.Draw(img, "RGBA")
        for k in range(26):
            u = k / 26
            tx, ty = lerp(1150, x, u), lerp(-100, y, u)
            r = 10 + 50 * u
            d.ellipse([tx - r, ty - r, tx + r, ty + r], fill=(255, 200, 140, int(20 + 120 * u)))
        paste(img, glow(140, (255, 210, 150), 1.0), x, y)
        paste(img, rock(1), x, y, 0.5, 1.0, t * 40)
        big(t, 0.4, "50-60 METROS", 300, 100, YEL)
    else:
        u = t - burst
        overlay(img, (255, 236, 200), 0.9 * math.exp(-u * 3))
        paste(img, glow(int(260 + 400 * min(1, u / 1.5)), (255, 190, 110), 1.0), 560, 560, 1.0, max(0.25, 1 - u / 3))
        ring = 100 + u * 520
        d = ImageDraw.Draw(img, "RGBA")
        d.ellipse([560 - ring, 560 - ring, 560 + ring, 560 + ring], outline=(255, 240, 210, int(200 * max(0, 1 - u / 2.5))), width=10)
        big(t, burst + 0.6, "CIENTOS DE", 280, 76, WHITE, sub="BOMBAS DE HIROSHIMA", subcol=YEL, pop=False,
            hold=max(1.0, a2 - burst - 1.0))
    fallen = clamp((t - burst - 0.5) / 1.0)
    taiga(img, t, hz, fallen, 560)
    d = ImageDraw.Draw(img, "RGBA")
    d.line([(160, 560), (160, hz)], fill=(255, 255, 255, 160), width=3)
    for yy in (560, hz):
        d.line([(140, yy), (180, yy)], fill=(255, 255, 255, 160), width=3)
    dd = td()
    if t > burst:
        dd.text((190, (560 + hz) / 2 - 30), "VARIOS KM", font=f(F_SER, 40), fill=(255, 255, 255, 220))
    if t > a2:
        big(t, a2 + 0.3, "NUNCA TOCÓ", 300, 96, WHITE, sub="EL SUELO", subcol=YEL)
    vignette(img, 170)


def sh_city(img, t, T, L):
    a1 = L[1][0]
    if t < a1:
        night_sky(img, t, 1300, 0.6, (10, 10, 24), (60, 40, 50))
        d = ImageDraw.Draw(img, "RGBA")
        rr = random.Random(7)
        x = 0
        while x < W:
            bw, bh = rr.uniform(70, 150), rr.uniform(250, 700)
            d.rectangle([x, 1300 - bh, x + bw, 1300], fill=(20, 20, 32))
            for wy in range(int(1300 - bh + 20), 1280, 36):
                for wx in range(int(x + 10), int(x + bw - 14), 24):
                    if rr.random() < 0.3:
                        d.rectangle([wx, wy, wx + 10, wy + 14], fill=(255, 220, 150))
            x += bw + 4
        ground(img, 1300, (20, 20, 26), (8, 8, 10))
        k = ease(clamp((t - 0.6) / 0.8))
        rr2 = 380 * k
        d.ellipse([540 - rr2, 900 - rr2, 540 + rr2, 900 + rr2], outline=(230, 60, 60, 230), width=10)
    else:
        space_bg(img, t, 13)
        g = spr(globe_sprite, 100.0, 50.0, 420, ())
        paste(img, g, 540, 900)
        x, y = proj_point(100.0, 50.0, 420, 101.9, 60.9)
        paste(img, glow(70, (255, 180, 90), 1.0), 540 + x, 900 + y, 1.0, 0.7 + 0.3 * math.sin(t * 5))
        a2 = L[2][0] if len(L) > 2 else T
        lower_third(img, t, a1 + 0.3, "SIBERIA", "UNO DE LOS LUGARES MÁS VACÍOS", 300, min(4.0, max(1.5, a2 - a1 - 0.9)))
        if len(L) > 2:    # reflexión final, en pantalla
            title2(t, a2 + 0.2, "¿CATÁSTROFE O CURIOSIDAD?", "DEPENDE DE DÓNDE CAIGA", 250, 48, 60,
                   hold=max(2.0, T - a2 - 0.4), c1=WHITE, c2=YEL, track=6)
    vignette(img, 180)


FNS = {k: globals()["sh_" + k] for k, *_ in SHOTS}
AUDIO = {
    "music": [("open", "drone"), ("fireball", "tension"), ("area", "doc"), ("question", "drone"), ("asteroid", "epic"),
              ("city", "space")],
    "amb": {"wind": ["open", "dawn", "witness", "expedition"], "birds": ["dawn"], "space": ["question", "city"],
            "city": ["nightglow"]},
    "sfx": [("open@L1+0.3", "rumble", 0.25), ("open@L1+0.4", "whoosh", 0.2),
            ("fireball+0.2", "riser_long", 0.18), ("fireball+2.2", "boom", 0.6),
            ("witness@L1+0.2", "boom", 0.4), ("witness@L1+0.25", "thud", 0.4),
            ("area+0.2", "swell", 0.15), ("area@L1", "pop", 0.2), ("area@L1+0.35", "pop", 0.2), ("area@L1+0.7", "pop", 0.2),
            ("nightglow@L1+0.6", "shutter", 0.3),
            ("expedition@L1+0.8", "impact", 0.25), ("question", "heart", 0.35), ("question+0.75", "heart", 0.35),
            ("asteroid+0.2", "riser", 0.15), ("asteroid@L1+0.2", "boom", 0.6), ("asteroid@L1+0.8", "rumble", 0.35),
            ("asteroid@L2+0.3", "thud", 0.3), ("city+0.6", "impact", 0.25), ("city@L1+0.3", "chime", 0.06)],
    "bed": [("witness", "question")],
    "bpm": 92,
}
