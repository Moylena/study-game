# Learning Log

A running record of concepts picked up while building this project.

---

## Git

**Why API keys must never be committed to git**
Git history is permanent. Even if you delete the key from a file and commit again, it still lives in the history — anyone who clones the repo can scroll back and find it. GitHub bots actively scan public repos for exposed keys within seconds of a push. Best practice: API keys are entered at runtime or stored in a `.env` file that is listed in `.gitignore`.

---

## Browser Concepts

**localStorage**
A browser API that lets a web page save small amounts of data (strings) that persist across page refreshes and browser restarts. Sandboxed per origin — only the page that saved the data can read it. Not encrypted. Good for local tools; not suitable for sensitive data on public-facing sites.

**CORS (Cross-Origin Resource Sharing)**
A browser security rule. When your JavaScript on one domain (e.g. `localhost:8000`) tries to call an API on a different domain (e.g. `api.openai.com`), the browser checks whether the API server sends back headers explicitly allowing that. Most LLM APIs allow it. A backend server sidesteps CORS entirely because server-to-server calls aren't subject to browser security rules.

**File System Access API**
A modern browser API that lets a web page request permission to read/write files directly on your disk. Requires the user to grant access once via a file picker. Alternative to downloading files manually. Not used in question-builder v1 (chose download-each-time instead), but worth knowing.

**HTML5 File API + Drag and Drop**
Native browser APIs for accepting files dropped onto a webpage. No libraries needed. `FileReader` reads file contents as text or base64. Works for plain text files (.java, .txt, .md). Needs a helper library (mammoth.js) for binary formats like .docx.

---

## Libraries

**mammoth.js**
A small JavaScript library (loaded via CDN, no install) that extracts plain text from `.docx` Word files in the browser. Used in question-builder to convert uploaded Word docs into text before sending to the LLM.

---

## Architecture Decisions

**Browser-only vs. small server**
A browser-only tool is simpler to build and requires no running server. Fine for local tools (localhost) where only you use it. A server is better when: the tool is public-facing, the API key needs to stay hidden, or file processing is too heavy for the browser. LLM API costs are the same either way.

**localhost security**
`localhost` is only reachable on your own machine. It is not accessible from the internet. A URL like `localhost:8000` cannot be visited by anyone else. Security concerns about API key exposure apply only when a tool is hosted on a public URL.

---
