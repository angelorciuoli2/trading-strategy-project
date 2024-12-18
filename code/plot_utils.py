import matplotlib.pyplot as plt
import numpy as np

class PlotUtils:
    @staticmethod
    def xtick_labels(ax, df, num_labels=7):
        unique_dates = df['Datetime'].dt.date.unique()
        if len(unique_dates) > num_labels:
            selected_dates = unique_dates[::len(unique_dates) // num_labels]
        else:
            selected_dates = unique_dates

        formatted_dates = [date.strftime("%b %d") for date in selected_dates]
        ax.set_xticks(np.linspace(0, len(df) - 1, num=len(selected_dates)))
        ax.set_xticklabels(formatted_dates, rotation=45, fontsize=14)

    @staticmethod
    def trading_plot(df, company):
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(df.index, df[company], color='blue', label='_nolegend_')
        ax.scatter(df.index[df['Action'] == 'BUY'], df.loc[df['Action'] == 'BUY', company], color='#39FF14', label='BUY', zorder=5, s=75)
        ax.scatter(df.index[df['Action'] == 'SELL'], df.loc[df['Action'] == 'SELL', company], color='#FF073A', label='SELL', zorder=5, s=75)

        ax.set_title(f"{company}", fontsize=26, fontweight='bold')
        pnl_ratio = f"{round((df['PnL'].iloc[-1] / df['Liquid Capital'].iloc[0]) * 100, 2)}%"
        stock_price_growth = f"{round(((df[company].iloc[-1] - df[company].iloc[0]) / df[company].iloc[0]) * 100, 2)}%"
        ax.legend(title=f"PnL Return: {pnl_ratio}\nStock Price Growth: {stock_price_growth}", loc='upper left', bbox_to_anchor=(1.05, 1), prop={'size': 12}, title_fontsize=16, facecolor="#aaaaaa")

        PlotUtils.xtick_labels(ax, df)
        ax.tick_params(axis='y', which='major', labelsize=14)
        ax.set_xlabel('2024', fontsize=20, labelpad=15)
        ax.set_ylabel('Price', fontsize=20, labelpad=15)
        ax.grid(True)
        return fig

plt.ioff()
