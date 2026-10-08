# Presence — holding page

Static holding page for Presence ("A reason to say hello."). No build step: `index.html`, `styles.css`, `preview.js`, `mark.svg`, `assets/`.

**Status:** in development, preview only. The mark and wording are provisional and pending approval. The waitlist form is a labelled design preview: it sends and stores nothing and never reports success. Wire a real backend (with an approved privacy notice) before removing that notice. Example-page photographs are from Unsplash (Annie Spratt, Daniel Gamez, Behnam Samipour) under the Unsplash licence; the people shown are not the fictional characters named.

Run locally: `npx serve .` (or any static server). Deployed via Vercel from `main`; `vercel.json` sets `X-Robots-Tag: noindex`.
