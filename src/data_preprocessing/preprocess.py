import pandas as pd
import os

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

def calculate_wma(df: pd.DataFrame, period: int = 3) -> pd.Series:
    """
    Calculate the Weighted Moving Average (WMA) for the given period.

    Args:
        df (pd.DataFrame): The dataframe containing stock data with a 'Close' column.
        period (int): The window for calculating WMA. Default is 3.

    Returns:
        pd.Series: A series containing the WMA values.
    """
    weights = list(range(1, period + 1))
    wma = df['Close'].rolling(window=period).apply(lambda x: sum(weights * x) / sum(weights), raw=True)
    return wma

def add_wma_columns(df: pd.DataFrame, period: int = 3) -> pd.DataFrame:
    """
    Add WMA columns to the dataframe:
    - WMA for the current day.
    - WMA for the previous 5 days.
    - The dependent variable WMA(3)t+1 - WMA(3)t.

    Args:
        df (pd.DataFrame): The dataframe containing stock data.
        period (int): The window for calculating WMA. Default is 3.

    Returns:
        pd.DataFrame: The dataframe with WMA columns added.
    """
    # Calculate the WMA for the current day and previous days
    df[f'WMA({period})t'] = calculate_wma(df, period=period)
    for i in range(1, 6):
        df[f'WMA({period})t-{i}'] = df[f'WMA({period})t'].shift(i)

    # TODO: Calculate the dependent variable WMA(3)t+1 - WMA(3)t
    # df[f'WMA({period})t+1'] = df[f'WMA({period})t'].shift(-1)
    # df[f'WMA({period})t+1 - WMA({period})t'] = df[f'WMA({period})t+1'] - df[f'WMA({period})t']

    # Drop any rows with NaN values
    df = df.dropna()

    return df

def preprocess_stock_data(file_path: str):
    """
    Preprocess stock data:
    - Remove 'Adj Close' column.
    - Add WMA columns.

    Args:
        file_path (str): Path to the CSV file of the stock data.

    Returns:
        pd.DataFrame: The preprocessed dataframe.
    """
    # Load the stock data
    df = pd.read_csv(file_path)
    
    # Remove 'Adj Close' column if it exists
    if 'Adj Close' in df.columns:
        df = df.drop(columns=['Adj Close'])

    # Add WMA columns
    df = add_wma_columns(df, period=3)

    return df

def save_preprocessed_data(df: pd.DataFrame, symbol: str, output_dir: str):
    """
    Save the preprocessed stock data to a CSV file.

    Args:
        df (pd.DataFrame): The preprocessed dataframe.
        symbol (str): The stock symbol used to name the output file.
        output_dir (str): The directory where the preprocessed file will be saved.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_file = os.path.join(output_dir, f'{symbol}_preprocessed.csv')
    df.to_csv(output_file, index=False)
    print(f"Preprocessed data for {symbol} saved to {output_file}.")

def main():
    """
    Main function to load stock symbols, preprocess their data, and save the results.
    """
    # Path to the CSV file containing stock tickers
    tickers_file = os.path.join('data', 'tickers.csv')

    # Load stock symbols from the CSV file
    stock_symbols = load_stock_symbols(tickers_file)

    # Directory where the raw stock data is stored
    stock_data_dir = os.path.join('data', 'raw')

    # Directory where the preprocessed data will be saved
    output_dir = os.path.join('data', 'preprocessed')

    # Process each stock symbol
    for symbol in stock_symbols:
        file_path = os.path.join(stock_data_dir, f'{symbol}.csv')
        try:
            print(f"Preprocessing data for {symbol}...")
            df = preprocess_stock_data(file_path)
            save_preprocessed_data(df, symbol, output_dir)
        except Exception as e:
            print(f"Failed to preprocess data for {symbol}: {e}")

if __name__ == "__main__":
    main()
