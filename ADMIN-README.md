# Mark Ratcliffe Moving — Admin System

A simple, file-based admin that lets you edit pages, meta tags, alt text, and create new pages or blog posts. No database needed.

---

## 1 · First-time setup (5 minutes)

### Required: PHP shared hosting

This admin runs on standard PHP shared hosting (cPanel, Hostinger, SiteGround, Bluehost, etc.). **PHP 7.4 or newer** is required (almost every host has 8.x by default — that's fine).

### Upload
Upload the **entire** `www.markratcliffemoving.co.uk/` folder to your web root (typically `public_html/` or `htdocs/`). Make sure these end up in your live root:

```
public_html/
├── index.html                      ← public pages
├── removals-eastbourne.html
├── ... (all other pages)
├── images/
├── css/
├── js/
├── blog/
├── areas-covered/
├── .htaccess                       ← important! controls redirects + security
├── admin-portal-xK7p9q/            ← the hidden admin
└── data/                           ← JSON content store (DENY enforced by .htaccess)
```

### Set permissions
The admin needs to **write** to two folders on save:

```bash
chmod 755 data/ data/pages/ data/blog/ admin-portal-xK7p9q/
chmod 644 data/*.json data/pages/*.json data/blog/*.json
```

On cPanel, set folder perms to 755 and file perms to 644 via File Manager. The web server user (often `www-data` or your cPanel user) must own them.

---

## 2 · Logging in

### Admin URL
```
https://www.markratcliffemoving.co.uk/admin-portal-xK7p9q/login.php
```

### Credentials
Open `ADMIN_CREDENTIALS.txt` (in the project root, **NOT** uploaded to the server). You'll see:

```
Username : mark
Password : (a randomly generated strong password)
```

**On first login:**
1. Sign in
2. Go to **Settings** in the top menu
3. Set a new password you'll remember
4. Delete `ADMIN_CREDENTIALS.txt` from your computer

---

## 3 · Rename the admin folder (recommended security step)

The default folder name `admin-portal-xK7p9q/` is hidden but predictable. Rename it before going live:

```bash
mv admin-portal-xK7p9q my-cms-2026
```

Your new admin URL becomes `https://www.markratcliffemoving.co.uk/my-cms-2026/login.php`.

No code changes needed — the admin uses **relative paths** for everything.

---

## 4 · How to use the admin

### Dashboard
Lists every page and blog post on the site, with their slug, title, and last updated date. Click any row to edit.

### Edit page
The editor shows you the only fields that matter for SEO and content:

| Field | Where it shows on the page |
|---|---|
| **URL slug** | The web address (changing this creates a 301 redirect automatically) |
| **Meta title** | The `<title>` — appears in browser tabs & Google results. Keep under 60 chars. |
| **Meta description** | The summary under your page in Google results. Keep under 160 chars. |
| **H1 heading** | The main big heading on the page |
| **Intro paragraph** | The first paragraph after the hero. |
| **Image alt text** | Per-image accessibility/SEO text. Lists every image on the page. |

Live character counters tell you when you've gone over the recommended length.

### Save
- Updates the JSON file at `/data/pages/{slug}.json`
- Updates the actual HTML file (`title`, `meta`, `h1`, intro, alts)
- If you changed the slug:
  - Renames the HTML file
  - Adds a **301 redirect** to `/data/redirects.json`
  - Updates `.htaccess` with the redirect
  - Writes a meta-refresh stub at the old URL (belt-and-braces fallback)

### New page / new blog post
- Click **+ New page** or **+ New blog post**
- Enter slug, title, meta description, H1, intro paragraph
- A new HTML file is created from a clean template
- You're dropped straight into the editor to fill out the rest
- The new page is added to `data/pages/` or `data/blog/`

> **Note**: You'll likely want to also add internal nav links to your new pages. Edit `update_nav_sitewide.py` in the project to add new menu items, then re-run it.

### Redirects
Lists every 301 redirect. You can also add one manually (old path → new path) or remove an existing one. The `.htaccess` file is automatically rewritten on every change.

### Settings
- Change the admin password
- View site info

---

## 5 · File structure

```
data/                          ← JSON content store (deny enforced)
├── config.json                ← admin credentials (bcrypt-hashed)
├── redirects.json             ← every 301 redirect (auto-managed)
├── pages/
│   ├── index.json             ← homepage content
│   ├── removals-eastbourne.json
│   └── ... (one .json per page)
└── blog/
    └── ... (one .json per blog post)

admin-portal-xK7p9q/           ← hidden admin (rename for production)
├── login.php                  ← login page
├── logout.php
├── index.php                  ← dashboard
├── edit.php                   ← page editor
├── new.php                    ← new page/blog wizard
├── redirects.php              ← redirect manager
├── settings.php               ← password change
├── _lib.php                   ← shared library (DENY enforced)
├── _auth.php                  ← auth helpers (DENY enforced)
├── _layout.php                ← admin HTML wrapper (DENY enforced)
└── style.css                  ← admin styling
```

---

## 6 · Security notes

The system uses several layers:

| Layer | Mechanism |
|---|---|
| Hidden URL | The admin folder name is random and not linked from anywhere public. Rename it after setup. |
| Bcrypt passwords | Cost 12. Cannot be reversed; PHP's `password_verify()` checks them. |
| CSRF tokens | Every form has a token; replay attacks fail. |
| Session cookie | Auth uses PHP's session. Logout destroys it. |
| `.htaccess` denies | `/data/` and `_*.php` helper files cannot be loaded directly from the browser. |
| Brute-force delay | Failed logins wait 0.3–0.8s before responding. |

**Recommended additions** (do these manually for production):
- Enable HTTPS in `.htaccess` (uncomment the force-HTTPS block)
- Add HTTP Basic Auth on the admin folder via cPanel's "Password Protect Directories" — gives a second password layer
- Restrict admin access to your IP if you have a fixed one
- Enable Cloudflare proxy with bot challenges if you get hit by scanners

---

## 7 · Troubleshooting

### "Page not found in JSON store"
The HTML file exists but no JSON record. Two options:
- Click **+ New page**, use the same slug, and re-enter the content
- Or run the extraction script locally: `python3 admin_build/extract_to_json.py` — generates JSON from existing HTML

### "Cannot write" / "Permission denied" on save
Permissions issue. Make sure `/data/` and its subdirectories are writable by the web server user (chmod 755 / 644 with proper ownership).

### Slug change didn't redirect
Check that:
- `.htaccess` is uploaded (some hosts strip dotfiles — set FTP to show hidden files)
- The `# === ADMIN REDIRECTS START ===` marker exists in `.htaccess`
- mod_rewrite is enabled (it almost always is on shared hosting)

### Lost admin password
SSH/SFTP into the server and edit `/data/config.json`:
1. Replace the `password_hash` value with an empty string
2. Visit `login.php` — it will reject any password
3. Use a PHP one-liner to generate a new hash:
   ```bash
   php -r "echo password_hash('your-new-password', PASSWORD_BCRYPT);"
   ```
4. Paste the output into `config.json` `password_hash`

---

## 8 · Backups

The data is just JSON files — back them up easily:

```bash
# Local backup (run via cron or manually)
tar -czf mr-backup-$(date +%Y%m%d).tar.gz data/
```

Restoring: untar over the existing `data/` folder and run the admin rebuild (or just keep the HTML files unchanged — they're independent).

---

## 9 · Adding the admin URL to your password manager

After your first login, add this to your password manager (1Password, Bitwarden, LastPass, etc.):

```
Item name : Mark Ratcliffe Moving Admin
URL       : https://www.markratcliffemoving.co.uk/YOUR-RENAMED-FOLDER/login.php
Username  : mark
Password  : (your new password)
```

That's it. Welcome to your admin system.
