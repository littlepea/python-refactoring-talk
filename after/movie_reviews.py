"""Movie Reviews.

Usage:  movie_reviews.py <title>
        movie_reviews.py (-h | --help)
        movie_reviews.py --version

Arguments:
  <title>         Movie title

Options:
  -h --help     Show this screen.
  --version     Show version.
"""
import os
import requests

from docopt import docopt
from dateutil import parser

from backends import TwitterReviews, IMDBReviews, NYTimesReviews


def main(title):
    reviews = []

    for backend_class in (TwitterReviews, IMDBReviews, NYTimesReviews):
        with backend_class(title) as reviews_backend:
            for review in reviews_backend.reviews:
                reviews.append(review)

    # Sort reviews by date
    reviews.sort(cmp=_sort_by_date_desc)

    # Display reviews
    for review in reviews:
        print('(%s) @%s: %s [Source: %s]' % (
            review['date'].strftime('%Y-%m-%d'),
            review['author'],
            review['summary'],
            review['source']))


def _sort_by_date_desc(first, second):
    first_date = first['date']
    second_date = second['date']

    if first_date > second_date:
        return -1
    elif first_date < second_date:
        return 1

    return 0


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Movie Reviews 0.1')
    if '<title>' in arguments:
        main(arguments['<title>'])
    else:
        print('Error: title not specified.')
