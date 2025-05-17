# Cryptocurrency Trading Strategies using Mean Reversion and Hurst Exponents

This repository presents a mean-reversion trading strategy developed for BTC/USDT using statistical signal processing and fractal analysis. The strategy was designed with an emphasis on systematic execution, quantitative rigor, and modular architecture. This can also be used on ETH/USDT considering the mean-correlation of BTC and ETH in real-time market.

## Overview

The strategy features:
- **Kalman Filter** for dynamic smoothing and estimation of price signals
- **Hurst Exponent** to assess trend persistence vs. mean reversion
- **Technical indicators** (OHLCV) via custom classes
- Integration with **Untrade API** to source crypto market data

##  Repository Structure

```bash
kalman-hurst-btc-strategy/
│
├── data/                 # Sample data
├── notebook/             # Research and exploration
├── src/                  # Modular strategy code
│   ├── indicators.py     # Indicator calculations
│   ├── strategy.py       # Strategy logic and backtesting
│   └── utils.py          # Helper utilities
├── requirements.txt
└── README.md
```
## Regime Flow

- Zerolag- Cusum based regime prediction, earlier methods used k-means and HMMs. 
- F1-Score and TDA used for performance metrics.
![newplot](https://github.com/user-attachments/assets/e718c43f-9534-4a96-9132-cfb65bb4256a)

## Strategy Flow

### BTC_Approach
- Pull BTC/USDT, ETH/USDT OHLCV data
- Initialse technical indicators listed in indicators.py file.
- Filter and smoothen using Kalman Filter
- Estimate Hurst Exponent
- Apply mean reversion logic in strategy.py
- Log Performance metrics and PnL
- **Actions**: Enter Long/Short, Exit Long/Short, Hold
- **Reward Function**: Profit/loss adjusted for commission and risk

### ETH_Correlation_Approach
- Correlation analysis between BTC/USDT and ETH log returns.
- CUSUM for regime shift detection
- ATR-based volatility thresholds
- Hurst Exponent for trend filtering
- Kalman & Gaussian Filters for smoothing

## Features

- 📉 **Mean-reversion strategy** leveraging Hurst Exponent and Kalman Filter smoothing
- 🧠 **Kalman Filter**-based price estimation for robust signal generation
- 📈 **Hurst Exponent analysis** to identify trending vs. mean-reverting regimes
- 🔁 Dynamic entry/exit signals based on residual spread from the Kalman filter
- ⚖️ Custom position sizing logic based on volatility-adjusted thresholds
- 🧪 Fully parameterized backtesting with metrics for performance and trade efficiency
- 📊 Clear performance tracking via cumulative returns and trade annotations

## Tech Stack

- **Python** – Core development language  
- **NumPy, Pandas** – Data manipulation and series handling  
- **Matplotlib** – Performance and signal visualization  
- **Statsmodels** – Hurst Exponent and statistical tools  
- **FilterPy** – Kalman filter implementation  
- **Jupyter Notebooks** – Strategy development and prototyping  
  
## Getting Started

1. Clone the repository:

    ```bash
    git clone https://github.com/Gradient-7788/BTC-ETH_Stat
    cd BTC-ETH_Stat
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run simulations:

    - Use Jupyter notebooks in the `notebooks/` folder for ETH correlation and BTC RL experiments.

## 👥 Contributors

Team 67 – Zelta Automations  


