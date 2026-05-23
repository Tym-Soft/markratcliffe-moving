// Cloudflare Worker — quote email relay for markratcliffemoving.co.uk
//
// Receives quote-calculator submissions from the static site and forwards
// two branded emails via Resend:
//   1. Office copy  → OFFICE_EMAIL (must succeed)
//   2. Customer confirmation → submitted email (best-effort)
//
// Optional payload field `attachments`: array of
//   { filename: "string", contentBase64: "string" }
// — typically the inventory PDF generated client-side. Attachments are
// forwarded as-is to Resend.

const MAX_BODY_BYTES = 3_500_000;       // ~3.5MB JSON cap (covers ~2.5MB PDF after base64)
const MAX_ATTACHMENT_BYTES = 5_000_000; // 5MB per attachment (base64 chars, not decoded)
const MAX_TOTAL_ATTACHMENTS = 8_000_000;

const BRAND = {
  name: 'Mark Ratcliffe Moving & Storage',
  shortName: 'Mark Ratcliffe Moving',
  tagline: 'Family-run removals &amp; storage in East Sussex since 1982',
  url: 'https://www.markratcliffemoving.co.uk',
  phone: '01323 848 008',
  phoneHref: '+441323848008',
  email: 'office@markratcliffemoving.co.uk',
  address: 'Unit J12 Swallow Business Park, Diamond Drive, Lower Dicker, BN27 4EL',
  hours: 'Mon–Fri 08:00–17:30 · Sat 09:00–13:00',
  founded: '1982',
  legal: 'EMV London Ltd t/a Mark Ratcliffe Moving &amp; Storage',
  // Colours pulled from css/critical.css (--midnight-blue, --goldenrod)
  purple: '#4d2e8f',
  purpleDark: '#3a226d',
  gold: '#C8A876',
  goldDark: '#A88E5C',
  ink: '#222',
  inkSoft: '#555',
  muted: '#888',
  surface: '#faf8f3',
  surfaceBorder: '#e6dec9',
};

export default {
  async fetch(request, env) {
    const origin = request.headers.get('Origin') || '';
    const allowed = (env.ALLOWED_ORIGINS || '').split(',').map((s) => s.trim()).filter(Boolean);
    const allowOrigin = allowed.includes(origin) ? origin : allowed[0] || '';

    const cors = {
      'Access-Control-Allow-Origin': allowOrigin,
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Max-Age': '86400',
      Vary: 'Origin',
    };

    if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: cors });
    if (request.method !== 'POST')    return json({ ok: false, error: 'Method not allowed' }, 405, cors);
    if (allowed.length && !allowed.includes(origin)) {
      return json({ ok: false, error: 'Origin not allowed' }, 403, cors);
    }

    const declaredLength = Number(request.headers.get('Content-Length') || 0);
    if (declaredLength > MAX_BODY_BYTES) {
      return json({ ok: false, error: 'Payload too large' }, 413, cors);
    }

    let body;
    try { body = await request.json(); }
    catch { return json({ ok: false, error: 'Invalid JSON' }, 400, cors); }

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

    const attachments = normaliseAttachments(body && body.attachments);
    if (attachments.error) return json({ ok: false, error: attachments.error }, 400, cors);

    const officeHtml = renderOfficeEmail({ name, email, phone, summary, hasPdf: attachments.list.length > 0 });
    const customerHtml = renderCustomerEmail({ name, email, phone, summary, hasPdf: attachments.list.length > 0 });

    const officeResult = await sendEmail(env, {
      to: env.OFFICE_EMAIL,
      replyTo: email,
      subject,
      html: officeHtml,
      attachments: attachments.list,
    });
    if (!officeResult.ok) {
      return json({ ok: false, error: 'Could not send quote — please call ' + BRAND.phone + '.', detail: officeResult.error }, 502, cors);
    }

    const customerResult = await sendEmail(env, {
      to: email,
      replyTo: env.OFFICE_EMAIL,
      subject: 'Your quote request — ' + BRAND.shortName,
      html: customerHtml,
      attachments: attachments.list,
    });

    return json({ ok: true, customerEmailed: customerResult.ok }, 200, cors);
  },
};

// ---------- Resend ------------------------------------------------------

async function sendEmail(env, { to, replyTo, subject, html, attachments }) {
  if (!env.RESEND_API_KEY) return { ok: false, error: 'RESEND_API_KEY not configured' };
  const payload = {
    from: env.FROM_EMAIL,
    to,
    subject,
    html,
    reply_to: replyTo,
  };
  if (attachments && attachments.length > 0) {
    payload.attachments = attachments.map((a) => ({
      filename: a.filename,
      content: a.contentBase64,
    }));
  }
  let res;
  try {
    res = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
  } catch (e) {
    return { ok: false, error: `Resend fetch failed: ${e.message || e}` };
  }
  if (res.ok) return { ok: true };
  let detail = '';
  try { detail = await res.text(); } catch {}
  return { ok: false, error: `Resend ${res.status}: ${detail || res.statusText}` };
}

// ---------- Validation --------------------------------------------------

function normaliseAttachments(raw) {
  if (raw == null) return { list: [] };
  if (!Array.isArray(raw)) return { error: 'attachments must be an array' };
  if (raw.length > 4) return { error: 'Too many attachments' };
  const list = [];
  let totalBytes = 0;
  for (const item of raw) {
    if (!item || typeof item !== 'object') return { error: 'Invalid attachment' };
    const filename = typeof item.filename === 'string' ? item.filename.trim() : '';
    const b64 = typeof item.contentBase64 === 'string' ? item.contentBase64.trim() : '';
    if (!filename || filename.length > 100) return { error: 'Invalid attachment filename' };
    if (!/^[A-Za-z0-9._ -]+$/.test(filename)) return { error: 'Attachment filename has invalid characters' };
    if (!b64) return { error: 'Attachment content missing' };
    if (b64.length > MAX_ATTACHMENT_BYTES) return { error: 'Attachment too large' };
    if (!/^[A-Za-z0-9+/=\s]+$/.test(b64)) return { error: 'Attachment content is not valid base64' };
    totalBytes += b64.length;
    if (totalBytes > MAX_TOTAL_ATTACHMENTS) return { error: 'Attachments total too large' };
    list.push({ filename, contentBase64: b64.replace(/\s+/g, '') });
  }
  return { list };
}

function strField(obj, key, max) {
  const v = obj && obj[key];
  if (typeof v !== 'string') return '';
  const trimmed = v.trim();
  return trimmed.length > max ? trimmed.slice(0, max) : trimmed;
}

// ---------- Email templates --------------------------------------------

function renderOfficeEmail({ name, email, phone, summary, hasPdf }) {
  const intro = `<p style="margin:0 0 8px;font-size:14px;color:${BRAND.inkSoft};">A new quote request was submitted via the website's moving calculator.</p>`;
  const contactBlock = `
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="border-collapse:collapse;margin:16px 0 8px;">
      <tr>
        <td style="padding:10px 14px;background:${BRAND.surface};border:1px solid ${BRAND.surfaceBorder};border-radius:8px;font-family:Arial,Helvetica,sans-serif;font-size:14px;color:${BRAND.ink};line-height:1.55;">
          <strong style="color:${BRAND.purple};">Customer</strong><br>
          ${escapeHtml(name)}<br>
          <a href="mailto:${escapeHtml(email)}" style="color:${BRAND.purple};text-decoration:none;">${escapeHtml(email)}</a><br>
          <a href="tel:${escapeHtml(phone)}" style="color:${BRAND.purple};text-decoration:none;">${escapeHtml(phone)}</a>
        </td>
      </tr>
    </table>
  `;
  const pdfNote = hasPdf
    ? `<p style="margin:8px 0 0;font-size:13px;color:${BRAND.inkSoft};"><strong>Attached:</strong> inventory PDF generated by the calculator.</p>`
    : '';
  const summaryBlock = `
    <h3 style="margin:20px 0 8px;font-family:Georgia,'Times New Roman',serif;font-size:18px;color:${BRAND.purple};font-weight:normal;">Full quote summary</h3>
    <pre style="font-family:ui-monospace,Menlo,Consolas,monospace;white-space:pre-wrap;font-size:12.5px;line-height:1.55;background:${BRAND.surface};border:1px solid ${BRAND.surfaceBorder};border-left:4px solid ${BRAND.gold};padding:14px 16px;border-radius:6px;color:${BRAND.ink};margin:0;">${escapeHtml(summary)}</pre>
    ${pdfNote}
    <p style="margin:18px 0 0;font-size:13px;color:${BRAND.inkSoft};">Hit <strong>Reply</strong> to respond directly to the customer — Reply-To is set to <strong>${escapeHtml(email)}</strong>.</p>
  `;
  return wrapEmail({ preheader: `New quote: ${name}`, body: intro + contactBlock + summaryBlock });
}

function renderCustomerEmail({ name, email, phone, summary, hasPdf }) {
  const first = firstName(name);
  const greeting = `
    <p style="margin:0 0 14px;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:${BRAND.ink};line-height:1.55;">Hi ${escapeHtml(first)},</p>
    <p style="margin:0 0 14px;font-family:Arial,Helvetica,sans-serif;font-size:16px;color:${BRAND.ink};line-height:1.6;">Thank you for using our online moving calculator. We've received the figures below and the office will reply with a formal written quote <strong>within 48 hours</strong> (usually sooner during business hours).</p>
  `;
  const attached = hasPdf
    ? `<p style="margin:0 0 14px;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:${BRAND.ink};line-height:1.55;">📎 A copy of your <strong>inventory PDF</strong> is attached to this email — handy for the day of the move, and exactly what we'll quote against.</p>`
    : '';
  const summaryBlock = `
    <h3 style="margin:6px 0 10px;font-family:Georgia,'Times New Roman',serif;font-size:20px;color:${BRAND.purple};font-weight:normal;">Your quote summary</h3>
    <pre style="font-family:ui-monospace,Menlo,Consolas,monospace;white-space:pre-wrap;font-size:12.5px;line-height:1.55;background:${BRAND.surface};border:1px solid ${BRAND.surfaceBorder};border-left:4px solid ${BRAND.gold};padding:14px 16px;border-radius:6px;color:${BRAND.ink};margin:0 0 18px;">${escapeHtml(summary)}</pre>
  `;
  const adjust = `
    <p style="margin:0 0 18px;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:${BRAND.ink};line-height:1.6;">If anything needs adjusting — items, dates, postcodes, access notes — just reply to this email and we'll work from your updated details. Or call us on <a href="tel:${BRAND.phoneHref}" style="color:${BRAND.purple};text-decoration:none;font-weight:bold;">${BRAND.phone}</a>.</p>
  `;
  const trust = `
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="border-collapse:collapse;margin:0 0 18px;">
      <tr>
        <td style="padding:14px 16px;background:${BRAND.purple};border-radius:8px;font-family:Arial,Helvetica,sans-serif;font-size:14px;color:#fff;line-height:1.6;">
          <strong style="color:${BRAND.gold};">Why customers choose us</strong><br>
          ✓ Family-run since ${BRAND.founded} · three generations of removers<br>
          ✓ Fully covered — Goods in Transit + Public Liability insurance<br>
          ✓ Local crews who know East Sussex, West Sussex, Surrey &amp; Kent<br>
          ✓ Fixed-price written quote — no hidden mileage or volumetric extras
        </td>
      </tr>
    </table>
  `;
  const signoff = `
    <p style="margin:0 0 6px;font-family:Arial,Helvetica,sans-serif;font-size:15px;color:${BRAND.ink};">Kind regards,</p>
    <p style="margin:0 0 16px;font-family:Georgia,'Times New Roman',serif;font-size:17px;color:${BRAND.purple};"><em>The team at ${BRAND.shortName}</em></p>
  `;
  return wrapEmail({
    preheader: `Thanks ${first} — we'll reply within 48 hours with your written quote.`,
    body: greeting + attached + summaryBlock + adjust + trust + signoff,
  });
}

function wrapEmail({ preheader, body }) {
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${BRAND.shortName}</title>
</head>
<body style="margin:0;padding:0;background:#f1ecdf;font-family:Arial,Helvetica,sans-serif;">
<div style="display:none;max-height:0;overflow:hidden;mso-hide:all;visibility:hidden;opacity:0;color:transparent;height:0;width:0;font-size:1px;line-height:1px;">${escapeHtml(preheader)}</div>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background:#f1ecdf;">
  <tr>
    <td align="center" style="padding:24px 12px;">
      <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="640" style="width:100%;max-width:640px;background:#ffffff;border-radius:12px;overflow:hidden;box-shadow:0 6px 24px rgba(77,46,143,0.08);">
        <!-- Brand band -->
        <tr>
          <td style="background:${BRAND.purple};padding:24px 28px 18px;text-align:left;">
            <div style="font-family:Georgia,'Times New Roman',serif;font-size:22px;line-height:1.2;color:#fff;letter-spacing:0.2px;">
              <span style="color:${BRAND.gold};">Mark Ratcliffe</span> <span style="color:#fff;font-weight:300;">Moving &amp; Storage</span>
            </div>
            <div style="margin-top:6px;font-family:Arial,Helvetica,sans-serif;font-size:12.5px;color:#e6dec9;letter-spacing:0.4px;text-transform:uppercase;">${BRAND.tagline}</div>
          </td>
        </tr>
        <!-- Gold divider -->
        <tr><td style="height:4px;background:${BRAND.gold};line-height:4px;font-size:0;">&nbsp;</td></tr>

        <!-- Body -->
        <tr>
          <td style="padding:24px 28px 8px;">
            ${body}
          </td>
        </tr>

        <!-- Footer -->
        <tr>
          <td style="padding:20px 28px 24px;background:${BRAND.surface};border-top:1px solid ${BRAND.surfaceBorder};">
            <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
              <tr>
                <td style="font-family:Arial,Helvetica,sans-serif;font-size:12px;color:${BRAND.inkSoft};line-height:1.55;">
                  <strong style="color:${BRAND.purple};font-size:13px;">${BRAND.shortName}</strong><br>
                  ${BRAND.address}<br>
                  <a href="tel:${BRAND.phoneHref}" style="color:${BRAND.purple};text-decoration:none;">${BRAND.phone}</a> ·
                  <a href="mailto:${BRAND.email}" style="color:${BRAND.purple};text-decoration:none;">${BRAND.email}</a> ·
                  <a href="${BRAND.url}" style="color:${BRAND.purple};text-decoration:none;">markratcliffemoving.co.uk</a><br>
                  ${BRAND.hours}
                  <div style="margin-top:10px;font-size:11px;color:${BRAND.muted};">${BRAND.legal} · Family-run since ${BRAND.founded}.</div>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
      <div style="font-family:Arial,Helvetica,sans-serif;font-size:11px;color:${BRAND.muted};padding:14px 0 0;">You're receiving this because you requested a quote at <a href="${BRAND.url}" style="color:${BRAND.muted};">markratcliffemoving.co.uk</a>.</div>
    </td>
  </tr>
</table>
</body>
</html>`;
}

// ---------- Helpers -----------------------------------------------------

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

function firstName(full) {
  const honorifics = new Set(['mr', 'mrs', 'miss', 'ms', 'mx', 'dr', 'prof']);
  const parts = String(full).trim().split(/\s+/);
  if (parts.length > 1 && honorifics.has(parts[0].toLowerCase().replace('.', ''))) return parts[1];
  return parts[0] || 'there';
}

function json(body, status, extraHeaders) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json', ...extraHeaders },
  });
}
