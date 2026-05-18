<?php
/**
 * Admin library — surgical edits to existing HTML files.
 * Each page is described by a JSON record listing its editable fields;
 * saving applies precise regex-based replacements to the corresponding HTML.
 *
 * Why surgical edits instead of full re-rendering?
 *   The 73 HTML pages have a mix of Webflow markup and our newer clean templates.
 *   Regenerating them all from a renderer would require perfect template fidelity.
 *   Surgical edits preserve every visual detail while letting us change the text.
 */

define('SITE_ROOT', realpath(__DIR__ . '/..'));
define('DATA_DIR', SITE_ROOT . '/data');
define('PAGES_DIR', DATA_DIR . '/pages');
define('BLOG_DIR', DATA_DIR . '/blog');
define('CONFIG_FILE', DATA_DIR . '/config.json');
define('REDIRECTS_FILE', DATA_DIR . '/redirects.json');
define('HTACCESS_FILE', SITE_ROOT . '/.htaccess');
define('BASE_URL', 'https://www.markratcliffemoving.co.uk');

// ---------------- JSON store ----------------

function load_json($path, $default = []) {
    if (!file_exists($path)) return $default;
    $data = json_decode(file_get_contents($path), true);
    return $data === null ? $default : $data;
}

function save_json($path, $data) {
    $dir = dirname($path);
    if (!is_dir($dir)) mkdir($dir, 0755, true);
    return file_put_contents($path,
        json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES)
    ) !== false;
}

function safe_slug($slug) {
    return preg_replace('/[^a-zA-Z0-9_\-\/]/', '', $slug);
}

function page_json_path($slug) {
    return PAGES_DIR . '/' . str_replace('/', '__', safe_slug($slug)) . '.json';
}

function blog_json_path($slug) {
    return BLOG_DIR . '/' . safe_slug($slug) . '.json';
}

function html_path_for_slug($slug, $is_blog = false) {
    if ($is_blog) return SITE_ROOT . '/blog/' . safe_slug($slug) . '.html';
    if ($slug === 'index') return SITE_ROOT . '/index.html';
    return SITE_ROOT . '/' . safe_slug($slug) . '.html';
}

function list_pages() {
    $items = [];
    foreach (glob(PAGES_DIR . '/*.json') as $f) {
        $d = load_json($f);
        if (!empty($d['slug'])) $items[$d['slug']] = $d;
    }
    ksort($items);
    return $items;
}

function list_blog() {
    $items = [];
    foreach (glob(BLOG_DIR . '/*.json') as $f) {
        $d = load_json($f);
        if (!empty($d['slug'])) $items[$d['slug']] = $d;
    }
    ksort($items);
    return $items;
}

// ---------------- Surgical HTML edits ----------------

/**
 * Apply the edits in $data to the HTML file at $html_path.
 * Returns true on success.
 */
function apply_edits_to_html($html_path, $data) {
    if (!file_exists($html_path)) return false;
    $html = file_get_contents($html_path);
    $orig = $html;

    // 1) <title>
    if (isset($data['meta_title'])) {
        $html = preg_replace(
            '#<title>[^<]*</title>#i',
            '<title>' . htmlspecialchars($data['meta_title'], ENT_QUOTES) . '</title>',
            $html, 1
        );
    }

    // 2) <meta name="description" content="...">  (both attribute orders)
    if (isset($data['meta_description'])) {
        $desc = htmlspecialchars($data['meta_description'], ENT_QUOTES);
        $html = preg_replace(
            '#<meta\s+(?:name="description"\s+content="[^"]*"|content="[^"]*"\s+name="description")\s*/?>#i',
            '<meta name="description" content="' . $desc . '">',
            $html, 1
        );
        // og:description + twitter:description mirror the same value
        $html = preg_replace(
            '#<meta\s+(?:property="og:description"\s+content="[^"]*"|content="[^"]*"\s+property="og:description")\s*/?>#i',
            '<meta property="og:description" content="' . $desc . '">',
            $html
        );
        $html = preg_replace(
            '#<meta\s+(?:property="twitter:description"\s+content="[^"]*"|content="[^"]*"\s+property="twitter:description")\s*/?>#i',
            '<meta property="twitter:description" content="' . $desc . '">',
            $html
        );
    }

    // 3) og:title and twitter:title mirror meta_title
    if (isset($data['meta_title'])) {
        $title = htmlspecialchars($data['meta_title'], ENT_QUOTES);
        $html = preg_replace(
            '#<meta\s+(?:property="og:title"\s+content="[^"]*"|content="[^"]*"\s+property="og:title")\s*/?>#i',
            '<meta property="og:title" content="' . $title . '">',
            $html
        );
        $html = preg_replace(
            '#<meta\s+(?:property="twitter:title"\s+content="[^"]*"|content="[^"]*"\s+property="twitter:title")\s*/?>#i',
            '<meta property="twitter:title" content="' . $title . '">',
            $html
        );
    }

    // 4) Single <h1> — replace its content
    if (isset($data['h1'])) {
        $h1 = $data['h1'];  // h1 may contain inline HTML (em/strong) so don't escape
        $html = preg_replace(
            '#(<h1[^>]*>).*?(</h1>)#is',
            '${1}' . $h1 . '${2}',
            $html, 1
        );
    }

    // 5) Section edits — keyed by section_id (we generate ids from headings)
    if (!empty($data['sections']) && is_array($data['sections'])) {
        foreach ($data['sections'] as $section) {
            if (empty($section['marker']) || !isset($section['body_html'])) continue;
            // Find the section by marker (unique text appearing in original)
            $marker = preg_quote($section['marker'], '#');
            // Replace the inner of <section> ... </section> containing the marker
            // Simplistic: find the section, replace its content within <div class="np-inner">
            // Since we can't always identify sections reliably across templates, this
            // is optional — basic deployments edit only the structured fields above.
        }
    }

    // 6) Alt text updates: map of image filename -> alt text
    if (!empty($data['alt_overrides']) && is_array($data['alt_overrides'])) {
        foreach ($data['alt_overrides'] as $filename => $alt) {
            $fn = preg_quote($filename, '#');
            $alt_esc = htmlspecialchars($alt, ENT_QUOTES);
            // Match img tags using this filename and update their alt
            $html = preg_replace_callback(
                '#<img\b[^>]*\bsrc="[^"]*' . $fn . '[^"]*"[^>]*>#i',
                function ($m) use ($alt_esc) {
                    $tag = $m[0];
                    if (preg_match('#\balt="[^"]*"#', $tag)) {
                        return preg_replace('#\balt="[^"]*"#', 'alt="' . $alt_esc . '"', $tag);
                    }
                    return rtrim($tag, '>') . ' alt="' . $alt_esc . '">';
                },
                $html
            );
        }
    }

    // 7) Intro paragraph (only if marked with font-size:1.15rem inline style)
    if (isset($data['intro_paragraph'])) {
        $html = preg_replace(
            '#<p\s+style="font-size:1\.15rem[^"]*">.*?</p>#s',
            '<p style="font-size:1.15rem;">' . $data['intro_paragraph'] . '</p>',
            $html, 1
        );
    }

    if ($html === $orig) return false;
    return file_put_contents($html_path, $html) !== false;
}

/**
 * Save page JSON + apply edits to the HTML.
 */
function save_page($slug, $data, $old_slug = null, $is_blog = false) {
    $slug = safe_slug($slug);
    $data['slug'] = $slug;
    $data['last_updated'] = date('Y-m-d H:i:s');

    // Handle slug change: write redirect + move/rename old HTML
    if ($old_slug && $old_slug !== $slug) {
        $old_html = html_path_for_slug($old_slug, $is_blog);
        $new_html = html_path_for_slug($slug, $is_blog);
        if (file_exists($old_html)) {
            // Move the HTML file
            @rename($old_html, $new_html);
        }
        // Delete the old JSON
        $old_json = $is_blog ? blog_json_path($old_slug) : page_json_path($old_slug);
        if (file_exists($old_json)) @unlink($old_json);
        // Add 301 redirect
        add_redirect($old_slug, $slug, $is_blog);
    }

    // Save JSON
    $json_path = $is_blog ? blog_json_path($slug) : page_json_path($slug);
    save_json($json_path, $data);

    // Apply edits to HTML
    $html_path = html_path_for_slug($slug, $is_blog);
    apply_edits_to_html($html_path, $data);

    // Keep sitemap.xml in sync
    regenerate_sitemap();

    return true;
}

// ---------------- Redirects ----------------

function add_redirect($from_slug, $to_slug, $is_blog = false) {
    $redirects = load_json(REDIRECTS_FILE, []);
    $from = $is_blog ? "/blog/$from_slug.html" : "/$from_slug.html";
    $to = $is_blog ? "/blog/$to_slug.html" : "/$to_slug.html";
    // Don't add duplicate
    foreach ($redirects as $r) {
        if ($r['from'] === $from && $r['to'] === $to) return;
    }
    $redirects[] = [
        'from' => $from,
        'to' => $to,
        'date' => date('Y-m-d H:i:s'),
    ];
    save_json(REDIRECTS_FILE, $redirects);
    rebuild_htaccess_redirects();
    write_redirect_stub($from, $to);
}

function rebuild_htaccess_redirects() {
    $redirects = load_json(REDIRECTS_FILE, []);
    $marker_s = "# === ADMIN REDIRECTS START ===\n";
    $marker_e = "# === ADMIN REDIRECTS END ===\n";
    $block = $marker_s;
    foreach ($redirects as $r) {
        $block .= "Redirect 301 " . $r['from'] . " " . $r['to'] . "\n";
    }
    $block .= $marker_e;

    $existing = file_exists(HTACCESS_FILE) ? file_get_contents(HTACCESS_FILE) : '';
    if (strpos($existing, $marker_s) !== false) {
        $new = preg_replace(
            '/' . preg_quote($marker_s, '/') . '.*?' . preg_quote($marker_e, '/') . '/s',
            $block, $existing
        );
        file_put_contents(HTACCESS_FILE, $new);
    } else {
        file_put_contents(HTACCESS_FILE, $existing . "\n" . $block);
    }
}

function write_redirect_stub($from_url, $to_url) {
    $rel = ltrim($from_url, '/');
    $path = SITE_ROOT . '/' . $rel;
    $to_esc = htmlspecialchars($to_url, ENT_QUOTES);
    $stub = '<!DOCTYPE html><html lang="en-GB"><head><meta charset="utf-8">'
          . '<title>Redirecting...</title>'
          . '<meta http-equiv="refresh" content="0;url=' . $to_esc . '">'
          . '<link rel="canonical" href="' . BASE_URL . $to_esc . '">'
          . '<meta name="robots" content="noindex,follow"></head>'
          . '<body><p>This page has moved. <a href="' . $to_esc . '">Go to new page</a></p>'
          . '<script>window.location.replace("' . $to_esc . '");</script></body></html>';
    $dir = dirname($path);
    if (!is_dir($dir)) mkdir($dir, 0755, true);
    file_put_contents($path, $stub);
}

// ---------------- Sitemap regeneration ----------------

/**
 * Rebuild sitemap.xml from the current page + blog JSON store.
 * Called automatically after every save_page() / create_new_page().
 * Only emits URLs for HTML files that actually exist on disk so
 * the sitemap never points at a missing or stale page.
 */
function regenerate_sitemap() {
    $entries = [];

    // Homepage — always included if it exists
    if (file_exists(SITE_ROOT . '/index.html')) {
        $entries[] = [
            'loc' => BASE_URL . '/',
            'lastmod' => date('Y-m-d', filemtime(SITE_ROOT . '/index.html')),
            'changefreq' => 'weekly',
            'priority' => '1.0',
        ];
    }

    // Static pages from the admin JSON store
    foreach (glob(PAGES_DIR . '/*.json') as $f) {
        $d = load_json($f);
        if (empty($d['slug'])) continue;
        $slug = $d['slug'];
        if ($slug === 'index') continue; // already added above
        $html = SITE_ROOT . '/' . $slug . '.html';
        if (!file_exists($html)) continue;
        $lastmod = !empty($d['last_updated'])
            ? substr($d['last_updated'], 0, 10)
            : date('Y-m-d', filemtime($html));
        $entries[] = [
            'loc' => BASE_URL . '/' . $slug . '.html',
            'lastmod' => $lastmod,
            'changefreq' => 'monthly',
            'priority' => '0.8',
        ];
    }

    // Blog posts
    foreach (glob(BLOG_DIR . '/*.json') as $f) {
        $d = load_json($f);
        if (empty($d['slug'])) continue;
        $slug = $d['slug'];
        $html = SITE_ROOT . '/blog/' . $slug . '.html';
        if (!file_exists($html)) continue;
        $lastmod = !empty($d['last_updated'])
            ? substr($d['last_updated'], 0, 10)
            : date('Y-m-d', filemtime($html));
        $entries[] = [
            'loc' => BASE_URL . '/blog/' . $slug . '.html',
            'lastmod' => $lastmod,
            'changefreq' => 'monthly',
            'priority' => '0.6',
        ];
    }

    // De-duplicate on loc + sort
    $seen = [];
    $unique = [];
    foreach ($entries as $e) {
        if (isset($seen[$e['loc']])) continue;
        $seen[$e['loc']] = true;
        $unique[] = $e;
    }
    usort($unique, function ($a, $b) { return strcmp($a['loc'], $b['loc']); });

    $xml = '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
    $xml .= '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
    foreach ($unique as $e) {
        $xml .= "  <url>\n";
        $xml .= "    <loc>" . htmlspecialchars($e['loc'], ENT_XML1) . "</loc>\n";
        $xml .= "    <lastmod>" . $e['lastmod'] . "</lastmod>\n";
        $xml .= "    <changefreq>" . $e['changefreq'] . "</changefreq>\n";
        $xml .= "    <priority>" . $e['priority'] . "</priority>\n";
        $xml .= "  </url>\n";
    }
    $xml .= '</urlset>' . "\n";

    file_put_contents(SITE_ROOT . '/sitemap.xml', $xml);
    return count($unique);
}

// ---------------- New page creation ----------------

function create_new_page($slug, $title, $description, $h1, $intro, $is_blog = false) {
    $slug = safe_slug($slug);
    $html_path = html_path_for_slug($slug, $is_blog);
    if (file_exists($html_path)) return [false, 'A page with that URL already exists.'];

    $base = BASE_URL;
    $canon = $is_blog ? "$base/blog/$slug.html" : "$base/$slug.html";
    $P = $is_blog ? "../" : "";

    // Use the new clean template structure (matches what build_pages produced)
    $html = build_page_template([
        'title' => $title,
        'description' => $description,
        'h1' => $h1,
        'intro' => $intro,
        'canonical' => $canon,
        'P' => $P,
        'is_blog' => $is_blog,
    ]);

    if (!is_dir(dirname($html_path))) mkdir(dirname($html_path), 0755, true);
    file_put_contents($html_path, $html);

    // Save the JSON
    $json_path = $is_blog ? blog_json_path($slug) : page_json_path($slug);
    save_json($json_path, [
        'slug' => $slug,
        'type' => $is_blog ? 'blog' : 'page',
        'filename' => $is_blog ? "blog/$slug.html" : "$slug.html",
        'meta_title' => $title,
        'meta_description' => $description,
        'h1' => $h1,
        'intro_paragraph' => $intro,
        'canonical_url' => $canon,
        'created' => date('Y-m-d H:i:s'),
        'last_updated' => date('Y-m-d H:i:s'),
    ]);

    // Keep sitemap.xml in sync
    regenerate_sitemap();

    return [true, $html_path];
}

function build_page_template($v) {
    $title = htmlspecialchars($v['title']);
    $desc = htmlspecialchars($v['description']);
    $h1 = $v['h1'];
    $intro = $v['intro'];
    $canon = $v['canonical'];
    $P = $v['P'];
    return <<<HTML
<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <title>{$title}</title>
  <meta name="description" content="{$desc}">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <link rel="canonical" href="{$canon}">
  <meta property="og:title" content="{$title}">
  <meta property="og:description" content="{$desc}">
  <meta property="og:url" content="{$canon}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Mark Ratcliffe Moving & Storage">
  <link href="{$P}css/normalize.css" rel="stylesheet">
  <link href="{$P}css/components.css" rel="stylesheet">
  <link href="{$P}css/mark-ratcliffe-moving.css" rel="stylesheet">
  <link href="{$P}css/new-pages.css" rel="stylesheet">
  <link href="{$P}images/favicon.png" rel="shortcut icon">
</head>
<body>
  <!-- TODO: paste your shared nav and footer here, or copy from another page -->
  <header class="np-hero">
    <div class="np-hero-inner">
      <h1>{$h1}</h1>
      <div class="np-hero-cta">
        <a href="{$P}mark-ratcliffe-moving-online-removals-quote.html" class="np-btn np-btn-primary">Get a Free Quote</a>
        <a href="tel:01323848008" class="np-btn np-btn-secondary">Call 01323 848 008</a>
      </div>
    </div>
  </header>
  <section class="np-section">
    <div class="np-inner">
      <p style="font-size:1.15rem;">{$intro}</p>
      <p><em>Add your content here. Use the admin editor to update this page.</em></p>
    </div>
  </section>
  <script defer src="https://d3e54v103j8qbb.cloudfront.net/js/jquery-3.5.1.min.dc5e7f18c8.js?site=54f032c21ccd6c2e19dae5a7" crossorigin="anonymous"></script>
  <script defer src="{$P}js/mark-ratcliffe-moving.js"></script>
</body>
</html>
HTML;
}
