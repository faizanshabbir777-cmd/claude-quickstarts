---
name: restart-pitch-variant-a
description: Variant A Restart — supplier has been dark ≥2 months; the ask is "switch WSP back on now."
slide_count: 6
applies_when:
  - last_month_wsp == 0  OR  last_month_wsp < (0.1 * trailing_6mo_avg_wsp)
  - prior_period_wsp_active == true
  - prior_period_ws_roas >= 3   # the supplier had proven returns before going dark
canonical_example: TuttiBambini · Way Day 2026 (Faizan/Tapanshi)
ask:
  variant: A
  rule_pct: 5
  ask_template: "Switch WSP back on now at ~£{amount} / month — 5% of last month's wholesale revenue (~£{last_wsc}), set on day 1 so it never goes dark mid-month"
required_data:
  - supplier_name, supplier_id, period_label, srm_name
  - dark_days: int                 # consecutive days WSP was off
  - dark_window: {start_date, end_date}
  - missed_wholesale_estimate: £   # rough number for the "while it was dark" card
  - pre_dark_ws_roas: £            # the returns before they went dark
  - pre_dark_attr_wsc: £
  - pre_dark_wsp_spend: £
  - daily_calendar:                # day-by-day for last 30-45 days
      - {date, status: "on"|"off"}
  - search_traffic_trend: "rising"|"flat"|"falling"
  - last_month_wsc: £
references_baseline_slide: TuttiBambini slides 1-6 (this storyboard mirrors TuttiBambini almost beat for beat)
---

# Slide 1 — COVER

**LAYOUT:** `deep_purple_kpi_ribbon`
**EYEBROW:** gold — `"{SUPPLIER_NAME} · WAYFAIR SPONSORED PRODUCTS"`
**TITLE:** Serif Bold Italic, ~115pt, white, ends in period
**TITLE_EXAMPLES** (direct, urgent, conversational):
- *"Switch your WSP back on."*    ← TuttiBambini's exact line
- *"Restart now — the maths still works."*
- *"You were on. You went dark. The fix is one rule."*
**SUBTITLE:** Serif Italic, ~38pt, white, 2 lines, format `"It was working — then it went dark. Here is what it drove for you, and the simple way to keep it on."`
**KPI_RIBBON:** 4 cards. First three have GOLD top stripes (positive metrics). Fourth has **CORAL top stripe** (the loss).
- card 1: `EVERY £1 OF WSP` → serif italic `"£{pre_dark_ratio} back"` → sub `"in wholesale revenue (pre-dark)"`
- card 2: `{EVENT} ORDERS` (or `WSP ORDERS`) → serif italic `"×{ratio}"` → sub `"{prior_orders} → {peak_orders} in {days} days"`
- card 3: `{EVENT} WHOLESALE` → serif italic `"+£{delta}k"` → sub `"vs the weeks before"`
- card 4: **CORAL stripe** — `DAYS WSP WENT DARK` → serif italic `"{dark_days}"` in CORAL → sub `"right after {event_name}"`
**FOOTER:** `"{event_window} · prepared for {srm_name} · UK · GBP"`

---

# Slide 2 — VALUE STORY (when it was on)

**EYEBROW:** purple — `"01 · WHAT WSP WAS DRIVING"`
**TITLE:** *"When it's on, WSP turns small spend into big wholesale revenue."*
**LAYOUT:** `lavender_hero_left_chart_right` (same as value-review slide 2)

**LEFT CARD** (lavender):
- eyebrow: `"SO FAR IN {YEAR}"` or `"BEFORE IT WENT DARK"`
- hero: serif italic ~180pt, deep purple — `"£{ratio}"`
- explanation: `"of wholesale revenue for every £1 of WSP spend"`
- three rows:
  - `You spent` / `£{pre_dark_spend} on WSP`
  - `It drove` / `£{pre_dark_attr_wsc} wholesale revenue`
  - `That's` / `1 in {ratio} — a strong return`

**RIGHT CHART:** purple bars, monthly wholesale-per-£1 (or wholesale attributed)

**TAKEAWAY:** `"Take-away: your WSP has paid back about £{ratio} for every £1 — the engine works whenever it is running."`

---

# Slide 3 — THE EVENT RECAP (if there was a promo)

Use only if the dark period followed a specific event (Way Day, BFCM, etc.). Otherwise skip to slide 4.

**EYEBROW:** purple — `"02 · {EVENT} {YEAR} RECAP"`
**TITLE:** *"{Event} proved it: you put more in, and a lot more came out."*
**LAYOUT:** `deep_purple_kpi_band_left_lavender_side`

**LEFT BAND** (deep purple, 3 columns):
- col 1: `WSP SPEND` → `£{event_spend}` → `from £{pre_event_spend}` → green pill `×{ratio}`
- col 2: `ORDERS` → `{event_orders}` → `from {pre_event_orders}` → green pill `×{ratio}`
- col 3: `WHOLESALE REVENUE` → `£{event_wsc}` → `from £{pre_event_wsc}` → green pill `+£{delta}`

**RIGHT CARD** (lavender):
- eyebrow: `SHARE OF {CATEGORY}`
- 3 ascending green bars
- green serif italic: `"Rising"`
- slate sub: `"Your share grew during {event} (direction shown, not size)"`

**BODY SENTENCE:**
`"You nearly doubled WSP spend during {event} (from £{pre} to £{event}) — [GREEN: and orders doubled while wholesale revenue jumped +£{delta} (+{pct}%)]."`

**DATE FOOTNOTE:** `"{event} {dates} vs matched pre-period {pre_dates} ({n} days each)."`

**LAVENDER CALLOUT:**
`"The playbook is simple: more WSP on the right products = more shoppers reaching you = more orders and more wholesale revenue."`

---

# Slide 4 — THE PROBLEM (dark-days calendar)

**EYEBROW:** **CORAL** — `"03 · THE PROBLEM"`  (eyebrow colour shifts to coral because the slide is about loss)
**TITLE:** Serif Bold Italic — *"Right after {event}, your WSP went dark — and the orders stopped."*
**LAYOUT:** `dark_days_calendar`

**TOP:** small instruction caption — `"Each block is one day. Purple = WSP running. Grey = switched off."`

**CALENDAR VISUALISATION:** see `SKILL.md §A.5.4` for the full pattern.
- One row of small vertical blocks, one per day in `daily_calendar`
- Purple `#7B189F` = WSP on, Grey `#CFC7D6` = WSP off
- Gold tab `"{EVENT}"` above the event window with thin gold line below
- CORAL tab `"{N} DAYS DARK"` above the contiguous grey stretch with coral line below
- CORAL `"TODAY: OFF"` annotation if relevant on the last block
- Day numbers (every 7 days) and month labels in small slate Calibri below

**TWO CARDS BELOW THE CALENDAR:**

LEFT (CORAL bg `#FCE8E8`, coral left stripe):
- eyebrow CORAL: `"WHILE IT WAS DARK"`
- hero serif italic CORAL `~150pt`: `"~£{missed}k"`
- sub: `"of wholesale revenue likely missed over those {dark_days} days"`

RIGHT (LAVENDER bg, purple left stripe):
- eyebrow purple: `"THE PATTERN"`
- hero serif italic deep purple `~120pt`: `"On = sales"`
- sub: `"off = silence. The budget keeps running out mid-month."`

**TAKEAWAY:** `"Every day WSP is off, you stop showing up to ready-to-buy shoppers — and a competitor takes that slot."`

---

# Slide 5 — THE BIGGER PICTURE (search context)

**EYEBROW:** **CORAL** — `"04 · THE BIGGER PICTURE"`
**TITLE:** Serif Bold Italic — *"Your biggest source of shoppers is shrinking — WSP wins it back."*
**LAYOUT:** `search_decline_left_wsp_mockup_right`

LEFT card (CORAL-tinted bg, coral left stripe):
- eyebrow CORAL: `"SEARCH — HOW MOST SHOPPERS FIND YOU"`
- 3 descending coral bars (no axis labels)
- CORAL serif italic large: `"Falling"`
- sub: `"Fewer {category-shoppers} are finding you through search on their own — and it has been sliding for months."`

RIGHT card (LAVENDER bg, GOLD top stripe):
- eyebrow purple: `"WSP PUTS YOU BACK ON TOP OF SEARCH"`
- mock search bar: `Searching: "{example query}"`
- DEEP purple "SPONSORED" pill with `"{Supplier} {category}"` text
- grey "A competitor" row below
- sub: `"Sponsored Products place your {category} at the very top — right when a shopper is ready to buy."`

**TAKEAWAY:** `"With free search traffic shrinking, WSP isn't just upside — it's how you defend the shoppers you're losing."`

---

# Slide 6 — THE ASK (Variant A Restart)

**EYEBROW:** purple — `"05 · WHERE WE GO FROM HERE"`
**TITLE:** Serif Bold Italic — *"Restart WSP now — the maths still works."*
**LAYOUT:** `three_pillars_plus_ask`

**THREE PILLAR CARDS** (lavender bg, GOLD top stripe each):
- card 1: `IT WORKS` → `"£{ratio} / £1"` → `"Every £1 of WSP has returned about £{ratio} in wholesale revenue this year."`
- card 2: `GOING DARK COSTS YOU` → `"~£{missed}k"` → `"likely missed in just {dark_days} dark days after {event}. Off means £0 coming back."`
- card 3: `A SIMPLE RULE` → `"5%"` → `"of last month's wholesale revenue, set as the budget on day 1 — so it never runs dry."`

**THE ASK CARD** (full-width, DEEP purple, GOLD top stripe):
- gold eyebrow: `"THE ASK"`
- one sentence:
  `"Switch WSP back on now at  [GOLD: ~£{amount} / month]  —  5% of last month's wholesale revenue (~£{last_wsc}), set on day 1 so it never goes dark mid-month."`

**CLOSING LINE** (italic Georgia, slide bottom):
`"Proven £{ratio} back for every £1  ·  currently leaving wholesale revenue on the table  ·  one rule, live on day 1."`

---

# Computation rules

- `dark_days = count of consecutive days where status == "off" in daily_calendar`
- `missed = dark_days × (pre_dark_attr_wsc / pre_dark_period_days)` rounded down to nearest £k
- `amount = round(last_wsc × 0.05, -3)`
- `ratio = round(pre_dark_attr_wsc / pre_dark_spend, 2)`

# Reference

This storyboard mirrors the **TuttiBambini Way Day 2026 deck** (Faizan Shabbir / Tapanshi Agrawal) slide-for-slide. If the rendered output diverges visually from that reference, the agent has gone off-script — re-build using the storyboard literally.
