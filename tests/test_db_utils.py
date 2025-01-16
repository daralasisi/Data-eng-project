import pytest
from unittest.mock import patch, MagicMock, mock_open
import json
import mysql.connector
from src.db_utils import setup_db_connection,insert_company, insert_dates, insert_stock_prices

@patch("src.db_utils.mysql.connector.connect")
def test_setup_db_connection(mock_connect):
    """
    test for setup_db_connection() to ensure it calls mysql.connector.connect
    with the correct parameters and returns a connection object.
    """
    # mock connection object
    mock_connection = MagicMock()
    mock_connect.return_value = mock_connection

    conn = setup_db_connection()
    
    # ensure mysql.connector.connect was called with the db_config
    mock_connect.assert_called_once()
    # the setup_db_connection function should return a mock_connection
    assert conn == mock_connection


@patch("builtins.open", new_callable=mock_open, read_data=json.dumps({
    "AAPL": {
        "company_name": "Apple Inc.",
        "sector": "Technology",
        "industry": "Consumer Electronics"
    }
}))
@patch("src.db_utils.mysql.connector.connect")
def test_insert_company(mock_connect, mock_file):
    """
    test for insert_company() to verify that company_information.json is read,
    SQL is executed, and db commit logic.
    """
    # setup a mock connection & cursor
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
    mock_connect.return_value = mock_connection

    # reuse the existing connection from setup_db_connection()
    conn = setup_db_connection()

    symbol = "AAPL"
    insert_company(conn, symbol)

    # check that file was opened once
    mock_file.assert_called_once_with('../data/company_information.json', 'r')

    # cursor.execute should be called with the correct SQL statement and params
    # check the call arguments for the symbol, name, sector, industry
    expected_sql = """ 
        INSERT INTO Company (symbol, company_name, sector, industry)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        company_name = VALUES(company_name),
        sector = VALUES(sector),
        industry = VALUES(industry);
    """.strip()

    mock_cursor.execute.assert_called_once()
    actual_sql, actual_params = mock_cursor.execute.call_args[0]
    assert expected_sql in actual_sql
    assert actual_params == (
        "AAPL",
        "Apple Inc.",
        "Technology",
        "Consumer Electronics"
    )

    # ensure commit is called
    mock_connection.commit.assert_called_once()


@patch("src.db_utils.mysql.connector.connect")
def test_insert_dates(mock_connect):
    """
    test for the insert_dates function to ensure it executes the SQL insert and commits.
    """
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
    mock_connect.return_value = mock_connection

    conn = setup_db_connection()

    # sample date data
    dates_list = [
        {'date': '2024-01-01', 'day': 1, 'month': 1, 'year': 2024, 'quarter': 1},
        {'date': '2024-01-02', 'day': 2, 'month': 1, 'year': 2024, 'quarter': 1}
    ]

    insert_dates(conn, dates_list)

    # to ensure executemany was called with correct parameters
    expected_sql = """
        INSERT INTO Dates (d_date, d_day, d_month, d_quarter, d_year)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            d_day=VALUES(d_day),
            d_month=VALUES(d_month),
            d_quarter=VALUES(d_quarter),
            d_year=VALUES(d_year)
    """.strip()

    mock_cursor.executemany.assert_called_once()
    actual_sql, actual_params = mock_cursor.executemany.call_args[0]
    assert expected_sql in actual_sql

    # Check the data passed in executemany
    assert actual_params == [
        ('2024-01-01', 1, 1, 1, 2024),
        ('2024-01-02', 2, 1, 1, 2024)
    ]

    # Ensure commit is called
    mock_connection.commit.assert_called_once()


@patch("src.db_utils.mysql.connector.connect")
def test_insert_stock_prices(mock_connect):
    """
    test the insert_stock_prices fubction to ensure it executes the SQL insert and commits.
    """
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
    mock_connect.return_value = mock_connection

    conn = setup_db_connection()

    # sample stock price data
    stock_data = [
        {'date': '2024-01-05', 'symbol': 'AAPL', 'open': '185.59', 'high': '189.55', 'low': '184.68', 'close': '188.50', 'volume': '123456'},
        {'date': '2024-01-05', 'symbol': 'MSFT', 'open': '280.59', 'high': '285.55', 'low': '279.68', 'close': '283.50', 'volume': '98765'}
    ]

    insert_stock_prices(conn, stock_data)

    # to ensure executemany was called with correct parameters
    expected_sql = """
        INSERT INTO stockPrices (d_date, symbol, open_value, high, low, close_value, volume)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            symbol=VALUES(symbol),
            open_value=VALUES(open_value),
            high=VALUES(high),
            low=VALUES(low),
            close_value=VALUES(close_value),
            volume=VALUES(volume)
    """.strip()

    mock_cursor.executemany.assert_called_once()
    actual_sql, actual_params = mock_cursor.executemany.call_args[0]
    assert expected_sql in actual_sql

    # check the data passed
    assert actual_params == [
        ('2024-01-05', 'AAPL', '185.59', '189.55', '184.68', '188.50', '123456'),
        ('2024-01-05', 'MSFT', '280.59', '285.55', '279.68', '283.50', '98765')
    ]

    # to ensure commit is called
    mock_connection.commit.assert_called_once()