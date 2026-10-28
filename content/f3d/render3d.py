"""Render del vídeo 3D «El rebufo en F1» (three.js en Chromium headless → ffmpeg).
Uso:
  python3 render3d.py preview <salida.jpg>   hoja de fotogramas (sin voz: tiempos estimados)
  python3 render3d.py full <salida.mp4>      vídeo completo con voz (voz/f3d_rebufo.mp3 + _words.json), música y efectos
"""
import sys, os, json, re, base64, subprocess, threading, http.server, functools, difflib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = "/home/claude/shorts-ingenieria"
VOZ = os.path.join(ROOT, "content/cine/voz/f3d_rebufo")
FPS = 30

LINES = [
    "¿Por qué en la F1 los coches van tan *pegados* al de delante?",
    "Un F1 a más de *300 km/h* va empujando una pared de aire.",
    "Y ese aire frena muchísimo: a esa velocidad, casi toda la potencia se gasta en *apartarlo*.",
    "Pero detrás del coche queda un hueco de aire revuelto. Eso es el *rebufo*.",
    "Si te metes justo ahí… el aire ya *no te frena* tanto. Es como ir en bici justo detrás de otro ciclista.",
    "Con menos resistencia ganas velocidad sin tocar nada: unos *10 km/h* más al final de la recta.",
    "Y en la frenada… sales del rebufo en el último momento, te pones a su lado y lo *adelantas*.",
    "Pero tiene trampa: en las curvas, ese aire sucio te quita *carga aerodinámica*.",
    "El coche se agarra peor, las ruedas se *calientan*… y cuesta seguirle.",
    "Y desde *2026*, si vas a menos de un segundo, tienes un extra de *energía eléctrica* para atacar.",
    "Así que… ¿por qué van tan pegados? Porque detrás del otro, el aire te *regala velocidad*.",
]
OUTRO_LINE = "La próxima vez que veas dos coches en fila, ya sabes qué están cazando… ¡Ojo al dato!"
OUTRO_HOLD = 3.0


def script_text():
    return " ".join(l.replace("*", "") for l in LINES) + " " + OUTRO_LINE


def tokens_of(line):
    out = []
    for m in re.finditer(r"\*([^*]+)\*|(\S+)", line):
        if m.group(1):
            for w in m.group(1).split():
                out.append({"w": w, "key": True})
        else:
            out.append({"w": m.group(2), "key": False})
    # puntuación pegada a una clave («*rebufo*.») → se une a la palabra anterior
    fixed = []
    for tk in out:
        if fixed and re.fullmatch(r"[.,…:;!?]+", tk["w"]):
            fixed[-1]["w"] += tk["w"]
        else:
            fixed.append(tk)
    return fixed


def norm(w):
    return re.sub(r"[^\wáéíóúñü]", "", w.lower())


def timing():
    lines = [tokens_of(l) for l in LINES] + [tokens_of(OUTRO_LINE)]
    flat = [tk for ln in lines for tk in ln]
    wj = VOZ + "_words.json"
    if os.path.exists(wj):
        words = [w for w in json.load(open(wj))["words"] if w.get("type", "word") == "word"]
        a = [norm(tk["w"]) for tk in flat]
        b = [norm(w["text"]) for w in words]
        sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
        times = [None] * len(flat)
        for blk in sm.get_matching_blocks():
            for k in range(blk.size):
                times[blk.a + k] = (words[blk.b + k]["start"], words[blk.b + k]["end"])
        # huecos: interpolar
        for i in range(len(flat)):
            if times[i] is None:
                j = i - 1
                while j >= 0 and times[j] is None:
                    j -= 1
                k = i + 1
                while k < len(flat) and times[k] is None:
                    k += 1
                s0 = times[j][1] if j >= 0 else 0.0
                s1 = times[k][0] if k < len(flat) else s0 + 0.4 * (k - j)
                f = (i - j) / (k - j)
                st = s0 + (s1 - s0) * f
                times[i] = (st, st + 0.25)
        voice_end = words[-1]["end"]
    else:
        t, times = 0.25, []
        for ln in lines:
            for tk in ln:
                d = 0.11 + 0.055 * len(tk["w"])
                times.append((t, t + d * 0.9))
                t += d + (0.28 if re.search(r"[.…?!]$", tk["w"]) else 0.1 if re.search(r"[,:;]$", tk["w"]) else 0)
            t += 0.15
        voice_end = t
    i = 0
    L = []
    for ln in lines:
        toks = []
        for tk in ln:
            s, e = times[i]
            toks.append({"w": tk["w"], "key": tk["key"], "s": round(s, 3), "e": round(e, 3)})
            i += 1
        L.append({"start": toks[0]["s"] if L else 0.0, "end": toks[-1]["e"], "tokens": toks})
    for k in range(1, len(L)):
        L[k]["start"] = max(L[k - 1]["start"] + 0.8, L[k]["tokens"][0]["s"] - 0.12)
    total = voice_end + OUTRO_HOLD
    return {"lines": L[:-1], "outro": L[-1], "total": round(total, 3), "notif": round(total * 0.5, 2)}


def serve():
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=HERE)
    h.log_message = lambda *a, **k: None
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), h)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def open_page(p, T):
    srv = serve()
    b = p.chromium.launch(args=["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
    pg = b.new_page(viewport={"width": 720, "height": 1280})
    pg.on("pageerror", lambda e: print("JS:", e))
    pg.goto(f"http://127.0.0.1:{srv.server_address[1]}/index.html")
    pg.wait_for_function("window.READY === true", timeout=60000)
    pg.evaluate("document.fonts.ready")
    pg.evaluate(f"window.TIMING = {json.dumps(T)}")
    pg.wait_for_timeout(400)
    return b, pg


def frame(pg, t):
    d = pg.evaluate(f"renderAt({t:.4f})")
    return base64.b64decode(d.split(",", 1)[1])


def preview(outp):
    from playwright.sync_api import sync_playwright
    from PIL import Image
    import io
    T = timing()
    ts = []
    for L in T["lines"]:
        ts.append(L["start"] + 0.35 * (L["end"] - L["start"]) + 0.3)
    ts.append(T["outro"]["start"] + 1.5)
    with sync_playwright() as p:
        b, pg = open_page(p, T)
        ims = [Image.open(io.BytesIO(frame(pg, t))).convert("RGB") for t in ts]
        b.close()
    cols, sc = 6, 0.42
    w, h = int(720 * sc), int(1280 * sc)
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w + (cols + 1) * 10, rows * h + (rows + 1) * 10), "#d8d8d8")
    for i, im in enumerate(ims):
        sheet.paste(im.resize((w, h), Image.LANCZOS), (10 + (i % cols) * (w + 10), 10 + (i // cols) * (h + 10)))
    sheet.save(outp, quality=90)
    print(outp, "duración estimada", T["total"])


def audio(T, outwav):
    sys.path[:0] = [ROOT + "/pipeline"]
    import cine, music3 as M
    import scipy.io.wavfile as wf
    sr = M.SR
    n = int((T["total"] + 0.5) * sr)
    rng = np.random.default_rng(5)
    mus = cine.music_bed("playful", T["total"] + 1, rng)[:n]
    mus = np.pad(mus, (0, max(0, n - len(mus))))
    mus = mus / (np.max(np.abs(mus)) + 1e-9) * 0.5 * 1.7
    fx = np.zeros(n)
    cuts = [L["start"] for L in T["lines"][1:]] + [T["outro"]["start"]]
    for i, c in enumerate(cuts):
        M.add(fx, cine.fx("whoosh" if i % 2 == 0 else "whoosh_up", rng), max(0, c - 0.25), 0.07)
    for L in T["lines"] + [T["outro"]]:
        for tk in L["tokens"]:
            if tk["key"]:
                M.add(fx, cine.fx("pop", rng), tk["s"], 0.05)
    M.add(fx, M.fx_notif(), T["notif"] + 0.05, 0.22)
    M.add(fx, cine.fx("ding", rng), T["outro"]["start"] + 0.3, 0.07)
    # voz
    tmp = outwav + ".voz.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", VOZ + ".mp3", "-ac", "1", "-ar", str(sr), tmp], check=True)
    _, v = wf.read(tmp)
    v = v.astype(np.float64) / 32768.0
    voz = np.zeros(n)
    voz[:min(n, len(v))] = v[:n]
    env = np.convolve(np.abs(voz), np.ones(int(0.25 * sr)) / int(0.25 * sr), mode="same")
    duck = 1 - 0.45 * np.clip(env / (env.max() + 1e-9) * 4, 0, 1)
    mix = voz * 1.0 + mus * duck * 0.55 + fx
    fade = int(1.2 * sr)
    mix[-fade:] *= np.linspace(1, 0, fade)
    mix = mix / (np.max(np.abs(mix)) + 1e-9) * 0.95
    wf.write(outwav, sr, (mix * 32767).astype(np.int16))
    os.remove(tmp)


def full(outp):
    from playwright.sync_api import sync_playwright
    T = timing()
    wav = outp + ".wav"
    audio(T, wav)
    nfr = int(T["total"] * FPS)
    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "image2pipe", "-c:v", "mjpeg", "-framerate", str(FPS), "-i", "-",
                           "-i", wav, "-vf", "scale=1080:1920:flags=lanczos", "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
                           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", outp],
                          stdin=subprocess.PIPE)
    with sync_playwright() as p:
        b, pg = open_page(p, T)
        for i in range(nfr):
            ff.stdin.write(frame(pg, i / FPS))
            if i % 300 == 0:
                print("frame", i, "/", nfr, flush=True)
        b.close()
    ff.stdin.close(); ff.wait()
    os.remove(wav)
    print(outp, T["total"], "s")


if __name__ == "__main__":
    {"preview": preview, "full": full}[sys.argv[1]](sys.argv[2])
