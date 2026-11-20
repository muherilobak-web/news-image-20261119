#!/usr/bin/env python3
"""Draw the news-image-20261119 front page: one day's world news, drawn, not photographed.

Build-time only. Produces entry.png (1024x1024, PNG) in this directory.
Every picture on the page is drawn here from flat shapes and text -- no
downloaded photographs, no copied artwork, no AI-generated image.
The eight facts come from the strategy brief; the only numbers on the page
are the verified 19 November 2026 figures. Nothing from 20 November is used.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

# --- palette: flat colours only, no gradients --------------------------------
PAPER = (247, 243, 234)   # #F7F3EA
INK = (25, 25, 25)        # #191919
RED = (185, 28, 28)       # #B91C1C
BLUE = (30, 58, 95)       # #1E3A5F
GREEN = (31, 107, 74)     # #1F6B4A
ORANGE = (217, 119, 6)    # #D97706
SKY = (127, 163, 199)     # #7FA3C7
BROWN = (107, 74, 47)     # table wood
GREY = (138, 138, 138)    # smoke
WATER = (110, 150, 190)   # sea / river blue
SUNSET = (232, 131, 58)   # warm sunset band
SUN = (245, 200, 90)      # sun disc

# --- fonts: DejaVu Sans, bold for headlines, regular for captions ------------
FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def bold(px):
    return ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"), px)


def regular(px):
    return ImageFont.truetype(os.path.join(FONT_DIR, "DejaVuSans.ttf"), px)


# --- text helpers ------------------------------------------------------------
def ctext(d, cx, y, s, font, fill):
    """Centred text, top-anchored at y (anchor middle-ascender)."""
    d.text((cx, y), s, font=font, fill=fill, anchor="ma")


def ctext_mm(d, cx, cy, s, font, fill):
    """Centred text, centred on (cx, cy)."""
    d.text((cx, cy), s, font=font, fill=fill, anchor="mm")


def wrap(s, font, max_w):
    """Greedy word wrap to a pixel width; returns a list of lines."""
    lines, cur = [], ""
    for word in s.split():
        trial = (cur + " " + word).strip()
        if font.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_size(s, px, floor, max_w):
    """Largest bold size from px down to floor that fits max_w, else px=floor."""
    size = px
    while size > floor and bold(size).getlength(s) > max_w:
        size -= 1
    return size


def star_points(cx, cy, r_outer, r_inner, points=5, rot=-90):
    """Points of a star polygon centred on (cx, cy)."""
    pts = []
    for i in range(points * 2):
        r = r_outer if i % 2 == 0 else r_inner
        a = math.radians(rot + i * 180 / points)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


# --- canvas ------------------------------------------------------------------
W = H = 1024
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# Outer frame: 6px ink rule inset 12px -- the page reads as one object.
d.rectangle([12, 12, 1012, 1012], outline=INK, width=6)

# --- masthead, y 24-210 ------------------------------------------------------
ctext(d, 512, 28, "THE WORLD", bold(88), INK)

# Date: 46px red bold (54px would leave no room for the side rules).
date_font = bold(46)
date_text = "THURSDAY 19 NOVEMBER 2026"
dw = date_font.getlength(date_text)
ctext(d, 512, 130, date_text, date_font, RED)
rule_y = 153
d.line([24, rule_y, 512 - dw / 2 - 18, rule_y], fill=INK, width=2)
d.line([512 + dw / 2 + 18, rule_y, 1000, rule_y], fill=INK, width=2)

ctext(d, 512, 184,
      "Eight stories from a single day \u2014 every picture drawn for this page.",
      regular(19), INK)

# --- lead block, y 214-556 ---------------------------------------------------
ctext(d, 512, 212, "THREE LEADERS, ONE TABLE", bold(40), INK)
ctext(d, 512, 256, "A FIRST IN SHENZHEN", bold(40), INK)


def chip(d, x, y, label):
    """Small ink label chip, white bold text, top-left of an illustration."""
    f = bold(16)
    w = int(f.getlength(label)) + 18
    d.rounded_rectangle([x, y, x + w, y + 26], radius=4, fill=INK)
    d.text((x + 9, y + 13), label, font=f, fill=PAPER, anchor="lm")


def caption_bar(d, x0, x1, y0, y1, text):
    """Two-line caption, centred in the bar under an illustration.

    20px: the brief's floor for lead captions. The Shenzhen caption (exact
    wording from the brief) does not fit two lines at 22px in a 488px bar,
    so both captions use 20px for a consistent look.
    """
    f = regular(20)
    lines = wrap(text, f, x1 - x0 - 24)
    assert len(lines) <= 2, f"caption too long: {text!r} -> {lines}"
    line_h = 26
    total = line_h * len(lines)
    y = y0 + (y1 - y0 - total) // 2
    for line in lines:
        ctext(d, (x0 + x1) // 2, y, line, f, INK)
        y += line_h


# Left lead panel: SHENZHEN, x 24-512, illustration y 310-466, caption 470-552
d.rectangle([24, 306, 512, 556], outline=INK, width=3)
chip(d, 36, 314, "SHENZHEN")
# Three flag bands above the table: US stripes, China red+star, Russia tricolour.
# (Flags sit below the chip row so the chip never covers the US band.)
flag_y, flag_w, flag_h = 350, 96, 30
flag_cx = [105, 268, 431]
# US: white ground, red stripes, blue canton.
x = flag_cx[0] - flag_w // 2
d.rectangle([x, flag_y, x + flag_w, flag_y + flag_h], outline=INK, width=2, fill=(255, 255, 255))
for i in range(4):
    d.rectangle([x, flag_y + i * 8, x + flag_w, flag_y + i * 8 + 4], fill=RED)
d.rectangle([x, flag_y, x + 40, flag_y + 16], fill=BLUE)
# China: red ground, one yellow star.
x = flag_cx[1] - flag_w // 2
d.rectangle([x, flag_y, x + flag_w, flag_y + flag_h], outline=INK, width=2, fill=RED)
d.polygon(star_points(x + 20, flag_y + 15, 9, 4), fill=(255, 215, 0))
# Russia: white / blue / red horizontal bands.
x = flag_cx[2] - flag_w // 2
d.rectangle([x, flag_y, x + flag_w, flag_y + 10], outline=INK, width=2, fill=(255, 255, 255))
d.rectangle([x, flag_y + 10, x + flag_w, flag_y + 20], outline=INK, width=2, fill=(0, 60, 160))
d.rectangle([x, flag_y + 20, x + flag_w, flag_y + 30], outline=INK, width=2, fill=RED)
# Three seated figures: flat silhouettes, no faces. Head circle + body block.
for cx in flag_cx:
    d.ellipse([cx - 15, 391, cx + 15, 421], fill=INK)
    d.rounded_rectangle([cx - 35, 424, cx + 35, 452], radius=12, fill=INK)
# Long table with a red runner, and a small red round seal.
d.rectangle([48, 438, 488, 454], fill=BROWN)
d.rectangle([48, 438, 488, 443], fill=RED)
d.ellipse([449, 433, 475, 459], fill=RED)
d.polygon(star_points(462, 446, 8, 3.5), fill=(255, 255, 255))
caption_bar(d, 24, 512, 470, 552,
            "Trump, Xi and Putin hold the first three-way summit "
            "and sign a joint peace declaration.")

# Right lead panel: KYIV, x 524-1000, illustration y 310-466, caption 470-552
d.rectangle([524, 306, 1000, 556], outline=INK, width=3)
d.rectangle([527, 309, 997, 466], fill=SKY)
chip(d, 536, 318, "KYIV")
# Black skyline along the bottom, with one domed church in the middle.
base = 466
buildings = [(532, 60, 88), (596, 44, 66), (644, 52, 78), (700, 40, 58),
             (744, 56, 92), (804, 44, 70), (852, 48, 64), (904, 40, 80),
             (948, 48, 60)]
for bx, bw, bh in buildings:
    d.rectangle([bx, base - bh, bx + bw, base], fill=INK)
# Domed church: tower + onion dome + small cross, centred near x 770.
d.rectangle([742, base - 118, 798, base], fill=INK)
d.ellipse([738, base - 152, 802, base - 100], fill=INK)
d.line([770, base - 168, 770, base - 150], fill=INK, width=4)
d.line([762, base - 160, 778, base - 160], fill=INK, width=4)
# Grey smoke plume rising from a building on the right.
for cx, cy, r in [(916, 392, 26), (924, 362, 30), (912, 332, 24)]:
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GREY)
# One orange impact burst.
d.polygon(star_points(872, 344, 34, 14), fill=ORANGE)
d.polygon(star_points(872, 344, 17, 7), fill=(255, 215, 0))
caption_bar(d, 524, 1000, 470, 552,
            "Russia strikes Kyiv: 1 killed, a cathedral "
            "and two embassies damaged.")

# Divider: 4px ink rule at y 568.
d.line([24, 568, 1000, 568], fill=INK, width=4)

# --- secondary grid, y 580-960: 3 columns x 2 rows, panels 320x184 ---------------
COLS = [24, 356, 688]
ROWS = [580, 776]
PW, PH = 320, 184


def grid_headline(d, x0, y0, line1, line2):
    """Two-line bold headline at the bottom of a grid panel, 25px (floor 24px).

    Wording was shortened where the brief's text did not fit 314px at 25px:
    numbers and meaning are unchanged.
    """
    inner = PW - 12
    for i, line in enumerate((line1, line2)):
        size = fit_size(line, 25, 24, inner - 6)
        ctext(d, x0 + PW // 2, y0 + 120 + i * 30, line, bold(size), INK)


def panel(d, x0, y0, ground):
    """Grid panel: tinted ground + 3px ink border. Returns the inner box."""
    d.rectangle([x0, y0, x0 + PW, y0 + PH], outline=INK, width=3, fill=ground)
    return x0, y0


# 1. ICJ -- gavel + scales of justice, deep blue.
x0, y0 = COLS[0], ROWS[0]
panel(d, x0, y0, (220, 230, 242))
# Scales: pole, crossbar, two hanging pans.
d.line([x0 + 150, y0 + 18, x0 + 150, y0 + 92], fill=BLUE, width=5)
d.line([x0 + 100, y0 + 26, x0 + 200, y0 + 26], fill=BLUE, width=5)
for px in (100, 200):
    d.line([px, y0 + 26, px, y0 + 56], fill=BLUE, width=3)
    # Shallow bowl, not a triangle: a triangle reads as a downward arrow.
    d.pieslice([px - 18, y0 + 56, px + 18, y0 + 74], 0, 180, fill=BLUE)
# Gavel: head + handle striking a block.
d.rectangle([x0 + 232, y0 + 52, x0 + 292, y0 + 72], fill=BLUE)
d.line([x0 + 232, y0 + 62, x0 + 196, y0 + 96], fill=BLUE, width=8)
d.rectangle([x0 + 228, y0 + 88, x0 + 296, y0 + 98], fill=BLUE)
grid_headline(d, x0, y0, "ICJ: MYANMAR GUILTY", "GENOCIDE \u2014 A FIRST")

# 2. Anthropic -- green line chart rising steeply + upward arrow.
x0, y0 = COLS[1], ROWS[0]
panel(d, x0, y0, (221, 240, 228))
d.line([x0 + 24, y0 + 104, x0 + 296, y0 + 104], fill=INK, width=2)
pts = [(x0 + 34, y0 + 92), (x0 + 96, y0 + 78), (x0 + 152, y0 + 86),
       (x0 + 212, y0 + 52), (x0 + 268, y0 + 22)]
d.line(pts, fill=GREEN, width=8, joint="curve")
d.polygon([(x0 + 268, y0 + 22), (x0 + 246, y0 + 24), (x0 + 264, y0 + 44)],
          fill=GREEN)
grid_headline(d, x0, y0, "ANTHROPIC UP 17%", "ON NASDAQ DEBUT")

# 3. Kerch -- bridge over blue water, middle span broken and tilted, smoke.
x0, y0 = COLS[2], ROWS[0]
panel(d, x0, y0, (220, 233, 245))
d.rectangle([x0 + 3, y0 + 88, x0 + PW - 3, y0 + PH - 3], fill=WATER)
d.rectangle([x0 + 20, y0 + 62, x0 + 300, y0 + 70], fill=INK)
for tx in (70, 240):
    d.rectangle([x0 + tx, y0 + 24, x0 + tx + 8, y0 + 70], fill=INK)
# Broken middle span: a tilted slab, dropped on the right.
d.polygon([(x0 + 140, y0 + 58), (x0 + 186, y0 + 62),
           (x0 + 182, y0 + 78), (x0 + 136, y0 + 74)], fill=INK)
for cx, cy, r in [(x0 + 168, y0 + 46, 12), (x0 + 176, y0 + 32, 14), (x0 + 164, y0 + 20, 10)]:
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GREY)
grid_headline(d, x0, y0, "KERCH BRIDGE HIT", "THIRD HIT IN 4 DAYS")

# 4. Senate -- Capitol dome + ballot box, big 51-48.
x0, y0 = COLS[0], ROWS[1]
panel(d, x0, y0, (237, 230, 245))
# Dome: base + half-ellipse dome + pole, deep blue silhouette.
d.rectangle([x0 + 28, y0 + 72, x0 + 148, y0 + 88], fill=BLUE)
d.pieslice([x0 + 28, y0 + 8, x0 + 148, y0 + 76], 180, 360, fill=BLUE)
d.line([x0 + 88, y0 + 2, x0 + 88, y0 + 14], fill=BLUE, width=4)
d.rectangle([x0 + 88, y0 + 2, x0 + 104, y0 + 10], fill=RED)
# Big vote count, and a ballot box under it.
ctext_mm(d, x0 + 238, y0 + 52, "51\u201348", bold(40), INK)
d.rectangle([x0 + 208, y0 + 82, x0 + 268, y0 + 108], outline=INK, width=3,
            fill=(255, 255, 255))
d.line([x0 + 224, y0 + 82, x0 + 252, y0 + 82], fill=INK, width=4)
grid_headline(d, x0, y0, "SENATE REJECTS IRAN", "WAR-POWERS 51\u201348")

# 5. UK & Norway -- two naval craft on blue water, two flag poles.
x0, y0 = COLS[1], ROWS[1]
panel(d, x0, y0, (220, 233, 245))
d.rectangle([x0 + 3, y0 + 88, x0 + PW - 3, y0 + PH - 3], fill=WATER)
for sx, flag in [(x0 + 52, RED), (x0 + 196, BLUE)]:
    # Hull: trapezoid; cabin; mast with a small flag band.
    d.polygon([(sx, y0 + 74), (sx + 96, y0 + 74), (sx + 84, y0 + 90),
               (sx + 12, y0 + 90)], fill=INK)
    d.rectangle([sx + 30, y0 + 58, sx + 62, y0 + 74], fill=INK)
    d.line([sx + 46, y0 + 58, sx + 46, y0 + 34], fill=INK, width=3)
    d.rectangle([sx + 46, y0 + 34, sx + 70, y0 + 46], fill=flag)
grid_headline(d, x0, y0, "UK & NORWAY FUND", "2 WARSHIPS, \u00a3100M+")

# 6. GTA VI -- sunset band, palm silhouettes, controller, big VI in the sun.
x0, y0 = COLS[2], ROWS[1]
panel(d, x0, y0, (245, 230, 216))
d.rectangle([x0 + 3, y0 + 3, x0 + PW - 3, y0 + 56], fill=SUNSET)
d.ellipse([x0 + 132, y0 + 14, x0 + 188, y0 + 70], fill=SUN)
ctext_mm(d, x0 + 160, y0 + 42, "VI", bold(30), INK)
# Palm silhouettes, left and right of the sun.
for px, lean in [(x0 + 52, -1), (x0 + 268, 1)]:
    d.line([px, y0 + 108, px + lean * 10, y0 + 62], fill=INK, width=7)
    top = (px + lean * 10, y0 + 62)
    for dx, dy in [(-26, -6), (-18, -18), (0, -24), (18, -18), (26, -6)]:
        d.line([top, (top[0] + dx, top[1] + dy)], fill=INK, width=5)
# Game-controller silhouette: rounded body + two grips + buttons.
d.rounded_rectangle([x0 + 108, y0 + 78, x0 + 212, y0 + 102], radius=10, fill=INK)
d.ellipse([x0 + 112, y0 + 96, x0 + 132, y0 + 112], fill=INK)
d.ellipse([x0 + 188, y0 + 96, x0 + 208, y0 + 112], fill=INK)
d.ellipse([x0 + 178, y0 + 84, x0 + 186, y0 + 92], fill=PAPER)
d.ellipse([x0 + 190, y0 + 84, x0 + 198, y0 + 92], fill=PAPER)
grid_headline(d, x0, y0, "GTA VI IS OUT", "AFTER 13 YEARS")

# --- footer, y 962-1000 ------------------------------------------------------
ctext(d, 512, 968,
      "Drawn for this page \u2014 no photographs. Thursday 19 November 2026.",
      regular(18), INK)

# --- save --------------------------------------------------------------------
out = os.path.join(HERE, "entry.png")
img.save(out, "PNG")
size = os.path.getsize(out)
print(f"entry.png: {img.size[0]}x{img.size[1]} PNG, {size} bytes "
      f"({size / 1048576:.2f} MiB, limit 1 MiB)")
assert img.size == (1024, 1024), "canvas is not 1024x1024"
assert size <= 1048576, "entry.png exceeds 1 MiB"
