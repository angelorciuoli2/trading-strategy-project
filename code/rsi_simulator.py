import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.font_manager import FontProperties
import streamlit as st

from data_loader import DataLoader
from stock_plotter import StockPlotter
from plot_utils import PlotUtils
from ema import EMA
from sma import SMA
from rsi import RSI

st.set_page_config(layout="wide")
st.title("Trading Strategy Simulator")

uploaded_file = st.file_uploader("Upload CSV Data", type="csv")

if uploaded_file is not None:
    df = DataLoader.load_data(uploaded_file)
    st.write("Data Loaded Successfully!")

    # Defining date range
    min_date = df['Datetime'].min().date() 
    max_date = df['Datetime'].max().date()
    st.header("Select Date Range:")
    selected_date_range = st.date_input(" ", min_value=min_date, max_value=max_date, value=(min_date, max_date), key="date_range")
    start_date, end_date = selected_date_range
    df = df[(df['Datetime'].dt.date >= start_date) & (df['Datetime'].dt.date <= end_date)]

    # Finding top 5 most volatile stocks
    top_volatility_df = pd.DataFrame({
        'Company': df.columns[1:],  # Exclude 'Datetime' column
        'Volatility': df.iloc[:, 1:].std()  # Standard deviation of each stock
    }).sort_values(by='Volatility', ascending=False).head(5)

    top_companies = ', '.join(top_volatility_df['Company'])

    st.write(f"Recommendation: Trading strategies perform better with more volatile stocks. The top 5 most volatile stocks within this period are **{top_companies}**.")


    st.header("Select Stocks:")

    # Replace selectbox with checkboxes for multiple company selection
    selected_companies = []
    cols_per_row = 13  # Adjust this to control how many checkboxes per row

    # Create columns to display checkboxes
    for row in range((len(df.columns) - 1) // cols_per_row + 1):
        cols = st.columns(cols_per_row)
        for col_index, col in enumerate(cols):
            company_index = row * cols_per_row + col_index + 1
            if company_index < len(df.columns):
                company = df.columns[company_index]
                if col.checkbox(company, value=company in selected_companies):
                    # Add or remove company from selected_companies list
                    if company not in selected_companies:
                        selected_companies.append(company)
                    else:
                        selected_companies.remove(company)

    # Plot the selected companies immediately as they are selected
    if selected_companies:
        for company in selected_companies: 
            plotter = StockPlotter.plot(df, company, start_date, end_date)
            st.pyplot(plotter)

    # Check if there are selected companies
    if len(selected_companies) > 0:
        # Form columns for each company to define individual strategy settings
        form_cols = st.columns(len(selected_companies))

        final_company = None
        final_strategy = None
        final_lower_bound = None
        final_upper_bound = None
        final_period = None
        final_initial_capital = None

        # Loop over the selected companies to create form inputs for each one
        for i, company in enumerate(selected_companies):
            with form_cols[i].form(f'strategy_form_{company}'):
                st.subheader(f'{company} Strategy Settings')
                strategy = st.radio(f'Select Trading Strategy', ['RSI'], index=None, horizontal=True)
                initial_capital = st.number_input("Initial Capital ($):", min_value=10000)
                lower_bound = st.slider(f'RSI Lower Bound:', min_value=5, max_value=40, value=35)
                upper_bound = st.slider(f'RSI Upper Bound:', min_value=50, max_value=95, value=85)
                period = st.slider(f'RSI Period:', min_value=1, max_value=20, value=7)
                submit_button = st.form_submit_button(label=f"Execute")

                if submit_button:
                    final_company = company
                    final_strategy = strategy
                    final_lower_bound = lower_bound
                    final_upper_bound = upper_bound
                    final_period = period
                    final_initial_capital = initial_capital


        if final_strategy == "RSI":
            strategy_instance = RSI(df, final_company, final_lower_bound, final_upper_bound, final_period, final_initial_capital)
            company_df = strategy_instance.simulate_trading(start_date, end_date)
            st.subheader(f"RSI Trading Results for {final_company}")
            st.subheader(f"Final PnL: ${company_df['PnL'].iloc[-1]:.2f}")
            fig, pnl_return, stock_price_growth, buy_count, sell_count = PlotUtils.trading_plot(company_df, final_company, final_strategy)
            st.pyplot(fig)
                


        

        