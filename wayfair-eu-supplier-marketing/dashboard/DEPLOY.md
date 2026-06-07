# DEPLOY · 5-minute path to a shareable URL

The dashboard is committed to the repo, configured for cloud, and ready to ship. You don't need to write any code. Pick one of three deploy paths below — each gives you a public URL with a password gate.

---

## Option A — Streamlit Community Cloud · **FREE · 5 minutes · recommended for pilot**

Streamlit Cloud connects to your GitHub repo and auto-deploys whenever you push. Free for public apps, password-gated via the secrets we already added.

### The exact 5 clicks

1. Go to **[share.streamlit.io](https://share.streamlit.io)**. Sign in with your GitHub account (the same one that owns `claude-quickstarts`).

2. Click **"New app"** (top right).

3. Fill the form:
   - **Repository:** `faizanshabbir777-cmd/claude-quickstarts`
   - **Branch:** `claude/wayfair-supplier-marketing-plugin-bkz5E` (or `main` after the PR merges)
   - **Main file path:** `wayfair-eu-supplier-marketing/dashboard/app.py`
   - **App URL:** customise to something memorable — suggested `wsp-builder` → final URL becomes `https://wsp-builder.streamlit.app`

4. Click **"Advanced settings"** → **"Secrets"**. Paste this exactly:
   ```toml
   [auth]
   password = "Faizan's Claude Skill - EU WSP"
   ```
   (You can rotate the password later — see `BRIAN_RUNBOOK.md` for the steps.)

5. Click **"Deploy!"**. Wait ~90 seconds. The app boots, installs the requirements from `requirements.txt`, and the URL goes live.

### Share with the team

Once it's deployed, send Brian + the 3-4 pilot CM Champions a Slack DM:

> *"WSP Pitch Builder is live: https://wsp-builder.streamlit.app · Password: `Faizan's Claude Skill - EU WSP` · 90-second walkthrough video [Loom link]. Play with it this week, drop feedback in #wsp-pilot."*

### Pushing updates

Edit any file in the `dashboard/` folder, push to the branch, and Streamlit Cloud auto-redeploys in ~30 seconds. No further action needed.

---

## Option B — Wayfair internal K8s · **proper SSO · ~1 day of platform team time**

Once the pilot proves out, the production path lives on Wayfair internal infra so it picks up Wayfair SSO and the data layer's network access. The platform team needs:

- The `dashboard/` folder (clone the repo, copy the folder)
- `requirements.txt` (we ship this)
- A `Dockerfile` (see below — drop into `dashboard/`)
- Internal DNS entry: `wsp-builder.eu-sam.wayfair.internal`
- SSO config: scope to the EU CM Champion role

### Dockerfile

Save this as `dashboard/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# System deps for the QA loop (LibreOffice + pdftoppm)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libreoffice \
    poppler-utils \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT ["streamlit", "run", "app.py", \
            "--server.port=8501", \
            "--server.address=0.0.0.0", \
            "--server.enableCORS=false", \
            "--server.enableXsrfProtection=true"]
```

Hand this to the platform team with the Streamlit Cloud URL as proof the app works. They wrap it in the standard Wayfair internal deployment manifest.

---

## Option C — Google Cloud Run · **pay-per-use · ~30 min if you have GCP creds**

Cloud Run is the obvious target if Wayfair runs on GCP (which seems likely given Looker Studio adoption). Free tier covers a pilot, costs scale to near-zero outside business hours.

```bash
# From the dashboard/ directory
gcloud run deploy wsp-builder \
  --source . \
  --region europe-west2 \
  --port 8501 \
  --allow-unauthenticated \
  --set-env-vars STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Cloud Run uses the Dockerfile above. ~3 minutes for first deploy.
# URL prints when done: https://wsp-builder-xxxxx-ew.a.run.app
```

Add Cloud IAP (Identity-Aware Proxy) for Wayfair SSO. That's the platform team's standard pattern for internal-only Cloud Run services — they have a runbook for it.

---

## Recommended path

| Day | Action | Goal |
|---|---|---|
| **Friday afternoon (before leave)** | Option A — Streamlit Community Cloud | Get a working URL the team can use Monday |
| **Pilot week 1** | Team uses Option A URL | Validate the UX flow with real CM Champions |
| **Pilot week 2** | Platform team starts Option B or C in parallel | Production-grade deploy with SSO |
| **Post-pilot** | Migrate to whichever Option B or C the platform team prefers | Replace the Streamlit Cloud URL with the internal one |

The Streamlit Cloud URL doesn't have to live forever — it's the bridge that gets you from "I built a thing" to "the team is using a thing" in 5 minutes.

---

## Pre-flight checklist

Before you click Deploy on Friday, verify:

- [ ] Repo is pushed to GitHub with the latest commit
- [ ] `dashboard/app.py` runs locally without errors (`streamlit run dashboard/app.py`)
- [ ] `dashboard/requirements.txt` lists every import
- [ ] `dashboard/assets/` contains the 4 Monty PNG previews
- [ ] `dashboard/demo/Monty_Trading_April2026_WSP_Deck_v2.pptx` exists (download button needs it)
- [ ] Password in `secrets.toml.example` is what you want to share with CMs

If all six tick, you're good.

---

## Troubleshooting

### "Streamlit Cloud says module not found"
Add the missing module to `requirements.txt` and push. Streamlit auto-redeploys.

### "Password gate not working"
The secrets in Streamlit Cloud are separate from `secrets.toml.example` in the repo. Make sure you pasted them in the Streamlit Cloud UI under Advanced settings → Secrets.

### "Preview tab shows 'asset not found'"
The PNGs in `dashboard/assets/` weren't committed. Run from the repo root:
```bash
cd wayfair-eu-supplier-marketing/dashboard
ls assets/   # should show monty_tutti_s1.png through s4.png
ls demo/     # should show Monty_Trading_April2026_WSP_Deck_v2.pptx
```

### "Build button does nothing"
`session_state["build_in_progress"]` got stuck. Refresh the browser tab. (Pilot v0.2 will fix the state machine.)

### "URL stopped working overnight"
Streamlit Cloud puts free apps to sleep after 7 days of no traffic. First load after sleep takes ~30 seconds. Send a CM the URL once a week to keep it warm, or upgrade to Streamlit Cloud's paid tier (~$20/mo) for always-on.

---

## What lives where, in plain English

```
dashboard/
├── app.py                          ← the UI · what Streamlit runs
├── requirements.txt                ← Python deps · Streamlit Cloud uses this
├── .streamlit/
│   ├── config.toml                 ← magenta theme · port settings
│   └── secrets.toml.example        ← password template (copy to secrets.toml on cloud)
├── assets/
│   ├── monty_tutti_s1-4.png        ← Preview tab needs these
│   └── wayfair_logo_white.png      ← UI mockup uses this
├── demo/
│   └── Monty_Trading_April2026_*.pptx  ← Download button serves this
├── DEPLOY.md                       ← this file
├── EMAILS.md                       ← three outbound drafts
├── README.md                       ← what is/isn't wired
├── WSP_Builder_UI_Mockup.pdf       ← Clement-facing mockup
└── build_ui_mockup.py              ← source for the mockup
```

Everything the cloud needs lives in this folder. No external dependencies.
