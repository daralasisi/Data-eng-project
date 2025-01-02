import etl_utils as etl
import db_utils as db
import os

def main():
    api_key = os.getenv('AV_API_KEY')
    symbol = "GOOGL"
    
    # 1. Fetch raw data from pipeline
    raw_data = etl.get_data_from_api(api_key, symbol)
    # 2. Convert date info
    date_info = etl.convert_dates_to_info(raw_data)
    # 3. Extract stock prices
    stock_prices = etl.extract_stock_prices(raw_data, symbol)
    
    # 4. get connection
    connection = db.setup_db_connection()
    
    #Insert company details 
    db.insert_company(connection, symbol)
    # Insert date_info 
    db.insert_dates(connection, date_info)
    # Insert stock prices
    db.insert_stock_prices(connection, stock_prices)
    
    connection.close()

if __name__ == "__main__":
    main()
