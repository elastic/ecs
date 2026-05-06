import os
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from release_automation.release_notes import (
    _format_entry,
    _insert_after_comment_template,
    _version_anchor,
    update_all,
    update_breaking_changes,
    update_deprecations,
    update_index,
)


class TestVersionAnchor(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(_version_anchor("9.4.0"), "ecs-9-4-0")

    def test_double_digit(self):
        self.assertEqual(_version_anchor("10.12.3"), "ecs-10-12-3")


class TestFormatEntry(unittest.TestCase):

    REPO = "https://github.com/elastic/ecs"

    def test_converts_pr_reference(self):
        result = _format_entry("* Added foo field. #1234", self.REPO)
        self.assertEqual(result, "* Added foo field [#1234](https://github.com/elastic/ecs/pull/1234)")

    def test_handles_no_period_before_pr(self):
        result = _format_entry("* Added foo field #1234", self.REPO)
        self.assertEqual(result, "* Added foo field [#1234](https://github.com/elastic/ecs/pull/1234)")

    def test_no_pr_returns_unchanged(self):
        entry = "* Some change without PR ref"
        self.assertEqual(_format_entry(entry, self.REPO), entry)

    def test_trailing_whitespace(self):
        result = _format_entry("* Change #456  ", self.REPO)
        self.assertIn("[#456]", result)


class TestInsertAfterCommentTemplate(unittest.TestCase):

    def test_inserts_after_comment_block(self):
        content = textwrap.dedent("""\
            % ## version.next [ecs-next-release-notes]

            % ### Features and enhancements [ecs-next-features-enhancements]
            % *

            ## 9.3.0 [ecs-9-3-0-release-notes]
            old content""")
        result = _insert_after_comment_template(
            content, "## 9.4.0 NEW SECTION", r"^% ## version\.next"
        )
        self.assertIn("## 9.4.0 NEW SECTION", result)
        new_pos = result.find("9.4.0")
        old_pos = result.find("9.3.0")
        self.assertLess(new_pos, old_pos)

    def test_fallback_before_first_heading(self):
        content = "# Title\n\n## 9.3.0\nold"
        result = _insert_after_comment_template(content, "## 9.4.0 NEW", r"^% ## nonexistent")
        new_pos = result.find("9.4.0")
        old_pos = result.find("9.3.0")
        self.assertLess(new_pos, old_pos)


class TestUpdateIndex(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        rn_dir = Path(self.tmpdir) / "docs" / "release-notes"
        rn_dir.mkdir(parents=True)
        self.index_path = rn_dir / "index.md"
        self.index_path.write_text(textwrap.dedent("""\
            # Release notes

            % ## version.next [ecs-next-release-notes]

            % ### Features and enhancements [ecs-next-features-enhancements]
            % *

            % ### Fixes [ecs-next-fixes]
            % *

            ## 9.3.0 [ecs-9-3-0-release-notes]

            ### Features and enhancements [ecs-9-3-0-features-enhancements]

            * Old entry [#10](https://github.com/elastic/ecs/pull/10)
        """))

    def test_inserts_new_version(self):
        entries = {
            "schema_added": ["* New field. #100"],
            "tooling_improvements": ["* Better generator. #200"],
        }
        update_index("9.4.0", entries, "https://github.com/elastic/ecs", self.tmpdir)
        content = self.index_path.read_text()
        self.assertIn("## 9.4.0 [ecs-9-4-0-release-notes]", content)
        self.assertIn("[#100]", content)
        self.assertIn("[#200]", content)

    def test_skips_if_already_present(self):
        entries = {"schema_added": ["* Entry. #1"]}
        update_index("9.4.0", entries, "https://github.com/elastic/ecs", self.tmpdir)
        content_before = self.index_path.read_text()
        update_index("9.4.0", entries, "https://github.com/elastic/ecs", self.tmpdir)
        content_after = self.index_path.read_text()
        self.assertEqual(content_before, content_after)

    def test_bugfixes_go_to_fixes(self):
        entries = {"schema_bugfixes": ["* Fixed a bug. #300"]}
        update_index("9.4.0", entries, "https://github.com/elastic/ecs", self.tmpdir)
        content = self.index_path.read_text()
        self.assertIn("### Fixes [ecs-9-4-0-fixes]", content)
        self.assertIn("[#300]", content)


class TestUpdateBreakingChanges(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        rn_dir = Path(self.tmpdir) / "docs" / "release-notes"
        rn_dir.mkdir(parents=True)
        self.path = rn_dir / "breaking-changes.md"
        self.path.write_text(textwrap.dedent("""\
            # Breaking changes

            % ## Next version [ecs-nextversion-breaking-changes]

            % some template

            ## 9.0.0 [ecs-9-0-0-breaking-changes]

            None at this time
        """))

    def test_inserts_breaking_changes(self):
        entries = {"schema_breaking_changes": ["* Removed field. #500"]}
        update_breaking_changes("9.4.0", entries, "https://github.com/elastic/ecs", self.tmpdir)
        content = self.path.read_text()
        self.assertIn("## 9.4.0 [ecs-9-4-0-breaking-changes]", content)
        self.assertIn("dropdown", content)

    def test_none_when_empty(self):
        update_breaking_changes("9.4.0", {}, "https://github.com/elastic/ecs", self.tmpdir)
        content = self.path.read_text()
        self.assertIn("None at this time", content)
        self.assertIn("9.4.0", content)


class TestUpdateDeprecations(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        rn_dir = Path(self.tmpdir) / "docs" / "release-notes"
        rn_dir.mkdir(parents=True)
        self.path = rn_dir / "deprecations.md"
        self.path.write_text(textwrap.dedent("""\
            # Deprecations

            % ## Next version [ecs-versionnext-deprecations]

            % template

            ## 9.0.0 [ecs-9-0-0-deprecations]

            None at this time
        """))

    def test_inserts_deprecations(self):
        entries = {"schema_deprecated": ["* Deprecated x. #600"]}
        update_deprecations("9.4.0", entries, "https://github.com/elastic/ecs", self.tmpdir)
        content = self.path.read_text()
        self.assertIn("## 9.4.0 [ecs-9-4-0-deprecations]", content)

    def test_none_when_empty(self):
        update_deprecations("9.4.0", {}, "https://github.com/elastic/ecs", self.tmpdir)
        content = self.path.read_text()
        self.assertIn("None at this time", content)


class TestUpdateAll(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        rn_dir = Path(self.tmpdir) / "docs" / "release-notes"
        rn_dir.mkdir(parents=True)
        (rn_dir / "index.md").write_text(
            "# Notes\n\n% ## version.next [x]\n\n% *\n\n## 9.3.0 [old]\n"
        )
        (rn_dir / "breaking-changes.md").write_text(
            "# BC\n\n% ## Next version [x]\n\n% *\n\n## 9.0.0 [old]\n"
        )
        (rn_dir / "deprecations.md").write_text(
            "# Dep\n\n% ## Next version [x]\n\n% *\n\n## 9.0.0 [old]\n"
        )

    def test_updates_all_three_files(self):
        entries = {
            "schema_added": ["* New. #1"],
            "schema_breaking_changes": ["* Breaking. #2"],
            "tooling_deprecated": ["* Deprecated. #3"],
        }
        update_all("9.4.0", entries, "https://github.com/elastic/ecs", self.tmpdir)

        rn_dir = Path(self.tmpdir) / "docs" / "release-notes"
        self.assertIn("9.4.0", (rn_dir / "index.md").read_text())
        self.assertIn("9.4.0", (rn_dir / "breaking-changes.md").read_text())
        self.assertIn("9.4.0", (rn_dir / "deprecations.md").read_text())


if __name__ == "__main__":
    unittest.main()
