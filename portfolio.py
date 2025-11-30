def build_factor_score(factors, weights=None):
    """
    Combine factors into a single score.
    weights = {"momentum": 0.5, "volatility": 0.3, "size": 0.2}
    """
    if weights is None:
        weights = {col: 1/len(factors.columns) for col in factors.columns}

    # Normalize factors
    zscores = (factors - factors.mean()) / factors.std()

    # Weighted score
    score = sum(zscores[col] * w for col, w in weights.items())
    return score.sort_values(ascending=False)

def select_stocks(scores, n=10):
    """Pick top n stocks."""
    return scores.head(n).index.tolist()
