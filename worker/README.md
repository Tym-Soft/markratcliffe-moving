# Quote relay worker — mrm-quote

A small Cloudflare Worker that receives quote-calculator submissions from
`resources/storage-calculator.html` and forwards them to Resend, sending:

1. **Office copy** to `OFFICE_EMAIL` (reply-to = customer) — must succeed.
2. **Customer confirmation** back to the visitor — best-effort.

The site itself stays on GitHub Pages. The worker is the only piece that
holds the Resend API key.

---

## No-CLI option (recommended — no Node install needed)

If you don't have Node installed, deploy entirely from the Cloudflare dashboard:

1. Sign in at <https://dash.cloudflare.com/> → **Workers & Pages** → **Create application** → **Create Worker**.
2. Name it `mrm-quote`, then **Deploy** the boilerplate.
3. Click **Edit code**, paste the full contents of `src/index.js` over the existing `worker.js`, then **Save and deploy**.
4. Go to the worker's **Settings → Variables**:
   - **Environment Variables (plaintext):** add each of these with the matching value from `wrangler.toml`:
     - `OFFICE_EMAIL` → `office@markratcliffemoving.co.uk`
     - `FROM_EMAIL` → `Mark Ratcliffe Moving <onboarding@resend.dev>` (swap to a verified-domain address later)
     - `ALLOWED_ORIGINS` → `https://www.markratcliffemoving.co.uk,https://markratcliffemoving.co.uk`
   - **Environment Variables (encrypt):** add `RESEND_API_KEY` and paste the Resend key. Tick **Encrypt** before saving.
5. Copy the worker's URL from the top of the page (e.g. `https://mrm-quote.<your-subdomain>.workers.dev`).
6. Open `js/storage-calculator.js`, find `WORKER_QUOTE_ENDPOINT`, paste the URL in, commit + push.

To update the worker later, repeat step 3 with the new `src/index.js` contents.

---

## CLI option (Wrangler)

Needs Node + Wrangler installed (`npm i -g wrangler`).

```bash
cd worker

# 1. Log in to Cloudflare (browser pops open).
wrangler login

# 2. Store the Resend API key as a secret (don't commit it).
wrangler secret put RESEND_API_KEY
# Paste the key (starts with `re_…`) when prompted.

# 3. Verify the sender domain in the Resend dashboard
#    (Settings → Domains → Add `markratcliffemoving.co.uk`)
#    then update FROM_EMAIL in wrangler.toml to e.g.:
#    "Mark Ratcliffe Moving <quotes@markratcliffemoving.co.uk>"
#    Until verification finishes, the bundled `onboarding@resend.dev`
#    sandbox sender will still deliver to the office address fine, but
#    customer confirmations will land in spam — verify before go-live.

# 4. Deploy.
wrangler deploy
```

Wrangler prints the public URL, e.g.

```
https://mrm-quote.<your-subdomain>.workers.dev
```

Open `js/storage-calculator.js`, search for `WORKER_QUOTE_ENDPOINT`, and
paste that URL in (replacing the placeholder). Commit + push the change so
GitHub Pages rebuilds the site.

---

## Local development

```bash
cd worker
cp .dev.vars.example .dev.vars
# Edit .dev.vars and paste the Resend key.
wrangler dev
```

Wrangler serves on `http://localhost:8787` by default. To test against the
running calculator, temporarily change `WORKER_QUOTE_ENDPOINT` in
`js/storage-calculator.js` to `http://localhost:8787`.

---

## Rotating the API key

If the key has been pasted into chat, screenshots, or anywhere else
non-private, rotate it:

1. Resend dashboard → API Keys → revoke the old key, create a new one.
2. `cd worker && wrangler secret put RESEND_API_KEY` and paste the new value.
3. Update `.dev.vars` locally if you use `wrangler dev`.

No code changes needed — the worker reads `env.RESEND_API_KEY` at runtime.

---

## Files

| File | What it is |
|---|---|
| `src/index.js` | Worker source — validates payload, calls Resend twice. |
| `wrangler.toml` | Non-secret config (office address, from address, CORS allowlist). |
| `.dev.vars.example` | Template for local secret file. |
| `.dev.vars` | Local secret file (gitignored). |
| `.gitignore` | Excludes `.dev.vars`, `node_modules`, `.wrangler`. |
