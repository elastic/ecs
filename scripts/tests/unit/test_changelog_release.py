import os
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from release_automation.changelog import (
    _cut_changelog,
    _has_bullet_entries,
    _pr_sort_key,
    _remove_empty_sections,
    _sort_entries_in_section,
    cut_feature_freeze,
    cut_release,
    extract_section,
    finalize_changelog,
    get_section_text,
)


SAMPLE_NEXT = textwrap.dedent("""\
    <!-- comment block -->

    ## Unreleased

    ### Schema Changes

    #### Breaking changes

    #### Bugfixes

    #### Added

    * Added foo field. #100
    * Added bar field. #50

    #### Improvements

    #### Deprecated

    ### Tooling and Artifact Changes

    #### Breaking changes

    #### Bugfixes

    #### Added

    #### Improvements

    * Improved generator. #200

    #### Deprecated
""")

SAMPLE_MAIN = textwrap.dedent("""\
    <!-- Please add new changelog entries to CHANGELOG.next.md file -->

    # CHANGELOG

    ## [9.3.0](https://github.com/elastic/ecs/compare/v9.2.0...v9.3.0)

    ### Schema Changes

    #### Added

    * Old entry. #10
""")


class TestPrSortKey(unittest.TestCase):

    def test_extracts_pr_number(self):
        self.assertEqual(_pr_sort_key("* Some change #123"), 123)

    def test_returns_zero_for_no_pr(self):
        self.assertEqual(_pr_sort_key("* Some change without PR ref"), 0)

    def test_handles_trailing_whitespace(self):
        self.assertEqual(_pr_sort_key("* Change #456  "), 456)


class TestHasBulletEntries(unittest.TestCase):

    def test_true_with_bullets(self):
        self.assertTrue(_has_bullet_entries(["", "* entry", ""]))

    def test_false_without_bullets(self):
        self.assertFalse(_has_bullet_entries(["", "no bullets here", ""]))

    def test_false_empty(self):
        self.assertFalse(_has_bullet_entries([""]))


class TestRemoveEmptySections(unittest.TestCase):

    def test_removes_empty_h4_sections(self):
        text = textwrap.dedent("""\
            ## 1.0.0

            ### Schema Changes

            #### Added

            * An entry #1

            #### Bugfixes

            #### Improvements""")
        result = _remove_empty_sections(text)
        self.assertIn("#### Added", result)
        self.assertIn("* An entry #1", result)
        self.assertNotIn("#### Bugfixes", result)
        self.assertNotIn("#### Improvements", result)

    def test_preserves_h2_headings(self):
        text = "## 1.0.0\n\n### Empty\n\n#### Empty too"
        result = _remove_empty_sections(text)
        self.assertIn("## 1.0.0", result)

    def test_h3_emitted_before_h4_children(self):
        """Regression: ### headings must appear before their #### children."""
        text = textwrap.dedent("""\
            ## 1.0.0

            ### Schema Changes

            #### Breaking changes

            #### Added

            * Entry #1

            ### Tooling and Artifact Changes

            #### Added

            * Tool entry #2""")
        result = _remove_empty_sections(text)
        schema_pos = result.find("### Schema Changes")
        added_pos = result.find("#### Added")
        self.assertGreater(added_pos, schema_pos,
                           "### Schema Changes must appear before its #### Added child")

    def test_removes_h3_with_no_populated_children(self):
        text = textwrap.dedent("""\
            ## 1.0.0

            ### Schema Changes

            #### Breaking changes

            #### Bugfixes

            ### Tooling and Artifact Changes

            #### Added

            * Tool entry #1""")
        result = _remove_empty_sections(text)
        self.assertNotIn("### Schema Changes", result)
        self.assertIn("### Tooling and Artifact Changes", result)


class TestSortEntriesInSection(unittest.TestCase):

    def test_sorts_by_pr_id(self):
        text = textwrap.dedent("""\
            #### Added

            * Second #200
            * First #100
            * Third #300""")
        result = _sort_entries_in_section(text)
        lines = [l for l in result.split("\n") if l.startswith("*")]
        self.assertEqual(lines, ["* First #100", "* Second #200", "* Third #300"])

    def test_preserves_non_entry_lines(self):
        text = "#### Added\n\n* Entry #1\n"
        result = _sort_entries_in_section(text)
        self.assertIn("#### Added", result)


class TestCutFeatureFreeze(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        (self._next_path).write_text(SAMPLE_NEXT)

    @property
    def _next_path(self):
        from pathlib import Path
        return Path(self.tmpdir) / "CHANGELOG.next.md"

    def test_renames_unreleased(self):
        result = cut_feature_freeze("9.4.0", repo_root=self.tmpdir)
        self.assertIn("## 9.4.0 (Feature Freeze)", result)
        self.assertNotIn("## Unreleased", result)

    def test_inserts_fresh_unreleased(self):
        cut_feature_freeze("9.4.0", repo_root=self.tmpdir)
        content = self._next_path.read_text()
        self.assertIn("## Unreleased", content)
        unreleased_pos = content.find("## Unreleased")
        ff_pos = content.find("## 9.4.0 (Feature Freeze)")
        self.assertLess(unreleased_pos, ff_pos)

    def test_sorts_entries(self):
        result = cut_feature_freeze("9.4.0", repo_root=self.tmpdir)
        lines = [l for l in result.split("\n") if l.startswith("*")]
        pr_nums = [int(l.split("#")[-1]) for l in lines if "#" in l]
        self.assertEqual(pr_nums, sorted(pr_nums))

    def test_removes_empty_sections(self):
        result = cut_feature_freeze("9.4.0", repo_root=self.tmpdir)
        self.assertNotIn("#### Breaking changes", result)
        self.assertNotIn("#### Bugfixes", result)
        self.assertNotIn("#### Deprecated", result)


class TestExtractSection(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        from pathlib import Path
        cut_content = textwrap.dedent("""\
            <!-- comment -->

            ## Unreleased

            ## 9.4.0 (Feature Freeze)

            ### Schema Changes

            #### Added

            * Added foo. #100

            ### Tooling and Artifact Changes

            #### Improvements

            * Improved bar. #200
        """)
        (Path(self.tmpdir) / "CHANGELOG.next.md").write_text(cut_content)

    def test_extracts_categorized_entries(self):
        entries = extract_section("9.4.0", repo_root=self.tmpdir)
        self.assertIn("schema_added", entries)
        self.assertIn("tooling_improvements", entries)
        self.assertEqual(len(entries["schema_added"]), 1)
        self.assertIn("#100", entries["schema_added"][0])

    def test_raises_for_missing_version(self):
        with self.assertRaises(ValueError):
            extract_section("99.99.0", repo_root=self.tmpdir)


class TestFinalizeChangelog(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        from pathlib import Path
        next_content = textwrap.dedent("""\
            <!-- comment -->

            ## Unreleased

            ## 9.4.0 (Feature Freeze)

            ### Schema Changes

            #### Added

            * Entry. #100
        """)
        (Path(self.tmpdir) / "CHANGELOG.next.md").write_text(next_content)
        (Path(self.tmpdir) / "CHANGELOG.md").write_text(SAMPLE_MAIN)

    def test_moves_section_to_main(self):
        from pathlib import Path
        finalize_changelog("9.4.0", "9.3.0", "https://github.com/elastic/ecs", self.tmpdir)
        main_content = (Path(self.tmpdir) / "CHANGELOG.md").read_text()
        self.assertIn("[9.4.0](https://github.com/elastic/ecs/compare/v9.3.0...v9.4.0)", main_content)
        self.assertIn("* Entry. #100", main_content)

    def test_removes_section_from_next(self):
        from pathlib import Path
        finalize_changelog("9.4.0", "9.3.0", "https://github.com/elastic/ecs", self.tmpdir)
        next_content = (Path(self.tmpdir) / "CHANGELOG.next.md").read_text()
        self.assertNotIn("9.4.0", next_content)

    def test_inserts_before_existing_versions(self):
        from pathlib import Path
        finalize_changelog("9.4.0", "9.3.0", "https://github.com/elastic/ecs", self.tmpdir)
        main_content = (Path(self.tmpdir) / "CHANGELOG.md").read_text()
        new_pos = main_content.find("9.4.0")
        old_pos = main_content.find("9.3.0")
        self.assertLess(new_pos, old_pos)


class TestGetSectionText(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        content = textwrap.dedent("""\
            <!-- comment -->

            ## Unreleased

            ## 9.4.0 (Feature Freeze)

            ### Schema Changes

            #### Added

            * Entry one. #100
            * Entry two. #101

            ## 9.3.0

            ### Schema Changes

            #### Added

            * Old entry. #50
        """)
        (Path(self.tmpdir) / "CHANGELOG.next.md").write_text(content)

    def test_returns_section_text_for_ff_title(self):
        text = get_section_text("9.4.0", repo_root=self.tmpdir)
        self.assertIn("9.4.0 (Feature Freeze)", text)
        self.assertIn("Entry one. #100", text)
        self.assertIn("Entry two. #101", text)

    def test_does_not_include_adjacent_section(self):
        text = get_section_text("9.4.0", repo_root=self.tmpdir)
        self.assertNotIn("9.3.0", text)
        self.assertNotIn("Old entry", text)

    def test_returns_empty_string_for_missing_version(self):
        text = get_section_text("99.99.0", repo_root=self.tmpdir)
        self.assertEqual(text, "")

    def test_returns_non_empty_for_existing_version(self):
        text = get_section_text("9.3.0", repo_root=self.tmpdir)
        self.assertIn("Old entry", text)


class TestCutRelease(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        (Path(self.tmpdir) / "CHANGELOG.next.md").write_text(SAMPLE_NEXT)

    def test_uses_plain_version_title(self):
        result = cut_release("9.3.1", repo_root=self.tmpdir)
        self.assertIn("## 9.3.1", result)
        self.assertNotIn("Feature Freeze", result)

    def test_inserts_fresh_unreleased(self):
        cut_release("9.3.1", repo_root=self.tmpdir)
        content = (Path(self.tmpdir) / "CHANGELOG.next.md").read_text()
        self.assertIn("## Unreleased", content)
        unreleased_pos = content.find("## Unreleased")
        version_pos = content.find("## 9.3.1")
        self.assertLess(unreleased_pos, version_pos)

    def test_sorts_entries(self):
        result = cut_release("9.3.1", repo_root=self.tmpdir)
        lines = [l for l in result.split("\n") if l.startswith("*")]
        pr_nums = [int(l.split("#")[-1]) for l in lines if "#" in l]
        self.assertEqual(pr_nums, sorted(pr_nums))

    def test_removes_empty_sections(self):
        result = cut_release("9.3.1", repo_root=self.tmpdir)
        self.assertNotIn("#### Breaking changes", result)
        self.assertNotIn("#### Bugfixes", result)
        self.assertNotIn("#### Deprecated", result)


class TestCutChangelog(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        (Path(self.tmpdir) / "CHANGELOG.next.md").write_text(SAMPLE_NEXT)

    def test_custom_title(self):
        result = _cut_changelog("9.4.0", "9.4.0 (custom)", repo_root=self.tmpdir)
        self.assertIn("## 9.4.0 (custom)", result)

    def test_returns_section_text(self):
        result = _cut_changelog("9.4.0", "9.4.0 (Feature Freeze)", repo_root=self.tmpdir)
        self.assertIn("Added foo field", result)
        self.assertIn("Improved generator", result)


class TestExtractSectionRemoveprefix(unittest.TestCase):
    """Verify extract_section correctly strips heading markers using removeprefix."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        content = textwrap.dedent("""\
            ## 9.4.0 (Feature Freeze)

            ### Schema Changes

            #### Added

            * Schema add entry. #10

            #### Breaking changes

            * Schema break entry. #20

            ### Tooling and Artifact Changes

            #### Improvements

            * Tooling improvement. #30
        """)
        (Path(self.tmpdir) / "CHANGELOG.next.md").write_text(content)

    def test_h3_prefix_stripped_correctly(self):
        entries = extract_section("9.4.0", repo_root=self.tmpdir)
        # schema_added and tooling_improvements keys confirm h3/h4 heading text
        # was correctly parsed (not mangled by lstrip)
        self.assertIn("schema_added", entries)
        self.assertIn("tooling_improvements", entries)

    def test_h4_prefix_stripped_correctly(self):
        entries = extract_section("9.4.0", repo_root=self.tmpdir)
        self.assertIn("schema_breaking_changes", entries)
        self.assertIn("Schema break entry", entries["schema_breaking_changes"][0])

    def test_entries_assigned_to_correct_category(self):
        entries = extract_section("9.4.0", repo_root=self.tmpdir)
        self.assertIn("#10", entries["schema_added"][0])
        self.assertIn("#30", entries["tooling_improvements"][0])


if __name__ == "__main__":
    unittest.main()
