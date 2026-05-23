/* Mark Ratcliffe Moving — contact modal
 *
 * Intercepts clicks on "Email us" / mailto:office@... links and opens a
 * branded contact form. Submissions POST to the same Cloudflare Worker
 * that handles the calculator quote form (with formType="contact"), so
 * the customer gets a friendly confirmation and the office gets the
 * message with Reply-To set to the customer.
 *
 * Self-contained: injects its own DOM + CSS on load. To add a manual
 * trigger, give an element data-open-contact-form (any tag works).
 */
(function () {
  'use strict';

  var WORKER_QUOTE_ENDPOINT = 'https://markratcliffe-moving.vandymanservices.workers.dev';
  var OFFICE_EMAIL_NEEDLE = 'office@markratcliffemoving.co.uk';

  // ---------- CSS ----------
  var css = '' +
    '.mrm-cf-backdrop{position:fixed;inset:0;background:rgba(15,8,33,0.72);' +
      'backdrop-filter:blur(3px);-webkit-backdrop-filter:blur(3px);z-index:10000;' +
      'display:none;align-items:flex-start;justify-content:center;padding:24px 14px;' +
      'overflow-y:auto;opacity:0;transition:opacity .18s ease;}' +
    '.mrm-cf-backdrop.is-open{display:flex;opacity:1;}' +
    '.mrm-cf-card{background:#fff;border-radius:14px;width:100%;max-width:520px;' +
      'box-shadow:0 24px 70px rgba(77,46,143,0.45);overflow:hidden;' +
      'font-family:Arial,Helvetica,sans-serif;color:#222;position:relative;' +
      'transform:translateY(12px);transition:transform .22s ease;}' +
    '.mrm-cf-backdrop.is-open .mrm-cf-card{transform:translateY(0);}' +
    '.mrm-cf-head{background:#4d2e8f;padding:18px 22px 14px;position:relative;}' +
    '.mrm-cf-head:after{content:"";display:block;height:4px;background:#C8A876;' +
      'position:absolute;left:0;right:0;bottom:0;}' +
    '.mrm-cf-title{margin:0;font-family:Georgia,"Times New Roman",serif;color:#fff;' +
      'font-size:20px;line-height:1.2;font-weight:normal;}' +
    '.mrm-cf-title b{color:#C8A876;font-weight:normal;}' +
    '.mrm-cf-sub{margin:4px 0 0;font-size:13px;color:#e6dec9;letter-spacing:.3px;}' +
    '.mrm-cf-close{position:absolute;top:10px;right:10px;width:34px;height:34px;' +
      'background:transparent;border:0;color:#fff;border-radius:6px;cursor:pointer;' +
      'font-size:22px;line-height:1;display:flex;align-items:center;justify-content:center;' +
      'transition:background .15s ease;}' +
    '.mrm-cf-close:hover,.mrm-cf-close:focus{background:rgba(255,255,255,0.12);outline:none;}' +
    '.mrm-cf-body{padding:18px 22px 22px;}' +
    '.mrm-cf-row{margin-bottom:12px;}' +
    '.mrm-cf-label{display:block;font-size:13px;font-weight:600;color:#4d2e8f;' +
      'margin-bottom:4px;letter-spacing:.2px;}' +
    '.mrm-cf-input,.mrm-cf-textarea{width:100%;box-sizing:border-box;padding:10px 12px;' +
      'border:1px solid #d4cbb5;border-radius:8px;font:inherit;font-size:15px;color:#222;' +
      'background:#fdfcf8;transition:border-color .15s ease,box-shadow .15s ease;}' +
    '.mrm-cf-input:focus,.mrm-cf-textarea:focus{outline:none;border-color:#4d2e8f;' +
      'box-shadow:0 0 0 3px rgba(77,46,143,0.18);}' +
    '.mrm-cf-textarea{min-height:120px;resize:vertical;line-height:1.5;}' +
    '.mrm-cf-actions{display:flex;gap:10px;align-items:center;margin-top:14px;flex-wrap:wrap;}' +
    '.mrm-cf-submit{background:#C8A876;color:#3a226d;border:0;border-radius:8px;' +
      'padding:12px 22px;font-weight:700;font-size:15px;letter-spacing:.3px;cursor:pointer;' +
      'transition:background .15s ease,transform .12s ease;}' +
    '.mrm-cf-submit:hover,.mrm-cf-submit:focus{background:#D6B274;outline:none;}' +
    '.mrm-cf-submit:active{transform:translateY(1px);}' +
    '.mrm-cf-submit[disabled]{opacity:.6;cursor:default;}' +
    '.mrm-cf-cancel{background:transparent;color:#4d2e8f;border:0;font-size:14px;' +
      'text-decoration:underline;cursor:pointer;padding:8px 4px;}' +
    '.mrm-cf-cancel:hover,.mrm-cf-cancel:focus{color:#3a226d;outline:none;}' +
    '.mrm-cf-status{margin:10px 0 0;font-size:14px;line-height:1.45;color:#4d2e8f;' +
      'background:#faf6e9;border:1px solid #e6dec9;border-radius:6px;padding:10px 12px;' +
      'display:none;}' +
    '.mrm-cf-status.is-error{background:#fbeeee;border-color:#e7c2c2;color:#8a2626;}' +
    '.mrm-cf-status.is-shown{display:block;}' +
    '.mrm-cf-hp{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden;}' +
    '.mrm-cf-foot{padding:0 22px 18px;font-size:12px;color:#666;line-height:1.5;}' +
    '.mrm-cf-foot a{color:#4d2e8f;text-decoration:none;}' +
    '.mrm-cf-foot a:hover{text-decoration:underline;}' +
    '@media (max-width:520px){.mrm-cf-card{border-radius:12px;}' +
      '.mrm-cf-title{font-size:18px;}.mrm-cf-head{padding:16px 18px 13px;}' +
      '.mrm-cf-body{padding:16px 18px 18px;}.mrm-cf-foot{padding:0 18px 16px;}}';

  // ---------- HTML ----------
  var html =
    '<div class="mrm-cf-card" role="dialog" aria-modal="true" aria-labelledby="mrm-cf-title">' +
      '<div class="mrm-cf-head">' +
        '<button type="button" class="mrm-cf-close" aria-label="Close">&times;</button>' +
        '<h2 class="mrm-cf-title" id="mrm-cf-title"><b>Email</b> Mark Ratcliffe Moving &amp; Storage</h2>' +
        '<p class="mrm-cf-sub">We reply within 1 working day. Need us sooner? Call 01323 848 008.</p>' +
      '</div>' +
      '<form class="mrm-cf-body" novalidate>' +
        '<div class="mrm-cf-hp"><label>Leave blank<input type="text" name="company_website" autocomplete="off" tabindex="-1"></label></div>' +
        '<div class="mrm-cf-row">' +
          '<label class="mrm-cf-label" for="mrm-cf-name">Your name</label>' +
          '<input class="mrm-cf-input" id="mrm-cf-name" name="name" type="text" autocomplete="name" required placeholder="Jane Smith">' +
        '</div>' +
        '<div class="mrm-cf-row">' +
          '<label class="mrm-cf-label" for="mrm-cf-email">Email</label>' +
          '<input class="mrm-cf-input" id="mrm-cf-email" name="email" type="email" autocomplete="email" required placeholder="you@example.com">' +
        '</div>' +
        '<div class="mrm-cf-row">' +
          '<label class="mrm-cf-label" for="mrm-cf-phone">Phone</label>' +
          '<input class="mrm-cf-input" id="mrm-cf-phone" name="phone" type="tel" autocomplete="tel" required placeholder="01234 567 890">' +
        '</div>' +
        '<div class="mrm-cf-row">' +
          '<label class="mrm-cf-label" for="mrm-cf-message">Your message</label>' +
          '<textarea class="mrm-cf-textarea" id="mrm-cf-message" name="message" required placeholder="Tell us what you need — moving date, postcodes, anything heavy or fragile, questions about storage…"></textarea>' +
        '</div>' +
        '<div class="mrm-cf-actions">' +
          '<button type="submit" class="mrm-cf-submit">Send message</button>' +
          '<button type="button" class="mrm-cf-cancel">Cancel</button>' +
        '</div>' +
        '<div class="mrm-cf-status" role="status" aria-live="polite"></div>' +
      '</form>' +
      '<div class="mrm-cf-foot">By sending, you agree we can reply to your enquiry. We won\'t share your details — see our <a href="/privacy-policy.html">privacy policy</a>.</div>' +
    '</div>';

  // ---------- Setup ----------
  var backdrop, form, statusEl, submitBtn, nameInput, lastFocus;

  function init() {
    var style = document.createElement('style');
    style.textContent = css;
    document.head.appendChild(style);

    backdrop = document.createElement('div');
    backdrop.className = 'mrm-cf-backdrop';
    backdrop.innerHTML = html;
    document.body.appendChild(backdrop);

    form = backdrop.querySelector('form');
    statusEl = backdrop.querySelector('.mrm-cf-status');
    submitBtn = backdrop.querySelector('.mrm-cf-submit');
    nameInput = backdrop.querySelector('#mrm-cf-name');

    backdrop.addEventListener('click', function (e) { if (e.target === backdrop) close(); });
    backdrop.querySelector('.mrm-cf-close').addEventListener('click', close);
    backdrop.querySelector('.mrm-cf-cancel').addEventListener('click', close);
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && backdrop.classList.contains('is-open')) close();
    });

    form.addEventListener('submit', onSubmit);

    // Intercept any "email us" link, plus explicit triggers.
    document.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a[href^="mailto:"]');
      if (a && a.getAttribute('href').toLowerCase().indexOf(OFFICE_EMAIL_NEEDLE) !== -1) {
        e.preventDefault();
        open(a);
        return;
      }
      var trig = e.target.closest && e.target.closest('[data-open-contact-form]');
      if (trig) {
        e.preventDefault();
        open(trig);
      }
    });
  }

  function open(opener) {
    lastFocus = opener || document.activeElement;
    setStatus('', '');
    backdrop.classList.add('is-open');
    document.documentElement.style.overflow = 'hidden';
    setTimeout(function () { try { nameInput.focus({ preventScroll: true }); } catch (_) { nameInput.focus(); } }, 50);
  }

  function close() {
    backdrop.classList.remove('is-open');
    document.documentElement.style.overflow = '';
    if (lastFocus && lastFocus.focus) { try { lastFocus.focus(); } catch (_) {} }
  }

  function setStatus(text, kind) {
    statusEl.className = 'mrm-cf-status' + (text ? ' is-shown' : '') + (kind === 'error' ? ' is-error' : '');
    statusEl.textContent = text;
  }

  function onSubmit(e) {
    e.preventDefault();
    var hp = form.elements['company_website'].value.trim();
    var name = form.elements['name'].value.trim();
    var email = form.elements['email'].value.trim();
    var phone = form.elements['phone'].value.trim();
    var message = form.elements['message'].value.trim();

    if (!name)    { setStatus('Please add your name.', 'error'); form.elements['name'].focus(); return; }
    if (!email)   { setStatus('Please add your email.', 'error'); form.elements['email'].focus(); return; }
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) { setStatus('That email address looks off — please check.', 'error'); form.elements['email'].focus(); return; }
    if (!phone)   { setStatus('Please add a phone number.', 'error'); form.elements['phone'].focus(); return; }
    if (!message || message.length < 5) { setStatus('Please write a short message.', 'error'); form.elements['message'].focus(); return; }

    submitBtn.disabled = true;
    var oldLabel = submitBtn.textContent;
    submitBtn.textContent = 'Sending…';
    setStatus('Sending your message…', '');

    fetch(WORKER_QUOTE_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        hp: hp,
        formType: 'contact',
        name: name,
        email: email,
        phone: phone,
        summary: message,
        subject: 'Website contact — ' + name
      })
    }).then(function (r) {
      return r.json().catch(function () { return { ok: false, error: 'Server error' }; })
        .then(function (data) { return { httpStatus: r.status, data: data }; });
    }).then(function (resp) {
      if (resp.httpStatus === 200 && resp.data && resp.data.ok) {
        form.reset();
        setStatus('Thanks ' + name.split(' ')[0] + ' — your message has been sent. A copy is on its way to ' + email + ' and we\'ll reply within 1 working day.', '');
        submitBtn.textContent = 'Sent ✓';
      } else {
        var msg = (resp.data && resp.data.error) || 'Could not send right now — please call 01323 848 008 or email office@markratcliffemoving.co.uk directly.';
        setStatus(msg, 'error');
        submitBtn.disabled = false;
        submitBtn.textContent = oldLabel;
      }
    }).catch(function () {
      setStatus('Network issue — please check your connection or call 01323 848 008.', 'error');
      submitBtn.disabled = false;
      submitBtn.textContent = oldLabel;
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
