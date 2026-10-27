"""La mascota de siempre (el stickman del narrador, pipeline/narrator.py) con el ojo nuevo del logo 21:
almendra blanca, iris rojo, pupila negra con brillo. Colores del estilo 7: líneas negras sobre blanco y acento rojo. 21/10."""
import sys
sys.path.insert(0, "/home/claude/shorts-ingenieria/pipeline")
from PIL import Image, ImageDraw, ImageFont
import narrator as N

K, R, WH, BGP = (22, 22, 26), (230, 40, 40), (255, 255, 255), (248, 248, 246)
N.INK, N.BG, N.YEL = K, WH, R
N.Pen.stroke.__defaults__ = (26, K)
N.Pen.curve.__defaults__ = (26, K, 20)
N.Pen.dot.__defaults__ = (K,)
N.sparkle.__defaults__ = (R,)
IX = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"
IB = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
OUT = "/home/claude/shorts-ingenieria/marca/"
SS = N.SS


def eye_head(p, cx, cy, s, look=(0, 0), open_k=1.0, lid=0.0, brow=None, iris_r=0.19):
    top, bot = N.almond(cx, cy, s, open_k)
    Wd, Hd = p.im.size
    mask = Image.new("L", (Wd, Hd), 0)
    ImageDraw.Draw(mask).polygon(p.P(top + bot[::-1]), fill=255)
    lay = Image.new("RGBA", (Wd, Hd), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    ld.polygon(p.P(top + bot[::-1]), fill=WH + (255,))
    ix, iy, r = cx + look[0] * s, cy + look[1] * s, s * iris_r
    ld.ellipse([(ix - r) * SS, (iy - r) * SS, (ix + r) * SS, (iy + r) * SS], fill=R + (255,))
    rp = r * 0.5
    ld.ellipse([(ix - rp) * SS, (iy - rp) * SS, (ix + rp) * SS, (iy + rp) * SS], fill=K + (255,))
    ld.ellipse([(ix - r * 0.55) * SS, (iy - r * 0.6) * SS, (ix - r * 0.12) * SS, (iy - r * 0.18) * SS], fill=WH + (255,))
    if lid > 0:
        y_l = cy - s * 0.21 * open_k + lid * s * 0.42 * open_k
        ld.rectangle([0, 0, Wd, y_l * SS], fill=WH + (255,))
    clip = Image.new("RGBA", (Wd, Hd), (0, 0, 0, 0))
    clip.paste(lay, (0, 0), mask)
    p.paste(clip)
    w = s * 0.05
    p.stroke(top, w)
    p.stroke(bot, w)
    if 0 < lid < 0.98:
        y_l = cy - s * 0.21 * open_k + lid * s * 0.42 * open_k
        xs = [x for x, y in top if y <= y_l + 1]
        if xs:
            p.curve((min(xs) + 6, y_l + 2), (cx, y_l + 10), (max(xs) - 6, y_l + 2), w * 0.9)
    if brow:
        tilt, hgt = brow
        y0 = cy - s * 0.21 * open_k - hgt
        p.curve((cx - s * 0.30, y0 + tilt), (cx, y0 - 24), (cx + s * 0.30, y0 - tilt), w * 1.1)


N.eye_head = eye_head


def fig(pose, lid=0.0, look=(0.06, 0.0), talk=0.0):
    p = N.Pen()
    N._pose(p, pose, lid, look, talk)
    return p.im.resize((N.W0 // 2, N.H0 // 2), Image.LANCZOS)


POSES = [("Hola", "wave", {}), ("Señala", "point", {}), ("Pensando", "think", {}), ("¡Sorpresa!", "surprise", {}),
         ("Pícaro", "smirk", {}), ("Con bandera", "flag", {}), ("Adiós", "bye", {"talk": 0.5})]
if __name__ == "__main__":
    tiles = []
    for nm, ps, kw in POSES:
        im = Image.new("RGB", (500, 600), BGP)
        f = fig(ps, **kw)
        im.paste(f, (0, 0), f)
        im.save(OUT + f"ojo_viejo_{ps}.png")
        tiles.append((nm, im))
    # foto de perfil
    pf = Image.new("RGB", (600, 600), BGP)
    f = fig("wave").resize((560, 672), Image.LANCZOS).crop((0, 60, 560, 470))
    pf.paste(f, (30, 40), f)
    d = ImageDraw.Draw(pf)
    fo = ImageFont.truetype(IX, 66)
    t = "Ojo al dato"
    wdt = d.textlength(t, font=fo)
    d.rectangle([0, 450, 600, 600], fill=BGP)
    d.text((290, 520), t, font=fo, fill=K, anchor="mm")
    d.ellipse([290 + wdt / 2 + 6, 530, 290 + wdt / 2 + 20, 544], fill=R)
    pf.save(OUT + "ojo_viejo_perfil.png")
    sheet = Image.new("RGB", (4 * 330 + 50, 2 * 460 + 30), (16, 16, 20))
    dd = ImageDraw.Draw(sheet)
    for i, (nm, im) in enumerate(tiles + [("Foto de perfil", pf)]):
        x, y = 10 + (i % 4) * 340, 10 + (i // 4) * 470
        dd.text((x + 4, y + 22), nm, font=ImageFont.truetype(IB, 28), fill=(255, 255, 255), anchor="lm")
        if nm == "Foto de perfil":
            m = Image.new("L", (330, 330), 0)
            ImageDraw.Draw(m).ellipse([0, 0, 329, 329], fill=255)
            sheet.paste(im.resize((330, 330), Image.LANCZOS), (x, y + 60), m)
        else:
            sheet.paste(im.resize((330, 396), Image.LANCZOS), (x, y + 46))
    sheet.save(OUT + "ojo_viejo_poses.jpg", quality=92)
    print("ok")
