---
name: mbr-supplier-review
description: Monthly Business Review for INTERNAL audiences (Wayfair leadership, EU SAM team). GRS-permitted because audience is internal. Formal, tabular, em-dash titles, dense KPI tiles with bps deltas.
slide_count: 4
applies_when:
  - audience is internal Wayfair leadership (not supplier-facing)
  - the brief mentions "MBR", "monthly business review", or matches the March '26 WSP MBR cadence
canonical_example: WSP_MBR_March2026 (the team's monthly MBR template)
ask:
  variant: Internal — usually next-month priorities, not a £-rule pitch
hard_rules:
  - GRS IS PERMITTED — but only because the audience is internal. Mark the deck "INTERNAL ONLY" in the cover footer.
  - bps deltas ARE PERMITTED (internal audiences parse them). Don't translate to pt unless asked.
  - Other supplier names ARE PERMITTED (internal benchmarking is allowed).
required_data:
  - period (month '25/'26 format), prior_month, year_ago
  - For EU and for each segment shown:
      total_spend, GRS, WSC, ws_roas, wsp_pct_grs, wsp_pct_wsc, MoM_bps, YoY_bps
  - top_suppliers: list of 12-16 with spend, MoM, YoY, %GRS, %WSC
  - category_breakdown: list with the same metrics
  - drag_categories (optional): categories below internal benchmark with gap-£
  - priorities for next month: 3-4 bullet items
references_baseline_slide: WSP MBR March '26 (the team's existing template — visual register is different from TuttiBambini)
visual_register: Internal MBR — em-dash titles, dense tabular slides. NOT the TuttiBambini register. See SKILL.md §C standard layout for the internal MBR rules.
---

# Slide 1 — COVER

**LAYOUT:** `mbr_cover_minimal`  (not the TuttiBambini KPI ribbon)
**TITLE:** Serif Bold ~80pt — `"Monthly Business Review"`
**SUBTITLE:** Serif ~30pt — `"EU Supplier Advertising"`
**FOOTER:** small slate Calibri — `"{period} · INTERNAL ONLY · prepared by EU WSP Lead"`

---

# Slide 2 — EXECUTIVE SUMMARY

**EYEBROW:** small caps purple — `"Executive Summary — EU (UK + APS)"`
**TITLE:** em-dash separator format — `"{month} '{yy} MBR  |  {one-line headline}"`
**LAYOUT:** `mbr_kpi_tiles_plus_commentary`

KPI tiles (4 in a row, top half):
- Each tile: big bold % at top (e.g. `"2.03%"`) → grey label below (e.g. `"EU % GRS — ATH"`) → bps deltas (`"+2 bps MoM | +113 bps YoY"`)

Commentary box (bottom half):
- Dense factual readout with bold inline call-outs (e.g. `"Top SU: UKMHStar £63.7K @ 2.17% GRS (Jo Zhang)"`)
- Apr MTD pacing
- Non-spending pipeline %
- April priorities (3-4 bullets)

---

# Slide 3 — CATEGORY DEEP DIVE

**EYEBROW:** `"Category Deep-Dive — Full EU View"`
**TITLE:** em-dash — `"{month} '{yy} vs {prior} '{yy}  |  % GRS primary  |  {key callout}"`
**LAYOUT:** `mbr_dense_table`

Full data table with columns: # · Category · Spend · MoM · YoY · % WSC · % GRS · MoM bps · YoY bps
Row count: 12-15

---

# Slide 4 — TOP SUPPLIERS

**EYEBROW:** `"Top EU WSP Suppliers — KPIs ({month} '{yy})"`
**TITLE:** em-dash — `"Ranked by Ad Spend  |  % GRS"`
**LAYOUT:** `mbr_dense_table_2col`

Two-column table (split for readability) with: Supplier · Spend · MoM · YoY · % GRS · % WSC
12-16 suppliers per side

Bottom footnote: aggregate stats — `"Top 50 avg: {X}% GRS  |  EU overall: {Y}% GRS  |  Top 50 = {Z}% of {month} spend"`

---

# Variants on the standard MBR

For lighter MBRs (or quarterly cuts), drop slide 3 → 3-slide deck.

For a deep-dive supplier MBR (single supplier, internal review), use a 5-slide variant: cover · supplier exec summary · 12-month trajectory · CG concentration + engine SKUs · priorities. The visual register stays internal-MBR (em-dash titles, dense tiles) — NOT TuttiBambini.

---

# Important distinction

The supplier-facing decks (value-review, restart, switch-to-5pct, promo recap, summit) all use the **TuttiBambini visual register** — serif italic, conversational sentences, lots of whitespace.

The MBR deck uses the **internal MBR register** — em-dash titles, dense KPI tiles, full data tables, bps deltas. Different audience, different register.

The skill picks the right register based on the storyboard selected.
