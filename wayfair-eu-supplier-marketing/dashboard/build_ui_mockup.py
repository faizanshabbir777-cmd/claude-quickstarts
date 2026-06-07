"""WSP Pitch Builder — UI mockup matching the EURTA NART / InfoHub aesthetic.
Models a dashboard CMs would use without touching a terminal."""

from PIL import Image, ImageDraw, ImageFont
import os

W, H = 2800, 1750  # high-res mockup

# Wayfair InfoHub palette (sampled from the screenshot)
HEADER_MAGENTA = (124, 19, 132)      # #7C1384 — the deep magenta header
HEADER_LIGHT   = (160, 50, 168)
PINK_LABEL     = (197, 37, 154)      # #C5259A — section eyebrows
CREAM_BG       = (248, 244, 237)     # off-white page bg
WHITE_T        = (255, 255, 255)
DARK_GREY      = (80, 80, 88)
LIGHT_GREY     = (220, 215, 225)
PURPLE_TAB     = (124, 19, 132)
TAB_INACTIVE   = (150, 150, 160)
INPUT_BORDER   = (200, 195, 210)
INPUT_BG       = (255, 255, 255)
INK            = (40, 40, 48)
SLATE          = (110, 110, 122)
GOLD           = (212, 160, 23)
GREEN          = (14, 143, 96)
LAV            = (246, 235, 251)


def sans(size, bold=False, italic=False, mono=False):
    if mono:
        return ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf", size)
    paths = {(True, True): "/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf",
             (True, False): "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
             (False, True): "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf",
             (False, False): "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"}
    p = paths.get((bold, italic))
    if p and os.path.exists(p): return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def tsize(d, t, f):
    b = d.textbbox((0,0), t, font=f); return b[2]-b[0], b[3]-b[1]


img = Image.new("RGB", (W, H), CREAM_BG)
d = ImageDraw.Draw(img)


# =========================================================================
# TOP TAB BAR — matches "Pricing Structure | Price/Margin/Strategy..." row
# =========================================================================
tab_y = 0
tab_h = 110
d.rectangle([0, 0, W, tab_h], fill=CREAM_BG)
tabs = [
    ("📊", "Storyboards",       True),
    ("📈", "Filters",            False),
    ("📋", "Data Preview",       False),
    ("⚙",  "Build",              False),
    ("👁",  "Preview & QA",       False),
    ("✉",  "Send",               False),
    ("📚", "Skill Library",       False),
    ("ℹ",  "Definitions",         False),
]
tab_w = W // len(tabs)
for i, (icon, label, active) in enumerate(tabs):
    cx = i * tab_w + tab_w // 2
    color = PURPLE_TAB if active else TAB_INACTIVE
    # icon
    f_icon = sans(32)
    iw, _ = tsize(d, icon, f_icon)
    d.text((cx - iw // 2, 18), icon, font=f_icon, fill=color)
    # label
    f_lbl = sans(20, bold=active)
    lw, _ = tsize(d, label, f_lbl)
    d.text((cx - lw // 2, 60), label, font=f_lbl, fill=color)
    # active underline
    if active:
        d.rectangle([cx - 100, 100, cx + 100, 105], fill=PURPLE_TAB)


# =========================================================================
# MAGENTA HEADER BAR — matches "Cost Stack / Current Pricing Structure"
# =========================================================================
hdr_y = tab_h
hdr_h = 110
d.rectangle([0, hdr_y, W, hdr_y + hdr_h], fill=HEADER_MAGENTA)

# Left logo + breadcrumb
if os.path.exists("/tmp/forte_deck/wayfair_logo_white.png"):
    logo = Image.open("/tmp/forte_deck/wayfair_logo_white.png").convert("RGBA")
    logo.thumbnail((150, 70))
    img.paste(logo, (30, hdr_y + 20), logo)

f_breadcrumb = sans(38)
d.text((230, hdr_y + 35), "WSP Builder /",
       font=f_breadcrumb, fill=(220, 195, 220))
bw, _ = tsize(d, "WSP Builder /", f_breadcrumb)
d.text((250 + bw, hdr_y + 30), "Pitch Deck Generation",
       font=sans(44, bold=True), fill=WHITE_T)

# Right-side action chips (OVERVIEW, PLAYBOOK, INFOHUB, Slack) — moved left of branding
chip_y = hdr_y + 18
chip_h = 74
chip_w = 120
chips = [
    ("🏠", "OVERVIEW"),
    ("📖", "PLAYBOOK"),
    ("ℹ", "INFOHUB"),
    ("💬", "SLACK"),
]
cx = W - 540   # leaves room for the CM Champions branding on the right
for icon, label in reversed(chips):
    cx -= chip_w + 10
    # Box with white border (matches InfoHub button style)
    d.rectangle([cx, chip_y, cx + chip_w, chip_y + chip_h], outline=WHITE_T, width=2)
    d.text((cx + chip_w//2 - 16, chip_y + 8), icon, font=sans(28), fill=WHITE_T)
    lw, _ = tsize(d, label, sans(13, bold=True))
    d.text((cx + chip_w//2 - lw//2, chip_y + 50), label, font=sans(13, bold=True), fill=WHITE_T)

# Far-right branding strip
d.text((W - 460, hdr_y + 35), "EU CM CHAMPIONS",
       font=sans(20, bold=True), fill=WHITE_T)
d.text((W - 460, hdr_y + 65), "WAYFAIR SPONSORED PRODUCTS",
       font=sans(13), fill=(220, 200, 220))


# =========================================================================
# CONTENT AREA — PORTFOLIO FILTERS PANEL
# =========================================================================
content_y = tab_h + hdr_h + 30
M = 40   # margin

# Section title
d.text((M, content_y), "Pitch Filters",
       font=sans(28, bold=True), fill=HEADER_MAGENTA)
d.text((M + 220, content_y + 10),
       "(applied across all storyboards)",
       font=sans(20, italic=True), fill=SLATE)
content_y += 60


# Filter group renderer
def render_filter_group(label, dropdowns, x, y, w, h, label_color=PINK_LABEL):
    # Pink section eyebrow
    d.text((x, y), label, font=sans(18, bold=True), fill=label_color)
    cur_y = y + 30
    rows = (len(dropdowns) + 1) // 2
    row_h = (h - 30) // max(rows, 1)
    col_w = (w - 16) // 2
    for i, (lbl, hint) in enumerate(dropdowns):
        col = i % 2
        row = i // 2
        dx = x + col * (col_w + 16)
        dy = cur_y + row * row_h
        dropdown(dx, dy, col_w, row_h - 10, lbl, hint)


def dropdown(x, y, w, h, label, placeholder=""):
    d.rectangle([x, y, x + w, y + h], outline=INPUT_BORDER, width=1, fill=INPUT_BG)
    d.text((x + 12, y + 8), label, font=sans(13, bold=True), fill=SLATE)
    if placeholder:
        d.text((x + 12, y + 30), placeholder, font=sans(15), fill=INK)
    # down arrow
    arrow_x = x + w - 22
    arrow_y = y + h // 2 - 4
    d.polygon([(arrow_x, arrow_y), (arrow_x + 12, arrow_y), (arrow_x + 6, arrow_y + 8)],
              fill=SLATE)


# Two-row grid of filter panels — match InfoHub style precisely
panel_w = (W - 2*M - 30) // 4
panel_gap = 30
y_row1 = content_y

# Group 1 — Supplier Selection (leftmost, like "Catalog Granularity")
render_filter_group(
    "Supplier Selection",
    [
        ("Supplier Name",   "Monty Trading Ltd"),
        ("Supplier ID",     "37802"),
        ("Brand Catalog",   "Wayfair UK"),
        ("Vertical",        "Dining · Outdoor"),
    ],
    M, y_row1, panel_w, 300
)

# Group 2 — Brief & Storyboard
render_filter_group(
    "Brief & Storyboard",
    [
        ("Pitch Variant",   "B · Continue at current pace"),
        ("Storyboard",      "value-review-variant-b.md"),
        ("Audience",        "Supplier-facing"),
        ("Currency",        "GBP at 1:1 from USD"),
    ],
    M + panel_w + panel_gap, y_row1, panel_w, 300
)

# Group 3 — Period
render_filter_group(
    "Period",
    [
        ("Reporting Month", "April 2026"),
        ("Trailing Window", "L12M"),
        ("YoY Compare",     "April 2025 (auto)"),
        ("Last-30-days WSC","Locked at landed"),
    ],
    M + 2*(panel_w + panel_gap), y_row1, panel_w, 300
)

# Group 4 — Account team
render_filter_group(
    "Account Team",
    [
        ("CM Champion",     "(auto-fills from SSO)"),
        ("SRM",             "(auto-fills from SuID)"),
        ("WPP Supplier?",   "Yes"),
        ("Supplier Tier",   "Tier 1 · EU Champion"),
    ],
    M + 3*(panel_w + panel_gap), y_row1, panel_w, 300
)


# ====== SECOND ROW — Promo + advanced ======
y_row2 = y_row1 + 340

# Group 5 — Promo (only relevant if storyboard = promo-recap)
render_filter_group(
    "Promo Window (only if Storyboard = Promo Recap)",
    [
        ("Event Name",      "—"),
        ("Promo Start",     "—"),
        ("Promo End",       "—"),
        ("Pre-Period Start","—"),
    ],
    M, y_row2, panel_w * 2 + panel_gap, 200,
    label_color=SLATE
)

# Group 6 — Output settings
render_filter_group(
    "Output",
    [
        ("Filename Format", "{Supplier}_{Period}_WSP_Deck.pptx"),
        ("Save To",         "./outputs/"),
        ("Run QA Loop",     "Yes (LibreOffice → JPG)"),
        ("Visual Register", "TuttiBambini (default)"),
    ],
    M + 2*(panel_w + panel_gap), y_row2, panel_w * 2 + panel_gap, 200
)


# =========================================================================
# BUILD STRIP — big purple action button + status
# =========================================================================
build_y = y_row2 + 240
build_h = 130

# Left: build button
btn_x = M
btn_w = 380
d.rectangle([btn_x, build_y, btn_x + btn_w, build_y + build_h],
            fill=HEADER_MAGENTA)
d.text((btn_x + 30, build_y + 25), "▶  Build Pitch Deck",
       font=sans(28, bold=True), fill=WHITE_T)
d.text((btn_x + 30, build_y + 78),
       "≈ 90 seconds  ·  QA loop included",
       font=sans(16), fill=(230, 200, 230))

# Status timeline (centered)
status_x = btn_x + btn_w + 60
status_w = 1200
d.rectangle([status_x, build_y, status_x + status_w, build_y + build_h],
            fill=WHITE_T, outline=LIGHT_GREY)
d.text((status_x + 20, build_y + 14), "PIPELINE STATUS",
       font=sans(14, bold=True), fill=PINK_LABEL)
# Pipeline steps
steps = [("Data prep", True), ("Storyboard fill", True),
         ("Render", False), ("QA loop", False), ("Ready", False)]
step_x = status_x + 30
step_w = (status_w - 60) // len(steps)
for i, (name, done) in enumerate(steps):
    sx = step_x + i * step_w
    # circle
    cx, cy = sx + 20, build_y + 75
    color = GREEN if done else LIGHT_GREY
    d.ellipse([cx-12, cy-12, cx+12, cy+12], fill=color)
    if done:
        d.text((cx-7, cy-9), "✓", font=sans(18, bold=True), fill=WHITE_T)
    # line to next
    if i < len(steps) - 1:
        line_color = GREEN if done and steps[i+1][1] else LIGHT_GREY
        d.line([(cx + 12, cy), (sx + step_w - 12, cy)], fill=line_color, width=3)
    # label
    d.text((sx + 5, build_y + 95), name, font=sans(14), fill=DARK_GREY)

# Right: deck info
out_x = status_x + status_w + 60
out_w = W - out_x - M
d.rectangle([out_x, build_y, out_x + out_w, build_y + build_h],
            fill=LAV, outline=HEADER_MAGENTA)
d.text((out_x + 20, build_y + 14), "WHEN IT'S READY",
       font=sans(14, bold=True), fill=HEADER_MAGENTA)
d.text((out_x + 20, build_y + 38),
       "📥  Download .pptx",
       font=sans(22, bold=True), fill=HEADER_MAGENTA)
d.text((out_x + 20, build_y + 70),
       "📨  Send to SRM (Slack)",
       font=sans(22, bold=True), fill=HEADER_MAGENTA)
d.text((out_x + 20, build_y + 102),
       "👁  Preview slides (QA tab)",
       font=sans(22, bold=True), fill=HEADER_MAGENTA)


# =========================================================================
# BOTTOM PREVIEW STRIP — storyboard scaffold preview
# =========================================================================
preview_y = build_y + 170
d.text((M, preview_y),
       "Storyboard preview — value-review-variant-b.md",
       font=sans(20, bold=True), fill=HEADER_MAGENTA)
d.text((M, preview_y + 30),
       "The agent will fill this scaffold with your filtered data. You can override any title or pillar before render.",
       font=sans(15, italic=True), fill=SLATE)

slide_y = preview_y + 75
slide_h = 230
slide_gap = 20
slide_count = 4
slide_w = (W - 2*M - slide_gap*(slide_count-1)) // slide_count

slide_descriptions = [
    ("Slide 1  ·  COVER",
     "Deep purple bg · gold eyebrow · serif italic title 'Keep your WSP on at this pace.' · 4 KPI cards"),
    ("Slide 2  ·  01 · WHAT WSP IS DOING",
     "Lavender £5.71 hero card · monthly bar chart · italic takeaway sentence"),
    ("Slide 3  ·  02 · APRIL '26 vs APRIL '25",
     "Deep purple KPI band with green delta pills · lavender 'Above benchmark' callout"),
    ("Slide 4  ·  03 · WHERE WE GO FROM HERE",
     "Three pillar cards · DEEP PURPLE 'THE ASK' card · gold-highlighted £-amount"),
]

for i, (name, desc) in enumerate(slide_descriptions):
    sx = M + i * (slide_w + slide_gap)
    # Card
    d.rectangle([sx, slide_y, sx + slide_w, slide_y + slide_h],
                fill=WHITE_T, outline=INPUT_BORDER)
    # Top tab
    d.rectangle([sx, slide_y, sx + slide_w, slide_y + 4], fill=HEADER_MAGENTA)
    # Slide name
    d.text((sx + 15, slide_y + 18), name, font=sans(15, bold=True), fill=HEADER_MAGENTA)
    # Description (wrap)
    f_d = sans(13)
    words = desc.split()
    lines = []; line = []
    for w in words:
        test = " ".join(line + [w])
        if tsize(d, test, f_d)[0] > slide_w - 30:
            lines.append(" ".join(line)); line = [w]
        else: line.append(w)
    if line: lines.append(" ".join(line))
    for j, ln in enumerate(lines):
        d.text((sx + 15, slide_y + 50 + j*18), ln, font=f_d, fill=INK)

    # "View scaffold" link at bottom
    d.text((sx + 15, slide_y + slide_h - 30), "View scaffold ▸",
           font=sans(13, bold=True), fill=HEADER_MAGENTA)


# =========================================================================
# Footer with link back to Operator Pack
# =========================================================================
d.rectangle([0, H - 70, W, H], fill=HEADER_MAGENTA)
d.text((M, H - 50),
       "WSP Pitch Builder  ·  v0.1 mockup  ·  built on the wayfair-supplier-pitching skill (v0.4.0)",
       font=sans(15), fill=WHITE_T)
d.text((W - 700, H - 50),
       "github.com/faizanshabbir777-cmd/claude-quickstarts  ·  Faizan Shabbir, EU WSP Lead",
       font=sans(13, mono=True), fill=(230, 200, 230))

img.save("/tmp/forte_deck/WSP_Builder_UI_Mockup.png", "PNG", optimize=True)

# Also save as PDF for sharing
img_rgb = img.convert("RGB")
img_rgb.save("/tmp/forte_deck/WSP_Builder_UI_Mockup.pdf", "PDF", resolution=144)

print("Saved WSP_Builder_UI_Mockup.png and .pdf")
