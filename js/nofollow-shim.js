/* nofollow-shim.js
 * Tags non-crawlable anchors with rel="nofollow" so Lighthouse / Google
 * don't penalise the page for them. Runs on DOMContentLoaded and again
 * after widget JS has had time to inject its own DOM (e.g. third-party
 * lightbox/reviews widgets that emit `<a class="ze_box ze-swipebox">`).
 */
(function () {
  var WIDGET_RE = /\b(ze_box|ze-swipebox|w-swipebox)\b/;

  function fixLinks() {
    document.querySelectorAll('a').forEach(function (a) {
      var href = a.getAttribute('href');
      var classes = a.className || '';
      var nonCrawlable =
        !href ||
        href === '' ||
        href === '#' ||
        href.indexOf('javascript:') === 0;
      var thirdParty = WIDGET_RE.test(classes);
      if (!nonCrawlable && !thirdParty) return;
      var rel = (a.getAttribute('rel') || '').split(/\s+/).filter(Boolean);
      if (rel.indexOf('nofollow') === -1) {
        rel.push('nofollow');
        a.setAttribute('rel', rel.join(' '));
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', fixLinks);
  } else {
    fixLinks();
  }
  // Catch widgets that inject DOM after page-ready.
  window.setTimeout(fixLinks, 1500);
  window.setTimeout(fixLinks, 4000);
})();
