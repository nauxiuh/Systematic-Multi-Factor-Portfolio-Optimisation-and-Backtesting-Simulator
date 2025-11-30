import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

from factors import calculate_factors
from portfolio import build_factor_score, select_stocks
from backtest import backtest

# --- App title ---
st.title("Systematic Factor Strategy Workbench")

# --- User inputs ---
tickers_input = st.text_input(
    "Enter tickers (comma-separated):",
    "AAPL,MSFT,GOOGL,AMZN,TSLA,META"
)
n_stocks = st.slider("Number of stocks to select:", 3, 20, 5)

if st.button("Run Simulation"):
    # Clean tickers
    tickers = [t.strip() for t in tickers_input.split(",") if t.strip()]

    if not tickers:
        st.error("Please enter at least one valid ticker.")
        st.stop()

    st.write("Loading data...")

    # Explicitly set auto_adjust=True to avoid Adj Close issues
    raw_data = yf.download(tickers, period="5y", auto_adjust=True)

    if raw_data.empty:
        st.error("No data was downloaded. Please check your tickers or try again later.")
        st.stop()

    # Handle both single-index and multi-index column formats from yfinance
    if isinstance(raw_data.columns, pd.MultiIndex):
    # yfinance can return either (field, ticker) or (ticker, field)
        level0 = raw_data.columns.get_level_values(0)
        level1 = raw_data.columns.get_level_values(1)

        try:
            if "Close" in level0:
                # case 1: ('Close', 'AAPL'), ('Close', 'AMZN'), ...
                price_df = raw_data.xs("Close", level=0, axis=1)
            elif "Close" in level1:
                # case 2: ('AAPL', 'Close'), ('AMZN', 'Close'), ...
                price_df = raw_data.xs("Close", level=1, axis=1)
            else:
                raise KeyError("Close not found in any column level")
        except KeyError as e:
            st.error("Could not find 'Close' prices in downloaded data. Please check your tickers.")
            st.write("Columns found:", list(raw_data.columns))
            st.stop()

    else:
        # For a single ticker: columns like ['Open','High','Low','Close',...]
        if "Close" not in raw_data.columns:
            st.error("Downloaded data does not contain a 'Close' column.")
            st.write("Columns found:", list(raw_data.columns))
            st.stop()
        close_series = raw_data["Close"]
        price_df = close_series.to_frame() if not isinstance(close_series, pd.DataFrame) else close_series

    # Drop rows with missing prices
    price_df = price_df.dropna(how="any")

    if price_df.empty:
        st.error("Price data is empty after dropping missing values. Try different tickers or period.")
        st.stop()

    # Real market caps using price × shares outstanding
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
            mcaps[t] = latest_price * 1e9  # assume 1 billion shares as a rough placeholder

    market_caps = pd.Series(mcaps, index=price_df.columns)

    # Calculate factors
    st.write("Calculating factors...")
    factors = calculate_factors(price_df, market_caps)
    st.subheader("Factor Values")
    st.dataframe(factors)

    # Build scores
    scores = build_factor_score(factors)

    # Select portfolio
    selected = select_stocks(scores, n=n_stocks)
    st.subheader("Selected Portfolio:")
    st.write(selected)

    # Backtest
    st.write("Running backtest...")
    ret, cumulative = backtest(price_df, selected)

    # Plot cumulative return
    fig = px.line(cumulative, title="Cumulative Returns")
    st.plotly_chart(fig)

    st.subheader("Performance Stats")
    total_return = cumulative.iloc[-1] - 1
    ann_vol = ret.std() * (12 ** 0.5)
    sharpe = (ret.mean() / ret.std() * (12 ** 0.5)) if ret.std() != 0 else float("nan")

    st.write(f"Total return: {total_return:.2%}")
    st.write(f"Annual volatility: {ann_vol:.2%}")
    st.write(f"Sharpe ratio (approx): {sharpe:.2f}")
