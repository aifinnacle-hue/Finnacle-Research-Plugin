---
name: equity-doc-sourcing-llama
description: "Source, download, and convert Indian equity research documents (Annual Reports, Concall Transcripts, Investor Presentations) for any BSE/NSE-listed company and its competitors, using the LlamaParse connector for high-fidelity PDF-to-Markdown conversion. Trigger this skill whenever a user asks to download company documents or build a research library AND mentions LlamaParse, LlamaIndex, premium parsing, high-quality parsing, better table extraction, or asks for the \"llama\" variant of the doc-sourcing pipeline. Also trigger when the user says \"use LlamaParse for [company]\" or \"download docs with LlamaParse\" or wants cleaner Markdown output from PDFs than pdfplumber produces. For the standard pdfplumber-based pipeline, use the equity-doc-sourcing skill instead."
license: "Proprietary. © 2026 Finnacle Institute. All rights reserved. See LICENSE."
---

> **Curated by Vastav Parikh & Yash Master for Finnacle Shah Classes.**  
> Intellectual property of Finnacle Institute. © 2026 Finnacle Institute. All rights reserved.  
> Keep this notice intact in any copy or modified version of this file.

# Equity Document Sourcing Skill — LlamaParse Variant (LlamaParse connector)

End-to-end pipeline for acquiring Annual Reports, Concall Transcripts, and Investor Presentations for BSE/NSE-listed Indian companies and converting them to high-fidelity Markdown with **LlamaParse, through the LlamaParse connector** in Claude.

This is the premium-parsing variant of `equity-doc-sourcing`. Use it when the user wants clean Markdown tables from financial statements (LlamaParse preserves table structure faithfully; pdfplumber produces flat text dumps).

The connector carries the user's own LlamaCloud sign-in, and parsing is billed to that account. This skill never asks for, reads or stores a LlamaCloud API key.

## Step 0 — Access check (before anything else)

Confirm the **LlamaParse connector** is available in this session (its tools include `uploadFileByUrl`, `getUploadUrl`, `parseFile`, `parseWithLiteParse` and `estimateFileComplexity`).

If it is not, stop and tell the user:

```
This skill converts documents through the LlamaParse connector, which isn't connected yet.
Connect "LlamaParse" in Claude (Settings → Connectors), sign in with your LlamaCloud
account, then ask me again.
```

Do not offer an API-key route, and do not ask the user to paste a key.

## Step 1 — Collect User Input

Ask the user:

1. **Primary company** — "What company do you want documents for?"
2. **Peers/Competitors** — "Which peer or competitor companies should I include?" (1-5 names)
3. **Years of history** — "How many years of data do you need?" (default: 10)
4. **Output location** — where the files should end up: a folder on their computer (if this conversation is linked to it) or files delivered in the conversation (default when no folder is linked).

Do NOT proceed to URL discovery until all four inputs are confirmed.

## Step 2 — Discover Document URLs

Identical to the base `equity-doc-sourcing` skill. For EACH company (primary + peers):

### 2a. Find the Screener.in page

Search the web for `screener.in [COMPANY NAME] consolidated` and fetch the page. From the Documents section, extract:
- All **Annual Report** links (labeled "Financial Year YYYY from bse")
- All **Concall Transcript** links (labeled "Transcript")
- All **Investor Presentation** links (labeled "PPT")

Note the filing date shown next to each document; it feeds the Upload Date in Step 5.

### 2b. If the page truncates

Use a browser (Claude in Chrome or the built-in browser, whichever is available). Navigate to the Screener.in page and run JavaScript extraction in three passes (transcripts, PPTs, annual reports).

### 2c. Supplement from the company IR website

Search for `[COMPANY NAME] investor relations annual reports`. Essential for:
- Companies listed less than 10 years (pre-IPO reports)
- Older concall transcripts not indexed by Screener
- Documents where BSE links return 403

### 2d. URL source priority

1. **Screener.in → BSE PDFs** (most reliable)
2. **Company IR website** (direct PDFs, backup)
3. **BSE corporate announcements search** (last resort)

### Known BSE URL patterns

```
Recent filings:  https://www.bseindia.com/stockinfo/AnnPdfOpen.aspx?Pname={GUID}.pdf
Older filings:   https://www.bseindia.com/xml-data/corpfiling/AttachHis/{GUID}.pdf
Annual reports:  https://www.bseindia.com/bseplus/AnnualReport/{BSE_CODE}/{BSE_CODE}03{YY}.pdf
```

## Step 3 — Confirm Scope Before Spending Credits

Summarize for the user before converting anything:
- Total documents discovered, broken down by company and doctype
- The LlamaParse tier each doctype will use (Step 4c)
- Any gaps or companies where discovery failed
- A reminder that parsing uses credits on their own LlamaCloud account

Wait for the user's go-ahead. They may trim the list (for example, fewer years of annual reports) or override the tiers.

## Step 4 — Fetch and Convert Each Document

Work through the documents one at a time. Never hold more than one document's text in the conversation: write each result to its `.md` file as soon as it arrives.

### 4a. Get the PDF into LlamaCloud

1. **By URL (first choice).** Call `uploadFileByUrl` with the document URL, `fileName` set to the canonical name from 4d (with `.pdf`), `fileType` `application/pdf` and `purpose` `parse`. It returns a file ID.
2. **Local upload (when the URL route fails,** for example BSE refusing LlamaCloud's fetch with 403). Download the PDF into the workspace with a browser-like `User-Agent` header and up to 3 retries with exponential backoff. Then call `getUploadUrl` and POST the file as a multipart form under the `file` key to the URL it returns; the response contains the `file_id`. The upload URL expires after a few minutes, so request a fresh one per batch.
3. **Ask the user (last resort).** If neither route works, list the documents that could not be fetched and ask the user to attach those PDFs; upload them as in step 2.

Whenever the workspace can download a PDF, also keep a copy under `pdfs/` (Step 6).

### 4b. Parse

Call `parseFile` with the file ID, `markdown` true and the tier from 4c.

- **Long documents:** first call `estimateFileComplexity` (free) to learn the page count. For documents over ~40 pages, parse in page ranges of about 25 pages using the `pages` parameter, appending each range's text to the `.md` file in order. Check the first range's output to confirm the page numbering matches what you asked for.
- Write the Document Information block (Step 5) at the top of the file before the first parsed text.

### 4c. Tier routing by doctype

| Doctype | LlamaParse tier | Rationale |
|---|---|---|
| Annual Report | `agentic_plus` | Complex tables, financial statements, multi-column layouts |
| Investor Presentation | `agentic` | Charts and graphics, but simpler than ARs |
| Concall Transcript | `cost_effective` | Prose-heavy, minimal structure |

Tier routing is the default, not mandatory. If the user wants everything on `agentic_plus` (maximum fidelity) or everything on `cost_effective` (minimum cost), apply that override to the entire run.

### 4d. Naming conventions

| Document type | Pattern | Example |
|---|---|---|
| Annual Report | `{Company}_AR_FY{YY}.pdf` / `.md` | `Thyrocare_AR_FY25.pdf` |
| Concall Transcript | `{Company}_CC_Q{N}FY{YY}.pdf` / `.md` | `DrLal_CC_Q4FY25.pdf` |
| Investor Presentation | `{Company}_PPT_Q{N}FY{YY}.pdf` / `.md` | `Metro_PPT_Q2FY26.pdf` |

Use short company names (e.g., Thyrocare, DrLal, Metro, Apollo, MaxHealth, Fortis, Narayana, Syngene, Laurus, Divis).

### 4e. Track every document

Keep a running log (`download_log.txt` and `conversion_log.txt`) with, per document: canonical name, source URL, upload route used (URL / local upload / user-attached), tier, pages parsed, status, error message if any, timestamp.

### 4f. Handle failures

- If a parse fails with a **credit or quota error** (a message mentioning credit, quota, insufficient or payment), stop converting immediately. Keep logging the remaining documents as not converted, and go to Step 7.
- Any **other failure** (malformed PDF, timeout, unsupported file): log it, skip that document and continue.
- **Do NOT fall back to another parser automatically.**

## Step 5 — Mandatory Document Metadata Block

Every Markdown file — whether converted with LlamaParse or a fallback — MUST begin with a Document Information block. This is non-negotiable. The block gives downstream analysis (LLMs, indexing, manual review) unambiguous context about what the file contains.

### 5a. Required fields

The block must include these four fields, in this order:

| Field | Definition | Source |
|---|---|---|
| **Document Name** | The canonical filename without extension | Derived from the naming convention in 4d (e.g., `Thyrocare_AR_FY25`) |
| **Period Covered** | The fiscal period the document reports on, expressed as both short form and explicit date range | Parsed from the filename suffix |
| **Upload Date** | The date the document was originally filed / published by the company | See 5d |
| **Description** | A 1-2 sentence description of the document's contents | Template-based by doctype — see 5c |

### 5b. Exact Markdown format

Emit this block verbatim at the top of every `.md` file, before any parsed content:

```markdown
# {Document Name}

## Document Information

| Field | Value |
|---|---|
| **Document Name** | Thyrocare_AR_FY25 |
| **Period Covered** | FY25 (1 April 2024 – 31 March 2025) |
| **Upload Date** | 15 July 2024 |
| **Description** | Annual Report of Thyrocare Technologies Limited for Financial Year 2025. Contains audited consolidated and standalone financial statements, management discussion and analysis, director's report, auditor's report, and corporate governance disclosures. |

---

{parsed markdown content starts here}
```

### 5c. Description templates by doctype

- **Annual Report** → `Annual Report of {Company} for {Period}. Contains audited consolidated and standalone financial statements, management discussion and analysis, director's report, auditor's report, and corporate governance disclosures.`

- **Concall Transcript** → `Earnings conference call transcript of {Company} for {Period}. Contains management's prepared remarks on quarterly financial and operational performance, followed by a Q&A session with sell-side analysts and institutional investors.`

- **Investor Presentation** → `Investor presentation of {Company} for {Period}. Summarises business performance, financial highlights, segmental metrics, strategic initiatives, and forward-looking commentary shared with the investor community.`

### 5d. Upload Date logic

Populate Upload Date using this cascade:

1. **Filing date from the source listing** — the date shown next to the document on Screener.in or BSE (Step 2a).
2. **PDF `CreationDate` metadata** — when a local copy exists, read it (e.g. with `pypdf` or `pdfplumber`); the `D:YYYYMMDD...` format becomes `DD Month YYYY` (e.g., `15 July 2024`).
3. **Filename period as proxy** — infer a plausible filing window from typical Indian filing timelines (AR → July–September following FY end; Concall → within 60 days of quarter end; IP → around concall date) and append `(inferred from period)`.
4. **Last resort — `Unknown`.** Do not guess.

### 5e. Period formatting

| Filename suffix | Period Covered value |
|---|---|
| `FY25` | `FY25 (1 April 2024 – 31 March 2025)` |
| `Q1FY26` | `Q1 FY26 (April – June 2025)` |
| `Q2FY26` | `Q2 FY26 (July – September 2025)` |
| `Q3FY26` | `Q3 FY26 (October – December 2025)` |
| `Q4FY25` | `Q4 FY25 (January – March 2025)` |

### 5f. Backfilling existing files

If the user has existing converted files without the block and asks for a backfill: walk the `markdown/` tree, skip files that already have a `## Document Information` block, derive doctype, company and period from the filename, take the Upload Date per 5d, prepend the block, and log each file as `UPDATED`, `SKIPPED (already has block)` or `FAILED (reason)` in `backfill_log.txt`. Do this only when the user explicitly asks.

## Step 6 — Output Organization and Delivery

```
{OUTPUT_BASE}/
├── pdfs/
│   ├── {company1}/
│   │   ├── annual_reports/
│   │   ├── concalls/
│   │   └── presentations/
│   └── {company2}/ ...
├── markdown/
│   ├── {company1}/
│   │   ├── annual_reports/
│   │   ├── concalls/
│   │   └── presentations/
│   └── {company2}/ ...
├── download_log.txt
├── conversion_log.txt
└── research_log.md
```

If the conversation is linked to the user's computer, write the tree into the folder they named. Otherwise build it in the workspace and send it to the user (a single `.zip` for large runs).

## Step 7 — Failure Protocol (when any conversion failed)

### 7a. Classify the failures

- **Credit exhaustion** — conversion stopped on a credit/quota error
- **Individual failures** — specific documents failed for other reasons while others succeeded

### 7b. Ask the user how to proceed — do not assume

```
{N} documents could not be converted with LlamaParse:

  - Credit exhaustion: {X} documents (your LlamaCloud credits ran out)
  - Other failures: {Y} documents (malformed, timeout, etc.)

How would you like to proceed?

  [A] Free fallback for the failed documents — LiteParse through the same
      connector (no credits; lower fidelity, tables may be flattened)
  [B] Top up your LlamaCloud credits and resume with LlamaParse
      (top up at https://cloud.llamaindex.ai/billing, then say "resume")
  [C] Mix — free fallback for the non-credit failures, top up and resume
      for the credit-exhausted ones
```

### 7c. Execute the user's choice

- **Fallback:** convert with `parseWithLiteParse` (`markdown` true). If LiteParse also fails and a local PDF copy exists, offer pdfplumber in the workspace as a further fallback. Mark every fallback file with a header line directly under the Document Information block: `<!-- CONVERTED WITH FALLBACK PARSER (LiteParse/pdfplumber) - TABLES MAY BE FLATTENED -->`.
- **Resume:** after the user confirms the top-up, re-run Step 4 for the logged failures only, with the same tier routing.

## Step 8 — Research Log

Write `research_log.md` at the output root, containing:

- Date of acquisition
- Company names and BSE codes
- Every document: filename, source URL, upload route, conversion method (LlamaParse tier / LiteParse / pdfplumber fallback), pages parsed, status
- Summary counts by company, doctype and conversion method
- Gaps and any permanently failed documents
- Total pages parsed per tier (for the user's LlamaCloud cost tracking)

## Hard Rules

- **Never ask for, accept or store a LlamaCloud API key.** All parsing goes through the LlamaParse connector. If the user pastes a key anyway, don't use it, and suggest they rotate it.
- **Never skip URL verification.** Every URL must come from Screener.in, BSE, or the company IR site. Do not guess or construct URLs from patterns alone without verifying they resolve.
- **Never start converting before the user confirms the scope** (Step 3); parsing spends their credits.
- **Never proceed with an empty or incomplete document list.** If a company's documents can't be found, flag it and ask the user how to proceed.
- **Always confirm the output location** before writing files.
- **Always include the research log.** It's the audit trail and tracks LlamaParse usage.
- **BSE links may return 403.** Use the local-upload route (4a) and flag persistent failures for manual follow-up.
- **For companies listed less than 10 years**, get all post-listing documents plus any pre-IPO annual reports available on BSE.
- **Never silently fall back from LlamaParse to another parser.** Always ask first (Step 7).
- **Every Markdown file must begin with the Document Information block** (Step 5), including fallback and backfilled files. A file without it is a failed conversion and must be regenerated.
