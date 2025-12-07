import numpy as np
import pandas as pd

def build_factor_score(factors: pd.DataFrame, weights=None) -> pd.Series:
    """
    Combine factors into a single composite score.

    - 'factors' should include columns like ['momentum', 'volatility', 'size'].
      'size' is expected to be raw market cap (for display).

    - 'weights' is a dict of factor weights, e.g.:
      {"momentum": 0.5, "volatility": 0.3, "size": 0.2}

    This function:
    1. Log-transforms market cap for stability (internally only).
    2. Z-scores all factors for comparability.
    3. Flips the sign of the size z-score so that smaller caps rank higher
       (consistent with the Fama–French SMB small-cap premium).
    4. Computes a weighted sum of z-scores.
    """

    if weights is None:
        weights = {col: 1 / len(factors.columns) for col in factors.columns}

    # Work on a copy so we don't modify the original factors table
    scoring_factors = factors.copy()

    # Optional but recommended: log-transform market cap before z-scoring
    if "size" in scoring_factors.columns:
        scoring_factors["size"] = np.log(scoring_factors["size"].clip(lower=1))

    # Standardise all factors to z-scores
    zscores = (scoring_factors - scoring_factors.mean()) / scoring_factors.std()

    # Flip size so that SMALL caps get HIGHER size scores
    if "size" in zscores.columns:
        zscores["size"] = -zscores["size"]

    # Weighted composite score
    score = sum(
        zscores[col] * w
        for col, w in weights.items()
        if col in zscores.columns
    )

    return score.sort_values(ascending=False)


def select_stocks(scores: pd.Series, n=10):
    """Pick top n stocks by composite factor score."""
    return scores.head(n).index.tolist()
