from . import etl_utils as etl
from . import db_utils as db
import logging
from . import logging_config 
import os
import sys

logger = logging.getLogger(__name__)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def main() -> None:
    api_key = os.getenv('AV_API_KEY')
    symbols = ['AAPL', 'GOOGL', 'MSFT'] 

    # get connection
    connection = db.setup_db_connection()
    
    for symbol in symbols:
        try:
            logger.info(f'Pipeline started for symbol {symbol}!')

            # fetch data...
            logger.info(f'Calling etl.get_data_from_api with: {api_key}, {symbol}!')
            raw_data = etl.get_data_from_api(api_key, symbol)
            date_info = etl.convert_dates_to_info(raw_data)
            stock_prices = etl.extract_stock_prices(raw_data, symbol)
            
            # database inserts
            logger.info(f'Inserting data for symbol {symbol} into database!')
            db.insert_company(connection, symbol)
            db.insert_dates(connection, date_info)
            db.insert_stock_prices(connection, stock_prices)
            
            logger.info(f'Pipeline completed successfully for {symbol}!')

        except Exception as e:
            # Log the exception, then continue
            logger.exception(f'An error occurred while processing {symbol}. Skipping this symbol and moving on!')
            continue

    connection.close()
    logger.info('All symbols processed, pipeline complete!')

if __name__ == "__main__":
    main()
