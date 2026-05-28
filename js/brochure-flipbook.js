/**
 * Brochure flipbook initialiser — Thai page.
 * - Uses StPageFlip (vanilla JS, MIT licence, vendored)
 * - 12 brochure pages rendered as JPGs in /images/brochure-pages/
 * - Page-turn sound synthesised via Web Audio API (paper rustle).
 */
(function () {
  'use strict';

  var container = document.getElementById('brochure-flipbook');
  if (!container || !window.St || !window.St.PageFlip) return;

  // Build page elements
  var TOTAL = 8;
  for (var i = 1; i <= TOTAL; i++) {
    var pn = String(i).padStart(2, '0');
    var pg = document.createElement('div');
    pg.className = 'brochure-page';
    pg.innerHTML = '<img src="../images/brochure-pages/page-' + pn + '.jpg" ' +
                   'alt="Brochure page ' + i + ' of ' + TOTAL + '" ' +
                   'loading="' + (i <= 2 ? 'eager' : 'lazy') + '">';
    container.appendChild(pg);
  }

  // Tall narrow leaflet pages: 280pt × 595pt source → aspect 2.12 (h/w).
  // 320px wide × 678px tall on desktop. StPageFlip auto-handles single
  // page on small screens via usePortrait.
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
    showCover: true,
    mobileScrollSupport: false,
    swipeDistance: 30,
    showPageCorners: true,
    disableFlipByClick: false,
  });
  flip.loadFromHTML(container.querySelectorAll('.brochure-page'));

  // Build the page-turn sound via Web Audio (paper rustle)
  // Single short noise burst with a high-pass filter swept downward.
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
    // Resume if suspended (browser autoplay policy)
    if (ctx.state === 'suspended') ctx.resume();

    var now = ctx.currentTime;
    // White-noise buffer
    var bufSize = ctx.sampleRate * 0.25;
    var buffer = ctx.createBuffer(1, bufSize, ctx.sampleRate);
    var data = buffer.getChannelData(0);
    for (var i = 0; i < bufSize; i++) {
      data[i] = (Math.random() * 2 - 1) * 0.5;
    }
    var src = ctx.createBufferSource();
    src.buffer = buffer;

    // High-pass filter starts high (sharp rustle), sweeps down (settles to soft)
    var filter = ctx.createBiquadFilter();
    filter.type = 'bandpass';
    filter.Q.value = 1.2;
    filter.frequency.setValueAtTime(4500, now);
    filter.frequency.exponentialRampToValueAtTime(800, now + 0.20);

    // Volume envelope — quick attack, soft decay
    var gain = ctx.createGain();
    gain.gain.setValueAtTime(0, now);
    gain.gain.linearRampToValueAtTime(0.18, now + 0.02);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.22);

    src.connect(filter);
    filter.connect(gain);
    gain.connect(ctx.destination);

    src.start(now);
    src.stop(now + 0.25);
  }

  // Hook the sound to the flip event
  flip.on('flip', function () { playFlipSound(); });
  // Also trigger on first user interaction so the AudioContext unlocks
  container.addEventListener('click', ensureAudio, { once: true });
  container.addEventListener('touchstart', ensureAudio, { once: true, passive: true });

  // Custom prev/next buttons
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
