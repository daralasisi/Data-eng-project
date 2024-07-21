import pytest
from pipeline import get_data_from_api

def test_get_data_from_api ():
    #arrange
    api_key = 'ABCD'
    symbol = 'XYZ'
    url = f'https://www.testing.co/query?
function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'
    

    #act
result = get_data_from_api()

    #assert