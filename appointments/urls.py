from django.urls import path
from appointments.views import appointment_add, appointment_book, appointment_delete, appointments_get, booked_appointments, booked_appointments_doctor, appointment_book_reject, appointment_book_accept

urlpatterns = [
    path('<int:id>', appointments_get, name='appointments.appointments_get'),
    path('add/', appointment_add, name='appointments.appointments_add'),
    path('delete/<int:id>', appointment_delete,
         name='appointments.appointments_delete'),
    path('book/<int:id>', appointment_book,
         name='appointments.appointment_book'),
    path('booked/<int:id>', booked_appointments,
         name='appointments.booked_appointments'),
    path('book/reject/<int:id>', appointment_book_reject,
         name='appointments.appointment_book_reject'),
    path('book/accept/<int:id>', appointment_book_accept,
         name='appointments.appointment_book_accept'),
    path('booked/doctor/<int:id>', booked_appointments_doctor,
         name='appointments.booked_appointments_doctor'),
]
