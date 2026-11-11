---
name: relative-multiples
description: >-
  Build a peer relative-valuation ("relative multiples" / trading comps) sheet for a
  subject company against its listed peers — every EV multiple (EV/Revenue, EV/Gross
  Profit, EV/EBITDA, EV/EBIT, EV/CFO, EV/FCFF, plus sector KPI multiples like EV/Sample or
  EV/Patient) and every equity multiple (P/E, P/B) — per year, with a median and a base-year
  (FY-end share price) snapshot, in the analyst's peer-sheet format. Trigger whenever the
  user asks for "relative multiples", "relative valuation", "peer multiples", "trading
  comps", "peer comparison of multiples", to "update the relative-multiple / peer-valuation
  sheet", or names a company and asks how its P/E, EV/EBITDA etc. compare with peers, or to
  add a new year to a peer-valuation model. This is trading/peer multiples — NOT precedent
  transactions / deal comps, which is the separate "transaction-multiples" skill. Runs on an
  existing company model: the subject's historical numbers already live in the linked model;
  the peers' numbers you gather yourself.
license: "Proprietary. © 2026 Finnacle Institute. All rights reserved. See LICENSE."
---

> **Curated by Vastav Parikh & Yash Master for Finnacle Shah Classes.**  
> Intellectual property of Finnacle Institute. © 2026 Finnacle Institute. All rights reserved.  
> Keep this notice intact in any copy or modified version of this file.

# Relative Multiples (peer trading comps)

Compare a **subject company** against its **listed peers** on the multiples the market is
actually paying, year by year, so the reader can see who trades rich or cheap and on which
metric. The output is a two-panel block per company (multiples + median on the left, the
underlying data on the right), a summary median table, and a **base-year snapshot** taken at
the fiscal-year-end share price.

## The operating model (important — this shapes the whole task)

This skill runs **on top of an existing company model**. The subject company's historical
financials (revenue, margins, cash flows, book value, KPIs) already exist in the analyst's
linked workbook — the "Industry Mastersheet" / model the peer sheet references. Your job is:

1. **Subject** — its numbers are already there (linked). You pull its base-year figures and
   its through-cycle median from that model; you don't re-source its history.
2. **Peers / competitors** — their numbers are **NOT** in the model. You gather them yourself
   from public filings (this is the bulk of the work).
3. Compute the multiples and assemble the sheet.

When you don't have the linked model in hand (e.g. running standalone), you can only hardcode
whatever historical values are cached in the sheet and add the new year — say so plainly.

## The multiples

Standard, computed off the same enterprise/equity value each year:

```
Market Cap = FY-end Share Price × Shares Outstanding / 1e7      (₹ Crore)
Enterprise Value (EV) = Market Cap + Debt − Cash & Investments
EV multiples : EV / {Revenue, Gross Profit, EBITDA, EBIT, CFO, FCFF}
KPI multiples: EV / {sector KPI}  — e.g. EV/Sample, EV/Patient (diagnostics); swap per sector
Equity       : P/E = Market Cap / PAT ;  P/B = Market Cap / Book Value of Equity
Median       : MEDIAN across the years that have data
```

The KPI multiples are **sector-specific** — the whole point of comparing operational scale.
Diagnostics uses EV/Sample (tests) and EV/Patient; a retailer would use EV/Store, a telco
EV/Subscriber, a hospital EV/Bed. Infer the right KPI(s) from the subject's disclosures.

## Workflow

### 1. Read the existing sheet and scope
Open the peer-valuation workbook. Identify the **subject**, the **peer set**, the **multiples
and KPIs** already in use, the **year columns**, and the **base year** to add. Reverse-engineer
the convention from a populated column so your new year is consistent (see
`references/methodology.md`). Confirm the peer set and the base year with the user if adding a
new year to an existing model.

### 2. Gather the peers' base-year data (the real work)
For each peer, source the base fiscal year (consolidated, same basis as the model):
Revenue, Gross Profit, EBITDA, EBIT, CFO, FCFF, PAT; the sector KPI counts; total Debt; Cash &
investments; Book Value of equity; **Shares Outstanding at FY-end**; and the **FY-end (31-Mar)
closing share price**. Fan out one research agent per peer if subagents are available.
`references/sourcing.md` has the hierarchy and the traps.

### 3. Handle the three things that break this analysis
These are the recurring failure modes — check every one (details in `references/methodology.md`):

- **Bonus issues / splits.** A peer that did a bonus in the base year has a share count and
  price on a *new* basis. The model's historical prices/shares are usually **retro-adjusted**
  for the split — so your base-year price and share count must be on that same adjusted basis,
  or market cap is wrong by the split factor. This is the single most common error.
- **Definition consistency.** The model may define "Revenue" as Total Income (incl. other
  income) for one peer and revenue-from-operations for another, or put other income and
  pre-exceptional items into EBITDA. Match **each peer's own historical basis in the model**,
  not the textbook definition. Reconcile your base-year figure to the prior-year trend before
  trusting it.
- **The FY-end price.** The exact 31-Mar close (especially post-bonus) is often the hardest,
  least reliable input and it drives every multiple. Put Share Price in a **blue input cell**
  so the user can drop in the exact close; use your best-sourced value as a clearly-flagged
  placeholder and say it's an estimate.

### 4. Build the sheet
Use the bundled engine — it writes live formulas over the data cells, so overwriting a share
price recomputes everything, and it matches the peer-sheet format:

```bash
python scripts/build_relative_sheet.py data.json output.xlsx
python <xlsx-skill>/scripts/recalc.py output.xlsx 60      # verify 0 errors
```

Assemble `data.json` per `assets/example_data.json` (schema documented at the top of the
script). The engine builds each two-panel block, computes EV and all multiples as formulas,
extends the median, and emits the base-year snapshot table. Historicals are hardcoded (from
the model / cache); the base year is sourced; share price, shares, debt, cash and book value
are blue inputs.

The sheet is **self-contained** (no external links) so it verifies and opens anywhere. If the
user instead wants it kept live-linked to their mastersheet, add only the new base-year column
to their workbook and leave the historical link formulas untouched (note: openpyxl drops
cached values on save, so the links only resolve on their machine where the model is present).

### 5. QC and deliver
Recalc (0 errors), recompute 2–3 multiples by hand, render to check the format, and read back
the base-year column. Deliver the file and, if the source is on the user's disk, write it back.
Then report clearly: the base-year multiples, and **every constraint** — estimated prices,
definition mismatches, bonus adjustments, and any peer figure that came from a secondary
source and should be confirmed against the audited filing.

## Reference files
- `references/methodology.md` — multiple definitions, the EV convention, the base-year price
  rule, and the bonus / definition-consistency checks in detail.
- `references/sourcing.md` — where to find each peer figure (filings, presentations, KPIs) and
  the common gaps.
- `assets/example_data.json` — a worked config the engine consumes (Thyrocare vs Dr Lal /
  Metropolis), doubling as the schema reference.
- `scripts/build_relative_sheet.py` — the build engine. Run it; don't re-implement the layout.
