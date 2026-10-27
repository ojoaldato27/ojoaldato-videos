"""Motor de edición v2: tres paquetes de edición completamente distintos.
  live : look neón oscuro, HUD, cortes cada 2 bloques de texto, encuadres suaves, palabras clave que se iluminan.
  pop  : look plano de colores vivos, cortes en cada bloque, golpe de zoom, destellos blancos, temblor en los números,
         estallidos de rayos detrás del texto, subtítulos en mayúsculas.
  show : look concurso de TV (morado con focos), subtítulos en píldora, cortes en cada bloque, destello verde/rojo
         en las respuestas, brillo en los datos clave.
"""
import math, random, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import render as R
from render import W, H, FPS, C, ease, lerp, mix, clamp, font
import styles
from styles import chunks_for, parse_words, wrap

THEMES = {
    "live": dict(bg=(10, 10, 30), grid=(26, 24, 60), fg=(232, 236, 255), muted=(130, 135, 190),
                 accent=(255, 210, 63), comp=(0, 229, 255), tens=(255, 140, 60), steel=(150, 160, 230)),
    "pop": dict(bg=(255, 205, 70), grid=(240, 190, 60), fg=(22, 20, 35), muted=(110, 80, 30),
                accent=(225, 25, 95), comp=(25, 90, 230), tens=(235, 90, 30), steel=(60, 60, 80)),
    "show": dict(bg=(20, 6, 44), grid=(50, 20, 90), fg=(250, 245, 255), muted=(190, 160, 230),
                 accent=(255, 210, 63), comp=(255, 90, 210), tens=(255, 170, 60), steel=(200, 160, 240)),
}
PALETTE = {"live": "neon", "pop": "pop", "show": "show"}
RTHEME = {"live": "neon", "pop": "pop", "show": "show"}

EDIT = {
    "live": dict(glow=True, cut_every=1, punch=0.06, flash=0.25, shake=8.0, burst=False, framings=[
        (1.00, 0.45, 0.5), (1.12, 0.40, 0.3), (1.06, 0.50, 0.7), (1.16, 0.38, 0.5)]),
    "pop": dict(glow=False, cut_every=1, punch=0.10, flash=0.6, shake=16.0, burst=True, framings=[
        (1.00, 0.45, 0.5), (1.15, 0.38, 0.25), (1.08, 0.50, 0.75), (1.18, 0.42, 0.5), (1.05, 0.36, 0.4)]),
    "show": dict(glow=True, cut_every=1, punch=0.07, flash=0.3, shake=10.0, burst=False, framings=[
        (1.00, 0.45, 0.5), (1.12, 0.40, 0.7), (1.06, 0.48, 0.3), (1.14, 0.42, 0.5)]),
}


# ---------------- fondos ----------------
def bg_pop():
    ys = np.linspace(0, 1, H)[:, None, None]
    top, bot = np.array([255, 214, 80]), np.array([255, 160, 60])
    arr = np.broadcast_to(top + (bot - top) * ys, (H, W, 3)).copy()
    img = Image.fromarray(arr.astype(np.uint8))
    d = ImageDraw.Draw(img)
    for y in range(20, H, 46):
        for x in range(20 + (23 if (y // 46) % 2 else 0), W, 46):
            d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(250, 190, 60))
    return img


def bg_show():
    img = Image.new("RGB", (W, H), (14, 4, 32))
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for cx, col in ((180, (255, 90, 210, 60)), (900, (90, 160, 255, 60))):
        d.polygon([(cx - 40, -20), (cx + 40, -20), (540 + (cx - 540) * 0.2 + 420, H), (540 + (cx - 540) * 0.2 - 420, H)], fill=col)
    lay = lay.filter(ImageFilter.GaussianBlur(40))
    img = img.convert("RGBA")
    img.alpha_composite(lay)
    d2 = ImageDraw.Draw(img)
    for i in range(30):
        x = (i * 37) % W
        d2.ellipse([x - 2, 1840 + (i % 3) * 12, x + 2, 1844 + (i % 3) * 12], fill=(255, 220, 120, 200))
    return img.convert("RGB")


CALM = False


def back(x):
    """Entrada con rebote (sobrepasa y vuelve)."""
    x = clamp(x)
    if CALM:
        return 1.0
    c = 2.2
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


# ---------------- subtítulos ----------------
def glue(chunk):
    """Une '°C', '%', '…' a la palabra anterior para que nunca salten de línea."""
    out = []
    for w, h in chunk:
        if out and (w.startswith("°") or w in ("%", "°C", "km", "km/h", "m") and out[-1][0][-1:].isdigit()):
            out[-1] = (out[-1][0] + "\u00a0" + w, out[-1][1] or h)
        else:
            out.append((w, h))
    return out

def cap_pill(img, chunk, t_in):
    d = ImageDraw.Draw(img, "RGBA")
    size = int(80 * lerp(0.55, 1.0, back(t_in / 0.16)))
    f = font(size, "Black")
    lines = wrap(d, chunk, f, 860)
    lh = int(size * 1.25)
    y = 1530 - len(lines) * lh / 2
    for ln in lines:
        txt = " ".join(x for x, _ in ln)
        tw = d.textlength(txt, font=f)
        x = (W - tw) / 2
        d.rounded_rectangle([x - 34, y - 10, x + tw + 34, y + size + 18], radius=40, fill=(230, 40, 150, 235))
        for wd, hl in ln:
            col = (255, 220, 70) if hl else (255, 255, 255)
            d.text((x, y), wd, font=f, fill=col)
            x += d.textlength(wd + " ", font=f)
        y += lh


def cap_word2(img, chunk, t_in, y_center=1530):
    d = ImageDraw.Draw(img)
    size = int(90 * lerp(0.55, 1.0, back(t_in / 0.16)))
    f = font(size, "Black")
    lines = wrap(d, chunk, f, 900)
    lh = int(size * 1.1)
    y = y_center - len(lines) * lh / 2
    for ln in lines:
        x = (W - d.textlength(" ".join(x for x, _ in ln), font=f)) / 2
        for wd, hl in ln:
            col = (255, 214, 64) if hl else (255, 255, 255)
            d.text((x + 4, y + 6), wd, font=f, fill=(0, 0, 0), stroke_width=8, stroke_fill=(0, 0, 0))
            d.text((x, y), wd, font=f, fill=col, stroke_width=7, stroke_fill=(0, 0, 0))
            x += d.textlength(wd + " ", font=f)
        y += lh


def cap_pop(img, chunk, t_in):
    d = ImageDraw.Draw(img)
    size = int(108 * lerp(0.5, 1.0, back(t_in / 0.16)))
    f = font(size, "Black")
    words = [(w.upper(), h) for w, h in chunk]
    lines = wrap(d, words, f, 940)
    lh = int(size * 1.06)
    y = 1520 - len(lines) * lh / 2
    rot = (hash(" ".join(w for w, _ in chunk)) % 5 - 2) * 0.6
    for ln in lines:
        x = (W - d.textlength(" ".join(x for x, _ in ln), font=f)) / 2
        for wd, hl in ln:
            col = (255, 255, 255) if not hl else (255, 235, 60)
            d.text((x + 6, y + 8), wd, font=f, fill=(22, 20, 35), stroke_width=10, stroke_fill=(22, 20, 35))
            d.text((x, y), wd, font=f, fill=col, stroke_width=9, stroke_fill=(22, 20, 35))
            x += d.textlength(wd + " ", font=f)
        y += lh


def burst(img, t_in, cx=540, cy=1520):
    """Estallido de rayos detrás del texto (pop)."""
    a = 1 - ease(t_in / 0.45)
    if a <= 0:
        return
    d = ImageDraw.Draw(img, "RGBA")
    r0, r1 = 120 + 260 * ease(t_in / 0.45), 220 + 420 * ease(t_in / 0.45)
    for i in range(14):
        ang = i / 14 * 2 * math.pi + 0.2
        d.line([(cx + math.cos(ang) * r0, cy + math.sin(ang) * r0 * 0.55),
                (cx + math.cos(ang) * r1, cy + math.sin(ang) * r1 * 0.55)], fill=(255, 255, 255, int(220 * a)), width=10)


def sticker(img, txt, t_in):
    d = ImageDraw.Draw(img, "RGBA")
    a = ease(t_in / 0.25)
    f = font(36, "Black")
    tw = d.textlength(txt.upper(), font=f)
    x, y = 60, 200
    d.rounded_rectangle([x, y, x + tw + 40, y + 62], radius=16, fill=(22, 20, 35, int(240 * a)))
    d.text((x + 20, y + 10), txt.upper(), font=f, fill=(255, 235, 60, int(255 * a)))


def chapter_live(img, txt, t_in):
    d = ImageDraw.Draw(img, "RGBA")
    a = ease(t_in / 0.4)
    f = font(30, "Mono")
    d.text((60, 196), txt.upper(), font=f, fill=(0, 229, 255, int(255 * a)))
    d.line([(60, 240), (60 + 420 * a, 240)], fill=(0, 229, 255, int(160 * a)), width=2)


def notif_banner(img, t_in, title, body, hold=2.6, icon=None):
    """Banner tipo notificación del móvil que baja desde arriba con rebote."""
    if t_in < 0 or t_in > hold + 0.35:
        return img
    if t_in < 0.45:
        k = back(t_in / 0.45)
    elif t_in > hold:
        k = 1 - ease((t_in - hold) / 0.35)
    else:
        k = 1.0
    bw, bh, r = 1000, 196, 52
    x0 = (W - bw) // 2
    y0 = int(lerp(-bh - 30, 70, k))
    if y0 + bh <= 0:
        return img
    box = (x0, max(0, y0), x0 + bw, y0 + bh)
    region = img.crop(box).filter(ImageFilter.GaussianBlur(28))
    region = Image.blend(region, Image.new("RGB", region.size, (242, 242, 247)), 0.62)
    mask = Image.new("L", (bw, bh), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, bw - 1, bh - 1], radius=r, fill=255)
    mask = mask.crop((0, max(0, -y0), bw, bh))
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([x0, y0 + 10, x0 + bw, y0 + bh + 10], radius=r, fill=(0, 0, 0, 70))
    sh = sh.filter(ImageFilter.GaussianBlur(18))
    base = img.convert("RGBA")
    base.alpha_composite(sh)
    img = base.convert("RGB")
    img.paste(region, box[:2], mask)
    d = ImageDraw.Draw(img)
    ix, iy, isz = x0 + 34, y0 + (bh - 100) // 2, 100
    if icon is not None:                      # foto de perfil de la marca (Ojo al dato, 21/10)
        ic = icon.convert("RGB").resize((isz, isz), Image.LANCZOS)
        m_ = Image.new("L", (isz, isz), 0)
        ImageDraw.Draw(m_).rounded_rectangle([0, 0, isz - 1, isz - 1], radius=24, fill=255)
        img.paste(ic, (ix, iy), m_)
    else:
        d.rounded_rectangle([ix, iy, ix + isz, iy + isz], radius=24, fill=(14, 15, 18))
        R.eye_icon(d, ix + isz / 2, iy + isz / 2, 64, (255, 255, 255), (255, 210, 63), (14, 15, 18))
    tx = ix + isz + 28
    d.text((tx, y0 + 40), title, font=font(42, "Bold"), fill=(10, 10, 12))
    ft = font(34, "Semi")
    d.text((x0 + bw - 40 - d.textlength("ahora", font=ft), y0 + 46), "ahora", font=ft, fill=(120, 120, 128))
    d.text((tx, y0 + 98), body, font=font(38, "Semi"), fill=(30, 30, 34))
    return img


# ---------------- render ----------------
def render_v2(script, out_mp4, audio_wav, only_times=None):
    style = script["style"]
    E = dict(EDIT[style])
    calm = bool(script.get("calm"))
    global CALM
    CALM = calm
    if calm:
        E.update(cut_every=10 ** 6, punch=0.0, shake=4.0, framings=[(1.0, 0.45, 0.5)], flash=E["flash"] * 0.5)
    R.CURRENT_THEME = RTHEME[style]
    C.update(THEMES[style])
    import scenes_nls, scenes_planes
    R.SCENES.update(scenes_nls.SCENES)
    R.SCENES.update(scenes_planes.SCENES)
    scenes_planes.set_palette(PALETTE[style])
    bg = {"live": R.background_neon, "pop": bg_pop, "show": bg_show}[style]()
    dur = script["duration"]
    n = int(dur * FPS)
    offset_y = 100
    caps = sorted(script["captions"], key=lambda c: c["start"])
    chunks = []
    for c in caps:
        chunks += chunks_for(c["text"], c["start"], c["end"], n=script.get("chunk_n", 3))
    # puntos de corte: inicio de escena y cada N bloques
    cuts = sorted({sc["start"] for sc in script["scenes"]} |
                  {cs for i, (cs, ce, g) in enumerate(chunks) if i % E["cut_every"] == 0})
    booms = [sc["start"] for sc in script["scenes"] if sc["type"] == "top_card"]
    reveals = [(sc["start"] + sc["params"].get("count_at", 1.2) + 3.0, sc["params"].get("answer"))
               for sc in script["scenes"] if sc["type"] == "quiz"]
    scene_starts = [sc["start"] for sc in script["scenes"] if sc["start"] > 0]
    # zooms suaves solo en datos clave, separados al menos `zoom_gap` segundos
    key_zooms, last = [], -99
    for cs, ce, g in chunks:
        if any(h for _, h in g) and cs - last >= script.get("zoom_gap", 4.5):
            key_zooms.append((cs, ce))
            last = cs
    rng = random.Random(5)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-i", audio_wav, "-c:v", "libx264", "-preset", "medium", "-crf", "19",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
           "-shortest", "-movflags", "+faststart", out_mp4]
    pipe = None if only_times else subprocess.Popen(cmd, stdin=subprocess.PIPE)
    frames = [int(x * FPS) for x in only_times] if only_times else range(n)
    shots = []
    wm = script.get("watermark", "")
    for i in frames:
        t = i / FPS
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        dl = ImageDraw.Draw(lay)
        cur_sc = None
        for sc in script["scenes"]:
            if sc["start"] <= t < sc["end"]:
                R.SCENES[sc["type"]](dl, t - sc["start"], sc.get("params", {}), lay)
                cur_sc = sc
        # encuadre según el último corte
        ci = max([k for k, c in enumerate(cuts) if c <= t] or [0])
        fz, fy, fx = E["framings"][ci % len(E["framings"])]
        if cur_sc and cur_sc["type"] in ("quiz", "top_card", "title", "quiz_end", "outro_nls"):
            fz, fy, fx = 1.0 + 0.04 * (ci % 2), 0.45, 0.5
        since_cut = t - cuts[ci] if cuts else 9
        kchunk = None
        for cs, ce, g in chunks:
            if cs <= t < ce:
                kchunk = (cs, g)
        is_key = bool(kchunk and any(h for _, h in kchunk[1]))
        kt = t - kchunk[0] if kchunk else 9
        if calm:
            z = 1.0
            for zs, ze in key_zooms:
                if zs <= t < ze + 0.6:
                    up = ease(clamp((t - zs) / 0.45))
                    down = 1 - ease(clamp((t - ze) / 0.6))
                    z = 1 + 0.06 * up * down
        else:
            z = fz * (1 + 0.05 * clamp(since_cut / 2.0)) + E["punch"] * (1 - ease(since_cut / 0.2))
        if is_key and not calm:
            z += 0.06 * (1 - ease(kt / 0.25))
        if z > 1.001:
            zw, zh = int(W * z), int(H * z)
            big = lay.resize((zw, zh), Image.BILINEAR)
            ox, oy = int((zw - W) * fx), int((zh - H) * fy)
            lay = big.crop((ox, oy, ox + W, oy + H))
        # transición de barrido al empezar cada escena (alterna dirección)
        if cur_sc and cur_sc["start"] > 0:
            ts = t - cur_sc["start"]
            if calm and ts < 0.25:
                a = lay.getchannel("A").point(lambda v, k=ease(ts / 0.25): int(v * k))
                lay.putalpha(a)
            elif not calm and ts < 0.22:
                k = ease(ts / 0.22)
                dirn = 1 if script["scenes"].index(cur_sc) % 2 else -1
                dx = int((1 - k) * W * 0.55 * dirn)
                blurred = lay.resize((W // 16, H), Image.BILINEAR).resize((W, H), Image.BILINEAR)
                lay = Image.blend(lay, blurred, 0.85 * (1 - k))
                moved = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                moved.alpha_composite(lay.crop((max(0, -dx), 0, min(W, W - dx), H)), (max(0, dx), 0))
                lay = moved
        sx = sy = 0
        if is_key and kt < 0.22 and not calm:
            a = 1 - kt / 0.22
            sx, sy = int(rng.uniform(-1, 1) * E["shake"] * 0.6 * a), int(rng.uniform(-1, 1) * E["shake"] * 0.6 * a)
        for b in booms:
            if 0 <= t - b < 0.35:
                a = 1 - (t - b) / 0.35
                sx, sy = int(rng.uniform(-1, 1) * E["shake"] * a), int(rng.uniform(-1, 1) * E["shake"] * a)
        shifted = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        shifted.alpha_composite(lay.crop((max(0, -sx), 0, W - max(0, sx), H - offset_y - abs(sy))), (max(0, sx), max(0, offset_y + sy)))
        lay = shifted
        fr = bg.convert("RGBA")
        cur_chunk = None
        for cs, ce, g in chunks:
            if cs <= t < ce:
                cur_chunk = (cs, g)
        key_boost = 0.0
        if cur_chunk and any(h for _, h in cur_chunk[1]):
            key_boost = 1 - ease((t - cur_chunk[0]) / 0.5)
        if E["glow"]:
            glow = lay.resize((W // 2, H // 2), Image.BILINEAR).filter(ImageFilter.GaussianBlur(9)).resize((W, H), Image.BILINEAR)
            fr.alpha_composite(glow)
            fr.alpha_composite(glow)
            if key_boost > 0.05:
                a = glow.getchannel("A").point(lambda v: int(v * key_boost))
                g2 = glow.copy()
                g2.putalpha(a)
                fr.alpha_composite(g2)
                fr.alpha_composite(g2)
        else:
            sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            sh.alpha_composite(lay.crop((0, 0, W - 7, H - 8)), (7, 8))
            a = sh.getchannel("A").point(lambda v: int(v * 0.22))
            black = Image.new("RGBA", (W, H), (22, 20, 35, 0))
            black.putalpha(a)
            fr.alpha_composite(black)
        fr.alpha_composite(lay)
        img = fr.convert("RGB")
        # destellos
        if E["flash"]:
            for s0 in scene_starts:
                if 0 <= t - s0 < 0.12:
                    fl = (255, 255, 255) if style != "show" else (255, 120, 220)
                    img = Image.blend(img, Image.new("RGB", (W, H), fl), E["flash"] * (1 - (t - s0) / 0.12))
        for rt, ok in reveals:
            if 0 <= t - rt < 0.35:
                col = (60, 230, 140) if ok else (255, 60, 80)
                img = Image.blend(img, Image.new("RGB", (W, H), col), 0.45 * (1 - (t - rt) / 0.35))
        # capítulos
        for ch in script.get("chapters", []):
            if ch["start"] <= t < ch["end"]:
                if style == "live":
                    if not (cur_sc and cur_sc["type"] == "flight" and cur_sc["params"].get("hud", True)):
                        chapter_live(img, ch["text"], t - ch["start"])
                elif style == "pop":
                    sticker(img, ch["text"], t - ch["start"])
        # subtítulos
        if cur_chunk:
            cur_chunk = (cur_chunk[0], glue(cur_chunk[1]))
            ti = t - cur_chunk[0]
            if style == "pop":
                if E["burst"] and any(h for _, h in cur_chunk[1]):
                    burst(img, ti)
                cap_pop(img, cur_chunk[1], ti)
            elif style == "show":
                cap_pill(img, cur_chunk[1], ti)
            else:
                cap_word2(img, cur_chunk[1], ti)
        d = ImageDraw.Draw(img)
        if wm:
            R.eye_icon(d, 100, 140, 70, C["fg"], (255, 210, 63), (14, 15, 18))
            d.text((150, 120), wm, font=font(34, "Mono" if style == "live" else "Semi"), fill=C["muted"])
        for nt in script.get("notifs", []):
            img = notif_banner(img, t - nt["t"], nt["title"], nt["body"])
        d = ImageDraw.Draw(img)
        d.rectangle([0, H - 12, W * (t / dur), H], fill=C["accent"])
        if pipe is None:
            shots.append(img)
            continue
        pipe.stdin.write(img.tobytes())
    if pipe is None:
        return shots
    pipe.stdin.close()
    if pipe.wait() != 0:
        raise RuntimeError("ffmpeg falló")
    return out_mp4
