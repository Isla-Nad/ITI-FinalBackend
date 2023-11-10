from django.urls import path
from custom_admin.views import admin,ViewMedicalHistory,MedicalDetailView,MedicalUpdateView,MedicalCreateView,MedicalDeleteView
from custom_admin.views import PostsListView,PostDetialView,PostCreateView,PostDeleteView

urlpatterns = [
     path('admin_home/', admin, name='admin_home'),
     path('allmedical',ViewMedicalHistory,name='allmedical'),
     path('allmedical/<int:pk>/', MedicalDetailView.as_view(), name='medical_detail'),
     path('allmedical/update/<int:pk>/', MedicalUpdateView.as_view(), name='medical_update'),
     path('medical/create/', MedicalCreateView.as_view(), name='medical_create'),
     path('medical/delete/<int:pk>/', MedicalDeleteView.as_view(), name='medical_delete'),
     path('posts', PostsListView.as_view(), name='postslist'),
     path('post/<int:pk>', PostDetialView.as_view(), name='postdetial'),
     path('createpost', PostCreateView.as_view(), name='postcreate'),
     path('deletepost/<int:pk>', PostDeleteView.as_view(), name='postdelete'),
]




