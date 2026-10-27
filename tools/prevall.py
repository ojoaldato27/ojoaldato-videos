import sys, time
sys.path.insert(0, "/home/claude/shorts-ingenieria/pipeline"); sys.path.insert(0, "/home/claude/shorts-ingenieria/content/cine")
import fast, cine
from PIL import Image
mod, out = sys.argv[1], sys.argv[2]
fr = float(sys.argv[3]) if len(sys.argv) > 3 else 0.7
t0 = time.time()
V, shots, caps, chunks, total = fast.setup(mod)
ts = [s["start"] + (s["end"] - s["start"]) * fr for s in shots] + [total - 1.5]
cols = 6
rows = (len(ts) + cols - 1) // cols
tw, th = 270, 480
sh = Image.new("RGB", (cols * (tw + 8) + 8, rows * (th + 8) + 8), (16, 16, 20))
for k, t in enumerate(ts):
    im = cine.frame(V, shots, chunks, total, int(t * fast.FPS))
    sh.paste(im.resize((tw, th), Image.LANCZOS), (8 + (k % cols) * (tw + 8), 8 + (k // cols) * (th + 8)))
sh.save(out, quality=88)
print("ok", round(total, 2), "s", len(shots), "planos", round(time.time() - t0, 1), "s")
