-- Create the table for bitcoin - the table schema is the same
-- for each coin, but has different values for the columns
CREATE TABLE bitcoin (
	Unix_Timestamp INT,
	Entry_Date TIMESTAMP WITH TIME ZONE,
	Symbol VARCHAR(10),
	Open_Price DECIMAL,
	High_Price DECIMAL,
	Low_Price DECIMAL,
	Close_Price DECIMAL,
	Coin_Volume DECIMAL,
	PRIMARY KEY (Unix_Timestamp, Symbol)
);

-- Create the table for ethereum - the table schema is the same
-- for each coin, but has different values for the columns
CREATE TABLE ethereum (
	Unix_Timestamp INT,
	Entry_Date TIMESTAMP WITH TIME ZONE,
	Symbol VARCHAR(10),
	Open_Price DECIMAL,
	High_Price DECIMAL,
	Low_Price DECIMAL,
	Close_Price DECIMAL,
	Coin_Volume DECIMAL,
	PRIMARY KEY (Unix_Timestamp, Symbol)
);
