---
name: implied-multiple-v2
description: "Build an implied valuation multiple (P/E or EV/EBITDA) using the EVA / franchise-value framework: Implied Multiple = Steady-State Multiple + Future-Value-Creation Multiple, over an explicit forecast into a distant terminal year. Use when the user asks for an \"implied PE\", \"implied EV/EBITDA\", \"implied multiple\", or a value-creation/EVA-based multiple. Includes an optional mid-forecast (e.g. 3-year exit) implied multiple."
license: "Proprietary. © 2026 Finnacle Institute. All rights reserved. See LICENSE."
---

> **Curated by Vastav Parikh & Yash Master for Finnacle Shah Classes.**  
> Intellectual property of Finnacle Institute. © 2026 Finnacle Institute. All rights reserved.  
> Keep this notice intact in any copy or modified version of this file.

Build an **implied valuation multiple** on a dedicated sheet using the EVA / franchise-value framework:

**Implied Multiple = Steady-State Multiple + Future-Value-Creation Multiple.**

Everything links to the workbook's forecast (Top-Down / P&L / DCF); only elicited assumptions are hard-coded. Formatting matches the other model sheets.

## The metric trio (P/E vs EV/EBITDA) — pick per the user
The maths is identical; only the trio swaps:
| | **Implied P/E** (equity) | **Implied EV/EBITDA** (firm) |
|---|---|---|
| Base metric | PAT (adjusted) | EBITDA |
| Return | ROE | ROIC |
| Discount rate | cost of equity (Ke) | WACC |
| Reinvestment base | PAT | NOPAT |
| Reinvestment rate | retention | reinvestment rate |
Everything below says "metric / return / r / earnings / retention" — substitute the chosen trio.

## Step 1 — Scope & inputs (ask FIRST)
- **Which multiple** — P/E or EV/EBITDA (or EV/Sales: base = sales, return = ROIC).
- **Base year** for the multiple (e.g. FY26) and the **terminal/last forecast year** (e.g. FY52).
- **Optional mid-forecast exit** (e.g. a 3-year exit at FY29) — build a second table if wanted.
- Confirm the **source cells**: base-metric series, return series (ROE/ROIC — link the Top-Down/forecast; explicit through the detailed years, tapered after), discount rate (link a DCF's Ke/WACC or ask rf/beta/market return/premium and compute), and **perpetual growth g**.
Ask only what's missing/unclear.
**Done when:** trio, base year, terminal year, and all source cells are settled.

## Step 2 — Value-creation driver rows (one column per year, base→terminal)
1. **Metric** (PAT or EBITDA) — link the forecast.
2. **Metric growth %** — YoY.
3. **Return %** (ROE or ROIC) — link the forecast.
4. **Retention / reinvestment rate = current-year growth ÷ current-year return** (the same year's metric growth divided by that year's return).
5. **Reinvestment = earnings × retention** (earnings = PAT for P/E, NOPAT for EV).
6. **Economic Value Creation (EVC) = reinvestment × (return − r)**.
7. **Discount factor** = `1/(1+r)^(COLUMN(year)−COLUMN(base_year))` — the **base year's exponent is 0** (no discount), not 1.
8. **PV of EVC** = `EVC × discount_factor / r` — i.e. `[EVC_n /(1+r)^n] / r`: discount the year's EVC to today, then capitalise it as a perpetuity (that year's value creation is assumed to persist forever from that year on).
**Done when:** rows fill across all years.
**Watch-out:** in a high near-term-growth year, current-year growth can exceed the return, giving retention > 100% (reinvestment > earnings) and an inflated base-year EVC — flag this to the user and offer to cap retention at 100% or exclude the base year from the EVC sum.

## Step 3 — Implied-multiple table (long window, base year)
1. **Discount rate (r)** — Ke or WACC.
2. **Terminal growth (g)**.
3. **Steady-state value** = base-year metric × (1+g)/(r−g).
4. **Steady-state multiple** = steady-state value ÷ base metric  (= (1+g)/(r−g)).
5. **Future value creation (FVC)** = Σ PV of EVC across the explicit forecast (base year included, exponent 0).
6. **Future-value multiple** = FVC ÷ base metric.
7. **Total value** = steady-state value + FVC.
8. **Implied multiple** = total value ÷ base metric  (= steady-state multiple + future-value multiple).
**Done when:** implied multiple = SS multiple + FV multiple, and ties to Total ÷ base metric.

## Step 4 — Mid-forecast (exit) implied multiple — only if requested
Use a **separate discount-factor row and a separate PV-of-EVC row** — do NOT scale the long-window numbers. The mid-forecast discount factor uses `1/(1+r)^(COLUMN(year)−COLUMN(new_base))` with the new base year's exponent = 0. Steady-state value uses the **new base year's** metric. FVC(exit) = Σ the mid-forecast PV-of-EVC **from the year after the base onwards**. Implied exit multiple = (steady-state value + FVC) ÷ new-base-year metric. Mirror the long-window table's layout exactly.
**Done when:** the exit table stands on its own discount rows and the multiple = total ÷ new-base metric.

## Step 5 — Formatting
Workbook standard: navy #1F4E78 headers (white bold); assumption inputs blue #0000FF on yellow #FFFF00; cross-sheet links green #008000; calculations black; forecast-column band #DDEBF7 with a navy left-border divider at the base year; multiples as `0.0"x"`; percentages 0.0%; magnitude decimals on currency (|x|≥100→0dp, 10–100→1dp, <10→2dp); grey-italic meta rows (growth, retention, discount factor).
**Done when:** number formats and colours pass a read-back and match the other sheets.

## Guardrails
- **Retention/reinvestment = current-year growth ÷ current-year return.** Never hardcode.
- **Steady-state multiple = (1+g)/(r−g)** — sanity-check it equals steady-state value ÷ base metric.
- **Discount-factor base-year exponent = 0.** PV of EVC = EVC ÷ r × discount factor.
- **Link, don't hardcode** (quote sheet names with `&`/`-`/spaces: `'Top-Down'!C26`, `'Short DCF'!B9`).
- Verify no #REF!/#VALUE!/#DIV-0!/#NAME?; if a return or growth series is missing for any year, ask rather than invent.
- Note that a high discount rate compresses the steady-state multiple sharply (e.g. (1+g)/(r−g) is small when r is high).
