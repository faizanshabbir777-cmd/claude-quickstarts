---
name: switch-to-5pct-variant-c
description: Variant C — supplier is active but under-spending (<3% of WSC) or erratic; the ask is "lock in the 5% rule on day 1 monthly."
slide_count: 5
applies_when:
  - last_month_wsp > 0           # actively spending
  - wsp_intensity_pct < 3        # but below benchmark
  - OR: MoM_spend_swing > 50% with stable WSC  (erratic)
canonical_example: an under-spender from the MBR slide 8 drag list
ask:
  variant: C
  rule_pct: 5
  ask_template: "{rule_pct}% × last-30-days wholesale = next month's WSP budget, set on day 1. That works out to ~£{amount} for next month."
required_data:
  - supplier_name, supplier_id, period_label, srm_name
  - last_12mo_monthly: [{month, spend, wsc}]
  - current_wsp_intensity_pct
  - last_30_days_wsc
  - recommended_monthly_budget (= last_30_days_wsc × 0.05)
  - gap_to_benchmark (= recommended_monthly_budget - current_monthly_spend)
  - cap_hit_days (optional but powerful — see SKILL.md §A.2.3)
  - erratic_evidence (optional — months where spend swung >50% with stable WSC)
---

# Slide 1 — COVER

**LAYOUT:** `deep_purple_kpi_ribbon`
**EYEBROW:** gold — `"{SUPPLIER_NAME} · WAYFAIR SPONSORED PRODUCTS"`
**TITLE:**
- *"One rule to fix lumpy spend."*
- *"You're already spending — let's make it work harder."*
**SUBTITLE:** `"Your WSP is on. The maths is good. The cadence is missing — and here is the simple fix."`
**KPI_RIBBON:** 4 cards
- card 1: `EVERY £1 OF WSP` → `"£{ratio} back"` → sub `"in wholesale (last 12 months)"`
- card 2: `CURRENT WSP % WSC` → `"{pct}%"` → sub `"vs the 5% benchmark"`
- card 3: `OPEN BUDGET PER MONTH` → `"+£{gap}k"` → sub `"the gap to 5%"`
- card 4: **CORAL stripe** if erratic — `MONTHS WSP PAUSED MID-WAY` → CORAL `"{N}"` → sub `"in the last 12"`. OR `CAP HIT DAYS` → CORAL `"{N}"` if cap-hit story.
**FOOTER:** `"{period} · prepared for {srm_name} · UK · GBP"`

---

# Slide 2 — VALUE STORY

Same as `value-review-variant-b.md` slide 2.

**EYEBROW:** `"01 · WHAT WSP IS DOING FOR YOU"`
**TITLE:** *"The £{ratio} per £1 is real — it just isn't running often enough."*

---

# Slide 3 — WHAT ERRATIC SPEND COST

**EYEBROW:** **CORAL** — `"02 · WHAT IS HOLDING IT BACK"`
**TITLE:** *"Spend drops off mid-month — and the wholesale drops with it."*
**LAYOUT:** `monthly_intensity_chart_left_dark_days_right`

LEFT: 12-month chart, two series:
- Purple bars: monthly WSP spend
- Gold line: monthly WSP % of WSC, with a horizontal dashed line at 5% as the benchmark
- Visually shows the supplier dipping below benchmark

RIGHT (CORAL bg if erratic, LAVENDER if cap-hit story):
- eyebrow CORAL: `"WHEN THE BUDGET RAN DRY"` (or `"WHEN THE CAP WAS HIT"`)
- hero serif italic CORAL: `"{N} months"` (or `"{N}% of days"`)
- sub: short explanation

**TAKEAWAY:** `"Every month the budget runs out by week three, you stop showing up for the last ten days — and the wholesale dips."`

---

# Slide 4 — THE PORTFOLIO RULE

**EYEBROW:** purple — `"03 · WHAT THE RULE UNLOCKS"`
**TITLE:** *"A simple rule fixes lumpy spend — for every supplier on it."*
**LAYOUT:** `three_pillars_plus_ask` (preview)

THREE LAVENDER CARDS with GOLD top stripes:
- card 1: `WHAT ERRATIC SPEND COST` → CORAL `"~£{missed}"` → `"likely lost over the months WSP went dark mid-cycle."`
- card 2: `THE PORTFOLIO RULE` → `"5%"` → `"of last month's wholesale, set as the WSP budget on day 1. Every month. No drama."`
- card 3: `WHAT THE RULE UNLOCKS` → `"£{recommended}/mo"` → `"set automatically from last month's landed wholesale — no negotiation needed."`

---

# Slide 5 — THE ASK

**EYEBROW:** purple — `"04 · WHERE WE GO FROM HERE"`
**TITLE:** *"One rule. Live on day 1. Every month."*
**LAYOUT:** `ask_card_full_width`

**THE ASK CARD** (full-width, DEEP purple, GOLD top stripe):
- gold eyebrow: `"THE ASK"`
- one sentence:
  `"Set {rule_pct}% × last-30-days wholesale as next month's WSP budget, live on day 1. For next month that is  [GOLD: ~£{amount}]  — based on £{last_30d_wsc} of wholesale in the last 30 days."`

**CLOSING LINE:** `"Proven £{ratio} back for every £1  ·  the gap to benchmark is +£{gap}  ·  one rule, live on day 1."`

---

# Computation rules

- `recommended_monthly_budget = last_30_days_wsc × 0.05`
- `gap_to_benchmark = recommended_monthly_budget - current_monthly_spend`
- `amount` displayed rounded to nearest £500 (e.g. £4,500, £11,000, £23,500)
- Cap-hit evidence is OPTIONAL but turns the deck into a much stronger argument — include if available
