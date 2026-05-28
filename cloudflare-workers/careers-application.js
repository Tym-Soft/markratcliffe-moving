/**
 * Cloudflare Worker — Careers application endpoint.
 *
 * Route: POST https://markratcliffe-moving.vandymanservices.workers.dev/api/careers
 * Or:    POST https://api.markratcliffemoving.co.uk/careers   (if you bind a custom subdomain)
 *
 * What it does:
 *   1. Parses the JSON application from the careers form
 *   2. Validates required fields + honeypot + GDPR consent
 *   3. Generates a PDF copy of the application (pdf-lib)
 *   4. Sends two emails via Resend, each with the PDF attached:
 *        a. To the APPLICANT  — confirmation, "we'll be in touch"
 *        b. To the OWNER      — new application notification
 *
 * Required Cloudflare environment variables:
 *   RESEND_API_KEY     re_xxxxxxxxxxxxxxxxxxxxxxxx
 *   OWNER_EMAIL        office@markratcliffemoving.co.uk
 *   FROM_EMAIL         careers@markratcliffemoving.co.uk    (must be verified on Resend)
 *   ALLOWED_ORIGIN     https://www.markratcliffemoving.co.uk
 *
 * Dependencies (install with `npm i pdf-lib`):
 *   pdf-lib   ~ 280KB, well within free-tier 1MB worker bundle limit
 *
 * Deploy:
 *   wrangler deploy   (or merge into existing worker if you prefer)
 *
 * Add this route OR a separate worker — if merging into the existing
 * worker that handles the calculator quote, branch on URL pathname:
 *
 *     if (url.pathname === '/api/careers') return handleCareers(request, env);
 *     if (url.pathname === '/api/quote')   return handleQuote(request, env);
 */

import { PDFDocument, StandardFonts, rgb } from 'pdf-lib';

const REQUIRED_FIELDS = [
  'firstName', 'lastName', 'email', 'phone', 'postcode',
  'position', 'rightToWork', 'gdprConsent'
];

export default {
  async fetch(request, env, ctx) {
    return handleCareers(request, env);
  },
};

async function handleCareers(request, env) {
  const allowedOrigin = env.ALLOWED_ORIGIN || 'https://www.markratcliffemoving.co.uk';
  const corsHeaders = {
    'Access-Control-Allow-Origin': allowedOrigin,
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400',
  };

  // Preflight
  if (request.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: corsHeaders });
  }
  if (request.method !== 'POST') {
    return json({ error: 'POST only' }, 405, corsHeaders);
  }

  let data;
  try {
    data = await request.json();
  } catch (e) {
    return json({ error: 'Invalid JSON body' }, 400, corsHeaders);
  }

  // Honeypot — bot trap. If filled, silently 200 so bot thinks it succeeded.
  if (data.website && data.website.length > 0) {
    return json({ ok: true }, 200, corsHeaders);
  }

  // GDPR
  if (data.gdprConsent !== true && data.gdprConsent !== 'true') {
    return json({ error: 'GDPR consent required' }, 400, corsHeaders);
  }

  // Field validation
  const missing = REQUIRED_FIELDS.filter(f => !data[f] || String(data[f]).trim() === '');
  if (missing.length > 0) {
    return json({ error: 'Missing required fields', missing }, 400, corsHeaders);
  }

  // Basic email regex
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) {
    return json({ error: 'Invalid email address' }, 400, corsHeaders);
  }

  // Build PDF
  const pdfBytes = await buildApplicationPdf(data);
  const pdfBase64 = bytesToBase64(pdfBytes);
  const filename = `application-${data.lastName.replace(/[^a-z0-9]/gi, '')}-${Date.now()}.pdf`;

  // Send both emails (Resend)
  const ownerEmail = env.OWNER_EMAIL || 'office@markratcliffemoving.co.uk';
  const fromEmail  = env.FROM_EMAIL  || 'careers@markratcliffemoving.co.uk';

  try {
    await Promise.all([
      sendEmail(env.RESEND_API_KEY, {
        from: `Mark Ratcliffe Moving Careers <${fromEmail}>`,
        to: data.email,
        subject: 'Thank you for your application — Mark Ratcliffe Moving',
        html: applicantEmailHtml(data),
        text: applicantEmailText(data),
        attachments: [{ filename, content: pdfBase64 }],
      }),
      sendEmail(env.RESEND_API_KEY, {
        from: `Mark Ratcliffe Moving Careers <${fromEmail}>`,
        to: ownerEmail,
        reply_to: data.email,
        subject: `New application — ${data.firstName} ${data.lastName} for ${data.position}`,
        html: ownerEmailHtml(data),
        text: ownerEmailText(data),
        attachments: [{ filename, content: pdfBase64 }],
      }),
    ]);
  } catch (e) {
    return json({ error: 'Email send failed', detail: String(e) }, 502, corsHeaders);
  }

  return json({ ok: true, message: 'Application received. Confirmation email on its way.' }, 200, corsHeaders);
}

// --------------------------------------------------------------------------
// PDF generation
// --------------------------------------------------------------------------

async function buildApplicationPdf(d) {
  const pdf = await PDFDocument.create();
  const page = pdf.addPage([595.28, 841.89]); // A4
  const font = await pdf.embedFont(StandardFonts.Helvetica);
  const bold = await pdf.embedFont(StandardFonts.HelveticaBold);

  const navy = rgb(0.075, 0.027, 0.384);    // #130762
  const magenta = rgb(0.741, 0.169, 0.439); // #bd2b70
  const grey = rgb(0.4, 0.4, 0.4);

  let y = 800;
  const left = 50;
  const right = 545;

  // Header bar
  page.drawRectangle({ x: 0, y: 800, width: 595.28, height: 41.89, color: navy });
  page.drawText('Mark Ratcliffe Moving & Storage', { x: left, y: 815, font: bold, size: 14, color: rgb(1, 1, 1) });
  page.drawText('Job Application', { x: right - 110, y: 815, font: font, size: 12, color: rgb(1, 1, 1) });

  y = 770;
  page.drawText(`Submitted: ${new Date().toUTCString()}`, { x: left, y, font, size: 9, color: grey });

  y -= 30;
  drawSection(page, bold, 'PERSONAL', y, magenta); y -= 20;
  y = drawRow(page, font, bold, left, y, 'Full name',     `${d.firstName} ${d.lastName}`);
  y = drawRow(page, font, bold, left, y, 'Email',         d.email);
  y = drawRow(page, font, bold, left, y, 'Phone',         d.phone);
  y = drawRow(page, font, bold, left, y, 'Address',       [d.address, d.town, d.postcode].filter(Boolean).join(', '));
  if (d.dob) y = drawRow(page, font, bold, left, y, 'Date of birth', d.dob);
  y = drawRow(page, font, bold, left, y, 'Right to work in UK', d.rightToWork);

  y -= 14;
  drawSection(page, bold, 'POSITION', y, magenta); y -= 20;
  y = drawRow(page, font, bold, left, y, 'Position',      d.position);
  if (d.positionOther) y = drawRow(page, font, bold, left, y, 'Other (specify)', d.positionOther);
  y = drawRow(page, font, bold, left, y, 'Availability',  d.availability || '—');
  y = drawRow(page, font, bold, left, y, 'Earliest start', d.startDate || '—');

  y -= 14;
  drawSection(page, bold, 'DRIVING', y, magenta); y -= 20;
  y = drawRow(page, font, bold, left, y, 'Driving licence', d.licence || '—');
  y = drawRow(page, font, bold, left, y, 'Licence categories', Array.isArray(d.licenceCats) ? d.licenceCats.join(', ') : (d.licenceCats || '—'));
  y = drawRow(page, font, bold, left, y, 'Years driving',  d.yearsDriving || '—');

  y -= 14;
  drawSection(page, bold, 'EXPERIENCE', y, magenta); y -= 20;
  y = drawRow(page, font, bold, left, y, 'Years in removals', d.yearsRemovals || '—');
  y = drawWrappedRow(page, font, bold, left, y, 'Previous experience', d.experience || '—', 480);
  y = drawWrappedRow(page, font, bold, left, y, 'Why this role',       d.whyRole || '—', 480);

  y -= 14;
  drawSection(page, bold, 'CONSENTS', y, magenta); y -= 20;
  y = drawRow(page, font, bold, left, y, 'GDPR consent',  d.gdprConsent ? 'Yes' : 'No');
  y = drawRow(page, font, bold, left, y, 'Marketing opt-in', d.marketingOptIn ? 'Yes' : 'No');

  // Footer
  page.drawLine({ start: { x: left, y: 50 }, end: { x: right, y: 50 }, color: grey, thickness: 0.5 });
  page.drawText('Submitted via markratcliffemoving.co.uk/careers', { x: left, y: 35, font, size: 8, color: grey });
  page.drawText('EMV London Ltd t/a Mark Ratcliffe Moving & Storage', { x: left, y: 22, font, size: 8, color: grey });

  return await pdf.save();
}

function drawSection(page, font, label, y, color) {
  page.drawText(label, { x: 50, y, font, size: 10, color });
  page.drawLine({ start: { x: 120, y: y + 3 }, end: { x: 545, y: y + 3 }, color, thickness: 0.5 });
}

function drawRow(page, font, bold, x, y, label, value) {
  page.drawText(label + ':', { x, y, font: bold, size: 10 });
  page.drawText(String(value || '—'), { x: x + 130, y, font, size: 10 });
  return y - 16;
}

function drawWrappedRow(page, font, bold, x, y, label, value, maxWidth) {
  page.drawText(label + ':', { x, y, font: bold, size: 10 });
  const lines = wordWrap(String(value || '—'), font, 10, maxWidth - 130);
  let cy = y;
  for (const line of lines) {
    page.drawText(line, { x: x + 130, y: cy, font, size: 10 });
    cy -= 14;
  }
  return cy - 4;
}

function wordWrap(text, font, size, maxWidth) {
  const words = text.split(/\s+/);
  const lines = [];
  let cur = '';
  for (const w of words) {
    const test = cur ? cur + ' ' + w : w;
    if (font.widthOfTextAtSize(test, size) > maxWidth) {
      if (cur) lines.push(cur);
      cur = w;
    } else {
      cur = test;
    }
  }
  if (cur) lines.push(cur);
  return lines;
}

// --------------------------------------------------------------------------
// Email helpers
// --------------------------------------------------------------------------

async function sendEmail(apiKey, payload) {
  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    throw new Error(`Resend ${res.status}: ${await res.text()}`);
  }
  return res.json();
}

function applicantEmailHtml(d) {
  return `<!doctype html><html><body style="font-family:Arial,sans-serif;color:#130762;max-width:600px;margin:0 auto;padding:24px;">
    <h1 style="color:#130762;font-family:Georgia,serif;font-size:22px;">Thank you for your application, ${esc(d.firstName)}</h1>
    <p>We have received your application for the role of <strong>${esc(d.position)}</strong> at Mark Ratcliffe Moving &amp; Storage.</p>
    <p>A copy of your application is attached as a PDF for your records. We aim to review every application within 5 working days. If your experience matches what we're looking for, we'll be in touch to arrange a call or interview at our Lower Dicker depot just outside Eastbourne.</p>
    <p>If you have any questions in the meantime, reply to this email or call us on <a href="tel:01323848008" style="color:#bd2b70;">01323 848 008</a>.</p>
    <hr style="border:0;border-top:1px solid #ccc;margin:24px 0;">
    <p style="font-size:12px;color:#666;">Mark Ratcliffe Moving &amp; Storage<br>EMV London Ltd · Unit J12 Swallow Business Park, Diamond Drive, Lower Dicker BN27 4EL<br>BAR member · BS 8564 accredited · APG protected deposits</p>
  </body></html>`;
}
function applicantEmailText(d) {
  return `Thank you for your application, ${d.firstName}.\n\nWe have received your application for the role of ${d.position} at Mark Ratcliffe Moving & Storage. A copy is attached as a PDF.\n\nWe aim to review applications within 5 working days. If your experience fits, we'll be in touch to arrange a call or interview.\n\nQuestions? Reply to this email or call 01323 848 008.\n\n— Mark Ratcliffe Moving & Storage\nLower Dicker depot, BN27 4EL`;
}
function ownerEmailHtml(d) {
  return `<!doctype html><html><body style="font-family:Arial,sans-serif;color:#130762;max-width:600px;margin:0 auto;padding:24px;">
    <h1 style="color:#130762;font-family:Georgia,serif;font-size:20px;">New application — ${esc(d.position)}</h1>
    <table style="width:100%;border-collapse:collapse;font-size:14px;">
      <tr><td style="padding:6px 0;color:#666;width:140px;">Name</td><td><strong>${esc(d.firstName)} ${esc(d.lastName)}</strong></td></tr>
      <tr><td style="padding:6px 0;color:#666;">Email</td><td><a href="mailto:${esc(d.email)}" style="color:#bd2b70;">${esc(d.email)}</a></td></tr>
      <tr><td style="padding:6px 0;color:#666;">Phone</td><td><a href="tel:${esc(d.phone)}" style="color:#bd2b70;">${esc(d.phone)}</a></td></tr>
      <tr><td style="padding:6px 0;color:#666;">Postcode</td><td>${esc(d.postcode)}</td></tr>
      <tr><td style="padding:6px 0;color:#666;">Right to work UK</td><td>${esc(d.rightToWork)}</td></tr>
      <tr><td style="padding:6px 0;color:#666;">Position</td><td><strong>${esc(d.position)}</strong> ${d.positionOther ? '(' + esc(d.positionOther) + ')' : ''}</td></tr>
      <tr><td style="padding:6px 0;color:#666;">Availability</td><td>${esc(d.availability || '—')}</td></tr>
      <tr><td style="padding:6px 0;color:#666;">Earliest start</td><td>${esc(d.startDate || '—')}</td></tr>
      <tr><td style="padding:6px 0;color:#666;">Driving licence</td><td>${esc(d.licence || '—')} ${Array.isArray(d.licenceCats) ? '(' + d.licenceCats.map(esc).join(', ') + ')' : ''}</td></tr>
      <tr><td style="padding:6px 0;color:#666;">Years driving</td><td>${esc(d.yearsDriving || '—')}</td></tr>
      <tr><td style="padding:6px 0;color:#666;">Years removals</td><td>${esc(d.yearsRemovals || '—')}</td></tr>
    </table>
    <h3 style="color:#130762;margin-top:20px;">Previous experience</h3>
    <p style="white-space:pre-wrap;background:#f5f5f5;padding:12px;border-radius:4px;">${esc(d.experience || '—')}</p>
    <h3 style="color:#130762;">Why this role</h3>
    <p style="white-space:pre-wrap;background:#f5f5f5;padding:12px;border-radius:4px;">${esc(d.whyRole || '—')}</p>
    <p style="font-size:12px;color:#888;margin-top:24px;">PDF copy attached. Full application also stored in the applicant's own copy of this email.</p>
  </body></html>`;
}
function ownerEmailText(d) {
  return `New application — ${d.position}\n\nName: ${d.firstName} ${d.lastName}\nEmail: ${d.email}\nPhone: ${d.phone}\nPostcode: ${d.postcode}\nRight to work UK: ${d.rightToWork}\nPosition: ${d.position}${d.positionOther ? ' (' + d.positionOther + ')' : ''}\nAvailability: ${d.availability || '—'}\nEarliest start: ${d.startDate || '—'}\nDriving licence: ${d.licence || '—'}\nLicence categories: ${Array.isArray(d.licenceCats) ? d.licenceCats.join(', ') : '—'}\nYears driving: ${d.yearsDriving || '—'}\nYears removals: ${d.yearsRemovals || '—'}\n\nPrevious experience:\n${d.experience || '—'}\n\nWhy this role:\n${d.whyRole || '—'}\n\nPDF copy attached.`;
}
function esc(s) {
  return String(s == null ? '' : s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}

// --------------------------------------------------------------------------
// Utilities
// --------------------------------------------------------------------------

function bytesToBase64(bytes) {
  let bin = '';
  for (let i = 0; i < bytes.length; i++) bin += String.fromCharCode(bytes[i]);
  return btoa(bin);
}

function json(obj, status, extra) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { 'Content-Type': 'application/json', ...(extra || {}) },
  });
}
