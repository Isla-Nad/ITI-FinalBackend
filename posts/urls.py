
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from posts.views import CommentViewSet,LikeViewSet,PostViewSet
from posts.views import show_comment

router = DefaultRouter()
router.register(r'comments', CommentViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'all', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('test',show_comment,name='showcomment' ),
]

# print(router.urls)
