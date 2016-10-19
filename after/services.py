from backends import TwitterReviews, IMDBReviews, NYTimesReviews


def get_reviews(title):
    reviews = []
    for backend_class in (TwitterReviews, IMDBReviews, NYTimesReviews):
        with backend_class(title) as reviews_backend:
            for review in reviews_backend.reviews:
                reviews.append(review)

    return reversed(sorted(reviews, key=_get_review_date))


def _get_review_date(review):
    return review.date