# Finnacle Research Automation

> **Curated by Vastav Parikh & Yash Master for Finnacle Shah Classes.**  
> Intellectual property of Finnacle Institute. © 2026 Finnacle Institute. All rights reserved. See [LICENSE](LICENSE).

A buy-side equity research toolkit for Indian (BSE/NSE) listed companies, by Finnacle Institute. It bundles 14 skills in three stages: sourcing the documents, analysing the business, and valuing it.

## Skills

### Sourcing
| Skill | What it does |
|---|---|
| `equity-doc-sourcing-llama` | Finds and downloads annual reports, concall transcripts and investor presentations for a company and its peers, and converts them to Markdown with LlamaParse. |
| `youtube-transcript-sourcing` | Finds management interviews, earnings-call and industry videos on chosen YouTube channels, transcribes them through HappyScribe and saves them as Markdown. |
| `valuepickr-scraper` | Generates a script that downloads full ValuePickr forum threads as clean Markdown. |
| `telegram-ic-report-sourcing` | Pulls initiating-coverage broker reports for a company from Telegram channels you are a member of, and converts them to Markdown. |
| `ace-model-loader` | Loads ACE Equity model workbooks into your own Supabase database. |

### Business analysis
| Skill | What it does |
|---|---|
| `business-model-value-chain` | Explains how the business works: product, industry chain, sizing and value chain. |
| `industry-master-sheet` | Period-flexible historical and peer comparison of financial and operating metrics. |
| `return-matrix` | Buy-side P&L, margin and capital-efficiency analysis (turnover, working capital, DuPont ROE, ROCE, ROIC). |
| `management-analysis` | Management quality, guidance credibility, capital allocation and governance scorecard. |
| `short-investment-thesis-v2` | A 5–7 page note to decide whether a company deserves a deep dive or should be avoided. |

### Valuation
| Skill | What it does |
|---|---|
| `short-dcf` | Two-approach DCF (exit multiple and perpetuity) linked to an existing forecast workbook. |
| `implied-multiple-v2` | Implied P/E or EV/EBITDA using the EVA / franchise-value framework. |
| `relative-multiples` | Peer trading-multiples sheet (EV and equity multiples, medians, base-year snapshot). |
| `exit-multiple-return` | Holding-period return at an exit multiple, with a multiple × growth sensitivity grid. |

## Setup: your own keys

This plugin ships with **no API keys, tokens or account details**. The skills that call paid or authenticated services read your own credentials from environment variables on your machine. Never paste a key into chat.

| Skill | Environment variables | Where to get them |
|---|---|---|
| `equity-doc-sourcing-llama` | `LLAMA_CLOUD_API_KEY` | https://cloud.llamaindex.ai |
| `telegram-ic-report-sourcing` | `TELEGRAM_API_ID`, `TELEGRAM_API_HASH`, `LLAMA_CLOUD_API_KEY` | https://my.telegram.org (API development tools) and https://cloud.llamaindex.ai |
| `ace-model-loader` | `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` | Your Supabase project → Project Settings → API |

Set them once in your terminal, for example on macOS/Linux:

```bash
export LLAMA_CLOUD_API_KEY="llx-..."
export TELEGRAM_API_ID="1234567"
export TELEGRAM_API_HASH="..."
```

On Windows use `setx NAME "value"` and open a new terminal. Telegram login (phone number and OTP) happens in your own terminal the first time the script runs; Claude never handles it.

LlamaParse is billed per page by LlamaIndex. Annual reports are routed to the higher-cost tier, so check your credit balance before large runs.

## Requirements and limits

- **ACE Equity** — `ace-model-loader` needs ACE Equity model exports and a Supabase database with the schema described in `skills/ace-model-loader/reference/db_schema.md`.
- **HappyScribe** — `youtube-transcript-sourcing` needs the HappyScribe connector connected in Claude, using your own HappyScribe account.
- **Screener.in** — `short-investment-thesis-v2` reads trend data from Screener.in pages.
- **Existing model** — `short-dcf`, `relative-multiples`, `implied-multiple-v2` and `exit-multiple-return` work on a company model workbook you already have.
- **Python** — the sourcing skills generate scripts that run on your own machine with Python 3 (`requests`, `pdfplumber`, `llama-cloud-services`, `telethon`, `openpyxl` as needed; each skill states its install line).
- **Research use only** — outputs are analytical aids for research and education, not investment advice.

## Suggested workflow

1. Source documents for the company and its peers (Sourcing skills).
2. Run `business-model-value-chain` → `industry-master-sheet` → `return-matrix` → `management-analysis`, or `short-investment-thesis-v2` for a quick screen.
3. Value it with `short-dcf`, `implied-multiple-v2`, `relative-multiples` and `exit-multiple-return`.
