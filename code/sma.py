from ma_strategy import MovingAverageStrategy

class SMA(MovingAverageStrategy):
    def calculate_short_long(self):
        self.df['Short'] = self.df[self.company].rolling(window=self.short_span, min_periods=1).mean()
        self.df['Long'] = self.df[self.company].rolling(window=self.long_span, min_periods=1).mean()
