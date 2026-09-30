# Reading Notes Editorial Style Guide

Reuse this system for long-form Chinese reading notes. Keep all article rules scoped to `.article-style-reading-notes`; never add unscoped `h2`, `h3`, `figure`, `blockquote`, or table rules that alter other posts.

## Editorial hierarchy

- Write chapter numbering explicitly in Markdown: H2 uses `1.`, `2.`, and so on; H3 uses parent-child numbers such as `3.1`, `3.2`. Keep both sequences continuous.
- Insert an explicit Markdown `---` between adjacent H2 chapters. Do not rely on CSS alone for structural separation.
- Render every H2 as a chapter opening with generous whitespace and a 3px charcoal top rule.
- Render every H3 as a subsection: indent it from the chapter edge, add a yellow left bar, and use a pale cream-to-transparent gradient. Keep its size and spacing visibly subordinate to H2.
- Keep figures aligned with the H2/body text inset. Place captions inside the figure frame, left-aligned, visually labeled as captions, and separated from the following prose.
- Preserve comfortable space between the chapter figure, prose, lists, tables, and the next heading. Do not use decorative separators between ordinary paragraphs.
- Convert actionable reminders to Markdown blockquotes such as `> **工作提醒**：...` or `> **AI 与工作提醒**：...`. Present these as red annotation blocks within the scoped article rather than as generic quotations.

## Palette and materials

Use a restrained book-page palette. Adjust shades only to maintain accessible contrast.

| Role | Suggested color | Use |
| --- | --- | --- |
| Cream paper | `#F7F0DE` | Figure ground, framed paper, pale washes |
| Charcoal | `#2F2B26` | Type, outlines, H2 rule |
| Highlighter yellow | `#F2C94C` | H3 bar, highlights, key paths |
| Annotation red | `#B5483F` | Handwritten notes, arrows, reminder accents |
| Muted ink | `#746B60` | Secondary labels and supporting lines |

Keep text contrast strong. Use yellow as a highlight behind or beside dark text, not as low-contrast body text.

## Chapter SVGs

- Create exactly one explanatory SVG per H2. Explain the chapter's central mechanism; do not reuse one composition with only its title changed.
- Build a self-contained cream paper scene with charcoal lines, yellow highlighter marks, and red handwritten annotations or arrows.
- Write all reader-visible labels and annotations in Chinese. Do not load external fonts, scripts, stylesheets, images, or URLs.
- Give every root SVG a responsive `viewBox` and omit fixed presentation dimensions when they would prevent scaling. Use a consistent wide editorial canvas, such as `viewBox="0 0 1200 630"`, unless the content needs another ratio.
- Add a unique Chinese `<title>` and Chinese `<desc>` describing the visual's meaning. Connect them with `aria-labelledby` when authoring explicit SVG accessibility attributes.
- Keep important text and marks inside safe margins. Ensure labels remain legible when the figure is displayed at mobile width.
- Prefer simple vectors, limited detail, and strong grouping. Preserve the paper-and-ink character without simulating illegible handwriting.

## Files and references

- Store figures at `static/images/<article-slug>/`.
- Name files `<NN>-<topic>.svg` with a zero-padded chapter number and short lowercase kebab-case topic, for example `03-two-systems.svg`.
- Reference each asset as `/images/<article-slug>/<NN>-<topic>.svg`, and use each normalized SVG path only once per article.
- Place the `reading-note-figure` shortcode immediately after its H2. Provide an `alt` that states the visual relationship and a concise `caption` that states the takeaway. Do not duplicate the filename or use generic text such as “章节配图”.
- Keep `.qoder/tmp`, `/Users/`, `/tmp/`, fetchable HTTP(S) references, and protocol-relative URLs out of Markdown and SVG source, regardless of case. The exact `xmlns="http://www.w3.org/2000/svg"` and `xmlns:xml="http://www.w3.org/XML/1998/namespace"` declarations are allowed.

## Responsive behavior

- Let figures scale to the article width while preserving their `viewBox` ratio.
- Reduce H2/H3 font sizes, chapter whitespace, figure padding, and annotation offsets at narrow breakpoints; retain the 3px H2 rule and clear H2/H3 distinction.
- Allow wide tables to scroll horizontally inside the scoped article instead of shrinking text beyond readability.
- Check that Chinese labels do not clip, overlap, or become too small on a phone-width preview.

## Review checklist

- Confirm every H2 has one distinct local SVG and every H3 remains subordinate.
- Confirm H2 and H3 numbering is explicit and sequential in Markdown, with `---` between chapters.
- Confirm SVG title, description, visible Chinese text, alt text, and caption all match the chapter.
- Confirm figure captions stay inside the frame and do not visually merge with prose.
- Confirm the generated nested article page links `/css/custom.css`, not a page-relative `css/custom.css`.
- Confirm reminders read as red annotation blocks and retain their original message.
- Run the validator and Hugo, then inspect desktop and mobile previews before requesting approval.
