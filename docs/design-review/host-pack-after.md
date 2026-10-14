| ID | Status | Evidence |
| --- | --- | --- |
| V-1 | pass | Two complete directions rendered; differences and rejection reason recorded in `host-pack-brief.md`; alternate previews retained. |
| V-2 | pass | All four actual PDF pages inspected at print and phone fit-to-page sizes; screenshots in `docs/host-pack/review`. |
| S-1 | pass | Main ink on ground 16.06:1; muted #5E5B57 on ground 6.24:1; no text over photographs. Printed stock needs Dan. |
| S-11 / S-26 | pass | Words explain the mechanism; both the scenario and venue are explicitly fictional, photo is stock; no invented evidence. |
| S-21 / S-32 | pass | Internal privacy terminology replaced with visitor-information choices; non-sequence category numbers removed. Page counts are actual pagination. |
| H-20 | pass | Repeated caps, category numbering, left-border callout and heavy phone frame replaced by the content-led connection motif and simpler hierarchy. |
| H-18 | pass | Concrete scenario, useful photo caption, configured contact and user-confirmed Leah sign-off improve specificity. Real host content is not invented. |
| V-4 | pass | Static applicable checks: selectable/tagged text, fonts/images loaded, no clipping/footer overlap, valid email/domain link annotations. Not a PDF/UA certification. |
| V-5 | needs Dan | Agent critique finds a stronger signature and the top three changes are addressed. Independent logo-swap/perception and final major-work ornament judgement are not complete. |
| V-3 / V-6 / S-33 | needs Dan | No fresh independent perception test or three representative host sessions performed. |
| S-32 / H-21 final major call | needs Dan | Ornament log is provided; final human judgement remains required. |
| V-7 | pass | Status/evidence ledger distinguishes completed checks from human-dependent work. |

# Critique: Presence host invitation — review-ready revision — major

Verdict: the mechanism is concrete, host expectations are earlier, and the contact is explicit. Eye lands on the established tagline followed by a fictional shared-interest moment. Signature is the paired introductions and connection language. Logo-swap: the connection now explains the idea within the inherited Presence system; independent recognition still needs testing.

## Applied top three

1. Cover explains a specific visitor moment and separates sharing from optional discovery. No automatic scanning or proven hardware is implied.
2. Page 2 makes host expectations and trial arrangements visible. Page 3 reduces the example’s visual weight and gives unresolved equipment/detection its own plain section. No category numbers remain.
3. Page 4 uses a direct contact and questions a host can answer, including what would make them say no. Email/domain links use meetpresence.com. Leah signs off, as confirmed by the user.

## Page verdicts

- Page 1: aligned two-introduction comparison; high text contrast; motif explains common interest; no generic stock hero delaying the proposition. Fiction label precedes the imagined moment.
- Page 2: role columns align; practical copy is 11pt rather than compressed below a phone; photograph is subordinate and its caption explains its relevance. Fits with footer clearance.
- Page 3: smaller flat example, direct annotations and one open-questions section; no nested topic chips or decorative step numbering. Fits, with selectable text.
- Page 4: three specific conversation prompts, prominent configured address and a direct next action; no anonymous “continue with whoever shared this” instruction. Remaining privacy/trial matters stay honest.

Phone fit-to-page viewing still makes an A4 document small; a real-device reading task is needed. The redesign improves hierarchy and raises the minimum PDF caption size from approximately 8pt to 9pt. S-31's web/email font minimums are not misapplied to print/static PDF.

## Verification

- Offline renderer: all fonts/images loaded; four pages fit; no footer overlap; tagged PDF and outline generated.
- PDF inspection: four tagged pages, correct fiction/exploratory wording, no 01/02/03 category labels, `mailto:hello@meetpresence.com` and `https://meetpresence.com/spaces` links, no temporary/local-server link URLs.
- Both directions rendered successfully. Primary PDF size approximately 624 KB.
- `tests/spaces_browser.py`: route/PDF/keyboard/form gates passed at 1440/768/390/320px, including JavaScript disabled. Synthetic entries only on temporary cloud server.
- Production website code/configuration is unchanged. All site-audit failures are reported separately and are not disguised as fixed by this PDF revision.

Not tested: human perception/tasks, actual paper stock, PDF screen reader, or new trials. No production publication is performed by this PR.
