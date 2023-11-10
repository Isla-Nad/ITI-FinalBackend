from django.urls import path
from custom_admin.views import admin,ViewMedicalHistory,MedicalDetailView,MedicalUpdateView,MedicalCreateView,MedicalDeleteView


urlpatterns = [
     path('admin_home/', admin, name='admin_home'),
     path('allmedical',ViewMedicalHistory,name='allmedical'),
     path('allmedical/<int:pk>/', MedicalDetailView.as_view(), name='medical_detail'),
     path('allmedical/update/<int:pk>/', MedicalUpdateView.as_view(), name='medical_update'),
     path('medical/create/', MedicalCreateView.as_view(), name='medical_create'),
     path('medical/delete/<int:pk>/', MedicalDeleteView.as_view(), name='medical_delete'),
]




