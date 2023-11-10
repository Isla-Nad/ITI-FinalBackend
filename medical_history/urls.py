from django.urls import path
from medical_history.views import medical_history, medical_history_create, medical_history_delete, medical_history_edit


urlpatterns = [
    path('history', medical_history_create),
    path('history/<int:id>', medical_history),
    path('history/delete/<int:id>', medical_history_delete),
    path('history/edit/<int:id>', medical_history_edit),
]
 