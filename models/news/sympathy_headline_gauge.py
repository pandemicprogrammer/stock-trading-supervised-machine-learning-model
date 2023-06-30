import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Download the VADER lexicon
nltk.download('vader_lexicon')

# Initialize the VADER sentiment intensity analyzer
sia = SentimentIntensityAnalyzer()

# Load the news headlines
df = pd.read_csv('data/raw/news/headlines.csv')

# Define a function to calculate the sentiment score
def calculate_sentiment(title: str) -> float:
    return sia.polarity_scores(title)['compound']

# Apply the function to the news headlines
df['Sentiment'] = df['Title'].apply(calculate_sentiment)

# Convert sentiment scores to a scale of 0-100
df['Sentiment'] = ((df['Sentiment'] + 1) / 2) * 100

# Save the DataFrame with the sentiment scores to a CSV file
df.to_csv('data/raw/news/headlines_with_sentiment.csv', index=False)
