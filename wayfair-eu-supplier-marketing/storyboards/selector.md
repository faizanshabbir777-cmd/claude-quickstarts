# Storyboard selector — which storyboard for which brief

The selector is a decision tree. The agent runs it BEFORE building anything. If the brief doesn't fit cleanly, the agent asks the analyst rather than picking the closest match by default.

## Decision tree

```
Q1: Is the brief about a single event (promo, sale, holiday)?
  YES → Q1a: Are exact promo dates AND matched pre-period dates known?
    YES → promo-recap-tier0.md
    NO  → ASK ANALYST FOR DATES, then promo-recap-tier0.md
  NO  → Q2

Q2: Is the brief multi-supplier (a summit, an industry event, a panel)?
  YES → summit-case-study.md
  NO  → Q3

Q3: Is the ask a portfolio-level prioritisation ("who do I pitch first")?
  YES → portfolio-outreach.md (outputs a ranked list, not a deck)
  NO  → Q4

Q4: Is the supplier currently DARK (no WSP spend in the last 2+ months
     OR last-month spend < 10% of trailing-6-month average)?
  YES → restart-pitch-variant-a.md
  NO  → Q5

Q5: Is the supplier ACTIVE but UNDER-SPENDING (intensity < 3% of WSC,
     OR MoM spend swings > 50% with stable WSC)?
  YES → switch-to-5pct-variant-c.md
  NO  → Q6

Q6: Is the supplier AT/ABOVE benchmark (intensity ≥ 4% of WSC, ROAS holding,
     spend consistent)?
  YES → value-review-variant-b.md
  NO  → Q7

Q7: Does the brief mention "MBR", "monthly business review", or follow a
     recurring monthly cadence?
  YES → mbr-supplier-review.md
  NO  → ASK ANALYST — no clean match
```

## What the agent says when it picks

After running the selector, the agent announces which storyboard it picked and why, before building. Format:

```
Storyboard: {name}.md
Why: {brief reason citing the rule that matched}
Slide count: {N}
Slides: 1·{cover description} · 2·{slide 2 eyebrow} · ... · N·{closing eyebrow}
Required data I have: ✓ all present | ✗ missing: [field, field]
Proceeding to Stage 1 build.
```

If required data is missing, the agent asks before building — same kickoff-question rule from `SKILL.md §A`.

## What the agent NEVER does

- Pick a storyboard "close to" the brief without saying so
- Invent a slide that isn't in the storyboard
- Skip a slide that the storyboard requires
- Change the eyebrow numbering
- Override the title pattern with prose

If the brief genuinely doesn't fit any storyboard, the agent surfaces a custom storyboard proposal to the analyst (slide count, slide list, layouts per slide) and asks for confirmation before building.
