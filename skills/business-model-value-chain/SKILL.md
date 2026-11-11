---
name: "business-model-value-chain"
description: "Buy-side analysis of how one Indian company's business works: Product 101, industry chain zoomed to its product, industry sizing, value chain. Auto-builds 3D diagrams and films for complex chains. Not for overview or summary."
license: "Proprietary. © 2026 Finnacle Institute. All rights reserved. See LICENSE."
---

> **Curated by Vastav Parikh & Yash Master for Finnacle Shah Classes.**  
> Intellectual property of Finnacle Institute. © 2026 Finnacle Institute. All rights reserved.  
> Keep this notice intact in any copy or modified version of this file.

# Business Model, Value Chain & Industry Sizing

Build a buy-side analysis of how a single Indian company's business works, grounded in the project corpus and delivered as one interactive HTML report. The reader should finish knowing: what the product is, where it sits in its industry, why it matters to the customer, how big the market is, how the company makes money, and at which points in the chain value and advantage are created.

This is one module in a modular research process. The **business overview and executive summary are not written here**; they are written in the final note after all modules have run, so they can be synthesised across modules. This module ends with a short takeaways box that feeds that final note.

## Persona and voice

Write as a **buy-side senior equity research analyst / sector specialist with 10+ years covering the sector**, explaining the business to a smart reader who is **not technical**. Two rules follow:

1. **Plain language first.** Explain every concept in everyday words before using the technical term. Use one simple, physical analogy per hard concept (for example: a bushing is the rubber grommet where a cable passes through a steel almirah). Test each analogy: it must explain the mechanism, not just sound friendly. Short sentences. No jargon without an inline explanation.
2. **Mechanisms, not just facts.** The reader builds a durable mental model on top of this output, so a stated cause with its "why" is worth more than a bare fact.

## Scope

Covered here: Product 101, the industry value chain and zoom ladder, industry sizing and segmentation, and the business model and value chain.

Hand off in one line, do not do:

- **Business overview, executive summary, scale snapshot, corporate structure, milestones, ownership** → final note. (Exception: mention a subsidiary or JV only where it owns a stage of the value chain.)
- **General P&L or margin decomposition** → `pnl-driver-analysis`. The narrow exception is financial impact caused by a value-chain change (see "Linking financials to the value chain").
- **Management, capital allocation, governance** → `management-analysis`.
- **Historical growth-driver attribution** → `historical-growth-drivers`.
- **Competitive-advantage verdict** → the moat module. This skill only *locates* where an advantage could sit (moat-location tags) and gives the evidence; it does not rule on how strong the moat is.
- **Business risk, valuation, modelling** → separate modules.

---

# Evidence standards & guardrails

These apply to every claim, table, diagram and film caption. A single invented number quietly corrupts everything downstream, and an unlabelled inference looks like a fact six months later.

## Source universe

Work **only** from documents in the active project: annual reports, audited and exchange filings, DRHP/RHP/QIP, investor presentations, concall transcripts, credit-rating reports, ICRs, Ace Equity exports, management interviews, scuttlebutt notes, and anything the user names at run time. The corpus routinely includes **listed peers' filings**; use them, especially for industry sizing and profit pools. Never use a peer's document to state the **subject company's own** facts.

Do not use web search or outside data unless the user allows it in chat. When allowed (for example, public tender awards to price an end product), cite the website as below.

**General knowledge** may be used only to explain how a product or process works physically (engineering, chemistry, physics) when the corpus is silent. Tag it **[General knowledge]**. Never use it for numbers, market facts, or company facts.

## Citations: document and page for every fact (mandatory)

- Every fact carries an inline citation with the **document short name and page number**, for example *(RHP p.172)*, *(AR FY26 p.26–27)*, *(Concall Q4FY26 p.8)*, *(Investor PPT Q4FY26 p.14)*. This applies to body text, every table row (use a Source column), every diagram caption, and every film caption.
- For web sources: site or publisher name, page title, full URL and the date accessed.
- **State what was taken from each source.** The report ends with a **source register**: one entry per document with its full name, period, tier, page-number convention, and a list of the facts taken from it with pages. Inline citations are clickable links to their register entry.
- **Page convention.** Use the PDF page number. Where the printed page differs (cover letters, two-page spreads), say so in that document's register entry.
- Non-sourced content must be tagged as one of: **[General knowledge]**, **[Analyst arithmetic]** (show the formula), **[Analyst view]**, **[Analyst Assumption]**.

## Source hierarchy

| Tier | What it is |
|---|---|
| **T1** | Verified primary documents and primary-sourced data: annual report, audited filings, exchange filings, DRHP/RHP, QIP document, government-portal databases, historical financial models (e.g. Ace Equity) |
| **T2a** | Independent verification: rating agencies (CRISIL, CARE, ICRA, Fitch, India Ratings) |
| **T2b** | Management communications: concalls, investor presentations, management interviews, AGM transcripts, analyst meets, special calls |
| **T3** | Secondary research: broker/analyst notes, ValuePickr threads, third-party aggregators |
| **T4** | Unverified background only; never cite as evidence |

Label every claim with its tier. When sources conflict on facts, the higher tier wins.

**Peer filings as an industry source.** For industry-level sizing and structure (not company facts), a listed peer's annual-report industry section counts as **T1** and its investor presentation as **T2b**. Name the underlying research agency the peer cites (e.g. CRISIL, Frost & Sullivan), the peer, and the reference year.

## Conflict resolution

1. Higher tier wins.
2. Same tier: more recent wins.
3. Same recency: more specific wins.
4. Still unresolved: present both and disclose the conflict.

## Disclosure Gap rule

When **T2a** discloses something **T2b** is silent on, flag it as a **Disclosure Gap**. Do not resolve it, and do not assume silence means immaterial.

## Claim labelling

Label every conclusion as **Fact** (stated in a source, with tier, period and page), **Inference** (reasoned from sourced facts; show the chain) or **Hypothesis** (plausible but unverified; say what evidence would confirm it).

## Derived numbers

For every derived number show: (1) the formula, (2) each input, (3) the tier, page and period of each input.

## Management statements

Classify each as **A. Formal Quantitative Guidance**, **B. Directional Commentary** or **C. Aspirational Target**. Never treat B or C as A. Never blend guidance with reported numbers. Numeric conversions of qualitative commentary are tagged **Analyst Assumption**. Company claims that are self-serving (e.g. "it takes 8–10 years to get approved") are reported as company claims and, where possible, tested against the company's own record.

## No fabrication

If data is unavailable, write **`Unavailable — not in source`**. Do not estimate, interpolate or fill from memory. This applies with special force to **market share, capacity utilisation, segment margins, segment realisations, customer/supplier concentration, industry size, end-product prices and content per unit**. An explicit gap is a finding; a fabricated number is a defect.

## Analyst sanity checks (run before finalising)

- **Cross-check derived numbers against reported totals.** Units × price must not exceed the revenue line it belongs to; segment shares must sum to ~100%; a claimed unit price implies a revenue that must fit the P&L. Example of the check catching an error: "≈950 units × ₹25 lakh = ₹237 cr, above total FY25 revenue of ₹150 cr, so ₹25 lakh cannot be the average realised price."
- **Check the company's own documents against each other.** Where two documents (or two pages of the same document) disagree, show both with pages and flag it as an **Internal inconsistency**. Do not silently pick one.
- **Check user-supplied models and notes** in the corpus against the filings; flag mismatches plainly with the arithmetic.
- **Ratio sanity:** content per unit as % of end-product price, margins and market shares should land in plausible ranges; if not, re-check inputs before publishing.
- List every flag in a short **Sanity-check log** in the report.

## Other conventions

- Reporting basis defaults to **consolidated**; flag prominently when falling back to standalone.
- **₹ crore**, **Ind AS** terminology, fiscal years (FY15 … FY26), **YoY and QoQ** where relevant.
- Tag every change or driver **structural vs temporary**.
- **Running glossary:** explain each technical term inline the first time it appears, and collect all of them in a glossary appendix.

## Required inputs (confirm before running)

Confirm: (1) company, (2) industry/sector, (3) as-of period, (4) reporting basis if not consolidated, (5) the documents in the project (list every file opened), (6) whether web sources are allowed, (7) any user hypotheses or focus areas. If company, industry or a usable corpus is missing, ask one clarifying question first.

---

# Step 0: Design the report before writing it

Every company and industry is different. Before writing, make three judgements and state them in a short **"How this report is built"** box at the top of the report, with one line of reasoning each.

## 0.1 Emphasis profile: where the depth goes

Classify the business into its archetype(s) and weight each part **Deep / Standard / Brief**. Use this as a starting point, then adjust to the evidence:

| Archetype | Examples | Go deep on | Keep brief |
|---|---|---|---|
| Engineered component or intermediate sold to OEMs | bushings, auto components, bearings, electronic sub-assemblies | zoom ladder, content per unit, criticality, process, qualification gates, customer insourcing | brand, retail channel |
| Process / chemistry manufacturer | specialty chemicals, API, agrochemicals, glass | process steps and yields, backward integration, raw-material chokepoints, capex cycle, approvals (USFDA etc.) | channel |
| Commodity converter / spread business | steel, cement, sugar, paper, refining | supply side (raw material, energy, logistics), spread economics, cost-curve position, capacity and utilisation | Product 101 |
| Branded consumer | FMCG, durables, apparel, QSR | demand side: brand, pricing tiers, distribution reach, channel shift, own vs outsourced manufacturing | process detail |
| Project / EPC / B2G | infrastructure, defence, capital goods | order book, tendering (L1), contract terms, execution cycle, working capital | brand |
| Asset-heavy service / utility | power generation, ports, hospitals, telecom | asset commercialisation cycle, regulation and tariffs, utilisation, capex | Product 101 |
| Financial / platform / software | banks, NBFCs, exchanges, SaaS | flow-of-money chain, pricing or take rate, customer acquisition, funding side as the "supply" side | process films, 3D |

A company can mix archetypes (e.g. a component maker with an EPC arm). Weight each segment separately.

## 0.2 Zoom ladder: how many levels to explain

A reader cannot understand a component without first seeing the system it sits in and the industry that system serves. Build a **zoom ladder** from the industry down to the company's product:

- **Start** one level above where the end customer's money originates (the industry value chain).
- **Zoom** one level at a time: industry → the system or end product → the company's product → (if it is what makes or breaks the product) the critical sub-component inside it.
- **Stop** at the company's product, or one level below it if a sub-component is where the know-how, cost or risk sits.

Examples:
- Bushings: power sector (generation → transmission → distribution) → power transformer → bushing → condenser core.
- Auto component: auto industry → vehicle → braking system → brake pad / friction material.
- API maker: healthcare → formulation (tablet) → API → key starting material.
- FMCG brand: often only two levels (category → product); no deep ladder needed.
- Bank / NBFC: no physical ladder; use a flow-of-money chain (savers → bank → borrowers → end use).

At each level show: what it is in one plain line, who the players are, rough market size (sourced), and where the company sits.

## 0.3 Visual plan: which diagrams and films to build

Score the company on four factors, 0–2 each:

| Factor | 0 | 1 | 2 |
|---|---|---|---|
| **Process complexity** | trading, assembly of bought parts, services | a few physical steps | 4+ physical or chemical transformation steps the reader has never seen |
| **Product unfamiliarity** | consumer sees it daily | known by name, not by how it works | invisible industrial part or molecule |
| **Chain depth** | sells to the end user | one level from the end user | component inside a system inside an industry |
| **Criticality asymmetry** | failure is cheap and visible | moderate consequence | small share of cost, large consequence of failure |

Then build visuals **automatically** by score:

- **Total 0–2:** flat interactive SVG diagrams only (value chain, flow of money). No 3D, no films.
- **Total 3–4:** 3D isometric static diagrams for the industry chain, the zoom ladder and the product cut-away. No films unless one factor scores 2 and a film is the clearest way to explain it.
- **Total 5–8:** all of the above, plus:
  - a **production-process film** when process complexity = 2;
  - a **criticality film** (how the product works inside the system and what happens when it fails) when criticality asymmetry = 2 or chain depth = 2.

State the scores and the resulting visual plan in the "How this report is built" box. Never add a film for decoration; each must answer one question the text cannot answer as well.

---

# Handling multiple segments or industries

- **Segments in different industries:** run Parts 2–4 separately and in full per industry, each with its own zoom ladder, sizing and value chain.
- **Same industry, similar value chains:** explain together, surface differences inline.
- **Same industry, genuinely different chains** (e.g. quartz vs steel sinks): separate value chains and diagrams.

State the structural choice and why, in the "How this report is built" box.

---

# The analysis

Produce the parts below in this order. Depth per part follows the emphasis profile from Step 0.

## Top of report

1. **How this report is built** box (emphasis profile, zoom ladder levels, visual-plan scores, multi-segment choice).
2. **Module takeaways** box: five or six plain-language points the reader should remember from this module (what the product is, where it sits, why it is critical, market size and growth, how the company makes money, where advantage could sit). Each point is cited. This is the input to the final note's executive summary, not a replacement for it.

## Part 1. Product 101

Only what the reader needs before the value chain makes sense.

1. **What it is, in plain words** — two or three sentences plus one physical analogy.
2. **Product cut-away (diagram)** — show only the **core components, at most five labelled parts**. Cut every decorative or secondary detail. One sentence per part on what it does. Where one part is the heart of the product (e.g. the condenser core of a bushing), add a dedicated plain-language explainer in Q&A form: what is it, what is it wound or built on, what is it made of, what does each material do, how do the variants differ.
3. **Job-to-be-done** — what problem it solves for the customer, what it replaces or competes with, and why the customer buys it.
4. **Product portfolio table** — per product: what it is (one line), key features, variant/technology (e.g. OIP vs RIP), positioning (mass/premium), indicative price point, share of revenue, market feedback from the corpus. Mark gaps `Unavailable — not in source`.

## Part 2. Industry value chain, zoom ladder and criticality

1. **Industry value chain diagram (3D when the visual plan says so)** — the whole industry flow from raw input to end use, with the owners at each stage (e.g. generators, transmission utilities, distribution companies) and the company's place marked in one accent colour.
2. **Zoom figure** — industry → system → product (→ sub-component), with plain labels and sourced market sizes at each level.
3. **Content per unit / "which product goes where" table** — one row per class of end product (e.g. distribution transformer, 132 kV power transformer, 400 kV transformer):
   | End-product class | Typical end-product price (sourced) | Company's product fitted (type, count) | Content value (₹ and % of end-product price) | Company presence: Core / Next target / Niche / Absent | Source |
   Highlight the rows where the company mainly sits. Content values derived from a % rule are **[Analyst arithmetic]** with the formula shown. Sanity-check the % against the industry ratio (e.g. component market ÷ end-product market). Add a one-line "how to read this table".
4. **Criticality: cost share vs consequence of failure** — place the product on a simple 2×2: share of the customer's cost (low/high) vs consequence of failure (low/high), with sourced evidence for each axis (e.g. "~5% of transformer cost (Concall p.27)"; "bushing failures are a top cause of transformer fires (RHP p.157)"). Explain in plain words what the position implies for the customer's willingness to switch suppliers for a small saving. Leave the moat verdict to the moat module.
5. **Criticality film** (if triggered in Step 0) — how the product works inside the system and what happens when it fails.

## Part 3. Industry sizing & segmentation

Every market-size and share number names its document, page, reference year and tier, and is tagged independent estimate vs management claim. **Never fabricate market share.**

**Triangulate across the corpus**: the DRHP/RHP industry section, rating reports, broker notes, and **listed peers' annual-report industry sections and presentations**. Where sources differ, show a small cross-source table and the range; do not blend silently.

Repeat per industry where the company spans several.

1. **Industry size & growth** — value and volume, full historical series the corpus supports (ideally 5–10 years):

   | | FY15 | FY16 | … | FY25 | CAGR |
   |---|---|---|---|---|---|
   | Industry size (value) | | | | | |
   | YoY (%) | | | | | |
   | Industry size (volume) | | | | | |
   | YoY (%) | | | | | |

   State the exact CAGR window; give long-term CAGR, year-by-year growth and latest-period growth; say whether growth is price-led or volume-led; show forecasts with source.
2. **Segments** — each with size (value + volume), historical growth, CAGR (window, source, tier), latest growth, and forward growth only if a credible source gives it (class A/B/C if from management). Segment the way the economics differ (e.g. by technology, voltage class, end-use).
3. **End-user mix** — who ultimately buys, by end-use bucket, with share, historical growth and outlook. The company's growth is bounded by the growth of the end-users it is exposed to.
4. **TAM / SAM / SOM** — whole industry, the slice the company can address with its current approvals and range, and what it serves today.
5. **Demand drivers per segment (brief)** — the main structural driver(s) behind each segment's growth. Full attribution belongs to the growth-drivers module.
6. **Growth divergence** — faster vs slower segments and why (structural vs cyclical).
7. **Company positioning & market share by segment** — share as a historical series where sourced; rank; trajectory. If you derive share, show the derivation and label it **Inference**.
8. **Competitive set per segment** — players and rough shares; organised vs unorganised; top-N concentration; imports as a competitor; customers who make the product in-house (captive supply) as a competitor.
9. **Geographic sizing** — by country/region/state where sourced; India vs export.
10. **Import / export dynamics** — import dependence, export competitiveness, China dependence, anti-dumping/safeguard context.
11. **White space** — under-penetrated segments or geographies the company targets (class A/B/C).

## Part 4. Business model & value chain

Open with the **company value chain diagram**, then the profit pool and chokepoint overlays, then the revenue engine, then the three sides.

### 4.0 Company value chain diagram

An interactive diagram of the stages from raw material to end customer, with the company's position and degree of integration marked. Clickable or hoverable stages reveal: what happens there, who the players are, the company's presence (in-house / outsourced / imported), and margin captured. One diagram per distinct chain.

### 4.1 Profit pools: where the money is made along the chain

For each stage of the chain, show the typical EBITDA margin and ROCE range of listed players at that stage, from their filings in the corpus (name each player, period, page). Show this as a band or bar on the chain diagram and as a table. Where no listed player exists for a stage, write `Unavailable — not in source`. Then say in plain words which stages capture the most value and where the company sits relative to them. Peer figures are industry evidence, not the company's own facts.

### 4.2 Chokepoints and make-vs-buy

Mark on the diagram and list in a table every point where the chain can be squeezed:

- **Single-source or concentrated inputs** (top supplier share, sourced).
- **Import dependence** by input and country.
- **Capacity-constrained nodes** (industry shortages, long lead-time equipment).
- **Customer insourcing** (OEMs making the product themselves).
- **Make-vs-buy per process step:** in-house / outsourced / imported, with source. Call out plainly when the hardest step is not done in-house (e.g. "the core is imported ready-made (RHP p.175)").

### Linking financials to the value chain (applies throughout 4.3–4.6)

Inside each part of the chain, not in a separate section:

1. **Evolution and change** — how this part of the chain has changed (backward integration, a plant commissioned, a channel shift, a supplier replaced, technology licensed). Tag structural vs temporary.
2. **The financial impact of that change, quantified right there** — e.g. the gross-margin movement after backward integration, with numbers, years and pages.

Surface **only** effects caused by a value-chain change. Commodity prices, forex or subsidy accounting belong to the P&L module. When a number has both kinds of driver, state the value-chain contribution only, then add exactly: *"Other drivers also affected this, and are covered in the P&L module."* Do not name, characterise or quantify the other drivers.

### 4.3 Revenue & pricing engine

1. **How it earns** — every revenue stream with % mix (this replaces the old revenue-mix snapshot).
2. **Quality of revenue** — recurring vs one-time; aftermarket, spares, service, retrofit/replacement share.
3. **Revenue recognition** — point-in-time vs over-time (Ind AS 115), % completion, principal vs agent, and why it changes how to read the numbers.
4. **Volume × realisation table (the company's own numbers)**, longest series available, per segment/product where disclosed:

   | | FY15 | FY16 | … | FY25 | CAGR |
   |---|---|---|---|---|---|
   | Volume | | | | | |
   | Volume YoY (%) | | | | | |
   | Realisation | | | | | |
   | Realisation YoY (%) | | | | | |
   | Revenue | | | | | |
   | Revenue YoY (%) | | | | | |

   Volume-led or realisation-led? Mix effect? Reasons for sharp moves. No industry rows here.
5. **Pricing model** — cost-plus, commodity-linked, tender/auction, negotiated, yield-managed, spread-based, feature-based.
6. **What drives realisation** — mix, technology tier, currency, commodity spread, escalation clauses, regulation.
7. **Pricing power / pass-through** — can it pass on raw-material inflation, with what lag, formula-linked or not.
8. **Order book (where relevant)** — tender vs nomination; L1 bidding; size, composition, ageing; book-to-bill; order-to-revenue lag; stuck orders.
9. **Contract terms** — tenor, pass-through and escalation clauses, take-or-pay, liquidated damages, credit period, warranties, retention money.
10. **Ancillary economics** — discounts, returns, scrap/by-product sales, other operating income.
11. **Government / regulatory revenue effects** — price caps, duties, GST, export incentives, PLI, subsidies, and where they show up.
12. **Working-capital signature** — what the model implies for receivables, inventory, payables and the cash cycle.
13. **Evolution + linked financial impact.**

### 4.4 Demand side (end customer & route to market)

- **Customer profile** — who buys; B2B/B2C/B2G; government vs private; organised vs unorganised.
- **Client concentration** — top-5/top-10 share and trend; single-customer dependence; stickiness and switching costs. Never fabricate percentages.
- **Qualification / approval gates (where customers must approve suppliers)** — who approves (test lab, OEM, end utility/regulator, consultant), what is tested or inspected, how long each gate takes, how long approvals stay valid, and what forces a re-approval. Show as a simple gate diagram and a timeline of the company's own approval history, with pages. Separate company claims about approval time from evidence of the company's actual record.
- **Demand drivers & cyclicality** — macro/sector variables, cyclical vs structural, seasonality.
- **Distribution & reach** — own network vs distributors; channel mix; dealer count; export routes.
- **Positioning** — brand vs commodity; price tier; demand generation vs fulfilment.
- **Evolution + linked financial impact.**

### 4.5 Supply side (procurement & inbound)

- **Backward integration** — which inputs made in-house vs bought; captive vs merchant.
- **Key raw materials** — each as approx % of RM cost or COGS; price behaviour; forex content.
- **Supplier base** — who and where; concentration; single-source risk; domestic vs import; country dependence; terms. Procurement map (material → counterparty → relationship → country → purpose) where sourced.
- **Procurement structure** — long-term vs spot; formula-linked pricing; hedging.
- **Supply-chain evolution** — localisation, China+1, vendor development, import substitution, inventory strategy.
- **Evolution + linked financial impact** — with derivations labelled Inference or Analyst Assumption where not disclosed.

### 4.6 Central side (manufacturing, assets, technology)

- **Manufacturing footprint** — plant-wise table (location → product → capacity), owned vs leased vs job-work.
- **Manufacturing process, explained simply** — walk through the steps in plain words, one short paragraph per step, so a non-technical reader understands how the product is actually made. Add a five-or-so-station **process diagram** with, for each step: in-house / outsourced / imported, the bottleneck or value-adding steps, and its **moat-location tag** (see 4.7). Add the **production-process film** here if triggered in Step 0.
- **Capacity & asset-commercialisation cycle** — installed vs operating capacity, utilisation, capex-to-commissioning lead time, ramp-up. **Never fabricate utilisation.**
- **Capex intensity & operating leverage** — asset turns; fixed vs variable costs; capex pipeline (class A/B/C).
- **Technology** — in-house vs licensed vs JV; process know-how; automation.
- **R&D & intangibles** — R&D % of sales; patents, brands; regulatory approvals and certifications as barriers.
- **Quality & compliance** — certifications, type tests, audit history, environmental clearances.
- **Evolution + linked financial impact.**

### 4.7 Moat-location map

Tag each stage and process step where an advantage **could** sit, using a small fixed set of tags:

- **Recipe** (design or formulation know-how)
- **Process** (hard-to-copy manufacturing step, yield, cycle time)
- **Approval** (qualification gates, type tests, vendor lists)
- **Scale / cost** (cost position, utilisation, procurement scale)
- **Channel / brand**
- **Switching cost / installed base** (retrofit, spares, track record)

For each tag give the evidence with pages and one line on what would weaken it (e.g. customer insourcing, a technology shift). Summarise in one table. **Do not grade the moat**; hand the verdict to the moat module.

## Part 5. Monitorables and open questions

1. **Value-chain monitorables** — 5–10 KPIs that would change the view, each with: current value and source, why it matters, and the trigger level or event (e.g. "in-house core commercial by H2 FY27 (Concall p.8)"; "OEM insourcing capacity additions").
2. **Open questions** — what the corpus could not answer, split into questions for management and checks for channels, customers or suppliers.

## Appendices

- **Sanity-check log** — every flag from the analyst sanity checks.
- **Glossary** — every technical term, in plain English.
- **Source register** — as specified under Citations.

---

# Visual and film standards

## All diagrams

- Each figure answers **one question**, stated in its title (e.g. "Where does the bushing sit in the grid?"). Number every figure.
- **Cut the noise:** at most five labelled elements per view; no decorative detail; one accent colour for the company's position, neutral greys for everything else.
- Every figure has a caption with its sources (document + page).
- Build in inline SVG with `viewBox` scaling so it works on mobile; no horizontal page scroll at phone width.

## 3D isometric static diagrams

Draw with a small inline-SVG isometric helper (project x, y, z to 2D; primitives for boxes, cylinders and labels). Use them for the industry chain, the zoom ladder and the product cut-away. Keep depth cues simple: three face shades per object.

## 3D films

- **Library:** three.js r128 from cdnjs (`https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js`); everything else inline.
- **Length and structure:** 30–45 seconds; 4–6 scenes; one idea per scene; scene buttons to jump, play/pause, scrubber, elapsed time.
- **Captions:** each scene has a plain-language caption with its citation; at most four on-screen labels at once, projected from 3D positions onto DOM labels.
- **Palette:** a fixed dark "dusk" palette independent of the page theme, so contrast is stable in light and dark mode. Avoid overexposed lighting; keep glow effects subdued.
- **Robustness:** cap device pixel ratio (~1.75); cap frame delta so the film keeps real time on slow devices; pause when off-screen; give each film unique element IDs and scoped selectors; if WebGL is unavailable, show a static storyboard (key frames as SVG with captions) instead.
- **Honesty:** label every film "Illustration, not footage" and do not show anything the sources do not support (e.g. do not show the company performing a step it outsources).
- **Testability:** expose `window.__filmN = {seek, play, pause}` for each film.

## Production-process film pattern

Stations left to right in process order (e.g. winding → drying oven → impregnation → assembly → testing). The product visibly changes state at each station (colour, layers added, liquid level). The caption names the step, the duration where sourced, and whether the company does it in-house.

## Criticality film pattern

Start at system level (e.g. the grid), zoom into the system component (the transformer), then the product, show its normal function, then the failure and its consequence (e.g. flashover → fire → outage), ending on the cost-share vs consequence point.

---

# Output

- One **self-contained interactive HTML report**: sticky table of contents; collapsible parts; the "How this report is built" and "Module takeaways" boxes at the top; appendices at the end.
- Tables: sortable where useful; always wrapped in a horizontally scrollable container; no fixed widths wider than their column; side-by-side tables reflow on narrow screens. The right-most column of every table must be visible.
- Styling: clean and professional; reads like a research note, not a marketing page.
- **Delivery:** publish with the Artifact tool when available (one artifact per company, republished to the same URL on later updates); also save a copy to `/mnt/user-data/outputs/` and, when a research folder is connected, to that folder. Save a short markdown summary of the key findings to the project.

## Build checks (run before delivering)

Run the page headless (Playwright + Chromium) and confirm:

- zero JavaScript errors in the console;
- no horizontal overflow at 400 px width;
- every inline citation and table-of-contents link resolves to an anchor;
- each film exposes its test API, advances when played, and seeks to each scene;
- no table is clipped;
- take screenshots of each figure and each film scene and look at them: labels readable, nothing overlapping, nothing too dark or washed out.

Tell the user anything that could not be verified (e.g. smooth playback on real devices).

# Quality-control checklist

- "How this report is built" box present: emphasis profile, zoom levels, visual-plan scores, multi-segment choice.
- Depth follows the emphasis profile; Brief parts are genuinely brief.
- Product 101 uses plain words, one analogy per hard concept, a cut-away with at most five labelled parts, and a Q&A explainer for the critical sub-component where relevant.
- Zoom ladder runs from the industry to the company's product, with market sizes at each level.
- Content-per-unit table present (where the product goes into another product), with the company's main zone highlighted and derivations shown.
- Criticality 2×2 with sourced evidence on both axes.
- Industry sizing: historical series and CAGR, segments, end-user mix, TAM/SAM/SOM, triangulated across peers' filings, conflicts disclosed.
- Profit pools by chain stage from peer filings; chokepoints and make-vs-buy per process step marked.
- Volume × realisation table is the company's own numbers only.
- Evolution and its quantified financial impact appear inline, limited to value-chain causes, with the exact pointer line where other drivers exist.
- Qualification gates mapped where customers approve suppliers; company claims separated from the company's actual record.
- Moat-location map with evidence and weakening factors; no moat verdict.
- Monitorables and open questions present.
- Every fact cited with document and page; web facts with URL and date; general knowledge, analyst arithmetic, analyst view and assumptions tagged; source register lists what was taken from each document.
- Every conclusion labelled Fact / Inference / Hypothesis; every derived number shows formula, inputs, tier, page and period.
- Management statements classified A/B/C; no guidance blended with actuals.
- Sanity-check log present; internal inconsistencies flagged with both pages.
- Nothing fabricated: market share, utilisation, segment margins, concentration, industry size, end-product prices and content per unit are sourced or marked `Unavailable — not in source`.
- Visuals follow the Step 0 plan; films labelled as illustrations; build checks passed.
- No business overview, executive summary, P&L decomposition, management audit, growth attribution, moat verdict, risk or valuation content.

# Failure / escalation rules

- **Corpus insufficient for a part** → say which part and which documents are needed; do not fabricate.
- **Market size, share, utilisation or end-product prices not in the corpus** → `Unavailable — not in source`; if web sources would fill the gap, ask the user once whether web is allowed.
- **Sources conflict** → apply the conflict order; disclose unresolved conflicts.
- **Only standalone available** → proceed on standalone and flag it prominently.
- **WebGL or the CDN unavailable in testing** → ship the static storyboard fallback and say so.