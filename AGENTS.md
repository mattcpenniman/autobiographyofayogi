# AGENTS.md

This repo is now designed so a human or agent can make content changes quickly without needing to understand a build pipeline.

## Source of truth

- Treat [index.html](/mnt/www/map/polloanalytics.com/public_html/autobioyogi/index.html) as the live site.
- Treat the `BOOK_DATA` object inside `index.html` as the primary content model.
- Do not assume `build.py` or the old template files are part of the active publishing flow.

## File map

- `index.html`
  Live homepage, CSS, data, and JavaScript rendering.
- `reader.html`
  Redirects old reader links to `#chapters`.
- `README.md`
  Human-friendly quickstart.
- `index.legacy.html`, `reader.legacy.html`
  Previous generated versions kept only as reference.
- `index.html.template`, `index.html.snapshot`, `build.py`
  Legacy artifacts. Leave them alone unless you are intentionally restoring a generated workflow.

## Easy update rules

When making routine content changes, stay inside `BOOK_DATA` whenever possible.

Common edits:

- New homepage summary:
  Update `BOOK_DATA.heroSummary`.
- New stat card:
  Append to `BOOK_DATA.stats`.
- New reading path:
  Append to `BOOK_DATA.readingPaths`.
- New chapter summary:
  Append or edit an object in `BOOK_DATA.chapters`.
- New quote:
  Append to `BOOK_DATA.quotes`.
- New timeline moment:
  Append to `BOOK_DATA.timeline`.
- New “place to drill down into”:
  Usually add a new object to `BOOK_DATA.themes`.

## How to add a new drill-down area

The current homepage already supports expandable content patterns. The easiest safe expansion path is:

1. Add a new theme to `BOOK_DATA.themes`.
2. Link it to relevant chapter numbers in `chapters`.
3. Add supporting chapter cards or deepen existing `detail` arrays.

If a richer new section is needed, follow this structure:

1. Add a new top-level array in `BOOK_DATA`.
2. Add a new `<section>` block in the HTML.
3. Add a small renderer function near the bottom of the script.
4. Keep naming parallel to the existing patterns like `renderThemes`, `renderQuotes`, and `renderTimeline`.

## Editing guardrails

- Prefer changing data before changing layout.
- Keep content concise enough to fit card layouts on mobile.
- If you change class names in HTML, update the related JS selectors in the same edit.
- If you add required properties to a data object, update every existing object in that array.
- Avoid reactivating the legacy generator unless the user explicitly asks for that workflow.

## Verification checklist

After edits, verify:

- The page loads with no blank sections.
- Theme spotlight buttons still work.
- Reading path buttons still switch detail content.
- Chapter search still filters.
- Chapter expand buttons still open detail panels.
- Mobile layout still stacks cleanly.

## Maintenance philosophy

This project should stay easy to patch under pressure.

- Favor static HTML/CSS/JS over new tooling.
- Favor one obvious content model over scattered hard-coded copy.
- Favor small, local UI patterns that can be extended without rewriting the page.
