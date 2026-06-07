# WSP Pitch Builder · dashboard

The Streamlit app + pipeline that lets CM Champions ship supplier pitch decks without writing Python.

## Quick links

- **Deploy guide (3 min):** [RENDER_DEPLOY.md](./RENDER_DEPLOY.md) ← active path
- **Operator's manual:** [../HOW_TO_USE.md](../HOW_TO_USE.md)
- **Data safety:** [DATA_SAFETY.md](./DATA_SAFETY.md)
- **Brian runbook (during leave):** [BRIAN_RUNBOOK.md](./BRIAN_RUNBOOK.md)
- **Sophie transition plan (Phase 1 → 2):** [SOPHIE_TRANSITION_PLAN.md](./SOPHIE_TRANSITION_PLAN.md)
- **Multi-agent demo:** [../MULTI_AGENT_DEMO.md](../MULTI_AGENT_DEMO.md)

## What this is

A Streamlit web app + Python pipeline (`data_prep.py` + `deck_builder.py`) that produces personalised supplier pitch decks in the TuttiBambini visual register.

Three storyboards live in v1.0:
- `value-review-variant-b` (Monty pattern)
- `restart-pitch-variant-a` (TuttiBambini pattern with dark-days calendar)
- `switch-to-5pct-variant-c` (under-spender pattern)

Audit-confirmed **zero Claude / Anthropic API dependencies** in the runtime. The pipeline runs on any Python 3.10+ environment.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Opens `http://localhost:8501`. Default password: `Faizan's Claude Skill - EU WSP`.

## Deploy to Render (3 min)

The active deploy path. Free tier, 750 hrs/mo, Frankfurt EU region, auto-deploys from `main`.

```
Render → New → Blueprint → paste:
https://github.com/faizanshabbir777-cmd/claude-quickstarts
```

Render auto-detects `dashboard/render.yaml`. Set the `WSP_PASSWORD` env var, click Apply, URL goes live in ~90 seconds.

Full step-by-step in [RENDER_DEPLOY.md](./RENDER_DEPLOY.md).

## File layout

```
dashboard/
├── app.py                       Streamlit UI (6 tabs)
├── data_prep.py                 CSV/XLSX parser + metric computation
├── deck_builder.py              Slide renderers + dispatcher (3 live storyboards)
├── requirements.txt             pip dependencies
├── render.yaml                  Render Blueprint (declarative deploy)
├── Dockerfile                   Container build (for Cloud Run / Fly.io / internal K8s)
├── RENDER_DEPLOY.md             3-min deploy guide (active path)
├── DEPLOY.md                    All deploy alternatives (Streamlit Cloud, K8s, Docker, etc.)
├── DATA_SAFETY.md               Full safety doc for IT/security review
├── Leadership_Data_Safety_Memo.pdf  1-page for Clement forwarding
├── BRIAN_RUNBOOK.md             What to do if anything breaks during Faizan's leave
├── SOPHIE_TRANSITION_PLAN.md    Phase 1 → 2 transition map for Sophie
├── SOPHIE_HANDOFF_FROM_FAIZAN.md  Pre-leave checklist Faizan fills in
├── EMAILS.md                    Send-order drafts (Brian, Clement, EURTA NART)
├── .streamlit/
│   ├── config.toml              InfoHub-matching magenta theme
│   └── secrets.toml.example     Local secrets template
├── .cursorrules                 Primes any AI editor (Cursor, Copilot, etc.) with WSP rules
├── assets/                      Slide preview PNGs + Wayfair logo
└── demo/                        5 pre-built example decks
```

## Three subagent roles

The pipeline mirrors the multi-agent spec in `../agents/`:

- `wsp-data-prep` (= `data_prep.py`) — ingest CSV/XLSX, compute metrics
- `wsp-deck-author` (= storyboard logic in `deck_builder.build_deck()`) — pick storyboard, fill scaffold
- `wsp-deck-renderer` (= render functions + python-pptx) — produce .pptx

Each role's spec is in `../agents/wsp-*.md`. They're readable in Cursor, GitHub Copilot, VS Code with Continue, Windsurf — any AI editor — via the `.cursorrules` priming.

## Hard rules (enforced in code)

1. No GRS in supplier-facing material (Rule #1)
2. GBP at 1:1 from USD
3. pt not bps for share shifts
4. No blame language
5. Plain English on every analytical slide
6. Closing slide never auto-builds (mid-deck checkpoint)

Full rules in `../skills/wayfair-supplier-pitching/SKILL.md`.

## Status

| | State |
|---|---|
| Three storyboards live (B / A / C) | ✅ |
| Real personalised pptx from uploaded CSV | ✅ |
| Render Blueprint ready | ✅ |
| Dockerfile ready (Cloud Run / Fly.io / K8s) | ✅ |
| Audit-confirmed zero Claude deps | ✅ |
| Brian's coverage runbook | ✅ |
| Sophie's Phase 1→2 transition plan | ✅ |
| Plugin v0.7.0 merged to main | ✅ |
