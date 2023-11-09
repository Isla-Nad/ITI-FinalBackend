from django.urls import  path
from posts.views import index, post_resource
urlpatterns = [
        path('index',index),
        path('<int:id>', post_resource)
]