import yfinance as yf
import pandas as pd
import os
import zipfile

def load_stock_symbols(file_path: str) -> list:
    """
    Load stock symbols from a CSV file.

    Args:
        file_path (str): Path to the CSV file containing the stock symbols.

    Returns:
        list: A list of stock symbols.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    # Load the CSV file
    df = pd.read_csv(file_path)
    
    # Ensure the 'ticker' column exists
    if 'ticker' not in df.columns:
        raise ValueError("The CSV file must contain a 'ticker' column.")
    
    # Return the list of tickers
    return df['ticker'].tolist()

def download_stock_data(symbols: list, start_date: str, end_date: str):
    """
    Download stock data from Yahoo Finance for each symbol and save it to individual files.

    Args:
        symbols (list): List of stock symbols to download data for.
        start_date (str): The start date for the data (format: 'YYYY-MM-DD').
        end_date (str): The end date for the data (format: 'YYYY-MM-DD').

    """
    if not os.path.exists('data/stocks'):
        os.makedirs('data/stocks')
    
    for symbol in symbols:
        try:
            print(f"Downloading data for {symbol}...")
            stock_data = yf.download(symbol, start=start_date, end=end_date)
            
            if stock_data.empty:
                print(f"No data found for {symbol}.")
                continue
            
            # Save each stock's data into a separate CSV file
            output_file = os.path.join('data/stocks', f'{symbol}.csv')
            stock_data.to_csv(output_file)
            print(f"Data for {symbol} saved to {output_file}.")
        except Exception as e:
            print(f"Failed to download data for {symbol}: {e}")

def compress_files(zip_filename: str, directory: str):
    """
    Compress all files in the specified directory into a zip file.

    Args:
        zip_filename (str): The name of the zip file to create.
        directory (str): The directory containing the files to compress.
    """
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for foldername, subfolders, filenames in os.walk(directory):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                zipf.write(file_path, os.path.relpath(file_path, directory))
    print(f"Files compressed into {zip_filename}")

def main():
    """
    Main function to execute the stock data download and compression.
    """
    # Path to the CSV file containing stock tickers
    tickers_file = os.path.join('data', 'tickers.csv')

    # Load stock symbols from the CSV file
    stock_symbols = load_stock_symbols(tickers_file)

    # Define the start and end dates for the dataset
    start_date = '2011-01-01'
    end_date = '2021-12-31'

    # Download the stock data and save to individual CSV files
    download_stock_data(stock_symbols, start_date, end_date)

    # Compress all CSV files into a zip file
    zip_filename = os.path.join('data', 'hong_kong_banking_stocks.zip')
    compress_files(zip_filename, 'data/stocks')

if __name__ == "__main__":
    main()
