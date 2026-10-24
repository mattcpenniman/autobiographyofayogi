# Autobiography of a Yogi Interactive Site

This project is a lightweight, static website for presenting an interactive experience around *Autobiography of a Yogi*.

## What matters most

- The public entrypoint is [index.html](/mnt/www/map/polloanalytics.com/public_html/autobioyogi/index.html).
- The current site is intentionally self-contained.
- Most content updates happen in one place: the `BOOK_DATA` object near the bottom of `index.html`.

## Current structure

- [index.html](/mnt/www/map/polloanalytics.com/public_html/autobioyogi/index.html): homepage, styling, data, and rendering logic.
- [reader.html](/mnt/www/map/polloanalytics.com/public_html/autobioyogi/reader.html): full-text reader with chapter navigation and search.
- [AGENTS.md](/mnt/www/map/polloanalytics.com/public_html/autobioyogi/AGENTS.md): maintainer notes for humans and coding agents.
- [index.legacy.html](/mnt/www/map/polloanalytics.com/public_html/autobioyogi/index.legacy.html): old broken/generated homepage kept for reference.
- [reader.legacy.html](/mnt/www/map/polloanalytics.com/public_html/autobioyogi/reader.legacy.html): old generated reader kept for reference.
- [index.html.template](/mnt/www/map/polloanalytics.com/public_html/autobioyogi/index.html.template), [index.html.snapshot](/mnt/www/map/polloanalytics.com/public_html/autobioyogi/index.html.snapshot), [build.py](/mnt/www/map/polloanalytics.com/public_html/autobioyogi/build.py): legacy generation artifacts, not required by the current homepage.

## How to update content

Open `index.html` and edit `BOOK_DATA`.

Useful sections:

- `heroSummary`: homepage intro text
- `stats`: the small number cards in the hero
- `readingPaths`: the guided path buttons and spotlight content
- `themes`: the theme cards
- `chapters`: the searchable chapter explorer
- `quotes`: the quote cards
- `timeline`: the spiritual journey timeline
- `practices`: the final usage cards

## Safe editing workflow

1. Update one array or object in `BOOK_DATA`.
2. Reload the page in a browser.
3. Check mobile width and desktop width.
4. Verify that buttons still open, filters still work, and no section looks empty by accident.

## Adding new material

To add a new chapter card, append another object to `BOOK_DATA.chapters` with:

- `number`
- `title`
- `arc`
- `summary`
- `motifs`
- `detail`

To add a new theme drill-down card, append another object to `BOOK_DATA.themes` with:

- `title`
- `summary`
- `chapters`
- `prompts`

## Notes

- The site does not depend on npm, a framework, or a build step.
- Keeping the experience in one file makes quick edits easier and lowers the chance of another broken generation step.

## Deployment (VEC-1029)

Keep the source checkout and all agent configuration outside the web root. Build
an allowlisted artifact from the reviewed source revision:

```sh
python3 package_site.py /tmp/autobioyogi-site.tar.gz
tar -tzf /tmp/autobioyogi-site.tar.gz
```

The archive contains exactly `index.html`, `reader.html`, and `.htaccess`. Both
pages embed their data; `text/` and the legacy generator are not runtime assets.
Deploy only these archive members into the site's `autobioyogi/` directory.
Do not copy the checkout recursively or use `git pull` in a document root.
`.gitignore` alone is not a deployment exclusion. The package allowlist excludes
agent settings, Git metadata, environment files, source instructions, legacy
snapshots, and build/operations scripts even if new ones are added to the source.
Add future public assets explicitly to `PUBLIC_FILES` after review.

The host-level policy is versioned in
`ops/polloanalytics-development-paths.conf`. Install it with:

```sh
sudo install -o root -g root -m 0644 ops/polloanalytics-development-paths.conf /etc/apache2/conf-available/polloanalytics-development-paths.conf
sudo a2enconf polloanalytics-development-paths
sudo apache2ctl configtest
sudo systemctl reload apache2
```

It denies hidden directories/files and agent instruction/configuration files in
both the main and fileshare document roots. `.well-known/` remains allowed,
including certificate-validation files; hidden descendants are still denied.
The shipped `.htaccess` also blocks sensitive paths on Apache hosts with
`mod_rewrite` and `AllowOverride` enabled. Verify the homepage and reader return
200, agent settings and Git metadata return 403/404, and a temporary plain-text
ACME challenge file returns 200 over HTTP (following HTTPS redirects) and HTTPS.
Remove the challenge fixture afterward.
