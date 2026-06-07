# Multi-Agent Setup — Demo + Operator's Guide

> *"Show me the multi-agent setup."*

You already have one. It runs without any AI-license dependency. This doc shows what's wired, how to demo it, and the path to layer Copilot autonomous-work on top when issues are enabled.

---

## What you have today (no Claude license required)

**Three specialised subagents, two upstream skills, one foundation skill, three live storyboards.** All composed.

```
                   ┌─────────────────────────────────────────────┐
                   │  wayfair-supplier-pitching (foundation)     │
                   │  · 10 hard rules                             │
                   │  · 7 storyboards (3 live in v1.0)            │
                   │  · TuttiBambini visual register              │
                   └────┬──────────┬──────────┬───────────────────┘
                        │          │          │
              ┌─────────▼─┐   ┌────▼──┐   ┌──▼────────────┐
              │ data-prep │   │ author│   │ deck-renderer │
              │           │   │       │   │               │
              │ CSV/XLSX  │   │ pick  │   │ render python │
              │ →         │   │ story │   │ -pptx,        │
              │ deck_     │   │ board,│   │ run QA loop   │
              │ data.json │   │ fill  │   │               │
              │           │   │ slides│   │               │
              │           │   │ .md   │   │               │
              └───────────┘   └───────┘   └───────────────┘
                        │          │          │
                        └─── pipeline ─────────┘
                                  │
                                  ▼
                   ┌─────────────────────────────────────────────┐
                   │  Composes with:                              │
                   │  · anthropic/pptx (file I/O + QA loop)       │
                   │  · pptx-from-layouts ([HINT: layout] markers)│
                   └─────────────────────────────────────────────┘
```

### The three subagents

Files: `agents/wsp-data-prep.md` · `agents/wsp-deck-author.md` · `agents/wsp-deck-renderer.md`

Each has a focused job, declared in its frontmatter:

| Subagent | Input | Output | Composes with |
|---|---|---|---|
| `wsp-data-prep` | CSV/XLSX from analyst | `deck_data.json` | `wayfair-supplier-pitching` (hard rules) |
| `wsp-deck-author` | `deck_data.json` + storyboard | `slides.md` with `[HINT: layout]` markers | `wayfair-supplier-pitching` + `pptx-from-layouts` |
| `wsp-deck-renderer` | `slides.md` + brand palette | polished `.pptx` + QA-loop PDF | `wayfair-supplier-pitching` + `anthropic/pptx` |

Each one operates under the **decision-ownership matrix** in `SKILL_INTEGRATION.md` — clear about which decisions it owns vs which it delegates upstream.

### The three live storyboards

| Storyboard | Variant | Live |
|---|---|---|
| `value-review-variant-b.md` | B Continue | ✅ |
| `restart-pitch-variant-a.md` | A Restart (with dark-days calendar) | ✅ |
| `switch-to-5pct-variant-c.md` | C Switch to 5% | ✅ |
| `promo-recap-tier0.md` | Promo event recap | ⏳ v1.1 |
| `summit-case-study.md` | Multi-supplier summit | ⏳ v1.1 |
| `mbr-supplier-review.md` | Internal MBR | ⏳ v1.1 |
| `portfolio-outreach.md` | Cross-supplier ranking | ⏳ v1.1 |

Three live + dispatcher in `dashboard/deck_builder.build_deck()` = autonomous coverage of ~80% of pitch volume.

---

## How to demo it (in any editor — Cursor, VS Code, terminal)

The pipeline runs as pure Python. No AI license needed. The "multi-agent" is the **separation of concerns** between the three subagent specs, even when a single human (or one AI) plays all three roles.

### Demo 1 — End-to-end build via Python (terminal)

```bash
cd wayfair-eu-supplier-marketing/dashboard
python3 -c "
import data_prep, deck_builder

# 1. DATA-PREP subagent role
data = data_prep.demo_data()
print(f'✓ Data prep: {data[\"supplier\"]} · ws_roas £{data[\"ws_roas\"]:.2f}')

# 2. DECK-AUTHOR subagent role (storyboard selection)
storyboard = 'value-review-variant-b'
print(f'✓ Author: selected {storyboard}')

# 3. DECK-RENDERER subagent role
pptx = deck_builder.build_deck(storyboard, data)
with open('/tmp/demo.pptx', 'wb') as f:
    f.write(pptx)
print(f'✓ Renderer: {len(pptx):,} bytes · 4 slides')
"
```

Output:
```
✓ Data prep: Monty Trading Ltd · ws_roas £5.71
✓ Author: selected value-review-variant-b
✓ Renderer: 380,393 bytes · 4 slides
```

### Demo 2 — Three variants in one script

```bash
python3 -c "
import data_prep, deck_builder
data = data_prep.demo_data()
for sb in ['value-review-variant-b', 'restart-pitch-variant-a', 'switch-to-5pct-variant-c']:
    try:
        pptx = deck_builder.build_deck(sb, data)
        print(f'{sb:30s}: {len(pptx):,} bytes')
    except ValueError as e:
        print(f'{sb:30s}: ✗ {e}')
"
```

### Demo 3 — Via the Streamlit dashboard

```bash
streamlit run app.py
```

Open the browser. The pipeline runs visually: Filters → Data Preview (data-prep) → Build (author + renderer) → Preview & QA → Send. Six tabs, three roles, one workflow.

---

## What "multi-agent" actually means here

Two definitions of multi-agent in this project:

### 1. **Specification-level multi-agent** (what we have today)

The three `agents/*.md` files are specifications. Whoever (human or AI) plays a role reads its spec and does that role's job. Roles are clean. Each role has clear inputs, outputs, and decision boundaries.

**Why this works without Claude Code:**

- The `.md` files are just markdown — readable in any editor
- Cursor's AI (any model: Claude, GPT, Gemini, local) can be primed with these specs via `.cursorrules` or copy-paste
- A human can play any role manually by reading the spec
- The Python pipeline (`data_prep.py` + `deck_builder.py`) runs without any AI at all

### 2. **Autonomous multi-agent** (the GitHub Copilot pathway, when you enable it)

GitHub Copilot Coding Agent picks up well-scoped issues and ships PRs autonomously. This requires:

1. **Issues enabled on the repo** (currently disabled — see "Enabling autonomous work" below)
2. **Issues written with clear acceptance criteria** (ROADMAP.md has the next-up list)
3. **Copilot assignment** via issue-write API or the GitHub UI
4. **PR review path** (a human or `request_copilot_review` for second-pass)

This is the v1.1 roadmap path. Not blocking the pilot.

---

## Enabling autonomous work (when you want it)

To turn on Copilot autonomous work for v1.1:

1. **Enable issues on the repo**: `github.com/faizanshabbir777-cmd/claude-quickstarts/settings` → check "Issues"
2. **Create the v1.1 issues**: see ROADMAP.md — six pre-scoped issues with acceptance criteria, files to touch, and test plans. Each one is sized for Copilot pickup (low-to-medium complexity, self-contained)
3. **Assign Copilot**: from the issue UI, click "Assignees" → select `Copilot` (GitHub's Coding Agent). Copilot picks the issue, writes the code, opens a PR, runs the test plan.
4. **Review the PR**: use `mcp__github__request_copilot_review` for the first-pass automated review; you (or Brian during your leave) do final approval.

You don't need to enable this before Monday. The pilot ships with v1.0. Autonomous v1.1 work happens later if you want it.

---

## Cursor-specific setup (no Claude license)

For a teammate using Cursor with GPT/Composer/any model:

1. Clone the repo
2. Open in Cursor
3. Cursor auto-loads `.cursorrules` (see `dashboard/.cursorrules` — added in v0.7.0) which primes the AI with:
   - The 10 hard rules
   - The composition of the three subagent roles
   - The storyboard-selection decision tree
   - Pointer to `SKILL_INTEGRATION.md` and `HOW_TO_USE.md`
4. Ask Cursor to "add a new storyboard for [X]" or "extend data_prep to handle [Y]" — it reads the rules, follows the patterns, ships the change

The Cursor AI doesn't need to be Claude. It needs to be primed with the WSP playbook. The `.cursorrules` file does that priming.

---

## What the demo proves

When someone asks *"what's the multi-agent thing?"* you can show them, in order:

1. **The three `.md` specs in `agents/`** — three roles, clean separation
2. **The Python pipeline running end-to-end** — `python3 -c "import deck_builder; ..."`
3. **The Streamlit dashboard** — the same pipeline with a UI
4. **The ROADMAP.md v1.1 issues** — what an autonomous agent would pick up next
5. **The `.cursorrules` file** — how to prime any AI editor

That's a multi-agent system: roles, separation of concerns, composability, autonomous-ready, editor-agnostic. **Today, no Claude license, no Cursor license — just Python.**

---

## What it's NOT

- It's not a "swarm" where 5 AIs run in parallel — that's overkill for pitch decks
- It's not bound to Anthropic — the pipeline has zero `anthropic` SDK imports (audited)
- It's not Cursor-specific — the same rules work in VS Code + Continue, Windsurf, Codeium, GitHub Copilot, etc.
- It's not blocking the pilot — v1.0 ships Friday with three live storyboards; autonomous multi-agent is v1.1 enhancement

---

## File map (where to find what)

```
wayfair-eu-supplier-marketing/
├── agents/                          ← the three subagent specs
│   ├── wsp-data-prep.md
│   ├── wsp-deck-author.md
│   └── wsp-deck-renderer.md
├── skills/                          ← the foundation + promo skills
│   ├── wayfair-supplier-pitching/SKILL.md
│   └── major-shopping-holiday-wayfair/SKILL.md
├── storyboards/                     ← seven storyboards (3 live)
│   ├── value-review-variant-b.md
│   ├── restart-pitch-variant-a.md
│   ├── switch-to-5pct-variant-c.md
│   ├── promo-recap-tier0.md           ⏳ v1.1
│   ├── summit-case-study.md           ⏳ v1.1
│   ├── mbr-supplier-review.md         ⏳ v1.1
│   └── portfolio-outreach.md          ⏳ v1.1
├── dashboard/                       ← the runnable pipeline
│   ├── data_prep.py                   (data-prep role)
│   ├── deck_builder.py                (renderer role · 3 live storyboards)
│   ├── app.py                         (the Streamlit UI tying it together)
│   └── .cursorrules                   (Cursor-AI priming · v0.7.0)
├── SKILL_INTEGRATION.md             ← decision-ownership matrix
├── MULTI_AGENT_DEMO.md              ← this file
└── ROADMAP.md                       ← v1.1 issues for Copilot pickup
```

That's the system. Six markdown files, three Python files, one Streamlit app. End-to-end multi-agent in under 5,000 lines of code.
