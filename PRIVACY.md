# Privacy Policy — Finnacle Research Automation

Last updated: 11 November 2026

This policy covers the Finnacle Research Automation plugin for Claude, published by Finnacle Institute.

## What Finnacle Institute collects

Nothing. The plugin is a set of instructions (skills) and helper scripts that run inside your own Claude session and on your own machine. Finnacle Institute operates no server, receives no data from the plugin, and keeps no logs, analytics or copies of your work.

## Personal data

The plugin is built to work on public company information (annual reports, concall transcripts, investor presentations, filings and financial models). It does not ask for, read or store personal data such as names, email addresses or postal addresses.

## Your keys and logins

Skills that use a paid or authenticated service read your own key from your own machine and use it only to call that service. Keys are never sent to Finnacle Institute and are never written into chat, files the plugin creates, or this repository. Your Telegram login (phone number and one-time code) is entered by you in your own terminal.

## Third-party services

Some skills send data to the services below, always through your own account. Each service handles that data under its own privacy policy and retention rules.

| Service | Skills | What is sent |
|---|---|---|
| LlamaCloud (LlamaParse) | `equity-doc-sourcing-llama`, `telegram-ic-report-sourcing` | Public company documents and broker reports, for PDF-to-Markdown conversion |
| HappyScribe | `youtube-transcript-sourcing` | Links to public YouTube videos, for transcription |
| Telegram | `telegram-ic-report-sourcing` | Your login, to read channels you already belong to |
| Supabase | `ace-model-loader` | Company financial data from your ACE Equity models, written to your own Supabase project |

Other skills only read public web pages (BSE, NSE, Screener.in, ValuePickr, YouTube, company websites) and send no user data to them.

## Children

The plugin is intended for adults (18+) doing financial research and study.

## Changes and contact

Changes to this policy are published in this repository. Questions can be raised as an issue at https://github.com/aifinnacle-hue/Finnacle-Research-Plugin/issues.
