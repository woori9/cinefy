from rest_framework import serializers
from .models import Review, Comment

class ReviewListSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)
    username = serializers.CharField(source='user.username')
    class Meta:
        model = Review
        fields = ('id', 'movie_title', 'title', 'username', 'created_at', 'like_count',)

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'user', 'review', 'content', 'username', )
        read_only_fields = ('user', 'review',)

class ReviewSerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(source='comment_set.count', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    like_count = serializers.IntegerField(source='like_users.count', read_only=True)
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user', 'like_users')
