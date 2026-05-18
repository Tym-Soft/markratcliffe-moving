<?php
require_once __DIR__ . '/_auth.php';
require_once __DIR__ . '/_layout.php';
require_once __DIR__ . '/_lib.php';
require_login();

$cfg = admin_config();
$msg = '';
$type = 'success';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    check_csrf();
    $current = $_POST['current'] ?? '';
    $new1 = $_POST['new1'] ?? '';
    $new2 = $_POST['new2'] ?? '';
    if (empty($cfg['admin']['password_hash']) || password_verify($current, $cfg['admin']['password_hash'])) {
        if (strlen($new1) < 10) {
            $msg = 'New password must be at least 10 characters.'; $type = 'error';
        } elseif ($new1 !== $new2) {
            $msg = 'New passwords do not match.'; $type = 'error';
        } else {
            $cfg['admin']['password_hash'] = password_hash($new1, PASSWORD_BCRYPT);
            save_json(CONFIG_FILE, $cfg);
            $msg = 'Password updated.';
        }
    } else {
        $msg = 'Current password is incorrect.'; $type = 'error';
    }
    flash($msg, $type);
    header('Location: settings.php');
    exit;
}

$csrf = csrf_token();
admin_header('Settings');
show_flash();
?>

<div class="ab-card">
  <h2 class="ab-h2" style="margin-top:0;">Account</h2>
  <p>Logged in as <strong><?= htmlspecialchars($cfg['admin']['username'] ?? '—') ?></strong></p>
</div>

<div class="ab-card">
  <h2 class="ab-h2" style="margin-top:0;">Change password</h2>
  <form method="post" autocomplete="off">
    <input type="hidden" name="csrf" value="<?= htmlspecialchars($csrf) ?>">
    <div class="ab-form-row">
      <label for="current">Current password</label>
      <input class="ab-input" type="password" id="current" name="current" required>
    </div>
    <div class="ab-form-row">
      <label for="new1">New password <small>At least 10 characters. Mix of letters, numbers, symbols recommended.</small></label>
      <input class="ab-input" type="password" id="new1" name="new1" minlength="10" required>
    </div>
    <div class="ab-form-row">
      <label for="new2">Confirm new password</label>
      <input class="ab-input" type="password" id="new2" name="new2" minlength="10" required>
    </div>
    <button class="ab-btn ab-btn-primary" type="submit">Update password</button>
  </form>
</div>

<div class="ab-card">
  <h2 class="ab-h2" style="margin-top:0;">Site info</h2>
  <p class="muted">Base URL: <code><?= htmlspecialchars($cfg['base_url'] ?? BASE_URL) ?></code></p>
  <p class="muted">Data folder: <code>/data/</code></p>
  <p class="muted">.htaccess: <code><?= file_exists(HTACCESS_FILE) ? 'present' : 'missing' ?></code></p>
</div>

<?php admin_footer(); ?>
