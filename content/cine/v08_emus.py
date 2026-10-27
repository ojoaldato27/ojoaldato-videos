"""V08 · La Gran Guerra del Emú (Australia, 1932)."""
from cine import *

TITLE = "La_guerra_que_Australia_perdio_contra_unos_pajaros"
LINES = [
    "En 1932, el ejército de Australia declaró la guerra… a unos *pájaros*.",
    "¿Quién crees que ganó?",
    "Australia Occidental, 1932.",
    "Muchos granjeros eran antiguos soldados de la Primera Guerra Mundial.",
    "Y tenían un problema: unos *20.000 emús* arrasando sus campos de trigo.",
    "Los emús miden casi *dos metros* y corren a unos 50 kilómetros por hora.",
    "Los granjeros pidieron ayuda… y el gobierno mandó *ametralladoras*.",
    "Al mando, el mayor *Meredith*, con dos ametralladoras y *10.000 balas*.",
    "Noviembre de 1932: empieza la operación.",
    "Primera emboscada: unos mil emús a tiro… y la ametralladora *se atasca*.",
    "Prueban a disparar desde un camión… pero el camión *no puede seguirlos*.",
    "Los emús se separan en grupos pequeños, como una *guerrilla*.",
    "Meredith llegó a decir que aguantaban las balas *como tanques*.",
    "Tras unas semanas, el ejército *se retira*.",
    "Según Meredith: *986 emús* abatidos con 9.860 balas.",
    "*Diez balas* por cada pájaro.",
    "Y los emús siguieron comiéndose el trigo.",
    "Así que la respuesta es: ganaron *los emús*.",
]
SHOTS = [("open", 0, 1, 0.3), ("farm", 2, 3, 0.3), ("invasion", 4, 5, 0.3), ("guns", 6, 7, 0.3), ("ambush", 8, 9, 0.4),
         ("truck", 10, 10, 0.3), ("guerrilla", 11, 12, 0.4), ("retreat", 13, 13, 0.3), ("stats", 14, 15, 0.4),
         ("winner", 16, 17, 1.8)]
FOCUS = {"open": (560, 1100), "farm": (540, 1050), "invasion": (560, 1100), "guns": (520, 1080), "ambush": (560, 1100),
         "truck": (540, 1100), "retreat": (560, 1100), "stats": (540, 900), "winner": (560, 1100)}
NOTIF = ("guns", 1.0)

EMU = (70, 54, 40)
WHEAT = (226, 186, 100)


# ------------------------------------------------------------------ sprites
HYPE = {"line": 1, "text": ['¿QUIÉN CREES', 'QUE GANÓ?'], "delay": [0, 0.4]}
KW_OVERRIDE = {16: ["SIGUIERON COMIÉNDOSE EL TRIGO"]}
STICKER_EXTRA = [('ejercito', '🪖'), ('guerra', '⚔️'), ('pajaro', '🐦'), ('gano', '🏆'), ('australia', '🦘'), ('granjero', '🌾'), ('soldado', '🪖'), ('problema', '😩'), ('emu', '🐦'), ('trigo', '🌾'), ('campos', '🌾'), ('metros', '📏'), ('corren', '💨'), ('ayuda', '🆘'), ('gobierno', '🏛️'), ('ametralladora', '🔫'), ('balas', '💥'), ('noviembre', '📅'), ('emboscada', '🫣'), ('atasca', '⚠️'), ('disparar', '💥'), ('camion', '🚚'), ('guerrilla', '🥷'), ('tanques', '🛡️'), ('retira', '🏳️'), ('abatidos', '🎯'), ('comiendo', '😋')]

def emu(pose="stand", phase=0, col=EMU):
    def fn(d, s):
        c, c2 = col, tuple(max(0, x - 20) for x in col)
        bx, by = 200, 300
        # cuerpo con plumaje caído (borde inferior dentado)
        top = [(bx - 130, by + 10), (bx - 100, by - 60), (bx - 20, by - 90), (bx + 60, by - 70), (bx + 110, by - 20)]
        skirt = []
        for k in range(11):
            u = k / 10
            x = bx + 110 - u * 250
            y = by + 60 + math.sin(u * math.pi) * 40 + (18 if k % 2 else 0)
            skirt.append((x, y))
        d.polygon(sc(top + skirt, s), fill=c)
        for k in range(14):
            x = bx - 100 + (k % 7) * 30
            y = by - 30 + (k // 7) * 50
            d.line(sc([(x, y), (x - 14, y + 30)], s), fill=c2, width=int(5 * s))
        if pose == "peck":
            neck = [(bx + 70, by - 30), (bx + 150, by + 40), (bx + 190, by + 150)]
            head = (bx + 200, by + 170)
        else:
            neck = [(bx + 60, by - 40), (bx + 90, by - 150), (bx + 96, by - 230)]
            head = (bx + 108, by - 250)
        d.line(sc(neck, s), fill=(90, 90, 110), width=int(22 * s), joint="curve")
        d.ellipse(sb([head[0] - 24, head[1] - 20, head[0] + 24, head[1] + 20], s), fill=(60, 60, 80))
        d.polygon(sc([(head[0] + 18, head[1] - 6), (head[0] + 52, head[1] + 4), (head[0] + 18, head[1] + 10)], s), fill=(50, 40, 30))
        d.ellipse(sb([head[0] + 2, head[1] - 10, head[0] + 12, head[1]], s), fill=(240, 120, 40))
        legc = (110, 96, 80)
        if pose == "run":
            a = math.sin(phase) * 0.7
            for sgn in (1, -1):
                kx, ky = bx + sgn * math.sin(a) * 60, by + 170
                fx_, fy = bx + sgn * math.sin(a) * 120 + 20, by + 330
                d.line(sc([(bx, by + 60), (kx, ky), (fx_, fy)], s), fill=legc, width=int(12 * s), joint="curve")
                d.line(sc([(fx_, fy), (fx_ + 34, fy)], s), fill=legc, width=int(8 * s))
        else:
            for dx in (-20, 30):
                d.line(sc([(bx + dx, by + 60), (bx + dx + 10, by + 190), (bx + dx, by + 330)], s), fill=legc, width=int(12 * s))
                d.line(sc([(bx + dx, by + 330), (bx + dx + 34, by + 330)], s), fill=legc, width=int(8 * s))
    return sprite(("emu", pose, phase, col), 420, 650, fn)


def truck():
    def fn(d, s):
        c = (40, 44, 36)
        d.rectangle(sb([40, 140, 520, 250], s), fill=c)
        d.polygon(sc([(520, 250), (520, 90), (640, 90), (700, 170), (760, 180), (760, 250)], s), fill=c)
        d.rectangle(sb([560, 110, 630, 160], s), fill=(140, 160, 170))
        for x in (150, 640):
            d.ellipse(sb([x - 60, 210, x + 60, 330], s), fill=(20, 20, 20))
            d.ellipse(sb([x - 24, 246, x + 24, 294], s), fill=(90, 90, 90))
        d.line(sc([(260, 140), (300, 60)], s), fill=c, width=int(12 * s))
        d.rectangle(sb([280, 40, 460, 70], s), fill=c)
    return sprite("truck", 780, 340, fn)


def lewis():
    def fn(d, s):
        c = (34, 34, 30)
        d.line(sc([(200, 200), (80, 360)], s), fill=c, width=int(10 * s))
        d.line(sc([(200, 200), (320, 360)], s), fill=c, width=int(10 * s))
        d.line(sc([(200, 200), (200, 360)], s), fill=c, width=int(10 * s))
        d.rounded_rectangle(sb([60, 170, 400, 220], s), radius=int(20 * s), fill=c)
        d.rectangle(sb([400, 185, 520, 200], s), fill=c)
        d.ellipse(sb([150, 120, 250, 170], s), fill=c)
        d.polygon(sc([(60, 180), (0, 230), (20, 240), (70, 210)], s), fill=c)
    return sprite("lewis", 540, 380, fn)


def windmill():
    def fn(d, s):
        c = (40, 34, 32)
        d.line(sc([(150, 600), (190, 120)], s), fill=c, width=int(8 * s))
        d.line(sc([(250, 600), (210, 120)], s), fill=c, width=int(8 * s))
        for y in range(200, 600, 100):
            d.line(sc([(150 + (600 - y) * 0.08, y), (250 - (600 - y) * 0.08, y)], s), fill=c, width=int(5 * s))
        for k in range(12):
            a = k / 12 * 2 * math.pi
            d.line(sc([(200, 110), (200 + math.cos(a) * 100, 110 + math.sin(a) * 100)], s), fill=c, width=int(9 * s))
        d.polygon(sc([(220, 110), (340, 90), (340, 140)], s), fill=c)
    return sprite("mill", 400, 600, fn)


def wheat(img, t, y, density=1.0, seed=2, col=WHEAT, trampled=0.0):
    d = ImageDraw.Draw(img, "RGBA")
    rr = random.Random(seed)
    for i in range(int(260 * density)):
        x = rr.uniform(-20, W + 20)
        yy = y + rr.uniform(0, 260)
        h = rr.uniform(40, 90) * (0.6 + (yy - y) / 260)
        if rr.random() < trampled:
            d.line([(x, yy), (x + h * 0.9, yy - h * 0.15)], fill=tuple(int(c * 0.75) for c in col) + (255,), width=3)
            continue
        sw = math.sin(t * 1.5 + x / 80) * 8
        d.line([(x, yy), (x + sw, yy - h)], fill=col + (255,), width=3)
        d.ellipse([x + sw - 4, yy - h - 14, x + sw + 4, yy - h + 2], fill=col + (255,))


def outback(img, t, hz=1180, sunset=True):
    if sunset:
        sky(img, (60, 70, 140), (255, 170, 90), 1.3)
        paste(img, glow(420, (255, 200, 120), 0.8), 760, hz - 60)
    else:
        sky(img, (110, 160, 220), (250, 220, 170), 1.3)
    mountains(img, hz, 90, (150, 90, 70) if sunset else (190, 130, 90), 3, 0.3, peaks=3)
    ground(img, hz, (200, 140, 80), (120, 80, 50))


# ------------------------------------------------------------------ planos
def sh_open(img, t, T, L):
    outback(img, t)
    wheat(img, t, 1240, 1.0)
    paste(img, emu("stand"), 640, 1120, 1.4)
    title2(t, 0.25, "LA GUERRA", "CONTRA LOS EMÚS", 290, 70, 86, hold=max(1.5, L[1][0] - 0.3))
    vignette(img, 160)


def sh_farm(img, t, T, L):
    outback(img, t, 1180, False)
    clouds(img, t, 700, (255, 255, 255), 120, 8, 4, 1.0)
    paste(img, windmill(), 860, 1180 - 300)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([120, 1000, 460, 1180], fill=(170, 150, 120))
    d.polygon([(90, 1010), (290, 900), (490, 1010)], fill=(120, 60, 50))
    d.rectangle([250, 1080, 310, 1180], fill=(80, 60, 44))
    wheat(img, t, 1220, 1.0, 3)
    paste(img, spr(person, 240, 600, (50, 40, 34), "cap", True), 600, 1230, 1.05)
    date_stamp(t, 0.3, "AUSTRALIA OCCIDENTAL · 1932", 300, max(1.8, L[1][0] - 0.3))
    lower_third(img, t, L[1][0] + 0.2, "ANTIGUOS SOLDADOS", "CONVERTIDOS EN GRANJEROS", 300, 3.2)
    vignette(img, 150)


def sh_invasion(img, t, T, L):
    outback(img, t, 1100, False)
    wheat(img, t, 1140, 1.2, 4, trampled=clamp(t / T) * 0.6)
    rr = random.Random(5)
    items = sorted([(rr.uniform(-60, W + 60), rr.uniform(1080, 1400), rr.choice(["stand", "peck", "peck"])) for _ in range(16)], key=lambda v: v[1])
    a1 = L[1][0]
    for x, y, pose in items:
        sc_ = 0.35 + (y - 1080) / 320 * 0.35
        paste(img, emu(pose), x + math.sin(t + x) * 6, y - 200 * sc_, sc_)
    if t < a1:
        big(t, 0.3, counter(t, 0.3, 1.8, 0, 20000), 300, 124, YEL, sub="EMÚS")
    else:
        d = ImageDraw.Draw(img, "RGBA")
        k = ease(clamp((t - a1) / 0.5))
        x0 = 860
        d.rectangle([x0 - 8, 1400 - 640, x0 + 8, 1400], fill=(255, 255, 255, int(220 * k)))
        for i in range(5):
            y = 1400 - i * 160
            d.line([(x0 - 30, y), (x0 + 30, y)], fill=(255, 255, 255, int(220 * k)), width=4)
        paste(img, emu("stand"), 640, 1400 - 325 * 1.0, 1.0, k)
        big(t, a1 + 0.2, "1,9 M · 50 KM/H", 300, 92, YEL, pop=False)
    vignette(img, 150)


def sh_guns(img, t, T, L):
    outback(img, t, 1180, False)
    paste(img, truck(), 760, 1180 - 60, 0.9)
    paste(img, lewis(), 360, 1260, 0.9)
    for i, x in enumerate((220, 520)):
        paste(img, spr(person, 240, 600, (60, 56, 40), "cap", True, False, -0.8 if i else 0.0), x, 1200, 0.95)
    lower_third(img, t, L[1][0] + 0.1, "MAYOR G. P. W. MEREDITH", "ARTILLERÍA REAL AUSTRALIANA", 300, 2.4)
    big(t, L[1][0] + 2.8, "10.000 BALAS", 300, 104, YEL, sub="2 AMETRALLADORAS LEWIS")
    vignette(img, 150)


def sh_ambush(img, t, T, L):
    outback(img, t, 1100, False)
    wheat(img, t, 1140, 1.2, 6)
    rr = random.Random(7)
    for k in range(12):
        x, y = rr.uniform(200, 1080), rr.uniform(1060, 1250)
        sc_ = 0.3 + (y - 1060) / 190 * 0.25
        paste(img, emu("peck" if k % 2 else "stand"), x, y - 200 * sc_, sc_)
    paste(img, lewis(), 220, 1360, 1.1)
    date_stamp(t, 0.3, "4 DE NOVIEMBRE DE 1932", 300, max(1.6, L[1][0] - 0.3))
    a_jam = L[1][1] - 1.4
    if t > a_jam:
        k = ease(clamp((t - a_jam) / 0.25))
        st = Image.new("RGBA", (620, 220), (0, 0, 0, 0))
        sd = ImageDraw.Draw(st)
        sd.rounded_rectangle([10, 30, 610, 190], radius=16, outline=(220, 40, 40, 240), width=10)
        tw = sd.textlength("¡ATASCADA!", font=f(F_SER, 90))
        sd.text(((620 - tw) / 2, 50), "¡ATASCADA!", font=f(F_SER, 90), fill=(220, 40, 40, 240))
        paste(img, st, 540, 820, lerp(1.6, 1.0, k), k, -8)
    vignette(img, 150)


def sh_truck(img, t, T, L):
    outback(img, t, 1100, False)
    ground(img, 1100, (210, 160, 100), (150, 100, 60))
    bump = abs(math.sin(t * 9)) * 18
    tx = 120 + t * 90
    smoke(img, t, [(tx - 120, 1250, 1.4)], col=(210, 170, 120), alpha=120, spread=(220, 40), grow=80, speed=0.8)
    paste(img, truck(), tx, 1190 - bump, 0.75, 1.0, math.sin(t * 9) * 2)
    for i in range(5):
        ex = 520 + i * 120 + t * 170
        paste(img, emu("run", round((t * 12 + i) % 6.28, 1)), ex % (W + 300), 1080 + (i % 2) * 40, 0.5)
    big(t, 0.4, "DEMASIADO RÁPIDOS", 300, 84, WHITE, pop=False)
    vignette(img, 150)


def sh_guerrilla(img, t, T, L):
    a1 = L[1][0]
    if t < a1:
        ground(img, 0, (200, 150, 90), (170, 120, 70))
        d = ImageDraw.Draw(img, "RGBA")
        rr = random.Random(3)
        q = ease(clamp((t - 0.6) / 2.0))
        groups = [(300, 600), (800, 560), (250, 1150), (780, 1200), (540, 880)]
        for i in range(60):
            g = groups[i % 5]
            x0, y0 = 540 + rr.gauss(0, 60), 880 + rr.gauss(0, 60)
            x = lerp(x0, g[0] + rr.gauss(0, 30), q)
            y = lerp(y0, g[1] + rr.gauss(0, 30), q)
            d.ellipse([x - 10, y - 10, x + 10, y + 10], fill=(60, 44, 32, 255))
        big(t, 0.4, "GUERRILLA", 300, 110, YEL)
    else:
        outback(img, t, 1180)
        paste(img, emu("stand"), 760, 1120, 1.3)
        quote(t, a1 + 0.3, ["PUEDEN ENFRENTARSE A", "LAS AMETRALLADORAS CON", "LA INVULNERABILIDAD", "DE LOS TANQUES»"], "— MAYOR MEREDITH, 1932", 340, 52)
    vignette(img, 160)


def sh_retreat(img, t, T, L):
    outback(img, t, 1180)
    tx = 700 - t * 120
    smoke(img, t, [(tx + 200, 1260, 1.0)], col=(210, 160, 110), alpha=110, spread=(-160, 30), grow=60, speed=0.8)
    paste(img, truck(), tx, 1200, 0.55, 1.0, 0, flip=True)
    paste(img, emu("stand"), 880, 1130, 1.1)
    big(t, 0.4, "RETIRADA", 300, 110, WHITE)
    vignette(img, 170)


def sh_stats(img, t, T, L):
    sky(img, (40, 30, 20), (14, 10, 8), 1.0)
    spotlight(img, t, 540, 0, 1400, 140, 600, 45)
    d = ImageDraw.Draw(img, "RGBA")
    a1 = L[1][0]
    nb = int(clamp((t - 0.3) / 2.2) * 100)
    for i in range(nb):
        x = 160 + (i % 20) * 38
        y = 600 + (i // 20) * 90
        d.rounded_rectangle([x, y, x + 18, y + 60], radius=8, fill=(200, 160, 70, 255))
        d.rectangle([x, y + 40, x + 18, y + 60], fill=(150, 110, 40, 255))
    ne = int(clamp((t - 1.0) / 1.5) * 10)
    for i in range(ne):
        paste(img, emu("stand"), 140 + i * 88, 1200, 0.22)
    dd = td()
    if t < a1:
        spaced(dd, 540, 260, counter(t, 0.3, 2.5, 0, 9860) + " BALAS", f(F_SER, 80), YEL + (255,), 4)
        spaced(dd, 540, 370, counter(t, 1.0, 2.5, 0, 986) + " EMÚS", f(F_SER, 60), (255, 255, 255, 255), 4)
    else:
        big(t, a1 + 0.1, "10 BALAS", 300, 120, YEL, sub="POR CADA EMÚ")
    vignette(img, 190)


def sh_winner(img, t, T, L):
    outback(img, t)
    wheat(img, t, 1240, 1.1, 8, trampled=0.4)
    rr = random.Random(9)
    for k in range(7):
        x, y = rr.uniform(0, W), rr.uniform(1180, 1350)
        sc_ = 0.45 + (y - 1180) / 170 * 0.3
        paste(img, emu("peck" if k % 2 else "stand"), x, y - 200 * sc_, sc_)
    paste(img, emu("stand"), 620, 1150, 1.25)
    a1 = L[1][0]
    if t > a1:
        k = ease(clamp((t - a1 - 0.5) / 0.6))
        d = ImageDraw.Draw(img, "RGBA")
        cx, cy = 743, 768 - 30 * (1 - k)
        pts = [(cx - 50, cy), (cx - 50, cy - 50), (cx - 25, cy - 25), (cx, cy - 60), (cx + 25, cy - 25), (cx + 50, cy - 50), (cx + 50, cy)]
        d.polygon(pts, fill=(255, 210, 63, int(255 * k)))
        big(t, a1 + 0.4, "GANARON", 280, 84, WHITE, sub="LOS EMÚS", subcol=YEL)
    vignette(img, 160)


FNS = {k: globals()["sh_" + k] for k, *_ in SHOTS}
AUDIO = {
    "music": [("open", "playful"), ("guns", "tension"), ("truck", "playful"), ("retreat", "drone"), ("stats", "playful")],
    "gains": {"playful": 1.0},
    "amb": {"wind": ["open", "farm", "invasion", "ambush", "truck", "guerrilla", "retreat", "winner"], "birds": ["farm"]},
    "sfx": [("open@L1+0.2", "pop", 0.2), ("invasion+0.3", "riser", 0.1), ("invasion+1.8", "impact", 0.2),
            ("invasion@L1+0.2", "pop", 0.2), ("guns+0.3", "thud", 0.25), ("guns@L1+2.8", "impact", 0.3),
            ("ambush@L1e-1.6", "rattle", 0.22), ("ambush@L1e-1.4", "click", 0.5), ("ambush@L1e-1.2", "click", 0.5),
            ("ambush@L1e-1.4", "thud", 0.3), ("truck", "drill", 0.08), ("truck+1.0", "rattle", 0.15),
            ("guerrilla+0.6", "whoosh", 0.15), ("guerrilla@L1+0.3", "swell", 0.15),
            ("retreat+0.4", "thud", 0.25), ("stats+0.3", "tick", 0.15), ("stats+1.0", "tick", 0.15), ("stats+1.7", "tick", 0.15),
            ("stats@L1+0.1", "impact", 0.25), ("winner@L1+0.4", "chime", 0.08), ("winner@L1+0.5", "pop", 0.25)],
    "bed": [("farm", "retreat"), ("stats", "end")],
    "bpm": 104,
}
