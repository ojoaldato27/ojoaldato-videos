"""Control de calidad de los mp4 renderizados: duración, formato, volumen, fotogramas negros y hoja de fotogramas."""
import sys, subprocess, json, re, os
from PIL import Image

out_dir = "/home/claude/shorts-ingenieria/output/cine"


def probe(p):
    j = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", p],
                                  capture_output=True, text=True).stdout)
    v = next(s for s in j["streams"] if s["codec_type"] == "video")
    a = next((s for s in j["streams"] if s["codec_type"] == "audio"), None)
    return float(j["format"]["duration"]), v["width"], v["height"], v["r_frame_rate"], a is not None, int(j["format"]["size"])


def loud(p):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", p, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", r)
    return float(m[-1]) if m else None


def black(p):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", p, "-vf", "blackdetect=d=0.4:pix_th=0.06", "-an", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    return re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", r)


def sheet(p, n=8):
    dur = probe(p)[0]
    ims = []
    for k in range(n):
        t = dur * (k + 0.5) / n
        tmp = f"/tmp/qc_{k}.png"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t), "-i", p, "-frames:v", "1", "-vf", "scale=216:384", tmp])
        ims.append(Image.open(tmp).convert("RGB"))
    out = Image.new("RGB", (216 * n, 384))
    for i, im in enumerate(ims):
        out.paste(im, (i * 216, 0))
    sp = p.replace(".mp4", "_qc.jpg")
    out.save(sp)
    return sp


if __name__ == "__main__":
    for p in sys.argv[1:]:
        d, w, h, fr, aud, size = probe(p)
        res = {"file": os.path.basename(p), "dur": round(d, 1), "res": f"{w}x{h}", "fps": fr, "audio": aud,
               "MB": round(size / 1e6, 1), "LUFS": loud(p), "black": black(p), "srt": os.path.exists(p.replace(".mp4", ".srt"))}
        ok = 60 <= d <= 90 and (w, h) == (1080, 1920) and fr in ("30/1", "60/1") and aud and res["LUFS"] is not None and abs(res["LUFS"] + 14) < 1.5 \
            and not res["black"] and res["srt"] and size < 30e6
        res["OK"] = ok
        res["sheet"] = sheet(p)
        print(json.dumps(res, ensure_ascii=False))
