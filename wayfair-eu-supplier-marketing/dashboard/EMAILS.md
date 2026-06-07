# Outbound emails — pilot kickoff

Three drafts. Send in this order:

1. **Brian** — frames the pilot, names the CM Champions, asks him to be the in-leave contact
2. **Clement** — the formal pitch + asks for greenlight
3. **EURTA NART tech team** — the longer-term integration ask, only sent AFTER Clement greenlights

Don't send #3 before #2 lands. It puts IT before strategy.

---

## Email 1 — to Brian (direct manager, in-leave contact)

**Subject:** WSP Pitch Builder · 2-week pilot · need your read before I send to Clement

> Brian,
>
> Quick share before I'm out from Friday. Spent the last two weeks codifying our WSP pitching playbook into a Claude Code skill — anchored to my TuttiBambini deck for Tapanshi. Brand rules enforced, storyboards stop drift, QA loop catches layout breaks. Half-day pitch builds compress to minutes.
>
> Sending Clement the formal pitch tomorrow. Before I do, I'd like 15 minutes with you to:
>
> 1. Walk you through the 90-second demo
> 2. Show you the dashboard mockup (looks exactly like InfoHub / EURTA NART — Tableau-style filter grid, magenta header, CMs would recognise it immediately)
> 3. Get your read on which 3-4 CM Champions should be in the pilot
>
> Pilot scope:
> - **3-4 EU CM Champions** building real pitches via a shared Claude.ai Project (week 1) and a Streamlit dashboard (week 2)
> - **2-week window** starting when I'm back from leave
> - **Deliverable:** each CM ships 5 pitches through the tool, and we get feedback on what should become the production version
>
> While I'm out, I'd like to leave you as the point of contact if Clement or anyone else has questions. Everything's documented in the repo — I'll send you the operator pack and the storyboard files separately so you have the full picture.
>
> Repo: github.com/faizanshabbir777-cmd/claude-quickstarts/tree/main/wayfair-eu-supplier-marketing
>
> Free for 15 minutes today or tomorrow?
>
> Faizan

---

## Email 2 — to Clement (CC Brian)

**Subject:** WSP Pitch Builder · 2-week pilot ask · 3-4 EU CM Champions

> Hi Clement, (cc Brian)
>
> Quick share before I'm out from Friday. I've built something I think changes how the EU SAM team produces supplier pitches.
>
> One-pager attached explains it in 30 seconds. 90-second video shows it actually working on Monty Trading's April data. Receipts portfolio shows the four decks the skill has already produced — same visual register as the TuttiBambini deck I built for Tapanshi.
>
> Short version: it's a Claude Code plugin that codifies our pitch playbook — the ten hard rules, the four pitch variants, the QA loop, the TuttiBambini visual conventions. Storyboards stop drift (every pitch type has a fixed scaffold). A CM types one command in chat (or eventually clicks through a dashboard that looks just like InfoHub) and the skill builds the deck. The Monty deck attached was built end-to-end in 3 minutes.
>
> **Asking for a 2-week pilot when I'm back from leave:**
> - 3-4 EU CM Champions (Brian and I will land on names)
> - Week 1: use the skill via a shared Claude.ai Project — chat interface, no terminal
> - Week 2: ship a Streamlit dashboard that looks like InfoHub (mockup attached)
> - Each CM ships ~5 real supplier pitches through the tool
> - I take their feedback and harden the basic version into something we can roll out to the broader team
>
> **What I'm NOT asking for:** broad rollout, IT-heavy integration, budget approval. The basic version works end-to-end today. Pilot just gets us real CM feedback before we wire anything to Looker, BigQuery, or EURTA NART.
>
> Brian has all the artefacts and the storyboard while I'm out. The 90-second video stands on its own if it comes up in any meeting before I'm back.
>
> Faizan
>
> Attached:
> - Clement_OnePager.pdf
> - Demo_Storyboard_90s.pdf (or Loom link)
> - Receipts_Portfolio_v2.pdf
> - WSP_Builder_UI_Mockup.pdf (the dashboard mockup)

---

## Email 3 — to EURTA NART / InfoHub tech team (only after Clement greenlights)

**Subject:** WSP Pitch Builder · early read on integration into EURTA NART after pilot

> Hi {tech team lead},
>
> Brian / Clement signed off on a 2-week pilot of a tool I've built that produces WSP supplier pitch decks for the EU CM Champion team. It currently runs as a Streamlit dashboard hosted on internal K8s. Mockup attached — visual language is deliberately consistent with InfoHub / EURTA NART (magenta header, Tableau-style filter grid, pink section eyebrows) so CMs in the pilot recognise the UI immediately.
>
> **What I'd like to explore with your team after the pilot lands:**
>
> 1. **Embed the tool as a tab inside EURTA NART** rather than running it as a separate URL. Reduces context-switching, lives in the tool CMs already open daily.
> 2. **Wire the data layer to the same source EURTA NART uses** — currently we ingest from CSVs the analyst exports manually, or from Looker Studio dashboard IDs in pilot week 2. The dream is direct read from the BigQuery dataset EURTA NART already queries.
> 3. **Auth model** — pilot uses GitHub OAuth (it's a 4-CM trial), production needs Wayfair SSO scoped to the CM Champion role.
>
> Pilot artefacts so you can see what we're working with:
>
> - Skill source: github.com/faizanshabbir777-cmd/claude-quickstarts/tree/main/wayfair-eu-supplier-marketing
> - Dashboard source: same repo, `dashboard/app.py`
> - Mockup: WSP_Builder_UI_Mockup.pdf
>
> Happy to share a 30-min walkthrough after the pilot ships week 2 deliverable (~3 weeks from now). No action needed from you before then — this is just an early read so it's not a surprise when it lands.
>
> Faizan
> EU WSP Lead

---

## Notes

- **Re: Brian as the in-leave contact.** Don't sugarcoat this in the Clement email. Clement will respect the "Brian has all the artefacts" line because it shows you've planned for the gap. Don't say "Faizan is sick" — say "I'm out from Friday" and leave it at that.
- **Re: the dashboard mockup.** The mockup is the artefact that gets the EURTA NART team interested. Send it to Clement up front. They'll forward it to tech. The skill plugin is the substance; the mockup is the bridge.
- **Re: timing.** Send Email 1 (to Brian) Monday or Tuesday. Email 2 (to Clement) Wednesday morning after Brian has seen it. Email 3 (to EURTA NART) waits until Clement greenlights — don't pre-empt.
