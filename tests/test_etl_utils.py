import pytest
from unittest.mock import Mock, patch
from datetime import datetime, date
import requests 
from src.etl_utils import get_data_from_api, convert_dates_to_info, extract_stock_prices

@pytest.fixture
def mock_api_response():
    return {
        "2024-01-05": {
            "1. open": "189.8000",
            "2. high": "192.5500",
            "3. low": "189.1200",
            "4. close": "191.2400",
            "5. volume": "14264659"
        },
        "2024-01-04": {
            "1. open": "188.0000",
            "2. high": "190.0000",
            "3. low": "187.0000",
            "4. close": "189.0000",
            "5. volume": "12345678"
        }
    }

def test_get_data_from_api_success(mock_api_response):
    with patch('requests.get') as mock_get:
        # setup mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "Time Series (Daily)": mock_api_response  # using the fixture above
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = get_data_from_api("fake_key", "AAPL")
        
        # verify the API was called correctly
        mock_get.assert_called_once()
        assert "alphavantage.co" in mock_get.call_args[0][0]
        assert "AAPL" in mock_get.call_args[0][0]
        assert result == mock_api_response  

def test_get_data_from_api_error():
    with patch('requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.RequestException("API Error")
        
        with pytest.raises(requests.exceptions.RequestException):
            get_data_from_api("fake_key", "AAPL")


def test_convert_dates_to_info(mock_api_response):
    result = convert_dates_to_info(mock_api_response)
    
    assert len(result) == 2
    assert isinstance(result[0]['date'], date)
    assert result[0]['day'] == 5
    assert result[0]['month'] == 1
    assert result[0]['year'] == 2024
    assert result[0]['quarter'] == 1


def test_convert_dates_to_info_empty():
    result = convert_dates_to_info({})
    assert len(result) == 0
    assert isinstance(result, list)


def test_extract_stock_prices(mock_api_response):
    symbol = "GOOGL"
    result = extract_stock_prices(mock_api_response, symbol)
    
    assert len(result) == 2
    assert result[0]['symbol'] == symbol
    assert result[0]['date'] == "2024-01-05"
    assert result[0]['open'] == "189.8000"
    assert result[0]['high'] == "192.5500"
    assert result[0]['low'] == "189.1200"
    assert result[0]['close'] == "191.2400"
    assert result[0]['volume'] == "14264659"

def test_extract_stock_prices_missing_data(mock_api_response):
    # removed some fields to test how it handles missing data
    del mock_api_response["2024-01-05"]["1. open"]
    
    result = extract_stock_prices(mock_api_response, "GOOGL")
    assert result[0]['open'] == ''  # should handle missing data gracefully, fingers crossed (yes it does! :)


def test_extract_stock_prices_empty():
    result = extract_stock_prices({}, "GOOGL")
    assert len(result) == 0
    assert isinstance(result, list)
