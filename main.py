import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.font_manager import FontProperties
import streamlit as st

from data_loader import DataLoader  # Assuming you have a DataLoader class to handle file loading
from plot_utils import PlotUtils
from ema import EMA
from sma import SMA

st.title("Trading Strategy Simulator")

uploaded_file = st.sidebar.file_uploader("Upload CSV Data", type="csv")

if uploaded_file is not None:
    df = DataLoader.load_data(uploaded_file)
    st.sidebar.write("Data Loaded Successfully!")

    company = st.sidebar.selectbox("Choose a Company:", df.columns)
    initial_capital = st.sidebar.number_input("Initial Capital ($):", min_value=10000)

    short_span = st.sidebar.slider("Short Span (minutes):", min_value=5, max_value=150, value=40)
    long_span = st.sidebar.slider("Long Span (minutes):", min_value=10, max_value=250, value=100)
    strategy = st.sidebar.selectbox("Select a Strategy", ["EMA", "SMA"])

    if short_span >= long_span:
        st.sidebar.error("Long Span must be greater than Short Span.")
    elif st.sidebar.button("Execute Strategy"):
        if strategy == "EMA":
            strategy_instance = EMA(df, company, short_span, long_span, initial_capital)
            company_df = strategy_instance.apply_strategy()
            st.subheader(f"EMA Trading Results for {company}")
            st.subheader(f"Final PnL: ${company_df['PnL'].iloc[-1]:.2f}")
            st.pyplot(PlotUtils.trading_plot(company_df, company))

        elif strategy == "SMA":
            strategy_instance = SMA(df, company, short_span, long_span, initial_capital)
            company_df = strategy_instance.apply_strategy()
            st.subheader(f"SMA Trading Results for {company}")
            st.subheader(f"Final PnL: ${company_df['PnL'].iloc[-1]:.2f}")
            st.pyplot(PlotUtils.trading_plot(company_df, company))