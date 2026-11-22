"""Offline checks of the statistics and rules added for Milestone 3 against reference values."""
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "ml"))
sys.path.insert(0, str(ROOT / "src" / "collect"))

from strict_labels import release_line  # noqa: E402
from train_eval import holm  # noqa: E402


class HolmTest(unittest.TestCase):
    def test_matches_statsmodels_reference_values(self):
        # statsmodels.stats.multitest.multipletests([.01,.04,.03,.005], method="holm")[1]
        p = pd.Series([0.01, 0.04, 0.03, 0.005])
        np.testing.assert_allclose(holm(p).to_numpy(), [0.03, 0.06, 0.06, 0.02])

    def test_monotone_capped_and_nan_kept(self):
        p = pd.Series([0.5, np.nan, 0.4, 0.9])
        h = holm(p)
        self.assertTrue(np.isnan(h.iloc[1]))
        self.assertTrue((h.dropna() <= 1).all())
        self.assertGreaterEqual(h.iloc[0], h.iloc[2])


class StrictLabelRulesTest(unittest.TestCase):
    def test_release_line_from_tags(self):
        self.assertEqual(release_line("release-3.6.0"), "3.6.")
        self.assertEqual(release_line("5.1.0"), "5.1.")
        self.assertEqual(release_line("rel/release-2.7.7"), "2.7.")

    def test_release_line_does_not_match_other_lines(self):
        line = release_line("release-3.6.0")
        self.assertTrue("3.6.4".startswith(line))
        self.assertFalse("3.61.0".startswith(line))
        self.assertFalse("3.7.0".startswith(line))


if __name__ == "__main__":
    unittest.main()
