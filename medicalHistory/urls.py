from django.urls import path
from medicalHistory.api.views import medicalhistoryapidata
urlpatterns = [
    path('medicalhistoryapi/', medicalhistoryapidata, name='medicalhistory'),
   
]
