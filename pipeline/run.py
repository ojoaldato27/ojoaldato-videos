"""Pipeline completo para un guion: música -> render -> control de calidad -> metadatos -> registro.
Uso: python3 run.py ../content/scripts/001-viga-i.json"""
import csv, datetime, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from music import build_track  # noqa: E402
from render import render, W, H, FPS  # noqa: E402


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def loudness(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)
    return float(m[-1]) if m else None


def black_frames(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-vf", "blackdetect=d=0.1:pix_th=0.02",
                        "-an", "-f", "null", "-"], capture_output=True, text=True)
    return re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", r.stderr)


def silence(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", "silencedetect=n=-45dB:d=2",
                        "-vn", "-f", "null", "-"], capture_output=True, text=True)
    return re.findall(r"silence_start: ([\d.]+)", r.stderr)


def qc(script, mp4):
    issues, info = [], {}
    bl = black_frames(mp4)
    if bl:
        issues.append(f"fotogramas negros en {bl}")
    si = silence(mp4)
    if si:
        issues.append(f"silencio de más de 2 s en {si}")
    if not script.get("reviewed_by_human"):
        info["pendiente"] = "revisión humana del contenido"
    p = probe(mp4)
    v = [s for s in p["streams"] if s["codec_type"] == "video"][0]
    a = [s for s in p["streams"] if s["codec_type"] == "audio"]
    dur = float(p["format"]["duration"])
    info.update(width=v["width"], height=v["height"], fps=v["r_frame_rate"], duration=round(dur, 2))
    if (v["width"], v["height"]) != (W, H):
        issues.append(f"resolución {v['width']}x{v['height']} (esperado {W}x{H})")
    if v["r_frame_rate"] != f"{FPS}/1":
        issues.append(f"fps {v['r_frame_rate']}")
    if not a:
        issues.append("sin pista de audio")
    if not 10 <= dur <= 180:
        issues.append(f"duración {dur:.1f}s fuera de 10-180s (límite de Shorts)")
    lu = loudness(mp4)
    info["lufs"] = lu
    if lu is None or not -16.5 <= lu <= -11.5:
        issues.append(f"volumen {lu} LUFS (objetivo -14)")
    # subtítulos: dentro de la duración, sin solaparse, legibles
    caps = sorted(script["captions"], key=lambda c: c["start"])
    for i, c in enumerate(caps):
        n = len(c["text"].replace("*", ""))
        cps = n / (c["end"] - c["start"])
        if cps > 20:
            issues.append(f"subtítulo demasiado rápido ({cps:.0f} car/s): {c['text'][:30]}")
        if c["end"] > script["duration"] + 0.01:
            issues.append(f"subtítulo fuera del vídeo: {c['text'][:30]}")
        if i and c["start"] < caps[i - 1]["end"] - 0.01:
            issues.append(f"subtítulos solapados en {c['start']}s")
    if caps and caps[0]["start"] > 0.3:
        issues.append("el gancho no aparece en los primeros 0,3 s")
    # metadatos
    md = script["metadata"]
    if len(md["title"]) > 100:
        issues.append("título > 100 caracteres")
    if len(md["description"]) > 5000:
        issues.append("descripción > 5000 caracteres")
    # derechos: todos los recursos deben ser propios o con licencia declarada
    for r in script.get("rights", []):
        if r.get("license") not in ("propio", "CC0", "licencia comercial"):
            issues.append(f"recurso sin licencia clara: {r}")
    return issues, info


def _ts_srt(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def _ts_ass(t):
    cs = int(round(t * 100))
    return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"


def export_subs(s, out, sid):
    """Escribe los subtítulos en .srt (universal) y .ass (con estilo y palabras clave en amarillo)."""
    caps = sorted(s["captions"], key=lambda c: c["start"])
    with open(os.path.join(out, f"{sid}.srt"), "w", encoding="utf-8") as f:
        for i, c in enumerate(caps, 1):
            f.write(f"{i}\n{_ts_srt(c['start'])} --> {_ts_srt(c['end'])}\n{c['text'].replace('*', '')}\n\n")
    head = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 0\n\n"
            "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, "
            "Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
            "Alignment, MarginL, MarginR, MarginV, Encoding\n"
            "Style: Default,Inter Display Black,72,&H00EAF1F4,&H00EAF1F4,&H00000000,&H64000000,"
            "-1,0,0,0,100,100,0,0,1,6,0,5,90,90,0,1\n\n"
            "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
    with open(os.path.join(out, f"{sid}.ass"), "w", encoding="utf-8") as f:
        f.write(head)
        for c in caps:
            txt, on = "", False
            for ch in c["text"]:
                if ch == "*":
                    txt += "{\\c&H3FD2FF&}" if not on else "{\\c&HEAF1F4&}"
                    on = not on
                else:
                    txt += ch
            f.write(f"Dialogue: 0,{_ts_ass(c['start'])},{_ts_ass(c['end'])},Default,,0,0,0,,"
                    f"{{\\pos(540,1330)}}{txt}\n")


def main(script_path, clean=False):
    s = json.load(open(script_path))
    sid = s["id"]
    if clean:
        s["burn_captions"] = False
    out = os.path.join(ROOT, "output", sid)
    os.makedirs(out, exist_ok=True)
    wav = os.path.join(out, "musica.wav")
    mp4 = os.path.join(out, f"{sid}{'-sin-subtitulos' if clean else ''}.mp4")
    export_subs(s, out, sid)
    cues = [sc["start"] for sc in s["scenes"]]
    V3 = s.get("style") in ("viral", "doc", "mystery", "creative", "premium", "exp")
    sfx = []
    if s.get("style") and not V3:
        import styles
        for c in s["captions"]:
            for i, (cs, ce, g) in enumerate(styles.chunks_for(c["text"], c["start"], c["end"], n=s.get("chunk_n", 3))):
                sfx.append((cs, "ding" if any(h for _, h in g) else "pop"))
        for sc in s["scenes"]:
            pr = sc.get("params", {})
            if sc["type"] == "quiz":
                t0 = sc["start"] + pr.get("count_at", 1.2)
                sfx += [(t0 + k, "tick") for k in range(3)]
                sfx.append((t0 + 3.0, "correct" if pr.get("answer") else "wrong"))
            if sc["type"] == "top_card":
                sfx.append((sc["start"], "boom"))
    if s.get("style") == "fun":
        import music3
        music3.build_track3(s.get("music", "creative"), s["duration"], [tuple(x) for x in s.get("sfx", [])], [], wav,
                            seed=s.get("seed", 7))
    elif V3:
        import edit_v3, music3
        sfx3, duck = edit_v3.plan_audio(s)
        music3.build_track3(s["style"], s["duration"], sfx3, duck, wav, seed=s.get("seed", 7))
    else:
      sfx += [(nt["t"], "notif") for nt in s.get("notifs", [])]
      build_track(s["duration"], cues, wav, seed=s.get("seed", 7), bpm=s.get("bpm", 100), sfx=sfx, sfx_gain=s.get("sfx_gain", 1.0),
                music_gain=s.get("music_gain", 1.0))
    render(s, mp4, wav)
    issues, info = qc(s, mp4)
    # miniatura = fotograma del gancho
    thumb = os.path.join(out, "miniatura.jpg")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(s.get("thumb_time", 1.2)),
                    "-i", mp4, "-frames:v", "1", "-q:v", "2", thumb], check=True)
    md = s["metadata"]
    with open(os.path.join(out, "metadatos.txt"), "w") as f:
        f.write(f"TÍTULO:\n{md['title']}\n\nDESCRIPCIÓN:\n{md['description']}\n\n"
                f"ETIQUETAS:\n{', '.join(md['tags'])}\n\n"
                f"Contenido sintético alterado (IA realista): No\n"
                f"Apto para niños: No\n")
    estado = "listo para revisar" if not issues else "BLOQUEADO: no publicar"
    if issues:
        with open(os.path.join(ROOT, "errores.log"), "a") as f:
            f.write(f"{datetime.datetime.now().isoformat()} {sid}: {'; '.join(issues)}\n")
    report = {"id": sid, "ok": not issues, "estado": estado, "issues": issues, **info}
    json.dump(report, open(os.path.join(out, "qc.json"), "w"), indent=2, ensure_ascii=False)
    log = os.path.join(ROOT, "registro.csv")
    new = not os.path.exists(log)
    with open(log, "a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["fecha_render", "id", "titulo", "duracion_s", "lufs", "qc_ok", "estado",
                        "fecha_publicacion", "url", "vistas_48h", "retencion_media_%", "notas"])
        w.writerow([datetime.date.today().isoformat(), sid, md["title"], info["duration"],
                    info["lufs"], "sí" if not issues else "no", estado,
                    "", "", "", "", "; ".join(issues)])
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return report


if __name__ == "__main__":
    main(sys.argv[1], clean="--sin-subtitulos" in sys.argv)
