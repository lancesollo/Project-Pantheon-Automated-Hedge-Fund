# Project Pantheon: Automated Hedge Fund

## Overview

Project Pantheon is a modular, agent-based trading system designed to simulate algorithmic trading with a human-readable and explainable structure. It connects multiple agents to form a pipeline:

1. **Technical Agent**: Generates BUY, SELL, or HOLD signals using EMA, RSI, and MACD indicators.
2. **Risk Manager**: Assesses volatility and assigns confidence to signals. Filters out risky trades.
3. **Portfolio Manager**: Executes trades and maintains account balance and positions.
4. **main.py**: Orchestrates the pipeline, performs backtesting, logs trades, and reports final performance.

---

## File Descriptions

### `technical.py`

* Calculates EMA (Exponential Moving Average), RSI (Relative Strength Index), and MACD (Moving Average Convergence Divergence).
* Uses those indicators to generate trading signals.
* Output: A pandas DataFrame with signal labels for each day.

### `risk_manager.py`

* Evaluates trade risk using rolling volatility from the historical price series.
* Converts volatility to a confidence score and approves/rejects trades accordingly.
* Returns structured feedback with position size and reasoning.

### `portfolio_manager.py`

* Executes approved trades.
* Tracks positions (how many shares held, entry price).
* Tracks cash balance and logs every transaction.

### `main.py`

* Loads cleaned stock price data (from `CSV/aapl_clean.csv`).
* Runs the trading simulation pipeline day-by-day.
* Prints trade logs and calculates performance summary.

---

## How to Run

1. Ensure dependencies are installed:

```bash
pip install pandas numpy
```

2. Place your cleaned AAPL data in `CSV/aapl_clean.csv`.

3. Run the main script:

```bash
python main.py
```

---

## Sample Output

```
Downloading data for AAPL...
Downloaded 250 days of data
Starting trading simulation...
2023-04-13: SELL at $163.91
...
Performance Summary:
Initial Value: $10000.00
Final Value: $10250.50
Total Return: 2.51%
Total Trades: 10 (Buys: 5, Sells: 5)
```

---

## Key Concepts

* **Modular Design**: Each agent performs one job and passes its result to the next.
* **Confidence Scoring**: Volatility is inversely correlated with confidence.
* **Backtesting**: Simulation occurs using historical data for objective performance review.
* **Technical Analysis**: Simple yet powerful indicators help identify market momentum and reversal.

---

## Future Extensions

* Real-time trading via APIs
* Strategy optimization using genetic algorithms
* Performance visualization dashboard
* More advanced risk controls (e.g., stop loss, drawdown limits)

---

## Author

Lance Silliman, Computer Science Capstone
Project Pantheon, 2025
