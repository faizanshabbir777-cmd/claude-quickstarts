# Leave Coverage Terms — the source of truth

> *"Lock in: Faizan no contact post today. 6 weeks. Phase 2 only post that."*

This is the canonical document. Anyone unsure about what to do during the 6-week leave reads this first. All other runbooks defer to it.

---

## The terms

| | |
|---|---|
| **Leave starts** | End of today |
| **Leave duration** | 6 weeks |
| **Return date** | _________ (Faizan to fill in before signing off today) |
| **Contact policy** | **Absolute no-contact.** No Slack, no email, no "urgent" pings, no exceptions. |
| **Phase 2 work (license procurement + Claude transition)** | **Does not begin until Faizan returns.** Sophie waits. |
| **Phase 1 operations (Render URL + Brian covers)** | Active throughout the 6 weeks |

---

## What this means for each person

### Brian Delsignore — owns Phase 1 operations

**Your scope for the 6 weeks:**

1. The Render-hosted WSP Pitch Builder URL stays live
2. Pilot CM Champions use the 3 live storyboards (Value Review · Restart · Switch-to-5%)
3. You handle the operational issues in `BRIAN_RUNBOOK.md`
4. You do NOT make decisions Faizan should make on return:
   - No license procurement
   - No new CM Champion additions to the pilot
   - No code changes (storyboard edits, new variants, etc.)
   - No Sophie-handoff before Faizan returns
5. **You do not contact Faizan.** Anything Faizan-level gets parked in `#wsp-pilot` Slack with the tag `[FOR-FAIZAN]` for batch triage on his return.

If something is genuinely catastrophic (the Render service is permanently dead, supplier data has leaked, the CM cohort is mutinying), escalate to Clement. **Not** Faizan.

### Sophie — owns Phase 2 (but not yet)

**Your scope for the 6 weeks:** **Nothing operational.**

- You do NOT procure Claude licenses during the leave
- You do NOT install the skill plugin with any CM
- You do NOT touch the Render URL or any deploy config
- You do NOT contact Faizan

**Your scope for week 1 of Faizan's return:**

1. Schedule a 30-min sync with Faizan
2. Walk through `SOPHIE_TRANSITION_PLAN.md` together
3. Get the answers to `SOPHIE_HANDOFF_FROM_FAIZAN.md` (Faizan should have signed it before leaving — if not, ask him then)
4. Faizan greenlights Gate 1 (license procurement). You start that week.

That's it. Read the docs during the 6 weeks if you want context. Don't act on them.

### Pilot CM Champions — operate the dashboard

**Your scope for the 6 weeks:**

1. Use the Render URL to ship pitch decks for your suppliers
2. Drop feedback in `#wsp-pilot` Slack — both wins and friction
3. If something breaks, ping Brian in `#wsp-pilot`
4. **Do not contact Faizan.** Yes, even if you have a great idea.

**What you can expect on Faizan's return:**

- A batch triage of every `[FOR-FAIZAN]`-tagged message in `#wsp-pilot`
- Personal follow-ups on any feature requests
- v1.1 storyboards (promo recap, summit, MBR, portfolio) shipping over the following weeks

### Clement & senior leadership — strategic context only

You may want updates during the leave. Brian provides those. Brian summarises:

- Number of decks shipped via the dashboard
- Feedback themes from CM Champions
- Any operational issues + how they were resolved

Brian does NOT consult Faizan to produce these summaries. He uses the audit log + Slack channel.

If a strategic decision genuinely cannot wait 6 weeks (e.g. an exec-summit deck date moves forward), Clement decides — using the v0.8.0 Render-hosted system + the 2026 Exec Summit deck shell that already ships with the dashboard. Faizan is not in the loop.

---

## Why no-contact is non-negotiable

This is medical leave. The point is rest and recovery. Every "quick question" creates cognitive load on a person whose job is to NOT think about work. Even reading a Slack notification is a tax.

The system was deliberately built to be operable without Faizan. That investment only pays off if the team actually operates it without him. One "quick question" sets the precedent for ten more.

If you are tempted to ping Faizan during the 6 weeks, ask yourself:
- Does the answer change what we do today? If no — wait.
- Is the action genuinely catastrophic and one-way-door? If no — wait.
- Have I exhausted `BRIAN_RUNBOOK.md`, `SOPHIE_TRANSITION_PLAN.md`, `DATA_SAFETY.md`, `RENDER_DEPLOY.md`, and `HOW_TO_USE.md`? If no — read them.

The answer is essentially always "wait."

---

## What happens in week 1 of Faizan's return

Day 1:
- Faizan reads `#wsp-pilot` Slack from oldest to newest
- Triages every `[FOR-FAIZAN]` message into: ship-it, queue-it, decline
- Quick 1:1 with Brian (15 min) to learn what broke + how he fixed it
- Quick 1:1 with Sophie (30 min) to greenlight Gate 1

Day 2-5:
- Phase 2 Gate 1 starts (Sophie drives, Faizan unblocks)
- Faizan starts shipping the v1.1 storyboards from `ROADMAP.md`
- One v1.1 storyboard per week becomes the cadence

By the end of return-week 4:
- All 4 v1.1 storyboards live in the dashboard
- All pilot CM Champions have Claude licenses + a paired install session
- Sophie owns Phase 2 steady-state

---

## Out-of-bounds for the leave period

A list of things that will NOT happen during the 6 weeks, with explicit "wait for Faizan" tagging:

| Thing | Status |
|---|---|
| New storyboard added to dashboard | Wait for Faizan |
| Claude Code license procurement | Wait for Faizan |
| Wayfair Anthropic enterprise agreement | Wait for Faizan + procurement |
| New CM Champion added to pilot | Wait for Faizan |
| Looker Studio direct-read integration | Wait for Faizan |
| Slack webhook send-to-SRM | Wait for Faizan |
| Migration off Render | Wait for Faizan |
| EURTA NART internal-tool integration | Wait for Faizan |
| Vercel / Next.js rewrite | Wait for Faizan |
| BigQuery integration | Wait for Faizan |
| v1.1 storyboards | Wait for Faizan |
| Sunset of the Render URL | Wait for Faizan |
| Rotating the dashboard password | Brian can, if leak suspected |
| Restarting the Render service | Brian can, see runbook |
| Telling a CM their deck won't ship via the tool | Brian can, "hold until Faizan back" |
| Triaging a `[FOR-FAIZAN]` Slack message | Brian can park, not action |
| Producing leadership update summaries | Brian does, no Faizan input |

---

## Sign-off

Brian: _______________________________ Date: __________ (acknowledges the no-contact rule)

Sophie: ______________________________ Date: __________ (acknowledges Phase 2 waits)

Clement (cc'd): ______________________ Date: __________ (acknowledges escalation goes through Brian, not Faizan)

Faizan: ______________________________ Date: __________ (signs off the day leave starts)
