"""Fondos según el tema (Iker, 29/10: «el blanco es muy soso, hazlo acorde al tema; el del microondas, una cocina»).
Colores suaves para que el dibujo de delante y los subtítulos se lean bien. Zona de subtítulos (y 1480-1680) siempre clara.
Uso en un módulo:  import fondos;  FONDO = fondos.cocina();  y al final  fondos.instalar(globals()).
"""
import math
from PIL import Image, ImageDraw, ImageFilter
from flat3 import W, H

INK = (28, 28, 32)
_C = {}


def _soft(img, r=1.2):
    return img.filter(ImageFilter.GaussianBlur(r))


def cocina():
    if "cocina" in _C:
        return _C["cocina"]
    img = Image.new("RGB", (W, H), (250, 244, 234))
    d = ImageDraw.Draw(img, "RGBA")
    for r, y in enumerate(range(330, 1180, 56)):
        off = 0 if r % 2 == 0 else 56
        for x in range(-112 + off, W + 112, 112):
            d.rounded_rectangle([x + 3, y + 3, x + 109, y + 53], radius=8, fill=(246, 241, 232), outline=(226, 218, 204), width=2)
    d.rectangle([0, 0, W, 300], fill=(196, 214, 198))
    for x in (0, 270, 540, 810):
        d.rounded_rectangle([x + 14, 14, x + 256, 286], radius=14, fill=(206, 222, 208), outline=(160, 182, 164), width=4)
        d.rounded_rectangle([x + 116, 230, x + 154, 244], radius=6, fill=(230, 200, 120))
    d.rectangle([0, 300, W, 330], fill=(170, 190, 172))
    d.rounded_rectangle([830, 420, 1060, 760], radius=10, fill=(214, 236, 250), outline=(180, 160, 130), width=10)
    d.line([(945, 420), (945, 760)], fill=(180, 160, 130), width=8)
    d.line([(830, 590), (1060, 590)], fill=(180, 160, 130), width=8)
    d.ellipse([990, 460, 1040, 510], fill=(255, 236, 160))
    d.rectangle([20, 600, 230, 616], fill=(196, 160, 120))
    for i, (h, col) in enumerate([(80, (240, 200, 160)), (110, (210, 230, 210)), (70, (250, 214, 214))]):
        x = 40 + i * 64
        d.rounded_rectangle([x, 600 - h, x + 52, 600], radius=10, fill=col + (230,), outline=(190, 180, 170), width=3)
        d.rectangle([x + 6, 600 - h - 14, x + 46, 600 - h], fill=(190, 160, 120))
    d.line([(260, 400), (560, 400)], fill=(170, 150, 130), width=6)
    for i, x in enumerate((300, 380, 460, 530)):
        d.line([(x, 400), (x, 470)], fill=(160, 160, 170), width=6)
        if i % 2:
            d.ellipse([x - 22, 466, x + 22, 510], outline=(160, 160, 170), width=6)
        else:
            d.rounded_rectangle([x - 18, 466, x + 18, 520], radius=8, fill=(190, 190, 200))
    d.rectangle([0, 1180, W, 1240], fill=(214, 178, 132))
    d.line([(0, 1180), (W, 1180)], fill=(170, 130, 90), width=5)
    d.rectangle([0, 1240, W, H], fill=(214, 228, 216))
    for x in (0, 360, 720):
        d.rounded_rectangle([x + 16, 1260, x + 344, 1460], radius=14, fill=(222, 234, 224), outline=(176, 196, 180), width=4)
        d.rounded_rectangle([x + 150, 1300, x + 210, 1314], radius=6, fill=(230, 200, 120))
        d.rounded_rectangle([x + 16, 1700, x + 344, 1900], radius=14, fill=(222, 234, 224), outline=(176, 196, 180), width=4)
    d.rounded_rectangle([20, 1480, W - 20, 1680], radius=30, fill=(250, 248, 242, 235))
    img = _soft(img)
    _C["cocina"] = img
    return img


def congreso():
    if "congreso" in _C:
        return _C["congreso"]
    img = Image.new("RGB", (W, H), (246, 238, 226))
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, 0, W, 300], fill=(232, 218, 196))
    for k in range(9):
        x = k * 135
        d.line([(x, 0), (x + 60, 300)], fill=(214, 196, 168), width=4)
    d.rectangle([0, 290, W, 316], fill=(206, 170, 90))
    for x in (60, 1020):
        d.rectangle([x - 34, 316, x + 34, 1180], fill=(240, 232, 218), outline=(214, 200, 178), width=4)
        for j in range(4):
            d.line([(x - 18 + j * 12, 330), (x - 18 + j * 12, 1170)], fill=(226, 214, 196), width=3)
        d.rectangle([x - 46, 316, x + 46, 346], fill=(226, 210, 184))
    for side in (-1, 1):
        x0 = 0 if side < 0 else W
        pts = [(x0, 300), (x0 + side * 260, 300), (x0 + side * 120, 560), (x0, 760)]
        d.polygon(pts, fill=(176, 40, 46))
        for j in range(4):
            d.line([(x0 + side * (40 + j * 50), 300), (x0 + side * (20 + j * 26), 600 - j * 60)], fill=(150, 30, 36), width=6)
        d.ellipse([x0 + side * 110 - 18, 540, x0 + side * 110 + 18, 576], fill=(220, 180, 80))
    d.ellipse([480, 100, 600, 220], fill=(230, 200, 120), outline=(190, 150, 70), width=6)
    d.ellipse([510, 130, 570, 190], fill=(244, 228, 190))
    d.rectangle([0, 1180, W, 1250], fill=(196, 140, 92))
    d.line([(0, 1180), (W, 1180)], fill=(150, 100, 60), width=5)
    d.rectangle([0, 1250, W, H], fill=(214, 120, 110))
    for y in range(1270, H, 70):
        d.line([(0, y), (W, y)], fill=(200, 108, 98), width=4)
    d.rounded_rectangle([20, 1480, W - 20, 1680], radius=30, fill=(250, 246, 240, 240))
    img = _soft(img)
    _C["congreso"] = img
    return img


def instalar(g):
    """Envuelve cada plano para que pinte el fondo antes del dibujo y cambia el recorte para que respete el fondo."""
    fondo = g["FONDO"]

    def con_fondo(fn):
        def run(img, t, T, L):
            img.paste(fondo, (0, 0))
            fn(img, t, T, L)
        return run

    g["FNS"] = {n: con_fondo(f) for n, f in g["FNS"].items()}

    def _clip(img, y1=1151):
        img.paste(fondo.crop((0, 0, W, 330)), (0, 0))
        img.paste(fondo.crop((0, 1480, W, H)), (0, 1480))
    g["_clip"] = _clip
