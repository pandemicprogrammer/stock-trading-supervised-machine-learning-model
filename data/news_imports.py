from newsapi import NewsApiClient
from datetime import datetime, timedelta
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.

# Initialize a new NewsApiClient instance
newsapi = NewsApiClient(api_key=os.getenv('NEWS_API'))

# Calculate the date 7 days ago
seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%S')

tickers = ['Exxon Mobil Corp', 'Johnson & Johnson', 'Jpmorgan Chase & Co', 'Visa Inc Class a Shares', 'Eli Lilly & Co', 'Broadcom Inc', 'Procter & Gamble Co', 'Mastercard Inc A', 'Home Depot Inc', 'Merck & Co. Inc.', 'Chevron Corp', 'Pepsico Inc', 'Costco Wholesale Corp', 'Abbvie Inc', 'Coca Cola Co', 'Adobe Inc', 'Walmart Inc', 'Mcdonald S Corp', 'Cisco Systems Inc', 'Salesforce Inc', 'Pfizer Inc', 'Bank of America Corp', 'Thermo Fisher Scientific Inc', 'Accenture Plc Cl A', 'Netflix Inc', 'Abbott Laboratories', 'Linde Plc', 'Oracle Corp', 'Advanced Micro Devices', 'Comcast Corp Class A', 'Walt Disney Co', 'Texas Instruments Inc', 'Wells Fargo & Co', 'Danaher Corp', 'Verizon Communications Inc', 'Philip Morris International', 'Nextera Energy Inc', 'Raytheon Technologies Corp', 'Nike Inc Cl B', 'Honeywell International Inc', 'Intel Corp', 'Bristol Myers Squibb Co', 'Lowe S Cos Inc', 'Qualcomm Inc', 'S&p Global Inc', 'Intuit Inc', 'United Parcel Service Cl B', 'Caterpillar Inc', 'Union Pacific Corp', 'Conocophillips', 'Intl Business Machines Corp', 'Applied Materials Inc', 'Boeing Co', 'Intuitive Surgical Inc']




# Create an empty list to hold the news headlines
news_data = []

# Loop through the tickers list
for ticker in tickers:

    # Fetch top headlines
    all_articles = newsapi.get_everything(
        q=ticker,
        from_param=seven_days_ago,
        to=datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
        language='en',
        sort_by='relevancy'
    )
    
    # Append the news headlines to the list
    for article in all_articles['articles']:
        # Only append the article's title if the company's name is in the title
        if ticker in article['title']:
            news_data.append([ticker, article['title']])

# Convert the list into a DataFrame
df = pd.DataFrame(news_data, columns=['Company', 'Title'])

# Save the DataFrame to a CSV file
df.to_csv('data/raw/news/headlines.csv', index=False)
