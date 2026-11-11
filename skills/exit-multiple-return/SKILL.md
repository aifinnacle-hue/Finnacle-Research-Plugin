---
name: exit-multiple-return
description: Build an exit-multiple (exit P/E or EV/EBITDA) holding-period return analysis with a sensitivity table: entry vs exit valuation, future forecast metric, gain and CAGR at exit, and a multiple x growth sensitivity grid. Use when the user asks for an "exit PE analysis", "exit multiple sensitivity", "holding-period return", "3-year exit CAGR/IRR", or "what return if I exit at Nx".
license: "Proprietary. © 2026 Finnacle Institute. All rights reserved. See LICENSE."
---

> **Curated by Vastav Parikh & Yash Master for Finnacle Shah Classes.**  
> Intellectual property of Finnacle Institute. © 2026 Finnacle Institute. All rights reserved.  
> Keep this notice intact in any copy or modified version of this file.

Build an **exit-multiple holding-period return** analysis on a dedicated sheet: buy at today's price, exit at year N at an assumed multiple, and show the gain / CAGR, plus a **multiple × growth sensitivity** grid. Links to the workbook's forecast; only assumptions are hard-coded. Formatting matches the other model sheets.

## Step 1 — Elicit / confirm
- **Multiple type**: exit P/E (equity, base = adjusted PAT) or exit EV/EBITDA (firm, base = EBITDA). **Always use the ADJUSTED metric** (e.g. adjusted PAT with ESOP added back), consistent with the rest of the model.
- **Exit multiple** value (e.g. 42×) — a blue/yellow input.
- **Exit year / holding period** (e.g. FY29 = 3 years) and the number of period columns (default: 1…N to the exit year; don't add years beyond the explicit forecast unless asked).
- **CMP** and **share count** (link a DCF/details sheet).
**Done when:** multiple type, exit multiple, horizon, CMP and shares are settled.

## Step 2 — Entry block
- **Current / TTM metric** = latest actual adjusted metric (link the model).
- **Shares**, **CMP** (link). **Market cap = CMP × shares** (consistent units — cr).
- **Entry multiple = market cap ÷ current metric** (P/E) or **EV ÷ EBITDA** (EV case; EV = market cap + net debt).
- **Implied metric growth** = (exit-year metric ÷ current metric)^(1/years) − 1 (a derived CAGR for reference and for the sensitivity axis).
**Done when:** entry multiple and implied growth compute.

## Step 3 — Future metric & exit value (per holding year 1…N)
- **Future metric each year = the ACTUAL forecast** from the model (link FY+1, FY+2, … adjusted PAT/EBITDA) — **do NOT CAGR-extrapolate** the explicit years.
- **Exit market cap (year k) = future metric(k) × exit multiple.**
- **Gain = exit market cap − entry market cap**; **Gain % = gain ÷ entry**.
- **CAGR (year k) = (exit market cap ÷ entry market cap)^(1/k) − 1.**
(EV case: convert exit EV back to equity — exit EV − net debt — before the per-share/return step.)
**Done when:** each holding-year column shows future metric, exit value, gain, gain %, CAGR — no extrapolated years beyond the forecast.

## Step 4 — Sensitivity table (multiple × growth → CAGR)
- Rows = **exit multiple** (base ±2 steps, e.g. 36/39/42/45/48). Columns = **metric growth** (base implied growth ±2 steps).
- Each cell = holding-period CAGR at that (multiple, growth): `((current_metric × (1+growth)^years × multiple) / entry_market_cap)^(1/years) − 1`. Lock row/col refs so one seed copies across.
- **Centre cell must equal the base-case CAGR** (because base growth = the implied CAGR that reproduces the actual exit-year metric).
- Add a 3-colour scale (red = low → green = high).
**Done when:** centre ties to the base CAGR; colour scale applied.

## Step 5 — Formatting (convert any pre-built template to our standard)
Navy #1F4E78 headers (white bold); assumption inputs (exit multiple) blue #0000FF on yellow #FFFF00; cross-sheet links green #008000; calculations black; multiples `0.0"x"`; percentages 0.0%; currency magnitude decimals (|x|≥100→0dp, 10–100→1dp, <10→2dp). Keep any existing border structure; replace the template's own fill scheme with the above.
**Done when:** colour-coding and number formats pass a read-back and match the other sheets.

## Guardrails
- **Adjusted metric everywhere** (PAT or EBITDA with the same add-backs as the model).
- **Future metric = linked actual forecast**, not a smoothed CAGR, for the explicit years.
- **Link, don't hardcode** (quote sheet names with `&`/`-`/spaces: `'P&L'!K96`, `'Short DCF'!I8`).
- Verify no #REF!/#VALUE!/#DIV-0!/#NAME? and that the sensitivity centre = base CAGR.
- Interpretation to surface: compare entry vs exit multiple and the resulting CAGR against the cost of equity — a CAGR ≈ Ke means roughly fair value.
