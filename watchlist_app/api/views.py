from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework import status, mixins, generics, viewsets

from watchlist_app.api.permissions import ReviewUserOrReadOnly
from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer


class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get("pk")
        watchlist = WatchList.objects.get(pk=pk)
        # Check if user already submit a review
        review_user = self.request.user
        review = Review.objects.filter(watchlist=watchlist, review_user=review_user)
        if review.exists():
            raise ValidationError("You already review this movie")

        # Update Movie's reviews count and average rating
        if watchlist.reviews_count == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2
        watchlist.reviews_count += 1
        watchlist.save()

        serializer.save(watchlist=watchlist, review_user=review_user)


class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    def get_queryset(self):
        pk = self.kwargs.get("pk")
        return Review.objects.filter(watchlist=pk)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserOrReadOnly]

# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
# class ReviewList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# -------------- WatchList View ----------------

class WatchListAV(APIView):
    def get(self, request):
        watch_list = WatchList.objects.all()
        serializer = WatchListSerializer(watch_list, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        # Execute validations
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class WatchListDetailAV(APIView):
    def get(self, request, movie_id):
        try:
            watch_list = WatchList.objects.get(id=movie_id)
        except WatchList.DoesNotExist:
            return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = WatchListSerializer(watch_list, context={"show_len": True})
        return Response(serializer.data)
    
    def put(self, request, movie_id):
        watch_list = WatchList.objects.get(id=movie_id)
        serializer = WatchListSerializer(watch_list, data=request.data)
        # Execute validations
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, movie_id):
        watch_list = WatchList.objects.get(id=movie_id)
        watch_list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#----------- SreamPlatform ------------------

class StreamPlatformListAV(APIView):
    def get(self, request):
        stream_platforms = StreamPlatform.objects.all()
        serializer = StreamPlatformSerializer(stream_platforms, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        # Execute validations
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StreamPlatformDetailAV(APIView):
    def get(self, request, platform_id):
        try:
            stream_platform = StreamPlatform.objects.get(id=platform_id)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Stream platform not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StreamPlatformSerializer(stream_platform)
        return Response(serializer.data)

    def put(self, request, platform_id):
        stream_platform = StreamPlatform.objects.get(id=platform_id)
        serializer = StreamPlatformSerializer(stream_platform, data=request.data)
        # Execute validations
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, platform_id):
        stream_platform = StreamPlatform.objects.get(id=platform_id)
        stream_platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)