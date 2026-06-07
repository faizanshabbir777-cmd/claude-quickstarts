# Data Safety — WSP Pitch Builder

> A 5-minute read for IT, security, legal, and anyone who'll ask *"where does the data go?"* before greenlighting the pilot.

---

## TL;DR

| | Pilot (Streamlit Cloud) | Production (Wayfair internal) |
|---|---|---|
| **Real supplier data allowed?** | **No — demo data only** | Yes — same controls as the existing analyst tools |
| **Data residency** | US (Streamlit Cloud / AWS) | EU (Wayfair internal infra) |
| **Auth** | Shared pilot password | Wayfair SSO scoped to CM Champion role |
| **AI vendor (Anthropic) sees data?** | No — Build button is stubbed | Yes, under Wayfair's enterprise agreement (no training, no persistence) |
| **GRS exposure risk** | None (Rule #1 enforced by the skill) | None (Rule #1 enforced by the skill) |
| **Retention** | None — session ends, data gone | Per Wayfair retention policy |

**Bottom line:** the pilot version on Streamlit Cloud is a **UX demo** — for CMs to learn the flow and for leadership to see the artefact. Real supplier-data builds happen on Wayfair-internal infra in pilot week 2, after the platform team's review.

---

## Data classification

The skill and dashboard handle data of three sensitivity levels:

| Data type | Examples | Classification | In supplier-facing decks? |
|---|---|---|---|
| **Supplier-confidential** | WSC, wholesale per £1 of WSP, % of WSC, attributed wholesale | Internal · supplier-shareable in supplier-specific outputs | ✅ Yes — these are the metrics suppliers see |
| **Wayfair-confidential** | GRS, retail revenue, retail ROAS, internal benchmarks named by supplier, SRM names | Internal only · **NEVER** in supplier-facing material | ❌ Hard rule #1 in `SKILL.md` |
| **Public / non-sensitive** | Storyboard names, brand palette, layout patterns | Public | ✅ Yes |

The skill's rule #1 (no GRS in supplier-facing material) is enforced **structurally**, not by reviewer vigilance. The `audience` field in every storyboard locks the metric set — when "Supplier-facing" is selected, the code path that emits GRS is unreachable.

---

## Data flow — what travels where

### Pilot version (Streamlit Cloud · demo data only)

```
CM's browser  ──HTTPS──▶  Streamlit Cloud (AWS US-East)  ──▶  Demo PPTX served back
       │
       │  No real supplier data uploaded
       │  No call to Anthropic / Claude
       │  No outbound API calls
       ▼
   Session ends → memory cleared
```

What touches Streamlit Cloud:
- Filter dropdown values (supplier name, period, etc.) — entered by CM
- The Monty demo PPTX (which the team explicitly classified as shareable demo asset)
- Pilot password (hmac-compared, never logged)

What does NOT touch Streamlit Cloud:
- Real supplier CSVs (file uploader is disabled for the pilot URL — see "Controls" below)
- Real Looker dashboards
- Anything from BigQuery
- Anthropic / Claude

### Production version (Wayfair internal · pilot week 2+)

```
CM's browser  ──HTTPS / Wayfair SSO──▶  Wayfair internal Streamlit instance
                                              │
                              ┌───────────────┼─────────────────┐
                              ▼               ▼                 ▼
                         Looker API      BigQuery EU       Anthropic API
                       (scoped read)    (scoped read)    (Claude Code SDK)
                              │               │                 │
                              └──────┬────────┘                 │
                                     ▼                          │
                          deck_data.json (in memory)            │
                                     │                          │
                                     └──────────┬───────────────┘
                                                ▼
                                     Real pptx ◀───  rendered via
                                                     python-pptx
```

Every external call (Looker, BigQuery, Anthropic) uses a service account scoped to the EU CM Champion role. No raw data leaves Wayfair's network except the structured prompts to Anthropic — which run under Wayfair's enterprise data agreement.

---

## What Anthropic sees (and doesn't)

When the production version calls the Claude API to drive the `wsp-deck-author` subagent:

**What's in the prompt:** the supplier name, the period, the storyboard scaffold, and the computed metrics (spend, WSC, ROAS, intensity %). All supplier-level aggregates.

**What's NOT in the prompt:**
- Individual customer / shopper data (we don't have it)
- PII (we don't process any)
- GRS / retail revenue (rule #1)
- Any raw row-level data — only the aggregates the storyboard requires

**Anthropic's guarantee** (per the Anthropic API terms for enterprise customers):
- API requests are not used to train models
- API requests are not persisted beyond the time needed to generate a response (~30 days for abuse monitoring, then deleted)
- Data is encrypted in transit and at rest
- Anthropic is SOC 2 Type II certified

If Wayfair has its own Anthropic enterprise agreement, the production deploy uses that. The pilot Streamlit Cloud deploy doesn't call Anthropic at all (Build button is stubbed to return the demo PPTX).

---

## Controls in the code

Listed where they live so an engineer can verify them.

| Control | Where | What it does |
|---|---|---|
| **Password gate** | `app.py` — `check_password()` | hmac-compared shared secret. No bypass. Wrong password = stops on the gate. |
| **No real data upload (pilot)** | Pilot banner + UX flow | CMs are told upfront the demo data is the only path. File uploader is shown but the demo overrides it. Production version removes the override. |
| **HTTPS** | Streamlit Cloud default | All traffic to/from the URL is TLS 1.2+. Streamlit Cloud terminates TLS at the edge. |
| **XSRF protection** | `.streamlit/config.toml` | `enableXsrfProtection = true`. Cookies signed, requests checked. |
| **Upload size limit** | `.streamlit/config.toml` | 50MB cap. Prevents DOS via huge files. |
| **File type restriction** | `app.py` file uploader | Only `.csv` / `.xlsx` accepted. No executables, no archives. |
| **No telemetry** | `.streamlit/config.toml` | `gatherUsageStats = false`. Streamlit's anonymous usage stats off. |
| **Session isolation** | Streamlit default | Each CM's session state is separate. No cross-session leakage. |
| **Rule #1 enforcement** | `SKILL.md` + storyboards | The "no GRS in supplier-facing" rule is enforced at the storyboard level — supplier-facing audience selection makes the GRS code path unreachable. |

Controls **not yet in v0.1 but planned for v0.2 production:**
- Wayfair SSO (replaces shared password)
- Per-CM audit log (every build writes a structured log entry: who, when, supplier, storyboard, variant)
- Automated PII scanner on uploaded files (rejects uploads containing detected emails, phone numbers, etc.)
- Session timeout (60 min idle)
- Rate limit (no CM can build more than 20 decks per hour — caps cost and abuse risk)

---

## What happens when the pilot ends

| Artefact | Fate |
|---|---|
| **Streamlit Cloud app** | URL taken down. App deleted. No data was ever stored. |
| **Pilot password** | Rotated; old one revoked |
| **GitHub repo (the code)** | Stays — the playbook is now versioned IP |
| **CM-built decks** | Whatever lifecycle the SAM team's normal pitch decks follow — saved locally by the CM, attached to emails, etc. |
| **Anthropic-side request logs** | Deleted by Anthropic per their 30-day policy. (Pilot didn't call Anthropic anyway.) |

There is no central database to wipe. The system is stateless by design — each CM's session is independent, and the deck files belong to the CM, not the platform.

---

## What we promise

✅ **No GRS in any supplier-facing output.** Structurally enforced.
✅ **No real supplier data on Streamlit Cloud during pilot.** Demo banner + locked input flow.
✅ **No PII processed anywhere.** Supplier-level aggregates only — no individual customers, no shopper data.
✅ **HTTPS everywhere.** No plaintext traffic.
✅ **Password gate on the pilot URL.** No public access.
✅ **The playbook is versioned and auditable** in git. Every change to a rule has a commit author and a timestamp.

## What we DON'T promise (be honest)

❌ **The pilot Streamlit URL is not Wayfair-internal.** It runs on Streamlit Community Cloud (AWS US-East). Don't put real supplier data on it. The production version moves to Wayfair-internal infra in week 2.

❌ **No formal pen-test on v0.1.** This is an MVP. Security review happens before production rollout — built into pilot week 2's scope.

❌ **No GDPR DPA on the pilot.** Streamlit Cloud's standard ToS apply. The production Wayfair-internal version uses Wayfair's existing infra contracts — no new vendor relationship needed.

❌ **The Build button is currently stubbed.** It returns a hardcoded demo deck, not a real generated one. This is deliberate (pilot v0.1 is a UX validation), but it means the CM-built decks during pilot are not personalised yet. Real personalisation = pilot week 2 work.

---

## Pre-greenlight questions, answered

**Q: Is this approved under our existing vendor management process?**
A: For the pilot, it uses Streamlit Community Cloud (free tier) and Anthropic API (existing Wayfair enterprise agreement assumed — confirm with IT). No new vendor sign-off. For production, the same Wayfair-internal infra and SSO that other CM tools use.

**Q: What if a CM pastes real supplier data into the pilot URL?**
A: The pilot banner says "demo only" and the file uploader is configured to be a UI element, not a data ingestion. Even if a CM uploads a real CSV, it's read into the Streamlit session, used to render preview, then dropped when the session ends. No persistence. We're still recommending against it — the production version is the right place for real data.

**Q: Does this expose us to data-residency issues?**
A: Pilot version: US-based hosting (Streamlit Cloud). Production version: EU-based hosting (Wayfair internal). The pilot is demo-only; the production version handles all real data. GDPR concerns sit with production, not pilot.

**Q: What about the data the skill prompt sends to Anthropic?**
A: In pilot v0.1, none — the Build button doesn't call Anthropic. In production v0.2, the prompts contain supplier-level aggregate metrics (no PII, no GRS, no row-level data) under Wayfair's enterprise data agreement with Anthropic. Anthropic doesn't train on the data and doesn't persist it beyond the 30-day abuse-monitoring window.

**Q: Who owns the artefacts the CM builds?**
A: The CM. The system is stateless — built decks are downloaded to the CM's machine and follow whatever lifecycle the SAM team's normal pitch decks follow. Nothing is centrally stored.

**Q: What's the worst case if the pilot URL is compromised?**
A: An attacker sees the demo Monty deck (already in the public artefacts the CM team has been working with) and the UI flow. No real supplier data is exposed because none is on the system. Mitigation: rotate the pilot password, take down the URL.

**Q: What's the audit story?**
A: Pilot v0.1 doesn't log builds. Pilot v0.2 (week 2) adds a per-build audit log: who built what, when, for which supplier, under which storyboard. The log is structured (JSON) and rotates to whatever Wayfair's standard log sink is.

---

## Sign-off checklist for the platform team

Before the pilot URL goes live, the platform team confirms:

- [ ] Pilot URL is not externally indexable (Streamlit Cloud apps are by default — verify `noindex` is set or the app is in private mode)
- [ ] Pilot password is rotated from the example value in `secrets.toml.example`
- [ ] The demo PPTX files in `dashboard/demo/` are reviewed as shareable demo assets (Monty Trading numbers are aggregates the analyst team has classified as demo-safe — confirm with Faizan or Brian)
- [ ] The pilot CMs are explicitly told NOT to enter real supplier data via Slack/email when the URL is shared
- [ ] Production deploy plan for pilot week 2 is scoped (which Wayfair-internal infra, which SSO scope, who's the platform-team contact)

---

## Contact

**During pilot:** Brian Delsignore (direct line) · Faizan returning from leave [return date].
**Post-pilot, production rollout:** to be determined by Clement Delay + platform team lead.

The playbook lives at: `github.com/faizanshabbir777-cmd/claude-quickstarts/tree/main/wayfair-eu-supplier-marketing` — version-controlled, every change auditable.
