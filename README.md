# Presence — holding page

Static holding page for Presence ("A reason to say hello."). No build step: `index.html`, `styles.css`, `preview.js`, `mark.svg`, `assets/`.

**Status:** in development, preview only. The mark and wording are provisional and pending approval. The waitlist form is a labelled design preview: it sends and stores nothing and never reports success. Wire a real backend (with an approved privacy notice) before removing that notice. Example-page photographs are from Unsplash (Annie Spratt, Daniel Gamez, Behnam Samipour) under the Unsplash licence; the people shown are not the fictional characters named.

Run locally: `npx serve .` (or any static server). Deployed via Vercel from `main`; `vercel.json` sets `X-Robots-Tag: noindex`.

## Split-layout concept

On this exploration branch, the default straight connection eases into a person,
briefly enlarges the orange dot, and holds through a wider scroll interval before
withdrawing. A faint dashed circle identifies the target as the connection
approaches. Before release, the target grows slightly and yields a few pixels;
it then settles back as the line gently retracts and the circle fades.
Only the illustration settles; page scrolling is never snapped.
`?v=thread` and `?v=ripple` remain available for comparison. Reduced-motion mode
shows a static connection and dashed target circle, with no pulses or scroll-driven movement, including
when the preference changes while the page is open.

Cloud browser regression gate (Python Playwright and `/usr/bin/chromium`):

```sh
python3 tests/connection_browser.py
```

The gate starts its own temporary cloud static server. It tests desktop, tablet,
mobile and narrow layouts, forward/reverse scroll, connection hold and endpoint,
reduced-motion changes, navigation and the non-collecting form. Synthetic form
data is submitted only to that temporary development server.

## Spaces in the split concept

The consumer homepage links discreetly to `/spaces`, which uses the same split
layout, shared styles and connection field. Its content carries over the trial
walkthrough and proposed early equipment supply from the current main site.
A shareable page for participating spaces is described as a proposed feature;
this static preview does not create live venue pages or public listings.
`/spaces` includes a compact fictional host-page example in the same phone frame as the personal examples. It links to the full café page at `/spaces/example`; both use the same original illustration.
Any trial equipment is intended to be small and discreet; specifications remain exploratory.

Both interest forms use the shared non-collecting preview handler. Buttons stay
disabled until the handler is installed, so disabling JavaScript cannot submit
field values. No backend, email provider or data collection is configured.

Run `python3 tests/spaces_browser.py` for routes, responsive layouts, navigation,
keyboard/label checks and both forms, including JavaScript-disabled behavior.

## Access gate

`middleware.js` is a free edge gate: if the `PRESENCE_CODE` env var is set in Vercel, visitors see a code prompt and get a 30-day cookie on success. Delete the env var (and redeploy) to open the site. Don't use Vercel's built-in Password Protection — it is a paid add-on.

## Provisional mark

`mark.svg` is the shared loose-orbit mark for page headers, personal-page examples and the favicon. Outer dots vary subtly in angle and distance around a stable centre; the orange connection remains. See `docs/logo-review/index.html` for the old/new comparison at small and large sizes.

## Host conversation pack

`assets/presence-for-spaces.pdf` is a static four-page PDF linked from `/spaces`.
The editable source and edition configuration are in `docs/host-pack/`.
Rebuild in the prepared cloud environment (Python Playwright and Chromium):

```sh
python3 scripts/render_host_pack.py --screenshots docs/host-pack/review
```

The renderer uses bundled fonts/images through a temporary cloud asset server;
no external services or network assets are needed. It checks image/font loading,
page overflow and footer clearance before creating a tagged PDF.
See [edition guidance](docs/host-pack/README.md) for manual photo/copy tailoring.
