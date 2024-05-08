
import streamlit as st
from streamlit.logger import get_logger
import tweepy
from dotenv import load_dotenv
import os
import logging
from streamlit_searchbox import st_searchbox
import requests

logging.basicConfig(level=logging.DEBUG)

load_dotenv()




LOGGER = get_logger(__name__)

##Fetch Stock tickers for dropdown
def fetch_symbols(query):
  api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
  if query:
    url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={query}&apikey={api_key}'
    r = requests.get(url)
    data = r.json()
    if 'bestMatches' in data:
        symbols = [item['1. symbol'] for item in data['bestMatches']]
    else:
        symbols = []
        print("No matches found")
    return symbols

##Search tweets with given query
def search_tweets(query):
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
    auth = tweepy.OAuth2BearerHandler(bearer_token)
    api = tweepy.API(auth)
    search_results = api.search_tweets(query)
    if 'SearchResults' in search_results:
      tweets = [tweet['text'] for tweet in search_results['data']]
    else:
      tweets = []
      print("No data found")
    return tweets


def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

## Autocomplete search
    selected_symbol = st_searchbox(
        fetch_symbols,
        key="stock_searchbox",
    )

##Search tweets
    if selected_symbol:
        if st.button('Search'):
          st.write(f'You selected: {selected_symbol}')
          tweets = search_tweets(selected_symbol)
          st.write('Related tweets:')
          for tweet in tweets:
              st.write(tweet)


if __name__ == "__main__":
    run()
