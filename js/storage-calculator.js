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
  var milesInput     = document.getElementById('cost-miles');
  var costVehicle    = document.getElementById('cost-vehicle');
  var costVolume     = document.getElementById('cost-volume');
  var costMileage    = document.getElementById('cost-mileage');
  var costMinimum    = document.getElementById('cost-minimum');
  var costNettTotal  = document.getElementById('cost-nett-total');
  var costVAT        = document.getElementById('cost-vat');
  var costTotal      = document.getElementById('cost-total');

  // Storage-unit price list (sqft, NETT daily rate — VAT added at booking).
  // Source: Mark Ratcliffe Moving Prestige steel storage rate sheet
  // ("Rate Nett £" column).
  var STORAGE_UNITS = [
    { sqft:  25, daily:  2.16 },
    { sqft:  30, daily:  2.52 },
    { sqft:  40, daily:  3.74 },
    { sqft:  60, daily:  5.40 },
    { sqft:  65, daily:  6.19 },
    { sqft:  75, daily:  7.42 },
    { sqft: 120, daily: 11.40 },
    { sqft: 145, daily: 12.95 },
    { sqft: 200, daily: 18.00 },
    { sqft: 280, daily: 20.40 }
  ];
  // Lower-ceiling 75 sqft room — nett rate.
  var STORAGE_LOW_CEILING_75 = { sqft: 75, daily: 5.76, label: '75 sqft low-ceiling' };
  var STORAGE_CUFT_PER_SQFT = 7; // packing efficiency: 7 cu ft per sqft of floor

  var storageEnabled    = document.getElementById('storage-enabled');
  var storageDaysInput  = document.getElementById('storage-days');
  var storageUnitEl     = document.getElementById('storage-unit');
  var storageDailyEl    = document.getElementById('storage-daily');
  var storageTotalEl    = document.getElementById('storage-total');
  var storageSummarySqft = document.getElementById('storage-summary-sqft');
  var storageSummaryCuft = document.getElementById('storage-summary-cuft');
  var storageSummaryCum  = document.getElementById('storage-summary-cum');
  var grandTotalValue    = document.getElementById('cost-grand-total-value');

  // Inventory summary (in-card list of selected items grouped by room).
  var inventorySummary           = document.getElementById('inventory-summary');
  var inventorySummaryRooms      = document.getElementById('inventory-summary-rooms');
  var inventorySummaryTotalLine  = document.getElementById('inventory-summary-total-line');

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c];
    });
  }

  function updateInventorySummary() {
    if (!inventorySummary || !inventorySummaryRooms) return;
    var html = '';
    var anyItems = false;
    var totalItems = 0;
    var totalCuft  = 0;
    for (var p = 0; p < panels.length; p++) {
      var panel = panels[p];
      var roomLabel = '';
      for (var t = 0; t < tabs.length; t++) {
        if (tabs[t].dataset.target === panel.id) {
          var lab = tabs[t].querySelector('.calc-tab-label');
          if (lab) roomLabel = lab.textContent;
          break;
        }
      }
      var items = panel.querySelectorAll('.calc-item');
      var roomHtml = '';
      var roomCuft = 0;
      var roomCount = 0;
      for (var i = 0; i < items.length; i++) {
        var inp = items[i].querySelector('input[type="number"][data-cuft]');
        if (!inp) continue;
        var qty = parseInt(inp.value, 10) || 0;
        if (qty <= 0) continue;
        var nameEl = items[i].querySelector('.calc-item-name');
        var name = nameEl ? nameEl.textContent : 'Item';
        var cuftPer = parseFloat(inp.dataset.cuft) || 0;
        var itemCuft = qty * cuftPer;
        roomCuft += itemCuft;
        roomCount += qty;
        roomHtml +=
          '<div class="qc-inventory-summary-item">' +
            '<span class="qc-isum-name">' + qty + ' × ' + escapeHtml(name) + '</span>' +
            '<div class="qc-isum-stepper">' +
              '<button type="button" class="qc-isum-btn" data-action="minus" data-target="' + escapeHtml(inp.id) + '" aria-label="Decrease ' + escapeHtml(name) + '">−</button>' +
              '<button type="button" class="qc-isum-btn" data-action="plus"  data-target="' + escapeHtml(inp.id) + '" aria-label="Increase ' + escapeHtml(name) + '">+</button>' +
            '</div>' +
            '<span class="qc-isum-cuft">' + Math.round(itemCuft) + ' cu ft</span>' +
          '</div>';
      }
      if (roomCount > 0) {
        anyItems = true;
        totalItems += roomCount;
        totalCuft  += roomCuft;
        html +=
          '<div class="qc-inventory-summary-room">' +
            '<div class="qc-inventory-summary-room-name">' +
              escapeHtml(roomLabel) +
              ' <span class="qc-isum-room-cuft">' + Math.round(roomCuft) + ' cu ft</span>' +
            '</div>' +
            roomHtml +
          '</div>';
      }
    }
    if (anyItems) {
      inventorySummaryRooms.innerHTML = html;
      if (inventorySummaryTotalLine) {
        inventorySummaryTotalLine.textContent = totalItems + ' items · ' + Math.round(totalCuft).toLocaleString('en-GB') + ' cu ft';
      }
      inventorySummary.hidden = false;
    } else {
      inventorySummary.hidden = true;
    }
  }

  // Event delegation on the summary container — handles + / − clicks on
  // every rendered item, drives the source input qty (which is what the
  // rest of the calculator reads from), then recalcs.
  if (inventorySummaryRooms) {
    inventorySummaryRooms.addEventListener('click', function (e) {
      var btn = e.target.closest && e.target.closest('.qc-isum-btn');
      if (!btn) return;
      var id = btn.getAttribute('data-target');
      if (!id) return;
      var srcInput = document.getElementById(id);
      if (!srcInput) return;
      var qty = parseInt(srcInput.value, 10) || 0;
      if (btn.getAttribute('data-action') === 'minus') {
        srcInput.value = Math.max(0, qty - 1);
      } else {
        srcInput.value = qty + 1;
      }
      recalc();
    });
  }

  // Returns an array of { unit, qty } pairs that cover the required sqft.
  // For volumes that fit a single room, returns [{ unit, qty: 1 }].
  // For volumes that need multiple rooms, fills with as many of the
  // biggest (280 sqft) as needed, then tops up with the SMALLEST single
  // room that covers the remainder — so customers don't pay for two
  // 280 sqft rooms when they only need 286 sqft total.
  function pickStorageUnits(cuft) {
    var sqftNeeded = Math.ceil(cuft / STORAGE_CUFT_PER_SQFT);
    // Single-room case
    for (var i = 0; i < STORAGE_UNITS.length; i++) {
      if (STORAGE_UNITS[i].sqft >= sqftNeeded) {
        return [{ unit: STORAGE_UNITS[i], qty: 1 }];
      }
    }
    // Multi-room mix
    var biggest = STORAGE_UNITS[STORAGE_UNITS.length - 1];
    var nFull = Math.floor(sqftNeeded / biggest.sqft);
    var picks = [{ unit: biggest, qty: nFull }];
    var remainder = sqftNeeded - nFull * biggest.sqft;
    if (remainder > 0) {
      for (var j = 0; j < STORAGE_UNITS.length; j++) {
        if (STORAGE_UNITS[j].sqft >= remainder) {
          picks.push({ unit: STORAGE_UNITS[j], qty: 1 });
          break;
        }
      }
    }
    return picks;
  }

  // Pricing model (per-property base + monotonic excess):
  //   • Each bedroom selection has its own base charge that covers the
  //     property's typical cu ft volume.
  //   • Every cu ft above the property's typical adds £1.21 — price
  //     rises continuously, no plateaus.
  //   • Vehicle is auto-picked by cu ft for the mileage rate only.
  //   • Volume cost = bed.base + max(0, cuft − bed.typicalCuft) × £1.21
  //   • Nett total  = volume cost + miles × picked-vehicle mile rate
  //   • VAT         = nett × 20%
  //   • Inc-VAT     = nett × 1.20 (storage rates already include VAT)
  // Default excess £/cu ft if a property doesn't override its own rate.
  var DEFAULT_EXCESS_RATE = 1.51;
  var VAT_RATE            = 0.20;
  var VEHICLE_TIERS = [
    { name: 'Luton Van (3.5t)', maxCuft:  800, mileRate: 2.00 },
    { name: '7.5 Tonne Lorry',  maxCuft: 1500, mileRate: 2.75 },
    { name: '18 Tonne Lorry',   maxCuft: 2500, mileRate: 4.00 },
    { name: '44 Tonne Artic',   maxCuft: Infinity, mileRate: 4.00 }
  ];

  // Per-property pricing tiers. typicalCuft auto-fills the cu ft input
  // and also defines the volume the property's base charge already
  // covers. Above typicalCuft, each extra cu ft adds £1.21.
  var BED_DEFAULTS = {
    // Tiny is capped at 500 cu ft — above that we always defer to a real
    // bed tier so the £1/cu ft Tiny rate can't undercut larger jobs.
    'tiny': { label: 'Tiny move',                    typicalCuft:  300, base:  300, rate: 1.00, maxCuft: 500 },
    '1bed': { label: '1-bed flat or studio',         typicalCuft:  500, base:  500, rate: 1.51 },
    '2bed': { label: '2-bed home',                   typicalCuft:  800, base:  650, rate: 1.51 },
    '3bed': { label: '3-bed home',                   typicalCuft: 1000, base:  900, rate: 1.51 },
    '4bed': { label: '4-bed home',                   typicalCuft: 1800, base: 1500, rate: 1.51 },
    '5bed': { label: '5+ bed / antiques / country',  typicalCuft: 2800, base: 2500, rate: 1.51 }
  };

  function computeVolumeCost(cuft, bed) {
    var excess = Math.max(0, cuft - bed.typicalCuft);
    var rate = (typeof bed.rate === 'number') ? bed.rate : DEFAULT_EXCESS_RATE;
    return bed.base + excess * rate;
  }
  // Picks the cheapest valid bed tier for a given cu ft. Tiers with a
  // maxCuft are skipped when the volume exceeds it (so the £1/cu ft Tiny
  // rate can't take over at high volumes). Mirrors the
  // pickStorageUnits/pickVehicle "always cheapest" logic.
  function pickCheapestBed(cuft) {
    var bestBed = null;
    var bestCost = Infinity;
    Object.keys(BED_DEFAULTS).forEach(function (key) {
      var b = BED_DEFAULTS[key];
      if (typeof b.maxCuft === 'number' && cuft > b.maxCuft) return;
      var c = computeVolumeCost(cuft, b);
      if (c < bestCost) { bestCost = c; bestBed = b; }
    });
    return bestBed || BED_DEFAULTS['3bed'];
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
  // Pounds with pence — used for the headline estimate so VAT pence show.
  function poundsPence(n) {
    return '£' + n.toLocaleString('en-GB', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
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
      var picks = pickStorageUnits(cuft);
      var totalSqft = 0;
      for (var p = 0; p < picks.length; p++) totalSqft += picks[p].unit.sqft * picks[p].qty;
      return '~ ' + totalSqft + ' sqft room' + (totalSqft >= picks[0].unit.sqft * 2 ? 's' : '');
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
      // While inventory drives the figure: disable the field AND keep
      // its displayed value in sync with the live inventory sum so the
      // customer can see the cu ft figure update as items are added,
      // removed or +/- stepped.
      manualCuftInput.disabled = hasInventory;
      if (hasInventory) {
        manualCuftInput.value = Math.round(invCuft);
      }
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
    updateInventorySummary();
    updateTabCounts();
    updateQuotePreview(effectiveCuft, invKg);
  }

  // Update the per-tab item-count badge — shows total qty of all ticked
  // items inside each room panel, hidden when zero.
  function updateTabCounts() {
    for (var p = 0; p < panels.length; p++) {
      var panel = panels[p];
      var panelInputs = panel.querySelectorAll('input[type="number"][data-cuft]');
      var count = 0;
      for (var i = 0; i < panelInputs.length; i++) {
        var q = parseInt(panelInputs[i].value, 10);
        if (q && q > 0) count += q;
      }
      var tab = null;
      for (var t = 0; t < tabs.length; t++) {
        if (tabs[t].dataset.target === panel.id) { tab = tabs[t]; break; }
      }
      if (!tab) continue;
      var badge = tab.querySelector('.calc-tab-count');
      if (!badge) continue;
      if (count > 0) {
        badge.textContent = count;
        badge.hidden = false;
      } else {
        badge.hidden = true;
      }
    }
  }

  // Build the live quote-preview panel inside the contact form (shows
  // the customer exactly what will be emailed).
  function updateQuotePreview(cuft, invKg) {
    var mode = getCalcMode();
    var modeLabel = mode === 'storage' ? 'Storage only'
                  : mode === 'removals' ? 'Removals only'
                  : 'Removals + Storage';
    var fromInput = document.getElementById('qf-from');
    var toInput   = document.getElementById('qf-to');
    var fromPC = fromInput ? fromInput.value.trim().toUpperCase() : '';
    var toPC   = toInput   ? toInput.value.trim().toUpperCase()   : '';
    var miles = parseInt((milesInput && milesInput.value) || '0', 10) || 0;
    var days  = parseInt((storageDaysInput && storageDaysInput.value) || '0', 10) || 0;

    var bedForLabel = getBed();         // customer's bedroom radio (label only)
    var bedForPrice = pickCheapestBed(cuft);
    var vehicle = pickVehicle(cuft);
    var kg = invKg > 0 ? Math.round(invKg) : Math.round(cuft * 6.5);
    var cum = (cuft * 0.02832).toFixed(2);

    function setText(id, text) {
      var el = document.getElementById(id);
      if (el) el.textContent = text;
    }

    setText('qp-mode',  modeLabel);
    setText('qp-from',  fromPC || '—');
    setText('qp-to',    toPC   || '—');
    setText('qp-miles', miles + ' mile' + (miles === 1 ? '' : 's'));
    setText('qp-storage-duration', days + ' day' + (days === 1 ? '' : 's') +
      ' (~' + (days / 7).toFixed(days % 7 === 0 ? 0 : 1) + ' wk)');
    setText('qp-bedroom', bedForLabel.label);
    setText('qp-volume',  cuft.toLocaleString('en-GB') + ' cu ft · ' + cum + ' cu m');
    setText('qp-weight',  kg.toLocaleString('en-GB') + ' kg');
    setText('qp-vehicle', vehicle.name);

    // Storage room
    var picks = pickStorageUnits(cuft);
    var totalSqft = 0;
    var roomBits = [];
    for (var p = 0; p < picks.length; p++) {
      totalSqft += picks[p].unit.sqft * picks[p].qty;
      roomBits.push((picks[p].qty > 1 ? picks[p].qty + ' × ' : '') + picks[p].unit.sqft + ' sqft');
    }
    setText('qp-storage-room', roomBits.join(' + '));

    // Pricing (nett)
    var rmExcess = Math.max(0, cuft - bedForPrice.typicalCuft);
    var rmRate   = (typeof bedForPrice.rate === 'number') ? bedForPrice.rate : DEFAULT_EXCESS_RATE;
    var rmVolCost = bedForPrice.base + rmExcess * rmRate;
    var rmMileCost = miles * vehicle.mileRate;
    var rmNett = (mode === 'storage') ? 0 : rmVolCost + rmMileCost;
    var stPerDay = 0;
    for (var s = 0; s < picks.length; s++) stPerDay += picks[s].unit.daily * picks[s].qty;
    var stNett = (mode === 'removals' || cuft === 0) ? 0 : stPerDay * days;

    function moneyNett(n) { return '£' + n.toLocaleString('en-GB', { minimumFractionDigits: 2, maximumFractionDigits: 2 }); }
    setText('qp-removals-price', moneyNett(rmNett));
    setText('qp-storage-price',  moneyNett(stNett));
    setText('qp-total-price',    moneyNett(rmNett + stNett));

    // Inventory list grouped by room
    var roomsEl = document.getElementById('qp-inventory-rooms');
    var totalEl = document.getElementById('qp-inventory-total');
    if (!roomsEl || !totalEl) return;
    var html = '';
    var totalItems = 0;
    var totalCuft  = 0;
    for (var pi = 0; pi < panels.length; pi++) {
      var panel = panels[pi];
      var roomLabel = '';
      for (var ti = 0; ti < tabs.length; ti++) {
        if (tabs[ti].dataset.target === panel.id) {
          var lab = tabs[ti].querySelector('.calc-tab-label');
          if (lab) roomLabel = lab.textContent;
          break;
        }
      }
      var items = panel.querySelectorAll('.calc-item');
      var roomHtml = '';
      var roomCuft = 0;
      var roomCount = 0;
      for (var ii = 0; ii < items.length; ii++) {
        var inp = items[ii].querySelector('input[type="number"][data-cuft]');
        if (!inp) continue;
        var qty = parseInt(inp.value, 10) || 0;
        if (qty <= 0) continue;
        var nameEl = items[ii].querySelector('.calc-item-name');
        var name = nameEl ? nameEl.textContent : 'Item';
        var cuftPer = parseFloat(inp.dataset.cuft) || 0;
        var itemCuft = qty * cuftPer;
        roomCuft += itemCuft;
        roomCount += qty;
        roomHtml +=
          '<div class="qp-inv-row"><span class="qp-inv-name">' + qty + ' × ' + escapeHtml(name) + '</span>' +
          '<span class="qp-inv-cuft">' + Math.round(itemCuft) + ' cu ft</span></div>';
      }
      if (roomCount > 0) {
        totalItems += roomCount;
        totalCuft  += roomCuft;
        html += '<div class="qp-inv-room"><div class="qp-inv-room-head"><span>' +
          escapeHtml(roomLabel) + '</span><span>' + Math.round(roomCuft) + ' cu ft</span></div>' +
          roomHtml + '</div>';
      }
    }
    roomsEl.innerHTML = html;
    totalEl.textContent = totalItems > 0
      ? totalItems + ' items · ' + Math.round(totalCuft).toLocaleString('en-GB') + ' cu ft'
      : '0 items';
  }

  function recalcCost(cuft) {
    if (!costVehicle) return;
    var mode  = getCalcMode();
    var miles = parseInt((milesInput && milesInput.value) || '0', 10);
    if (isNaN(miles) || miles < 0) miles = 0;

    // Pricing tier = cheapest valid bed for the cu ft (independent of
    // which bedroom radio the customer ticked — that's just for the
    // inventory preset and the auto-fill cu ft default).
    var bed = pickCheapestBed(cuft);
    var vehicle = pickVehicle(cuft);
    var headlineLabel = document.getElementById('cost-headline-label');

    // --- REMOVALS leg ---
    var excessCuft = Math.max(0, cuft - bed.typicalCuft);
    var volCost    = computeVolumeCost(cuft, bed);
    var mileCost   = miles * vehicle.mileRate;
    var removalsNett = (mode === 'storage') ? 0 : (volCost + mileCost);
    var removalsVAT  = removalsNett * VAT_RATE;
    var removalsInc  = removalsNett + removalsVAT;

    costVehicle.textContent = vehicle.name;
    if (cuft === 0) {
      costVolume.textContent = pounds(bed.base) + ' (' + bed.label + ' base · first ' + bed.typicalCuft + ' cu ft)';
    } else if (excessCuft === 0) {
      costVolume.textContent = pounds(bed.base) + ' (' + bed.label + ' base · ' + cuft + ' / ' + bed.typicalCuft + ' cu ft included)';
    } else {
      costVolume.textContent = pounds(volCost) + ' (' + pounds(bed.base) + ' base + ' + excessCuft + ' extra × £' + (bed.rate || DEFAULT_EXCESS_RATE).toFixed(2) + ')';
    }
    costMileage.textContent = pounds(mileCost) + ' (' + miles + ' × £' + vehicle.mileRate.toFixed(2) + ')';
    if (costNettTotal) costNettTotal.textContent = pounds(removalsNett);
    if (costVAT)       costVAT.textContent       = pounds(removalsVAT);
    costTotal.textContent = (mode === 'storage') ? '£0' : pounds(removalsNett);

    // --- STORAGE leg + GRAND TOTAL (NETT — VAT added at booking) ---
    var storageTotal = updateStorage(cuft, mode);
    var grandTotalNett = removalsNett + storageTotal;
    if (grandTotalValue) grandTotalValue.textContent = poundsPence(grandTotalNett);

    // Both-mode split panel: show removals + storage + total separately.
    if (mode === 'both') {
      var splitRm = document.getElementById('split-removals');
      var splitSt = document.getElementById('split-storage');
      var splitTo = document.getElementById('split-total');
      var splitStLabel = document.getElementById('split-storage-label');
      if (splitRm) splitRm.textContent = poundsPence(removalsNett);
      if (splitSt) splitSt.textContent = poundsPence(storageTotal);
      if (splitTo) splitTo.textContent = poundsPence(grandTotalNett);
      if (splitStLabel) {
        var days = parseInt((storageDaysInput && storageDaysInput.value) || '0', 10) || 0;
        splitStLabel.textContent = 'Storage (' + days + ' days)';
      }
    }

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
        prefix = 'Live estimate (+ VAT)';
      } else if (excessCuft > 0) {
        prefix = excessCuft + ' cu ft above ' + bed.typicalCuft + ' included · + VAT';
      } else {
        prefix = bed.label + ' base · + VAT';
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
      if (storageSummarySqft) storageSummarySqft.textContent = '—';
      if (storageSummaryCuft) storageSummaryCuft.textContent = '— cu ft';
      if (storageSummaryCum)  storageSummaryCum.textContent  = '— cu m';
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

    var picks = pickStorageUnits(cuft);
    var perDay = 0;
    var totalSqft = 0;
    var labelParts = [];
    var dailyParts = [];
    for (var k = 0; k < picks.length; k++) {
      var pu = picks[k].unit;
      var pq = picks[k].qty;
      perDay   += pu.daily * pq;
      totalSqft += pu.sqft  * pq;
      labelParts.push((pq > 1 ? pq + ' × ' : '') + pu.sqft + ' sqft');
      dailyParts.push((pq > 1 ? pq + ' × ' : '') + '£' + pu.daily.toFixed(2));
    }
    var storageTotal = perDay * days;
    var totalCuft = totalSqft * STORAGE_CUFT_PER_SQFT;
    var totalCum  = totalCuft * 0.02832;
    var isMulti   = picks.length > 1 || picks[0].qty > 1;

    storageUnitEl.textContent  = labelParts.join(' + ') + ' Prestige steel room' + (isMulti ? 's' : '');
    storageDailyEl.textContent = isMulti
      ? '£' + perDay.toFixed(2) + ' (' + dailyParts.join(' + ') + ')'
      : '£' + perDay.toFixed(2);
    storageTotalEl.textContent = '£' + storageTotal.toFixed(2);

    // Customer-facing summary (sqft / cu ft / cu m of the picked rooms)
    if (storageSummarySqft) {
      storageSummarySqft.textContent = isMulti
        ? labelParts.join(' + ') + ' (' + totalSqft + ' sqft total)'
        : totalSqft + ' sqft';
    }
    if (storageSummaryCuft) storageSummaryCuft.textContent = totalCuft.toLocaleString('en-GB') + ' cu ft';
    if (storageSummaryCum)  storageSummaryCum.textContent  = totalCum.toFixed(2) + ' cu m';

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

  // Inventory toggle prompt — a switch that auto-fills the standard
  // loadout for the picked bedroom. Customers can also tick items
  // manually via the "Or tick items manually" link.
  var inventoryPrompt    = document.getElementById('inventory-prompt');
  var inventoryPromptMsg = document.getElementById('inventory-prompt-detail');
  var inventoryToggle    = document.getElementById('inventory-toggle');

  function hasAnyInventory() {
    for (var i = 0; i < inputs.length; i++) {
      var q = parseInt(inputs[i].value, 10);
      if (q && q > 0) return true;
    }
    return false;
  }

  function showInventoryPrompt() {
    if (!inventoryPrompt) return;
    // Hide prompt entirely if the current mode is storage-only (inventory
    // still drives cu ft but the toggle isn't needed there) or if the
    // current property has no preset (Tiny).
    if (getCalcMode() === 'storage') { inventoryPrompt.hidden = true; return; }
    var size = getHomeSize();
    if (!BED_INVENTORY_DATA[size]) { inventoryPrompt.hidden = true; return; }
    // Refresh the bedroom label inside the toggle text.
    var bedLabelEl = document.getElementById('inventory-toggle-bed');
    if (bedLabelEl) bedLabelEl.textContent = getBed().label;
    if (inventoryPromptMsg) {
      inventoryPromptMsg.textContent =
        'Auto-fills a standard ' + getBed().label + ' loadout — adjust quantities after.';
    }
    inventoryPrompt.hidden = false;
  }

  function loadPresetForSize(size) {
    var preset = BED_INVENTORY_DATA[size];
    if (!preset) return false;
    clearAllInventoryInputs();
    Object.keys(preset).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) el.value = preset[id];
    });
    return true;
  }

  function clearAllInventoryInputs() {
    for (var i = 0; i < inputs.length; i++) inputs[i].value = 0;
  }

  function setInventoryVisible(visible, scroll) {
    var invSection = document.getElementById('inventory-section');
    if (!invSection) return;
    invSection.hidden = !visible;
    if (visible && scroll) {
      invSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    if (visible) {
      // Re-measure after layout settles (section was hidden, dimensions were 0).
      requestAnimationFrame(function () { requestAnimationFrame(updateTabsMoreBtn); });
    }
  }

  // "More →" tab-strip affordance — appears when tabs are scrolled
  // offscreen to the right. Clicking scrolls the tab strip further right.
  var tabsContainer = root.querySelector('.calc-tabs');
  var tabsMoreBtn   = document.getElementById('calc-tabs-more');
  function updateTabsMoreBtn() {
    if (!tabsContainer || !tabsMoreBtn) return;
    var moreRight = tabsContainer.scrollLeft + tabsContainer.clientWidth < tabsContainer.scrollWidth - 2;
    tabsMoreBtn.hidden = !moreRight;
  }
  if (tabsContainer) {
    tabsContainer.addEventListener('scroll', updateTabsMoreBtn);
    window.addEventListener('resize', updateTabsMoreBtn);
  }
  if (tabsMoreBtn && tabsContainer) {
    tabsMoreBtn.addEventListener('click', function () {
      var amount = Math.max(220, tabsContainer.clientWidth * 0.7);
      tabsContainer.scrollBy({ left: amount, behavior: 'smooth' });
    });
  }

  // Toggle change handler — ON loads the preset and shows the editor;
  // OFF clears items and hides the editor.
  if (inventoryToggle) {
    inventoryToggle.addEventListener('change', function () {
      if (inventoryToggle.checked) {
        var loaded = loadPresetForSize(getHomeSize());
        if (loaded) {
          setInventoryVisible(true, true);
          manualCuftTouched = true; // inventory now drives cu ft
        } else {
          inventoryToggle.checked = false; // no preset, snap back
        }
      } else {
        clearAllInventoryInputs();
        setInventoryVisible(false, false);
        // Reset cu ft to the bedroom's default once items are cleared.
        manualCuftTouched = false;
        applyHomeSizeDefault();
      }
      recalc();
    });
  }

  // "Or tick items manually" — open the empty editor without auto-fill.
  var addManuallyBtn = document.getElementById('add-inventory-manually');
  if (addManuallyBtn) {
    addManuallyBtn.addEventListener('click', function () {
      setInventoryVisible(true, true);
    });
  }

  // Home size radios — switching bedrooms:
  //   • resets cu ft to the new property's default
  //   • clears any loaded inventory items
  //   • if the auto-fill toggle is ON: reloads the preset for the new
  //     bedroom (and keeps the editor open + scrolls)
  //   • if the toggle is OFF: hides the editor (clean slate)
  var homeSizeRadios = document.querySelectorAll('input[name="home-size"]');
  for (var hs = 0; hs < homeSizeRadios.length; hs++) {
    homeSizeRadios[hs].addEventListener('change', function () {
      manualCuftTouched = false;
      clearAllInventoryInputs();
      applyHomeSizeDefault();
      showInventoryPrompt(); // refreshes the toggle label for the new size
      if (inventoryToggle && inventoryToggle.checked) {
        if (loadPresetForSize(getHomeSize())) {
          setInventoryVisible(true, false);
          manualCuftTouched = true;
        } else {
          // No preset for this size (e.g. Tiny) — snap toggle back to OFF.
          inventoryToggle.checked = false;
          setInventoryVisible(false, false);
        }
      } else {
        setInventoryVisible(false, false);
      }
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

  // CTA → toggle the in-card quote dropdown (form + preview).
  var quoteCtaToggle = document.getElementById('quote-cta-toggle');
  var quoteDropdown  = document.getElementById('quote-dropdown');
  if (quoteCtaToggle && quoteDropdown) {
    quoteCtaToggle.addEventListener('click', function () {
      var willOpen = quoteDropdown.hidden;
      quoteDropdown.hidden = !willOpen;
      quoteCtaToggle.setAttribute('aria-expanded', willOpen ? 'true' : 'false');
      if (willOpen) {
        requestAnimationFrame(function () {
          quoteDropdown.scrollIntoView({ behavior: 'smooth', block: 'start' });
          var emailField = document.getElementById('qf-email');
          if (emailField) emailField.focus({ preventScroll: true });
        });
      }
    });
  }

  // Keep the live preview in sync when the customer types postcodes etc.
  ['qf-from', 'qf-to'].forEach(function (id) {
    var el = document.getElementById(id);
    if (el) el.addEventListener('input', recalc);
  });

  // Quote request form — build a pre-filled mailto: with all the
  // calculator output + the customer's contact details.
  var quoteForm = document.getElementById('quote-request-form');
  if (quoteForm) {
    quoteForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var email  = document.getElementById('qf-email').value.trim();
      var phone  = document.getElementById('qf-phone').value.trim();
      var fromPC = document.getElementById('qf-from').value.trim().toUpperCase();
      var toPC   = document.getElementById('qf-to').value.trim().toUpperCase();
      var notes  = document.getElementById('qf-notes').value.trim();
      var status = document.getElementById('qf-status');

      var calcMode = getCalcMode();
      var modeLabel = calcMode === 'storage' ? 'Storage only'
                    : calcMode === 'removals' ? 'Removals only'
                    : 'Removals + Storage';

      // Pull the live figures the page already computed.
      var cuft = parseInt((totalCuft && totalCuft.textContent) || '0', 10) || 0;
      var cum  = (totalCum && totalCum.textContent) || '0';
      var kg   = parseInt((totalKg && totalKg.textContent) || '0', 10) || 0;
      var miles = parseInt((milesInput && milesInput.value) || '0', 10) || 0;
      var days  = parseInt((storageDaysInput && storageDaysInput.value) || '0', 10) || 0;
      var bedSelected = getBed();
      var bedForPrice = pickCheapestBed(cuft);
      var vehicle = pickVehicle(cuft);

      // Removals pricing (nett — VAT added at booking)
      var rmExcess   = Math.max(0, cuft - bedForPrice.typicalCuft);
      var rmRate     = (typeof bedForPrice.rate === 'number') ? bedForPrice.rate : DEFAULT_EXCESS_RATE;
      var rmVolCost  = bedForPrice.base + rmExcess * rmRate;
      var rmMileCost = miles * vehicle.mileRate;
      var rmNett     = (calcMode === 'storage') ? 0 : rmVolCost + rmMileCost;

      // Storage pricing (nett)
      var picks      = pickStorageUnits(cuft);
      var stPerDay   = 0;
      var stTotalSqft = 0;
      var stBits     = [];
      for (var i = 0; i < picks.length; i++) {
        stPerDay   += picks[i].unit.daily * picks[i].qty;
        stTotalSqft += picks[i].unit.sqft  * picks[i].qty;
        stBits.push((picks[i].qty > 1 ? picks[i].qty + ' × ' : '') + picks[i].unit.sqft + ' sqft');
      }
      var stNett = (calcMode === 'removals' || cuft === 0) ? 0 : stPerDay * days;

      function fp(n) { return '£' + n.toLocaleString('en-GB', { minimumFractionDigits: 2, maximumFractionDigits: 2 }); }
      function pad(label, val) { while (label.length < 22) label += ' '; return label + val; }

      // Items grouped by room
      var roomLines = [];
      var totalItems = 0;
      for (var p = 0; p < panels.length; p++) {
        var panel = panels[p];
        var roomLabel = '';
        for (var t = 0; t < tabs.length; t++) {
          if (tabs[t].dataset.target === panel.id) {
            var lab = tabs[t].querySelector('.calc-tab-label');
            if (lab) roomLabel = lab.textContent;
            break;
          }
        }
        var items = panel.querySelectorAll('.calc-item');
        var rows = [];
        var roomCuft = 0;
        var roomCount = 0;
        for (var ii = 0; ii < items.length; ii++) {
          var inp = items[ii].querySelector('input[type="number"][data-cuft]');
          if (!inp) continue;
          var qty = parseInt(inp.value, 10) || 0;
          if (qty <= 0) continue;
          var nameEl = items[ii].querySelector('.calc-item-name');
          var name = nameEl ? nameEl.textContent : 'Item';
          var cuftPer = parseFloat(inp.dataset.cuft) || 0;
          var itemCuft = qty * cuftPer;
          roomCuft += itemCuft;
          roomCount += qty;
          rows.push('    ' + qty + ' × ' + name + ' — ' + Math.round(itemCuft) + ' cu ft');
        }
        if (roomCount > 0) {
          totalItems += roomCount;
          roomLines.push('  ' + roomLabel + ' (' + Math.round(roomCuft) + ' cu ft)');
          roomLines = roomLines.concat(rows);
          roomLines.push('');
        }
      }

      // Compose the email body — readable for the customer (who's CC'd)
      // AND comprehensive for the office.
      var lines = [];
      lines.push('QUOTE REQUEST — Mark Ratcliffe Moving & Storage');
      lines.push('==================================================');
      lines.push('');
      lines.push('Hi Mark Ratcliffe Moving,');
      lines.push('');
      lines.push('Please prepare a quote for the move detailed below.');
      lines.push('All figures are nett — VAT (20%) will be added at booking.');
      lines.push('');
      lines.push('CONTACT');
      lines.push(pad('  Email:', email));
      lines.push(pad('  Phone:', phone));
      lines.push(pad('  Moving FROM:', fromPC));
      lines.push(pad('  Moving TO:', toPC));
      lines.push(pad('  Round-trip distance:', miles + ' mile' + (miles === 1 ? '' : 's')));
      lines.push(pad('  Service type:', modeLabel));
      lines.push('');
      lines.push('PROPERTY & VOLUME');
      lines.push(pad('  Home size selected:', bedSelected.label));
      lines.push(pad('  Total volume:', cuft.toLocaleString('en-GB') + ' cu ft'));
      lines.push(pad('  Cubic metres:', cum + ' cu m'));
      lines.push(pad('  Estimated weight:', kg.toLocaleString('en-GB') + ' kg'));
      lines.push(pad('  Load size:', (vanEstimate && vanEstimate.textContent) || ''));
      lines.push('');
      if (calcMode !== 'storage') {
        lines.push('REMOVALS (nett — VAT added at booking)');
        lines.push(pad('  Vehicle recommended:', vehicle.name + '  (' + fp(vehicle.mileRate) + '/mi)'));
        lines.push(pad('  Pricing tier:',        bedForPrice.label));
        lines.push(pad('  Base charge:',         fp(bedForPrice.base) + '  (covers first ' + bedForPrice.typicalCuft + ' cu ft)'));
        if (rmExcess > 0) {
          lines.push(pad('  Excess volume:',     rmExcess + ' cu ft × ' + fp(rmRate) + ' = ' + fp(rmExcess * rmRate)));
        }
        lines.push(pad('  Mileage cost:',        fp(rmMileCost) + '  (' + miles + ' × ' + fp(vehicle.mileRate) + ')'));
        lines.push(pad('  REMOVALS TOTAL:',      fp(rmNett) + '  nett'));
        lines.push('');
      }
      if (calcMode !== 'removals') {
        lines.push('STORAGE (nett — VAT added at booking)');
        lines.push(pad('  Room(s) required:',    stBits.join(' + ') + (picks.length > 1 || picks[0].qty > 1 ? '  (' + stTotalSqft + ' sqft total, ' + (stTotalSqft * 7).toLocaleString('en-GB') + ' cu ft capacity)' : '')));
        lines.push(pad('  Daily rate:',          fp(stPerDay)));
        lines.push(pad('  Duration:',            days + ' day' + (days === 1 ? '' : 's') + '  (~' + (days / 7).toFixed(days % 7 === 0 ? 0 : 1) + ' weeks)'));
        lines.push(pad('  STORAGE TOTAL:',       fp(stNett) + '  nett'));
        lines.push('');
      }
      lines.push('QUOTE SUMMARY');
      if (calcMode !== 'storage') lines.push(pad('  Removals (nett):',  fp(rmNett)));
      if (calcMode !== 'removals') lines.push(pad('  Storage (nett):',   fp(stNett)));
      lines.push('  ──────────────────────────────────────────────');
      lines.push(pad('  TOTAL (nett):',          fp(rmNett + stNett) + '  (+ VAT at booking)'));
      lines.push('');

      if (roomLines.length > 0) {
        lines.push('INVENTORY  (' + totalItems + ' items · ' + cuft.toLocaleString('en-GB') + ' cu ft)');
        lines.push('');
        lines = lines.concat(roomLines);
      } else {
        lines.push('INVENTORY');
        lines.push('  (No specific items ticked — quote calculated from the cu ft figure.)');
        lines.push('');
      }
      if (notes) {
        lines.push('NOTES FROM CUSTOMER');
        lines.push('  ' + notes.split('\n').join('\n  '));
        lines.push('');
      }
      lines.push('──────────────────────────────────────────────');
      lines.push('Sent from the Mark Ratcliffe Moving online quote calculator.');
      lines.push('Office reply within 48 hours. EMV London Ltd t/a Mark');
      lines.push('Ratcliffe Moving & Storage. Family-run since 1982.');

      var totalNett = rmNett + stNett;
      var subject = 'Quote request — ' + bedSelected.label + ' · ' + (fromPC || 'FROM') +
        ' → ' + (toPC || 'TO') + ' · ' + cuft.toLocaleString('en-GB') + ' cu ft · ' + fp(totalNett) + ' nett';

      var params = 'subject=' + encodeURIComponent(subject) +
                   '&body='  + encodeURIComponent(lines.join('\n'));
      if (email) params = 'cc=' + encodeURIComponent(email) + '&' + params;
      var mailto = 'mailto:office@markratcliffemoving.co.uk?' + params;

      if (status) {
        status.textContent = 'Opening your email app… we send to office@markratcliffemoving.co.uk and CC you a copy. If nothing happens, email office@markratcliffemoving.co.uk directly with the figures from the preview above.';
      }
      window.location.href = mailto;
    });
  }

  recalc();
  // Trigger the inventory auto-fill prompt on first paint (mode permitting).
  if (getCalcMode() !== 'storage') showInventoryPrompt();
})();
