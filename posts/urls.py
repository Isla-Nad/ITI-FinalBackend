from django.urls import path, include
from rest_framework.routers import DefaultRouter
from posts.views import CommentViewSet,LikeViewSet,PostViewSet

router = DefaultRouter()
router.register(r'comments', CommentViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'all', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

# print(router.urls)