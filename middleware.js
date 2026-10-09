// Free access gate for the preview: one shared code, set as PRESENCE_CODE in Vercel env.
// Runs at the edge on every request. No code set → site is open.
export const config = { matcher: ['/((?!assets/|mark.svg|styles.css|preview.js|signup-config.js|field.js).*)'] };

const COOKIE = 'presence_gate';

async function token(code) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode('presence:' + code));
  return Array.from(new Uint8Array(buf)).map((b) => b.toString(16).padStart(2, '0')).join('');
}

function page(error) {
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex, nofollow"><title>Presence — preview</title>
<link rel="stylesheet" href="/assets/fonts/outfit.css">
<style>body{margin:0;min-height:100vh;display:grid;place-items:center;background:#F6F6F4;color:#1B1A19;font-family:Outfit,system-ui,sans-serif}
form{width:min(92vw,380px);display:flex;flex-direction:column;gap:18px;padding:24px}
h1{font-weight:300;font-size:40px;letter-spacing:-.03em;line-height:1;margin:0}p{margin:0;color:#6E6B67;font-size:15px}
input{font:400 18px Outfit,sans-serif;padding:0 16px;height:54px;border:1.5px solid #CFCECA;border-radius:12px;background:#fff;color:#1B1A19}
input:focus{outline:3px solid #F0A35E;outline-offset:2px;border-color:#1B1A19}
button{height:52px;border-radius:999px;border:0;background:#1B1A19;color:#F6F6F4;font:500 16px Outfit,sans-serif;cursor:pointer}
.err{color:#B9731F;font-weight:500}</style></head><body>
<form method="post" action="/__gate"><h1>Presence</h1><p>This preview is shared by invitation. Enter the code you were given.</p>
<label for="c" style="font-size:15px;font-weight:500">Access code</label><input id="c" name="code" type="password" autocomplete="off" autofocus required>
${error ? '<p class="err">That code didn’t match.</p>' : ''}<button type="submit">Open preview</button></form></body></html>`;
}

export default async function middleware(req) {
  const code = process.env.PRESENCE_CODE;
  if (!code) return;
  const url = new URL(req.url);
  const expected = await token(code);
  const cookies = req.headers.get('cookie') || '';
  const authed = cookies.split(';').some((c) => c.trim() === `${COOKIE}=${expected}`);

  if (url.pathname === '/__gate' && req.method === 'POST') {
    const form = await req.formData();
    const given = String(form.get('code') || '').trim();
    if (given === code) {
      return new Response(null, {
        status: 303,
        headers: {
          location: '/',
          'set-cookie': `${COOKIE}=${expected}; Path=/; Max-Age=2592000; HttpOnly; Secure; SameSite=Lax`,
        },
      });
    }
    return new Response(page(true), { status: 401, headers: { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store' } });
  }

  if (authed) return;
  return new Response(page(false), { status: 401, headers: { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'no-store' } });
}
