from rest_framework.throttling import UserRateThrottle, ScopedRateThrottle

class ReviewCreateThrottle(UserRateThrottle):
    scope = "review-create"

class ReviewListThrottle(UserRateThrottle):
    scope = "review-list"