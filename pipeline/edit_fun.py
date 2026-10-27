"""Motor «fun»: vídeos alegres y no lineales.
Cada escena = un fondo de color + pegatinas que entran con rebote, mascota que reacciona,
opciones A/B/C que se resuelven al final, contadores, sellos y confeti. Cámara fija (sin zooms):
el dinamismo viene de lo que entra y sale, y de la transición deslizante entre escenas."""
import math, random, subprocess
from PIL import Image, ImageDraw
import render as R
from render import W, H, FPS, ease, lerp, mix, clamp
import fun_icons as FI
from fun_icons import INK, WHITE, YEL, pf
from styles import chunks_for, wrap
import edit_v2 as V2

BG = {"yellow": (255, 214, 92), "mint": (150, 228, 196), "pink": (255, 176, 196), "sky": (150, 205, 255),
      "lilac": (200, 178, 255), "orange": (255, 184, 112), "cream": (255, 243, 224), "navy": (44, 50, 98),
      "coral": (255, 140, 120), "lime": (200, 240, 120)}


def spring(x):
    if x <= 0:
        return 0.0
    return 1 - math.exp(-6 * x) * math.cos(11 * x)


def tween(item, key, ts, default):
    tw = item.get("tw", {}).get(key)
    if not tw:
        return item.get(key, default)
    t0, t1, v0, v1 = tw
    return lerp(v0, v1, ease(clamp((ts - t0) / max(1e-3, t1 - t0))))


def darker(c, k=0.08):
    return tuple(int(v * (1 - k)) for v in c)


def pattern(d, bgc, seed, ts):
    rng = random.Random(seed)
    col = darker(bgc, 0.07)
    for _ in range(26):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        y = (y - ts * rng.uniform(8, 20)) % H
        kind = rng.choice((0, 1, 2))
        s = rng.uniform(10, 26)
        if kind == 0:
            d.ellipse([x - s, y - s, x + s, y + s], outline=col, width=5)
        elif kind == 1:
            d.line([(x - s, y), (x + s, y)], fill=col, width=6)
            d.line([(x, y - s), (x, y + s)], fill=col, width=6)
        else:
            d.line([(x - s, y), (x - s / 2, y - s / 2), (x, y), (x + s / 2, y - s / 2), (x + s, y)], fill=col, width=5)


def pill_text(d, cx, cy, txt, size, fg=INK, bg=WHITE, k=1.0):
    f = pf(size)
    tw = d.textlength(txt, font=f)
    pad = size * 0.45
    box = [cx - tw / 2 - pad, cy - size * 0.72, cx + tw / 2 + pad, cy + size * 0.62]
    d.rounded_rectangle(box, radius=size * 0.6, fill=bg, outline=INK, width=max(3, int(size * 0.07)))
    d.text((cx - tw / 2, cy - size * 0.72), txt, font=f, fill=fg)


def stamp(d, cx, cy, txt, size, col, k):
    f = pf(size)
    tw = d.textlength(txt, font=f)
    lay = Image.new("RGBA", (int(tw + size * 1.6), int(size * 2.2)), (0, 0, 0, 0))
    dl = ImageDraw.Draw(lay)
    dl.rounded_rectangle([6, 6, lay.size[0] - 6, lay.size[1] - 6], radius=size * 0.3, outline=col, width=int(size * 0.12))
    dl.text((size * 0.8, size * 0.35), txt, font=f, fill=col)
    lay = lay.rotate(-12, expand=True, resample=Image.BICUBIC)
    sc = lerp(2.2, 1.0, ease(k))
    lay = lay.resize((max(1, int(lay.size[0] * sc)), max(1, int(lay.size[1] * sc))), Image.BICUBIC)
    a = lay.getchannel("A").point(lambda v: int(v * clamp(k * 2)))
    lay.putalpha(a)
    return lay, (int(cx - lay.size[0] / 2), int(cy - lay.size[1] / 2))


def draw_item(img, d, it, ts):
    at = it.get("at", 0.0)
    if ts < at:
        return
    k = spring((ts - at) / 0.55)
    if "out" in it and ts > it["out"]:
        k = max(0.0, 1 - ease((ts - it["out"]) / 0.25))
        if k <= 0:
            return
    x, y = tween(it, "x", ts, 540), tween(it, "y", ts, 800)
    if it.get("float", True):
        y += math.sin(ts * 2.2 + x * 0.01) * 7
    s = tween(it, "s", ts, 300) * k
    if s < 24:
        return
    if "icon" in it:
        opts = {kk: tween(it, kk, ts, v) for kk, v in it.get("opt", {}).items()}
        for kk in it.get("tw", {}):
            if kk not in ("x", "y", "s"):
                opts[kk] = tween(it, kk, ts, 0)
        FI.draw(it["icon"], d, x, y, s, ts, **opts)
    elif "mascot" in it:
        FI.mascot(d, x, y, s, ts, it["mascot"], bubble=it.get("bubble", True))
    elif "text" in it:
        size = it.get("size", 70) * k
        if it.get("pill", True):
            pill_text(d, x, y, it["text"], size, it.get("fg", INK), it.get("bg", WHITE))
        else:
            FI.text_c(d, x, y, it["text"], size, it.get("fg", INK))
    elif "count" in it:
        a, b = it["count"]
        q = ease(clamp((ts - at) / it.get("dur", 1.4)))
        v = lerp(a, b, q)
        txt = it.get("fmt", "{:.0f}").format(v).replace(",", ".")
        size = it.get("size", 150)
        f = pf(size)
        tw = d.textlength(txt, font=f)
        d.text((x - tw / 2 + 6, y - size * 0.62 + 8), txt, font=f, fill=INK)
        d.text((x - tw / 2, y - size * 0.62), txt, font=f, fill=it.get("fg", WHITE), stroke_width=int(size * 0.05), stroke_fill=INK)
        if it.get("sub"):
            FI.text_c(d, x, y + size * 0.62, it["sub"], size * 0.28, INK, False)
    elif "options" in it:
        rv = it.get("reveal")
        for i, op in enumerate(it["options"]):
            ki = spring((ts - at - i * 0.18) / 0.5)
            if ki <= 0:
                continue
            oy = y + i * 150
            ok = rv is not None and ts >= rv
            correct = i == it.get("correct", -1)
            bgc = (120, 220, 140) if ok and correct else ((225, 225, 230) if ok else WHITE)
            w = 820 * ki
            d.rounded_rectangle([x - w / 2, oy - 56, x + w / 2, oy + 56], radius=56, fill=bgc, outline=INK, width=6)
            if ki > 0.6:
                d.ellipse([x - w / 2 + 14, oy - 42, x - w / 2 + 98, oy + 42], fill=YEL, outline=INK, width=5)
                FI.text_c(d, x - w / 2 + 56, oy + 4, "ABC"[i], 50)
                f = pf(46)
                d.text((x - w / 2 + 125, oy - 30), op, font=f, fill=INK if not (ok and not correct) else (130, 130, 140))
                if ok:
                    (FI.check if correct else FI.cross)(d, x + w / 2 - 70, oy, 70, ts)
    elif "stamp" in it:
        lay, pos = stamp(d, x, y, it["stamp"], it.get("size", 90), it.get("col", (230, 50, 60)), clamp((ts - at) / 0.3))
        img.alpha_composite(lay, (max(0, pos[0]), max(0, pos[1])))


def confetti(d, ts, t0, seed=1):
    if ts < t0 or ts > t0 + 2.2:
        return
    rng = random.Random(seed)
    cols = [(255, 90, 120), (90, 160, 255), (255, 210, 63), (90, 210, 140), (190, 120, 255), (255, 150, 60)]
    u = ts - t0
    for _ in range(90):
        x0 = rng.uniform(0, W)
        vy = rng.uniform(500, 900)
        vx = rng.uniform(-120, 120)
        x = x0 + vx * u + math.sin(u * 6 + x0) * 20
        y = -40 + vy * u + 300 * u * u - rng.uniform(0, 300)
        if 0 < y < H:
            a = u * 8 + x0
            s = rng.uniform(10, 18)
            pts = [(x + s * math.cos(a), y + s * 0.5 * math.sin(a)), (x - s * math.sin(a) * 0.5, y + s * math.cos(a)),
                   (x - s * math.cos(a), y - s * 0.5 * math.sin(a)), (x + s * math.sin(a) * 0.5, y - s * math.cos(a))]
            d.polygon(pts, fill=rng.choice(cols))


def scene_frame(sc, ts, idx):
    p = sc["params"]
    bgc = BG.get(p.get("bg", "cream"), (255, 243, 224))
    img = Image.new("RGBA", (W, H), bgc + (255,))
    d = ImageDraw.Draw(img, "RGBA")
    pattern(d, bgc, idx * 7 + 3, ts)
    for it in p.get("items", []):
        draw_item(img, d, it, ts)
    if "confetti" in p:
        confetti(d, ts, p["confetti"], idx)
    return img


def cap(img, chunk, t_in, y=1580):
    d = ImageDraw.Draw(img)
    size = int(84 * lerp(0.85, 1.0, ease(t_in / 0.12)))
    f = pf(size)
    lines = wrap(d, chunk, f, 920)
    lh = int(size * 1.22)
    yy = y - len(lines) * lh / 2
    for ln in lines:
        widths = [d.textlength(w, font=f) for w, _ in ln]
        sp = d.textlength(" ", font=f)
        x = (W - (sum(widths) + sp * (len(ln) - 1))) / 2
        for (wd, hl), wdt in zip(ln, widths):
            if hl:
                d.rounded_rectangle([x - 14, yy - 6, x + wdt + 14, yy + size * 1.12], radius=20, fill=INK)
                d.text((x, yy), wd, font=f, fill=YEL)
            else:
                d.text((x, yy), wd, font=f, fill=WHITE, stroke_width=9, stroke_fill=INK)
            x += wdt + sp
        yy += lh


def question_bar(img, q, t):
    if not q or t < q["from"]:
        return
    d = ImageDraw.Draw(img)
    k = ease(clamp((t - q["from"]) / 0.4))
    solved = t >= q["reveal"]
    f = pf(36)
    txt = q["text"]
    tw = d.textlength(txt, font=f)
    x0 = (W - tw) / 2 - 40
    y0 = lerp(160, 210, k)
    bgc = (120, 220, 140) if solved else WHITE
    d.rounded_rectangle([x0 - 50, y0, x0 + tw + 80, y0 + 72], radius=36, fill=bgc, outline=INK, width=5)
    pulse = 1 + 0.12 * math.sin(t * 5) if not solved else 1
    r = 24 * pulse
    d.ellipse([x0 - 30, y0 + 36 - r, x0 - 30 + 2 * r, y0 + 36 + r], fill=YEL, outline=INK, width=4)
    FI.text_c(d, x0 - 30 + r, y0 + 38, "!" if solved else "?", 30)
    d.text((x0 + 30, y0 + 12), txt, font=f, fill=INK)


def norm(o):
    if isinstance(o, dict):
        return {k: norm(v) for k, v in o.items()}
    if isinstance(o, list):
        if len(o) in (3, 4) and all(isinstance(v, int) for v in o):
            return tuple(o)
        return [norm(v) for v in o]
    return o


def render_fun(script, out_mp4, audio_wav, only_times=None):
    scenes = [norm(sc) for sc in script["scenes"]]
    dur = script["duration"]
    n = int(dur * FPS)
    chunks = []
    for c in sorted(script["captions"], key=lambda c: c["start"]):
        chunks += chunks_for(c["text"], c["start"], c["end"], n=script.get("chunk_n", 3))
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-i", audio_wav, "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
           "-shortest", "-movflags", "+faststart", out_mp4]
    pipe = None if only_times else subprocess.Popen(cmd, stdin=subprocess.PIPE)
    frames = [int(x * FPS) for x in only_times] if only_times else range(n)
    shots = []
    TR = 0.42
    for i in frames:
        t = i / FPS
        si = next((k for k, sc in enumerate(scenes) if sc["start"] <= t < sc["end"]), len(scenes) - 1)
        sc = scenes[si]
        ts = t - sc["start"]
        cur = scene_frame(sc, ts, si)
        if si > 0 and ts < TR:
            prev = scenes[si - 1]
            pf_ = scene_frame(prev, t - prev["start"], si - 1)
            k = spring(ts / TR * 0.9)
            k = min(1.06, k)
            off = int(W * (1 - k))
            frame = Image.new("RGBA", (W, H), BG.get(sc["params"].get("bg", "cream"), (255, 243, 224)) + (255,))
            frame.paste(pf_, (off - W, 0))
            frame.paste(cur, (off, 0))
            cur = frame
        img = cur
        question_bar(img, script.get("question"), t)
        img = img.convert("RGB")
        for cs, ce, g in chunks:
            if cs <= t < ce:
                cap(img, V2.glue(g), t - cs)
        d = ImageDraw.Draw(img)
        bgc = BG.get(sc["params"].get("bg", "cream"), (255, 243, 224))
        ink = WHITE if sum(bgc) < 300 else INK
        R.eye_icon(d, 92, 112, 60, ink, YEL, (14, 15, 18))
        d.text((134, 94), script.get("watermark", ""), font=pf(30), fill=ink)
        for nt in script.get("notifs", []):
            img = V2.notif_banner(img, t - nt["t"], nt["title"], nt["body"])
        d = ImageDraw.Draw(img)
        d.rectangle([0, H - 14, W, H], fill=darker((255, 255, 255), 0.15))
        d.rectangle([0, H - 14, W * (t / dur), H], fill=ink if ink == INK else YEL)
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
