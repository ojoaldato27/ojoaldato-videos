"""Marca «Ojo al dato» (@ojoaldato), 21/10: foto de perfil (Ojo sin traje, fondo rojo) y banner de YouTube."""
from PIL import Image, ImageDraw, ImageFont
import ojo_viejo as OV
from ojo_viejo import N, K, R, WH, BGP, IX, IB, OUT
import ojo_trajes as T, ojo_trajes2 as T2, ojo_cient as C

IS = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"


def pen_fig(pose, pre=None, post=None, look=(0.06, 0.0)):
    p = N.Pen()
    if pre:
        pre(p)
    N._pose(p, pose, 0.0, look, 0.0)
    if post:
        post(p)
    return p.im                                   # 2000 × 2400 (unidades × 2)


def crop_units(im, box):
    s = N.SS
    return im.crop(tuple(int(v * s) for v in box))


# ------------------------------------------------------------------ foto de perfil
pf = Image.new("RGB", (1080, 1080), R)
f = crop_units(pen_fig("wave", look=(0.07, -0.02)), (90, 40, 910, 860)).resize((1080, 1080), Image.LANCZOS)
pf.paste(f, (0, 60), f)
pf.save(OUT + "OJO_perfil_1080.png")
m = Image.new("L", (1080, 1080), 0)
ImageDraw.Draw(m).ellipse([0, 0, 1079, 1079], fill=255)
prev = Image.new("RGB", (1080, 1080), (16, 16, 20))
prev.paste(pf, (0, 0), m)
prev.save(OUT + "OJO_perfil_circulo.png")

# ------------------------------------------------------------------ banner de YouTube (2560 × 1440; zona segura 1546 × 423 en el centro)
bw, bh = 2560, 1440
bn = Image.new("RGB", (bw, bh), BGP)
d = ImageDraw.Draw(bn)
d.rectangle([0, bh - 60, bw, bh], fill=R)
sx0, sy0, sx1, sy1 = 507, 508, 2053, 931
main = pen_fig("wave").resize((330, 396), Image.LANCZOS)
bn.paste(main, (sx0 + 30, sy0 + 20), main)
fo = ImageFont.truetype(IX, 170)
t = "Ojo al dato"
tx = sx0 + 420
d.text((tx, 690), t, font=fo, fill=K, anchor="lm")
tw = d.textlength(t, font=fo)
d.ellipse([tx + tw + 14, 690 + 40, tx + tw + 54, 690 + 80], fill=R)
d.text((tx + 6, 820), "Curiosidades que no te esperas, cada día", font=ImageFont.truetype(IS, 50), fill=(120, 120, 128), anchor="lm")
d.rectangle([tx + 6, 880, tx + 170, 890], fill=R)
# fuera de la zona segura (solo se ve en ordenador y tele): Ojo con los trajes de cada tema
extras = [(T2.piloto_pre, None, "flag"), (lambda p: coat(p), None, "wave") if False else (T.coat, lambda p: (T.bow(p), T.flask(p, 330, 640)), "wave"),
          (T2.astronauta_pre, T2.astronauta_post, "wave"), (T2.romano_pre, T2.romano_post, "point")]
xs = [2120, 2330, 120, 330]
for (pre, post, pose), x in zip(extras, xs):
    im = pen_fig(pose, pre, post).resize((220, 264), Image.LANCZOS)
    bn.paste(im, (x - 30, 600), im)
bn.save(OUT + "OJO_banner_youtube.png")
# vista previa con las zonas
pv = bn.resize((1280, 720), Image.LANCZOS)
pd = ImageDraw.Draw(pv)
pd.rectangle([sx0 / 2, sy0 / 2, sx1 / 2, sy1 / 2], outline=(60, 160, 255), width=3)
pd.text((sx0 / 2 + 8, sy0 / 2 - 22), "zona que se ve en el móvil", font=ImageFont.truetype(IB, 18), fill=(60, 160, 255))
pv.save(OUT + "OJO_banner_preview.png")
print("ok")
