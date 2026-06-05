---
name: promo-recap-tier0
description: Way Day, Black Friday, Cyber Week, BFCM, Boxing Day, January Sale, Easter, Bank Holiday weekends, Summer Sale, Christmas / Year-End Clearance.
slide_count: 5
applies_when:
  - brief mentions specific event_name from the Tier 0 list
  - exact promo_dates AND matched pre_period_dates are CONFIRMED by the analyst
canonical_example: TuttiBambini · Way Day 2026
ask:
  variant: depends on supplier state — A Restart if dark after the event, B Continue if active, C Switch-to-5% if erratic
hard_rules:
  - Step 0 — confirm exact promo dates AND matched pre-period dates BEFORE building anything. Never infer from filenames.
  - Use the pre-event email evidence trail (SKILL.md §A.5.2) if the email exists.
  - Use the mitigation cascade (SKILL.md §A.5.3) if Wayfair pulled future-month spend forward.
  - Otherwise use the standard 4-card hero band on slide 3.
required_data:
  - supplier_name, supplier_id, srm_name
  - event_name, event_year
  - promo_dates: {start, end}
  - pre_period_dates: {start, end}
  - promo_spend, promo_orders, promo_wsc, promo_visits, promo_wsc_share
  - pre_spend,  pre_orders,  pre_wsc,  pre_visits,  pre_wsc_share
  - ytd_wsp_spend, ytd_wsp_attr_wsc, ytd_wsc, ytd_ws_roas, ytd_wsp_pct_wsc
  - last_30_days_wsc                      # drives the recommendation £
  - pre_event_email_trail (optional)
  - budget_journey (optional, for mitigation cascade)
references_baseline_slide: TuttiBambini deck (uses this pattern almost exactly)
---

# Slide 1 — COVER + KPI ribbon

**LAYOUT:** `deep_purple_kpi_ribbon`
**EYEBROW:** gold — `"{SUPPLIER_NAME} · {EVENT_NAME} {YEAR} RECAP"`
**TITLE:** Serif Bold Italic, white, ends in period
**TITLE_EXAMPLES:**
- *"{Event} proved it. Now let's keep going."*
- *"Switch your WSP back on."*  ← if the supplier went dark after
- *"You doubled WSP, and a lot more came back."*
**SUBTITLE:** 2 lines, italic — `"{Event} {dates}. Here is what the {N}-day window drove for you, and the simple rule to capture it next time."`
**KPI_RIBBON:** 4 cards
- card 1: `YTD WSP SPEND` → `"£{X}k"` → sub `"+{pct}% YoY"`
- card 2: `WHOLESALE PER £1 OF WSP (YTD)` → `"£{X}"` → sub `"YoY {direction} from £{prior}"`
- card 3: `WSP % OF WSC (YTD)` → `"{pct}%"` → sub `"vs {prior_pct}% in {prior_year}"`
- card 4: `{EVENT} CATEGORY SHARE` → `"+{X}pt"` → sub `"shift vs pre-period"`  (CORAL stripe if NEGATIVE)
**FOOTER:** `"{event_dates} · prepared for {srm_name} · UK · GBP"`

---

# Slide 2 — YTD VALUE CONTEXT

**EYEBROW:** purple — `"01 · THE YTD VALUE STORY"`
**TITLE:** plain English YoY framing
**TITLE_EXAMPLES:**
- *"You doubled WSP — and 1 in {N} wholesale pounds came from it."*
- *"WSP is paying for itself {N} times over — and the gap to last year is closing."*
**LAYOUT:** `lavender_hero_left_combo_chart_right`

**LEFT** lavender hero-stat card:
- eyebrow: `"SO FAR IN {YEAR}"`
- hero: serif italic deep purple `"£{ratio}"`  (the wholesale-per-£1)
- explanation
- 3 rows: spend / drove / ratio

**RIGHT** combo chart:
- Monthly WSP spend bars (purple)
- Wholesale-per-£1 line (gold) on secondary axis
- 13-16 months of history

**BOTTOM** 4-cell YoY reframe row (small cards):
- Spend YoY (delta pill)
- Wholesale-per-£1 YoY (delta pill — note this often DROPS as scale grows; the §C scale-compression reframe applies)
- WSC YoY (delta pill)
- WSP % WSC YoY (delta pill)

**TAKEAWAY:** italic serif sentence naming the wholesale-per-£1 compression logic out loud — e.g. `"Yes, your wholesale-per-£1 dipped from £{prior} to £{latest} — that is what scale costs you, and you still cleared £{X}k of attributed wholesale that didn't exist last year."`

---

# Slide 3 — PROMO RECAP CENTREPIECE

**EYEBROW:** purple — `"02 · {EVENT} {YEAR} RECAP"`
**TITLE:** the spend → WSC → share chain in one sentence
**LAYOUT:** branches based on what evidence exists:

**BRANCH A** — Standard hero band (no pre-event email, no mitigation):
- 4-card hero band on DEEP background:
  - WSP SPEND (£) + green pill delta
  - ORDERS + green pill delta
  - WHOLESALE (£) + green pill delta
  - {CATEGORY} SHARE (pt delta — CORAL pill if negative)
- Below: two lavender cards — `"WHAT YOU PUT IN"` (spend share delta) and `"WHAT YOU GOT OUT"` (WSC share delta)
- Footer: incremental maths in plain English — `"£{X} extra WSP → £{Y} extra wholesale = £{Z} per £1 of extra spend"`

**BRANCH B** — Pre-event email trail exists:
- Use the three-card grading from `SKILL.md §A.5.2`:
  - RECOMMENDED (lavender, purple cap, full presence)
  - APPROVED (white, hairline, grey cap, diminished)
  - CONSEQUENCE (deep purple, gold cap)
- Each card has the per-day rate, total, and 3 bullets
- The CONSEQUENCE card has a specific predicted detail from the email + `"Outcome predicted in [date] email"`

**BRANCH C** — Mitigation pull-forward happened:
- Use the four-card cascade from `SKILL.md §A.5.3`:
  - RECOMMENDED · APPROVED · ACTUAL · RESULT
- Below the cards: 3-bar mitigation visualisation (RECOMMENDED / ACTUAL / CAP-ONLY)
- Footer in plain English: `"The cap alone would have run £{Z}. Pulling {month} forward lifted you to £{Y} — and you still lost −{N}pt of share."`

---

# Slide 4 (optional) — Supporting detail

Add ONLY if a story reinforces the ask. Pick ONE:
- SKU / class spotlight (top 1-3 SKUs that did the heavy lifting)
- Weekly cadence (for multi-week events)
- Forward pillars (3 lavender cards — Efficient / Durable / Share-shifting)

White background. EYEBROW: `"03 · {WHAT THIS SHOWS}"`. Single chart OR single hero block, not both.

---

# Slide 5 — THE ASK

**EYEBROW:** purple — `"04 · WHERE WE GO FROM HERE"`  (renumber up if slide 4 was added: `"04 · ..."` becomes `"05 · ..."`)
**TITLE:** depends on which variant the analyst confirms at the mid-deck checkpoint:
- Variant A Restart: *"Restart WSP now — the maths still works."*
- Variant B Continue: *"Three reasons to keep investing — and a simple monthly rule."*
- Variant C Switch-to-%: *"One rule to fix lumpy spend: % of last month's wholesale."*

**LAYOUT:** `three_pillars_plus_ask` (same as `value-review-variant-b.md` slide 4)

THREE PILLAR CARDS (lavender, gold top stripe each) — content depends on variant. See `SKILL.md §B.3 Final slide` for the three variant templates.

THE ASK CARD (full-width, DEEP purple, GOLD top stripe) — sentence with the £-amount HIGHLIGHTED IN GOLD.

CLOSING LINE — italic Georgia, 3 clauses separated by `·`.

---

# Mid-deck checkpoint (REQUIRED)

After building slides 1-3, **stop and check in with the analyst**. Present in chat:

1. Plain-English data summary (4-6 bullets)
2. Recommended path with a one-sentence reason
3. Four-option pick: A Restart / B Continue / C Switch to % / D Custom

Only build slide 5 after the analyst confirms.

---

# QA checklist (before delivery)

See `SKILL.md §B.6`. The promo-specific bits to verify:
- Promo dates AND pre-period dates cited explicitly on slide 3 in UK format ("23 April 2026")
- Slide 3 footer states incremental wholesale-per-£1 in plain English
- The £ ask amount uses last-30-days WSC, not promo WSC
