"""Offline checks of the statistics added for Milestone 3 against reference implementations."""
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "ml"))
sys.path.insert(0, str(ROOT / "src" / "collect"))

from train_eval import holm  # noqa: E402
from validation_agreement import cohen_kappa, wilson  # noqa: E402


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


class AgreementTest(unittest.TestCase):
    def test_kappa_matches_sklearn(self):
        from sklearn.metrics import cohen_kappa_score
        rng = np.random.default_rng(1)
        a = pd.Series(rng.choice(["yes", "no", "unsure"], 60, p=[.7, .2, .1]))
        b = a.where(rng.random(60) > 0.25, pd.Series(rng.choice(["yes", "no"], 60)))
        self.assertAlmostEqual(cohen_kappa(a, b), cohen_kappa_score(a, b), places=10)

    def test_perfect_agreement(self):
        a = pd.Series(["yes", "no", "yes", "unsure"])
        self.assertAlmostEqual(cohen_kappa(a, a), 1.0)

    def test_wilson_reference(self):
        lo, hi = wilson(34, 40)          # reference: 0.7091, 0.9293
        self.assertAlmostEqual(lo, 0.709, places=3)
        self.assertAlmostEqual(hi, 0.929, places=3)


if __name__ == "__main__":
    unittest.main()
