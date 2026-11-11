---
name: youtube-transcript-sourcing
description: Extract management discussions, earnings calls, and industry deep-dive videos from specific YouTube channels, transcribe them via HappyScribe, and convert to Markdown files for equity research. Trigger this skill whenever a user asks to find YouTube videos about a company or industry, transcribe YouTube content, get management interviews from YouTube, source video transcripts for research, or says "get YouTube transcripts for [company]" or "find diagnostics videos on YouTube." Also trigger when the user mentions YouTube channels in the context of equity research, wants to build a video transcript library, or asks to transcribe investor presentations or earnings discussions from YouTube. This skill restricts searches to user-approved YouTube channels only — it never browses the full YouTube universe.
license: "Proprietary. © 2026 Finnacle Institute. All rights reserved. See LICENSE."
---

> **Curated by Vastav Parikh & Yash Master for Finnacle Shah Classes.**  
> Intellectual property of Finnacle Institute. © 2026 Finnacle Institute. All rights reserved.  
> Keep this notice intact in any copy or modified version of this file.

# YouTube Transcript Sourcing Skill

End-to-end pipeline for discovering relevant equity research videos on pre-approved YouTube channels, transcribing them via HappyScribe MCP, and delivering clean Markdown files organized by company.

## Prerequisites

- **Claude in Chrome** — Required for YouTube channel search (YouTube loads content dynamically via JavaScript; web_search and web_fetch cannot reliably extract video URLs from channel pages)
- **HappyScribe MCP connector** — Required for transcription. Must be connected in Claude.ai settings.
- **Approved YouTube channels** — The user must provide specific channel URLs. This skill NEVER searches the full YouTube universe.

---

## Step 1 — Collect User Input

Ask the user:

1. **Primary company or industry** — "What company or industry sector are you researching?"
2. **Peer companies** — "Any peer/competitor companies to include in the search?" (helps build search queries)
3. **YouTube channels** — "Which YouTube channels should I search?" (require at least one `youtube.com/@handle` URL)
4. **Search terms** — Confirm or refine the search keywords (auto-generated from company/industry + peers)

If the user has previously provided channels in the conversation, use those. Do NOT proceed without at least one confirmed YouTube channel URL.

### Default Channel Registry

If the user is working within the Indian equity research context, suggest these channels (but always confirm):

```
Read references/channel_registry.md for the maintained list of approved channels by sector
```

---

## Step 2 — Discover Videos via Claude in Chrome

This step REQUIRES Claude in Chrome. If it is not connected, ask the user to connect it and retry.

### 2a. Get browser context

```
Call: Claude in Chrome:tabs_context_mcp (createIfEmpty: true)
→ Returns tabId for use in subsequent steps
```

### 2b. For EACH YouTube channel, search for relevant videos

Navigate to the channel's search page with appropriate keywords:

```
Call: Claude in Chrome:navigate
→ URL: https://www.youtube.com/@{CHANNEL_HANDLE}/search?query={SEARCH_TERMS}
```

Then extract video titles and IDs using JavaScript:

```
Call: Claude in Chrome:javascript_tool
→ Code: references/youtube_extract.js (read this file for the full extraction script)
```

### 2c. Build the search query strategy

For each channel, run multiple search passes to maximize coverage:

| Pass | Query pattern | Example |
|------|--------------|---------|
| 1 | `{industry}` | `diagnostics` |
| 2 | `{primary company}` | `Thyrocare` |
| 3 | `{peer names}` | `Dr Lal Metropolis pathology` |
| 4 | `{industry} + business model OR analysis` | `diagnostics industry analysis` |

Deduplicate results across passes by video ID.

### 2d. Filter and classify videos

From the raw results, classify each video:

| Category | Priority | Indicators |
|----------|----------|------------|
| **Industry deep-dive** | HIGH | Titles containing "industry", "sector", "business model", "deep dive", "analysis" |
| **Management interview** | HIGH | Titles containing company name + "CEO", "MD", "management", "explains", "business model" |
| **Earnings / Concall discussion** | MEDIUM | Titles containing "Q1", "Q2", "results", "earnings", "quarterly" |
| **Stock / valuation commentary** | LOW | Titles containing "buy", "sell", "target price", "multibagger" |
| **Shorts / promos** | SKIP | Videos under 2 minutes, titles with "#Shorts", promotional clips |

Present the filtered list to the user for confirmation before proceeding to transcription. Include:
- Video title
- YouTube URL (`https://www.youtube.com/watch?v={VIDEO_ID}`)
- Estimated duration (if visible)
- Category classification
- Which channel it came from

**Do NOT proceed to transcription until the user confirms the video list.**

---

## Step 3 — Transcribe via HappyScribe

### 3a. Submit each confirmed video to HappyScribe

For each video URL in the confirmed list:

```
Call: HappyScribe:create_transcription
→ url: "https://www.youtube.com/watch?v={VIDEO_ID}"
→ language: "auto"
→ operation: "transcription"
```

### 3b. Known limitation: Long YouTube videos may fail

HappyScribe's server-side YouTube download is blocked by YouTube for some longer videos (typically 30+ minutes). If a video fails to appear in `HappyScribe:list_transcriptions` after 5 minutes:

1. **Resubmit once** — Sometimes a retry succeeds.
2. **If second attempt fails**, inform the user and provide the manual workaround:
   - Download the video locally using `yt-dlp`:
     ```bash
     yt-dlp -f "bestaudio" -o "%(title)s.%(ext)s" {YOUTUBE_URL}
     ```
   - Upload to HappyScribe via the upload widget:
     ```
     Call: HappyScribe:upload_file
     → User uploads the downloaded file
     → Returns client_upload_uuid
     ```
   - Then transcribe the uploaded file:
     ```
     Call: HappyScribe:create_transcription
     → client_upload_uuid: "{UUID_FROM_UPLOAD}"
     → language: "auto"
     → operation: "transcription"
     ```

### 3c. Monitor transcription progress

Poll for completion:
```
Call: HappyScribe:list_transcriptions
→ created_after: "{SESSION_START_ISO_DATETIME}"
→ limit: 20
→ preview_mode: "none"
```

Check that all submitted videos show `status: automatic_done`. Short videos (under 15 min) typically complete in 1-3 minutes. Longer videos (30-90 min) take 5-15 minutes.

---

## Step 4 — Retrieve and Convert to Markdown

### 4a. Pull full transcription text

For each completed transcription:

```
Call: HappyScribe:get_transcription
→ id: "{TRANSCRIPTION_HASHED_ID}"
→ display_mode: "full_text"
```

Batch up to 5 at a time using `get_transcriptions`.

### 4b. Convert to Markdown format

For each transcript, create a `.md` file with this structure:

```
Read references/markdown_template.md for the complete template
```

Key formatting rules:
- **Header block**: Title, source channel, YouTube URL, date, duration, speakers, transcription method, access date
- **Transcript body**: Replace `[Speaker N]` tags with identified speaker names where possible (from video title/description context). Format timestamps as `*(MM:SS)*`.
- **Key Takeaways section**: Add 5-10 bullet points summarizing the most analytically important points from the transcript. Focus on: business model insights, financial metrics mentioned, competitive dynamics, management guidance, industry structure data.
- **Separator line** (`---`) between header, transcript, and takeaways.

### 4c. File naming convention

```
{Source}_{Type}_{CompanyOrTopic}.md
```

| Field | Values |
|-------|--------|
| Source | Channel short name: `PPFAS`, `NDTV`, `SOIC`, `MoneyControl`, etc. |
| Type | `Transcript` (always) |
| CompanyOrTopic | Descriptive slug: `Thyrocare-Business-Model`, `Diagnostics-Industry-DeepDive`, `DrLal-CEO-Interview` |

Examples:
- `PPFAS_Transcript_Diagnostics-Lab-Business.md`
- `NDTV_Transcript_Thyrocare-Management-Business-Model.md`
- `SOIC_Transcript_Tata1mg-Disrupting-Diagnostics.md`

---

## Step 5 — Organize and Deliver

### 5a. Create output folder

All files go into a single folder in `/mnt/user-data/outputs/`:

```
/mnt/user-data/outputs/{Company} YouTube Transcripts/
```

Where `{Company}` is the primary company name from Step 1. Examples:
- `Thyrocare YouTube Transcripts/`
- `Diagnostics Sector YouTube Transcripts/`

### 5b. Copy all .md files into the folder

Use `bash_tool` to create the folder and move files:

```bash
mkdir -p "/mnt/user-data/outputs/{Company} YouTube Transcripts"
cp /home/claude/*.md "/mnt/user-data/outputs/{Company} YouTube Transcripts/"
```

### 5c. Generate a research index

Create an `_INDEX.md` file inside the folder that lists all transcripts with metadata:

```markdown
# {Company} — YouTube Transcript Library

**Generated:** {DATE}
**Channels searched:** {LIST OF CHANNELS}
**Search terms:** {TERMS USED}

## Transcripts

| # | File | Source | Duration | Category | Key Topic |
|---|------|--------|----------|----------|-----------|
| 1 | filename.md | PPFAS | 1h 17m | Industry deep-dive | Diagnostics lab business model |
| ... | ... | ... | ... | ... | ... |

## Videos That Failed Transcription

| # | Title | URL | Reason |
|---|-------|-----|--------|
| ... | ... | ... | HappyScribe YouTube download blocked |

## Notes
- Transcripts are auto-generated and may contain errors, especially for Hindi/English code-switched speech.
- Timestamps are approximate.
```

### 5d. Present files to the user

```
Call: present_files
→ filepaths: [all .md file paths in the output folder]
```

---

## Hard Rules

1. **NEVER search the full YouTube universe.** Only search channels explicitly provided or confirmed by the user. If zero channels are provided, ask for them — do not guess.
2. **NEVER proceed to transcription without user confirmation** of the video list. The user must approve which videos to transcribe (HappyScribe credits are consumed per minute of audio).
3. **Always use Claude in Chrome for YouTube search.** Web search and web_fetch cannot reliably extract video URLs from YouTube channel pages due to dynamic loading.
4. **Always include the Key Takeaways section** in every Markdown file. Raw transcripts alone have low research utility — the takeaways are what makes these files actionable.
5. **Always generate the _INDEX.md** research index. This is the audit trail and entry point for the transcript library.
6. **Flag transcription failures explicitly.** Do not silently drop videos. List them in the index with the failure reason and manual workaround.
7. **Deduplicate across channels.** The same video may appear on multiple channels (e.g., a management interview posted by both NDTV and the company). Prefer the version from the more authoritative source.
