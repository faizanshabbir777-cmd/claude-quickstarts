# How to use the WSP skill — operator's manual

A practical guide. No abstract architecture. Just the commands, the mental model, and the gotchas.

---

## Mental model (read this first)

You are not driving the AI. **The playbook is driving the AI.** Your job is to:

1. **State the brief** (one sentence)
2. **Answer four kickoff questions** when asked
3. **Pick the closing variant** at the mid-deck checkpoint
4. **Open the .pptx** when it lands

The skill picks a storyboard from `storyboards/selector.md`, fills the scaffold with your data, and renders. You do not negotiate slide count, eyebrow numbering, layout, or title with the AI. The storyboard already decided.

If the brief doesn't fit a storyboard cleanly, the skill **asks before building**. It does not silently pick "close enough."

---

## 5-minute setup (one-time)

On your local Mac:

```bash
# 1. Clone the repo
git clone https://github.com/faizanshabbir777-cmd/claude-quickstarts.git
cd claude-quickstarts

# 2. Install the plugin
claude-code /plugin install ./wayfair-eu-supplier-marketing

# 3. Copy the subagents into Claude Code's agent dir
mkdir -p ~/.claude/agents
cp wayfair-eu-supplier-marketing/agents/*.md ~/.claude/agents/

# 4. Install the Python deps
pip install python-pptx pandas openpyxl lxml matplotlib pydantic

# 5. Install LibreOffice for the QA loop (one-time)
brew install --cask libreoffice
brew install poppler

# 6. Verify
which libreoffice pdftoppm
claude-code /plugin list   # should show wayfair-eu-supplier-marketing v0.4.0
```

---

## The 4 prompts you will use 80% of the time

### Prompt 1 — Value review (Variant B Continue)

When the supplier is at or above 4–5% benchmark and the ask is "keep doing what you're doing":

```
/wsp {Supplier} UK · WSP value review · {month}
Storyboard: value-review-variant-b
Files in ./data/
```

The skill will:
- Ask: supplier name + SuID + currency + audience + which files
- Read the data, compute the metrics, write `deck_data.json`
- Build slides 1–3, post a data summary in chat
- Mid-deck checkpoint: ask you to confirm Variant B
- Render slide 4 (The Ask)
- Run the QA loop
- Drop the .pptx in `./outputs/`

Example: `/wsp Monty Trading UK · WSP value review · April 2026`

### Prompt 2 — Restart pitch (Variant A — supplier went dark)

When the supplier has been dark ≥2 months and the ask is "switch back on":

```
/wsp {Supplier} UK · restart pitch · post-{event}
Storyboard: restart-pitch-variant-a
Files in ./data/
```

The skill will use the **TuttiBambini storyboard** — same 6-slide structure as your Way Day deck for Tapanshi. The dark-days calendar visualisation gets generated automatically from the daily WSP status data.

Example: `/wsp UKGFW restart pitch — dark since November`

### Prompt 3 — Switch to 5% rule (Variant C — under-spender)

When the supplier is active but under-spending or erratic:

```
/wsp {Supplier} UK · switch to 5% · {month}
Storyboard: switch-to-5pct-variant-c
Files in ./data/
```

Example: `/wsp UKShireSheds switch to 5% rule — running at 0.9% intensity`

### Prompt 4 — Promo recap (Variant B/C — after Way Day, BFCM, etc.)

```
/wsp {Supplier} {Event} {Year} recap
Storyboard: promo-recap-tier0
Promo window: {start} to {end}
Pre-period: {start} to {end}
Files in ./data/
```

**Important:** the skill will refuse to proceed without exact dates. Rule #8 is enforced — never inferred from filenames.

Example:
```
/wsp Forte UK · Way Day 2026 recap
Promo: 25–27 April 2026
Pre-period: 28–30 March 2026
```

---

## Decision tree — which storyboard for what I want

| I want to... | Storyboard | Notes |
|---|---|---|
| Celebrate a supplier already at benchmark | `value-review-variant-b` | Monty pattern |
| Convince a dark supplier to come back | `restart-pitch-variant-a` | TuttiBambini pattern |
| Fix lumpy / under-budget spend | `switch-to-5pct-variant-c` | Most common variant |
| Recap a Tier-0 promo event | `promo-recap-tier0` | Requires exact dates |
| Build a multi-supplier showcase | `summit-case-study` | Numbers stripped |
| Produce the internal monthly MBR | `mbr-supplier-review` | Internal register, GRS allowed |
| Rank suppliers for outreach this week | `portfolio-outreach` | Output is a list, not a deck |

If none of these fit cleanly, the skill will propose a custom storyboard for you to confirm before building.

---

## The kickoff questions you'll always answer

The skill asks the same four things at the start of every deck build:

1. **Supplier name + Supplier ID**
   Example: `Monty Trading Ltd (SuID 37802)`

2. **Time window**
   Example: `April 2026 headline, 12-month trajectory`. For promos: exact promo dates AND matched pre-period dates.

3. **Currency confirmation**
   Default: GBP at 1:1 from USD. Confirm unless something is different.

4. **Audience**
   Supplier-facing (Monty C-suite) → TuttiBambini register, no GRS.
   Internal (Wayfair leadership) → internal MBR register, GRS allowed.

Answer all four in one message. The skill won't proceed until they're locked in.

---

## The mid-deck checkpoint (the one moment you make a real decision)

After slides 1–3 are built, the skill stops and asks:

```
Data summary (4–6 bullets):
  · {key metric 1}
  · {key metric 2}
  · ...

Recommended path: Variant {A/B/C/D}
Why: {one-sentence reason}

Pick a closing variant:
  A · Restart   B · Continue   C · Switch to 5%   D · Custom
```

Reply with one letter: `B`. The skill renders the closing slide and ships.

The skill **never auto-commits the variant**. This is enforced — the £-rule is too important to autopilot.

---

## Common errors + how to fix them

### "Plugin not found"
You forgot step 2 of setup, or you're in the wrong directory. Run from the repo root: `claude-code /plugin install ./wayfair-eu-supplier-marketing`.

### "Skill not auto-activating when I type WSP"
Type `/wsp` explicitly to force-load. If that works but natural prompts don't, the description's trigger phrases aren't matching — open an issue.

### "LibreOffice not found — QA loop skipped"
Install LibreOffice (step 5 of setup). The deck builds without it, but you lose the visual QA. On a fresh Mac install it took me 6 minutes. Do it once.

### "It's using GRS in a supplier-facing slide"
This should be impossible by design. If it happens, file an issue — rule #1 has a hole. Use a different prompt while it's investigated.

### "The output looks like generic AI"
Two causes:
1. The agent ignored the storyboard and invented structure — re-run with `Storyboard: {name}` in the prompt explicitly
2. Liberation Serif rendering on a non-Mac box — open the .pptx on macOS with Georgia installed and it'll snap to the TuttiBambini look

### "I want to override the title — none of the examples fit"
The skill will surface this in chat:
```
Slide 3 — none of the storyboard's title examples fit. Proposed alternative: "..."
Confirm or override before I render.
```
Reply with your own sentence. The skill will use it.

### "The deck is taking >5 minutes to build"
Normal for the first build after a fresh install (LibreOffice is slow on first launch). Subsequent builds are 60–90 seconds.

---

## What to do next (your first three deck builds)

1. **Build the Monty deck** to confirm install works end-to-end:
   ```
   /wsp Monty Trading UK · WSP value review · April 2026
   ```
2. **Build a real new pitch** for the supplier you care about most this week. Use whichever storyboard matches.
3. **Build a Restart pitch** for a dark supplier — this exercises the dark-days calendar, which is the killer visual.

By the end of those three builds you'll know the workflow cold.

---

## How to extend the skill

If you find a pattern that should be enforced (new pitch variant, new event type, brand rule update):

1. Edit the relevant `storyboards/*.md` or `SKILL.md`
2. Bump `metadata.version` in the YAML frontmatter
3. Bump `version` in `.claude-plugin/plugin.json`
4. Commit, push, send a PR

The playbook is now a versioned, reviewable artefact. Treat changes like code changes — the team can review them.
