"""Render the news-25-b27-numbers front page (1024x640) with Pillow.

Build-time only. The grader never runs this file; main.py (stdlib only)
copies the committed entry.png to MAKEFUN_OUTPUT_DIR.
"""

import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 640
OUT = "entry.png"

NAVY = (20, 33, 61)
RED = (193, 39, 45)
TEAL = (14, 124, 123)
GOLD = (176, 124, 12)
INK = (24, 24, 24)
GREY = (110, 110, 110)
PAPER = (250, 247, 240)
CARD = (255, 255, 255)
LINE = (200, 196, 188)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    try:
        return ImageFont.truetype(FONT_DIR + name, size)
    except OSError:
        return ImageFont.load_default()


F_TITLE = font("DejaVuSans-Bold.ttf", 30)
F_DATE = font("DejaVuSans-Bold.ttf", 15)
F_META = font("DejaVuSans.ttf", 12)
F_BIGNUM = font("DejaVuSans-Bold.ttf", 46)
F_HEAD = font("DejaVuSans-Bold.ttf", 15)
F_WHY = font("DejaVuSans.ttf", 11)
F_ALSO = font("DejaVuSans.ttf", 10)
F_TABLE_HEAD = font("DejaVuSans-Bold.ttf", 13)
F_ROW = font("DejaVuSans.ttf", 11)
F_BADGE = font("DejaVuSans-Bold.ttf", 10)
F_TAG = font("DejaVuSans-Bold.ttf", 10)
F_SCENE = font("DejaVuSans-Bold.ttf", 11)

HEROES = [
    {
        "num": "20%",
        "color": RED,
        "head": "TRUMP HITS 14 PARTNERS WITH NEW TARIFFS, CHINA AT 20%",
        "why": ("WHY IT MATTERS: Higher import costs will ripple through "
                "global supply chains and could push consumer prices up "
                "around the world."),
        "also": "ALSO: Allies seek exemptions as talks open this week.",
        "scene": "14 PARTNERS NAMED",
    },
    {
        "num": "-6.16%",
        "color": TEAL,
        "head": "AI CHIP SELLOFF SINKS KOSPI TO 4,697.51",
        "why": ("WHY IT MATTERS: The selloff wipes out weeks of AI-chip "
                "gains and signals investor doubt about sky-high chip "
                "valuations."),
        "also": "ALSO: Samsung -9.87%, SK Hynix -11.05% in Seoul rout.",
        "scene": "KOSPI 4,697.51",
    },
    {
        "num": "1ST",
        "color": GOLD,
        "head": "SHENZHOU-24 CARRIES FIRST FOREIGN ASTRONAUT TO TIANGONG",
        "why": ("WHY IT MATTERS: China opens its space station to "
                "international partners, marking a new era of crewed "
                "space diplomacy."),
        "also": "ALSO: Muhammad Zeeshan Ali of Pakistan joins the crew.",
        "scene": "TIANGONG STATION",
    },
]

# (region, tag C/R/CL, headline) -- 47 rows, badge = row number 01..47
ROWS = [
    ("US", "C", "White House defends tariff plan"),
    ("US", "R", "Fed hints at slower pace of cuts"),
    ("US", "C", "Thanksgiving travel sets records"),
    ("US", "R", "US stocks slide as chips sell off"),
    ("US", "C", "Grid braces for AI power demand"),
    ("CHINA", "C", "Beijing vows reply to tariffs"),
    ("CHINA", "R", "China chipmakers rally on push"),
    ("CHINA", "C", "China cargo run heads to Tiangong"),
    ("CHINA", "R", "Yuan steadies after tariff news"),
    ("KOREA", "C", "Seoul backs chip supply chain"),
    ("KOREA", "R", "Samsung weighs output cuts"),
    ("KOREA", "C", "Korea chip orders cool, data show"),
    ("INDONESIA", "C", "Bogor mine: 9 dead, 17 trapped"),
    ("INDONESIA", "R", "Rescue race for trapped miners"),
    ("INDONESIA", "C", "Jakarta watches rupiah slide"),
    ("INDONESIA", "R", "Indonesia weighs tariff response"),
    ("EUROPE", "C", "EU leaders split on retaliation"),
    ("EUROPE", "R", "Euro slips as trade tensions rise"),
    ("EUROPE", "C", "COP31 talks enter final stretch"),
    ("EUROPE", "R", "UK inflation eases, cut bets grow"),
    ("MIDDLE EAST", "C", "Oil steadies amid tariff fears"),
    ("MIDDLE EAST", "R", "Gulf states court AI chip cash"),
    ("MIDDLE EAST", "C", "Gaza ceasefire talks resume"),
    ("SPACE", "C", "Ali trains for Tiangong mission"),
    ("SPACE", "R", "Satellite launch set for Dec"),
    ("SPACE", "C", "Moon crews rehearse landing"),
    ("MARKETS", "C", "Gold climbs as haven demand grows"),
    ("MARKETS", "R", "Bitcoin steadies after wild week"),
    ("MARKETS", "C", "Bond yields fall on growth fears"),
    ("MARKETS", "R", "Copper slides on weak China outlook"),
    ("TECH", "C", "AI chip stocks lead market rout"),
    ("TECH", "R", "Nvidia suppliers feel the heat"),
    ("TECH", "C", "Open-source AI gains in Asia"),
    ("TECH", "R", "Chip gear orders slow, makers warn"),
    ("CLIMATE", "C", "Antalya pushes climate finance deal"),
    ("CLIMATE", "R", "Floods hit SE Asia after rains"),
    ("CLIMATE", "C", "Renewables pass coal in new build"),
    ("US", "C", "Holiday shoppers hunt for deals"),
    ("CHINA", "R", "EV makers cut prices for year-end"),
    ("KOREA", "C", "K-pop tour tickets sell out fast"),
    ("INDONESIA", "C", "Jakarta floods test monsoon walls"),
    ("EUROPE", "R", "German factories cut shifts"),
    ("MIDDLE EAST", "C", "Dubai air show draws record orders"),
    ("SPACE", "R", "Debris warning closes launch window"),
    ("MARKETS", "C", "Dollar firms as haven demand grows"),
    ("TECH", "C", "Robotaxi fleets reach new cities"),
    ("CLIMATE", "R", "Coral study warns of reef bleaching"),
]

assert len(ROWS) == 47, len(ROWS)
assert len({r[0] for r in ROWS}) == 10, {r[0] for r in ROWS}


def wrap(draw, text, fnt, width):
    """Wrap text to fit width in pixels; returns list of lines."""
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


def draw_hero(draw, x, y, w, h, hero):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=6,
                           fill=CARD, outline=LINE, width=1)
    pad = 12
    cx = x + pad
    cy = y + 10
    # Big number gets its own space at the top, never over the headline.
    draw.text((cx, cy), hero["num"], font=F_BIGNUM, fill=hero["color"])
    cy += 56
    for line in wrap(draw, hero["head"], F_HEAD, w - 2 * pad):
        draw.text((cx, cy), line, font=F_HEAD, fill=NAVY)
        cy += 19
    cy += 4
    for line in wrap(draw, hero["why"], F_WHY, w - 2 * pad):
        draw.text((cx, cy), line, font=F_WHY, fill=INK)
        cy += 14
    cy += 3
    for line in wrap(draw, hero["also"], F_ALSO, w - 2 * pad):
        draw.text((cx, cy), line, font=F_ALSO, fill=GREY)
        cy += 13
    # Mini scene strip at the bottom of the card.
    sy = y + h - 30
    draw.rectangle([x + 1, sy, x + w - 1, y + h - 1], fill=hero["color"])
    label = hero["scene"]
    tw = draw.textlength(label, font=F_SCENE)
    draw.text((x + (w - tw) / 2, sy + 7), label, font=F_SCENE,
              fill=(255, 255, 255))
    return cy


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- Masthead ------------------------------------------------------
    draw.text((16, 10), "THE WORLD IN NUMBERS", font=F_TITLE, fill=NAVY)
    right = "50 STORIES  •  10 REGIONS"
    draw.text((W - 16 - draw.textlength(right, font=F_META), 20),
              right, font=F_META, fill=GREY)
    draw.text((16, 44), "DATE CHECK  —  Wednesday 25 November 2026",
              font=F_DATE, fill=RED)
    draw.line([(16, 66), (W - 16, 66)], fill=NAVY, width=2)

    # ---- Hero trio -----------------------------------------------------
    hero_y, hero_h = 76, 218
    hero_w = (W - 32 - 16) // 3
    for i, hero in enumerate(HEROES):
        draw_hero(draw, 16 + i * (hero_w + 8), hero_y, hero_w, hero_h, hero)

    # ---- Numbers table: 47 more stories -------------------------------
    ty = hero_y + hero_h + 12
    draw.text((16, ty), "THE NUMBERS  —  47 MORE STORIES",
              font=F_TABLE_HEAD, fill=NAVY)
    draw.line([(16, ty + 20), (W - 16, ty + 20)], fill=LINE, width=1)

    rows_top = ty + 28
    row_h = 19
    col_w = (W - 32 - 16) // 3
    tag_colors = {"C": RED, "R": TEAL, "CL": GOLD}
    for idx, (region, tag, head) in enumerate(ROWS):
        col = idx // 16
        row = idx % 16
        x = 16 + col * (col_w + 8)
        y = rows_top + row * row_h
        # Number badge.
        badge = "%02d" % (idx + 1)
        draw.rounded_rectangle([x, y + 2, x + 24, y + 16], radius=3,
                               fill=NAVY)
        bw = draw.textlength(badge, font=F_BADGE)
        draw.text((x + (24 - bw) / 2, y + 4), badge, font=F_BADGE,
                  fill=(255, 255, 255))
        # Headline, clipped to the column so nothing is cut mid-word.
        hx = x + 30
        tag_txt = region + " " + tag
        tw = draw.textlength(tag_txt, font=F_TAG)
        max_w = col_w - 30 - tw - 8
        line = head
        while draw.textlength(line, font=F_ROW) > max_w and len(line) > 4:
            line = line[:-1]
        draw.text((hx, y + 3), line, font=F_ROW, fill=INK)
        # Region + C/R/CL tag at the right edge of the column.
        draw.text((x + col_w - tw, y + 3), tag_txt, font=F_TAG,
                  fill=tag_colors[tag])

    img.save(OUT, optimize=True)
    print("saved %s %dx%d" % (OUT, W, H))


if __name__ == "__main__":
    main()
