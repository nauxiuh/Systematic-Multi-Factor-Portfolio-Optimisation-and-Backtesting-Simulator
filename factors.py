import pandas as pd
import numpy as np

def calculate_momentum(price_df, lookback=252):
    """12-month momentum excluding last month."""
    return price_df.pct_change(lookback).iloc[-1]

def calculate_volatility(price_df, window=252):
    """1-year annualized volatility."""
    return price_df.pct_change().std() * np.sqrt(252)

def calculate_size(market_caps):
    """Market cap factor."""
    return market_caps

def calculate_factors(price_df, market_caps):
    factors = pd.DataFrame()
    factors["momentum"] = calculate_momentum(price_df)
    factors["volatility"] = calculate_volatility(price_df)
    factors["size"] = calculate_size(market_caps)
    return factors
