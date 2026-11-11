---
name: ace-model-loader
description: "Load Ace Equity financial model Excel files (named like \"CompanyName_Ace Model.xlsx\") into the user's indian-equities-financials Supabase database through the Supabase connector. Trigger whenever the user uploads one or more Ace model workbooks and asks to \"load into the database\", \"ingest these models\", \"fill the DB\", \"add these companies\", \"run the loader\", or points to a folder of Ace models to ingest. Parses company profile (sector, industry, BSE and NSE codes into the company directory), annual P&L, balance sheet and cash flow, quarterly P&L and BS, forensic datapoints, and derived ratio, glance and fund-flow sheets; upserts everything idempotently; and stops for user approval whenever a NEW line item, metric, sector or industry would be added to the dictionaries."
license: "Proprietary. © 2026 Finnacle Institute. All rights reserved. See LICENSE."
---

> **Curated by Vastav Parikh & Yash Master for Finnacle Shah Classes.**  
> Intellectual property of Finnacle Institute. © 2026 Finnacle Institute. All rights reserved.  
> Keep this notice intact in any copy or modified version of this file.

# Ace Model → Supabase Loader (Supabase connector)

Loads Ace Equity model workbooks into the user's own Supabase project (referred to below as
**indian-equities-financials**). All database access goes through the **Supabase connector**,
which carries the user's own Supabase sign-in. This skill never asks for, reads or stores a
Supabase key, URL, password or `.env` file.

The database schema is documented in `reference/db_schema.md`. The bundled script
`scripts/ace_loader.py` only parses workbooks and writes `.sql` files; it never connects to
a database. Claude runs those files through the connector.

## Step 0 — Access check (before anything else)

1. Confirm the Supabase connector is available in this session (its tools include
   `list_projects` and `execute_sql`). If it is not, stop and ask the user to connect the
   **Supabase** connector in Claude (Settings → Connectors) and sign in with the Supabase
   account that owns the database, then try again. Do not offer any key-based alternative.
2. Call `list_projects` and pick the project that holds the indian-equities-financials schema.
   If more than one project could be it, ask the user which one. Use that `project_id` for
   every `execute_sql` call below.
3. Confirm the connector can write: the connector must not be in read-only mode. If the first
   write is refused for that reason, tell the user to turn off read-only mode for the Supabase
   connector and stop.

Dependency for the parser: `pip install openpyxl`.

## Workflow — ALWAYS in this order

Use a fresh working folder for each run, for example `ace_run/`.

1. **Collect files.** Accept uploaded .xlsx files or a folder (`--folder DIR` picks up every
   `*.xlsx`). Only Ace model workbooks qualify (they contain sheets like `P&L - Ace`,
   `BS - Ace`, `Company Name Input`).

2. **Parse.**
   ```
   python3 scripts/ace_loader.py parse FILE1.xlsx FILE2.xlsx ... --out ace_run
   ```
   Writes `ace_run/parsed/*.json`, `ace_run/codes.tsv` (code → label, statement) and
   `ace_run/01_check.sql`. Files that fail to parse are skipped with a message; tell the user
   and continue with the rest.

3. **Check against the database (read-only).** Read `ace_run/01_check.sql` and pass its full
   text, unchanged, as the `query` of `execute_sql`. Save the returned rows to
   `ace_run/check_result.json` as a JSON list of `{"kind": ..., "key": ...}` (write `[]` if no
   rows came back). Kinds: `new_line_item`, `new_metric`, `new_sector`, `new_industry`,
   `new_company`, `already_loaded`.

4. **Approval gate (mandatory).** If the check shows any *new line items, new metrics, new
   sectors or new industries*: **STOP and show the user the exact list** with labels (look the
   codes up in `codes.tsv`), using AskUserQuestion. These rows would be added to shared
   dictionary tables and affect all companies. Only after explicit approval continue with
   `--approve-new`. New *companies* are expected and need no pre-approval, but mention them.
   Files reported as `already_loaded` are skipped automatically; tell the user which ones.

5. **Build the load files.**
   ```
   python3 scripts/ace_loader.py sql ace_run [--approve-new]
   ```
   Without `--approve-new` the script exits with code 2 if the check found new dictionary
   entries. It writes `RUN_ORDER.txt` and these files:
   - `10_dictionary.sql`: the approved new dictionary rows, and marks their auto-alerts approved
   - per workbook: `20_<company>_00_header.sql` (batch row + company directory upsert),
     numbered data files (each one idempotent upsert of up to ~30,000 characters), and
     `20_<company>_99_finish.sql` (marks the batch completed and returns its row counts)
   - `30_alerts.sql`: open alerts raised since the files were built

6. **Load.** Run every file listed in `RUN_ORDER.txt`, in that order, one `execute_sql` call
   per file, passing the file's full text unchanged. Never edit, merge, shorten or retype the
   SQL. Each data file returns `rows_written`; the finish file returns the batch's stats.
   If a call fails, stop, report the file name and error, and do not continue with that
   company's remaining files. Every file is idempotent, so after fixing the cause you can
   re-run from the failed file.

7. **Report.** Relay the per-company stats from each finish file and, critically, every row
   returned by `30_alerts.sql`: `new_company` alerts and any `value_conflict` alerts (a stored
   value changed vs a previous load). Show `value_conflict` alerts to the user verbatim and
   ask how to proceed.

Size note: every byte of SQL passes through the conversation, so a large workbook can take
several data files. Load one or a few workbooks per run rather than a whole folder at once,
and tell the user how many files a run involves before starting step 6.

## What gets loaded where

| Workbook sheet | Target |
|---|---|
| Company Name Input + General | `companies` (directory: sector, industry, subsector, BSE/NSE/ISIN, management) + `sectors`/`industries` |
| P&L - Ace / BS - Ace / Cash Flow - Ace | `fact_pnl_annual` / `fact_balance_sheet_annual` / `fact_cash_flow_annual` |
| Qtrly P&L / Qtrly BS (YYYYMM columns only; annual-total columns skipped) | `fact_pnl_quarterly` / `fact_balance_sheet_quarterly` |
| Forensic - Ace (codes routed by dictionary statement; CSR/employees/RPT → other) | `fact_other_annual` (or main fact tables) |
| Return/BS/CF Ratios, Forensics, P&L/BS Glance, Fund Flow | `fact_derived` (period_type `fy`, `cum_3y`, `cum_5y`) |
| Rolling Return Ratios / Rolling P&L Glance | `fact_derived` with period_type `ttm` |
| Common Size / Common Sizing | NOT loaded — DB views `v_common_size_pnl` / `v_common_size_bs` compute these live |
| Universe / Co. | ignored (reference sheet / leftover) |

Conventions: values in ₹ crore; `basis` from the workbook's Type field
(consolidated/standalone); fiscal_year 2018 = FY ending Mar-2018; period_code
201706 = quarter ended Jun-2017 (Q1 FY2018). Zeros are stored as-is. Where a Forensic - Ace
value and a statement-sheet value exist for the same line item and year, the forensic value
is the one loaded.

## Rules

- NEVER ask the user for a Supabase key, service-role key, database password, connection
  string or `.env` file, and never read one from their machine. The connector is the only
  route to the database.
- NEVER hand-edit or "fix" parsed values or the generated SQL; load exactly what the file says.
- NEVER bypass the approval gate by defaulting to `--approve-new`.
- One batch row per file is written to `ingestion_batches`; a failure leaves the batch
  `in_progress` — report and investigate, don't silently retry.
- If a workbook is missing expected sheets or the fincode can't be resolved, skip that file,
  tell the user, and continue with the rest.
- Query `v_open_alerts` / `v_company_directory` through `execute_sql` for post-load review.
