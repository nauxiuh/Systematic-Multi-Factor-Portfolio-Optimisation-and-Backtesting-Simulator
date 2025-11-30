import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

from factors import calculate_factors
from portfolio import build_factor_score, select_stocks
from backtest import backtest, compute_optimal_weights

# --- App title ---
st.title("Systematic Multi-Factor Portfolio Optimisation Simulator")

# --- User inputs ---

tickers_input = st.text_input(
    "Enter tickers (comma-separated):",
    "AAPL,MSFT,GOOGL,AMZN,TSLA,META"
)

col_left, col_right = st.columns(2)

with col_left:
    # History length for prices
    lookback_years = st.slider(
        "Price history lookback (years):",
        min_value=1,
        max_value=10,
        value=5,
        help="Controls how many years of historical data are downloaded."
    )

    # Momentum lookback in months (converted to trading days)
    mom_lookback_months = st.slider(
        "Momentum lookback (months):",
        min_value=3,
        max_value=24,
        value=12,
        help="Lookback window for the momentum factor."
    )

with col_right:
    # Volatility window in trading days
    vol_window_days = st.slider(
        "Volatility window (trading days):",
        min_value=20,
        max_value=252,
        value=252,
        help="Number of trading days used to estimate volatility."
    )

    # Weighting method
    weighting_method = st.radio(
        "Portfolio weighting method:",
        ["Equal weight", "Optimal (max Sharpe)"]
    )

# Factor weights
with st.expander("Advanced: factor weights"):
    st.markdown("Adjust the relative importance of each factor (they will be normalised to sum to 1).")
    mom_w = st.slider("Momentum weight", 0.0, 1.0, 0.33, 0.01)
    vol_w = st.slider("Volatility weight", 0.0, 1.0, 0.33, 0.01)
    size_w = st.slider("Size weight", 0.0, 1.0, 0.34, 0.01)

    w_sum = mom_w + vol_w + size_w
    if w_sum == 0:
        factor_weights = {"momentum": 1/3, "volatility": 1/3, "size": 1/3}
    else:
        factor_weights = {
            "momentum": mom_w / w_sum,
            "volatility": vol_w / w_sum,
            "size": size_w / w_sum,
        }

n_stocks = st.slider("Number of stocks to select:", 3, 30, 5)

if st.button("Run Simulation"):
    # Clean tickers
    tickers = [t.strip() for t in tickers_input.split(",") if t.strip()]

    if not tickers:
        st.error("Please enter at least one valid ticker.")
        st.stop()

    st.write(f"Loading data for the past **{lookback_years}** years...")
    raw_data = yf.download(tickers, period=f"{lookback_years}y", auto_adjust=True)

    if raw_data.empty:
        st.error("No data was downloaded. Please check your tickers or try again later.")
        st.stop()

    # Handle single-index vs MultiIndex columns
    if isinstance(raw_data.columns, pd.MultiIndex):
        level0 = raw_data.columns.get_level_values(0)
        level1 = raw_data.columns.get_level_values(1)

        try:
            if "Close" in level0:
                price_df = raw_data.xs("Close", level=0, axis=1)
            elif "Close" in level1:
                price_df = raw_data.xs("Close", level=1, axis=1)
            else:
                raise KeyError("Close not found in any column level")
        except KeyError:
            st.error("Could not find 'Close' prices in downloaded data. Please check your tickers.")
            st.write("Columns found:", list(raw_data.columns))
            st.stop()
    else:
        if "Close" not in raw_data.columns:
            st.error("Downloaded data does not contain a 'Close' column.")
            st.write("Columns found:", list(raw_data.columns))
            st.stop()
        close_series = raw_data["Close"]
        price_df = close_series.to_frame() if not isinstance(close_series, pd.DataFrame) else close_series

    # Drop missing prices
    price_df = price_df.dropna(how="any")
    if price_df.empty:
        st.error("Price data is empty after dropping missing values. Try different tickers or period.")
        st.stop()

    # --- REAL market caps using price × shares outstanding ---
    st.write("Fetching shares outstanding and computing market caps...")
    mcaps = {}
    for t in price_df.columns:
        try:
            ticker = yf.Ticker(t)
            shares_series = ticker.get_shares_full(start="2000-01-01")
            if shares_series is None or len(shares_series) == 0:
                raise ValueError("No shares data returned")

            latest_shares = float(shares_series.iloc[-1])
            latest_price = float(price_df[t].iloc[-1])

            mcaps[t] = latest_price * latest_shares
        except Exception as e:
            st.warning(f"Could not fetch full shares data for {t}: {e}. Using fallback market cap.")
            latest_price = float(price_df[t].iloc[-1])
            mcaps[t] = latest_price * 1e9  # fallback

    market_caps = pd.Series(mcaps, index=price_df.columns)

    # --- Factor calculation with user lookbacks ---
    st.write("Calculating factors...")
    mom_lookback_days = int(mom_lookback_months * 21)  # approx 21 trading days per month
    factors = calculate_factors(
        price_df,
        market_caps,
        mom_lookback_days=mom_lookback_days,
        vol_window_days=vol_window_days
    )
    st.subheader("Factor Values")
    st.dataframe(factors)

    # --- Build scores with user factor weights ---
    scores = build_factor_score(factors, weights=factor_weights)

    # --- Select portfolio ---
    selected = select_stocks(scores, n=n_stocks)
    st.subheader("Selected Portfolio:")
    st.write(selected)

    # --- Portfolio weighting / backtest ---
    if weighting_method == "Equal weight":
        st.write("Using equal-weight portfolio...")
        weights = None
    else:
        st.write("Computing optimal weights (max Sharpe)...")
        weights = compute_optimal_weights(price_df, selected)
        st.subheader("Optimal Weights")
        st.write(weights)

    st.write("Running backtest...")
    ret, cumulative = backtest(price_df, selected, weights)

    # Plot cumulative return
    fig = px.line(cumulative, title="Cumulative Returns")
    st.plotly_chart(fig)

    # Performance stats (daily-based)
    st.subheader("Performance Stats")
    total_return = cumulative.iloc[-1] - 1
    ann_vol = ret.std() * (252 ** 0.5)
    sharpe = (ret.mean() / ret.std() * (252 ** 0.5)) if ret.std() != 0 else float("nan")

    st.write(f"Total return: {total_return:.2%}")
    st.write(f"Annual volatility: {ann_vol:.2%}")
    st.write(f"Sharpe ratio (approx): {sharpe:.2f}")
