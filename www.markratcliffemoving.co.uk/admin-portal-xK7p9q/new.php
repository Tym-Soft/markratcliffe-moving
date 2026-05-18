<?php
require_once __DIR__ . '/_auth.php';
require_once __DIR__ . '/_layout.php';
require_once __DIR__ . '/_lib.php';
require_login();

$is_blog = ($_GET['type'] ?? '') === 'blog';
$error = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    check_csrf();
    $slug = safe_slug(trim($_POST['slug'] ?? ''));
    $title = trim($_POST['meta_title'] ?? '');
    $desc  = trim($_POST['meta_description'] ?? '');
    $h1    = trim($_POST['h1'] ?? '');
    $intro = trim($_POST['intro_paragraph'] ?? '');

    if (!$slug || !$title || !$h1) {
        $error = 'Slug, title and H1 are required.';
    } else {
        list($ok, $info) = create_new_page($slug, $title, $desc, $h1, $intro, $is_blog);
        if ($ok) {
            flash('New ' . ($is_blog ? 'blog post' : 'page') . ' created. Editing now.');
            header('Location: edit.php?' . ($is_blog ? 'blog' : 'slug') . '=' . urlencode($slug));
            exit;
        } else {
            $error = $info;
        }
    }
}

$csrf = csrf_token();
admin_header('New ' . ($is_blog ? 'blog post' : 'page'));
show_flash();
?>

<div class="ab-help">
  Create a new <?= $is_blog ? 'blog post' : 'page' ?>. We'll generate the HTML from a clean template &mdash;
  you can fill in the rest of the body in the editor afterwards.
</div>

<?php if ($error): ?>
  <div class="ab-flash ab-flash-error"><?= htmlspecialchars($error) ?></div>
<?php endif; ?>

<form method="post" class="ab-card">
  <input type="hidden" name="csrf" value="<?= htmlspecialchars($csrf) ?>">

  <div class="ab-form-row">
    <label for="slug">URL slug <small>Lowercase letters, numbers, hyphens. No spaces.</small></label>
    <input class="ab-input" type="text" id="slug" name="slug" placeholder="<?= $is_blog ? 'best-moving-tips-eastbourne' : 'new-service-page' ?>" required>
    <small>The page will live at <code><?= BASE_URL ?>/<?= $is_blog ? 'blog/' : '' ?><span id="slug-preview">slug</span>.html</code></small>
  </div>

  <div class="ab-form-row">
    <label for="meta_title">Meta title <span class="ab-charcount" id="cc-title">0 / 60</span></label>
    <input class="ab-input" type="text" id="meta_title" name="meta_title" required>
  </div>

  <div class="ab-form-row">
    <label for="meta_description">Meta description <span class="ab-charcount" id="cc-desc">0 / 160</span></label>
    <textarea class="ab-textarea" id="meta_description" name="meta_description" rows="2"></textarea>
  </div>

  <div class="ab-form-row">
    <label for="h1">H1 heading <small>This is what visitors see as the big page title.</small></label>
    <input class="ab-input" type="text" id="h1" name="h1" required>
  </div>

  <div class="ab-form-row">
    <label for="intro_paragraph">Intro paragraph</label>
    <textarea class="ab-textarea" id="intro_paragraph" name="intro_paragraph" rows="3" placeholder="Write a short opening paragraph that introduces this page&hellip;"></textarea>
  </div>

  <div class="ab-btn-row">
    <button type="submit" class="ab-btn ab-btn-primary">Create &amp; continue editing</button>
    <a href="index.php" class="ab-btn ab-btn-secondary">Cancel</a>
  </div>
</form>

<script>
function bind(id, max, target) {
  var el = document.getElementById(id), out = document.getElementById(target);
  function up() { var l = el.value.length; out.textContent = l + ' / ' + max; out.style.color = (l > max) ? '#dc3545' : '#6b5d8f'; }
  el.addEventListener('input', up); up();
}
bind('meta_title', 60, 'cc-title');
bind('meta_description', 160, 'cc-desc');
var slugIn = document.getElementById('slug'), slugPv = document.getElementById('slug-preview');
slugIn.addEventListener('input', function () { slugPv.textContent = (slugIn.value.replace(/[^a-z0-9-]/gi, '').toLowerCase()) || 'slug'; });
</script>

<?php admin_footer(); ?>
