class BaseReview(object):
    def __init__(self, review):
        self.review = review

    @property
    def author(self):
        raise NotImplementedError

    @property
    def summary(self):
        raise NotImplementedError

    @property
    def text(self):
        raise NotImplementedError

    @property
    def date(self):
        raise NotImplementedError

    @property
    def source(self):
        raise NotImplementedError

    def display(self):
        print '(%s) @%s: %s [Source: %s]' % (
            self.date.strftime('%Y-%m-%d'),
            self.author,
            self.summary,
            self.source)
