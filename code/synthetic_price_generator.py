import numpy as np
import pandas as pd
import yfinance as yf
import warnings
warnings.filterwarnings("ignore")

# Functions and retrieving yahoo finance data

# Brownian Bridge Function
def brownian_bridge(start, end, steps):
    dt = 1 / steps
    brownian_motion = np.random.normal(0, np.sqrt(dt), size=steps)
    brownian_motion[0] = 0  # Starting point
    brownian_bridge = np.cumsum(brownian_motion) - (np.arange(steps) / steps) * np.cumsum(brownian_motion)[-1]
    return float(start) + (float(end) - float(start)) * (np.arange(steps) / steps) + brownian_bridge

# Function that calls Brownian Bridge to generate synthetic intraday prices
def simulate_intraday_prices(open_price, close_price, steps=60):
    return brownian_bridge(open_price, close_price, steps)

# Selected securites
tickers = ['AAPL', 'TSLA', 'AMZN', 'MSFT', 'GOOGL', 'NVDA', 'META', 'AVGO', 'CSCO', 'ADBE', 'ORCL', 'CRM', 'AMD', 'QCOM', 'INTC', 'TXN', 'PYPL', 'NFLX', 'UBER', 'SNOW', 'ZM', 'SPOT', 'SHOP', 'SQ', 'PLTR', 'TWLO', 'TEAM', 'DDOG', 'NET', 'CRWD', 'FTNT', 'ROKU', 'MRVL', 'MTCH', 'TTD', 'OKTA', 'DBX']

# Retrieving yahoo finance intraday data for the last 5 business days, datapoint per minute
intraday_data = yf.download(tickers=tickers, period='5d', interval='1m')

# Creation of synthetic data

# Range of collected dates
recent_dates = pd.date_range(end=pd.Timestamp.today(), periods=5, freq='B')  # Get last 5 business days because period parameter is 5

# Dictionary to hold simulated prices
simulated_data = {}

# Loop through each ticker
for ticker in tickers:
    simulated_prices = []  # Initialize list to store prices for this ticker
    time_indices = []  # List to store corresponding time indices

    # Loop through each day
    for day in recent_dates:
        try:
            # Access data for the specific day
            day_data = intraday_data.loc[
                (intraday_data.index.date == day.date()),  # Filter for the current day
                (slice(None), slice(None))
            ]

            # Check if day_data is empty
            if day_data.empty:
                print(f"No data found for {ticker} on {day.date()}. Skipping this day.")
                continue  # Skip this day if no data is found

            day_data = day_data.xs(ticker, level=1, axis=1)  # Select data for the current ticker

            # Generating 60 synthetic datapoints for each 1-minute interval
            for i in range(len(day_data) - 1):
                open_price = day_data['Open'].iloc[i]
                close_price = day_data['Close'].iloc[i + 1]
                synthetic_prices = simulate_intraday_prices(open_price, close_price, steps=60)  # 60 seconds so 60 steps

                # Time index for synthetic prices
                start_time = day_data.index[i]
                time_index = pd.date_range(start=start_time, periods=len(synthetic_prices), freq='S')

                simulated_prices.extend(synthetic_prices)
                time_indices.extend(time_index)

            # Append the last close price
            simulated_prices.append(day_data['Close'].iloc[-1])
            time_indices.append(day_data.index[-1] + pd.Timedelta(seconds=60))  # Add a time index for the last close price

        except KeyError:
            print(f"No data found for {ticker} on {day.date()}. Check data availability or date format.")
            continue  # Skip this day if data is not found

    # Store each ticker's simulated data in a DataFrame
    simulated_data[ticker] = pd.DataFrame(simulated_prices, index=pd.to_datetime(time_indices), columns=['Price'])

# Coverting simulated_data dictionary into DataFrame

# Looping through dictionary
rows = []
for ticker, df in simulated_data.items():
    for index, row in df.iterrows():
        rows.append((index, ticker, row['Price']))

# Formatting sythetic data into single index DataFrame
df = pd.DataFrame(rows, columns=['Datetime', 'Company', 'Price']).pivot(index='Datetime', columns='Company', values='Price').reset_index()
df.columns.name = None

# CSV
# df.to_csv('MM-DD_MM-DD.csv', index=False)
