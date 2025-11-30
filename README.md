# Systematic Multi-Factor Portfolio Optimisation and Backtesting Simulator
*A tool for constructing, optimising, and backtesting systematic multi-factor equity portfolios using live market data.*

## Overview

This app provides a hands-on environment for exploring systematic factor-based investing. It retrieves **5 years of automatically adjusted daily price data** and computes **real market capitalisation** using each company’s latest **shares outstanding**. It then calculates three investment factors: **12-month momentum**, **annualised volatility**, and **size**, standardises them into **z-scores**, and combines them into a single **multi-factor score** used to rank stocks.<br>

The top-ranked names are selected into a portfolio and can be tested using either **equal-weighting** or **optimal Markowitz weights** (maximum Sharpe ratio). The simulator performs a full **daily-return backtest**, displaying cumulative performance, total return, annualised volatility, and Sharpe ratio through an interactive Streamlit interface.

## Features

- **Live Data Retrieval**  
  Pulls 5 years of adjusted daily prices and computes real market caps using `price × shares outstanding`.

- **Factor Computation**  
  - Momentum: past 12-month return  
  - Volatility: annualised standard deviation of daily returns  
  - Size: market capitalisation (last price × shares outstanding)

- **Multi-Factor Scoring**  
  Converts each factor into a z-score and aggregates them into a composite ranking.

- **Portfolio Construction**  
  Selects the top *N* ranked stocks and supports:  
  - Equal-weight portfolios  
  - Optimised max-Sharpe portfolios using mean–variance optimisation

- **Daily Backtesting**  
  Evaluates performance using daily returns for more accurate risk metrics.

- **Interactive Visualisation**  
  Streamlit + Plotly charts for equity curves, factor tables, and optimal weight allocation.

## Project Structure
```
Systematic-Multi-Factor-Portfolio-Optimisation-and-Backtesting-Simulator
├── app.py
├── factors.py
├── portfolio.py
├── backtest.py
└── requirements.txt
```

## Installation
```bash
git clone https://github.com/nauxiuh/Systematic-Multi-Factor-Portfolio-Optimisation-and-Backtesting-Simulator
cd Systematic-Multi-Factor-Portfolio-Optimisation-and-Backtesting-Simulator
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit interface:
```bash
streamlit run app.py
```
2. Enter a list of stock tickers (e.g., AAPL, MSFT, GOOGL, AMZN, META) and select how many top-ranked stocks to include.
3. Click Run Simulation to download data, compute factor scores, build the portfolio, optimise weights, and generate a full backtest.



## How It Works

1. **Load historical prices**  
   - Downloads 5 years of automatically adjusted daily prices (`auto_adjust=True`).

2. **Calculate investment factors**  
   - **Momentum**: 12-month percentage return  
   - **Volatility**: annualised standard deviation of daily returns  
   - **Size**: real market capitalisation (`price × shares outstanding`)

3. **Standardise factors**  
   - Converts raw factor values into z-scores for comparability.

4. **Build composite factor score**  
   - Computes a weighted sum of all factor z-scores.

5. **Select top-ranked stocks**  
   - Picks the highest-scoring stocks for portfolio inclusion.

6. **Portfolio weighting**  
   - **Equal-weight** (baseline)  
   - **Optimal Markowitz weight** (max Sharpe ratio)

7. **Backtest using daily returns**  
   - Computes daily portfolio returns and cumulative performance.

8. **Display results**  
   - Cumulative equity curve  
   - Optimal weights  
   - Factor table  
   - Total return  
   - Annualised volatility  
   - Sharpe ratio


## Example Outputs

### **Factor Table**
- 12-month momentum  
- Annualised volatility  
- Market cap (size)  
- Z-scores and composite factor ranking  

### **Ranked Stock List**
- Highest → lowest composite factor score  
- Top *N* selections highlighted  

### **Portfolio Weights**
- Equal-weight or **max-Sharpe optimised weights**  

### **Backtest Charts**
- Cumulative performance (Plotly)  
- Daily portfolio returns  

### **Performance Metrics**
- **Total return**  
- **Annualised volatility**  
- **Sharpe ratio** (daily returns × √252)
