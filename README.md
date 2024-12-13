# High-Frequency Trading Strategy with Machine Learning

This project explores using machine learning techniques to generate returns in equity markets. The initial focus is on high-frequency trading (HFT) data simulations, but the framework can be adapted to daily market data as well. The goal is to develop a model capable of predicting short-term price movements to inform trading decisions.

###1. Data Acquisition and Preprocessing:

Data Source: Free, minute-tick intraday stock data was initially extracted from Yahoo Finance (limited to 5 business days).
Synthetic Data Generation: Due to data limitations, a Brownian Bridge model was developed to simulate realistic price movements and generate synthetic high-frequency data (second-level) for a larger dataset.
Technical Indicators and Trading Strategy:

Moving Averages:
An algorithm calculates both exponential and simple moving averages for any chosen stock.
A crossover trading strategy is implemented using these moving averages to generate buy/sell signals.
Trading Signal Generation:
The strategy uses the moving averages to create a "Signal" column indicating a buy (1) or hold (0) signal based on the short-term moving average crossing above the long-term one.
A "Positions" column is derived from the difference in the Signal column, capturing buy/sell transitions.
Trading Logic: (This section is clarified)
The code snippet outlines the trading logic based on the generated "Signal" values:
If the signal is 1 (buy), a portion of the capital is used to buy shares based on the current price.
If the signal is -1 (sell) and there are existing shares, those shares are sold at the current price.
If neither condition is met, the strategy holds the existing position.
Parameter Optimization:
A grid search was employed to find the optimal lengths for the short and long moving averages within a defined range. This optimization aims to identify the combination that maximizes profit and loss (PnL).
Visualization:
The code plots the stock price alongside markers indicating the buy/sell points triggered by the strategy.
This visualization provides a clear picture of the trading activity based on the strategy.
Additional Functionality:

Streamlit Integration:
A Streamlit dashboard allows users to:
Select the stock they want to analyze.
Specify the desired lengths for the short and long moving averages.
Visualize the performance of the trading strategy compared to the stock's price movement.
