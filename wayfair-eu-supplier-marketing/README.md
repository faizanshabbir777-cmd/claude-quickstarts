# Wayfair EU Supplier Marketing — Claude Code Plugin

A Claude Code plugin that loads the working context, non-negotiable rules, glossary, MBR data-set schemas, and analytical frameworks used by the Wayfair EU Supplier Marketing analyst. Auto-activates whenever you start working with WSP / WSC / Castlegate / supplier pitch-deck tasks. Format follows the [Agent Skills](https://github.com/coreyhaines31/marketingskills) convention used by Corey Haines' marketingskills and the [OpenClaudia](https://github.com/OpenClaudia/openclaudia-skills) catalogue.

## What's inside

```
wayfair-eu-supplier-marketing/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── wayfair-eu-supplier-marketing/
        └── SKILL.md
```

`SKILL.md` carries:
- 🔴 Non-negotiable rules (no GRS on supplier-facing material, Wholesale ROAS only, Evergreen ≠ Priority)
- 📖 Full Wayfair glossary
- 📊 MBR SET 1 / 2 / 3 + portfolio table schemas + Way Day share-shift
- 🧮 Data cleaning checklist
- 🎯 Five analytical frameworks (ROAS gap reframe, WSC correlation, cap-hit, 5%-of-WSC budget, portfolio prioritisation)
- 📐 .pptx output standards + EU purple brand palette
- 🗣️ Working style + persistent context doc convention (`.agents/wayfair-supplier-context.md`)

## Install

### Option A — Claude Code plugin (recommended)

From any Claude Code session:

```
/plugin install ./wayfair-eu-supplier-marketing
```

Or, after this branch is merged, install directly from GitHub:

```
/plugin install faizanshabbir777-cmd/claude-quickstarts/wayfair-eu-supplier-marketing
```

(`/plugin` syntax may vary by Claude Code version — see the Claude Code plugin docs.)

### Option B — Personal skill (no plugin manager)

```bash
mkdir -p ~/.claude/skills
cp -r wayfair-eu-supplier-marketing/skills/wayfair-eu-supplier-marketing \
      ~/.claude/skills/
```

Start a new Claude Code session — the skill will be auto-discovered.

### Option C — Project-level

Commit the skill into a specific repo so everyone working there gets it:

```bash
mkdir -p .claude/skills
cp -r /path/to/wayfair-eu-supplier-marketing/skills/wayfair-eu-supplier-marketing \
      .claude/skills/
git add .claude/skills && git commit -m "Add Wayfair EU supplier marketing skill"
```

### Option D — claude.ai Projects (web app)

Skills only auto-load in Claude Code. For the claude.ai web app, paste the contents of `skills/wayfair-eu-supplier-marketing/SKILL.md` (everything below the YAML frontmatter) into a Claude Project's custom instructions / project knowledge panel.

## How activation works

The skill's YAML `description` lists trigger phrases — anything containing WSP, MWSP, WSC, GRS, Wholesale ROAS, Castlegate, CG penetration, cap-hit, Way Day, MBR SET 1/2/3, the campaign codes RE / VE / OE / OU, or supplier-summit pitch-deck language will auto-pull it in. You can also force-load with `/wayfair-eu-supplier-marketing`.

## Persistent supplier context

For projects lasting longer than one session, drop a `.agents/wayfair-supplier-context.md` next to the work — the skill checks for it on entry and won't re-ask facts already captured there. Suggested sections: suppliers in scope (name, SuID, SRM, category, WSC band), currency convention, latest landed-month WSC per supplier, known data caveats, open pitches and their evidence pillars.

## Updating

Edit `skills/wayfair-eu-supplier-marketing/SKILL.md`, bump `metadata.version` in the frontmatter and `version` in `plugin.json`, then re-install / re-copy. Keep the `description:` trigger keywords current as the analyst's workflow evolves.
