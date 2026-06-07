---
name: major-shopping-holiday-wayfair
description: "When the user wants a Wayfair Sponsored Products (WSP) promo-event recap deck — Way Day, Black Friday, Cyber Week, BFCM, Boxing Day, January Sale, Easter, Bank Holiday weekends, Summer Sale, Christmas / Year-End Clearance. Also use when the user mentions 'share shift report,' 'promo for [supplier],' 'BFCM recap,' 'Way Day deck,' 'Cyber Week pitch,' 'pre-event email,' 'budget journey,' 'cap-only vs actual spend,' 'mitigation pull-forward,' 'incremental wholesale-per-pound,' or any event-specific recap. Produces a 4-6 slide PowerPoint ending in a recommended-action slide. Always asks for exact promo dates AND matched pre-period dates before any analysis (never infers from filenames or 'the holiday'). Applies all the foundation skill's hard rules (WSC never GRS, GBP, pt not bps, no blame language, plain English, scale-compression reframe). Uses the pre-event email evidence trail and/or mitigation cascade visualization on slide 3 when the supporting artefacts exist. Composes with anthropic/pptx (canonical PPTX) and pptx-from-layouts ([HINT: layout_name] pattern) via the wayfair-supplier-pitching foundation skill."
metadata:
  version: 1.0.1
  composes_with:
    - "wayfair-supplier-pitching (sibling foundation skill) — hard rules, visual register, storyboard mechanics"
    - "anthropic/pptx (https://github.com/anthropics/skills/blob/main/skills/pptx/SKILL.md) — canonical PPTX file I/O + QA loop"
    - "pptx-from-layouts (https://github.com/tristan-mcinnis/pptx-from-layouts-skill) — [HINT: layout_name] marker pattern"
---

> **Skill composition.** This skill is event-specific layered on top of `wayfair-supplier-pitching`. All hard rules, visual conventions, and storyboard mechanics come from the foundation skill. This skill specialises the deck architecture for promo events (Step 0 = exact dates, mid-deck checkpoint = required, 4-6 slide structure). PPTX file I/O is delegated to `anthropic/pptx`. See `SKILL_INTEGRATION.md` at the plugin root for the full skill graph.

# Major Shopping Holiday — Promo Recap Skill

For Way Day, Black Friday, Cyber Week, Boxing Day, January Sale, Easter, Bank Holiday weekends, Summer Sale, Christmas / Year-End Clearance. Produces a **4–6 slide PowerPoint** ending in a recommended-action slide.

**This skill builds on the `wayfair-supplier-pitching` foundation.** All hard rules, the workflow, the visual system, and the four recommendation variants come from there. This skill specialises the deck architecture for promo events.

---

## Step 0 — Establish the promo window (REQUIRED, do this first)

If exact dates aren't given, **ASK before doing anything else**. The whole framework hinges on two windows being defined precisely.

Lock in:

1. **Promo window** — start and end of the holiday event (e.g., Way Day 25–27 April 2026)
2. **Matched pre-period** — equal-length window before the promo. **Default**: same days-of-week, 4 weeks before. Offer this default but confirm. For multi-week events (BFCM, etc.), use the equivalent multi-week window 4–5 weeks prior, avoiding other promos.
3. **Supplier** — name and Supplier ID
4. **Region** — confirm UK (skill is UK-tuned)

**Never infer dates from filenames** or vague phrases. Data contains many spikes (Way Day, secondary promos, viral SKUs, Bank Holidays) — only the user knows which window the deck is meant to recap.

---

## Required inputs (typical)

- **Share Shift Report** (xlsx) — promo vs pre-period at supplier × category level (visits, orders, WSC, WSP spend, share %)
- **Extended advertising campaign reporting** CSV — monthly supplier-level WSP perf, used for YTD context AND last-30-days WSC (drives the budget recommendation)
- Optional: SKU-level retail data for class/SKU spotlight

---

## Slide-by-slide

### Slide 1 — Cover + KPI ribbon (always)

- DEEP background, white serif headline ≤40pt one line
- Four gold-topped KPI cards along the bottom (~2.85" wide each):
  - YTD WSP SPEND (£) + YoY%
  - WHOLESALE PER £1 OF WSP (YTD)
  - WSP % OF WSC (YTD) + prior-year comparison
  - {PROMO} CATEGORY SHARE delta (+X.Xpt)
- Never let a KPI value wrap. "+590 bps" → "+5.9pt".

### Slide 2 — YTD value context (always)

- White background, eyebrow "01 · THE YTD VALUE STORY"
- Title ≤22pt: plain English YoY framing ("You doubled WSP — and 1 in 5 wholesale pounds came from it")
- Left: lavender hero-stat card with WSP-attributed WSC share as hero number, 3 supporting stat rows
- Right: combo chart — monthly WSP spend bars + wholesale-per-£1 line on secondary axis, 13–16 months
- Bottom: four-cell YoY reframe row with delta pills (green good, red bad — always explain reds in a note)
- Footer takeaway: italic serif sentence naming the reframe

### Slide 3 — Promo recap centrepiece (always)

- White background, eyebrow "02 · {PROMO} {YEAR} RECAP"
- Title ≤20pt: the spend → WSC → share chain in one line
- **Four-card hero band on DEEP background**: WSP Spend (£), Orders, Wholesale (£), Category Share. Each card: eyebrow label / promo value (large serif) / "from {pre-period value}" / gold delta badge
- Below: two lavender cards — "WHAT YOU PUT IN" (spend share delta) and "WHAT YOU GOT OUT" (WSC share delta)
- Footer: incremental maths in plain English ("£X extra WSP → £Y extra wholesale = £Z per £1 of extra spend")

**If the pre-event email trail exists**: use the three-card grading from the foundation skill (RECOMMENDED / APPROVED / CONSEQUENCE) instead of the 4-card hero band.

**If there was a mitigation pull-forward**: use the four-card cascade (RECOMMENDED / APPROVED / ACTUAL / RESULT) + spend cascade bars below.

### Slide 4 (optional) — Supporting detail

Add ONLY if a story reinforces the ask. Pick ONE:

- **SKU / class spotlight** — top 1–3 SKUs that did the heavy lifting in the promo
- **Weekly cadence** — for multi-week events, WSP spend × wholesale-per-£1 across weeks
- **Forward pillars** — three lavender pillar cards (Efficient / Durable / Share-shifting)

White background, eyebrow "03 · {WHAT THIS SHOWS}". Single chart OR single hero block, not both.

### Slide 5 (optional) — Second supporting slide

Same rules as 4. Add only if genuinely necessary. If in doubt, drop.

### Final slide — Recommended action (always, last)

**Do not build until after the mid-deck checkpoint.**

Three variants (matching the foundation skill's A/B/C):

- **Variant A — Restart**: Title "Restart WSP — the maths still works." Pillars: What it did last time / What pausing cost / Low-risk re-entry. THE ASK: "Restart WSP at £X / month, set on Day 1 from prior month's landed WSC."
- **Variant B — Continue**: Title "Three reasons to keep investing — and a simple monthly rule." Pillars: Efficient / Durable / Share-shifting. THE ASK: "Continue WSP at current cadence — {benchmark}% of prior month's landed WSC, Day 1 monthly."
- **Variant C — Switch to %**: Title "One rule to fix lumpy spend: % of last month's wholesale." Pillars: What erratic spend cost / The portfolio rule / What the rule unlocks. THE ASK: "{Benchmark}% × last-30-days WSC = next month's WSP budget, set on Day 1." Show the actual £ figure.

**Default benchmark is 5% of WSC.** Confirm with the user if uncertain. Always show the resulting £ figure prominently.

---

## Mid-deck checkpoint (REQUIRED)

After building slides 1–3, **stop and check in with the user before generating the final slide**. Present in chat:

1. **Plain-English data analysis summary** — 4–6 bullets covering:
   - What the promo did (incremental £ wholesale, incremental wholesale-per-£1)
   - How the supplier sits on YTD (WSP % of WSC vs benchmark, YoY direction)
   - Whether WSP is currently active / paused / erratic (last-30-days WSC in £)
   - Any red flags (declining YoY, missed category outperformance, etc.)
2. **Your recommended path** with a one-sentence reason
3. **Four-option pick** for the user: Restart / Continue / Switch to % / You decide

Once they pick, build the final slide using the matching variant.

---

## Computation rules (promo)

For the promo window:
- `promo_spend`, `promo_wsc`, `promo_orders`, `promo_visits` — sum across promo dates
- `pre_spend`, `pre_wsc`, `pre_orders`, `pre_visits` — same for matched pre-period
- `wsc_share_pt = (supplier % of category WSC in promo) − (% in pre-period)` × 100, expressed as percentage points
- `incremental_wsc = promo_wsc − pre_wsc`
- `incremental_spend = promo_spend − pre_spend`
- `incremental_wholesale_per_pound = incremental_wsc / incremental_spend`

For YTD context (1 Jan → end of latest landed month):
- `wholesale_per_pound = wsp_attributed_wsc / wsp_spend` (NEVER GRS / spend)
- `wsp_pct_wsc = wsp_spend / total_wsc` (spend intensity)
- `wsp_attr_wsc = wsp_spend × wholesale_per_pound` (wholesale-equivalent of attributed revenue)

For the recommendation slide (Variants B/C):
- `last_30_days_wsc = sum of WSC across most recent 30 calendar days of landed data`
- `recommended_monthly_budget = benchmark_pct × last_30_days_wsc` (default benchmark 5%)
- Show both the rule AND the resulting £ figure

---

## QA checklist (before delivery)

- [ ] Every currency figure visible to supplier is **£ and WSC-based** (not $, not GRS)
- [ ] Promo dates AND pre-period dates cited explicitly on slide 3 in UK format ("23 April 2026")
- [ ] Slide count is 4–6 (cover, YTD, promo recap, optional 1–2 supporting, final ask)
- [ ] Final slide matches the recommendation variant the user confirmed
- [ ] If Variant C, the £ budget is shown explicitly using last-30-days WSC
- [ ] No KPI value wraps to two lines
- [ ] No title wraps awkwardly (last word alone on second line)
- [ ] Slide 2 footer names the wholesale-per-£1 compression logic out loud
- [ ] Slide 3 footer states incremental wholesale-per-£1 in plain English
- [ ] Final slide closing line: one sentence, three clauses, italic
- [ ] Filename matches `{Supplier}_{Promo}_{Year}_WSP_Deck.pptx`

---

## When to use the killer narrative patterns

Apply the patterns from the foundation skill (`wayfair-supplier-pitching`) when their preconditions exist:

- **CG/RTV reframe** — always include as a one-liner on the YTD value slide (slide 2) or on the supporting slide
- **Pre-event email evidence trail (three-card grading)** — use as slide 3 if the pre-event recommendation email exists
- **Mitigation cascade (four-card + spend bars)** — use as slide 3 if Wayfair pulled future-month spend forward to cover under-approved budget

If both pre-event-email evidence AND mitigation exist, the mitigation cascade subsumes the three-card grading and is the preferred slide 3.
