"""Regression gates for the v2.1 contrast, reflow and preview-label fixes."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
import json
import re
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = Path('/tmp/presence-design-checks')
OUT.mkdir(exist_ok=True)
ROUTES = ['/', '/spaces', '/spaces/example', '/privacy', '/cookies', '/terms']


def contrast(first, second):
    def luminance(colour):
        rgb = [int(x) / 255 for x in re.findall(r'\d+', colour)[:3]]
        linear = [x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4 for x in rgb]
        return sum(x * weight for x, weight in zip(linear, [.2126, .7152, .0722]))
    a, b = sorted([luminance(first), luminance(second)])
    return (b + .05) / (a + .05)


css = (ROOT / 'styles.css').read_text()
assert len(set(re.findall(r'--space-[\w-]+(?=:)', css))) == 8
assert len(set(re.findall(r'--type-[\w-]+(?=:)', css))) == 7
# Component spacing/type must use named roles; geometry (radii/widths) is separate.
for match in re.finditer(r'(?<![\w-])(padding(?:-[a-z]+)?|margin(?:-[a-z]+)?|gap|font-size):\s*([^;}]+)', css):
    assert not re.search(r'\d(?:px|rem|vh|vw)', match[2]), match[0]


class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=str(ROOT)))
Thread(target=server.serve_forever, daemon=True).start()
base = f'http://127.0.0.1:{server.server_port}'
results = []
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
        page = browser.new_page(reduced_motion='reduce')
        for route in ROUTES:
            for width in [1440, 390, 320]:
                page.set_viewport_size({'width': width, 'height': 1000 if width == 1440 else 844})
                for mode in ['normal', 'text-spacing', 'text200']:
                    page.goto(base + route, wait_until='networkidle')
                    assert page.evaluate("async () => {await document.fonts.ready; return [300,400,500].every(w => document.fonts.check(w + ' 16px Outfit'))}")
                    if mode == 'text-spacing':
                        page.add_style_tag(content='*{line-height:1.5!important;letter-spacing:.12em!important;word-spacing:.16em!important}p{margin-bottom:2em!important}')
                    if mode == 'text200':
                        # Snapshot first: nested inheritance must not multiply repeatedly.
                        page.evaluate('''() => {
                          const items = [...document.querySelectorAll('body *')]
                            .filter(e => !e.closest('svg') && !['SCRIPT','STYLE'].includes(e.tagName))
                            .map(e => ({e, size:parseFloat(getComputedStyle(e).fontSize), line:parseFloat(getComputedStyle(e).lineHeight)}));
                          items.forEach(({e,size,line}) => {e.style.fontSize=size*2+'px';if(!isNaN(line))e.style.lineHeight=line*2+'px'});
                        }''')
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (route, width, mode)
                    if route in ['/', '/spaces'] and mode != 'normal':
                        for selector in ['.left-top', '.site-nav', 'form button', 'form input[type=email]']:
                            rect = page.locator(selector).bounding_box()
                            assert rect['x'] >= 0 and rect['x'] + rect['width'] <= width + 1, (route, width, mode, selector)
                    results.append({'route':route, 'width':width, 'mode':mode, 'reflow':'pass'})
                    if route in ['/', '/spaces'] and width in [1440, 320] and mode != 'text-spacing':
                        name = 'home' if route == '/' else 'spaces'
                        page.screenshot(path=str(OUT / f'{name}-{width}-{mode}.png'), full_page=True)
        page.set_viewport_size({'width':1440,'height':1000})
        ratios = []
        for route in ['/', '/spaces']:
            page.goto(base + route, wait_until='networkidle')
            assert page.locator('form button').inner_text() == 'Try the form preview'
            page.keyboard.press('Tab')
            assert page.locator('.skip').evaluate('e => e === document.activeElement')
            page.locator('.site-nav a').focus()
            focus = page.locator('.site-nav a').evaluate('e => getComputedStyle(e).outlineColor')
            ground = page.locator('body').evaluate('e => getComputedStyle(e).backgroundColor')
            edge = page.locator('input[type=email]').evaluate('e => [getComputedStyle(e).borderColor,getComputedStyle(e).backgroundColor]')
            requests = []
            page.on('request', lambda r: requests.append(r.url))
            page.locator('form button').click()
            status = page.locator('form [role=status]')
            assert status.is_visible() and 'nothing was sent or stored' in status.inner_text()
            assert status.evaluate('e => e === document.activeElement')
            text = status.evaluate('e => getComputedStyle(e).color')
            values = {'route':route,'focus':contrast(focus,ground),'edge':contrast(*edge),'status':contrast(text,ground)}
            assert values['focus'] >= 3 and values['edge'] >= 3 and values['status'] >= 4.5, values
            assert not requests
            ratios.append(values)
        browser.close()
    (OUT / 'results.json').write_text(json.dumps({'reflow':results,'contrast':ratios},indent=2))
    print('PASS: 54 route/width/text-mode checks; 320px reflow and 200% text; eight spacing and seven type tokens')
    print('PASS: honest non-collecting buttons, keyboard status focus; contrast ratios:', json.dumps(ratios))
    print('Evidence:', OUT)
finally:
    server.shutdown()
