import os
import openai
import json
import pandas as pd

class OpenAIExtractor:
    def __init__(self, api_key):
        
        self.api_key = "shhhh"
        os.environ['OPENAI_API_KEY'] = self.api_key  # Set API key in environment

        # Define the system prompt for structured extraction
        self.system_prompt = """
        You are an AI assistant that extracts structured insights from financial-related user inputs.
        For any given text, return a structured JSON object containing:
        - PROMPT: The original user input.
        - SUMMARY: Reword the input in a concise, structured way.
        - EMA: A value of 1, if the user input is asking to see a visualization of EMA, otherwise 0
        - SMA: A value of 1, if the user input is asking to see a visualization of SMA, otherwise 0
        - RSI: A value of 1, if the user input is asking to see a visualization of RSI, otherwise 0
        - STRAT: A value of 1, if the user input is specifically asking to see any of the three indicators (EMA, SMA, RSI) applied to a company, otherwise 0
        - TICK: Only contains a value if STRAT is 1. If STRAT is 1, TICK should contain a comma-separated list of stock ticker symbols the user is asking to apply a strategy to (e.g., 'AAPL' for Apple, 'MSFT' for Microsoft, 'TSLA' for Tesla). If more than one company is involved, provide the tickers as a list (e.g., ['AAPL', 'MSFT']).
        - TICK2: Contains a comma-separated list of stock ticker symbols for all the companies the user is mentioning (e.g., 'META' for META, 'MSFT' for Microsoft, 'TSLA' for Tesla). If more than one company is involved, provide the tickers as a list (e.g., ['AAPL', 'MSFT']).
        - INTENT: A numerical representation of the likely intent behind the user's input. If any of the three indicators (EMA, SMA, RSI) appear, INTENT will never be a 1, 2, or 3. Use the following codes:
            1. User wants advice and does not want to see any graphs or use a simulator.
            2. User wants to see just one stock graph.
            3. User wants to see more than one stock graph.
            4. User wants to simulate one strategy over one company.
            5. User wants to simulate two strategies over one company.
            6. User wants to simulate three strategies over one company.
            7. User wants to simulate one strategy over two or more companies.
            8. User wants to simulate multiple strategies over two or more companies.
            9. User wants to compare strategies or visualizations for multiple companies.
            10. User is asking for other specific financial insights or data that don't involve strategies/graphs (e.g., earnings reports, financial metrics).
            11. User is asking for specific data points about a stock. For example, they want to know, the high price and close price of a stock from a given week. Or they might want to know the range, or the variance of a stock.
            12. None of the options above accurately represent the intent of the user's input. 

        Return only a JSON object with these fields.
        """

    def extract_insights(self, user_prompt):
        """
        Calls OpenAI API to extract structured insights from the user prompt.
        Returns a Pandas DataFrame containing the structured response.
        """
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )

        # Process OpenAI API response into structured JSON
        structured_response = json.loads(response.choices[0].message.content)
        
        # Convert to DataFrame for easier processing
        df = pd.DataFrame([structured_response])
        return df