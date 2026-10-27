"""Kit de ilustración detallada (estilo «Titanic pro» con más volumen):
degradados dentro de formas, degradados radiales, sombras suaves, brillos y reflejos, todo con supermuestreo."""
from cine import *


class Cv:
    """Lienzo supermuestreado. Coordenadas en píxeles finales; internamente ×ss."""

    def __init__(self, w, h, ss=3):
        self.w, self.h, self.ss = w, h, ss
        self.im = Image.new("RGBA", (w * ss, h * ss), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    # utilidades
    def S(self, pts):
        return [(x * self.ss, y * self.ss) for x, y in pts]

    def B(self, box):
        return [v * self.ss for v in box]

    def _mask_poly(self, pts):
        m = Image.new("L", self.im.size, 0)
        ImageDraw.Draw(m).polygon(self.S(pts), fill=255)
        return m

    def _mask_ellipse(self, box):
        m = Image.new("L", self.im.size, 0)
        ImageDraw.Draw(m).ellipse(self.B(box), fill=255)
        return m

    def _vgrad(self, bbox, c1, c2, power=1.0, horizontal=False):
        x0, y0, x1, y1 = [int(v) for v in bbox]
        w, h = max(1, x1 - x0), max(1, y1 - y0)
        n = w if horizontal else h
        u = np.linspace(0, 1, n) ** power
        cols = np.array(c1, float)[None, :] + (np.array(c2, float) - np.array(c1, float))[None, :] * u[:, None]
        if len(c1) == 3:
            cols = np.concatenate([cols, np.full((n, 1), 255.0)], axis=1)
        arr = np.broadcast_to(cols[None, :, :], (h, w, 4)) if horizontal else np.broadcast_to(cols[:, None, :], (h, w, 4))
        return Image.fromarray(arr.astype(np.uint8).copy(), "RGBA"), (x0, y0)

    def _paste_masked(self, src, pos, mask):
        bb = mask.getbbox()
        if not bb:
            return
        mk = mask.crop(bb)
        sx0, sy0 = bb[0] - pos[0], bb[1] - pos[1]
        sr = src.crop((sx0, sy0, sx0 + bb[2] - bb[0], sy0 + bb[3] - bb[1]))
        a = np.array(sr.getchannel("A"), np.uint16) * np.array(mk, np.uint16) // 255
        sr.putalpha(Image.fromarray(a.astype(np.uint8), "L"))
        self.im.alpha_composite(sr, (bb[0], bb[1]))

    # primitivas
    def poly(self, pts, fill=None, grad=None, power=1.0, horizontal=False, outline=None, width=0):
        if grad:
            m = self._mask_poly(pts)
            bb = m.getbbox()
            if bb:
                g, pos = self._vgrad(bb, grad[0], grad[1], power, horizontal)
                self._paste_masked(g, pos, m)
        elif fill is not None:
            if len(fill) == 4 and fill[3] < 255:
                P_ = self.S(pts)
                x0 = max(0, int(min(p[0] for p in P_)) - 2)
                y0 = max(0, int(min(p[1] for p in P_)) - 2)
                x1 = min(self.im.size[0], int(max(p[0] for p in P_)) + 3)
                y1 = min(self.im.size[1], int(max(p[1] for p in P_)) + 3)
                if x1 <= x0 or y1 <= y0:
                    return
                lay = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0))
                ImageDraw.Draw(lay).polygon([(p[0] - x0, p[1] - y0) for p in P_], fill=fill)
                self.im.alpha_composite(lay, (x0, y0))
            else:
                self.d.polygon(self.S(pts), fill=fill)
        if outline:
            self.d.line(self.S(list(pts) + [pts[0]]), fill=outline, width=int(width * self.ss), joint="curve")

    def rect(self, box, fill=None, grad=None, power=1.0, horizontal=False, r=0):
        x0, y0, x1, y1 = box
        if r > 0:
            m = Image.new("L", self.im.size, 0)
            ImageDraw.Draw(m).rounded_rectangle(self.B(box), radius=int(r * self.ss), fill=255)
            bb = m.getbbox()
            if not bb:
                return
            if grad:
                g, pos = self._vgrad(bb, grad[0], grad[1], power, horizontal)
            else:
                g, pos = Image.new("RGBA", (bb[2] - bb[0], bb[3] - bb[1]), tuple(fill) + (() if len(fill) == 4 else (255,))), bb[:2]
            self._paste_masked(g, pos, m)
        else:
            self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill, grad, power, horizontal)

    def ellipse(self, box, fill=None, grad=None, radial=None, power=1.0, center=(0.5, 0.5)):
        m = self._mask_ellipse(box)
        bb = m.getbbox()
        if not bb:
            return
        if radial:
            x0, y0, x1, y1 = bb
            w, h = x1 - x0, y1 - y0
            yy, xx = np.mgrid[0:h, 0:w]
            cx, cy = w * center[0], h * center[1]
            dist = np.sqrt(((xx - cx) / (w / 2)) ** 2 + ((yy - cy) / (h / 2)) ** 2)
            u = np.clip(dist, 0, 1) ** power
            c1, c2 = np.array(radial[0], float), np.array(radial[1], float)
            arr = c1[None, None, :] + (c2 - c1)[None, None, :] * u[:, :, None]
            if arr.shape[2] == 3:
                arr = np.concatenate([arr, np.full((h, w, 1), 255.0)], axis=2)
            self._paste_masked(Image.fromarray(arr.astype(np.uint8), "RGBA"), (x0, y0), m)
        elif grad:
            g, pos = self._vgrad(bb, grad[0], grad[1], power)
            self._paste_masked(g, pos, m)
        elif fill is not None:
            B_ = self.B(box)
            if len(fill) == 4 and fill[3] < 255:
                self._blend(B_, lambda d, x0, y0: d.ellipse([B_[0] - x0, B_[1] - y0, B_[2] - x0, B_[3] - y0], fill=fill))
            else:
                self.d.ellipse(B_, fill=fill)

    def _blend(self, bbox, fn):
        """Dibuja con transparencia mezclando de verdad (ImageDraw sobre RGBA sustituye píxeles)."""
        x0, y0 = max(0, int(bbox[0])), max(0, int(bbox[1]))
        x1, y1 = min(self.im.size[0], int(bbox[2]) + 1), min(self.im.size[1], int(bbox[3]) + 1)
        if x1 <= x0 or y1 <= y0:
            return
        lay = Image.new("RGBA", (x1 - x0, y1 - y0), (0, 0, 0, 0))
        fn(ImageDraw.Draw(lay), x0, y0)
        self.im.alpha_composite(lay, (x0, y0))

    def line(self, pts, col, w=2):
        P_, ww = self.S(pts), max(1, int(w * self.ss))
        if len(col) == 4 and col[3] < 255:
            xs, ys = [p[0] for p in P_], [p[1] for p in P_]
            self._blend((min(xs) - ww, min(ys) - ww, max(xs) + ww, max(ys) + ww),
                        lambda d, x0, y0: d.line([(x - x0, y - y0) for x, y in P_], fill=col, width=ww, joint="curve"))
        else:
            self.d.line(P_, fill=col, width=ww, joint="curve")

    def arc(self, box, a0, a1, col, w=2):
        B_, ww = self.B(box), max(1, int(w * self.ss))
        if len(col) == 4 and col[3] < 255:
            self._blend((B_[0] - ww, B_[1] - ww, B_[2] + ww, B_[3] + ww),
                        lambda d, x0, y0: d.arc([B_[0] - x0, B_[1] - y0, B_[2] - x0, B_[3] - y0], a0, a1, fill=col, width=ww))
        else:
            self.d.arc(B_, a0, a1, fill=col, width=ww)

    def glow(self, x, y, r, col, strength=1.0):
        g = S.glow(int(r * self.ss), col, strength)
        self.im.alpha_composite(g, (int(x * self.ss - g.size[0] / 2), int(y * self.ss - g.size[1] / 2)))

    def shadow(self, box, alpha=120, blur=12):
        lay = Image.new("RGBA", self.im.size, (0, 0, 0, 0))
        ImageDraw.Draw(lay).ellipse(self.B(box), fill=(0, 0, 0, alpha))
        lay = lay.filter(ImageFilter.GaussianBlur(blur * self.ss))
        base = Image.alpha_composite(lay, self.im)
        self.im = base
        self.d = ImageDraw.Draw(self.im)

    def text(self, xy, txt, size, col, font=None, anchor="mm"):
        self.d.text((xy[0] * self.ss, xy[1] * self.ss), txt, font=f(font or F_CAP, int(size * self.ss)), fill=col, anchor=anchor)

    def done(self):
        return self.im.resize((self.w, self.h), Image.LANCZOS)


def shade(c, k):
    """Oscurece (k<1) o aclara (k>1) un color."""
    if k <= 1:
        return tuple(int(v * k) for v in c)
    return tuple(int(v + (255 - v) * (k - 1)) for v in c)


# ------------------------------------------------------------------ escenarios comunes
def city_lights(img, t, y, seed=4, n=160, col=(255, 200, 120), spread=60):
    d = ImageDraw.Draw(img, "RGBA")
    rr = random.Random(seed)
    for i in range(n):
        x = rr.uniform(0, W)
        yy = y + rr.uniform(-spread, spread * 0.3)
        r = rr.uniform(1.2, 3.2)
        a = int(140 + 100 * (0.5 + 0.5 * math.sin(t * rr.uniform(1, 3) + i)))
        c = col if rr.random() < 0.7 else (220, 230, 255)
        d.ellipse([x - r, yy - r, x + r, yy + r], fill=c + (a,))


def lens_flare(img, x, y, k=1.0, col=(255, 230, 190)):
    if k <= 0:
        return
    paste(img, glow(220, col, 0.7), x, y, 1.0, k)
    paste(img, glow(60, (255, 255, 255), 1.0), x, y, 1.0, k)
    d = ImageDraw.Draw(img, "RGBA")
    d.line([(x - 300 * k, y), (x + 300 * k, y)], fill=(255, 240, 220, int(120 * k)), width=2)


def light_cone(img, x0, y0, x1, y1, spread0, spread1, col=(255, 240, 200), alpha=90, blur=18):
    """Haz de luz (faros, focos) como polígono degradado y difuminado."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dd = ImageDraw.Draw(im)
    ang = math.atan2(y1 - y0, x1 - x0)
    nx, ny = -math.sin(ang), math.cos(ang)
    steps = 12
    for i in range(steps):
        u0, u1 = i / steps, (i + 1) / steps
        p0 = (x0 + (x1 - x0) * u0, y0 + (y1 - y0) * u0)
        p1 = (x0 + (x1 - x0) * u1, y0 + (y1 - y0) * u1)
        s0 = lerp(spread0, spread1, u0)
        s1 = lerp(spread0, spread1, u1)
        a = int(alpha * (1 - u0) ** 1.3)
        dd.polygon([(p0[0] + nx * s0, p0[1] + ny * s0), (p1[0] + nx * s1, p1[1] + ny * s1),
                    (p1[0] - nx * s1, p1[1] - ny * s1), (p0[0] - nx * s0, p0[1] - ny * s0)], fill=col + (a,))
    AC(img, im.filter(ImageFilter.GaussianBlur(blur)))
