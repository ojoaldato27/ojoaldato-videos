"""Render rápido de prueba: reparte los fotogramas entre 2 procesos y luego une vídeo y audio.
Uso: python3 fast.py <modulo> [salida.mp4]"""
import sys, os, importlib, subprocess, time
from multiprocessing import Process

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "pipeline"))
sys.path.insert(0, HERE)
import cine
from styles import chunks_for

FPS, W, H = cine.FPS, cine.W, cine.H


def setup(mod):
    global FPS
    V = importlib.import_module(mod)
    if getattr(V, "FPS", None):          # p. ej. 60 fps en el estilo «pop» (movimiento más fluido)
        FPS = cine.FPS = V.FPS
    shots, caps, total = cine.timeline(V)
    cine.CAPS_[0] = caps
    chunks = []
    if cine.is_docu(V):
        import docu
        chunks = docu.make_chunks(caps)
    else:
        for c in caps:
            chunks += chunks_for(c["text"], c["start"], c["end"], n=3)
    return V, shots, caps, chunks, total


def part(mod, i0, i1, path):
    V, shots, caps, chunks, total = setup(mod)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p", path]
    pipe = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(i0, i1):
        pipe.stdin.write(cine.frame(V, shots, chunks, total, i).tobytes())
    pipe.stdin.close()
    pipe.wait()


if __name__ == "__main__":
    mod = sys.argv[1]
    V, shots, caps, chunks, total = setup(mod)
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join("/home/claude/shorts-ingenieria/output/cine", V.TITLE + ".mp4")
    tmp = out.replace(".mp4", "")
    t0 = time.time()
    n = int(total * FPS)
    mid = n // 2
    ps = [Process(target=part, args=(mod, 0, mid, tmp + "_a.mp4")), Process(target=part, args=(mod, mid, n, tmp + "_b.mp4"))]
    for p in ps:
        p.start()
    wav = tmp + ".wav"
    cine.build_audio(V, shots, total, wav, chunks=None if cine.is_docu(V) else chunks)
    for p in ps:
        p.join()
    with open(tmp + "_list.txt", "w") as fh:
        fh.write(f"file '{tmp}_a.mp4'\nfile '{tmp}_b.mp4'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", tmp + "_list.txt", "-i", wav,
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-shortest",
                    "-movflags", "+faststart", out], check=True)

    def ts(x):
        ms = int(round(x * 1000))
        return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
    with open(out.replace(".mp4", ".srt"), "w") as fh:
        for k, c in enumerate(caps, 1):
            fh.write(f"{k}\n{ts(c['start'])} --> {ts(c['end'])}\n{c['text'].replace('*', '')}\n\n")
    for f_ in (tmp + "_a.mp4", tmp + "_b.mp4", tmp + "_list.txt", wav):
        os.remove(f_)
    print("ok", out, round(time.time() - t0), "s")
