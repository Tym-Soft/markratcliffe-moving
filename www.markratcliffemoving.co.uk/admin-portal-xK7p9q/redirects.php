<?php
require_once __DIR__ . '/_auth.php';
require_once __DIR__ . '/_layout.php';
require_once __DIR__ . '/_lib.php';
require_login();

// Handle delete
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['delete'])) {
    check_csrf();
    $idx = (int)$_POST['delete'];
    $redirects = load_json(REDIRECTS_FILE, []);
    if (isset($redirects[$idx])) {
        array_splice($redirects, $idx, 1);
        save_json(REDIRECTS_FILE, $redirects);
        rebuild_htaccess_redirects();
        flash('Redirect removed.');
    }
    header('Location: redirects.php');
    exit;
}

// Handle manual add
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['add'])) {
    check_csrf();
    $from = trim($_POST['from'] ?? '');
    $to = trim($_POST['to'] ?? '');
    if ($from && $to && $from !== $to) {
        $from = '/' . ltrim($from, '/');
        $to = '/' . ltrim($to, '/');
        $redirects = load_json(REDIRECTS_FILE, []);
        $redirects[] = ['from' => $from, 'to' => $to, 'date' => date('Y-m-d H:i:s')];
        save_json(REDIRECTS_FILE, $redirects);
        rebuild_htaccess_redirects();
        write_redirect_stub($from, $to);
        flash('Redirect added.');
    } else {
        flash('Please provide different from/to paths.', 'error');
    }
    header('Location: redirects.php');
    exit;
}

$redirects = load_json(REDIRECTS_FILE, []);
$csrf = csrf_token();

admin_header('Redirects');
show_flash();
?>

<div class="ab-help">
  301 redirects are added automatically whenever you change a page's slug.
  You can also add one manually here if you have an old URL pointing somewhere new.
</div>

<div class="ab-card">
  <h2 class="ab-h2" style="margin-top:0;">Add a redirect</h2>
  <form method="post">
    <input type="hidden" name="csrf" value="<?= htmlspecialchars($csrf) ?>">
    <input type="hidden" name="add" value="1">
    <div style="display:flex; gap:0.75rem; align-items:end; flex-wrap:wrap;">
      <div style="flex:1; min-width:200px;">
        <label style="font-weight:600; font-size:0.9rem; color:#4a3c70;">From (old path)</label>
        <input class="ab-input" type="text" name="from" placeholder="/old-page.html" required>
      </div>
      <div style="flex:1; min-width:200px;">
        <label style="font-weight:600; font-size:0.9rem; color:#4a3c70;">To (new path)</label>
        <input class="ab-input" type="text" name="to" placeholder="/new-page.html" required>
      </div>
      <button class="ab-btn ab-btn-primary" type="submit">Add 301</button>
    </div>
  </form>
</div>

<h2 class="ab-h2">All redirects (<?= count($redirects) ?>)</h2>

<table class="ab-table">
  <thead><tr><th>From</th><th>To</th><th>Date</th><th></th></tr></thead>
  <tbody>
  <?php if (empty($redirects)): ?>
    <tr><td colspan="4" class="muted">No redirects yet.</td></tr>
  <?php endif; ?>
  <?php foreach ($redirects as $i => $r): ?>
    <tr>
      <td><code><?= htmlspecialchars($r['from']) ?></code></td>
      <td>→ <code><?= htmlspecialchars($r['to']) ?></code></td>
      <td class="muted"><?= htmlspecialchars($r['date'] ?? '—') ?></td>
      <td>
        <form method="post" style="display:inline;" onsubmit="return confirm('Remove this redirect?');">
          <input type="hidden" name="csrf" value="<?= htmlspecialchars($csrf) ?>">
          <input type="hidden" name="delete" value="<?= $i ?>">
          <button class="ab-btn ab-btn-danger" style="padding:0.35rem 0.85rem; font-size:0.85rem;" type="submit">Remove</button>
        </form>
      </td>
    </tr>
  <?php endforeach; ?>
  </tbody>
</table>

<?php admin_footer(); ?>
