# Regime-Adaptive Intraday Alpha Model  
### Quantitative Research Framework

---

## Overview

This project develops and evaluates a systematic intraday alpha framework operating on 5-minute bars across a correlation-defined equity universe.

The objective is not historical optimization, but to rigorously test whether a structurally defined signal family produces statistically credible excess returns under:

- Controlled parameter derivation  
- Bias-aware execution modeling  
- Cross-sectional validation  
- Regime segmentation  
- Walk-forward evaluation  

The emphasis is structural hypothesis validation, robustness, and disciplined research design.

---

## Structural Hypothesis

The strategy is built on the following assumptions:

1. Persistent positioning relative to VWAP reflects intraday institutional bias.
2. Short-horizon EMA cross events represent momentum inflection points with decaying predictive value.
3. Volatility regimes materially affect signal reliability.
4. Structural alignment (VWAP + trend + momentum) reduces false positives.
5. Risk anchored to structural invalidation improves payoff asymmetry.
6. Intraday signal strength varies by time-of-day and must be statistically derived.

This framework defines the signal class under investigation.

---

## Strategy Architecture

### Structural (Non-Optimized) Components

- 5-minute bar resolution  
- EMA(9,20) momentum transition pair  
- HMA(20) structural trend filter  
- RSI(14) and MACD confirmation  
- VWAP structural bias  
- Fixed notional position sizing  
- No overnight exposure  

These define the modeling space and are not tuned for performance maximization.

---

## Correlation-Defined Universe

NVDA is designated as the anchor asset.

Universe members are selected using rolling 252-day correlation with NVDA’s daily returns.  
The top N correlated, high-liquidity equities form the trading universe.

Universe selection is frozen prior to evaluation to prevent look-ahead bias.

---

## Statistically Derived Parameters

The following parameters are empirically determined using distributional analysis, conditional return studies, and stability testing:

- ATR lookback length  
- ATR percentile volatility threshold  
- EMA cross freshness window  
- VWAP activation delay  
- VWAP proximity band  
- Stop-loss distance (VWAP-anchored)  
- Breakeven trigger threshold  
- EMA/HMA reversal buffer  
- VWAP slope lookback windows  
- Intraday session participation windows  

Parameters are selected based on stability plateaus rather than peak Sharpe.

---

## Execution Model

- Signals computed at bar close (t)  
- Entries executed at open of bar (t+1)  
- Exits executed at next open following trigger  
- One active position per asset  
- Long and short performance evaluated independently  

This enforces symmetric, bias-controlled execution.

---

## Validation Framework

Data Range: 2016–2026

### 1. Static Parameter Validation

- Calibration: 2016–2019  
- Parameters locked  
- Out-of-sample evaluation: 2020–2026  

Tests structural permanence.

---

### 2. Rolling Recalibration (Walk-Forward)

- 3–4 year rolling training window  
- 1 year strictly out-of-sample test window  
- Repeated through 2025  

Simulates realistic deployment under regime drift.

---

### Final Holdout

2026 remains untouched until final evaluation.  
Represents simulated live deployment.

---

## Robustness Controls

The strategy must demonstrate stability across:

- Time (static vs rolling tests)  
- Volatility regimes  
- Cross-sectional universe members  
- Parameter neighborhoods  
- EMA pair perturbations  
- VWAP deviation perturbations  
- Risk buffer perturbations  
- Long vs short decomposition  

Edge must remain statistically credible under multiple independent stress dimensions.

---

## Evaluation Metrics

- Sharpe ratio  
- Trade return t-statistic  
- Maximum drawdown  
- Trade count stability  
- Regime-conditioned returns  
- Long vs short contribution  
- Return on deployed capital  

The objective is structural stability and statistical defensibility.

---

## Research Classification

This project represents:

A correlation-defined, volatility-conditioned, regime-aware intraday alpha research framework governed by formal statistical parameter calibration and dual validation protocols.

The goal is not to produce an optimized backtest, but to determine whether a structurally defined signal family exhibits stable, defensible alpha under disciplined research controls.

---

## Authors

Raymond Chbeir  
Maximillian Keller  

UC Berkeley