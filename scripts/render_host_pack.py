"""Render the static host-pack template with bundled assets; no external network or services."""
import argparse
import html
import json
from pathlib import Path
from string import Template
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
import mimetypes
import base64
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'docs/host-pack'
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--edition', type=Path, default=PACK / 'edition.json', help='Edition JSON; photo paths are relative to its directory')
parser.add_argument('--output', type=Path, default=ROOT / 'assets/presence-for-spaces.pdf')
parser.add_argument('--screenshots', type=Path, help='Optional directory for page screenshots')
args = parser.parse_args()
edition_path = args.edition.resolve()
values = json.loads(edition_path.read_text())
assets = {}
for key in ['cover_photo', 'context_photo']:
    asset = (edition_path.parent / values[key]).resolve()
    if not asset.is_file():
        raise FileNotFoundError(asset)
    assets[key] = asset
assets.update(mark=ROOT / 'mark.svg', example_art=ROOT / 'assets/example-space.svg')
for weight in [300, 400, 500]:
    assets['font_' + str(weight)] = PACK / f'assets/outfit-{weight}.ttf'
class AssetServer(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass
    def do_GET(self):
        asset = assets.get(self.path.lstrip('/'))
        if asset is None:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', mimetypes.guess_type(str(asset))[0] or 'application/octet-stream')
        self.end_headers()
        self.wfile.write(asset.read_bytes())

server = ThreadingHTTPServer(('127.0.0.1', 0), AssetServer)
Thread(target=server.serve_forever, daemon=True).start()
base = f'http://127.0.0.1:{server.server_port}'
for key in assets:
    values[key] = base + '/' + key
rendered = Template((PACK / 'pack.html').read_text()).substitute({k: html.escape(v, quote=True) for k, v in values.items()})
args.output.parent.mkdir(parents=True, exist_ok=True)
if args.screenshots:
    args.screenshots.mkdir(parents=True, exist_ok=True)
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
        page = browser.new_page(viewport={'width': 794, 'height': 1123})
        # A pack should render reproducibly with no external network requests.
        page.route('**/*', lambda route: route.continue_() if route.request.url.startswith(base + '/') else route.abort())
        page.set_content(rendered, wait_until='load')
        page.emulate_media(media='print')
        page.evaluate('document.fonts.ready')
        assert page.evaluate('Array.from(document.fonts).every(f => f.status === "loaded")'), 'Bundled fonts did not load'
        assert page.locator('.page').count() == 4
        assert page.evaluate('Array.from(document.images).every(i => i.complete && i.naturalWidth > 0)')
        for i, sheet in enumerate(page.locator('.page').all(), 1):
            if args.screenshots:
                sheet.screenshot(path=str(args.screenshots / f'page-{i}.png'))
            # Fixed page layouts must fit before a PDF can be shared.
            assert sheet.evaluate('e => e.scrollHeight <= e.clientHeight && e.scrollWidth <= e.clientWidth'), f'Overflow on page {i}'
            footer_top = sheet.locator('.footer').bounding_box()['y']
            for child in sheet.locator(':scope > *:not(.footer)').all():
                box = child.bounding_box()
                assert box['y'] + box['height'] < footer_top, f'Content overlaps footer on page {i}'
        session = page.context.new_cdp_session(page)
        pdf = session.send('Page.printToPDF', {'printBackground': True, 'preferCSSPageSize': True, 'generateTaggedPDF': True, 'generateDocumentOutline': True})
        args.output.write_bytes(base64.b64decode(pdf['data']))
        browser.close()
finally:
    server.shutdown()
print(args.output)
