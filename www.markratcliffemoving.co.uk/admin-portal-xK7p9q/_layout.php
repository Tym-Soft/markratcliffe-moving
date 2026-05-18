<?php
/**
 * Admin layout wrapper. Usage:
 *   admin_header('Page title');
 *   ... content ...
 *   admin_footer();
 */
function admin_header($title = 'Admin') {
    $h_title = htmlspecialchars($title);
    $is_logged = function_exists('is_logged_in') && is_logged_in();
    $logout = $is_logged ? '<a class="ab-link" href="logout.php">Logout</a>' : '';
    $nav = '';
    if ($is_logged) {
        $nav = '<nav class="ab-nav">
          <a href="index.php">Dashboard</a>
          <a href="pages.php">Pages</a>
          <a href="blog.php">Blog Posts</a>
          <a href="new.php">+ New Page</a>
          <a href="new.php?type=blog">+ New Blog Post</a>
          <a href="redirects.php">Redirects</a>
          <a href="settings.php">Settings</a>
        </nav>';
    }
    echo <<<HTML
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{$h_title} · Mark Ratcliffe Admin</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex,nofollow">
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <header class="ab-topbar">
    <div class="ab-brand">Mark Ratcliffe · Admin</div>
    {$logout}
  </header>
  {$nav}
  <main class="ab-main">
    <h1 class="ab-h1">{$h_title}</h1>
HTML;
}

function admin_footer() {
    echo <<<HTML
  </main>
</body>
</html>
HTML;
}

function flash($msg, $type = 'success') {
    $_SESSION['flash'] = ['msg' => $msg, 'type' => $type];
}

function show_flash() {
    if (!empty($_SESSION['flash'])) {
        $f = $_SESSION['flash'];
        $class = $f['type'] === 'error' ? 'ab-flash ab-flash-error' : 'ab-flash';
        echo '<div class="' . $class . '">' . htmlspecialchars($f['msg']) . '</div>';
        unset($_SESSION['flash']);
    }
}
