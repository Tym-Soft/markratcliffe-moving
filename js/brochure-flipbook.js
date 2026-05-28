/**
 * Brochure viewer — Thai page.
 *
 * - Desktop / tablet (≥769px): StPageFlip flipbook with page-turn
 *   sound + prev/next controls + corner-flip interaction.
 * - Mobile (≤768px): simple vertical stack of the 8 page images.
 *   The flipbook's tiny pages and corner-flip UX don't work well
 *   on a phone screen, so we render the brochure as readable
 *   full-width images you can scroll and pinch-zoom.
 */
(function () {
  'use strict';

  var container = document.getElementById('brochure-flipbook');
  if (!container) return;

  var TOTAL = 8;
  var isMobile = window.matchMedia('(max-width: 768px)').matches;

  // --------------------------------------------------------------
  // Mobile path: simple vertical stack
  // --------------------------------------------------------------
  if (isMobile) {
    container.classList.add('brochure-mobile-stack');
    container.innerHTML = '';
    for (var i = 1; i <= TOTAL; i++) {
      var pn = String(i).padStart(2, '0');
      var fig = document.createElement('figure');
      fig.className = 'brochure-mobile-page';
      fig.innerHTML =
        '<img src="../images/brochure-pages/page-' + pn + '.jpg" ' +
        'alt="Brochure page ' + i + ' of ' + TOTAL + '" ' +
        'loading="' + (i <= 2 ? 'eager' : 'lazy') + '">' +
        '<figcaption>Page ' + i + ' of ' + TOTAL + '</figcaption>';
      container.appendChild(fig);
    }
    // Hide the flipbook prev/next controls + indicator on mobile;
    // the page-count is now per-image and scroll is the navigation.
    var ctl = document.querySelector('.brochure-flipbook-controls');
    var hint = document.querySelector('.brochure-flipbook-hint');
    if (ctl) ctl.style.display = 'none';
    if (hint) hint.textContent = 'Scroll to read · pinch to zoom · download button below for the full PDF';
    return;
  }

  // --------------------------------------------------------------
  // Desktop / tablet path: StPageFlip flipbook
  // --------------------------------------------------------------
  if (!window.St || !window.St.PageFlip) return;

  for (var j = 1; j <= TOTAL; j++) {
    var pnj = String(j).padStart(2, '0');
    var pg = document.createElement('div');
    pg.className = 'brochure-page';
    pg.innerHTML = '<img src="../images/brochure-pages/page-' + pnj + '.jpg" ' +
                   'alt="Brochure page ' + j + ' of ' + TOTAL + '" ' +
                   'loading="' + (j <= 2 ? 'eager' : 'lazy') + '">';
    container.appendChild(pg);
  }

  var flip = new St.PageFlip(container, {
    width: 320,
    height: 678,
    size: 'stretch',
    minWidth: 220,
    maxWidth: 440,
    minHeight: 460,
    maxHeight: 920,
    drawShadow: true,
    flippingTime: 600,
    usePortrait: true,
    startZIndex: 0,
    autoSize: true,
    maxShadowOpacity: 0.4,
    showCover: false,
    mobileScrollSupport: false,
    swipeDistance: 30,
    showPageCorners: true,
    disableFlipByClick: false,
  });
  flip.loadFromHTML(container.querySelectorAll('.brochure-page'));

  // Synthesised page-turn sound
  var AudioCtx = window.AudioContext || window.webkitAudioContext;
  var audioCtx = null;
  function ensureAudio() {
    if (!audioCtx && AudioCtx) {
      try { audioCtx = new AudioCtx(); } catch (e) {}
    }
    return audioCtx;
  }
  function playFlipSound() {
    var ctx = ensureAudio();
    if (!ctx) return;
    if (ctx.state === 'suspended') ctx.resume();
    var now = ctx.currentTime;
    var bufSize = ctx.sampleRate * 0.25;
    var buffer = ctx.createBuffer(1, bufSize, ctx.sampleRate);
    var data = buffer.getChannelData(0);
    for (var i = 0; i < bufSize; i++) data[i] = (Math.random() * 2 - 1) * 0.5;
    var src = ctx.createBufferSource();
    src.buffer = buffer;
    var filter = ctx.createBiquadFilter();
    filter.type = 'bandpass';
    filter.Q.value = 1.2;
    filter.frequency.setValueAtTime(4500, now);
    filter.frequency.exponentialRampToValueAtTime(800, now + 0.20);
    var gain = ctx.createGain();
    gain.gain.setValueAtTime(0, now);
    gain.gain.linearRampToValueAtTime(0.18, now + 0.02);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.22);
    src.connect(filter); filter.connect(gain); gain.connect(ctx.destination);
    src.start(now); src.stop(now + 0.25);
  }
  flip.on('flip', playFlipSound);
  container.addEventListener('click', ensureAudio, { once: true });
  container.addEventListener('touchstart', ensureAudio, { once: true, passive: true });

  // Prev/Next + page indicator
  var prevBtn = document.getElementById('brochure-prev');
  var nextBtn = document.getElementById('brochure-next');
  var pageInd = document.getElementById('brochure-page-indicator');
  if (prevBtn) prevBtn.addEventListener('click', function () { flip.flipPrev(); });
  if (nextBtn) nextBtn.addEventListener('click', function () { flip.flipNext(); });
  function updateIndicator() {
    if (!pageInd) return;
    var cur = flip.getCurrentPageIndex() + 1;
    pageInd.textContent = 'Page ' + cur + ' of ' + TOTAL;
  }
  flip.on('flip', updateIndicator);
  updateIndicator();
})();
