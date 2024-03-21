# -*- coding: utf-8 -*-
"""“SIA_test_1209.ipynb”的副本

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UyMYR2g8_rDFxItKgT73P4TuJxiKe8Ew

# Examine the data
"""

import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

u = pd.read_csv('drivers_subred.csv')

u.columns

u.head()

u.head(10)

"""# Data pre-processing"""

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

def clean_text(text):
    # Check if the input is a string
    if not isinstance(text, str):
        return ''

    # Removing HTML tags
    text = re.sub(r'<.*?>', '', text)
    # Converting text to lowercase
    text = text.lower()
    # Removing non-ASCII characters (preserving emojis)
    text = text.encode('ascii', 'ignore').decode('ascii')
    # Tokenization
    tokens = word_tokenize(text)
    # Removing stopwords
    clean_tokens = [word for word in tokens if word not in stopwords.words('english')]
    return ' '.join(clean_tokens)

# Apply the cleaning function to the 'text' column
u['cleaned_text'] = u['selftext'].apply(clean_text)

u.head()

#exclude entries without text in selftext
u1 = u.dropna(subset=['selftext'])

u1.head()

"""# Sentiment analysis"""

from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

def get_sentiment(text):
    return sia.polarity_scores(text)

"""** SIA in nltk accepts raw text as input, as opposed to vectorized data, to preserve the sentiment. It should be able to handle emojis too. Here I did not perform vectorization. **"""

u1['neg'] = u1['selftext'].apply(lambda text: sia.polarity_scores(text)['neg'])
u1['neu'] = u1['selftext'].apply(lambda text: sia.polarity_scores(text)['neu'])
u1['pos'] = u1['selftext'].apply(lambda text: sia.polarity_scores(text)['pos'])
u1['compound'] = u1['selftext'].apply(lambda text: sia.polarity_scores(text)['compound'])

u1.head(10)

"""* Positive sentiment: compound score >= 0.05
* Neutral sentiment: compound score > -0.05 and < 0.05
* Negative sentiment: compound score <= -0.05

### Plotting
"""

import seaborn as sns
import matplotlib.pyplot as plt

sns.histplot(u1['compound'], bins=20, kde=True)
plt.xlabel('Compound Sentiment Score')
plt.ylabel('Frequency')
plt.title('Distribution of Sentiment Scores')
plt.show()