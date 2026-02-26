# Regime-Adaptive Intraday Alpha Program  
### Dual-Architecture Quantitative Research Framework  

---

## Overview

This project develops and evaluates a systematic intraday alpha research program operating on 5-minute bars.

Rather than optimizing a single trading strategy, this work implements a **controlled experimental framework** comparing two competing signal architectures:

- **Model A (Control): Price-Derivative Momentum Framework**
- **Model B (Experimental): Flow-Structural Microstructure Framework**

The objective is to determine which structural signal family — price momentum or volume-derived flow pressure — exhibits more durable, statistically defensible alpha under institutional-grade validation constraints.

The emphasis is:

- Structural hypothesis testing  
- Parameter governance  
- Bias-aware execution modeling  
- Regime robustness  
- Transaction cost survivability  
- Walk-forward validation  

This is a research study — not an optimized backtest.

---

# Research Question

> Does short-horizon price momentum (EMA-based structure) outperform flow-derived microstructure pressure signals under disciplined, cost-adjusted, multi-regime validation?

Model A serves as the **control architecture**.  
Model B serves as the **experimental upgrade**.

Both are evaluated under identical time splits, cost assumptions, and robustness protocols.

---

# Model A — Control Architecture  
## Price-Derivative Momentum Framework

### Structural Hypothesis

1. Persistent positioning relative to VWAP reflects intraday institutional bias.
2. Short-horizon EMA cross events represent momentum inflection points with decaying predictive value.
3. Volatility regimes materially affect signal reliability.
4. Structural alignment (VWAP + trend + momentum) reduces false positives.
5. Risk anchored to structural invalidation improves payoff asymmetry.
6. Intraday signal strength varies by time-of-day and must be statistically derived.

### Structural (Non-Optimized) Components

- 5-minute bar resolution  
- EMA(9,20) momentum transition pair  
- HMA(20) structural trend filter  
- RSI(14) and MACD confirmation  
- VWAP structural bias  
- Fixed notional position sizing  
- No overnight exposure  

These define the modeling space and are not tuned for peak Sharpe.

---

# Model B — Experimental Architecture  
## Flow-Structural Microstructure Framework

### Structural Hypothesis

1. Volume-weighted directional pressure better reflects true order flow than lagging price derivatives.
2. Auction-based structural acceptance (Point of Control) provides superior trend validation.
3. Liquidity- and volatility-adaptive universe construction improves regime resilience.
4. Institutional participation intensity (time-relative volume) filters weak signals.
5. Alpha must survive realistic transaction cost modeling.

### Core Components

- 5-minute OHLCV-based Estimated Volume Delta (EVD)  
- Rolling flow oscillator (sum or slope of recent EVD)  
- VWAP structural alignment  
- Intraday Volume Profile & Point of Control (POC)  
- Time-of-day Relative Volume (RVOL) filter  
- Dynamic high-volatility, high-liquidity universe  

Model B tests whether flow-derived pressure dominates price-based momentum.

---

# Universe Construction

## Model A — Correlation-Defined Universe

- Anchor asset: NVDA  
- 252-day rolling correlation with NVDA daily returns  
- Top N high-liquidity correlated equities selected  
- Universe frozen prior to evaluation to prevent look-ahead bias  

## Model B — Dynamic Volatility-Liquidity Universe

- Ranked by 14-day ATR relative to price  
- Filtered by minimum dollar liquidity  
- Elevated pre-market participation required  
- Daily rebalanced using strictly lagged data  

This tests static correlation clustering vs adaptive volatility selection.

---

# Statistically Derived Parameters

Parameters are selected using:

- MAE/MFE distribution analysis  
- Conditional forward return studies  
- Stability plateau identification  
- Cross-sectional robustness  
- Regime segmentation  

No parameter is selected solely on peak Sharpe.

Parameters include:

- ATR lookback & percentile thresholds  
- EMA freshness windows  
- VWAP proximity bands  
- Stop-loss & breakeven geometry  
- Structural reversal buffers  
- VWAP slope filters  
- Session participation windows  
- RVOL thresholds  
- Flow window length  

---

# Execution Model

- Signals computed at bar close (t)  
- Orders executed at open of bar (t+1)  
- All exits executed at next open after trigger  
- One active position per asset  
- Long and short performance evaluated independently  
- No overnight exposure  

Execution symmetry is enforced to reduce bias.

---

# Transaction Cost Modeling (TCA)

A conservative proportional cost model is applied:

- 5 bps round-trip (2.5 bps per side)

Long Entry:
Actual_Entry = Theoretical_Open × (1 + 0.00025)

Long Exit:
Actual_Exit = Theoretical_Exit × (1 − 0.00025)

Equivalent logic applied to shorts.

Sensitivity testing includes ±1–2 bps perturbations.

Alpha must survive cost-adjusted evaluation.

---

# Validation Framework

Data Range: 2016–2026

## 1. Static Parameter Validation

- Calibration: 2016–2019  
- Parameters locked  
- Out-of-sample: 2020–2026  

Tests structural permanence.

---

## 2. Rolling Recalibration (Walk-Forward)

- 3–4 year rolling training window  
- 1 year strictly out-of-sample test window  
- Repeated through 2025  

Simulates realistic regime drift.

---

## Final Holdout

2026 remains untouched until final evaluation.  
Represents simulated live deployment.

---

# Robustness & Anti-Overfitting Controls

Each architecture must demonstrate stability across:

- Static vs rolling evaluation  
- Volatility regimes  
- Cross-sectional universe members  
- Parameter neighborhoods  
- EMA pair perturbations  
- VWAP deviation perturbations  
- Risk buffer perturbations  
- Flow window perturbations  
- Session window sensitivity  
- Long vs short decomposition  

Edges must persist on stability plateaus, not isolated parameter peaks.

---

# Evaluation Metrics

- Sharpe ratio  
- Trade return t-statistic  
- Maximum drawdown  
- Trade count stability  
- Regime-conditioned returns  
- Long vs short contribution  
- Return on deployed capital  
- Cost-adjusted performance  

The objective is structural durability and statistical defensibility.

---

# Research Philosophy

This project does not assume alpha exists.

If both models fail under:

- Transaction costs  
- Rolling out-of-sample validation  
- Parameter perturbation  
- Regime segmentation  

Then the signal family will be rejected.

The framework is reusable for future alpha exploration.

---

# Research Classification

This project represents:

A dual-architecture intraday alpha research program comparing price-derivative momentum signals against flow-structural microstructure signals under disciplined parameter governance, realistic execution modeling, and multi-regime validation protocols.

The goal is not backtest optimization —  
but to determine whether a structurally defined signal family exhibits durable, defensible alpha.

---

# Authors

Raymond Chbeir  
Maximillian Keller  

UC Berkeley