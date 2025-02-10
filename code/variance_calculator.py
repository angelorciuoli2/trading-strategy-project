# variance_calculator.py

class VarianceCalculator:
    def __init__(self, df):
        self.df = df.copy()

    def calculate_variance(self, company, start_date, end_date):

        self.df = self.df[(self.df['Datetime'].dt.date >= start_date) & (self.df['Datetime'].dt.date <= end_date)].reset_index(drop=True)

        company_data = self.df[company]
        variance = company_data.var()

        return variance