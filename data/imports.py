import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import os

# Add 'BUD' to the list of ticker symbols
tickers = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'BRK-B', 'TSLA', 'V', 'JNJ', 'WMT', 'PG', 'NVDA', 'HD', 'MA', 'DIS', 'ADBE', 'NFLX', 'PYPL', 'KO', 'INTC', 'BUD']

# Fetch data
data = yf.download(tickers, start='2020-01-01', group_by='ticker')

# Create the directory if it does not exist
os.makedirs('data/raw', exist_ok=True)

# Save the data to a CSV file in the data/raw/ directory and plot for each stock
for ticker in tickers:
    data[ticker].to_csv(f'data/raw/{ticker}_daily_2020_onwards.csv')
    data[ticker]['Close'].plot()
    plt.title(f'Daily Time Series for the {ticker} stock (2020 onwards)')
    plt.show()
