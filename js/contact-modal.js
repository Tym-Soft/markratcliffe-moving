/* Mark Ratcliffe Moving — "Email us" → quote-form redirect
 *
 * Intercepts clicks on any mailto: link pointing to office@markratcliffemoving.co.uk
 * (and any element with [data-open-contact-form]) and sends the user straight
 * to the embedded iframe quote form at /mark-ratcliffe-moving-online-removals-quote.html.
 *
 * Drop-in: include `<script defer src="/js/contact-modal.js?v=…"></script>` on any
 * page where you want this behaviour. No DOM or CSS is injected.
 */
(function () {
  'use strict';

  var TARGET_URL = '/mark-ratcliffe-moving-online-removals-quote.html';
  var OFFICE_EMAIL_NEEDLE = 'office@markratcliffemoving.co.uk';

  document.addEventListener('click', function (e) {
    // Modifier-click → respect the browser's default behaviour.
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;

    var t = e.target.closest && e.target.closest('a[href^="mailto:"], [data-open-contact-form]');
    if (!t) return;

    if (t.matches && t.matches('a[href^="mailto:"]')) {
      var href = (t.getAttribute('href') || '').toLowerCase();
      if (href.indexOf(OFFICE_EMAIL_NEEDLE) === -1) return; // only intercept the office address
    }

    e.preventDefault();
    window.location.assign(TARGET_URL);
  });
})();
