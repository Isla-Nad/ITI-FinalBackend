from django.urls import path
from community.views import comment_add, comment_delete, comment_edit, like_add, like_remove, post_add, post_delete, post_edit, post_list, review_add, review_delete, review_edit, review_list, top_rated_doctors

urlpatterns = [
    path('reviews/<int:id>', review_list, name='community.review_list'),
    path('reviews/add/', review_add, name='community.review_add'),
    path('reviews/delete/<int:id>', review_delete,
         name='community.review_delete'),
    path('reviews/edit/<int:id>', review_edit, name='community.review_edit'),
    path('posts/', post_list, name='community.post_list'),
    path('posts/add/', post_add, name='community.post_add'),
    path('posts/delete/<int:id>', post_delete, name='community.post_delete'),
    path('posts/edit/<int:id>', post_edit, name='community.post_edit'),
    path('posts/<int:post_id>/comments/add/',
         comment_add, name='community.comment_add'),
    path('posts/<int:post_id>/comments/edit/<int:comment_id>/',
         comment_edit, name='community.comment_edit'),
    path('posts/<int:post_id>/comments/delete/<int:comment_id>/',
         comment_delete, name='community.comment_delete'),
    path('posts/<int:post_id>/likes/add/', like_add, name='community.like_add'),
    path('posts/<int:post_id>/likes/remove/<int:like_id>/',
         like_remove, name='community.like_remove'),
    path('top_rated/doctors/', top_rated_doctors,
         name='community.top_rated_doctors'),
]
