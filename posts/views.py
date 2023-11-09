from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from posts.models import Comment,Like,Post
from posts.serializers import CommentSerializer,LikeSerializer,PostSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [IsAuthenticated]

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset= Post.objects.all()
    serializer_class = PostSerializer
