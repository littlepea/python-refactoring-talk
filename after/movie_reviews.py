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
from docopt import docopt

from services import get_reviews


def main(title):
    for review in get_reviews(title):
        review.display()


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Movie Reviews 0.1')
    if '<title>' in arguments:
        main(arguments['<title>'])
    else:
        print('Error: title not specified.')
