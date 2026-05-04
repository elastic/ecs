import json
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from release_automation.helpers import (
    count_labeled_prs,
    derive_previous_version,
    find_merged_pr,
    find_open_pr,
    forward_port_targets,
    parse_version,
    release_branch_for,
    require_no_backports,
)


class TestReleaseBranchFor(unittest.TestCase):

    def test_basic(self):
        self.assertEqual(release_branch_for("9.4.0"), "9.4")

    def test_double_digit(self):
        self.assertEqual(release_branch_for("10.12.3"), "10.12")

    def test_single_digit(self):
        self.assertEqual(release_branch_for("1.0.0"), "1.0")


class TestFindOpenPr(unittest.TestCase):

    def _make_result(self, prs: list) -> MagicMock:
        r = MagicMock()
        r.stdout = json.dumps(prs)
        return r

    @patch("release_automation.helpers.gh")
    def test_returns_first_pr_when_found(self, mock_gh):
        pr = {"number": 42, "url": "https://github.com/x/y/pull/42", "title": "Bump"}
        mock_gh.return_value = self._make_result([pr])
        result = find_open_pr("head-branch", "main", "x/y")
        self.assertEqual(result, pr)

    @patch("release_automation.helpers.gh")
    def test_returns_none_when_not_found(self, mock_gh):
        mock_gh.return_value = self._make_result([])
        result = find_open_pr("head-branch", "main", "x/y")
        self.assertIsNone(result)

    @patch("release_automation.helpers.gh")
    def test_queries_with_open_state(self, mock_gh):
        mock_gh.return_value = self._make_result([])
        find_open_pr("my-branch", "main", "elastic/ecs")
        args = mock_gh.call_args[0]
        self.assertIn("--state", args)
        self.assertIn("open", args)


class TestFindMergedPr(unittest.TestCase):

    def _make_result(self, prs: list) -> MagicMock:
        r = MagicMock()
        r.stdout = json.dumps(prs)
        return r

    @patch("release_automation.helpers.gh")
    def test_returns_first_pr_when_found(self, mock_gh):
        pr = {"number": 10, "url": "https://github.com/x/y/pull/10", "title": "Done"}
        mock_gh.return_value = self._make_result([pr])
        result = find_merged_pr("head-branch", "9.4", "x/y")
        self.assertEqual(result, pr)

    @patch("release_automation.helpers.gh")
    def test_returns_none_when_not_found(self, mock_gh):
        mock_gh.return_value = self._make_result([])
        result = find_merged_pr("head-branch", "9.4", "x/y")
        self.assertIsNone(result)

    @patch("release_automation.helpers.gh")
    def test_queries_with_merged_state(self, mock_gh):
        mock_gh.return_value = self._make_result([])
        find_merged_pr("my-branch", "9.4", "elastic/ecs")
        args = mock_gh.call_args[0]
        self.assertIn("--state", args)
        self.assertIn("merged", args)


class TestForwardPortTargets(unittest.TestCase):

    def _make_ls_remote_result(self, branches: list[str]) -> MagicMock:
        r = MagicMock()
        lines = [f"abc123\trefs/heads/{b}" for b in branches]
        r.stdout = "\n".join(lines)
        return r

    @patch("release_automation.helpers.git")
    def test_returns_branches_ahead_of_base(self, mock_git):
        mock_git.return_value = self._make_ls_remote_result(
            ["9.2", "9.3", "9.4", "9.5", "main"]
        )
        result = forward_port_targets("9.3", "elastic/ecs")
        self.assertEqual(result, ["9.4", "9.5", "main"])

    @patch("release_automation.helpers.git")
    def test_includes_main(self, mock_git):
        mock_git.return_value = self._make_ls_remote_result(
            ["9.3", "9.4", "main"]
        )
        result = forward_port_targets("9.3", "elastic/ecs")
        self.assertIn("main", result)

    @patch("release_automation.helpers.git")
    def test_excludes_same_and_earlier_branches(self, mock_git):
        mock_git.return_value = self._make_ls_remote_result(
            ["9.1", "9.2", "9.3", "9.4", "main"]
        )
        result = forward_port_targets("9.3", "elastic/ecs")
        self.assertNotIn("9.1", result)
        self.assertNotIn("9.2", result)
        self.assertNotIn("9.3", result)

    @patch("release_automation.helpers.git")
    def test_returns_sorted_order(self, mock_git):
        mock_git.return_value = self._make_ls_remote_result(
            ["9.5", "9.3", "10.0", "9.4", "main"]
        )
        result = forward_port_targets("9.3", "elastic/ecs")
        self.assertEqual(result, ["9.4", "9.5", "10.0", "main"])

    @patch("release_automation.helpers.git")
    def test_returns_only_main_for_non_semver_base(self, mock_git):
        mock_git.return_value = self._make_ls_remote_result(
            ["9.3", "9.4", "main"]
        )
        result = forward_port_targets("some-feature", "elastic/ecs")
        self.assertEqual(result, ["main"])

    @patch("release_automation.helpers.git")
    def test_empty_when_no_branches_ahead(self, mock_git):
        mock_git.return_value = self._make_ls_remote_result(
            ["9.1", "9.2", "9.3"]
        )
        result = forward_port_targets("9.3", "elastic/ecs")
        self.assertEqual(result, [])

    @patch("release_automation.helpers.git")
    def test_excludes_main_when_include_main_false(self, mock_git):
        mock_git.return_value = self._make_ls_remote_result(
            ["9.3", "9.4", "9.5", "main"]
        )
        result = forward_port_targets("9.3", "elastic/ecs", include_main=False)
        self.assertEqual(result, ["9.4", "9.5"])

    @patch("release_automation.helpers.git")
    def test_non_semver_base_with_include_main_false_returns_empty(self, mock_git):
        mock_git.return_value = self._make_ls_remote_result(
            ["9.3", "9.4", "main"]
        )
        result = forward_port_targets("feature-branch", "elastic/ecs", include_main=False)
        self.assertEqual(result, [])


class TestParseVersion(unittest.TestCase):

    def test_valid_version(self):
        self.assertEqual(parse_version(["script", "9.4.0"]), "9.4.0")

    def test_patch_version(self):
        self.assertEqual(parse_version(["script", "9.3.1"]), "9.3.1")

    def test_double_digit(self):
        self.assertEqual(parse_version(["script", "10.12.3"]), "10.12.3")

    def test_missing_argument_exits(self):
        with self.assertRaises(SystemExit):
            parse_version(["script"])

    def test_malformed_version_exits(self):
        with self.assertRaises(SystemExit):
            parse_version(["script", "9.4"])

    def test_prerelease_suffix_exits(self):
        with self.assertRaises(SystemExit):
            parse_version(["script", "9.4.0-rc1"])


class TestCountLabeledPrs(unittest.TestCase):

    def _make_result(self, prs: list) -> MagicMock:
        r = MagicMock()
        r.stdout = json.dumps(prs)
        return r

    @patch("release_automation.helpers.gh")
    def test_defaults_to_open_state(self, mock_gh):
        mock_gh.return_value = self._make_result([])
        count_labeled_prs("elastic/ecs", "needs_backport")
        args = mock_gh.call_args[0]
        self.assertIn("--state", args)
        idx = list(args).index("--state")
        self.assertEqual(args[idx + 1], "open")

    @patch("release_automation.helpers.gh")
    def test_passes_custom_state(self, mock_gh):
        mock_gh.return_value = self._make_result([])
        count_labeled_prs("elastic/ecs", "needs_backport", state="merged")
        args = mock_gh.call_args[0]
        idx = list(args).index("--state")
        self.assertEqual(args[idx + 1], "merged")

    @patch("release_automation.helpers.gh")
    def test_returns_count_and_prs(self, mock_gh):
        prs = [
            {"number": 1, "title": "PR1", "url": "u1"},
            {"number": 2, "title": "PR2", "url": "u2"},
        ]
        mock_gh.return_value = self._make_result(prs)
        count, result = count_labeled_prs("elastic/ecs", "some_label")
        self.assertEqual(count, 2)
        self.assertEqual(result, prs)


class TestRequireNoBackports(unittest.TestCase):

    def _make_result(self, prs: list) -> MagicMock:
        r = MagicMock()
        r.stdout = json.dumps(prs)
        return r

    @patch("release_automation.helpers.gh")
    def test_passes_when_no_merged_backports(self, mock_gh):
        mock_gh.return_value = self._make_result([])
        require_no_backports("elastic/ecs")

    @patch("release_automation.helpers.gh")
    def test_exits_when_merged_backports_exist(self, mock_gh):
        prs = [{"number": 99, "title": "Old PR", "url": "https://github.com/x/y/pull/99"}]
        mock_gh.return_value = self._make_result(prs)
        with self.assertRaises(SystemExit):
            require_no_backports("elastic/ecs")

    @patch("release_automation.helpers.gh")
    def test_queries_merged_state(self, mock_gh):
        mock_gh.return_value = self._make_result([])
        require_no_backports("elastic/ecs")
        args = mock_gh.call_args[0]
        idx = list(args).index("--state")
        self.assertEqual(args[idx + 1], "merged")


class TestDerivePreviousVersion(unittest.TestCase):

    def _make_result(self, releases: list) -> MagicMock:
        r = MagicMock()
        r.stdout = json.dumps(releases)
        return r

    @patch("release_automation.helpers.gh")
    def test_finds_latest_stable_release(self, mock_gh):
        releases = [
            {"tagName": "v9.4.0-rc1", "isPrerelease": True, "isDraft": False},
            {"tagName": "v9.3.0", "isPrerelease": False, "isDraft": False},
            {"tagName": "v9.2.0", "isPrerelease": False, "isDraft": False},
        ]
        mock_gh.return_value = self._make_result(releases)
        self.assertEqual(derive_previous_version("elastic/ecs"), "9.3.0")

    @patch("release_automation.helpers.gh")
    def test_scopes_to_same_minor_line(self, mock_gh):
        releases = [
            {"tagName": "v9.4.0", "isPrerelease": False, "isDraft": False},
            {"tagName": "v9.3.0", "isPrerelease": False, "isDraft": False},
            {"tagName": "v9.2.0", "isPrerelease": False, "isDraft": False},
        ]
        mock_gh.return_value = self._make_result(releases)
        self.assertEqual(derive_previous_version("elastic/ecs", "9.3.1"), "9.3.0")

    @patch("release_automation.helpers.gh")
    def test_falls_back_to_global_when_no_same_line_match(self, mock_gh):
        releases = [
            {"tagName": "v9.4.0", "isPrerelease": False, "isDraft": False},
        ]
        mock_gh.return_value = self._make_result(releases)
        self.assertEqual(derive_previous_version("elastic/ecs", "9.3.1"), "9.4.0")

    @patch("release_automation.helpers.gh")
    def test_skips_prereleases_and_drafts(self, mock_gh):
        releases = [
            {"tagName": "v9.4.0-rc1", "isPrerelease": True, "isDraft": False},
            {"tagName": "v9.4.0", "isPrerelease": False, "isDraft": True},
            {"tagName": "v9.3.0", "isPrerelease": False, "isDraft": False},
        ]
        mock_gh.return_value = self._make_result(releases)
        self.assertEqual(derive_previous_version("elastic/ecs"), "9.3.0")

    @patch("release_automation.helpers.gh")
    def test_returns_fallback_when_no_releases(self, mock_gh):
        mock_gh.return_value = self._make_result([])
        self.assertEqual(derive_previous_version("elastic/ecs"), "0.0.0")

    @patch("release_automation.helpers.gh")
    def test_strips_v_prefix(self, mock_gh):
        releases = [
            {"tagName": "v1.0.0", "isPrerelease": False, "isDraft": False},
        ]
        mock_gh.return_value = self._make_result(releases)
        self.assertEqual(derive_previous_version("elastic/ecs"), "1.0.0")


if __name__ == "__main__":
    unittest.main()
