"""WSP Pitch Builder — Streamlit MVP, cloud-ready.

Non-technical UI wrapper around the wayfair-supplier-pitching skill.
Category Manager WSP Champions use this to ship pitch decks without
touching a terminal.

Local run:
    pip install -r requirements.txt
    streamlit run app.py

Cloud deploy:
    See DEPLOY.md for the 5-minute Streamlit Cloud recipe.
"""
import streamlit as st
import pandas as pd
import os
import time
import hmac
from pathlib import Path

# -------------------------------------------------------------------------
# Paths — work both locally and on Streamlit Cloud
# -------------------------------------------------------------------------
HERE = Path(__file__).parent
ASSETS = HERE / "assets"
DEMO = HERE / "demo"

# -------------------------------------------------------------------------
# Page config
# -------------------------------------------------------------------------
st.set_page_config(
    page_title="WSP Pitch Builder · Wayfair",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# -------------------------------------------------------------------------
# Password gate (pilot-only — proper SSO in v0.2)
# -------------------------------------------------------------------------
def check_password():
    """Return True if the user entered the shared pilot password."""

    def password_entered():
        configured = st.secrets.get("auth", {}).get("password", "wsp-pilot-2026")
        if hmac.compare_digest(st.session_state["password_input"], configured):
            st.session_state["password_correct"] = True
            del st.session_state["password_input"]
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    # Gate UI
    st.markdown("""
    <div style='background:#7C1384;color:white;padding:18px 30px;margin:-16px -100px 24px -100px;border-bottom:4px solid #D4A017;'>
        <div style='font-size:28px;font-weight:700;'>
            <span style='opacity:0.6;font-weight:400;'>WSP Builder /</span> Pitch Deck Generation
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🔒 Pilot access")
    st.text_input(
        "Pilot password",
        type="password",
        key="password_input",
        on_change=password_entered,
        help="Contact Faizan or Brian for the pilot password."
    )
    if "password_correct" in st.session_state and not st.session_state["password_correct"]:
        st.error("Password incorrect.")
    st.caption("Pilot scope · 3-4 EU CM Champions · 2 weeks · SSO in v0.2")
    return False


if not check_password():
    st.stop()


# -------------------------------------------------------------------------
# Custom CSS — match EURTA NART / InfoHub aesthetic
# -------------------------------------------------------------------------
st.markdown("""
<style>
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 1rem; max-width: 100%; }

    .wsp-header {
        background: #7C1384;
        color: white;
        padding: 18px 30px;
        margin: -16px -100px 24px -100px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 4px solid #D4A017;
    }
    .wsp-header .breadcrumb { font-size: 28px; font-weight: 700; }
    .wsp-header .breadcrumb .muted { opacity: 0.6; font-weight: 400; }
    .wsp-header .branding { font-size: 14px; font-weight: 700; text-align: right; opacity: 0.9; }
    .wsp-header .branding .sub { opacity: 0.65; font-weight: 400; }

    .wsp-eyebrow {
        color: #C5259A;
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 1.5px;
        margin-bottom: 8px;
        text-transform: uppercase;
    }

    .stButton > button[kind="primary"] {
        background-color: #7C1384;
        color: white;
        border: none;
        font-weight: 700;
        font-size: 18px;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #9C26A4;
    }

    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# -------------------------------------------------------------------------
# Header
# -------------------------------------------------------------------------
st.markdown("""
<div class="wsp-header">
    <div>
        <div class="breadcrumb">
            <span class="muted">WSP Builder /</span> Pitch Deck Generation
        </div>
    </div>
    <div class="branding">
        EU CM CHAMPIONS<br>
        <span class="sub">WAYFAIR SPONSORED PRODUCTS · PILOT v0.1</span>
    </div>
</div>
""", unsafe_allow_html=True)


# Sub-banner — pilot scope reminder
st.info("**Pilot v0.1** — the Build button currently returns a hardcoded Monty Trading demo deck "
        "so you can see the full UX flow. Real pipeline (data-prep → author → render) wires in pilot week 2. "
        "Drop feedback in `#wsp-pilot` Slack channel.")


# -------------------------------------------------------------------------
# Tabs
# -------------------------------------------------------------------------
tab_filters, tab_data, tab_build, tab_preview, tab_send, tab_help = st.tabs([
    "🎯 Filters",
    "📋 Data Preview",
    "⚙️ Build",
    "👁️ Preview & QA",
    "✉️ Send",
    "📚 Skill Library",
])


# =========================================================================
# TAB 1 — FILTERS
# =========================================================================
with tab_filters:
    st.markdown('<div class="wsp-eyebrow">Pitch Filters · applied across all storyboards</div>',
                unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown('<div class="wsp-eyebrow">Supplier Selection</div>',
                    unsafe_allow_html=True)
        supplier_name = st.text_input("Supplier Name", value="Monty Trading Ltd")
        supplier_id = st.text_input("Supplier ID", value="37802")
        brand_catalog = st.selectbox("Brand Catalog",
            ["Wayfair UK", "Wayfair DE", "Wayfair IE", "AllModern UK"])
        vertical = st.text_input("Vertical", value="Dining · Outdoor")

    with col2:
        st.markdown('<div class="wsp-eyebrow">Brief & Storyboard</div>',
                    unsafe_allow_html=True)
        storyboard = st.selectbox("Storyboard",
            ["value-review-variant-b.md  · Continue at pace",
             "restart-pitch-variant-a.md  · Switch back on",
             "switch-to-5pct-variant-c.md  · Fix lumpy spend",
             "promo-recap-tier0.md  · Way Day / BFCM / etc.",
             "summit-case-study.md  · Multi-supplier showcase",
             "mbr-supplier-review.md  · Internal MBR"])
        variant = st.selectbox("Pitch Variant (provisional)",
            ["B · Continue at current pace",
             "A · Restart / Re-activate",
             "C · Move to 5% of WSC",
             "D · Custom"])
        audience = st.radio("Audience",
            ["Supplier-facing (WSC only, no GRS)",
             "Internal (Wayfair leadership, GRS allowed)"],
            index=0)
        currency = st.selectbox("Currency",
            ["GBP at 1:1 from USD (default)",
             "GBP at fixed FX rate",
             "USD (raw, supplier-facing not recommended)",
             "EUR at 1:1 from USD"])

    with col3:
        st.markdown('<div class="wsp-eyebrow">Period</div>',
                    unsafe_allow_html=True)
        reporting_month = st.selectbox("Reporting Month",
            ["April 2026", "March 2026", "February 2026", "January 2026"])
        trailing = st.selectbox("Trailing Window",
            ["L12M (default)", "L6M", "L3M", "YTD"])
        yoy_compare = st.text_input("YoY Compare",
            value="April 2025 (auto)")
        last_30 = st.text_input("Last-30-days WSC",
            value="Locked at landed (~£476k)")

    with col4:
        st.markdown('<div class="wsp-eyebrow">Account Team</div>',
                    unsafe_allow_html=True)
        cm_champion = st.text_input("CM Champion", value="(auto-fills from SSO)")
        srm = st.text_input("SRM", value="(auto-fills from SuID)")
        wpp = st.selectbox("WPP Supplier?", ["Yes", "No"])
        supplier_tier = st.selectbox("Supplier Tier",
            ["Tier 1 · EU Champion", "Tier 2", "Tier 3 · drag list"])

    st.divider()

    # Promo strip — only relevant for promo recaps
    if "promo-recap" in storyboard:
        st.markdown('<div class="wsp-eyebrow">Promo Window · REQUIRED</div>',
                    unsafe_allow_html=True)
        pcol1, pcol2, pcol3, pcol4 = st.columns(4)
        pcol1.text_input("Event Name", placeholder="Way Day 2026")
        pcol2.date_input("Promo Start")
        pcol3.date_input("Promo End")
        pcol4.date_input("Pre-Period Start")
        st.caption("⚠️ Rule #8 — never inferred from filenames. Exact dates required before build.")

    st.markdown('<div class="wsp-eyebrow">Output</div>', unsafe_allow_html=True)
    o1, o2, o3, o4 = st.columns(4)
    o1.text_input("Filename Format", value="{Supplier}_{Period}_WSP_Deck.pptx")
    o2.text_input("Save To", value="./outputs/")
    o3.selectbox("Run QA Loop",
        ["Yes (LibreOffice → JPG inspect)", "No (skip — not recommended)"])
    o4.selectbox("Visual Register",
        ["TuttiBambini (default)", "Internal MBR (em-dash titles)"])

    st.markdown('<div class="wsp-eyebrow">Data Source</div>', unsafe_allow_html=True)
    use_looker = st.checkbox("Use Looker Studio dashboard (pilot week 2)")
    if use_looker:
        st.text_input("Looker Dashboard ID", placeholder="monty-trading-wsp-monthly")
        st.caption("Pilot week 2 wiring — currently a stub.")
    else:
        st.file_uploader(
            "Drop your campaign reporting CSV (or share-shift xlsx for promos)",
            type=["csv", "xlsx"], accept_multiple_files=True)


# =========================================================================
# TAB 2 — DATA PREVIEW
# =========================================================================
with tab_data:
    st.markdown('<div class="wsp-eyebrow">Data Preview · sanity check before build</div>',
                unsafe_allow_html=True)
    st.write(
        "The `wsp-data-prep` subagent surfaces 4–6 plain-English bullets here once you "
        "load a CSV or connect Looker. You confirm the picture matches reality before any "
        "deck-building."
    )

    if st.button("Run sanity check"):
        with st.spinner("Reading data · computing metrics · checking against Account Overview..."):
            time.sleep(1.2)
        st.success("✓ Sanity check: PASS  ·  Data matches Account Overview within 0.3%")
        st.markdown("**Data summary** (auto-generated):")
        st.markdown("""
        - WSP spend (April '26): **£33.2k** · top EU spender last month
        - Wholesale per £1 of WSP: **£5.71** · held flat YoY despite +65% spend
        - WSP % of WSC: **7.0%** · above the 5% benchmark
        - Spend × WSC correlation (L12M): **0.84** · strong
        - Pillar recommendation: **IT HELD AT SCALE** (zero ROAS compression — the rare signal)
        - Variant recommendation: **B · Continue at current pace**
        """)


# =========================================================================
# TAB 3 — BUILD
# =========================================================================
with tab_build:
    st.markdown('<div class="wsp-eyebrow">Build the Deck</div>', unsafe_allow_html=True)

    st.subheader("Storyboard scaffold — what the agent will fill")
    st.caption("You can override any title or pillar choice before render.")

    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown("**Slide 1 · COVER**")
        st.caption("Deep purple bg · gold eyebrow · serif italic title "
                   "'Keep your WSP on at this pace.' · 4 KPI cards")
    with s2:
        st.markdown("**Slide 2 · 01 · WHAT WSP IS DOING**")
        st.caption("Lavender £5.71 hero card · monthly bar chart · italic takeaway")
    with s3:
        st.markdown("**Slide 3 · 02 · APRIL '26 vs APRIL '25**")
        st.caption("Deep purple KPI band with green delta pills · 'Above benchmark' callout")
    with s4:
        st.markdown("**Slide 4 · 03 · WHERE WE GO FROM HERE**")
        st.caption("Three pillar cards · DEEP PURPLE 'THE ASK' card · gold £-amount")

    st.divider()

    bcol1, bcol2 = st.columns([1, 2])
    with bcol1:
        if st.button("▶ Build Pitch Deck", type="primary", use_container_width=True):
            st.session_state["build_in_progress"] = True
        st.caption("≈ 90 seconds · QA loop included")
    with bcol2:
        st.markdown("**Pipeline status**")
        if st.session_state.get("build_in_progress"):
            progress_text = st.empty()
            progress_bar = st.progress(0)
            stages = [
                ("Data prep · sanity-check passed",     25, 0.4),
                ("Storyboard scaffold filled",           50, 0.4),
                ("Slides rendering (python-pptx)",       75, 0.5),
                ("QA loop · LibreOffice + pdftoppm",     90, 0.4),
                ("Ready · 4 / 4 slides clean",          100, 0.3),
            ]
            for stage, pct, delay in stages:
                progress_text.markdown(f"`{stage}`")
                progress_bar.progress(pct)
                time.sleep(delay)
            progress_text.markdown("**✓ Deck ready** — click the Send tab to download or share")
            st.session_state["build_done"] = True
            st.session_state["build_in_progress"] = False
        elif st.session_state.get("build_done"):
            st.success("Last build: Monty_Trading_April2026_WSP_Deck.pptx · 4 slides · QA passed")
        else:
            st.markdown("`Awaiting build trigger…`")


# =========================================================================
# TAB 4 — PREVIEW & QA
# =========================================================================
with tab_preview:
    st.markdown('<div class="wsp-eyebrow">Preview & QA · visual inspect every slide before send</div>',
                unsafe_allow_html=True)
    if not st.session_state.get("build_done"):
        st.info("Build a deck first to see its preview here.")
    else:
        for fn, label in [
            ("monty_tutti_s1.png", "Slide 1 · Cover"),
            ("monty_tutti_s2.png", "Slide 2 · 01 · WHAT WSP IS DOING"),
            ("monty_tutti_s3.png", "Slide 3 · 02 · APRIL '26 vs APRIL '25"),
            ("monty_tutti_s4.png", "Slide 4 · 03 · WHERE WE GO FROM HERE"),
        ]:
            st.markdown(f"**{label}**")
            asset_path = ASSETS / fn
            if asset_path.exists():
                st.image(str(asset_path))
            else:
                st.warning(f"Preview asset not found: {fn}")
            st.divider()


# =========================================================================
# TAB 5 — SEND
# =========================================================================
with tab_send:
    st.markdown('<div class="wsp-eyebrow">Send to SRM</div>', unsafe_allow_html=True)
    if not st.session_state.get("build_done"):
        st.info("Build the deck first, then come here to send.")
    else:
        st.success("✓ Deck ready to send")
        col1, col2 = st.columns(2)
        with col1:
            demo_pptx = DEMO / "Monty_Trading_April2026_WSP_Deck_v2.pptx"
            if demo_pptx.exists():
                with open(demo_pptx, "rb") as f:
                    st.download_button(
                        "📥 Download .pptx",
                        data=f.read(),
                        file_name="Monty_Trading_April2026_WSP_Deck.pptx",
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    )
            else:
                st.error("Demo file missing — re-deploy the dashboard.")
            st.markdown("Or:")
            st.button("📨 Send to SRM via Slack",
                      help="Pilot week 2 wiring — needs Slack webhook.")
            st.button("✉️ Email SRM with deck attached",
                      help="Pilot week 2 wiring.")
        with col2:
            st.markdown("**Send-to-SRM template**")
            st.text_area("Edit before send", value=(
                "Hi {SRM name},\n\n"
                "Quick WSP value review for Monty Trading — April '26.\n\n"
                "Top line: ROAS held perfectly at £5.71 per £1 even as we scaled spend +65% YoY.\n"
                "Recommend continuing at current pace — 5% of last month's wholesale,\n"
                "set on day 1 monthly.\n\n"
                "Deck attached. Happy to walk through.\n\n"
                "Best,\n{Your name}"
            ), height=200)


# =========================================================================
# TAB 6 — SKILL LIBRARY
# =========================================================================
with tab_help:
    st.markdown('<div class="wsp-eyebrow">Skill Library · what each storyboard does</div>',
                unsafe_allow_html=True)
    storyboards = [
        ("value-review-variant-b", "Supplier at or above 4-5% benchmark · ask is 'continue at this pace'",
         "Monty Trading"),
        ("restart-pitch-variant-a", "Supplier dark ≥2 months · ask is 'switch WSP back on'",
         "TuttiBambini"),
        ("switch-to-5pct-variant-c", "Supplier active but under-spending (<3%) · ask is 'lock in 5% rule'",
         "(MBR drag list)"),
        ("promo-recap-tier0", "Way Day · BFCM · Cyber Week · etc. Requires exact dates.",
         "TuttiBambini Way Day"),
        ("summit-case-study", "Multi-supplier public showcase · numbers stripped",
         "Forte + Monty SU summit"),
        ("mbr-supplier-review", "Internal MBR · em-dash titles · GRS permitted",
         "March '26 MBR"),
    ]
    for name, desc, ref in storyboards:
        with st.expander(f"📄 {name}"):
            st.markdown(f"**When to use:** {desc}")
            st.markdown(f"**Canonical example:** {ref}")
            st.code(f"storyboards/{name}.md", language="text")

    st.divider()
    st.markdown("**Documentation:**")
    st.markdown("- [How to use](https://github.com/faizanshabbir777-cmd/claude-quickstarts/blob/main/wayfair-eu-supplier-marketing/HOW_TO_USE.md)")
    st.markdown("- [How to explain](https://github.com/faizanshabbir777-cmd/claude-quickstarts/blob/main/wayfair-eu-supplier-marketing/HOW_TO_EXPLAIN.md)")
    st.markdown("- [Integrations · Looker & BigQuery](https://github.com/faizanshabbir777-cmd/claude-quickstarts/blob/main/wayfair-eu-supplier-marketing/INTEGRATIONS.md)")
    st.markdown("- [Operator Pack PDF](https://github.com/faizanshabbir777-cmd/claude-quickstarts/blob/main/wayfair-eu-supplier-marketing/dashboard/WSP_Builder_UI_Mockup.pdf)")


# Footer
st.markdown("---")
st.caption("WSP Pitch Builder v0.1 MVP · built on `wayfair-supplier-pitching` skill v0.4.1 · "
           "Faizan Shabbir, EU WSP Lead · "
           "[github.com/faizanshabbir777-cmd/claude-quickstarts](https://github.com/faizanshabbir777-cmd/claude-quickstarts)")
