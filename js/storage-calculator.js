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

  function loadSizeLabel(cuft) {
    if (cuft === 0)    return 'No items selected';
    if (cuft <= 80)    return '~ Small-van load';
    if (cuft <= 250)   return '~ Luton van load';
    if (cuft <= 600)   return '~ 3.5-tonne lorry';
    if (cuft <= 1100)  return '~ 7.5-tonne lorry';
    if (cuft <= 1700)  return '~ 18-tonne lorry';
    return '~ Artic lorry / multiple loads';
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
    totalCuft.textContent   = Math.round(cuft);
    totalCum.textContent    = cum.toFixed(2);
    totalKg.textContent     = Math.round(kg);
    vanEstimate.textContent = loadSizeLabel(Math.round(cuft));
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

  recalc();
})();
