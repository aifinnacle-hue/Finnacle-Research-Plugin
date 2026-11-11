> **Curated by Vastav Parikh & Yash Master for Finnacle Shah Classes.**  
> Intellectual property of Finnacle Institute. © 2026 Finnacle Institute. All rights reserved.  
> Keep this notice intact in any copy or modified version of this file.

# Database reference — indian-equities-financials (user's own Supabase project)

## Dictionaries
- `line_items` (561 seeded): `ace_code` unique (PLC_/BSC_/CFC_/QTRC_/QTRCB_/CD_ + CALC_* for
  code-less Excel rows like Gross Profit), `label`, `statement` enum
  (pnl_annual | balance_sheet_annual | cash_flow_annual | pnl_quarterly |
  balance_sheet_quarterly | forensic_annual | company_master), `unit`, `display_order`.
- `derived_metrics` (278 seeded): `metric_code` unique with prefixes RR_/BSR_/CFR_/FOR_/FF_/PG_/BG_,
  `name`, `category`, `unit`. Codes are deterministic slugs of the Excel row labels with `_2`,`_3`
  suffixes for repeated labels within a sheet — the loader regenerates them with the identical algorithm.

## Company directory
- `companies`: `id` (unique company ID), `fincode` unique (Ace/Accord code), `name`, `isin`,
  `bse_code`, `nse_symbol`, `bloomberg_code`, `bse_scrip_name`, `sector_id`→`sectors`,
  `industry_id`→`industries`, `sub_industry`, `house`, `chairman`, `managing_director`,
  `auditor`, `credit_rating`, `preferred_basis`, `coverage_status`.
- View `v_company_directory`: company_id, fincode, name, sector, industry, subsector,
  bse_code, nse_symbol, isin, house, credit_rating, preferred_basis, coverage_status.

## Facts (all have company_id, basis consolidated|standalone, value numeric, batch_id)
- `fact_pnl_annual`, `fact_balance_sheet_annual`, `fact_cash_flow_annual`, `fact_other_annual`
  — unique (company_id, line_item_id, fiscal_year, basis).
- `fact_pnl_quarterly`, `fact_balance_sheet_quarterly`
  — unique (company_id, line_item_id, period_code, basis); also fiscal_year + fiscal_quarter.
- `fact_derived` — unique (company_id, metric_id, period_type, basis, fiscal_year, period_code);
  period_type enum fy | quarter | ttm | cum_3y | cum_5y; unused period fields default 0.

## Ops & guardrails
- `ingestion_batches`: one per file (source_file, file_hash, status, stats jsonb).
- `ingestion_alerts`: DB triggers auto-insert alerts on (a) any INSERT into
  line_items/companies/sectors/industries/derived_metrics (`new_*`, warning) and
  (b) any UPDATE that changes a stored fact value (`value_conflict`, critical, old/new in details).
  Alert workflow: status open → approved | rejected. Suppress inside a transaction with
  `set_config('app.suppress_alerts','on',true)` (bulk pre-approved loads only).
- RLS: authenticated = read-only; writes require service role.

## Useful views
`v_company_master`, `v_company_directory`, `v_pnl_annual`, `v_balance_sheet_annual`,
`v_cash_flow_annual`, `v_pnl_quarterly`, `v_balance_sheet_quarterly`,
`v_common_size_pnl` (% of Net Sales), `v_common_size_bs` (% of Total Assets),
`v_derived_metrics`, `v_open_alerts`.
