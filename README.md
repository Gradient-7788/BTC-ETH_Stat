# Cryptocurrency Trading Strategies using Mean Reversion and Hurst Exponents

This repository presents a mean-reversion trading strategy developed for BTC/USDT using statistical signal processing and fractal analysis. The strategy was designed with an emphasis on systematic execution, quantitative rigor, and modular architecture. This can also be used on ETH/USDT considering the mean-correlation of BTC and ETH in real-time market.

## Overview

The strategy features:
- **Kalman Filter** for dynamic smoothing and estimation of price signals
- **Hurst Exponent** to assess trend persistence vs. mean reversion
- **Technical indicators** (OHLCV) via custom classes
- Integration with **Untrade API** to source crypto market data

## Structure

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

- **

## Strategy Flow



