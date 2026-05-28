# Cloudflare Workers — markratcliffemoving.co.uk

Email + PDF endpoints for the static site. Currently:

## `careers-application.js` — Job application endpoint

**Route:** `POST /api/careers`

Receives the JSON body from the `/careers.html` form, builds a PDF of
the application using `pdf-lib`, and sends it as an attachment in two
emails via Resend — one to the applicant (confirmation) and one to the
office (notification).

### Required environment variables

| Var | Example | Purpose |
|---|---|---|
| `RESEND_API_KEY` | `re_xxxxxxxxxxxx` | Resend API key (eu-west-1 region) |
| `OWNER_EMAIL` | `office@markratcliffemoving.co.uk` | Where notifications go |
| `FROM_EMAIL` | `careers@markratcliffemoving.co.uk` | Verified sender on Resend |
| `ALLOWED_ORIGIN` | `https://www.markratcliffemoving.co.uk` | CORS origin |

### Deploy steps (Wrangler)

```bash
# in cloudflare-workers/ directory
npm init -y
npm install pdf-lib
npx wrangler init     # if you don't already have wrangler.toml

# Add to wrangler.toml:
#   name = "markratcliffe-careers"
#   main = "careers-application.js"
#   compatibility_date = "2026-05-01"

npx wrangler secret put RESEND_API_KEY
npx wrangler secret put OWNER_EMAIL
npx wrangler secret put FROM_EMAIL
npx wrangler secret put ALLOWED_ORIGIN

npx wrangler deploy
```

### Or: merge into existing `markratcliffe-moving` worker

If you already have a worker handling the calculator quote, add this
file's logic as a second handler. In your existing worker entry:

```js
import { handleCareers } from './careers-application.js';

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (url.pathname === '/api/careers') return handleCareers(request, env);
    if (url.pathname === '/api/quote')   return handleQuote(request, env);
    return new Response('Not found', { status: 404 });
  },
};
```

(Export the handler from `careers-application.js` rather than using its
default export when merging.)

### Frontend wiring

The careers form on `/careers.html` posts to
`https://markratcliffe-moving.vandymanservices.workers.dev/api/careers`
by default. Change the URL in `js/careers-form.js` if you deploy to a
different domain (e.g., a custom subdomain like
`https://api.markratcliffemoving.co.uk/careers`).

### Resend setup checklist

1. Add `careers@markratcliffemoving.co.uk` as a verified sender in Resend
2. Add SPF + DKIM records to the markratcliffemoving.co.uk DNS (Resend dashboard generates these)
3. Ensure DMARC record allows or quarantines (don't reject) until SPF/DKIM are verified

### Testing

```bash
curl -X POST https://markratcliffe-moving.vandymanservices.workers.dev/api/careers \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "Test",
    "lastName":  "Applicant",
    "email":     "you@example.com",
    "phone":     "07000000000",
    "postcode":  "BN27 4EL",
    "position":  "Driver (LGV)",
    "rightToWork": "Yes",
    "gdprConsent": true
  }'
```

Expect HTTP 200 with `{ok: true, ...}` and two emails delivered (one to
the test applicant address, one to `OWNER_EMAIL`).
