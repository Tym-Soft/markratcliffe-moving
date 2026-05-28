/**
 * Careers application form handler.
 * POSTs the form as JSON to the Cloudflare worker, which generates
 * the PDF and sends two emails (applicant + owner).
 */
(function () {
  'use strict';

  // Change this if the worker is deployed to a different URL
  var ENDPOINT = 'https://markratcliffe-moving.vandymanservices.workers.dev/api/careers';

  var form = document.getElementById('careers-application-form');
  if (!form) return;

  var statusBox = document.getElementById('careers-form-status');
  var submitBtn = form.querySelector('button[type="submit"]');

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    // Honeypot — if "website" filled, treat as success without sending
    var honeypot = form.querySelector('input[name="website"]');
    if (honeypot && honeypot.value.trim() !== '') {
      showStatus('ok', 'Application received. Confirmation email on its way.');
      form.reset();
      return;
    }

    // GDPR
    var gdpr = form.querySelector('input[name="gdprConsent"]');
    if (!gdpr || !gdpr.checked) {
      showStatus('err', 'Please tick the data-protection consent box to submit.');
      gdpr && gdpr.focus();
      return;
    }

    // Collect fields
    var data = collectData(form);

    submitBtn.disabled = true;
    submitBtn.textContent = 'Sending application…';
    showStatus('info', 'Submitting your application — please wait.');

    fetch(ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
      .then(function (res) {
        return res.json().then(function (body) {
          return { status: res.status, body: body };
        });
      })
      .then(function (r) {
        if (r.status >= 200 && r.status < 300 && r.body.ok) {
          showStatus('ok', 'Thank you — your application has been received. A confirmation email with a PDF copy is on its way to you. Most applications get a reply within 5 working days.');
          form.reset();
          submitBtn.textContent = 'Application sent';
        } else {
          var msg = (r.body && r.body.error) ? r.body.error : 'Something went wrong. Please call 01323 848 008 or email office@markratcliffemoving.co.uk.';
          showStatus('err', msg);
          submitBtn.disabled = false;
          submitBtn.textContent = 'Submit application';
        }
      })
      .catch(function (err) {
        showStatus('err', 'Network error — please try again, call 01323 848 008, or email office@markratcliffemoving.co.uk.');
        submitBtn.disabled = false;
        submitBtn.textContent = 'Submit application';
      });
  });

  function collectData(form) {
    var fd = new FormData(form);
    var data = {};
    // Single-value fields
    var singles = ['firstName','lastName','email','phone','address','town','postcode','dob','rightToWork','position','positionOther','availability','startDate','licence','yearsDriving','yearsRemovals','experience','whyRole'];
    singles.forEach(function (k) { data[k] = (fd.get(k) || '').toString().trim(); });
    // Multi-select: licence categories
    data.licenceCats = fd.getAll('licenceCats');
    // Booleans
    data.gdprConsent = !!form.querySelector('input[name="gdprConsent"]:checked');
    data.marketingOptIn = !!form.querySelector('input[name="marketingOptIn"]:checked');
    // Honeypot (always present in JSON but normally empty)
    data.website = (fd.get('website') || '').toString();
    return data;
  }

  function showStatus(kind, msg) {
    if (!statusBox) return;
    statusBox.className = 'careers-form-status careers-form-status-' + kind;
    statusBox.textContent = msg;
    statusBox.style.display = 'block';
    statusBox.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }
})();
