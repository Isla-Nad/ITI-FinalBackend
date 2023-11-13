from django.urls import path

from clinics.views import index, search_clinics, show, delete, create_case, create_clinic_image


urlpatterns = [
    path("", index, name='clinics.index'),
    path("show/<int:id>", show, name='clinics.show'),
    path("delete/<int:id>", delete, name='clinics.delete'),
    path("createcase", create_case, name='create_case'),
    path("createclinicimage", create_clinic_image, name='create_clinic_image'),
    path('search/clinics', search_clinics, name='clinics.search_clinics'),
]
