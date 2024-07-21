import requests 
import pandas as pd 
import json

api_key = 'ZAKSXJ3OE1BQFASN'
symbol = 'GOOGL'
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'

def get_data_from_api(api_key, symbol, url):
    response = requests.get(url)
    data = response.json()

    print (data)
    return data

data = get_data_from_api(api_key, symbol, url)
