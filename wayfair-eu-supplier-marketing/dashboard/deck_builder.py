"""Real deck builder for the WSP Pitch Builder dashboard.

Takes structured supplier data, produces a personalised .pptx in the
TuttiBambini visual register. No Claude API call required.

This is the production v1.0 backend — not a stub.
"""
import io
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import os


# ============================================================
# Palette — matches SKILL.md §C and the TuttiBambini reference
# ============================================================
DEEP_T   = (60, 26, 80)
PURPLE_T = (123, 24, 159)
LAV_T    = (246, 235, 251)
GOLD_T   = (212, 160, 23)
INK_T    = (26, 26, 26)
SLATE_T  = (91, 91, 102)
HAIR_T   = (229, 222, 236)
WHITE_T  = (255, 255, 255)
GREEN_T  = (14, 143, 96)
GREEN_LIGHT = (37, 171, 122)


# ============================================================
# Fonts (Liberation Serif/Sans available on Streamlit Cloud)
# ============================================================
def serif(size, bold=False, italic=False):
    paths = {
        (True, True):   "/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf",
        (True, False):  "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
        (False, True):  "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
        (False, False): "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    }
    p = paths.get((bold, italic))
    if p and os.path.exists(p):
        return ImageFont.truetype(p, size)
    # Fallback if Liberation isn't on this box
    fb = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if bold else \
         "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
    if os.path.exists(fb):
        return ImageFont.truetype(fb, size)
    return ImageFont.load_default()


def sans(size, bold=False, italic=False):
    paths = {
        (True, True):   "/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf",
        (True, False):  "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        (False, True):  "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf",
        (False, False): "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    }
    p = paths.get((bold, italic))
    if p and os.path.exists(p):
        return ImageFont.truetype(p, size)
    fb = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else \
         "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    if os.path.exists(fb):
        return ImageFont.truetype(fb, size)
    return ImageFont.load_default()


def tsize(d, t, f):
    b = d.textbbox((0,0), t, font=f); return b[2]-b[0], b[3]-b[1]


def draw_ls(d, x, y, txt, f, fill, sp=3):
    cx = x
    for ch in txt:
        d.text((cx, y), ch, font=f, fill=fill)
        b = d.textbbox((0,0), ch, font=f); cx += (b[2]-b[0]) + sp


def wrap(d, t, mw, f):
    out, line = [], []
    for w in t.split():
        test = " ".join(line + [w])
        if tsize(d, test, f)[0] > mw:
            out.append(" ".join(line)); line = [w]
        else: line.append(w)
    if line: out.append(" ".join(line))
    return out


# Slide dimensions match TuttiBambini (16:9, rendered at 150 DPI)
W, H = 2400, 1350
M = 130


# ============================================================
# Slide renderers — TuttiBambini visual register
# ============================================================
def render_cover(data: dict) -> Image.Image:
    """Slide 1 — cover with KPI ribbon."""
    img = Image.new("RGB", (W, H), tuple(DEEP_T))
    d = ImageDraw.Draw(img)

    # Wayfair logo
    here = Path(__file__).parent
    logo_path = here / "assets" / "wayfair_logo_white.png"
    if logo_path.exists():
        logo = Image.open(logo_path).convert("RGBA")
        logo.thumbnail((240, 100))
        img.paste(logo, (M, 80), logo)

    # Gold eyebrow
    eyebrow = f"{data['supplier'].upper()}  ·  WAYFAIR SPONSORED PRODUCTS"
    draw_ls(d, M, 220, eyebrow, sans(26, bold=True), GOLD_T, sp=3)

    # Hero title (auto-picked based on data)
    title = data.get('cover_title', 'Keep your WSP on at this pace.')
    d.text((M, 320), title, font=serif(115, bold=True), fill=WHITE_T)

    # Subtitle
    subtitle = data.get('cover_subtitle',
        'Your ads are doing the work. Here is what they returned, and the simple way to lock it in.')
    sub_lines = wrap(d, subtitle, W - 2*M - 100, serif(38, italic=True))
    for i, ln in enumerate(sub_lines[:2]):
        d.text((M, 530 + i*55), ln, font=serif(38, italic=True), fill=WHITE_T)

    # 4 KPI cards along bottom
    card_y = 880; card_h = 320
    card_w = (W - 2*M - 3*30) // 4
    card_gap = 30
    kpis = data['kpis_cover']  # list of 4 dicts: {label, value, sub}
    for i, kpi in enumerate(kpis[:4]):
        cx = M + i * (card_w + card_gap)
        d.rectangle([cx, card_y, cx + card_w, card_y + card_h], fill=LAV_T)
        d.rectangle([cx, card_y, cx + card_w, card_y + 10], fill=GOLD_T)
        draw_ls(d, cx + 35, card_y + 38, kpi['label'].upper(),
                sans(20, bold=True), PURPLE_T, sp=2)
        d.text((cx + 35, card_y + 95), kpi['value'],
               font=serif(75, bold=True, italic=True), fill=DEEP_T)
        d.text((cx + 35, card_y + card_h - 70), kpi['sub'],
               font=sans(20), fill=INK_T)

    # Footer
    footer = f"{data['period']}  ·  prepared for {data.get('srm', 'the team')}  ·  UK  ·  GBP"
    d.text((M, H - 75), footer, font=sans(20), fill=(180, 165, 200))
    return img


def render_value_story(data: dict) -> Image.Image:
    """Slide 2 — '01 · WHAT WSP IS DOING FOR YOU' with hero card + chart."""
    img = Image.new("RGB", (W, H), WHITE_T)
    d = ImageDraw.Draw(img)
    draw_ls(d, M, 90, "01  ·  WHAT WSP IS DOING FOR YOU",
            sans(22, bold=True), PURPLE_T, sp=3)

    ratio = data['ws_roas']
    title = data.get('story_title',
        f"When it is on, every pound comes back about {int(round(ratio))} times over.")
    d.text((M, 165), title, font=serif(48, bold=True), fill=INK_T)

    # LEFT lavender hero card
    left_x = M; left_w = 850; left_y = 370; left_h = 700
    d.rectangle([left_x, left_y, left_x + left_w, left_y + left_h], fill=LAV_T)
    draw_ls(d, left_x + 40, left_y + 40, f"SO FAR IN {data['year']}",
            sans(22, bold=True), PURPLE_T, sp=2)
    d.text((left_x + 40, left_y + 95), f"£{ratio:.2f}",
           font=serif(180, bold=True, italic=True), fill=DEEP_T)
    d.text((left_x + 40, left_y + 300),
           "of wholesale revenue for every £1 of WSP",
           font=sans(28), fill=INK_T)
    d.text((left_x + 40, left_y + 340), "spend",
           font=sans(28), fill=INK_T)
    rows = [
        ("You spent", f"£{_fmt(data['wsp_spend_ytd'])} on WSP"),
        ("It drove",  f"£{_fmt(data['attr_wsc_ytd'])} wholesale revenue"),
        ("That's",    f"1 in £{ratio:.2f} — strong and steady"),
    ]
    rx = left_x + 40; ry = left_y + 440
    for label, value in rows:
        d.text((rx, ry), label, font=sans(22), fill=SLATE_T)
        d.text((rx + 230, ry), value, font=sans(22, bold=True), fill=INK_T)
        ry += 60

    # RIGHT chart — bars by month
    chart_x = left_x + left_w + 60
    chart_y = left_y - 30
    chart_w = W - chart_x - M
    chart_h = left_h + 30
    d.text((chart_x, chart_y), "Wholesale revenue driven by WSP, each month (£)",
           font=sans(24, bold=True), fill=INK_T)

    months_data = data['monthly_attr_wsc'][-5:]  # last 5 months
    months = [m[0] for m in months_data]
    values = [m[1] for m in months_data]
    if values and max(values) > 0:
        max_v = max(values) * 1.18
        bar_area_top = chart_y + 80
        bar_area_bot = chart_y + chart_h - 90
        bar_area_h = bar_area_bot - bar_area_top
        n = len(values); gap = 30
        bw = (chart_w - gap*(n-1)) // n
        for i, v in enumerate(values):
            bh = int(v / max_v * bar_area_h)
            bx = chart_x + i*(bw + gap)
            by = bar_area_bot - bh
            d.rectangle([bx, by, bx + bw, bar_area_bot], fill=PURPLE_T)
            label = f"{int(v/1000)}k"
            f_lbl = sans(28, bold=True)
            lw, _ = tsize(d, label, f_lbl)
            d.text((bx + (bw - lw)//2, by - 50), label, font=f_lbl, fill=INK_T)
            f_m = sans(22)
            mw_, _ = tsize(d, months[i], f_m)
            d.text((bx + (bw - mw_)//2, bar_area_bot + 18), months[i], font=f_m, fill=SLATE_T)

    takeaway = data.get('story_takeaway',
        f"Take-away: your WSP has paid back about £{ratio:.2f} for every £1 — and it has every month this year.")
    d.text((M, H - 120), takeaway, font=serif(28, italic=True), fill=INK_T)
    return img


def render_yoy_proof(data: dict) -> Image.Image:
    """Slide 3 — '02 · YoY proof' with deep purple KPI band + green pills."""
    img = Image.new("RGB", (W, H), WHITE_T)
    d = ImageDraw.Draw(img)
    eyebrow = f"02  ·  {data['period'].upper()} vs {data['yoy_period'].upper()}"
    draw_ls(d, M, 90, eyebrow, sans(22, bold=True), PURPLE_T, sp=3)
    d.text((M, 165),
           data.get('yoy_title', "You doubled down on ads — and the ads doubled down on you."),
           font=serif(58, bold=True), fill=INK_T)

    pc_x = M; pc_y = 380; pc_w = 1500; pc_h = 500
    d.rectangle([pc_x, pc_y, pc_x + pc_w, pc_y + pc_h], fill=DEEP_T)
    col_w = pc_w // 3
    for div in [pc_x + col_w, pc_x + 2*col_w]:
        d.rectangle([div - 1, pc_y + 50, div + 1, pc_y + pc_h - 50], fill=(120, 90, 140))

    cols = data['yoy_columns']  # list of 3 dicts: {label, value, sub, pill}
    for i, col in enumerate(cols[:3]):
        cx = pc_x + i*col_w + 50
        draw_ls(d, cx, pc_y + 60, col['label'], sans(22, bold=True), GOLD_T, sp=2)
        d.text((cx, pc_y + 130), col['value'],
               font=serif(100, bold=True, italic=True), fill=WHITE_T)
        d.text((cx, pc_y + 290), col['sub'],
               font=sans(24), fill=(180, 165, 200))
        pill = col['pill']
        f_pill = sans(28, bold=True)
        pw_, ph_ = tsize(d, pill, f_pill)
        pill_w = pw_ + 70; pill_h = ph_ + 26
        pill_x = cx; pill_y = pc_y + 360
        d.rounded_rectangle([pill_x, pill_y, pill_x + pill_w, pill_y + pill_h],
                              radius=8, fill=GREEN_T)
        d.text((pill_x + 35, pill_y + 13), pill, font=f_pill, fill=WHITE_T)

    # RIGHT lavender side card
    rx = pc_x + pc_w + 50
    rw = W - rx - M
    d.rectangle([rx, pc_y, rx + rw, pc_y + pc_h], fill=LAV_T)
    draw_ls(d, rx + 35, pc_y + 40, "WSP % OF WSC",
            sans(22, bold=True), PURPLE_T, sp=2)
    bar_bw = 60; bar_gap = 25; bar_bot = pc_y + 290
    bar_heights = [80, 130, 175]
    bar_x = rx + 60
    for i, bh in enumerate(bar_heights):
        bx = bar_x + i*(bar_bw + bar_gap)
        d.rectangle([bx, bar_bot - bh, bx + bar_bw, bar_bot], fill=GREEN_LIGHT)
    pct = data['wsp_pct_wsc_latest']
    label = "Above" if pct >= 5.0 else "Below"
    d.text((rx + 35, pc_y + 320), label,
           font=serif(50, italic=True), fill=GREEN_T if pct >= 5.0 else (200, 100, 100))
    d.text((rx + 35, pc_y + 380), "5% benchmark",
           font=serif(50, italic=True), fill=GREEN_T if pct >= 5.0 else (200, 100, 100))
    d.text((rx + 35, pc_y + pc_h - 60),
           f"Your spend share is now\n{pct:.1f}% of wholesale.",
           font=sans(20, italic=True), fill=SLATE_T)

    cb_y = 1110; cb_h = 110
    d.rectangle([M, cb_y, W - M, cb_y + cb_h], fill=LAV_T)
    callout = data.get('yoy_callout',
        f"The pattern is clear: spend and wholesale move together, every month.")
    d.text((M + 35, cb_y + 35), callout, font=sans(24), fill=INK_T)
    return img


def render_ask(data: dict) -> Image.Image:
    """Slide 4 — '03 · WHERE WE GO FROM HERE' with three pillars + THE ASK card."""
    img = Image.new("RGB", (W, H), WHITE_T)
    d = ImageDraw.Draw(img)
    draw_ls(d, M, 90, "03  ·  WHERE WE GO FROM HERE",
            sans(22, bold=True), PURPLE_T, sp=3)
    d.text((M, 165), data.get('ask_title',
           "Lock in the rhythm — same return, no surprises."),
           font=serif(58, bold=True), fill=INK_T)

    card_y = 360; card_h = 520
    card_w = (W - 2*M - 2*30) // 3
    card_gap = 30
    cards = data['pillars']  # list of 3 dicts: {label, hero, body}
    for i, card in enumerate(cards[:3]):
        cx = M + i*(card_w + card_gap)
        d.rectangle([cx, card_y, cx + card_w, card_y + card_h], fill=LAV_T)
        d.rectangle([cx, card_y, cx + card_w, card_y + 10], fill=GOLD_T)
        draw_ls(d, cx + 35, card_y + 40, card['label'],
                sans(22, bold=True), PURPLE_T, sp=2)
        d.text((cx + 35, card_y + 110), card['hero'],
               font=serif(95, bold=True, italic=True), fill=DEEP_T)
        body_lines = wrap(d, card['body'], card_w - 70, sans(24))
        for j, ln in enumerate(body_lines):
            d.text((cx + 35, card_y + 290 + j*36), ln, font=sans(24), fill=INK_T)

    # THE ASK card
    ask_y = 920; ask_h = 220
    d.rectangle([M, ask_y, W - M, ask_y + ask_h], fill=DEEP_T)
    draw_ls(d, M + 40, ask_y + 32, "THE ASK", sans(24, bold=True), GOLD_T, sp=3)
    ask_amount = data['ask_amount_text']  # e.g. "~£23k / month"
    last_wsc = _fmt(data['last_month_wsc'])
    d.text((M + 40, ask_y + 80), "Continue WSP at  ", font=sans(40), fill=WHITE_T)
    cw1, _ = tsize(d, "Continue WSP at  ", sans(40))
    d.text((M + 40 + cw1, ask_y + 80), ask_amount,
           font=sans(40, bold=True), fill=GOLD_T)
    cw2, _ = tsize(d, ask_amount, sans(40, bold=True))
    d.text((M + 40 + cw1 + cw2, ask_y + 80), "  —  5% of last month's",
           font=sans(40), fill=WHITE_T)
    d.text((M + 40, ask_y + 135),
           f"wholesale revenue (£{last_wsc}), set on day 1 so the engine never stutters.",
           font=sans(40), fill=WHITE_T)

    closing = data.get('ask_closing',
        f"Proven £{data['ws_roas']:.2f} back for every £1  ·  one rule, live on day 1.")
    d.text((M, H - 80), closing, font=serif(28, italic=True), fill=INK_T)
    return img


# ============================================================
# Top-level builder — Image[] → real .pptx bytes
# ============================================================
def build_deck_value_review_b(data: dict) -> bytes:
    """Build a Variant B value-review deck. Returns .pptx bytes ready to download.

    Uses tempfiles (not BytesIO) for the PNG → python-pptx handoff because some
    PowerPoint versions are picky about images embedded via memory streams.
    """
    import tempfile
    slides = [
        render_cover(data),
        render_value_story(data),
        render_yoy_proof(data),
        render_ask(data),
    ]

    from pptx import Presentation
    from pptx.util import Inches

    prs = Presentation()
    prs.slide_width  = Inches(13.333)
    prs.slide_height = Inches(7.5)
    BLANK = prs.slide_layouts[6]

    # Save each PNG to a real tempfile (conventional) and embed via file path
    with tempfile.TemporaryDirectory() as td:
        for i, slide_img in enumerate(slides):
            # Convert to RGB and save as a clean baseline PNG
            if slide_img.mode != "RGB":
                slide_img = slide_img.convert("RGB")
            png_path = f"{td}/slide_{i}.png"
            slide_img.save(png_path, "PNG", optimize=False)

            s = prs.slides.add_slide(BLANK)
            s.shapes.add_picture(png_path, 0, 0,
                                  width=prs.slide_width,
                                  height=prs.slide_height)

        out = io.BytesIO()
        prs.save(out)
        out.seek(0)
        return out.read()


# ============================================================
# Helpers
# ============================================================
def _fmt(v):
    """Format big numbers cleanly: £476k, £1.2M, £33.2k."""
    if v >= 1e6:
        return f"{v/1e6:.2f}M"
    elif v >= 1e3:
        return f"{v/1e3:.1f}k"
    else:
        return f"{v:.0f}"


# =====================================================================
# VARIANT A — RESTART PITCH
# Mirrors the TuttiBambini Way Day deck: cover · value-was-driving ·
# the-event-proved-it · the-problem (dark-days calendar) · the-ask.
# =====================================================================

# Coral palette for problem framing
CORAL_T = (184, 58, 58)
CORAL_LIGHT = (252, 232, 232)
GREY_BAR = (207, 199, 214)


def render_restart_cover(data: dict) -> Image.Image:
    """Cover with 4 KPI cards; the 4th has a CORAL stripe (the loss)."""
    img = Image.new("RGB", (W, H), tuple(DEEP_T))
    d = ImageDraw.Draw(img)
    here = Path(__file__).parent
    logo_path = here / "assets" / "wayfair_logo_white.png"
    if logo_path.exists():
        logo = Image.open(logo_path).convert("RGBA")
        logo.thumbnail((240, 100))
        img.paste(logo, (M, 80), logo)

    draw_ls(d, M, 220,
            f"{data['supplier'].upper()}  ·  WAYFAIR SPONSORED PRODUCTS",
            sans(26, bold=True), GOLD_T, sp=3)
    d.text((M, 320), data.get('cover_title', "Switch your WSP back on."),
           font=serif(115, bold=True), fill=WHITE_T)

    sub = data.get('cover_subtitle',
        "It was working — then it went dark. Here is what it drove for you, and the simple way to keep it on.")
    sub_lines = wrap(d, sub, W - 2*M - 100, serif(38, italic=True))
    for i, ln in enumerate(sub_lines[:2]):
        d.text((M, 530 + i*55), ln, font=serif(38, italic=True), fill=WHITE_T)

    card_y = 880; card_h = 320
    card_w = (W - 2*M - 3*30) // 4
    card_gap = 30
    kpis = data['kpis_cover']
    for i, kpi in enumerate(kpis[:4]):
        cx = M + i * (card_w + card_gap)
        d.rectangle([cx, card_y, cx + card_w, card_y + card_h], fill=LAV_T)
        # CORAL stripe on the loss KPI (typically the 4th)
        stripe_color = tuple(CORAL_T) if kpi.get('is_loss') else GOLD_T
        d.rectangle([cx, card_y, cx + card_w, card_y + 10], fill=stripe_color)
        draw_ls(d, cx + 35, card_y + 38, kpi['label'].upper(),
                sans(20, bold=True),
                tuple(CORAL_T) if kpi.get('is_loss') else PURPLE_T, sp=2)
        value_color = tuple(CORAL_T) if kpi.get('is_loss') else DEEP_T
        d.text((cx + 35, card_y + 95), kpi['value'],
               font=serif(75, bold=True, italic=True), fill=value_color)
        d.text((cx + 35, card_y + card_h - 70), kpi['sub'],
               font=sans(20), fill=INK_T)

    footer = f"{data.get('event_window', data['period'])}  ·  prepared for {data.get('srm','the team')}  ·  UK  ·  GBP"
    d.text((M, H - 75), footer, font=sans(20), fill=(180, 165, 200))
    return img


def render_dark_days_calendar(data: dict) -> Image.Image:
    """The killer slide — day-by-day purple/grey blocks showing dark days."""
    img = Image.new("RGB", (W, H), WHITE_T)
    d = ImageDraw.Draw(img)
    draw_ls(d, M, 90, "03  ·  THE PROBLEM",
            sans(22, bold=True), tuple(CORAL_T), sp=3)
    d.text((M, 165),
           data.get('problem_title',
               f"Right after the event, your WSP went dark — and the orders stopped."),
           font=serif(48, bold=True), fill=INK_T)

    # Calendar instruction
    d.text((M, 270),
           "Each block is one day. Purple = WSP running. Grey = switched off.",
           font=sans(22), fill=SLATE_T)

    # The calendar
    calendar = data.get('daily_calendar', [])
    if calendar:
        cal_top = 360; cal_bot = 620
        cal_h = cal_bot - cal_top
        n_days = len(calendar)
        gap = 6
        block_w = (W - 2*M - gap*(n_days-1)) // max(n_days, 1)
        block_w = min(block_w, 50)  # cap at 50px for readability

        # Annotations above (event window + dark window)
        event_indices = [i for i, day in enumerate(calendar) if day.get('event')]
        dark_indices = [i for i, day in enumerate(calendar) if day['status'] == 'off']

        # Event tab in gold
        if event_indices:
            ex_start = M + event_indices[0] * (block_w + gap)
            ex_end = M + (event_indices[-1]+1) * (block_w + gap) - gap
            d.rectangle([ex_start, cal_top - 50, ex_end, cal_top - 30], fill=GOLD_T)
            draw_ls(d, ex_start, cal_top - 90,
                    data.get('event_name', 'EVENT').upper(),
                    sans(18, bold=True), GOLD_T, sp=2)

        # Dark stretch in coral
        if dark_indices:
            # Find longest contiguous run
            longest_start, longest_len = 0, 0
            cur_start, cur_len = dark_indices[0], 1
            for j in range(1, len(dark_indices)):
                if dark_indices[j] == dark_indices[j-1] + 1:
                    cur_len += 1
                else:
                    if cur_len > longest_len:
                        longest_start, longest_len = cur_start, cur_len
                    cur_start, cur_len = dark_indices[j], 1
            if cur_len > longest_len:
                longest_start, longest_len = cur_start, cur_len

            dx_start = M + longest_start * (block_w + gap)
            dx_end = M + (longest_start + longest_len) * (block_w + gap) - gap
            d.rectangle([dx_start, cal_top - 50, dx_end, cal_top - 30], fill=tuple(CORAL_T))
            draw_ls(d, dx_start, cal_top - 90,
                    f"{longest_len} DAYS DARK",
                    sans(18, bold=True), tuple(CORAL_T), sp=2)

        # Day blocks
        for i, day in enumerate(calendar):
            bx = M + i * (block_w + gap)
            color = PURPLE_T if day['status'] == 'on' else GREY_BAR
            d.rectangle([bx, cal_top, bx + block_w, cal_bot], fill=color)
            # Date label every 7 days
            if i % 7 == 0 or i == len(calendar) - 1:
                date_lbl = day.get('label', '')
                if date_lbl:
                    d.text((bx, cal_bot + 12), date_lbl,
                           font=sans(16), fill=SLATE_T)

    # Bottom: two cards
    card_y = 760; card_h = 320
    card_w = (W - 2*M - 40) // 2

    # LEFT — coral card "WHILE IT WAS DARK"
    d.rectangle([M, card_y, M + card_w, card_y + card_h], fill=CORAL_LIGHT)
    d.rectangle([M, card_y, M + 8, card_y + card_h], fill=tuple(CORAL_T))
    draw_ls(d, M + 35, card_y + 40, "WHILE IT WAS DARK",
            sans(22, bold=True), tuple(CORAL_T), sp=2)
    missed_text = data.get('missed_wholesale_text', '~£15k')
    d.text((M + 35, card_y + 100), missed_text,
           font=serif(140, bold=True, italic=True), fill=tuple(CORAL_T))
    d.text((M + 35, card_y + 270),
           data.get('missed_wholesale_caption',
               "of wholesale revenue likely missed over those days"),
           font=sans(20), fill=INK_T)

    # RIGHT — lavender "THE PATTERN"
    rx = M + card_w + 40
    d.rectangle([rx, card_y, rx + card_w, card_y + card_h], fill=LAV_T)
    d.rectangle([rx, card_y, rx + 8, card_y + card_h], fill=PURPLE_T)
    draw_ls(d, rx + 35, card_y + 40, "THE PATTERN",
            sans(22, bold=True), PURPLE_T, sp=2)
    d.text((rx + 35, card_y + 100), "On = sales",
           font=serif(110, bold=True, italic=True), fill=DEEP_T)
    d.text((rx + 35, card_y + 270),
           "Off = silence. The budget keeps running out mid-month.",
           font=sans(20), fill=INK_T)

    # Takeaway
    d.text((M, H - 80),
           data.get('problem_takeaway',
               "Every day WSP is off, you stop showing up to ready-to-buy shoppers — and a competitor takes that slot."),
           font=serif(28, italic=True), fill=INK_T)
    return img


def render_restart_ask(data: dict) -> Image.Image:
    """Restart variant Ask slide — same pattern as Variant B but with restart-specific pillars."""
    img = Image.new("RGB", (W, H), WHITE_T)
    d = ImageDraw.Draw(img)
    draw_ls(d, M, 90, "04  ·  WHERE WE GO FROM HERE",
            sans(22, bold=True), PURPLE_T, sp=3)
    d.text((M, 165),
           data.get('ask_title', "Restart WSP now — the maths still works."),
           font=serif(58, bold=True), fill=INK_T)

    card_y = 360; card_h = 520
    card_w = (W - 2*M - 2*30) // 3
    card_gap = 30
    cards = data['pillars']
    for i, card in enumerate(cards[:3]):
        cx = M + i*(card_w + card_gap)
        d.rectangle([cx, card_y, cx + card_w, card_y + card_h], fill=LAV_T)
        d.rectangle([cx, card_y, cx + card_w, card_y + 10], fill=GOLD_T)
        draw_ls(d, cx + 35, card_y + 40, card['label'],
                sans(22, bold=True), PURPLE_T, sp=2)
        # Coral hero if it's the "what going dark cost" pillar
        hero_color = tuple(CORAL_T) if card.get('is_loss') else DEEP_T
        d.text((cx + 35, card_y + 110), card['hero'],
               font=serif(95, bold=True, italic=True), fill=hero_color)
        body_lines = wrap(d, card['body'], card_w - 70, sans(24))
        for j, ln in enumerate(body_lines):
            d.text((cx + 35, card_y + 290 + j*36), ln, font=sans(24), fill=INK_T)

    ask_y = 920; ask_h = 220
    d.rectangle([M, ask_y, W - M, ask_y + ask_h], fill=DEEP_T)
    draw_ls(d, M + 40, ask_y + 32, "THE ASK", sans(24, bold=True), GOLD_T, sp=3)
    ask_amount = data['ask_amount_text']
    last_wsc = _fmt(data['last_month_wsc'])
    d.text((M + 40, ask_y + 80), "Switch WSP back on at  ", font=sans(40), fill=WHITE_T)
    cw1, _ = tsize(d, "Switch WSP back on at  ", sans(40))
    d.text((M + 40 + cw1, ask_y + 80), ask_amount,
           font=sans(40, bold=True), fill=GOLD_T)
    cw2, _ = tsize(d, ask_amount, sans(40, bold=True))
    d.text((M + 40 + cw1 + cw2, ask_y + 80), "  —  5% of last month's",
           font=sans(40), fill=WHITE_T)
    d.text((M + 40, ask_y + 135),
           f"wholesale revenue (£{last_wsc}), set on day 1 so it never goes dark mid-month.",
           font=sans(40), fill=WHITE_T)

    closing = data.get('ask_closing',
        f"Proven £{data['ws_roas']:.2f} back for every £1  ·  currently leaving wholesale revenue on the table  ·  one rule, live on day 1.")
    d.text((M, H - 80), closing, font=serif(28, italic=True), fill=INK_T)
    return img


def build_deck_restart_pitch_a(data: dict) -> bytes:
    """Build a Variant A Restart pitch deck. Uses the dark-days calendar pattern."""
    import tempfile
    slides = [
        render_restart_cover(data),
        render_value_story(data),        # 01 · WHAT WSP WAS DRIVING (reuse)
        render_yoy_proof(data),          # 02 · THE EVENT RECAP (reuse)
        render_dark_days_calendar(data), # 03 · THE PROBLEM
        render_restart_ask(data),        # 04 · WHERE WE GO FROM HERE
    ]
    from pptx import Presentation
    from pptx.util import Inches
    prs = Presentation()
    prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)
    BLANK = prs.slide_layouts[6]
    with tempfile.TemporaryDirectory() as td:
        for i, slide_img in enumerate(slides):
            if slide_img.mode != "RGB":
                slide_img = slide_img.convert("RGB")
            png_path = f"{td}/slide_{i}.png"
            slide_img.save(png_path, "PNG", optimize=False)
            s = prs.slides.add_slide(BLANK)
            s.shapes.add_picture(png_path, 0, 0,
                                  width=prs.slide_width,
                                  height=prs.slide_height)
        out = io.BytesIO(); prs.save(out); out.seek(0)
        return out.read()


# =====================================================================
# VARIANT C — SWITCH TO 5% RULE
# Same opening as Variant B, but slide 3 reframes as "what erratic spend cost"
# and the ask is the budget-fixing rule rather than continuation.
# =====================================================================

def render_switch_to_5pct_ask(data: dict) -> Image.Image:
    """Variant C Ask — fixes lumpy spend, frames the rule as the unlock."""
    img = Image.new("RGB", (W, H), WHITE_T)
    d = ImageDraw.Draw(img)
    draw_ls(d, M, 90, "03  ·  WHERE WE GO FROM HERE",
            sans(22, bold=True), PURPLE_T, sp=3)
    d.text((M, 165),
           data.get('ask_title', "One rule fixes lumpy spend — for every supplier on it."),
           font=serif(58, bold=True), fill=INK_T)

    card_y = 360; card_h = 520
    card_w = (W - 2*M - 2*30) // 3
    card_gap = 30
    cards = data['pillars']
    for i, card in enumerate(cards[:3]):
        cx = M + i*(card_w + card_gap)
        d.rectangle([cx, card_y, cx + card_w, card_y + card_h], fill=LAV_T)
        d.rectangle([cx, card_y, cx + card_w, card_y + 10], fill=GOLD_T)
        draw_ls(d, cx + 35, card_y + 40, card['label'],
                sans(22, bold=True), PURPLE_T, sp=2)
        hero_color = tuple(CORAL_T) if card.get('is_loss') else DEEP_T
        d.text((cx + 35, card_y + 110), card['hero'],
               font=serif(95, bold=True, italic=True), fill=hero_color)
        body_lines = wrap(d, card['body'], card_w - 70, sans(24))
        for j, ln in enumerate(body_lines):
            d.text((cx + 35, card_y + 290 + j*36), ln, font=sans(24), fill=INK_T)

    ask_y = 920; ask_h = 220
    d.rectangle([M, ask_y, W - M, ask_y + ask_h], fill=DEEP_T)
    draw_ls(d, M + 40, ask_y + 32, "THE ASK", sans(24, bold=True), GOLD_T, sp=3)
    ask_amount = data['ask_amount_text']
    last_wsc = _fmt(data['last_month_wsc'])
    d.text((M + 40, ask_y + 80), "Set next month's WSP at  ", font=sans(40), fill=WHITE_T)
    cw1, _ = tsize(d, "Set next month's WSP at  ", sans(40))
    d.text((M + 40 + cw1, ask_y + 80), ask_amount,
           font=sans(40, bold=True), fill=GOLD_T)
    cw2, _ = tsize(d, ask_amount, sans(40, bold=True))
    d.text((M + 40 + cw1 + cw2, ask_y + 80), "  —  5% of last 30 days'",
           font=sans(40), fill=WHITE_T)
    d.text((M + 40, ask_y + 135),
           f"wholesale revenue (£{last_wsc}), set on day 1 — and every day 1 after.",
           font=sans(40), fill=WHITE_T)

    closing = data.get('ask_closing',
        f"Proven £{data['ws_roas']:.2f} back for every £1  ·  the gap to benchmark is now closed  ·  one rule, live on day 1.")
    d.text((M, H - 80), closing, font=serif(28, italic=True), fill=INK_T)
    return img


def build_deck_switch_to_5pct_c(data: dict) -> bytes:
    """Build a Variant C Switch-to-5% deck. Same data shape as Variant B."""
    import tempfile
    slides = [
        render_cover(data),
        render_value_story(data),
        render_yoy_proof(data),
        render_switch_to_5pct_ask(data),
    ]
    from pptx import Presentation
    from pptx.util import Inches
    prs = Presentation()
    prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)
    BLANK = prs.slide_layouts[6]
    with tempfile.TemporaryDirectory() as td:
        for i, slide_img in enumerate(slides):
            if slide_img.mode != "RGB":
                slide_img = slide_img.convert("RGB")
            png_path = f"{td}/slide_{i}.png"
            slide_img.save(png_path, "PNG", optimize=False)
            s = prs.slides.add_slide(BLANK)
            s.shapes.add_picture(png_path, 0, 0,
                                  width=prs.slide_width,
                                  height=prs.slide_height)
        out = io.BytesIO(); prs.save(out); out.seek(0)
        return out.read()


# =====================================================================
# Dispatcher — picks the right builder based on storyboard name
# =====================================================================
def build_deck(storyboard: str, data: dict) -> bytes:
    """Dispatch to the right builder based on storyboard name.

    Args:
        storyboard: storyboard name (with or without .md extension)
        data: structured data dict from data_prep

    Returns:
        .pptx bytes

    Raises:
        ValueError: if no builder is registered for the storyboard
    """
    key = storyboard.replace('.md', '').strip().split()[0]
    builders = {
        'value-review-variant-b':   build_deck_value_review_b,
        'restart-pitch-variant-a':  build_deck_restart_pitch_a,
        'switch-to-5pct-variant-c': build_deck_switch_to_5pct_c,
    }
    if key not in builders:
        raise ValueError(
            f"No builder for storyboard '{key}' yet. Available: {list(builders)}. "
            f"Other storyboards (promo-recap, summit, MBR) ship in v1.1."
        )
    return builders[key](data)
