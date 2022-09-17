from django.urls import path, include
from watchlist_app.views import movie_list, movie_details

urlpatterns = [
    path('list/', movie_list, name='movie-list'),
    path('<int:movie_id>', movie_details, name='movie-details'),
]
