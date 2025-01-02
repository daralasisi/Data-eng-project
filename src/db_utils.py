import mysql.connector
import requests
import os 
import json
import datetime

# Database configuration
db_config = {
    'user': 'root',
    'password': 'rootpassword',
    'host': 'localhost',  
    'database': 'FinancialDashboard'
}

def setup_db_connection():
    print(f'setup_db_connection: Opening Connection to {db_config["database"]} with user {db_config["user"]}')
    connection = mysql.connector.connect(**db_config)

    cursor = connection.cursor()

    print ('setup_db-connection: Finished opening connection!')
    return connection, cursor


def insert_company(connection, symbol):
    """
    Inserts or updates a company record in the 'Company' table.

    """
    file_path = './data/company_information.json'
    sql = """ 
        INSERT INTO Company (symbol, company_name, sector, industry)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        company_name = VALUES(company_name)
        sector = VALUES(sector)
        industry = VALUES(industry);
    """
    print(f"insert_company: inserting{symbol}'s data...")

    try:
        # Load the JSON file
        with open(file_path, 'r') as file:
            company_data = json.load(file)

        # Extract company details
        if symbol not in company_data:
            raise KeyError(f"Symbol '{symbol}' not found in the JSON file.")
        
        company_details = company_data[symbol]

        # Insert or update company record
        with connection.cursor() as cursor:
            cursor.execute(
                sql, 
                (
                    symbol,
                    company_details.get('company_name'),
                    company_details.get('sector'),
                    company_details.get('industry')
                )
            )
            connection.commit()
            print("insert_company: Data successfully inserted or updated!")

    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except json.JSONDecodeError:
        print("Error: The file is not valid JSON.")
    except KeyError as e:
        print(f"Error: {e}")
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        connection.rollback()  # Rollback on error to avoid partial commits
    except Exception as e:
        print(f"Unexpected error: {e}")
        connection.rollback()

def insert_dates(connection, dates):
    """
    Inserts date records into the 'dates' table, updating on duplicate keys.
    """
      
    sql = """
        INSERT INTO Dates (d_date, d_day, d_month, d_quarter, d_year)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            d_day=VALUES(d_day),
            d_month=VALUES(d_month),
            d_quarter=VALUES(d_quarter),
            d_year=VALUES(d_year)
    """
    print(f"insert_dates: inserting dates...")

    try:
        # Using a context manager to handle cursor automatically
        with connection.cursor() as cursor:
            cursor.executemany(
                sql,
                [(entry['date'], entry['day'], entry['month'], entry['quarter'], entry['year']) for entry in dates],
            )
            connection.commit()
            print(f"insert_dates: {len(dates)} rows inserted!")

    except mysql.connector.Error as err:
        print(f"Database error: {err}") 
        connection.rollback()  # Rollback to avoid partial commits
        raise 

    except Exception as e:
        print(f"Unexpected error: {e}")
        connection.rollback()

def insert_stock_prices (connection, data):
    """
    Inserts stock prices into the 'stock_prices' table, updating on duplicate keys.
    """

    sql = """
        INSERT INTO stockPrices (d_date, symbol, open_value, high, low, close_value, volume)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            symbol=VALUES(symbol),
            open_value=VALUES(open_value),
            high=VALUES(high),
            low=VALUES(low)
            close_value=VALUES(close_value)
            volume=VALUES(volume)
    """
    print(f"insert_stock_prices: inserting stock prices...")

    try:
        # Using a context manager to handle cursor automatically
        with connection.cursor() as cursor:
            cursor.executemany(
                sql,
                [(entry['date'], entry['symbol'], entry['open'], entry['high'], entry['low'], entry['close'], entry['volume']) for entry in data],
            )
            connection.commit()
            print(f"insert_stock_prices: {len(data)} rows inserted!")
   
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        connection.rollback()  # Rollback to avoid partial commits

    except Exception as e:
        print(f"Unexpected error: {e}")
        connection.rollback()

