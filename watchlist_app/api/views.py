from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework import status, mixins, generics, viewsets
from rest_framework.permissions import IsAuthenticated

from watchlist_app.api.permissions import ReviewUserOrReadOnly, IsAdminOrReadOnly
from watchlist_app.models import Movie, StreamPlatform, Review
from watchlist_app.api.serializers import MovieSerializer, StreamPlatformSerializer, ReviewSerializer
from watchlist_app.api.throttling import ReviewCreateThrottle, ReviewListThrottle

#----------- SreamPlatform ------------------

class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [IsAdminOrReadOnly]


#----------- Reviews ------------------

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get("pk")
        movie = Movie.objects.get(pk=pk)
        # Check if user already submit a review
        review_user = self.request.user
        review = Review.objects.filter(movie=movie, review_user=review_user)
        if review.exists():
            raise ValidationError("You already review this movie")

        # Update Movie's reviews count and average rating
        if movie.reviews_count == 0:
            movie.avg_rating = serializer.validated_data['rating']
        else:
            movie.avg_rating = (movie.avg_rating + serializer.validated_data['rating'])/2
        movie.reviews_count += 1
        movie.save()

        serializer.save(movie=movie, review_user=review_user)


class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    throttle_classes = [ReviewListThrottle]
    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return Review.objects.filter(movie=pk)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]

# -------------- movie View ----------------

class MovieAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request):
        watch_list = Movie.objects.all()
        serializer = MovieSerializer(watch_list, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        # Execute validations
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MovieDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request, movie_id):
        try:
            watch_list = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = MovieSerializer(watch_list, context={"show_len": True})
        return Response(serializer.data)
    
    def put(self, request, movie_id):
        watch_list = Movie.objects.get(id=movie_id)
        serializer = MovieSerializer(watch_list, data=request.data)
        # Execute validations
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, movie_id):
        watch_list = Movie.objects.get(id=movie_id)
        watch_list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

