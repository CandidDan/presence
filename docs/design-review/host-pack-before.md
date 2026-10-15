| ID | Status | Evidence |
| --- | --- | --- |
| V-7 | pass | This report opens with the evidence ledger and distinguishes findings from unperformed human checks. No design is changed or shipped by this audit. |
| S-1 | pass | RGB contrast: body 16.06:1; captions 4.90:1; large orange numbers 3.51:1. Actual PDF text spans and backgrounds inspected. Physical print reproduction still needs Dan. |
| S-11 / S-26 | pass | Meaning is expressed in text; Common Ground is labelled fictional and photographs illustrative. No claimed trial results or fabricated testimonials. |
| S-32 | fail | Page 2 labels visitor/space/trial categories 01/02/03, which are not a chronological sequence. The rule explicitly reserves this numbering for real sequences. |
| S-21 | fail | For the static screen-reading use, “approved privacy configuration” is internal vocabulary in a host-facing document. Rewrite as concrete privacy arrangements and visitor choices. |
| S-33 / V-3 | needs Dan | No controlled image-only two-second test with three humans. The friend's AI reaction is useful feedback, not evidence of passing/failing the defined purpose test. |
| H-18 / H-20 | fail | Broad stock interiors, general copy and no named sender offer little real human context. ALL-CAPS eyebrows, a coloured left-border callout and repeated polished fragments are listed tells. |
| V-2 | pass | All four pages inspected at full-page rendering and phone fit-to-page size; page-by-page craft verdicts below. |
| V-5 | fail | Reviewer logo-swap assessment: most of the pack could serve another community/connection product with small name/copy substitutions. The logo/motif is visible but the page structure and voice are not sufficiently ownable. Top three changes are logged below. Final major-work ornament judgement needs Dan. |
| V-1 / V-6 | needs Dan | No evidence of two explored directions, one deliberately excessive, or three representative task sessions. These must be completed for a major redesign; they cannot be retroactively claimed from this audit. |
| V-4 | pass | Agent-applicable static checks completed: actual text colours/sizes inspected, contrast computed, four-page fit viewed. Web/app procedures are outside this PDF audit. PDF tags/outline exist, but screen-reader usability is not proved. |

# Critique: Presence host pack — existing published draft — major redesign scope

**Verdict:** recognisable brand and careful product boundaries; a generic brochure structure and abstract voice weaken the invitation. **Eye lands on:** “A reason to say hello.” **I-3:** communicates connection broadly, but whether a host understands the proposal/next step within two seconds needs a human test. **Signature visible:** a small connection motif, with limited transfer into the content/layout. **Logo-swap:** fail, reviewer assessment.

This audit uses both requested skills, not the earlier preliminary assessment alone:

- [Core v2.1](https://github.com/CandidDan/mods/blob/aaf177483c33ae4158d4ecb43d710e7e277ef628/design-standards/skills/design-standards/SKILL.md)
- [Audit detail v2.1](https://github.com/CandidDan/mods/blob/aaf177483c33ae4158d4ecb43d710e7e277ef628/design-standards/skills/design-standards-audit/SKILL.md)

The skills' Claude source-of-truth URL returned an artifact wrapper without the rule text or a visible version. No newer version was observed; this report is specifically against the supplied GitHub v2.1 text.

## Reviewed artifact and scope

The live four-page PDF from https://meetpresence.com/assets/presence-for-spaces.pdf was downloaded on 14 October 2026 and matches the repository PDF byte-for-byte.
SHA-256: `9eae5548e3557862366e055e8c034a86181e9ab777cc1fedac3ec0063bcb796c`.

Platforms: **P**, A4 print/handout; **S**, static screen viewing of the same document. This is not an HTML email or interactive web-page audit. Its original creation introduced a new document layout; a structural redesign calls for the major workflow. A tiny copy correction alone could be trivial, but it would not resolve the character/intent findings.

The review does not determine AI authorship from appearance. The issue is whether the pack communicates a specific, considered proposition with real human context.

## Brief reconstruction — hypotheses, not an approved new brief

- **I-1:** a café/coworking host considering an unfamiliar proposal, possibly reading a forwarded PDF on a phone. The exact reader and moment still need confirmation.
- **I-2:** decide whether an initial conversation about a small Presence trial is worth their time.
- **I-3, proposed:** understand what Presence would do for visitors and what the host would be asked to do. A branded headline alone is insufficient evidence that this happens.
- **I-4:** inherit Presence's existing palette, mark and softer type. Preserve the distinction between sharing an introduction and optional nearby visibility.
- **I-5:** clarity should win ties for this introductory host handout.
- **I-6:** A4 PDF, also read on screens. A phone-first companion could be considered if an A4 handout remains impractical to read without zooming.
- **I-7:** unverified assumption: hosts see enough potential benefit to spend time discussing a trial. Test with representative hosts, rather than treating a friend's appearance reaction as a full task session.
- **I-8 / I-9:** no explicit character/risk brief was found for the pack. These should be agreed before redesign. Proposed starting point: warm, observant, direct; outside-software reference: the small introductions and notes around a neighbourhood café's shared table. Develop a signature that links a specific topic to a possible conversation using Presence's connection language. The deliberate risk could be opening with one clearly illustrative visitor moment, making the mechanism concrete immediately. This is a proposed direction, not a claim that it is already built or tested.

## Findings

| Finding | ID | Severity | Fix |
| --- | --- | --- | --- |
| Page 2's 01/02/03 denote categories, not steps | S-32 | Ship blocker under v2.1 | Remove numbers from these categories. Use numbering only for an actual sequence, such as introduction, visitor choice, feedback. |
| Generic structure/voice can largely survive a brand swap | I-8, I-9, V-5 | Structural | Rebrief the pack around its specific reader, first takeaway and ownable signature, then restructure. Whitespace or colour tweaks alone will not address this. |
| Repeated balanced slogans and ALL-CAPS eyebrows read like a reusable pitch template | H-20 | High | Replace each tell with purposeful voice/hierarchy tied to I-8. Keep the established “A reason to say hello” line; reduce new generic slogans. |
| Stock interiors convey mood but no specific host insight | H-18, H-21 | High | For a tailored edition, use permissioned real-space images with informative captions. If that content is unavailable, use one honestly labelled stock image or informative illustration; do not invent partnerships or testimonials. |
| Practical host expectations are compressed beneath a large phone mockup on page 3 | I-2, I-3, V-5 hierarchy/usability | High | Elevate “What we'd ask of you”, proposed Presence support and unresolved technology/trial terms. Annotate a smaller example at the moment it explains the choice visitors make. |
| “Approved privacy configuration” asks a host to interpret internal terminology | S-21 (S), V-5 | High | Explain plainly whose details would be used, for what, who handles questions and what must be settled before a trial. Keep honest limitations. |
| Closing gives no named person or direct contact, despite asking for a conversation | I-2, H-18, V-5 | High | Use a real approved sender and one monitored contact/next action. `hello@meetpresence.com` is configured according to the user; a named person's sign-off still needs that person's approval. |
| Grey rounded notes and the orange left-border closing are reusable treatments | H-12, H-20, H-21 | Medium | Integrate constraints and next action into a deliberate hierarchy. Log why any remaining callout/ornament carries information or builds the signature. |
| Page 3's 9–10pt practical copy and 8pt captions are difficult at phone fit-to-page size | V-5 phone usability | Medium | Shorten and reprioritise the content, then test a phone reading task. Do not falsely cite S-31's web/email font floor as a print/PDF violation. |

## V-2: page-by-page craft verdicts

| Page | Spacing, typography, contrast, alignment, fit, repetition |
| --- | --- |
| 1 | Consistent alignment and generous spacing; good contrast and large headline; fits. Several abstract introductory phrases precede a concrete explanation. Stock image is attractive but unconnected to a particular host. |
| 2 | Clear row alignment and readable body at print size; good contrast; fits. Three parallel categories and numbering imply a sequence that does not exist. The headline and photo reinforce atmosphere more than understanding. |
| 3 | Overall grid fits and contrast is strong; practical text becomes dense beside/below the mockup. Phone viewing requires zoom for the important operational details. Repeated three-part headings amplify the formulaic voice. |
| 4 | Clear question list and strong contrast; fits with considerable whitespace. Another large general headline, readiness callout and generic closing repeat the brochure pattern. The final instruction delegates the human connection to an unspecified sender. |

## Contrast and typography evidence

Measured foreground/background pairs used by the document:

| Use | Pair | Ratio | S-1 |
| --- | --- | --- | --- |
| Main text | #1B1A19 / #F6F6F4 | 16.06:1 | pass |
| Muted captions/footer | #6E6B67 / #F6F6F4 | 4.90:1 | pass |
| Page 2 numbers, 18pt normal = 24 CSS px | #B9731F / #F6F6F4 | 3.51:1 | pass at large-text threshold of 3:1 |
| Note text | #1B1A19 / #ECEBE7 | 14.57:1 | pass |

Actual extracted PDF sizes include 48pt cover, 34pt headings, 15pt introductions, 11pt main body, 9–10pt page 3 detail and approximately 8pt captions/footer. The skills' S-29/S-30/S-31 token and size requirements apply to W/A/E, not P/S, so they are not failed here. Printed contrast on the intended stock and viewing distance remain **needs Dan**. The poster-style three-metre check should not be used as a body-reading criterion for a desk-read A4 handout.

The PDF has searchable text, a marked structure tree and an outline; it contains no forms. Link annotations lead to the existing spaces site and the Unsplash licence. Those are useful construction facts, not proof of a successful screen-reader reading order or user journey.

## Ornament inventory — retrospective reviewer assessment

No builder's H-21 ornament log was found. This is a review inventory, not a fabricated original log.

| Element | Job / judgement |
| --- | --- |
| Cover connection motif | Carries the established connection metaphor; reasonable to retain. Its role could become more informative if linked to the visitor scenario. Final major-work S-32/H-21 judgement needs Dan. |
| Page 2 category numbers | Present categories as steps: S-32 fail. Remove or repurpose for a genuine sequence. |
| Section hairlines | Group related information; not automatically an anti-default violation. Check whether each divider remains necessary after restructuring. |
| Fictional phone frame | Demonstrates a proposed space page; information-bearing, but disproportionately prominent relative to the host's practical job. |
| Rounded topic tags | Explain example interests. Because they inherit the site's profile component and are inside a labelled example, they are not an automatic demand to redesign the product component. Review their prominence and H-20 tell in context. |
| Rounded shaded constraint notes | Group important caveats, but repeated generic surface treatment weakens hierarchy. Keep only if the new structure needs it. |
| Orange left-border closing | Explicit H-20 tell with no unique informational function established. Replace with a clearer ownable invitation treatment. |
| ALL-CAPS eyebrows | Explicit H-20 tell. Rework within the inherited type system so navigation/context has a useful hierarchy without the repeated template signal. |

## What passes / what to preserve

- Honest fictional/illustrative labelling, optional visibility and no commercial or detection promises.
- Existing Presence brand: mark, restrained type, established line/motif and tagline.
- Strong measured text contrast and no clipping in the inspected artifact.
- Searchable/tagged PDF construction and image credits.

**Palette nuance:** H-8/H-10 discourage default cream/orange combinations, but the skill's precedence places the existing brand/system above H. A rebrand is not required to fix this PDF. Keep the inherited palette unless a considered redesign brief calls for a change; all S requirements still apply.

## Top three changes — logged for the next iteration

1. Rebrief and restructure around a concrete visitor moment and an immediately understandable host proposition (I-1–I-3, I-8–I-9, V-5).
2. Bring practical expectations/support/open questions forward; remove the misleading category numbering and internal vocabulary (S-32, S-21, V-5).
3. Introduce approved real human content: named sender/contact, relevant space context or permissioned photographs; replace H-20 tells with that character (H-18, H-20, H-21).

## Applicability and outstanding checks

Web/app-only checks are n.a. for this artifact: S-0, S-2–S-10, S-13, S-15–S-20, S-27–S-30. S-14/S-22/S-23/S-25/S-31 are W/A/E and n.a. to the static P/S pack; the clarity of its next action is still judged under I-2/V-5. S-12 is n.a. for print and pass for the static screen artifact (no motion/audio). S-24 is pass for screen content (no coercion, urgency or hidden commitment). S-11/S-26 are pass as documented above.

Human checks remain **needs Dan**: V-3/S-33 with three humans; V-6 with representative hosts; print/stock inspection; phone reading on a real device; PDF screen-reader reading order if accessible PDF distribution is in scope; final major-work S-32/H-21 ornament judgement. No dark-mode edition exists, so V-5's dark-mode review is n.a., not a passed dark-mode design.

**v2.1 readiness verdict:** the existing pack does not pass the requested standard. Its objective S-32 failure and editorial/character findings should be resolved before a revised version is treated as ready. The PDF and production site are unchanged by this review.
