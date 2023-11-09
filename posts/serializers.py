from rest_framework import serializers
from posts.models import Comment
from posts.models import Like
from posts.models import Post

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model= Post
        fields = '__all__'
