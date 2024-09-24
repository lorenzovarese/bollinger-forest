
import unittest
import pandas as pd
import os

# Import the methods you are testing from the preprocess.py file
from src.data_preprocessing.preprocess import load_stock_symbols, preprocess_stock_data, calculate_wma

class TestStockDataProcessing(unittest.TestCase):

    def setUp(self):
        """
        Set up the test environment. This includes defining the paths for the mock files.
        """
        # Define the path to the mock folder
        self.mock_folder = os.path.join('tests', 'data_preprocessing', 'mock')

        # Define the path to the mock tickers CSV file
        self.tickers_file = os.path.join(self.mock_folder, 'mock_tickers.csv')

        # Define the path for the mock stock CSV file (for 0005.HK)
        self.mock_stock_file = os.path.join(self.mock_folder, 'mock_0005.HK.csv')

        # Directory where preprocessed files will be saved
        self.output_dir = os.path.join('tests', 'data_preprocessing', 'mock_preprocessed')
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def tearDown(self):
        """
        Clean up the test environment by deleting any preprocessed files.
        """
        if os.path.exists(self.output_dir):
            for file in os.listdir(self.output_dir):
                file_path = os.path.join(self.output_dir, file)
                os.remove(file_path)
            os.rmdir(self.output_dir)

    def test_preprocess_stock_data(self):
        """
        Test that stock data is preprocessed correctly:
        - 'Adj Close' column is removed.
        - WMA and dependent variables are calculated.
        """
        df = preprocess_stock_data(self.mock_stock_file)

        # Ensure 'Adj Close' is removed
        self.assertNotIn('Adj Close', df.columns)

        # Check if WMA columns are added
        self.assertIn('WMA(3)t', df.columns)
        # self.assertIn('WMA(3)t+1 - WMA(3)t', df.columns) # TODO: add this column

        # Check that all values in the WMA(3)t column are not null
        self.assertTrue(df['WMA(3)t'].notnull().all())
        
    def test_calculate_wma(self):
        """
        Test that WMA is calculated correctly based on the logic defined in the paper:
        - Formula: WMA = (Close_t + 2*Close_(t-1) + 3*Close_(t-2)) / 6
        """
        # Create mock stock data for testing
        data = {
            'Date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-06', '2023-01-07'],
            'Close': [110.0, 108.0, 107.0, 105.0, 103.0]
        }
        df = pd.DataFrame(data)
        df['Date'] = pd.to_datetime(df['Date'])

        # Expected WMA(3) based on the formula for a period of 3
        expected_wma = pd.Series([None, None, (3*107 + 2*108 + 110) / 6, (3*105 + 2*107 + 108) / 6, (3*103 + 2*105 + 107) / 6])

        # Calculate WMA using the function
        calculated_wma = calculate_wma(df, period=3)

        # Assert the WMA values are correct
        pd.testing.assert_series_equal(calculated_wma.iloc[2:], expected_wma.iloc[2:], check_names=False)

if __name__ == '__main__':
    unittest.main()
