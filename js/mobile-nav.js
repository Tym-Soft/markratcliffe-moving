/* Mobile nav helpers — independent of Webflow's runtime so dropdowns always work.
   Toggles .w--open on the parent .dropdown when its .dropdown-toggle is tapped/clicked.
   Also closes other open dropdowns when one is opened, and closes everything when
   tapping outside on desktop.
*/
(function () {
  'use strict';

  function init() {
    var toggles = document.querySelectorAll('.navbar .dropdown.w-dropdown .dropdown-toggle.w-dropdown-toggle');
    toggles.forEach(function (toggle) {
      // Avoid double-binding if Webflow also attaches
      if (toggle.__mrnInit) return;
      toggle.__mrnInit = true;

      // Make it keyboard accessible
      if (!toggle.hasAttribute('tabindex')) toggle.setAttribute('tabindex', '0');
      if (!toggle.hasAttribute('role')) toggle.setAttribute('role', 'button');
      toggle.setAttribute('aria-expanded', 'false');

      toggle.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        var parent = toggle.closest('.dropdown.w-dropdown');
        if (!parent) return;
        var isOpen = parent.classList.contains('w--open');
        // Close all other open dropdowns
        document.querySelectorAll('.navbar .dropdown.w-dropdown.w--open').forEach(function (d) {
          if (d !== parent) {
            d.classList.remove('w--open');
            var t = d.querySelector('.dropdown-toggle');
            if (t) t.setAttribute('aria-expanded', 'false');
          }
        });
        // Toggle this one
        parent.classList.toggle('w--open', !isOpen);
        toggle.setAttribute('aria-expanded', !isOpen ? 'true' : 'false');
      });

      toggle.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          toggle.click();
        }
      });
    });

    // Click outside to close
    document.addEventListener('click', function (e) {
      if (e.target.closest('.dropdown.w-dropdown')) return;
      document.querySelectorAll('.navbar .dropdown.w-dropdown.w--open').forEach(function (d) {
        d.classList.remove('w--open');
        var t = d.querySelector('.dropdown-toggle');
        if (t) t.setAttribute('aria-expanded', 'false');
      });
    });

    // --- Mobile megamenu accordion ---
    // Each .mega-col is collapsible on mobile via clicking its .mega-h header.
    document.querySelectorAll('.mega-col .mega-h').forEach(function (h) {
      if (h.__mrnAcc) return;
      h.__mrnAcc = true;
      h.setAttribute('role', 'button');
      h.setAttribute('tabindex', '0');
      h.setAttribute('aria-expanded', 'false');
      function toggleCol(e) {
        // Accordion behaviour applies on desktop AND mobile now
        e.preventDefault();
        e.stopPropagation();
        var col = h.parentElement;
        var open = col.getAttribute('data-open') === 'true';
        // Close sibling columns
        col.parentElement.querySelectorAll('.mega-col').forEach(function (c) {
          if (c !== col) {
            c.setAttribute('data-open', 'false');
            var hh = c.querySelector('.mega-h');
            if (hh) hh.setAttribute('aria-expanded', 'false');
          }
        });
        col.setAttribute('data-open', open ? 'false' : 'true');
        h.setAttribute('aria-expanded', open ? 'false' : 'true');
      }
      h.addEventListener('click', toggleCol);
      h.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') toggleCol(e);
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
