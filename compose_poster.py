#!/usr/bin/env python3
"""Compose the news-image-20261122 entry poster, enlarged v3 (1024x1024 PNG).

Dense broadsheet, 42 stories / 8 regions: masthead + top story (COP31
collapse) + six illustrated leads (2 rows x 3) + world map with dots + 35
one-line stories in 8 region groups (3 columns) + by-the-numbers strip +
date check. Every word is drawn here with PIL so the text is crisp; the
icons and map are cropped from the text-free AI illustrations hero.png /
hero2.png (same set as the 20261120 entry). Run:
    python3 compose_poster.py   # writes entry.png next to this file
"""
import hashlib
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 243, 227)
NAVY = (20, 38, 77)
RED = (178, 44, 32)
GOLD = (232, 184, 74)
INK = (24, 28, 36)
GREY = (82, 88, 98)
CARD = (255, 255, 255)
LINE = (205, 198, 178)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def wrap_item(draw, text, fnt, first_w, rest_w):
    """Wrap with a narrower first line (the place prefix occupies it)."""
    lines, cur, w = [], "", first_w
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
            w = rest_w
    if cur:
        lines.append(cur)
    return lines


def icons_from(hero, n=6, strip_top=0.0, strip_bottom=0.40, size=96):
    """Crop n evenly spaced vignettes out of a hero strip."""
    hw, hh = hero.size
    y0, y1 = int(hh * strip_top), int(hh * strip_bottom)
    out = []
    for i in range(n):
        cx = int(hw * (i + 0.5) / n)
        cy = (y0 + y1) // 2
        side = int(hw / n * 0.80)
        box = (cx - side // 2, cy - side // 2,
               cx + side // 2, cy + side // 2)
        out.append(hero.crop(box).resize((size, size), Image.LANCZOS))
    return out


TOP_HEAD = "TOP STORY — COP31 COLLAPSES: NO CLIMATE DEAL IN ANTALYA"
TOP_SUB = ("Nearly 200 nations end two days late with no pact  ·  "
           "EU rejects text with no fossil fuels  ·  Guterres: deeply disappointing")

# (kicker, headline, body, icon) — icon: (hero, index)
LEADS = [
    ("GULF · BAHRAIN",
     "Iran strikes US bases in Bahrain",
     "Sitra site hit; 2 hurt. Tehran claims 2 Patriot radars destroyed.",
     ("h1", 3)),
    ("LIBYA · BENGHAZI",
     "Sea drones hit Russian warship",
     "Corvette Merkury badly damaged; 6 drones, 2 got through.",
     ("h2", 2)),
    ("WAR · UKRAINE",
     "Drone hits flats near Kyiv; 14 missing",
     "Missile kills 2 in Kryvyi Rih, 60 hurt; Sparta II still burning.",
     ("h1", 2)),
    ("MEXICO · SINALOA",
     "'El Chapo Isidro' captured in raid",
     "11 killed, incl. 4 soldiers; gunmen torch cars in Guasave.",
     ("h1", 0)),
    ("GULF · HORMUZ",
     "Iran to send 14 tankers past US blockade",
     "3 tankers struck; 2 hit mines as shipping fears grow.",
     ("h2", 0)),
    ("SPACE · MERCURY",
     "BepiColombo reaches Mercury orbit",
     "8-year flight ends; two orbiters split in December.",
     ("h2", 5)),
]

# (region, [(place, headline), ...]) — 35 one-line stories, 8 regions
GROUPS = [
    ("EUROPE", [
        ("BRUSSELS", "UK–EU pact: youth mobility, food trade; +£17bn a year by 2040."),
        ("COPENHAGEN", "Denmark expels Russian attaché over 'kill plot'."),
        ("ABU DHABI", "Zelenskyy backs US three-way peace talks before Christmas."),
        ("MADRID", "Spain heads to snap election on 29 Nov as Sánchez fights on."),
        ("PARIS", "Three French police sentenced over racist assault."),
    ]),
    ("MIDDLE EAST", [
        ("RIYADH", "Saudi-led coalition intercepts three Houthi missiles."),
        ("GAZA", "Israeli strike on Gaza City truck kills three men."),
        ("RAMALLAH", "Settlers torch 12 vehicles in four villages; inquiry opened."),
        ("BEIRUT", "Aoun presses Israel to withdraw; Hezbollah arms row drags on."),
        ("DOHA", "Iran shows off missile launcher as Qatar mediates new talks."),
    ]),
    ("ASIA & PACIFIC", [
        ("SEOUL", "Education minister quits over AI cheating at college exams."),
        ("TOKYO", "China–Japan row deepens over Taiwan; Beijing curbs minerals."),
        ("JAKARTA", "EU–Indonesia sign trade deal; tariffs cut on 98.5% of goods."),
        ("HONG KONG", "Election Committee polls: turnout over 98%; 856 vie for 723 seats."),
        ("CIKANDE", "Candy factory fire kills three; 36 still missing in Banten."),
        ("KATHMANDU", "Nepal PM Balendra Shah visits India for talks with Modi."),
        ("MANIPUR", "Toxic alcohol kills 11; more than 180 in hospital."),
    ]),
    ("AFRICA", [
        ("KHARTOUM", "Drones hit Khartoum, damage UN building; war grinds on."),
        ("BAYELSA", "Funeral boat capsizes in Nigeria; 24 dead."),
        ("JOHANNESBURG", "ANC in coalition talks; Mlambo-Ngcuka dies, 71."),
        ("KINSHASA", "Ebola teams in DR Congo face attacks fuelled by rumours."),
    ]),
    ("AMERICAS", [
        ("WASHINGTON", "FBI probes apparent hack of its NCIC crime database."),
        ("BRASÍLIA", "Bolsonaro in intensive care; serving a 27-year term."),
        ("LIMA", "Magnitude 6.7 quake hits Peru; one dead, 853 displaced."),
        ("PORT-AU-PRINCE", "Haiti signs prison deal with El Salvador."),
        ("RIO GRANDE DO SUL", "Storm kills three; gusts hit 114 km/h."),
    ]),
    ("OCEANIA & SPORT", [
        ("DUBLIN", "Ireland beat South Africa 20–17; France reach the final."),
        ("LONDON", "England 37–12 New Zealand; Fiji edge Italy 21–16."),
    ]),
    ("MARKETS & TECH", [
        ("NEW YORK", "S&P 500 down 8.6% in a week; Nasdaq off 10%."),
        ("WASHINGTON", "US tightens AI chip curbs on China; Beijing hits back."),
        ("CALIFORNIA", "Paralysed man plays GTA VI using a Neuralink implant."),
        ("GENEVA", "UN talks on 'killer robots' extended to 2028; no binding rules."),
    ]),
    ("CULTURE & SCIENCE", [
        ("THE HAGUE", "Rohingya welcome ICJ genocide verdict; want to go home."),
        ("WORLD", "Signal blocks AI assistants from reading chats on screen."),
        ("UN", "World on course to pass 1.5°C warming limit."),
    ]),
]

NUMBERS = ("BY THE NUMBERS  —  14 tankers  ·  98% turnout in HK  ·  "
           "S&P −8.6% in a week  ·  24 dead off Nigeria  ·  Quake 6.7, Peru  ·  "
           "723 seats, HK")

FOOTER = ("DATE CHECK — Every story reported Sunday 22 November 2026 (UTC)  ·  "
          "Compiled 23 Nov 2026, 02:00 UTC  ·  Sources: AP · Reuters · BBC · AFP · Al Jazeera")


def main():
    hero = Image.open("hero.png").convert("RGB")
    hero2 = Image.open("hero2.png").convert("RGB")
    h1 = icons_from(hero, 6, 0.0, 0.40, 96)
    h2 = icons_from(hero2, 6, 0.12, 0.90, 96)
    icons = {"h1": h1, "h2": h2}

    map_band = hero.crop((0, int(hero.size[1] * 0.405), hero.size[0],
                          hero.size[1])).resize((W, 58), Image.LANCZOS)

    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # --- masthead ----------------------------------------------------------
    d.rectangle([0, 0, W, 76], fill=NAVY)
    d.rectangle([0, 76, W, 80], fill=RED)
    d.text((24, 10), "THE WORLD IN ONE DAY", font=font(SERIF_B, 32),
           fill=CREAM)
    f_date = font(SANS_B, 20)
    date = "SUNDAY, 22 NOVEMBER 2026"
    d.text((W - 24 - d.textlength(date, font=f_date), 16), date,
           font=f_date, fill=GOLD)
    d.text((24, 50), "42 stories  ·  8 regions  ·  Every figure sourced  ·  All times UTC",
           font=font(SANS, 15), fill=(196, 205, 224))

    # --- top story ---------------------------------------------------------
    ty = 80
    d.rectangle([0, ty, W, ty + 42], fill=(255, 250, 230))
    d.rectangle([0, ty, 8, ty + 42], fill=RED)
    img.paste(h2[1].resize((34, 34), Image.LANCZOS), (20, ty + 4))
    d.text((66, ty + 4), TOP_HEAD, font=font(SANS_B, 17), fill=RED)
    d.text((66, ty + 25), TOP_SUB, font=font(SANS, 13), fill=INK)

    # --- six lead cards, 2 rows x 3 ----------------------------------------
    cw = 318
    gap = (W - 2 * 20 - 3 * cw) // 2
    lh = 88
    max_lead_bottom = 0
    for i, (kicker, head, body, (hset, hidx)) in enumerate(LEADS):
        row, col = divmod(i, 3)
        x = 20 + col * (cw + gap)
        y = 130 + row * (lh + 8)
        d.rounded_rectangle([x, y, x + cw, y + lh], radius=8,
                            fill=CARD, outline=LINE, width=1)
        img.paste(icons[hset][hidx].resize((48, 48), Image.LANCZOS),
                  (x + 10, y + 10))
        tx = x + 68
        tw = cw - 68 - 10
        d.text((tx, y + 8), kicker, font=font(SANS_B, 11), fill=RED)
        hl = wrap(d, head, font(SERIF_B, 15), tw)[:2]
        yy = y + 26
        for ln in hl:
            d.text((tx, yy), ln, font=font(SERIF_B, 15), fill=INK)
            yy += 17
        bl = wrap(d, body, font(SANS, 11), tw)[:2]
        yy += 1
        for ln in bl:
            d.text((tx, yy), ln, font=font(SANS, 11), fill=GREY)
            yy += 13
        max_lead_bottom = max(max_lead_bottom, yy)
        assert len(hl) <= 2 and len(bl) <= 2, f"lead {i} wraps too far"

    # --- map banner with dots ----------------------------------------------
    my = 322
    img.paste(map_band, (0, my))
    d.rectangle([0, my + 58, W, my + 62], fill=NAVY)
    # dots: (x fraction, y fraction of banner) — Antalya, Bahrain,
    # Benghazi, Kyiv, Guasave, Hormuz.
    dots = [(0.545, 0.30), (0.605, 0.52), (0.525, 0.55),
            (0.550, 0.22), (0.160, 0.52), (0.620, 0.55)]
    for fx, fy in dots:
        px, py = int(W * fx), my + int(58 * fy)
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=RED,
                  outline=(255, 255, 255), width=2)

    # --- region lists, 3 columns --------------------------------------------
    cols = [[GROUPS[0], GROUPS[1], GROUPS[7]],
            [GROUPS[2], GROUPS[3]],
            [GROUPS[4], GROUPS[5], GROUPS[6]]]
    col_w = 318
    col_x = [20, 353, 686]
    gy = 392
    list_bottom = gy
    f_head = font(SANS_B, 13)
    f_item = font(SANS, 13)
    f_item_b = font(SANS_B, 13)
    n_items = 0
    for ci, groups in enumerate(cols):
        x = col_x[ci]
        y = gy
        for region, items in groups:
            d.text((x, y), region, font=f_head, fill=RED)
            d.line([x, y + 18, x + col_w, y + 18], fill=RED, width=2)
            y += 24
            for place, head in items:
                n_items += 1
                prefix = f"{place} — "
                pre_w = d.textlength(prefix, font=f_item_b)
                lines = wrap_item(d, head, f_item, col_w - pre_w, col_w)
                assert len(lines) <= 2, f"{place}: wraps to {len(lines)} lines"
                d.text((x, y), prefix, font=f_item_b, fill=INK)
                yy = y
                for j, ln in enumerate(lines):
                    d.text((x + (pre_w if j == 0 else 0), yy), ln,
                           font=f_item, fill=INK)
                    yy += 16
                y = yy + 2
            y += 1
        list_bottom = max(list_bottom, y)
    assert n_items == 35, f"one-liners: {n_items}, want 35"
    assert list_bottom <= 922, f"lists end at {list_bottom}, over 922"

    # --- numbers strip + footer ----------------------------------------------
    d.rectangle([0, 930, W, 966], fill=NAVY)
    f_num = font(SANS_B, 13)
    while d.textlength(NUMBERS, font=f_num) > W - 48 and f_num.size > 10:
        f_num = font(SANS_B, f_num.size - 1)
    d.text((24, 942), NUMBERS, font=f_num, fill=CREAM)
    d.rectangle([0, 966, W, H], fill=(12, 22, 48))
    f_foot = font(SANS, 12)
    while d.textlength(FOOTER, font=f_foot) > W - 48 and f_foot.size > 10:
        f_foot = font(SANS, f_foot.size - 1)
    d.text((24, 985), FOOTER, font=f_foot, fill=(196, 205, 224))

    img.save("entry.png", optimize=True)
    data = open("entry.png", "rb").read()
    total = 1 + len(LEADS) + n_items
    print(f"wrote entry.png {img.size} {len(data)} bytes "
          f"sha256={hashlib.sha256(data).hexdigest()[:16]} "
          f"stories={total} regions={len(GROUPS)} "
          f"lists_bottom={list_bottom} leads_bottom={max_lead_bottom}")
    assert total == 42, f"stories: {total}, want 42"
    assert len(GROUPS) == 8, f"regions: {len(GROUPS)}, want 8"
    assert len(data) <= 1024 * 1024, "entry.png over 1 MiB"


if __name__ == "__main__":
    main()
