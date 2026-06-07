"""Real data prep — parses the team's standard CSV/xlsx exports
and produces the structured dict that deck_builder.py needs.

Production v1.0 — no Claude API call, deterministic, runs in the cloud.
"""
import pandas as pd
import io
from datetime import datetime
from collections import defaultdict


# Standard column names the parser recognises across MBR / campaign exports
COLUMN_ALIASES = {
    'wsp_spend': ['Sponsored Product Total Spend', 'Total Spend', 'WSP Spend',
                  'Ad Spends Sponsored Product Total Spend', 'Total Spend (USD)'],
    'attr_wsc': ['Sponsored Product Attributed Revenue', 'Performance Attributed Revenue',
                 'WSP Attributed Revenue', 'Ad Spends Sponsored Product Attributed Revenue',
                 'Total Revenue (USD)'],
    'wsc': ['Wholesale Cost', 'WSC', 'Finance Wholesale Cost', 'Gross WSC'],
    'date': ['Date Month', 'Date Week', 'Reporting Month', 'Date & Time Date Month',
             'Reporting Date'],
    'supplier': ['Parent Supplier', 'Supplier Name', 'Original Partner Name',
                 '[Global] Supplier Parent Supplier'],
    'suid': ['Parent SuID', 'Supplier ID', '[Global] Supplier Parent SuID',
             '[Global] Supplier Original SuID'],
    'visits': ['SKU Visit Count', 'Traffic SKU Visit Count', 'Mkc Visit Count'],
    'orders': ['Order Quantity', 'Finance Total Order Count'],
}


def find_col(df, key):
    """Find a column by alias key, return None if no match."""
    for alias in COLUMN_ALIASES.get(key, []):
        if alias in df.columns:
            return alias
    return None


def clean_money(s):
    """Strip $, £, ,, % from numeric strings; cast to float."""
    if pd.isna(s):
        return 0.0
    if isinstance(s, (int, float)):
        return float(s)
    return float(str(s).replace('$', '').replace('£', '')
                       .replace(',', '').replace('%', '').strip() or 0)


def parse_uploaded_file(file_obj, supplier_name: str, supplier_id: str,
                       period_label: str) -> dict:
    """Parse a CSV or xlsx upload into the structured dict deck_builder needs.

    Args:
        file_obj: Streamlit UploadedFile
        supplier_name: from the dashboard's Supplier Name field
        supplier_id: from the dashboard's Supplier ID field
        period_label: e.g. "April 2026"

    Returns:
        dict matching deck_builder.build_deck_value_review_b's schema

    Raises:
        ValueError: if the file is unparseable or required columns are missing
    """
    # Read the file
    name = getattr(file_obj, 'name', 'upload')
    if name.lower().endswith('.xlsx') or name.lower().endswith('.xls'):
        df = pd.read_excel(file_obj)
    else:
        df = pd.read_csv(file_obj)

    if df.empty:
        raise ValueError("File is empty.")

    # Find the columns we need
    col_spend = find_col(df, 'wsp_spend')
    col_attr  = find_col(df, 'attr_wsc')
    col_wsc   = find_col(df, 'wsc')
    col_date  = find_col(df, 'date')

    missing = []
    if not col_spend: missing.append("WSP spend column")
    if not col_attr:  missing.append("Attributed revenue column")
    if not col_wsc:   missing.append("Wholesale Cost column")
    if not col_date:  missing.append("Date column")
    if missing:
        raise ValueError(
            "Couldn't find required columns: " + ", ".join(missing) +
            ". Expected the standard campaign_reporting_extended or MBR SET format. "
            "Columns found: " + ", ".join(df.columns[:8]) + "..."
        )

    # Clean numerics
    df[col_spend] = df[col_spend].apply(clean_money)
    df[col_attr]  = df[col_attr].apply(clean_money)
    df[col_wsc]   = df[col_wsc].apply(clean_money)

    # Convert dates
    df[col_date] = pd.to_datetime(df[col_date], errors='coerce')
    df = df[df[col_date].notna()]

    # Aggregate by month
    df['_ym'] = df[col_date].dt.to_period('M').astype(str)
    monthly = df.groupby('_ym').agg({
        col_spend: 'sum',
        col_attr:  'sum',
        col_wsc:   'sum',
    }).reset_index().sort_values('_ym')
    monthly.columns = ['ym', 'spend', 'attr', 'wsc']

    # Compute the metrics the storyboard needs
    if monthly.empty:
        raise ValueError("No valid monthly data after date parsing.")

    # Last 12 months
    last12 = monthly.tail(12)
    ytd = last12.iloc[-12:] if len(last12) >= 12 else last12

    ytd_spend = ytd['spend'].sum()
    ytd_attr  = ytd['attr'].sum()
    ytd_wsc   = ytd['wsc'].sum()
    ws_roas   = (ytd_attr / ytd_spend) if ytd_spend > 0 else 0
    wsp_pct_wsc = (ytd_spend / ytd_wsc * 100) if ytd_wsc > 0 else 0

    # Latest month + YoY comparison
    latest_row = monthly.iloc[-1]
    latest_month_str = latest_row['ym']
    latest_spend = latest_row['spend']
    latest_attr  = latest_row['attr']
    latest_wsc   = latest_row['wsc']
    latest_pct_wsc = (latest_spend / latest_wsc * 100) if latest_wsc > 0 else 0

    # YoY: try to find same month last year
    try:
        latest_dt = pd.Period(latest_month_str)
        prior_dt = (latest_dt - 12).strftime('%Y-%m')
        prior_row = monthly[monthly['ym'] == prior_dt]
        if not prior_row.empty:
            prior_spend = prior_row['spend'].values[0]
            prior_attr  = prior_row['attr'].values[0]
            prior_wsc   = prior_row['wsc'].values[0]
            prior_roas  = (prior_attr / prior_spend) if prior_spend > 0 else 0
        else:
            prior_spend = prior_attr = prior_wsc = prior_roas = 0
    except Exception:
        prior_spend = prior_attr = prior_wsc = prior_roas = 0

    # Format YoY columns
    def pct_change(new, old):
        if old <= 0:
            return "+∞"
        change = (new - old) / old * 100
        return f"{'+' if change >= 0 else ''}{change:.0f}%"

    def x_change(new, old):
        if old <= 0:
            return "—"
        return f"×{new/old:.2f}"

    spend_pill = x_change(latest_spend, prior_spend) if prior_spend > 0 else "new"
    wsc_pill   = f"+£{(latest_wsc - prior_wsc)/1000:.0f}k" if prior_wsc > 0 else "new"
    roas_pill  = "Held" if abs(ws_roas - prior_roas) < 0.1 else (
                  f"+£{ws_roas - prior_roas:.2f}" if ws_roas > prior_roas else
                  f"−£{prior_roas - ws_roas:.2f}")

    # 5% rule ask amount
    ask_raw = latest_wsc * 0.05
    if ask_raw >= 1000:
        ask_amount_text = f"~£{round(ask_raw/1000):.0f}k / month"
    else:
        ask_amount_text = f"~£{round(ask_raw):,.0f} / month"

    # Pick a hero title based on the data shape
    if ws_roas >= 5:
        cover_title = "Keep your WSP on at this pace."
    elif ws_roas >= 3:
        cover_title = "Your WSP is doing the work."
    else:
        cover_title = "WSP value — and how to take it further."

    # Build the structured dict
    data = {
        'supplier': supplier_name or "Supplier",
        'suid': supplier_id,
        'period': period_label,
        'year': period_label.split()[-1] if ' ' in period_label else "2026",
        'srm': "the team",  # could be auto-filled from a lookup table in v1.1
        'cover_title': cover_title,
        'cover_subtitle': (f"Top WSP spender among your peers. Here is what it returned "
                          f"in {period_label}, and the simple way to lock it in."),
        'kpis_cover': [
            {'label': 'EVERY £1 OF WSP',
             'value': f"£{ws_roas:.2f}",
             'sub':   f"in wholesale (last 12 months)"},
            {'label': 'YoY SPEND',
             'value': spend_pill,
             'sub':   f"vs same month last year"},
            {'label': 'WSP % OF WSC',
             'value': f"{wsp_pct_wsc:.1f}%",
             'sub':   "above 5%" if wsp_pct_wsc >= 5 else "below 5% — opportunity"},
            {'label': 'WHOLESALE ATTR.',
             'value': f"£{_fmt_short(latest_attr)}",
             'sub':   f"in {period_label}"},
        ],
        'ws_roas': ws_roas,
        'wsp_spend_ytd': ytd_spend,
        'attr_wsc_ytd':  ytd_attr,
        'wsc_ytd':       ytd_wsc,
        'wsp_pct_wsc_latest': wsp_pct_wsc,
        'last_month_wsc': latest_wsc,
        'monthly_attr_wsc': [
            (_format_month(row['ym']), row['attr'])
            for _, row in monthly.iterrows()
        ],
        'yoy_period': f"{_format_month(prior_dt)} '{prior_dt[2:4]}" if prior_spend > 0 else "prior year",
        'yoy_columns': [
            {'label': 'WSP SPEND',
             'value': f"£{_fmt_short(latest_spend)}",
             'sub':   f"from £{_fmt_short(prior_spend)}" if prior_spend > 0 else "first-time",
             'pill':  spend_pill},
            {'label': 'WHOLESALE',
             'value': f"£{_fmt_short(latest_wsc)}",
             'sub':   f"from £{_fmt_short(prior_wsc)}" if prior_wsc > 0 else "first-time",
             'pill':  wsc_pill},
            {'label': 'ROAS',
             'value': f"£{ws_roas:.2f}",
             'sub':   f"from £{prior_roas:.2f}" if prior_roas > 0 else "first-time",
             'pill':  roas_pill},
        ],
        'pillars': [
            {'label': 'IT WORKS',
             'hero':  f"£{ws_roas:.2f} / £1",
             'body':  f"Every £1 of WSP has returned about £{ws_roas:.2f} in wholesale revenue this year."},
            {'label': 'IT IS DURABLE',
             'hero':  "Every month",
             'body':  f"WSP has paid back consistently month-after-month for the trailing window."},
            {'label': 'A SIMPLE RULE',
             'hero':  "5%",
             'body':  "of last month's wholesale revenue, set as the budget on day 1 — so it never runs dry."},
        ],
        'ask_amount_text': ask_amount_text,
        # Diagnostic
        '_n_months_parsed': len(monthly),
        '_columns_found': {
            'spend': col_spend, 'attr': col_attr, 'wsc': col_wsc, 'date': col_date,
        },
    }
    return data


def _fmt_short(v):
    if v >= 1e6: return f"{v/1e6:.2f}M"
    if v >= 1e3: return f"{v/1e3:.0f}k"
    return f"{v:.0f}"


def _format_month(ym_str):
    """Convert 2026-04 to 'Apr'."""
    try:
        return datetime.strptime(ym_str, '%Y-%m').strftime("%b")
    except Exception:
        return ym_str


# Sample/demo data — used when no file is uploaded so the dashboard still works
def demo_data() -> dict:
    """Hardcoded Monty Trading numbers for first-load + offline demo."""
    return {
        'supplier': 'Monty Trading Ltd',
        'suid': '37802',
        'period': 'April 2026',
        'year': '2026',
        'srm': 'the team',
        'cover_title': 'Keep your WSP on at this pace.',
        'cover_subtitle': ('Top WSP spender in Europe last month. Here is what it returned, '
                          'and the simple way to lock it in.'),
        'kpis_cover': [
            {'label': 'EVERY £1 OF WSP', 'value': '£5.71', 'sub': 'in wholesale (last 12 months)'},
            {'label': 'YoY SPEND',       'value': '×1.65', 'sub': 'from £20k → £33k'},
            {'label': 'WSP % OF WSC',    'value': '7.0%',  'sub': 'above the 5% benchmark'},
            {'label': 'WHOLESALE ATTR.', 'value': '£189k', 'sub': 'in April 2026'},
        ],
        'ws_roas': 5.71,
        'wsp_spend_ytd': 117_000,
        'attr_wsc_ytd':  548_000,
        'wsc_ytd': 4_400_000,
        'wsp_pct_wsc_latest': 7.0,
        'last_month_wsc': 476_000,
        'monthly_attr_wsc': [
            ('Dec', 113_000), ('Jan', 76_000), ('Feb', 66_000),
            ('Mar', 162_000), ('Apr', 189_000), ('May', 55_000),
        ],
        'yoy_period': 'April 2025',
        'yoy_columns': [
            {'label': 'WSP SPEND', 'value': '£33.2k', 'sub': 'from £20.1k', 'pill': '×1.65'},
            {'label': 'WHOLESALE', 'value': '£476k',  'sub': 'from £364k',  'pill': '+£112k'},
            {'label': 'ROAS',      'value': '£5.71',  'sub': 'from £5.71',  'pill': 'Held'},
        ],
        'pillars': [
            {'label': 'IT WORKS',
             'hero':  '£5.71 / £1',
             'body':  'Every £1 of WSP returned about £5.71 in wholesale revenue this year.'},
            {'label': 'IT HELD AT SCALE',
             'hero':  '0pt',
             'body':  'Spend +65% YoY, wholesale-per-£1 unchanged. The rarest signal in WSP.'},
            {'label': 'A SIMPLE RULE',
             'hero':  '5%',
             'body':  "of last month's wholesale revenue, set as the budget on day 1 — so it never runs dry."},
        ],
        'ask_amount_text': '~£23k / month',
    }
