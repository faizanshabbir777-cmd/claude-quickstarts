---
name: portfolio-outreach
description: Cross-supplier prioritisation — "who do I pitch first this month?" Outputs a ranked LIST, not a deck.
slide_count: 0   # this is a markdown/CSV output, not a slide deck
applies_when:
  - brief is "who should I pitch first"
  - brief asks for a ranked list of suppliers by opportunity size
  - brief mentions "portfolio", "outreach plan", "weekly pitch list"
canonical_example: Mar '26 MBR slide 8 (UK supplier targeting within drag categories)
required_data:
  - campaign_reporting_csv (full portfolio for the period)
  - period_label
  - benchmark_pct (default 5%)
  - latest_landed_month_wsc per supplier
  - last_3mo_wsp_pattern per supplier (active / dark / erratic)
---

# Output format

Not a slide deck. The output is a **ranked markdown table + a 4-line outreach script per supplier**.

## Step 1 — Compute per supplier

For every supplier in the portfolio reporting CSV:
- `wsp_intensity = wsp_spend / wsc`
- `gap_to_benchmark = (wsc × benchmark_pct) − wsp_spend`
- `category`: one of `no_spend` | `under_spending` | `at_benchmark` | `at_risk` | `over_benchmark`

Filter out suppliers with WSC < £1,000 (too small).

## Step 2 — Categorise

- **No spend** (last_month_wsp == 0)         → Variant A pitch (`restart-pitch-variant-a.md`)
- **Under-spending** (wsp_intensity < 3%)    → Variant C pitch (`switch-to-5pct-variant-c.md`)
- **At benchmark** (4-6%)                     → Variant B pitch (`value-review-variant-b.md`) — usually not urgent
- **At risk** (intensity dropping ≥1pt over last 3 months)  → Variant A or D
- **Over benchmark** (>7%)                    → No pitch needed; flag for the SAM

## Step 3 — Rank

Rank by WSC size descending WITHIN each category — big suppliers first.

## Step 4 — Output table

Markdown table with columns:
```
| Rank | Supplier | SuID | SRM | Category (WSP) | WSC (last mo) | WSP (last mo) | Intensity | Gap to 5% | Variant | Action |
```

Order: all No-spend first (ranked by WSC), then all Under-spending (ranked by WSC), then At-risk. Skip At-benchmark and Over-benchmark unless explicitly requested.

## Step 5 — Per-supplier 4-line outreach script

For the top 10 in the table, produce:

```
{Supplier}
  · Variant {A/B/C}
  · Ask: {one-line ask sentence using the variant template}
  · Storyboard: {storyboard_name}.md
  · Data prep: {what data the analyst needs to pull before building}
```

## Step 6 — Aggregate stats

Top of the output, before the table:

```
Period: {month}
Suppliers analysed: {N}
Total addressable gap to {benchmark_pct}%: £{X}M
Top 3 opportunities by gap-£: {names}
SRMs with most targets: {names + counts}
```

## What this storyboard does NOT do

- Build any slide decks. The output is text/CSV the analyst then uses to drive their week.
- For each supplier the analyst then runs the matching variant storyboard to build the actual deck.

## When the agent is asked

When the brief is "who should I pitch first", the agent runs this storyboard and surfaces the ranked list. It does NOT build decks proactively for all suppliers — that's wasteful. The analyst picks 3-5 from the top of the list and asks for those specific decks one at a time.
