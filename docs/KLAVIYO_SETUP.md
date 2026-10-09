# Klaviyo activation

The integration is prepared but disabled. This code does not create or change Klaviyo account settings, lists, flows or campaigns, and no emails were sent during development. Use only Klaviyo's **public company/site ID** in the browser. Private API keys never belong in source, a frontend environment variable or chat.

## What is implemented

- Direct client subscription request to `https://a.klaviyo.com/client/subscriptions/?company_id=…`, API revision `2026-07-15`.
- Separate list IDs and namespaced profile properties for people and spaces. A shared email can express both interests without one form overwriting the other's fields.
- Unchecked email-consent controls; email is required in live mode. Space contact/name/town/country are required in live mode; type/link remain optional. People town/country remain optional.
- No Klaviyo onsite script, cookies, analytics or automatic host-pack delivery. Requests omit credentials and the referrer. Email open/click tracking consent is explicitly `UNSUBSCRIBED`.
- Only HTTP 202 displays a request-received message, which explicitly does not confirm subscription. Failures retain entries; timeouts do not claim the provider received nothing. Pending requests block repeat submissions.
- Without JavaScript, submission stays disabled. Unapproved/incomplete configuration uses the existing non-collecting preview.

## Configuration required before activation

1. Confirm the legal controller, country, public privacy contact, email scope and retention/deletion process. Replace the visibly pending parts of `/privacy`, and revise the preview descriptions in `/cookies`, `/terms` and the host PDF when signup actually opens. Check provider agreements and any international processing safeguards for the real accounts.
2. In the authorised Klaviyo account, create/choose two distinct lists: Presence people interest and Presence spaces interest. Verify **double opt-in** for both lists, confirmation/consent pages, branding and unsubscribe behaviour. Do not enable campaigns or flows as a side effect of this code change.
3. Configure the sender identity, required organisation/address information, authenticated sending domain and an operational deletion/access process in Klaviyo. Verify that email-open and click tracking are disabled for the messages/flows that will use these lists. Recording tracking consent alone does not prove that all account-level email tracking is disabled.
4. Put the public site ID and the two public list IDs in `signup-config.js`. Set the verified hostname(s) explicitly in `allowedHosts`. Do not allow every Vercel preview hostname. Set `privacyApproved`, `doubleOptInVerified` and `emailTrackingDisabled` only after those checks are complete. `enabled` is the final activation switch.
5. Complete an explicitly authorised provider test with controlled recipients before opening collection. Current browser tests mock **all** Klaviyo requests, so they send no email and do not validate the real account, CORS or double opt-in delivery. Record the test result and obtain approval of the final privacy configuration before activating real signup.

The user-supplied public company/site ID and both list IDs are configured in `signup-config.js`. The user has confirmed double opt-in is enabled for both lists, email-open/click tracking is off and `hello@meetpresence.com` is configured as the sender, with `send.meetpresence.com` as the sending domain. Remaining inputs are responsible operator/country/privacy contact, intended email scope and retention/deletion process, plus the allowed hostname. The privacy draft contains explicit placeholders at the user’s request. Real provider delivery has not been tested. No account access exists in this cloud workspace. Do not ask for a private key as a workaround.

## Fields sent

Both requests contain email, `presence_consent_version` and a custom consent source. API subscriptions cover email only; no phone number, precise location or SMS consent is sent.

People properties: `presence_people_interest`, `presence_people_town`, `presence_people_country`.
Spaces properties: `presence_space_interest`, `presence_space_contact_name`, `presence_space_name`, `presence_space_town`, `presence_space_country`, `presence_space_type`, `presence_space_link`.
Blank optional properties are omitted. The company/list IDs are public identifiers, not credentials. Provider consent records carry the subscription timestamp; the browser does not pretend that an accepted request proves a completed double opt-in.

## Verification

```sh
python3 tests/subscriptions_browser.py
python3 tests/spaces_browser.py
python3 tests/connection_browser.py
```

The subscription gate uses synthetic `example.invalid` entries and intercepts every Klaviyo API request. Never submit test entries to production lists. Existing preview gates continue to use only a temporary cloud server.

Official references read during implementation:
- https://developers.klaviyo.com/en/reference/create_client_subscription (public client API and OpenAPI schema, revision 2026-07-15)
- https://developers.klaviyo.com/en/docs/collect_email_and_sms_consent_via_api (consent and list opt-in settings)
