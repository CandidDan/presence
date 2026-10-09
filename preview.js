// Static client subscriptions, disabled by default. No Klaviyo tracking script.
(function () {
  'use strict';
  var config = window.PRESENCE_SIGNUP_CONFIG || {};
  var ready = config.enabled === true && config.privacyApproved === true &&
    config.doubleOptInVerified === true && config.emailTrackingDisabled === true &&
    /^[A-Za-z0-9]{6}$/.test(config.companyId || '') &&
    /^[A-Za-z0-9]{6}$/.test((config.lists || {}).people || '') &&
    /^[A-Za-z0-9]{6}$/.test((config.lists || {}).spaces || '') &&
    config.lists.people !== config.lists.spaces &&
    Array.isArray(config.allowedHosts) && config.allowedHosts.indexOf(location.hostname) !== -1;

  document.querySelectorAll('[data-preview-form]').forEach(function (form) {
    var msg = form.querySelector('[role="status"]');
    var button = form.querySelector('button[type="submit"]');
    if (!msg || !button) return;
    var kind = form.id === 'space-interest-form' ? 'spaces' : 'people';
    var consent = form.querySelector('[data-email-consent]');
    var notice = document.getElementById(form.getAttribute('aria-describedby'));
    var busy = false;
    function show(text) {
      if (text) msg.textContent = text;
      msg.hidden = false;
      msg.setAttribute('tabindex', '-1');
      msg.focus();
    }
    function value(name) {
      var field = form.elements.namedItem(name);
      return field ? field.value.trim() : '';
    }
    if (ready) {
      notice.textContent = 'Email updates are handled by Klaviyo. We use double opt-in; check your inbox if a confirmation is needed. You can unsubscribe at any time. Read the privacy notice below.';
      form.querySelectorAll('[data-live-required]').forEach(function (field) { field.required = true; });
      if (consent) consent.required = true;
      document.querySelectorAll('[data-preview-only]').forEach(function (item) { item.hidden = true; });
    }
    form.addEventListener('submit', async function (event) {
      event.preventDefault();
      if (!ready) { show(); return; }
      if (busy) return;
      if (!form.reportValidity() || !consent || !consent.checked) return;
      var email = value(kind === 'people' ? 'email' : 'space-email');
      var properties = { presence_consent_version: config.consentVersion };
      var prefix = kind === 'people' ? 'presence_people_' : 'presence_space_';
      properties[prefix + 'interest'] = true;
      // Keep each form's properties separate when the same email joins both lists.
      if (kind === 'people') {
        properties[prefix + 'town'] = value('town');
        properties[prefix + 'country'] = value('country');
      } else {
        properties[prefix + 'contact_name'] = value('contact-name');
        properties[prefix + 'name'] = value('space-name');
        properties[prefix + 'town'] = value('space-town');
        properties[prefix + 'country'] = value('space-country');
        properties[prefix + 'type'] = value('space-type');
        properties[prefix + 'link'] = value('space-link');
      }
      Object.keys(properties).forEach(function (key) { if (properties[key] === '') delete properties[key]; });
      var payload = { data: {
        type: 'subscription',
        attributes: {
          custom_source: 'Presence ' + kind + ' interest (' + config.consentVersion + ')',
          profile: { data: { type: 'profile', attributes: {
            email: email,
            properties: properties,
            subscriptions: { email: {
              marketing: { consent: 'SUBSCRIBED' },
              open_tracking: { consent: 'UNSUBSCRIBED' },
              click_tracking: { consent: 'UNSUBSCRIBED' }
            } }
          } } }
        },
        relationships: { list: { data: { type: 'list', id: config.lists[kind] } } }
      } };
      busy = true;
      button.disabled = true;
      form.setAttribute('aria-busy', 'true');
      var controller = new AbortController();
      var timeout = setTimeout(function () { controller.abort(); }, 15000);
      try {
        var response = await fetch('https://a.klaviyo.com/client/subscriptions/?company_id=' + encodeURIComponent(config.companyId), {
          method: 'POST',
          headers: { 'Content-Type': 'application/vnd.api+json', 'Accept': 'application/vnd.api+json', 'revision': '2026-07-15' },
          credentials: 'omit',
          referrerPolicy: 'no-referrer',
          signal: controller.signal,
          body: JSON.stringify(payload)
        });
        if (response.status !== 202) throw new Error('Request not accepted');
        show('Request received. Check your inbox if a confirmation is needed. This response does not confirm that you are subscribed. You can unsubscribe from Presence emails at any time.');
        form.reset();
      } catch (error) {
        // A timeout may happen after acceptance; avoid claiming nothing was received.
        show('We couldn’t confirm that your request was received. Your details are still here so you can try again. If a confirmation email arrives, follow its instructions.');
      } finally {
        clearTimeout(timeout);
        busy = false;
        button.disabled = false;
        form.removeAttribute('aria-busy');
      }
    });
    // With JavaScript disabled, buttons stay disabled and the form cannot submit.
    button.disabled = false;
  });
})();
