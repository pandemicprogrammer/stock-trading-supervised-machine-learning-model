from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import numpy as np
from datetime import datetime
import pandas as pd
import alpaca_trade_api as tradeapi
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.

try:
    # Initialize Alpaca API
    api = tradeapi.REST(os.getenv('ALPACA_KEY'), os.getenv('ALPACA_SECRET'), base_url='https://paper-api.alpaca.markets')
except Exception as e:
    print(f"Error initializing Alpaca API: {e}")
    exit(1)

# List of ticker symbols
tickers = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'BRK-B', 'TSLA', 'V', 'JNJ', 'WMT', 'PG', 'NVDA', 'HD', 'MA', 'DIS', 'ADBE', 'NFLX', 'PYPL', 'KO', 'INTC', 'BUD', 'PEP', 'IBM', 'MCD', 'NKE', 'XOM', 'JNJ', 'JPM', 'V', 'LLY', 'AVGO', 'PG', 'MA', 'HD', 'MRK', 'CVX', 'PEP', 'COST', 'ABBV', 'KO', 'ADBE', 'WMT', 'MCD', 'CSCO', 'CRM', 'PFE', 'BAC', 'TMO', 'ACN', 'NFLX', 'ABT', 'LIN', 'ORCL', 'AMD', 'CMCSA', 'DIS', 'TXN', 'WFC', 'DHR', 'VZ', 'PM', 'NEE', 'RTX', 'NKE', 'HON', 'INTC', 'BMY', 'LOW', 'QCOM', 'SPGI', 'INTU', 'UPS', 'CAT', 'UNP', 'COP', 'IBM', 'AMAT', 'BA', 'ISRG', 'AMGN', 'GE', 'MDT', 'T', 'SBUX', 'PLD', 'NOW', 'MS', 'DE', 'GS', 'ELV', 'LMT', 'BLK', 'AXP', 'SYK', 'MDLZ', 'BKNG', 'TJX', 'ADI', 'GILD', 'MMC', 'C', 'ADP', 'AMT', 'VRTX', 'CVS', 'LRCX', 'SCHW', 'CI', 'MO', 'ZTS', 'ETN', 'TMUS']

# List to store tickers that meet the criteria
good_tickers = []

for ticker in tickers:
    
    filename = f'data/raw/ticker_histories/{ticker}_daily_2020_onwards.csv'

    try:
        # Load the data from the CSV file
        data = pd.read_csv(filename)
    except FileNotFoundError:
        print(f"File not found: {filename}")
        continue
    except Exception as e:
        print(f"Error loading file {filename}: {e}")
        continue

    # Calculate the number of days since the start of the data
    data['Date'] = pd.to_datetime(data['Date'])
    data['Days'] = (data['Date'] - data['Date'].min()).dt.days

    # Create a new DataFrame with just the Days and Close price
    data = data[['Days', 'Close']]

    # Get the last close price
    last_close_price = data['Close'].iloc[-1]

    try:
        # Split the data into training and testing data
        X_train, X_test, y_train, y_test = train_test_split(data['Days'].values.reshape(-1,1), data['Close'], test_size=0.2, random_state=0)

        # Create and train the model
        model = LinearRegression()
        model.fit(X_train, y_train)
    except Exception as e:
        print(f"Error creating or training model for {ticker}: {e}")
        continue

    try:
        # Use the model to make predictions on the test data
        y_pred = model.predict(X_test)

        # Predict the closing price for the next day
        last_day = data['Days'].max()
        next_day = np.array([last_day + 1]).reshape(-1, 1)
        predicted_price = model.predict(next_day)
    except Exception as e:
        print(f"Error predicting price for {ticker}: {e}")
        continue

    # Print the mean squared error of the predictions and the predicted price
    print(f'Ticker: {ticker}, Mean Squared Error: {metrics.mean_squared_error(y_test, y_pred)}, Last Close Price: {last_close_price}, Predicted Price for Next Day: {predicted_price[0]}')

    # Append the ticker, prediction, last close price, and current date to the file
    with open("data/2020-onward-predictions.txt", "a") as file:
        file.write(f'Ticker: {ticker}, Date: {datetime.now().strftime("%Y-%m-%d")}, Last Close Price: {last_close_price}, Predicted Price for Next Day: {predicted_price[0]}\n')
    
    # Delete the file
    try:
        os.remove(filename)
    except Exception as e:
        print(f"Error deleting file {filename}: {e}")

    # Check if the MSE is under 100 and predicted price is at least 10% less than the closing price
    mse = metrics.mean_squared_error(y_test, y_pred)
    
    if mse < 100 and predicted_price < (0.9 * last_close_price):
        good_tickers.append(ticker)    
        
        try:
            if mse < 500 and predicted_price < (0.9 * last_close_price):
                # Submit a market order to buy 1 share of the stock
                order = api.submit_order(
                    symbol=ticker,
                    qty=1,
                    side='buy',
                    type='market',
                    time_in_force='gtc'
                )
                print(f"Submitted an order to buy 1 share of {ticker} at market price. Order ID: {order.id}")
        except Exception as e:
            print(f"Error submitting order for {ticker}: {e}")

# Visualize the good tickers
try:
    plt.figure(figsize=(10,5))
    plt.bar(range(len(good_tickers)), [1]*len(good_tickers), tick_label=good_tickers)
    plt.title('Tickers with MSE < 100 and Predicted Price 10% less than Last Close')
    plt.xlabel('Ticker')
    plt.ylabel('Frequency')
    plt.show()
except Exception as e:
    print(f"Error generating plot: {e}")
