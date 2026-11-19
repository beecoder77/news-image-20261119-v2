#!/usr/bin/env python3
"""Build the news-image-20261119 v2 front page (1024x1024 PNG).

Written in this session for the make.fun news-image-20261119 bounty.
Draws a dense newspaper front page for Thursday 19 November 2026 from
40 verified stories (research-19nov.md plus fresh 19 Nov checks), rebuilt
around a drawn world map with numbered markers keyed to the 8 biggest
stories. Uses Pillow locally; the submitted entrypoint main.py is
stdlib-only and simply copies the finished entry.png.
Deterministic: fixed layout, fixed palette, no timestamps, no randomness.
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (251, 246, 233)
INK = (20, 20, 20)
RED = (166, 30, 30)
NAVY = (31, 58, 95)
GREY = (90, 88, 80)
RULE = (60, 58, 50)
OCEAN = (198, 220, 232)
LAND = (232, 222, 196)
LAND_EDGE = (120, 110, 80)
TEAL = (14, 92, 96)
GREEN = (34, 96, 52)
PURPLE = (88, 60, 130)
BROWN = (128, 74, 22)
MAROON = (122, 30, 60)

FDIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FDIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FDIR, "DejaVuSerif.ttf")
SANS_B = os.path.join(FDIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FDIR, "DejaVuSans.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


F_MAST = font(SERIF_B, 40)
F_DATE = font(SANS_B, 17)
F_SUB = font(SANS, 10)
F_KICK = font(SANS_B, 10)
F_LEAD_H = font(SERIF_B, 30)
F_LEAD_D = font(SERIF, 13)
F_LEAD_S = font(SANS, 9)
F_TL_T = font(SANS_B, 10)
F_TL_L = font(SANS, 9)
F_MAP_T = font(SANS_B, 12)
F_LEG = font(SANS, 9)
F_REG = font(SANS_B, 11)
F_HEAD = font(SERIF_B, 12)
F_SUM = font(SANS, 9)
F_NUM_H = font(SERIF_B, 14)
F_NUM = font(SANS, 9)
F_FOOT = font(SANS, 9)
F_CAP = font(SANS_B, 8)


def wrap(draw, text, fnt, width):
    """Wrap text to fit width; return list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_h(draw, lines, fnt, leading):
    return len(lines) * leading


# ---------------------------------------------------------------- stories
# (headline, summary) -- every story verified 19 Nov 2026; see README.
APEC = [
    ("Putin sees 'big potential benefit'",
     "First-ever three-way talks could pay off, he says."),
    ("Handshake before the talks",
     "Trump and Putin greet at the APEC banquet as host Xi looks on."),
    ("Xi pledges openness at APEC",
     "Xi urges free trade; Putin dismisses sanctions."),
    ("Takaichi meets Putin, 30 minutes",
     "Japan's PM holds first face-to-face talks with Russia's leader."),
    ("Canada-China thaw advances",
     "Carney and Xi agree tariff relief on C$400m of exports."),
]
NORTH_AM = [
    ("Democrats take the Senate, 56-44",
     "Peltola wins Alaska; nine GOP seats flipped."),
    ("First Taiwanese American caucus chair",
     "Liu Yunping elected to lead House Democrats."),
    ("Jeffries in line to be first Black speaker",
     "Democrats nominate their leader after the midterm sweep."),
    ("Fed leans to more rate rises",
     "Minutes: most officials see further hikes if inflation stays hot."),
    ("Trump 'unhappy' with Vance on Iran",
     "NYT: president privately praised Rubio instead."),
    ("Huang and Lutnick to testify",
     "Ex-Nvidia chief and commerce secretary to face Senate panel."),
]
LATIN_AM = [
    ("US and Venezuela join drug fight",
     "Hegseth's surprise Caracas trip; forces to cooperate."),
    ("Brazil Senate backs $10bn package",
     "Lula's fiscal plan passes; now to the lower house."),
    ("Mexico bets big on wind",
     "6.86 GW of new wind power planned by 2030."),
]
EUROPE = [
    ("EU: \u20ac45bn Ukraine loan for 2027",
     "Repaid only once Russia pays reparations; \u20ac25bn of it for arms."),
    ("Kerch Bridge span collapses",
     "Ukrainian strikes drop a road arch; rail still stands."),
    ("France: troops sent to Ukraine",
     "Paris confirms soldiers train and maintain weapons there."),
    ("Tanker sinks off Bulgaria",
     "Gas Husky hit by projectiles; all 19 crew rescued."),
    ("Berlin hosts Ukraine summit",
     "Merz brings Macron and Burnham together on guarantees."),
    ("World court rules on Rohingya today",
     "ICJ reads its Myanmar genocide judgment in The Hague."),
]
MIDDLE_EAST = [
    ("Iran widens Gulf attacks",
     "US base in Kuwait hit; Bahrain intercepts strikes a third time."),
    ("US jets hit missile site on Qeshm",
     "Strike answers Iran's attack on a US radar post in Bahrain."),
    ("Saudi all-clear in the south",
     "Danger passed in Jazan, Najran, Khamis Mushait."),
    ("Israel pushes past Gaza 'Yellow Line'",
     "Rare ground operation to clear a 'terror tunnel'; Hamas protests."),
    ("Australia sanctions settlers",
     "Three people and four groups hit over West Bank expansion."),
]
AFRICA = [
    ("Somalia accuses UAE of proxy war",
     "President alleges secret bases; ministry voices 'grave concern'."),
    ("Drugs seized in east Libya",
     "Cocaine and millions of pills seized, officials say."),
]
ASIA_PAC = [
    ("Cyclone Akvan nears India",
     "Severe storm off Andhra; landfall due Friday noon."),
    ("India and Japan in 2+2 talks",
     "Defence ministers review ties in Tokyo."),
    ("Bank Indonesia lifts rates",
     "Surprise 25bp rise to support the rupiah."),
    ("Taiwan counts down to local polls",
     "DPP aims to hold five cities and counties."),
    ("N. Korea enrichment site 'complete'",
     "IAEA: Yongbyon extension externally finished; no access since 2009."),
]
SCIENCE = [
    ("GTA VI is out \u2014 in New Zealand",
     "Rolling midnight launch begins; 16m preorders, $1.5bn banked."),
    ("Nvidia: record $115.8bn quarter",
     "Sales up 103%; first report since founder Huang's resignation."),
    ("Nvidia halts H200 chips to China",
     "Shares fall 4% as board rules out Huang's return."),
    ("Anthropic lists on Nasdaq today",
     "AI firm's shares begin trading after pricing this week."),
    ("Voyager 1, a light-day away",
     "NASA briefs media today on the probe's 25.9bn km milestone."),
    ("Duckett ton seals England series",
     "133 in Hobart; England win the ODI decider by 97 runs."),
    ("Curry: knee damage irreversible",
     "Star reveals cartilage degeneration; out about a month."),
]

NUMBERS = [
    ("\u20ac45bn", "EU loan proposed for Ukraine in 2027"),
    ("$115.8bn", "Nvidia Q3 revenue, up 103% YoY"),
    ("25.9bn km", "Voyager 1 from Earth: one light-day"),
    ("56\u201344", "Democrats' new US Senate majority"),
    ("1.2m", "Rohingya await the ICJ ruling"),
    ("90\u2013100 km/h", "Cyclone Akvan winds, gusting 110"),
]

TIMELINE = [
    ("00:00 NZDT", "GTA VI unlocks in NZ"),
    ("05:30 IST", "Cyclone Akvan off India"),
    ("TODAY", "ICJ reads Myanmar ruling"),
    ("12:00 EST", "NASA Voyager briefing"),
    ("TODAY", "APEC trilateral, Shenzhen"),
    ("TODAY", "Berlin Ukraine summit"),
]

# Map markers: (number, lon, lat, short key) -- keyed to the story list.
MARKERS = [
    (1, 114.0, 22.5, "Shenzhen: first-ever Trump\u2013Xi\u2013Putin talks"),
    (2, 4.3, 52.0, "The Hague: ICJ rules on Rohingya"),
    (3, -77.0, 39.0, "Washington: Democrats take the Senate"),
    (4, 36.5, 45.3, "Kerch Strait: bridge span down"),
    (5, 50.5, 26.0, "The Gulf: Iran widens attacks"),
    (6, 82.0, 16.0, "Andhra coast: Cyclone Akvan"),
    (7, 16.0, 49.0, "Berlin: Ukraine guarantees summit"),
    (8, -62.0, 30.0, "New York: Anthropic lists on Nasdaq"),
]

# ---------------------------------------------------------------- world map
# Simplified continent outlines in (lon, lat). Rough but recognisable.
NORTH_AMERICA_POLY = [(-168, 66), (-155, 71), (-140, 70), (-128, 71), (-115, 73),
                 (-100, 73), (-90, 74), (-82, 66), (-80, 73), (-70, 62),
                 (-65, 60), (-60, 55), (-55, 52), (-60, 47), (-65, 44),
                 (-70, 42), (-74, 39), (-76, 35), (-80, 32), (-81, 26),
                 (-84, 30), (-89, 29), (-91, 19), (-95, 16), (-97, 16),
                 (-105, 20), (-110, 23), (-114, 28), (-117, 33), (-122, 37),
                 (-124, 42), (-124, 48), (-130, 54), (-140, 60), (-150, 61),
                 (-158, 58), (-165, 60)]
GREENLAND_POLY = [(-58, 64), (-52, 60), (-44, 60), (-40, 64), (-32, 68),
             (-25, 70), (-20, 74), (-25, 78), (-40, 80), (-55, 76),
             (-60, 74), (-62, 70)]
SOUTH_AMERICA_POLY = [(-79, 9), (-72, 12), (-64, 11), (-60, 8), (-52, 5),
                 (-44, 2), (-35, -6), (-35, -9), (-40, -15), (-40, -22),
                 (-48, -27), (-52, -32), (-58, -35), (-62, -39), (-65, -45),
                 (-68, -50), (-70, -54), (-74, -50), (-73, -44), (-72, -37),
                 (-70, -30), (-70, -20), (-75, -15), (-80, -8), (-81, -4),
                 (-80, 1)]
EUROPE_POLY = [(-10, 36), (-9, 38), (-9, 43), (-2, 44), (-1, 46), (-4, 48),
          (-2, 50), (2, 51), (4, 53), (7, 54), (8, 57), (10, 59), (12, 58),
          (18, 56), (21, 55), (21, 58), (24, 59), (28, 60), (30, 62),
          (30, 66), (28, 71), (24, 71), (20, 70), (15, 68), (12, 66),
          (8, 62), (5, 60), (5, 58), (0, 58), (-3, 58), (-5, 56), (-6, 55),
          (-5, 53), (-3, 53), (-5, 50), (-2, 49), (-5, 48), (-2, 47),
          (-1, 44), (0, 42), (3, 42), (7, 44), (10, 44), (12, 44),
          (15, 44), (18, 40), (19, 42), (23, 40), (23, 36), (26, 38),
          (28, 41), (30, 40), (28, 38), (26, 36), (23, 36), (20, 38),
          (15, 38), (12, 38), (8, 39), (3, 38), (-1, 36), (-6, 36)]
AFRICA_POLY = [(-17, 15), (-16, 20), (-13, 27), (-9, 31), (-5, 35), (0, 36),
          (5, 37), (10, 37), (15, 32), (20, 32), (25, 31), (30, 31),
          (32, 31), (35, 28), (37, 22), (39, 18), (40, 15), (43, 12),
          (48, 11), (51, 12), (51, 10), (48, 5), (44, 0), (40, -5),
          (40, -10), (37, -15), (35, -20), (33, -25), (32, -28), (28, -32),
          (25, -34), (20, -35), (17, -32), (15, -27), (13, -20), (12, -15),
          (13, -10), (12, -5), (9, 0), (9, 4), (6, 4), (2, 6), (-4, 5),
          (-8, 5), (-13, 8), (-16, 12)]
ASIA_POLY = [(26, 36), (30, 36), (36, 36), (40, 38), (44, 39), (48, 40),
        (50, 42), (55, 44), (58, 46), (62, 48), (66, 50), (70, 52),
        (75, 55), (80, 58), (85, 62), (90, 66), (95, 70), (100, 72),
        (105, 74), (110, 74), (115, 73), (120, 73), (125, 72), (130, 71),
        (135, 71), (140, 72), (145, 72), (150, 70), (155, 68), (160, 66),
        (165, 66), (170, 67), (178, 65), (178, 62), (172, 60), (168, 60),
        (162, 58), (158, 53), (156, 51), (150, 59), (142, 55), (142, 50),
        (140, 45), (138, 43), (135, 40), (132, 38), (129, 35), (127, 35),
        (126, 38), (124, 40), (122, 38), (120, 35), (120, 31), (118, 28),
        (116, 24), (113, 22), (110, 20), (108, 18), (108, 13), (106, 10),
        (104, 9), (103, 7), (100, 7), (98, 10), (97, 15), (95, 16),
        (93, 18), (91, 22), (89, 22), (87, 21), (85, 19), (82, 17),
        (80, 15), (80, 13), (77, 8), (76, 10), (75, 13), (73, 16),
        (72, 20), (70, 21), (68, 23), (66, 25), (64, 25), (62, 25),
        (60, 25), (58, 26), (56, 27), (54, 27), (52, 27), (51, 29),
        (50, 29), (48, 30), (46, 29), (44, 29), (42, 30), (40, 31),
        (39, 32), (37, 34), (35, 35), (33, 35), (30, 36)]
AUSTRALIA_POLY = [(113, -22), (114, -28), (115, -32), (116, -35), (120, -34),
             (124, -33), (129, -32), (132, -32), (135, -35), (137, -35),
             (140, -38), (142, -39), (145, -38), (147, -39), (150, -37),
             (153, -32), (153, -28), (152, -24), (150, -22), (148, -20),
             (146, -19), (143, -15), (142, -11), (141, -13), (137, -12),
             (135, -15), (132, -12), (130, -13), (128, -14), (126, -14),
             (124, -16), (122, -17), (120, -19), (117, -20), (114, -21)]
NEW_ZEALAND_POLY = [(167, -45), (170, -42), (173, -40), (175, -38), (177, -38),
               (178, -37), (176, -40), (174, -41), (172, -43), (169, -46)]
UNITED_KINGDOM_POLY = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57),
                  (0, 53), (1, 51)]
JAPAN_POLY = [(130, 31), (132, 33), (134, 34), (136, 35), (138, 35), (140, 37),
         (141, 39), (141, 41), (142, 43), (144, 44), (143, 42), (141, 39),
         (139, 37), (137, 37), (135, 34), (133, 34), (131, 33)]
BORNEO_POLY = [(109, 1), (111, 2), (114, 4), (117, 6), (119, 1), (117, -2),
          (114, -3), (110, -3)]
SUMATRA_POLY = [(95, 5), (98, 3), (101, 0), (104, -3), (106, -6), (104, -5),
           (100, -1), (97, 2)]
NEW_GUINEA_POLY = [(131, -1), (135, -2), (138, -3), (141, -4), (145, -6),
              (147, -7), (150, -9), (147, -8), (143, -8), (140, -8),
              (136, -6), (132, -3)]
MADAGASCAR_POLY = [(44, -16), (47, -15), (50, -16), (49, -20), (47, -24),
              (45, -25), (43, -22), (43, -18)]
ICELAND_POLY = [(-22, 64), (-18, 63), (-15, 64), (-14, 66), (-18, 66),
           (-22, 65)]
CONTINENTS = [NORTH_AMERICA_POLY, GREENLAND_POLY, SOUTH_AMERICA_POLY,
              EUROPE_POLY, AFRICA_POLY, ASIA_POLY, AUSTRALIA_POLY,
              NEW_ZEALAND_POLY, UNITED_KINGDOM_POLY, JAPAN_POLY,
              BORNEO_POLY, SUMATRA_POLY, NEW_GUINEA_POLY, MADAGASCAR_POLY,
              ICELAND_POLY]


def project(lon, lat, x0, y0, x1, y1):
    """Equirectangular: lon -180..180, lat 85..-58 -> panel rect."""
    x = x0 + (lon + 180.0) / 360.0 * (x1 - x0)
    y = y0 + (85.0 - lat) / 143.0 * (y1 - y0)
    return (x, y)


def draw_map(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=OCEAN, outline=RULE, width=1)
    # faint graticule
    for lon in range(-150, 181, 30):
        gx, _ = project(lon, 0, x0, y0, x1, y1)
        draw.line([(gx, y0), (gx, y1)], fill=(215, 230, 238), width=1)
    for lat in (60, 30, 0, -30):
        _, gy = project(0, lat, x0, y0, x1, y1)
        draw.line([(x0, gy), (x1, gy)], fill=(215, 230, 238), width=1)
    for poly in CONTINENTS:
        pts = [project(lon, lat, x0, y0, x1, y1) for lon, lat in poly]
        draw.polygon(pts, fill=LAND, outline=LAND_EDGE)
    # equator label
    _, eq = project(0, 0, x0, y0, x1, y1)
    draw.text((x0 + 4, eq - 12), "EQUATOR", font=F_CAP, fill=(110, 130, 140))
    for num, lon, lat, _key in MARKERS:
        mx, my = project(lon, lat, x0, y0, x1, y1)
        r = 9
        draw.ellipse([mx - r, my - r, mx + r, my + r], fill=RED,
                     outline=(255, 255, 255), width=2)
        label = str(num)
        tw = draw.textlength(label, font=F_SANS_B if False else font(SANS_B, 10))
        draw.text((mx - tw / 2, my - 7), label, font=font(SANS_B, 10),
                  fill=(255, 255, 255))


# ---------------------------------------------------------------- panels
def draw_lead_panel(draw, x0, y0, x1, y1):
    """Shenzhen dusk skyline, three leaders seated at a table."""
    draw.rectangle([x0, y0, x1, y1], fill=(24, 30, 58))
    # sky glow
    draw.rectangle([x0, y1 - 52, x1, y1], fill=(196, 88, 44))
    # skyline blocks
    towers = [(0, 46, 26, 84), (30, 30, 52, 84), (56, 52, 78, 84),
              (82, 22, 104, 84), (108, 40, 128, 84), (132, 30, 152, 84),
              (156, 48, 176, 84), (180, 26, 202, 84), (206, 44, 226, 84),
              (230, 34, 252, 84), (256, 50, 276, 84), (280, 28, 300, 84),
              (304, 42, 326, 84), (330, 36, 352, 84), (356, 48, 376, 84)]
    for dx, top, dx2, _bot in towers:
        draw.rectangle([x0 + dx, y0 + top, x0 + dx2, y1 - 8], fill=(12, 16, 34))
    # lit windows
    for wx in range(x0 + 8, x1 - 6, 14):
        for wy in range(y0 + 30, y1 - 20, 12):
            if (wx * 7 + wy * 13) % 5 < 2:
                draw.rectangle([wx, wy, wx + 4, wy + 6], fill=(255, 196, 90))
    # ground
    draw.rectangle([x0, y1 - 8, x1, y1], fill=(10, 12, 26))
    # table
    cx = (x0 + x1) // 2
    ty = y1 - 34
    draw.ellipse([cx - 118, ty, cx + 118, ty + 22], fill=(122, 52, 34))
    draw.ellipse([cx - 118, ty, cx + 118, ty + 10], fill=(168, 74, 44))
    # three seated figures: navy, red, dark grey suits
    for i, (dx, shirt, suit) in enumerate(
            [(-72, (40, 70, 140), (24, 32, 66)),
             (0, (178, 44, 44), (90, 22, 22)),
             (72, (90, 90, 96), (36, 36, 40))]):
        fx = cx + dx
        draw.ellipse([fx - 15, ty - 62, fx + 15, ty - 32], fill=(232, 196, 160))
        draw.polygon([(fx - 24, ty - 6), (fx - 20, ty - 34), (fx - 8, ty - 38),
                      (fx + 8, ty - 38), (fx + 20, ty - 34), (fx + 24, ty - 6)],
                     fill=suit)
        draw.polygon([(fx - 7, ty - 38), (fx + 7, ty - 38), (fx + 4, ty - 14),
                      (fx - 4, ty - 14)], fill=shirt)
    # flags on the table: three small pennants
    for i, col in enumerate([(40, 70, 140), (178, 44, 44), (90, 90, 96)]):
        px = cx - 30 + i * 30
        draw.line([(px, ty - 2), (px, ty - 18)], fill=(220, 220, 210), width=2)
        draw.polygon([(px, ty - 18), (px + 16, ty - 14), (px, ty - 10)],
                     fill=col)


def draw_bridge_panel(draw, x0, y0, x1, y1):
    """Kerch Bridge: deck with a collapsed span dropped into the sea."""
    draw.rectangle([x0, y0, x1, y1], fill=(214, 228, 236))
    sea_y = y0 + (y1 - y0) * 2 // 3
    draw.rectangle([x0, sea_y, x1, y1], fill=(64, 110, 150))
    for wx in range(x0 + 6, x1 - 4, 22):
        draw.arc([wx, sea_y + 6, wx + 16, sea_y + 14], 0, 180,
                 fill=(220, 235, 245), width=2)
    # pylons
    for px in (x0 + 52, x1 - 52):
        draw.rectangle([px - 3, y0 + 4, px + 3, sea_y], fill=(90, 88, 84))
        draw.line([(px, y0 + 4), (x0 + 20, y0 + 16)], fill=(90, 88, 84), width=2)
        draw.line([(px, y0 + 4), (x1 - 20, y0 + 16)], fill=(90, 88, 84), width=2)
    # deck, left and right of the gap
    deck_y = y0 + 14
    draw.rectangle([x0, deck_y, x0 + 118, deck_y + 6], fill=(70, 68, 64))
    draw.rectangle([x1 - 118, deck_y, x1, deck_y + 6], fill=(70, 68, 64))
    # fallen span, tilted into the water
    draw.polygon([(x0 + 118, deck_y), (x1 - 118, deck_y + 6),
                  (x1 - 128, deck_y + 16), (x0 + 128, deck_y + 10)],
                 fill=(120, 40, 36))


def draw_cyclone_panel(draw, x0, y0, x1, y1):
    """Cyclone Akvan: spiral over the Bay of Bengal, arrow to the coast."""
    draw.rectangle([x0, y0, x1, y1], fill=(206, 224, 232))
    # coast line on the right
    draw.polygon([(x1 - 58, y0), (x1, y0), (x1, y1), (x1 - 44, y1),
                  (x1 - 52, y0 + (y1 - y0) // 2)], fill=(232, 222, 196),
                 outline=LAND_EDGE)
    cx, cy = x0 + 56, y0 + (y1 - y0) // 2 + 1
    for r in (18, 13, 8):
        draw.arc([cx - r, cy - r, cx + r, cy + r], 20, 300,
                 fill=(30, 60, 120), width=3)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
    # track arrow toward the coast
    draw.line([(cx + 20, cy + 4), (x1 - 62, cy - 4)], fill=RED, width=2)
    draw.polygon([(x1 - 62, cy - 4), (x1 - 74, cy - 9), (x1 - 74, cy + 1)],
                 fill=RED)


def draw_voyager_panel(draw, x0, y0, x1, y1):
    """Voyager 1: starfield, probe, and the one-light-day line."""
    draw.rectangle([x0, y0, x1, y1], fill=(10, 12, 26))
    for sx in range(x0 + 8, x1 - 4, 17):
        for sy in range(y0 + 5, y1 - 5, 13):
            if (sx * 11 + sy * 7) % 4 == 0:
                draw.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
    # probe body + dish + boom
    px, py = x0 + 120, y0 + (y1 - y0) // 2
    draw.rectangle([px - 14, py - 6, px + 14, py + 6], fill=(200, 200, 205))
    draw.ellipse([px + 12, py - 12, px + 34, py + 12], outline=(230, 230, 235),
                 width=2)
    draw.line([(px - 14, py), (px - 34, py - 10)], fill=(200, 200, 205), width=2)
    draw.line([(px, py + 6), (px + 8, py + 18)], fill=(200, 200, 205), width=2)
    # signal line to Earth
    draw.line([(px + 34, py), (x1 - 58, py + 4)], fill=(255, 196, 90), width=2)
    draw.ellipse([x1 - 52, py - 2, x1 - 40, py + 10], fill=(70, 130, 190))

# ---------------------------------------------------------------- layout
BRIEFS = {"Huang and Lutnick to testify", "Mexico bets big on wind",
          "Tanker sinks off Bulgaria", "Saudi all-clear in the south",
          "India and Japan in 2+2 talks", "Duckett ton seals England series",
          "Drugs seized in east Libya", "Canada-China thaw advances",
          "Curry: knee damage irreversible",
          "Anthropic lists on Nasdaq today", "Bank Indonesia lifts rates",
          "Taiwan counts down to local polls", "N. Korea enrichment site 'complete'"}

REGION_COLORS = {
    "APEC & THE SUMMIT": NAVY, "NORTH AMERICA": RED,
    "LATIN AMERICA": GREEN, "EUROPE": PURPLE,
    "MIDDLE EAST": BROWN, "AFRICA": MAROON,
    "ASIA-PACIFIC": TEAL, "SCIENCE, TECH & SPORT": (40, 40, 44),
}

COLS = [
    [("region", "APEC & THE SUMMIT", APEC),
     ("region", "NORTH AMERICA", NORTH_AM),
     ("numbers",)],
    [("region", "EUROPE", EUROPE),
     ("panel", "bridge"),
     ("region", "MIDDLE EAST", MIDDLE_EAST),
     ("region", "AFRICA", AFRICA)],
    [("region", "LATIN AMERICA", LATIN_AM),
     ("region", "ASIA-PACIFIC", ASIA_PAC),
     ("panel", "cyclone"),
     ("region", "SCIENCE, TECH & SPORT", SCIENCE),
     ("panel", "voyager")],
]
COL_X = [(14, 342), (350, 678), (686, 1010)]
STORY_Y0, STORY_Y1 = 506, 992


def story_height(draw, headline, summary, width):
    hl = wrap(draw, headline, F_HEAD, width)
    h = len(hl) * 14
    if summary:
        sl = wrap(draw, summary, F_SUM, width)
        h += len(sl) * 11
    return h


def block_height(draw, block, width):
    kind = block[0]
    if kind == "region":
        h = 19 + 3
        for headline, summary in block[2]:
            h += story_height(draw, headline,
                              "" if headline in BRIEFS else summary, width)
            h += 3
        return h
    if kind == "panel":
        return 36
    if kind == "numbers":
        return 18 + len(NUMBERS) * 21 + 4
    return 0


def draw_region(draw, x0, width, y, title, stories, gap_extra):
    color = REGION_COLORS[title]
    draw.rectangle([x0, y, x0 + width, y + 17], fill=color)
    draw.text((x0 + 6, y + 3), title, font=F_REG, fill=(255, 255, 255))
    count = str(len(stories))
    tw = draw.textlength(count, font=F_REG)
    draw.text((x0 + width - tw - 6, y + 3), count, font=F_REG,
              fill=(255, 255, 255))
    y += 19
    for headline, summary in stories:
        if headline in BRIEFS:
            summary = ""
        hl = wrap(draw, headline, F_HEAD, width)
        for line in hl:
            draw.text((x0, y), line, font=F_HEAD, fill=INK)
            y += 14
        if summary:
            sl = wrap(draw, summary, F_SUM, width)
            for line in sl:
                draw.text((x0, y), line, font=F_SUM, fill=(60, 58, 52))
                y += 11
        y += 3 + gap_extra
        draw.line([(x0, y - 2), (x0 + width, y - 2)], fill=(214, 208, 192),
                  width=1)
    return y


def draw_numbers(draw, x0, width, y):
    draw.rectangle([x0, y, x0 + width, y + 17], fill=(20, 20, 20))
    draw.text((x0 + 6, y + 3), "BY THE NUMBERS", font=F_REG,
              fill=(255, 255, 255))
    y += 19
    for value, label in NUMBERS:
        draw.text((x0, y), value, font=F_NUM_H, fill=RED)
        vw = draw.textlength(value, font=F_NUM_H)
        draw.text((x0 + vw + 8, y + 3), label, font=F_NUM, fill=INK)
        y += 21
    return y


def draw_column(draw, idx, blocks):
    x0, x1 = COL_X[idx]
    width = x1 - x0
    total = sum(block_height(draw, b, width) for b in blocks)
    avail = STORY_Y1 - STORY_Y0
    n_stories = sum(len(b[2]) for b in blocks if b[0] == "region")
    slack = avail - total
    gap_extra = max(0.0, slack / max(1, n_stories)) if slack > 0 else 0.0
    if slack < 0:
        print(f"WARNING column {idx} overflows by {-slack:.0f}px",
              file=sys.stderr)
    y = STORY_Y0
    for block in blocks:
        if block[0] == "region":
            y = draw_region(draw, x0, width, y, block[1], block[2], gap_extra)
        elif block[0] == "panel":
            if block[1] == "bridge":
                draw_bridge_panel(draw, x0, int(y), x1, int(y) + 36)
            elif block[1] == "cyclone":
                draw_cyclone_panel(draw, x0, int(y), x1, int(y) + 36)
            elif block[1] == "voyager":
                draw_voyager_panel(draw, x0, int(y), x1, int(y) + 36)
            y += 38
        elif block[0] == "numbers":
            y = draw_numbers(draw, x0, width, y)
    return y


def build(out_path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.text((14, 8), "No. 323", font=F_SUB, fill=GREY)
    d.text((14, 24), "SHENZHEN \u00b7 THE HAGUE \u00b7 NEW YORK", font=F_SUB,
           fill=GREY)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=F_MAST)
    d.text(((W - tw) / 2, 6), title, font=F_MAST, fill=INK)
    d.text((W - 14 - d.textlength("40 STORIES \u00b7 8 REGIONS", font=F_SUB),
            8), "40 STORIES \u00b7 8 REGIONS", font=F_SUB, fill=GREY)
    d.text((W - 14 - d.textlength("ALL TIMES UTC", font=F_SUB), 24),
           "ALL TIMES UTC", font=F_SUB, fill=GREY)
    d.line([(14, 58), (1010, 58)], fill=INK, width=3)

    # ---- date band
    d.rectangle([14, 64, 1010, 96], fill=RED)
    date = "THURSDAY  19  NOVEMBER  2026"
    tw = d.textlength(date, font=F_DATE)
    d.text(((W - tw) / 2, 72), date, font=F_DATE, fill=(255, 255, 255))
    sub = "The world in one page \u2014 every story below happened or was first reported today"
    tw = d.textlength(sub, font=F_SUB)
    d.text(((W - tw) / 2, 100), sub, font=F_SUB, fill=GREY)

    # ---- lead story + illustration
    d.text((14, 116), "THE DAY'S BIG STORY  \u2014  SHENZHEN", font=F_KICK,
           fill=RED)
    lead_lines = wrap(d, "THREE LEADERS, ONE TABLE", F_LEAD_H, 580)
    ly = 132
    for line in lead_lines:
        d.text((14, ly), line, font=F_LEAD_H, fill=INK)
        ly += 34
    deck = ("Trump, Xi and Putin meet today in Shenzhen \u2014 the first "
            "trilateral of the three powers. One hour is set aside; "
            "nuclear arms, the Iran war and Ukraine on the agenda. "
            "Commentators call it a \u201cnew Yalta\u201d.")
    dl = wrap(d, deck, F_LEAD_D, 580)
    dy = ly + 2
    for line in dl:
        d.text((14, dy), line, font=F_LEAD_D, fill=(40, 40, 40))
        dy += 17
    d.text((14, dy + 4), "Kremlin: no full-scale Trump\u2013Putin talks "
           "planned.  \u00b7  Reuters", font=F_LEAD_S, fill=GREY)
    draw_lead_panel(d, 612, 116, 1010, 244)

    # ---- UTC timeline strip
    d.rectangle([14, 250, 1010, 286], fill=NAVY)
    d.text((22, 254), "THE DAY IN UTC", font=F_TL_T, fill=(255, 196, 90))
    cell_w = (1010 - 14 - 150) / len(TIMELINE)
    for i, (when, what) in enumerate(TIMELINE):
        cx = 14 + 150 + i * cell_w
        if i:
            d.line([(cx, 254), (cx, 282)], fill=(90, 120, 160), width=1)
        d.text((cx + 8, 254), when, font=F_TL_T, fill=(255, 255, 255))
        wl = wrap(d, what, F_TL_L, cell_w - 16)
        wy = 268
        for line in wl[:1]:
            d.text((cx + 8, wy), line, font=F_TL_L, fill=(200, 214, 230))
            wy += 11

    # ---- world map panel: map left, numbered key right
    d.text((14, 292), "THE WORLD TODAY \u2014 ON THE MAP",
           font=F_MAP_T, fill=INK)
    draw_map(d, 14, 310, 654, 500)
    kx0, kx1 = 662, 1010
    d.rectangle([kx0, 310, kx1, 500], outline=RULE, width=1)
    d.rectangle([kx0, 310, kx1, 330], fill=NAVY)
    d.text((kx0 + 8, 314), "ON THE MAP \u2014 8 BIGGEST STORIES",
           font=F_MAP_T, fill=(255, 255, 255))
    ky = 336
    for num, _lo, _la, key in MARKERS:
        r = 8
        cx = kx0 + 14
        d.ellipse([cx - r, ky - r + 6, cx + r, ky + r + 6], fill=RED,
                  outline=(255, 255, 255), width=1)
        label = str(num)
        tw = d.textlength(label, font=font(SANS_B, 9))
        d.text((cx - tw / 2, ky - 1), label, font=font(SANS_B, 9),
               fill=(255, 255, 255))
        d.text((kx0 + 30, ky), key, font=F_LEG, fill=INK)
        ky += 20

    # ---- story columns
    for i, blocks in enumerate(COLS):
        draw_column(d, i, blocks)

    # ---- footer
    d.line([(14, 996), (1010, 996)], fill=INK, width=2)
    foot = ("40 stories. One day. Compiled 19 Nov 2026.  \u00b7  Sources: "
            "Reuters, AP, BBC, FT, SCMP, PBS, IMD, NASA, ESPNcricinfo, "
            "Japan Today  \u00b7  All times UTC")
    d.text((14, 1002), foot, font=F_FOOT, fill=GREY)

    img.save(out_path, "PNG", optimize=True)
    size = os.path.getsize(out_path)
    print(f"wrote {out_path} ({size} bytes, {W}x{H})")
    return size


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    build(target)
