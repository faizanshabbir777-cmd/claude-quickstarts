# Quickstart — WSP analyst in a box

Get from `git clone` to a built supplier pitch deck in under 10 minutes.

---

## 1. Install

```bash
# Clone the repo (only needed once)
git clone https://github.com/faizanshabbir777-cmd/claude-quickstarts.git
cd claude-quickstarts

# Install the plugin into Claude Code
claude-code /plugin install ./wayfair-eu-supplier-marketing

# Confirm it's there
claude-code /plugin list
# You should see: wayfair-eu-supplier-marketing  v0.3.0
```

You also need these on your machine for the QA loop:

```bash
pip install python-pptx pandas openpyxl lxml matplotlib

# macOS
brew install libreoffice poppler

# Ubuntu / Debian / WSL
sudo apt-get install libreoffice poppler-utils
```

Verify the tools are on your PATH:

```bash
which libreoffice pdftoppm
```

If either is missing, the deck will still build but the visual QA loop (rule #10) won't run.

---

## 2. First use

In any terminal, `cd` into your working folder (suggested: `~/wayfair-work/`). Drop your supplier data into `./data/`. Then:

```bash
claude-code
```

In the Claude Code session, type:

```
/wsp Monty Trading UK · WSP value review · April 2026 · supplier-facing
```

Claude will ask **four kickoff questions** before doing anything:

1. Supplier name + Supplier ID
2. Time window (for promos, exact promo dates AND matched pre-period)
3. Currency confirmation (default GBP at 1:1 from USD)
4. Which files you have for it

Answer them in one message. Claude will:

- Read the data
- Compute the 12-month build, WS ROAS, WSP intensity
- Build the cover + analysis slides
- **Pause at the mid-deck checkpoint** — present a data summary and ask you to pick a closing variant (A Restart / B Continue / C Switch to 5% / D Custom)
- Build the closing slide
- Run the QA loop (deck → PDF → JPGs → visual inspect)
- Save the deck to `./outputs/{Supplier}_{Period}_WSP_Deck.pptx`

---

## 3. Example output

The plugin has been tested end-to-end on:

| Supplier | Brief | Output | Time |
|---|---|---|---|
| **Forte UK** | March '26 MBR-format performance review | 3-slide MBR-style deck with em-dash titles, KPI tiles, READ-OUT strips, Annual Scorecard | 4 min |
| **Forte + Monty** | Supplier-summit case study, numbers stripped, audience = Niraj + supplier C-suite | 3-slide unified deck (Forte trends / Monty trends / shared playbook + CTA) | 6 min |
| **Monty Trading** | April '26 WSP value review, Variant B Continue | 3-slide deck (Cover/KPIs · Three pillars + trajectory · The Ask) | 3 min |

Each was built supplier-safe — WSC only, no GRS, GBP at 1:1, plain-English footer on every analytical slide.

See `/tmp/forte_deck/Monty_Trading_April2026_WSP_Deck.pdf` (or your own first deck) for what the output looks like.

---

## 4. Troubleshooting

### "Plugin not found"
Make sure you ran `/plugin install` from the repo root and that `.claude-plugin/plugin.json` exists in the `wayfair-eu-supplier-marketing/` directory.

### "Skill not auto-activating"
Two ways to force-load:
1. Type `/wsp` to invoke the slash command directly
2. Mention any of the skill's trigger phrases (WSP, WSC, GRS, Castlegate, MBR, Way Day, etc.) and the skill will activate

### "QA loop fails — `libreoffice not found`"
Install LibreOffice (see step 1). The deck still builds without it; you just won't get the visual JPG render. You can convert to PDF manually with Keynote/PowerPoint.

### "Output deck looks wrong"
Check the QA JPGs in `./outputs/qa_slide-*.jpg`. If a slide is broken, tell Claude — it will rebuild the affected slide and re-run the QA loop. Never deliver without inspecting the JPGs (rule #10).

### "GRS appeared in my deck"
That's a bug — file an issue. The hard rules should make this impossible. Trigger phrases like "supplier-facing" and "for supplier" should both enforce WSC-only.

### "Promo recap built with the wrong dates"
You skipped the kickoff. Run again and answer the **exact promo dates AND matched pre-period dates** when asked. Never let the skill infer dates from a filename.

---

## 5. Where to learn more

- **The full skill content** — `skills/wayfair-supplier-pitching/SKILL.md` (foundation) and `skills/major-shopping-holiday-wayfair/SKILL.md` (promo recaps)
- **The slash command** — `commands/wsp.md`
- **Visual system + Python helpers** — section §C in `skills/wayfair-supplier-pitching/SKILL.md`
- **Brand palette** — see "Wayfair EU brand palette" in the foundation skill
- **What NOT to do** — see "What NOT to do" section in the same skill

---

## How to extend the skill

If you find a pattern that should be enforced (e.g. a new pitch variant, a new killer narrative, a brand-rule update):

1. Edit the SKILL.md
2. Bump `metadata.version` in the YAML frontmatter
3. Bump `version` in `.claude-plugin/plugin.json`
4. Commit, push, send a PR — let the team review the playbook change like any code change

The playbook is now a versioned, reviewable artefact. Treat changes accordingly.
