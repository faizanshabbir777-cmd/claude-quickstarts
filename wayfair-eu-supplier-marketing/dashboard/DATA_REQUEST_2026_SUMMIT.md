# 2026 EU Exec Summit · Data Request

The deck shipped in v0.6.2 (`EU_Exec_Summit_2026.pptx`) is built from the **2025 file as the baseline** — `2024 WSC` and `2025 Ad Target ($)` columns are real, but where 2025 is "current year now nearly done," we need 2025 actuals (not targets) to make the 2026 ask credible.

Forward this memo to whoever owns the data pull (BI / analyst team / the SRM ops lead) so the data is ready when the deck needs to ship for the actual exec summit.

---

## What's in the 2025 file we already have

From `Ads_Target_Suppliers__Exec_Summit_2025.xlsx`:

| Column | Source | What it tells us |
|---|---|---|
| SuID, Supplier, Marketing Category, SRM, SAM, Tier | Snapshot, accurate | Supplier identity + ownership |
| 2024 WSC ($) | Closed year | Baseline |
| 2024 Total Ad Spend ($) | Closed year | What was spent |
| 2024 % of WSC | Computed | Spend intensity at year-end |
| 2025 Ad Target ($) | Set Jan '25 | The promise made at last year's summit |
| 2025 % of WSC Target | Set Jan '25 | The intensity goal |
| WSP Status | Live | Active / Lapsed / Unacquired / Acquired |
| Wallet Balance | Live | Current ad wallet $ |
| SRM Response · Context · SAM Context | Qualitative | The political map |

---

## What we need for the real 2026 deck

### Block 1 — 2025 actuals (replace the targets)

For every SuID in the file, the same columns BUT for 2025 actuals:

- [ ] **2025 WSC (actual)** — the closed-year wholesale
- [ ] **2025 Total Ad Spend (actual)** — what was actually spent
- [ ] **2025 % of WSC (actual)** — computed
- [ ] **2025 → Target delta** — actual vs target, "did they hit it?" check
- [ ] **2025 WSP Status (year-end)** — Active / Lapsed / etc as of Dec '25
- [ ] **2025 Wallet Balance (final)** — same time-stamp

If the year isn't closed when the deck runs, use **latest YTD as a proxy** and flag the cutoff date prominently on the cover slide.

### Block 2 — 2026 targets (the new ask)

For every SuID, compute or set:

- [ ] **2026 Ad Target ($) — proposed** at 5% of 2025 WSC (default — Faizan's rule)
- [ ] **2026 % of WSC Target** — should be 5.0% for everyone unless flagged
- [ ] **2026 Target − 2025 Actual** = the open ask per supplier
- [ ] **Tier (refreshed)** — has the supplier moved up or down a tier in 2025?
- [ ] **Priority cohort** for 2026: LIFT (active under 5%) / REACTIVATE (lapsed) / ACQUIRE (Tier 1/2 unacquired)

### Block 3 — Lapse / reactivation events in 2025

To populate the "reactivation pipeline" narrative:

- [ ] For each currently-lapsed supplier: **last-active date**, **last-active spend rate**, **estimated dark days**
- [ ] For each currently-active supplier that lapsed-then-returned in 2025: **lapse event date**, **reactivation date**, **what triggered the restart**

This data lets the deck show movement — who came back, who fell out — not just snapshots.

### Block 4 — SRM ownership refresh

- [ ] Confirm SRM names for every SuID (people move, accounts move)
- [ ] Add SAM-of-record (the SAM column was sparse in the 2025 file)
- [ ] Note pending SRM transitions (who's leaving / joining / restructuring)
- [ ] Confirm the 8 Top-SRM cohort for 2026 (the deck names: Rebecca Chiang, Jo Zhang, Jemma Zhang, Jose Pinheiro, Riccardo Citera, Irene Lougiakis, Alina Jiang, Kay Stueber — refresh from current org)

### Block 5 — 2026 strategic additions

The Sheet2 list had 3,841 suppliers — but for 2026 we want a focused hunt list:

- [ ] **Top 200 unacquired Tier 1 SUs** by 2025 WSC (the acquisition cohort)
- [ ] **Top 100 lapsed SUs** by 2024 WSC (the reactivation cohort)
- [ ] **Top 50 over-performing active SUs** by 2025 wholesale-per-£1 (the case-study cohort for the summit)

---

## What we DON'T need (deliberately scoped out)

- Individual SKU-level data for 3,841 suppliers (only for the case-study cohort)
- Pre-2024 history (the arc starts at 2024 baseline)
- Cross-region data (EU only — the deck is scoped to UK + APS EU + CTM Poland)
- Anything from non-WSP advertising products (no Display, no Brand, just Sponsored Products)

---

## File format expected

CSV or XLSX with these columns, one row per SuID:

```
SuID, Supplier, Marketing Category, SRM, SAM, Tier,
2024_WSC, 2024_Ad_Spend, 2024_pct_WSC,
2025_WSC_actual, 2025_Ad_Spend_actual, 2025_pct_WSC_actual,
2025_Ad_Target, 2025_pct_WSC_Target,
2026_Ad_Target_proposed, 2026_pct_WSC_Target,
WSP_Status_2024_year_end, WSP_Status_2025_year_end,
Wallet_Balance_current,
Priority_Cohort_2026,
SRM_Response, SRM_Context, SAM_Context, Notes
```

Drop the file in `dashboard/data/exec_summit_2026.xlsx` (we'll create the folder when the file arrives). The deck builder will read it as-is.

---

## Who to send this to

| Person | Why |
|---|---|
| **The SRM ops lead** | Owns the supplier-status data (Active / Lapsed / Unacquired) |
| **Hadi Ismail or whoever owns SAM context column** | Owns the qualitative notes per supplier |
| **The BI / analyst on the EU SAM team** | Pulls 2025 actuals from Looker / BigQuery |
| **Faizan when back from leave** | Sign-off on 2026 targets + priority cohorts |

---

## Timing

- **Week 1 of Faizan's return**: kick off the data pull
- **Week 2 of Faizan's return**: 2026 deck ships with real numbers
- **Q1 2026**: exec summit happens, deck presented

If the exec summit lands earlier than Faizan's return: Brian uses the **v0.6.2 deck as-is**, marking it as "2025 baseline · 2026 ask is preliminary" on the cover. That's enough for a placeholder conversation; it won't be enough for a commitment conversation.
