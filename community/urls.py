from django.urls import path
from community.views import post_add, post_delete, post_edit, post_list, review_add, review_delete, review_edit, review_list

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
]
