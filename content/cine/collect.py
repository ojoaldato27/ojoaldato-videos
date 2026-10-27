"""Revisa cada vídeo terminado (qc.py), corrige el volumen si se sale de -14 LUFS y lo copia numerado a la entrega.
Se puede lanzar varias veces: salta los que ya están copiados y los que aún no existen."""
import os, sys, json, shutil, subprocess, re, time

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = "/home/claude/shorts-ingenieria/output/cine"
DEST = "/home/claude/entrega16"
SINCE = time.mktime(time.strptime("2026-10-13 10:50", "%Y-%m-%d %H:%M"))

ORDER = ["t12_brawn", "t01_velocidad", "v00_titanic", "t02_microondas", "v01_krakatoa", "t08_gps", "v08_emus",
         "t10_palomitas", "v03_monalisa", "t05_airbag", "v02_lustig", "t06_nevera", "v09_cleopatra", "t04_qr",
         "v06_tunguska", "t07_induccion", "v07_kola", "t09_bateria", "v10_voyager", "t03_tactil", "v04_hachiko", "v05_apolo"]


def title(mod):
    m = re.search(r'^TITLE\s*=\s*"([^"]+)"', open(os.path.join(HERE, mod + ".py")).read(), re.M)
    return m.group(1)


def src(mod):
    if mod == "t01_velocidad":
        return "/home/claude/pruebas/coche_prueba2.mp4", 0
    return os.path.join(OUT, title(mod) + ".mp4"), SINCE


VOZ = "/home/claude/tts/voz_video.py"   # la voz del canal ("CANAL"): cada vídeo sale también con voz en off


USAR_VOZ = False   # 14-oct: Iker dice que la voz CANAL suena robótica; sin voz hasta que apruebe una


def con_voz(mod, dst):
    """Copia con la voz del canal al lado del vídeo (mismo nombre + _CON_VOZ), con su .srt."""
    if not USAR_VOZ or mod == "t01_velocidad":
        return None
    out = dst.replace(".mp4", "_CON_VOZ.mp4")
    r = subprocess.run([sys.executable, VOZ, mod, dst, out], capture_output=True, text=True)
    if r.returncode != 0:
        print("voz fallo", mod, r.stderr[-400:], flush=True)
        return None
    shutil.copy2(dst.replace(".mp4", ".srt"), out.replace(".mp4", ".srt"))
    return out


def qc(p):
    r = subprocess.run([sys.executable, os.path.join(HERE, "qc.py"), p], capture_output=True, text=True)
    return json.loads(r.stdout.strip().splitlines()[-1])


os.makedirs(DEST, exist_ok=True)
log_p = os.path.join(DEST, "_qc.json")
log = json.load(open(log_p)) if os.path.exists(log_p) else {}
for n, mod in enumerate(ORDER, 1):
    name = f"{n:02d}_{title(mod)}"
    p, since = src(mod)
    if not os.path.exists(p) or os.path.getmtime(p) < since or not os.path.exists(p.replace(".mp4", ".srt")):
        continue
    if name in log and log[name].get("src_mtime") == os.path.getmtime(p):
        continue
    if time.time() - os.path.getmtime(p) < 20:
        continue
    dst = os.path.join(DEST, name + ".mp4")
    shutil.copy2(p, dst)
    shutil.copy2(p.replace(".mp4", ".srt"), dst.replace(".mp4", ".srt"))
    r = qc(dst)
    if r["LUFS"] is not None and abs(r["LUFS"] + 14) >= 1.0:
        subprocess.run([os.path.join(HERE, "fixlufs.sh"), dst, str(r["LUFS"])], check=True)
        r = qc(dst)
    shutil.move(r["sheet"], os.path.join(OUT, name + "_qc.jpg"))
    r["sheet"] = os.path.join(OUT, name + "_qc.jpg")
    r["src_mtime"] = os.path.getmtime(p)
    v = con_voz(mod, dst)
    if v:
        rv = qc(v)
        os.remove(rv["sheet"])
        r["voz"] = {"dur": rv["dur"], "LUFS": rv["LUFS"], "OK": rv["OK"]}
    log[name] = r
    json.dump(log, open(log_p, "w"), ensure_ascii=False, indent=1)
    print(name, r["dur"], r["LUFS"], "OK" if r["OK"] else "REVISAR", r["black"], flush=True)
print("listos:", sum(1 for v in log.values() if v.get("OK")), "/", len(ORDER))
