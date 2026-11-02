"""The manual: the same structure and images in all 9 languages, placeholders, the loader, the PDF."""

import importlib.util
import re
import unittest

from support import ROOT

spec = importlib.util.spec_from_file_location("build_manual", ROOT / "scripts" / "build_manual.py")
build_manual = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build_manual)

HAS_WEASYPRINT = importlib.util.find_spec("weasyprint") is not None


def source(code):
    return (build_manual.MANUAL / code / "manual.md").read_text(encoding="utf-8")


def structure(text):
    """(heading level, id) of every heading with an id, the image names and the code blocks, in order."""
    headings = re.findall(r"^(#{1,3}) .+? \{#([\w-]+)\}$", text, re.M)
    images = re.findall(r"^!\[[^\]]*\]\(([^)]+)\)$", text, re.M)
    blocks = re.findall(r"^```\n(.*?)^```$", text, re.M | re.S)
    return [(len(level), anchor) for level, anchor in headings], images, blocks


class Sources(unittest.TestCase):
    def test_nine_languages_in_the_requested_order(self):
        self.assertEqual(build_manual.LANGUAGES, ["pt-BR", "en", "es", "it", "de", "ja", "zh-CN", "ko", "fr"])
        for code in build_manual.LANGUAGES:
            self.assertTrue((build_manual.MANUAL / code / "manual.md").is_file(), code)

    def test_every_language_has_the_structure_and_images_of_pt_br(self):
        headings, images, blocks = structure(source("pt-BR"))
        self.assertGreaterEqual(len(headings), 10)
        commands = [re.sub(r"<[^>]+>", "<v>", block) for block in blocks]
        for code in build_manual.LANGUAGES[1:]:
            with self.subTest(language=code):
                other_headings, other_images, other_blocks = structure(source(code))
                self.assertEqual(other_headings, headings)
                self.assertEqual(other_images, images, "same image placeholders, same order")
                self.assertEqual([re.sub(r"<[^>]+>", "<v>", block) for block in other_blocks], commands)

    def test_every_image_is_listed_in_the_images_readme(self):
        listed = (build_manual.IMAGES / "README.md").read_text(encoding="utf-8")
        for name in structure(source("pt-BR"))[1]:
            self.assertIn(f"`{name}`", listed)

    def test_commands_in_the_manual_exist(self):
        from hecate_volume import cli

        commands = set(cli.parser()._subparsers._group_actions[0].choices)
        for code in build_manual.LANGUAGES:
            for used in re.findall(r"hecate-g2000-pro-volume (\w+)", source(code)):
                self.assertIn(used, commands, f"{code}: {used}")


class Readme(unittest.TestCase):
    """The root README follows the reference project: one section per language, same order, same parts."""

    def test_nine_language_sections_with_the_same_parts_and_commands(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        names = [build_manual.NATIVE[code] for code in build_manual.LANGUAGES]
        self.assertEqual(re.findall(r"^## (.+)$", text, re.M), names)
        index = re.search(r"^\[Português \(Brasil\)\].*?(?=\n\n)", text, re.M | re.S)[0]
        self.assertEqual(re.findall(r"\[([^\]]+)\]\(#", index), names, "links to every section, in order")
        sections = re.split(r"^## .+$", text, flags=re.M)[1:]
        for name, section in zip(names, sections, strict=True):
            with self.subTest(language=name):
                self.assertEqual(len(re.findall(r"^### ", section, re.M)), 4, "structure, commands, docs, license")
                makes = re.findall(r"^(make \w+)", section, re.M)
                self.assertEqual(makes, ["make tools", "make check", "make build", "make manual"])
                links = re.findall(r"\]\(((?:docs|CHANGELOG|LICENSE)[^)]*)\)", section)
                for link in links:
                    self.assertTrue((ROOT / link).exists(), f"{name}: {link}")


class Rendering(unittest.TestCase):
    def test_missing_image_becomes_a_visible_placeholder(self):
        page = build_manual.Page("en")
        html = page.render("# Title {#t}\n\n![Alt text](nao_existe.jpg)\n\n```\ncode <x>\n```\n")
        self.assertIn('class="placeholder"', html)
        self.assertIn("&lt;nao_existe.jpg&gt;", html)
        self.assertIn("<pre><code>code &lt;x&gt;</code></pre>", html)
        self.assertEqual(page.missing, ["nao_existe.jpg"])

    def test_numbered_list_continues_after_a_code_block(self):
        html = build_manual.Page("en").render("1. one\n\n```\ncmd\n```\n\n2. two\n")
        self.assertIn('<ol style="counter-reset: list-item 1"><li>two</li></ol>', html)

    def test_unsafe_image_name_is_refused(self):
        with self.assertRaises(SystemExit):
            build_manual.Page("en").render("![x](../../etc/passwd.png)")

    @unittest.skipUnless(HAS_WEASYPRINT, "WeasyPrint not installed")
    def test_loader_refuses_files_outside_docs_manual(self):
        with self.assertRaises(ValueError):
            build_manual.fetcher((ROOT / "LICENSE").as_uri())
        with self.assertRaises(ValueError):
            build_manual.fetcher("https://example.com/x.png")

    def test_cover_links_every_language_in_its_own_name(self):
        page_html, missing = build_manual.document("0.0.0")
        self.assertEqual(set(missing), set(build_manual.LANGUAGES))
        cover = page_html.split('<section class="language"', 1)[0]
        for code, name in build_manual.NATIVE.items():
            self.assertIn(f'<a href="#{code}-toc">{name}</a>', cover)

    @unittest.skipUnless(HAS_WEASYPRINT, "WeasyPrint not installed")
    def test_pdf_bookmarks_one_per_language_and_links_have_targets(self):
        document, _ = build_manual.render("0.0.0")
        self.assertEqual(len(document.make_bookmark_tree()), len(build_manual.LANGUAGES))
        anchors = {anchor for page in document.pages for anchor in page.anchors}
        links = {link[1] for page in document.pages for link in page.links if link[0] == "internal"}
        self.assertTrue(links)
        self.assertLessEqual(links, anchors, "every internal link has a target")


if __name__ == "__main__":
    unittest.main()
