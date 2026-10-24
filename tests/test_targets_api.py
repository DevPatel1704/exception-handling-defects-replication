"""Offline tests for the dashboard's tag handling and input validation (no network).

Run: ./envrun.sh python -m unittest discover -s tests -v
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "pipeline"))
import targets_api as T  # noqa: E402

HIBERNATE = ["4.3.0.CR1", "4.3.0.Final", "4.3.11.Final", "5.0.0.CR1", "5.0.0.Final", "5.0.1.Final", "5.0.2.Final",
             "5.0.3.Final", "5.0.10.Final", "5.0.16", "5.0.3", "5.1.0", "5.1.1", "5.1.17", "5.2.0", "6.0.0.Alpha1"]
HADOOP = ["release-2.5.0", "release-2.5.2", "release-2.6.0", "release-2.6.0-rc0", "release-2.6.1", "release-2.6.3",
          "rel/release-2.6.5", "release-2.7.0", "feature_YARN-2928_2015-08-24", "YARN-7055-2018-03-02"]


class VersionParsing(unittest.TestCase):
    def test_versions(self):
        self.assertEqual(T._ver("release-2.6.5"), (2, 6, 5))
        self.assertEqual(T._ver("rel/release-2.6.5"), (2, 6, 5))
        self.assertEqual(T._ver("5.0.0.Final"), (5, 0, 0))
        self.assertEqual(T._ver("LANG_3_0_1"), (3, 0, 1))
        self.assertEqual(T._ver("gson-parent-2.13.2"), (2, 13, 2))
        self.assertIsNone(T._ver("feature_YARN-2928_2015-08-24"))
        self.assertIsNone(T._ver("YARN-7055-2018-03-02"))

    def test_prerelease(self):
        for t in ("5.0.0.CR1", "6.0.0.Alpha1", "release-2.6.0-rc0", "commons-lang-3.21.0-RC2", "LANG_3_0_B3",
                  "release-3.9.7-1"):
            self.assertTrue(T.is_prerelease(t), t)
        for t in ("5.0.0.Final", "release-2.6.0", "rel/release-2.6.5", "5.1.17"):
            self.assertFalse(T.is_prerelease(t), t)


class Suggestions(unittest.TestCase):
    def test_paper_choices_hibernate(self):   # the paper: 5.0.0.Final -> 5.0.16
        s = T.suggest_tags(sorted(HIBERNATE, key=T.version_key, reverse=True), "5.0.0.Final")
        self.assertEqual(s["post_release"], "5.0.16")
        self.assertEqual(s["prev_release"], "4.3.0.Final")

    def test_new_context_hibernate(self):     # our Phase 1 target: 5.1.0 -> 5.1.17, prev 5.0.0.Final
        s = T.suggest_tags(HIBERNATE, "5.1.0")
        self.assertEqual((s["post_release"], s["prev_release"]), ("5.1.17", "5.0.0.Final"))

    def test_paper_choices_hadoop(self):      # the paper: release-2.6.0 -> rel/release-2.6.5
        s = T.suggest_tags(HADOOP, "release-2.6.0")
        self.assertEqual((s["post_release"], s["prev_release"]), ("rel/release-2.6.5", "release-2.5.0"))

    def test_zookeeper_rc_suffix(self):     # release-3.7.2-0 is a release candidate of release-3.7.2
        tags = ["release-3.6.0", "release-3.7.0", "release-3.7.0-1", "release-3.7.1", "release-3.7.2", "release-3.7.2-0",
                "release-3.7.3-0"]
        s = T.suggest_tags(tags, "release-3.7.0")
        self.assertEqual((s["post_release"], s["prev_release"]), ("release-3.7.2", "release-3.6.0"))

    def test_no_later_patch(self):
        s = T.suggest_tags(["v1.0", "v1.1", "v1.2"], "v1.1")
        self.assertEqual(s["post_release"], "v1.2")
        self.assertTrue(any("next release" in n for n in s["notes"]))


class Validation(unittest.TestCase):
    def test_urls(self):
        self.assertEqual(T.normalize_repo_url("https://github.com/a/b.git/"), "https://github.com/a/b")
        for bad in ("http://github.com/a/b", "file:///etc/passwd", "https://github.com/a/../b", "git@github.com:a/b",
                    "https://github.com/a b/c", "ext::sh -c touch% /tmp/x", ""):
            with self.assertRaises(ValueError, msg=bad):
                T.normalize_repo_url(bad)


if __name__ == "__main__":
    unittest.main()
