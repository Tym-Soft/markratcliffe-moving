/* Mark Ratcliffe Moving — storage calculator
 * Reads quantity inputs across the page (each carries data-cuft, data-cum,
 * data-kg attributes) and updates the live totals + load-size estimate.
 * Served from 'self' so the CSP allows it.
 */
(function () {
  'use strict';
  var root = document.getElementById('storage-calc');
  if (!root) return;
  var inputs       = root.querySelectorAll('input[type="number"]');
  var totalCuft    = document.getElementById('total-cuft');
  var totalCum     = document.getElementById('total-cum');
  var totalKg      = document.getElementById('total-kg');
  var vanEstimate  = document.getElementById('van-estimate');
  var resetBtn     = document.getElementById('calc-reset');

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

  for (var i = 0; i < inputs.length; i++) {
    inputs[i].addEventListener('input', recalc);
    inputs[i].addEventListener('change', recalc);
  }
  if (resetBtn) {
    resetBtn.addEventListener('click', function () {
      for (var i = 0; i < inputs.length; i++) inputs[i].value = 0;
      recalc();
    });
  }

  // Initial calc in case the browser preserved values on reload
  recalc();
})();
