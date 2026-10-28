"""Tiempos por palabra SIN ElevenLabs (cuando la transcripción da 429).
Usa las pausas de la voz (ffmpeg silencedetect) y las encaja con la puntuación del guion;
dentro de cada tramo reparte las palabras por su longitud hablada.
Uso: python3 tools/align_local.py <modulo_en_content/cine> [voz.mp3]  → escribe <voz>_words.json
"""
import sys, os, re, json, subprocess, importlib

ROOT = "/home/claude/shorts-ingenieria"
sys.path[:0] = [ROOT + "/content/cine", ROOT + "/pipeline"]


def spoken_len(w):
    w = w.strip("¿¡.,…:;!?«»\"()")
    n = 0
    for ch in w:
        n += 3.2 if ch.isdigit() else 1
    return max(n, 1.5) + 1.2


def silences(mp3):
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", mp3, "-af", "silencedetect=noise=-38dB:d=0.12", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", out)]
    en = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", out)]
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp3],
                               capture_output=True, text=True).stdout)
    return list(zip(st, en)), dur


def align(text, mp3):
    toks = text.split()
    sil, dur = silences(mp3)
    # habla real: desde el final del silencio inicial hasta el inicio del final
    t0 = 0.0
    if sil and sil[0][0] < 0.05:
        t0 = sil[0][1]
        sil = sil[1:]
    t1 = dur
    if sil and sil[-1][1] > dur - 0.05:
        t1 = sil[-1][0]
        sil = sil[:-1]
    w = [spoken_len(t) for t in toks]
    cum = [0]
    for x in w:
        cum.append(cum[-1] + x)
    tot = cum[-1]
    punct = [i for i, t in enumerate(toks[:-1]) if re.search(r"[.,…:;!?»]$", t)]
    speech = (t1 - t0) - sum(b - a for a, b in sil)
    # posición esperada (en tiempo de habla) del final de cada token candidato
    exp_pos = {i: cum[i + 1] / tot for i in punct}
    sil_pos = []
    acc = 0.0
    prev = t0
    for a, b in sil:
        acc += a - prev
        sil_pos.append(acc / speech)
        prev = b
    S, P = len(sil), len(punct)
    INF = 1e18
    # DP: cada silencio se asigna a una puntuación distinta, en orden; puntuación sin silencio permitida
    dp = [[INF] * (P + 1) for _ in range(S + 1)]
    bk = [[None] * (P + 1) for _ in range(S + 1)]
    for j in range(P + 1):
        dp[0][j] = 0.0
    for s in range(1, S + 1):
        for j in range(1, P + 1):
            best, arg = dp[s][j - 1], ("skip",)
            c = dp[s - 1][j - 1] + (sil_pos[s - 1] - exp_pos[punct[j - 1]]) ** 2 * 400
            if c < best:
                best, arg = c, ("take",)
            dp[s][j], bk[s][j] = best, arg
    # silencios que no encajan (p. ej. pausas internas) → se ignoran si no hay solución
    assign = {}
    s, j = S, P
    if dp[S][P] >= INF:
        raise SystemExit("no se pudo alinear")
    while s > 0 and j > 0:
        if bk[s][j][0] == "take":
            assign[punct[j - 1]] = sil[s - 1]
            s -= 1
        j -= 1
    # tramos
    bounds = [(-1, None)] + sorted(assign.items()) + [(len(toks) - 1, None)]
    words = []
    cur = t0
    for k in range(len(bounds) - 1):
        a = bounds[k][0] + 1
        b = bounds[k + 1][0]
        end_t = bounds[k + 1][1][0] if bounds[k + 1][1] else t1
        seg = toks[a:b + 1]
        ww = w[a:b + 1]
        span = end_t - cur
        s_tot = sum(ww)
        t = cur
        for tok, x in zip(seg, ww):
            d = span * x / s_tot
            words.append({"text": tok, "type": "word", "start": round(t, 3), "end": round(t + d * 0.92, 3)})
            t += d
        cur = bounds[k + 1][1][1] if bounds[k + 1][1] else t1
    return words, len(assign), S


if __name__ == "__main__":
    mod = importlib.import_module(sys.argv[1])
    mp3 = sys.argv[2] if len(sys.argv) > 2 else mod.VOICE
    text = " ".join(l.replace("*", "") for l in mod.LINES) + " " + mod.OUTRO_LINE
    words, used, S = align(text, mp3)
    out = os.path.splitext(mp3)[0] + "_words.json"
    json.dump({"words": words, "source": "align_local"}, open(out, "w"), ensure_ascii=False, indent=0)
    print(out, len(words), "palabras;", used, "de", S, "pausas encajadas; fin", words[-1]["end"])
