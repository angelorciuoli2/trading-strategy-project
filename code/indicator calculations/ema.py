from ma_strategy import MovingAverageStrategy

class EMA(MovingAverageStrategy):
    def calculate_short_long(self):
        self.df['Short'] = self.df[self.company].ewm(span=self.short_span, adjust=False).mean()
        self.df['Long'] = self.df[self.company].ewm(span=self.long_span, adjust=False).mean()