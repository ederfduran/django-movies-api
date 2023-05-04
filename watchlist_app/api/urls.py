from django.urls import path, include
from watchlist_app.api.views import WatchListAV, WatchListDetailAV, StreamPlatformListAV, StreamPlatformDetailAV, ReviewList, ReviewDetail

urlpatterns = [
    path('list/', WatchListAV.as_view(), name='movie-list'),
    path('<int:movie_id>', WatchListDetailAV.as_view(), name='movie-details'),
    path('platforms/', StreamPlatformListAV.as_view(), name='stream-platform-list'),
    path('platforms/<int:platform_id>', StreamPlatformDetailAV.as_view(), name='stream-plarform-details'),
    path('reviews/', ReviewList.as_view(), name='review-list'),
    path('reviews/<int:pk>', ReviewDetail.as_view(), name='review-detail'),
]
