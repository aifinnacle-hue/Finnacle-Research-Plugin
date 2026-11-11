---
name: telegram-ic-report-sourcing
description: Fetch INITIATING-COVERAGE research reports for one or more companies from specified Telegram channels/groups, then convert each report to Markdown using LlamaParse (LlamaIndex). Trigger this skill whenever the user wants to pull initiating-coverage reports, IC reports, or brokerage initiation notes for a company out of Telegram groups, mentions searching Telegram channels for research reports, asks to "get the initiating coverage for [company] from my Telegram groups," or wants Telegram-sourced PDFs converted to Markdown. Also trigger for phrasings like "run the Telegram IC sourcing," "find initiation reports in [channel]," or "scrape my research channels for [company]." The skill collects the company names and the target channels, then hands the user a ready-to-run command for the bundled reusable script — it does NOT write a fresh script each time.
license: "Proprietary. © 2026 Finnacle Institute. All rights reserved. See LICENSE."
---

> **Curated by Vastav Parikh & Yash Master for Finnacle Shah Classes.**  
> Intellectual property of Finnacle Institute. © 2026 Finnacle Institute. All rights reserved.  
> Keep this notice intact in any copy or modified version of this file.

# Telegram Initiating-Coverage Report Sourcing

Pulls **initiating-coverage** research reports for specified companies out of specified Telegram channels, downloads the PDFs, and converts each to Markdown via LlamaParse. The work runs on the **user's own machine** through a single reusable script (`scripts/fetch_ic_reports.py`); changing the company or channels is just a change of command-line arguments, not a new script.

## What this skill does NOT do

- It does not log into Telegram on the user's behalf. Authentication (phone number + OTP + any 2FA) happens locally inside the script, prompted by Telethon, and entered by the user in their own terminal. Claude never handles the OTP.
- It does not embed or transmit secrets or account identifiers. The Telegram `api_id`, `api_hash` and the LlamaCloud key are all read from the user's environment variables, set once locally.

## Step 1 — Collect the two required inputs

Ask the user for:

1. **Company names.** For each, capture the display name plus any aliases the report might use (e.g. `Thyrocare` → also `Thyrocare Technologies`). Aliases improve match rate against captions and filenames.
2. **Telegram channels/groups** to search. Accept `@handle`, bare handle, or a `t.me/...` / `web.telegram.org/...` link — the script normalizes all three. The user must already be a member of each channel for their account to read it.

Optionally capture:
- **LlamaParse tier** — only if the user explicitly wants something other than the default. Default is `agentic`. Lower = `cost_effective`; higher = `agentic_plus`. Do not change the default unless the prompt says so.
- **Output folder** — default `./ic_reports`.

Confirm the company list and channel list before moving on.

## Step 2 — One-time local setup (state it, don't perform it)

The user sets two environment variables on their own machine, once. Tell them this exactly:

```
# Telegram API credentials for YOUR account. Get both from https://my.telegram.org
export TELEGRAM_API_ID="your_api_id"
export TELEGRAM_API_HASH="your_api_hash"

# LlamaCloud key for the Markdown conversion. Get it from https://cloud.llamaindex.ai
export LLAMA_CLOUD_API_KEY="llx-..."
```

Then the one-time install:

```
pip3 install telethon llama-cloud-services pdfplumber
```

The first time the script runs, Telethon prompts the user in their terminal for their phone number and the login OTP Telegram sends (and 2FA password if set). A local `.session` file is cached afterwards, so subsequent runs skip login. Deleting the `.session` file logs out.

**Why env vars and not inlining the secrets:** keeping the Telegram credentials and LlamaCloud key in the environment means they never pass through chat and never sit inside a shareable skill file. Do not inline them into the script.

## Step 3 — Deliver the script (first run only) and the command (every run)

The reusable script lives at `scripts/fetch_ic_reports.py`. On the first use in a session, copy it to the outputs directory and present it so the user has it locally. On later uses, the user already has the script — just give them the updated command.

Build the run command from the collected inputs. Each company becomes a `"Display=alias1,alias2"` token; channels are space-separated handles. Example:

```
python3 fetch_ic_reports.py \
    --companies "Thyrocare=Thyrocare,Thyrocare Technologies" \
    --channels <channel_handle_1> <channel_handle_2> \
    --tier agentic \
    --out ./ic_reports
```

Multiple companies in one run:

```
python3 fetch_ic_reports.py \
    --companies "Thyrocare=Thyrocare,Thyrocare Technologies" "Dr Lal=Dr Lal,Dr. Lal PathLabs,DLPL" \
    --channels <channel_handle_1> <channel_handle_2>
```

Omit `--tier` to use the default (`agentic`). Add it only when the user explicitly asks for `cost_effective` or `agentic_plus`.

## Step 4 — How the script identifies an initiating-coverage report

A message qualifies only if it (a) carries a document attachment, (b) matches a company alias in its caption or filename, and (c) reads as an initiation — i.e. contains a phrase like "initiating coverage," "initiation of coverage," "we initiate," or an `initiat…` stem co-occurring with "coverage." This keeps out ordinary "coverage update" or "maintain" notes. The script runs a server-side text search per alias, plus a filename scan to catch reports whose caption is generic but whose filename names the company. Reports posted to more than one channel are de-duplicated by file hash.

## Step 5 — Output

```
{out}/
├── pdfs/{Company}/{Company}_IC_{Broker|Channel}_{YYYY-MM-DD}_{msgid}.pdf
├── markdown/{Company}/{...}.md      # LlamaParse output, one per PDF
├── download_log.txt
├── conversion_log.txt
└── research_log.md                  # run summary: company, broker, channel, date, file
```

Every Markdown file begins with a Document Information block (Document Name, Company, Report Type = Initiating Coverage, Broker/Source, Telegram channel, message link, posted date, conversion tier, description) so downstream indexing and review have full provenance back to the exact Telegram message.

## Step 6 — Conversion-failure handling

The script logs every conversion to `conversion_log.txt`. If LlamaParse returns a credit/quota error (HTTP 402 or a body mentioning credit/quota/insufficient), it prints a `⚠️ LLAMAPARSE CREDITS EXHAUSTED` banner, stops further conversions, and exits cleanly so downloaded PDFs are preserved. After the user tops up at https://cloud.llamaindex.ai/billing they re-run the same command; already-converted files can be skipped or overwritten as they prefer. Individual non-credit failures (malformed PDF, timeout) are logged and skipped without aborting the run.

## Hard Rules

- **Never embed the Telegram api_id, api_hash or LlamaCloud key in this SKILL.md or in the bundled script.** All of them come from the user's environment (`TELEGRAM_API_ID`, `TELEGRAM_API_HASH`, `LLAMA_CLOUD_API_KEY`).
- **Never enter the OTP or perform the Telegram login.** It is interactive and local to the user's machine, by design.
- **Default LlamaParse tier is `agentic`.** Apply a different tier only when the prompt explicitly requests a lower or higher one.
- **Only "initiating coverage" reports.** Do not widen the match to general research notes, results updates, or rating changes unless the user asks for that explicitly.
- **The user must be a member** of each channel; flag channels the script reports it cannot access rather than guessing.
- **The script is reusable** — do not regenerate it per company. Re-deliver it only if the user has lost it; otherwise just update the command-line arguments.
