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
    raw_data = yf.download(tickers, period="5y")

    if raw_data.empty:
        st.error("No data was downloaded. Please check your tickers or try again later.")
        st.stop()

    # Handle both single-index and multi-index column formats from yfinance
    if isinstance(raw_data.columns, pd.MultiIndex):
        # Typical yfinance shape for multiple tickers: columns like (ticker, field)
        # e.g. ('AAPL', 'Adj Close'), ('MSFT', 'Adj Close'), ...
        try:
            price_df = raw_data.xs("Adj Close", level=1, axis=1)
        except KeyError:
            st.error("Could not find 'Adj Close' in downloaded data. Please check your tickers.")
            st.write("Columns found:", list(raw_data.columns))
            st.stop()
    else:
        # Single-index columns, e.g. for one ticker or older yfinance behaviour
        if "Adj Close" not in raw_data.columns:
            st.error("Downloaded data does not contain an 'Adj Close' column.")
            st.write("Columns found:", list(raw_data.columns))
            st.stop()
        price_df = raw_data["Adj Close"].to_frame() if not isinstance(raw_data["Adj Close"], pd.DataFrame) else raw_data["Adj Close"]

    # Drop rows with missing prices
    price_df = price_df.dropna(how="any")

    if price_df.empty:
        st.error("Price data is empty after dropping missing values. Try different tickers or period.")
        st.stop()

    # Fake market caps (for demo)
    market_caps = pd.Series(
        {t: yf.Ticker(t).info.get("marketCap", 1e10) for t in price_df.columns},
        index=price_df.columns,
    )

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
