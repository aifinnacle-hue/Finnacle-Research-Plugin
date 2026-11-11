> **Curated by Vastav Parikh & Yash Master for Finnacle Shah Classes.**  
> Intellectual property of Finnacle Institute. © 2026 Finnacle Institute. All rights reserved.  
> Keep this notice intact in any copy or modified version of this file.

# Methodology: multiples, EV convention, and the three checks

## The multiple set

| Multiple | Formula | Notes |
|---|---|---|
| EV / Revenue | EV ÷ Revenue | match the model's revenue definition (see below) |
| EV / Gross Profit | EV ÷ Gross Profit | GP = Revenue − cost of materials/reagents consumed |
| EV / EBITDA | EV ÷ EBITDA | check whether the model's EBITDA includes other income |
| EV / EBIT | EV ÷ EBIT | EBIT = EBITDA − D&A |
| EV / CFO | EV ÷ cash from operations | often blank for peers historically — fill where disclosed |
| EV / FCFF | EV ÷ free cash flow to firm | frequently not disclosed; leave blank unless computable |
| EV / <KPI> | EV ÷ operating KPI | **sector-specific** (EV/Sample, EV/Patient, EV/Store, EV/Subscriber…) |
| P/E | Market Cap ÷ PAT | equity multiple — off Market Cap, not EV |
| P/B | Market Cap ÷ Book Value of equity | equity multiple |

**Median** per company is `MEDIAN` across the years with data — the through-cycle read that the
summary table compares across peers. The **base-year snapshot** shows each company's base-year
multiple (at FY-end price) — the "where does it trade now" read.

## The EV / equity-value convention

```
Market Cap = FY-end Share Price × Shares Outstanding / 1e7      (₹ Crore)
EV         = Market Cap + Total Debt − Cash & Investments
```

- **Debt**: include lease liabilities (Ind AS 116) if the model treats them as debt — check a
  historical column. Many diagnostics names are financial-debt-free; their "borrowings" line is
  purely leases.
- **Cash & Investments**: cash & equivalents + current investments + non-current investments,
  on the same definition the model uses historically (it may be a specific sum of BS lines).
- **EV multiples** use EV; **P/E and P/B** use Market Cap (equity value). Don't mix them.
- If the model pulled EV from a linked balance sheet historically, keep those historical EVs as
  values and compute only the new year's EV from Market Cap + Debt − Cash.

## The three checks that break this analysis

### 1. Bonus issues, splits, and share-count basis
A peer that did a bonus/split in or before the base year has its share count and price on a new
basis. Analyst models almost always **retro-adjust the entire historical price and share-count
series** for the split so the market-cap series is continuous. Therefore:
- Your base-year **Shares Outstanding** must be the post-action count, and the **FY-end price**
  the post-action (ex-bonus) price — both consistent with the model's adjusted series.
- Sanity check: base-year Market Cap should sit on a smooth line with prior years. A 2×/3×/4×
  jump or drop is the tell that price and shares are on mismatched bases.
- Example failure: a 1:1 bonus doubles shares; if you pair the doubled share count with the
  pre-bonus price, Market Cap doubles and every multiple is 2× too high.

### 2. Definition consistency across peers
The model's line definitions are whatever the analyst chose, and they are not always uniform:
- "Revenue" may be **Total Income** (revenue-from-ops + other income) for one peer and
  **revenue-from-operations** for another.
- "EBITDA"/"EBIT" may **include other income** and be stated **before exceptional items**.
Match **each peer's own historical basis**, cell by cell, not the textbook definition — pull the
prior-year value the model uses and confirm your base-year figure continues that series. When
your sourced number and the model's basis disagree, reconcile before writing (e.g. add back
other income to hit the model's EBITDA). Flag any residual mismatch to the user.

### 3. The FY-end share price
This single input drives Market Cap and therefore every multiple, and the exact 31-Mar close —
especially just after a bonus — is often the least reliable figure you can find via search.
- Treat Share Price as a **blue input cell**; the engine already does. Put your best-sourced
  value in as a placeholder and tell the user it's an estimate to confirm against the NSE/BSE
  bhavcopy for that date.
- If 31-Mar was a market holiday, use the last trading day of the fiscal year and note it.

## Reconciling to the model when the linked file isn't attached
If you only have the peer sheet (not the mastersheet it links to), the historical cells hold
cached values only. Hardcode those cached values to make the sheet self-contained, add the base
year, and state that the historical link was replaced with its last cached values. Do not
recalc a workbook that still contains external links to a missing file — LibreOffice will wipe
them (see the xlsx skill's external-link warning).
