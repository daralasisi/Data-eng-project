CREATE TABLE Company (
    symbol VARCHAR(10) PRIMARY KEY,
    company_name VARCHAR(250) NOT NULL,
    Sector VARCHAR(250) NOT NULL,
    Industry VARCHAR(250) NOT NULL
);

CREATE TABLE Dates (
    d_date DATE PRIMARY KEY,
    d_day INT NOT NULL,
    d_month INT NOT NULL,
    d_quarter INT NOT NULL,
    d_year INT NOT NULL
);


CREATE TABLE stockPrices IF NOT EXISTS (
    stock_price_id VARCHAR (50) PRIMARY KEY,
    d_date DATE,
    symbol VARCHAR (10),
    open_value DECIMAL(10,4) NOT NULL,
    high DECIMAL(10,4) NOT NULL,
    low DECIMAL(10,4) NOT NULL,
    close_value DECIMAL(10,4) NOT NULL,
    volume BIGINT NOT NULL,
    FOREIGN KEY (d_date) REFERENCES Dates (d_date),
    FOREIGN KEY (symbol) REFERENCES Company (symbol)
)