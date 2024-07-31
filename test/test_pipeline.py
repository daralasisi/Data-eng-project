
import pytest
import sys
sys.path.insert(0, '../src')
from unittest.mock import Mock, patch
import pandas as pd
from pipeline import get_data_from_api


# Test function for fetch_stock_data
@patch('requests.get')
def test_get_data_from_api(mock_get):
    # Mock response data
    mock_response_data = {
        "Time Series (Daily)": {
            "2023-07-17": {
                "1. open": "192.7798",
                "2. high": "194.1100",
                "3. low": "190.6800",
                "4. close": "191.6800",
                "5. volume": "67220100"
            },
            "2023-07-14": {
                "1. open": "191.8300",
                "2. high": "194.9700",
                "3. low": "191.8000",
                "4. close": "193.1600",
                "5. volume": "59052500"
            }
        }
    }

    # Mock the JSON response
    mock_get.return_value.json.return_value = mock_response_data

    # Expected DataFrame
    expected_data = '../data/small_data.csv'
    expected_df = pd.read_csv(expected_data, index_col='Date', dtype=object, parse_dates=True)
    expected_df.index = pd.to_datetime(expected_df.index)
    expected_df = expected_df.sort_index()

    # Call the function
    actual_df = get_data_from_api('dummy_api_key', 'AAPL')
    actual_df = actual_df.sort_index()

    # Compare the DataFrame
    pd.testing.assert_frame_equal(actual_df, expected_df)

if __name__ == '__main__':
    pytest.main()