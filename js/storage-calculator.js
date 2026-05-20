/* Mark Ratcliffe Moving — storage calculator
 *
 * Handles:
 *   • Tab switching (one room visible at a time)
 *   • Search input filters items inside the active tab by name
 *   • − / + stepper buttons mutate each item's quantity input
 *   • Recalculates totals (cu ft, cu m, kg) and the load-size band
 *
 * Served from 'self' so the page CSP allows it.
 */
(function () {
  'use strict';
  var root = document.getElementById('storage-calc');
  if (!root) return;

  var tabs        = Array.prototype.slice.call(root.querySelectorAll('.calc-tab'));
  var panels      = Array.prototype.slice.call(root.querySelectorAll('.calc-cat-panel'));
  var searchInput = document.getElementById('calc-search-input');
  var inputs      = Array.prototype.slice.call(root.querySelectorAll('input[type="number"][data-cuft]'));
  var totalCuft   = document.getElementById('total-cuft');
  var totalCum    = document.getElementById('total-cum');
  var totalKg     = document.getElementById('total-kg');
  var vanEstimate = document.getElementById('van-estimate');
  var resetBtn    = document.getElementById('calc-reset');

  // Cost estimator elements
  var milesInput   = document.getElementById('cost-miles');
  var costVehicle  = document.getElementById('cost-vehicle');
  var costVolume   = document.getElementById('cost-volume');
  var costMileage  = document.getElementById('cost-mileage');
  var costMinimum  = document.getElementById('cost-minimum');
  var costTotal    = document.getElementById('cost-total');

  // Storage-unit price list (sqft, weekly rate inc VAT & insurance).
  // Source: Mark Ratcliffe Moving Prestige steel storage rate table.
  var STORAGE_UNITS = [
    { sqft:  25, weekly:  2.59 },
    { sqft:  30, weekly:  3.02 },
    { sqft:  40, weekly:  4.50 },
    { sqft:  50, weekly:  5.96 },
    { sqft:  60, weekly:  6.48 },
    { sqft:  65, weekly:  7.44 },
    { sqft:  75, weekly:  8.90 },
    { sqft: 100, weekly: 11.93 },
    { sqft: 120, weekly: 13.68 },
    { sqft: 145, weekly: 15.54 },
    { sqft: 200, weekly: 21.60 },
    { sqft: 280, weekly: 24.48 }
  ];
  // Lower-ceiling 75 sqft room (cheaper than the standard 75). Shown as a
  // side-by-side option whenever the auto-picker lands on the 75 sqft band
  // — the customer can pick the lower-ceiling option if their contents
  // won't stack high.
  var STORAGE_LOW_CEILING_75 = { sqft: 75, weekly: 6.91, label: '75 sqft low-ceiling' };
  var STORAGE_CUFT_PER_SQFT = 7; // packing efficiency: 7 cu ft per sqft of floor

  var storageEnabled    = document.getElementById('storage-enabled');
  var storageWeeksInput = document.getElementById('storage-weeks');
  var storageDetails    = document.getElementById('storage-details');
  var storageUnitEl     = document.getElementById('storage-unit');
  var storageWeeklyEl   = document.getElementById('storage-weekly');
  var storageTotalEl    = document.getElementById('storage-total');
  var grandTotalRow     = document.getElementById('cost-grand-total');
  var grandTotalValue   = document.getElementById('cost-grand-total-value');

  function pickStorageUnit(cuft) {
    var sqftNeeded = Math.ceil(cuft / STORAGE_CUFT_PER_SQFT);
    for (var i = 0; i < STORAGE_UNITS.length; i++) {
      if (STORAGE_UNITS[i].sqft >= sqftNeeded) return STORAGE_UNITS[i];
    }
    return STORAGE_UNITS[STORAGE_UNITS.length - 1]; // bigger than largest — flag this
  }

  // Per-home-size pricing profile. The chosen home size drives the
  // vehicle, the £/cu ft rate, the per-mile mileage rate AND the
  // minimum charge — Mark Ratcliffe Moving's published pricing model.
  //
  // Vehicle mapping (per the rate sheet):
  //   Small  →  Luton Van (3.5t)
  //   Medium →  7.5 – 18 Tonne Lorry
  //   Large  →  18 Tonne+ / 44 Tonne Artic
  var HOME_PROFILES = {
    small: {
      vehicle:   'Luton Van (3.5t)',
      rate:      2.25,   // £/cu ft (mid of £2.00–£2.50)
      mileRate:  2.00,   // £/mile
      minCharge: 360
    },
    medium: {
      vehicle:   '7.5 – 18 Tonne Lorry',
      rate:      1.60,   // £/cu ft (mid of £1.40–£1.80)
      mileRate:  2.75,   // £/mile (mid of 7.5t £2.50 and 18t £3.00)
      minCharge: 650
    },
    large: {
      vehicle:   '18 Tonne+ / Artic',
      rate:      1.30,   // £/cu ft (covers 18-26T and artic)
      mileRate:  3.50,   // £/mile (mid of £3.00 and £4.00)
      minCharge: 1000
    }
  };

  function pounds(n) {
    return '£' + Math.round(n).toLocaleString('en-GB');
  }

  // Friendly labels for home sizes (used in headline + emails).
  var HOME_SIZE_LABEL = {
    small:  '1-bed flat / studio',
    medium: '2-3 bed home',
    large:  '4+ bed / antiques / country property'
  };

  function getHomeSize() {
    var checked = document.querySelector('input[name="home-size"]:checked');
    return checked ? checked.value : 'medium';
  }

  function getCalcMode() {
    var checked = document.querySelector('input[name="calc-mode"]:checked');
    return checked ? checked.value : 'both';
  }

  function applyCalcMode() {
    var mode = getCalcMode();
    document.body.setAttribute('data-calc-mode', mode);
    // Storage is implied by both 'storage' and 'both' — auto-check the
    // checkbox and reveal the details panel so the redundant "Do you also
    // need storage?" question doesn't appear in either mode.
    if (storageEnabled && storageDetails) {
      if (mode === 'storage' || mode === 'both') {
        storageEnabled.checked = true;
        storageDetails.hidden = false;
      } else {
        storageEnabled.checked = false;
        storageDetails.hidden = true;
      }
    }
    recalc();
  }

  function loadSizeLabel(cuft) {
    if (cuft === 0)    return 'No items selected';
    if (cuft <= 600)   return '~ Luton Van (3.5t) load';
    if (cuft <= 1100)  return '~ 7.5 Tonne Lorry load';
    if (cuft <= 2000)  return '~ 18–26 Tonne Rigid load';
    return '~ 44 Tonne Artic load';
  }

  function recalc() {
    var cuft = 0, cum = 0, kg = 0;
    for (var i = 0; i < inputs.length; i++) {
      var q = parseInt(inputs[i].value, 10);
      if (!q || q < 0) continue;
      cuft += q * parseFloat(inputs[i].dataset.cuft);
      cum  += q * parseFloat(inputs[i].dataset.cum);
      kg   += q * parseFloat(inputs[i].dataset.kg);
    }
    var roundedCuft = Math.round(cuft);
    totalCuft.textContent   = roundedCuft;
    totalCum.textContent    = cum.toFixed(2);
    totalKg.textContent     = Math.round(kg);
    vanEstimate.textContent = loadSizeLabel(roundedCuft);
    recalcCost(roundedCuft);
  }

  function recalcCost(cuft) {
    if (!costVehicle) return;
    var miles = parseInt((milesInput && milesInput.value) || '0', 10);
    if (isNaN(miles) || miles < 0) miles = 0;

    var size     = getHomeSize();
    var profile  = HOME_PROFILES[size] || HOME_PROFILES.medium;
    var sizeText = size.charAt(0).toUpperCase() + size.slice(1);
    var headlineLabel = document.getElementById('cost-headline-label');

    var volCost  = cuft * profile.rate;
    var mileCost = miles * profile.mileRate;
    var base     = Math.max(profile.minCharge, volCost);
    var total    = base + mileCost;

    costVehicle.textContent = profile.vehicle;
    costVolume.textContent  = cuft === 0
      ? '£0 (tick items above)'
      : pounds(volCost) + ' (' + cuft + ' cu ft × £' + profile.rate.toFixed(2) + '/cu ft)';
    costMileage.textContent = pounds(mileCost) + ' (' + miles + ' mi × £' + profile.mileRate.toFixed(2) + '/mi)';
    costMinimum.textContent = pounds(profile.minCharge) + ' (' + sizeText + ' home)';
    costTotal.textContent   = pounds(total);

    if (headlineLabel) {
      headlineLabel.textContent = cuft === 0
        ? sizeText + ' home minimum · ' + miles + ' mi'
        : 'Estimated removals cost · ' + sizeText + ' home, ' + miles + ' mi';
    }

    updateStorage(cuft, total);
  }

  function updateStorage(cuft, removalsTotal) {
    if (!storageEnabled || !storageDetails) return;
    var enabled = storageEnabled.checked;
    storageDetails.hidden = !enabled;

    if (!enabled) {
      if (grandTotalRow) grandTotalRow.hidden = true;
      return;
    }

    var weeks = parseInt((storageWeeksInput && storageWeeksInput.value) || '0', 10);
    if (isNaN(weeks) || weeks < 0) weeks = 0;

    if (cuft === 0) {
      storageUnitEl.textContent = 'Select items first to see your unit size';
      storageWeeklyEl.textContent = '£0.00';
      storageTotalEl.textContent  = '£0.00';
      if (grandTotalRow) grandTotalRow.hidden = true;
      return;
    }

    var unit = pickStorageUnit(cuft);
    var storageTotal = unit.weekly * weeks;
    var sqftNeeded   = Math.ceil(cuft / STORAGE_CUFT_PER_SQFT);
    var biggerNote   = (sqftNeeded > unit.sqft) ? ' (or split across multiple ' + unit.sqft + ' sqft rooms)' : '';

    storageUnitEl.textContent   = unit.sqft + ' sqft Prestige steel room' + biggerNote;
    storageWeeklyEl.textContent = '£' + unit.weekly.toFixed(2);
    storageTotalEl.textContent  = '£' + storageTotal.toFixed(2);

    var storageLabel = document.getElementById('storage-headline-label');
    if (storageLabel) {
      storageLabel.textContent = 'Estimated storage cost · ' + weeks + ' weeks, ' + unit.sqft + ' sqft room';
    }

    if (grandTotalRow && grandTotalValue) {
      grandTotalValue.textContent = pounds(removalsTotal + storageTotal);
      grandTotalRow.hidden = false;
    }
  }

  function activateTab(targetId) {
    tabs.forEach(function (t) {
      var on = t.dataset.target === targetId;
      t.classList.toggle('active', on);
      t.setAttribute('aria-selected', on ? 'true' : 'false');
    });
    panels.forEach(function (p) {
      p.classList.toggle('active', p.id === targetId);
    });
    if (searchInput) {
      searchInput.value = '';
      filterItems('');
      var label = 'items';
      tabs.forEach(function (t) {
        if (t.dataset.target === targetId) {
          var lab = t.querySelector('.calc-tab-label');
          if (lab) label = lab.textContent;
        }
      });
      searchInput.placeholder = 'Search ' + label;
    }
    // Scroll the active tab into view in the horizontal bar
    var activeTab = tabs.find ? tabs.find(function (t) { return t.dataset.target === targetId; })
                              : (function () {
                                  for (var i = 0; i < tabs.length; i++) if (tabs[i].dataset.target === targetId) return tabs[i];
                                  return null;
                                })();
    if (activeTab && activeTab.scrollIntoView) {
      activeTab.scrollIntoView({ behavior: 'smooth', inline: 'center', block: 'nearest' });
    }
  }

  function filterItems(query) {
    var q = query.trim().toLowerCase();
    var activePanel = root.querySelector('.calc-cat-panel.active');
    if (!activePanel) return;
    var items = activePanel.querySelectorAll('.calc-item');
    for (var i = 0; i < items.length; i++) {
      var nameEl = items[i].querySelector('.calc-item-name');
      var name   = nameEl ? nameEl.textContent.toLowerCase() : '';
      var match  = !q || name.indexOf(q) !== -1;
      items[i].style.display = match ? '' : 'none';
    }
  }

  // Tab clicks
  tabs.forEach(function (tab) {
    tab.addEventListener('click', function () {
      activateTab(tab.dataset.target);
    });
    tab.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        activateTab(tab.dataset.target);
      }
    });
  });

  // Search input
  if (searchInput) {
    searchInput.addEventListener('input', function () {
      filterItems(searchInput.value);
    });
  }

  // Stepper buttons
  var steppers = root.querySelectorAll('.qty-stepper');
  for (var s = 0; s < steppers.length; s++) {
    (function (stepper) {
      var input = stepper.querySelector('input[type="number"]');
      var dec   = stepper.querySelector('.qty-dec');
      var inc   = stepper.querySelector('.qty-inc');
      if (dec) dec.addEventListener('click', function () {
        var v = parseInt(input.value, 10) || 0;
        input.value = Math.max(0, v - 1);
        recalc();
      });
      if (inc) inc.addEventListener('click', function () {
        var v = parseInt(input.value, 10) || 0;
        input.value = v + 1;
        recalc();
      });
    })(steppers[s]);
  }

  // Manual input
  inputs.forEach(function (input) {
    input.addEventListener('input', recalc);
    input.addEventListener('change', recalc);
  });

  // Reset
  if (resetBtn) {
    resetBtn.addEventListener('click', function () {
      inputs.forEach(function (input) { input.value = 0; });
      recalc();
    });
  }

  // Miles input
  if (milesInput) {
    milesInput.addEventListener('input', recalc);
    milesInput.addEventListener('change', recalc);
  }

  // Calculator-mode radios (Removals only / Storage only / Both)
  var calcModeRadios = document.querySelectorAll('input[name="calc-mode"]');
  for (var cm = 0; cm < calcModeRadios.length; cm++) {
    calcModeRadios[cm].addEventListener('change', applyCalcMode);
  }
  // Apply the initial mode on load so the right sections show
  applyCalcMode();

  // Home size radios
  var homeSizeRadios = document.querySelectorAll('input[name="home-size"]');
  for (var hs = 0; hs < homeSizeRadios.length; hs++) {
    homeSizeRadios[hs].addEventListener('change', recalc);
  }

  // Storage toggle + weeks
  if (storageEnabled)    storageEnabled.addEventListener('change', recalc);
  if (storageWeeksInput) {
    storageWeeksInput.addEventListener('input', recalc);
    storageWeeksInput.addEventListener('change', recalc);
  }

  // Quote request form — build a pre-filled mailto: with all the
  // calculator output + the customer's contact details.
  var quoteForm = document.getElementById('quote-request-form');
  if (quoteForm) {
    quoteForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var email   = document.getElementById('qf-email').value.trim();
      var phone   = document.getElementById('qf-phone').value.trim();
      var fromPC  = document.getElementById('qf-from').value.trim().toUpperCase();
      var toPC    = document.getElementById('qf-to').value.trim().toUpperCase();
      var notes   = document.getElementById('qf-notes').value.trim();
      var status  = document.getElementById('qf-status');

      var cuft        = (totalCuft  && totalCuft.textContent)  || '0';
      var cum         = (totalCum   && totalCum.textContent)   || '0';
      var kg          = (totalKg    && totalKg.textContent)    || '0';
      var van         = (vanEstimate && vanEstimate.textContent) || '';
      var vehicle     = (costVehicle && costVehicle.textContent) || '';
      var volumeCost  = (costVolume && costVolume.textContent) || '';
      var mileageCost = (costMileage && costMileage.textContent) || '';
      var minimumCost = (costMinimum && costMinimum.textContent) || '';
      var totalCost   = (costTotal && costTotal.textContent) || '';
      var miles       = (milesInput && milesInput.value) || '0';

      // Storage details (if enabled)
      var storageWanted = !!(storageEnabled && storageEnabled.checked);
      var storageWeeks  = parseInt((storageWeeksInput && storageWeeksInput.value) || '0', 10);
      var storageUnitTxt   = (storageUnitEl && storageUnitEl.textContent) || '';
      var storageWeeklyTxt = (storageWeeklyEl && storageWeeklyEl.textContent) || '';
      var storageTotalTxt  = (storageTotalEl && storageTotalEl.textContent) || '';
      var grandTotalTxt    = (grandTotalValue && grandTotalValue.textContent) || '';

      var picked = [];
      var anyItems = false;
      for (var i = 0; i < inputs.length; i++) {
        var q = parseInt(inputs[i].value, 10);
        if (!q || q < 0) continue;
        anyItems = true;
        var item = inputs[i].closest('.calc-item');
        var nameEl = item ? item.querySelector('.calc-item-name') : null;
        var name = nameEl ? nameEl.textContent : 'Item';
        picked.push('  - ' + q + ' x ' + name);
      }
      if (!anyItems) picked.push('  (no items selected on the calculator)');

      var calcMode = getCalcMode();
      var modeLabel = calcMode === 'storage' ? 'Storage only'
                    : calcMode === 'removals' ? 'Removals only'
                    : 'Removals + storage';
      var subjectParts = [modeLabel + ' quote request', cuft + ' cu ft', fromPC + ' -> ' + toPC];
      var subject = subjectParts.join(' | ');

      var body = [
        'Hi Mark Ratcliffe Moving,',
        '',
        'Please prepare a quote for my move.',
        '',
        'CONTACT',
        '  Email: ' + email,
        '  Phone: ' + phone,
        '  Moving from postcode: ' + fromPC,
        '  Moving to postcode:   ' + toPC,
        '',
        'CALCULATOR TOTALS',
        '  Quote type:    ' + modeLabel,
        '  Volume:        ' + cuft + ' cu ft (' + cum + ' cu m / ' + kg + ' kg)',
        '  Load size:     ' + van,
        ''
      ];
      if (calcMode !== 'storage') {
        body.push('ESTIMATED REMOVALS COST');
        body.push('  Vehicle band:    ' + vehicle);
        body.push('  Home size:       ' + getHomeSize());
        body.push('  Distance:        ' + miles + ' miles');
        body.push('  Volume cost:     ' + volumeCost);
        body.push('  Mileage cost:    ' + mileageCost);
        body.push('  Minimum charge:  ' + minimumCost);
        body.push('  Removals total:  ' + totalCost);
        body.push('');
      }
      if (storageWanted) {
        body.push('STORAGE REQUIRED');
        body.push('  Unit:            ' + storageUnitTxt);
        body.push('  Weekly rate:     ' + storageWeeklyTxt + ' (inc VAT & insurance)');
        body.push('  Duration:        ' + storageWeeks + ' weeks');
        body.push('  Storage total:   ' + storageTotalTxt);
        body.push('  Grand total:     ' + grandTotalTxt + ' (removals + storage)');
        body.push('');
      } else {
        body.push('STORAGE: not required');
        body.push('');
      }
      body.push('ITEMS SELECTED');
      body.push(picked.join('\n'));
      body.push('');
      if (notes) {
        body.push('NOTES');
        body.push('  ' + notes.split('\n').join('\n  '));
        body.push('');
      }
      body.push('Sent from the Mark Ratcliffe Moving online removals calculator.');

      var mailto =
        'mailto:office@markratcliffemoving.co.uk?subject=' +
        encodeURIComponent(subject) +
        '&body=' +
        encodeURIComponent(body.join('\n'));

      if (status) {
        status.textContent = 'Opening your email app... if nothing happens, email office@markratcliffemoving.co.uk and we will fill in the details from your message.';
      }
      window.location.href = mailto;
    });
  }

  recalc();
})();
