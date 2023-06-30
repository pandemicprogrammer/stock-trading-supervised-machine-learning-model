import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import os

# Add 'BUD' to the list of ticker symbols
tickers = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'BRK-B', 'TSLA', 'V', 'JNJ', 'WMT', 'PG', 'NVDA', 'HD', 'MA', 'DIS', 'ADBE', 'NFLX', 'PYPL', 'KO', 'INTC', 'BUD', 'PEP', 'IBM', 'MCD', 'NKE', 'XOM', 'JNJ', 'JPM', 'V', 'LLY', 'AVGO', 'PG', 'MA', 'HD', 'MRK', 'CVX', 'PEP', 'COST', 'ABBV', 'KO', 'ADBE', 'WMT', 'MCD', 'CSCO', 'CRM', 'PFE', 'BAC', 'TMO', 'ACN', 'NFLX', 'ABT', 'LIN', 'ORCL', 'AMD', 'CMCSA', 'DIS', 'TXN', 'WFC', 'DHR', 'VZ', 'PM', 'NEE', 'RTX', 'NKE', 'HON', 'INTC', 'BMY', 'LOW', 'QCOM', 'SPGI', 'INTU', 'UPS', 'CAT', 'UNP', 'COP', 'IBM', 'AMAT', 'BA', 'ISRG', 'AMGN', 'GE', 'MDT', 'T', 'SBUX', 'PLD', 'NOW', 'MS', 'DE', 'GS', 'ELV', 'LMT', 'BLK', 'AXP', 'SYK', 'MDLZ', 'BKNG', 'TJX', 'ADI', 'GILD', 'MMC', 'C', 'ADP', 'AMT', 'VRTX', 'CVS', 'LRCX', 'SCHW', 'CI', 'MO', 'ZTS', 'ETN', 'TMUS', 'CB', 'PGR', 'PANW', 'BSX', 'FI', 'REGN', 'SO', 'BDX', 'PYPL', 'EQIX', 'AON', 'MU', 'ITW', 'CSX', 'SLB', 'DUK', 'EOG', 'KLAC', 'CME', 'SNPS', 'NOC', 'APD', 'CL', 'WBA']

# Fetch data
data = yf.download(tickers, start='2020-01-01', group_by='ticker')

# Create the directory if it does not exist
os.makedirs('data/raw', exist_ok=True)

# Save the data to a CSV file in the data/raw/ directory and plot for each stock
for ticker in tickers:
    data[ticker].to_csv(f'data/raw/ticker_histories/{ticker}_daily_2020_onwards.csv')
    data[ticker]['Close'].plot()
    # plt.title(f'Daily Time Series for the {ticker} stock (2020 onwards)')
    # plt.show()
