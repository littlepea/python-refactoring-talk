# -*- coding: utf-8 -*-

import datetime
from .TwitterSearchException import TwitterSearchException
from .TwitterOrder import TwitterOrder
from .utils import py3k

try:
    from urllib.parse import parse_qs, quote_plus, unquote  # python3
except ImportError:
    from urlparse import parse_qs
    from urllib import quote_plus, unquote  # python2


class Tweet(object):
    """
    Temporary class just to demonstrate Java-like API naming for future refactoring
    """
    def __init__(self, tweet_dict):
        self.tweet = tweet_dict

    def getUserName(self):
        return self.tweet['user']['screen_name']

    def getText(self):
        return self.tweet['text']

    def getCreatedDate(self):
        return self.tweet['created_at']



class TwitterSearchResults(object):
    """
    Temporary class just to demonstrate Java-like API naming for future refactoring
    """
    def __init__(self, response):
        """ Constructor """

        self.content = response['content']
        self.meta = response['meta']
        self.tweets = response['content']['statuses']

    def getSize(self):
        return len(self.tweets)

    def getTweetByIndex(self, index):
        return Tweet(self.tweets[index])