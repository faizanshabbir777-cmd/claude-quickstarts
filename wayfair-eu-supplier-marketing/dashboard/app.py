"""WSP Pitch Builder — Streamlit MVP.

Non-technical UI wrapper around the wayfair-supplier-pitching skill.
Category Manager WSP Champions use this to ship pitch decks without
touching a terminal.

Run locally:
    pip install streamlit pandas openpyxl
    streamlit run app.py

Run on Wayfair internal infra:
    See dashboard/DEPLOYMENT.md for the K8s manifest + SSO wiring.
"""
import streamlit as st
import pandas as pd
import json
import subprocess
import os
import time
from pathlib import Path
from datetime import datetime

# -------------------------------------------------------------------------
# Page config & InfoHub-style theming
# -------------------------------------------------------------------------
st.set_page_config(
    page_title="WSP Pitch Builder · Wayfair",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS — match the EURTA NART / InfoHub aesthetic
st.markdown("""
<style>
    /* Hide Streamlit's default chrome */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 1rem; max-width: 100%; }

    /* Magenta header bar */
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

    /* Pink section eyebrow (matches InfoHub) */
    .wsp-eyebrow {
        color: #C5259A;
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 1.5px;
        margin-bottom: 8px;
        text-transform: uppercase;
    }

    /* Big magenta build button */
    .stButton > button[kind="primary"] {
        background-color: #7C1384;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 14px 28px;
        font-weight: 700;
        font-size: 18px;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #9C26A4;
    }

    /* Pipeline status pill */
    .status-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
        margin-right: 8px;
    }
    .status-done { background: #0E8F60; color: white; }
    .status-pending { background: #CFC7D6; color: #5B5B66; }
    .status-active { background: #D4A017; color: white; }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------------
# Header bar (magenta, matches InfoHub)
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
        <span class="sub">WAYFAIR SPONSORED PRODUCTS</span>
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------------
# Tab nav (matches the InfoHub Pricing Structure tab row)
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

    # Four filter columns matching the InfoHub layout
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
             "D · Custom (you fill in)"])
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

    # Promo strip (collapsible — only relevant for promo recaps)
    if "promo-recap" in storyboard:
        st.markdown('<div class="wsp-eyebrow">Promo Window · REQUIRED</div>',
                    unsafe_allow_html=True)
        pcol1, pcol2, pcol3, pcol4 = st.columns(4)
        event_name = pcol1.text_input("Event Name", placeholder="Way Day 2026")
        promo_start = pcol2.date_input("Promo Start")
        promo_end = pcol3.date_input("Promo End")
        pre_start = pcol4.date_input("Pre-Period Start")
        st.caption("⚠️ Rule #8 — never inferred from filenames. Exact dates required before build.")

    # Output strip
    st.markdown('<div class="wsp-eyebrow">Output</div>',
                unsafe_allow_html=True)
    o1, o2, o3, o4 = st.columns(4)
    filename_format = o1.text_input("Filename Format",
        value="{Supplier}_{Period}_WSP_Deck.pptx")
    save_to = o2.text_input("Save To", value="./outputs/")
    qa_loop = o3.selectbox("Run QA Loop",
        ["Yes (LibreOffice → JPG inspect)", "No (skip — not recommended)"])
    visual_register = o4.selectbox("Visual Register",
        ["TuttiBambini (default)", "Internal MBR (em-dash titles)"])

    # Data uploader
    st.markdown('<div class="wsp-eyebrow">Data Source</div>',
                unsafe_allow_html=True)
    use_looker = st.checkbox("Use Looker Studio dashboard (pilot scope)")
    if use_looker:
        looker_dashboard = st.text_input("Looker Dashboard ID",
            placeholder="monty-trading-wsp-monthly")
        st.caption("Pilot week 1: direct read from your existing dashboard. No CSV step.")
    else:
        uploaded = st.file_uploader(
            "Drop your campaign reporting CSV (or share-shift xlsx for promos)",
            type=["csv", "xlsx"], accept_multiple_files=True)


# =========================================================================
# TAB 2 — DATA PREVIEW
# =========================================================================
with tab_data:
    st.markdown('<div class="wsp-eyebrow">Data Preview · sanity check before build</div>',
                unsafe_allow_html=True)
    st.info("The data-prep subagent will surface 4-6 plain-English bullets here once you load a CSV or connect Looker. You confirm the picture matches reality before any deck-building.")

    # Mock preview for the mockup
    if st.button("Run sanity check"):
        with st.spinner("Reading data · computing metrics · checking against Account Overview..."):
            time.sleep(1)
        st.success("✓ Sanity check: PASS  ·  Data matches Account Overview within 0.3%")

        st.markdown("**Data summary** (auto-generated from `wsp-data-prep`):")
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
    st.markdown('<div class="wsp-eyebrow">Build the Deck</div>',
                unsafe_allow_html=True)

    # Storyboard scaffold preview
    st.subheader("Storyboard scaffold — what the agent will fill")
    st.caption("You can override any title or pillar choice before render.")

    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown("**Slide 1 · COVER**")
        st.caption("Deep purple bg · gold eyebrow · serif italic title "
                   "'Keep your WSP on at this pace.' · 4 KPI cards")
        st.button("View scaffold ▸", key="v1")
    with s2:
        st.markdown("**Slide 2 · 01 · WHAT WSP IS DOING**")
        st.caption("Lavender £5.71 hero card · monthly bar chart · italic takeaway")
        st.button("View scaffold ▸", key="v2")
    with s3:
        st.markdown("**Slide 3 · 02 · APRIL '26 vs APRIL '25**")
        st.caption("Deep purple KPI band with green delta pills · 'Above benchmark' callout")
        st.button("View scaffold ▸", key="v3")
    with s4:
        st.markdown("**Slide 4 · 03 · WHERE WE GO FROM HERE**")
        st.caption("Three pillar cards · DEEP PURPLE 'THE ASK' card · gold £-amount")
        st.button("View scaffold ▸", key="v4")

    st.divider()

    # Build action
    bcol1, bcol2 = st.columns([1, 2])
    with bcol1:
        build_clicked = st.button("▶ Build Pitch Deck", type="primary",
                                   use_container_width=True)
        st.caption("≈ 90 seconds · QA loop included")
    with bcol2:
        st.markdown("**Pipeline status**")
        if build_clicked:
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
            progress_text.markdown("**✓ Deck ready**")
            st.success("`outputs/Monty_Trading_April2026_WSP_Deck.pptx`")
            st.session_state["build_done"] = True
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
        for path, label in [
            ("/tmp/forte_deck/monty_tutti_s1.png", "Slide 1 · Cover"),
            ("/tmp/forte_deck/monty_tutti_s2.png", "Slide 2 · 01 · WHAT WSP IS DOING"),
            ("/tmp/forte_deck/monty_tutti_s3.png", "Slide 3 · 02 · APRIL '26 vs APRIL '25"),
            ("/tmp/forte_deck/monty_tutti_s4.png", "Slide 4 · 03 · WHERE WE GO FROM HERE"),
        ]:
            st.markdown(f"**{label}**")
            if os.path.exists(path):
                st.image(path)
            else:
                st.warning(f"Preview not available — generate via build first.")
            st.divider()

# =========================================================================
# TAB 5 — SEND
# =========================================================================
with tab_send:
    st.markdown('<div class="wsp-eyebrow">Send to SRM</div>',
                unsafe_allow_html=True)
    if not st.session_state.get("build_done"):
        st.info("Build the deck first, then come here to send.")
    else:
        st.success("✓ Deck ready to send")
        col1, col2 = st.columns(2)
        with col1:
            st.download_button("📥 Download .pptx",
                data=b"placeholder",
                file_name="Monty_Trading_April2026_WSP_Deck.pptx")
            st.markdown("Or:")
            st.button("📨 Send to SRM via Slack")
            st.button("✉️ Email SRM with deck attached")
        with col2:
            st.markdown("**Send-to-SRM template**")
            st.text_area("Edit before send", value=(
                f"Hi {{SRM name}},\n\n"
                f"Quick WSP value review for Monty Trading — April '26.\n\n"
                f"Top line: ROAS held perfectly at £5.71 per £1 even as we scaled spend +65% YoY.\n"
                f"Recommend continuing at current pace — 5% of last month's wholesale,\n"
                f"set on day 1 monthly.\n\n"
                f"Deck attached. Happy to walk through.\n\n"
                f"Best,\n{{Your name}}"
            ), height=200)

# =========================================================================
# TAB 6 — SKILL LIBRARY
# =========================================================================
with tab_help:
    st.markdown('<div class="wsp-eyebrow">Skill Library · what each storyboard does</div>',
                unsafe_allow_html=True)
    storyboards = [
        ("value-review-variant-b", "Supplier at or above 4-5% benchmark · ask is 'continue at this pace'", "Monty Trading"),
        ("restart-pitch-variant-a", "Supplier dark ≥2 months · ask is 'switch WSP back on'", "TuttiBambini"),
        ("switch-to-5pct-variant-c", "Supplier active but under-spending (<3%) · ask is 'lock in 5% rule'", "(MBR drag list)"),
        ("promo-recap-tier0", "Way Day · BFCM · Cyber Week · etc. Requires exact dates.", "TuttiBambini Way Day"),
        ("summit-case-study", "Multi-supplier public showcase · numbers stripped", "Forte + Monty SU summit"),
        ("mbr-supplier-review", "Internal MBR · em-dash titles · GRS permitted", "March '26 MBR"),
    ]
    for name, desc, ref in storyboards:
        with st.expander(f"📄 {name}"):
            st.markdown(f"**When to use:** {desc}")
            st.markdown(f"**Canonical example:** {ref}")
            st.code(f"storyboards/{name}.md", language="text")

# Footer
st.markdown("---")
st.caption("WSP Pitch Builder v0.1 MVP · built on `wayfair-supplier-pitching` skill v0.4.0 · "
           "Faizan Shabbir, EU WSP Lead · github.com/faizanshabbir777-cmd/claude-quickstarts")
