> **Curated by Vastav Parikh & Yash Master for Finnacle Shah Classes.**  
> Intellectual property of Finnacle Institute. © 2026 Finnacle Institute. All rights reserved.  
> Keep this notice intact in any copy or modified version of this file.

# Sourcing the peers' base-year data

You gather the peers yourself (the subject comes from the linked model). Source the base fiscal
year on a **consolidated** basis, matching the model's basis. Primary-first, one link per figure,
flag anything undisclosed rather than guessing.

## Where each figure lives
- **Revenue, EBITDA, EBIT, PAT, D&A**: FY results press release / investor presentation, then the
  annual report P&L. Cross-check EBITDA against Screener/StockAnalysis but anchor on the filing.
- **Gross Profit**: Revenue − cost of materials/reagents consumed. The materials line is usually
  only in the audited P&L note, not the press release — if only 9M is disclosed, pro-rate and flag.
- **CFO, Capex**: consolidated cash-flow statement (annual report / results filing). Investing
  outflow ≠ capex (it includes investments and acquisitions) — take the "purchase of PP&E" line.
- **FCFF**: rarely disclosed. Either compute (EBIT×(1−t) + D&A − capex − ΔNWC) if you have the
  parts, or leave blank — do not fabricate.
- **Total Debt & Cash/Investments**: consolidated balance sheet. Note the lease-liability split.
- **Book Value of equity**: total equity attributable to owners (exclude minority interest unless
  the model includes it).
- **Shares Outstanding (FY-end)**: from the results filing / BSE-NSE shareholding — on the
  post-bonus/split basis (see methodology check #1).
- **FY-end share price**: the 31-Mar (or last trading day of the fiscal year) NSE/BSE close,
  post-bonus. **Best source: Yahoo Finance historical data.** Yahoo's data API is robots-blocked
  to headless fetchers, but the human-facing history page works via browser automation (Claude in
  Chrome): open `https://finance.yahoo.com/quote/<TICKER>.NS/history/` and read the daily table.
  Take the **Close** (not Adj Close) on the last trading day of the fiscal year — Yahoo already
  reflects bonuses/splits as a "N:1 Stock Splits" row and shows post-adjustment raw closes from
  that date, so the close is on the same bonus-adjusted basis as a retro-adjusted model series.
  If 31-Mar was a market holiday, use the prior trading day and note it. Confirm the split factor:
  a 1:1 bonus shows as "2:1", a 3:1 bonus as "4:1" (Yahoo counts total post/pre shares).
- **Operating KPIs** (samples/tests, patients, stores, subscribers, beds…): investor presentation
  — managements report these prominently. Match the unit the model uses (e.g. crore).

## Sources, in order
1. Company FY / Q4 results press release and **investor presentation** (IR page) — best for
   EBITDA, KPIs, and management-stated figures.
2. **Annual report** audited statements — for the materials line, cash flow, and BS detail.
3. Exchange filings (BSE/NSE) — results, shareholding, bonus/split intimations.
4. Aggregators (Screener, StockAnalysis) — fast cross-checks; label as secondary and verify the
   ones that matter (D&A, capex, lease split) against the filing.

## Common gaps (expected — flag, don't fabricate)
- Gross-profit / materials split (peers often disclose only totals).
- FCFF (not a reported line).
- Exact FY-end post-bonus close (search rarely nails a specific past date).
- Non-current investments classification (affects the cash & investments total).
Report each gap in the delivery summary so the reader knows which cells to confirm.
