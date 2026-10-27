"""Motor de render: guion JSON -> fotogramas 1080x1920 -> MP4 (FFmpeg).
Todo lo visual se dibuja con código: no usa imágenes ni vídeos de terceros."""
import json, math, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
FONT_DIR = "/usr/share/fonts/opentype/inter/"
C = {
    "bg": (11, 16, 32), "grid": (24, 34, 62), "fg": (240, 244, 255),
    "muted": (140, 152, 185), "accent": (255, 138, 61), "comp": (77, 163, 255),
    "tens": (255, 90, 95), "steel": (175, 186, 205),
}


CURRENT_THEME = None
_FONTS = {}


def font(size, weight="Black"):
    key = (size, weight)
    if key not in _FONTS:
        if weight == "Mono":
            path = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
        else:
            path = FONT_DIR + {"Black": "InterDisplay-Black.otf", "Bold": "Inter-Bold.otf",
                               "Semi": "InterDisplay-SemiBold.otf"}[weight]
        _FONTS[key] = ImageFont.truetype(path, size)
    return _FONTS[key]


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def prog(t, a, b):
    return clamp((t - a) / max(1e-6, b - a))


def lerp(a, b, k):
    return a + (b - a) * k


def mix(c1, c2, k):
    return tuple(int(lerp(a, b, k)) for a, b in zip(c1, c2))


def background_neon():
    img = Image.new("RGB", (W, H), C["bg"])
    d = ImageDraw.Draw(img)
    for y in range(0, H, 4):
        k = y / H
        d.rectangle([0, y, W, y + 4], fill=mix((16, 14, 44), (6, 6, 20), k))
    for x in range(30, W, 60):
        for y in range(30, H, 60):
            d.ellipse([x - 1.5, y - 1.5, x + 1.5, y + 1.5], fill=(38, 36, 84))
    v = Image.new("L", (W, H), 0)
    ImageDraw.Draw(v).ellipse([-300, -200, W + 300, H + 200], fill=255)
    v = v.filter(ImageFilter.GaussianBlur(220))
    return Image.composite(img, Image.new("RGB", (W, H), (3, 3, 12)), v)


def background():
    if CURRENT_THEME == "neon":
        return background_neon()
    img = Image.new("RGB", (W, H), C["bg"])
    d = ImageDraw.Draw(img)
    for x in range(0, W, 60):
        d.line([(x, 0), (x, H)], fill=C["grid"], width=1)
    for y in range(0, H, 60):
        d.line([(0, y), (W, y)], fill=C["grid"], width=1)
    # viñeta
    v = Image.new("L", (W, H), 0)
    ImageDraw.Draw(v).ellipse([-300, -200, W + 300, H + 200], fill=255)
    v = v.filter(ImageFilter.GaussianBlur(220))
    dark = Image.new("RGB", (W, H), (5, 8, 16))
    return Image.composite(img, dark, v)


# ---------- primitivas ----------
def arrow(d, x0, y0, x1, y1, col, w=10, head=30):
    d.line([(x0, y0), (x1, y1)], fill=col, width=w)
    ang = math.atan2(y1 - y0, x1 - x0)
    p1 = (x1 - head * math.cos(ang - 0.45), y1 - head * math.sin(ang - 0.45))
    p2 = (x1 - head * math.cos(ang + 0.45), y1 - head * math.sin(ang + 0.45))
    d.polygon([(x1, y1), p1, p2], fill=col)


def i_section(d, cx, cy, fw, tf, tw, h, scale, col, outline=None):
    """Sección en I centrada; si fw == tw es un rectángulo."""
    s = scale
    top, bot = cy - h * s / 2, cy + h * s / 2
    pts = [(cx - fw * s / 2, top), (cx + fw * s / 2, top), (cx + fw * s / 2, top + tf * s),
           (cx + tw * s / 2, top + tf * s), (cx + tw * s / 2, bot - tf * s),
           (cx + fw * s / 2, bot - tf * s), (cx + fw * s / 2, bot), (cx - fw * s / 2, bot),
           (cx - fw * s / 2, bot - tf * s), (cx - tw * s / 2, bot - tf * s),
           (cx - tw * s / 2, top + tf * s), (cx - fw * s / 2, top + tf * s)]
    d.polygon(pts, fill=col, outline=outline)


def text_center(d, y, txt, size, col, weight="Black"):
    f = font(size, weight)
    w = d.textlength(txt, font=f)
    d.text(((W - w) / 2, y), txt, font=f, fill=col)


def inertia_I(fw, tf, tw, h):
    return fw * h ** 3 / 12 - (fw - tw) * (h - 2 * tf) ** 3 / 12


# ---------- escenas ----------
def sc_hook_ibeam(d, t, p, img):
    k = ease(t / 0.9)
    sec = p["section"]
    i_section(d, W / 2, 760, sec["fw"], sec["tf"], sec["tw"], sec["h"], 2.4 * lerp(0.4, 1, k),
              mix(C["bg"], C["steel"], k), outline=C["accent"] if k > 0.9 else None)
    if t > 0.6:
        a = ease((t - 0.6) / 0.5)
        text_center(d, 1090, p.get("label", ""), 52, mix(C["bg"], C["accent"], a), "Semi")


def sc_beam_bend(d, t, p, img):
    x0, x1, y = 140, 940, 760
    k = ease(prog(t, 0.6, 2.4))
    sag = 70 * k
    # apoyos
    for x in (x0, x1):
        d.polygon([(x, y + 40), (x - 45, y + 120), (x + 45, y + 120)], outline=C["muted"], width=6)
        d.line([(x - 70, y + 124), (x + 70, y + 124)], fill=C["muted"], width=6)
    # viga deformada (parábola), canto 80 px
    pts_top, pts_bot = [], []
    for i in range(41):
        u = i / 40
        x = lerp(x0 - 40, x1 + 40, u)
        dy = sag * (1 - (2 * u - 1) ** 2)
        pts_top.append((x, y - 40 + dy))
        pts_bot.append((x, y + 40 + dy))
    d.polygon(pts_top + pts_bot[::-1], fill=C["steel"])
    # carga
    ay = lerp(380, 560, ease(prog(t, 0.0, 0.6)))
    arrow(d, W / 2, ay - 170, W / 2, ay + sag * 0.0 + 70, C["accent"], 14, 44)
    text_center(d, ay - 240, p.get("load", "CARGA"), 46, C["accent"])
    # compresión arriba / tracción abajo
    c = ease(prog(t, 2.0, 2.8))
    if c > 0:
        for xa in (300, 440, 640, 780):
            u = (xa - x0 + 40) / (x1 - x0 + 80)
            dy = sag * (1 - (2 * u - 1) ** 2)
            direc = 1 if xa < W / 2 else -1
            arrow(d, xa - direc * 50 * c, y - 75 + dy, xa + direc * 10 * c, y - 75 + dy,
                  C["comp"], 8, 24)
        d.text((150, y - 165), p.get("top", "COMPRESIÓN"), font=font(44), fill=mix(C["bg"], C["comp"], c))
    tt = ease(prog(t, 3.0, 3.8))
    if tt > 0:
        for xa in (300, 440, 640, 780):
            u = (xa - x0 + 40) / (x1 - x0 + 80)
            dy = sag * (1 - (2 * u - 1) ** 2)
            direc = -1 if xa < W / 2 else 1
            arrow(d, xa - direc * 10 * tt, y + 80 + dy, xa + direc * 50 * tt, y + 80 + dy,
                  C["tens"], 8, 24)
        d.text((150, y + 170), p.get("bottom", "TRACCIÓN"), font=font(44), fill=mix(C["bg"], C["tens"], tt))


def sc_stress_profile(d, t, p, img):
    cx, cy, hh, ww = 380, 760, 520, 110
    k = ease(t / 0.6)
    d.rectangle([cx - ww / 2, cy - hh / 2, cx + ww / 2, cy + hh / 2], fill=mix(C["bg"], C["steel"], k))
    # diagrama de tensiones lineal
    g = ease(prog(t, 0.6, 1.8))
    bx = 620
    d.line([(bx, cy - hh / 2 - 20), (bx, cy + hh / 2 + 20)], fill=C["muted"], width=4)
    L = 230 * g
    d.polygon([(bx, cy), (bx - L, cy - hh / 2), (bx, cy - hh / 2)], fill=C["comp"])
    d.polygon([(bx, cy), (bx + L, cy + hh / 2), (bx, cy + hh / 2)], fill=C["tens"])
    # eje neutro
    e = ease(prog(t, 1.9, 2.6))
    if e > 0:
        for x in range(int(cx - ww / 2 - 30), int(bx + 260), 34):
            d.line([(x, cy), (x + 18, cy)], fill=mix(C["bg"], C["accent"], e), width=6)
        f = font(40, "Semi")
        tw_ = d.textlength(p.get("axis", "eje neutro"), font=f)
        d.text((cx - ww / 2 - tw_ - 40, cy - 60), p.get("axis", "eje neutro"), font=f,
               fill=mix(C["bg"], C["accent"], e))
    if t > 2.4:
        a = ease(prog(t, 2.4, 3.0))
        f = font(38, "Semi")
        d.text((bx + 20, cy - hh / 2 - 10), "máx.", font=f, fill=mix(C["bg"], C["comp"], a))
        d.text((bx + 20, cy + hh / 2 - 40), "máx.", font=f, fill=mix(C["bg"], C["tens"], a))
        d.text((bx + 40, cy + 22), "≈ 0", font=f, fill=mix(C["bg"], C["accent"], a))


def sc_section_morph(d, t, p, img):
    a, b = p["from"], p["to"]
    k = ease(prog(t, 0.5, 3.0))
    fw = lerp(a["fw"], b["fw"], k)
    tw = lerp(a["tw"], b["tw"], k)
    tf = lerp(a.get("tf", b["tf"]), b["tf"], k)
    i_section(d, W / 2, 760, fw, tf, tw, b["h"], 2.4, C["steel"])
    # flechas "del centro hacia fuera"
    if 0.6 < t < 3.0:
        q = ease(prog(t, 0.6, 1.6))
        for sgn in (-1, 1):
            arrow(d, W / 2, 760 + sgn * 40, W / 2, 760 + sgn * (40 + 180 * q), C["accent"], 8, 26)
    if t > 3.0:
        r = ease(prog(t, 3.0, 3.8))
        Ia = inertia_I(a["fw"], a.get("tf", b["tf"]), a["tw"], a["h"])
        Ib = inertia_I(b["fw"], b["tf"], b["tw"], b["h"])
        ratio = Ib / Ia
        f = font(44, "Semi")
        rows = [("Mismo acero (área)", "="), ("Misma altura", "="),
                ("Rigidez a flexión", f"x{ratio * r:.1f}".replace(".", ","))]
        for i, (lab, val) in enumerate(rows):
            yy = 250 + i * 66
            d.text((170, yy), lab, font=f, fill=mix(C["bg"], C["fg"], r))
            col = C["accent"] if i == 2 else C["muted"]
            vw = d.textlength(val, font=font(52))
            d.text((910 - vw, yy - 6), val, font=font(52), fill=mix(C["bg"], col, r))


def sc_outro_frame(d, t, p, img):
    # pórtico de edificio que se dibuja
    k = t / 2.2
    cols = [200, 440, 640, 880]
    floors = [1180, 960, 740, 520]
    for i, x in enumerate(cols):
        q = ease(clamp(k * 3 - i * 0.3))
        d.rectangle([x - 14, lerp(1180, 520, q), x + 14, 1180], fill=C["steel"])
    for j, y in enumerate(floors[1:]):
        q = ease(clamp(k * 3 - 1 - j * 0.35))
        if q > 0:
            d.rectangle([200, y - 16, lerp(200, 880, q), y + 16], fill=C["accent"] if j == 2 else C["steel"])
    d.line([(120, 1196), (960, 1196)], fill=C["muted"], width=8)


SCENES = {"hook_ibeam": sc_hook_ibeam, "beam_bend": sc_beam_bend,
          "stress_profile": sc_stress_profile, "section_morph": sc_section_morph,
          "outro_frame": sc_outro_frame}


# ---------- subtítulos ----------
def draw_caption(img, txt, t_in, t):
    """Texto grande con pop-in; *palabra* = color de acento."""
    d = ImageDraw.Draw(img)
    k = ease(t_in / 0.18)
    size = int(lerp(60, 72, k))
    f = font(size)
    words, hl_on = [], False
    for w in txt.split():
        start = w.startswith("*")
        end = w.rstrip(".,;:…!?»)").endswith("*")
        if start:
            hl_on = True
        words.append(("*" if hl_on else "") + w.replace("*", ""))
        if end:
            hl_on = False
    lines, cur = [], []
    for w in words:
        test = " ".join(x.strip("*") for x in cur + [w])
        if d.textlength(test, font=f) > 900 and cur:
            lines.append(cur)
            cur = [w]
        else:
            cur.append(w)
    lines.append(cur)
    lh = int(size * 1.18)
    y = 1330 - (len(lines) * lh) / 2
    for ln in lines:
        plain = " ".join(x.strip("*") for x in ln)
        x = (W - d.textlength(plain, font=f)) / 2
        for w in ln:
            hl = w.startswith("*")
            ww = w.strip("*")
            col = C["accent"] if hl else C["fg"]
            for ox, oy in ((-4, 0), (4, 0), (0, -4), (0, 4), (3, 3), (-3, 3), (3, -3), (-3, -3)):
                d.text((x + ox, y + oy), ww, font=f, fill=(0, 0, 0))
            d.text((x, y), ww, font=f, fill=col)
            x += d.textlength(ww + " ", font=f)
        y += lh


THEMES = {
    "neon": {"bg": (10, 10, 30), "grid": (26, 24, 60), "fg": (232, 236, 255),
             "muted": (130, 135, 190), "accent": (255, 210, 63), "comp": (0, 229, 255),
             "tens": (255, 140, 60), "steel": (150, 160, 230)},
    "nls": {"bg": (14, 15, 18), "grid": (24, 26, 32), "fg": (244, 241, 234),
            "muted": (150, 147, 140), "accent": (255, 210, 63), "comp": (77, 216, 255),
            "tens": (255, 107, 61), "steel": (190, 186, 178)},
}


def eye_icon(d, cx, cy, s, ink, accent, bg):
    """Logo del ojo de Ojo al dato, dibujado (s = ancho)."""
    pts_top, pts_bot = [], []
    for i in range(41):
        u = i / 40
        x = cx - s / 2 + s * u
        dy = (s * 0.42) * 4 * u * (1 - u) * 0.5
        pts_top.append((x, cy - dy))
        pts_bot.append((x, cy + dy))
    w = max(2, int(s * 0.045))
    d.line(pts_top, fill=ink, width=w, joint="curve")
    d.line(pts_bot, fill=ink, width=w, joint="curve")
    r = s * 0.19
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=accent)
    f = font(int(r * 1.5))
    tw = d.textlength("?", font=f)
    d.text((cx - tw / 2, cy - r * 0.95), "?", font=f, fill=bg)


def render(script, out_mp4, audio_wav):
    if script.get("style") == "fun":
        import edit_fun
        return edit_fun.render_fun(script, out_mp4, audio_wav)
    if script.get("style") in ("viral", "doc", "mystery", "creative", "premium", "exp"):
        import edit_v3
        return edit_v3.render_v3(script, out_mp4, audio_wav)
    if script.get("style") in ("live", "pop", "show"):
        import edit_v2
        return edit_v2.render_v2(script, out_mp4, audio_wav)
    if script.get("style"):
        import styles
        return styles.render_styled(script, out_mp4, audio_wav)
    global CURRENT_THEME
    theme = script.get("theme")
    CURRENT_THEME = theme
    if theme in THEMES:
        C.update(THEMES[theme])
    try:
        import scenes_nls
        SCENES.update(scenes_nls.SCENES)
    except ImportError:
        pass
    bg = background()
    dur = script["duration"]
    n = int(dur * FPS)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", audio_wav,
           "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
           "-shortest", "-movflags", "+faststart", out_mp4]
    pipe = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    wm = script.get("watermark", "")
    for i in range(n):
        t = i / FPS
        if theme == "neon":
            lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            dl = ImageDraw.Draw(lay)
            z = 1.0
            for sc in script["scenes"]:
                if sc["start"] <= t < sc["end"]:
                    SCENES[sc["type"]](dl, t - sc["start"], sc.get("params", {}), lay)
                    z = 1.0 + 0.045 * ease((t - sc["start"]) / max(0.1, sc["end"] - sc["start"]))
            if z > 1.001:
                zw, zh = int(W * z), int(H * z)
                big = lay.resize((zw, zh), Image.BILINEAR)
                ox, oy = int((zw - W) / 2), int((zh - H) * 0.4)
                lay = big.crop((ox, oy, ox + W, oy + H))
            glow = lay.resize((W // 2, H // 2), Image.BILINEAR).filter(ImageFilter.GaussianBlur(9)).resize((W, H), Image.BILINEAR)
            fr = bg.convert("RGBA")
            fr.alpha_composite(glow)
            fr.alpha_composite(glow)
            fr.alpha_composite(lay)
            img = fr.convert("RGB")
            d = ImageDraw.Draw(img)
        else:
            img = bg.copy()
            d = ImageDraw.Draw(img)
            for sc in script["scenes"]:
                if sc["start"] <= t < sc["end"]:
                    SCENES[sc["type"]](d, t - sc["start"], sc.get("params", {}), img)
        for cap in (script["captions"] if script.get("burn_captions", True) else []):
            if cap["start"] <= t < cap["end"]:
                draw_caption(img, cap["text"], t - cap["start"], t)
        if wm and theme in ("nls", "neon"):
            eye_icon(d, 100, 140, 70, C["fg"], C["accent"], C["bg"])
            d.text((150, 120), wm, font=font(36, "Semi"), fill=C["muted"])
        elif wm:
            d.text((60, 120), wm, font=font(36, "Semi"), fill=C["muted"])
        # barra de progreso fina (retención)
        d.rectangle([0, H - 10, W * (t / dur), H], fill=C["accent"])
        pipe.stdin.write(img.tobytes())
    pipe.stdin.close()
    if pipe.wait() != 0:
        raise RuntimeError("ffmpeg falló")
    return out_mp4


if __name__ == "__main__":
    s = json.load(open(sys.argv[1]))
    render(s, sys.argv[2], sys.argv[3])
