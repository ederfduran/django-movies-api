from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class WatchListSerializer(serializers.ModelSerializer):
    reviews = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = WatchList
        fields = "__all__"

class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)

    # returns whatever is in __str__ method on WatchList
    # watchlist = serializers.StringRelatedField(many=True, read_only=True)

    # returns WatchList ids
    #watchlist = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = StreamPlatform
        fields = "__all__"