"""WSP Pitch Builder — production v1.0.

Real backend wired in. Build button produces personalised .pptx from
uploaded data. No Claude API call — the storyboard scaffold + python-pptx
do the work locally.

Run locally:
    pip install -r requirements.txt
    streamlit run app.py

Run on Streamlit Cloud:
    See DEPLOY.md.
"""
import streamlit as st
import pandas as pd
import os
import time
import hmac
import json
import traceback
from pathlib import Path
from datetime import datetime

import data_prep
import deck_builder


HERE = Path(__file__).parent
ASSETS = HERE / "assets"
DEMO = HERE / "demo"
LOG_FILE = HERE / "audit_log.jsonl"  # production audit


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
# Password gate
# -------------------------------------------------------------------------
def check_password():
    def password_entered():
        configured = st.secrets.get("auth", {}).get("password", "wsp-pilot-2026")
        if hmac.compare_digest(st.session_state["password_input"], configured):
            st.session_state["password_correct"] = True
            del st.session_state["password_input"]
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    st.markdown("""
    <div style='background:#7C1384;color:white;padding:18px 30px;margin:-16px -100px 24px -100px;border-bottom:4px solid #D4A017;'>
        <div style='font-size:28px;font-weight:700;'>
            <span style='opacity:0.6;font-weight:400;'>WSP Builder /</span> Pitch Deck Generation
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("### 🔒 Restricted access")
    st.text_input(
        "Password",
        type="password",
        key="password_input",
        on_change=password_entered,
        help="Contact Brian Delsignore (EU SAM cover) for the access password."
    )
    if "password_correct" in st.session_state and not st.session_state["password_correct"]:
        st.error("Password incorrect.")
    return False


if not check_password():
    st.stop()


# -------------------------------------------------------------------------
# CSS — match EURTA NART / InfoHub
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
</style>
""", unsafe_allow_html=True)


# Header
st.markdown("""
<div class="wsp-header">
    <div>
        <div class="breadcrumb">
            <span class="muted">WSP Builder /</span> Pitch Deck Generation
        </div>
    </div>
    <div class="branding">
        EU CM CHAMPIONS<br>
        <span class="sub">WAYFAIR SPONSORED PRODUCTS · v1.0</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Production-grade banner — no longer demo-only
st.success(
    "**Production v1.0** — drop your campaign reporting CSV in the Filters tab → click Build → "
    "real personalised .pptx download. Faizan is out for 7 weeks · for issues contact Brian Delsignore · "
    "data safety: [DATA_SAFETY.md](https://github.com/faizanshabbir777-cmd/claude-quickstarts/blob/main/wayfair-eu-supplier-marketing/dashboard/DATA_SAFETY.md)."
)


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
        st.markdown('<div class="wsp-eyebrow">Supplier Selection</div>', unsafe_allow_html=True)
        supplier_name = st.text_input("Supplier Name", value="Monty Trading Ltd")
        supplier_id = st.text_input("Supplier ID", value="37802")
        brand_catalog = st.selectbox("Brand Catalog",
            ["Wayfair UK", "Wayfair DE", "Wayfair IE", "AllModern UK"])
        vertical = st.text_input("Vertical", value="Dining · Outdoor")

    with col2:
        st.markdown('<div class="wsp-eyebrow">Brief & Storyboard</div>', unsafe_allow_html=True)
        storyboard = st.selectbox("Storyboard",
            ["value-review-variant-b  · Continue at pace",
             "restart-pitch-variant-a  · Switch back on (coming v1.1)",
             "switch-to-5pct-variant-c  · Fix lumpy spend (coming v1.1)",
             "promo-recap-tier0  · Way Day / BFCM (coming v1.1)",
             "summit-case-study  · Multi-supplier showcase (coming v1.1)"])
        audience = st.radio("Audience",
            ["Supplier-facing (WSC only, no GRS)",
             "Internal (Wayfair leadership, GRS allowed) — coming v1.1"],
            index=0)
        currency = st.selectbox("Currency", ["GBP at 1:1 from USD (default)"])

    with col3:
        st.markdown('<div class="wsp-eyebrow">Period</div>', unsafe_allow_html=True)
        reporting_month = st.selectbox("Reporting Month",
            ["April 2026", "March 2026", "February 2026", "January 2026",
             "May 2026", "June 2026", "July 2026", "August 2026"])
        trailing = st.selectbox("Trailing Window", ["L12M (default)", "L6M", "L3M", "YTD"])

    with col4:
        st.markdown('<div class="wsp-eyebrow">Account Team</div>', unsafe_allow_html=True)
        cm_champion = st.text_input("CM Champion", value="(your name)")
        srm = st.text_input("SRM (for footer)", value="the team")
        wpp = st.selectbox("WPP Supplier?", ["Yes", "No"])

    st.divider()

    # Data uploader — REAL ingestion now
    st.markdown('<div class="wsp-eyebrow">Data Upload · CSV or XLSX</div>', unsafe_allow_html=True)
    st.caption("Drop your campaign reporting CSV (the `media_tbl_advertising_campaign_reporting_extended_*.csv` "
               "export, or the MBR SET 1/2/3 format, or a `retail_sku_store_date` xlsx). The parser handles all three.")
    uploaded = st.file_uploader(
        "Drop your file here",
        type=["csv", "xlsx"], accept_multiple_files=False,
        key="data_upload")

    if uploaded:
        st.session_state["uploaded_file"] = uploaded
        st.success(f"✓ File received: `{uploaded.name}` · {uploaded.size / 1024:.0f} KB")

    # Stash all the filters for the build tab
    st.session_state["filters"] = {
        "supplier_name": supplier_name,
        "supplier_id": supplier_id,
        "brand_catalog": brand_catalog,
        "vertical": vertical,
        "storyboard": storyboard,
        "audience": audience,
        "reporting_month": reporting_month,
        "trailing": trailing,
        "cm_champion": cm_champion,
        "srm": srm,
    }


# =========================================================================
# TAB 2 — DATA PREVIEW
# =========================================================================
with tab_data:
    st.markdown('<div class="wsp-eyebrow">Data Preview · sanity check before build</div>',
                unsafe_allow_html=True)

    if st.button("Run sanity check on uploaded data"):
        if "uploaded_file" not in st.session_state:
            st.warning("Upload a file in the Filters tab first.")
        else:
            try:
                with st.spinner("Reading data · computing metrics..."):
                    f = st.session_state["filters"]
                    parsed = data_prep.parse_uploaded_file(
                        st.session_state["uploaded_file"],
                        f["supplier_name"],
                        f["supplier_id"],
                        f["reporting_month"],
                    )
                    st.session_state["parsed_data"] = parsed
                st.success(f"✓ Parsed cleanly — {parsed['_n_months_parsed']} months of data")
                st.markdown("**Data summary**:")
                st.markdown(f"""
                - **wholesale-per-£1 of WSP (last 12 months):** £{parsed['ws_roas']:.2f}
                - **WSP % of WSC (12-month):** {parsed['wsp_pct_wsc_latest']:.1f}%
                - **Latest month wholesale:** £{parsed['last_month_wsc']/1000:.0f}k
                - **12-month attributed wholesale:** £{parsed['attr_wsc_ytd']/1000:.0f}k
                - **5% rule ask:** {parsed['ask_amount_text']}
                """)
                with st.expander("Columns matched in your file"):
                    st.json(parsed['_columns_found'])
            except ValueError as e:
                st.error(f"**Data prep failed:** {e}")
                st.caption("If your file format is non-standard, share with Brian Delsignore "
                           "(Faizan's cover) — he'll forward and we'll add the alias.")
            except Exception as e:
                st.error(f"Unexpected error: {e}")
                with st.expander("Traceback (for the diagnostics team)"):
                    st.code(traceback.format_exc())


# =========================================================================
# TAB 3 — BUILD
# =========================================================================
with tab_build:
    st.markdown('<div class="wsp-eyebrow">Build the Deck</div>', unsafe_allow_html=True)

    st.subheader("Storyboard scaffold — what the agent will fill")
    st.caption("Variant B Value Review. v1.1 will add the other variants.")

    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown("**Slide 1 · COVER**")
        st.caption("Deep purple bg · gold eyebrow · serif italic title · 4 KPI cards filled from your data")
    with s2:
        st.markdown("**Slide 2 · 01 · WHAT WSP IS DOING**")
        st.caption("Lavender hero card with computed £X.XX wholesale-per-£1 · monthly bar chart from your file")
    with s3:
        st.markdown("**Slide 3 · 02 · {LATEST} vs {YoY}**")
        st.caption("Deep purple KPI band with green delta pills computed from your YoY comparison")
    with s4:
        st.markdown("**Slide 4 · 03 · WHERE WE GO FROM HERE**")
        st.caption("Three pillar cards · DEEP PURPLE 'THE ASK' card · gold-highlighted £-amount from 5% rule")

    st.divider()

    bcol1, bcol2 = st.columns([1, 2])
    with bcol1:
        if st.button("▶ Build Pitch Deck", type="primary", use_container_width=True):
            f = st.session_state.get("filters", {})

            # Step 1: get data — either parsed upload or demo fallback
            if "parsed_data" in st.session_state:
                data = st.session_state["parsed_data"]
                source_note = "from your uploaded file"
            elif "uploaded_file" in st.session_state:
                try:
                    data = data_prep.parse_uploaded_file(
                        st.session_state["uploaded_file"],
                        f.get("supplier_name", "Supplier"),
                        f.get("supplier_id", ""),
                        f.get("reporting_month", "this period"),
                    )
                    st.session_state["parsed_data"] = data
                    source_note = "from your uploaded file"
                except Exception as e:
                    st.error(f"Data prep failed: {e}")
                    st.stop()
            else:
                data = data_prep.demo_data()
                source_note = "from demo data (no file uploaded)"

            # Override supplier metadata from the form
            data['supplier'] = f.get("supplier_name") or data['supplier']
            data['period']   = f.get("reporting_month") or data['period']
            data['srm']      = f.get("srm") or data.get('srm', 'the team')

            # Build the deck
            try:
                with st.spinner(f"Building deck {source_note}..."):
                    pptx_bytes = deck_builder.build_deck_value_review_b(data)
                st.session_state["pptx_bytes"] = pptx_bytes
                st.session_state["build_data"] = data
                st.session_state["build_done"] = True

                # Audit log
                _audit({
                    "ts": datetime.utcnow().isoformat() + "Z",
                    "supplier": data['supplier'],
                    "suid": data.get('suid'),
                    "period": data['period'],
                    "storyboard": f.get("storyboard", "value-review-variant-b"),
                    "cm_champion": f.get("cm_champion"),
                    "source": source_note,
                    "deck_bytes": len(pptx_bytes),
                })
                st.success(f"✓ Deck ready — head to **Preview & QA** tab to inspect, or **Send** tab to download.")
            except Exception as e:
                st.error(f"Build failed: {e}")
                with st.expander("Traceback"):
                    st.code(traceback.format_exc())
                st.caption("If this keeps happening, contact Brian Delsignore. "
                           "While Faizan's out, persistent issues will be queued for his return.")
        st.caption("~30 seconds · personalised from your data")
    with bcol2:
        st.markdown("**Pipeline status**")
        if st.session_state.get("build_done"):
            data = st.session_state.get("build_data", {})
            st.success(f"✓ Last build: **{data.get('supplier','?')}** · {data.get('period','?')} "
                       f"· wholesale-per-£1: £{data.get('ws_roas', 0):.2f}")
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
        data = st.session_state.get("build_data", {})
        st.markdown(f"### Preview · {data.get('supplier', 'Supplier')} · {data.get('period', '')}")

        # Render the 4 slide PNGs from the build_data and show in-app
        for renderer, label in [
            (deck_builder.render_cover,       "Slide 1 · Cover"),
            (deck_builder.render_value_story, "Slide 2 · 01 · WHAT WSP IS DOING"),
            (deck_builder.render_yoy_proof,   "Slide 3 · 02 · YoY proof"),
            (deck_builder.render_ask,         "Slide 4 · 03 · WHERE WE GO FROM HERE"),
        ]:
            st.markdown(f"**{label}**")
            try:
                slide_img = renderer(data)
                import io
                buf = io.BytesIO()
                slide_img.save(buf, "PNG")
                buf.seek(0)
                st.image(buf, use_container_width=True)
            except Exception as e:
                st.error(f"Render failed for this slide: {e}")
            st.divider()


# =========================================================================
# TAB 5 — SEND
# =========================================================================
with tab_send:
    st.markdown('<div class="wsp-eyebrow">Send to SRM</div>', unsafe_allow_html=True)
    if not st.session_state.get("build_done"):
        st.info("Build the deck first, then come here to send.")
    else:
        data = st.session_state.get("build_data", {})
        pptx_bytes = st.session_state.get("pptx_bytes")

        st.success(f"✓ Deck ready — {data.get('supplier', 'Supplier')} · {data.get('period', '')}")
        col1, col2 = st.columns(2)
        with col1:
            if pptx_bytes:
                fn = f"{data.get('supplier','Supplier').replace(' ','_')}_{data.get('period','').replace(' ','_')}_WSP_Deck.pptx"
                st.download_button(
                    "📥 Download .pptx",
                    data=pptx_bytes,
                    file_name=fn,
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    type="primary",
                )
            st.markdown("**Coming v1.1:**")
            st.button("📨 Send to SRM via Slack", disabled=True)
            st.button("✉️ Email SRM with deck attached", disabled=True)
        with col2:
            st.markdown("**Send-to-SRM template**")
            srm_name = st.text_input("SRM name", value=data.get('srm', 'the team'))
            template = (
                f"Hi {srm_name},\n\n"
                f"Quick WSP value review for {data.get('supplier','the supplier')} — {data.get('period','this period')}.\n\n"
                f"Top line: wholesale-per-£1 sits at £{data.get('ws_roas', 0):.2f}.\n"
                f"Recommend continuing at current pace — 5% of last month's wholesale,\n"
                f"set on day 1 monthly. Resulting budget for next month: {data.get('ask_amount_text','—')}.\n\n"
                f"Deck attached. Happy to walk through.\n\n"
                f"Best,\n{st.session_state.get('filters',{}).get('cm_champion','')}"
            )
            st.text_area("Edit before send", value=template, height=240, key="srm_template")


# =========================================================================
# TAB 6 — SKILL LIBRARY
# =========================================================================
with tab_help:
    st.markdown('<div class="wsp-eyebrow">Skill Library</div>', unsafe_allow_html=True)
    storyboards = [
        ("value-review-variant-b", "Supplier at or above 4-5% benchmark · ask is 'continue at this pace'",
         "Monty Trading", "✅ Live in v1.0"),
        ("restart-pitch-variant-a", "Supplier dark ≥2 months · ask is 'switch WSP back on'",
         "TuttiBambini", "⏳ v1.1"),
        ("switch-to-5pct-variant-c", "Supplier active but under-spending (<3%) · ask is 'lock in 5% rule'",
         "(MBR drag list)", "⏳ v1.1"),
        ("promo-recap-tier0", "Way Day · BFCM · Cyber Week. Requires exact dates.",
         "TuttiBambini Way Day", "⏳ v1.1"),
        ("summit-case-study", "Multi-supplier public showcase · numbers stripped",
         "Forte + Monty SU summit", "⏳ v1.1"),
        ("mbr-supplier-review", "Internal MBR · em-dash titles · GRS permitted",
         "March '26 MBR", "⏳ v1.1"),
    ]
    for name, desc, ref, status in storyboards:
        with st.expander(f"📄 {name}  ·  {status}"):
            st.markdown(f"**When to use:** {desc}")
            st.markdown(f"**Canonical example:** {ref}")
            st.code(f"storyboards/{name}.md", language="text")

    st.divider()
    st.markdown("### Troubleshooting (while Faizan is out)")
    st.markdown("""
    - **Build fails on your file** — check the "Columns found" panel in Data Preview. If the columns
      don't match expected aliases (e.g. you have "Wholesale Cost (GBP)" instead of "Wholesale Cost"),
      either rename the column in Excel before uploading OR contact Brian to add the alias to `data_prep.py`.
    - **Output looks wrong** — open the .pptx in PowerPoint, override what's off, share with Brian so
      Faizan can update the storyboard on return.
    - **App is down** — Streamlit Cloud puts free apps to sleep after 7 days of no traffic. First load
      takes ~30 sec. If it's actually down (not sleeping), restart from the Streamlit Cloud dashboard
      (Brian has access).
    - **Need a storyboard that doesn't exist yet** — queue the supplier name + period in `#wsp-pilot` Slack;
      Faizan batch-processes on return.

    **Docs:**
    - [How to use](https://github.com/faizanshabbir777-cmd/claude-quickstarts/blob/main/wayfair-eu-supplier-marketing/HOW_TO_USE.md)
    - [Data safety](https://github.com/faizanshabbir777-cmd/claude-quickstarts/blob/main/wayfair-eu-supplier-marketing/dashboard/DATA_SAFETY.md)
    - [Deploy](https://github.com/faizanshabbir777-cmd/claude-quickstarts/blob/main/wayfair-eu-supplier-marketing/dashboard/DEPLOY.md)
    """)


# Footer
st.markdown("---")
st.caption("WSP Pitch Builder v1.0 · "
           "Faizan Shabbir, EU WSP Lead · while Faizan is out: Brian Delsignore · "
           "[github.com/faizanshabbir777-cmd/claude-quickstarts](https://github.com/faizanshabbir777-cmd/claude-quickstarts)")


# -------------------------------------------------------------------------
# Audit log helper
# -------------------------------------------------------------------------
def _audit(entry: dict):
    """Append a single JSONL line to the audit log. Best-effort; never fails the build."""
    try:
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass  # don't crash the build because we couldn't log
