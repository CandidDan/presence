| ID | Status | Evidence |
| --- | --- | --- |
| S-0 | fail | Default-state axe scans are clean, but manual S-1/S-2/S-6 failures prevent a full WCAG-AA/standards pass. |
| S-1 | fail | Preview-status text #B9731F on #F6F6F4 is 3.51:1 at 16px; requires 4.5:1. Demonstrated on the cloud clone only, without submitting production forms. |
| S-2 | fail | Link focus ring #F0A35E on ground is 1.92:1; input boundary #CFCECA on white is 1.57:1. Neither reaches 3:1. Input focused black border is stronger, but link focus has no equivalent indicator. |
| S-4 / S-5 | pass | Browser keyboard walks across six pages; navigation and fields operable, outlines present and focus scrolls into view. Focus contrast still fails S-2. Real-device/screen-reader checks need Dan. |
| S-6 | fail | Baseline 320px reflow passes. Home/spaces prescribed text spacing produces 328px document width at 320px; 200% text yields 441px document width and menu overflow. Other audited routes retain width. |
| S-7 / S-8 | pass | Axe WCAG 2/2.1/2.2 A/AA scans: zero automated violations across six routes and three widths; illustrative images have alt/hidden semantics. This is bounded automated evidence, not blanket conformance. |
| S-12 | pass | Existing connection gate passes live preference changes, static reduced-motion state and scroll-driven variants. No autoplay media detected. |
| S-24 / S-26 | pass | Consent unchecked, non-collecting notices visible, no fake subscription success; profile/venue examples labelled illustrative/fictional. |
| S-27 lab | pass | Mobile Lighthouse home LCP 1.474s/TBT 0ms/CLS 0.00068; spaces LCP 1.118s/TBT 0ms/CLS 0.00068. Both performance/accessibility scores 100. Single cloud lab samples, not field p75. |
| S-27 field | needs Dan | Real-user p75 LCP/INP/CLS unavailable. |
| S-29 / S-30 | fail | Source uses many unrelated literal spacing/type values and hardcoded colours without a named scale/role-token layer. These strict S requirements are not waived by the inherited visual brand. |
| S-33 / V-3 / V-6 | needs Dan | No controlled two-second or three representative task sessions. |
| V-2 | pass | Full-page/section screenshots reviewed, including changed text conditions. Main page findings below. |
| V-4 | fail | Accessibility scan, keyboard, contrast, 320px, text-spacing and 200% text checks completed; manual failures remain. |
| V-5 | needs Dan | Agent critique finds a stronger signature than the old PDF: split layout and voluntary connection motion. Top three changes logged below. Independent logo-swap/perception and final S-32/H-21 call not complete. |
| V-7 | pass | Findings separated from verified behaviour and human-dependent checks. This audit does not ship website changes. |

# Critique: Presence live site — current production preview — major-work audit

Audited https://meetpresence.com on 15 October 2026 (Australia/Sydney), against the supplied [core v2.1](https://github.com/CandidDan/mods/blob/aaf177483c33ae4158d4ecb43d710e7e277ef628/design-standards/skills/design-standards/SKILL.md) and [audit skill](https://github.com/CandidDan/mods/blob/aaf177483c33ae4158d4ecb43d710e7e277ef628/design-standards/skills/design-standards-audit/SKILL.md). Source baseline: `4a5e56c507cff61eb4e308cd690d379febdca27c` (latest main at audit start).

Scope: homepage, `/spaces`, `/spaces/example`, `/privacy`, `/cookies`, `/terms`. Normal/reduced-motion page views and accessibility scans at 1440×1000, 390×844, 320×740. Both marketing entry pages also have mobile Lighthouse samples. Production forms were never submitted. Manual hidden-state checks use a temporary local cloud clone with collection disabled.

## Brief and first impression

I-1: an interested person deciding whether Presence could make an in-person introduction easier; for `/spaces`, a host considering a conversation. Actual reader/task research is still a hypothesis.
I-2: understand the idea and control over sharing/visibility, then choose whether to explore further. Joining a real list is not an available task in this phase; do not grade intentional preview closure as a broken live backend.
I-3: the human invitation plus a clear explanation that sharing an introduction and nearby discoverability are separate choices.
I-4: retain the existing visual system. I-5 clarity wins. I-6 web at desktop/phone. I-8, proposed description of the current character: welcoming, quiet, curious; outside-software reference a small introduction in a welcoming shared place; signature the split reading layout and gently forming/breaking connection. I-9/reader research were not explicitly documented at original creation and are not retroactively claimed as approved.

Verdict: the site has more ownable character than the old PDF, particularly the split reading layout and connection metaphor. Its main weaknesses are accessibility details, dense exploratory language and action labels that still sound like live registration. An entirely new visual direction is not indicated by this audit.

## Findings and proposed fixes

| Finding | ID | Priority | Proposed fix (not implemented here) |
| --- | --- | --- | --- |
| Low-contrast preview status text | S-1 | Required | Use an ink/darker role colour meeting 4.5:1, preserving orange for decorative/accent use. |
| Low-contrast link focus ring and input boundaries | S-2 | Required | Add a tested darker focus/border role. Keep a visibly distinct keyboard outline and verify every surface. |
| Menu/large text overruns phone layout at 200%; narrow text-spacing overflows | S-6 | Required | Allow the header/menu to wrap or stack under enlargement; remove unbreakable content where necessary; test actual text resize and spacing before shipping. |
| No named spacing/type/colour token layer | S-29/S-30 | Required | Map existing visual values into a documented ≤8-spacing/≤7-type-step system and role colours. Avoid changing the brand solely to satisfy house-style palette preferences. |
| “Join the waitlist” / “Register space interest” imply outcomes while buttons only preview a status | S-22, S-21 | High | Make the preview action explicit until actual signup opens, while retaining the honest notice. Confirm the primary homepage job for this phase. |
| Account/privacy readiness language dominates the final consumer paragraph | S-21, V-5 | High | Keep a short clear explanation in the flow and put operational readiness detail on privacy/setup pages. |
| Faux profiles and large phone frames dominate a long page before the CTA | H-17/H-18/V-5 | Medium | Test whether one annotated example is enough, and whether people understand it is illustrative. Preserve useful real-interest context without presenting real partnerships. |
| Topic pills and repeated rounded surfaces can read as generic UI vocabulary | H-20/H-21 | Medium | Log what each element explains. Preserve actual profile topic information, but test whether every pill/frame is necessary for this marketing page. |
| Meaningful choice motif can still compete with reading at some scroll positions | S-32/H-21 | needs Dan | Current connector is already 25% opacity; test reading at a range of scroll positions with people. Don't replace the signature with generic neutral styling. |
| Two-second purpose and next action unknown | S-33/V-3 | needs Dan | Test image-only first view with three humans; compare purpose/next-action answers to the brief. |

## V-2 page verdicts

- Homepage: readable baseline hierarchy and distinct split layout; concept explanation and choice separation are strong. Long illustrations and preview CTA may dilute the first action; enlarged text breaks the narrow header. Connection remains a plausible signature, not proof of real detection.
- Spaces: matches the system and explains participation without events/discounts. Inline example is useful; trial/equipment sections are long. Preview fields are labelled. Same header/text-resize and contrast failures as home.
- Fictional host: clear fiction label and optional conversation context; layout survives narrow, spacing and 200% text tests. Full profile illustration remains a proposed feature, not a venue listing.
- Privacy: readable draft and explicit placeholders; baseline and tested spacing/text resize fit. It remains unfinished for real collection and should not be described as approved.
- Cookies: focused explanation of the essential gate cookie and absence of tracking; tested layouts fit. No unnecessary banner is introduced.
- Preview information: sets expectations honestly; tested layouts fit. Stronger cross-linking than a generic legal contract; no fabricated operational service.

## Evidence and limits

`site-evidence/results.json` records all 18 route/width scans and document-width measurements. `manual.json` records focus/border/message computed styles and the overflowing text navigation element. Full-page/section evidence and keyboard walks were inspected in the cloud; selected screenshots are committed beside this report. The screenshot `home-text200.png` is a 320px viewport with text doubled, not a native phone screen capture.

- Axe-core 4.10.3: all tested default states returned zero violations for selected WCAG 2/2.1/2.2 A/AA tags. This omits unshown status states and does not prove focus contrast or human comprehension.
- Lighthouse 12.8.2: summaries in `lighthouse-home.json` and `lighthouse-spaces.json`; measurements used the actual public URLs with current access state. Chrome/proxy cloud conditions are a lab sample. Image format/sizing and response/dependency diagnostics were also flagged despite passing aggregate thresholds.
- Keyboard walk captured focus order/outline styles; no production input submission. Actual screen-reader usability, forced colours and real-device interaction remain needs Dan.
- Existing `tests/connection_browser.py` and `tests/spaces_browser.py` passed on the unchanged website source at 1440/768/390/320. Synthetic values only on the temporary cloud server. Those gates did not previously cover enlarged text or contrast, which is why this audit adds findings.
- No dark theme exists. V-5 dark-mode review is n.a., not a claimed pass. S-28 app start is n.a. No destructive actions or modals are offered, so S-16/S-17 are n.a.
- S-13 live signup is outside the declared non-collecting phase. S-15/S-18/S-19 API-state behaviour was mocked in earlier signup work; real account behaviour remains unverified. No fresh claim of real provider success is made.
- S-31's full line-length/dense-type compliance needs a separate complete content measurement; default automated scans do not prove it. No blanket typography pass is claimed.
- V-1 exploration belongs to a future major site redesign, not this read-only audit. V-3/V-6 and final major-work S-32/H-21 judgement remain needs Dan.

## Top three follow-on tasks

1. Correct status/focus/border contrast and retest every interactive state.
2. Fix enlarged-text/header/text-spacing behaviour, then extend the regression gate to those conditions.
3. Agree the primary preview action and map existing values to named tokens; simplify readiness copy and log/test the signature's ornaments.

These are findings and proposed work. The site, live forms, account settings and production deployment are unchanged by this audit.
