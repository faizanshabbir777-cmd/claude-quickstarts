# Wayfair EU Supplier Marketing — Claude Code Plugin

A Claude Code plugin that loads the working context, rules, glossary, data-set
schemas, and analytical frameworks used by the Wayfair EU Supplier Marketing
analyst. Once installed, Claude will automatically apply the rules (e.g. "never
show GRS to suppliers", "use Wholesale ROAS in supplier-facing decks") in any
session where you start working with WSP / WSC / Castlegate / pitch-deck tasks.

## What's inside

```
wayfair-eu-supplier-marketing/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── wayfair-eu-supplier-marketing/
        └── SKILL.md   ← all the rules, glossary, frameworks, output standards
```

The skill auto-activates on relevant context (WSP data, MBR SET 1/2/3, supplier
pitch decks, ROAS / WSC / Castlegate / cap-hit analysis, Way Day, etc.). You
can also invoke it explicitly with `/wayfair-eu-supplier-marketing` once
installed.

## Install — Option A: as a personal skill (simplest)

If you just want it in your own Claude Code sessions, copy the skill into your
user-level skills directory:

```bash
mkdir -p ~/.claude/skills
cp -r wayfair-eu-supplier-marketing/skills/wayfair-eu-supplier-marketing \
      ~/.claude/skills/
```

Then start a new Claude Code session — the skill will be auto-discovered.

## Install — Option B: as a plugin (shareable)

Plugins can be installed from a local path or a git repository. From this
repo's root:

```bash
# Inside any Claude Code session
/plugin install ./wayfair-eu-supplier-marketing
```

Or, after pushing this branch / merging to main, install directly from GitHub:

```bash
/plugin install faizanshabbir777-cmd/claude-quickstarts/wayfair-eu-supplier-marketing
```

(Exact `/plugin` syntax may evolve — see the Claude Code plugin docs for the
current command.)

## Install — Option C: project-level

To make this skill auto-load for everyone working in a specific repo, copy it
into that repo's `.claude/skills/` directory and commit it:

```bash
mkdir -p .claude/skills
cp -r /path/to/wayfair-eu-supplier-marketing/skills/wayfair-eu-supplier-marketing \
      .claude/skills/
git add .claude/skills && git commit -m "Add Wayfair EU supplier marketing skill"
```

## Using it in claude.ai (Projects)

If you also want this context in claude.ai chat (not just Claude Code), paste
the contents of `skills/wayfair-eu-supplier-marketing/SKILL.md` (minus the YAML
frontmatter) into a Claude Project's "Custom Instructions" or "Project
Knowledge" panel.

## Updating

Edit `skills/wayfair-eu-supplier-marketing/SKILL.md` and re-install / re-copy.
The `description:` field in the YAML frontmatter is what tells Claude when to
auto-activate the skill — keep the trigger keywords there current as the
analyst's workflow evolves.
