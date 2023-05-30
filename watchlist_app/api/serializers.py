from rest_framework import serializers
from watchlist_app.models import Movie, StreamPlatform, Review

class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        exclude = ("movie",)


class MovieSerializer(serializers.ModelSerializer):
    #reviews = serializers.StringRelatedField(many=True, read_only=True)
    platform = serializers.CharField(source="platform.name")
    class Meta:
        model = Movie
        fields = "__all__"

class StreamPlatformSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True, read_only=True)
    class Meta:
        model = StreamPlatform
        fields = "__all__"