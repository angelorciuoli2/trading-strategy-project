from momentum_strategy import MomentumStrategy

class RSI(MomentumStrategy):
    def calculate_rsi(self):
        delta = self.df[self.company].diff()  # Price differences between consecutive minutes
        gain = (delta.where(delta > 0, 0)).rolling(window=self.period).mean()  # Rolling mean of gains
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.period).mean()  # Rolling mean of losses
        rs = gain / loss  # RS (Relative Strength)
        self.df['RSI'] = 100 - (100 / (1 + rs))  # RSI formula