import re
from rest_framework.response import Response
from rest_framework.views import APIView
from watchlist_app.models import Movie
from watchlist_app.api.serializers import MovieSerializer
from rest_framework import status

# Create your views here.

class MovieListAV(APIView):
    
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        # Execute validations
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MovieDetailAV(APIView):
    def get(self, request, movie_id):
        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    
    def put(self, request, movie_id):
        movie = Movie.objects.get(id=movie_id)
        serializer = MovieSerializer(movie, data=request.data)
        # Execute validations
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, movie_id):
        movie = Movie.objects.get(id=movie_id)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)