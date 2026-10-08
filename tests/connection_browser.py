"""Cloud Chromium regression gate for the scroll-driven connection field."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
import math
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SHOTS = Path('/tmp/presence-connection-checks')
SHOTS.mkdir(exist_ok=True)

class QuietServer(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietServer, directory=str(ROOT)))
Thread(target=server.serve_forever, daemon=True).start()
base = 'http://127.0.0.1:' + str(server.server_port)

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
        for label, width, height in [('desktop', 1440, 1000), ('tablet', 768, 1024), ('mobile', 390, 844), ('narrow', 320, 740)]:
            context = browser.new_context(viewport={'width': width, 'height': height})
            page = context.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.goto(base, wait_until='networkidle')
            page.evaluate("document.documentElement.style.scrollBehavior = 'auto'")
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
            count = min(7, page.locator('#field .p').count())
            assert count >= 2
            maximum = page.evaluate('document.documentElement.scrollHeight - innerHeight')

            def scroll_phase(phase):
                y = maximum * (phase - .5) / (count - 1)
                page.evaluate('(y) => scrollTo(0, y)', y)
                page.wait_for_timeout(1100)
                assert abs(page.evaluate('scrollY') - y) <= 1, 'illustration must not snap page scroll'

            # One person holds across two separated positions, exactly at their centre.
            scroll_phase(1.3)
            node = page.locator('#field .p.on')
            assert node.count() == 1
            first = (node.get_attribute('cx'), node.get_attribute('cy'))
            path = page.locator('#field .ln').evaluate('(p) => { const end=p.getPointAtLength(p.getTotalLength()); return [end.x,end.y]; }')
            assert math.dist(path, tuple(map(float, first))) < .1
            page.screenshot(path=str(SHOTS / (label + '-connected.png')))
            scroll_phase(1.7)
            assert (node.get_attribute('cx'), node.get_attribute('cy')) == first
            # It withdraws and reaches a different person, forwards and backwards.
            scroll_phase(1.9)
            assert page.locator('#field .p.on').count() == 0
            scroll_phase(2.3)
            second = (node.get_attribute('cx'), node.get_attribute('cy'))
            assert second != first
            scroll_phase(1.3)
            assert (node.get_attribute('cx'), node.get_attribute('cy')) == first

            # Changing preferences while open must cancel pulses and freeze geometry.
            page.emulate_media(reduced_motion='reduce')
            page.wait_for_function("document.querySelector('#field').dataset.reducedMotion === 'true'")
            frozen = page.locator('#field').inner_html()
            style = page.locator('#field').get_attribute('style')
            page.evaluate('scrollTo(0, 0)')
            page.wait_for_timeout(150)
            assert page.locator('#field').inner_html() == frozen
            assert page.locator('#field').get_attribute('style') == style
            assert page.locator('#field').evaluate('(e) => e.getAnimations({subtree:true}).length') == 0
            page.emulate_media(reduced_motion='no-preference')
            page.wait_for_function("document.querySelector('#field').dataset.reducedMotion === 'false'")
            scroll_phase(2.3)
            assert page.locator('#field .p.on').count() == 1
            page.emulate_media(reduced_motion='reduce')
            page.wait_for_function("document.querySelector('#field').dataset.reducedMotion === 'true'")
            page.reload(wait_until='networkidle')
            assert page.locator('#field').get_attribute('data-reduced-motion') == 'true'
            frozen = page.locator('#field').inner_html()
            page.locator('.left-cta a').click()
            assert page.url.endswith('#waitlist')
            assert page.locator('#field').inner_html() == frozen
            assert page.locator('#field').evaluate('(e) => e.getAnimations({subtree:true}).length') == 0
            # Local synthetic submission must still be the non-collecting preview.
            page.locator('#email').fill('test@example.invalid')
            requests = []
            page.on('request', lambda req: requests.append(req.url))
            page.locator('#interest button').click()
            assert page.locator('#form-msg').is_visible()
            assert page.locator('#form-msg').evaluate('(e) => document.activeElement === e')
            assert 'nothing was sent or stored' in page.locator('#form-msg').inner_text()
            assert not requests
            assert page.evaluate('localStorage.length === 0 && sessionStorage.length === 0')
            assert not errors, errors
            print('PASS:', label, 'hold, exact endpoint, forward/reverse, natural scroll, static reduced motion, navigation and non-collecting form')
            context.close()

        for variant in ['thread', 'ripple']:
            page = browser.new_page()
            page.goto(base + '/?v=' + variant, wait_until='networkidle')
            assert page.locator('#field .p.on').count() == 1
            assert page.locator('#field .wave').count() == (2 if variant == 'ripple' else 0)
            assert page.locator('#field .ln').count() == (1 if variant == 'thread' else 0)
            page.emulate_media(reduced_motion='reduce')
            page.wait_for_function("document.querySelector('#field').dataset.reducedMotion === 'true'")
            frozen = page.locator('#field').inner_html()
            page.evaluate('scrollTo(0, 500)')
            page.wait_for_timeout(150)
            assert page.locator('#field').inner_html() == frozen
            print('PASS:', variant, 'switch and static reduced motion')
            page.close()
        browser.close()
finally:
    server.shutdown()
print('Screenshots:', SHOTS)
