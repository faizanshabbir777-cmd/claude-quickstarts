# Render deploy — WSP Pitch Builder · 3-minute setup

> The Render-hosted URL is the **active link** for the pilot bridge. No Claude license required. Stays up for the full 6-week leave.

---

## Why Render

- ✅ **Free tier** — 750 hours/month (24/7 for ~31 days)
- ✅ **EU region** — Frankfurt available (matches Wayfair EU data residency)
- ✅ **Streamlit-native** — no Docker required for the basic deploy
- ✅ **Persistent URL** — `wsp-builder.onrender.com` (or whatever name you pick)
- ✅ **Auto-deploys from main** — every git push to main triggers a redeploy automatically
- ✅ **Health check endpoint** — `/_stcore/health` baked into the Blueprint
- ⏳ **Idle sleep** — free tier sleeps after 15 min of no traffic; wakes in ~30 sec on next request

For the 2-week pilot bridge, the 30-second wake from sleep is acceptable. CMs aren't hitting it 24/7 — a slight delay on the first morning click is fine.

---

## The 3-minute deploy

### Option A · Blueprint-driven (recommended · 3 minutes)

1. Go to **[render.com](https://render.com)** → **Sign up** (free, GitHub SSO available)

2. Click **"+ New" → "Blueprint"** in the top-right.

3. Paste this URL when prompted:
   ```
   https://github.com/faizanshabbir777-cmd/claude-quickstarts
   ```
   Render auto-detects the `render.yaml` at `wayfair-eu-supplier-marketing/dashboard/render.yaml`.

4. Render shows you the planned services. Click **"Apply"**.

5. After ~30 seconds, you'll land on the service's dashboard. Render will prompt you to set the `WSP_PASSWORD` environment variable. Paste:
   ```
   Faizan's Claude Skill - EU WSP
   ```
   Click **"Save"**.

6. Render auto-builds the app (~90 seconds). When the status flips to **"Live"**, the URL is in the top-right corner.

7. Click the URL. You'll see the password gate. Enter the password. Done.

**URL format:** `https://wsp-builder.onrender.com` (or your chosen subdomain).

### Option B · Manual web-service deploy (5 minutes)

If Blueprint auto-detection has any issue:

1. Render → **"+ New" → "Web Service"**
2. Connect your GitHub → select `claude-quickstarts` repo
3. Fill the form:
   - **Name:** `wsp-builder`
   - **Region:** Frankfurt (EU)
   - **Branch:** `main`
   - **Root Directory:** `wayfair-eu-supplier-marketing/dashboard`
   - **Runtime:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
   - **Plan:** Free
4. Click **"Advanced" → "Add Environment Variable"**:
   - **Key:** `WSP_PASSWORD`
   - **Value:** `Faizan's Claude Skill - EU WSP`
5. Click **"Create Web Service"**. Wait ~2 min for build + first deploy.

---

## What CMs see

`https://wsp-builder.onrender.com` (or your chosen name).

They open the URL, enter the password, get the dashboard. Three storyboards live. Real personalised .pptx downloads on Build.

If the app is sleeping (no traffic for 15+ min), the first load takes ~30 seconds. Subsequent loads are instant. Tell CMs: *"Click the link, wait 30 seconds if it's been a while."*

---

## Sharing the URL with the pilot CMs (the Slack DM)

Once the URL is live, send each pilot CM this message:

> *"WSP Pitch Builder is live: `https://wsp-builder.onrender.com` · Password: `Faizan's Claude Skill - EU WSP` · 90-second walkthrough video [Loom link]. Play with it this week, drop feedback in #wsp-pilot. Brian's covering while I'm out — ping him if anything breaks."*

---

## Updating the app

Push to `main`. Render auto-redeploys within ~60 seconds. The URL stays the same; the app updates.

If you want to disable auto-deploy (so changes only ship when explicitly approved), turn off **"Auto-Deploy"** in the service's Settings tab.

---

## Pre-flight checklist

Before you click Deploy:

- [ ] PR #1 is merged to `main` (verified — confirmed at SHA `99fd527`)
- [ ] You have a GitHub account that can authorise Render
- [ ] You've decided on the subdomain name (`wsp-builder` recommended)
- [ ] You have the password ready to paste

That's it. The render.yaml + app.py do the rest.

---

## Cost projection

| Plan | Cost | What you get |
|---|---|---|
| **Free** | $0 | 750 hrs/mo, sleeps after 15 min idle, 512MB RAM |
| **Starter** | $7/mo | Always-on, 512MB RAM, custom domain |
| **Standard** | $25/mo | Always-on, 2GB RAM, faster CPU |

The Free tier covers the entire 6-week pilot bridge with **zero cost**. If you want zero sleep delay, upgrade to Starter ($7/mo). Don't go beyond that — Streamlit + this workload doesn't need more than 512MB.

---

## Monitoring and logs

In the Render dashboard, the `wsp-builder` service has:

- **Logs tab** — every Streamlit log line in real time
- **Metrics tab** — request rate, response time, memory, CPU
- **Events tab** — every deploy, scale-up, sleep/wake event
- **Settings → Environment** — where to rotate the password
- **Settings → Custom Domain** — if you want `wsp.wayfair.com` or similar (DNS work required)

Brian can sign in to Render with Faizan's GitHub during the leave to check logs if something seems wrong.

---

## Sleep-wake behaviour (important for CMs to understand)

The Free tier sleeps after 15 min of no requests. First click after sleep:

1. CM clicks the URL
2. They see the Render "Service waking up" page for 20-30 sec
3. Page reloads to the WSP Builder password gate
4. They enter the password, app loads normally

**This is expected.** Not a bug. Tell CMs once and they won't be surprised.

To avoid the wake delay during business hours, the simplest fix is to upgrade to **Starter** plan ($7/mo). Or set up a Cron-Job.org ping that hits the URL every 10 min during business hours (free workaround, ugly).

---

## If something breaks

See `BRIAN_RUNBOOK.md`. The escalation order:

1. **Check the Render dashboard Logs tab** — 80% of issues show up clearly
2. **Trigger a manual redeploy** (Settings → Manual Deploy → "Deploy latest commit") — solves 15%
3. **Ask in `#wsp-pilot` Slack** — someone on the team may know
4. **Wait for Faizan's return** — for non-blocking issues
5. **Take the URL offline** if it's leaking confidential supplier data (settings → "Suspend Service") — emergency button

---

## Migration from Render later

If Sophie's transition plan decides to move from Render to:

- **Wayfair internal infra** — the Dockerfile in this folder is what you hand to the platform team
- **Cloud Run / Fly.io / Railway** — same Dockerfile works
- **Streamlit Cloud / Hugging Face Spaces** — different config files; see DEPLOY.md
- **A Next.js wrapper on Vercel** — separate project; v2.0 scope

Render is the pilot host. Moving off it is a Phase 2/3 decision, not a Phase 1 blocker.

---

## What stays the same regardless of where it's hosted

- The app.py and deck_builder.py code (zero changes for hosting)
- The password env var pattern (`WSP_PASSWORD`)
- The audit log (writes to local `audit_log.jsonl`)
- The QA loop and visual register

Hosting is interchangeable. The app is portable.
