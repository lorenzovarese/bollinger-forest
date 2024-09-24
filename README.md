# Bollinger Forest 📈

### Project Overview

**Bollinger Forest** is a quantitative trading strategy project aimed at implementing the strategy described in the research paper *"Enhanced Bollinger Band Stock Quantitative Trading Strategy Based on Random Forest"* by Keyue Yan, Yimeng Wang, and Ying Li, published in **Artificial Intelligence Evolution**. The project combines **Random Forest** with **Bollinger Bands** to predict stock movements and improve trading performance for financial banking stocks in the Hong Kong stock market. The enhanced strategy seeks to generate higher returns compared to traditional Bollinger Band strategies by accurately predicting the next day’s Weighted Moving Average (WMA).

### Citation

This project implements the strategy discussed in the following publication:

- **Yan, K., Wang, Y., & Li, Y. (2022).** *Enhanced Bollinger Band Stock Quantitative Trading Strategy Based on Random Forest*. Artificial Intelligence Evolution. University of Macau, Beijing Institute of Technology-Zhuhai Campus. 

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/lorenzovarese/bollinger-forest.git
   cd bollinger-forest
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Data Preparation**:
   Place the raw stock data in the `data/raw` folder. You can also download stock data using the `src/data_preprocessing/download_data.py` script.

### Usage

1. **Preprocess stock data**:
   ```bash
   python src/data_preprocessing/preprocess.py
   ```

   This will preprocess stock data by calculating the Weighted Moving Average (WMA) and save the results to the `data/preprocessed` folder.

4. **TODO**:
   TODO


### Run Tests
   Execute the test suite to validate the functionality:
   ```bash
   python -m unittest discover tests
   ```

### License

This project is licensed under the GNU GENERAL PUBLIC LICENSE.

### Contributing

Contributions are welcome! Please submit a pull request or open an issue to suggest improvements.
