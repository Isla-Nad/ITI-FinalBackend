from django.urls import path

from clinics.views import index,show,delete,create_case



urlpatterns = [
    path("",index,name='clinics.index'),
    path("show/<int:id>",show,name='clinics.show'),
    path("delete/<int:id>",delete,name='clinics.delete'),
    path("createcase",create_case,name='create_case'),
    
]
