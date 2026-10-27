import sys
sys.path.insert(0, "/home/claude/shorts-ingenieria/pipeline"); sys.path.insert(0, "/home/claude/shorts-ingenieria/content/cine")
import fast, cine
mod, shot, dt, out = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
V, shots, caps, chunks, total = fast.setup(mod)
s = next(x for x in shots if x["name"] == shot)
im = cine.frame(V, shots, [], total, int((s["start"] + dt) * fast.FPS))
im.convert("RGB").save(out, quality=92); print("ok", out)
