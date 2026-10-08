# For spaces: cloud verification

Executed on 8 October 2026 against the cloud development server with Python Playwright and Chromium 151. No production form submissions, backend provisioning or emails.

Command: `python3 tests/browser_smoke.py`

```text
PASS: direct routes, redirect and shared assets
PASS: desktop layouts, links, keyboard access and non-collecting forms
PASS: mobile layouts, links, keyboard access and non-collecting forms
PASS: narrow layouts, links, keyboard access and non-collecting forms
PASS: JavaScript-disabled forms cannot submit
```

Desktop: 1440×1000; mobile: 390×844; narrow: 320×740. Both pages have no horizontal overflow. Tests cover navigation in both directions and the homepage invitation, skip links, field labels and ARIA references, keyboard submission and Enter from the email field. Both forms show the preview notice and focus it, without network requests, cookies or local/session storage. With JavaScript disabled, buttons remain disabled and Enter does not navigate or send field values. No browser JavaScript errors occurred.

Screenshots were visually reviewed. Optional Google Fonts is blocked by cloud network policy, so these captures use fallback typography:

| Page | Desktop | Mobile |
| --- | --- | --- |
| Homepage | [Screenshot](screenshots/home-desktop.png) | [Screenshot](screenshots/home-mobile.png) |
| Spaces | [Screenshot](screenshots/spaces-desktop.png) | [Screenshot](screenshots/spaces-mobile.png) |

`git diff --check` passed. No build step or existing CI suite is present. The development server redirects `/spaces` to `/spaces/` and serves the directory index. An explicit Vercel rewrite maps `/spaces` to `/spaces/index.html`; Vercel preview routing and deployment headers still need verification on an authorised preview when available.

Launch blockers: approved backend and privacy configuration for both forms; approval of provisional wording/mark and approval of illustrative example profiles; discovery technology and trial validation before hardware, cost or accuracy claims. These are future tasks, not completed work.
