"""Render de una escena three.js (content/f3d/<v>.js) a mp4 o a fotogramas sueltos.
Uso: python3 r3d.py <v> <salida.mp4> <dur> [fps]   |   python3 r3d.py <v> --frames t1,t2,... <salida.jpg>"""
import sys, os, base64, subprocess, threading, http.server, functools, io, time
from playwright.sync_api import sync_playwright
HERE = "/home/claude/shorts-ingenieria/content/f3d"

def serve():
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=HERE)
    h.log_message = lambda *a, **k: None
    s = http.server.ThreadingHTTPServer(("127.0.0.1", 0), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s

def run(v, cb):
    srv = serve()
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
        pg = b.new_page(viewport={"width": 720, "height": 1280})
        pg.on("pageerror", lambda e: print("JS:", e))
        pg.on("console", lambda m: print("console:", m.text) if m.type == "error" else None)
        pg.goto(f"http://127.0.0.1:{srv.server_address[1]}/index.html?v={v}")
        pg.wait_for_function("window.READY === true", timeout=120000)
        cb(lambda t: base64.b64decode(pg.evaluate(f"renderAt({t:.4f})").split(",", 1)[1]))
        b.close()

if __name__ == "__main__":
    v = sys.argv[1]
    if sys.argv[2] == "--frames":
        from PIL import Image
        ts = [float(x) for x in sys.argv[3].split(",")]
        out = sys.argv[4]
        ims = []
        def cb(fr):
            for t in ts:
                ims.append(Image.open(io.BytesIO(fr(t))).convert("RGB").resize((240, 427)))
        t0 = time.time(); run(v, cb)
        sheet = Image.new("RGB", (240 * len(ims), 427))
        for i, im in enumerate(ims): sheet.paste(im, (240 * i, 0))
        sheet.save(out); print("ok", round(time.time() - t0, 1), "s")
    else:
        out, dur = sys.argv[2], float(sys.argv[3]); fps = int(sys.argv[4]) if len(sys.argv) > 4 else 30
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", str(fps), "-c:v", "mjpeg", "-i", "-",
               "-vf", "scale=1080:1920:flags=lanczos", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", out]
        pp = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        t0 = time.time()
        def cb(fr):
            n = int(dur * fps)
            for i in range(n):
                pp.stdin.write(fr(i / fps))
        run(v, cb); pp.stdin.close(); pp.wait(); print("ok", out, round(time.time() - t0, 1), "s")
