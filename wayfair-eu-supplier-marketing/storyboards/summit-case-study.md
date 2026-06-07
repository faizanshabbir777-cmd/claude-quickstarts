---
name: summit-case-study
description: Multi-supplier showcase deck for the EU Supplier Summit or similar PUBLIC audiences. Numbers stripped — supplier names visible. The pitch is to OTHER suppliers in the room.
slide_count: 3
applies_when:
  - audience is public-supplier-facing (summit, panel, multi-supplier event)
  - the brief is "convince other suppliers to invest"
  - 2+ supplier case studies are being shown
canonical_example: Forte + Monty SU Summit deck
ask:
  variant: soft CTA — "Start the WSP conversation with your SRM."
hard_rules:
  - No specific performance numbers anywhere (intensities, %s, £-amounts)
  - Supplier names ARE visible (using them is the entire point of a case-study deck)
  - Survivorship-bias disclaimer mandatory ("two suppliers among many on the WSP platform")
  - Causation softened — "scaled with" not "powered" — see SKILL.md §C Hard Rule #4 extension
  - Directional verbs in green italic ("rose", "followed", "kept pace", "tracked it") replace specific numbers
required_data:
  - supplier_names: [list]
  - per supplier: category descriptor + 1-line origin (e.g. "Bedroom · Polish manufacturer")
  - per supplier: 4-6 funnel signals that moved in the relevant period
references_baseline_slide: Forte+Monty SU Summit deck v2 (already in receipts portfolio)
---

# Slide 1 — COVER

**LAYOUT:** `deep_purple_no_kpi_ribbon` (cover is text-only — no KPI cards because no numbers)
**EYEBROW:** gold — `"{EVENT_NAME}  ·  WAYFAIR SPONSORED PRODUCTS"`
**TITLE:** Two short sentences, each on its own line, Serif Bold Italic, ~115pt, white, each ends in period
**TITLE_EXAMPLES:**
- `"Two suppliers."` / `"One playbook."`
- `"Different brands."` / `"Same pattern."`
**SUBTITLE:** Serif Italic, 2-3 lines — `"{Supplier A} and {Supplier B} — different categories, different starting points. Same pattern emerges when WSP investment scales."`
**FOOTER:** `"{event_name} · prepared for the room · UK · sample of many"`

---

# Slide 2 — WHAT WE SAW (side by side)

**EYEBROW:** purple — `"01 · WHAT WE SAW"`
**TITLE:** *"When WSP investment scaled, every signal in the funnel scaled with it."*
**LAYOUT:** `two_lavender_cards_side_by_side`

For EACH supplier (2 cards):
- LAVENDER bg, GOLD top stripe
- eyebrow purple letter-spaced: `"{SUPPLIER NAME UK}"`
- sub: 2 lines, italic slate, category + origin (`"Bedroom · Polish manufacturer"`)
- Lead-in: Serif Bold Italic deep purple ~42pt — `"When WSP scaled,"`
- 4-6 bullet rows:
  - `■  {Signal name}    {GREEN ITALIC: directional verb}`
  - Examples: `Ad investment  →  rose` / `Customer visits  →  rose with it` / `Carts added  →  kept pace` / `Orders placed  →  kept pace` / `Total UK wholesale  →  tracked it`
- Bottom italic serif: a short summary line per supplier

**TAKEAWAY:** italic Georgia bottom — `"Take-away: different categories, different journeys, same pattern — the funnel responds when WSP scales."`

---

# Slide 3 — WHERE YOU FIT + THE ASK

**EYEBROW:** purple — `"02 · WHERE YOU FIT"`
**TITLE:** *"Your funnel could be next — same lever, same rule, your business."*
**LAYOUT:** `three_pillars_plus_soft_ask`

THREE PILLAR CARDS (lavender, gold top stripe):
- card 1: `THEY COMMITTED` → `"before they were sure"` → `"Both started with sustained micro-spend, not a one-month splash. The signal needed months to build."`
- card 2: `THEY HELD THE RULE` → `"every month, on day 1"` → `"5% of last month's wholesale, set as the WSP budget on the first of every month. No mid-month surprises."`
- card 3: `THE PATTERN HELD` → `"across the whole funnel"` → `"Visits, attribution, wholesale, fulfilment — all moved together. The skill is in keeping it consistent."`

THE ASK CARD (full-width, DEEP purple, GOLD top stripe — but SOFT ask, no £-amount):
- gold eyebrow: `"THE ASK"`
- main sentence (Calibri Bold ~44pt, white): `"Start the WSP conversation with your SRM."`
- DISCLAIMER (small, italic, light-lavender, 2 lines): `"Two suppliers among many on the WSP platform — different starting points produce different ramps, but the pattern recurs."`

CLOSING LINE: italic Georgia, three clauses — `"Same lever  ·  same rule  ·  your business."`

---

# Computation rules

- NO computation outputs go on the slides.
- Internal sanity check still happens — the agent should verify the case-study suppliers really did show the pattern before claiming so on the slides.

# Bias checks (mandatory — built into the storyboard)

- ✅ Survivorship bias disclosed via the "two suppliers among many" line on slide 3
- ✅ Causation overclaim avoided — "scaled with the growth" not "powered the growth"
- ✅ Soft CTA — "Your funnel COULD be next" not "Your funnel IS next"
- ✅ No specific numbers — viewer can't fact-check against their own performance and feel unimpressed

# What this storyboard does NOT cover

- Single-supplier value reviews (use `value-review-variant-b.md`)
- Single-supplier restart pitches (use `restart-pitch-variant-a.md`)
- Internal-audience leadership decks (use `mbr-supplier-review.md` — numbers permitted)
