# tabular_data.py

'''
Each user prompt will be fed into this, and will output tabular data

'''
import pandas as pd
from openai_client import OpenAIExtractor
from date_ranges import get_date_range_dict
from datetime import datetime
from entity_extractor import EntityExtractor

class TabularDataProcessor:
    def __init__(self, prompt, df, api_key="your_openai_api_key"):
        self.prompt = prompt
        self.df = df.copy()
        self.api_key = api_key
        self.df2 = None

    def process(self):
        # Initialize OpenAIExtractor with the API key
        openai_extractor = OpenAIExtractor(api_key=self.api_key)

        # Extract insights from the user's prompt
        self.df2 = openai_extractor.extract_insights(user_prompt=self.prompt)

        # spaCy entity extraction for organizations and dates
        entity_extractor = EntityExtractor()
        orgs_str, dates_str = entity_extractor.process_entities(self.prompt)
        self.df2["ORG"] = orgs_str
        self.df2["DATE"] = dates_str

        # Get date ranges from the original dataframe
        date_range_dict = get_date_range_dict(self.df)

        start_date = None
        end_date = None
        
        # Add start_date and end_date to df2 based on extracted dates
        for date_value in self.df2["DATE"]:
            if date_value in date_range_dict:
                start_date = datetime.strptime(date_range_dict[date_value]["start_date"], "%Y-%m-%d").date()
                end_date = datetime.strptime(date_range_dict[date_value]["end_date"], "%Y-%m-%d").date()
                self.df2["start_date"] = start_date
                self.df2["end_date"] = end_date
            else:
                # Use the range from the dataset if no specific date is found
                start_date = self.df['Datetime'].min().strftime("%Y-%m-%d")
                end_date = self.df['Datetime'].max().strftime("%Y-%m-%d")
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                self.df2["start_date"] = start_date
                self.df2["end_date"] = end_date

        # Apply algorithm indicators (RSI, EMA, SMA) to the dataframe
        self.df2['ALGOS'] = self.df2.apply(
            lambda row: ', '.join([col for col in ['RSI', 'EMA', 'SMA'] if row.get(col) == 1]), axis=1
        )

        return self.df2
