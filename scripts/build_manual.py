"""Build dist/Hecate-G2000-PRO-Volume-<version>-Manual.pdf: one PDF with the manual in every language.

Structure: a first page with the languages, each a link to that language's contents; then, per
language, its contents (links with page numbers) and the manual. PDF bookmarks mirror the contents.
Same layout, Markdown subset and image placeholders as the manual of opendeck-uno-overlays.

Sources (one per language, docs/manual/<code>/manual.md) use a small Markdown subset:
"# ", "## ", "### " headings (optionally with {#id}), paragraphs, "- " and "1. " lists, **bold**,
`code`, [text](https://...) and [text](#id) links, ![alt](name.jpg) images and ``` code blocks.
Images: docs/manual/imagens/<code>/<name> first, then docs/manual/imagens/<name>; when neither exists a
visible placeholder box with "<name>" takes its place, and the build lists every missing image. Put the
file there and build again to replace it.

Security (WeasyPrint 57.2 in Debian 12 has CVE-2025-68616, CVE-2026-49452 and CVE-2026-55073 open):
the HTML is built only from files of this repository; the fetcher allows only files under docs/manual
(no network, no redirects); the CSS is inline, not passed through write_pdf(stylesheets=...), and no
xmp_metadata or presentational hints are used, so none of the three code paths is reached.

    python3 -B scripts/build_manual.py   # needs WeasyPrint (Debian: apt install weasyprint) and Noto CJK fonts
"""

import html
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MANUAL = ROOT / "docs" / "manual"
IMAGES = MANUAL / "imagens"
sys.path.insert(0, str(ROOT / "src"))
from hecate_volume import __version__  # noqa: E402 - the version of the code itself

PRODUCT = "Hecate G2000 PRO Volume"
LANGUAGES = ["pt-BR", "en", "es", "it", "de", "ja", "zh-CN", "ko", "fr"]
NATIVE = {"pt-BR": "Português (Brasil)", "en": "English", "es": "Español", "it": "Italiano", "de": "Deutsch",
          "ja": "日本語", "zh-CN": "简体中文", "ko": "한국어", "fr": "Français"}  # fmt: skip


def inline(text, code):
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\[([^\]]+)\]\((https://[\w./%#?=&-]+)\)", r'<a href="\2">\1</a>', text)
    return re.sub(r"\[([^\]]+)\]\(#([\w.-]+)\)", lambda m: f'<a href="#{code}-{m[2]}">{m[1]}</a>', text)


def slug(text):
    return re.sub(r"[^\w]+", "-", text.lower(), flags=re.UNICODE).strip("-")[:60] or "s"


class Page:
    def __init__(self, code):
        self.code, self.missing, self.toc, self.ids = code, [], [], set()

    def anchor(self, text, wanted=None):
        base = f"{self.code}-{wanted or slug(text)}"
        anchor, n = base, 1
        while anchor in self.ids:
            n += 1
            anchor = f"{base}-{n}"
        self.ids.add(anchor)
        return anchor

    def heading(self, level, text, wanted=None):
        anchor = self.anchor(text, wanted)
        body = inline(text, self.code)
        self.toc.append((level, body, anchor))
        return f'<h{level} id="{anchor}">{body}</h{level}>'

    def image(self, alt, name):
        if not re.fullmatch(r"[\w.-]+\.(jpg|jpeg|png)", name):
            raise SystemExit(f"manual: unsupported image name {name!r} ({self.code})")
        caption = f"<figcaption>{html.escape(alt)}</figcaption></figure>"
        for path in (IMAGES / self.code / name, IMAGES / name):
            if path.is_file():
                return f'<figure><img src="{path.as_uri()}" alt="{html.escape(alt)}">{caption}'
        self.missing.append(name)
        box = f'<div class="placeholder" role="img" aria-label="{html.escape(alt)}">&lt;{html.escape(name)}&gt;</div>'
        return f"<figure>{box}{caption}"

    def render(self, source):
        out, items, kind, start, paragraph, code_block = [], [], None, 1, [], None

        def close():
            nonlocal items, kind
            if items:
                tag = "ol" if kind == "1" else "ul"
                # "2." after a code block; CSS, not start="", since presentational hints stay off (docstring)
                first = f' style="counter-reset: list-item {start - 1}"' if kind == "1" and start != 1 else ""
                out.append(f"<{tag}{first}>" + "".join(f"<li>{i}</li>" for i in items) + f"</{tag}>")
            items, kind = [], None

        def flush():
            if paragraph:
                out.append("<p>" + inline(" ".join(paragraph), self.code) + "</p>")
                paragraph.clear()

        for line in source.splitlines():
            stripped = line.strip()
            if code_block is not None:
                if stripped == "```":
                    out.append("<pre><code>" + html.escape("\n".join(code_block)) + "</code></pre>")
                    code_block = None
                else:
                    code_block.append(line)
                continue
            heading = re.match(r"(#{1,3}) (.+?)(?: \{#([\w-]+)\})?$", stripped)
            bullet = re.match(r"(-|\d+\.) (.+)$", stripped)
            image = re.fullmatch(r"!\[([^\]]*)\]\(([^)]+)\)", stripped)
            fence = stripped.startswith("```")
            if not stripped or heading or image or fence:
                flush()
                close()
            if not stripped:
                continue
            if fence:
                code_block = []
            elif heading:
                out.append(self.heading(len(heading[1]) + 1, heading[2], heading[3]))  # "#" in a source is h2
            elif image:
                out.append(self.image(image[1], image[2]))
            elif bullet:
                flush()
                new = "1" if bullet[1] != "-" else "-"
                if kind not in (None, new):
                    close()
                if kind is None and new == "1":
                    start = int(bullet[1].rstrip("."))
                kind = new
                items.append(inline(bullet[2], self.code))
            elif items:
                items[-1] += " " + inline(stripped, self.code)
            else:
                paragraph.append(stripped)
        if code_block is not None:
            raise SystemExit(f"manual: unclosed code block ({self.code})")
        flush()
        close()
        return "\n".join(out)


def document(version):
    """(HTML, {language: [missing images]})."""
    sections, missing, index = [], {}, []
    for code in LANGUAGES:
        source = (MANUAL / code / "manual.md").read_text(encoding="utf-8")
        title, contents, *body = source.splitlines()  # "% Title of the manual", "% Contents", the manual
        title, contents = title.removeprefix("% ").strip(), contents.removeprefix("% ").strip()
        page = Page(code)
        rendered = page.render("\n".join(body))
        toc = "".join(
            f'<li class="level{level}"><a href="#{anchor}">{text}</a></li>' for level, text, anchor in page.toc
        )
        sections.append(
            f'<section class="language" lang="{code}">'
            f'<h1 id="{code}">{html.escape(title)}</h1>'
            f'<nav class="toc" id="{code}-toc"><h2 class="toc-title">{html.escape(contents)}</h2><ul>{toc}</ul></nav>'
            f"{rendered}</section>"
        )
        index.append(f'<li><a href="#{code}-toc">{NATIVE[code]}</a></li>')
        missing[code] = page.missing
    cover = (
        f'<section class="cover"><p class="product">{PRODUCT} {html.escape(version)}</p>'
        f'<p class="kind">Manual</p><ul class="languages">{"".join(index)}</ul></section>'
    )
    css = (MANUAL / "manual.css").read_text(encoding="utf-8")
    page_html = (
        f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{PRODUCT} {html.escape(version)}'
        f"</title><style>{css}</style></head><body>{cover}{''.join(sections)}</body></html>"
    )
    return page_html, missing


def fetcher(url):
    """Only image files under docs/manual: no network, no other file (see the module docstring)."""
    from weasyprint import default_url_fetcher

    allowed = MANUAL.resolve().as_uri() + "/"
    if not url.startswith(allowed) or ".." in url:
        raise ValueError(f"manual: refused to load {url}")
    return default_url_fetcher(url)


def render(version):
    from weasyprint import HTML

    page_html, missing = document(version)
    return HTML(string=page_html, base_url=str(MANUAL), url_fetcher=fetcher).render(), missing


def check_fonts():
    """Japanese, Chinese and Korean need Noto CJK: without it they would print as empty boxes."""
    try:
        found = subprocess.run(["fc-list", ":lang=ja", "family"], capture_output=True, text=True, check=False).stdout  # noqa: S603, S607
    except OSError:
        sys.exit("manual: fontconfig (fc-list) is missing. Debian: sudo apt install fontconfig")
    if not found.strip():
        sys.exit("manual: no CJK font. Debian: sudo apt install fonts-noto-cjk")


def output_path(version=__version__):
    return ROOT / "dist" / f"{PRODUCT.replace(' ', '-')}-{version}-Manual.pdf"


def main():
    check_fonts()
    try:
        doc, missing = render(__version__)
    except ImportError:
        sys.exit("manual: WeasyPrint is missing. Debian: sudo apt install weasyprint fonts-noto-cjk fonts-dejavu-core")
    out = output_path()
    out.parent.mkdir(exist_ok=True)
    doc.write_pdf(out)
    for code, names in missing.items():
        if names:
            print(f"manual: {code}: placeholder for {', '.join(sorted(set(names)))}")
    print(f"{out.relative_to(ROOT)}  {len(doc.pages)} pages")


if __name__ == "__main__":
    main()
