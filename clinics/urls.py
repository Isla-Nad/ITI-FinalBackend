from django.urls import path

from clinics.views import index,show,delete



urlpatterns = [
    path("",index,name='clinics.index'),
    path("show/<int:id>",show,name='clinics.show'),
    path("delete/<int:id>",delete,name='clinics.delete'),
    
    
]
