from rest_framework import serializers
from posts.models import Post
from rest_framework import validators


class PostSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    creator=serializers.CharField(max_length=100)
    title=serializers.CharField(max_length=100)
    body=serializers.CharField()
    image=serializers.ImageField()
    created_at=serializers.DateTimeField(read_only=True)
    updated_at=serializers.DateTimeField(read_only=True)

    #create
    def create(self,validated_data):
        return Post.objects.create(**validated_data) 
