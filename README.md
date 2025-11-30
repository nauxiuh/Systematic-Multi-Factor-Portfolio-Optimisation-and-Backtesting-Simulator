# Simulator for Factor-Based Stock Selection and Portfolio Backtesting
*A tool for constructing and backtesting systematic multi-factor equity portfolios using live market data.*


## Overview

This app provides a hands-on environment for exploring systematic factor-based investing. It retrieves **5 years of adjusted close prices** and **live market capitalisation data** for any user-selected stock tickers, then computes three investment factors: **12-month momentum**, **annualised volatility**, and **size**. These factors are standardised into **z-scores** and combined into a **single multi-factor score** to rank stocks.<br>

The top-scoring names are selected into an **equal-weight portfolio**, which is then **backtested using monthly returns and rebalancing**. The app displays cumulative performance, total return, annualised volatility, and an approximate Sharpe ratio through an interactive Streamlit interface.


## Features

- **Live Data Retrieval**  
  Pulls 5 years of historical price data and real-time market caps using `yfinance`.

- **Factor Computation**  
  - Momentum: 12-month return  
  - Volatility: annualised standard deviation of daily returns  
  - Size: market capitalisation

- **Multi-Factor Scoring**  
  Converts factors into z-scores and combines them into a single weighted score.

- **Portfolio Construction**  
  Selects the top *N* ranked stocks to form an equal-weight strategy.

- **Monthly Backtesting**  
  Computes monthly returns, cumulative performance, and risk metrics.

- **Interactive Visualisation**  
  Streamlit + Plotly charts for equity curves and factor tables.
  

## Project Structure
```
factor_simulator
├── app.py
├── factors.py
├── portfolio.py
├── backtest.py
└── requirements.txt
```

## Installation
```bash
git clone https://github.com/nauxiuh/Simulator-for-Factor-Based-Stock-Selection-and-Portfolio-Backtesting
cd Simulator-for-Factor-Based-Stock-Selection-and-Portfolio-Backtesting
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit interface:
```bash
streamlit run app.py
```
2. Enter a list of stock tickers (e.g., AAPL, MSFT, GOOGL, AMZN, META) and choose how many top-ranked stocks to include in the portfolio.
Click Run Simulation to download data, compute factor scores, build the portfolio, and generate a full backtest.


## How It Works

1. **Load historical prices**  
   - Downloads 5 years of daily adjusted close prices using `yfinance`.

2. **Calculate investment factors**  
   - **Momentum**: 12-month return  
   - **Volatility**: annualised standard deviation of daily returns  
   - **Size**: live market capitalisation

3. **Standardise factors**  
   - Converts all factor values into z-scores for comparability.

4. **Build combined factor score**  
   - Computes a weighted sum of all factor z-scores.

5. **Select top-ranked stocks**  
   - Picks the highest-scoring stocks for an equal-weight portfolio.

6. **Backtest monthly**  
   - Calculates monthly returns, rebalances, and generates cumulative performance.

7. **Display results**  
   - Shows equity curve, total return, annualised volatility, and Sharpe ratio in Streamlit.


## Example Outputs

- Factor table displaying:  
  - 12-month momentum  
  - Annualised volatility  
  - Market cap (size)  
  - Z-scores and combined factor score  

- Ranked stock list  
  - Highest → lowest multi-factor scores  
  - Selected top *N* stocks highlighted  

- Backtest visualisations  
  - Cumulative return line chart (Plotly)  
  - Monthly portfolio returns  

- Performance metrics  
  - **Total return**  
  - **Annualised volatility**  
  - **Approximate Sharpe ratio**

