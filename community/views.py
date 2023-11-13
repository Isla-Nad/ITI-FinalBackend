from accounts.models import User
from accounts.serializers import UserSerializer
from community.models import Post, Review
from community.serializers import ReviewSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from medical_history.serializers import PostSerializer


@api_view(['GET'])
def review_list(request, id):
    reviewed_user = get_object_or_404(User, id=id)
    reviews = Review.objects.filter(
        reviewed_user=reviewed_user).order_by('-created_at')
    review_data = []
    for review in reviews:
        reviewing_user = review.reviewing_user
        review_serializer = ReviewSerializer(review).data
        reviewing_user_serializer = UserSerializer(reviewing_user).data
        review_data.append({
            'review': review_serializer,
            'reviewing_user': reviewing_user_serializer
        })
    return Response(review_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def review_add(request):
    user = request.user
    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        reviewed_user = serializer.validated_data.get('reviewed_user')
        if reviewed_user == user:
            return Response({"detail": "You cannot review yourself."}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(reviewing_user=user)
        reviewing_user_serializer = UserSerializer(
            serializer.instance.reviewing_user)
        data = {
            'review': serializer.data,
            'reviewing_user': reviewing_user_serializer.data
        }
        return Response(data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def review_delete(request, id):
    user = request.user
    review = get_object_or_404(Review, id=id)
    if review.reviewing_user != user:
        return Response({"detail": "You do not have permission to delete this review."}, status=status.HTTP_403_FORBIDDEN)
    review.delete()
    return Response({"detail": "Review deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def review_edit(request, id):
    user = request.user
    review = get_object_or_404(Review, id=id)
    if review.reviewing_user != user:
        return Response({"detail": "You do not have permission to edit this review."}, status=status.HTTP_403_FORBIDDEN)
    serializer = ReviewSerializer(
        instance=review, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        reviewing_user_serializer = UserSerializer(
            serializer.instance.reviewing_user)
        data = {
            'review': serializer.data,
            'reviewing_user': reviewing_user_serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    serializer = PostSerializer(posts, many=True)

    data_with_user = []
    for post_data in serializer.data:
        user_id = post_data['user']
        user = get_object_or_404(User, id=user_id)
        user_serializer = UserSerializer(user)
        post_data['user'] = user_serializer.data
        data_with_user.append(post_data)

    return Response(data_with_user, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_add(request):
    user = request.user
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def post_delete(request, id):
    user = request.user
    post = get_object_or_404(Post, id=id)
    if post.user != user:
        return Response({"detail": "You do not have permission to delete this post."}, status=status.HTTP_403_FORBIDDEN)
    post.delete()
    return Response({"detail": "Review deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def post_edit(request, id):
    user = request.user
    post = get_object_or_404(Post, id=id)
    if post.user != user:
        return Response({"detail": "You do not have permission to edit this post."}, status=status.HTTP_403_FORBIDDEN)
    serializer = PostSerializer(
        instance=post, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
