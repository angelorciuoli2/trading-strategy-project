# plot_utils.py

import matplotlib.pyplot as plt
import numpy as np

class PlotUtils:
    @staticmethod
    def trading_plot(df, company, strategy):

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(df.index, df[company], color='blue', label='_nolegend_')
        ax.scatter(df.index[df['Action'] == 'BUY'], df.loc[df['Action'] == 'BUY', company], color='#39FF14', label='BUY', zorder=5, s=50)
        ax.scatter(df.index[df['Action'] == 'SELL'], df.loc[df['Action'] == 'SELL', company], color='#FF073A', label='SELL', zorder=5, s=50)

        ax.set_title(f"{strategy} Simulation Results for {company}", fontsize=26, fontweight='bold')
        pnl_ratio = f"{round((df['PnL'].iloc[-1] / (df['Liquid Capital'].iloc[0] + df['Stock Value'].iloc[0])) * 100, 2)}%"
        stock_price_growth = f"{round(((df[company].iloc[-1] - df[company].iloc[0]) / df[company].iloc[0]) * 100, 2)}%"
        ax.legend(title=f"PnL Return: {pnl_ratio}\nStock Price Growth: {stock_price_growth}", loc='upper center', bbox_to_anchor=(0.5, -0.2), prop={'size': 12}, title_fontsize=16, facecolor="#aaaaaa", ncol=2)

        # Set x-tick labels directly in the plotting function
        unique_dates = df['Datetime'].dt.date.unique()
        if len(unique_dates) > 7:
            selected_dates = unique_dates[::len(unique_dates) // 7]  # Select the dates to display
        else:
            selected_dates = unique_dates

        formatted_dates = [date.strftime("%b %d") for date in selected_dates]
        xticks_positions = np.linspace(0, len(df) - 1, num=len(selected_dates)).astype(int)  # Get positions for x-ticks
        ax.set_xticks(df.index[xticks_positions])  # Set x-ticks at those positions
        ax.set_xticklabels(formatted_dates, rotation=45, fontsize=10)  # Set formatted date labels

        ax.tick_params(axis='y', which='major', labelsize=12)
        ax.set_ylabel('Price', fontsize=17, labelpad=12)
        ax.grid(True)

        buy_count = (df['Action'] == 'BUY').sum()
        sell_count = (df['Action'] == 'SELL').sum()

        return fig, pnl_ratio, stock_price_growth, buy_count, sell_count

plt.ioff()