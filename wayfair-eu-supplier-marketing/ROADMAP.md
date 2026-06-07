# Roadmap — v1.1+ work pre-scoped as issues

Each item below is **pre-scoped issue-ready**: title, context, acceptance criteria, files to touch, test plan. When `Issues` is enabled on the repo, paste each block as a new GitHub issue. Then assign Copilot Coding Agent via the issue's `Assignees` panel.

If a human teammate (Brian, a returning Faizan, another SAM) picks one up, they have everything they need to ship without backchannel context.

---

## Issue 1 — Implement `promo-recap-tier0` storyboard

**Title:** `[v1.1] Implement promo-recap-tier0 storyboard in deck_builder.py`

**Labels:** `enhancement` `v1.1` `storyboards` `low-complexity`

**Context**

The dashboard ships three storyboards in v1.0. We need to add `promo-recap-tier0` — the Way Day / BFCM / Cyber Week pattern. Storyboard spec already exists at `storyboards/promo-recap-tier0.md`.

**Acceptance criteria**

- [ ] Add `render_promo_cover()` — cover with promo dates + 4 KPI cards (YTD spend, wholesale-per-£1, WSP % WSC, promo share delta)
- [ ] Add `render_ytd_value_context()` — combo chart (monthly WSP bars + wholesale-per-£1 line) + 4-cell YoY reframe row
- [ ] Add `render_promo_recap_centrepiece()` — 4-card hero band (DEEP background) with Spend / Orders / Wholesale / Share deltas
- [ ] Add `build_deck_promo_recap_tier0(data)` → 5-slide deck
- [ ] Register in `deck_builder.build_deck()` dispatcher
- [ ] Extend `data_prep.py` with `parse_share_shift_xlsx()` handling the Share Shift Report format
- [ ] Add Promo Window UI (dates required) in `app.py` when this storyboard selected
- [ ] Smoke test: synthetic deck builds, validates via python-pptx, 5 slides, dates appear on slide 3

**Files to touch**

- `dashboard/deck_builder.py` (~250 lines)
- `dashboard/data_prep.py` (~80 lines)
- `dashboard/app.py` (storyboard dropdown + promo-window UI)

**Reference patterns**

- `restart-pitch-variant-a` is the closest existing 5-slide pattern (event-based)
- TuttiBambini deck is the visual reference (in `Forte_UK_2024-2026YTD_WSP_Deck_v2.pdf`)
- Storyboard spec: `storyboards/promo-recap-tier0.md`

**Out of scope**

- Pre-event email evidence trail (separate issue)
- Mitigation cascade visualization (separate issue)

**Test plan**

```bash
cd wayfair-eu-supplier-marketing/dashboard
python3 -c "
import data_prep, deck_builder
data = data_prep.demo_data()
data['event_name'] = 'Way Day 2026'
data['promo_dates'] = '2026-04-25 to 2026-04-27'
data['pre_period_dates'] = '2026-03-28 to 2026-03-30'
data['promo_spend'] = 3300
data['promo_wsc'] = 27600
pptx = deck_builder.build_deck('promo-recap-tier0', data)
with open('/tmp/test_promo.pptx', 'wb') as f: f.write(pptx)
from pptx import Presentation
p = Presentation('/tmp/test_promo.pptx')
assert len(p.slides) == 5
print('PASS')
"
```

---

## Issue 2 — Implement `summit-case-study` storyboard

**Title:** `[v1.1] Implement summit-case-study storyboard (numbers stripped)`

**Labels:** `enhancement` `v1.1` `storyboards` `low-complexity`

**Context**

The multi-supplier showcase storyboard for events like the EU Supplier Summit. Numbers stripped, supplier names visible. Storyboard spec at `storyboards/summit-case-study.md`.

**Acceptance criteria**

- [ ] Add `render_summit_cover()` — text-only cover, two short sentences
- [ ] Add `render_what_we_saw_side_by_side()` — two lavender cards side-by-side, qualitative verbs in green italic
- [ ] Add `render_where_you_fit_soft_ask()` — three pillar cards + DEEP "Start the WSP conversation" ask card (no £-amount, soft CTA)
- [ ] Add `build_deck_summit_case_study(data)` → 3-slide deck
- [ ] Register in dispatcher
- [ ] Extend `app.py` to allow MULTIPLE supplier names (the storyboard uses 2 case studies, not 1)
- [ ] Smoke test: builds with 2 supplier names; verify no numbers appear in slide text

**Files to touch**

- `dashboard/deck_builder.py` (~180 lines)
- `dashboard/app.py` (multi-supplier input UI)

**Reference**

- Storyboard spec: `storyboards/summit-case-study.md`
- Previous worked example: `Receipts_Portfolio_v2.pdf` includes the v1 summit deck

**Test plan**

```bash
python3 -c "
import deck_builder
data = {
  'supplier_a': 'Forte UK',
  'supplier_b': 'Monty Trading UK',
  'period': '2026 Summit',
  'signals_a': ['Ad investment scaled', 'Wholesale tracked it', 'Fulfilment matured'],
  'signals_b': ['Ad investment scaled', 'Visits rose', 'Orders kept pace'],
}
pptx = deck_builder.build_deck('summit-case-study', data)
with open('/tmp/test_summit.pptx', 'wb') as f: f.write(pptx)
from pptx import Presentation
assert len(Presentation('/tmp/test_summit.pptx').slides) == 3
print('PASS')
"
```

---

## Issue 3 — Implement `mbr-supplier-review` storyboard (internal register)

**Title:** `[v1.1] Implement mbr-supplier-review storyboard (em-dash titles, dense tables, internal register)`

**Labels:** `enhancement` `v1.1` `storyboards` `medium-complexity`

**Context**

The internal MBR register — em-dash titles, dense KPI tiles with bps deltas, full data tables, GRS permitted (internal audience only). Different visual register from TuttiBambini (the supplier-facing default).

**Acceptance criteria**

- [ ] Add `render_mbr_cover()` — minimal cover, "Monthly Business Review" Liberation Serif Bold
- [ ] Add `render_mbr_executive_summary()` — KPI tiles + commentary block
- [ ] Add `render_mbr_dense_table()` — 12-15 row data table with em-dash separator, % GRS / % WSC / MoM bps / YoY bps columns
- [ ] Add `render_mbr_top_suppliers()` — two-column dense table
- [ ] Add `build_deck_mbr_supplier_review(data)` → 4-slide deck
- [ ] Register `mbr-supplier-review` in dispatcher
- [ ] Add audience guard in `app.py` — only allow this storyboard when audience = Internal
- [ ] **Hard rule check**: GRS columns appear ONLY when audience = Internal; never in supplier-facing

**Files to touch**

- `dashboard/deck_builder.py` (~300 lines — denser tables than TuttiBambini)
- `dashboard/app.py` (audience-guard logic)

**Reference**

- The March '26 MBR (`a4f67009-WSP_MBR_March2026_11.pptx` in conversation history) is the visual baseline
- Storyboard spec: `storyboards/mbr-supplier-review.md`
- §C "Two visual registers" in `skills/wayfair-supplier-pitching/SKILL.md`

**Test plan**

Verify GRS does NOT appear when audience flag is set to supplier-facing. Verify the em-dash title format matches the existing March '26 MBR.

---

## Issue 4 — Add `portfolio-outreach` ranking output (no deck)

**Title:** `[v1.1] Implement portfolio-outreach storyboard (outputs ranked list, not a deck)`

**Labels:** `enhancement` `v1.1` `portfolio` `low-complexity`

**Context**

When a CM asks *"who should I pitch first this month?"* the output should be a ranked list, not a slide deck. Storyboard spec at `storyboards/portfolio-outreach.md`.

**Acceptance criteria**

- [ ] Add `compute_portfolio_ranking(df)` in `data_prep.py` that returns a ranked pandas DataFrame
- [ ] Ranking logic per spec: No-spend first (by WSC desc), then Under-spending (by WSC desc), then At-risk
- [ ] Compute `gap_to_5pct = wsc × 0.05 - current_spend` per supplier
- [ ] Add a new tab in `app.py` "Portfolio Ranking" that displays the ranked table + download as CSV
- [ ] Output 4-line outreach script per top-10 supplier (Variant + Ask + Storyboard + Data prep)
- [ ] Smoke test: feed the 2025 Summit xlsx, verify the top 10 rankings make sense

**Files to touch**

- `dashboard/data_prep.py` (~120 lines)
- `dashboard/app.py` (new tab)

---

## Issue 5 — Add Looker Studio data ingestion source

**Title:** `[v1.1] Read data directly from Looker Studio dashboard ID instead of CSV upload`

**Labels:** `enhancement` `v1.1` `integration` `medium-complexity` `needs-credentials`

**Context**

CMs currently export Looker dashboards to CSV before uploading. Direct read removes the manual export step. See `INTEGRATIONS.md` for the architecture.

**Acceptance criteria**

- [ ] Add `dashboard/scripts/looker_studio.py` with `fetch_dashboard(dashboard_id, period) -> pd.DataFrame`
- [ ] Service account creds from `.streamlit/secrets.toml` under `[looker]`
- [ ] Wire the "Use Looker Studio dashboard" checkbox in `app.py` Filters tab (currently a stub)
- [ ] Cache results for 15 minutes (don't re-query the API for every interaction)
- [ ] Graceful fallback if creds are missing → display "Looker creds not configured · using CSV upload instead"
- [ ] Smoke test with a mocked Looker response

**Files to touch**

- `dashboard/scripts/looker_studio.py` (new file)
- `dashboard/app.py` (wire the checkbox)
- `dashboard/.streamlit/secrets.toml.example` (add `[looker]` template)

**Out of scope**

- BigQuery direct query (separate issue — Issue 6)
- Looker write-back (not supported)

**Needs**

Service account credentials from Wayfair IT — see the IT paragraph in `INTEGRATIONS.md`.

---

## Issue 6 — Add Slack webhook for Send-to-SRM

**Title:** `[v1.1] Wire Slack webhook for the "Send to SRM via Slack" button`

**Labels:** `enhancement` `v1.1` `integration` `low-complexity`

**Context**

The Send tab has a "Send to SRM via Slack" button that's currently disabled. When the team's `#wsp` Slack webhook is configured, this button should post the deck to a DM or channel.

**Acceptance criteria**

- [ ] Add `dashboard/scripts/slack.py` with `post_deck_to_srm(srm_slack_id, deck_bytes, message) -> bool`
- [ ] Webhook URL from `.streamlit/secrets.toml` under `[slack]`
- [ ] Wire the button in `app.py` Send tab to call this
- [ ] Include the editable SRM message template in the Slack post body
- [ ] Attach the .pptx via Slack file upload API
- [ ] Smoke test against a test channel before shipping

**Files to touch**

- `dashboard/scripts/slack.py` (new file)
- `dashboard/app.py` (wire the button)
- `dashboard/.streamlit/secrets.toml.example` (add `[slack]` template)

**Needs**

Slack webhook URL or bot token from Wayfair Slack admin.

---

## How to use this ROADMAP

### Path A — Manual pickup (no Copilot)

A teammate (Brian during your leave, or you on return) reads an issue block above, branches off `main`, ships the changes, opens a PR. Each issue is self-contained.

### Path B — Copilot autonomous (when issues are enabled)

1. Enable issues on the repo: `github.com/{owner}/{repo}/settings` → check `Issues`
2. Paste each block above into a new GitHub issue
3. In the issue UI, click `Assignees` → select `Copilot` (GitHub Coding Agent)
4. Copilot picks the issue, ships a PR
5. Run `request_copilot_review` on the PR for second-pass review, or hand to a human

### Path C — Cursor / other AI editor

A teammate opens the repo in Cursor (or any AI editor). The `.cursorrules` file primes the AI with the WSP playbook context. The teammate says "implement Issue 1 from ROADMAP.md" and the editor's AI reads the block above and ships it.

---

## Triage — which path for which issue

| Issue | Complexity | Recommended path |
|---|---|---|
| 1. promo-recap-tier0 | Low (follows restart-pitch pattern) | Copilot or Cursor |
| 2. summit-case-study | Low (3 slides, no data math) | Copilot or Cursor |
| 3. mbr-supplier-review | Medium (different visual register) | Manual or Cursor with human review |
| 4. portfolio-outreach | Low (pandas ranking + new tab) | Copilot or Cursor |
| 5. Looker integration | Medium (needs IT creds) | Manual when creds land |
| 6. Slack webhook | Low (one API call) | Copilot or Cursor when creds land |

---

## What's NOT on this roadmap

- Mobile-responsive dashboard (Streamlit auto-handles)
- Multi-language (UK only for now)
- Real-time collaboration (single-CM workflow is fine)
- Database backend (stateless by design — see `DATA_SAFETY.md`)
- LLM-based slide-text generation (storyboards lock the text deliberately)
