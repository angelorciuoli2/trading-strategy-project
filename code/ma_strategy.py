# ma_strategy.py

import numpy as np
import streamlit as st

class MovingAverageStrategy:
    def __init__(self, df, company, short_span, long_span, initial_capital):
        self.df = df.copy()
        self.company = company
        self.short_span = short_span
        self.long_span = long_span
        self.initial_capital = initial_capital
        self.df_final = None

    def calculate_short_long(self):
        raise NotImplementedError("Must implement in subclass")

    def apply_strategy(self, start_date, end_date):
        self.calculate_short_long()
        
        # Filtering dataframe to desired timeframe
        self.df = self.df[(self.df['Datetime'].dt.date >= start_date) & (self.df['Datetime'].dt.date <= end_date)].reset_index(drop=True)

        # Generate trading signals
        self.df['Signal'] = np.where(self.df['Short'] > self.df['Long'], 1.0, 0.0)
        self.df['Positions'] = self.df['Signal'].diff()

        # Initialize variables
        capital = self.initial_capital
        shares = 0
        actions = []
        liquid_capital = []
        stock_values = []
        pnl_values = []

        # Iterate through the DataFrame and apply buy/sell conditions
        for i in range(len(self.df)):
            price = self.df[self.company].iloc[i]
            action = 'HOLD'

            # Buy condition
            if self.df['Positions'].iloc[i] == 1 and capital >= price:
                shares_to_buy = capital // price
                capital -= shares_to_buy * price
                shares += shares_to_buy
                action = 'BUY'

            # Sell condition
            elif self.df['Positions'].iloc[i] == -1 and shares > 0:
                capital += shares * price
                shares = 0
                action = 'SELL'

            # Store values in lists (for batch updates)
            actions.append(action)
            liquid_capital.append(float(capital))
            stock_values.append(float(shares * price))
            pnl_values.append(float(capital + (shares * price) - self.initial_capital))

        # Assign calculated values to the DataFrame in one batch (efficient)
        self.df['Action'] = actions
        self.df['Liquid Capital'] = liquid_capital
        self.df['# of Shares'] = shares
        self.df['Stock Value'] = stock_values
        self.df['PnL'] = pnl_values

        # Select and reorder final columns
        self.df_final = self.df.reset_index()[['Datetime', self.company, 'Short', 'Long', 'Action', 'Liquid Capital', '# of Shares', 'Stock Value', 'PnL']]
        
        return self.df_final