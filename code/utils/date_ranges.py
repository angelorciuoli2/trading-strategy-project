# date_ranges.py
import pandas as pd


def get_date_range_dict(df):
    # Ensure that the Datetime column is in datetime format
    df['Datetime'] = pd.to_datetime(df['Datetime'])

    # Date range dictionary definition
    date_range_dict = {
        'the past week': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[4].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'last week': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[4].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'past week': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[4].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'the previous week': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[4].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'previous week': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[4].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'the week before': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[10].strftime('%Y-%m-%d'),
            'end_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[5].strftime('%Y-%m-%d')
        },
        'last 7 days': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[4].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'this past week': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[4].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'the last week': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[4].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'this week': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[4].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'last 5 days': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[4].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'past 2 weeks': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[9].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'past two weeks': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[9].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'the past two weeks': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[9].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'previous 2 weeks': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[9].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'last couple weeks': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[9].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        '2 weeks ago': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[9].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'last 2 weeks': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[9].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'this past 2 weeks': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[9].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'the past 2 weeks': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[9].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'the last 2 weeks': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[9].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'the last two weeks': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[9].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
                },
        'past 3 weeks': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[14].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'past three weeks': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[14].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'the past three weeks': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[14].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'previous 3 weeks': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[14].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        '3 weeks ago': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[14].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'last 3 weeks': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[14].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'this past 3 weeks': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[14].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'the past 3 weeks': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[14].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'the last 3 weeks': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[14].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'the last three weeks': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[14].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'previous month': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[19].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'past month': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[19].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'last month': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[19].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'this past month': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[19].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'the past month': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[19].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'the last month': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[19].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'last 30 days': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[19].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        '30 days ago': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[19].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'this month': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[19].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'past 6 weeks': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[29].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'past six weeks': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[29].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'the past six weeks': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[29].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'previous 6 weeks': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[29].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        '6 weeks ago': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[29].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'last 6 weeks': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[29].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'this past 6 weeks': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[29].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'the past 6 weeks': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[29].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'the last 6 weeks': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[29].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'previous two months': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[39].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'past 2 months': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[39].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'last 2 months': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[39].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'the past two months': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[39].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'the past 2 months': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[39].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'the last two months': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[39].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
        'last 60 days': {
            'start_date': sorted(df['Datetime'].dt.date.unique(), reverse=True)[39].strftime('%Y-%m-%d'),
            'end_date': (df['Datetime'].iloc[-1].date()).strftime('%Y-%m-%d')
        },
    }
    
    return date_range_dict