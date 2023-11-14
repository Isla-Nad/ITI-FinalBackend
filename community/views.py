from django.db.models.functions import Coalesce
from django.db.models import Avg, Count
from django.forms import FloatField, IntegerField
from .serializers import CommentSerializer, LikeSerializer
from .models import Comment, Like
from accounts.models import User, UserProfile
from accounts.serializers import UserProfileSerializer, UserSerializer
from community.models import Post, Review
from community.serializers import ReviewSerializer, PostSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Avg


@api_view(['GET'])
def review_list(request, id):
    reviewed_user = get_object_or_404(User, id=id)
    reviews = Review.objects.filter(
        reviewed_user=reviewed_user).order_by('-created_at')
    overall_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    review_data = []
    for review in reviews:
        reviewing_user = review.reviewing_user
        review_serializer = ReviewSerializer(review).data
        reviewing_user_serializer = UserSerializer(reviewing_user).data
        review_data.append({
            'review': review_serializer,
            'reviewing_user': reviewing_user_serializer,
            'overall_rating': overall_rating
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

        post_id = post_data['id']
        comments = Comment.objects.filter(post=post_id).order_by('-created_at')
        comment_data = CommentSerializer(comments, many=True).data
        for comment in comment_data:
            comment_user_id = comment['user']
            comment_user = get_object_or_404(User, id=comment_user_id)
            comment_user_serializer = UserSerializer(comment_user)
            comment['user'] = comment_user_serializer.data

        post_data['comments'] = comment_data

        likes = Like.objects.filter(post=post_id)
        like_data = LikeSerializer(likes, many=True).data
        for like in like_data:
            like_user_id = like['user']
            like_user = get_object_or_404(User, id=like_user_id)
            like_user_serializer = UserSerializer(like_user)
            like['user'] = like_user_serializer.data

        likes_count = Like.objects.filter(post=post_id).count()
        post_data['likes'] = like_data
        post_data['likes_count'] = likes_count
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_add(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=user, post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def comment_edit(request, post_id, comment_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user != user:
        return Response({"detail": "You do not have permission to edit this comment."}, status=status.HTTP_403_FORBIDDEN)
    serializer = CommentSerializer(
        instance=comment, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def comment_delete(request, post_id, comment_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user != user:
        return Response({"detail": "You do not have permission to delete this comment."}, status=status.HTTP_403_FORBIDDEN)
    comment.delete()
    return Response({"detail": "Comment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_add(request, post_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    serializer = LikeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=user, post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def like_remove(request, post_id, like_id):
    user = request.user
    post = get_object_or_404(Post, id=post_id)
    like = get_object_or_404(Like, id=like_id, user=user, post=post)
    like.delete()
    return Response({"detail": "Like removed successfully."}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def top_rated_doctors(request):
    top_rated_doctors = UserProfile.objects.filter(user__is_doctor=True).annotate(
        avg_rating=Avg('user__reviews_received__rating'),
        num_reviews=Count('user__reviews_received')
    ).order_by('-avg_rating')[:5]

    serializer = UserProfileSerializer(top_rated_doctors, many=True)

    serialized_data = serializer.data
    for doctor_data, user_profile in zip(serialized_data, top_rated_doctors):
        user_data = UserSerializer(user_profile.user).data
        doctor_data['user'] = user_data
        doctor_data['avg_rating'] = user_profile.avg_rating
        doctor_data['profile_pic'] = str(user_profile.profile_picture)

    return Response(serialized_data, status=status.HTTP_200_OK)
