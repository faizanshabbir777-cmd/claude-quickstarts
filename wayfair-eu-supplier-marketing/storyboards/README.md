# Storyboard Index — WSP deck patterns

This directory holds the **base-level storyboards** that every WSP deck builds from. The agent picks one based on the brief, fills in the data, and renders. **Slide count, slide order, eyebrow numbering, layout per slide, and title patterns are fixed by the storyboard** — the agent does not invent structure.

This is what stops the decks from drifting off-script.

## How storyboards compose with upstream skills

Storyboards sit inside the `wayfair-supplier-pitching` skill but actively reference two upstream skills via their `[HINT: layout_name]` markers and visual-element principles:

- **`anthropic/pptx`** — supplies design ideas (don't make boring text-only slides, every slide needs a visual element, pick a bold colour palette and dominate-not-equal weighting). Our storyboards apply this: every slide-scaffold mandates a chart, card, hero number, or visual structure — never bullet-list-only slides.
- **`pptx-from-layouts`** — supplies the `[HINT: layout_name]` marker convention. Each slide-scaffold in our storyboards declares a `LAYOUT:` field which becomes the `[HINT:]` marker in the author's `slides.md` output, which the renderer maps to its concrete layout function.

See `../SKILL_INTEGRATION.md` for the full decision-ownership matrix.

## Pattern

Every storyboard is a markdown file with:

1. **YAML frontmatter** — name, when-to-use rules, slide count, required data fields, ask variant
2. **Per-slide scaffold** — `LAYOUT:`, `EYEBROW:`, `TITLE_PATTERN:`, `TITLE_EXAMPLES:`, element list, takeaway pattern
3. **Reference link** to the TuttiBambini baseline slide each pattern mirrors

When the agent receives a brief, it:

1. Reads `selector.md` (which storyboard for which brief)
2. Loads the storyboard markdown for the selected variant
3. Validates required data is present (asks the analyst if not)
4. Fills the scaffold from `deck_data.json`
5. Renders with python-pptx using the visual conventions in `SKILL.md §C`
6. Runs the QA loop

## Storyboards in this directory

| File | Use when |
|---|---|
| `value-review-variant-b.md` | Supplier is at or above the 4–5% benchmark; the ask is "continue at this pace". Monty Trading is the canonical example. |
| `restart-pitch-variant-a.md` | Supplier has been dark ≥2 months; the ask is "switch WSP back on". TuttiBambini is the canonical example — uses the dark-days calendar visualisation. |
| `switch-to-5pct-variant-c.md` | Supplier is active but under-spending (<3% of WSC), or spend is erratic. The ask is "lock in the 5% rule". |
| `promo-recap-tier0.md` | Way Day, Black Friday, Cyber Week, BFCM, Boxing Day, etc. Requires exact promo dates AND matched pre-period dates. |
| `mbr-supplier-review.md` | Recurring monthly business review. Formal, data-back, tabular register (mirrors the March '26 MBR template). |
| `summit-case-study.md` | Multi-supplier showcase for the EU Supplier Summit or similar public audiences. Numbers stripped, supplier names visible. |
| `portfolio-outreach.md` | Cross-supplier prioritisation — "who do I pitch first this month?" Outputs a ranked list, not a deck. |

## Selector

See `selector.md` for the routing logic — which storyboard fits which incoming brief.

## Adding a new storyboard

When a new pitch pattern recurs (a new variant, a new event type), add a new storyboard file here. Bump the skill `metadata.version` and `plugin.json` version. The playbook is now versioned — treat additions like code changes.
