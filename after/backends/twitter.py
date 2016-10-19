import logging
import os
from dateutil import parser

from TwitterSearch import TwitterSearch, TwitterSearchOrder, TwitterSearchException


class TwitterReviews(object):
    def __init__(self, movie, limit=10, language='en'):
        self.movie = movie
        self.limit = 10
        self.language = language
        self.client = TwitterSearch(
            consumer_key=os.environ.get('TWITTER_CONSUMER_KEY'),
            consumer_secret=os.environ.get('TWITTER_CONSUMER_SECRET'),
            access_token=os.environ.get('TWITTER_ACCESS_TOKEN'),
            access_token_secret=os.environ.get('TWITTER_TOKEN_SECRET')
        )

    def __enter__(self):
        self.client.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type == TwitterSearchException:
            logging.exception(str(exc_val))
            self.client.cleanUp()
        self.client.disconnect()

    @property
    def reviews(self):
        return Reviews(self._get_results(), limit=self.limit)

    def _prepare_request(self):
        tso = TwitterSearchOrder()
        tso.setKeywords(self._get_keywords())
        tso.setLanguage(self.language)
        tso.setIncludeEntities(False)
        return tso

    def _get_keywords(self):
        return ['#' + self.movie + 'Movie']

    def _get_results(self):
        request = self._prepare_request()
        return self.client.getSearchResults(request)


class Reviews(object):
    def __init__(self, tweets, limit=10):
        self.limit = limit
        self.tweets = tweets

    def __len__(self):
        size = self.tweets.getSize()
        return size if size < self.limit else self.limit

    def __getitem__(self, item):
        if item >= len(self):
            raise IndexError
        tweet = self.tweets.getTweetByIndex(item)
        return Review(tweet)


class Review(object):
    def __init__(self, review):
        self.review = review

    @property
    def author(self):
        return self.review.getUserName()

    @property
    def summary(self):
        return self.review.getText()

    @property
    def text(self):
        return self.review.getText()

    @property
    def date(self):
        return parser.parse(self.review.getCreatedDate(), ignoretz=True)

    @property
    def source(self):
        return 'Twitter'
