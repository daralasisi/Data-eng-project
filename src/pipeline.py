import requests 
import pandas as pd 
import json

api_key = 'ZAKSXJ3OE1BQFASN'
symbol = 'GOOGL'

def get_data_from_api(api_key, symbol):

    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'
    headers = {'Authorisation': f'Bearer {api_key}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status() 
    data = response.json()
    print('Fetched data:', data['Meta Data'])
    return data

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
        return pd.DataFrame()
    '''
data = get_data_from_api(api_key, symbol)


