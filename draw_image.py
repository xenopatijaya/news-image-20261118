#!/usr/bin/env python3
"""Draw the front page for Wednesday 18 November 2026.

One 1024x683 PNG: masthead with the date, lead story (APEC Shenzhen),
a labelled world map, and a numbered grid of 36 further stories.
All 38 stories are events that happened or were first reported on
18 November 2026, drawn from live news reporting of that day.
Flat colours only, so the file stays small and the text stays crisp.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 683
CREAM = (246, 241, 227)
INK = (18, 18, 18)
RED = (163, 18, 18)
DARKRED = (120, 10, 10)
BLUE = (28, 68, 120)
SEA = (203, 222, 235)
LAND = (232, 214, 164)
LAND_EDGE = (90, 70, 40)
GREY = (90, 86, 76)
LIGHT = (255, 252, 244)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Wrap text to lines no wider than width pixels."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, fnt, width, max_lines):
    """Wrap and truncate with an ellipsis to at most max_lines."""
    lines = wrap(draw, text, fnt, width)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and draw.textlength(lines[-1] + "…", font=fnt) > width:
            lines[-1] = lines[-1][:-1]
        lines[-1] += "…"
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# (number, tag, headline, one-line deck) — stories 3..38.
GRID = [
    (3, "EUROPE · KYIV", "Kerch Bridge hit again",
     "Second straight day of strikes"),
    (4, "GULF", "Bahrain all-clear after threat",
     "Kuwait drone intercepted"),
    (5, "GAZA", "Gaza: one hot meal in two",
     "WFP warns aid runs short"),
    (6, "LONDON", "UK sanctions 8 settler firms",
     "Also targets Gaza aid blockers"),
    (7, "BEIJING", "China–Canada extend trade ties",
     "Xi meets Carney before APEC"),
    (8, "MANILA", "Modi: world needs predictability",
     "ASEAN–India summit in Manila"),
    (9, "INDIA", "Amazon puts $7bn in India",
     "Renewable-energy investment"),
    (10, "INDIA", "India growth forecast 7.5%",
     "GDP outlook for the year"),
    (11, "TECH", "Nvidia revenue $115.8bn",
     "Quarterly sales beat forecasts"),
    (12, "TECH", "Baidu chief warns of AI bubble",
     "Warning ahead of APEC talks"),
    (13, "ASIA", "Japan offers energy storage",
     "Access for ASEAN nations"),
    (14, "ASIA", "Cyclone Akvan strengthens",
     "Severe storm expected 19 Nov"),
    (15, "SPORT", "Dhoni retires from the IPL",
     "Becomes Chennai mentor"),
    (16, "CULTURE", "Grammy 2027 nominees out",
     "Raye leads; Styles snubbed"),
    (17, "EUROPE", "Latvia approves new cabinet",
     "Kulbergs wins confidence vote"),
    (18, "USA", "Merchant jailed 27.5 years",
     "Plot against US officials"),
    (19, "AFRICA", "Sudan: 2,230 civilians dead",
     "UN toll, Jan–Oct drone strikes"),
    (20, "PAKISTAN", "Pakistan blast kills 5",
     "Checkpoint bombing wounds 13"),
    (21, "PAKISTAN", "74 militants killed",
     "Ten-day border operation"),
    (22, "SPACE", "SpaceX catches Starship",
     "Booster caught on return"),
    (23, "USA", "NSA comms network goes down",
     "Outage amid Iran fears"),
    (24, "USA", "Trump: Iran plot 'very serious'",
     "Alleged bomb plot on DC"),
    (25, "EUROPE", "Earthshot: PFAS-Free France",
     "First forever-chemical law"),
    (26, "PERU", "Pope Leo hit by rosary",
     "Beads strike his eye in crowd"),
    (27, "USA", "JetBlue turbulence injures 5",
     "Puerto Rico–Florida flight"),
    (28, "INDIA", "India re-elected to ITU Council",
     "Term 2027–2030"),
    (29, "UKRAINE", "UN: 372 civilians killed in Oct",
     "Ukraine toll for October"),
    (30, "UKRAINE", "Russia hits Kyiv bridges",
     "Strikes on crossings reported"),
    (31, "ASIA", "Trump hints at Kim meeting",
     "Possible talks this week"),
    (32, "GAZA", "Gaza families back to kerosene",
     "Gas shortages bite at home"),
    (33, "GAZA", "Board of Peace warns on Gaza",
     "Ceasefire could collapse"),
    (34, "GULF", "Tanker hit by mine near Hormuz",
     "Reported on 18 November"),
    (35, "GULF", "Iran hit US radar in Bahrain",
     "Drone strike reported 18 Nov"),
    (36, "MANILA", "Quad talks open in Manila",
     "Trump joins regional leaders"),
    (37, "SHENZHEN", "Xi speech and state banquet",
     "APEC opens Wednesday"),
    (38, "WORLD", "New START expired in Feb",
     "Nuclear talks top agenda"),
]

# Simplified continent outlines as (lon, lat) points.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-60, 62),
     (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16),
     (-105, 20), (-115, 28), (-125, 40), (-125, 49), (-140, 60), (-165, 60)],
    [(-80, 10), (-60, 8), (-50, 0), (-35, -8), (-40, -20), (-48, -28),
     (-58, -35), (-65, -41), (-70, -52), (-73, -40), (-75, -20), (-80, -5)],
    [(-10, 36), (0, 40), (10, 44), (20, 40), (28, 36), (30, 42), (20, 45),
     (10, 46), (0, 50), (-5, 55), (0, 58), (10, 58), (20, 60), (25, 65),
     (30, 70), (20, 70), (10, 65), (5, 60), (-5, 55), (-10, 50)],
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31), (35, 28),
     (43, 12), (51, 11), (48, 0), (40, -10), (35, -20), (30, -30),
     (20, -35), (15, -30), (12, -18), (9, -5), (9, 4), (-8, 4), (-13, 8)],
    [(30, 70), (60, 70), (90, 75), (120, 73), (150, 70), (170, 66),
     (180, 65), (170, 60), (160, 55), (140, 45), (130, 40), (127, 35),
     (120, 30), (110, 20), (105, 10), (100, 8), (95, 15), (90, 22),
     (80, 8), (75, 15), (70, 25), (60, 25), (55, 28), (50, 30), (45, 30),
     (40, 36), (35, 36), (30, 42)],
    [(113, -22), (125, -15), (135, -12), (142, -11), (150, -20),
     (153, -28), (150, -37), (140, -38), (130, -32), (120, -34), (113, -26)],
]

# (story number, label, lon, lat, label dx, dy, anchor) — dots on the map.
DOTS = [
    (1, "SHENZHEN", 114, 22, 10, -4, "lm"),
    (2, "MANILA", 121, 15, 10, 8, "lm"),
    (3, "KYIV", 30, 50, 9, 9, "lm"),
    (4, "BAHRAIN", 50, 26, 9, 10, "lm"),
    (5, "GAZA", 34, 31, -9, 10, "rm"),
    (8, "DELHI", 77, 29, 10, -10, "lm"),
    (6, "LONDON", 0, 51, -9, -10, "rm"),
    (11, "USA", -100, 39, 0, -12, "mm"),
]


def draw_map(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=SEA, outline=INK, width=2)
    def px(lon, lat):
        x = x0 + 6 + (lon + 170) / 360.0 * (x1 - x0 - 12)
        y = y0 + 4 + (75 - lat) / 135.0 * (y1 - y0 - 8)
        return (x, y)
    for poly in CONTINENTS:
        draw.polygon([px(lon, lat) for lon, lat in poly],
                     fill=LAND, outline=LAND_EDGE)
    small = font(SANS_B, 8)
    for num, label, lon, lat, dx, dy, anchor in DOTS:
        cx, cy = px(lon, lat)
        r = 6
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED,
                     outline=(255, 255, 255), width=1)
        draw.text((cx, cy - 5), str(num), font=font(SANS_B, 8),
                  fill=(255, 255, 255), anchor="mm")
        draw.text((cx + dx, cy + dy), label, font=small, fill=INK,
                  anchor=anchor)


def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    d.rectangle([6, 6, W - 7, H - 7], outline=INK, width=2)

    # ---- Masthead ----
    title = font(SERIF, 56)
    d.text((W // 2, 14), "THE WORLD", font=title, fill=INK, anchor="ma")
    d.line([(16, 72), (W - 16, 72)], fill=INK, width=2)
    # Date band — the date must be unmissable.
    d.rectangle([16, 78, W - 16, 108], fill=RED)
    date_f = font(SANS_B, 22)
    d.text((W // 2, 93), "WEDNESDAY 18 NOVEMBER 2026",
           font=date_f, fill=(255, 255, 255), anchor="mm")
    sub = font(SERIF_R, 13)
    d.text((W // 2, 112),
           "38 stories from six continents — everything that happened today, in one front page",
           font=sub, fill=GREY, anchor="ma")
    d.line([(16, 130), (W - 16, 130)], fill=INK, width=1)

    # ---- Lead story (left) ----
    lx, ly = 16, 140
    lw = 612
    kick = font(SANS_B, 12)
    d.text((lx, ly), "1  LEAD — SUMMIT IN SHENZHEN", font=kick, fill=RED)
    head = font(SERIF, 27)
    headline = "APEC opens as Xi, Trump and Putin head for Shenzhen"
    lines = fit_lines(d, headline, head, lw, 2)
    y = text_block(d, lx, ly + 18, lines, head, INK, 32)
    deck = font(SANS, 12)
    deck_text = ("Xi Jinping chairs the 33rd APEC leaders' meeting, 18–19 Nov. "
                 "Trump lands in Manila for Quad talks, then flies on late "
                 "Wednesday. A first Xi–Trump–Putin three-way is set for Thursday.")
    y = text_block(d, lx, y + 4,
                   fit_lines(d, deck_text, deck, lw, 3), deck, INK, 16) + 6
    # Second lead strip.
    d.rectangle([lx, y, lx + lw, y + 40], fill=LIGHT, outline=INK, width=1)
    d.text((lx + 8, y + 4), "2  TRUMP ARRIVES — LATE WEDNESDAY",
           font=font(SANS_B, 12), fill=RED)
    d.text((lx + 8, y + 22),
           "From Manila to Shenzhen: the US president lands after Quad talks.",
           font=font(SANS, 12), fill=INK)

    # ---- World map (right) ----
    mx0, my0, mx1 = 644, 140, W - 16
    d.text((mx0, my0), "THE WORLD IN ONE MAP", font=kick, fill=BLUE)
    draw_map(d, mx0, my0 + 20, mx1, 298)
    d.text((mx0, 304), "Red dots mark where today's stories happened.",
           font=font(SERIF_R, 11), fill=GREY)

    # ---- Grid header ----
    d.line([(16, 326), (W - 16, 326)], fill=INK, width=2)
    d.text((16, 332), "THE DAY IN 36 MORE STORIES",
           font=font(SANS_B, 13), fill=INK)
    d.text((W - 16, 332), "ALL REPORTED 18 NOVEMBER 2026",
           font=font(SANS_B, 11), fill=RED, anchor="ra")
    d.line([(16, 350), (W - 16, 350)], fill=INK, width=1)

    # ---- Story grid: 6 columns x 6 rows ----
    gx, gy = 16, 354
    cw = (W - 32 - 5 * 6) // 6
    ch = 49
    tag_f = font(SANS_B, 8)
    head_f = font(SANS_B, 11)
    deck_f = font(SANS, 9)
    num_f = font(SANS_B, 11)
    for i, (num, tag, headline, deckline) in enumerate(GRID):
        col, row = i % 6, i // 6
        x = gx + col * (cw + 6)
        yy = gy + row * (ch + 1)
        d.rectangle([x, yy, x + cw, yy + ch - 1], fill=LIGHT,
                    outline=(200, 192, 170), width=1)
        d.text((x + 5, yy + 4), str(num), font=num_f, fill=RED)
        d.text((x + 26, yy + 5), tag, font=tag_f, fill=GREY)
        hl = fit_lines(d, headline, head_f, cw - 10, 2)
        text_block(d, x + 5, yy + 16, hl, head_f, INK, 12)
        deck1 = fit_lines(d, deckline, deck_f, cw - 10, 1)
        if deck1:
            d.text((x + 5, yy + ch - 11), deck1[0], font=deck_f, fill=GREY)

    # ---- Footer ----
    d.line([(16, 660), (W - 16, 660)], fill=INK, width=1)
    d.text((W // 2, 664), "THE WORLD — WEDNESDAY 18 NOVEMBER 2026 · 38 STORIES",
           font=font(SANS_B, 9), fill=GREY, anchor="ma")

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
