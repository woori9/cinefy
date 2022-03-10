from rest_framework import serializers
from .models import Movie, Rating


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'


class RatingListSerializer(serializers.ModelSerializer):
    class MovieSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = ('id', 'title', 'overview', 'vote_average', 'category', 'poster_path')
    username = serializers.CharField(source='user.username', read_only=True)
    movie = MovieSerializer(read_only=True)
    class Meta:
        model = Rating
        fields = ('id', 'user', 'rank', 'content', 'username', 'movie')
        read_only_fields = ('user',)


class RatingSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Rating
        fields = '__all__'
        read_only_fields = ('user', 'movie', 'username', )
