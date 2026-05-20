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

  // Storage-unit price list (sqft, daily rate inc VAT & insurance).
  // Source: Mark Ratcliffe Moving Prestige steel storage rate sheet.
  var STORAGE_UNITS = [
    { sqft:  25, daily:  2.59 },
    { sqft:  30, daily:  3.02 },
    { sqft:  40, daily:  4.50 },
    { sqft:  60, daily:  6.48 },
    { sqft:  65, daily:  7.44 },
    { sqft:  75, daily:  8.90 },
    { sqft: 120, daily: 13.68 },
    { sqft: 145, daily: 15.54 },
    { sqft: 200, daily: 21.60 },
    { sqft: 280, daily: 24.48 }
  ];
  // Lower-ceiling 75 sqft room (cheaper than the standard 75). Shown as a
  // side-by-side option whenever the auto-picker lands on the 75 sqft band
  // — the customer can pick the lower-ceiling option if their contents
  // won't stack high.
  var STORAGE_LOW_CEILING_75 = { sqft: 75, daily: 6.91, label: '75 sqft low-ceiling' };
  var STORAGE_CUFT_PER_SQFT = 7; // packing efficiency: 7 cu ft per sqft of floor

  var storageEnabled    = document.getElementById('storage-enabled');
  var storageDaysInput  = document.getElementById('storage-days');
  var storageUnitEl     = document.getElementById('storage-unit');
  var storageDailyEl    = document.getElementById('storage-daily');
  var storageTotalEl    = document.getElementById('storage-total');
  var grandTotalValue   = document.getElementById('cost-grand-total-value');

  function pickStorageUnit(cuft) {
    var sqftNeeded = Math.ceil(cuft / STORAGE_CUFT_PER_SQFT);
    for (var i = 0; i < STORAGE_UNITS.length; i++) {
      if (STORAGE_UNITS[i].sqft >= sqftNeeded) return STORAGE_UNITS[i];
    }
    return STORAGE_UNITS[STORAGE_UNITS.length - 1]; // bigger than largest — flag this
  }

  // Pricing model (single monotonic formula):
  //   • Flat base charge of £360 covers the first 500 cu ft (any vehicle).
  //   • Every cu ft above 500 adds £1.61 — price rises continuously with
  //     cu ft, no plateaus, no tier discontinuities.
  //   • Vehicle is auto-picked by cu ft for naming + mileage rate only.
  //   • Volume cost = BASE + max(0, cuft − BASE_INCLUDED) × EXCESS_RATE
  //   • Total       = volume cost + miles × picked-vehicle mile rate
  var BASE_CHARGE   = 500;
  var BASE_INCLUDED = 500;
  var EXCESS_RATE   = 1.61;
  var VEHICLE_TIERS = [
    { name: 'Luton Van (3.5t)', maxCuft:  800, mileRate: 2.00 },
    { name: '7.5 Tonne Lorry',  maxCuft: 1500, mileRate: 2.75 },
    { name: '18 Tonne Lorry',   maxCuft: 2500, mileRate: 4.00 },
    { name: '44 Tonne Artic',   maxCuft: Infinity, mileRate: 4.00 }
  ];

  // Bedroom presets — auto-fill the LOWER bound of each property's
  // typical cu ft range so the headline £ figure starts at the cheapest
  // possible estimate. The customer can drag the cu ft figure higher.
  var BED_DEFAULTS = {
    '1bed': { label: '1-bed flat or studio',         typicalCuft:  100 },
    '2bed': { label: '2-bed home',                   typicalCuft:  800 },
    '3bed': { label: '3-bed home',                   typicalCuft: 1200 },
    '4bed': { label: '4-bed home',                   typicalCuft: 1800 },
    '5bed': { label: '5+ bed / antiques / country',  typicalCuft: 2800 }
  };

  function computeVolumeCost(cuft) {
    var excess = Math.max(0, cuft - BASE_INCLUDED);
    return BASE_CHARGE + excess * EXCESS_RATE;
  }
  function pickVehicle(cuft) {
    for (var i = 0; i < VEHICLE_TIERS.length; i++) {
      if (cuft <= VEHICLE_TIERS[i].maxCuft) return VEHICLE_TIERS[i];
    }
    return VEHICLE_TIERS[VEHICLE_TIERS.length - 1];
  }
  // BED_INVENTORY is emitted by the Python generator as inline JS just
  // before this script loads. Each entry maps "item-<slug>" → quantity.
  var BED_INVENTORY_DATA = (typeof BED_INVENTORY !== 'undefined') ? BED_INVENTORY : {};

  function pounds(n) {
    return '£' + Math.round(n).toLocaleString('en-GB');
  }

  function getBed() {
    var size = getHomeSize();
    return BED_DEFAULTS[size] || BED_DEFAULTS['3bed'];
  }

  function getHomeSize() {
    var checked = document.querySelector('input[name="home-size"]:checked');
    return checked ? checked.value : '3bed';
  }

  function getCalcMode() {
    var checked = document.querySelector('input[name="calc-mode"]:checked');
    return checked ? checked.value : 'removals';
  }

  function applyCalcMode() {
    var mode = getCalcMode();
    document.body.setAttribute('data-calc-mode', mode);
    // Storage is implied by mode — CSS handles show/hide via data-show-modes.
    if (storageEnabled) storageEnabled.checked = (mode === 'storage' || mode === 'both');
    recalc();
  }

  function loadSizeLabel(cuft) {
    if (cuft === 0) return 'No items selected';
    // In storage-only mode the load size should describe a storage room,
    // not a removals lorry.
    if (getCalcMode() === 'storage') {
      var unit = pickStorageUnit(cuft);
      return '~ ' + unit.sqft + ' sqft room';
    }
    if (cuft <= 600)   return '~ Luton Van (3.5t) load';
    if (cuft <= 1100)  return '~ 7.5 Tonne Lorry load';
    if (cuft <= 2000)  return '~ 18–26 Tonne Rigid load';
    return '~ 44 Tonne Artic load';
  }

  // Typical cu ft range used when no inventory items are selected —
  // pre-fills the manual cu ft input as the customer changes home size.
  var TYPICAL_RANGE = {
    '1bed':  '500–900 cu ft',
    '2bed':  '800–1,400 cu ft',
    '3bed':  '1,200–1,800 cu ft',
    '4bed':  '1,800–2,800 cu ft',
    '5bed':  '2,800–4,000+ cu ft'
  };
  var manualCuftInput = document.getElementById('cost-manual-cuft');
  var manualCuftHelp  = document.getElementById('cost-manual-cuft-help');
  var manualCuftTouched = false;

  function applyHomeSizeDefault() {
    var bed = getBed();
    if (manualCuftInput && !manualCuftTouched) {
      manualCuftInput.value = bed.typicalCuft;
    }
    if (manualCuftHelp) {
      var sz = getHomeSize();
      var rng = TYPICAL_RANGE[sz] || '';
      manualCuftHelp.textContent = 'Typical ' + bed.label + ': ' + rng +
        '. Auto-fills with this figure; tick items below for a precise volume — or hit "Load inventory" to populate the room lists for you.';
    }
  }

  function recalc() {
    var invCuft = 0, invCum = 0, invKg = 0;
    for (var i = 0; i < inputs.length; i++) {
      var q = parseInt(inputs[i].value, 10);
      if (!q || q < 0) continue;
      invCuft += q * parseFloat(inputs[i].dataset.cuft);
      invCum  += q * parseFloat(inputs[i].dataset.cum);
      invKg   += q * parseFloat(inputs[i].dataset.kg);
    }
    var hasInventory = invCuft > 0;
    var manualCuft = 0;
    if (manualCuftInput) {
      manualCuft = parseInt(manualCuftInput.value, 10);
      if (isNaN(manualCuft) || manualCuft < 0) manualCuft = 0;
      // Disable the manual input while inventory drives the figure
      manualCuftInput.disabled = hasInventory;
    }
    var effectiveCuft = hasInventory ? Math.round(invCuft) : manualCuft;

    totalCuft.textContent = effectiveCuft;
    if (hasInventory) {
      totalCum.textContent = invCum.toFixed(2);
      totalKg.textContent  = Math.round(invKg);
    } else {
      // Convert cu ft → cu m precisely; estimate kg at ~6.5 kg/cu ft.
      totalCum.textContent = (effectiveCuft * 0.02832).toFixed(2);
      totalKg.textContent  = Math.round(effectiveCuft * 6.5);
    }
    vanEstimate.textContent = loadSizeLabel(effectiveCuft);
    recalcCost(effectiveCuft);
  }

  function recalcCost(cuft) {
    if (!costVehicle) return;
    var mode  = getCalcMode();
    var miles = parseInt((milesInput && milesInput.value) || '0', 10);
    if (isNaN(miles) || miles < 0) miles = 0;

    var bed = getBed();
    var vehicle = pickVehicle(cuft);
    var headlineLabel = document.getElementById('cost-headline-label');

    // --- REMOVALS leg ---
    var excessCuft = Math.max(0, cuft - BASE_INCLUDED);
    var excessCost = excessCuft * EXCESS_RATE;
    var volCost    = computeVolumeCost(cuft);
    var mileCost   = miles * vehicle.mileRate;
    var removalsTotal = (mode === 'storage') ? 0 : (volCost + mileCost);

    costVehicle.textContent = vehicle.name;
    if (cuft === 0) {
      costVolume.textContent = pounds(BASE_CHARGE) + ' (base · first ' + BASE_INCLUDED + ' cu ft)';
    } else if (excessCuft === 0) {
      costVolume.textContent = pounds(BASE_CHARGE) + ' (base · ' + cuft + ' / ' + BASE_INCLUDED + ' cu ft included)';
    } else {
      costVolume.textContent = pounds(volCost) + ' (' + pounds(BASE_CHARGE) + ' base + ' + excessCuft + ' extra × £' + EXCESS_RATE.toFixed(2) + ')';
    }
    costMileage.textContent = pounds(mileCost) + ' (' + miles + ' × £' + vehicle.mileRate.toFixed(2) + ')';
    if (costMinimum) {
      costMinimum.textContent = pounds(BASE_CHARGE);
    }
    costTotal.textContent = (mode === 'storage') ? '£0' : pounds(removalsTotal);

    // --- STORAGE leg + GRAND TOTAL ---
    var storageTotal = updateStorage(cuft, mode);
    var grandTotal = removalsTotal + storageTotal;
    if (grandTotalValue) grandTotalValue.textContent = pounds(grandTotal);

    if (headlineLabel) {
      var bits = [];
      if (mode !== 'storage') bits.push(vehicle.name);
      if (mode !== 'storage') bits.push(miles + ' mi');
      if (mode !== 'removals') {
        var days = parseInt((storageDaysInput && storageDaysInput.value) || '0', 10) || 0;
        bits.push(days + ' days storage');
      }
      var prefix;
      if (mode === 'storage') {
        prefix = 'Live estimate';
      } else if (excessCuft > 0) {
        prefix = excessCuft + ' cu ft above ' + BASE_INCLUDED + ' included';
      } else {
        prefix = 'Base rate · ' + cuft + ' / ' + BASE_INCLUDED + ' cu ft included';
      }
      headlineLabel.textContent = prefix + ' · ' + bits.join(' · ');
    }
  }

  function updateStorage(cuft, mode) {
    if (!storageUnitEl) return 0;
    var wantsStorage = (mode === 'storage' || mode === 'both');
    if (!wantsStorage) {
      storageUnitEl.textContent  = '—';
      storageDailyEl.textContent = '£0.00';
      storageTotalEl.textContent = '£0.00';
      return 0;
    }

    var days = parseInt((storageDaysInput && storageDaysInput.value) || '0', 10);
    if (isNaN(days) || days < 0) days = 0;

    if (cuft === 0) {
      storageUnitEl.textContent  = 'Set a cu ft figure first';
      storageDailyEl.textContent = '£0.00';
      storageTotalEl.textContent = '£0.00';
      return 0;
    }

    var unit = pickStorageUnit(cuft);
    var storageTotal = unit.daily * days;
    var sqftNeeded   = Math.ceil(cuft / STORAGE_CUFT_PER_SQFT);
    var biggerNote   = (sqftNeeded > unit.sqft) ? ' (or split rooms)' : '';

    storageUnitEl.textContent  = unit.sqft + ' sqft Prestige steel' + biggerNote;
    storageDailyEl.textContent = '£' + unit.daily.toFixed(2);
    storageTotalEl.textContent = '£' + storageTotal.toFixed(2);
    return storageTotal;
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

  // Inventory auto-fill prompt — shown when the customer picks a bedroom
  // count but hasn't ticked any inventory items yet. They can load the
  // standard inventory for that size, or skip and edit cu ft manually.
  var inventoryPrompt    = document.getElementById('inventory-prompt');
  var inventoryPromptMsg = document.getElementById('inventory-prompt-detail');
  var loadInventoryBtn   = document.getElementById('load-inventory-btn');
  var skipInventoryBtn   = document.getElementById('dismiss-inventory-prompt');
  var inventoryPromptDismissed = false;

  function hasAnyInventory() {
    for (var i = 0; i < inputs.length; i++) {
      var q = parseInt(inputs[i].value, 10);
      if (q && q > 0) return true;
    }
    return false;
  }

  function showInventoryPrompt() {
    if (!inventoryPrompt) return;
    if (inventoryPromptDismissed) return;
    if (hasAnyInventory()) { inventoryPrompt.hidden = true; return; }
    var profile = getBed();
    if (inventoryPromptMsg) {
      inventoryPromptMsg.textContent =
        'Want me to auto-fill a standard ' + profile.label +
        ' inventory? You can tweak quantities after.';
    }
    if (loadInventoryBtn) {
      loadInventoryBtn.textContent = 'Load ' + profile.label + ' inventory';
    }
    inventoryPrompt.hidden = false;
  }

  function clearAllInventoryInputs() {
    for (var i = 0; i < inputs.length; i++) inputs[i].value = 0;
  }

  function loadInventoryForCurrentSize() {
    var size = getHomeSize();
    var preset = BED_INVENTORY_DATA[size];
    if (!preset) return;
    if (hasAnyInventory()) {
      var ok = window.confirm(
        'This will replace the items you have already ticked with the standard ' +
        getBed().label + ' inventory. Continue?'
      );
      if (!ok) return;
    }
    clearAllInventoryInputs();
    Object.keys(preset).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) el.value = preset[id];
    });
    inventoryPromptDismissed = true;
    if (inventoryPrompt) inventoryPrompt.hidden = true;
    // Reveal the inventory refinement section so the customer can tweak.
    var invSection = document.getElementById('inventory-section');
    if (invSection) {
      invSection.hidden = false;
      invSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    manualCuftTouched = true; // inventory now drives cu ft
    recalc();
  }

  if (loadInventoryBtn) {
    loadInventoryBtn.addEventListener('click', loadInventoryForCurrentSize);
  }
  if (skipInventoryBtn) {
    skipInventoryBtn.addEventListener('click', function () {
      inventoryPromptDismissed = true;
      if (inventoryPrompt) inventoryPrompt.hidden = true;
    });
  }

  // Home size radios — switching bedrooms always resets the cu ft to the
  // bedroom's default (overrides any manual edit), re-shows the auto-fill
  // prompt for the new size, and recalcs.
  var homeSizeRadios = document.querySelectorAll('input[name="home-size"]');
  for (var hs = 0; hs < homeSizeRadios.length; hs++) {
    homeSizeRadios[hs].addEventListener('change', function () {
      inventoryPromptDismissed = false;
      manualCuftTouched = false; // force overwrite — bedroom drives cu ft
      applyHomeSizeDefault();
      showInventoryPrompt();
      recalc();
    });
  }

  // Manual cu ft input — flag as touched so future home-size changes don't
  // overwrite the user's value.
  if (manualCuftInput) {
    manualCuftInput.addEventListener('input', function () {
      manualCuftTouched = true;
      recalc();
    });
    manualCuftInput.addEventListener('change', recalc);
    // Set the initial default + help text on load
    applyHomeSizeDefault();
  }

  // Storage toggle + days
  if (storageEnabled)   storageEnabled.addEventListener('change', recalc);
  if (storageDaysInput) {
    storageDaysInput.addEventListener('input', recalc);
    storageDaysInput.addEventListener('change', recalc);
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
      var storageDays   = parseInt((storageDaysInput && storageDaysInput.value) || '0', 10);
      var storageUnitTxt  = (storageUnitEl && storageUnitEl.textContent) || '';
      var storageDailyTxt = (storageDailyEl && storageDailyEl.textContent) || '';
      var storageTotalTxt = (storageTotalEl && storageTotalEl.textContent) || '';
      var grandTotalTxt   = (grandTotalValue && grandTotalValue.textContent) || '';

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
        var prof = getBed();
        body.push('ESTIMATED REMOVALS COST');
        body.push('  Vehicle band:    ' + vehicle);
        body.push('  Home size:       ' + prof.label);
        body.push('  Distance:        ' + miles + ' miles');
        body.push('  Volume cost:     ' + volumeCost);
        body.push('  Mileage cost:    ' + mileageCost);
        body.push('  Removals total:  ' + totalCost);
        body.push('');
      }
      if (storageWanted) {
        body.push('STORAGE REQUIRED');
        body.push('  Unit:            ' + storageUnitTxt);
        body.push('  Daily rate:      ' + storageDailyTxt + ' (inc VAT & insurance)');
        body.push('  Duration:        ' + storageDays + ' days (~' + (storageDays / 7).toFixed(storageDays % 7 === 0 ? 0 : 1) + ' weeks)');
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
  // Trigger the inventory auto-fill prompt on first paint (mode permitting).
  if (getCalcMode() !== 'storage') showInventoryPrompt();
})();
