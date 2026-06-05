# How to explain the WSP skill — by audience

Use the right framing for the right room. Same artefact, different angle.

---

## The 30-second explainer (Slack DM, walking-to-coffee length)

> *"I codified our WSP pitch playbook into a Claude Code skill. Same visual register as my TuttiBambini deck. A SAM picks a storyboard, answers four questions, and the skill builds the deck. Same playbook, every time. Want a 90-second video?"*

That's it. Don't say more. The video does the rest of the work.

---

## The 2-minute explainer (1:1 conversation length)

> *"Here's the problem we have: every SAM builds pitch decks differently. Slide count varies, brand rules drift, GRS occasionally leaks into a supplier-facing deck. Onboarding a new SAM takes weeks of mentoring.*
>
> *I built a Claude Code skill that encodes our playbook. Two things make it work:*
>
> ***Storyboards*** *— a named scaffold per pitch type. Value review. Restart pitch. Switch to 5%. Promo recap. Each storyboard fixes slide count, eyebrow numbering, layout per slide, and the title pattern. The agent fills the scaffold; it does not invent structure.*
>
> ***The TuttiBambini baseline*** *— the visual register is anchored to my own deck for Tapanshi, used successfully in-meeting in spring '26. Serif italic hero numbers, lavender + deep purple + gold cards, green delta pills, italic takeaway sentences. Every deck the skill builds matches that look.*
>
> *Result: half-day pitch builds compress to minutes. Brand rules are un-skippable. The output is indistinguishable from the deck I built by hand.*
>
> *Asking for a 2-week pilot with 3-4 SAMs when I'm back from leave. The basic version ships this week."*

---

## The 10-minute explainer (formal demo, sit-down review)

Use the 90-second video as the opener. Then walk through:

1. **The problem** (2 min) — show the WSP MBR slide 8 (your team's drag list). "These are 12 suppliers we should pitch this month. At current pace, that's 5-6 days of deck-building. Quality varies. New SAMs need someone to review their decks before they go out."

2. **The TuttiBambini baseline** (2 min) — open your Tapanshi deck. "This is what good looks like. Conversational titles. Serif italic heroes. Lavender + gold. Italic takeaway sentences. Calendar visualisation. This is what every supplier deck should look like."

3. **The skill in action** (3 min) — live demo from the storyboard. `/wsp Monty Trading UK · WSP value review · April 2026`. Walk through the kickoff questions, the mid-deck checkpoint, the output. Show the storyboard markdown — *"this is the scaffold the agent fills."*

4. **Why it doesn't drift** (2 min) — open `storyboards/value-review-variant-b.md`. Read the YAML frontmatter and the per-slide scaffold. "The agent does not pick slide count. Does not pick layout. Does not pick title. It picks from a list of pre-written title sentences. The structure is fixed."

5. **The ask** (1 min) — pilot with 3-4 SAMs for 2 weeks when I'm back. Honest about what's not built yet (some layout render functions, real Looker integration, Variant D Custom). Pilot's job is to harden it.

---

## One-liner for skeptics

> *"Generic AI writes what you ask for. A codified team playbook tells you when you're about to break a rule. Watch what happens when I tell it to put GRS on a supplier-facing slide."*

(Then run the `Watch It Refuse` demo.)

---

## Top 10 objections + responses

| Objection | Response |
|---|---|
| **"This is just AI building generic decks."** | "The skill builds from MY TuttiBambini deck — the one Tapanshi already saw work. It reproduces that visual register, not a generic AI aesthetic. Look at the receipts portfolio." |
| **"How is this different from a PowerPoint template?"** | "A template doesn't enforce rules. It doesn't ask for exact promo dates. It doesn't pause at the mid-deck checkpoint. It doesn't refuse to ship a GRS leak. The skill is a process, not a layout." |
| **"What if the agent picks the wrong storyboard?"** | "The selector decision tree is explicit. If the brief doesn't fit cleanly, the skill asks before building. It does not silently pick the closest match." |
| **"What if the data is wrong?"** | "The data-prep subagent runs a sanity check against Account Overview before any deck-building starts. Mismatches >5% are surfaced to the analyst." |
| **"What about the £-rule ask — what if the agent picks the wrong variant?"** | "The closing slide never auto-builds. The skill stops at the mid-deck checkpoint, presents a data summary, recommends a variant, and waits for the analyst to confirm with a single letter." |
| **"What if it produces something off-brand?"** | "Liberation Serif on Linux, Georgia on Mac. Brand palette hard-coded. Layouts named and fixed. Run the QA loop on every build — if a layout breaks, we see it before the supplier does." |
| **"Won't this make SAMs lazy?"** | "It removes 90% of the mechanical work — pulling data, formatting slides, writing the same takeaway sentences. SAMs spend their time on the actual judgement: the pitch, the pillar selection, the relationship with the SRM." |
| **"Why Claude Code, not [other AI tool]?"** | "Skills are Anthropic's Agent Skills convention. Same format as the marketing-skills bundle. Versioned, reviewable, install via one command. Hard to copy this with a wrapper around a generic LLM." |
| **"What's the risk surface?"** | "The plugin reads local CSVs. Nothing leaves your laptop unless you explicitly upload. No supplier data goes to Anthropic beyond the prompt itself — and you control what's in the prompt." |
| **"Why a pilot before rollout?"** | "Two suppliers tested (Monty + Forte). Variant D Custom not battle-tested. LibreOffice QA loop is env-dependent. We harden it with 3-4 SAMs over 2 weeks, then roll out." |

---

## Cheat sheet — words to use, words to avoid

| ✅ Use these | ❌ Avoid these |
|---|---|
| "Team playbook codified" | "AI generates decks" |
| "The skill enforces" | "The AI decides" |
| "Storyboards" | "Templates" |
| "Mid-deck checkpoint" | "Human in the loop" |
| "TuttiBambini baseline" | "Generic style" |
| "QA loop" | "Hope it works" |
| "Pilot with 3-4 SAMs" | "Roll it out everywhere" |
| "Same visual register" | "AI tries to look like" |
| "Hard rules un-skippable" | "AI usually follows rules" |

---

## When someone asks "can I see it?"

Send them three files:

1. **`Receipts_Portfolio_v2.pdf`** — the proof. TuttiBambini as baseline, Monty / Forte / SU Summit as reproductions.
2. **`Demo_Storyboard_90s.pdf`** or the 90-second video — the demo.
3. **The TuttiBambini deck itself** — the gold standard the skill reproduces.

Don't send the SKILL.md, the storyboards, or the subagents to a non-technical audience. Those are for the SAM team and IT to read during the pilot.

---

## When someone asks "is this real?"

Point them at the GitHub repo. Real code. Real markdown. Real version history.

```
https://github.com/faizanshabbir777-cmd/claude-quickstarts/tree/main/wayfair-eu-supplier-marketing
```

If they ask "did you actually build this?", show them the PR commit history. Every change is timestamped and signed.
