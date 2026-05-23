/* Mark Ratcliffe Moving — homepage hero "quick estimate" widget
 *
 * Lightweight version of the full storage calculator, sized to fit
 * inside the hero. Pricing formula is replicated from
 * js/storage-calculator.js (PRICE_ANCHORS + VEHICLE_TIERS) so the
 * figure shown here is consistent with what the customer sees once
 * they click through into the full calculator.
 *
 * The CTA deep-links to /resources/storage-calculator.html with
 * bed + miles encoded as query params, so the calculator opens
 * pre-filled and the customer never re-enters what they already did.
 */
(function () {
  'use strict';
  var card = document.querySelector('.hp-hero-quote-card');
  if (!card) return;

  // Pricing constants — mirror storage-calculator.js. Keep in sync.
  var PRICE_ANCHORS = [
    [0,       0],
    [300,   300],
    [500,   500],
    [800,   650],
    [1000,  900],
    [1800, 1500],
    [2800, 2500]
  ];
  var VEHICLES = [
    { maxCuft:  800, mileRate: 2.00 },
    { maxCuft: 1500, mileRate: 2.75 },
    { maxCuft: 2500, mileRate: 4.00 },
    { maxCuft: Infinity, mileRate: 4.00 }
  ];
  var VAT_RATE = 0.20;

  function computeVolumeCost(cuft) {
    if (cuft <= PRICE_ANCHORS[0][0]) return PRICE_ANCHORS[0][1];
    for (var i = 1; i < PRICE_ANCHORS.length; i++) {
      var x1 = PRICE_ANCHORS[i - 1][0], y1 = PRICE_ANCHORS[i - 1][1];
      var x2 = PRICE_ANCHORS[i][0],     y2 = PRICE_ANCHORS[i][1];
      if (cuft <= x2) return y1 + (cuft - x1) * (y2 - y1) / (x2 - x1);
    }
    var last = PRICE_ANCHORS[PRICE_ANCHORS.length - 1];
    var prev = PRICE_ANCHORS[PRICE_ANCHORS.length - 2];
    var slope = (last[1] - prev[1]) / (last[0] - prev[0]);
    return last[1] + (cuft - last[0]) * slope;
  }
  function pickVehicle(cuft) {
    for (var i = 0; i < VEHICLES.length; i++) {
      if (cuft <= VEHICLES[i].maxCuft) return VEHICLES[i];
    }
    return VEHICLES[VEHICLES.length - 1];
  }
  function fmt(n) {
    return Number(n || 0).toLocaleString('en-GB', { minimumFractionDigits: 0, maximumFractionDigits: 0 });
  }

  var bedBtns = Array.prototype.slice.call(card.querySelectorAll('.hpqq-bed'));
  var milesInput = card.querySelector('#hpqq-miles');
  var netEl = card.querySelector('#hpqq-net-amt');
  var grossEl = card.querySelector('#hpqq-gross-amt');
  var cta = card.querySelector('#hpqq-cta');

  function activeBed() {
    var btn = card.querySelector('.hpqq-bed.is-active') || bedBtns[3]; // default 3bed
    return {
      bed: btn.dataset.bed,
      cuft: parseInt(btn.dataset.cuft, 10) || 1000
    };
  }
  function currentMiles() {
    var m = parseInt(milesInput && milesInput.value, 10);
    return (isNaN(m) || m < 0) ? 0 : m;
  }

  function recalc() {
    var ab = activeBed();
    var miles = currentMiles();
    var vol = computeVolumeCost(ab.cuft);
    var vehicle = pickVehicle(ab.cuft);
    var net = vol + miles * vehicle.mileRate;
    var gross = net * (1 + VAT_RATE);
    if (netEl)   netEl.textContent   = fmt(net);
    if (grossEl) grossEl.textContent = fmt(gross);
    if (cta) {
      cta.href = 'resources/storage-calculator.html?bed=' + encodeURIComponent(ab.bed) +
                 '&miles=' + encodeURIComponent(miles);
    }
  }

  bedBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      bedBtns.forEach(function (b) {
        b.classList.remove('is-active');
        b.setAttribute('aria-pressed', 'false');
      });
      btn.classList.add('is-active');
      btn.setAttribute('aria-pressed', 'true');
      recalc();
    });
  });

  if (milesInput) {
    milesInput.addEventListener('input', recalc);
    milesInput.addEventListener('change', recalc);
  }

  recalc();
})();
