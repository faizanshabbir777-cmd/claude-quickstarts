---
name: value-review-variant-b
description: Variant B Continue — supplier is at or above the 4-5% WSC benchmark, the ask is "continue at this pace."
slide_count: 4
applies_when:
  - wsp_intensity_pct >= 4
  - ws_roas >= 3
  - last_month_wsp > 0
  - no_paused_months_in_last_3
canonical_example: Monty Trading UK · April '26
ask:
  variant: B
  rule_pct: 5
  ask_template: "Continue WSP at ~£{amount} / month — 5% of last month's wholesale ({last_wsc}), set on day 1"
required_data:
  - supplier_name
  - supplier_id
  - period_label
  - srm_name              # optional, falls back to "the {supplier} team"
  - latest_month:
      month, wsp_spend, wsc, attr_wsc, ws_roas, wsp_pct_wsc
  - yoy_compare:
      prior_period, prior_spend, prior_wsc, prior_attr_wsc, prior_roas
  - last_12mo:
      total_spend, total_attr_wsc, total_wsc, ws_roas_avg, correlation
  - monthly_trajectory (last 5 months for the bar chart)
  - best_month: month, ratio
references_baseline_slide: TuttiBambini slide 1 (cover), slide 2 (value story), slide 5 (the ask)
---

# Slide 1 — COVER

**LAYOUT:** `deep_purple_kpi_ribbon`
**EYEBROW:** gold, letter-spaced — `"{SUPPLIER_NAME} · WAYFAIR SPONSORED PRODUCTS"`
**TITLE:** Serif Bold Italic, ~115pt, white, ends in period
**TITLE_EXAMPLES:**
- *"Keep your WSP on at this pace."*
- *"Your ads are doing the work."*
- *"The engine is running."*
- *"You're already in the right place — let's stay there."*
**SUBTITLE:** Serif Italic, ~38pt, white, 2 lines, context-setting. Should answer "what's the headline of this deck?"
**KPI_RIBBON:** 4 cards (lavender bg, GOLD top stripe)
- card 1: `EVERY £1 OF WSP` → serif italic `"£{ratio} back"` → sub `"in wholesale revenue ({period})"`
- card 2: `YoY SPEND` → serif italic `"×{ratio}"` → sub `"from £{prior} → £{latest}"`
- card 3: `WSP % OF WSC` → serif italic `"{pct}%"` → sub `"above the 5% benchmark"`
- card 4: ROAS-related — either `ROAS CHANGE YoY` (`"0pt" / "no compression at scale"`) OR `WHOLESALE ATTRIBUTED` (`"£{X}k" / "+{pct}% YoY"`)
**FOOTER:** `"{period} · prepared for {srm_name} · UK · GBP"`

---

# Slide 2 — VALUE STORY

**EYEBROW:** purple, letter-spaced — `"01 · WHAT WSP IS DOING FOR YOU"`
**TITLE:** Serif Bold Italic, ~48pt, INK
**TITLE_EXAMPLES:**
- *"When it is on, every pound comes back about {N} times over."*
- *"The engine works whenever it is running."*
- *"Strong return, every month, no exceptions."*
**LAYOUT:** `lavender_hero_left_chart_right`

**LEFT CARD** (lavender, no top stripe):
- eyebrow: `"SO FAR IN {YEAR}"`
- hero number: Serif Bold Italic ~180pt, deep purple — `"£{ratio}"`
- explanation: `"of wholesale revenue for every £1 of WSP spend"`
- three label/value rows:
  - `You spent` / `£{spend} on WSP`
  - `It drove` / `£{attr_wsc} attributed wholesale`
  - `That's` / `1 in £{ratio} — strong and steady`

**RIGHT CHART** (clean purple bars, no axis numbers):
- chart title: `"Wholesale revenue driven by WSP, each month (£)"`
- data: last 5 months from `monthly_trajectory.attr_wsc`
- value label above each bar, month name below
- partial-month footnote if applicable: `"* {latest_month} to {day}th only — partial month"`

**TAKEAWAY** (italic serif, slide bottom):
`"Take-away: your WSP has paid back about £{ratio} for every £1 — and it has every month this year."`

---

# Slide 3 — YOY PROOF

**EYEBROW:** purple — `"02 · {LATEST_MONTH} '{YY} vs {PRIOR_MONTH} '{YY}"`
**TITLE:** Serif Bold Italic, INK
**TITLE_EXAMPLES:**
- *"You doubled down on ads — and the ads doubled down on you."*
- *"Bigger spend. Same return per pound. That is rare."*
**LAYOUT:** `deep_purple_kpi_band_left_lavender_side`

**LEFT BAND** (deep purple, 3 columns, vertical gold dividers):
- col 1: gold eyebrow `WSP SPEND` → white serif italic `£{X}` → grey `from £{prior}` → green pill `×{ratio}`
- col 2: gold eyebrow `WHOLESALE` → white serif italic `£{X}` → grey `from £{prior}` → green pill `+£{delta}`
- col 3: gold eyebrow `ROAS` → white serif italic `£{X}` → grey `from £{prior}` → green pill `Held` (if flat) or `+£{delta}` (if up)

**RIGHT CARD** (lavender):
- eyebrow: `WSP % OF WSC`
- 3 small ascending green bars
- green serif italic `"Above 5% benchmark"`
- slate sub: `"Your spend share grew from {pct1}% to {pct2}% YoY"`

**BODY SENTENCE** (one line, with inline green emphasis on the key phrase):
`"You scaled WSP by {pct}% — and instead of efficiency dropping, [GREEN: it held perfectly at £{ratio} per £1]."`

**DATE FOOTNOTE:** italic slate, `"{latest_period} vs {prior_period}."`

**LAVENDER CALLOUT BOX** (full width):
- `"The unusual part: at this scale, most ROAS compresses. Yours did not."`
- OR `"The pattern is clear: spend and wholesale move together, every month."`

---

# Slide 4 — THE ASK

**EYEBROW:** purple — `"03 · WHERE WE GO FROM HERE"`
**TITLE:** Serif Bold Italic, INK
**TITLE_EXAMPLES:**
- *"Lock in the rhythm — same return, no surprises."*
- *"Keep the rule. The budget writes itself."*
- *"One rule. Live on day 1. Every month."*
**LAYOUT:** `three_pillars_plus_ask`

**THREE PILLAR CARDS** (lavender bg, GOLD top stripe each):
- card 1: `IT WORKS` → serif italic `"£{ratio} / £1"` → body: `"Every £1 of WSP has returned about £{ratio} in wholesale revenue this year."`
- card 2: select one based on which is the stronger pillar:
  - `IT HELD AT SCALE` → `"0pt"` → `"Spend +{pct}% YoY, wholesale-per-£1 unchanged at £{ratio}. The rarest signal in WSP."` (use if no ROAS compression)
  - `IT GREW WITH YOU` → `"+{pct}%"` → `"UK wholesale moved from £{prior} to £{latest} as WSP scaled."` (use if both spend and wholesale up)
  - `IT IS DURABLE` → `"{N} months"` → `"WSP has returned ≥£{ratio_floor} per £1 every month since {start}."` (use if multi-month consistency)
- card 3: `A SIMPLE RULE` → serif italic `"5%"` → body: `"of last month's wholesale revenue, set as the budget on day 1 — so it never runs dry."`

**THE ASK CARD** (full-width, DEEP purple, GOLD top stripe):
- gold eyebrow: `"THE ASK"` letter-spaced
- one sentence, Calibri ~40pt, with the £-amount HIGHLIGHTED IN GOLD BOLD:
  `"Continue WSP at  [GOLD: ~£{amount} / month]  —  5% of last month's wholesale revenue (£{last_wsc}), set on day 1 so the engine never stutters."`

**CLOSING LINE** (italic Georgia, ~28pt, INK, slide bottom):
`"Proven £{ratio} back for every £1  ·  {efficiency_pillar}  ·  one rule, live on day 1."`

Examples of `{efficiency_pillar}`:
- `"ROAS held at scale"`
- `"correlation 0.84 across 14 months"`
- `"durable across {N} consecutive months"`

---

# Computation rules

- `ratio = round(attr_wsc / wsp_spend, 2)`
- `amount = round(last_wsc * 0.05, -3)` (rounded to nearest £1k, e.g. £23k not £22.79k)
- `wsp_pct_wsc = round(wsp_spend / wsc * 100, 1)`
- All £ in GBP at 1:1 from USD per `SKILL.md §C` rule #2
- `efficiency_pillar` is picked based on the strongest signal in the data

# What this storyboard does NOT cover

- Restart pitches (use `restart-pitch-variant-a.md`)
- Under-spender pitches (use `switch-to-5pct-variant-c.md`)
- Promo recaps (use `promo-recap-tier0.md`)

If the supplier's data straddles "value review" and one of the above, the agent surfaces the ambiguity and asks the analyst to pick — never picks silently.
