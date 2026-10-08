"""Cloud browser gate. Run against the development server, never production."""
import os
from pathlib import Path
from urllib.request import urlopen

from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:3000"
SHOTS = Path(os.environ.get("PRESENCE_SCREENSHOT_DIR", "/tmp/presence-screenshots"))
SHOTS.mkdir(parents=True, exist_ok=True)

for path in ["/", "/spaces", "/spaces/", "/styles.css", "/preview.js", "/mark.svg", "/assets/sample-coast.jpg"]:
    with urlopen(BASE + path) as response:
        assert response.status == 200, path
        assert response.read(), path
print("PASS: direct routes, redirect and shared assets")

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path="/usr/bin/chromium", args=["--no-sandbox"])
    for label, viewport in [("desktop", {"width": 1440, "height": 1000}), ("mobile", {"width": 390, "height": 844}), ("narrow", {"width": 320, "height": 740})]:
        context = browser.new_context(viewport=viewport, reduced_motion="reduce")
        page = context.new_page()
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        for route, form_id, message_id in [("/", "interest", "form-msg"), ("/spaces", "space-interest-form", "space-form-msg")]:
            page.goto(BASE + route, wait_until="networkidle")
            assert page.locator("h1").count() == 1
            assert page.locator('meta[name="robots"]').get_attribute("content") == "noindex, nofollow"
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), (route, label)
            for element in page.locator("[aria-labelledby], [aria-describedby]").all():
                for attr in ["aria-labelledby", "aria-describedby"]:
                    for target in (element.get_attribute(attr) or "").split():
                        assert page.locator("#" + target).count() == 1, (route, target)
            for field in page.locator("input").all():
                assert page.locator('label[for="' + field.get_attribute("id") + '"]').count() == 1
            # Keyboard navigation exposes the skip link and its destination.
            page.keyboard.press("Tab")
            assert page.locator(".skip").evaluate("el => document.activeElement === el")
            assert page.locator(".skip").bounding_box()["y"] >= 0
            page.keyboard.press("Enter")
            assert page.url.endswith("#waitlist" if route == "/" else "#main")
            page.goto(BASE + route, wait_until="networkidle")
            if label != "narrow":
                page.screenshot(path=str(SHOTS / ("home" if route == "/" else "spaces")) + "-" + label + ".png", full_page=True)
            form = page.locator("#" + form_id)
            message = page.locator("#" + message_id)
            assert message.is_hidden()
            for field in form.locator("input").all():
                typ = field.get_attribute("type")
                if typ == "checkbox":
                    field.check()
                else:
                    field.fill("test@example.invalid" if typ == "email" else "https://example.invalid" if typ == "url" else "Test space")
            requests = []
            page.on("request", lambda request: requests.append(request.url))
            # Activate the button with the keyboard, then try Enter from a field.
            form.locator("button").focus()
            page.keyboard.press("Enter")
            assert message.is_visible()
            assert "nothing was sent or stored" in message.inner_text()
            assert message.evaluate("el => document.activeElement === el")
            form.locator('input[type="email"]').focus()
            page.keyboard.press("Enter")
            page.wait_for_timeout(100)
            assert not requests, requests
            assert page.evaluate("localStorage.length === 0 && sessionStorage.length === 0")
            assert not context.cookies()
            assert not errors, errors
        page.goto(BASE + "/", wait_until="networkidle")
        page.locator('nav a[href="/spaces"]').click()
        assert page.locator("#spaces-h").is_visible()
        page.locator('header a[href="/"]').click()
        assert page.locator("#hero-h").is_visible()
        page.locator('.spaces-invitation a[href="/spaces"]').click()
        assert page.locator("#spaces-h").is_visible()
        print(f"PASS: {label} layouts, links, keyboard access and non-collecting forms")
        context.close()

    context = browser.new_context(java_script_enabled=False)
    page = context.new_page()
    for route in ["/", "/spaces"]:
        page.goto(BASE + route, wait_until="networkidle")
        form = page.locator("form")
        assert form.locator("button").is_disabled()
        assert form.locator("noscript").is_visible()
        form.locator('input[type="email"]').fill("test@example.invalid")
        requests = []
        page.on("request", lambda request: requests.append(request.url))
        form.locator('input[type="email"]').press("Enter")
        page.wait_for_timeout(100)
        assert not requests, requests
        assert "?" not in page.url
    print("PASS: JavaScript-disabled forms cannot submit")
    browser.close()
print("Screenshots:", SHOTS)
