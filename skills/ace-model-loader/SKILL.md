---
name: ace-model-loader
description: Load Ace Equity financial model Excel files (named like "CompanyName_Ace Model.xlsx") into the indian-equities-financials Supabase database. Trigger whenever the user uploads one or more Ace model workbooks and asks to "load into the database", "ingest these models", "fill the DB", "add these companies", "run the loader", or points to a folder of Ace models to ingest. Parses company profile (sector, industry, BSE and NSE codes into the company directory), annual P&L, balance sheet and cash flow, quarterly P&L and BS, forensic datapoints, and derived ratio, glance and fund-flow sheets; upserts everything idempotently; and stops for user approval whenever a NEW line item, metric, sector, industry or company would be added to the dictionaries.
license: "Proprietary. © 2026 Finnacle Institute. All rights reserved. See LICENSE."
---

> **Curated by Vastav Parikh & Yash Master for Finnacle Shah Classes.**  
> Intellectual property of Finnacle Institute. © 2026 Finnacle Institute. All rights reserved.  
> Keep this notice intact in any copy or modified version of this file.

# Ace Model → Supabase Loader

Loads Ace Equity model workbooks into the user's own Supabase project (referred to below as
**indian-equities-financials**; the project URL comes from the user's `SUPABASE_URL`).

The database schema is documented in `reference/db_schema.md`. Read it if you need
table/column details. The single entry point is `scripts/ace_loader.py`.

## Credentials (required for writing)

The script writes via the Supabase REST API using the **service role key**:

- Env vars: `SUPABASE_URL=https://<your-project-ref>.supabase.co` and
  `SUPABASE_SERVICE_ROLE_KEY=<your-service-role-key>`, or pass `--env-file path/to/.env`.
- Look for a `.env` or `supabase.env` in the working folder first. If no key is
  available, tell the user to set it in their own environment or `.env` file
  (Supabase Dashboard → Project Settings → API Keys → service_role) rather than
  pasting it into chat. Never print, store or write the key into any file.
- Without credentials only `--dry-run` (offline parse) works.

Dependencies: `pip install openpyxl requests --break-system-packages`.

## Workflow — ALWAYS in this order

1. **Collect files.** Accept uploaded .xlsx files or a folder path
   (`--folder DIR` picks up every `*.xlsx`). Only Ace model workbooks qualify
   (they contain sheets like `P&L - Ace`, `BS - Ace`, `Company Name Input`).

2. **Dry run first.**
   ```
   python3 scripts/ace_loader.py --env-file .env --dry-run FILE1.xlsx FILE2.xlsx ...
   ```
   This parses everything and diffs against the DB dictionaries. Review the
   `--- DIFF vs dictionary ---` block.

3. **Approval gate (mandatory).** If the diff shows any *new line items, new
   metrics, new sectors, or new industries*: **STOP and show the user the exact
   list** (use AskUserQuestion). These are rows that would be added to shared
   dictionary tables and affect all companies. Only after explicit approval,
   re-run with `--approve-new`. New *companies* are expected and do not need
   pre-approval, but mention them.

4. **Load.**
   ```
   python3 scripts/ace_loader.py --env-file .env [--approve-new] FILE1.xlsx ...
   ```
   The script is idempotent: re-running upserts, and files already loaded
   (same SHA-256) are skipped unless `--force`.

5. **Report.** Relay the per-company row counts and, critically, any
   **OPEN ALERTS** printed at the end (`new_company` audit alerts and any
   `value_conflict` alerts, which mean a stored value changed vs a previous
   load — surface those to the user verbatim and ask how to proceed).

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
201706 = quarter ended Jun-2017 (Q1 FY2018). Zeros are stored as-is.

## Rules

- NEVER hand-edit or "fix" parsed values; load exactly what the file says.
- NEVER bypass the approval gate by defaulting to `--approve-new`.
- One batch row per file is written to `ingestion_batches`; failures leave the
  batch `in_progress` — report and investigate, don't silently retry.
- If a workbook is missing expected sheets or the fincode can't be resolved,
  skip that file, tell the user, and continue with the rest.
- Query `v_open_alerts` / `v_company_directory` for post-load review.
