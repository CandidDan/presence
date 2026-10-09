# Host conversation pack

A four-page starter PDF for a first conversation with cafés, coworking spaces and other welcoming places. It explains the purpose, hoped-for benefits, proposed participation and unresolved questions. It makes no performance, revenue, hardware or equipment-funding promises. Current interest forms remain non-collecting.

Source: `pack.html` (content/layout), `edition.json` (audience, introduction, photography/captions), `assets/` (licensed stock images and bundled fonts). Output: `../../assets/presence-for-spaces.pdf`. Page images in `review/` are review artifacts, not photographs of trial participants.

From the repository root:

```sh
python3 scripts/render_host_pack.py --screenshots docs/host-pack/review
```

Requires Python Playwright and `/usr/bin/chromium`, already available in the prepared cloud environment. This is a document-generation tool; the static site needs no build step. It serves only selected local assets to cloud Chromium, blocks external requests, verifies fonts/images, checks four-page layout and footer clearance, then prints a tagged PDF with an outline.

## A tailored edition

Copy `edition.json` into a folder for the space. Update audience/intro and provide permissioned images relevant to the actual setting. Image paths are relative to that JSON file (absolute paths also work). Update alt text, captions and credits too. Be clear whether the images show that space or are illustrative. Use your own output filename; do not overwrite the generic site pack with one host's edition.

```sh
python3 scripts/render_host_pack.py --edition /tmp/example-space/edition.json --output /tmp/example-space/presence-host-pack.pdf --screenshots /tmp/example-space/review
```

Check the rendered pages before sharing: longer copy and different crops may need template adjustments. Source/permission details belong beside each edition. Never imply trial participation from a photo or tailored title.

Manual editing/rendering is supported. No contact collection, registration trigger, personalised email or automatic distribution is implemented. The PDF links to the existing spaces preview; `meetpresence.com` has not been connected by this change.

See [asset sources and licences](assets/SOURCES.md). The stock edition can be shared under the recorded licences; creator attribution can be improved when photo-detail pages are accessible.
