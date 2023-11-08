from django.urls import path
from medicalHistory.api.views import medicalhistoryapidata,MedicalhistoryDelete,MedicalhistoryUpdate
urlpatterns = [
    path('medicalhistoryapi/', medicalhistoryapidata, name='medicalhistory'),
    path('medicalhistoryapi/<int:pk>', MedicalhistoryDelete.as_view(), name='deleteapi'),
    path('medicalhistoryapi/update/<int:pk>', MedicalhistoryUpdate.as_view(), name='updateapi'),
   
]
