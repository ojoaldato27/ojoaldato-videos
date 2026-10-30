"""Voz más natural a partir de Kokoro (Iker, 30/10: «muy artificial, entonación británica, pausas mal»).
1. Solo voz española de Kokoro (sin mezclas con voces inglesas) y fonemas de español.
2. Lee FRASE A FRASE; los «…» y «:» se leen como coma dentro de la frase.
3. Entonación española con WORLD (pyworld): suaviza picos «a la inglesa», línea de declinación,
   final de afirmación → baja; pregunta → sube.
4. Pausas de persona entre frases y sonido cálido. Como cada frase se genera aparte, los tiempos
   por palabra salen exactos por frase (y repartidos por longitud dentro de ella).
Uso: python3 tools/voz_natural.py <modulo>        → VOICE del módulo (.mp3) + _words.json
     python3 tools/voz_natural.py --texto "<t>" <salida.mp3>
Variables: VOZ_ID (em_alex), VOZ_SPEED (1.0), VOZ_RANGO (0.9)
"""
import re, sys, os, json, subprocess, importlib
import numpy as np
import soundfile as sf
import pyworld as pw

ROOT = "/home/claude/shorts-ingenieria"
sys.path[:0] = [ROOT + "/content/cine", ROOT + "/pipeline"]
KOK = "/home/claude/tts"
_K = None
FS = 24000


def kokoro():
    global _K
    if _K is None:
        from kokoro_onnx import Kokoro
        _K = Kokoro(f"{KOK}/kokoro-v1.0.onnx", f"{KOK}/voices-v1.0.bin")
    return _K


def frases(t):
    t = re.sub(r"\s+", " ", t.strip())
    fr = [s.strip() for s in re.findall(r"[^.?!]+[.?!]+|[^.?!]+$", t) if s.strip()]
    out = []
    for s in fr:                       # las frases muy cortas solas suenan a inglés
        if out and len(s.split()) <= 3:
            out[-1] = out[-1] + " " + s
        else:
            out.append(s)
    return out


FON = {"Percy Spencer": "Persi Spénser", "km/h": "kilómetros por hora", "F1": "Fórmula 1", "%": " por ciento", "wifi": "güifi"}


def numeros(s):
    from num2words import num2words
    def n(m):
        x = m.group(0).replace(".", "")
        if "," in x:
            a, b = x.split(",")
            return num2words(int(a), lang="es") + " coma " + num2words(int(b), lang="es")
        return num2words(int(x), lang="es")
    return re.sub(r"\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d+(?:,\d+)?", n, s)


def para_leer(s):
    for a, b in FON.items():
        s = s.replace(a, b)
    s = numeros(s)
    s = s.replace("…", ",").replace(":", ",").replace(";", ",")
    s = re.sub(r",\s*,", ",", s)
    s = re.sub(r"[«»\"*]", "", s)
    return s


def entonacion(x, fs, tipo, suav=0.12):
    rango = float(os.environ.get("VOZ_RANGO", "0.9"))
    x = x.astype(np.float64)
    f0, t = pw.harvest(x, fs, f0_floor=60, f0_ceil=280, frame_period=5.0)
    f0 = pw.stonemask(x, f0, t, fs)
    sp = pw.cheaptrick(x, f0, t, fs)
    ap = pw.d4c(x, f0, t, fs)
    v = f0 > 0
    if v.sum() < 10:
        return x.astype(np.float32)
    lf = np.log2(np.where(v, f0, np.nan))
    idx = np.arange(len(lf))
    lfi = np.interp(idx, idx[v], lf[v])
    w = max(3, int(suav / 0.005))
    ker = np.hanning(w); ker /= ker.sum()
    sm = np.convolve(np.pad(lfi, w, mode="edge"), ker, "same")[w:-w]
    vi = idx[v]
    a, b = vi[0], vi[-1]
    med = np.median(lf[v])
    dec = med + (1.5 / 12) - (3.5 / 12) * np.clip((idx - a) / max(1, b - a), 0, 1)
    new = dec + rango * (sm - np.convolve(np.pad(sm, 80, mode="edge"), np.ones(161) / 161, "same")[80:-80])
    n_end = int(0.45 / 0.005)
    ramp = np.clip((idx - (b - n_end)) / n_end, 0, 1)
    if tipo == "?":
        new += (6.5 / 12) * ramp ** 1.5
    elif tipo == "!":
        new += (1.5 / 12) * np.sin(np.pi * ramp) - (2.0 / 12) * ramp ** 2
    else:
        new -= (3.0 / 12) * ramp ** 1.3
    f0n = np.where(v, 2 ** new, 0.0)
    y = pw.synthesize(f0n, sp, ap, fs, frame_period=5.0)
    return y.astype(np.float32)


def recorta(a, fs, db=40):
    import librosa
    iv = librosa.effects.split(a, top_db=db)
    return a[iv[0][0]: iv[-1][1]] if len(iv) else a


def spoken_len(w):
    w = w.strip("¿¡.,…:;!?«»\"()*")
    return sum(3.2 if c.isdigit() else 1 for c in w) + 1.5


def genera(texto, out, voz=None, vel=None, lang="es"):
    voz = voz or os.environ.get("VOZ_ID", "em_alex")
    vel = vel or float(os.environ.get("VOZ_SPEED", "1.0"))
    k = kokoro()
    st = k.get_voice_style(voz)
    partes, words, t = [np.zeros(int(FS * 0.12), np.float32)], [], 0.12
    for s in frases(texto):
        tipo = s[-1] if s[-1] in "?!." else "."
        a, fs = k.create(para_leer(s), voice=st, speed=vel, lang=lang)
        a = entonacion(recorta(a, fs), fs, tipo)
        dur = len(a) / FS
        toks = s.replace("*", "").split()
        L = [spoken_len(w) for w in toks]
        tot, acc = sum(L), 0.0
        for w, l in zip(toks, L):
            ws = t + dur * acc / tot
            acc += l
            words.append({"text": w, "type": "word", "start": round(ws, 3), "end": round(t + dur * acc / tot, 3)})
        partes.append(a)
        gap = {"?": 0.42, "!": 0.35}.get(tipo, 0.3)
        partes.append(np.zeros(int(FS * gap), np.float32))
        t += dur + gap
    y = np.concatenate(partes)
    wav = out[:-4] + ".wav"
    sf.write(wav, y, FS)
    af = ("highpass=f=75,lowpass=f=11000,equalizer=f=160:t=q:w=1:g=2,equalizer=f=3000:t=q:w=1.4:g=-1.5,"
          "acompressor=threshold=-22dB:ratio=2:attack=10:release=150,loudnorm=I=-16:TP=-1.5")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", wav, "-af", af, "-b:a", "160k", out], check=True)
    os.remove(wav)
    json.dump({"words": words, "source": "kokoro+voz_natural"}, open(out[:-4] + "_words.json", "w"), ensure_ascii=False, indent=0)
    print(out, len(words), "palabras · fin", words[-1]["end"])
    return out


if __name__ == "__main__":
    if sys.argv[1] == "--texto":
        genera(sys.argv[2], sys.argv[3])
    else:
        m = importlib.import_module(sys.argv[1])
        genera(" ".join(m.LINES) + " " + m.OUTRO_LINE, m.VOICE)
