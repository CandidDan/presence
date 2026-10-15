| ID | Status | Evidence |
| --- | --- | --- |
| V-1 | pass | Two complete directions rendered; differences and rejection reason recorded in `host-pack-brief.md`; alternate previews retained. |
| V-2 | pass | All five actual PDF pages inspected at print and phone fit-to-page sizes; screenshots in `docs/host-pack/review`. |
| S-1 | pass | Main ink on ground 16.06:1; muted #5E5B57 on ground 6.24:1; Cover uses a solid scrim: worst-case light-text contrast at least 5.30:1; other text is on flat ground. Printed stock needs Dan. |
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

1. The opening explanation shows a specific visitor moment and separates sharing from optional discovery. No automatic scanning or proven hardware is implied.
2. Page 3 makes host expectations and trial arrangements visible. Page 4 reduces the example’s visual weight and gives unresolved equipment/detection its own plain section. No category numbers remain.
3. Page 5 uses a direct contact and questions a host can answer, including what would make them say no. Email/domain links use meetpresence.com. Leah signs off, as confirmed by the user.

## Page verdicts

- Page 1: edge-to-edge illustrative café photograph, small mark and dominant established tagline. Solid scrim provides at least 5.30:1 light-text contrast even over a white image pixel. Print proof and perception test remain needs Dan.
- Page 2: matched interests explicitly belong to you and another person; the text states that local walks is what you share. High-contrast typography and fiction label; no claim of a live feature.
- Page 3: aligned host-role columns; practical expectations are the focus. The photograph is not repeated. Event/discount requirements and hoped-for benefit remain clear. Fits with footer clearance.
- Page 4: smaller example and annotations; plain “Before a trial” section explains that discovery needs testing and equipment, costs and help would be agreed. No Bluetooth or beacon terminology. Fits with footer clearance.
- Page 5: direct email invitation, three useful questions and Leah’s confirmed sign-off. The example/photograph disclaimers and credits remain present. Fits with footer clearance.

Phone fit-to-page viewing still makes an A4 document small; a real-device reading task is needed. The redesign improves hierarchy and raises the minimum PDF caption size from approximately 8pt to 9pt. S-31's web/email font minimums are not misapplied to print/static PDF.

## Verification

- Offline renderer: all fonts/images loaded; five pages fit; no footer overlap; tagged PDF and outline generated.
- PDF inspection: five tagged pages, correct fiction/exploratory wording, no 01/02/03 category labels, `mailto:hello@meetpresence.com` and `https://meetpresence.com/spaces` links, no temporary/local-server link URLs.
- Both directions rendered successfully. Primary PDF size approximately 0.6 MB.
- `tests/spaces_browser.py`: route/PDF/keyboard/form gates passed at 1440/768/390/320px, including JavaScript disabled. Synthetic entries only on temporary cloud server.
- Website code/configuration is unchanged apart from the PDF download’s page-count label. All site-audit failures are reported separately and are not disguised as fixed by this PDF revision.

Not tested: human perception/tasks, actual paper stock, PDF screen reader, or new trials. No production publication is performed by this PR.

## Cover and clarity follow-up

The pack now opens with an edge-to-edge illustrative café photograph and the hero wording “A reason to say hello.” The original explanation is page 2, titled “An interest in common”, and explicitly states that local walks is shared by both people. The image is no longer repeated on the host-role page. Bluetooth/beacon vocabulary has been removed from the plain-language “Before a trial” section; unproven discovery and proposed equipment/support arrangements remain clear. Leah signs page 5.

Page-fit and tagged-PDF checks were rerun for five pages. Professional print bleed/stock and independent perception checks remain human work. The prior four-page direction comparisons are retained as historical exploration, not claimed as the current cover.
