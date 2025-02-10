# avg_tr.py

import pandas as pd

class ATRCalculator:
    def __init__(self, intraday_df):
        """
        Requires intraday_data.py in order to execute
        """
        self.df = intraday_df.copy()

    def calculate_atr(self, company):
        """
        Computes the Average True Range (ATR) for given companies over a specified date range.
        """
        atr_df = self.df
        atr_values = {}  # Store ATR values for each company
        atr_percentages = {}


        # Compute True Range (TR) components
        high = atr_df[('High', company)]
        low = atr_df[('Low', company)]
        close = atr_df[('Close', company)]          

        # Shift close prices to get the previous day's close
        prev_close = close.shift(1)

        # Calculate TR components
        TR1 = high - low
        TR2 = abs(prev_close - high)
        TR3 = abs(prev_close - low)

        # Compute max(TR1, TR2, TR3)
        TRmax = pd.concat([TR1, TR2, TR3], axis=1).max(axis=1)
        TRmax = TRmax.iloc[1:]

        # Calculate ATR as the mean of TRmax
        atr_value = TRmax.mean()

        # Calculate ATR as a percentage of the last close price
        atr_percentage = round((atr_value / (close.iloc[-1])) * 100, 2)

        return atr_value, atr_percentage