# Presence — holding page

Static holding page for Presence ("A reason to say hello."). No build step: `index.html`, `styles.css`, `preview.js`, `mark.svg`, `assets/`.

**Status:** in development, preview only. The mark and wording are provisional and pending approval. The waitlist form is a labelled design preview: it sends and stores nothing and never reports success. Wire a real backend (with an approved privacy notice) before removing that notice. `assets/sample-coast.jpg` is a generated placeholder, not a real photograph.

Run locally: `npx serve .` (or any static server). Deployed via Vercel from `main`; `vercel.json` sets `X-Robots-Tag: noindex`.

`/spaces` is the separate space-interest preview, served from `spaces/index.html`. Its form also sends and stores nothing. Shared direction and working rules live in [docs/PROJECT_BRIEF.md](docs/PROJECT_BRIEF.md).

Cloud development (no build or runtime dependencies):

```sh
python3 -m http.server 3000 --bind 127.0.0.1 --directory /workspace/presence
```

Browser gate (requires Python Playwright and Chromium; both are available in the prepared cloud environment):

```sh
python3 tests/browser_smoke.py
```

The gate uses synthetic data against the development server only and saves desktop/mobile screenshots outside the checkout by default. Set `PRESENCE_SCREENSHOT_DIR` to choose their location. Google Fonts is optional; network restrictions may cause fallback typography. The Python server does not apply Vercel deployment headers.
