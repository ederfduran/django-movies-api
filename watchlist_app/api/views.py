from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, mixins, generics

from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer


class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class ReviewList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

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