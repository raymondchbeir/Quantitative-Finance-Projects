# Reinforcement Learning for Intraday Equity Trading
## Causal, Regime-Normalized State-Based Framework

This repository implements a reinforcement learning (RL) trading framework designed to learn execution-aware intraday trading policies on equities (NVDA, PLTR) using causally constructed market state representations.

Rather than training directly on price levels or raw technical indicators, the agent observes a volatility-normalized, regime-adaptive state vector composed of momentum, volatility, liquidity, and market-context features. The objective is to learn a policy capable of trading trend-continuation structures (e.g., EMA-9/EMA-20 alignment with VWAP context) while accounting for intraday volatility variation, transaction costs, and trade feasibility.

---

## Methodology and Architecture

The framework utilizes a shared feature encoder that feeds into separate actor heads for long/short entries and a shared critic. To ensure the model generalizes across different market conditions, a regime-normalization layer is employed to preserve stationarity:

$$x_{norm} = \frac{x_t - \mu_{window}}{\sigma_{window}}$$

### Key Objectives
* **Trend Continuation:** Capturing moves where EMA-9/20 and VWAP show strong directional alignment.
* **Execution Realism:** Implementing synthetic friction to discourage profits that would not survive real-world bid/ask spreads.
* **Risk Budgeting:** Entry actions are dynamically masked based on daily drawdown limits and trade feasibility.

---

## Repository Structure

```text
quant-github/
├── data/
│   ├── raw/                # Historical 5m Alpaca SIP data (ignored)
│   └── processed/          # Causal and normalized feature sets
├── notebooks/
│   └── RL_trading.ipynb    # Training loop and walk-forward validation
├── src/
│   ├── config/
│   │   └── settings.py     # Hyperparameters and API config
│   ├── data/
│   │   └── ingestion.py    # Alpaca API interface
│   └── features/
│       ├── candle_micro.py # Impulse vs. rejection logic
│       └── volatility.py   # Multi-horizon rolling volatility
└── README.md
```

---

## State Representation

The agent observation space is constructed using intraday-only statistics to preserve stationarity and avoid look-ahead leakage:

### 1. Market and Strategy Context
* **Volatility-Normalized Returns:** Multi-horizon returns divided by rolling intraday volatility.
* **Microstructure:** Candle impulse/rejection ratios and volume z-scores.
* **Trend Signals:** EMA-9/20 slope, distance to VWAP, and trend decay proxies.
* **Benchmark Awareness:** Relative strength vs. QQQ and rolling asset–market correlation.

### 2. Position and Risk State
* **Inventory:** Current position status and time-in-trade.
* **Excursion Tracking:** Max Adverse Excursion (MAE) and Max Favorable Excursion (MFE).
* **Budget:** Remaining daily trade allocation and high-watermark PnL.

---

## Setup

1. **Clone the Repository**
   ```bash
   git clone [https://github.com/username/quant-github.git](https://github.com/username/quant-github.git)
   cd quant-github
   ```

2. **Environment Variables**
   Create a `.env` file in the root directory:
   ```env
   ALPACA_API_KEY=your_api_key
   ALPACA_SECRET_KEY=your_secret_key
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## Evaluation

Performance is evaluated using rolling walk-forward validation. This ensures the agent is tested on unseen regimes, simulating deployment where market dynamics shift over time. Transaction-cost assumptions are included in the reward computation to ensure net profitability.

---

## Disclaimer

This repository is intended for research and educational purposes only. No financial advice is provided. Trading equities involves significant risk of loss.
