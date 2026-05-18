# markratcliffemoving.co.uk

Mark Ratcliffe Moving & Storage — Eastbourne removals company website.

## Structure

```
www.markratcliffemoving.co.uk/   ← deploy this folder to your web root
├── *.html                       ← public pages
├── css/                         ← stylesheets
├── js/                          ← scripts
├── images/                      ← all imagery (single source of truth)
├── blog/                        ← blog hub + posts
├── areas-covered/               ← location subpages
├── admin-portal-xK7p9q/         ← hidden PHP admin (see ADMIN-README.md)
├── data/                        ← JSON content store + redirects
└── .htaccess                    ← Apache redirects + security headers
```

## Local development

A PHP server is enough to test everything (admin + page editing):

```bash
cd www.markratcliffemoving.co.uk
php -S localhost:8000
```

Then visit `http://localhost:8000/`.

## Admin

See [ADMIN-README.md](ADMIN-README.md) for full setup, login URL, and security notes.

## Build scripts

The Python files in the project root rebuild specific sections of the site
(area pages, footer, sitemap, etc.). They are utilities — not required at
runtime. The site itself serves as static HTML once deployed.
