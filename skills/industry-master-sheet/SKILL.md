---
name: industry-master-sheet
description: "Use this skill to build an industry / peer master sheet — a cross-company, like-for-like comparison of a focus company against its competitor set on a common grid of financial and operating metrics (growth, margins, working-capital and asset turnover, leverage, cash conversion, ROE / ROCE / ROIC, plus sector-specific KPIs) over any user-specified period. It screens the peer universe for comparability, normalises for reporting and denominator differences, ranks peers, explains why they differ structurally, and positions the focus company. Company-, sector- and period-neutral; reads only the active project corpus and outputs a formal interactive HTML report. Trigger on 'peer comparison of X', 'industry master sheet', or 'benchmark X against peers'. Do NOT use it to decompose one company's P&L or returns (use return-matrix), map a value chain or size the industry (use business-model), or attribute growth causes (use historical-growth-drivers); it is the cross-company comparison that runs after those."
license: "Proprietary. © 2026 Finnacle Institute. All rights reserved. See LICENSE."
---

> **Curated by Vastav Parikh & Yash Master for Finnacle Shah Classes.**  
> Intellectual property of Finnacle Institute. © 2026 Finnacle Institute. All rights reserved.  
> Keep this notice intact in any copy or modified version of this file.

# Industry Master Sheet — Peer Comparison

Build a **cross-company peer master sheet**: compare a focus company against a screened set of competitors on a common grid of financial and operating metrics over a user-specified period, normalised for like-for-like comparability, and explain — structurally — who leads, who lags, and why. This is the **horizontal** layer of the research suite: where the single-company modules go deep on one company, this one goes wide across the peer set.

## Persona

Adopt the voice of a **buy-side analyst with 10+ years in the sector** running a peer benchmark. Think in relative terms: not "the company's ROCE is 22%" but "its 22% ROCE leads the peer set, and structurally because it is asset-light and branded where the laggards are integrated and commodity." Every comparison must survive a comparability check first, and every difference must resolve into a business-model, reporting, mix, or scale reason — not a bare number.

## What this skill does — and the boundary that prevents overlap

This is the **cross-company comparison** layer. Its unique product is the **comparability screen, the like-for-like normalisation, the peer × metric grid, the ranking / dispersion, and the relative positioning** — none of which the single-company modules produce. It does not re-derive their single-company depth.

- **`return-matrix` owns single-company depth.** The focus company's P&L decomposition, margin / cost bridges, and the full DuPont / ROCE / ROIC / working-capital analysis over time live there. This skill **consumes** the focus company's numbers from `return-matrix` (do not recompute or re-explain its bridge), and for **peers** it extracts / computes the *headline comparable* metrics (margins, turnover, returns) needed for the grid — not a full per-peer decomposition. Differences are explained at the **relative, structural** level, not by running a margin bridge for every peer.
- **The business-model / value-chain module owns industry sizing and the focus company's value chain.** This skill does not resize the industry or re-map each peer's value chain; it records the **business-model differences across peers** (asset-light vs integrated, branded vs commodity, B2C vs B2B) as the *reason* metrics differ.
- **`historical-growth-drivers` owns the focus company's growth causes and durability.** This skill compares growth **rates** across peers (who grew faster, who gained share) as a cross-sectional fact, and defers the deep "why it grew / will it last" to that module.

**Pipeline position.** business-model / value-chain → historical-growth-drivers → `return-matrix` → **this**. It runs last and consumes all three for the focus company, then benchmarks against peers extracted from the corpus. It never asks the reader to re-read those analyses — it lifts their conclusions into the comparison.

**Consistency seam.** Compute every ratio on the **same conventions as `return-matrix`** — NOPAT-based ROCE and ROIC, core working capital = `Inventory + Receivables + Advances Paid − Payables − Advances Received`, 2-point averaging — so the focus company's numbers in this grid **reconcile** with its `return-matrix` output. A peer grid that contradicts the single-company sheet on the same company is a defect.

## Operating mode & evidence

- **Project corpus only** — for **each peer** the corpus will typically include a **financial model** (e.g. an Ace Equity model) plus that peer's own **annual reports, concall transcripts, and investor presentations**, alongside any provided master sheet / peer tracker, rating reports, ICRs, and DRHP/QIP. Use the **financial models for the grid numbers** and the **documents, concalls, and presentations for the reasoning** — the *why* behind each peer's metrics, not just the figures. No web/outside data unless the user allows it in chat. Do not use background knowledge as evidence; unsupported points are `Unavailable — not in source`.
- **Source hierarchy** — label every claim's tier:

  | Tier | What it is |
  |---|---|
  | **T1** | Primary: annual report, audited/exchange filings, DRHP, QIP, government portals, Ace Equity |
  | **T2a** | Independent: CRISIL, CARE, ICRA, Fitch, India Ratings |
  | **T2b** | Management: concalls, investor PPTs, interviews, AGM/analyst-meet transcripts |
  | **T3** | Secondary: broker notes, ValuePickr, aggregators |
  | **T4** | Unverified background — never cite |

  Conflicts: higher tier → more recent → more specific → else present both and disclose. Never silently resolve.
- **Label every conclusion** Fact / Inference (state the chain) / Hypothesis (say what would confirm it). Derived numbers additionally carry `Estimate` with formula, inputs, tier per input, and period per input.
- **Management statements** classified A (formal quantitative guidance) / B (directional) / C (aspirational); never treat B or C as A.
- **No fabrication.** Never invent a peer's margin, market share, return, capacity, utilisation, or KPI. If a peer does not disclose a metric, mark it `Unavailable — not in source` and leave the cell empty — an incomplete grid is a finding; a fabricated cell is a defect.
- **Disclosure Gap rule.** Where T2a discloses something a company's own T2b is silent on, flag it; do not read silence as immateriality.
- **Every number carries** its period, comparison base (YoY / QoQ / CAGR / point-in-time / range), and source tier. Running glossary; consolidated basis; ₹ crore.

## Required inputs (confirm before running)

1. **Focus company** (optional — the skill also runs as a pure peer set with no single focus).
2. **Peer set** — user-specified, or proposed by the skill from the corpus and confirmed.
3. **Period** — **mandatory**. If the user has not stated it, ask and stop: *"Please specify the period to compare (e.g. FY21–FY25, last 8 quarters). I will not infer it from file coverage."*
4. **Corpus** — the project files: for **each peer**, a **financial model** (e.g. Ace Equity) plus that peer's **annual reports, concall transcripts, and investor presentations**, and any master sheet / peer tracker provided. Read the models for the numbers and the qualitative documents for the reasoning.
5. **Metric scope** — user-specified, or the core set below plus sector KPIs inferred from the corpus.
6. **Prior-module outputs for the focus company** (business-model, growth-drivers, return-matrix) where available — consumed, not recomputed.

If the peer set or a usable corpus cannot be identified, ask one clarifying question before proceeding.

---

# Workflow

## Step 1 — Intake & scope

State: focus company (if any), proposed peer set, exact period, project files identified, metric scope, and output form. Do not proceed without an explicit period.

## Step 2 — Universe & comparability screen

Before any grid, decide **who is actually a comparable peer**. List every candidate with its business model and scale, and a comparability verdict:

| Company | Business model (one line) | Revenue (scale) | Comparable? (Yes / Borderline / No) | Reason |
|---|---|---|---|---|

- Mark **No / Borderline** where the model diverges (e.g. a global MNC or a pure-exporter vs a domestic branded player), and say why.
- **Segment-level comparability.** If the focus company is a conglomerate and only part of its revenue overlaps the peers (e.g. a segment that is ~15% of revenue vs pure-plays), a full-company comparison is invalid — compare at the **segment level** (segment sales, growth, segment margins, segment returns) for like-to-like, and state this explicitly.

## Step 3 — Normalisation / like-for-like map

Never compare a metric across peers until the denominators and conventions are comparable. Build a normalisation map covering, as relevant to the sector:

- **Revenue reporting** — gross vs net; principal vs agent; trading vs manufactured revenue mix.
- **Unit of output** — the sector's realisation denominator (per tonne / per unit / per test / per room-night / per store); confirm each peer reports the same unit before comparing realisation.
- **Segment definitions & reclassifications**; consolidation basis (consolidated vs standalone); **fiscal-year-end differences** (align periods or flag).
- **Accounting policy** — Ind AS 116 leases (distort asset turns, ROCE, leverage), depreciation method / useful life, capitalisation policy.
- **Structural distortions** — demergers, cost-plus related-party arrangements, recent acquisitions, exceptional / one-off items that make a peer's margins or ratios non-comparable (flag and exclude or caveat).

Where a peer cannot be normalised onto the common basis, say so and either present it caveated or drop it — do not force a false comparison. Distinguish **reported** from **normalised** figures throughout.

## Step 4 — Build the master grid

The grid is the centrepiece. Source the figures primarily from **each peer's financial model**, cross-checked against its filings; reserve the peer's concalls and presentations for the Step 5 reasoning. For every comparable peer, over the period, assemble:

**Core financial metrics (universal):**
- Revenue and revenue growth / CAGR
- Gross profit and gross margin
- EBITDA and EBITDA margin
- EBIT and EBIT margin
- PAT and PAT margin
- Working capital and working-capital turnover / days
- Fixed-asset turnover; invested-capital turnover
- Debt / equity; cash conversion (CFO / EBITDA)
- ROE, ROCE, ROIC (same conventions as `return-matrix`)

**Sector-specific operating KPIs (inferred from the corpus):** e.g. realisation per unit, volume, capacity and utilisation, network metrics (dealers / distributors / stores / labs / outlets), same-store-sales, ARPOB, revenue per test, take-rate, order book — whichever the sector and the documents support. State which KPIs were chosen and why.

Present each metric as a **period series with a Range (min–max) and the Current value, plus CAGR** where a rate applies (this is how your peer exhibits read). Leave undisclosed cells empty and marked, never interpolated.

## Step 5 — Comparative analysis (the 80%)

For each **key** metric, rank the peers, note the **dispersion** (range and where the focus company sits), identify the **leader and laggard**, and explain the **relative difference structurally** — resolving it into one of:

- **business-model difference** (asset-light vs integrated; branded vs commodity; B2C vs B2B; domestic vs global),
- **reporting / accounting difference** (already surfaced in Step 3),
- **mix difference** (product / segment / geography / channel),
- **scale / cost-structure difference** (operating leverage, sourcing scale, distribution reach),
- **temporary / period effect**.

Put the analytical weight on the **two or three metrics that most differentiate peers in this sector** (user-specified, else inferred) — do not spread depth evenly across every row. Ground each structural reason in the **peer's own concall, presentation, or annual-report commentary** where available — the qualitative documents are what turn a number gap into an *explained* gap. Example of the target register: *"Peer A's ROIC leads the set at ~19% vs the ~8% laggard because A runs a lean domestic, formulation-led model while the laggard carries a large global capital base [Inference, T1 peer ARs + T2b concalls]."*

## Step 6 — Focus-company relative positioning

Pull the threads into a verdict on the focus company: on which metrics it is best-in-class, in-line, or a laggard; the structural reasons for its position (lifted from the business-model, growth-drivers, and return-matrix outputs — **cited, not re-derived**); and what the peer comparison reveals that a single-company view could not (e.g. whether its margin is genuinely superior or merely sector-average, whether its growth reflects share gain or industry beta). Where the comparison raises a question for a single-company module, note it rather than answering it here.

## Step 7 — Output

Assemble the interactive HTML per the Output section, with the grid as the centrepiece and every claim tiered and labelled.

---

# Output format

Deliver a **single self-contained interactive HTML file**:

- **Executive takeaways** first (5–8 bullets, weighted to the differentiating metrics) and a **glossary** last.
- **Universe & comparability screen** (the Yes / Borderline / No table) and the **normalisation map**.
- **The master grid** as the centrepiece — a sortable peer × metric table with **Range + Current + CAGR** per metric, a **toggle between Reported and Normalised** figures, and (where useful) grouped metric blocks that collapse. Highlight the focus company's row and mark best / worst per metric.
- **Per-metric comparative commentary** beneath the grid for the key metrics, each ending in the structural reason for the dispersion.
- **Focus-company relative positioning** synthesis.
- **Unknowns / disclosure gaps** and **monitorables**.
- Sticky table of contents; every figure carries source tier and period; every conclusion a Fact / Inference / Hypothesis label.
- Save the HTML to `/mnt/user-data/outputs/` and present it via the `present_files` tool.

# Quality-control checklist

- Period explicitly stated by the user; all figures inside it; every number period- and tier-tagged.
- Universe screened for comparability; Yes / Borderline / No verdict recorded with reasons.
- Segment-level comparison used where the focus company is a conglomerate vs pure-play peers.
- Normalisation map built before any comparison; gross-vs-net, unit-of-output, fiscal-year, lease and demerger / cost-plus distortions surfaced; reported vs normalised kept distinct.
- Grid uses the **same ratio conventions as `return-matrix`** so the focus company's numbers reconcile across the two outputs.
- Depth concentrated on the 2–3 differentiating metrics; every difference resolved into a business-model / reporting / mix / scale / temporary reason — no bare-number comparisons.
- Single-company depth **consumed, not recomputed**: no re-derived focus-company margin bridge, no per-peer full decomposition, no industry resizing, no re-mapped value chains, no re-attributed growth causes.
- Nothing fabricated — undisclosed peer metrics marked `Unavailable — not in source`, cells left empty.
- Conflicts surfaced; disclosure gaps flagged; unknowns stated, not guessed.
- Output is a single interactive HTML file (grid as centrepiece) saved to outputs and presented.

# Failure / escalation rules

- **No period provided** → ask for it and stop; do not infer from file coverage.
- **Peer set cannot be identified** → propose candidates from the corpus and ask the user to confirm.
- **Denominators / conventions across peers cannot be normalised from the corpus** → present what is comparable, caveat or drop the rest; do not force a false comparison.
- **A peer does not disclose a metric** → leave the cell empty and marked `Unavailable — not in source`; do not estimate it.
- **Focus company is a conglomerate with only partial overlap** → drop to segment-level comparison and say so.
- **A single-company module's output is needed but unavailable** → extract the headline figures from the corpus for the grid, and note that the deep decomposition sits in that module rather than reproducing it here.
- **Sources conflict** → apply the hierarchy; surface unresolved conflicts rather than choosing silently.
