"""Estilo «docu» (pedido por Iker el 19/10, copiando la edición de su vídeo de referencia de Julio César):
fondo azul noche con polvo dorado, título en serif cursiva arriba con una línea pequeña en mayúsculas espaciadas,
subtítulos de 1-3 palabras al ritmo de la voz con la palabra clave en dorado, tarjeta «Seguir → Siguiendo» a mitad
y transiciones suaves. Si el módulo trae VOICE (MP3/WAV de la locución), los tiempos salen de la propia voz."""
import math, os, re, subprocess, tempfile, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import render as R
from render import W, H, ease, lerp, clamp
from styles import parse_words

FD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fonts")
F_TITLE = os.path.join(FD, "PlayfairDisplay-Italic.ttf")
F_CAPS = os.path.join(FD, "Montserrat.ttf")
F_UI = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
F_UI_M = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"
F_UI_B = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"

CREAM = (246, 241, 230)
GOLD = (245, 186, 52)
SUBC = (198, 203, 218)
NAVY_C = (33, 41, 74)
NAVY_E = (9, 12, 25)
CARD = (27, 34, 62)
_F = {}


def font(path, size, var=None):
    k = (path, size, var)
    if k not in _F:
        fo = ImageFont.truetype(path, size)
        if var:
            try:
                fo.set_variation_by_name(var)
            except Exception:
                pass
        _F[k] = fo
    return _F[k]


def title_font(size):
    return font(F_TITLE, size, "SemiBold Italic")


def caps_font(size, var="Bold"):
    return font(F_CAPS, size, var)


# ------------------------------------------------------------------ fondo
_BG = {}


def _bg_base(cx, cy):
    k = (cx, cy)
    if k not in _BG:
        ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
        r = np.sqrt(((xs - cx) / 820.0) ** 2 + ((ys - cy) / 1180.0) ** 2)
        q = np.clip(r, 0, 1) ** 1.25
        a = np.array(NAVY_C, np.float32)
        b = np.array(NAVY_E, np.float32)
        im = a[None, None] * (1 - q[..., None]) + b[None, None] * q[..., None]
        # grano muy suave para que no haga bandas
        im += np.random.default_rng(1).normal(0, 1.4, im.shape)
        _BG[k] = Image.fromarray(np.clip(im, 0, 255).astype(np.uint8), "RGB")
    return _BG[k]


def dust(img, t, n=70, seed=2, col=(255, 214, 140), alpha=90, area=(0, 380, W, 1500), speed=10, size=(1.2, 3.2)):
    d = ImageDraw.Draw(img, "RGBA")
    rng = random.Random(seed)
    x0, y0, x1, y1 = area
    for _ in range(n):
        px, py = rng.uniform(x0, x1), rng.uniform(y0, y1)
        ph, sp, s = rng.uniform(0, 6.28), rng.uniform(0.4, 1.0), rng.uniform(*size)
        x = px + math.sin(t * 0.35 * sp + ph) * 26
        y = y0 + ((py - y0 - t * speed * sp) % (y1 - y0))
        tw = 0.55 + 0.45 * math.sin(t * 1.3 * sp + ph * 2)
        a = int(alpha * tw)
        d.ellipse([x - s, y - s, x + s, y + s], fill=col + (a,))


POP_BG = [None]          # estilo «pop» (pop.py): sustituye el fondo de todas las escenas


def bg(img, t, cx=540, cy=820, dust_n=70, seed=2):
    if POP_BG[0]:
        return POP_BG[0](img, t, cx, cy, dust_n, seed)
    img.paste(_bg_base(cx, cy))
    dust(img, t, dust_n, seed)


_GL = {}


def soft_glow(r, col, a=0.5):
    k = (r, col, a)
    if k not in _GL:
        s = int(r * 2)
        im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        ys, xs = np.mgrid[0:s, 0:s].astype(np.float32)
        q = np.clip(1 - np.sqrt((xs - r) ** 2 + (ys - r) ** 2) / r, 0, 1) ** 2.2
        arr = np.zeros((s, s, 4), np.uint8)
        arr[..., 0], arr[..., 1], arr[..., 2] = col
        arr[..., 3] = (q * 255 * a).astype(np.uint8)
        _GL[k] = Image.fromarray(arr, "RGBA")
    return _GL[k]


def glow_at(img, x, y, r, col=(255, 210, 130), a=0.5):
    g = soft_glow(int(r), col, a)
    img.paste(g, (int(x - r), int(y - r)), g) if img.mode == "RGB" else img.alpha_composite(g, (int(x - r), int(y - r)))


# ------------------------------------------------------------------ piezas gráficas
def pill(img, cx, cy, text, k=1.0, size=24, col=(222, 226, 238), fill=(13, 17, 33), border=(255, 255, 255)):
    """Etiqueta pequeña tipo «N₂ · CON SU CORONA»."""
    if k <= 0.01:
        return
    fo = font(F_UI, size)
    tr = 4
    tmp = ImageDraw.Draw(Image.new("RGBA", (4, 4)))
    tw = sum(tmp.textlength(ch, font=fo) for ch in text) + tr * (len(text) - 1)
    w, h = tw + 44, size + 26
    lay = Image.new("RGBA", (int(w) + 4, int(h) + 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle([2, 2, w, h], radius=10, fill=fill + (int(225 * k),), outline=border + (int(46 * k),), width=2)
    x = 24
    for ch in text:
        d.text((x, h / 2 + 2), ch, font=fo, fill=col + (int(255 * k),), anchor="lm")
        x += tmp.textlength(ch, font=fo) + tr
    y_off = (1 - k) * 10
    if img.mode == "RGB":
        img.paste(lay, (int(cx - w / 2), int(cy - h / 2 + y_off)), lay)
    else:
        img.alpha_composite(lay, (int(cx - w / 2), int(cy - h / 2 + y_off)))


def dotted(img, p0, p1, p2, k, col=GOLD, r=3.2, step=20, alpha=230, head=True):
    """Línea de puntos dorada que se va dibujando por una curva (p0 → p2, con p1 de control)."""
    if k <= 0:
        return
    d = ImageDraw.Draw(img, "RGBA")
    L = 0
    prev = p0
    pts = []
    for i in range(101):
        u = i / 100
        x = (1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * p1[0] + u * u * p2[0]
        y = (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * p1[1] + u * u * p2[1]
        L += math.hypot(x - prev[0], y - prev[1])
        pts.append((x, y, L))
        prev = (x, y)
    tot = pts[-1][2] * k
    s = 0.0
    j = 0
    while s <= tot:
        while j < len(pts) - 1 and pts[j][2] < s:
            j += 1
        x, y, _ = pts[j]
        a = alpha * (0.45 + 0.55 * (s / max(1, tot)))
        d.ellipse([x - r, y - r, x + r, y + r], fill=col + (int(a),))
        s += step
    if head and k < 1:
        x, y, _ = pts[j]
        glow_at(img, x, y, 30, col, 0.8)


def stamp_text(img, cx, cy, text, size, col=CREAM, k=1.0, glow=True, fo=None):
    """Texto grande en serif cursiva con brillo (para cifras dentro de la escena)."""
    if k <= 0.01:
        return
    fo = fo or title_font(size)
    tmp = ImageDraw.Draw(Image.new("RGBA", (4, 4)))
    tw = int(tmp.textlength(text, font=fo)) + 80
    th = int(size * 1.6)
    lay = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((tw / 2, th / 2), text, font=fo, fill=col + (255,), anchor="mm")
    out = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    if glow:
        g = lay.filter(ImageFilter.GaussianBlur(14))
        g.putalpha(g.getchannel("A").point(lambda v: int(v * 0.55)))
        out.alpha_composite(g)
    out.alpha_composite(lay)
    if k < 1:
        out.putalpha(out.getchannel("A").point(lambda v: int(v * k)))
    pos = (int(cx - tw / 2), int(cy - th / 2 + (1 - k) * 14))
    if img.mode == "RGB":
        img.paste(out, pos, out)
    else:
        img.alpha_composite(out, pos)


# ------------------------------------------------------------------ cabecera: título + subtítulo
_HC = {}


def _head_img(title, sub):
    k = (title, sub)
    if k in _HC:
        return _HC[k]
    size = 118
    tmp = ImageDraw.Draw(Image.new("RGBA", (4, 4)))
    while tmp.textlength(title, font=title_font(size)) > 980 and size > 60:
        size -= 4
    fo = title_font(size)
    lay = Image.new("RGBA", (W, 260), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.text((W / 2, 92), title, font=fo, fill=CREAM + (255,), anchor="mm")
    g = lay.filter(ImageFilter.GaussianBlur(16))
    g.putalpha(g.getchannel("A").point(lambda v: int(v * 0.5)))
    t_im = Image.new("RGBA", (W, 260), (0, 0, 0, 0))
    t_im.alpha_composite(g)
    t_im.alpha_composite(lay)
    s_im = Image.new("RGBA", (W, 60), (0, 0, 0, 0))
    if sub:
        sd = ImageDraw.Draw(s_im)
        so = font(F_UI_M, 23)
        tr = 7
        widths = [sd.textlength(ch, font=so) for ch in sub]
        tw = sum(widths) + tr * (len(sub) - 1)
        x = W / 2 - tw / 2
        for ch, wd in zip(sub, widths):
            sd.text((x, 30), ch, font=so, fill=SUBC + (255,), anchor="lm")
            x += wd + tr
    _HC[k] = (t_im, s_im)
    return _HC[k]


def _alpha(im, a):
    if a >= 0.999:
        return im
    im = im.copy()
    im.putalpha(im.getchannel("A").point(lambda v: int(v * a)))
    return im


def head_entries(V, caps):
    """[(t, título, subtítulo)] a partir de V.HEAD {línea(.fracción): (título, sub)}."""
    out = []
    for key_, val in sorted(V.HEAD.items()):
        li = int(key_)
        fr = key_ - li
        c = caps[li]
        t0 = c["start"] + (c["end"] - c["start"]) * fr - (0.15 if fr == 0 else 0)
        out.append((max(0.0, t0), val[0], val[1] if len(val) > 1 else ""))
    return out


def draw_head(img, t, entries, fade_out_at=None):
    cur = None
    for i, (t0, ti, su) in enumerate(entries):
        if t >= t0:
            cur = i
    if cur is None:
        return
    k_all = 1.0 if fade_out_at is None else 1 - clamp((t - fade_out_at) / 0.35)
    if k_all <= 0:
        return
    t0, ti, su = entries[cur]
    u = t - t0
    # el anterior se va
    if cur > 0 and u < 0.32:
        _, pti, psu = entries[cur - 1]
        a = (1 - ease(u / 0.32)) * k_all
        pt, ps = _head_img(pti, psu)
        img.paste(_alpha(pt, a), (0, 180 - int(10 * (1 - a))), _alpha(pt, a))
        img.paste(_alpha(ps, a), (0, 322), _alpha(ps, a))
    ti_im, su_im = _head_img(ti, su)
    a1 = ease(clamp((u - 0.12) / 0.4)) * k_all if cur > 0 else ease(clamp(u / 0.6)) * k_all
    a2 = ease(clamp((u - 0.28) / 0.4)) * k_all if cur > 0 else ease(clamp((u - 0.2) / 0.6)) * k_all
    if a1 > 0:
        im = _alpha(ti_im, a1)
        img.paste(im, (0, 180 + int(16 * (1 - a1))), im)
    if a2 > 0 and su:
        im = _alpha(su_im, a2)
        img.paste(im, (0, 322 + int(10 * (1 - a2))), im)


def channel_label(img, txt="No lo sabías", k=1.0):
    d = ImageDraw.Draw(img, "RGBA")
    d.text((W / 2, 112), txt, font=font(F_UI, 30), fill=(150, 156, 176, int(255 * k)), anchor="mm")


# ------------------------------------------------------------------ subtítulos al ritmo de la voz
def word_times(caps):
    """Cada línea → [(palabra, destacada, t0, t1)]. Si la voz ya dio tiempos por palabra, se usan."""
    out = []
    for c in caps:
        if c.get("words"):
            out.append(c["words"])
            continue
        ws = parse_words(c["text"])
        wts = []
        for w, _ in ws:
            n = len(re.sub(r"[^\wáéíóúüñÁÉÍÓÚÜÑ]", "", w)) + 1.5
            if w.endswith((",", ":", ";")):
                n += 2.5
            if w.endswith(("…", ".", "?", "!")):
                n += 3.5
            wts.append(n)
        tot = sum(wts)
        t, span = c["start"], c["end"] - c["start"]
        line = []
        for (w, hl), n in zip(ws, wts):
            dt = span * n / tot
            line.append((w, hl, t, t + dt))
            t += dt
        out.append(line)
    return out


STOP = {"el", "la", "los", "las", "un", "una", "de", "del", "que", "en", "a", "al", "y", "o", "es", "se", "su", "por", "para",
        "con", "lo", "le", "más", "mas", "tan", "como", "sin", "ya", "muy"}


def make_chunks(caps, n=3):
    """Grupos de 1-3 palabras: [(t0, t1, [(palabra, destacada)])]; una palabra destacada larga va sola o en pareja."""
    chunks = []
    for line in word_times(caps):
        cur = []
        for i, (w, hl, a, b) in enumerate(line):
            cur.append((w, hl, a, b))
            nxt = line[i + 1] if i + 1 < len(line) else None
            bare = w.lower().strip("¿¡,.:;…?!")
            end_punct = w.endswith((",", ".", ":", ";", "…", "?", "!"))
            hl_break = nxt is not None and nxt[1] != hl and len(cur) >= 2
            if (len(cur) >= n and bare not in STOP) or len(cur) >= n + 1 or end_punct or hl_break:
                chunks.append(cur)
                cur = []
        if cur:
            chunks.append(cur)
    out = []
    for i, ch in enumerate(chunks):
        t0 = ch[0][2]
        t1 = ch[-1][3]
        nxt = chunks[i + 1][0][2] if i + 1 < len(chunks) else t1 + 0.4
        t1 = min(nxt, t1 + 0.35)
        out.append((t0, t1, [(w, hl) for w, hl, _, _ in ch]))
    return out


def draw_caption(img, t, chunks, y=1500):
    cur = None
    for c in chunks:
        if c[0] - 0.02 <= t < c[1]:
            cur = c
            break
    if not cur:
        return
    t0, t1, words = cur
    u = t - t0
    a = ease(clamp(u / 0.12)) * (1 - clamp((t - (t1 - 0.08)) / 0.08))
    if a <= 0:
        return
    fo = caps_font(60)
    d0 = ImageDraw.Draw(Image.new("RGBA", (4, 4)))
    sp = d0.textlength(" ", font=fo)
    words = [(w.replace("*", ""), hl) for w, hl in words]
    widths = [d0.textlength(w, font=fo) for w, _ in words]
    # en una o dos líneas
    lines = [[]]
    lw = 0
    for (w, hl), wd in zip(words, widths):
        if lines[-1] and lw + sp + wd > 900:
            lines.append([])
            lw = 0
        lines[-1].append((w, hl, wd))
        lw += wd + (sp if len(lines[-1]) > 1 else 0)
    lh = 74
    lay = Image.new("RGBA", (W, 220), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    yy = 110 - (len(lines) - 1) * lh / 2
    for ln in lines:
        tw = sum(x[2] for x in ln) + sp * (len(ln) - 1)
        x = W / 2 - tw / 2
        for w, hl, wd in ln:
            d.text((x, yy), w, font=fo, fill=(GOLD if hl else (248, 248, 250)) + (255,), anchor="lm")
            x += wd + sp
        yy += lh
    sh = lay.filter(ImageFilter.GaussianBlur(7))
    sh = Image.merge("RGBA", (*[Image.new("L", sh.size, 0)] * 3, sh.getchannel("A").point(lambda v: int(v * 0.75))))
    out = Image.new("RGBA", lay.size, (0, 0, 0, 0))
    out.alpha_composite(sh, (0, 4))
    out.alpha_composite(lay)
    out = _alpha(out, a)
    img.paste(out, (0, int(y - 110 + (1 - ease(clamp(u / 0.16))) * 8)), out)


# ------------------------------------------------------------------ tarjeta «Seguir» a mitad del vídeo
def follow_card(img, u, name="No lo sabías", tag="Curiosidades que no te esperas", cy=1180, D=3.1):
    if u < 0 or u > D:
        return
    k_in = ease(clamp(u / 0.4))
    k_out = 1 - ease(clamp((u - (D - 0.35)) / 0.35))
    k = k_in * k_out
    if k <= 0:
        return
    w, h = 820, 224
    lay = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle([20, 20, 20 + w, 20 + h], radius=26, fill=CARD + (238,), outline=(255, 255, 255, 40), width=2)
    # avatar con el logo del ojo
    ax, ay, ar = 20 + 112, 20 + h / 2, 72
    d.ellipse([ax - ar, ay - ar, ax + ar, ay + ar], fill=(16, 20, 38, 255), outline=GOLD + (255,), width=4)
    R.eye_icon(d, ax, ay, 96, (243, 240, 232), GOLD, (16, 20, 38))
    d.text((20 + 218, 20 + 64), name, font=font(F_UI_B, 46), fill=(255, 255, 255, 255), anchor="lm")
    d.text((20 + 218, 20 + 112), tag, font=font(F_UI_M, 25), fill=(180, 186, 204, 255), anchor="lm")
    ok = u > 1.55
    press = 1 - 0.08 * math.sin(clamp((u - 1.4) / 0.3) * math.pi)
    bw, bh = 300 * press, 70 * press
    bx, by = 20 + 218 + 150, 20 + 170
    d.rounded_rectangle([bx - bw / 2, by - bh / 2, bx + bw / 2, by + bh / 2], radius=14, fill=GOLD + (255,))
    txt = "Siguiendo ✓" if ok else "Seguir"
    fo = font(F_UI_B, 32)
    if ok:
        d.text((bx - 14, by + 1), "Siguiendo", font=fo, fill=(22, 24, 36, 255), anchor="mm")
        tw = d.textlength("Siguiendo", font=fo)
        cx = bx - 14 + tw / 2 + 22
        d.line([(cx - 11, by + 1), (cx - 3, by + 9), (cx + 12, by - 9)], fill=(22, 24, 36, 255), width=5, joint="curve")
    else:
        d.text((bx, by + 1), txt, font=fo, fill=(22, 24, 36, 255), anchor="mm")
    if 1.4 < u < 2.0:   # destello al pulsar
        q = (u - 1.4) / 0.6
        rr = 30 + 160 * q
        d.rounded_rectangle([bx - bw / 2 - rr * 0.3, by - bh / 2 - rr * 0.1, bx + bw / 2 + rr * 0.3, by + bh / 2 + rr * 0.1],
                            radius=18, outline=GOLD + (int(150 * (1 - q)),), width=4)
    sh = Image.new("RGBA", lay.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([20, 30, 20 + w, 30 + h], radius=26, fill=(0, 0, 0, 150))
    sh = sh.filter(ImageFilter.GaussianBlur(16))
    out = Image.new("RGBA", lay.size, (0, 0, 0, 0))
    out.alpha_composite(sh)
    out.alpha_composite(lay)
    sc = lerp(0.94, 1.0, k_in)
    if abs(sc - 1) > 1e-3:
        out = out.resize((int(out.size[0] * sc), int(out.size[1] * sc)), Image.BICUBIC)
    out = _alpha(out, k)
    img.paste(out, (int(W / 2 - out.size[0] / 2), int(cy - out.size[1] / 2 + (1 - k_in) * 30)), out)


# ------------------------------------------------------------------ tiempos a partir de la voz
def load_audio(path, sr=16000):
    with tempfile.TemporaryDirectory() as td:
        o = os.path.join(td, "a.wav")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", path, "-ac", "1", "-ar", str(sr), o], check=True)
        from scipy.io import wavfile
        _, x = wavfile.read(o)
    return x.astype(np.float32) / 32768, sr


def fit_voice(path, max_total=89.6, lead=0.5, tail=1.0):
    """Si la locución no cabe en 90 s, la acelera un poco (sin cambiar el tono, máx. +10 %). Devuelve la ruta a usar."""
    x, sr = load_audio(path)
    segs = speech_segments(x, sr)
    end = segs[-1][1] if segs else len(x) / sr
    need = (end + lead + tail) / max_total
    if need <= 1.0:
        return path, 1.0
    k = min(1.10, need)
    out = os.path.splitext(path)[0] + f"_x{k:.3f}.wav"
    if not os.path.exists(out) or os.path.getmtime(out) < os.path.getmtime(path):
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", path, "-af", f"atempo={k:.4f}", "-ar", "44100", out], check=True)
    return out, k


def _syl(txt):
    t = re.sub(r"[^a-záéíóúüñ0-9 ]", " ", txt.lower())
    n = len(re.findall(r"[aeiouáéíóúü]+", t))
    for num in re.findall(r"\d+", t):
        n += {1: 2, 2: 3, 3: 4}.get(len(num), 5)
    return max(1, n)


def speech_segments(x, sr, min_pause=0.16):
    hop = int(sr * 0.01)
    e = np.array([np.sqrt(np.mean(x[i:i + hop * 2] ** 2) + 1e-10) for i in range(0, len(x) - hop * 2, hop)])
    db = 20 * np.log10(e + 1e-9)
    ref = np.percentile(db, 95)
    th = max(ref - 32, np.percentile(db, 12) + 6)
    on = db > th
    # rellena huecos muy cortos (oclusivas) y quita chasquidos
    segs = []
    i = 0
    n = len(on)
    while i < n:
        if on[i]:
            j = i
            while j < n and on[j]:
                j += 1
            segs.append([i * 0.01, j * 0.01])
            i = j
        else:
            i += 1
    merged = []
    for s in segs:
        if merged and s[0] - merged[-1][1] < min_pause:
            merged[-1][1] = s[1]
        else:
            merged.append(s)
    return [s for s in merged if s[1] - s[0] > 0.06]


def align(path, lines):
    """Reparte las líneas del guion sobre la locución (pausas = cortes posibles). Devuelve
    [(t0, t1, [(palabra, destacada, w0, w1)])] en segundos del audio."""
    x, sr = load_audio(path)
    segs = speech_segments(x, sr)
    P = len(segs)
    L = len(lines)
    syl = [_syl(l.replace("*", "")) for l in lines]
    speech = sum(b - a for a, b in segs)
    rate = speech / sum(syl)
    INF = 1e18
    # dp[i][j]: líneas 0..i-1 usan segmentos 0..j-1
    dp = np.full((L + 1, P + 1), INF)
    bk = np.zeros((L + 1, P + 1), int)
    dp[0][0] = 0
    for i in range(1, L + 1):
        exp = syl[i - 1] * rate
        for j in range(i, P - (L - i) + 1):
            for k in range(i - 1, j):
                if dp[i - 1][k] >= INF:
                    continue
                act = sum(b - a for a, b in segs[k:j])
                cost = (math.log((act + 0.05) / (exp + 0.05))) ** 2
                gap = segs[j][0] - segs[j - 1][1] if j < P else 1.0
                cost -= 0.15 * min(gap, 0.8)        # mejor cortar en pausas largas
                v = dp[i - 1][k] + cost
                if v < dp[i][j]:
                    dp[i][j] = v
                    bk[i][j] = k
    out = []
    j = P
    groups = []
    for i in range(L, 0, -1):
        k = bk[i][j]
        groups.append((k, j))
        j = k
    groups.reverse()
    for li, (k, j) in enumerate(groups):
        sub = segs[k:j]
        ws = parse_words(lines[li])
        out.append((sub[0][0], sub[-1][1], _words_on(ws, sub)))
    return out


def _words_on(ws, sub):
    """Palabras de una línea repartidas sobre sus trozos de voz (las pausas internas caen en comas o «…»)."""
    syl = [_syl(w) for w, _ in ws]
    # cortes posibles: después de una palabra con puntuación
    cuts = [i + 1 for i, (w, _) in enumerate(ws[:-1]) if w.endswith((",", "…", ":", ";", ".", "?", "!"))]
    groups = [(0, len(ws))]
    if len(sub) > 1 and cuts:
        # asigna cada pausa interna (de más larga a más corta) al corte de texto más cercano en proporción
        tot = sum(b - a for a, b in sub)
        acc = 0
        pos = []
        for a, b in sub[:-1]:
            acc += b - a
            pos.append(acc / tot)
        cs = sum(syl)
        cut_pos = {c: sum(syl[:c]) / cs for c in cuts}
        used = {}
        for pi, p in enumerate(pos):
            best = min(cut_pos, key=lambda c: abs(cut_pos[c] - p))
            if abs(cut_pos[best] - p) < 0.22 and best not in used.values():
                used[pi] = best
        # trozos de voz agrupados según los cortes elegidos
        bounds = sorted(used.items())
        groups, spans = [], []
        w0, s0 = 0, 0
        for pi, c in bounds:
            groups.append((w0, c))
            spans.append((sub[s0][0], sub[pi][1]))
            w0, s0 = c, pi + 1
        groups.append((w0, len(ws)))
        spans.append((sub[s0][0], sub[-1][1]))
    else:
        spans = [(sub[0][0], sub[-1][1])]
    out = []
    for (a, b), (t0, t1) in zip(groups, spans):
        tot = sum(syl[a:b]) or 1
        t = t0
        for i in range(a, b):
            dt = (t1 - t0) * syl[i] / tot
            out.append((ws[i][0], ws[i][1], t, t + dt))
            t += dt
    return out


# ------------------------------------------------------------------ tiempos exactos por palabra (transcripción de ElevenLabs)
def _nw(w):
    w = w.lower().replace("*", "")
    return re.sub(r"[^\wáéíóúüñ]", "", w)


def align_words(words_path, lines, scale=1.0):
    """Como align(), pero con los tiempos de cada palabra que da la transcripción (words.json)."""
    import json, difflib
    d = json.load(open(words_path))
    tw = [dict(w, start=w["start"] * scale, end=w["end"] * scale) for w in (d["words"] if isinstance(d, dict) else d)
          if w.get("type", "word") == "word" and not w["text"].startswith("[")]
    T = [_nw(w["text"]) for w in tw]
    S, owner = [], []
    for li, line in enumerate(lines):
        for w, hl in parse_words(line):
            S.append((w, hl))
            owner.append(li)
    Sn = [_nw(w) for w, _ in S]
    times = [None] * len(S)
    sm = difflib.SequenceMatcher(None, Sn, T, autojunk=False)
    for op, a0, a1, b0, b1 in sm.get_opcodes():
        if op == "equal":
            for k in range(a1 - a0):
                times[a0 + k] = (tw[b0 + k]["start"], tw[b0 + k]["end"])
        elif op == "replace":
            t0, t1 = tw[b0]["start"], tw[b1 - 1]["end"]
            n = a1 - a0
            for k in range(n):
                times[a0 + k] = (t0 + (t1 - t0) * k / n, t0 + (t1 - t0) * (k + 1) / n)
    # palabras del guion que la voz no dijo: pegadas a la anterior
    last = 0.0
    for i in range(len(times)):
        if times[i] is None:
            times[i] = (last, last)
        last = times[i][1]
    out = []
    for li in range(len(lines)):
        idx = [i for i, o in enumerate(owner) if o == li]
        ws = [(S[i][0], S[i][1], times[i][0], times[i][1]) for i in idx]
        out.append((ws[0][2], ws[-1][3], ws))
    return out
