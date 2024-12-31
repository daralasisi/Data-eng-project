import os
import requests 
import pandas as pd 
import json
from datetime import datetime

api_key = os.getenv('AV_API_KEY')
symbol = 'GOOGL'

def get_data_from_api(api_key, symbol):

    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'
    headers = {'Authorisation': f'Bearer {api_key}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status() 
    data = response.json()

    dates = []

    if 'Time Series (Daily)' in data:
        time_series_data = data['Time Series (Daily)']

    for item in time_series_data:
        date_obj = datetime.strptime(item, '%Y-%m-%d')
        date = datetime.strptime(item, '%Y-%m-%d').date()
        day = date_obj.day
        month = date_obj.month
        year = date_obj.year
        quarter = (month - 1) // 3 + 1 #floor division 

        dates.append({
            'date':date,
            'day': day,
            'month': month,
            'year': year,
            'quarter':quarter
        })
    
   # print (dates, len(dates))


    return time_series_data

    ''' if 'Time Series (Daily)' in data:
        df = pd.DataFrame(data['Time Series (Daily)']).transpose()
        df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        df.index = pd.to_datetime(df.index)
        df.index.name = 'Date'
        df['Symbol'] = symbol
        print(df)
        return df
    else:
        print (f'Error fetching data for {symbol}: {data}')
        return pd.DataFrame ()
    '''


def convert_date (data):
    """
    converts the date value into date, day, month, year and quarter
    """

    dates_list = []
    for item in data:
        date_obj = datetime.strptime(item, '%Y-%m-%d')
        date = datetime.strptime(item, '%Y-%m-%d').date()
        day = date_obj.day
        month = date_obj.month
        year = date_obj.year
        quarter = (month - 1) // 3 + 1 #floor division 

        dates_list.append({
            'date':date,
            'day': day,
            'month': month,
            'year': year,
            'quarter':quarter
        })

    return dates_list

def extract_stock_prices(raw_data, symbol):
    """
    extracts stock prices from the API data and returns a list of dictionaries with data for each date
    """
    processed_data = [
        {
        'date': date,
        'symbol': symbol,
        'open': metrics['1. open'],
        'high': metrics['2. high'],
        'low': metrics['3. low'],
        'close': metrics['4. close'],
        'volume': metrics['5. volume']
        }
        for date, metrics in raw_data.items()
    ]
    
    return processed_data


data = get_data_from_api(api_key, symbol)
stock_prices = extract_stock_prices(data)
#print (data)