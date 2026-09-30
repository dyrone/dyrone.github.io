---
name: reading-notes-blog-style
description: Use when publishing or restyling long-form Chinese reading notes in this Hugo blog, especially when chapter hierarchy, per-chapter explanatory SVGs, and preview-before-commit are required.
---

# Reading Notes Blog Style

Apply the repository's editorial chapter separators and Chinese book-annotation figures without changing the author's argument.

## Workflow

1. Inspect the source article, Hugo configuration, templates, shortcodes, CSS, asset layout, and nearby post patterns before editing.
2. Preserve every argument, example, and chapter order. Change structure and presentation only unless the user requests editorial rewriting.
3. Remove local or temporary references, including `.qoder/tmp`, `/Users/`, and remote image URLs. Keep publishable assets under `static/`.
4. Set Front Matter to `article_style: reading-notes` and `draft: false`.
5. Treat each H2 as one chapter and each H3 as a subsection. Write sequential numbering explicitly in Markdown: `## 1. ...`, `## 2. ...`, and `### 2.1 ...`, `### 2.2 ...`.
6. Insert `---` between adjacent H2 chapters so the separation survives theme or CSS changes.
7. Create exactly one original, self-contained Chinese book-annotation SVG for every H2. Follow the [reusable style guide](references/style-guide.md), and make each composition explain its own chapter.
8. Place one `reading-note-figure` shortcode immediately after each H2, before prose or H3 content. Supply non-empty, accurate `src`, `alt`, and `caption` values using straight ASCII quotes.
9. Convert work reminders into annotation-style blockquotes without changing their wording.
10. Run the [validation script](scripts/validate_reading_note.py), then run `hugo`.
11. Confirm the generated page links `/css/custom.css` from the site root, then start `hugo server --bind 127.0.0.1 --port 1313 --disableFastRender` and share the article preview URL.
12. Never commit or push before the user approves the preview.

## Validation

Run from the repository root:

```bash
python3 .qoder/skills/reading-notes-blog-style/scripts/validate_reading_note.py content/posts/<article>.md
hugo
hugo server --bind 127.0.0.1 --port 1313 --disableFastRender
```

Stop on validator or Hugo errors. Keep the working tree uncommitted while the user reviews the local preview.
