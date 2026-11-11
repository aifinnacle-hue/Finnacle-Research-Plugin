---
name: short-dcf
description: Build a short DCF valuation (Exit-multiple + Perpetuity approaches) into a linked Excel template, driven by user-supplied assumptions. Use when the user asks for a "short DCF", a two-approach DCF, or to value a company off an existing forecast model within the workbook.
license: "Proprietary. © 2026 Finnacle Institute. All rights reserved. See LICENSE."
---

> **Curated by Vastav Parikh & Yash Master for Finnacle Shah Classes.**  
> Intellectual property of Finnacle Institute. © 2026 Finnacle Institute. All rights reserved.  
> Keep this notice intact in any copy or modified version of this file.

Build a **short DCF** valuation on a dedicated sheet, fully linked to the workbook's existing forecast (P&L / Costing / BS / Ratios / Top-Down), presenting **two approaches: Exit-multiple and Perpetuity**. Every number links to source sheets — only the elicited assumptions are hard-coded (blue-on-yellow).

## When to use
- User asks for a "short DCF", "two-approach DCF", exit-multiple + perpetuity valuation, or to value the company off the already-built forecast.
- A multi-year forecast already exists in the workbook (revenue/PAT/CFO to the exit year). If it doesn't, build/confirm that first.

## Step 1 — Elicit assumptions (ask BEFORE building)
Use an interactive question tool (batch related ones). Always ask:
1. **Starting line item / cash-flow path** — one of: start from Sales; from PBT; from CFO; **PAT + ROE + FCFE**; **NOPAT + ROIC + FCFF**. This determines the build and the retention/reinvestment logic.
2. **Risk-free rate** (e.g., 7%).
3. **Beta** — value, and source (e.g., 3-year beta from a "Beta" sheet cell). Prefer linking to the source cell.
4. **Expected market return** — value/source (e.g., average of 5-yr rolling index returns).
5. **Premium on cost of equity** — is there one (pledging / governance / other)? name + value (e.g., +4%). May be none.
6. **Exit multiple** — type (P/E or EV/EBITDA) and value (e.g., 42×).
7. **Perpetual growth rate** (e.g., 3%) and **terminal ROE (or terminal ROIC)** (e.g., 15%).
8. **Exit year / horizon** (e.g., FY29) and the **valuation/transaction date**.
9. **Line items to present** (which rows to show in the cash-flow build).
10. **Debt?** If no debt, note **FCFE = FCFF** and equity value comes straight from the discounted flows (do NOT add cash in the bridge). If debt exists, discount FCFF at WACC → EV → +cash − debt → equity.
Also ask any other assumption you judge relevant (tax rate source, share count source, tax treatment of ESOP add-backs).

## Step 2 — Cost of equity & WACC
- Cost of equity (CAPM) = risk_free + beta × (market_return − risk_free); **ERP = market_return − risk_free**.
- Add the premium if any: **Final CoE = CAPM + premium**.
- WACC = We×CoE + Wd×(after-tax cost of debt), with Wd/We from a median D/E (link to BS debt/equity). **No debt → WACC = CoE.**
- Keep **terminal WACC = the computed WACC** unless the user says otherwise.

## Step 3 — Explicit cash flows to the exit year
- Build the chosen path across the explicit years (transaction date → exit year). Typical PAT+FCFE path: PAT → (+) add-backs (e.g. ESOP if non-cash) → Adjusted PAT; and CFO → (−) net capex → (−) lease payments → **FCFF (=FCFE if no debt)**. Link PAT/CFO/capex/lease to the model.
- **Discounting:** year-fraction row from the transaction date (first period is a stub, e.g. 0.71; later = 1). Transactional flow = flow / (1+WACC)^(cumulative year fraction).

## Step 4 — Terminal value (both approaches)
- **Exit multiple:** TV = exit_multiple × exit-year metric (Adjusted PAT for P/E; EBITDA for EV/EBITDA).
- **Perpetuity:**
  - **Retention (terminal) = perpetual growth ÷ terminal ROE** (or ÷ terminal ROIC when using NOPAT). Never hardcode.
  - Grow the last-forecast **NOPAT (or PAT)** by perpetual growth **once** → grown metric.
  - **Terminal FCFF (or FCFE) = grown metric × (1 − retention).**
  - **Terminal Value = Terminal FCFF ÷ (terminal WACC − perpetual growth).**
- Discount each TV to present at the exit-year cumulative discount factor.
**PAT/ROE/FCFE vs NOPAT/ROIC/FCFF:** identical formulas — swap the metric trio. PAT↔ROE↔retention↔FCFE; NOPAT↔ROIC↔reinvestment↔FCFF.

## Step 5 — Equity value & per share
- Main flow uses the approach the user designates (default: exit multiple). Equity value = PV(explicit flows) + PV(terminal).
- **FCFE / no debt: equity value = the discounted flows directly — do NOT add cash or subtract debt.** FCFF/with debt: EV → +cash − debt → equity.
- Per share = equity value ÷ share count. Compare to CMP.
- Compute the **other** approach's per-share alongside so both are visible.

## Step 6 — Sensitivity table
- 5×5 grid: **exit multiple** across columns (median ±2 steps of the chosen increment — e.g. 42 → 36/39/42/45/48) × **WACC** down rows (base ±2 steps of ±1%).
- Each cell recomputes the main-approach per-share at that (multiple, WACC). Centre cell must equal the base case.
- Add a **3-colour scale** conditional format (red = low → white → green = high).
- If native What-If data tables aren't available, write explicit formulas per cell (lock row/col refs so one seed copies across).

## Step 7 — Template layout & formatting
Regenerate this block structure on the sheet:
- **WACC block**: risk-free, market return, ERP, beta, CoE, premium, final CoE; debt side (pre-tax Kd, tax, after-tax Kd); weights (median D/E, Wd, We, WACC).
- **Details block**: transaction date, ROE, perpetual growth, exit multiple, CMP, shares.
- **DCF block**: date row, year-fraction row, cash-flow line items → FCFF → transactional FCFF → terminal value → total.
- **Terminal blocks**: perpetuity (terminal beta, WACC, growth, ROE, retention, grown PAT, terminal FCFF, TV, per-share) and exit-multiple (multiple, exit-year metric, TV).
- **Intrinsic value**: EV / cash / debt / equity value / per share.
- **Sensitivity** grid.
Apply standard formatting: **navy #1F4E78 headers (white bold); assumption inputs blue #0000FF on yellow #FFFF00; cross-sheet links green #008000; calculations black; magnitude decimal rule (|x|≥100→0dp, 10–100→1dp, <10→2dp); zeros as "-", negatives in ()**; percentages 0.0%; multiples 0.0x.

## Guardrails
- **Link, don't hardcode.** Only the elicited assumptions are typed values; all financials link to source sheets. Quote sheet names with `&`/`-`/spaces in single quotes: `'P&L'!K92`, `'Top-Down'!C37`.
- Verify no #REF!/#VALUE!/#NAME? and that the sensitivity centre = base case before reporting done.
- Flag material divergences between the two approaches (a high WACC can make the perpetuity value far below an exit-multiple value — say so).