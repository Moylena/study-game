# Space Quiz Game — Knowledge Base

## What This Project Is
A browser-based spaceship shooter study game. A question appears at the top of the screen; four asteroids fall with answer choices inside them. The player moves a gun left/right and shoots the asteroid with the correct answer. Wrong answer or missed asteroids = game over.

---

## Files

| File | Purpose |
|------|---------|
| `space-quiz.html` | The full game — open via local server to play |
| `questions.json` | Edit this file to change or add questions |
| `space-quiz-tests.html` | Unit tests for pure game logic — open in browser |
| `KNOWLEDGE_BASE.md` | This file |

---

## How to Run

Requires a local server (because the game fetches `questions.json`):

```bash
cd /Users/ariellemoylen/Git
python3 -m http.server 8000
```

Then open: `http://localhost:8000/space-quiz.html`

To stop the server: `Ctrl+C`

---

## How to Add/Edit Questions

Edit `questions.json` directly in VS Code and save. Refresh the browser to pick up changes.

**Format:**
```json
[
  {
    "question": "Your question here?",
    "correct": "Right answer",
    "wrong": ["Wrong 1", "Wrong 2", "Wrong 3"]
  }
]
```

**Rules:**
- `wrong` must have exactly 3 items
- Answers can be words, numbers, or mixed
- Every entry except the last needs a comma after its closing `}`

---

## Game Rules

- 1 point per correct answer
- Shooting a wrong asteroid = game over
- Any asteroid reaching the bottom = game over
- After all questions answered or game over: score is shown for 5 seconds, then returns to start screen
- Score resets each game

## Controls

| Key | Action |
|-----|--------|
| Left arrow | Move gun left |
| Right arrow | Move gun right |
| Spacebar | Fire one bullet |

---

## Branch Structure

| Branch | Purpose |
|--------|---------|
| `cld_game_base` | Stable v1 baseline — hardcoded questions, single HTML file |
| `cgpt_v2_game_branch` | v2 — questions loaded from `questions.json`, dynamic font sizing |
| `dyn_qs_branch` | Current working branch — branched from v2 |

---

## Architecture Notes

- Single HTML file + separate `questions.json` — no build step, no dependencies
- Game loop uses `requestAnimationFrame` with delta-time capped at 50ms (handles tab switching)
- Asteroids are placed in shuffled horizontal zones to prevent overlap
- Answer font size auto-scales to fit text within asteroid circle (min 9px, max 15px)
- All answers normalised to strings at load time — numeric answers work fine

### Game States
```
LOADING → START → PLAYING → END → START
              ↓
            ERROR
```

### Pure Functions (tested in space-quiz-tests.html)
- `shuffleArray(arr)` — Fisher-Yates shuffle, returns new array
- `buildAsteroids(qObj)` — creates 4 asteroid objects from a question
- `asteroidFontSize(text)` — calculates font size to fit text in circle
- `bulletHitsAsteroid(b, a)` — circle collision detection
- `asteroidReachedBottom(a)` — floor boundary check
- `validateQuestions(data)` — validates loaded JSON structure

---

## Known Decisions & Trade-offs

- **Why `fetch` instead of hardcoded?** Makes questions editable without touching game code
- **Why a local server?** Browsers block `fetch` on `file://` protocol for security
- **Why zones for asteroid placement?** Prevents asteroids from overlapping horizontally
- **Why cap delta-time at 50ms?** Prevents huge position jumps when user switches tabs
