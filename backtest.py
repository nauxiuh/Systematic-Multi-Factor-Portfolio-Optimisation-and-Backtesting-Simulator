import pandas as pd
import numpy as np

def compute_optimal_weights(price_df, stocks):
    """
    Compute Markowitz optimal weights (max Sharpe ratio)
    using daily returns.
    """

    returns = price_df[stocks].pct_change().dropna()

    mu = returns.mean().values           # expected returns
    cov = returns.cov().values           # covariance matrix

    n = len(stocks)
    ones = np.ones(n)

    # Solve for max Sharpe ratio portfolio:
    # w = inv(Cov) * mu / (1' * inv(Cov) * mu)

    inv_cov = np.linalg.inv(cov)
    numer = inv_cov @ mu
    denom = ones @ numer
    w = numer / denom

    # Guarantee no negative NaN
    w = np.maximum(w, 0)
    w = w / w.sum()

    return pd.Series(w, index=stocks)


def backtest(price_df, stocks, weights=None):
    """
    Backtest using either:
    - equal weight (if weights=None)
    - optimal weights (from compute_optimal_weights)
    """

    returns = price_df[stocks].pct_change().dropna()

    if weights is None:
        # Equal weight
        port_returns = returns.mean(axis=1)
    else:
        # Matrix multiply daily returns with weight vector
        w = weights.values
        port_returns = returns @ w

    cumulative = (1 + port_returns).cumprod()

    return port_returns, cumulative
