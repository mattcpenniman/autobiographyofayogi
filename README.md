# Autobiography of a Yogi Interactive Site

This project is a lightweight, static website for presenting an interactive experience around *Autobiography of a Yogi*.

## What matters most

- The public entrypoint is [index.html](/mnt/www/map/polloanalytics.com/public_html/autobioyogi/index.html).
- The current site is intentionally self-contained.
- Most content updates happen in one place: the `BOOK_DATA` object near the bottom of `index.html`.

## Current structure

- [index.html](/mnt/www/map/polloanalytics.com/public_html/autobioyogi/index.html): homepage, styling, data, and rendering logic.
- [reader.html](/mnt/www/map/polloanalytics.com/public_html/autobioyogi/reader.html): simple redirect to the chapter explorer.
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
