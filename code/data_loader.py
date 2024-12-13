import pandas as pd

class DataLoader:
    @staticmethod
    def load_data(file_path):
        df = pd.read_csv(file_path)
        df['Datetime'] = pd.to_datetime(df['Datetime'])
        df = df[df['Datetime'].dt.second == 0]
        df.reset_index(drop=True, inplace=True)
        df.set_index('Datetime', inplace=True)
        return df
