from django.urls import path
from appointments.views import appointment_add, appointment_book, appointment_delete, appointments_get, booked_appointments

urlpatterns = [
    path('<int:id>', appointments_get, name='appointments.appointments_get'),
    path('add/', appointment_add, name='appointments.appointments_add'),
    path('delete/<int:id>', appointment_delete,
         name='appointments.appointments_delete'),
    path('book/<int:id>', appointment_book,
         name='appointments.appointment_book'),
    path('booked/<int:id>', booked_appointments,
         name='appointments.booked_appointments'),
]
