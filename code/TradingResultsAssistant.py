# TradingResultsAssistant.py

from phi.assistant import Assistant
from phi.llm.openai import OpenAIChat

class TradingResultsAssistant:
    def __init__(self):
        self.assistant = Assistant(
            llm=OpenAIChat(model="gpt-3.5-turbo"),
            description="You are an assistant designed to analyze the performance of a stock trading strategy. You are provided with the following inputs: \n\n"
                        "1. **Trading Strategy**: The strategy used (RSI, EMA, or SMA).\n"
                        "2. **Company**: The stock symbol of the company being analyzed.\n"
                        "3. **Timeframe**: The start and end date of the analysis period.\n"
                        "4. **PnL Return**: The profit and loss ratio of a user’s stock + liquid capital growth using the strategy over the given timeframe with the specific company.\n"
                        "5. **Stock Price Growth**: The percentage growth if the user simply bought the stock at the beginning of the timeframe and held it until the end.\n"
                        "6. **Buy Count**: The number of times the strategy would trigger a buy signal.\n"
                        "7. **Sell Count**: The number of times the strategy would trigger a sell signal.\n\n"
                        "Your task is to analyze the performance of the strategy using these inputs. Specifically, you should:\n\n"
                        "- Compare the **PnL return** to the **stock price growth** (just holding the stock) and assess which performed better.\n"
                        "- Discuss the effectiveness of the strategy based on the number of times it triggered buys and sells, and how this influenced the overall performance.\n"
                        "- Provide insights into whether the strategy would have been a good choice based on its performance relative to holding the stock.\n\n"
                        "Provide a concise and structured analysis of the strategy's performance, highlighting the key takeaways from the data provided.",
            instructions=[
                "Focus on comparing the PnL return of the strategy with the stock price growth over the same period. Provide clear insights about which approach was more profitable.",
                "Discuss the frequency of buy and sell signals in the context of the strategy's overall performance. Consider if too many or too few buy/sell signals had a positive or negative impact.",
                "Your analysis should highlight the strategy's effectiveness based on the provided metrics and provide actionable insights for the user.",
                "Do not mention any limitations about the analysis or ask for additional information. Simply work with the inputs given."
            ],
        )

    def analyze_trading_results(self, pnl_ratio, stock_price_growth, buy_count, sell_count, strategy, company, start_date, end_date):
        # Construct the input message for the assistant
        input_message = f"""
        Trading Strategy: {strategy}
        Company: {company}
        Timeframe: {start_date} to {end_date}
        PnL Ratio: {pnl_ratio}%
        Stock Price Growth: {stock_price_growth}%
        Number of BUY Actions: {buy_count}
        Number of SELL Actions: {sell_count}

        Analyze the performance of the trading strategy. Specifically:
        1. Compare the PnL return to the stock price growth (just holding the stock).
        2. Discuss how the frequency of buy and sell actions influenced the performance.
        3. Provide insights into whether the strategy performed well based on the provided metrics.
        4. Highlight any potential improvements or adjustments that could be made to optimize the strategy.
        """

        # Pass the message to the assistant for analysis
        response_chunks = self.assistant.run(input_message, stream=True)
        response = ""

        for chunk in response_chunks:
            response += chunk
        
        return response