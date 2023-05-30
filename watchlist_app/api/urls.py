from django.urls import path, include
from rest_framework.routers import DefaultRouter
from watchlist_app.api.views import (
    MovieAV, MovieDetailAV,
    ReviewList, ReviewDetail,
    ReviewCreate, StreamPlatformVS,
    MovieGV)

router = DefaultRouter()
router.register(r"platforms", StreamPlatformVS, basename="streamplatform")

urlpatterns = [
    path('movies/', MovieAV.as_view(), name='movie-list'),
    path('movies-list/', MovieGV.as_view(), name='movie-list-2'),
    path('movies/<int:movie_id>/', MovieDetailAV.as_view(), name='movie-details'),
    path('movies/<int:pk>/reviews-create/', ReviewCreate.as_view(), name='review-create'),
    path('movies/<int:pk>/reviews/', ReviewList.as_view(), name='review-list'),
    path('reviews/<int:pk>', ReviewDetail.as_view(), name='review-detail'),
    path('', include(router.urls)),
]
