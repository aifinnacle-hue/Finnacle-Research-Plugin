---
name: equity-doc-sourcing-llama
description: Source, download, and convert Indian equity research documents (Annual Reports, Concall Transcripts, Investor Presentations) for any BSE/NSE-listed company and its competitors, using LlamaParse for high-fidelity PDF-to-Markdown conversion. Trigger this skill whenever a user asks to download company documents or build a research library AND mentions LlamaParse, LlamaIndex, premium parsing, high-quality parsing, better table extraction, or asks for the "llama" variant of the doc-sourcing pipeline. Also trigger when the user says "use LlamaParse for [company]" or "download docs with LlamaParse" or wants cleaner Markdown output from PDFs than pdfplumber produces. For the standard pdfplumber-based pipeline, use the equity-doc-sourcing skill instead.
license: "Proprietary. © 2026 Finnacle Institute. All rights reserved. See LICENSE."
---

> **Curated by Vastav Parikh & Yash Master for Finnacle Shah Classes.**  
> Intellectual property of Finnacle Institute. © 2026 Finnacle Institute. All rights reserved.  
> Keep this notice intact in any copy or modified version of this file.

# Equity Document Sourcing Skill — LlamaParse Variant

End-to-end pipeline for acquiring Annual Reports, Concall Transcripts, and Investor Presentations for BSE/NSE-listed Indian companies. Downloads PDFs via `requests` and converts them to high-fidelity Markdown using LlamaParse (LlamaIndex).

This is the premium-parsing variant of `equity-doc-sourcing`. Use this skill when the user wants clean Markdown tables from financial statements (LlamaParse preserves table structure faithfully; pdfplumber produces flat text dumps).

## Prerequisites

- A **LlamaCloud API key** from https://cloud.llamaindex.ai (format: `llx-...`)
- Python 3.9+ on the user's machine
- One-time pip install: `pip3 install requests llama-cloud-services pdfplumber pandas`
  - `llama-cloud-services` is the current package for LlamaParse
  - `pdfplumber` is installed only for the fallback path
  - `pandas` is used for the research log

## Step 1 — Collect User Input

Ask the user:

1. **Primary company** — "What company do you want documents for?"
2. **Peers/Competitors** — "Which peer or competitor companies should I include?" (1-5 names)
3. **Years of history** — "How many years of data do you need?" (default: 10)
4. **Output location** — "Where should I save the files on your machine?" (e.g., `~/Documents/Research/Pharma`)

Do NOT proceed to URL discovery until all four inputs are confirmed.

Do NOT ask for the API key yet — that comes in Step 3, after the document list is built and the user has seen the scope of the job. This avoids the user handing over a key before they know whether they want to run the pipeline.

## Step 2 — Discover Document URLs

Identical to the base `equity-doc-sourcing` skill. For EACH company (primary + peers):

### 2a. Find the Screener.in page

Search the web for `screener.in [COMPANY NAME] consolidated` and fetch the page. From the Documents section, extract:
- All **Annual Report** links (labeled "Financial Year YYYY from bse")
- All **Concall Transcript** links (labeled "Transcript")
- All **Investor Presentation** links (labeled "PPT")

### 2b. If the page truncates

Use Claude in Chrome. Navigate to the Screener.in page and run JavaScript extraction in three passes (transcripts, PPTs, annual reports).

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

Once URLs are collected, summarize the scope for the user:
- Total documents discovered, broken down by company and doctype
- Any gaps or companies where discovery failed

## Step 3 — LlamaParse API Key (environment variable)

After URL discovery is complete and the user has seen the document scope, tell them the script reads their own LlamaCloud key from the environment, and how to set it once:

```
I've discovered {N} documents across {M} companies. Ready to generate the scraping script.
The script reads your LlamaCloud API key from the LLAMA_CLOUD_API_KEY environment variable.
If you haven't set it yet, get a key from https://cloud.llamaindex.ai and run once in your terminal:
    export LLAMA_CLOUD_API_KEY="llx-..."      (macOS/Linux)
    setx LLAMA_CLOUD_API_KEY "llx-..."        (Windows, then open a new terminal)
```

Rules:
- Do not ask the user to paste the key into chat, and never inline a key into the generated script or any file.
- The script must exit with a clear message if `LLAMA_CLOUD_API_KEY` is missing or does not start with `llx-`.

## Step 4 — Generate the Download + Convert Script

Generate a customized `download_and_convert_llama.py` that:

### 4a. Downloads PDFs via `requests`

- Iterates through the `DOCUMENTS` dictionary
- Uses a browser-like `User-Agent` header to avoid BSE 403s
- Retries failed downloads up to 3 times with exponential backoff
- Writes PDFs to `{OUTPUT_BASE}/pdfs/{company}/{doctype}/`
- Logs every download (URL, status, size, timestamp) to `download_log.txt`

### 4b. Converts PDFs via LlamaParse with doctype-based tier routing

| Doctype | LlamaParse tier | Rationale |
|---|---|---|
| Annual Report | `agentic_plus` | Complex tables, financial statements, multi-column layouts |
| Investor Presentation | `agentic` | Charts and graphics, but simpler than ARs |
| Concall Transcript | `cost_effective` | Prose-heavy, minimal structure |

The script must use the `llama-cloud-services` SDK:

```python
import os
from llama_cloud_services import LlamaParse

parser = LlamaParse(
    api_key=os.environ["LLAMA_CLOUD_API_KEY"],  # read from the user's environment, never inlined
    result_type="markdown",
    tier=TIER_FOR_DOCTYPE[doctype],
    verbose=False,
    language="en",
)
docs = parser.load_data(pdf_path)
markdown_text = "\n\n".join(d.text for d in docs)
```

Write Markdown output to `{OUTPUT_BASE}/markdown/{company}/{doctype}/{filename}.md`. Every output file must begin with the Document Information block defined in Step 5.

### 4c. Handle LlamaParse failures gracefully

For each PDF, wrap the parse call in try/except. On failure:

- Capture the error type (credit exhaustion, malformed PDF, timeout, rate limit, network)
- Log to `conversion_log.txt` with: filename, error type, error message, timestamp
- **Do NOT automatically fall back to pdfplumber.** The script continues to the next PDF and leaves failures for the user to review.

Detect credit exhaustion explicitly — LlamaCloud returns HTTP 402 or a response body containing "credit", "quota", or "insufficient". When detected, the script must:
- Print a prominent banner: `⚠️  LLAMAPARSE CREDITS EXHAUSTED — remaining PDFs skipped`
- Stop attempting further LlamaParse calls (but continue downloading)
- Exit cleanly so the user can decide next steps

### 4d. Naming conventions

| Document type | Pattern | Example |
|---|---|---|
| Annual Report | `{Company}_AR_FY{YY}.pdf` / `.md` | `Thyrocare_AR_FY25.pdf` |
| Concall Transcript | `{Company}_CC_Q{N}FY{YY}.pdf` / `.md` | `DrLal_CC_Q4FY25.pdf` |
| Investor Presentation | `{Company}_PPT_Q{N}FY{YY}.pdf` / `.md` | `Metro_PPT_Q2FY26.pdf` |

Use short company names (e.g., Thyrocare, DrLal, Metro, Apollo, MaxHealth, Fortis, Narayana, Syngene, Laurus, Divis).

### 4e. Present the script to the user

Save `download_and_convert_llama.py` to `/mnt/user-data/outputs/` and present it:

```
1. Download the script
2. Open your terminal
3. One-time install (skip if done):
     pip3 install requests llama-cloud-services pdfplumber pandas
4. Run:
     cd ~/Downloads
     python3 download_and_convert_llama.py
5. Expected runtime: 30-60 minutes (LlamaParse is slower than pdfplumber but much higher quality)
```

## Step 5 — Mandatory Document Metadata Block

Every Markdown file produced by the script — whether converted via LlamaParse or the pdfplumber fallback — MUST begin with a Document Information block. This is non-negotiable. The block gives downstream analysis (LLMs, indexing, manual review) unambiguous context about what the file contains.

### 5a. Required fields

The block must include these four fields, in this order:

| Field | Definition | Source |
|---|---|---|
| **Document Name** | The canonical filename without extension | Derived from the naming convention in 4d (e.g., `Thyrocare_AR_FY25`) |
| **Period Covered** | The fiscal period the document reports on, expressed as both short form and explicit date range | Parsed from the filename suffix |
| **Upload Date** | The date the document was originally filed / published by the company | PDF `CreationDate` metadata (primary), filename period as proxy (secondary), or `Unknown` (last resort) — see 5d |
| **Description** | A 1-2 sentence description of the document's contents | Template-based by doctype — see 5c |

### 5b. Exact Markdown format

The script MUST emit this block verbatim at the top of every `.md` file, before any parsed content:

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

Use these templates (substitute `{Company}` and `{Period}` at generation time):

- **Annual Report** → `Annual Report of {Company} for {Period}. Contains audited consolidated and standalone financial statements, management discussion and analysis, director's report, auditor's report, and corporate governance disclosures.`

- **Concall Transcript** → `Earnings conference call transcript of {Company} for {Period}. Contains management's prepared remarks on quarterly financial and operational performance, followed by a Q&A session with sell-side analysts and institutional investors.`

- **Investor Presentation** → `Investor presentation of {Company} for {Period}. Summarises business performance, financial highlights, segmental metrics, strategic initiatives, and forward-looking commentary shared with the investor community.`

### 5d. Upload Date extraction logic

The script should populate Upload Date using this cascade:

1. **Primary — PDF `CreationDate` metadata.** Extract using `pdfplumber` (already a dependency):
   ```python
   with pdfplumber.open(pdf_path) as pdf:
       raw = pdf.metadata.get("CreationDate")  # e.g., "D:20240715143022+05'30'"
   ```
   Parse the `D:YYYYMMDD...` format into `DD Month YYYY` (e.g., `15 July 2024`).

2. **Secondary — filename period as proxy.** If PDF metadata is missing or malformed, use the period suffix to infer a plausible filing window based on typical Indian filing timelines (AR → July–September following FY end; Concall → within 60 days of quarter end; IP → around concall date). Append `(inferred from period)` to the value so it's flagged.

3. **Last resort — `Unknown`.** If neither source yields a date, write `Unknown` literally. Do not guess.

### 5e. Period formatting

Expand the filename period suffix into a human-readable range:

| Filename suffix | Period Covered value |
|---|---|
| `FY25` | `FY25 (1 April 2024 – 31 March 2025)` |
| `Q1FY26` | `Q1 FY26 (April – June 2025)` |
| `Q2FY26` | `Q2 FY26 (July – September 2025)` |
| `Q3FY26` | `Q3 FY26 (October – December 2025)` |
| `Q4FY25` | `Q4 FY25 (January – March 2025)` |

### 5f. Backfilling existing files

If the user has already run a conversion (via this skill or the base `equity-doc-sourcing` skill) and wants to retrofit the metadata block onto existing files, generate a standalone `backfill_metadata.py` script that:

- Walks the existing `markdown/` directory tree
- For each `.md` file, checks whether a `## Document Information` block already exists and skips if yes
- Looks up the corresponding PDF in the `pdfs/` tree to extract `CreationDate`
- Derives doctype, company, and period from the filename
- Prepends the metadata block using the rules above
- Logs each file as `UPDATED`, `SKIPPED (already has block)`, or `FAILED (reason)` to `backfill_log.txt`

Do not generate this script unless the user explicitly asks for a backfill.

## Step 6 — Fallback Protocol (invoked when user reports failures)

After the user runs the script and reports results, check `conversion_log.txt`. If any conversions failed:

### 6a. Classify the failures

- **Credit exhaustion** — one or more PDFs failed with HTTP 402 / quota errors
- **Individual PDF failures** — specific PDFs failed for other reasons (malformed, timeout, etc.) while others succeeded

### 6b. Ask the user how to proceed

Present the failure summary and ask — **do not assume**:

```
{N} PDFs failed LlamaParse conversion. Here's the breakdown:

  - Credit exhaustion: {X} PDFs (your LlamaCloud credits ran out)
  - Other failures: {Y} PDFs (malformed, timeout, etc.)

How would you like to proceed?

  [A] Fall back to pdfplumber for all failed PDFs (free, lower quality —
      tables will be flattened to plain text)
  [B] Top up my LlamaCloud credits and resume with LlamaParse
      (I'll pause; you top up at https://cloud.llamaindex.ai/billing,
      then say "resume" and I'll generate a retry script for just the
      failed PDFs)
  [C] Mix — fall back to pdfplumber for the non-credit failures (B won't
      fix those anyway) and top up + resume for the credit-exhausted ones
```

### 6c. Execute the user's choice

- **Option A (pdfplumber fallback):** Generate `fallback_pdfplumber.py` that reads the failed PDF filenames from `conversion_log.txt` and converts them using pdfplumber. Mark those Markdown files with a header line: `<!-- CONVERTED WITH PDFPLUMBER FALLBACK - TABLES MAY BE FLATTENED -->` so the user can see at a glance which files have degraded quality. The Document Information block from Step 5 is still required on these files.

- **Option B (top up and resume):** After the user confirms they've topped up, generate `retry_llama.py` — a stripped-down version of the main script that only processes PDFs listed in `conversion_log.txt`. Same API key, same tier routing.

- **Option C (mix):** Generate both scripts. The pdfplumber one handles non-credit failures; the retry-llama one handles credit-exhausted PDFs after top-up.

### 6d. Never silently degrade

Do not automatically convert with pdfplumber without asking. The quality difference matters for financial statements, and the user should make the call explicitly.

## Step 7 — Post-Download Organization

After a successful run (including any fallback), verify the output:

```bash
find {OUTPUT_BASE} -name "*.pdf" | wc -l
find {OUTPUT_BASE} -name "*.md" | wc -l
```

Expected folder structure:

```
{OUTPUT_BASE}/
├── pdfs/
│   ├── {company1}/
│   │   ├── annual_reports/
│   │   ├── concalls/
│   │   └── presentations/
│   └── {company2}/
│       └── ...
├── markdown/
│   ├── {company1}/
│   │   ├── annual_reports/
│   │   ├── concalls/
│   │   └── presentations/
│   └── {company2}/
│       └── ...
├── download_log.txt
├── conversion_log.txt
└── research_log.md
```

## Step 8 — Generate Research Log

The script auto-generates `research_log.md` at the output root, containing:

- Date of acquisition
- Company names and BSE codes
- Complete list of every document: filename, source URL, download status, conversion method (LlamaParse tier / pdfplumber fallback), file size
- Summary counts by company, doctype, and conversion method
- List of gaps and any permanently-failed documents
- Total LlamaParse pages consumed (for cost tracking)

## Hard Rules

- **Never skip URL verification.** Every URL must come from Screener.in, BSE, or the company IR site. Do not guess or construct URLs from patterns alone without verifying they resolve.
- **Never embed the API key in `SKILL.md`.** The key is collected from the user in chat at generation time (Step 3) and inlined into the generated script only.
- **Never proceed to script generation with an empty or incomplete DOCUMENTS dictionary.** If a company's documents can't be found, flag it explicitly and ask the user how to proceed.
- **Always confirm the output path** before generating the script.
- **Always include the research log.** It's the audit trail and tracks LlamaParse usage for cost reporting.
- **BSE links may return 403.** The script handles retries, but flag persistent failures for manual follow-up.
- **For companies listed less than 10 years**, get all post-listing documents plus any pre-IPO annual reports available on BSE.
- **Never silently fall back from LlamaParse to pdfplumber.** Always ask the user first when conversions fail (Step 6). This is the core behavioral difference vs. the base skill.
- **Every Markdown file must begin with the Document Information block** defined in Step 5. This applies to LlamaParse output, pdfplumber fallback output, and backfilled files. No exceptions. A file without the block is considered a failed conversion and must be regenerated.
- **Treat the generated script as sensitive** (it contains the API key). Remind the user once at delivery time not to commit or share it. Do not remind repeatedly.
- **Tier routing is default, not mandatory.** If the user wants everything on `agentic_plus` (for maximum fidelity) or everything on `cost_effective` (for minimum cost), respect that override and apply it to the entire run.
