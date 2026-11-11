---
name: management-analysis
description: "Use this skill to audit management quality, guidance credibility, capital allocation, board depth, and governance risk for a listed company within a specified industry using project documents as the primary evidence base."
license: "Proprietary. © 2026 Finnacle Institute. All rights reserved. See LICENSE."
---

> **Curated by Vastav Parikh & Yash Master for Finnacle Shah Classes.**  
> Intellectual property of Finnacle Institute. © 2026 Finnacle Institute. All rights reserved.  
> Keep this notice intact in any copy or modified version of this file.

---
name: industry-management-governance-audit
description: Use this skill to audit management quality, guidance credibility, capital allocation, board depth, and governance risk for a listed company within a specified industry using project documents as the primary evidence base.
---

# Purpose

Use this skill to conduct a rigorous, evidence-led audit of a listed company's management in the context of its industry.

The skill is designed for buy-side diligence, position sizing, management-quality review, governance stress-testing, and pre-investment decision support. It is not a generic company-summary skill. It is specifically for determining whether management deserves trust on competence, capital allocation, guidance credibility, governance quality, and minority-shareholder alignment.

The skill must prioritize primary evidence from project documents and remain skeptical, neutral, auditable, and falsifiable.

# How To Use This Skill

This skill is designed to be self-contained.


Place all supporting evidence in the same project, including as available:
- annual reports
- exchange filings
- investor presentations
- conference call transcripts
- AGM transcripts
- corporate governance reports
- shareholding disclosures
- remuneration disclosures
- related party transaction disclosures
- official regulatory or court orders
- proxy adviser reports, if the user explicitly permits them

Do not rely on a separate scoring attachment. Use the embedded scoring framework in this file.

At runtime, the task prompt should provide only the company-specific details that vary by case, such as:
- target company
- industry
- analysis period
- peer set if known
- whether secondary governance-forensic sources are allowed

Treat the project documents as the default evidence corpus.

# When To Use This Skill

Use this skill when the goal is to evaluate one or more of the following:

- management competence
- scale-up quality
- capital allocation track record
- guidance credibility vs actual delivery
- antifragility during stress periods
- promoter alignment and ownership structure
- related party risk
- dilution, pledging, or minority-shareholder treatment
- board and KMP quality
- management depth, retention, and succession risk
- governance and forensic red flags

This skill is especially appropriate for:
- pre-investment diligence
- IC memo support
- management quality scorecards
- governance risk reviews
- management meeting preparation
- conviction sizing for concentrated positions

# When Not To Use This Skill

Do not use this skill for:
- a quick fact lookup
- valuation-only work
- industry overviews with no management objective
- a simple transcript summary
- live-news monitoring
- claims that require evidence outside the project when that evidence is unavailable
- speculative allegations unsupported by cited materials

# Required Inputs

The user or project should supply:

1. `target_company`
2. `industry_name`
3. `analysis_period`
   - default: last 5 fiscal years plus latest available interim period
4. `primary_document_pack`
   - annual reports
   - filings
   - presentations
   - conference call transcripts
   - AGM transcripts if available
5. `output_preference`
   - full memo
   - scorecard-first
   - table-first
   - note-first

# Optional Inputs

Use these if provided:

- `peer_set`
- `industry_specific_kpis`
- `known_red_flags_to_test`
- `specific_management_claims_to_verify`
- `stress_period_to_test`
- `secondary_governance_sources_allowed`
- `preferred_score_weights`
- `exclusions`

If `peer_set` is not provided, propose the 3 most relevant listed peers and state the basis for selection before proceeding.

# Workflow

## Step 1 — Confirm the Operating Frame Before Full Analysis

Before substantive analysis, explicitly confirm:

- target company
- industry
- analysis period
- proposed peer set
- source boundary
- whether secondary governance-forensic sources are permitted
- requested output form

Do not silently assume these as they materially affect the work.

If a key input is missing, ask one targeted clarification question. If the missing point is not material, make the narrowest defensible assumption and label it.

## Step 2 — Define the Core Variables Before Analysis Begins

Before analysis, list the core variables relevant to this company and industry.

Always include these universal variables:
- growth quality
- capital allocation quality
- return profile
- working-capital or balance-sheet discipline
- guidance credibility
- governance alignment
- board and KMP quality
- succession depth
- minority-shareholder treatment

Then add industry-specific variables.

Examples:
- Banks / NBFCs:
  - liability franchise
  - cost of funds
  - NIM
  - asset quality
  - credit cost
  - ALM
  - capital adequacy
- IT services:
  - pricing
  - bill-rate trajectory
  - utilization
  - delivery mix
  - attrition
  - margin offsets
  - deal quality
- Consumer:
  - volume growth
  - pricing power
  - gross margin
  - channel mix
  - inventory discipline
  - distribution productivity
- Manufacturing / Industrials:
  - capacity utilization
  - asset turns
  - capex productivity
  - order-book quality
  - input-cost pass-through
  - receivables discipline

For each variable, state:
- why it matters
- which section it belongs to
- which source types should evidence it

Do not proceed to final judgment until the variable list is explicit.

## Step 3 — Neutralize the Frame

Before taking a view, restate the management question neutrally.

Identify:
- the user’s implied premise, if any
- 2–3 plausible alternative framings
- what evidence would distinguish between them

Do not simply inherit the user’s tone. Convert directional phrasing into neutral analytical language.

Examples:
- replace “great management” with “management with evidence-backed strengths and weaknesses”
- replace “governance red flag” with “potential governance concern pending evidence review”

## Step 4 — Apply the Source Hierarchy

Use this source hierarchy throughout the analysis.

### Tier 1 — Verified Primary
Highest authority.
Examples:
- annual reports
- audited financial statements
- official filings
- official shareholding disclosures
- official remuneration disclosures
- official related party disclosures
- official AGM notices or transcripts where filed
- official regulator or court orders

### Tier 2a — Independent Verification
Use when relevant and available.
Examples:
- IiAS
- SES governance
- formal regulatory commentary
- Credit rating surveillance reports where they provide factual detail

### Tier 2b — Management Communications
Useful but not definitive on contested facts.
Examples:
- conference call transcripts
- investor presentations
- management commentary
- Management official interviews included in project materials

### Tier 3 — Secondary Governance Commentary
Use only in the governance stress-test section and only if explicitly permitted.
Examples:
- Moneylife
- Dr. Vijay Malik
- other user-approved forensic commentary

### Tier 4 — Unverified Background
Do not use as evidence.

When sources conflict:
1. higher tier wins
2. if same tier, more recent wins
3. if same recency, more specific wins
4. if still unresolved, present both and label the conflict

When Tier 2a or Tier 3 flags a factual concern that Tier 2b does not address, label it:
**Disclosure Gap**

Do not silently resolve it.

## Step 5 — Conduct the Management Competence Audit

### 5.1 Evolution and Scale

Evaluate how the company moved from earlier scale to current position.

Assess:
- revenue growth over the analysis period
- margin and return-ratio progression
- market-position improvement where evidenced
- peer comparison versus top peers
- whether scale came from:
  - disciplined organic expansion
  - productive capex
  - efficient reinvestment
  - prudent acquisitions
  - or lower-quality methods such as loose working capital, growth with worsening cash conversion, repeated dilution, or high-risk acquisitions

Explicitly test:
- working-capital quality during growth
- return quality ROE/ROCE/ROIC during scale-up
- acquisition dependence vs organic compounding
- whether growth quality weakened as scale rose

### 5.2 Capital Allocation Track Record

Audit where capital was deployed and whether it earned acceptable returns.

Assess:
- segmental capital allocation where data permits
- capex decisions
- M&A decisions
- leverage policy
- dividend / buyback behavior
- whether the best-return businesses received incremental capital
- whether weak businesses absorbed disproportionate capital
- what management mistakes occurred
- how quickly and credibly they were corrected

Do not call something a mistake unless supported by evidence such as:
- write-downs
- underutilized capacity
- abandoned strategy
- repeated guidance resets
- margin collapse
- management admission
- reversal after poor results

### 5.3 Antifragility

Select at least one period of industry stress.

Test whether management:
- protected margins better than peers
- protected cash generation better than peers
- preserved balance-sheet quality
- avoided destructive dilution
- gained share or strategic position while weaker peers struggled

Do not use vague phrases like “handled downturn well.”
State:
- the exact bad period
- what happened to the industry
- what happened to peers
- what happened to the company
- what management actions explain the difference

## Step 6 — Conduct the Guidance vs Deliverables Audit

Review the last 5 years of:
- conference call transcripts
- annual reports
- investor presentations
- Management Interviews/Management Interview transcripts 
- AGM transcripts if available

Capture guidance across:
- volume growth
- revenue growth
- margin
- capex
- returns
- leverage or balance-sheet targets
- industry-specific KPIs

For each guidance item:
1. record the exact guidance statement
2. classify it as:
   - Formal Quantitative Guidance
   - Directional Commentary
   - Aspirational Target
3. cite the exact source and period
4. identify the later actual outcome
5. judge it as:
   - Achieved
   - Partially Achieved
   - Not Achieved
   - Unclear / Unmeasurable
6. explain why that judgment is supported
7. note whether management later:
   - reaffirmed
   - diluted
   - reframed
   - reset
   - stopped mentioning it

If a management claim cannot be verified from primary documents, label it:
**Unsubstantiated Statement**

Do not convert qualitative optimism into delivered performance.

## Step 7 — Conduct the Corporate Governance and Forensic Check

Primary disclosures remain the base layer.

Secondary governance or forensic sources may be used only if explicitly allowed.

### 7.1 Ownership and Structure

Map the evolution of:
- promoter holding
- promoter reclassification
- cross-holdings
- holding-company layers
- multi-layer subsidiary structures
- trusts, LLPs, or private entities linked to control
- structural complexity that may reduce transparency

### 7.2 Unlisted Interests and Related Party Transactions

Check whether promoters or KMPs have interests in private entities connected to:
- suppliers
- customers
- distributors
- service providers
- adjacent or overlapping businesses

Audit RPTs for:
- scale
- recurrence
- unusual terms
- economic rationale
- weak disclosure
- potential value transfer

### 7.3 Pledging and Dilution

Review history of:
- promoter pledging
- preferential allotments
- warrants
- conversions
- repeated issuance
- dilution events that may have disadvantaged minorities

### 7.4 Remuneration and ESOP Audit

Compare:
- KMP pay growth vs net profit growth
- KMP pay growth vs business outcomes
- ESOP dilution over time
- vesting design
- performance linkage
- whether compensation appears aligned with durable value creation

### 7.5 Integrity Watch

List material:
- litigations
- regulatory notices
- insider trading matters
- governance disputes
- accounting disputes
- auditor concerns
- resignations of key directors or auditors
- proxy-adviser vote-against recommendations
- repeated governance concerns

### 7.6 Secondary Governance Stress Test

Use this only if secondary sources are explicitly allowed.

Check whether IiAS, SES, Moneylife, Dr. Vijay Malik, or other permitted sources flagged:
- vote-against recommendations
- problematic reappointments
- auditor-fee concerns
- RPT concerns
- governance circularity
- disclosure weaknesses
- promoter-benefiting structures
- minority-unfriendly resolutions

Do not present secondary commentary as established fact unless it is tied back to cited documents.

Use secondary commentary to:
- stress-test management disclosures
- surface unresolved conflicts
- generate diligence questions
- highlight where primary disclosure may be incomplete

## Step 8 — Build the KMP and Board Profile

Create a structured profile table covering:

1. Name
2. Role
3. Date of appointment
4. Education
5. Relevant experience
6. Specific value-add to the business
7. External directorships
8. Latest disclosed shareholding
9. Litigation / regulatory encumbrance status
10. Retention status over the period

If any field is unavailable, state:
**UNKNOWN**

Do not infer pedigree or litigation status.

## Step 9 — Assess Management Depth and Stability

Review the last 5 years for:
- KMP changes
- CEO / CFO / COO / business-head turnover
- independent-director turnover
- cluster departures around difficult periods
- founder dependence
- second-line visibility
- succession depth
- board refresh quality

Assess whether leadership depth is institutional or concentrated in one or two individuals.

## Step 10 — Score and Synthesize

After evidence review, score each factor using the embedded scoring framework.

Do not score based on:
- tone
- reputation
- market narrative
- personal admiration
- one-off management charisma

Every score must include:
- score
- short evidence note
- source basis
- unresolved uncertainty if any

Then synthesize into:
- Management Competence score
- Guidance Credibility score
- Governance & Forensic score
- Management Depth & Stability score
- Overall management trust view

End with:
- what is proven
- what is strongly suggested
- what remains unknown
- what would change the conclusion

# Clarification Rules

Ask one targeted clarification question only when the missing point materially changes the analysis.

Material items include:
- industry
- geography
- analysis period
- peer set if peer comparison is central
- whether secondary governance-forensic sources are allowed
- whether the user wants a note-first or table-first output

If peer set is missing, propose a default peer set and state the basis.

If the project corpus is incomplete, proceed only as far as the evidence allows and clearly label what cannot be concluded.

# Evidence and Reasoning Guardrails

## Evidence Classes

Every material statement must be labeled as one of:
- Fact
- Estimate
- Opinion
- Unknown

Definitions:
- Fact = verified, source-backed, period-tagged statement
- Estimate = derived conclusion or modeled number with assumptions shown
- Opinion = attributed view from management, proxy adviser, analyst, or this analysis
- Unknown = evidence is insufficient

## Unknown Rule

If evidence is insufficient, state:
**UNKNOWN**

Do not fill gaps with plausible detail.
Do not present inference as fact.
Do not convert management language into verified truth.

## Numbers Must Have Periods

Every numerical statement must include:
- exact period
- comparison base
- whether QoQ / YoY / vs average / vs peer
- source basis

Do not mix periods without disclosure.

## Derived Numbers Must Show Their Work

For every derived number, show:
- formula or logic
- inputs
- source basis for each input
- period for each input
- assumptions
- update trigger

## Guidance Discipline

Classify every management statement as:
- Formal Quantitative Guidance
- Directional Commentary
- Aspirational Target

Never treat commentary or aspiration as delivered guidance.

## Load-Bearing Claims

Classify claims as:
- Load-Bearing
- Supporting
- Background

Load-Bearing claims should, where possible, rest on at least two independent supporting sources and preferably include one Tier 1 source.

## Citation Discipline

Every factual claim must carry a traceable source reference using available project evidence.

At minimum, identify:
- source type
- document
- period or date
- section or context
- page or location if available

Do not fabricate citations.
Do not imply a document was reviewed if it was not.

## Reasoning Method

Reason from first principles after the variable list is defined.

Do not default to consensus narratives.
Use outside commentary only for triangulation and reconciliation.
If the evidence does not support a strong conclusion, keep the conclusion weak.

## Falsifiability

After forming the conclusion, state:
1. the single assumption the conclusion cannot survive
2. the evidence that would force revision
3. the monitorables that should be tracked going forward

# Scoring Framework

Use a 1 to 5 scale.

- 1 = clear concern / repeated evidence of weak quality
- 2 = below average / multiple unresolved concerns
- 3 = mixed / balanced or incomplete evidence
- 4 = good / mostly positive with monitorables
- 5 = strong / evidence-backed quality with limited concern

Do not give half-points unless the user explicitly asks.

## Default Weights

### Management Competence — 40%
- Evolution & Scale — 12%
- Capital Allocation — 18%
- Antifragility — 10%

### Guidance Credibility — 20%
- Guidance accuracy across revenue / volume / margin / KPIs — 15%
- Candor and measurability of guidance — 5%

### Governance & Forensic — 25%
- Ownership & structure — 5%
- RPT / unlisted interests — 8%
- Pledging / dilution — 4%
- Remuneration / ESOP — 4%
- Integrity / proxy / regulatory flags — 4%

### Management Depth & Stability — 15%
- KMP retention — 8%
- Succession depth / second line — 7%

## Scoring Anchors

### Evolution & Scale
- 1: Growth relied on weak balance-sheet discipline, risky acquisitions, or poor-quality scaling
- 3: Growth was credible but mixed in quality
- 5: Growth was disciplined, durable, and supported by strong operating quality

### Capital Allocation
- 1: Capital repeatedly flowed to weak-return uses with poor correction
- 3: Mixed allocation record with both good and poor decisions
- 5: Capital largely flowed to high-return, strategically justified uses with evidence of learning

### Antifragility
- 1: Performance deteriorated worse than peers in stress periods
- 3: Resilience was mixed
- 5: Management preserved economics and position better than peers in bad times

### Guidance Credibility
- 1: Repeated misses, evasive language, or untestable statements
- 3: Mixed record on delivery and transparency
- 5: Specific, measurable guidance with strong delivery or credible transparent resets

### Ownership & Governance Structure
- 1: Opaque, complexity-adding, minority-unfriendly structure
- 3: Some complexity but manageable
- 5: Clear, stable, minority-readable structure

### RPT / Unlisted Interests
- 1: Material conflict or value-shifting risk
- 3: Some risk but not clearly abusive
- 5: Limited, well-explained, well-disclosed related-party exposure

### Pledging / Dilution
- 1: Meaningful adverse history
- 3: Some past concerns or limited benign dilution
- 5: Clean or clearly non-abusive history

### Remuneration / ESOP
- 1: Pay and dilution poorly aligned with outcomes
- 3: Mixed alignment
- 5: Strong alignment with durable value creation

### Integrity / Proxy / Regulatory Flags
- 1: Repeated material concerns or unresolved serious flags
- 3: Some concerns but not clearly systemic
- 5: Few material concerns and no meaningful pattern of integrity failure

### Management Depth & Stability
- 1: Key-person dependence, turnover, weak succession visibility
- 3: Moderate continuity with some bench concerns
- 5: Stable leadership bench with visible succession depth

# Output Requirements

Produce the final output in this order.

## 1. Executive Verdict
A short conclusion on:
- management competence
- governance quality
- overall trust level
- key reservation, if any

## 2. Score Summary Table
Show:
- section
- weight
- score
- weighted score
- short reason

## 3. Management Competence
Cover:
- Evolution & Scale
- Capital Allocation
- Antifragility

Use evidence-backed subheadings.

## 4. Guidance vs Deliverables Table
Required columns:
- Year / period
- Source
- Guidance statement
- Classification
- Later actual outcome
- Status
- Evidence note

## 5. Corporate Governance & Forensic Check
Use subsections:
- Ownership & Structure
- Unlisted Interests & RPTs
- Pledging & Dilution
- Remuneration & ESOP
- Integrity Watch
- Secondary Governance Stress Test, if permitted

## 6. KMP & Board Profile Table
Required columns:
- Name
- Role
- Appointment date
- Education / pedigree
- Relevant experience
- External directorships
- Shareholding
- Litigation / regulatory status
- Comment

## 7. Management Depth & Stability
Provide:
- key exits / joins over 5 years
- stability assessment
- succession-risk view

## 8. Key Monitorables
List the variables that should be watched to update the view.

## 9. Open Unknowns
Explicitly state what cannot be concluded from available evidence.

## 10. Failure Condition / Revision Trigger
State:
- the assumption the thesis cannot survive
- the evidence that would force a revision

# Style Rules

- Be direct, skeptical, and objective
- Avoid vague praise or vague criticism
- Use bold only for the most important findings
- Use tables where required
- Prefer precise claims over broad narratives
- Label any unverifiable management claim as **Unsubstantiated Statement**
- Separate actuals from commentary and aspirations
- Admit uncertainty explicitly

# Quality Control Checklist

Before finalizing, verify that:

- the operating frame was confirmed
- the core variables were defined explicitly
- the question was neutralized before conclusions
- peer set was stated or defensibly proposed
- every major claim has evidence support
- every major number has a period
- derived math is shown where used
- guidance is separated from actual delivery
- governance commentary does not outrun the evidence
- secondary sources were used only if permitted
- unresolved conflicts are visible
- unknowns were not filled in
- final conclusions are falsifiable
- the output is usable as an analyst-grade note without major rewriting

# Failure / Escalation Rules

Stop or narrow scope when:

- primary documents are unavailable
- the industry is missing and materially changes the variable map
- the peer comparison cannot be done credibly
- governance allegations rely only on unverified commentary
- citations cannot be tied to reviewed project materials
- the user asks for certainty beyond the evidence
- the corpus does not support a conclusion on a requested issue

In those cases:
1. state exactly what is missing
2. state what can still be concluded
3. label the unresolved area as UNKNOWN
4. identify the minimum additional evidence needed