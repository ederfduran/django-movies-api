from django.urls import path, include
from rest_framework.routers import DefaultRouter
from watchlist_app.api.views import (
    WatchListAV, WatchListDetailAV, StreamPlatformListAV,
    StreamPlatformDetailAV, ReviewList, ReviewDetail,
    ReviewCreate, StreamPlatformVS)

router = DefaultRouter()
router.register(r"platforms", StreamPlatformVS, basename="streamplatform")

urlpatterns = [
    path('list/', WatchListAV.as_view(), name='movie-list'),
    path('<int:movie_id>', WatchListDetailAV.as_view(), name='movie-details'),
    path('', include(router.urls)),
    # path('platforms/', StreamPlatformListAV.as_view(), name='stream-platform-list'),
    # path('platforms/<int:platform_id>', StreamPlatformDetailAV.as_view(), name='stream-plarform-details'),
    # path('reviews/', ReviewList.as_view(), name='review-list'),
    # path('reviews/<int:pk>', ReviewDetail.as_view(), name='review-detail'),
    path('platforms/<int:pk>/reviews-create/', ReviewCreate.as_view(), name='review-create'),
    path('platforms/<int:pk>/reviews/', ReviewList.as_view(), name='review-list'),
    path('platforms/reviews/<int:pk>', ReviewDetail.as_view(), name='review-detail'),
]
