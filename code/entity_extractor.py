# entity_extractor.py

import spacy
import pandas as pd

class EntityExtractor:
    def __init__(self):
        # Load the spaCy model for entity recognition
        self.nlp = spacy.load("en_core_web_sm")
        # Define a set of terms that should never be classified as organizations
        self.invalid_orgs = {"EMA", "SMA", "RSI"}

    def extract_entities(self, prompt):
        # Initialize categories for tokens
        rows = []
        doc = self.nlp(prompt)  # Process the user's prompt
        
        # Extract and organize entities into rows
        for ent in doc.ents:
            if ent.label_ == "ORG" and ent.text not in self.invalid_orgs:
                rows.append({"ORG": ent.text, "DATE": None})
            elif ent.label_ == "DATE":
                rows.append({"ORG": None, "DATE": ent.text})

        # Return as a pandas DataFrame
        return pd.DataFrame(rows).fillna("")

    def process_entities(self, prompt):
        df_entities = self.extract_entities(prompt)

        # ORG Processing
        if not df_entities.empty:
            orgs_str = ", ".join(df_entities["ORG"].unique())
        else:
            orgs_str = None

        # DATE Processing
        if not df_entities.empty:
            dates_str = "".join(df_entities["DATE"].unique())
        else:
            dates_str = None

        # Return the processed ORG and DATE values
        return orgs_str, dates_str