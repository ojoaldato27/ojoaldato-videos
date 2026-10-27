"""Tres estilos de edición sobre las mismas escenas:
  neon_doc : neón documental (inspirado en explicativos de línea de neón): brillo, zoom lento,
             subtítulos frase a frase pequeños en letra mono, etiquetas de capítulo.
  paper    : mapa de papel tipo documental: fondo de papel con grano, rojo cartográfico,
             tipografía con serifa, rotulador sobre las palabras clave, tarjetas de capítulo.
  punch    : ritmo viral: subtítulos palabra a palabra (2-3 por pantalla) muy grandes,
             golpe de zoom en cada bloque, destello en cada cambio de escena.
"""
import math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import render as R
from render import W, H, FPS, C, ease, lerp, mix, clamp, font

SERIF_B = "/usr/share/fonts/truetype/crosextra/Caladea-Bold.ttf"
_SF = {}


def serif(size):
    if size not in _SF:
        try:
            _SF[size] = ImageFont.truetype(SERIF_B, size)
        except OSError:
            _SF[size] = font(size, "Black")
    return _SF[size]


PAPER = {"bg": (236, 228, 212), "grid": (214, 204, 184), "fg": (34, 30, 26),
         "muted": (120, 108, 92), "accent": (206, 44, 44), "comp": (40, 90, 160),
         "tens": (206, 44, 44), "steel": (110, 100, 88)}


def background_paper():
    rng = np.random.default_rng(3)
    base = np.zeros((H, W, 3), np.float32)
    ys = np.linspace(0, 1, H)[:, None]
    for i, (a, b) in enumerate(zip((240, 233, 218), (226, 216, 196))):
        base[:, :, i] = a + (b - a) * ys
    base += rng.normal(0, 5.5, (H, W, 1))
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))
    v = Image.new("L", (W, H), 0)
    ImageDraw.Draw(v).ellipse([-260, -160, W + 260, H + 160], fill=255)
    v = v.filter(ImageFilter.GaussianBlur(240))
    return Image.composite(img, Image.new("RGB", (W, H), (200, 186, 160)), v)


# ---------- texto ----------
def parse_words(txt):
    out, on = [], False
    for w in [x for x in txt.replace("\n", " ").replace("\t", " ").split(" ") if x]:  # el espacio duro (\u00a0) une «80 %»
        st = w.startswith("*")
        en = w.rstrip(".,;:…!?»)").endswith("*")
        if st:
            on = True
        out.append((w.replace("*", ""), on))
        if en:
            on = False
    return out


def wrap(d, words, f, maxw):
    lines, cur = [], []
    for w in words:
        test = " ".join(x for x, _ in cur + [w])
        if d.textlength(test, font=f) > maxw and cur:
            lines.append(cur)
            cur = [w]
        else:
            cur.append(w)
    if cur:
        lines.append(cur)
    return lines


def cap_doc(img, txt, t_in):
    """Frase completa, letra mono, caja oscura discreta."""
    d = ImageDraw.Draw(img, "RGBA")
    f = font(44, "Mono")
    words = parse_words(txt)
    lines = wrap(d, words, f, 860)
    lh = 60
    a = ease(t_in / 0.2)
    h = len(lines) * lh + 40
    y0 = 1500 - h / 2
    wmax = max(d.textlength(" ".join(x for x, _ in ln), font=f) for ln in lines)
    d.rounded_rectangle([(W - wmax) / 2 - 30, y0, (W + wmax) / 2 + 30, y0 + h], radius=18,
                        fill=(8, 8, 26, int(200 * a)), outline=(0, 229, 255, int(110 * a)), width=2)
    y = y0 + 20
    for ln in lines:
        x = (W - d.textlength(" ".join(x for x, _ in ln), font=f)) / 2
        for wd, hl in ln:
            col = C["accent"] if hl else C["fg"]
            d.text((x, y), wd, font=f, fill=col + (int(255 * a),))
            x += d.textlength(wd + " ", font=f)
        y += lh


def cap_paper(img, txt, t_in):
    """Tercio inferior con serifa; las palabras clave se subrayan con rotulador amarillo."""
    d = ImageDraw.Draw(img, "RGBA")
    f = serif(62)
    words = parse_words(txt)
    lines = wrap(d, words, f, 880)
    lh = 78
    y = 1490 - len(lines) * lh / 2
    mk = ease(clamp((t_in - 0.15) / 0.35))
    for ln in lines:
        x = (W - d.textlength(" ".join(x for x, _ in ln), font=f)) / 2
        for wd, hl in ln:
            ww = d.textlength(wd, font=f)
            if hl and mk > 0:
                d.rectangle([x - 6, y + 22, x - 6 + (ww + 12) * mk, y + 70], fill=(255, 214, 64, 200))
            d.text((x, y), wd, font=f, fill=PAPER["fg"])
            x += d.textlength(wd + " ", font=f)
        y += lh


def chunks_for(txt, start, end, n=3):
    words = parse_words(txt)
    stop = {"el", "la", "los", "las", "un", "una", "de", "del", "que", "en", "a", "al", "y", "o",
            "es", "se", "su", "por", "para", "con", "lo", "mas", "más", "tan", "como", "→", "esta", "este"}
    groups, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        nxt_exists = i + 1 < len(words)
        ends_stop = (w[0].lower().strip("¿¡") in stop or any(ch.isdigit() for ch in w[0])) and nxt_exists
        if (len(cur) >= n and not ends_stop) or len(cur) >= n + 2 or w[0].endswith((",", ".", ":", "…", "?", "!")):
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    total = sum(len(g) for g in groups)
    out, t = [], start
    for g in groups:
        dt = (end - start) * len(g) / total
        out.append((t, t + dt, g))
        t += dt
    return out


def cap_punch(img, chunk, t_in):
    d = ImageDraw.Draw(img)
    pop = ease(t_in / 0.12)
    size = int(lerp(80, 100, pop))
    f = font(size, "Black")
    lines = wrap(d, chunk, f, 920)
    lh = int(size * 1.08)
    y = 1290 - len(lines) * lh / 2
    for ln in lines:
        x = (W - d.textlength(" ".join(x.upper() for x, _ in ln), font=f)) / 2
        for wd, hl in ln:
            wd = wd.upper()
            col = C["accent"] if hl else (255, 255, 255)
            d.text((x, y), wd, font=f, fill=col, stroke_width=9, stroke_fill=(0, 0, 0))
            x += d.textlength(wd + " ", font=f)
        y += lh


def cap_word(img, chunk, t_in):
    """Estilo de las referencias: 2-3 palabras, blanco grueso con contorno, centrado, palabra clave en amarillo."""
    d = ImageDraw.Draw(img)
    pop = ease(t_in / 0.1)
    size = int(lerp(78, 88, pop))
    f = font(size, "Black")
    lines = wrap(d, chunk, f, 900)
    lh = int(size * 1.1)
    y = 1480 - len(lines) * lh / 2
    for ln in lines:
        x = (W - d.textlength(" ".join(x for x, _ in ln), font=f)) / 2
        for wd, hl in ln:
            col = (255, 214, 64) if hl else (255, 255, 255)
            d.text((x + 4, y + 6), wd, font=f, fill=(0, 0, 0), stroke_width=8, stroke_fill=(0, 0, 0))
            d.text((x, y), wd, font=f, fill=col, stroke_width=7, stroke_fill=(0, 0, 0))
            x += d.textlength(wd + " ", font=f)
        y += lh


def chapter_tag(img, txt, t_in, style):
    d = ImageDraw.Draw(img, "RGBA")
    a = ease(t_in / 0.4)
    if style == "neon_doc":
        f = font(30, "Mono")
        d.text((60, 196), txt.upper(), font=f, fill=C["comp"] + (int(255 * a),))
        d.line([(60, 240), (60 + 420 * a, 240)], fill=C["comp"] + (int(160 * a),), width=2)
    elif style == "paper":
        if t_in < 2.2:
            num, _, title = txt.partition(" · ")
            f1, f2 = serif(120), serif(56)
            k = ease(t_in / 0.35) * (1 - ease(clamp((t_in - 1.7) / 0.5)))
            d.text((70, 210), num, font=f1, fill=PAPER["accent"] + (int(255 * k),))
            d.text((70, 340), title, font=f2, fill=PAPER["fg"] + (int(255 * k),))
            d.line([(70, 418), (70 + 520 * k, 418)], fill=PAPER["fg"] + (int(200 * k),), width=4)


# ---------- render ----------
def render_styled(script, out_mp4, audio_wav):
    style = script["style"]
    theme = "paper" if style == "paper" else "neon"
    R.CURRENT_THEME = theme
    C.update(PAPER if theme == "paper" else R.THEMES["neon"])
    import scenes_nls, scenes_planes
    R.SCENES.update(scenes_nls.SCENES)
    R.SCENES.update(scenes_planes.SCENES)
    bg = background_paper() if theme == "paper" else R.background_neon()
    dur = script["duration"]
    n = int(dur * FPS)
    offset_y = {"neon_doc": 150, "paper": 200, "punch": 60}[style]
    caps = sorted(script["captions"], key=lambda c: c["start"])
    pchunks = []
    word_mode = script.get("caption_mode") == "words"
    if style == "punch" or word_mode:
        for c in caps:
            pchunks += chunks_for(c["text"], c["start"], c["end"])
    scene_starts = [sc["start"] for sc in script["scenes"] if sc["start"] > 0]
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", audio_wav,
           "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
           "-shortest", "-movflags", "+faststart", out_mp4]
    pipe = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    wm = script.get("watermark", "")
    for i in range(n):
        t = i / FPS
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        dl = ImageDraw.Draw(lay)
        z = 1.0
        for sc in script["scenes"]:
            if sc["start"] <= t < sc["end"]:
                R.SCENES[sc["type"]](dl, t - sc["start"], sc.get("params", {}), lay)
                z = 1.0 + 0.045 * ease((t - sc["start"]) / max(0.1, sc["end"] - sc["start"]))
        cur_chunk = None
        if style == "punch" or word_mode:
            for cs, ce, g in pchunks:
                if cs <= t < ce:
                    cur_chunk = (cs, g)
                    if style == "punch":
                        z += 0.05 * (1 - ease((t - cs) / 0.22))
        if z > 1.001:
            zw, zh = int(W * z), int(H * z)
            big = lay.resize((zw, zh), Image.BILINEAR)
            ox, oy = int((zw - W) / 2), int((zh - H) * 0.4)
            lay = big.crop((ox, oy, ox + W, oy + H))
        if offset_y:
            shifted = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            shifted.alpha_composite(lay.crop((0, 0, W, H - offset_y)), (0, offset_y))
            lay = shifted
        fr = bg.convert("RGBA")
        if theme == "neon":
            glow = lay.resize((W // 2, H // 2), Image.BILINEAR).filter(ImageFilter.GaussianBlur(9)).resize((W, H), Image.BILINEAR)
            fr.alpha_composite(glow)
            fr.alpha_composite(glow)
        fr.alpha_composite(lay)
        img = fr.convert("RGB")
        # destello en cambios de escena (ritmo viral)
        if style == "punch":
            for s0 in scene_starts:
                if 0 <= t - s0 < 0.12:
                    a = 1 - (t - s0) / 0.12
                    img = Image.blend(img, Image.new("RGB", (W, H), (255, 255, 255)), 0.55 * a)
        # capítulos
        for ch in script.get("chapters", []):
            if ch["start"] <= t < ch["end"]:
                chapter_tag(img, ch["text"], t - ch["start"], style)
        # subtítulos
        if word_mode and cur_chunk:
            cap_word(img, cur_chunk[1], t - cur_chunk[0])
        elif style == "punch" and cur_chunk:
            cap_punch(img, cur_chunk[1], t - cur_chunk[0])
        else:
            for c in caps:
                if c["start"] <= t < c["end"]:
                    (cap_doc if style == "neon_doc" else cap_paper)(img, c["text"], t - c["start"])
        d = ImageDraw.Draw(img)
        if wm:
            R.eye_icon(d, 100, 140, 70, C["fg"], (255, 210, 63), (14, 15, 18))
            wf = font(34, "Mono") if style != "paper" else serif(38)
            d.text((150, 120), wm, font=wf, fill=C["muted"])
        d.rectangle([0, H - 10, W * (t / dur), H], fill=C["accent"])
        pipe.stdin.write(img.tobytes())
    pipe.stdin.close()
    if pipe.wait() != 0:
        raise RuntimeError("ffmpeg falló")
    return out_mp4
