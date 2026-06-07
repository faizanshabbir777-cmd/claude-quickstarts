# WSP Pitch Builder — Streamlit MVP

Non-technical dashboard wrapper around the `wayfair-supplier-pitching` skill. Built so EU CM Champions can ship pitch decks without ever opening a terminal.

## What this is

A Streamlit web app that mirrors the EURTA NART / InfoHub aesthetic CMs already know (magenta header, tab nav, Tableau-style filter dropdowns, pink section eyebrows). Under the hood it calls the skill's three subagents — `wsp-data-prep`, `wsp-deck-author`, `wsp-deck-renderer` — and surfaces the same mid-deck checkpoint and QA loop the chat interface enforces.

## Run locally

```bash
# 1. Install deps (~30 seconds)
pip install streamlit pandas openpyxl

# 2. Run it
cd dashboard/
streamlit run app.py

# 3. Open in browser
# Streamlit will print the local URL — typically http://localhost:8501
```

## The 6 tabs

1. **Filters** — supplier · brief · storyboard · period · account team · output · data source (CSV upload or Looker dashboard ID)
2. **Data Preview** — `wsp-data-prep` sanity-check output, 4-6 plain-English bullets, pillar + variant recommendation
3. **Build** — storyboard scaffold preview + the big magenta build button + live pipeline status
4. **Preview & QA** — visual inspect every slide before send (the rule #10 QA loop, in the browser)
5. **Send** — download .pptx · send via Slack · email with attached deck + editable send-to-SRM template
6. **Skill Library** — what each storyboard does, when to use it, the canonical example

## What's wired vs what's stubbed in v0.1

**Wired:**
- Full UI matching the EURTA NART aesthetic
- All form inputs, dropdowns, tab navigation
- Storyboard selector (8 storyboards from `storyboards/`)
- Variant picker, audience picker, currency picker
- File uploader for CSVs / xlsx
- Visual register selector (TuttiBambini default · Internal MBR for the team's MBR)
- Preview tab showing the actual rendered slides if they exist in `outputs/`
- Send tab with download button + Slack hook + SRM email template

**Stubbed (week 1 pilot scope):**
- The "Run sanity check" button — currently shows a mock result. Wire to `wsp-data-prep` subagent via `subprocess` or via the Claude Agent SDK.
- The "Build Pitch Deck" pipeline — currently animates a progress bar. Wire to `wsp-deck-author` → `wsp-deck-renderer`.
- The "Send to SRM via Slack" button — currently a no-op. Wire to your team's Slack webhook.
- The "Email SRM" button — wire to whatever mail service Wayfair uses.
- The Looker dashboard ID field — currently a text input. Wire to Looker Studio REST API in pilot week 2.

Plumbing each stub into the real skill is a 1-2 hour task per stub. The hardest part is auth (Slack token, Gmail token, Looker service account) — none of the code.

## Deployment

For pilot scope, deploy via:

| Option | Effort | Auth |
|---|---|---|
| **Streamlit Community Cloud** | 10 minutes | GitHub SSO — fine for an open pilot |
| **Wayfair internal K8s** | 1 day | Wayfair SSO — proper auth, talk to platform team |
| **Retool wrap** | 1 week | Same auth as other Wayfair Retool apps — likely the production target |

Recommended: deploy to Streamlit Community Cloud for week 1 of the pilot (CM Champions click the URL, sign in with GitHub). If the workflow lands, migrate to Wayfair K8s in pilot week 2 with proper SSO.

## How a CM uses it (the 30-second flow)

1. Open the URL → see the Filters tab
2. Fill in: Supplier Name + ID, pick a Storyboard, pick the Period, pick the Audience, upload the CSV
3. Click **Data Preview** tab → click "Run sanity check" → confirm the data summary looks right
4. Click **Build** tab → review the storyboard scaffold → click "▶ Build Pitch Deck"
5. Watch the pipeline run (~90 seconds)
6. Click **Preview & QA** tab → flip through the rendered slides
7. Click **Send** tab → download or push to Slack

No terminal. No `git clone`. No Python install on the CM's laptop.

## What's NOT in the MVP

- **Multi-user state.** Each session is isolated. For a shared workspace ("see Faizan's builds, see Brian's builds") add a database backend.
- **Audit log.** Every build should write a log line (who, when, which supplier, which storyboard, which variant) for governance. Pilot week 2 work.
- **Version control on storyboards.** Editing a storyboard via the UI isn't supported — edit the markdown file in the repo. (This is intentional — the playbook is versioned in git, not in a database.)

## Mapping the UI to the underlying skill files

| UI element | Backed by |
|---|---|
| Storyboard dropdown | `storyboards/*.md` files |
| Variant picker | `wsp-deck-author` mid-deck checkpoint logic |
| "Run sanity check" | `wsp-data-prep` agent |
| Build button | `wsp-deck-author` → `wsp-deck-renderer` chain |
| Visual register selector | `SKILL.md §F` register switch |
| Preview tab | Output of `wsp-deck-renderer` QA loop |
| Skill Library tab | Live read of `storyboards/README.md` + each `*.md` frontmatter |

## Next steps (post-pilot)

1. **Migrate the auth model** from GitHub OAuth → Wayfair SSO
2. **Add per-CM build history** (Postgres, ~1 day's work)
3. **Wire the Looker direct-read** path (replace CSV upload for the 80% of cases where a dashboard already exists)
4. **Embed in EURTA NART as a tab** rather than running as a separate URL

Each of these is its own ticket. The pilot should generate the priority order.
