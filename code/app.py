import streamlit as st
import numpy as np
from phi.assistant import Assistant
from phi.llm.openai import OpenAIChat
from data_loader import DataLoader
from stock_plotter import StockPlotter
from intraday_data import IntradayDataProcessor
from avg_tr import ATRCalculator
from tabular_data import TabularDataProcessor
from variance_calculator import VarianceCalculator
import pandas as pd
from ema import EMA
from sma import SMA
from rsi import RSI
from plot_utils import PlotUtils
from TradingResultsAssistant import TradingResultsAssistant


# PART 1: LEVERAGING LLM, SETTING UP AI ASSISTANT, AND DISPLAYING CONVO BETWEEN USER AND AI ON STREAMLIT
st.set_page_config(layout="wide")
st.title("AI-assisted Stock Trading Simulator")

st.markdown("""
This AI assistant simulates the performance of three distinct trading strategies on any stock of your choice. 
By analyzing historical data, it helps you understand how these strategies would have performed over a specified timeframe.
            
The available trading strategies are:
""")
cols = st.columns(3)

with cols[0]:
    with st.expander("1. **Simple Moving Average (SMA)**"):
        st.write("""
        SMA uses two averages applied to a stock's price: a short-term average (e.g., avg of the previous 40 minutes) and a long-term average (e.g., avg of the previous 100 minutes). 
        The strategy triggers a buy when the short average crosses above the long average, and a sell when the long average crosses above the short average. 
        The period for both averages can be customized.
        """)

with cols[1]:
    with st.expander("2. **Exponential Moving Average (EMA)**"):
        st.write("""
        EMA is a trend-following strategy applied to a stock’s price, calculating the average price over a set period, with more weight given to recent prices. 
        The strategy buys when the short-term EMA crosses above the long-term EMA and sells when the long-term EMA crosses above the short-term EMA. 
        The periods for both averages can be customized based on the trader's preferences.
        """)

with cols[2]:
    with st.expander("3. **Relative Strength Index (RSI)**"):
        st.write("""
        RSI is a momentum-based strategy applied to a stock’s price, measuring the speed and change of price movements over a set period (e.g., 7 minutes or 7 days). 
        The RSI ranges from 0 to 100, with values above the upper bound indicating overbought conditions, prompting a sell, and values below the lower bound indicating oversold conditions, prompting a buy. 
        The period and bounds can be customized based on the trader's preferences.
        """)
            
st.markdown("""
Simply prompt the assistant to apply any of these strategies to a stock of your choice and define the time period for analysis. 
The assistant will then simulate how the selected strategy would have performed over the stock.
""")

uploaded_file = st.file_uploader("Upload CSV Data", type="csv")
if uploaded_file is not None:
    df = DataLoader.load_data(uploaded_file)
    st.write("Data Loaded Successfully!")

# Create two columns
col1, col2 = st.columns([3,4])

# Left Column: Moving Average Spans
with col1:
    with st.expander("**SMA & EMA: set custom parameters.**"):
        st.markdown("**Short Span:** Averages data over a shorter period, making it more responsive to recent price changes. The duration is determined by the value you set.") 
        st.markdown("**Long Span:** Averages data over a longer period, making it less responsive to recent price changes and smoother overall. The duration is determined by the value you set.")
        
        short_span = st.slider('Short Span:', min_value=5, max_value=150, value=40)
        long_span = st.slider('Long Span:', min_value=10, max_value=250, value=100)

# Right Column: RSI Bounds
with col2:
    with st.expander("**Relative Strength Index (RSI): set custom parameters.**"):
        st.markdown("**Lower Bound:** The RSI value below which a stock is considered oversold, indicating a buying opportunity.") 
        st.markdown("**Upper Bound:** The RSI value above which a stock is considered overbought, indicating a selling opportunity.")  
        st.markdown("**Period:** The number of minutes used to calculate the RSI, determining how sensitive it is to price changes.")
        lower_bound = st.slider('RSI Lower Bound:', min_value=5, max_value=40, value=35)
        upper_bound = st.slider('RSI Upper Bound:', min_value=50, max_value=95, value=85)
        period = st.slider('RSI Period:', min_value=1, max_value=20, value=7)

# Initialize your Assistant with stock trading context
assistant = Assistant(
    llm=OpenAIChat(model="gpt-3.5-turbo"),
    description="You provide stock trading advice and structure user requests for visualizations. If a user asks for a visualization of RSI, EMA, or SMA, provide a concise definition of the strategy before structuring their request for visualization. Do not mention limitations about generating charts.",
    instructions=[
        "Ensure responses are based on up-to-date market trends and sound trading principles.",
        "If a user asks for a visualization, focus on structuring their request concisely without disclaiming any limitations on chart generation.",
        "The three trading strategies available are Relative Strength Index (RSI), Simple Moving Average (SMA), and Exponential Moving Average (EMA).",
        "If a user requests a strategy outside of these three, respond briefly by stating that only RSI, SMA, and EMA can be used and no other strategies are supported.",
        "If a user is clearly asking for a strategy to be applied to a stock, only provide a concise definition of the strategy (RSI, SMA, or EMA). Do not mention the process of generating the visualization."
    ],
)

# Initialize session state for messages (a chat log)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Displaying the chat log (handling both text and figures)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if isinstance(message["content"], str):  # Text messages
            st.markdown(message["content"])
        elif isinstance(message["content"], pd.DataFrame):  # Table messages
            st.table(message["content"])  # Display the table
        else:  # Figure messages
            col1, col2, col3 = st.columns([1, 6, 1])
            with col2:
                st.pyplot(message["content"])


# Prompts for user input and adds the input to the chat log
if prompt := st.chat_input("What stock advice can you give me today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display the user input
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Breaking down the input into tabular data
    processor = TabularDataProcessor(prompt=prompt, df=df)
    df2 = processor.process()
    st.write("Tabular Data:", df2)

    # Extract values from OpenAI's structured response
    tick_value = df2.loc[0, 'TICK']
    tick_value = tick_value.split(", ") if isinstance(tick_value, str) else tick_value # Ensure tick_value is a list even if there's only one ticker
    tick_value2 = df2.loc[0, 'TICK2']
    tick_value2 = tick_value2.split(", ") if isinstance(tick_value2, str) else tick_value2
    intent_value = df2.loc[0, 'INTENT']
    algos = df2.loc[0, 'ALGOS']
    algos = algos.split(", ")
    date = df2.loc[0, 'DATE']
    
    start_date = df2["start_date"]
    end_date = df2["end_date"]
    start_date = pd.to_datetime(start_date).dt.date
    start_date = start_date.iloc[0]
    end_date = pd.to_datetime(end_date).dt.date
    end_date = end_date.iloc[0]

    # Start the response as an empty string for each new prompt
    response = ""

    # If the user wants to see how a strategy is performed over a certain stock

    if intent_value in [4,5, 6, 7, 8, 9]:
        col1, col2, col3 = st.columns([1, 6, 1])
        with col2:
        
            assistant = TradingResultsAssistant()
            for algo in algos:
                for company in tick_value:
                    if algo == "RSI":
                        strategy_instance = RSI(df, company, lower_bound, upper_bound, period, 10000)
                        company_df = strategy_instance.simulate_trading(start_date, end_date)
                        
                    else:  # Handles EMA and SMA
                        strategy_instance = eval(algo)(df, company, short_span, long_span, 10000)
                        company_df = strategy_instance.apply_strategy(start_date, end_date)

                    fig, pnl_return, stock_price_growth, buy_count, sell_count = PlotUtils.trading_plot(company_df, company, algo)
                    st.session_state.messages.append({"role": "assistant", "content": fig})
                    with st.chat_message("assistant"):
                        st.pyplot(fig)
                    
                    analysis = assistant.analyze_trading_results(pnl_return, stock_price_growth, buy_count, sell_count, algo, company, start_date, end_date)
                    st.session_state.messages.append({"role": "assistant", "content": analysis})
                    with st.chat_message("assistant"):
                        st.markdown(analysis)





    elif intent_value in [2,3,11] and len(tick_value2) > 0:
        results = []
        intraday_processor = IntradayDataProcessor(df)
        intraday_data = intraday_processor.resample_to_daily(start_date, end_date)
        atr_calculator = ATRCalculator(intraday_data)
        variance_calculator = VarianceCalculator(df)


        cols = st.columns(2)
        for i, company in enumerate(tick_value2):
            col_index = i % 2  # This ensures it wraps around after the 2nd column
            
            with cols[col_index]:
                plotter = StockPlotter.plot(df, company, start_date, end_date)
                st.session_state.messages.append({"role": "assistant", "content": plotter})
                with st.chat_message("assistant"):
                    st.pyplot(plotter)

                company_high = round(intraday_data['High', company].max(), 2)
                company_low = round(intraday_data['Low', company].min(), 2)
                variance = variance_calculator.calculate_variance(company,start_date,end_date)
                std_dev = np.sqrt(variance)
                atr_value, atr_percentage = atr_calculator.calculate_atr(company)

                results.append({
                    "Company": company,
                    "Highest Price ($)": f"${company_high}",
                    "Lowest Price ($)": f"${company_low}",
                    "Variance ($²)": f"{round(variance, 2)}",
                    "Standard Deviation ($)": f"{round(std_dev, 2)}",
                    "Average True Range ($)": f"${round(atr_value, 2)}",
                    "Average True Range (%)": f"{round(atr_percentage, 2)}%"
                })
            
        results_df = pd.DataFrame(results)
        st.session_state.messages.append({"role": "assistant", "content": results_df})
        with st.chat_message("assistant"):
            st.table(results_df)

    else:
        st.write("Sorry, I am not equipped to answer that question (yet).")