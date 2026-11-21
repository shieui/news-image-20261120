#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news poster.

Build-time only: renders entry.png (1024x1024, RGB) with PIL.
Everything is drawn from primitives; no downloaded images, no network,
no randomness, no clock -- the output bytes are fully deterministic.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024

# ---- palette ------------------------------------------------------------
NAVY = (15, 27, 45)
CREAM = (245, 239, 224)
INK = (20, 32, 46)
RED = (192, 57, 43)
WHITE = (255, 255, 255)
PANEL_LINE = (216, 222, 230)
GREY = (90, 100, 114)
SKY = (38, 62, 96)
GOLD = (212, 160, 40)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSerif-Bold.ttf", 54)
F_DATE = font("DejaVuSans-Bold.ttf", 46)
F_SUB = font("DejaVuSans.ttf", 21)
F_KICKER = font("DejaVuSans-Bold.ttf", 19)
F_HEAD = font("DejaVuSans-Bold.ttf", 29)
F_BODY = font("DejaVuSans.ttf", 18)
F_STRIP = font("DejaVuSans-Bold.ttf", 18)
F_STRIP_BODY = font("DejaVuSans.ttf", 18)
F_FOOT = font("DejaVuSans.ttf", 15)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_panel(draw, x, y, w, h, accent, kicker, headline, body, pict):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10,
                           fill=WHITE, outline=PANEL_LINE, width=2)
    draw.rectangle([x, y, x + w, y + 7], fill=accent)
    draw.text((x + 18, y + 18), kicker, font=F_KICKER, fill=accent)
    tx = x + 18
    tw = w - 36
    lines = wrap(draw, headline, F_HEAD, tw)[:2]
    ly = y + 44
    for ln in lines:
        draw.text((tx, ly), ln, font=F_HEAD, fill=INK)
        ly += 32
    ly = y + 112
    for ln in wrap(draw, body, F_BODY, tw)[:3]:
        draw.text((tx, ly), ln, font=F_BODY, fill=(52, 64, 80))
        ly += 22
    pict(draw, x + 18, y + h - 56, w - 36, 44)


# ---- pictograms (simple flat drawings, one per story) -------------------

def pic_missiles(draw, x, y, w, h):
    # night sky, streaking missile, Polish flag on a pole
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    draw.line([x + 8, y + 12, x + w - 60, y + h - 8], fill=(255, 214, 90), width=3)
    for cx, cy, r in [(x + 60, y + 20, 2), (x + 130, y + 30, 2),
                      (x + 200, y + 16, 2), (x + 300, y + 26, 2)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE)
    draw.polygon([(x + w - 52, y + 6), (x + w - 38, y + 12),
                  (x + w - 52, y + 18)], fill=(255, 214, 90))
    # Polish flag: white over red
    fx, fy = x + w - 110, y + 8
    draw.line([fx, fy, fx, fy + 36], fill=(200, 200, 200), width=2)
    draw.rectangle([fx + 2, fy, fx + 42, fy + 12], fill=WHITE)
    draw.rectangle([fx + 2, fy + 12, fx + 42, fy + 24], fill=(220, 20, 60))
    # burst
    bx, by = x + 40, y + h - 12
    for dx, dy in [(0, -8), (7, -4), (8, 4), (0, 8), (-8, 4), (-7, -4)]:
        draw.line([bx, by, bx + dx, by + dy], fill=(255, 120, 40), width=2)


def pic_scales(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(232, 238, 244))
    cx = x + w // 2
    draw.line([cx, y + 6, cx, y + h - 6], fill=(60, 70, 84), width=4)
    draw.line([cx - 52, y + 12, cx + 52, y + 12], fill=(60, 70, 84), width=4)
    for s in (-1, 1):
        px = cx + s * 52
        draw.line([px, y + 12, px, y + 22], fill=(60, 70, 84), width=2)
        draw.pieslice([px - 20, y + 16, px + 20, y + 36], start=0, end=180,
                      fill=(60, 70, 84))
    draw.ellipse([cx - 4, y + 2, cx + 4, y + 10], fill=GOLD)


def pic_chart(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(248, 232, 230))
    pts = [(x + 10, y + 8), (x + 70, y + 14), (x + 120, y + 10),
           (x + 180, y + 24), (x + 240, y + 30), (x + 300, y + h - 10)]
    draw.line(pts, fill=RED, width=4)
    draw.polygon([(x + 300, y + h - 10), (x + 300, y + h - 20),
                  (x + 312, y + h - 6), (x + 292, y + h - 4)], fill=RED)
    for bx, bh in [(20, 12), (70, 18), (120, 14), (170, 24), (220, 30), (270, 40)]:
        draw.rectangle([x + bx, y + h - bh, x + bx + 26, y + h - 4],
                       fill=(200, 120, 110))
    draw.text((x + w - 108, y + 4), "-4.8%", font=F_STRIP, fill=RED)


def pic_climate(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(226, 240, 232))
    cx, cy, r = x + 46, y + h // 2, 20
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(46, 125, 190))
    draw.ellipse([cx - 12, cy - 10, cx - 2, cy - 2], fill=(74, 160, 90))
    draw.ellipse([cx + 2, cy + 4, cx + 12, cy + 12], fill=(74, 160, 90))
    draw.ellipse([cx - 6, cy + 8, cx + 4, cy + 14], fill=(74, 160, 90))
    # thermometer
    tx = x + w - 60
    draw.rounded_rectangle([tx, y + 4, tx + 14, y + h - 14], radius=7,
                           outline=(90, 100, 114), width=2, fill=WHITE)
    draw.ellipse([tx - 6, y + h - 20, tx + 20, y + h - 6], fill=RED)
    draw.rectangle([tx + 4, y + 12, tx + 10, y + h - 12], fill=RED)
    draw.text((x + 90, y + 12), "COP31", font=F_STRIP, fill=(46, 125, 60))


def pic_towers(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(38, 52, 74))
    base = y + h - 4
    towers = [(x + 16, 34), (x + 66, 44), (x + 116, 28), (x + 166, 40),
              (x + 216, 32), (x + 266, 44)]
    for tx, th in towers:
        draw.rectangle([tx, base - th, tx + 34, base], fill=(120, 140, 168))
        for wy in range(base - th + 6, base - 4, 10):
            draw.rectangle([tx + 5, wy, tx + 12, wy + 5], fill=(255, 214, 90))
            draw.rectangle([tx + 20, wy, tx + 27, wy + 5], fill=(255, 214, 90))
    # damaged tower top: jagged break + smoke
    tx, th = towers[2]
    draw.polygon([(tx, base - th), (tx + 12, base - th - 8),
                  (tx + 22, base - th), (tx + 34, base - th - 6),
                  (tx + 34, base - th + 4), (tx, base - th + 4)],
                 fill=(200, 120, 90))
    for sx, sy, sr in [(tx + 8, base - th - 2, 3), (tx + 22, base - th - 5, 4),
                       (tx + 14, base - th - 8, 3)]:
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(200, 200, 200))


def pic_flags(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(232, 238, 244))
    # three small flags on poles
    fx = x + 30
    # US: six red/white stripes with a blue canton
    draw.line([fx, y + 4, fx, y + h - 6], fill=(90, 100, 114), width=2)
    for i in range(6):
        col = (178, 34, 52) if i % 2 == 0 else (255, 255, 255)
        draw.rectangle([fx + 2, y + 6 + i * 5, fx + 62, y + 11 + i * 5],
                       fill=col, outline=(90, 100, 114))
    draw.rectangle([fx + 2, y + 6, fx + 28, y + 21], fill=(60, 59, 110))
    fx += 118
    # China: red field, gold stars
    draw.line([fx, y + 4, fx, y + h - 6], fill=(90, 100, 114), width=2)
    draw.rectangle([fx + 2, y + 6, fx + 62, y + 36], fill=(222, 41, 16),
                   outline=(90, 100, 114))
    for sx, sy in [(fx + 10, y + 13), (fx + 22, y + 13), (fx + 16, y + 22)]:
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 222, 0))
    fx += 118
    # Russia: white, blue, red
    draw.line([fx, y + 4, fx, y + h - 6], fill=(90, 100, 114), width=2)
    for i, col in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        draw.rectangle([fx + 2, y + 6 + i * 10, fx + 62, y + 16 + i * 10],
                       fill=col, outline=(90, 100, 114))
    draw.text((x + w - 92, y + h - 26), "no deal", font=F_STRIP, fill=RED)


PANELS = [
    ((192, 57, 43), "EUROPE  ·  SECURITY",
     "Russian missiles land in Poland",
     "Two missiles and a drone came down overnight. PM Tusk calls it an "
     "\u201cintentional provocation\u201d; NATO chief Rutte calls it a "
     "\u201cgrave violation\u201d.",
     pic_missiles),
    ((14, 124, 123), "JUSTICE  ·  THE HAGUE",
     "World court: Myanmar guilty of genocide",
     "The ICJ finds Myanmar responsible for genocide against the Rohingya "
     "\u2014 the first state ever so judged. Myanmar\u2019s junta rejects "
     "the verdict.",
     pic_scales),
    ((142, 31, 31), "MARKETS  ·  ECONOMY",
     "Stocks plunge as the AI boom turns to bust",
     "Japan\u2019s Nikkei falls 4.8% and Wall Street extends its slide. "
     "Anthropic drops 13% a day after its record IPO.",
     pic_chart),
    ((46, 125, 60), "CLIMATE  ·  COP31",
     "COP31 draft drops fossil fuels",
     "The draft deal in Antalya, Turkey, omits any call to phase out fossil "
     "fuels. Activists and leaders condemn the text.",
     pic_climate),
    ((178, 106, 0), "MIDDLE EAST  ·  RIYADH",
     "Saudi Arabia strikes back at the Houthis",
     "After Thursday\u2019s missile hit on Riyadh\u2019s PIF Tower, Saudi "
     "forces attack Houthi targets and intercept more missiles and drones.",
     pic_towers),
    ((31, 78, 121), "DIPLOMACY  ·  AFTER SHENZHEN",
     "No breakthrough after the three-way summit",
     "Trump, Xi and Putin\u2019s talks end with no nuclear deal. Trump says "
     "China\u2019s nuclear build-up is \u201chot and heavy\u201d.",
     pic_flags),
]

STRIP_LINES = [
    "EU and UK hold their second summit in Brussels  ·  "
    "Kenya discharges its last Ebola patient",
    "Israeli troops cross the Gaza ceasefire line  ·  "
    "Over a million workers strike across Italy",
]


def main():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    # ---- masthead ------------------------------------------------------
    d.rectangle([0, 0, W, 148], fill=CREAM)
    d.rectangle([0, 148, W, 154], fill=RED)
    d.text((24, 10), "THE WORLD IN ONE DAY", font=F_TITLE, fill=INK)
    d.text((24, 74), "FRIDAY 20 NOVEMBER 2026", font=F_DATE, fill=RED)
    d.text((24, 126), "Six stories from around the world",
           font=F_SUB, fill=GREY)

    # ---- story grid ----------------------------------------------------
    gx, gy = 24, 166
    pw, ph = 480, 238
    gap = 14
    for i, (accent, kicker, head, body, pict) in enumerate(PANELS):
        col, row = i % 2, i // 2
        draw_panel(d, gx + col * (pw + gap), gy + row * (ph + gap),
                   pw, ph, accent, kicker, head, body, pict)

    # ---- also-today strip ----------------------------------------------
    sy = 166 + 3 * ph + 2 * gap + 10
    d.rounded_rectangle([24, sy, W - 24, sy + 72], radius=8, fill=WHITE)
    d.text((40, sy + 8), "ALSO TODAY:", font=F_STRIP, fill=RED)
    d.text((40, sy + 30), STRIP_LINES[0], font=F_STRIP_BODY, fill=INK)
    d.text((40, sy + 52), STRIP_LINES[1], font=F_STRIP_BODY, fill=INK)

    # ---- footer ---------------------------------------------------------
    d.text((24, H - 24),
           "Drawn from news reported on Friday 20 November 2026.",
           font=F_FOOT, fill=(150, 164, 180))
    d.text((W - 24 - d.textlength("ONE DAY  ·  ONE PICTURE", font=F_FOOT),
            H - 26), "ONE DAY  ·  ONE PICTURE", font=F_FOOT,
           fill=(150, 164, 180))

    img.save(OUT, format="PNG")
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()
