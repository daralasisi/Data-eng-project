USE FinancialDashboard;

CREATE TABLE IF NOT EXISTS Company  (
    symbol VARCHAR(10) PRIMARY KEY,
    company_name VARCHAR(250) NOT NULL,
    sector VARCHAR(250) NOT NULL,
    industry VARCHAR(250) NOT NULL
);

CREATE TABLE IF NOT EXISTS Dates (
    d_date DATE PRIMARY KEY,  
    d_day INT NOT NULL,
    d_month INT NOT NULL,
    d_quarter INT NOT NULL,
    d_year INT NOT NULL
);


CREATE TABLE IF NOT EXISTS stockPrices (
    stock_price_id INT AUTO_INCREMENT PRIMARY KEY,
    d_date DATE,
    symbol VARCHAR (10),
    open_value DECIMAL(10,4) NOT NULL,
    high DECIMAL(10,4) NOT NULL,
    low DECIMAL(10,4) NOT NULL,
    close_value DECIMAL(10,4) NOT NULL,
    volume BIGINT NOT NULL,
    FOREIGN KEY (d_date) REFERENCES Dates (d_date),
    FOREIGN KEY (symbol) REFERENCES Company (symbol)
);

INSERT INTO Company (symbol,
company_name, sector, industry) VALUES
('AAPL', 'Apple Inc.', 'Technology', 'Consumer Electronics'),
('MSFT', 'Microsoft Corporation', 'Technology', 'Software');


INSERT INTO Dates (d_date, 
d_day, d_month, d_quarter, d_year) VALUES
('2023-07-17', 17, 7, 3, 2023),
('2023-07-14', 14, 7, 3, 2023);


INSERT INTO stockPrices (d_date, 
symbol, open_value, high, low, close_value, volume) VALUES
('2023-07-17', 'AAPL', 192.7798, 194.1100, 190.6800, 191.6800, 67220100),
('2023-07-14', 'AAPL', 191.8300, 194.9700, 191.8000, 193.1600, 59052500),
('2023-07-17', 'MSFT', 276.5000, 280.0000, 274.4500, 277.9400, 23350000),
('2023-07-14', 'MSFT', 275.0000, 278.5500, 274.1200, 276.9800, 20021000);