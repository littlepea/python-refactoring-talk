import logging
import os

import requests
from dateutil import parser

from .base import BaseReview


class NYTimesReviews(object):
    def __init__(self, movie, limit=10, language='en'):
        self.movie = movie
        self.limit = 10
        self.language = language
        self.url = 'https://api.nytimes.com/svc/movies/v2/reviews/search.json'
        self.api_key = os.environ.get('NY_TIMES_API_KEY')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            logging.exception(str(exc_val))

    @property
    def reviews(self):
        return [Review(result) for result in self._get_results()]

    def _get_results(self):
        response = requests.get(self.url, self._prepare_request_data())
        return response.json()['results']

    def _prepare_request_data(self):
        return {
            'query': self.movie,
            'api-key': self.api_key
        }


class Review(BaseReview):
    @property
    def author(self):
        return self.review['byline']

    @property
    def summary(self):
        return self.review['headline']

    @property
    def text(self):
        return self.review['summary_short']

    @property
    def date(self):
        return parser.parse(self.review['date_updated'], ignoretz=True)

    @property
    def source(self):
        return 'NYTimes'
