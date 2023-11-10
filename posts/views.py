from django.shortcuts import render , HttpResponse
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

def show_comment(request):
    post = Post.objects.get(id=1)
    comments = post.all_comments
    likes = post.all_likes
    context = {'post':post,'comments':comments,'likes':likes}
    return render(request,'test.html',context)