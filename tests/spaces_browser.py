"""Cloud gates for spaces routing, split layout and non-collecting previews."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.request import urlopen
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SHOTS = Path('/tmp/presence-spaces-split')
SHOTS.mkdir(exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass
server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=str(ROOT)))
Thread(target=server.serve_forever, daemon=True).start()
base = 'http://127.0.0.1:' + str(server.server_port)
try:
    for route in ['/', '/spaces', '/spaces/', '/spaces/example', '/spaces/example/', '/styles.css', '/field.js', '/preview.js']:
        with urlopen(base + route) as response:
            assert response.status == 200
            assert response.read()
    print('PASS: direct spaces routes and shared assets')
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
        for label, width, height in [('desktop', 1440, 1000), ('tablet', 768, 1024), ('mobile', 390, 844), ('narrow', 320, 740)]:
            context = browser.new_context(viewport={'width': width, 'height': height}, reduced_motion='reduce')
            page = context.new_page()
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            for route in ['/', '/spaces']:
                page.goto(base + route, wait_until='networkidle')
                assert page.locator('h1').count() == 1
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
                assert page.locator('#field .target-halo').count() == 1
                assert page.locator('.left').evaluate("e => getComputedStyle(e).position") == ('sticky' if width >= 1024 else 'relative')
                for el in page.locator('[aria-labelledby], [aria-describedby]').all():
                    for attr in ['aria-labelledby', 'aria-describedby']:
                        for target in (el.get_attribute(attr) or '').split():
                            assert page.locator('#' + target).count() == 1
                for field in page.locator('form input').all():
                    assert page.locator('label[for="' + field.get_attribute('id') + '"]').count() == 1
                if route == '/spaces':
                    assert page.locator('form input').count() == 7
                    assert page.locator('.trial-steps > li').count() == 3
                    assert 'proposed feature' in page.locator('[aria-labelledby="space-page-h"] .small').inner_text()
                page.keyboard.press('Tab')
                assert page.locator('.skip').evaluate('e => document.activeElement === e')
                page.keyboard.press('Enter')
                assert page.url.endswith('#main' if route == '/spaces' else '#waitlist')
                page.goto(base + route, wait_until='networkidle')
                if label in ['desktop', 'mobile']:
                    page.screenshot(path=str(SHOTS / (('spaces' if route == '/spaces' else 'home') + '-' + label + '.png')), full_page=True)
                requests = []
                form = page.locator('form')
                message = form.locator('[role="status"]')
                assert message.is_hidden()
                for field in form.locator('input').all():
                    kind = field.get_attribute('type')
                    if kind == 'checkbox':
                        field.check()
                    else:
                        field.fill('test@example.invalid' if kind == 'email' else 'https://example.invalid' if kind == 'url' else 'Test space')
                page.on('request', lambda request: requests.append(request.url))
                form.locator('button').focus()
                page.keyboard.press('Enter')
                assert message.is_visible()
                assert 'nothing was sent or stored' in message.inner_text()
                assert message.evaluate('e => document.activeElement === e')
                form.locator('input[type="email"]').press('Enter')
                page.wait_for_timeout(100)
                assert not requests
                assert page.evaluate('localStorage.length === 0 && sessionStorage.length === 0')
                assert not context.cookies()
                assert not errors, errors
            page.goto(base, wait_until='networkidle')
            page.locator('nav a[href="/spaces"]').click()
            assert 'A place to say' in page.locator('h1').inner_text()
            page.locator('.left-cta a').click()
            assert page.url.endswith('#space-interest')
            page.locator('nav a[href="/"]').click()
            assert 'A reason to say' in page.locator('h1').inner_text()
            page.locator('.spaces-invitation a').click()
            assert page.locator('#participation-h').is_visible()
            assert 'small and discreet' in page.locator('.trial-equipment').inner_text()
            page.locator('.example-link').click()
            assert page.locator('#host-name').inner_text() == 'Common Ground'
            assert 'Fictional example' in page.locator('.host-example-note').inner_text()
            assert page.locator('form').count() == 0
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
            assert page.locator('meta[name="robots"]').get_attribute('content') == 'noindex, nofollow'
            assert page.locator('.host-details a').get_attribute('href') == 'https://example.com'
            page.keyboard.press('Tab')
            # Start a fresh navigation to test the example's own skip link.
            page.goto(base + '/spaces/example', wait_until='networkidle')
            page.keyboard.press('Tab')
            assert page.locator('.skip').evaluate('e => document.activeElement === e')
            page.keyboard.press('Enter')
            assert page.url.endswith('#host-main')
            for link, target in [('.host-nav a[href="#about-space"]', '#about-space'), ('.host-nav a[href="#conversation"]', '#conversation'), ('.host-nav a[href="#visit-space"]', '#visit-space')]:
                page.locator(link).click()
                assert page.url.endswith(target)
            page.goto(base + '/spaces/example/', wait_until='networkidle')
            if label in ['desktop', 'mobile']:
                page.screenshot(path=str(SHOTS / ('host-' + label + '.png')), full_page=True)
            page.locator('header a[href="/spaces"]').click()
            assert page.locator('#participation-h').is_visible()
            assert not errors, errors
            print('PASS:', label, 'split layout, discreet equipment, example host page/navigation, labels and non-collecting forms')
            context.close()
        context = browser.new_context(java_script_enabled=False)
        page = context.new_page()
        for route in ['/', '/spaces']:
            page.goto(base + route, wait_until='networkidle')
            assert page.locator('form button').is_disabled()
            assert page.locator('noscript').is_visible()
            requests = []
            page.on('request', lambda request: requests.append(request.url))
            page.locator('input[type="email"]').fill('test@example.invalid')
            page.locator('input[type="email"]').press('Enter')
            page.wait_for_timeout(100)
            assert not requests
            assert '?' not in page.url
        print('PASS: both previews cannot submit with JavaScript disabled')
        browser.close()
finally:
    server.shutdown()
print('Screenshots:', SHOTS)
