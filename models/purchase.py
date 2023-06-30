from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import numpy as np
from datetime import datetime
import pandas as pd
import alpaca_trade_api as tradeapi
import matplotlib.pyplot as plt

# Initialize Alpaca API
api = tradeapi.REST('PKDO0DUXPYPM7URFX3XJ', 'NA9Z45R3aeb7ptOinnz0i9VHfZiJAGWV6CFubiX4', base_url='https://paper-api.alpaca.markets')

# List of ticker symbols
tickers = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'BRK-B', 'TSLA', 'V', 'JNJ', 'WMT', 'PG', 'NVDA', 'HD', 'MA', 'DIS', 'ADBE', 'NFLX', 'PYPL', 'KO', 'INTC', 'BUD']

# List to store tickers that meet the criteria
good_tickers = []

for ticker in tickers:

    # Load the data from the CSV file
    data = pd.read_csv(f'data/raw/{ticker}_daily_2020_onwards.csv')

    # Calculate the number of days since the start of the data
    data['Date'] = pd.to_datetime(data['Date'])
    data['Days'] = (data['Date'] - data['Date'].min()).dt.days

    # Create a new DataFrame with just the Days and Close price
    data = data[['Days', 'Close']]

    # Get the last close price
    last_close_price = data['Close'].iloc[-1]

    # Split the data into training and testing data
    X_train, X_test, y_train, y_test = train_test_split(data['Days'].values.reshape(-1,1), data['Close'], test_size=0.2, random_state=0)

    # Create and train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Use the model to make predictions on the test data
    y_pred = model.predict(X_test)

    # Predict the closing price for the next day
    last_day = data['Days'].max()
    next_day = np.array([last_day + 1]).reshape(-1, 1)
    predicted_price = model.predict(next_day)

    # Print the mean squared error of the predictions and the predicted price
    print(f'Ticker: {ticker}, Mean Squared Error: {metrics.mean_squared_error(y_test, y_pred)}, Last Close Price: {last_close_price}, Predicted Price for Next Day: {predicted_price[0]}')

    # Append the ticker, prediction, last close price, and current date to the file
    with open("data/2020-onward-predictions.txt", "a") as file:
        file.write(f'Ticker: {ticker}, Date: {datetime.now().strftime("%Y-%m-%d")}, Last Close Price: {last_close_price}, Predicted Price for Next Day: {predicted_price[0]}\n')

    # Check if the MSE is under 100 and predicted price is at least 10% less than the closing price
    mse = metrics.mean_squared_error(y_test, y_pred)
    
    if mse < 100 and predicted_price < (0.9 * last_close_price):
        good_tickers.append(ticker)    
        
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

# Visualize the good tickers
plt.figure(figsize=(10,5))
plt.bar(range(len(good_tickers)), [1]*len(good_tickers), tick_label=good_tickers)
plt.title('Tickers with MSE < 100 and Predicted Price 10% less than Last Close')
plt.xlabel('Ticker')
plt.ylabel('Frequency')
plt.show()