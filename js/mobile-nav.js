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

/* ---------------------------------------------------------
   Hamburger open-state — mirrors Webflow's .w--open onto <body>
   so we can hide the sticky FABs while the menu is open (they
   were intercepting taps on the menu's bottom action row).
   --------------------------------------------------------- */
(function () {
  'use strict';
  function bindOpenState() {
    var btn = document.querySelector('.menu-button.w-nav-button');
    if (!btn) return;
    function sync() {
      document.body.classList.toggle('nav-open', btn.classList.contains('w--open'));
    }
    sync();
    var mo = new MutationObserver(sync);
    mo.observe(btn, { attributes: true, attributeFilter: ['class'] });
    btn.addEventListener('click', function () { setTimeout(sync, 50); });
    btn.addEventListener('touchend', function () { setTimeout(sync, 50); });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bindOpenState);
  } else {
    bindOpenState();
  }
})();

/* ---------------------------------------------------------
   Sticky-header scroll state — adds .is-scrolled to .nav-section
   once the user has scrolled more than a few pixels.
   --------------------------------------------------------- */
(function () {
  'use strict';
  function bind() {
    var nav = document.querySelector('.nav-section');
    if (!nav) return;
    var lastState = null;
    function update() {
      var scrolled = window.scrollY > 8;
      if (scrolled === lastState) return;
      lastState = scrolled;
      nav.classList.toggle('is-scrolled', scrolled);
    }
    update();
    window.addEventListener('scroll', update, { passive: true });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bind);
  } else {
    bind();
  }
})();

/* ---------------------------------------------------------
   Active page highlighting — adds .is-active to the matching
   navbar link, and .has-active to the parent dropdown if the
   current page lives inside a dropdown menu.
   --------------------------------------------------------- */
(function () {
  'use strict';
  function fileFromHref(href) {
    if (!href) return '';
    return href.split('?')[0].split('#')[0].split('/').pop().toLowerCase();
  }
  function bind() {
    var current = fileFromHref(location.pathname) || 'index.html';
    if (current === '' || current === '/') current = 'index.html';

    var links = document.querySelectorAll(
      '.navbar .navlink, .navbar .dropdown-list a, ' +
      '.navbar .mega-menu a, .navbar .mega-col a'
    );
    links.forEach(function (link) {
      if (link.tagName !== 'A') return;
      var file = fileFromHref(link.getAttribute('href') || '');
      if (file && file === current) link.classList.add('is-active');
    });

    document.querySelectorAll('.navbar .dropdown.w-dropdown').forEach(function (drop) {
      if (drop.querySelector('a.is-active')) drop.classList.add('has-active');
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bind);
  } else {
    bind();
  }
})();

/* ---------------------------------------------------------
   Auto Table of Contents — builds itself from page H2s and
   mounts inside <aside class="np-toc-mount"></aside>.
   Skips H2s that live inside marketing/secondary sections.
   --------------------------------------------------------- */
(function () {
  'use strict';
  function slugify(text) {
    return text.toLowerCase()
      .replace(/&[a-z]+;/g, ' ')
      .replace(/[^a-z0-9\s-]/g, '')
      .replace(/\s+/g, '-')
      .replace(/-+/g, '-')
      .replace(/^-|-$/g, '');
  }
  // Sections we don't want in the TOC (they're page-furniture, not article content)
  var SKIP_SELECTOR = '.np-toc, .np-toc-mount, .np-faq, .np-related, ' +
                      '.np-cta-band, .hp-usps, .hp-process, .hp-testimonials, ' +
                      '.hp-areas, .hp-fleet, .hp-accred, .hp-cta-band, ' +
                      '.hp-blog-strip, .hp-services, .np-accred, ' +
                      '.hp-section-head, .hp-test-grid';

  function build() {
    var mount = document.querySelector('.np-toc-mount');
    if (!mount) return;
    var h2s = document.querySelectorAll('h2');
    var headings = [];
    h2s.forEach(function (h) {
      if (h.closest(SKIP_SELECTOR)) return;
      if (!h.textContent.trim()) return;
      headings.push(h);
    });
    if (headings.length < 3) {
      mount.style.display = 'none';
      return;
    }
    var used = {};
    headings.forEach(function (h) {
      if (!h.id) {
        var base = slugify(h.textContent) || 'section';
        var id = base, i = 2;
        while (used[id] || document.getElementById(id)) {
          id = base + '-' + i;
          i++;
        }
        used[id] = true;
        h.id = id;
      }
      // Give the H2 a scroll-offset so it lands clear of the sticky nav
      h.style.scrollMarginTop = '110px';
    });
    var html  = '<nav class="np-toc" aria-label="On this page">';
        html += '<button class="np-toc-toggle" type="button" aria-expanded="false">On this page</button>';
        html += '<ol>';
    headings.forEach(function (h) {
      html += '<li><a href="#' + h.id + '">' + h.textContent + '</a></li>';
    });
        html += '</ol></nav>';
    mount.innerHTML = html;

    var toc = mount.querySelector('.np-toc');
    var btn = mount.querySelector('.np-toc-toggle');
    function setOpen(open) {
      toc.classList.toggle('is-open', open);
      if (btn) btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    }
    if (btn) {
      btn.addEventListener('click', function () {
        setOpen(!toc.classList.contains('is-open'));
      });
    }
    // Open by default on tablet+, collapsed on phones (CSS-driven media)
    setOpen(window.matchMedia('(min-width: 601px)').matches);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', build);
  } else {
    build();
  }
})();
