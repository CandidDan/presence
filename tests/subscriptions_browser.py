"""Cloud signup gates: real API requests are always intercepted; no email is sent."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
import json
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SHOTS = Path('/tmp/presence-signup-review')
SHOTS.mkdir(exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass
server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=str(ROOT)))
Thread(target=server.serve_forever, daemon=True).start()
base = f'http://127.0.0.1:{server.server_port}'
CONFIG = dict(enabled=True, companyId='TEST01', lists=dict(people='PEOPLE', spaces='SPACES'),
              allowedHosts=['127.0.0.1'], privacyApproved=True, doubleOptInVerified=True,
              emailTrackingDisabled=True, consentVersion='presence-updates-v1')

def fill(form, kind):
    form.locator('input[type="email"]').fill('test@example.invalid')
    if kind == 'spaces':
        for name, value in [('contact-name', 'Test contact'), ('space-name', 'Test space'),
                            ('space-town', 'Test town'), ('space-country', 'Test country'),
                            ('space-type', 'Café'), ('space-link', 'https://example.invalid')]:
            form.locator('[name="' + name + '"]').fill(value)
    else:
        form.locator('[name="town"]').fill('Test town')
        form.locator('[name="country"]').fill('Test country')

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='/usr/bin/chromium', args=['--no-sandbox'])
        for label, width, height in [('desktop', 1440, 1000), ('tablet', 768, 1024), ('mobile', 390, 844), ('narrow', 320, 740)]:
            context = browser.new_context(viewport=dict(width=width, height=height), reduced_motion='reduce')
            calls = []
            context.route('https://a.klaviyo.com/**', lambda route: (calls.append(route.request), route.abort()))
            page = context.new_page()
            external = []
            page.on('request', lambda r: external.append(r.url) if not r.url.startswith(base) else None)
            for route in ['/privacy', '/cookies', '/terms']:
                page.goto(base + route, wait_until='networkidle')
                assert page.locator('h1').count() == 1
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
                for item in page.locator('[aria-labelledby]').all():
                    assert page.locator('#' + item.get_attribute('aria-labelledby')).count() == 1
                page.keyboard.press('Tab')
                assert page.locator('.skip').evaluate('e => e === document.activeElement')
                page.keyboard.press('Enter')
                assert page.url.endswith('#main')
                if label in ['desktop', 'mobile']:
                    page.evaluate('document.activeElement.blur()')
                    page.screenshot(path=str(SHOTS / (route.strip('/') + '-' + label + '.png')), full_page=True)
            for route in ['/', '/spaces']:
                page.goto(base + route, wait_until='networkidle')
                form = page.locator('form')
                assert not form.locator('[data-email-consent]').is_checked()
                form.locator('input[type="email"]').fill('test@example.invalid')
                form.locator('button').click()
                assert 'nothing was sent or stored' in form.locator('[role="status"]').inner_text()
                assert page.locator('.legal-nav a[href="/privacy"]').count() == 1
            assert not calls and not external
            assert page.evaluate('localStorage.length === 0 && sessionStorage.length === 0')
            context.close()
            print('PASS:', label, 'legal routes, keyboard access, overflow, local fonts, no external calls and disabled signup')

        # Incomplete settings must never cause a submission, even if enabled is set.
        for change in [dict(privacyApproved=False), dict(doubleOptInVerified=False),
                       dict(emailTrackingDisabled=False), dict(allowedHosts=['example.invalid']),
                       dict(lists=dict(people='PEOPLE', spaces='PEOPLE')), dict(companyId='')]:
            context = browser.new_context()
            settings = {**CONFIG, **change}
            context.add_init_script('window.PRESENCE_SIGNUP_CONFIG = ' + json.dumps(settings))
            calls = []
            context.route('https://a.klaviyo.com/**', lambda route: (calls.append(route.request), route.abort()))
            page = context.new_page()
            page.goto(base, wait_until='networkidle')
            page.locator('form button').click()
            assert 'nothing was sent or stored' in page.locator('form [role="status"]').inner_text()
            assert not calls
            context.close()
        print('PASS: incomplete configuration and unapproved hosts fail closed')

        for kind, route in [('people', '/'), ('spaces', '/spaces')]:
            context = browser.new_context()
            context.add_init_script('window.PRESENCE_SIGNUP_CONFIG = ' + json.dumps(CONFIG))
            captured = []
            def accept(r):
                captured.append(r.request)
                r.fulfill(status=202, body='')
            context.route('https://a.klaviyo.com/**', accept)
            page = context.new_page()
            page.goto(base + route, wait_until='networkidle')
            form = page.locator('form')
            assert form.locator('[data-email-consent]').get_attribute('required') is not None
            assert not form.locator('[data-email-consent]').is_checked()
            fill(form, kind)
            form.locator('button').click()
            assert not captured  # No implicit email consent.
            form.locator('[data-email-consent]').check()
            form.locator('button').focus()
            page.keyboard.press('Enter')
            page.wait_for_function('!document.querySelector("form").hasAttribute("aria-busy")')
            assert len(captured) == 1
            request = captured[0]
            assert request.headers['revision'] == '2026-07-15'
            assert 'authorization' not in request.headers and 'cookie' not in request.headers
            (SHOTS / ('mock-' + kind + '.json')).write_text(json.dumps(request.post_data_json))
            data = request.post_data_json['data']
            assert data['relationships']['list']['data']['id'] == CONFIG['lists'][kind]
            attrs = data['attributes']['profile']['data']['attributes']
            assert attrs['email'] == 'test@example.invalid'
            assert attrs['subscriptions']['email']['marketing']['consent'] == 'SUBSCRIBED'
            assert attrs['subscriptions']['email']['open_tracking']['consent'] == 'UNSUBSCRIBED'
            assert attrs['subscriptions']['email']['click_tracking']['consent'] == 'UNSUBSCRIBED'
            assert attrs['properties']['presence_' + ('people' if kind == 'people' else 'space') + '_interest']
            if kind == 'spaces':
                assert attrs['properties']['presence_space_contact_name'] == 'Test contact'
                assert attrs['properties']['presence_space_name'] == 'Test space'
                assert attrs['properties']['presence_space_link'] == 'https://example.invalid'
            assert 'does not confirm that you are subscribed' in form.locator('[role="status"]').inner_text()
            assert form.locator('[role="status"]').evaluate('e => e === document.activeElement')
            assert not form.locator('input[type="email"]').input_value()
            assert not context.cookies()
            context.close()
            print('PASS:', kind, 'explicit consent, list/property mapping, no tracking consent and honest accepted-request status')

        # Rejections and network failures preserve values and never claim success.
        for status in [400, 429, 500, 'network']:
            context = browser.new_context()
            context.add_init_script('window.PRESENCE_SIGNUP_CONFIG = ' + json.dumps(CONFIG))
            def reject(r):
                if status == 'network': r.abort()
                else: r.fulfill(status=status, body='{}', content_type='application/json')
            context.route('https://a.klaviyo.com/**', reject)
            page = context.new_page()
            page.goto(base, wait_until='networkidle')
            form = page.locator('form')
            fill(form, 'people')
            form.locator('[data-email-consent]').check()
            form.locator('button').click()
            page.wait_for_function('!document.querySelector("form").hasAttribute("aria-busy")')
            assert 'couldn’t confirm' in form.locator('[role="status"]').inner_text()
            assert form.locator('input[type="email"]').input_value() == 'test@example.invalid'
            assert form.locator('button').is_enabled()
            context.close()
        print('PASS: 400/429/500 and network errors retain details and do not claim signup')

        context = browser.new_context()
        context.add_init_script('window.PRESENCE_SIGNUP_CONFIG = ' + json.dumps(CONFIG))
        pending = []
        context.route('https://a.klaviyo.com/**', lambda route: pending.append(route))
        page = context.new_page()
        page.goto(base, wait_until='networkidle')
        form = page.locator('form')
        fill(form, 'people')
        form.locator('[data-email-consent]').check()
        form.locator('button').click()
        page.wait_for_function('document.querySelector("form").getAttribute("aria-busy") === "true"')
        form.evaluate('e => e.dispatchEvent(new Event("submit", {bubbles:true, cancelable:true}))')
        assert form.locator('button').is_disabled() and len(pending) == 1
        pending[0].fulfill(status=202, body='')
        page.wait_for_function('!document.querySelector("form").hasAttribute("aria-busy")')
        context.close()
        print('PASS: duplicate submissions blocked while a request is pending')
        browser.close()
finally:
    server.shutdown()
print('Screenshots:', SHOTS)
