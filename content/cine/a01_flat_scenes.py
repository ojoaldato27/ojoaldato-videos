"""Las 16 escenas del vídeo A1 (Tesla Roadster) dibujadas con flat3 (estilos minimal / vhs / póster, 21/10).
Mismo guion, misma voz y mismos planos que a01_tesla; el coche en pantalla es un Cybertruck."""
import math, random
from PIL import Image, ImageDraw
import flat3 as FL
from flat3 import TH, W, H, GROUND_Y, F, lt, pop, car, car_geo
from render import ease, clamp, lerp

CEIL, CXR, CYR, RR = 650, 700, 970, 320          # rampa: techo, centro y radio del medio tubo


def _ramp(img):
    d = ImageDraw.Draw(img)
    n = TH["name"]
    col = TH["ink"] if n == "minimal" else (TH["acc"] if n == "poster" else (206, 196, 186))
    w = 8 if n == "minimal" else 30
    d.arc([CXR - RR - w / 2, CYR - RR - w / 2, CXR + RR + w / 2, CYR + RR + w / 2], -90, 90, fill=col, width=w)
    d.line([(110, CEIL - w / 2), (CXR, CEIL - w / 2)], fill=col, width=w)
    if n != "minimal":
        d.rectangle([110, CEIL - w, 128, GROUND_Y], fill=col)
    FL.ground(img)


def sh_open(img, t, T, L):
    FL.bg(img, t)
    _ramp(img)
    for x, c in ((330, 0), (590, 1)):
        FL.parked(img, x, GROUND_Y, 220, TH["pc"][c])
    sc = 46
    spin = -t * 9
    if t < 2.3:
        u = ease(t / 2.3)
        cx, cy, ang = lerp(-300, CXR, u), GROUND_Y, 0.0
        FL.speed_lines(img, cx - 420, GROUND_Y - 80, cx - 160, GROUND_Y - 10, clamp(t / 0.5), 4, 1)
    elif t < 3.6:
        a = math.radians(lerp(90, -90, ease((t - 2.3) / 1.3)))
        cx, cy, ang = CXR + RR * math.cos(a), CYR + RR * math.sin(a), math.degrees(a) - 90
    elif t < 4.8:
        u = ease((t - 3.6) / 1.2)
        cx, cy, ang = lerp(CXR, 330, u), CEIL, -180.0
    elif t < 6.4:
        u = (t - 4.8) / 1.6
        cx = lerp(330, 150, u)
        cy = lerp(CEIL, GROUND_Y, u * u) - 160 * math.sin(math.pi * u)
        ang = -180 - 180 * ease(clamp(u * 1.25))
    else:
        cx, cy, ang = 150, GROUND_Y - 24 * abs(math.sin((t - 6.4) * 9)) * math.exp(-(t - 6.4) * 4), 0.0
    if 2.3 <= t < 4.8:
        FL.dotted_arc(img, CXR, CYR, RR - 120, math.pi / 2, math.pi / 2 - math.pi * clamp((t - 2.3) / 1.3), 1.0)
    g = car(img, cx, cy, sc, ang, -1 if 3.6 <= t < 4.8 else 1, spin=spin)
    if 4.8 <= t < 6.4:
        x, y = g["center"]
        k = 1 - (t - 4.8) / 1.6
        FL.puff(img, x, y + 40, math.pi / 2, k, 34, 6, int(t * 9))
        FL.puff(img, x - 100, y, math.pi, k * 0.8, 28, 5, int(t * 7) + 3)
    FL.pill(img, 540, 1400, "BASE DE SPACEX · TEXAS", ease(clamp((t - 0.5) / 0.4)))
    FL.head(img, t, 0)


def sh_question(img, t, T, L):
    FL.bg(img, t)
    FL.ground(img)
    bob = 10 * math.sin(t * 5)
    car(img, 540, GROUND_Y - abs(bob) * 0.4, 110, -1.5 * math.sin(t * 5))
    FL.big(img, 540, 640 + bob, "?", 420, TH["acc"], ease(clamp((t - 0.15) / 0.35)))
    k2 = clamp((t - lt(L, 0, 0.55)) / 0.35)
    FL.big(img, 880, 560 - bob, "?", 230, TH["ink"] if TH["name"] != "vhs" else TH["acc2"], k2)
    FL.big(img, 210, 600 + bob, "?", 180, TH["soft"], clamp((t - lt(L, 0, 0.3)) / 0.35))
    FL.head(img, t, 1)


def sh_present(img, t, T, L):
    FL.bg(img, t)
    FL.rocket(img, 880, GROUND_Y, 0.75)
    FL.ground(img)
    k = ease(clamp(t / 1.1))
    car(img, lerp(-300, 430, k), GROUND_Y, 82, 0, 1, spin=-k * 30)
    if t < 1.1:
        FL.speed_lines(img, lerp(-300, 430, k) - 520, GROUND_Y - 120, lerp(-300, 430, k) - 240, GROUND_Y - 20, 1 - k, 4, 2)
    FL.pill(img, 540, 470, "15 DE OCTUBRE DE 2026", ease(clamp((t - lt(L, 0, 0.28)) / 0.35)))
    FL.pill(img, 540, 580, "McGREGOR, TEXAS", ease(clamp((t - lt(L, 0, 0.72)) / 0.35)), col=TH["acc"] if TH["name"] == "minimal" else TH["acc2"])
    FL.head(img, t, 2)


def sh_fans(img, t, T, L):
    FL.bg(img, t)
    FL.ground(img, 1200)
    g = car(img, 540, 1200, 150, 0, 1, alpha=110 if TH["name"] == "minimal" else 150)
    k = ease(clamp((t - 0.35) / 0.4))
    fans = [g["T"](1.95, 0.62), g["T"](3.75, 0.62)]
    for x, y in fans:
        FL.fan(img, x, y, 74, t)
    d = ImageDraw.Draw(img, "RGBA")
    col = (90, 190, 240) if TH["name"] != "poster" else TH["acc"]
    if TH["name"] == "minimal":
        col = TH["acc"]
    if k > 0:
        rr = random.Random(3)
        for i in range(30):
            u = (t * 0.9 + i / 30) % 1.0
            side = -1 if i % 2 else 1
            x0 = 540 + side * 520
            fx, fy = fans[0] if side < 0 else fans[1]
            x = lerp(x0, fx, u)
            y = lerp(1180, fy, u * u) + rr.uniform(-6, 6)
            r = 9
            d.ellipse([x - r, y - r, x + r, y + r], fill=col + (int(230 * k * (1 - u * 0.4)),))
    kd = ease(clamp((t - 1.3) / 0.4))
    if kd > 0:
        for x in (330, 540, 750):
            y0 = 640
            d.line([(x, y0), (x, y0 + 130 * kd)], fill=TH["ink"], width=12)
            d.polygon([(x - 26, y0 + 130 * kd - 6), (x + 26, y0 + 130 * kd - 6), (x, y0 + 130 * kd + 30)], fill=TH["ink"])
    FL.pill(img, 540, 1400, "CHUPAN EL AIRE DE DEBAJO", ease(clamp((t - 0.8) / 0.4)))
    FL.head(img, t, 3)


def sh_upside(img, t, T, L):
    FL.bg(img, t, "nosun" if TH["name"] == "poster" else "day")
    d = ImageDraw.Draw(img)
    d.rectangle([0, 560, W, 600], fill=TH["ink"])
    k = ease(clamp(t / 0.9))
    x = lerp(1450, 560, k)
    car(img, x, 600, 100, 180, 1, spin=t * 10)
    FL.speed_lines(img, x + 300, 640, x + 620, 760, 1 - k * 0.6, 4, 5)
    for i, xx in enumerate((300, 540, 780)):
        q = ease(clamp((t - 0.6 - i * 0.1) / 0.45))
        if q > 0:
            y0 = 1080
            d.line([(xx, y0), (xx, y0 - 190 * q)], fill=TH["acc"], width=16)
            d.polygon([(xx - 34, y0 - 190 * q + 8), (xx + 34, y0 - 190 * q + 8), (xx, y0 - 190 * q - 40)], fill=TH["acc"])
    FL.pill(img, 540, 1190, "LA SUCCIÓN LO SUJETA", ease(clamp((t - 1.0) / 0.4)))
    FL.head(img, t, 4)


def sh_brabham(img, t, T, L):
    FL.bg(img, t)
    FL.ground(img)
    k = ease(clamp(t / 0.9))
    t_ban = lt(L, 0, 0.8)
    gray = ease(clamp((t - t_ban) / 0.4))
    FL.f1(img, lerp(-500, 560, k), GROUND_Y - 116, 0.95, t, gray)
    if t < 0.9:
        FL.speed_lines(img, lerp(-500, 560, k) - 900, GROUND_Y - 200, lerp(-500, 560, k) - 480, GROUND_Y - 30, 1 - k, 5, 6)
    FL.big(img, 540, 560, "1978", 190 if TH["name"] != "minimal" else 150, TH["ink"] if TH["name"] != "vhs" else (255, 255, 255),
           clamp((t - lt(L, 0, 0.12)) / 0.35))
    kw = clamp((t - lt(L, 0, 0.45)) / 0.35)
    if kw > 0:
        d = ImageDraw.Draw(img)
        fx, fy, s = 820, 760, 26
        wave = math.sin(t * 6)
        d.line([(fx - 10, fy - 30), (fx - 10, fy + 260)], fill=TH["ink"], width=10)
        for i in range(6):
            for j in range(4):
                c = TH["ink"] if (i + j) % 2 else (TH["bg"] if TH["name"] != "vhs" else (255, 255, 255))
                x0 = fx + i * s
                y0 = fy - 30 + j * s + math.sin(i * 0.9 + t * 7) * 6 * kw
                d.rectangle([x0, y0, x0 + s, y0 + s], fill=c)
        FL.pill(img, 540, 1400, "1 CARRERA · 1 VICTORIA", ease(kw), col=TH["acc2"] if TH["name"] != "minimal" else None)
    FL.stamp(img, 540, 900, "PROHIBIDO", ease(clamp((t - t_ban) / 0.22)))
    FL.head(img, t, 5)


NOZZ = [(0.08, 0.95), (0.1, 0.55), (1.3, 0.42), (2.4, 0.42), (3.5, 0.42), (4.6, 0.42), (5.55, 0.62), (5.6, 0.98), (3.06, 1.86), (1.4, 1.52)]


def sh_thrusters(img, t, T, L):
    FL.bg(img, t)
    FL.ground(img, 1180)
    g = car(img, 540, 1180, 150, 0, 1)
    cx, cy = g["center"]
    d = ImageDraw.Draw(img, "RGBA")
    for i, (x, y) in enumerate(NOZZ):
        kk = ease(clamp((t - 0.3 - i * 0.12) / 0.25))
        if kk <= 0:
            continue
        px, py = g["T"](x, y)
        d.ellipse([px - 14, py - 14, px + 14, py + 14], fill=TH["acc"] + (int(255 * kk),))
        ang = math.atan2(py - cy, px - cx)
        on = 0.55 + 0.45 * math.sin(t * 9 + i)
        FL.puff(img, px, py, ang, kk * on, 40, 5, i)
    FL.pill(img, 540, 1400, "10 TOBERAS · AIRE A PRESIÓN", ease(clamp((t - 1.4) / 0.4)))
    FL.head(img, t, 6)


def sh_tanks(img, t, T, L):
    FL.bg(img, t)
    FL.ground(img, GROUND_Y, 440, W)
    lvl = 1.0 - 0.6 * clamp((t - lt(L, 0, 0.5)) / 2.0)
    FL.tank(img, 240, 1000, lvl)
    FL.big(img, 240, 600, "600 L", 130 if TH["name"] != "minimal" else 96, TH["acc"], clamp((t - 0.3) / 0.35))
    v = clamp((t - lt(L, 0, 0.45)) / 2.2)
    y = GROUND_Y - math.sin(v * math.pi) * 400
    g = car(img, 740, y, 52, 360 * ease(v), 1, spin=-t * 8)
    if 0 < v < 1:
        x, yy = g["center"]
        FL.puff(img, x, yy + 50, math.pi / 2, 1.0, 34, 6, int(t * 9))
    FL.head(img, t, 7)


def sh_space(img, t, T, L):
    FL.bg(img, t, "space")
    if TH["name"] == "poster":
        ImageDraw.Draw(img).ellipse([-300, 1250, 1380, 2600], fill=TH["acc"])
    rot = 25 * math.sin(t * 0.9)
    FL.satellite(img, 560, 900, rot, 1.1)
    side = 1 if math.sin(t * 0.9 + 1.2) > 0 else -1
    a = math.radians(-rot)
    tip = (560 + side * 330 * math.cos(a), 900 - side * 330 * math.sin(a) * -1)
    FL.puff(img, tip[0], tip[1], 0 if side > 0 else math.pi, 0.85, 40, 6, int(t * 5))
    kf = clamp((t - 0.1) / 0.6)
    if t < lt(L, 0, 0.42):
        FL.flame_x(img, 540, 560, kf)
    FL.pill(img, 540, 1260, "GAS A PRESIÓN, SIN COMBUSTIÓN", ease(clamp((t - 0.6) / 0.4)), col=TH["acc2"] if TH["name"] == "poster" else None)
    FL.head(img, t, 8, inv=True)


def sh_accel(img, t, T, L):
    FL.bg(img, t)
    FL.ground(img)
    run = clamp((t - 0.3) / 0.81)
    FL.stopwatch(img, 540, 820, 250, run * 0.81, f"{0.81 * run:.2f} s".replace(".", ","))
    if 0.3 < t < 1.6:
        u = clamp((t - 0.3) / 1.1)
        x = -300 + 1800 * u * u
        car(img, x, GROUND_Y, 52, 0, 1, spin=-t * 30)
        FL.speed_lines(img, x - 700, GROUND_Y - 100, x - 160, GROUND_Y - 10, 1.0, 5, 8)
    FL.pill(img, 540, 1190, "DE 0 A 97 KM/H", ease(clamp((t - 0.8) / 0.4)), col=TH["acc2"] if TH["name"] != "minimal" else None)
    FL.pill(img, 540, 1400, "SIN COMPROBAR", ease(clamp((t - lt(L, 0, 0.6)) / 0.4)), col=TH["acc"])
    FL.head(img, t, 9, t_hide=(1.65, 4.9))


def sh_versions(img, t, T, L):
    FL.bg(img, t, "nosun" if TH["name"] == "poster" else "day")
    d = ImageDraw.Draw(img, "RGBA")
    cards = [("PERFORMANCE", "2 PLAZAS", "< 1,6 s"), ("THRUST", "2 PLAZAS", "< 0,9 s"), ("ROCKET", "1 PLAZA", "< 0,59 s")]
    n = TH["name"]
    fo_n = F(*TH["lab"]) if n != "minimal" else F(FL.INTER_X, 30)
    fo_v = F(TH["big"], 96 if n != "minimal" else 64)
    fo_s = F(*TH["lab"]) if n != "minimal" else F(FL.INTER, 30)
    hl = t > lt(L, 0, 0.45)
    for i, (nm, seats, acc) in enumerate(cards):
        k = ease(clamp((t - 0.2 - i * 0.3) / 0.35))
        if k <= 0:
            continue
        x, y = 200 + i * 340, 860 + (1 - k) * 60
        on = hl and i == 2
        bc = TH["acc"] if on else (TH["ink"] if n != "vhs" else (200, 180, 190))
        fill = (255, 255, 255) if n == "minimal" else ((30, 20, 44) if n == "vhs" else TH["bg"])
        a = int(255 * k)
        d.rounded_rectangle([x - 150, y - 300, x + 150, y + 300], radius=24 if n != "poster" else 0, fill=fill + (a,), outline=bc + (a,), width=10 if on else 5)
        txtc = TH["ink"] if n != "vhs" else (255, 255, 255)
        d.text((x, y - 230), nm, font=fo_n, fill=txtc + (a,), anchor="mm")
        d.text((x, y - 80), acc, font=fo_v, fill=(TH["acc"] if on else txtc) + (a,), anchor="mm")
        d.text((x, y + 40), seats, font=fo_s, fill=TH["soft"] + (a,), anchor="mm")
        car(img, x, y + 190, 44, 0, 1, alpha=a)
        if i == 2 and on:
            d.text((x, y + 250), "NO APTO", font=fo_s, fill=TH["acc"] + (a,), anchor="mm")
    if hl:
        FL.pill(img, 540, 1310, "NO APTO PARA LA CALLE", ease(clamp((t - lt(L, 0, 0.7)) / 0.35)), col=TH["acc"])
    FL.pill(img, 540, 1440 if hl else 1310, "DE 0 A 97 KM/H, SEGÚN TESLA", ease(clamp((t - 1.4) / 0.4)))
    FL.head(img, t, 10)


def sh_y2028(img, t, T, L):
    FL.bg(img, t, "nosun" if TH["name"] == "poster" else "day")
    k28 = clamp((t - lt(L, 0, 0.5)) / 0.4)
    if k28 < 1:
        FL.big(img, 540, 860, "¿?", 300, TH["soft"], clamp(t / 0.3) * (1 - k28))
    FL.big(img, 540, 860, "2028", 330 if TH["name"] != "minimal" else 250, TH["acc"], k28)
    FL.pill(img, 540, 1160, "INICIO DE LA PRODUCCIÓN", ease(clamp((t - lt(L, 0, 0.62)) / 0.4)))
    FL.head(img, t, 11)


def sh_delays(img, t, T, L):
    FL.bg(img, t, "nosun" if TH["name"] == "poster" else "day")
    d = ImageDraw.Draw(img)
    pts = [(200, "2017", "SE ENSEÑA"), (540, "2020", "IBA A LLEGAR"), (880, "2028", "AHORA")]
    k = ease(clamp(t / 1.6))
    d.line([(160, 900), (160 + 760 * k, 900)], fill=TH["ink"] if TH["name"] != "vhs" else (220, 210, 220), width=10)
    fy = F(TH["big"], 110 if TH["name"] != "minimal" else 80)
    fl = F(*TH["lab"]) if TH["name"] != "minimal" else F(FL.INTER, 30)
    for i, (x, yr, lb) in enumerate(pts):
        kk = ease(clamp((t - 0.2 - i * 0.6) / 0.3))
        if kk <= 0:
            continue
        col = TH["acc"] if i == 2 else (TH["ink"] if TH["name"] != "vhs" else (255, 255, 255))
        a = int(255 * kk)
        dd = ImageDraw.Draw(img, "RGBA")
        dd.ellipse([x - 26, 874, x + 26, 926], fill=col + (a,))
        dd.text((x, 760), yr, font=fy, fill=col + (a,), anchor="mm")
        dd.text((x, 990), lb, font=fl, fill=TH["soft"] + (a,), anchor="mm")
        if i == 1 and t > lt(L, 0, 0.75):
            q = ease(clamp((t - lt(L, 0, 0.75)) / 0.25))
            dd.line([(x - 110, 830), (x - 110 + 220 * q, 750)], fill=TH["acc"], width=14)
    u = clamp(t / max(1.0, T * 0.9))
    cx = lerp(200, 880, ease(u))
    car(img, cx, 874, 26, 0, 1, spin=-t * 12)
    FL.pill(img, 540, 1160, "SE HA RETRASADO VARIAS VECES", ease(clamp((t - lt(L, 0, 0.85)) / 0.3)))
    FL.head(img, t, 12)


def sh_lost(img, t, T, L):
    FL.bg(img, t, "nosun" if TH["name"] == "poster" else "day")
    d = ImageDraw.Draw(img, "RGBA")
    BW = 640
    rows = [("PLAZAS", 4, 2, 4, "", 0.0), ("AUTONOMÍA", 1000, 480, 1000, " km", 0.45)]
    fl = F(*TH["lab"]) if TH["name"] != "minimal" else F(FL.INTER_B, 38)
    fv = F(TH["big"], 84 if TH["name"] != "minimal" else 56)
    fs = F(FL.INTER, 26) if TH["name"] == "minimal" else F(TH["sub"][0], int(TH["sub"][1] * 0.6))
    txtc = TH["ink"] if TH["name"] != "vhs" else (255, 255, 255)
    for i, (lbl, a, b, mx, unit, fr) in enumerate(rows):
        k = ease(clamp((t - lt(L, 0, fr)) / 0.5))
        if k <= 0:
            continue
        y = 640 + i * 380
        al = int(255 * k)
        d.text((120, y - 70), lbl, font=fl, fill=txtc + (al,), anchor="lm")
        d.text((120 + BW, y - 70), f"PROMETIDO: {a:,}".replace(",", ".") + unit, font=fs, fill=TH["soft"] + (al,), anchor="rm")
        d.rectangle([120, y, 120 + BW, y + 90], fill=TH["soft"] + (int(110 * k),))
        q = ease(clamp((t - lt(L, 0, fr) - 0.6) / 0.7))
        w2 = BW * lerp(a, b, q) / mx
        d.rectangle([120, y, 120 + w2, y + 90], fill=TH["acc"] + (al,))
        txt = f"{int(round(lerp(a, b, q))):,}".replace(",", ".") + unit
        d.text((120 + w2 + 24, y + 46), txt, font=fv, fill=txtc + (al,), anchor="lm")
    FL.head(img, t, 13)


def sh_money(img, t, T, L):
    FL.bg(img, t)
    FL.ground(img)
    n = int(clamp((t - 0.1) / 1.2) * 9)
    FL.bills(img, 560, GROUND_Y - 10, n, 1.0)
    FL.big(img, 540, 640, "50.000 $", 190 if TH["name"] != "minimal" else 150, TH["acc"], clamp((t - 0.35) / 0.35))
    FL.pill(img, 540, 1400, "PRECIO FINAL: SIN ANUNCIAR", ease(clamp((t - lt(L, 0, 0.6)) / 0.4)), col=TH["acc"])
    FL.head(img, t, 14)


def sh_final(img, t, T, L):
    FL.bg(img, t)
    FL.ground(img)
    a, b = L[0]
    v = clamp(t / max(1.0, b * 0.55))
    x = lerp(-300, 560, ease(v))
    y = GROUND_Y - math.sin(v * math.pi) * 420
    g = car(img, x, y, 70, -6 * math.sin(v * math.pi), 1, spin=-t * 8)
    if v < 1:
        cx, cy = g["center"]
        FL.puff(img, cx - 160, cy + 40, math.pi * 0.8, 1 - v, 40, 6, int(t * 7))
        FL.puff(img, cx, cy + 70, math.pi / 2, (1 - v) * 0.8, 34, 5, int(t * 9) + 2)
    kc = clamp((t - lt(L, 0, 0.6)) / 0.4)
    if kc > 0:
        s = pop(kc)
        FL.clock(img, 800, 640, 150 * s, t * 3)
    FL.head(img, t, 15)


FNS = {k: globals()["sh_" + k] for k in ("open", "question", "present", "fans", "upside", "brabham", "thrusters", "tanks", "space",
                                         "accel", "versions", "y2028", "delays", "lost", "money", "final")}
FOCUS_PT = {"open": (700, 970), "question": (540, 700), "present": (430, 1150), "fans": (540, 1100), "upside": (560, 700),
            "brabham": (560, 1180), "thrusters": (540, 1080), "tanks": (240, 1000), "space": (560, 900), "accel": (540, 820),
            "versions": (880, 860), "y2028": (540, 860), "delays": (540, 900), "lost": (440, 700), "money": (540, 700),
            "final": (560, 1100)}


# ------------------------------------------------------------------ subtítulos y cierre
def CAPTION(img, t, chunks, y=1560):
    cur = next((c for c in chunks if c[0] - 0.02 <= t < c[1]), None)
    if not cur:
        return
    t0, t1, words = cur
    n = TH["name"]
    up = n != "minimal"
    fo = F(*TH["cap"])
    d = ImageDraw.Draw(img)
    ws = [((w.upper() if up else w), hl, a) for w, hl, a, b in words]
    sp = d.textlength(" ", font=fo)
    tw = sum(d.textlength(w, font=fo) for w, _, _ in ws) + sp * (len(ws) - 1)
    size = TH["cap"][1]
    while tw > 980 and size > 30:
        size -= 6
        fo = F(TH["cap"][0], size)
        sp = d.textlength(" ", font=fo)
        tw = sum(d.textlength(w, font=fo) for w, _, _ in ws) + sp * (len(ws) - 1)
    x = W / 2 - tw / 2
    yy = 1580
    if n == "minimal":
        col, hlc = (120, 120, 128), (20, 20, 22)
    else:
        col, hlc = TH["cap_col"], TH["cap_hl"]
    for w, hl, a in ws:
        if t >= a - 0.04:
            k = ease(clamp((t - a + 0.04) / 0.12))
            d.text((x, yy + (1 - k) * 14), w, font=fo, fill=hlc if hl else col, anchor="lm",
                   stroke_width=TH["stroke"], stroke_fill=(30, 20, 40) if TH["stroke"] else None)
        x += d.textlength(w, font=fo) + sp


def OUTRO_FN(img, u, D):
    out = Image.new("RGB", (W, H), TH["bg"])
    FL.bg(out, u)
    n = TH["name"]
    k1 = clamp((u - 0.1) / 0.35)
    k2 = clamp((u - 0.35) / 0.35)
    col1 = TH["ink"] if n != "vhs" else (255, 255, 255)
    FL.big(out, 540, 560, "¡DALE A LIKE" if n != "minimal" else "Dale a like", 150 if n != "minimal" else 110, col1, k1)
    FL.big(out, 540, 740, "Y SÍGUEME!" if n != "minimal" else "y sígueme.", 150 if n != "minimal" else 110, TH["acc"], k2)
    d = ImageDraw.Draw(out, "RGBA")
    fo = F(*TH["lab"]) if n != "minimal" else F(FL.INTER_B, 40)
    kb = ease(clamp((u - 0.6) / 0.3))
    if kb > 0:
        pressed1 = u > 1.3
        pressed2 = u > 1.9
        for i, (txt, on) in enumerate(((("♥ ME GUSTA" if n != "vhs" else "<3 ME GUSTA"), pressed1), (("SIGUIENDO" if pressed2 else "+ SEGUIR"), pressed2))):
            x = 300 + i * 480
            y = 1000 + (1 - kb) * 40
            fill = TH["acc"] if on else ((255, 255, 255) if n == "minimal" else ((30, 20, 44) if n == "vhs" else TH["bg"]))
            tc = (255, 255, 255) if on or n == "vhs" else TH["ink"]
            sq = 0.94 if (on and (1.3 < u < 1.45 if i == 0 else 1.9 < u < 2.05)) else 1.0
            w2, h2 = 200 * sq, 64 * sq
            d.rounded_rectangle([x - w2, y - h2, x + w2, y + h2], radius=int(h2) if n == "minimal" else 6, fill=fill, outline=TH["ink"] if n != "vhs" else TH["acc"], width=5)
            fo2 = fo if n != "minimal" else F(FL.INTER_B, 38)
            d.text((x, y), txt, font=fo2 if "♥" not in txt else F(FL.DJ, 40), fill=tc, anchor="mm")
    hx = ease(clamp((u - 0.9) / 0.4))
    if hx > 0:
        FL.text(out, (540, 1200), "@ojoaldato.ya", F(*TH["sub"]) if n != "minimal" else F(FL.INTER, 40), TH["soft"], alpha=int(255 * hx), stroke=0)
    vx = clamp(u / max(1.0, D))
    FL.ground(out, 1380)
    car(out, lerp(-300, 1400, vx), 1380, 40, 0, 1, spin=-u * 20)
    return out
