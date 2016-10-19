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
import logging
import os
import requests

from docopt import docopt
from dateutil import parser
from imdbpie import Imdb

from backends import TwitterReviews


def main(title):
    reviews = []

    with TwitterReviews(title) as reviews_backend:
        for review in reviews_backend.reviews:
            reviews.append(review)

    # Search Imdb
    imdb = Imdb()
    try:
        response = imdb.search_for_title(title)[0]
        title_id = response['imdb_id']
        response = imdb.get_title_reviews(title_id, max_results=10)
    except IndexError as e:
        logging.exception(str(e))
    else:
        for review in response:
            reviews.append({
                'author': review.username,
                'summary': review.summary,
                'text': review.text,
                'date': parser.parse(review.date, ignoretz=True),
                'source': 'IMDB'
            })

    # Search NYTimes
    url = "https://api.nytimes.com/svc/movies/v2/reviews/search.json"
    data = {
        'query': title,
        'api-key': os.environ.get('NY_TIMES_API_KEY')
    }
    response = requests.get(url, data)
    count = 0
    for review in response.json()['results']:
        if count > 9:
            break
        reviews.append({
            'author': review['byline'],
            'summary': review['headline'],
            'text': review['summary_short'],
            'date': parser.parse(review['date_updated'], ignoretz=True),
            'source': 'NYTimes'
        })
        count += 1

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
