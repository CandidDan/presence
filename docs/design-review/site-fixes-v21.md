| ID | Status | Evidence |
| --- | --- | --- |
| S-1 / S-2 | pass | Feedback 16.06:1, keyboard outline 6.21:1, field boundary 4.66:1. Tested rendered styles on both forms. |
| S-4 / S-5 / S-8 / S-12 | pass | Four-width navigation/form/motion gates; keyboard status focus; disabled-JavaScript closure; reduced-motion changes and both animation variants. |
| S-6 | pass | Six routes × three widths × normal/200% text/prescribed text spacing: 54 checks, no horizontal overflow. |
| S-21 / S-22 | pass | “Try the form preview” matches its non-collecting outcome. Readiness copy uses everyday language; live mode has separately named update-request buttons. |
| S-29 / S-30 | pass | Eight named spacing steps, seven type roles, semantic colour roles; no literal component spacing/font sizes outside the scale. The largest spacing step is responsive within reading sections. No dark theme is offered. |
| S-0 | needs Dan | Zero axe violations in 18 default-state scans plus targeted manual checks; these do not establish full WCAG conformance. Screen reader, forced colours and real devices remain unverified. |
| S-27 lab | pass | Final mobile cloud samples: home LCP 2.178s, spaces 1.427s; both TBT 0ms and CLS 0.00004. |
| S-27 field | needs Dan | No real-user p75 LCP/INP/CLS evidence. |
| V-2 | pass | Section verdicts below and screenshots beside this report. |
| V-3 / S-33 / V-5 final | needs Dan | Independent image-only purpose test and final perception/ornament judgement outstanding; Leah signs off. |
| V-1 / V-6 | n.a. | This is an existing-site refinement, not a new major design direction. |
| V-7 | pass | Implemented fixes, measured evidence and human review are separated. |

# Presence website: v2.1 audit recommendations applied

Scope: Mi refinement of existing web pages, based on main `4a5e56c507cff61eb4e308cd690d379febdca27c`. Standards: [core v2.1](https://github.com/CandidDan/mods/blob/aaf177483c33ae4158d4ecb43d710e7e277ef628/design-standards/skills/design-standards/SKILL.md) and [audit](https://github.com/CandidDan/mods/blob/aaf177483c33ae4158d4ecb43d710e7e277ef628/design-standards/skills/design-standards-audit/SKILL.md). The original findings and PDF redesign are in PR #16. Its reviewed five-page pack and editable source are now included here so the updated website downloads the same PDF.

## Intent inherited from the canonical brief

I-1: a person deciding whether Presence makes an in-person introduction easier, or a host considering a conversation about a trial. I-2: understand the idea and decide whether to explore further. I-3: “A reason to say hello,” with personal sharing and voluntary local visibility clearly separate. I-4: inherit the existing identity and split layout. I-5: clarity wins. I-6: static web, desktop and mobile.

I-7: the examples help people understand the idea without mistaking them for live profiles. Test this with readers; it is not proven by an automated scan. I-8: welcoming, quiet, curious; reference a short introduction in a welcoming shared place; signature the split reading layout and forming/breaking connection. I-9: keep that unusually slow connection metaphor, because it demonstrates a voluntary opening rather than demanding an immediate interaction.

## What changed

The previous 3.51:1 feedback, 1.92:1 focus outline and 1.57:1 field boundary have dedicated high-contrast roles. Headers, labels, badges and buttons can wrap. Sticky panels can grow; the development badge participates in mobile layout so enlarged text does not run beneath it. Headline nonbreaking spaces no longer force an overflow.

Shared CSS and inline rules use an eight-step spacing and seven-role type system. The largest spacing step responds to viewport height within the long reading column, while phone-example spacing remains fixed. Phone frames, avatars, glyph sizes and radii are component geometry, separate from the rhythm scale. Semantic colours include distinct text, surface, accent, focus and control roles. Orange remains decorative rather than carrying readable feedback.

Homepage entry says “Explore early access”; both form buttons say “Try the form preview.” Feedback explicitly says nothing was sent or stored. Operational readiness details stay in the setup/privacy documentation; marketing copy says who looks after details and how to delete them will be explained before signup opens. The prepared live mode names the update-request outcome, but stays disabled.

Existing Outfit fonts are delivered as WOFF2 (54KB total instead of 143KB),
with identical glyph mappings and widths; original TTFs remain for editable
print sources. Initial uncompressed local mobile Lighthouse home samples were
2.507s and 2.554s LCP, just over the 2.5s gate. After compression the final
samples pass; all samples, including failures, are retained in the summary.
These are cloud lab results, not field or production measurements.

## V-2 section review

- Home first view: split layout and hand-set headline remain recognisable; navigation wraps without meeting the badge under enlargement. Contrast and hierarchy support reading.
- Home three steps: glyph/text alignment and common vertical rhythm retained; each step explains sharing, control or connection rather than decoration alone.
- Home examples: interests/photos provide concrete conversation context, labelled illustrative; cards and link rows wrap at increased text size. Two examples remain pending reader feedback.
- Home early access and spaces invitation: darker field edges/status text; action describes preview behaviour; operational wording shortened. Link to spaces stays discreet.
- Spaces first view and shareable host example: same character, clearly proposed/fictional, readable optional-choice explanation. Trial claims remain exploratory.
- Spaces trial/equipment: actual sequence numbering retained; no cost, hardware accuracy or equipment-supply commitment introduced.
- Spaces form: visible labels, wrapping, focus and feedback verified; registration remains closed and non-collecting.
- Fictional host page: identity and navigation wrap; fiction notice remains prominent; content fits all tested text conditions.
- Privacy, cookies and preview information: inherited readable single column, named text/spacing roles, draft placeholders retained. No approved legal operator or working signup is invented.

## V-5 critique and ornament log

Top three audit fixes implemented: (1) contrast, (2) enlargement/reflow, (3) honest preview actions plus named scales. Hover lift was removed; hover still changes the button surface.

The agent logo-swap review finds character in the split invitation and gentle voluntary connection, visible without the mark. This is an agent judgement, not independent reader evidence.

- Field dots, orange line and dashed target circle: carry the existing connection/choice signature; remain at the existing faint opacity and static under reduced motion.
- Example phone frames and photographs: show what a personal introduction or host page could contain; labelled illustrative and retained for reader testing.
- Topic pills: carry actual example interests; test whether readers need both profiles before reducing them.
- Trial numbers: indicate a real ordered walkthrough, not decorative counting.
- Development pill: signals actual preview state; grows in normal mobile flow under text enlargement.

## Verification and limits

All development and browser checks used temporary cloud static servers; no production form was submitted. `signup-config.js` stays unchanged with collection disabled.

- `python3 tests/design_browser.py`: 54 reflow/text-condition checks; rendered contrast values and keyboard status focus; eight spacing/seven type roles.
- `python3 tests/spaces_browser.py`: 1440/768/390/320 layouts, direct routes, PDF download, host example, labels, navigation, forms and JavaScript-disabled behaviour.
- `python3 tests/connection_browser.py`: all four widths, forward/reverse scroll, halo/hold/tension/return, static reduced motion and thread/ripple variants.
- `python3 tests/subscriptions_browser.py`: supporting pages at four widths, fail-closed configuration, mocked consent/payload/accepted request/error/duplicate behaviour. Every provider call mocked; no email sent.
- Axe-core 4.10.3: six routes × 1440/390/320, zero default-state WCAG A/AA-tagged violations. This does not prove every manual criterion or hidden/live provider state.
- Actual scan measurements, keyboard walks, form contrast and selected screenshots are in `site-fixes-evidence/`. Runtime access cookies are excluded.

### Remaining launch blockers and human checks

Leah's visual/copy sign-off and an independent two-second purpose test remain outstanding. Test screen-reader use, forced colours, actual phones and reading with the connector at different scroll positions. The decision to shorten/remove a profile example should follow reader feedback, not an untested assumption.

Real signup still requires approved responsible-operator/contact/retention details, approved privacy/hostname configuration and an authorised real-provider delivery test. Local discovery still needs technical and trial validation. The `/spaces` host-pack link now downloads the five-page edition with its full-bleed “A reason to say hello” cover. No service, collection, campaign, public venue listing or production deployment is enabled by this PR.
