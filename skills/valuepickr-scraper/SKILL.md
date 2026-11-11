---
name: valuepickr-scraper
description: Scrape full discussion threads from ValuePickr (forum.valuepickr.com) and convert them to clean Markdown files for equity research. Trigger this skill whenever a user provides a ValuePickr URL, mentions scraping or downloading a ValuePickr thread, says "get the ValuePickr discussion on [company]", references forum.valuepickr.com, or asks to collect community research/discussion data from ValuePickr. Also trigger when the user asks to add more ValuePickr threads to an existing scraping job, or wants to build a research library from investor forum discussions. This skill generates a ready-to-run Python script that the user executes locally.
license: "Proprietary. © 2026 Finnacle Institute. All rights reserved. See LICENSE."
---

> **Curated by Vastav Parikh & Yash Master for Finnacle Shah Classes.**  
> Intellectual property of Finnacle Institute. © 2026 Finnacle Institute. All rights reserved.  
> Keep this notice intact in any copy or modified version of this file.

# ValuePickr Data Scraper

Scrapes complete discussion threads from ValuePickr (Discourse-based forum) into clean, timestamped Markdown files. Each post is preserved with username, date, like count, and full content — ready for research analysis.

## How It Works

ValuePickr runs on Discourse, which exposes a JSON API. The scraper uses `/t/{topic_id}.json` and `/t/{topic_id}/posts.json` endpoints to pull structured data — no HTML scraping needed. This makes output clean and reliable.

---

## Step 1 — Collect User Input

The user must provide:

1. **Thread URL(s)** — One or more ValuePickr thread URLs (required). Accept URLs in any format:
   - `https://forum.valuepickr.com/t/some-thread/12345`
   - `https://forum.valuepickr.com/t/some-thread/12345/67` (with post number — ignore the post number, scrape the full thread)
   - Bare thread IDs if the user provides them (e.g., "topic 12345")

2. **Output location** — Where to save files on the user's machine. Default: `~/Documents/Research/ValuePickr`. Ask only if the user hasn't specified a preference. If the user has a known research directory from prior context, use that.

Do NOT generate the script until at least one valid URL is confirmed.

If the user provides URLs across multiple messages, accumulate them into a single script. Always confirm the final list before generating.

---

## Step 2 — Validate URLs

For each URL provided:

1. Extract the `topic_id` using regex: `/t/[^/]+/(\d+)`
2. Verify the URL points to `forum.valuepickr.com`
3. Strip any trailing post number — the script always scrapes the **entire thread**

If a URL cannot be parsed, flag it immediately and ask the user to verify.

---

## Step 3 — Generate the Python Script

Read the template script:

```
Read scripts/valuepickr_template.py for the complete template
```

Generate a customized `valuepickr_scraper.py` by:

1. Populating `THREAD_URLS` with all validated URLs
2. Setting `OUTPUT_DIR` to the user's specified output path
3. Leaving all other configuration at defaults unless the user requests changes

### Output format

Each thread produces one Markdown file with this structure:

```markdown
# {Thread Title}

**Source:** https://forum.valuepickr.com/t/{topic_id}
**Total posts scraped:** {count} / {expected}
**Scraped on:** {YYYY-MM-DD HH:MM}

---

### Post #1 — @{username}
*{DD Mon YYYY, HH:MM AM/PM}* · {N} likes

{Post content converted from HTML to Markdown}

---

### Post #2 — @{username}
...
```

### Naming convention

Files are named by sanitizing the thread title:
- Replace special characters with nothing
- Replace spaces with underscores
- Truncate to 80 characters
- Append `.md`

Example: `Cochin_Shipyard__No_more_Cheap.md`

---

## Step 4 — Present Script to User

Save `valuepickr_scraper.py` to the outputs directory and present it with these instructions:

**First-time setup (one-time only):**
```
pip3 install requests
```

**Run the script:**
```
cd ~/Downloads
python3 valuepickr_scraper.py
```

Tell the user:
- The script fetches posts in chunks of 20 with a 1.5-second delay between requests to be polite to the server
- Large threads (200+ posts) may take a few minutes
- A summary table prints at the end showing OK/PARTIAL/FAILED status per thread
- Files land in the configured output directory

---

## Step 5 — Post-Scrape Verification

After the user confirms the script ran successfully:

1. Ask if all threads show **OK** status in the summary
2. If any show **PARTIAL**, the Discourse API may have rate-limited — suggest the user wait a minute and re-run. The script is idempotent and will overwrite existing files.
3. If any show **FAILED**, check:
   - Is the URL correct?
   - Is the thread private or deleted?
   - Is the forum temporarily down?
4. Offer to generate a retry script with just the failed URLs

---

## Hard Rules

- **Never guess thread URLs.** Only use URLs explicitly provided by the user. Do not search for or construct ValuePickr URLs.
- **Always scrape full threads.** Even if the user provides a URL with a specific post number (e.g., `/137`), the script scrapes all posts in the thread.
- **Respect rate limits.** Maintain at least 1.5 seconds between API requests. Do not reduce this.
- **Preserve all post metadata.** Every post must include: post number, username, timestamp, like count, and full content.
- **HTML to Markdown conversion must be clean.** Convert `<strong>` → `**`, `<em>` → `*`, `<a>` → `[]()`, `<blockquote>` → `>`, `<li>` → `-`, headings, images. Strip all remaining HTML tags.
- **Always confirm output path** before generating the script.
- **One script per session.** If the user adds URLs incrementally, regenerate a single updated script — do not create multiple scripts.
