import pytest
from unittest.mock import Mock, patch
import logging
import os
from src.pipeline import main

@pytest.fixture
def mock_connection():
    return Mock()

@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv('AV_API_KEY', 'test_key')

@pytest.fixture
def mock_date_info():
    return [
        {'date': '2024-01-05', 'day': 5, 'month': 1, 'year': 2024, 'quarter': 1},
        {'date': '2024-01-04', 'day': 4, 'month': 1, 'year': 2024, 'quarter': 1}
    ]

@pytest.fixture
def mock_stock_prices():
    return [
        {'date': '2024-01-05','symbol': 'AAPL',  'open': 185.59, 'high': 192.5500, 'low':189.1200, 'close': 191.2400, 
         'volume': 14264659},
         {'date': '2024-01-05','symbol': 'MSFT',  'open': 184.59, 'high': 197.4560, 'low':190.1700, 'close': 195.2700, 
         'volume': 17294689},
    ]

def test_main_success(mock_connection, mock_env_vars, mock_date_info, mock_stock_prices):
   with patch('src.etl_utils.get_data_from_api') as mock_get_data, \
         patch('src.etl_utils.convert_dates_to_info', return_value=mock_date_info) as mock_convert, \
         patch('src.etl_utils.extract_stock_prices', return_value=mock_stock_prices) as mock_extract, \
         patch('src.db_utils.setup_db_connection', return_value=mock_connection) as mock_setup_db_connection, \
         patch('src.db_utils.insert_company') as mock_insert_company, \
         patch('src.db_utils.insert_dates') as mock_insert_dates, \
         patch('src.db_utils.insert_stock_prices') as mock_insert_prices:
        
        
        main()

        # Verify that the database connection was set up
        mock_setup_db_connection.assert_called_once()

        # Verify `get_data_from_api` was called for each symbol
        expected_symbols = ["AAPL", "GOOGL", "MSFT"]
        actual_symbols = [args[1] for args, _ in mock_get_data.call_args_list]
        assert actual_symbols == expected_symbols
        
        # Verify data processing
        assert mock_get_data.call_count == 3
        assert mock_convert.call_count == 3
        assert mock_extract.call_count == 3
        
        # Verify database operations
        assert mock_insert_company.call_count == 3
        assert mock_insert_dates.call_count == 3
        assert mock_insert_prices.call_count == 3
        mock_connection.close.assert_called_once()

def test_main_handles_api_error(mock_connection, mock_env_vars):
    # test to verify that when an API call fails, pipeline does not crash
    with patch('src.etl_utils.get_data_from_api', side_effect=Exception("API Error")), \
         patch('src.db_utils.setup_db_connection', return_value=mock_connection):
        
        main()  # Should not raise exception but should go to the next symbol if there's an issue processing
        
        mock_connection.close.assert_called_once()

def test_db_connection_error(mock_env_vars):
    # test to verify that an exception is raised when a database connection fails.
    with patch('src.db_utils.setup_db_connection', side_effect=Exception("DB Error")):
        with pytest.raises(Exception):
            main()