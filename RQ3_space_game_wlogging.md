# Requirements: `question-builder.html` — v1

## Purpose

A standalone local browser tool that accepts uploaded study files, uses an LLM to generate quiz questions compatible with the Space Quiz game, allows human review and approval, and produces a downloadable `questions.json` for use in the game.

---

## Constraints

- Single HTML file, no build step, no framework
- Runs locally at `localhost` only (not hosted publicly)
- One CDN dependency: mammoth.js (Word doc parsing)
- No server required

---

## Supported File Types

| Type | Extension | How it's read |
|---|---|---|
| Word document | `.docx` | mammoth.js → plain text |
| Java source file | `.java` | FileReader API → plain text |
| Handwritten notes | `.jpg`, `.jpeg`, `.png` | FileReader → base64, sent as image to LLM (requires multimodal model) |

Multiple files can be dropped at once. All content is combined into a single context and sent to the LLM as one batch.

---

## Modules

| Module | Responsibility |
|---|---|
| **FileIngestor** | Drag-and-drop zone, file type detection, reading files via FileReader / mammoth.js |
| **LLMConnector** | Model-agnostic fetch wrapper, injects API key from settings, formats prompt, parses response, captures token usage from response |
| **ReviewUI** | Renders questions as cards, approve/reject per card, select-all / deselect-all, undo |
| **StorageManager** | localStorage for version history, usage log, settings persistence |
| **DeployManager** | Validates approved questions, generates `questions.json` download |
| **SettingsPanel** | API key entry, model/endpoint config, skip-review toggle, per-token pricing table |
| **UsageTracker** | Logs token counts and estimated cost per call, stores cumulative totals, renders usage panel |

---

## User Flow

```
1. SETTINGS (first time)
   └── Enter API key + model endpoint → saved to localStorage
   └── Optionally set per-token pricing for cost estimates

2. UPLOAD
   └── Drag and drop one or more files onto drop zone
   └── Files parsed → combined text/images assembled
   └── [Undo: clear uploaded files, return to drop zone]

3. GENERATE
   └── LLM called with combined content + prompt
   └── Token usage captured from API response → logged to UsageTracker
   └── Response parsed into question objects
   └── [Undo: re-run generation, discard previous output]

4a. REVIEW (skip-review = off)
   └── Questions displayed as cards
   └── Approve / reject each card individually
   └── Select all / deselect all available
   └── Rejected questions discarded (not saved — v2 adds discarded list)
   └── [Undo: restore last rejected question]
   └── "Deploy approved questions" button → go to step 5

4b. SKIP REVIEW (skip-review = on)
   └── All generated questions auto-approved
   └── Proceed directly to step 5

5. DEPLOY
   └── Approved questions validated against game format
   └── questions.json download triggered
   └── Version snapshot saved to localStorage (timestamp + question count + content)
   └── If user cancels download or no questions approved: previous file unchanged
   └── [Undo: download the previous version from version history]

6. VERSION HISTORY (accessible any time)
   └── List of past deployments with timestamp and question count
   └── Any version can be re-downloaded
```

---

## Question Format

Output must conform to the game's existing format. Each question requires exactly 3 wrong answers.

```json
[
  {
    "question": "What is X?",
    "correct": "Right answer",
    "wrong": ["Wrong 1", "Wrong 2", "Wrong 3"]
  }
]
```

The LLM prompt must explicitly require this structure. Validation runs before download is offered.

---

## Settings

| Setting | Storage | Default |
|---|---|---|
| API key | localStorage | (empty) |
| Model endpoint URL | localStorage | (empty) |
| Model name | localStorage | (empty) |
| Skip human review | localStorage | off |
| Input token price (per 1M tokens) | localStorage | (empty — cost tracking skipped if unset) |
| Output token price (per 1M tokens) | localStorage | (empty — cost tracking skipped if unset) |

Settings panel accessible from a persistent button. Changing skip-review takes effect on the next generation.

---

## Usage Tracker

Captures data returned by the API response after each LLM call. Nothing is estimated or assumed — only what the API reports is recorded.

**Per-call log entry:**
- Timestamp
- Model name
- Input tokens
- Output tokens
- Estimated cost (input tokens × input price + output tokens × output price — only shown if pricing is set in Settings)

**Cumulative totals:**
- Total input tokens (all time)
- Total output tokens (all time)
- Total estimated spend (only shown if pricing is set)

**UI:**
- "Usage" button in top bar opens a panel
- Shows cumulative totals at the top
- Shows per-call history table below (most recent first)
- Note in panel: "To check your remaining balance, visit your provider dashboard"
- Stored in localStorage

---

## Undo Points

| Stage | What undo does |
|---|---|
| After upload | Clears all files, returns to drop zone |
| After generation | Discards LLM output, allows re-upload or re-generate |
| During review | Restores the last rejected question to approved |
| After deploy | Makes previous version available for re-download |

---

## Version History

- Stored in localStorage as an array of snapshots
- Each snapshot: timestamp, question count, full questions array
- Displayed in a collapsible panel
- Any snapshot can be re-downloaded as `questions.json`
- No automatic pruning in v1 (storage alert deferred to future version)

---

## Out of Scope for v1

- Discarded questions list (v2)
- Claude API specifically (v2 — currently model-agnostic)
- Storage size alert (future)
- Public hosting / authentication (future)
- Inline question editing during review (future)
