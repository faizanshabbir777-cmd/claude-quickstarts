"""1-page data safety memo for Clement / Brian / IT to forward.
Designed to be the answer to 'is this safe to pilot?' in one read."""

from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1224, 1584  # US Letter @ 144 DPI

DEEP = (60, 26, 80); PURPLE = (123, 24, 159); LAV = (246, 235, 251)
GOLD = (212, 160, 23); INK = (26, 26, 26); SLATE = (91, 91, 102)
HAIR = (229, 222, 236); WHITE = (255, 255, 255); GREEN = (14, 143, 96)
CORAL = (184, 58, 58); CREAM = (250, 248, 252); MAGENTA = (124, 19, 132)


def serif(size, bold=False, italic=False):
    paths = {(True, True): "/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf",
             (True, False): "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
             (False, True): "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
             (False, False): "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"}
    p = paths.get((bold, italic))
    if p and os.path.exists(p): return ImageFont.truetype(p, size)
    return ImageFont.load_default()


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


def draw_ls(d, x, y, txt, f, fill, sp=2):
    cx = x
    for ch in txt:
        d.text((cx, y), ch, font=f, fill=fill)
        b = d.textbbox((0,0), ch, font=f); cx += (b[2]-b[0]) + sp


def wrap(d, t, mw, f):
    out, line = [], []
    for w in t.split():
        test = " ".join(line + [w])
        if tsize(d, test, f)[0] > mw: out.append(" ".join(line)); line = [w]
        else: line.append(w)
    if line: out.append(" ".join(line))
    return out


img = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(img)
M = 60

# --- Header band ---
d.rectangle([0, 0, W, 110], fill=MAGENTA)
d.rectangle([0, 110, W, 116], fill=GOLD)
if os.path.exists("/tmp/forte_deck/wayfair_logo_white.png"):
    logo = Image.open("/tmp/forte_deck/wayfair_logo_white.png").convert("RGBA")
    logo.thumbnail((140, 60)); img.paste(logo, (M, 28), logo)
draw_ls(d, M + 200, 30, "WSP PITCH BUILDER  ·  DATA SAFETY MEMO",
        sans(13, bold=True), GOLD, sp=2)
d.text((M + 200, 55), "1-page brief for leadership forwarding",
       font=sans(22, bold=True), fill=WHITE)
# right side: classified
d.text((W - M - 280, 35), "INTERNAL · v0.4.2",
       font=sans(13, bold=True), fill=GOLD)
d.text((W - M - 280, 58), "Pilot scope · 2-week window",
       font=sans(13), fill=WHITE)
d.text((W - M - 280, 78), "Author: Faizan Shabbir · EU WSP Lead",
       font=sans(11), fill=(220, 200, 220))

# --- Title ---
y = 145
d.text((M, y), "Can we pilot this safely?",
       font=serif(36, bold=True, italic=True), fill=INK)
y += 60

# --- TL;DR box ---
d.rectangle([M, y, W-M, y+135], fill=LAV)
d.rectangle([M, y, M+8, y+135], fill=GREEN)
d.text((M+22, y+14), "✓  TL;DR — YES, IF",
       font=sans(15, bold=True), fill=GREEN)
tldr_lines = [
    "1.  The pilot Streamlit URL uses DEMO DATA ONLY — no real supplier",
    "    files uploaded · the password gate is rotated from the example",
    "    in the repo · pilot CMs are told this in writing.",
    "2.  Real-data builds wait for the Wayfair-internal deployment in",
    "    pilot week 2 (Wayfair SSO, EU residency, normal audit).",
]
for i, l in enumerate(tldr_lines):
    d.text((M+30, y+44+i*18), l, font=sans(13), fill=INK)
y += 155

# --- What does it handle / what doesn't ---
d.text((M, y), "What the system handles",
       font=sans(14, bold=True), fill=PURPLE)
draw_ls(d, M, y+22, "DATA CLASSIFICATION  ·  PILOT VERSION",
        sans(10, bold=True), MAGENTA, sp=2)
y += 50

# Two-column table
col_w = (W - 2*M - 20) // 2
cols = [
    (GREEN, "✓  Allowed in pilot", [
        "Storyboard names · brand palette",
        "Supplier names (Monty Trading, Forte UK, TuttiBambini)",
        "Demo metrics (already public artefacts on team Slack)",
        "Pilot password (hmac-compared, never logged)",
    ]),
    (CORAL, "✗  Forbidden in pilot", [
        "Real supplier CSVs (uploader is UI-only · no ingest)",
        "GRS · retail revenue · internal-only benchmarks",
        "Looker API calls · BigQuery queries",
        "Anthropic API calls (Build button is stubbed in v0.1)",
    ]),
]
for i, (color, head, rows) in enumerate(cols):
    cx = M + i * (col_w + 20)
    d.rectangle([cx, y, cx + col_w, y + 175], fill=CREAM)
    d.rectangle([cx, y, cx + col_w, y + 4], fill=color)
    d.text((cx + 16, y + 14), head, font=sans(13, bold=True), fill=color)
    for j, r in enumerate(rows):
        d.text((cx + 16, y + 44 + j*30), "·", font=sans(14, bold=True), fill=color)
        for k, ln in enumerate(wrap(d, r, col_w - 35, sans(12))):
            d.text((cx + 28, y + 44 + j*30 + k*14), ln, font=sans(12), fill=INK)
y += 195

# --- Controls in the code ---
d.text((M, y), "Controls already in the code",
       font=sans(14, bold=True), fill=PURPLE)
y += 28
controls = [
    ("Password gate", "hmac-compared shared secret · no bypass"),
    ("HTTPS everywhere", "Streamlit Cloud terminates TLS · no plaintext"),
    ("XSRF protection on", "config.toml flag · cookies signed, requests checked"),
    ("Upload size capped", "50MB · prevents DOS via huge files"),
    ("File-type allowlist", "CSV / XLSX only · no executables, no archives"),
    ("No telemetry", "gatherUsageStats = false · no Streamlit telemetry"),
    ("Session isolation", "each CM's session state is independent · no leakage"),
    ("Rule #1 enforced structurally", "supplier-facing audience locks GRS code path · unreachable"),
]
for head, body in controls:
    d.rectangle([M, y+4, M+8, y+16], fill=GOLD)
    d.text((M+18, y), head, font=sans(12, bold=True), fill=DEEP)
    hw, _ = tsize(d, head, sans(12, bold=True))
    d.text((M+18+hw+8, y), "— " + body, font=sans(12), fill=INK)
    y += 22
y += 12

# --- What we don't promise ---
d.rectangle([M, y, W-M, y+108], fill=CREAM)
d.rectangle([M, y, M+8, y+108], fill=CORAL)
d.text((M+22, y+12), "What we DON'T promise in pilot v0.1",
       font=sans(13, bold=True), fill=CORAL)
non_promises = [
    "Streamlit Cloud is US-hosted (AWS) · not Wayfair-internal · pilot URL is demo only",
    "No formal pen-test on v0.1 · security review = pilot week 2 work",
    "No GDPR DPA on pilot URL · production version uses Wayfair existing infra contracts",
]
for i, l in enumerate(non_promises):
    d.text((M+30, y+38+i*22), "·", font=sans(14, bold=True), fill=CORAL)
    d.text((M+42, y+38+i*22), l, font=sans(12), fill=INK)
y += 125

# --- Bottom: pre-greenlight checklist ---
d.text((M, y), "Pre-greenlight checklist for platform team",
       font=sans(14, bold=True), fill=PURPLE)
y += 28
checks = [
    "Pilot URL is not externally indexable · noindex set or app in private mode",
    "Pilot password rotated from the example value in secrets.toml.example",
    "Demo PPTX files reviewed as shareable demo assets (confirm with Faizan/Brian)",
    "Pilot CMs told in writing NOT to enter real supplier data on the URL",
    "Production deploy plan scoped for pilot week 2 (infra · SSO · platform contact)",
]
for c in checks:
    d.rectangle([M, y+4, M+14, y+18], outline=DEEP, width=2)
    for k, ln in enumerate(wrap(d, c, W - M*2 - 30, sans(12))):
        d.text((M+22, y + k*16), ln, font=sans(12), fill=INK)
    y += max(22, 16 * len(wrap(d, c, W - M*2 - 30, sans(12))))

# --- Footer ---
d.rectangle([0, H-65, W, H], fill=DEEP)
d.text((M, H-50),
       "Full doc: github.com/faizanshabbir777-cmd/claude-quickstarts/blob/main/wayfair-eu-supplier-marketing/dashboard/DATA_SAFETY.md",
       font=sans(11, mono=True), fill=(230, 200, 230))
d.text((M, H-30),
       "Pilot contact (while Faizan is out): Brian Delsignore · Production sign-off: Clement Delay + platform team lead",
       font=sans(11), fill=(220, 200, 220))

img.save("/tmp/forte_deck/Leadership_Data_Safety_Memo.pdf", "PDF", resolution=144)
img.save("/tmp/forte_deck/Leadership_Data_Safety_Memo.png", "PNG", optimize=True)
print("Saved Leadership_Data_Safety_Memo.pdf and .png")
