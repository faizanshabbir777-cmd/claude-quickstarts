# Integrations — Looker Studio, BigQuery, Account Overview

How the WSP skill connects (or could connect) to the data sources you already use. This is a forward-looking doc — most of what's described here is pilot scope, not the basic working version.

---

## TL;DR

| Source | Today (basic version) | After pilot | Effort |
|---|---|---|---|
| **Looker Studio dashboards** | Manual CSV export → drop in `./data/` | Direct read via the Looker Studio REST API | Low (~1 week) |
| **BigQuery** (Looker sits on it) | None | Direct SQL query in `wsp-data-prep` | Medium (~2 weeks, needs creds) |
| **Account Overview** | Manual screenshot for sanity-check | Direct read for automated sanity-check | Low–medium |
| **MBR SET 1/2/3** | Manual CSV/xlsx | Same — these are scheduled exports, not live |  — |
| **Detailed Listing Health** | Manual export | Same — internal tool, no API |  — |

---

## Today: the manual data flow

The basic working version assumes the analyst manually exports data and drops it in `./data/`. This is fine and works — it's just not yet automated.

```
┌────────────────┐       ┌──────────┐
│ Looker dash    │──┐  ┌─│ Account  │
│ (the SAM views)│  │  │ │ Overview │
└────────────────┘  │  │ └──────────┘
                    │  │
                    ▼  ▼
                ┌──────────┐
                │ ./data/  │  ← analyst drops CSVs / xlsx here
                │  *.csv   │
                │  *.xlsx  │
                └──────────┘
                    │
                    ▼
           ┌─────────────────┐
           │ wsp-data-prep   │  ← cleans, computes, sanity-checks
           │ → deck_data.json│
           └─────────────────┘
                    │
                    ▼
           ┌─────────────────┐
           │ wsp-deck-author │  → slides.md
           └─────────────────┘
                    │
                    ▼
           ┌──────────────────┐
           │ wsp-deck-renderer│  → outputs/*.pptx
           └──────────────────┘
```

**This works. Ship it. Don't wait for integrations.**

---

## Pilot scope: Looker Studio direct read

Looker Studio exposes a REST API. The skill could query it to pull data directly, removing the manual CSV export step.

### What's needed

1. **Looker Studio service account credentials** (one-time, IT involvement)
2. **The dashboard IDs** the team uses for WSP performance (the existing analyst dashboards)
3. **A small Python wrapper** in `scripts/looker_studio.py` that takes a dashboard ID + report period and returns the data as a pandas DataFrame

### The new flow

```
┌────────────────┐
│ Looker dash    │
│ (dashboard ID) │
└────────────────┘
        │
        │  REST API call
        ▼
┌─────────────────┐
│ wsp-data-prep   │  ← reads Looker directly, no CSV export
│ → deck_data.json│
└─────────────────┘
```

### What the analyst types

```
/wsp Monty Trading UK · WSP value review · April 2026
Looker dashboard: monty-trading-wsp-monthly
```

The skill pulls the data, does the rest.

### Why this matters

- Eliminates the most error-prone step (manual export → drop in folder)
- Guarantees the deck and the dashboard agree (no version skew)
- Lets the SAM build a deck from any dashboard URL — the storyboard doesn't change

### Why this isn't in the basic version

- Needs IT involvement for service-account credentials
- Looker dashboards aren't standardised across the team — each SAM's dashboard is slightly different
- Pilot's job: find the 2-3 canonical dashboard layouts, build adapters for each

---

## Stretch: BigQuery direct query

Looker Studio sits on BigQuery. For deeper analyses (cap-hit frequency, spend × WSC correlation across categories, etc.), querying BigQuery directly is more powerful than reading a pre-built dashboard.

### What's needed

1. **BigQuery project access** for the EU WSP dataset (IT, scoped read-only)
2. **A query template per storyboard** — what to SELECT for a value-review vs a restart pitch vs a promo recap
3. **Caching layer** so the same supplier-month isn't re-queried for every deck (BigQuery costs add up)

### The new flow

```
┌─────────────┐
│ BigQuery    │
│ EU WSP DS   │
└─────────────┘
       │
       │ scoped SQL query
       ▼
┌─────────────────┐
│ wsp-data-prep   │  ← runs storyboard's query, caches result
│ → deck_data.json│
└─────────────────┘
```

### What the analyst types

```
/wsp Monty Trading UK · WSP value review · April 2026
Source: bigquery
```

The skill queries the standard EU WSP dataset for SuID 37802, April 2026 + 12-month context, writes deck_data.json.

### Why this matters

- Lets the skill compute analyses that aren't on any pre-built dashboard (cap-hit frequency, engine SKU identification, CG concentration)
- Removes the dependency on which SAM uses which dashboard
- Unlocks portfolio-outreach storyboard at proper scale (current MBR analysis is monthly; with BigQuery the agent can rank suppliers weekly)

### Risk surface (be honest)

- Query costs scale with how often the team builds decks. Cache aggressively.
- Read-only credentials, scoped to the EU WSP dataset only. No write access. No PII columns.
- Service account credentials live in `~/.claude/secrets/` on the SAM's local machine — never committed.

---

## What I would NOT integrate

| Source | Why not |
|---|---|
| **The supplier's own systems** | We don't have access. Not the integration's job. |
| **Email / Slack** | Out of scope. The deck is the artefact; sending it is the SAM's job. |
| **Salesforce / SRM CRM** | Different ownership. SAM tools should stay agnostic. |
| **Anthropic's API directly** | The skill runs via Claude Code. No bespoke API calls. |

---

## Architecture decision

If you're choosing between Looker Studio API vs BigQuery direct:

- **Pick Looker Studio API for the pilot.** Lower IT lift. Faster to ship. Covers 80% of the analyst's needs (data the team already trusts).
- **Move to BigQuery in v2** once the pilot proves out and the team agrees on a canonical query template per storyboard.

Don't try to do both at once. Pick one.

---

## What I need from IT to start the pilot

Send IT this paragraph:

> *"Pilot scope: 3-4 EU SAMs using a Claude Code skill that reads Wayfair WSP performance data from the team's existing Looker Studio dashboards. Needed: a service account with read-only access to the WSP EU dashboards, scoped to the SAM team's standard dashboard set. Credentials stored locally on each SAM's machine (~/.claude/secrets/), never committed. No write access. 2-week pilot, then evaluate widening to BigQuery direct."*

Their first question will be about data residency and PII. The answer: WSP performance data is supplier-level aggregates (no individual user data), already viewable by the SAM team, and the integration is a local-machine fetch — no Anthropic-side persistence beyond the active prompt.

---

## What's the minimum needed to demo the integration

A static `looker_studio.py` mock that returns a hard-coded DataFrame for one supplier. The SAM types the prompt, the skill "queries Looker," and produces the same Monty deck — but without manually dropping a CSV.

That mock is 30 lines of Python. I can write it before I go on leave if Brian / Clement greenlight the pilot. Otherwise it's day-1 work when I'm back.

---

## Summary

- **Today:** manual CSV/xlsx → skill works end-to-end. Ship this.
- **Pilot week 1:** Looker Studio API integration — analyst types dashboard ID, skill pulls data.
- **Pilot week 2:** BigQuery direct query for advanced analyses (cap-hit, engine SKU, portfolio ranking).
- **Post-pilot:** decide whether to upgrade everyone to BigQuery or keep Looker Studio as the default for self-service SAMs.

The basic version doesn't need any integration to be valuable. The integrations are the second derivative.
