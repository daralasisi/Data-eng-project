import mysql.connector
import requests
import os 
import json

# Database configuration
db_config = {
    'user': 'root',
    'password': 'rootpassword',
    'host': 'localhost',  # Can also use Docker container's IP
    'database': 'FinancialDashboard'
}


def setup_db_connection():
    print(f'setup_db_connection: Opening Connection to {db_config["database"]} with user {db_config["user"]}')
    connection = mysql.connector.connect(**db_config)

    cursor = connection.cursor()

    print ('setup_db-connection: Finished opening connection!')
   


def insert_company(connection, cursor, symbol, data):
    file_path = './data/company_information.json'
    sql = """ 
        INSERT INTO Company (symbol, company_name, sector, industry)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        company_name = VALUES(company_name)
        sector = VALUES(sector)
        industry = VALUES(industry);
    """
    print(f'insert_company: inserting{len(data)} rows...')

    #check that the data is a list of dictionaries 
    with open (file_path, 'r') as file:
        company_data = json.load(file)

    for company in company_data:
        cursor.execute (sql, (
                company['symbol'],
                company['company_name'],
                company['sector'],
                company['industry']
            ))
        connection.commit()
        print (f'insert_company: {len(data)} rows inserted...')

    else:
        print ('Data format error')


    # data from api and load the company's details into the db


def insert_dates(connection, cursor, data):
      # SQL statement as a variable
    sql = """
        INSERT INTO dates (d_date, d_day, d_month, d_quarter, d_year)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            day=VALUES(d_day),
            month=VALUES(d_month),
            quarter=VALUES(d_quarter),
            year=VALUES(d_year)
    """
    
    # Assuming the dates is a list of dictionaries
    if isinstance(dates, list):
        for date_entry in dates:
            # Ensure date is in the correct format
            date_str = date_entry['date']
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            
            day = date_obj.day
            month = date_obj.month
            year = date_obj.year
            quarter = (month - 1) // 3 + 1
            
            cursor.execute(sql, (
                date_str, 
                day, 
                month, 
                quarter, 
                year
            ))
    else:
        print("Data format error:", dates)  # Debug: Print data format error
    

def main():
    # Connect to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    try:
        # Create database and tables
        create_database_and_tables(cursor)

        # Fetch data from API
        data = fetch_data_from_api()

        # Insert data into the database
        insert_data_into_db(cursor, data)

        # Commit changes
        conn.commit()

    finally:
        # Close connections
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()