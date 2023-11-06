from django.urls import path
from community.views import review_add, review_delete, review_edit, review_list

urlpatterns = [
    path('reviews/<int:id>', review_list, name='community.review_list'),
    path('reviews/add/', review_add, name='community.review_add'),
    path('reviews/delete/<int:id>', review_delete,
         name='community.review_delete'),
    path('reviews/edit/<int:id>', review_edit, name='community.review_edit'),
]
