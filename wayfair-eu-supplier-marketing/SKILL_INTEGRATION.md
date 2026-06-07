# Skill integration — how `wayfair-supplier-pitching` composes with other skills

This plugin doesn't operate in a vacuum. It declares dependencies on, and delegates to, the following upstream skills. Every subagent in `agents/` and every storyboard in `storyboards/` operates under the combined rule set.

---

## The skill graph

```
                   ┌─────────────────────────────────────────────┐
                   │  wayfair-supplier-pitching  (this plugin)   │
                   │  · ten hard rules                            │
                   │  · seven-step workflow                       │
                   │  · TuttiBambini visual register              │
                   │  · seven named storyboards                   │
                   └────────────┬────────────────┬───────────────┘
                                │                │
                  delegates ↓   │                │   ↓ delegates
                                │                │
                ┌───────────────▼───┐    ┌──────▼───────────────┐
                │  anthropic/pptx   │    │  pptx-from-layouts   │
                │  · file I/O        │    │  · layout-name HINTs │
                │  · QA loop         │    │  · template mapping  │
                │  · design palettes │    │  · catalog-driven    │
                └───────────────────┘    └──────────────────────┘
                            ↑                       ↑
                            │                       │
                            └────── BOTH supply ────┘
                                slide-rendering primitives
```

`wayfair-supplier-pitching` owns: WHAT the deck says (the playbook). It does NOT re-implement PPTX file I/O or slide layout mechanics — it delegates those to the canonical skills.

---

## What we delegate to `anthropic/pptx`

The Anthropic skills repo ships a canonical `pptx` skill (`github.com/anthropics/skills/blob/main/skills/pptx/SKILL.md`). It is the conventional Claude Code skill for any work that touches a `.pptx` file. We compose with it rather than duplicate it.

| Concern | Source of truth |
|---|---|
| File I/O — reading existing decks, extracting text via `markitdown`, unpacking XML | `anthropic/pptx` |
| Creating new decks from scratch via `PptxGenJS` | `anthropic/pptx` |
| Editing decks via template manipulation | `anthropic/pptx` |
| **The QA loop** — "convert .pptx → PDF → JPGs → visual fresh-eyes inspect" | `anthropic/pptx` (our `wsp-deck-renderer` follows this convention) |
| **Design palette principles** — "dominance over equality, 60/30/10 colour weighting" | `anthropic/pptx` design ideas section |
| Typography pairing principles — header font with personality, clean body font | `anthropic/pptx` (Georgia + Calibri pairing is in their canonical list) |
| Anti-pattern: text-only slides with bullets | `anthropic/pptx` ("Don't create boring slides") |

What we override / specialise on top:

| Concern | Where we override |
|---|---|
| The exact visual register — TuttiBambini · Liberation Serif Bold Italic heroes · lavender + gold + deep purple + green pills | `SKILL.md` §C |
| Specific colour palette — `#7B189F / #3C1A50 / #F6EBFB / #D4A017 / #0E8F60` (locked to the Wayfair EU brand, NOT the canonical palettes from `pptx` skill) | `SKILL.md` §C |
| Storyboard-driven structure (slide count, eyebrow numbering, title patterns are NOT picked by the agent) | `storyboards/*.md` |
| Hard rules unique to supplier-facing material (no GRS, GBP only, no blame language, plain English) | `SKILL.md` §A |
| Mid-deck checkpoint enforcing analyst confirmation of closing variant | `SKILL.md` §A.3.1 |
| The 5%-of-WSC budget rule | `SKILL.md` §A.3.3 |

---

## What we delegate to `pptx-from-layouts`

Tristan McInnis's `pptx-from-layouts-skill` (`github.com/tristan-mcinnis/pptx-from-layouts-skill`) is the layout-template approach we adopted in §F of our SKILL.md. The `[HINT: layout_name]` marker pattern comes from there.

| Concern | Source of truth |
|---|---|
| Layout-by-name addressing in markdown outlines | `pptx-from-layouts` |
| Template profiling — extracting layout names from a `.pptx` master | `pptx-from-layouts` |
| The author → render handoff via tagged markdown | `pptx-from-layouts` |

What we specialise:

| Concern | Where |
|---|---|
| The fixed list of layouts our render functions implement (`deep_purple_kpi_ribbon`, `lavender_hero_left_chart_right`, `dark_days_calendar`, etc.) | `agents/wsp-deck-renderer.md` mapping table |
| Storyboard-locked layout-per-slide choices (the storyboard picks the layout, NOT the agent) | `storyboards/*.md` |

---

## How the subagents inherit this

Each of the three subagents in `agents/` has been updated so its frontmatter and body explicitly declare it operates under:

1. `wayfair-supplier-pitching` (this plugin's foundation skill)
2. `anthropic/pptx` (the canonical PPTX skill)
3. `pptx-from-layouts` (the layout-name addressing pattern)

When Claude Code loads any of these subagents, all three skills' rules apply simultaneously. The subagent's body specifies which skill owns which decision.

### Decision-ownership matrix

| Decision | `wayfair-supplier-pitching` | `anthropic/pptx` | `pptx-from-layouts` |
|---|---|---|---|
| Storyboard selection | ✅ owns | — | — |
| Variant choice (A/B/C/D) | ✅ owns | — | — |
| Visual register (TuttiBambini vs Internal MBR) | ✅ owns | — | — |
| Layout name per slide | ✅ owns (via storyboard) | — | — |
| Brand colour palette | ✅ owns (locks the EU palette) | references the design principles | — |
| Typography pairing | ✅ owns (Liberation Serif + Sans) | references the principle of "header with personality" | — |
| File I/O (saving `.pptx`) | — | ✅ owns | — |
| QA loop (.pptx → PDF → JPG → inspect) | — | ✅ owns | — |
| `[HINT: layout]` marker syntax in `slides.md` | — | — | ✅ owns |
| Layout-name → render-function mapping | ✅ owns (Wayfair-specific layouts) | — | references the pattern |
| Hard rule: no GRS in supplier-facing material | ✅ owns (Rule #1) | — | — |
| Mid-deck checkpoint enforcement | ✅ owns (Rule #9) | — | — |

---

## What this means in practice

**For a CM Champion using the dashboard**: nothing changes. They drop a CSV in, click Build, get a deck. The composed skill graph is invisible to them.

**For Faizan editing a storyboard**: the YAML frontmatter and per-slide scaffold are still the contract. Adding a new title pattern, KPI card, or layout still happens in the storyboard markdown — not in the upstream skills.

**For an engineer extending the system (e.g. adding the Restart pitch render code)**: they should:

1. Read the `restart-pitch-variant-a.md` storyboard for what the slide structure must be
2. Read `agents/wsp-deck-renderer.md` for the layout-name → function mapping
3. Read `dashboard/deck_builder.py` to see how the existing `value-review-variant-b` is implemented
4. Read `anthropic/pptx` SKILL.md for the QA loop convention
5. Implement the new render function in `deck_builder.py` following the same pattern

**For a security reviewer auditing the plugin**: this file (and the DATA_SAFETY.md) is your map. We didn't reinvent the PPTX wheel — we composed with the canonical skill and added a domain-specific layer (the playbook + the brand register + the storyboards) on top.

---

## Versioning

| Skill | Version pinned for v0.5.1 of this plugin |
|---|---|
| `wayfair-supplier-pitching` | 1.0.0 (this plugin) |
| `major-shopping-holiday-wayfair` | 1.0.0 (this plugin) |
| `anthropic/pptx` | latest from `github.com/anthropics/skills/main/skills/pptx` |
| `pptx-from-layouts` | latest from `github.com/tristan-mcinnis/pptx-from-layouts-skill` |

When upstream skills publish breaking changes, bump this file's "pinned" column and run the smoke test in `dashboard/` to confirm the renderer still produces openable .pptx files.

---

## Why this matters for the pilot

A CM Champion or Brian, asked "what skills does this depend on?", can answer in one sentence:

> *"It's three composed skills: Anthropic's canonical PPTX skill for file mechanics, Tristan McInnis's layout-from-template skill for the layout addressing pattern, and Faizan's `wayfair-supplier-pitching` skill on top for the WSP playbook + brand register + storyboards. Everything is git-versioned, every change is reviewable, and the system never invents a slide layout the storyboards didn't already define."*

That sentence is what makes this an enterprise-credible system rather than "AI builds decks."
