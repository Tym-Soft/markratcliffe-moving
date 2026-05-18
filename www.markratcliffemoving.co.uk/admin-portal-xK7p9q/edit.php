<?php
require_once __DIR__ . '/_auth.php';
require_once __DIR__ . '/_layout.php';
require_once __DIR__ . '/_lib.php';
require_login();

$is_blog = isset($_GET['blog']);
$slug = $_GET['slug'] ?? ($_GET['blog'] ?? '');
$slug = safe_slug($slug);
if (!$slug) { header('Location: index.php'); exit; }

$json_path = $is_blog ? blog_json_path($slug) : page_json_path($slug);
$data = load_json($json_path);
if (empty($data)) {
    flash('Page not found in JSON store.', 'error');
    header('Location: index.php');
    exit;
}

// Handle save
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    check_csrf();
    $new_slug = safe_slug(trim($_POST['slug'] ?? $slug));
    $data['meta_title']       = trim($_POST['meta_title'] ?? '');
    $data['meta_description'] = trim($_POST['meta_description'] ?? '');
    $data['h1']               = trim($_POST['h1'] ?? '');
    $data['intro_paragraph']  = trim($_POST['intro_paragraph'] ?? '');

    // Alt overrides
    $alts = [];
    if (!empty($_POST['alt']) && is_array($_POST['alt'])) {
        foreach ($_POST['alt'] as $fn => $v) {
            $fn = basename($fn);
            $alts[$fn] = trim($v);
        }
    }
    $data['alt_overrides'] = $alts;

    save_page($new_slug, $data, $slug, $is_blog);

    if ($new_slug !== $slug) {
        flash("Saved. URL changed — old URL now redirects (301) to /$new_slug.html.");
        header('Location: edit.php?' . ($is_blog ? 'blog' : 'slug') . '=' . urlencode($new_slug));
    } else {
        flash('Saved successfully.');
        header('Location: edit.php?' . ($is_blog ? 'blog' : 'slug') . '=' . urlencode($slug));
    }
    exit;
}

$csrf = csrf_token();
$view_url = $is_blog
    ? '../blog/' . htmlspecialchars($slug) . '.html'
    : '../' . htmlspecialchars($slug) . '.html';

admin_header('Edit: ' . ($data['meta_title'] ?? $slug));
show_flash();
?>

<div class="ab-help">
  Fields below map directly to what visitors see. Saving rewrites the page's
  <code>&lt;title&gt;</code>, meta description, H1 and intro paragraph — and any image alt text you edit below.
  <br><strong>Tip:</strong> meta titles work best under 60 characters. Descriptions under 160.
  <br>Preview your live page anytime: <a href="<?= $view_url ?>" target="_blank">open in new tab →</a>
</div>

<form method="post" class="ab-card">
  <input type="hidden" name="csrf" value="<?= htmlspecialchars($csrf) ?>">

  <div class="ab-form-row">
    <label for="slug">
      URL slug
      <small>Changing this creates a 301 redirect from the old URL automatically.</small>
    </label>
    <input class="ab-input" type="text" id="slug" name="slug" value="<?= htmlspecialchars($data['slug']) ?>" required>
    <small>Final URL: <code><?= BASE_URL ?>/<?= $is_blog ? 'blog/' : '' ?><span id="slug-preview"><?= htmlspecialchars($data['slug']) ?></span>.html</code></small>
  </div>

  <div class="ab-form-row">
    <label for="meta_title">
      Meta title
      <span class="ab-charcount" id="cc-title">0 / 60</span>
    </label>
    <input class="ab-input" type="text" id="meta_title" name="meta_title"
           value="<?= htmlspecialchars($data['meta_title'] ?? '') ?>" required>
    <small>Shows in browser tabs and search results.</small>
  </div>

  <div class="ab-form-row">
    <label for="meta_description">
      Meta description
      <span class="ab-charcount" id="cc-desc">0 / 160</span>
    </label>
    <textarea class="ab-textarea" id="meta_description" name="meta_description" rows="2"><?= htmlspecialchars($data['meta_description'] ?? '') ?></textarea>
    <small>The summary that appears under your page in Google results.</small>
  </div>

  <div class="ab-form-row">
    <label for="h1">H1 heading</label>
    <input class="ab-input" type="text" id="h1" name="h1" value="<?= htmlspecialchars($data['h1'] ?? '') ?>">
    <small>The main heading on the page. Only one H1 per page (this one).</small>
  </div>

  <div class="ab-form-row">
    <label for="intro_paragraph">Intro paragraph</label>
    <textarea class="ab-textarea ab-textarea-large" id="intro_paragraph" name="intro_paragraph" rows="4"><?= htmlspecialchars($data['intro_paragraph'] ?? '') ?></textarea>
    <small>The first paragraph under the hero. Plain text or simple HTML is allowed.</small>
  </div>

  <?php if (!empty($data['images']) && is_array($data['images'])): ?>
    <h2 class="ab-h2">Image alt text</h2>
    <small>Update the alt text on each image. Empty alt = decorative.</small>
    <ul class="ab-alt-list">
      <?php foreach ($data['images'] as $img):
        $src = $img['src'] ?? '';
        if (!$src) continue;
        $fn = basename($src);
        $current_alt = $data['alt_overrides'][$fn] ?? ($img['alt'] ?? '');
        $img_url = $is_blog ? '../' . $src : '../' . $src;
      ?>
        <li>
          <img src="<?= htmlspecialchars($img_url) ?>" alt="" onerror="this.style.display='none'">
          <div class="img-info">
            <code><?= htmlspecialchars($fn) ?></code>
          </div>
          <input type="text" name="alt[<?= htmlspecialchars($fn) ?>]"
                 value="<?= htmlspecialchars($current_alt) ?>"
                 placeholder="Describe the image (or leave empty if decorative)">
        </li>
      <?php endforeach; ?>
    </ul>
  <?php endif; ?>

  <div class="ab-btn-row">
    <button type="submit" class="ab-btn ab-btn-primary">Save changes</button>
    <a href="index.php" class="ab-btn ab-btn-secondary">Cancel</a>
    <a href="<?= $view_url ?>" class="ab-btn ab-btn-secondary" target="_blank">View live page</a>
  </div>
</form>

<script>
// Character counters and live slug preview
function bind(id, max, target) {
  var el = document.getElementById(id);
  var out = document.getElementById(target);
  function up() {
    var l = el.value.length;
    out.textContent = l + ' / ' + max;
    out.style.color = (l > max) ? '#dc3545' : '#6b5d8f';
  }
  el.addEventListener('input', up); up();
}
bind('meta_title', 60, 'cc-title');
bind('meta_description', 160, 'cc-desc');
var slugIn = document.getElementById('slug'), slugPv = document.getElementById('slug-preview');
slugIn.addEventListener('input', function () { slugPv.textContent = slugIn.value.replace(/[^a-zA-Z0-9_\-\/]/g, ''); });
</script>

<?php admin_footer(); ?>
