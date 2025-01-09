import logging

from typing import Dict, List
import os
import requests
import json
from datetime import datetime, date

logger = logging.getLogger(__name__)

def get_data_from_api(api_key: str, symbol: str) -> Dict[str, Dict[str, str]]:
    """
    Fetches daily time series data from Alpha Vantage for a given symbol.
    
    Returns:
        A dictionary mapping date strings (YYYY-MM-DD) to a dictionary of stock metrics,
        for example:
        {
          '2024-12-30': {
              '1. open': '189.8000',
              '2. high': '192.5500',
              '3. low': '189.1200',
              '4. close': '191.2400',
              '5. volume': '14264659'
          },
          ...
        }
    """
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'
    # headers = {'Authorization': f'Bearer {api_key}'}
    headers = {}
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raises HTTPError if the response code is not 200-299
    
    data = response.json()
    logger.info(f"Fetching data for symbol {symbol} from Alpha Vantage.")

    if 'Time Series (Daily)' in data:
        logger.debug(f"Found {len(data['Time Series (Daily)'])} entries in 'Time Series (Daily)'.")
        return data['Time Series (Daily)']
    else:
      logger.warning(f"No 'Time Series (Daily)' found for {symbol}")        
      return {}

def convert_dates_to_info(raw_data: Dict[str, Dict[str, str]]) -> List[Dict[str, int]]:
    """
    Converts a dict mapping date-strings to different stock values into a list of dictionaries,
    each containing date, day, month, year, and quarter.
    
    Example Output:
      [
        {'date': 2024-12-30, 'day': 30, 'month': 12, 'year': 2024, 'quarter': 4},
        ...
      ]
    """
    logger.info("Converting raw data to date info.")
    dates_list: List[Dict[str, int]] = []
    
    for date_str in raw_data.keys():
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        day = date_obj.day
        month = date_obj.month
        year = date_obj.year
        quarter = (month - 1) // 3 + 1

        dates_list.append({
            'date': date_obj.date(),  #Python date object
            'day': day,
            'month': month,
            'year': year,
            'quarter': quarter
        })
    logger.info("Conversion completed!.")
    return dates_list


def extract_stock_prices(raw_data: Dict[str, Dict[str, str]], symbol: str) -> List[Dict[str, str]]:
    """
    Converts the raw time series data into a list of dictionaries describing the stock’s
    open, high, low, close, and volume for each date, plus the symbol.
    
    Example Output:
      [
        {
          'date': '2024-12-30',
          'symbol': 'GOOGL',
          'open': '189.8000',
          'high': '192.5500',
          'low': '189.1200',
          'close': '191.2400',
          'volume': '14264659'
        },
        ...
      ]
    """
    logger.info(f"Extracting stock price records for symbol {symbol}")
    processed_data: List[Dict[str, str]] = []
    
    for date_str, metrics in raw_data.items():
        processed_data.append({
            'date': date_str,           
            'symbol': symbol,
            'open': metrics.get('1. open', ''),
            'high': metrics.get('2. high', ''),
            'low': metrics.get('3. low', ''),
            'close': metrics.get('4. close', ''),
            'volume': metrics.get('5. volume', '')
        })

    logger.info(f"Stock price extraction for records for symbol {symbol} completed!")
    return processed_data

def main() -> None:
    
    api_key = os.getenv('AV_API_KEY')
    symbol = 'GOOGL'
    
    # 1. Fetch raw data from API
    raw_data = get_data_from_api(api_key, symbol)
    print(f"Fetched {len(raw_data)} days of data for {symbol}.\n")
    
    # 2. Convert dates to info
    dates_info = convert_dates_to_info(raw_data)
    print(f"Dates Info (first 2 items): {dates_info[:2]}\n")
    
    # 3. Extract stock prices
    stock_prices = extract_stock_prices(raw_data, symbol)
    print(f"Stock Prices (first 2 items): {stock_prices[:2]}\n")


if __name__ == "__main__":
    main()
