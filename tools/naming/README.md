# Related words: recovered Naming workbench

Temporary exploration preview, recovered from the 15 October conversation
“Explore a visual naming tool with clash checks”. This is a separate tool;
it is not linked from Presence's consumer pages and should not be merged into
production as a product feature.

Open `/tools/naming/?word=connection` to start the Presence exploration.
`index.html` is a portable, self-contained copy: no build, account or new backend.
It uses the existing deployment access gate, if configured; no gate settings change.

- Space, Work and Perch maps are recovered from the original source.
- Screenshot routes are reconstructed from the original exported naming paths;
  they are not a byte-for-byte recovery of the older full screenshot map.
- Other words query Datamuse for meaning, association, sound and spelling.
  Only the lookup word is sent; the interface discloses this.
- Notes and shortlists use local browser storage on this preview's origin.
  This does not import data from the original Mac file or Brand Workshop.
- Export/import backs up or transfers the workspace. Research links are searches,
  not automatic clash checks or trademark clearance.

Recovery includes the original recorded fixes for context, stale requests and
prototype-name lookup. A redacted request-counter line was repaired, and long
imported names now wrap on narrow screens. The optional `word` query parameter
starts a new exploration with the agreed consumer-brand context.

Cloud verification: `python3 tests/naming_browser.py`. Tests use synthetic notes
only against a temporary static server, including real browser export/import.
