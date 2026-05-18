<?php
require_once __DIR__ . '/_auth.php';
require_once __DIR__ . '/_layout.php';
require_once __DIR__ . '/_lib.php';
require_login();

$pages = list_pages();
$posts = list_blog();

admin_header('Dashboard');
show_flash();
?>

<div class="ab-help">
  Welcome. Use the cards below to edit existing pages, create new ones, or manage redirects.
  All changes write a JSON copy to <code>/data/</code> and update the live HTML file in place.
</div>

<div class="ab-card">
  <h2 class="ab-h2" style="margin-top:0;">Quick actions</h2>
  <div class="ab-btn-row" style="margin-top:0;">
    <a class="ab-btn ab-btn-primary" href="new.php">+ New page</a>
    <a class="ab-btn ab-btn-primary" href="new.php?type=blog">+ New blog post</a>
    <a class="ab-btn ab-btn-secondary" href="redirects.php">Redirects (<?= count(load_json(REDIRECTS_FILE, [])) ?>)</a>
    <a class="ab-btn ab-btn-secondary" href="settings.php">Settings</a>
  </div>
</div>

<h2 class="ab-h2">Pages (<?= count($pages) ?>)</h2>
<table class="ab-table">
  <thead><tr><th>Slug / URL</th><th>Title</th><th>Last updated</th><th></th></tr></thead>
  <tbody>
  <?php foreach ($pages as $slug => $p): ?>
    <tr>
      <td>
        <a href="edit.php?slug=<?= urlencode($slug) ?>"><?= htmlspecialchars($slug) ?></a>
        <?php if (!empty($p['type']) && $p['type'] === 'home'): ?>
          <span class="ab-pill">home</span>
        <?php endif; ?>
        <div class="muted">/<?= htmlspecialchars($slug) ?>.html</div>
      </td>
      <td><?= htmlspecialchars(mb_strimwidth($p['meta_title'] ?? '', 0, 70, '…')) ?></td>
      <td class="muted"><?= htmlspecialchars($p['last_updated'] ?? '—') ?></td>
      <td><a href="edit.php?slug=<?= urlencode($slug) ?>">Edit →</a></td>
    </tr>
  <?php endforeach; ?>
  </tbody>
</table>

<h2 class="ab-h2">Blog posts (<?= count($posts) ?>)</h2>
<table class="ab-table">
  <thead><tr><th>Slug</th><th>Title</th><th>Last updated</th><th></th></tr></thead>
  <tbody>
  <?php foreach ($posts as $slug => $p): ?>
    <tr>
      <td>
        <a href="edit.php?blog=<?= urlencode($slug) ?>"><?= htmlspecialchars($slug) ?></a>
        <span class="ab-pill ab-pill-blog">blog</span>
        <div class="muted">/blog/<?= htmlspecialchars($slug) ?>.html</div>
      </td>
      <td><?= htmlspecialchars(mb_strimwidth($p['meta_title'] ?? '', 0, 70, '…')) ?></td>
      <td class="muted"><?= htmlspecialchars($p['last_updated'] ?? '—') ?></td>
      <td><a href="edit.php?blog=<?= urlencode($slug) ?>">Edit →</a></td>
    </tr>
  <?php endforeach; ?>
  </tbody>
</table>

<?php admin_footer(); ?>
