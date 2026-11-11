---
name: "return-matrix"
description: "Use this skill to analyze an Indian listed or pre-IPO company's profit and loss statement plus its capital efficiency and returns, from a buy-side perspective, and to answer the numbered hypothesis list handed over by growth-drivers. P&L triggers: revenue, gross margin, EBITDA margin, PAT margin or operating-cost drivers; YoY margin or cost bridges; material P&L fluctuations; structural-versus-temporary classification. Capital-efficiency triggers: asset turnover, working-capital days, financial leverage, DuPont ROE, and ROE versus ROCE versus ROIC. Also fires on 'decompose the P&L', 'explain the margin movement', 'build a margin bridge', 'analyse ROCE / ROIC / ROE', 'DuPont analysis', or 'working-capital analysis for [company]'. Do NOT use for business-model or value-chain mapping, industry sizing, growth-driver attribution, management or governance audit, or valuation."
license: "Proprietary. © 2026 Finnacle Institute. All rights reserved. See LICENSE."
---

> **Curated by Vastav Parikh & Yash Master for Finnacle Shah Classes.**  
> Intellectual property of Finnacle Institute. © 2026 Finnacle Institute. All rights reserved.  
> Keep this notice intact in any copy or modified version of this file.

# Purpose

Perform a buy-side senior-analyst-grade decomposition of an Indian company's profit and loss statement **and its capital efficiency / returns** across a user-specified period. The skill identifies, quantifies, and explains the drivers of revenue, gross margin, EBITDA margin, PAT margin, every material cost line, depreciation, and below-EBITDA items; then extends into the capital-efficiency layer — asset and working-capital turnover, financial leverage, the DuPont ROE decomposition, and ROE vs ROCE vs ROIC — and classifies each material movement as structural, temporary, mixed, or unknown.

The P&L section (Steps 1–11) is the established decomposition; the capital-efficiency section (Steps 12–17) sits on top of it and reuses P&L outputs (e.g., net margin, EBIT, NOPAT) rather than recomputing them. **Step 18 closes the loop with `growth-drivers`**: it answers, one by one, every numbered hypothesis that module handed over.

Output is evidence-backed, period-tagged, source-tiered, and suitable for an internal buy-side research note.

# Operating Mode

- **Source universe is the active project only.** Read exclusively from documents inside the project's files. Do not use web search, external aggregators, or any document not present in the project. If a needed document is absent, mark the gap as `UNKNOWN` rather than searching externally.
- **Reporting basis defaults to consolidated** unless the user specifies standalone or the company reports only on one basis. Balance-sheet and cash-flow data for the capital-efficiency layer are read on the same consolidated basis.
- **Default output format is formal HTML** following the structure in the Output section. If the user explicitly asks for Word, Markdown, or another format in chat, use that instead.

# When To Use

- Detailed P&L decomposition for an Indian listed or pre-IPO company
- Revenue / gross margin / EBITDA / PAT margin driver analysis
- YoY margin bridge or cost bridge
- Linking financial movements to KPIs, management commentary, filings, rating reports, DRHP, QIP, or investor presentations
- Structural-versus-temporary classification of cost and margin shifts
- Capital-efficiency / returns analysis: asset and working-capital turnover, working-capital days, financial leverage, DuPont ROE, ROE vs ROCE vs ROIC
- Testing the hypotheses handed over by `growth-drivers`

# When Not To Use

- Valuation-only work; standalone balance-sheet or cash-flow analysis with no P&L or returns linkage
- Generic sector summaries or company background notes
- Simple extraction of one number or one table
- Forecasting without sufficient historical data and explicit assumptions

# Required Inputs

Confirm these before running the full analysis:

1. Company name
2. Industry
3. Analysis period (e.g., FY21–FY25, FY24–Q3FY26, specific quarters)
4. Financial statements / model data containing P&L, balance-sheet, and cash-flow line items (project file). For the capital-efficiency layer specifically: gross block, net block, CWIP, total assets, inventory, trade receivables, trade payables, advances (paid and received), net worth, total debt, cash and current investments, and cash flow from operations / capex. If only P&L is available, run the P&L layer and mark the returns layer `UNKNOWN`.
5. Available source documents in the project (any of: Annual Reports, audited filings, exchange filings, concall transcripts, investor presentations, management interviews, AGM transcripts, analyst day transcripts, credit rating reports, DRHP, QIP, ValuePickr thread, Ace Equity export, user-specified materials)
6. **The `growth-drivers` hand-off**, if that module has been run: look for `<Company>_growth_handoff.json` in the project or outputs folder, or the `growth-handoff` JSON block in its HTML report. If none exists, note it and skip Step 18.
7. Any user-provided observations, KPI focus areas, or hypotheses

If company, period, or financial data is missing, ask one clarifying question before proceeding. If the user mentions specific KPIs or observations, integrate them into the standard workflow — **do not create a separate dedicated section** for them unless the user explicitly asks.

# Workflow

## Step 1 — Confirm Core Variables

State:

- Company, industry, period
- Reporting currency and units
- Annual vs quarterly basis
- Consolidated vs standalone
- Source documents reviewed (list every file from the project actually opened)
- Whether a `growth-drivers` hand-off was found, and how many H- and T-series hypotheses it contains
- Any missing inputs marked `UNKNOWN`

Read the hand-off list now, before Step 2, so the analysis gathers the evidence each hypothesis needs as it goes, rather than as an afterthought.

## Step 2 — Comparability Check (Mandatory Before Any Bridge)

Before any YoY or period comparison, test whether reported numbers are like-for-like. Check for:

- Revenue recognition changes (Ind AS 115 transitions, scheme rebates, deferred revenue)
- Gross vs net revenue presentation
- Principal vs agent presentation
- Segment reclassification or segment-definition changes
- Discontinued operations
- Acquisitions or disposals (and from which date consolidated)
- Accounting presentation changes
- Regrouping of expense lines
- New disclosure buckets
- Movement of costs between employee cost / other expense / COGS / depreciation / finance cost
- Lease-accounting impacts (Ind AS 116 transition or modifications)
- Exceptional / one-off items
- KPI-definition changes (e.g., ARPOB redefinition, same-store-sales basis change)
- Annual vs quarterly comparability issues
- Restatements or recast numbers
- Depreciation method changes (SLM/WDV), useful-life revisions, capitalization policy changes, commissioning date treatment

For each issue found:

1. State exactly what changed
2. Identify when the change began
3. List which line items / KPIs are affected
4. Explain how it distorts growth, margin, or bridge analysis
5. Note whether adjusted / recast numbers are available
6. Adjust interpretation — **do not compare unadjusted numbers as if like-for-like**

## Step 3 — Prepare Financial Base Table

For every period in scope, extract or compute: Revenue, Gross Profit, Gross Margin %, EBITDA, EBITDA Margin %, PAT, PAT Margin %, COGS / cost of materials consumed, Stock changes, Employee Benefit Expenses, Power & Fuel, Advertisement & Marketing, Logistics & Freight, Other Expenses, Depreciation & Amortization, Finance Cost, Tax, Exceptional Items, and any other material line.

Express each cost line as % of revenue. Compute YoY change (absolute and bps as % of revenue).

For every derived number, show formula, inputs, period of each input, and source tier of each input.

## Step 4 — Identify Material Movements

Flag every item where:

- A cost line or margin moves by **>1% of revenue YoY**
- ESOP expense is **>1% of revenue** in any period (check notes to accounts even if not separately disclosed in P&L; if not disclosed anywhere, flag as a **Disclosure Gap**)
- Any "other expenses" sub-line is **>3% of revenue**
- A KPI movement appears to explain a revenue, gross margin, EBITDA, or PAT margin shift

For each flagged item quantify: absolute change, change as % of revenue, bps impact on margin, YoY change, QoQ change only when useful for intra-year timing, and structural / temporary / mixed / unknown classification.

## Step 5 — Revenue Drivers

Decompose revenue using applicable drivers:

- Volume vs price split
- Segment / product / channel / geography mix
- Export vs domestic mix
- Seasonality (prefer YoY over QoQ where seasonality exists)
- One-off revenue
- Pass-through revenue
- Net vs gross / principal vs agent changes
- Revenue nature shift (licensing, royalty, service, manpower, software, platform revenue)
- Operational KPIs as applicable: Revenue/Test, ARPOB, Realization/Tonne, ASK/RASK, Occupancy, Utilization, Volume Throughput, ASP, Same-Store-Sales, footfall, basket size, take-rate, GMV, or any industry-specific KPI the company discloses

If volume / pricing split is unavailable, state `UNKNOWN`. Do not estimate.

## Step 6 — Gross Margin Drivers

Assess gross margin movement using:

- Backward integration (e.g., API for formulations player, iron-ore mine for steel, captive yarn for garments)
- Forward integration (e.g., commodity producer moving into finished products, B2B player expanding retail/distribution)
- Product / segment / geography mix
- Raw material inflation and pricing power
- Pass-through capability and pricing lag
- Contract structures (long-term, take-or-pay, formula-linked)
- Spread expansion / compression
- Procurement cycle timing
- Bulk discounts, vendor renegotiation, scale sourcing
- Inventory gains / losses, low-cost inventory benefit, commodity timing gains, inventory write-downs, FIFO/LIFO where relevant
- Revenue nature shift (services / royalty drag pulling gross margin up)
- Gross-vs-net reporting changes (revenue shrinks, GP unchanged → optical margin expansion)

**Unit economics rule:** When pass-through dynamics matter, separate margin % from absolute profit per unit. Example: if Revenue/Tonne goes 100 → 120 and COGS/Tonne goes 80 → 100, GP/Tonne is unchanged at 20 but gross margin compresses from 20% to 17%. Interpretation: unit profitability stable, margin % compressed purely by pass-through mechanics.

## Step 7 — Operating & Fixed Cost Drivers

Separate fixed, variable, semi-variable, and one-off cost movements where evidence allows.

### Employee Benefit Expenses
Drivers to consider: plant / lab / branch / store expansion, centralized vs decentralized structure, senior management hiring, ESOP expense, salesforce expansion, wage inflation, utilization changes, attrition, productivity. **Quantify ESOP separately** where >1% of revenue. Check notes to accounts disclosure even when not broken out in the P&L. If completely undisclosed, flag as Disclosure Gap.

### Power & Fuel
Captive vs purchased mix, renewable transition, energy mix changes, commodity-linked volatility, power intensity per unit of output.

### Advertisement & Marketing
Customer acquisition intensity, platform scaling, organic vs paid growth, network effects, CAC efficiency, branding investment cycles, A&P-to-revenue benchmarking across periods.

### Logistics & Freight
Rail vs road vs air mix, lead distance to market, distribution optimization, hub-and-spoke, warehousing changes, global freight rate volatility, FOB vs CIF terms.

### Capacity Utilization (cross-cutting)
Operating leverage / deleverage, ramp-up trajectory, frontloaded fixed costs, stabilization period after commissioning.

### Other Expenses
For any sub-line >3% of revenue, perform full driver analysis as above. Sub-lines to scan: legal & professional, repairs & maintenance, rent (post-Ind AS 116 should be minimal), travel, R&D expensed, CSR, provisions / bad debts, royalty, technology / IT, commission, packing, job work.

## Step 8 — EBITDA Margin Bridge

Build a period-by-period bridge:

| Driver | bps impact |
|---|---|
| Revenue / mix effect | |
| Gross margin effect | |
| Employee cost effect | |
| Other expense effect | |
| Other operating items | |
| **Net EBITDA margin change** | |

For each driver state: structural vs temporary, fixed vs variable, operating leverage vs deleverage, and sustainability commentary.

## Step 9 — Depreciation and Below-EBITDA

Depreciation: change in method (SLM/WDV), useful-life revisions, capitalization policy, commissioning of new assets, impairments. Finance cost: gross debt change, cost of debt, interest capitalization, lease interest (Ind AS 116). Tax: effective tax rate vs statutory, deferred tax movements, tax holiday expiry, 115BAA election. Exceptional items: nature, recurrence risk, cash vs non-cash.

## Step 10 — PAT Margin Analysis

Separate operating contribution (EBITDA margin) from below-EBITDA contribution (D&A, finance cost, tax, exceptional). State which is doing the work.

## Step 11 — Structural vs Temporary Classification

For each material driver, classify and justify:

- **Structural** — embedded in business model, mix, integration, or competitive position
- **Temporary** — cyclical, one-off, ramp-up, or commodity-cycle driven
- **Mixed** — partly structural, partly temporary
- **Unknown** — evidence insufficient; state what evidence would resolve it

# Capital-Efficiency Layer

The P&L is now decomposed. The capital-efficiency layer answers the next question — how efficiently the business converts that P&L into returns on the capital it employs. It reads the balance sheet and cash-flow statement on the same consolidated basis, source-tier discipline, and anti-shallow standard as the P&L, and it **reuses** P&L outputs (net margin, EBIT, NOPAT) rather than recomputing them. Analyse every metric at the same depth as the P&L drivers: quantify, link to evidence, explain the *cause*, and classify structural vs temporary.

For every ratio series in this layer — the asset-side turnovers, working-capital days, financial leverage, and ROE / ROCE / ROIC — apply the same treatment the P&L section gives margins and costs: state the **broad multi-year trend** in a Trend Summary, and additionally **flag and explain each material YoY movement** (a move large enough to change the trend or the investment read) with its driver and a structural-vs-temporary tag. Do not just tabulate the ratios — read the trend and interrogate the years that break it.

## Step 12 — Balance-Sheet Base, Conventions & Comparability

State and apply these conventions once, consistently, and disclose them in the output so every ratio is auditable and reproducible across runs.

**Working-capital definition (used everywhere below).** Core operating working capital is:

`Inventory + Trade Receivables + Advances Paid to suppliers − Trade Payables − Advances Received from customers`

This is deliberately **not** `current assets − current liabilities`. Exclude cash, current investments, borrowings, current maturities of debt, tax balances, and other non-operating current items. Advances (paid and received) are included only when material. If a component is unavailable, state it rather than defaulting to the balance-sheet subtotal.

**Averaging and the Average / Closing toggle.** Compute every turnover and return ratio on **two bases**: (i) a 2-point average denominator, (opening + closing) / 2 — the **default** view — and (ii) a **closing** (year-end) denominator. Present both: every ratio table carries an interactive **toggle above it to switch between Average (default) and Closing**, with both number sets precomputed and embedded so switching is instant and client-side. Within a given view be consistent — never mix average and closing in one series. If opening balances are unavailable for the earliest period, show closing for that period and flag it.

**Return definitions (fix and disclose; change only on user instruction):**
- **ROE** = PAT attributable to owners / average Net Worth (exclude minority interest from both).
- **ROCE** = NOPAT / average Capital Employed, where Capital Employed = Net Worth + Total Debt (include lease liabilities where Ind AS 116 is material — state the treatment). NOPAT = EBIT × (1 − effective tax rate). Using NOPAT (not EBIT) keeps ROCE post-tax and directly comparable with ROIC, so the only difference between the two becomes the capital base. CWIP sits inside capital employed but earns nothing yet, so a large CWIP temporarily depresses ROCE; show an ex-CWIP variant where CWIP is material and flag it.
- **ROIC** = NOPAT / average Invested Capital. NOPAT = EBIT × (1 − effective tax rate). Invested Capital = Net Fixed Assets (net PPE + operating intangibles / goodwill as relevant) + Core Working Capital (formula above). Invested Capital **excludes cash and non-operating investments** — this is precisely why a cash-rich company shows ROIC above ROE / ROCE.

**Balance-sheet comparability** (run before any returns bridge, extending Step 2): revaluation of PPE; goodwill / intangibles added by acquisitions (inflate capital employed and invested capital); CWIP capitalised or commissioned mid-year (asset-base timing); mid-period capital raises (QIP, rights, preferential) or buybacks that move the denominator; Ind AS 116 right-of-use assets and lease liabilities (distort asset turns, capital employed, and leverage at once); reclassification between current and non-current; change in cash / treasury-investment mix. Where a break exists, state it and prefer average denominators or an adjusted variant.

**Returns base table** — for every period compute and show (with formula, inputs, tier and period per input): Total Assets, Net Fixed Assets, Gross Block, Net Block, CWIP, Core Working Capital and its components, Net Worth, Total Debt, Cash and investments, Capital Employed, Invested Capital, EBIT, NOPAT, PAT — then the ratios in Steps 13–17.

## Step 13 — Asset Profile & Turnover Analysis

Compute per period: Total Asset Turnover (Revenue / avg Total Assets), Gross Block Turnover (Revenue / avg Gross Block), Net Block Turnover (Revenue / avg Net Block), PPE Turnover (Revenue / avg Net PPE), and Working-Capital Turnover (Revenue / avg Core WC). Working-capital **days** are analysed in Step 14.

**Read turnover through the nature of the business first — a number is only high or low relative to the model:**
- **Manufacturing-heavy:** asset turns are structurally low and margins high; PPE dominates total assets; working capital may be high or low by sub-model. Judge asset turns against manufacturing peers, not a trader.
- **Retail / trading:** margins thin, asset turns high; PPE often negligible, so working capital (inventory, receivables) is the bulk of total assets.
- Across any model, **goodwill / acquired intangibles** and **CWIP** inflate the asset base without (yet) producing revenue, and therefore **temporarily depress** total-asset and PPE turns — strip or flag them before concluding the operating asset base has become less productive.

Drivers to analyse for each turnover (quantify; classify structural vs temporary):
- **Total-asset / PPE turnover:** capacity utilisation and operating leverage; capex-cycle timing (turns dip during build / ramp, recover as revenue catches up); asset age (heavily depreciated assets flatter *net*-block turnover optically and foreshadow replacement capex); CWIP as a share of gross block; acquisition goodwill; asset-light shift (outsourcing, contract manufacturing, leasing); Ind AS 116 ROU assets; greenfield vs brownfield; demand cyclicality.
- **Gross vs net block turnover divergence:** gross-block turnover strips accumulated depreciation and is the cleaner cross-time and cross-company comparison; a wide gap (high net-block, moderate gross-block turnover) signals an old, near-depreciated asset base — high current returns but a looming capex cliff. Say so.

## Step 14 — Working-Capital Analysis

Working-capital days = Receivable days + Inventory days − Payable days (+ Advances-paid days − Advances-received days), each = component / Revenue (use COGS for inventory and payables where disclosure supports it) × 365, on the WC definition fixed in Step 12. Also compute the **cash conversion cycle**, and tie the year's WC movement to operating cash flow (CFO / EBITDA) — WC release or absorption is where reported profit does or doesn't become cash.

Analyse each component at full depth — the *reason* for a days movement matters more than the movement:

**Receivable days.**
- Customer mix is the first lens: government / PSU clients pay slowly (long, lumpy receivables); private and retail faster; export receivables run longer and carry currency risk. A rising receivable-days trend is often a mix shift toward government or exports, not deteriorating collection — separate the two.
- Credit-policy changes: extending credit to win share deliberately lengthens receivables (this is the *effect*; the strategic *choice* is a Growth-Drivers item — note the link, don't re-explain it).
- **Ageing profile** (30 / 60 / 90 / 180+ day buckets): the older the book, the higher the probability of write-off / bad debt. Rising ageing or rising ECL provisioning (Ind AS 109) signals collection stress or channel stuffing. Pull the ageing schedule from notes where disclosed.
- Bill discounting / factoring / securitisation optically lowers receivable days by moving them off balance sheet — flag if used and normalise.
- Period-end effects: a year-end sales push inflates closing receivables; prefer averages or quarterly data. Check unbilled receivables where revenue is recognised over time.

**Inventory days.**
- Distinguish **strategic** stocking from **inefficiency**: building RM inventory ahead of a commodity price rise is a margin play, not a WC problem; import lead times (China dependence) and supply-chain disruption justify buffer stock; long-gestation production (capital goods, EPC) carries heavy WIP.
- Finished-goods build ahead of a season, launch, or channel fill; SKU proliferation.
- **Obsolescence / write-down risk** (fashion, tech, perishables) and inventory ageing — a rising days trend with an ageing skew is a red flag; the same trend from deliberate low-cost stocking is not.

**Payable days.**
- Supplier bargaining power (scale earns longer credit); import LC terms; backward integration reduces external purchases and therefore payables (links to the supply-side value chain in the business-model module).
- Cash-discount vs credit trade-off: taking early-payment discounts shortens payables but lifts gross margin — read payables and margin together.
- Stretching payables flatters the cash cycle but can signal liquidity stress or strained suppliers; supply-chain / vendor financing optically extends them — flag.

**Advances.**
- **Advances received** (customer advances, milestone billing in projects / EPC, subscription prepayments) are a negative WC contributor and a sign of pricing / negotiating power and pre-funded growth; strong order-book businesses can run structurally negative working capital.
- **Advances paid** (to secure scarce RM, book capacity, or where buyer power is weak) are a positive WC contributor; read them as a signal about input scarcity or bargaining position.

Classify each WC shift structural vs temporary (a durable move into government orders raises WC structurally; a one-off year-end receivable spike is temporary). This module explains the **actual realised days and every driver behind them — value-chain causes included** (backward integration cutting payables, a channel shift lengthening receivables, a sourcing change altering inventory). Do not defer value-chain reasons elsewhere; surface them here alongside the non-value-chain ones — this is the comprehensive home for the numbers and their full causation. The business-model / value-chain module separately describes the *structural WC signature the model implies* (qualitative). Since the value-chain and growth-drivers analyses are normally run before this one, if they already exist in the project, read them as context to sharpen the causation. Where a working-capital finding bears on a growth-drivers hypothesis (e.g. "H1: share won on extended credit"), note the hypothesis ID inline here; the formal verdict goes in Step 18.

## Step 15 — Financial Leverage

The DuPont leverage multiplier is **average Total Assets / average Equity**. Alongside it, show D/E, net D/E, and interest coverage (EBIT / finance cost), plus debt-maturity and cost-of-debt context where disclosed, to judge leverage *quality*, not just level.

Drivers: debt-funded vs internally-funded capex; working-capital borrowings; cash-rich low-leverage balance sheets; Ind AS 116 lease liabilities inflating both assets and leverage; equity raises (dilution lowers leverage) and buybacks (raise it). Distinguish **productive** leverage (funding growth that earns above the cost of debt) from **risky** leverage (funding low-return assets or plugging cash burn) — the same D/E means very different things in each case.

## Step 16 — DuPont ROE Integration

Integrate the three levers:

`ROE = Net Margin (PAT / Revenue) × Asset Turnover (Revenue / avg Total Assets) × Equity Multiplier (avg Total Assets / avg Equity)`

Show the three components per period and **attribute the ROE change to the lever that moved it** — margin (profitability), turnover (asset efficiency), or leverage (capital structure). The net-margin term is already computed in the P&L section; reuse it.

Then judge **quality of ROE**: an ROE rising on margin or turnover is operating-quality; an ROE rising mainly on leverage is lower-quality and riskier. Where debt and tax are material, extend to the 5-step DuPont (tax burden × interest burden × EBIT margin × asset turnover × leverage) to separate operating, financing, and tax effects.

## Step 17 — ROE vs ROCE vs ROIC

Show all three side by side over the period and **explain the divergences — the gaps are the insight, not the levels:**
- **Heavy debt → ROE > ROCE.** Leverage inflates the equity return; a wide ROE-over-ROCE gap means returns are leverage-dependent and will compress if debt is repaid or rates rise.
- **Cash-rich → ROIC > ROE and > ROCE.** Surplus cash sits in the ROE and ROCE denominators but is excluded from invested capital, so ROIC runs higher; a wide ROIC-over-ROCE gap flags a lazy balance sheet — cash earning treasury yields instead of being deployed or returned.
- **Acquisitive → ROIC depressed vs ROCE** where acquisition goodwill sits in invested capital; the gap reads on how much was overpaid and whether the acquired business earns its purchase price.
- **Non-operating investments / associates** distort ROE and ROCE; ROIC (operating) is the cleaner read on core-business economics.
- **Tax:** all three are post-tax under this convention (ROE from PAT; ROCE and ROIC from NOPAT), so tax is deliberately *not* a wedge between them — this isolates the two real differences: leverage (ROE vs ROCE) and the capital base (ROCE vs ROIC). A tax holiday or 115BAA election lifts all three together; note it as a common driver rather than a divergence.

Compute **incremental returns** where the period allows — incremental ROCE = ΔEBIT / Δcapital employed, incremental ROIC = ΔNOPAT / Δinvested capital — to test whether new capital is being deployed above the cost of capital. (The *judgement* on capital allocation and management intent belongs to the management-analysis module; here, produce the return math and state it.)

Close with the **so-what**: which metric best reflects this business's core economics, what the divergences reveal about capital structure, cash deployment, and acquisition discipline, and whether the returns profile is structural or temporary (mix / integration / operating leverage vs cyclical margin, ramp distortion, or a transient cash build).

**Anti-shallow standard applies here too.** Not *"ROCE fell because of the new plant."* Instead: *"ROCE fell ~640 bps YoY to 15.7% in FY25 [Fact, T1, FY25 AR, computed]: ~₹900 cr of the ₹1,200 cr Dahej project sat in CWIP at year-end — in capital employed but earning nothing — and the commissioned line ran at ~40% utilisation [T2b, Q4 concall], so operating profit lagged the capital. Ex-CWIP ROCE was ~19.5% [Inference]. Temporary ramp distortion, not structural erosion, provided incremental ROCE on the project clears the ~14% cost of capital as utilisation normalises."*

## Step 18 — Answer the Growth-Drivers Hand-off (mandatory when a hand-off exists)

This is where the quality-of-growth question deferred by `growth-drivers` is settled. Answer **every** hypothesis in the hand-off list, by ID, in order. None may be skipped or merged.

**H-series (past hypotheses).** For each:
- **Verdict:** Confirmed / Partly confirmed / Rejected / Unknown.
- **Evidence:** the specific numbers from Steps 3–17 that decide it (e.g. receivable days FY22 → FY24, incremental ROCE FY23–25 vs cost of capital), each cited with source and period, and the step where the full analysis sits.
- **Explanation:** one or two sentences on why, under the anti-shallow standard.
- **So-what for growth quality:** did this growth come while holding margins, returns and balance-sheet strength, or by stretching them?

**T-series (future-trigger hypotheses).** These concern effects not yet in the reported numbers. For each:
- **Verdict:** Supported / Not supported / Not yet testable.
- **Evidence from history:** the closest analogue in the data — current segment margins of the target segment, economics of past capacity ramps (margin and asset-turn trajectory after commissioning), current working-capital profile of similar business, past incremental ROCE on comparable capex.
- **What to watch:** the reported metric and the quarter in which the effect should first show.
- Do not build a forecast; this is a test against historical evidence only.

Present as one table:

| ID | Hypothesis (as handed over) | Verdict | Deciding evidence (cited) | Where in this report | So-what / what to watch |

Then a two-to-three line **closing read**: taking the verdicts together, was past growth high quality, and do the triggers look economically attractive on the evidence so far?

Also write the verdicts back as `<Company>_growth_handoff_verdicts.json` (fields: id, verdict, evidence, citation, report_section, watch_item) next to the hand-off file, so later modules (management analysis, short thesis) can use them.

If no hand-off exists, write `Growth-drivers hand-off not found — Step 18 skipped` and continue.

# Evidence and Reasoning Guardrails

## Evidence Classes
Label each material conclusion as: **Fact** (verified, sourced, period-tagged), **Inference** (logical derivation from facts; state the chain), **Estimate** (modeled; show formula, inputs, assumptions, tiers), **Opinion** (management / rating agency / user view; attribute), **Hypothesis** (plausible but unverified; label clearly), or **Unknown**.

## Source Hierarchy
- **Tier 1** — Verified primary documents: Annual Report, audited filings, exchange filings, DRHP, QIP, government-portal databases, historical company financial models (Ace Equity etc.)
- **Tier 2a** — Independent verification: CRISIL, CARE, ICRA, Fitch, India Ratings
- **Tier 2b** — Management communications: concalls, investor presentations, management interviews, AGM transcripts, analyst meets, M&A / acquisition calls
- **Tier 3** — Secondary research: broker / analyst notes, ValuePickr threads, third-party aggregators
- **Tier 4** — Unverified background only; **never cite as evidence**

Conflict resolution: higher tier wins → more recent wins → more specific wins → if still unresolved, present both and disclose the conflict. Do not silently pick.

## Disclosure Gap Rule
When Tier 2a discloses something Tier 2b is silent on, flag as `Disclosure Gap`. Do not resolve. Do not assume management silence implies immateriality. Surface the asymmetry explicitly.

## Management Statement Classification
Classify each management statement as:

- **A. Formal Quantitative Guidance** (specific number with a time horizon, stated as guidance)
- **B. Directional Commentary** ("we expect margins to improve")
- **C. Aspirational Target** ("we aim to reach X by FY30")

Never treat B or C as A. Never blend management guidance with reported numbers. If converting qualitative commentary into a numeric inference, tag as `Analyst Assumption`.

## Reported Numbers vs Guidance
For historical periods, always use actually reported numbers from the AR / filings — never the guidance once given for that period. Where the company gave guidance but no actual reported number is available yet, state it as guidance / aspiration only.

## Derived Number Rule
For every derived number, show: formula, each input, source tier per input, period per input, assumptions, and the update trigger that would change the number.

## Citation Rule
Every factual claim carries an inline source tag. Format:

`[Evidence Class, Source Tier, Document Name, Date/Period, Section, Page/Location]`

Example: `[Fact, T1, FY2025 Annual Report, FY25, Notes to Accounts, p. 142]`

Do not cite unread documents. Distinguish prepared remarks from Q&A in concall citations.

## Anti-Shallow-Reasoning Rule
Reject reasoning like *"Other expenses rose due to commissioning of the Gujarat plant"* or *"Gross margin rose due to mix change."*

Acceptable form: *"Other expenses rose 320 bps YoY as % of revenue due to commissioning of the Gujarat plant in Q1FY26, operating at ~45% utilization per concall [Q1FY26 concall, mgmt opening remarks], creating temporary fixed-cost absorption pressure from utilities and maintenance before revenue ramp-up. [Inference, T1+T2b]"*

Quantify, link to KPIs, link to commentary, and classify structural vs temporary.

# Output Requirements

Default format: **formal HTML** with the structure below. Use clear headings, tables, and bullet points. Every factual claim carries an inline citation tag.

```html
<h1>P&L & Capital-Efficiency Analysis: [Company Name] | [Period]</h1>

<h2>1. Executive Summary</h2>
<!-- Include a one-line tally of growth-drivers hand-off verdicts, e.g. "Hand-off: 4 confirmed, 1 rejected, 2 not yet testable" -->

<h2>2. Scope, Sources, and Period Covered</h2>
<!-- Table of files reviewed with tier and period; note whether a growth-drivers hand-off was found -->

<h2>3. Comparability Check</h2>
<!-- Issue / When began / Affected items / Impact / Adjustment -->

<h2>4. Financial Base Table</h2>
<!-- All P&L lines, absolute + % of revenue + YoY bps -->

<h2>5. Material Movement Summary</h2>
<!-- All items >1% of revenue YoY; ESOP >1%; other-expense sub-lines >3% -->

<h2>6. Revenue Analysis</h2>
<!-- Volume / price / mix / geography / KPI linkage -->
<p><strong>Trend Summary:</strong> ...</p>

<h2>7. Gross Margin Analysis</h2>
<p><strong>Trend Summary:</strong> ...</p>

<h2>8. Operating Cost Analysis</h2>
<h3>Employee Benefit Expenses (incl. ESOP)</h3>
<h3>Power & Fuel</h3>
<h3>Advertisement & Marketing</h3>
<h3>Logistics & Freight</h3>
<h3>Other Expenses</h3>
<!-- Trend Summary under each -->

<h2>9. EBITDA Margin Bridge</h2>
<!-- Driver / bps / Structural-Temporary / Sustainability -->

<h2>10. Depreciation and Below-EBITDA Analysis</h2>

<h2>11. PAT Margin Analysis</h2>

<h2>12. Balance-Sheet Base & Capital-Efficiency Conventions</h2>
<!-- Returns base table; WC / ROCE / ROIC conventions stated; BS comparability -->

<h2>13. Asset Profile & Turnover Analysis</h2>
<!-- Ratio table with Average/Closing toggle; total asset / gross & net block / PPE / WC turnover; nature-of-business read -->
<p><strong>Trend Summary:</strong> broad multi-year trend + explanation of each material YoY movement</p>

<h2>14. Working Capital Analysis</h2>
<!-- Days table with Average/Closing toggle; receivable / inventory / payable / advances; CCC; CFO linkage; per-component drivers (value-chain causes included) -->
<p><strong>Trend Summary:</strong> broad multi-year trend + explanation of each material YoY movement</p>

<h2>15. Financial Leverage</h2>
<!-- Ratio table with Average/Closing toggle; equity multiplier, D/E, net D/E, interest coverage; productive vs risky -->
<p><strong>Trend Summary:</strong> broad multi-year trend + explanation of each material YoY movement</p>

<h2>16. DuPont ROE Integration</h2>
<!-- Table with Average/Closing toggle; net margin x asset turnover x equity multiplier; attribute ROE change to the lever -->
<p><strong>Trend Summary:</strong> broad multi-year trend + explanation of each material YoY movement</p>

<h2>17. ROE vs ROCE vs ROIC</h2>
<!-- Table with Average/Closing toggle; side by side; divergence diagnostics; incremental returns; so-what -->
<p><strong>Trend Summary:</strong> broad multi-year trend + explanation of each material YoY movement</p>

<h2>18. Growth-Drivers Hand-off: Verdicts</h2>
<!-- One row per H- and T-series ID: hypothesis / verdict (colour-coded) / deciding evidence (cited) / link to the section above / so-what or what to watch; closing read -->

<h2>19. Structural vs Temporary Driver Summary</h2>
<!-- Covers both P&L and capital-efficiency drivers -->

<h2>20. Disclosure Gaps, Conflicts, and Unknowns</h2>

<h2>21. Key Monitorables</h2>
<!-- Include the 'what to watch' items from T-series verdicts -->
```

Per material line item include: what changed, magnitude, margin impact in bps, evidence-backed driver explanation, KPI linkage where available, management commentary linkage where available, structural vs temporary classification, and trend summary.

**Ratio tables (Steps 13–17):** every ratio table carries an **Average / Closing toggle** above it (default: Average). Precompute both number sets and embed them; switch client-side with a small script (show/hide or swap precomputed values) — no recomputation on toggle. Each ratio series is accompanied by a Trend Summary that states the multi-year trend and explains the material YoY movements.

**Verdict table (Step 18):** colour-code verdicts (Confirmed / Supported = green, Partly = amber, Rejected / Not supported = red, Unknown / Not yet testable = grey); each row links to the section holding the full analysis.

Save the HTML file to `/mnt/user-data/outputs/` and present it via the present_files tool. Save the verdicts JSON alongside it.

# Quality Control Checklist

Before finalizing, verify:

- Company, industry, and period stated
- Consolidated vs standalone basis explicit
- Comparability tested before any bridge
- Every movement >1% of revenue YoY analyzed
- Every other-expense sub-line >3% of revenue analyzed
- ESOP separately checked (P&L + notes to accounts); Disclosure Gap flagged if absent
- Revenue drivers cover volume, price, mix, geography, seasonality where relevant
- Gross margin separates margin % from absolute unit profitability where pass-through matters
- EBITDA bridge reconciles line-item movements to net margin change
- PAT bridge separates operating from below-EBITDA drivers
- Structural vs temporary classification is evidence-backed
- Every number carries period and comparison base
- Every derived number shows formula and inputs
- Management guidance / commentary / aspiration kept separate, never blended with actuals
- Source tier shown on every factual claim
- Disclosure Gaps explicitly surfaced
- Unknowns are stated, not filled with invented assumptions
- Working capital uses `Inventory + Receivables + Advances Paid − Payables − Advances Received`, never `current assets − current liabilities`; advances included where material
- Return conventions (ROE = PAT / equity; ROCE = NOPAT / capital employed; ROIC = NOPAT / invested capital; averaging, CWIP and cash treatment) stated once and applied consistently
- Every ratio table computed on both Average (default) and Closing bases, with a working toggle above it
- Each returns/turnover/leverage series has a Trend Summary (multi-year trend) and explains material YoY movements, same discipline as the P&L
- Asset turns read against the nature of the business; goodwill / CWIP effects flagged before concluding on asset productivity
- Working-capital days broken into receivable / inventory / payable / advances, each with a cause, not just a number
- DuPont reconciles: net margin × asset turnover × equity multiplier ties to ROE
- ROE vs ROCE vs ROIC divergences explained (leverage, cash, goodwill, tax), not just reported
- Every growth-drivers hypothesis (H- and T-series) answered by ID with a verdict and cited deciding evidence; none skipped; verdicts JSON saved (or Step 18 skip noted)
- Output is in the requested format (default HTML) and presented via outputs directory

# Failure / Escalation Rules

- **Financial data unavailable in project** → state that P&L analysis cannot be completed, list missing data required, do not fabricate.
- **Source documents unavailable** → analyze only the provided financial data, mark explanation gaps as `UNKNOWN`, do not invent management commentary or KPI values.
- **Comparability unresolvable** → present reported numbers, flag absence of like-for-like comparability, avoid definitive YoY conclusions.
- **KPI data unavailable** → state `KPI data unavailable`; do not infer utilization, volume, realization, market share, or CAC without evidence.
- **Sources conflict** → apply hierarchy; surface unresolved conflicts; do not silently choose.
- **Structural vs temporary unresolvable** → classify as `Unknown` and state what evidence would resolve it.
- **Balance-sheet or cash-flow data unavailable** → run the P&L layer, mark the capital-efficiency layer `UNKNOWN`, and state which balance-sheet lines are missing. Do not fabricate a balance sheet.
- **Segment-level capital employed not disclosed** → state that segment ROCE / ROIC cannot be computed (companies disclose segment margins far more often than segment capital). Do not invent a denominator.
- **WC components (advances, payables split) not separable** → state which are unavailable and show the days on the components that are; do not silently fall back to `current assets − current liabilities`.
- **Market share, segment-level margins, utilization, or any number not in the project documents** → do not fabricate. State `Not disclosed in available project documents.`
- **Hand-off hypothesis cannot be tested with available data** → verdict `Unknown` (H-series) or `Not yet testable` (T-series), stating exactly which data would decide it. Never drop the hypothesis.