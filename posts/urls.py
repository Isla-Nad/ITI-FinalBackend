from django.urls import  path
from posts.views import index
urlpatterns = [
        path('index',index),
        # path('test',test),
        # path('try1',try1),
]