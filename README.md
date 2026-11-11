# Finnacle Research Automation

> **Curated by Vastav Parikh & Yash Master for Finnacle Shah Classes.**  
> Intellectual property of Finnacle Institute. © 2026 Finnacle Institute. All rights reserved. See [LICENSE](LICENSE).

A buy-side equity research toolkit for Indian (BSE/NSE) listed companies, by Finnacle Institute. It bundles 14 skills in three stages: sourcing the documents, analysing the business, and valuing it.

## Skills

### Sourcing
| Skill | What it does |
|---|---|
| `equity-doc-sourcing-llama` | Finds and downloads annual reports, concall transcripts and investor presentations for a company and its peers, and converts them to Markdown through the LlamaParse connector. |
| `youtube-transcript-sourcing` | Finds management interviews, earnings-call and industry videos on chosen YouTube channels, transcribes them through HappyScribe and saves them as Markdown. |
| `valuepickr-scraper` | Generates a script that downloads full ValuePickr forum threads as clean Markdown. |
| `telegram-ic-report-sourcing` | Finds initiating-coverage broker reports for a company in your own Telegram Desktop channel exports, and converts them to Markdown through the LlamaParse connector. |
| `ace-model-loader` | Loads ACE Equity model workbooks into your own Supabase database through the Supabase connector. |

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

## Setup: connectors, not keys

This plugin ships with **no API keys, tokens or account details**, and no skill asks for one or reads one from your machine. Skills that use an outside service work through a Claude connector that you connect and sign in to yourself (Settings → Connectors), or through an export you make yourself.

| Skill | What you need |
|---|---|
| `equity-doc-sourcing-llama` | The **LlamaParse** connector, signed in to your LlamaCloud account |
| `telegram-ic-report-sourcing` | **Telegram Desktop**, to export the channels you belong to ("Export chat history"), plus the **LlamaParse** connector |
| `ace-model-loader` | The **Supabase** connector, signed in to the Supabase account that owns your database (not in read-only mode) |
| `youtube-transcript-sourcing` | The **HappyScribe** connector |

If a connector isn't connected, the skill stops and tells you which one to connect. Never paste a key into chat.

LlamaParse is billed per page by LlamaIndex to your own account. Annual reports are routed to the higher-cost tier, and each skill confirms the document list with you before it parses anything.

## Third-party services and what they receive

Finnacle Institute runs no server: nothing is sent to or kept by Finnacle. Some skills send data to the services below, always through a connector signed in to **your own** account.

| Service | Skills | What is sent |
|---|---|---|
| LlamaCloud (LlamaParse) | `equity-doc-sourcing-llama`, `telegram-ic-report-sourcing` | Public company documents (annual reports, concall transcripts, presentations, broker reports) uploaded for PDF-to-Markdown conversion |
| HappyScribe | `youtube-transcript-sourcing` | Links to public YouTube videos, for transcription |
| Telegram | `telegram-ic-report-sourcing` | Nothing. You export channels yourself in Telegram Desktop and give Claude the export |
| Supabase | `ace-model-loader` | Company financial data from your ACE Equity models, written to your own Supabase project through the Supabase connector |

Other skills only read public pages (BSE, NSE, Screener.in, ValuePickr, YouTube, company websites) and send no user data to them. No skill collects personal data.

## Requirements and limits

- **ACE Equity** — `ace-model-loader` needs ACE Equity model exports and a Supabase database with the schema described in `skills/ace-model-loader/reference/db_schema.md`.
- **HappyScribe** — `youtube-transcript-sourcing` needs the HappyScribe connector connected in Claude, using your own HappyScribe account.
- **Screener.in** — `short-investment-thesis-v2` reads trend data from Screener.in pages.
- **Existing model** — `short-dcf`, `relative-multiples`, `implied-multiple-v2` and `exit-multiple-return` work on a company model workbook you already have.
- **Python** — `ace-model-loader` and `relative-multiples` run bundled Python scripts in Claude's workspace (`openpyxl`); `valuepickr-scraper` generates a script you run on your own machine. None of them reads credentials.
- **Research use only** — outputs are analytical aids for research and education, not investment advice.

## Suggested workflow

1. Source documents for the company and its peers (Sourcing skills).
2. Run `business-model-value-chain` → `industry-master-sheet` → `return-matrix` → `management-analysis`, or `short-investment-thesis-v2` for a quick screen.
3. Value it with `short-dcf`, `implied-multiple-v2`, `relative-multiples` and `exit-multiple-return`.
