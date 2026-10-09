# Presence: project brief and working rules

## Settled product decisions

Purpose: “Presence should be the layer to reduce the friction in making an IRL connection.”

The mechanism is a customisable, shareable personal page, with separate, optional local discoverability. Local visibility is off by default and under the person's control. Automatic discovery without repeated venue check-ins is the ambition; detection technology is not yet proven.

Keep the existing visual direction and “A reason to say hello.” The homepage stays consumer-first. Leah's founder story, Candid Conversations and table invitations belong on her LinkedIn, not this site.

This phase excludes perks, loyalty schemes, recruitment marketplaces, event platforms, AI matching, messaging and profile-building apps.

Spaces could introduce Presence and give trial feedback. Participation does not require events or discounts. Any trial equipment should be small and discreet, fitting quietly into the space; this is a design intention pending technical validation. Small Bluetooth beacons are being investigated; hardware requirements, costs and accuracy remain unconfirmed. Explain how a trial could fit into a space and the intended benefit of helping regulars and newcomers connect. The proposed early-trial approach is for Presence to supply any required equipment instead of asking spaces to buy a beacon; this is exploratory, not an approved supply or funding commitment. Interest is neither a commitment nor a public venue listing.

A shareable page for participating spaces is a proposed benefit, independent of local discovery. A fictional static host-page example illustrates the proposed space page; no live venue pages or listing service are built by this preview, and interest never creates a page or public listing.

Both interest forms remain explicitly non-collecting previews until an approved backend and privacy configuration exist. Never simulate successful registration or collect personal data during development.

## Working rules

- Start from the latest default branch, read the README and open PRs, and respect concurrent changes. Extend the existing site rather than replacing it.
- Use the cloud workspace for checkout, development, browser testing and gates. Do not use the user's Mac or start local Docker. Use the existing isolated checkout; do not create worktrees unless requested.
- Retain the static-site approach unless a demonstrated need requires otherwise. Share styles and preview behavior; avoid duplicate specifications.
- Follow repository instructions, including `.flow/PROTOCOL.md` if added. No Flow automation is currently installed in this repository.
- Test desktop and mobile layout, navigation, keyboard use, form behavior (including JavaScript disabled) and direct `/spaces` routing. Use synthetic data only against the cloud development server; never submit test data to production.
- Open focused PRs with screenshots, actual test results and remaining launch blockers. Return a verified authorised preview URL when available. Do not merge, change production settings, provision services, send emails or deploy to production without explicit authorisation.

## Launch blockers and possible follow-on work

Registration needs an approved privacy notice naming the controller, contact, purpose, provider and deletion process, plus an approved backend configuration. The mark and wording remain provisional; example photographs are from Unsplash and depict illustrative fictional profiles. Local discovery needs technical and trial validation before any performance or hardware claims.

Backend integration, discovery experiments and public launch approval are follow-on work, not implemented features. This brief records direction, not proof that a task or gate has completed. Consult each PR for its verified scope and results.

A concise host PDF is proposed follow-on work for outreach or sharing after an initial conversation: purpose, hoped-for benefits, trial expectations and unresolved questions. Use a shared core with relevant space photography (host-supplied with permission or licensed). Tailoring and distribution are not implemented, and this does not enable registration or automatic email delivery.
