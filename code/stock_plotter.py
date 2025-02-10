# stock_plotter.py

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

class StockPlotter:
    @staticmethod
    def plot(df, company, start_date, end_date):
        # Filter the dataframe based on the date range
        df = df[(df['Datetime'].dt.date >= start_date) & (df['Datetime'].dt.date <= end_date)].reset_index(drop=True)
        
        # Create a new figure for the company
        fig, ax = plt.subplots(figsize=(10, 6))

        # Plot the data for the company
        df[company].plot(ax=ax, label=company)

        # 5 evenly spaced positions for xtick labels
        xticks_positions = np.linspace(0, len(df) - 1, 5).astype(int)
        ax.set_xticks(df.index[xticks_positions])
        ax.set_xticklabels([df['Datetime'].iloc[i].strftime('%b %d') for i in xticks_positions], fontsize=8)

        # Format the plot
        ax.tick_params(axis='y', labelsize=10)
        ax.tick_params(axis='x', labelsize=10)
        ax.set_ylabel('Price', fontsize=12)
        ax.set_title(f'{company}', fontsize=18, fontweight='bold')
        ax.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5, color='gray')

        # Adjust layout to ensure the plot is properly spaced
        plt.tight_layout()
        
        return fig

        # Use Streamlit to display the plot
plt.ioff()