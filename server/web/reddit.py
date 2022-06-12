import praw
import pandas as pd
from finance import StockData
from sent_analyze import SIA
from words import STOP_WORDS
from words import TICKERS, remove_dollarsign, format_ticker
from termcolor import colored, cprint
from itertools import chain
from nltk.tokenize import wordpunct_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from finance import volume_change, price_change
from statistics import mean


reddit_secrets = pd.read_json('secrets.json')

reddit = praw.Reddit(client_id=reddit_secrets['reddit']['client_id'],
                    client_secret=reddit_secrets['reddit']['client_secret'],
                    user_agent=reddit_secrets['reddit']['user_agent'])

def submissions(subreddit, limit=500):
    most_recent_comments = reddit.subreddit(subreddit).hot(limit=limit)
    live_comments = reddit.subreddit(subreddit).stream.submissions()

    for submission in chain(most_recent_comments, live_comments):
        content = submission.title
        yield content

def comments(subreddit, limit=500):
    most_recent_comments = reddit.subreddit(subreddit).comments(limit=limit)
    live_comments = reddit.subreddit(subreddit).stream.comments()

    for submission in chain(most_recent_comments, live_comments):
        content = submission.body
        yield content

def analyze_subreddit(subreddit, queue, stock_sentiment, stock_data, limit=500):
    subreddit_submissions = submissions(subreddit, limit=limit)
    subreddit_comments = comments(subreddit, limit=limit)
    subreddit_content = chain(subreddit_submissions, subreddit_comments)

    for content in subreddit_content:
        tokenized = wordpunct_tokenize(content)
        if any([token in TICKERS and token not in STOP_WORDS for token in tokenized]):
            for word in tokenized:
                if word in TICKERS and word not in STOP_WORDS:
                    cleaned_word = format_ticker(word)
                    score = SIA().polarity_scores(content)['compound']
                    volume = volume_change(cleaned_word, '2d')
                    price = price_change(cleaned_word, '2d') * 100

                    if cleaned_word not in stock_sentiment:
                        stock_sentiment[cleaned_word] = [score]
                    else:
                        stock_sentiment[cleaned_word].append(score)

                    stock_info = StockData(ticker=cleaned_word, sentiment=round(mean(stock_sentiment[cleaned_word]), 2), volume_change=round(volume, 2), price_change=round(price, 2))
                    stock_data[cleaned_word] = stock_info
                    queue.put(stock_info)

def demo(subreddit, limit=500):
    subreddit_submissions = submissions(subreddit, limit=limit)
    subreddit_comments = comments(subreddit, limit=limit)
    subreddit_content = chain(subreddit_submissions, subreddit_comments)

    for content in subreddit_content:
        tokenized = wordpunct_tokenize(content)
        if any([token in TICKERS and token not in STOP_WORDS for token in tokenized]):
            score = SIA().polarity_scores(content)
            print(f"YES -- {colored(score['compound'], 'green')}")
            for word in tokenized:
                if word in TICKERS and word not in STOP_WORDS:
                    cleaned_word = remove_dollarsign(word)
                    print(colored(word, 'green') + f" Volume:{volume_change(cleaned_word, '7d')} Price:{price_change(cleaned_word, '7d')} \n", end="")
            print()
            print(f"content: {content}")
            print("================")
        else:
            print(f"NO: {content}")
            print("================")

# demo('wallstreetbets', 500)
