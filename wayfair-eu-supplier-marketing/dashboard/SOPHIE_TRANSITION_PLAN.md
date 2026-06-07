# Sophie's Transition Plan — bridging to Claude-licensed workflows

> *"Sophie needs to ensure we can move to Claude transition after licences across WSP Champions are acquired."*

This doc maps the path from **Phase 1 (today)** — Streamlit dashboard, no Claude license required — to **Phase 2 (post-license)** — same dashboard, plus Claude-assisted enhancements that unlock the more strategic work.

---

## TL;DR

The current system is **fully usable without Claude**. CM Champions can ship pitch decks today via the Render URL using only the Streamlit UI.

When Claude licenses arrive for the WSP Champion cohort, **the dashboard does not change.** What changes is which CM Champion can additionally use the underlying Claude Code skill (`wayfair-supplier-pitching`) directly — for custom analysis, ad-hoc questions, and the v1.1 storyboards that involve judgement (promo recap with mid-deck checkpoint, summit case study with bias check).

Three transition gates. Sophie owns the readiness of each.

---

## Phase 1 — Today · No Claude license needed

**What the team has:**

- ✅ Render URL — `wsp-builder.onrender.com`
- ✅ Password-gated (`Faizan's Claude Skill - EU WSP`)
- ✅ Three live storyboards via Build button (Value Review · Restart · Switch-to-5%)
- ✅ Audit-confirmed zero Claude / Anthropic API dependencies in the runtime
- ✅ Real personalised builds from CSV uploads
- ✅ Brian's runbook for 7-week leave coverage

**What CM Champions do:**

1. Open the URL
2. Enter password
3. Filter → Upload CSV → Build → Download .pptx
4. Forward to SRM

**What CM Champions can NOT do (Phase 1):**

- Run free-form analysis ("how is supplier X doing across categories?")
- Get AI-assisted title selection from the storyboard examples
- Use the v1.1 storyboards (promo recap, summit, MBR) that require judgement at checkpoints

That's fine for the bridge period. The 3 live storyboards cover ~80% of pitch volume.

---

## Phase 2 — Post-license · Claude-assisted enhancements

**What unlocks for each CM Champion who has a Claude Code license:**

### 2a. Direct skill activation

```bash
claude-code /plugin install ./wayfair-eu-supplier-marketing
```

A licensed CM can install the `wayfair-supplier-pitching` skill directly. Then in any Claude Code session:

```
/wsp Forte UK · Way Day 2026 recap · share shift report in ./data/
```

Claude reads the storyboard, asks the kickoff questions, builds the deck. **Same playbook, same TuttiBambini visual register, same hard rules.** The dashboard becomes optional — the skill is the workhorse.

### 2b. Ambiguous-CSV handling via Claude

The current `data_prep.py` matches columns via a hard-coded `COLUMN_ALIASES` dict. When a CM uploads a file with weird column names ("Spend (GBP)" vs "Total Spend" vs "Sponsored Product Spend"), the deterministic parser fails.

With Claude licensed, the data-prep subagent can **read the file's headers and infer the column mapping** via the Claude API. This is the difference between "parser fails, CM contacts Brian" and "parser works on first try."

### 2c. v1.1 storyboards with judgement checkpoints

The promo recap, summit, and MBR storyboards require **mid-deck checkpoints** where a Claude-assisted agent presents a data summary and asks the CM to confirm the closing variant. The Streamlit dashboard can't do this gracefully — it needs Claude in the loop.

When licenses arrive, these storyboards ship as Phase 2 enhancements.

### 2d. SRM-personalised send-to-SRM messages

Phase 1 Send tab has an editable template. Phase 2: Claude reads the SRM's last 3-5 interactions (from a CRM export) and personalises the message to the relationship.

---

## The three transition gates (Sophie's checklist)

### Gate 1 · License procurement (Sophie owns)

- [ ] Confirm CM Champion roster with Clement (3-4 names + Brian + 1-2 expansion candidates)
- [ ] Procure Claude Code licenses for the cohort (enterprise tier vs individual — see "License model" below)
- [ ] Confirm Wayfair's Anthropic enterprise agreement is in place (data residency, no-training clause, retention policy)
- [ ] Distribute license activation instructions

### Gate 2 · Skill plugin install across the cohort (Sophie + Brian)

- [ ] Each licensed CM runs `claude-code /plugin install` once
- [ ] Verify the skill auto-activates on WSP-related prompts in a test session
- [ ] Brief each CM on the `/wsp` slash command + the kickoff questions
- [ ] Run a paired session for each CM's first real deck (Brian shadowing)

### Gate 3 · v1.1 storyboard activation (Faizan back + Sophie)

- [ ] Faizan returns, ships the 4 v1.1 storyboards (promo recap, summit, MBR, portfolio)
- [ ] Sophie coordinates the rollout cadence (one storyboard per week, paired sessions)
- [ ] Update the dashboard's storyboard dropdown to mark v1.1 as ✅ Live
- [ ] Sunset the "v1.1 coming" copy

---

## What stays the same across the transition

| Asset | Phase 1 | Phase 2 |
|---|---|---|
| Render URL | ✅ Live | ✅ Same URL, same password |
| Streamlit dashboard | ✅ The single entry point | ✅ Still the default — Claude path is *additional* |
| TuttiBambini visual register | ✅ Locked | ✅ Locked |
| 10 hard rules | ✅ Enforced in code | ✅ Enforced in code AND skill |
| Storyboards | ✅ 3 live | ✅ 7 live |
| Dashboard password | ✅ `Faizan's Claude Skill - EU WSP` | ✅ Same (or Sophie rotates if needed) |
| `BRIAN_RUNBOOK.md` | ✅ Brian's coverage doc | Becomes Sophie's doc |
| `DATA_SAFETY.md` | ✅ Current safety surface | Plus the Anthropic data agreement |

---

## What CHANGES across the transition

| Capability | Phase 1 | Phase 2 |
|---|---|---|
| Where the build happens | Streamlit dashboard only | Dashboard OR `/wsp` in Claude Code |
| Column-mapping for non-standard CSVs | Hard-coded aliases · fail silently | Claude infers · just works |
| Title selection from `TITLE_EXAMPLES` | Defaults to first example | Claude picks the best fit for the supplier |
| Mid-deck checkpoint | Auto-defaults to recommended variant | Claude surfaces summary, CM confirms |
| Free-form supplier analysis | Not supported | Supported via Claude Code chat |
| Promo recap / summit / MBR storyboards | "v1.1 coming" | ✅ Live |
| Audit log | JSONL file in container | JSONL file + Claude session transcripts |
| Cost per build | $0 (Streamlit free tier) | $0.05-0.15 (Claude API tokens) |

---

## License model — what Sophie needs to decide

Three options:

### Option A · Individual Claude Pro/Max licenses
- Each CM Champion buys their own Claude subscription (~$20-200/mo)
- Simplest. No procurement gate.
- Risk: inconsistent license states across the team

### Option B · Wayfair enterprise Claude Code agreement
- Anthropic enterprise contract scoped to the WSP Champion cohort
- Sophie or Wayfair IT owns the agreement
- Best: consistent tooling, data agreement covers everyone

### Option C · Hybrid
- Wayfair enterprise contract for the core CM Champion cohort
- Individual licenses for expansion users (other SAMs not in the pilot)

**Recommendation:** Option B for the pilot cohort (3-4 CMs + Brian). Move to Option C if/when the rollout expands beyond the pilot.

---

## Data residency · what doesn't change

- Phase 1: supplier data stays on the Render service (Frankfurt EU region) — no Claude API calls
- Phase 2: supplier data stays the same — Claude API calls travel under Wayfair's enterprise data agreement (no training, 30-day retention max, then deleted)
- Both phases: GDPR compliance via the EU-region hosting choice
- Both phases: no PII processed (supplier-level aggregates only)

Sophie confirms Anthropic's enterprise data agreement matches Wayfair's standard vendor data terms before Gate 2. The `DATA_SAFETY.md` doc has the framework — extend it for Phase 2 with the Anthropic agreement specifics.

---

## Timeline (suggested)

| Week | Phase | Action | Owner |
|---|---|---|---|
| **Pilot Week 1-2** | Phase 1 | CMs use Render URL with the 3 live storyboards | Brian covers issues |
| **Pilot Week 3-4** | Phase 1 → 2 transition | Sophie procures licenses, runs Gate 1 | Sophie |
| **Pilot Week 5-6** | Phase 2 install | Each CM installs the plugin, runs paired session | Sophie + Brian |
| **Faizan returns** | Phase 2 buildout | Ship v1.1 storyboards (promo, summit, MBR, portfolio) | Faizan + Sophie |
| **Post-launch** | Phase 2 operating | Sophie owns the steady-state | Sophie |

---

## What Sophie needs from Faizan before he leaves

1. **Roster of CM Champions** — names + emails + which tier the user is targeting
2. **Anthropic enterprise contact** — if Wayfair already has an agreement, who's the AM?
3. **Budget envelope** — what's the procurement budget for the licenses?
4. **Sunset criteria** — when (if ever) does the Render URL get retired in favour of the Claude Code workflow?

(Faizan: please fill in the answers in `SOPHIE_HANDOFF_FROM_FAIZAN.md` before you leave Friday.)

---

## What Sophie does NOT need to do

- ❌ Re-deploy the dashboard. The Render service stays live throughout both phases.
- ❌ Re-train CM Champions on the dashboard. The UI doesn't change.
- ❌ Re-negotiate the password. It stays `Faizan's Claude Skill - EU WSP` unless explicitly rotated.
- ❌ Touch the Streamlit Cloud configuration. The deploy lives on Render, not Streamlit Cloud.

---

## The honest constraint

**The Streamlit dashboard solves the "fast supplier deck builds" problem.** It does not solve the "strategic supplier-marketing assistant" problem. That second problem needs Claude.

Phase 2 is about widening what CM Champions can do — not replacing what the dashboard does. The dashboard is the **defensive line** (it always works, no license needed); Claude Code is the **offensive line** (it unlocks the strategic work when licensed).

Sophie's job is to ensure the offensive line is staffed without ever putting the defensive line at risk.

---

## Pointer files

- `wayfair-eu-supplier-marketing/SKILL_INTEGRATION.md` — the composed-skill architecture Sophie inherits
- `wayfair-eu-supplier-marketing/ROADMAP.md` — the v1.1 storyboards Sophie coordinates with Faizan
- `dashboard/DATA_SAFETY.md` — the data surface Sophie extends for Phase 2
- `dashboard/BRIAN_RUNBOOK.md` — Brian's coverage doc that becomes Sophie's during transition
- `dashboard/RENDER_DEPLOY.md` — the active deploy path (Render Frankfurt EU)
- `wayfair-eu-supplier-marketing/MULTI_AGENT_DEMO.md` — the multi-agent setup Sophie demos to leadership

— Faizan, EU WSP Lead · prepared for Sophie · v0.8.0
