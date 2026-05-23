// Cloudflare Worker — quote email relay for markratcliffemoving.co.uk
//
// The site is hosted on GitHub Pages (static), so the Resend API key cannot
// live in client JS. This worker holds the key as a wrangler secret and is
// the only place that talks to Resend.
//
// Flow:
//   1. Calculator page POSTs JSON (name, email, phone, summary, etc.)
//   2. Worker validates + honeypot-screens the payload.
//   3. Worker sends two emails via Resend:
//        a) Office copy (must succeed — surfaces 502 if it fails).
//        b) Customer confirmation (best-effort — soft-fails).
//
// Environment (set via `wrangler secret put` or wrangler.toml [vars]):
//   RESEND_API_KEY  — secret. The Resend bearer token.
//   OFFICE_EMAIL    — where the office copy lands.
//   FROM_EMAIL      — RFC5322 "Name <addr>" string; addr must be on a
//                     Resend-verified domain (or onboarding@resend.dev for tests).
//   ALLOWED_ORIGINS — comma-separated list of permitted CORS origins.

export default {
  async fetch(request, env) {
    const origin = request.headers.get('Origin') || '';
    const allowed = (env.ALLOWED_ORIGINS || '')
      .split(',')
      .map((s) => s.trim())
      .filter(Boolean);
    const allowOrigin = allowed.includes(origin) ? origin : allowed[0] || '';

    const cors = {
      'Access-Control-Allow-Origin': allowOrigin,
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Max-Age': '86400',
      Vary: 'Origin',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: cors });
    }
    if (request.method !== 'POST') {
      return json({ ok: false, error: 'Method not allowed' }, 405, cors);
    }
    if (allowed.length && !allowed.includes(origin)) {
      return json({ ok: false, error: 'Origin not allowed' }, 403, cors);
    }

    const contentLength = Number(request.headers.get('Content-Length') || 0);
    if (contentLength > 50_000) {
      return json({ ok: false, error: 'Payload too large' }, 413, cors);
    }

    let body;
    try {
      body = await request.json();
    } catch {
      return json({ ok: false, error: 'Invalid JSON' }, 400, cors);
    }

    // Honeypot: legitimate forms leave `hp` empty; bots tend to fill every field.
    if (body && typeof body.hp === 'string' && body.hp.trim() !== '') {
      return json({ ok: true }, 200, cors);
    }

    const name = strField(body, 'name', 120);
    const email = strField(body, 'email', 200);
    const phone = strField(body, 'phone', 40);
    const summary = strField(body, 'summary', 20_000);
    const subject = strField(body, 'subject', 250) || `Quote request — ${name || 'Customer'}`;

    if (!name) return json({ ok: false, error: 'Name is required' }, 400, cors);
    if (!email) return json({ ok: false, error: 'Email is required' }, 400, cors);
    if (!phone) return json({ ok: false, error: 'Phone number is required' }, 400, cors);
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
      return json({ ok: false, error: 'That email address looks invalid' }, 400, cors);
    }
    if (!summary) return json({ ok: false, error: 'Quote summary missing' }, 400, cors);

    const officeHtml = `
      <div style="font-family:Arial,sans-serif;font-size:14px;color:#222;max-width:680px;">
        <p><strong>Customer:</strong> ${escapeHtml(name)}<br>
           <strong>Email:</strong> <a href="mailto:${escapeHtml(email)}">${escapeHtml(email)}</a><br>
           <strong>Phone:</strong> <a href="tel:${escapeHtml(phone)}">${escapeHtml(phone)}</a></p>
        <pre style="font-family:ui-monospace,Menlo,Consolas,monospace;white-space:pre-wrap;font-size:13px;line-height:1.5;background:#f6f4ef;border:1px solid #e6dec9;padding:16px;border-radius:6px;color:#222;">${escapeHtml(summary)}</pre>
        <p style="font-size:12px;color:#666;">Reply directly to this email — the Reply-To is set to the customer.</p>
      </div>
    `;

    const customerHtml = `
      <div style="font-family:Arial,sans-serif;font-size:15px;line-height:1.55;color:#222;max-width:640px;">
        <p>Hi ${escapeHtml(firstName(name))},</p>
        <p>Thank you for using our online quote calculator. The figures you sent are below — we've received this at the office and will reply <strong>within 48 hours</strong> with a formal written quote.</p>
        <pre style="font-family:ui-monospace,Menlo,Consolas,monospace;white-space:pre-wrap;font-size:13px;line-height:1.5;background:#f6f4ef;border:1px solid #e6dec9;padding:16px;border-radius:6px;color:#222;">${escapeHtml(summary)}</pre>
        <p>If anything needs adjusting in the meantime — items, dates, postcodes — just reply to this email and we'll work from your updated details.</p>
        <p>Kind regards,<br>The team at Mark Ratcliffe Moving &amp; Storage</p>
        <p style="font-size:12px;color:#666;margin-top:24px;">EMV London Ltd t/a Mark Ratcliffe Moving &amp; Storage · 01323 848008 · office@markratcliffemoving.co.uk · Family-run since 1982.</p>
      </div>
    `;

    const officeResult = await sendEmail(env, {
      to: env.OFFICE_EMAIL,
      replyTo: email,
      subject,
      html: officeHtml,
    });
    if (!officeResult.ok) {
      return json({ ok: false, error: 'Could not send quote — please call 01323 848008.', detail: officeResult.error }, 502, cors);
    }

    const customerResult = await sendEmail(env, {
      to: email,
      replyTo: env.OFFICE_EMAIL,
      subject: 'Your quote request — Mark Ratcliffe Moving & Storage',
      html: customerHtml,
    });

    return json({ ok: true, customerEmailed: customerResult.ok }, 200, cors);
  },
};

async function sendEmail(env, { to, replyTo, subject, html }) {
  if (!env.RESEND_API_KEY) return { ok: false, error: 'RESEND_API_KEY not configured' };
  let res;
  try {
    res = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${env.RESEND_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from: env.FROM_EMAIL,
        to,
        subject,
        html,
        reply_to: replyTo,
      }),
    });
  } catch (e) {
    return { ok: false, error: `Resend fetch failed: ${e.message || e}` };
  }
  if (res.ok) return { ok: true };
  let detail = '';
  try { detail = await res.text(); } catch {}
  return { ok: false, error: `Resend ${res.status}: ${detail || res.statusText}` };
}

function strField(obj, key, max) {
  const v = obj && obj[key];
  if (typeof v !== 'string') return '';
  const trimmed = v.trim();
  return trimmed.length > max ? trimmed.slice(0, max) : trimmed;
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

function firstName(full) {
  const honorifics = new Set(['mr', 'mrs', 'miss', 'ms', 'mx', 'dr', 'prof']);
  const parts = String(full).trim().split(/\s+/);
  if (parts.length > 1 && honorifics.has(parts[0].toLowerCase().replace('.', ''))) {
    return parts[1];
  }
  return parts[0] || 'there';
}

function json(body, status, extraHeaders) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json', ...extraHeaders },
  });
}
