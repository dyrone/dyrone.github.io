#!/usr/bin/env python3
"""Validate a Hugo reading-note article and its local chapter SVGs."""

from __future__ import annotations

import posixpath
import re
import sys
from pathlib import Path
from typing import Iterable

ALLOWED_SVG_NAMESPACE_PATTERNS = (
    re.compile(r'(?<!\S)xmlns="http://www.w3.org/2000/svg"(?=\s|/?>)'),
    re.compile(
        r'(?<!\S)xmlns:xml="http://www.w3.org/XML/1998/namespace"(?=\s|/?>)'
    ),
)
REFERENCE_CHARACTER = r"[^\s<>\"'`)\]}]"
FORBIDDEN_REFERENCE_PATTERNS = (
    re.compile(rf"https?://{REFERENCE_CHARACTER}+", re.IGNORECASE),
    re.compile(
        rf"(?<![A-Za-z0-9_:/.-])//{REFERENCE_CHARACTER}+", re.IGNORECASE
    ),
    re.compile(rf"\.qoder/tmp{REFERENCE_CHARACTER}*", re.IGNORECASE),
    re.compile(rf"/users/{REFERENCE_CHARACTER}*", re.IGNORECASE),
    re.compile(
        rf"(?<![A-Za-z0-9_.-])/tmp/{REFERENCE_CHARACTER}*", re.IGNORECASE
    ),
)
H2_PATTERN = re.compile(r"(?m)^[ ]{0,3}##(?!#)[ \t]+([^\r\n]+)")
H3_PATTERN = re.compile(r"(?m)^[ ]{0,3}###(?!#)[ \t]+([^\r\n]+)")
H2_NUMBER_PATTERN = re.compile(r"^(?P<chapter>\d+)\.\s+\S")
H3_NUMBER_PATTERN = re.compile(r"^(?P<chapter>\d+)\.(?P<section>\d+)\s+\S")
SHORTCODE_PATTERN = re.compile(
    r"\{\{<\s*reading-note-figure\b(?P<arguments>.*?)>\}\}", re.DOTALL
)
PARAMETER_PATTERN = re.compile(
    r"(?P<name>[A-Za-z_][\w-]*)\s*=\s*(?:\"(?P<double>[^\"]*)\"|'(?P<single>[^']*)')",
    re.DOTALL,
)
XML_COMMENT_PATTERN = re.compile(r"<!--.*?(?:-->|$)", re.DOTALL)
XML_ATTRIBUTE_TEXT = r'(?:[^>\"\']|\"[^\"]*\"|\'[^\']*\')*'
ROOT_SVG_PATTERN = re.compile(
    rf"^\ufeff?\s*"
    rf"(?:<\?xml\b.*?\?>\s*)?"
    rf"(?:<!DOCTYPE\b{XML_ATTRIBUTE_TEXT}>\s*)?"
    rf"<svg\b(?P<attributes>{XML_ATTRIBUTE_TEXT})>",
    re.IGNORECASE | re.DOTALL,
)
REQUIRED_PARAMETERS = ("src", "alt", "caption")


def error(message: str) -> str:
    return f"ERROR: {message}"


def strip_yaml_comment(value: str) -> str:
    quote = ""
    escaped = False
    for index, character in enumerate(value):
        if escaped:
            escaped = False
            continue
        if character == "\\" and quote == '"':
            escaped = True
            continue
        if character in ("'", '"'):
            if not quote:
                quote = character
            elif quote == character:
                quote = ""
            continue
        if character == "#" and not quote and (index == 0 or value[index - 1].isspace()):
            return value[:index].rstrip()
    return value.strip()


def yaml_scalar(value: str) -> str:
    value = strip_yaml_comment(value.strip())
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    return value


def split_front_matter(text: str) -> tuple[dict[str, str], str, list[str]]:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].lstrip("\ufeff").strip() != "---":
        return {}, text, [error("missing YAML front matter")]

    closing_index = next(
        (index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---"),
        None,
    )
    if closing_index is None:
        return {}, text, [error("YAML front matter is not closed")]

    values: dict[str, str] = {}
    key_pattern = re.compile(r"^([A-Za-z_][\w-]*)\s*:\s*(.*?)\s*$")
    for line in lines[1:closing_index]:
        match = key_pattern.match(line.rstrip("\r\n"))
        if match:
            values[match.group(1)] = yaml_scalar(match.group(2))

    body = "".join(lines[closing_index + 1 :])
    return values, body, []


def blank_line_content(line: str) -> str:
    return re.sub(r"[^\r\n]", " ", line)


def mask_fenced_code(text: str) -> str:
    """Blank fenced code while preserving offsets and line endings."""
    masked: list[str] = []
    fence_character = ""
    fence_length = 0

    for line in text.splitlines(keepends=True):
        opening = re.match(r"^[ ]{0,3}(`{3,}|~{3,})", line)
        if not fence_character and opening:
            marker = opening.group(1)
            fence_character = marker[0]
            fence_length = len(marker)
            masked.append(blank_line_content(line))
            continue

        if fence_character:
            closing = re.match(
                rf"^[ ]{{0,3}}{re.escape(fence_character)}{{{fence_length},}}[ \t]*(?:\r?\n)?$",
                line,
            )
            masked.append(blank_line_content(line))
            if closing:
                fence_character = ""
                fence_length = 0
            continue

        masked.append(line)

    return "".join(masked)


def repository_root(markdown_path: Path) -> Path:
    script_path = Path(__file__).resolve()
    candidates = [script_path.parent, *script_path.parents, markdown_path.parent, *markdown_path.parents]
    for candidate in candidates:
        if (candidate / ".git").exists():
            return candidate
    raise OSError("repository root not found")


def parameter_values(arguments: str) -> dict[str, list[str]]:
    values: dict[str, list[str]] = {}
    for match in PARAMETER_PATTERN.finditer(arguments):
        value = match.group("double")
        if value is None:
            value = match.group("single")
        values.setdefault(match.group("name"), []).append(value)
    return values


def is_within(path: Path, directory: Path) -> bool:
    try:
        path.relative_to(directory)
    except ValueError:
        return False
    return True


def forbidden_errors(
    text: str, label: str, *, allow_svg_namespaces: bool = False
) -> list[str]:
    searchable = text
    if allow_svg_namespaces:
        for pattern in ALLOWED_SVG_NAMESPACE_PATTERNS:
            searchable = pattern.sub(
                lambda match: " " * len(match.group(0)), searchable
            )

    errors: list[str] = []
    for pattern in FORBIDDEN_REFERENCE_PATTERNS:
        match = pattern.search(searchable)
        if match:
            errors.append(error(f"{label} contains forbidden reference {match.group(0)}"))
    return errors


def has_non_empty_element(svg: str, tag: str) -> bool:
    element_pattern = re.compile(
        rf"<{tag}\b{XML_ATTRIBUTE_TEXT}>(?P<content>.*?)</{tag}\s*>",
        re.IGNORECASE | re.DOTALL,
    )
    for match in element_pattern.finditer(svg):
        text_content = re.sub(r"<[^>]*>", "", match.group("content"))
        if text_content.strip():
            return True
    return False


def validate_svg(svg_path: Path, display_src: str) -> list[str]:
    errors: list[str] = []
    try:
        svg = svg_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError, ValueError) as exc:
        return [error(f"cannot read SVG {display_src}: {exc}")]

    svg_without_comments = XML_COMMENT_PATTERN.sub("", svg)
    root = ROOT_SVG_PATTERN.match(svg_without_comments)
    if root is None:
        errors.append(error(f"SVG {display_src} is missing root <svg> opening tag"))
    elif not re.search(
        r"(?:^|\s)viewBox\s*=", root.group("attributes"), re.IGNORECASE
    ):
        errors.append(error(f"SVG {display_src} root <svg> is missing viewBox"))

    for tag in ("title", "desc"):
        if not has_non_empty_element(svg_without_comments, tag):
            errors.append(error(f"SVG {display_src} requires non-empty <{tag}>"))

    errors.extend(
        forbidden_errors(
            svg_without_comments,
            f"SVG {display_src}",
            allow_svg_namespaces=True,
        )
    )
    return errors


def validate_figures(
    shortcodes: Iterable[re.Match[str]], static_root: Path
) -> list[str]:
    errors: list[str] = []
    try:
        resolved_static = static_root.resolve()
    except (OSError, RuntimeError, ValueError):
        return [error("cannot resolve repository static directory")]

    seen_sources: dict[str, int] = {}
    for index, shortcode in enumerate(shortcodes, start=1):
        parameters = parameter_values(shortcode.group("arguments"))
        for name in REQUIRED_PARAMETERS:
            values = parameters.get(name, [])
            if len(values) != 1 or not values[0].strip():
                errors.append(error(f"figure {index} requires one non-empty {name}"))

        src_values = parameters.get("src", [])
        if len(src_values) != 1 or not src_values[0].strip():
            continue

        src = src_values[0].strip()
        normalized_src = posixpath.normpath(src)
        first_index = seen_sources.get(normalized_src)
        if first_index is not None:
            errors.append(
                error(
                    f"figure {index} has duplicate normalized SVG src "
                    f"{normalized_src} (first used by figure {first_index})"
                )
            )
        else:
            seen_sources[normalized_src] = index

        if not src.startswith("/images/"):
            errors.append(error(f"figure {index} src must begin with /images/: {src}"))
            continue
        if not src.lower().endswith(".svg"):
            errors.append(error(f"figure {index} must reference an SVG: {src}"))
            continue

        try:
            svg_path = (resolved_static / src.lstrip("/")).resolve()
        except (OSError, RuntimeError, ValueError):
            errors.append(error(f"cannot resolve SVG for figure {index}: {src}"))
            continue
        if not is_within(svg_path, resolved_static):
            errors.append(error(f"figure {index} src escapes repository static/: {src}"))
            continue
        try:
            svg_exists = svg_path.is_file()
        except (OSError, ValueError):
            errors.append(error(f"cannot inspect SVG for figure {index}: {src}"))
            continue
        if not svg_exists:
            errors.append(error(f"SVG not found for figure {index}: {src}"))
            continue

        errors.extend(validate_svg(svg_path, src))

    return errors


def validate(markdown_path: Path, markdown: str) -> tuple[list[str], int, int]:
    errors: list[str] = []
    errors.extend(forbidden_errors(markdown, "Markdown"))

    front_matter, body, front_matter_errors = split_front_matter(markdown)
    errors.extend(front_matter_errors)
    if front_matter.get("article_style") != "reading-notes":
        errors.append(error("front matter article_style must be reading-notes"))
    if front_matter.get("draft", "").lower() != "false":
        errors.append(error("front matter draft must be false"))

    masked_body = mask_fenced_code(body)
    headings = list(H2_PATTERN.finditer(masked_body))
    subsection_headings = list(H3_PATTERN.finditer(masked_body))
    shortcodes = list(SHORTCODE_PATTERN.finditer(masked_body))

    if not headings:
        errors.append(error("article must contain at least one H2 chapter"))

    immediate_shortcode_starts: set[int] = set()
    for chapter_number, heading in enumerate(headings, start=1):
        title = re.sub(r"[ \t]+#+[ \t]*$", "", heading.group(1)).strip()
        number_match = H2_NUMBER_PATTERN.match(title)
        if number_match is None or int(number_match.group("chapter")) != chapter_number:
            errors.append(
                error(f"H2 chapter {chapter_number} must start with '{chapter_number}. ': {title}")
            )

        if chapter_number > 1:
            separator_region = masked_body[headings[chapter_number - 2].end() : heading.start()]
            if re.search(r"(?m)^---[ \t]*\r?\n[ \t\r\n]*$", separator_region) is None:
                errors.append(error(f"chapter {chapter_number} must be preceded by a Markdown --- separator"))

        chapter_end = headings[chapter_number].start() if chapter_number < len(headings) else len(masked_body)
        chapter_subsections = [
            subsection
            for subsection in subsection_headings
            if heading.end() < subsection.start() < chapter_end
        ]
        for section_number, subsection in enumerate(chapter_subsections, start=1):
            subsection_title = re.sub(
                r"[ \t]+#+[ \t]*$", "", subsection.group(1)
            ).strip()
            subsection_match = H3_NUMBER_PATTERN.match(subsection_title)
            if (
                subsection_match is None
                or int(subsection_match.group("chapter")) != chapter_number
                or int(subsection_match.group("section")) != section_number
            ):
                errors.append(
                    error(
                        f"H3 subsection must start with '{chapter_number}.{section_number} ': {subsection_title}"
                    )
                )

        whitespace = re.match(r"[ \t\r\n]*", masked_body[heading.end() :])
        shortcode_start = heading.end() + (whitespace.end() if whitespace else 0)
        shortcode = SHORTCODE_PATTERN.match(masked_body, shortcode_start)
        if shortcode is None:
            errors.append(
                error(
                    f"chapter {chapter_number} must be immediately followed by one reading-note-figure shortcode"
                )
            )
        else:
            immediate_shortcode_starts.add(shortcode.start())

    for shortcode in shortcodes:
        if shortcode.start() not in immediate_shortcode_starts:
            errors.append(error("reading-note-figure shortcode must immediately follow an H2"))

    if len(shortcodes) != len(headings):
        errors.append(
            error(
                f"figure count {len(shortcodes)} does not match chapter count {len(headings)}"
            )
        )

    try:
        static_root = repository_root(markdown_path) / "static"
    except (OSError, RuntimeError, ValueError) as exc:
        errors.append(error(f"cannot resolve repository root: {exc}"))
    else:
        errors.extend(validate_figures(shortcodes, static_root))

    return errors, len(headings), len(shortcodes)


def main(argv: list[str] | None = None) -> int:
    arguments = sys.argv if argv is None else argv
    if len(arguments) != 2:
        print(error("usage: validate_reading_note.py <markdown-path>"))
        return 1

    display_path = arguments[1]
    try:
        markdown_path = Path(display_path).expanduser()
        markdown = markdown_path.read_text(encoding="utf-8")
    except (OSError, RuntimeError, UnicodeError, ValueError) as exc:
        print(error(f"cannot read Markdown {display_path}: {exc}"))
        return 1

    try:
        resolved_markdown_path = markdown_path.resolve()
    except (OSError, RuntimeError, ValueError):
        print(error(f"cannot resolve Markdown path {display_path}"))
        return 1

    errors, chapter_count, figure_count = validate(resolved_markdown_path, markdown)
    if errors:
        for message in errors:
            print(message)
        return 1

    print(
        f"PASS: {display_path} ({chapter_count} chapters, {figure_count} local figures)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
