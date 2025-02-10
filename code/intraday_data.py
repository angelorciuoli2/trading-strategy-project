# intraday_data.py

import pandas as pd

class IntradayDataProcessor:
    def __init__(self, df):
        self.df = df.copy()  # Avoid modifying the original dataframe

    def resample_to_daily(self, start_date, end_date):

        self.df = self.df[(self.df['Datetime'].dt.date >= start_date) & (self.df['Datetime'].dt.date <= end_date)].reset_index(drop=True)
        
        # Ensure 'Date' column exists and is formatted correctly
        self.df['Date'] = self.df['Datetime'].dt.date.astype(str)
        self.df.insert(1, 'Date', self.df.pop('Date'))  # Move 'Date' to the second column
        
        # Define the price types and companies (excluding Date & Datetime)
        price = ['Open', 'Close', 'High', 'Low']
        company = [col for col in self.df.columns if col not in ['Date', 'Datetime']]

        # Create a MultiIndex for the new DataFrame
        multi_index = pd.MultiIndex.from_product([price, company], names=['Price', 'Company'])

        # Initialize the intraday_data DataFrame with 'Date' as the index
        intraday_data = pd.DataFrame(index=pd.Index(self.df['Date'].unique(), name='Date'), columns=multi_index)

        # Assign aggregated values
        grouped = self.df.groupby('Date')[company]
        intraday_data.loc[:, ('Open', slice(None))] = grouped.first().values
        intraday_data.loc[:, ('Close', slice(None))] = grouped.last().values
        intraday_data.loc[:, ('High', slice(None))] = grouped.max().values
        intraday_data.loc[:, ('Low', slice(None))] = grouped.min().values

        return intraday_data