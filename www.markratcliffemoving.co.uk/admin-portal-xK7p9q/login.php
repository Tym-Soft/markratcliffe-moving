<?php
require_once __DIR__ . '/_auth.php';
require_once __DIR__ . '/_layout.php';

if (is_logged_in()) {
    header('Location: index.php');
    exit;
}

$error = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    check_csrf();
    $u = trim($_POST['username'] ?? '');
    $p = $_POST['password'] ?? '';
    if (attempt_login($u, $p)) {
        // Regenerate session id post-login (defense against fixation)
        session_regenerate_id(true);
        header('Location: index.php');
        exit;
    }
    $error = 'Invalid username or password.';
    // Add a small delay to slow brute-force attempts
    usleep(rand(300000, 800000));
}

$csrf = csrf_token();
?>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Sign in · Mark Ratcliffe Admin</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex,nofollow">
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div class="ab-login">
    <h1>Sign in</h1>
    <?php if ($error): ?>
      <div class="ab-flash ab-flash-error"><?= htmlspecialchars($error) ?></div>
    <?php endif; ?>
    <form method="post" autocomplete="off">
      <input type="hidden" name="csrf" value="<?= htmlspecialchars($csrf) ?>">
      <div class="ab-form-row">
        <label for="u">Username</label>
        <input class="ab-input" type="text" id="u" name="username" required autofocus>
      </div>
      <div class="ab-form-row">
        <label for="p">Password</label>
        <input class="ab-input" type="password" id="p" name="password" required>
      </div>
      <button class="ab-btn ab-btn-primary" type="submit" style="width:100%;">Sign in</button>
    </form>
  </div>
</body>
</html>
