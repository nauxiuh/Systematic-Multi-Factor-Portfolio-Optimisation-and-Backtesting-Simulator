import pandas as pd
import numpy as np

def calculate_momentum(price_df, lookback=252):
    """
    12-month momentum by default.
    Uses percentage change over 'lookback' trading days.
    """
    # pct_change over 'lookback' periods, take last row
    if len(price_df) <= lookback:
        lookback = len(price_df) - 1  # avoid empty
    return price_df.pct_change(lookback).iloc[-1]

def calculate_volatility(price_df, window=252):
    """
    Annualised volatility based on 'window' trading days.
    """
    daily_ret = price_df.pct_change()
    if len(daily_ret) <= window:
        window = len(daily_ret) - 1
    rolling = daily_ret.tail(window)
    return rolling.std() * np.sqrt(252)

def calculate_size(market_caps):
    """Market cap factor."""
    return market_caps

def calculate_factors(price_df, market_caps, mom_lookback_days=252, vol_window_days=252):
    """
    Calculate all factors with configurable lookbacks.
    """
    factors = pd.DataFrame()
    factors["momentum"] = calculate_momentum(price_df, lookback=mom_lookback_days)
    factors["volatility"] = calculate_volatility(price_df, window=vol_window_days)
    factors["size"] = calculate_size(market_caps)
    return factors
