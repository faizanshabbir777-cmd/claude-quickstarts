# While Faizan is out — Brian's runbook

Faizan is out for 7 weeks from {DATE}. The WSP Pitch Builder is **production v1.0** and runs autonomously. CMs upload data → click Build → get a personalised deck. No Faizan-in-the-loop required.

This doc tells you what to do if something goes wrong.

---

## The system at a glance

| What | Where |
|---|---|
| Live URL | `https://wsp-builder.streamlit.app` (whatever URL came back from the Streamlit Cloud deploy) |
| Repo | `github.com/faizanshabbir777-cmd/claude-quickstarts/tree/main/wayfair-eu-supplier-marketing` |
| Streamlit Cloud dashboard | `share.streamlit.io` — sign in with Faizan's GitHub (he leaves you the password) |
| Password for users | `wsp-pilot-2026` (rotate if pilot CMs leak it — see "Password rotation" below) |
| Slack channel | `#wsp-pilot` |

---

## CM reports "the app is down"

90% of the time, this is **Streamlit Cloud's free-tier sleep** — apps idle for 7 days get suspended. First load takes ~30 seconds. Tell the CM:

> *"Refresh once and wait 30 seconds. It's just waking up."*

If still down after 60 seconds, sign into `share.streamlit.io` and:

1. Find the `wsp-builder` app
2. Click the three-dot menu → **Reboot app**
3. Wait 90 seconds
4. Refresh the URL

If that fails, check **Manage app → Logs** in the Streamlit dashboard. Errors are usually obvious (Python traceback). Send a screenshot to `#wsp-pilot` Slack — Faizan or someone else on the team can diagnose.

---

## CM reports "Build failed on my file"

Most common cause: their CSV has columns the parser doesn't recognise. Tell them:

> *"Go to the Data Preview tab, click 'Run sanity check', and expand 'Columns matched in your file'. If `wsc` or `attr` shows `null`, your file uses a non-standard column name. Either rename the column in Excel before uploading, or share the file with me."*

If you can't fix it that way, the canonical CSV format is the `media_tbl_advertising_campaign_reporting_extended_*.csv` export. If they're using something else (a Looker export with different column names, a custom MBR cut), Faizan needs to add the column alias to `data_prep.py` when he's back.

**For now**, the CM can do the build in PowerPoint manually using the same scaffold — share them the existing Monty / Forte / TuttiBambini decks as templates.

---

## CM reports "the deck looks wrong"

There are two possible reasons:

**(a) The data is wrong** — verify with the CM that the numbers in the data-preview tab match what they see in Looker / Account Overview. If the numbers in the tab are off, the parser picked the wrong columns. Same fix as above.

**(b) The visuals are off** — typo in the supplier name in the form, weird chart scaling, etc. Tell the CM:

> *"Open the .pptx in PowerPoint and override what's off — that copy is yours. Share what was wrong in #wsp-pilot Slack and Faizan will fix the template when he's back."*

Don't try to patch the code yourself unless you're comfortable. The dashboard is python-pptx + PIL — read-ahead requires it. **Better to ship a hand-fixed deck this week than introduce a bug.**

---

## CM reports "data privacy concern"

Send them the data safety memo first: `dashboard/Leadership_Data_Safety_Memo.pdf`.

If they have a specific concern (where does the file go, who can see it, etc.), the short answers are:

| Concern | Answer |
|---|---|
| Where does my uploaded CSV go? | Read into memory in the Streamlit Cloud session, used to compute metrics, dropped when the session ends. Not stored anywhere. |
| Can Anthropic / Claude see the data? | No. The Build pipeline is python-pptx + matplotlib — no Claude API call in v1.0. |
| Can other CMs see my deck? | No. Each session is isolated. |
| What if I'm on the train and someone shoulder-surfs the URL? | Password-gated. They'd see the gate, not the dashboard. |
| Is supplier data encrypted in transit? | Yes — Streamlit Cloud terminates HTTPS at the edge. |

For anything more complex, send to `infosec@wayfair` and CC me — I'll surface to Faizan on his return for a proper response.

---

## Password rotation

If you suspect the pilot password has leaked beyond the intended CMs:

1. Sign into `share.streamlit.io` with Faizan's GitHub
2. Open the `wsp-builder` app → **Settings** → **Secrets**
3. Replace the `password = "wsp-pilot-2026"` line with a new value (use a passphrase like `wsp-summer-2026-mar`)
4. Save — Streamlit auto-reloads the app
5. DM the new password to the pilot CMs only

Don't write the new password in Slack `#wsp-pilot` — DM each CM separately.

---

## What I (Brian) should NOT do

❌ Edit the Python code without Faizan to QA the changes. The skill is versioned in git for a reason — accidental edits can ship broken decks to suppliers.

❌ Add new CMs to the pilot without checking with Clement. The pilot scope was 3-4 CM Champions; opening it wider is a separate decision.

❌ Use the dashboard for high-stakes Tier-0 supplier pitches where an error would be catastrophic. Use it for medium-stakes pitches. For Tier-0, build by hand or wait for Faizan.

❌ Promise CMs "feature X will ship next week" without checking the v1.1 roadmap. The v1.1 storyboards (Restart, Switch-to-5%, Promo Recap, Summit) are all Faizan-back work.

---

## What good looks like over 7 weeks

By the time Faizan is back, you want:

- The dashboard URL still works and has been used by the pilot CMs
- At least one CM has shipped a real pitch with it that landed well
- A list of issues / feature requests collected in `#wsp-pilot` for Faizan to triage
- The audit log (in `dashboard/audit_log.jsonl` or wherever the Streamlit instance writes it) showing 10-50 builds happened

If none of that happens — if the URL goes dark, if no CM uses it, if no one says anything in Slack — that's signal too. Faizan needs to know on day one back so he can pivot.

---

## When something seems genuinely broken

The escalation order:

1. **Check Streamlit Cloud logs** (Manage app → Logs). 80% of issues show up clearly.
2. **Restart the app** (Reboot from the Streamlit dashboard). Solves 15%.
3. **Ask in `#wsp-pilot` Slack** — someone else on the team may know.
4. **Email Faizan** at `{faizan email}` — only if it's blocking a supplier pitch this week. He's checking once a week, briefly. Don't escalate unless it's blocking.
5. **If the dashboard is down for >24 hours** and you can't restart it, take it offline and tell the CMs to use Claude.ai with the SKILL.md pasted in (legacy path — see `HOW_TO_USE.md`). This is the fallback.

---

## A note from Faizan

Brian — thank you for covering. The system is designed to need very little from you. Most weeks you'll do nothing because nothing breaks. The Streamlit Cloud sleep is the most common "issue" and refresh-and-wait fixes it.

The pitch decks the CMs build this week are real artefacts that suppliers will see. Treat them with the same respect as decks I'd build myself. If you're not sure about a specific deck, hold it until I'm back rather than ship something off-brand.

The repo has everything you need. Read `HOW_TO_EXPLAIN.md` if Clement asks you what this thing is.

— Faizan
