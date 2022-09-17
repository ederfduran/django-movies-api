from rest_framework import serializers
from watchlist_app.models import Movie

# param level validation
def name_length(value):
    if len(value) < 2:
        raise serializers.ValidationError('name is too short')
    return value
    
class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(validators=[name_length])
    description = serializers.CharField()
    active = serializers.BooleanField()
    
    def create(self, validated_data):
        return Movie.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance
    
    # File level validation
    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError('name is too short')
        return value
    
    # Object level validation
    def validate(self, data):
        if data['name'] == data['description']:
            raise serializers.ValidationError('name should be different from description')
        return data