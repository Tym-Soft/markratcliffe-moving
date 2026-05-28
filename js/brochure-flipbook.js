/**
 * Brochure viewer — Thai page.
 *
 * Flipbook on all devices. On mobile, swipe + corner-grab + click-to-flip
 * are all disabled — navigation is exclusively via the Prev/Next buttons.
 * Desktop keeps full corner-flip interaction.
 */
(function () {
  'use strict';

  var container = document.getElementById('brochure-flipbook');
  if (!container || !window.St || !window.St.PageFlip) return;

  var TOTAL = 8;
  var isMobile = window.matchMedia('(max-width: 768px)').matches;

  // Build page elements
  for (var i = 1; i <= TOTAL; i++) {
    var pn = String(i).padStart(2, '0');
    var pg = document.createElement('div');
    pg.className = 'brochure-page';
    pg.innerHTML = '<img src="../images/brochure-pages/page-' + pn + '.jpg" ' +
                   'alt="Brochure page ' + i + ' of ' + TOTAL + '" ' +
                   'loading="' + (i <= 2 ? 'eager' : 'lazy') + '">';
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
    mobileScrollSupport: true,
    // Mobile: lock out all user-gesture flipping (only Prev/Next buttons work).
    // Desktop: keep corner-grab + click-to-flip.
    swipeDistance: isMobile ? 99999 : 30,
    showPageCorners: !isMobile,
    disableFlipByClick: isMobile,
    useMouseEvents: !isMobile,
  });
  flip.loadFromHTML(container.querySelectorAll('.brochure-page'));

  // Page-turn sound (Web Audio API — synthesised paper rustle)
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

  // Prev/Next buttons + page indicator
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

  // Update the hint text per device
  var hint = document.querySelector('.brochure-flipbook-hint');
  if (hint) {
    hint.textContent = isMobile
      ? 'Use the Prev / Next buttons to turn the page.'
      : 'Click or grab the page corners to turn — a soft page-turn sound plays as you flick.';
  }
})();
