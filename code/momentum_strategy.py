# momentum_strategy.py

class MomentumStrategy:
    def __init__(self, df, company, buy_condition, sell_condition, period, initial_capital):
        self.df = df.copy()
        self.company = company
        self.buy_condition = buy_condition
        self.sell_condition = sell_condition
        self.period = period
        self.initial_capital = initial_capital
        self.df_final = None

    def calculate_rsi(self):
        raise NotImplementedError("Must implement in subclass")

    def simulate_trading(self, start_date, end_date):
        self.calculate_rsi()  # Calculate RSI

        # Filtering dataframe to desired timeframe
        self.df = self.df[(self.df['Datetime'].dt.date >= start_date) & (self.df['Datetime'].dt.date <= end_date)].reset_index(drop=True)

        # Initialize variables and lists to store trading actions
        capital = self.initial_capital
        shares = 0
        actions = []
        liquid_capital = []
        stock_values = []
        pnl_values = []

        # Iterate through the DataFrame and apply buy/sell conditions
        for i in range(len(self.df)):
            price = self.df[self.company].iloc[i]  # Stock price for current row
            action = 'HOLD'  # Default action

            # Check buy condition
            if self.df['RSI'].iloc[i] < self.buy_condition and capital >= price:
                shares_to_buy = capital // price  # Determine how many shares to buy
                capital -= shares_to_buy * price  # Deduct capital spent
                shares += shares_to_buy  # Increase shares
                action = 'BUY'

            # Check sell condition
            elif self.df['RSI'].iloc[i] > self.sell_condition and shares > 0:
                capital += shares * price  # Sell all shares
                shares = 0  # Reset shares to 0
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
        self.df_final = self.df.reset_index()[['Datetime', self.company, 'RSI', 'Action', 'Liquid Capital', '# of Shares', 'Stock Value', 'PnL']]
        
        return self.df_final