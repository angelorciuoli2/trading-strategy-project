import numpy as np

class MovingAverageStrategy:
    def __init__(self, df, company, short_span, long_span, initial_capital):
        self.df = df.copy()
        self.company = company
        self.short_span = short_span
        self.long_span = long_span
        self.initial_capital = initial_capital
        self.final_pnl = 0
        self.df_final = None

    def calculate_short_long(self):
        raise NotImplementedError("Must implement in subclass")

    def apply_strategy(self):
        self.calculate_short_long()

        self.df['Signal'] = np.where(self.df['Short'] > self.df['Long'], 1.0, 0.0)
        self.df['Positions'] = self.df['Signal'].diff()

        capital = self.initial_capital
        shares = 0
        self.df['Action'] = ''
        self.df['Liquid Capital'] = capital
        self.df['# of Shares'] = shares
        self.df['Stock Value'] = shares * self.df[self.company]

        for i in range(1, len(self.df)):
            price = self.df[self.company].iloc[i]
            position = self.df['Positions'].iloc[i]

            if position == 1:
                shares_bought = capital // price
                capital -= shares_bought * price
                shares += shares_bought
                self.df.at[self.df.index[i], 'Action'] = 'BUY'
            elif position == -1 and shares > 0:
                capital += shares * price
                shares = 0
                self.df.at[self.df.index[i], 'Action'] = 'SELL'
            else:
                self.df.at[self.df.index[i], 'Action'] = 'HOLD'

            self.df.at[self.df.index[i], 'Liquid Capital'] = capital
            self.df.at[self.df.index[i], '# of Shares'] = shares
            self.df.at[self.df.index[i], 'Stock Value'] = shares * price
            self.df.at[self.df.index[i], 'PnL'] = capital + (shares * price) - self.initial_capital

        pnl = self.df['PnL'].iloc[-1]

        self.df_final = self.df # Intializing df_final

        if pnl > self.final_pnl:
            self.final_pnl = pnl
            self.df_final = self.df

        self.df_final.reset_index(inplace=True)
        self.df_final.drop(columns=['Signal', 'Positions'], inplace=True)
        self.df_final = self.df_final[['Datetime', self.company, 'Short', 'Long', 'Action', 'Liquid Capital', '# of Shares', 'Stock Value', 'PnL']]

        return self.df_final
