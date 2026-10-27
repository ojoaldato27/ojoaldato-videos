"""Ojo, la mascota de «Ojo al dato» (@ojoaldato.ya; YouTube @ojoaldatoya): el stickman de siempre con el ojo del logo
(almendra blanca, iris rojo, pupila negra). Se viste según el tema del vídeo (pedido por Iker el 21/10: «uno estándar
para el perfil y que en cada vídeo salga con la temática»). Solo ropa y sombreros: nada en las manos, para que valga
en todas las poses.
figure(pose, traje, lid, look, talk) → RGBA 500×600 (cacheado). Poses: wave, point, think, surprise, smirk, flag, bye."""
from PIL import Image
import ojo_viejo as OV
from ojo_viejo import N, K, R, WH
import ojo_trajes as T
import ojo_trajes2 as T2
import ojo_cient as C

SS = N.SS
_C = {}


def _hat_reportero(p):
    p.poly([(300, 235), (700, 235), (690, 255), (310, 255)], K + (255,))
    p.poly([(370, 240), (630, 240), (600, 150), (400, 150)], (60, 64, 80, 255))


def _hat_detective(p):
    p.poly([(300, 235), (700, 235), (690, 255), (310, 255)], (110, 80, 50, 255))
    p.poly([(370, 240), (630, 240), (600, 140), (400, 140)], (130, 95, 60, 255))
    p.stroke([(370, 240), (400, 140), (600, 140), (630, 240)], 8)
    p.stroke([(372, 215), (628, 215)], 14, K)


def _hat_obra(p):
    p.d.chord([330 * SS, 120 * SS, 670 * SS, 380 * SS], 180, 360, fill=T2.YEL, outline=K, width=int(9 * SS))
    p.stroke([(310, 250), (690, 250)], 18, T2.YEL)
    p.stroke([(310, 250), (690, 250)], 6)
    p.stroke([(500, 125), (500, 245)], 12, (230, 180, 30))


def _hat_mago(p):
    p.poly([(330, 250), (670, 250), (520, 0), (500, -10)], T2.PUR + (255,))
    p.stroke([(330, 250), (505, -10), (670, 250)], 9)
    p.stroke([(320, 252), (680, 252)], 22, T2.PUR)
    p.stroke([(320, 252), (680, 252)], 6)
    for (x, y, r) in ((470, 130, 18), (540, 70, 14), (560, 190, 16)):
        N.sparkle(p, x, y, r, T2.YEL)


from PIL import ImageFont
_FB = "/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf"


HELM, HELM2, SUIT, SUIT2, VISOR = (255, 204, 40), (30, 70, 170), (28, 58, 140), (255, 255, 255), (24, 28, 38)


SUITS = {   # monos de piloto para elegir (21/10): color base, rayas, banda del pecho, puños/cuello
    "azul": dict(base=(28, 58, 140), stripe=(255, 255, 255), stripe2=HELM, band=None, cuff=HELM),
    "blanco": dict(base=(245, 245, 248), stripe=HELM2, stripe2=HELM, band=(HELM2, HELM), cuff=HELM2),
    "amarillo": dict(base=HELM, stripe=HELM2, stripe2=(255, 255, 255), band=None, cuff=HELM2, shoulders=HELM2),
    "negro": dict(base=(30, 30, 36), stripe=HELM, stripe2=HELM, band=None, cuff=HELM),
}
SUIT_SEL = ["azul"]


def _helmet(p):
    p.d.ellipse([282 * SS, 112 * SS, 718 * SS, 512 * SS], fill=HELM, outline=K, width=int(10 * SS))
    p.d.chord([300 * SS, 330 * SS, 700 * SS, 512 * SS], 25, 155, fill=HELM2)
    p.d.rounded_rectangle([290 * SS, 244 * SS, 710 * SS, 416 * SS], radius=84 * SS, fill=VISOR)
    p.stroke([(410, 120), (380, 236)], 24, HELM2)
    p.stroke([(590, 120), (620, 236)], 24, HELM2)
    p.stroke([(500, 106), (500, 236)], 14, (255, 255, 255))


PROP = [None]                                   # objeto en la mano: None, "volante", "trofeo", "champan"
_FS = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"


def _patch(p, x, y, w, h, txt, bgc=(255, 255, 255), fg=(28, 58, 140)):
    p.d.rounded_rectangle([(x - w / 2) * SS, (y - h / 2) * SS, (x + w / 2) * SS, (y + h / 2) * SS], radius=5 * SS, fill=bgc,
                          outline=K, width=int(3 * SS))
    if txt:
        p.d.text((x * SS, y * SS), txt, font=ImageFont.truetype(_FB, int(h * 0.62 * SS)), fill=fg, anchor="mm")


def _piloto_pre(p):
    """Piloto de F1 (3.ª versión, 21/10: «el traje no parece de piloto»): mono ajustado de una pieza con collarín HANS,
    hombreras, cremallera, cinturón ancho y parches de patrocinadores por todas partes; casco amarillo aprobado."""
    S_ = SUITS[SUIT_SEL[0]]
    base = S_["base"]
    torso = [(392, 448), (608, 448), (622, 525), (578, 655), (590, 770), (410, 770), (422, 655), (378, 525)]
    p.poly(torso, base + (255,))
    p.stroke(torso + [torso[0]], 9)
    p.stroke([(392, 470), (430, 470)], 26, K)                     # hombreras (asas de rescate)
    p.stroke([(570, 470), (608, 470)], 26, K)
    p.stroke([(500, 455), (500, 760)], 6, (90, 100, 130))         # cremallera
    p.d.rectangle([418 * SS, 650 * SS, 582 * SS, 684 * SS], fill=(20, 20, 26))     # cinturón ancho
    p.d.rounded_rectangle([484 * SS, 652 * SS, 516 * SS, 682 * SS], radius=4 * SS, fill=(190, 194, 204))
    _patch(p, 445, 530, 70, 30, "OJO", (255, 255, 255), (220, 30, 40))
    _patch(p, 555, 530, 70, 30, "GP", HELM, (28, 58, 140))
    _patch(p, 500, 600, 120, 34, "AL DATO", (255, 255, 255), (28, 58, 140))
    _patch(p, 450, 730, 50, 24, "7", (230, 40, 40), (255, 255, 255))
    _patch(p, 550, 730, 60, 24, "F1", (255, 255, 255), (20, 20, 26))
    # collarín HANS detrás del casco, apoyado en los hombros
    p.d.rounded_rectangle([372 * SS, 420 * SS, 628 * SS, 480 * SS], radius=26 * SS, fill=(30, 30, 36), outline=K, width=int(6 * SS))
    _helmet(p)


def _piloto_post(p):
    p.d.rounded_rectangle([290 * SS, 244 * SS, 710 * SS, 416 * SS], radius=84 * SS, outline=K, width=int(10 * SS))
    p.d.arc([300 * SS, 248 * SS, 560 * SS, 332 * SS], 190, 260, fill=(210, 230, 255), width=int(8 * SS))
    p.d.rounded_rectangle([696 * SS, 300 * SS, 736 * SS, 360 * SS], radius=10 * SS, fill=(60, 60, 70), outline=K, width=int(5 * SS))
    for x in (455, 485, 515, 545):
        p.dot(x, 450, 7, (20, 20, 26))


def _gear_body(glove=(255, 255, 255), boot=(20, 20, 26)):
    """Brazos y piernas con guantes y botas (en lugar de la mano y el pie del stickman)."""
    def body(p, neck, hip, arms, legs, w=26):
        p.stroke([neck, hip], w)
        for a in arms:
            p.stroke(a, w)
            x, y = a[-1]
            p.d.ellipse([(x - 30) * SS, (y - 30) * SS, (x + 30) * SS, (y + 30) * SS], fill=glove, outline=K, width=int(7 * SS))
        for l in legs:
            p.stroke(l, w)
            x, y = l[-1]
            dirx = 1 if x >= hip[0] else -1
            p.d.rounded_rectangle([min(x, x + 70 * dirx) * SS - 8 * SS, (y - 26) * SS, max(x, x + 70 * dirx) * SS + 8 * SS, (y + 12) * SS],
                                  radius=14 * SS, fill=boot)
    return body


def _suit_body(p, neck, hip, arms, legs, w=26):
    S_ = SUITS[SUIT_SEL[0]]
    base = S_["base"]
    ww = w * 2.2
    for seg in arms + legs:
        p.stroke(seg, ww + 10, K)
    for seg in arms + legs:
        p.stroke(seg, ww, base)
    for seg in legs:
        p.stroke(seg, 8, S_["stripe"])
    for seg in arms:                                              # parche en cada brazo
        (x0, y0), (x1, y1) = seg[0], seg[1]
        _patch(p, x0 + (x1 - x0) * 0.6, y0 + (y1 - y0) * 0.6, 40, 22, "", HELM)
    for seg in legs:                                              # rodilleras
        x, y = seg[1]
        _patch(p, x, y, 46, 26, "", (255, 255, 255))
    hands = []
    for a in arms:
        x, y = a[-1]
        px, py = a[-2]
        cx, cy = px + (x - px) * 0.78, py + (y - py) * 0.78
        p.stroke([(cx, cy), (x, y)], ww + 8, (240, 240, 244))     # guantes con puño largo
        p.stroke([(cx, cy), (cx + (x - cx) * 0.25, cy + (y - cy) * 0.25)], ww + 8, K)
        p.d.ellipse([(x - 34) * SS, (y - 34) * SS, (x + 34) * SS, (y + 34) * SS], fill=(240, 240, 244), outline=K, width=int(7 * SS))
        hands.append((x, y))
    for l in legs:
        x, y = l[-1]
        dirx = 1 if x >= hip[0] else -1
        p.d.rounded_rectangle([min(x, x + 78 * dirx) * SS - 12 * SS, (y - 40) * SS, max(x, x + 78 * dirx) * SS + 12 * SS, (y + 16) * SS],
                              radius=16 * SS, fill=(20, 20, 26))
    _prop(p, hands)


def _prop(p, hands):
    """Objeto de piloto en la mano más alta (dibujado en grande)."""
    if not PROP[0] or not hands:
        return
    hx, hy = min(hands, key=lambda h: h[1])
    q = N.Pen()
    x, y = 500, 600
    _prop_draw(q, x, y)
    from PIL import Image as _I
    lay = q.im.resize((int(q.im.width * 1.6), int(q.im.height * 1.6)), _I.LANCZOS)
    ox, oy = int(hx * SS - x * SS * 1.6), int(hy * SS - y * SS * 1.6)
    p.im.alpha_composite(lay, (max(0, ox), max(0, oy)), (max(0, -ox), max(0, -oy)))
    p.d = __import__("PIL.ImageDraw", fromlist=["ImageDraw"]).Draw(p.im)


def _prop_draw(p, x, y):
    if PROP[0] == "trofeo":
        g, g2 = (250, 196, 46), (200, 140, 20)
        p.d.rectangle([(x - 40) * SS, (y + 20) * SS, (x + 40) * SS, (y + 50) * SS], fill=(60, 60, 70))
        p.d.rectangle([(x - 12) * SS, (y - 30) * SS, (x + 12) * SS, (y + 22) * SS], fill=g2)
        p.d.chord([(x - 70) * SS, (y - 170) * SS, (x + 70) * SS, (y - 10) * SS], 0, 180, fill=g, outline=K, width=int(6 * SS))
        p.d.rectangle([(x - 70) * SS, (y - 100) * SS, (x + 70) * SS, (y - 88) * SS], fill=g)
        for sx in (-1, 1):
            p.d.arc([(x + sx * 70 - 30) * SS, (y - 110) * SS, (x + sx * 70 + 30) * SS, (y - 50) * SS], 90 if sx > 0 else 270, 270 if sx > 0 else 90,
                    fill=K, width=int(8 * SS))
        N.sparkle(p, x + 90, y - 160, 22, (255, 220, 80))
    elif PROP[0] == "champan":
        p.d.rounded_rectangle([(x - 24) * SS, (y - 120) * SS, (x + 24) * SS, (y + 40) * SS], radius=14 * SS, fill=(30, 90, 50), outline=K, width=int(6 * SS))
        p.d.rectangle([(x - 12) * SS, (y - 170) * SS, (x + 12) * SS, (y - 116) * SS], fill=(250, 196, 46))
        p.d.rectangle([(x - 24) * SS, (y - 70) * SS, (x + 24) * SS, (y - 30) * SS], fill=(240, 240, 230))
        import random as _r
        rr = _r.Random(3)
        for k in range(22):
            ang = -1.9 + rr.uniform(-0.45, 0.45)
            dd = rr.uniform(40, 220)
            px_, py_ = x + math.cos(ang) * dd * 0.6, y - 175 + math.sin(ang) * dd
            p.dot(px_, py_, rr.uniform(5, 12), (255, 236, 150))
    elif PROP[0] == "volante":
        p.d.rounded_rectangle([(x - 90) * SS, (y - 50) * SS, (x + 90) * SS, (y + 50) * SS], radius=36 * SS, fill=(30, 30, 36), outline=K, width=int(6 * SS))
        p.d.rounded_rectangle([(x - 40) * SS, (y - 30) * SS, (x + 40) * SS, (y + 10) * SS], radius=6 * SS, fill=(90, 200, 255))
        for k, c in enumerate(((230, 40, 40), (255, 204, 40), (60, 200, 90))):
            p.dot(x - 60 + k * 60, y + 30, 9, c)


import math


def _moto_pre(p):
    """Mono de cuero de MotoGP (21/10): una pieza ajustada, joroba aerodinámica detrás del casco, paneles de colores
    en diagonal, parches de patrocinadores; con el casco amarillo."""
    W_, B_, Y_ = (245, 245, 248), HELM2, HELM
    p.poly([(612, 452), (690, 470), (700, 560), (622, 560)], W_ + (255,))            # joroba (de lado, a la espalda)
    p.stroke([(612, 452), (690, 470), (700, 560), (622, 560)], 8)
    torso = [(392, 448), (608, 448), (622, 525), (578, 655), (590, 770), (410, 770), (422, 655), (378, 525)]
    p.poly(torso, W_ + (255,))
    p.poly([(378, 525), (622, 470), (622, 545), (392, 610)], B_ + (255,))           # panel azul en diagonal
    p.poly([(392, 610), (622, 545), (600, 600), (410, 650)], Y_ + (255,))           # franja amarilla
    p.poly([(422, 655), (578, 655), (590, 770), (410, 770)], B_ + (255,))
    p.stroke(torso + [torso[0]], 9)
    p.stroke([(500, 455), (500, 650)], 6, (90, 100, 130))
    _patch(p, 452, 492, 64, 28, "OJO", (255, 255, 255), (220, 30, 40))
    _patch(p, 548, 600, 70, 26, "MOTO", (255, 255, 255), (28, 58, 140))
    _patch(p, 500, 712, 64, 34, "7", Y_, (28, 58, 140))
    p.d.rounded_rectangle([380 * SS, 424 * SS, 620 * SS, 474 * SS], radius=24 * SS, fill=(30, 30, 36), outline=K, width=int(6 * SS))
    _helmet(p)


def _moto_body(p, neck, hip, arms, legs, w=26):
    W_, B_, Y_ = (245, 245, 248), HELM2, HELM
    ww = w * 2.3
    for seg in arms + legs:
        p.stroke(seg, ww + 10, K)
    for seg in arms:
        p.stroke(seg, ww, W_)
        p.stroke([seg[0], seg[1]], ww * 0.45, B_)                                     # franja azul en el brazo
    for seg in legs:
        p.stroke(seg, ww, B_)
        p.stroke(seg, 10, Y_)
    for seg in arms:                                                                # deslizadores de codo
        x, y = seg[1]
        p.d.ellipse([(x - 20) * SS, (y - 20) * SS, (x + 20) * SS, (y + 20) * SS], fill=(40, 40, 46), outline=K, width=int(4 * SS))
    for seg in legs:                                                                # deslizadores de rodilla (los «pucks»)
        x, y = seg[1]
        p.d.ellipse([(x - 34) * SS, (y - 26) * SS, (x + 34) * SS, (y + 26) * SS], fill=(250, 250, 250), outline=K, width=int(6 * SS))
        p.d.ellipse([(x - 20) * SS, (y - 14) * SS, (x + 20) * SS, (y + 14) * SS], fill=Y_)
    for a in arms:
        x, y = a[-1]
        px, py = a[-2]
        cx, cy = px + (x - px) * 0.78, py + (y - py) * 0.78
        p.stroke([(cx, cy), (x, y)], ww + 8, (30, 30, 36))
        p.d.ellipse([(x - 34) * SS, (y - 34) * SS, (x + 34) * SS, (y + 34) * SS], fill=(30, 30, 36), outline=K, width=int(7 * SS))
        p.d.rounded_rectangle([(x - 22) * SS, (y - 30) * SS, (x + 22) * SS, (y - 16) * SS], radius=4 * SS, fill=Y_)
    for l in legs:
        x, y = l[-1]
        dirx = 1 if x >= hip[0] else -1
        p.d.rounded_rectangle([min(x, x + 82 * dirx) * SS - 12 * SS, (y - 60) * SS, max(x, x + 82 * dirx) * SS + 12 * SS, (y + 16) * SS],
                              radius=16 * SS, fill=(245, 245, 248), outline=K, width=int(6 * SS))
        p.d.rectangle([(x - 12) * SS, (y - 46) * SS, (x + 12) * SS, (y - 10) * SS], fill=B_)
        tx = x + 82 * dirx
        p.d.ellipse([(tx - 14) * SS, (y - 8) * SS, (tx + 14) * SS, (y + 16) * SS], fill=(150, 154, 166))


GEAR = {"piloto": _suit_body, "motogp": _moto_body, "astronauta": _gear_body((240, 240, 244), (200, 204, 214))}


def _badge_leaf(p):
    p.d.ellipse([548 * SS, 600 * SS, 600 * SS, 640 * SS], fill=(70, 170, 90), outline=K, width=int(4 * SS))
    p.stroke([(552, 636), (596, 604)], 4)


def _badge_star(p):
    N.sparkle(p, 575, 620, 24, (255, 204, 48))


TRAJES = {
    None: (None, None),
    # científicos según el tema (21/10: «dejemos al científico… depende de la temática»)
    "c_clasico": (lambda p: T.coat(p), lambda p: (T.bow(p), C.glasses_round(p))),
    "c_quimico": (lambda p: (C.strap(p), T.coat(p)), lambda p: (C.big_goggles(p),)),
    "c_fisico": (lambda p: T.coat(p), lambda p: (T.bow(p),)),  # 21/10: sin átomo fijo junto a la cabeza
    "c_biologo": (lambda p: (T.coat(p), _badge_leaf(p)), lambda p: (C.glasses_round(p),)),
    "c_astronomo": (lambda p: (T.coat(p, (40, 50, 90)), _badge_star(p)), lambda p: (C.glasses_round(p),)),
    "c_inventor": (lambda p: T.coat(p), lambda p: (C.burn(p),)),  # 21/10: sin lupa en la cara
    "c_loco": (lambda p: (T.hair(p, 7), T.coat(p)), lambda p: (C.lightning_hair(p), C.burn(p))),
    "c_profe": (lambda p: T.coat(p, (70, 74, 90)), lambda p: (C.glasses_round(p), T.bow(p))),
    "cientifico": (lambda p: T.coat(p), lambda p: (T.bow(p), C.glasses_round(p))),
    "loco": (lambda p: (T.hair(p, 7), T.coat(p)), lambda p: (C.lightning_hair(p),)),
    "profesor": (lambda p: T.coat(p, (60, 64, 80)), lambda p: (T.bow(p), T.cap(p))),
    "piloto": (_piloto_pre, _piloto_post),
    "motogp": (_moto_pre, _piloto_post),
    "astronauta": (T2.astronauta_pre, T2.astronauta_post),
    "romano": (T2.romano_pre, T2.romano_post),
    "reportero": (lambda p: T.coat(p, (60, 64, 80)), _hat_reportero),
    "detective": (lambda p: T.coat(p, (196, 160, 110)), _hat_detective),
    "obra": (T2.obra_pre, _hat_obra),
    "mago": (T2.mago_pre, _hat_mago),
    "explorador": (None, T.helmet),
    "callejero": (T2.calle_pre, T2.calle_post),
}


def _coat_body(p, neck, hip, arms, legs, w=26):
    """Con bata (21/10, Iker): la bata tapa el torso — sin la raya del cuerpo; las piernas salen por debajo de la bata."""
    CB = 806
    for a in arms:
        p.stroke(a, w)
        p.dot(*a[-1], w * 0.95)
    for l in legs:
        pts = list(l)
        (x0, y0), (x1, y1) = pts[0], pts[1]
        if y0 < CB < y1:
            u = (CB - y0) / (y1 - y0)
            pts[0] = (x0 + (x1 - x0) * u, CB)
        p.stroke(pts, w)
        x, y = pts[-1]
        dirx = 1 if x >= hip[0] else -1
        p.stroke([(x, y), (x + 34 * dirx, y)], w)


COAT = {"c_clasico", "c_quimico", "c_fisico", "c_biologo", "c_astronomo", "c_inventor", "c_loco", "c_profe", "cientifico",
        "loco", "profesor", "reportero", "detective"}


def figure(pose="point", traje=None, lid=0.0, look=(0.06, 0.0), talk=0.0):
    k = (pose, traje, SUIT_SEL[0] if traje == "piloto" else "", round(lid, 1), tuple(round(v, 2) for v in look), round(talk, 1))
    if k not in _C:
        pre, post = TRAJES.get(traje, (None, None))
        p = N.Pen()
        if pre:
            pre(p)
        body0 = N.body
        if traje in GEAR:
            N.body = GEAR[traje]
        elif traje in COAT:
            N.body = _coat_body
        try:
            N._pose(p, pose, lid, look, talk)
        finally:
            N.body = body0
        if post:
            post(p)
        _C[k] = p.im.resize((N.W0 // 2, N.H0 // 2), Image.LANCZOS)
    return _C[k]
