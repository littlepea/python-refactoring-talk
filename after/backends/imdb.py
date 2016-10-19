import logging

from dateutil import parser
from imdbpie import Imdb


class IMDBReviews(object):
    def __init__(self, movie, limit=10, language='en'):
        self.movie = movie
        self.limit = limit
        self.language = language
        self.client = Imdb()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            logging.exception(str(exc_val))

    @property
    def reviews(self):
        return [Review(result) for result in self._get_results()]

    def _get_results(self):
        try:
            response = self.client.search_for_title(self.movie)[0]
            title_id = response['imdb_id']
            response = self.client.get_title_reviews(title_id, max_results=10)
            return response
        except IndexError as e:
            logging.exception(str(e))
            return []


class Review(object):
    def __init__(self, review):
        self.review = review

    @property
    def author(self):
        return self.review.username

    @property
    def summary(self):
        return self.review.summary

    @property
    def text(self):
        return self.review.text

    @property
    def date(self):
        return parser.parse(self.review.date, ignoretz=True)

    @property
    def source(self):
        return 'IMDB'
