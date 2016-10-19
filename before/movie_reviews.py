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


import requests
from docopt import docopt
from TwitterSearch import *
from dateutil import parser
from imdbpie import Imdb
import logging

def main(title):
    reviews = []

    # Search tweets
    ts = TwitterSearch(
        consumer_key = 'LdOuFqLzmwhT9kRelUBw',
        consumer_secret = 'orry3Mv7G6XyZlSHgKr3WIWSzJDvTsLAGcsvaWzs',
        access_token = '38117536-1rZ452ZMzNL7akQ20mf7CaBuM2JXfDEgILaBCwinE',
        access_token_secret = 'spX9fAe5VZpguNLwZIifY1g05awoIklkjXRmjfueU'
    )
    try:
        ts.connect()

        tso = TwitterSearchOrder() # create a TwitterSearchOrder object
        tso.setKeywords(['#' + title + 'Movie']) # let's define all words we would like to have a look for
        tso.setLanguage('en') # we want to see German tweets only
        tso.setIncludeEntities(False) # and don't give us all those entity information

        # add tweets to reviews list
        results = ts.getSearchResults(tso)

    except TwitterSearchException as e: # take care of all those ugly errors if there are some
        logging.exception(str(e))
        ts.cleanUp()
    else:
        for offset in range(results.getSize()):
            if offset > 9:
                break
            tweet = results.getTweetByIndex(offset)
            reviews.append({
                'author': tweet.getUserName(),
                'summary': tweet.getText(),
                'text': tweet.getText(),
                'date': parser.parse(tweet.getCreatedDate(), ignoretz=True),
                'source': 'Twitter'
            })
    finally:
        ts.disconnect()

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
        'api-key': 'ebcc7a694ae34583a43da210bae3a426'
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
    reviews.sort(cmp=_cmprev)

    # Print reviews
    for review in reviews:
        print('(%s) @%s: %s [Source: %s]' % ( review['date'].strftime('%Y-%m-%d'), review['author'], review['summary'], review['source'] ) )

def _cmprev(r1, r2):
    if r1['date']>r2['date']:
        return -1
    elif r1['date']<r2['date']:
        return 1
    else:
        return 0

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Movie Reviews 0.1')
    if '<title>' in arguments:
        main(arguments['<title>'])
    else:
        print('Error: title not specified.')
